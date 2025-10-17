from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import chromadb
from chromadb.utils import embedding_functions
import requests
import os
import uuid

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
embed_fn = embedding_functions.DefaultEmbeddingFunction()
faq_collection = chroma_client.get_or_create_collection(
    name="faq",
    embedding_function=embed_fn
)

# Load FAQ exact matches
faq_path = "faq.txt"
faq_dict = {}
faq_variants = {}  # For small variations
if os.path.exists(faq_path):
    with open(faq_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if ":" in line:
                q, a = line.split(":", 1)
                faq_dict[q.strip()] = a.strip()
                # Add lowercase variant to handle slight differences
                faq_variants[q.strip().lower()] = a.strip()

# In-memory session memory: {session_id: [{"user":..,"bot":..},...]}
session_memory = {}

class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None

def call_ollama(prompt: str, model: str = OLLAMA_MODEL) -> str:
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        r = requests.post(OLLAMA_URL, json=payload, timeout=120)
        r.raise_for_status()
        j = r.json()

        if isinstance(j, dict):
            if "response" in j:
                return j["response"]
            if "generation" in j and isinstance(j["generation"], dict) and "content" in j["generation"]:
                return j["generation"]["content"]
            if "generations" in j and isinstance(j["generations"], list) and len(j["generations"]) > 0:
                gen = j["generations"][0]
                if isinstance(gen, dict):
                    return gen.get("text") or gen.get("content") or str(gen)
            if "message" in j and isinstance(j["message"], dict) and "content" in j["message"]:
                return j["message"]["content"]

        return str(j)
    except Exception as e:
        return f"Ollama error: {e}"

@app.post("/chat")
async def chat(req: ChatRequest):
    user_q = req.question.strip()
    if not user_q:
        return {"answer": "Please ask a question."}

    # Generate session_id if not provided
    session_id = req.session_id or str(uuid.uuid4())
    if session_id not in session_memory:
        session_memory[session_id] = []

    # 1️⃣ Check exact match first (case-insensitive)
    faq_answer = faq_dict.get(user_q) or faq_variants.get(user_q.lower())
    if faq_answer:
        reply_text = faq_answer
    # 2️⃣ Check for summarization request
    elif "summarize" in user_q.lower():
        history = session_memory.get(session_id, [])
        if history:
            convo_text = "\n".join([f"User: {m['user']}\nBot: {m['bot']}" for m in history])
            prompt = f"Summarize the following conversation:\n{convo_text}\nSummary:"
            reply_text = call_ollama(prompt)
        else:
            reply_text = "No conversation history to summarize."
    # 3️⃣ RAG fallback
    else:
        try:
            results = faq_collection.query(
                query_texts=[user_q],
                n_results=1,
                include=["documents", "distances"]
            )
        except Exception:
            results = None

        top_doc = ""
        relevance_threshold = 0.6

        if results and results.get("documents") and results["documents"][0]:
            doc = results["documents"][0][0]
            distance = results["distances"][0][0] if results.get("distances") else 1.0
            if distance <= (1.0 - relevance_threshold):
                top_doc = doc

        if top_doc:
            prompt = f"Use the context below to answer.\n\nContext:\n{top_doc}\n\nQ: {user_q}\nA:"
            reply_text = call_ollama(prompt)
        else:
            reply_text = "I'm not able to answer this question. Escalating to human support."

    # Store in session memory
    session_memory[session_id].append({"user": user_q, "bot": reply_text})
    # Keep only last 5 exchanges
    session_memory[session_id] = session_memory[session_id][-5:]

    return {"answer": reply_text, "session_id": session_id}
