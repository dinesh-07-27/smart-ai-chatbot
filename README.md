# 🤖 Smart AI Customer Support Chatbot

A full-stack AI-powered customer support chatbot using **FastAPI**, **React**, and **Llama2 (via Ollama)**.  
It uses **RAG (Retrieval-Augmented Generation)** with FAQ retrieval to give context-aware answers.

---

## 🚀 Key Features
- Answers based on your FAQ set using RAG  
- Natural responses via Llama2  
- REST backend with FastAPI (`/chat` endpoint)  
- React frontend UI for interactive chat  
- SQLite + ChromaDB for storing knowledge and chat data  

---

## 🛠 Tech Stack
- **Backend**: FastAPI (Python)  
- **Frontend**: React (JavaScript)  
- **Knowledge store**: ChromaDB and `faq.txt`  
- **Model**: Llama2 via Ollama  
- **Database**: SQLite  

---

## ⚡ How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/dinesh-07-27/smart-ai-chatbot.git
cd smart-ai-chatbot

# 2. Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python ingest.py   # load FAQ into ChromaDB
uvicorn main:app --reload --port 8000

# 3. Frontend
cd frontend
npm install
npm start

# 4. Open in browser
http://localhost:3000
