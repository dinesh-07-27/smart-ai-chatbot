
# 🤖 Smart AI Customer Support Chatbot

A full-stack **AI-powered customer support chatbot** built with:
- **FastAPI** (backend, API endpoints)
- **React** (frontend, chat UI)
- **Ollama + Llama2** (LLM responses)
- **ChromaDB** (for Retrieval-Augmented Generation - RAG, FAQ retrieval)
- **SQLite** (chat history storage)

This project demonstrates how modern **Generative AI** can be integrated with traditional databases and APIs to provide **real-time, context-aware customer support**.

---

## 🚀 Features
- Natural conversation powered by **Llama2 via Ollama**
- **RAG integration**: retrieves relevant answers from `faq.txt`
- **FastAPI backend** with REST endpoints (`/chat`)
- **React frontend** with a simple, responsive chat interface
- Cross-origin support with CORS
- Stores chat history in SQLite
- Modular design (easily extendable to more data sources)

---

## 🛠️ Tech Stack
- **Frontend**: React (JavaScript, Fetch API)
- **Backend**: FastAPI (Python)
- **Database**: SQLite + ChromaDB (vector database)
- **AI Models**: Llama2 via [Ollama](https://ollama.ai)
- **Others**: Docker (optional for deployment)

---

## 📂 Project Structure
