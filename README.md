# 🤖 Smart AI Customer Support Chatbot

A **full-stack AI-powered chatbot** for customer support using **FastAPI, React, and Llama2 (via Ollama)**.  
It combines **RAG (Retrieval-Augmented Generation)** with a FAQ knowledge base to provide **context-aware, real-time responses**.

---

## 🚀 Features
- Natural conversation with **Llama2**  
- **RAG-powered FAQ retrieval** (`faq.txt`)  
- **FastAPI backend** with REST API  
- **React frontend** with real-time chat UI  
- **SQLite + ChromaDB** for chat history & vector search  
- Easy to extend with more data sources  

---

## 🛠️ Tech Stack
- **Frontend**: React (JavaScript)  
- **Backend**: FastAPI (Python)  
- **Database**: SQLite + ChromaDB  
- **AI Model**: Llama2 via [Ollama](https://ollama.ai)  

---

## ⚡ Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/dinesh-07-27/smart-ai-chatbot.git
cd smart-ai-chatbot
2. Backend
bash
Copy code
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python ingest.py   # load FAQ into ChromaDB
uvicorn main:app --reload --port 8000
3. Frontend
bash
Copy code
cd frontend
npm install
npm start
4. Open App
👉 http://localhost:3000

📌 Future Improvements
🌍 Multi-language support

🎙️ Voice (STT + TTS) integration

☁️ Cloud deployment (AWS/Render/Vercel)

📊 Analytics dashboard for admins

👤 Author
K Dinesh Reddy
🔗 LinkedIn • GitHub • LeetCode

yaml
Copy code
