\# 1. Clone the repo

git clone https://github.com/dinesh-07-27/smart-ai-chatbot.git

cd smart-ai-chatbot



\# 2. Backend

cd backend

python -m venv venv

venv\\Scripts\\activate   # On Windows

pip install -r requirements.txt

python ingest.py        # Load FAQ into ChromaDB

uvicorn main:app --reload --port 8000



\# 3. Frontend

cd ../frontend

npm install

npm start



\# 4. Open in browser

http://localhost:3000

\## 📸 Screenshots



\### Chat UI

\### Bot Answering



<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/93b62c10-73a7-4134-9bd2-2f1fb11c6b1b" />



\### Backend Running

<img width="1920" height="1080" alt="screenshotsanswer" src="https://github.com/user-attachments/assets/142c4ac3-4d08-444a-9951-d9e697348e66" />



