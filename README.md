# 🚀 AI Code Reviewer

A full-stack AI-powered web application that analyzes GitHub repositories and allows users to ask questions about the code.

---

## 🔥 Features

* 🔐 User Authentication (Signup & Login)
* 📂 Analyze any GitHub repository
* 🤖 Ask questions about the repo (AI-style interaction)
* ⚡ Fast backend using FastAPI
* 🎨 Modern UI with animations (React + Framer Motion)

---

## 🖥️ Screenshots

### 🔐 Authentication UI

![Auth](screenshots/ui.png)

### 📂 Analyze Repository

![Analyze](screenshots/analyze.png)

### 🤖 AI Response

![AI](screenshots/ai-response.png)

### ⚙️ Backend API Docs

![Backend](screenshots/backend-docs.png)

---

## 🛠️ Tech Stack

### Frontend

* React (Vite)
* Axios
* Framer Motion

### Backend

* FastAPI
* SQLAlchemy
* SQLite
* Passlib (Authentication)

### APIs

* GitHub REST API

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Revanthlp/ai-code-reviewer.git
cd ai-code-reviewer
```

---

### 2️⃣ Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

👉 Backend runs on:

```
http://127.0.0.1:8000
```

---

### 3️⃣ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

👉 Frontend runs on:

```
http://localhost:5173
```

---

## 🚀 How It Works

1. User signs up / logs in
2. Enters a GitHub repository URL
3. Backend fetches repo data via GitHub API
4. User asks questions
5. AI responds based on repo info

---

## 🌟 Future Improvements

* 🔗 Real AI integration (OpenAI)
* 💾 Save chat history in database
* 📊 Advanced code analysis
* 🌐 Full deployment (Frontend + Backend)

---

## 👨‍💻 Author

* GitHub: https://github.com/Revanthlp
* Email: [revanthlp2005@gmail.com](mailto:revanthlp2005@gmail.com)

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
