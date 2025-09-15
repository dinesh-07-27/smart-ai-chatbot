from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions
import requests
import os

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

chroma_client = chromadb.PersistentClient(path="./chroma_db")
embed_fn = embedding_functions.DefaultEmbeddingFunction()
faq_collection = chroma_client.get_or_create_collection(
    name="faq",
    embedding_function=embed_fn
)

class ChatRequest(BaseModel):
    question: str

def call_ollama(prompt: str, model: str = OLLAMA_MODEL) -> str:
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False   # ✅ Force single JSON response instead of stream
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

    try:
        results = faq_collection.query(
            query_texts=[user_q],
            n_results=1,
            include=["documents"]
        )
    except Exception:
        results = None

    context = ""
    if results and results.get("documents") and results["documents"][0]:
        top_doc = results["documents"][0][0]
        if top_doc and top_doc.strip():
            context = top_doc

    if context:
        prompt = f"Use the context below to answer.\n\nContext:\n{context}\n\nQ: {user_q}\nA:"
    else:
        prompt = f"Q: {user_q}\nA:"

    reply_text = call_ollama(prompt)
    return {"answer": reply_text}
