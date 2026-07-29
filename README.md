
**🏥 Bilingual Hospital AI Assistant**

A production-ready Tamil + English hospital chatbot powered by Sarvam AI, FastAPI, and RAG architecture. Patients can ask questions in Tamil or English and receive instant, accurate answers about doctors, appointments, visiting hours, and hospital policies.

**✨ Features**
**Feature	Details**
🌐 Bilingual	Tamil & English — auto-detected, auto-translated
🤖 Sarvam AI	LLM for language ID, translation, policy answers
📄 RAG Pipeline	ChromaDB + sentence-transformers for PDF/TXT retrieval
⚡ Fast Intent	Rule-based classifier — zero LLM latency for doctor queries
🔐 Auth	JWT + bcrypt + Role-based access (Admin/Doctor/Patient)
📅 Appointments	Book, cancel, reschedule with email confirmation
💬 Chat Widget	Embeddable HTML widget with typing indicator
🗄️ SQLite	No PostgreSQL or Docker needed — runs anywhere

**🏗️ Architecture**
User (Tamil/English)
        │
        ▼
  Chat Widget (HTML/JS)
        │
        ▼
  FastAPI /chat endpoint
        │
        ▼
  Language Detector (Sarvam LID)
        │
        ▼
  Intent Classifier (Rule-based, instant)
        │
   ┌────┴────┐
   ▼         ▼
SQLite    ChromaDB
(Doctors)  (Policies)
   │         │
   └────┬────┘
        ▼
  Final Answer
        │
  Translate back (Sarvam)
        │
        ▼
   Reply to User
🚀 Quick Start
bash
# 1. Clone and setup
git clone https://github.com/yourusername/hospital-ai-assistant
cd hospital-ai-assistant
python -m venv venv && venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Add your SARVAM_API_KEY and JWT_SECRET_KEY in .env

# 4. Start server
uvicorn app.main:app --reload

# 5. Open browser
# http://127.0.0.1:8000

**📁 Project Structure**
hospital_ai_assistant/
├── app/
│   ├── main.py                  # FastAPI app + auto-index startup
│   ├── config.py                # Environment settings
│   ├── models.py                # SQLAlchemy ORM models
│   ├── schemas.py               # Pydantic request/response schemas
│   ├── auth.py                  # JWT + bcrypt + RBAC
│   ├── email_service.py         # SMTP appointment notifications
│   ├── sarvam_client.py         # Sarvam AI API wrapper
│   ├── agent/
│   │   ├── intent_classifier.py # Rule-based intent engine
│   │   ├── language_detector.py # Tamil/English detection
│   │   └── router.py            # Multi-step reasoning orchestrator
│   ├── rag/
│   │   ├── chroma_store.py      # ChromaDB vector store
│   │   └── document_loader.py   # PDF/TXT chunker and indexer
│   └── routers/
│       ├── auth_routes.py       # Register/login/refresh
│       ├── doctors.py           # Doctor CRUD (admin-only writes)
│       ├── appointments.py      # Booking/cancellation
│       └── chat.py              # AI chat endpoint
├── policy_docs/                 # Hospital PDF/TXT knowledge base
├── scripts/
│   └── seed_doctors.py          # Seed sample doctor data
├── chat_ui.html                 # Embeddable chat widget
├── requirements.txt
├── .env.example
└── README.md


**🔑 Environment Variables**
env
SARVAM_API_KEY=your-key-here
SARVAM_CHAT_MODEL=sarvam-m
JWT_SECRET_KEY=your-secret-here
DB_ENGINE=sqlite
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

**🛠️ Tech Stack**
Backend: Python 3.11, FastAPI, SQLAlchemy, Pydantic v2
LLM: Sarvam AI (sarvam-30b) — chat, language ID, translation
Vector DB: ChromaDB with sentence-transformers embeddings
Database: SQLite (dev) / PostgreSQL (prod)
Auth: python-jose (JWT), passlib (bcrypt)
Email: smtplib (SMTP)
Frontend: Vanilla HTML/CSS/JavaScript

**📌 API Endpoints**
Method	Endpoint	Description
POST	/auth/register	Register new user
POST	/auth/login	Login, get JWT token
GET	/doctors/	List all doctors
POST	/doctors/	Create doctor (admin)
POST	/appointments/	Book appointment
GET	/appointments/me	My appointments
POST	/chat/	Chat with AI assistant
GET	/health	Health check + RAG stats
GET	/	Chat widget UI

**🌟 How to Update Hospital Data**
Edit or replace files in policy_docs/
Delete the chroma_store/ folder
Restart the server — auto-indexes on startup
