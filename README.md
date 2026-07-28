<<<<<<< HEAD
# Bilingual (Tamil + English) Hospital AI Assistant

Production-style hospital assistant backend with LLM-powered intent routing,
appointment booking, doctor management, and RAG-based policy Q&A — built on
**Sarvam AI** as the primary LLM/translation provider.

## Architecture

```
User (Tamil/English)
      │
      ▼
 FastAPI /chat endpoint
      │
      ▼
 app/agent/router.py  ── orchestrates:
   1. language_detector.py   → Sarvam LID (Tamil vs English)
   2. intent_classifier.py   → Sarvam chat completion → JSON intent + entities
   3. Route to data source:
        • hospital_policy_query → ChromaDB (RAG over policy docs)
        • doctor/appointment intents → PostgreSQL (Doctor table)
   4. Sarvam chat completion → grounded final answer
   5. Translate back to user's language
      │
      ▼
 Reply + logged to chat_logs table
```

Appointment booking and doctor management are exposed as standard REST
endpoints (JWT-protected, RBAC-enforced) so both the chat agent and a
front-end UI / receptionist dashboard can use them.

## Tech Stack

| Layer            | Technology                          |
|------------------|--------------------------------------|
| LLM & Translation| Sarvam AI (chat completion, LID, translate) |
| API Framework    | FastAPI                              |
| Relational DB    | PostgreSQL (doctors, appointments, users) |
| Vector DB        | ChromaDB (hospital policy documents) |
| Auth             | JWT (python-jose) + bcrypt (passlib) |
| Email            | SMTP (smtplib)                       |
| Validation       | Pydantic v2                          |

## Project Structure

```
hospital_ai_assistant/
├── app/
│   ├── main.py                  # FastAPI app entrypoint
│   ├── config.py                # Settings (env vars)
│   ├── database.py               # SQLAlchemy engine/session
│   ├── models.py                 # ORM models (User, Doctor, Appointment, ChatLog)
│   ├── schemas.py                 # Pydantic request/response schemas
│   ├── auth.py                    # JWT + bcrypt + RBAC
│   ├── email_service.py           # SMTP notifications (bilingual)
│   ├── sarvam_client.py           # Sarvam AI API wrapper
│   ├── agent/
│   │   ├── language_detector.py   # Tamil/English detection + translation
│   │   ├── intent_classifier.py   # LLM-based intent classification
│   │   └── router.py              # Multi-step reasoning orchestrator
│   ├── rag/
│   │   ├── chroma_store.py        # ChromaDB vector store wrapper
│   │   └── document_loader.py     # Chunk + ingest policy docs
│   └── routers/
│       ├── auth_routes.py         # register/login/refresh
│       ├── doctors.py             # doctor CRUD (admin-only writes)
│       ├── appointments.py        # booking, cancellation, listing
│       └── chat.py                # /chat endpoint (the AI agent)
├── policy_docs/                   # Sample .txt policy documents for RAG
├── scripts/
│   └── seed_doctors.py            # Populate sample doctors
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Setup

### 1. Clone & configure environment

```bash
cp .env.example .env
# Edit .env: add your SARVAM_API_KEY, Postgres creds, JWT secret, SMTP creds
```

Get a Sarvam AI API key from https://dashboard.sarvam.ai (or the current
Sarvam developer console) — used for chat completion, language ID, and
translation. Sign up, create an API subscription key, and paste it into
`SARVAM_API_KEY`.

### 2. Run with Docker (recommended)

```bash
docker compose up --build
```

This starts PostgreSQL + the FastAPI app. The app will auto-create tables on
first boot (via `Base.metadata.create_all`).

### 3. Or run locally without Docker

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Make sure PostgreSQL is running locally and matches your .env settings
uvicorn app.main:app --reload
```

### 4. Seed sample doctors

```bash
python -m scripts.seed_doctors
```

### 5. Ingest hospital policy documents into ChromaDB

```bash
python -m app.rag.document_loader ./policy_docs
```

Add your own `.txt`/`.md` files to `policy_docs/` (visiting hours, billing,
discharge process, etc.) before running this — it chunks and embeds each file.

### 6. Try it out

Visit **http://localhost:8000/docs** for interactive Swagger UI.

- `POST /auth/register` → create a patient account
- `POST /auth/login` → get access/refresh tokens
- `POST /doctors/` (admin token) → add doctors
- `POST /appointments/` (patient token) → book an appointment (sends email)
- `POST /chat/` → talk to the AI assistant in Tamil or English, e.g.:

```json
{
  "session_id": "abc123",
  "message": "எனக்கு இதய மருத்துவரிடம் அப்பாயின்ட்மென்ட் வேண்டும்"
}
```
or
```json
{
  "session_id": "abc123",
  "message": "What are the visiting hours for the ICU?"
}
```

## Key Design Notes

- **Sarvam as primary LLM**: `app/sarvam_client.py` centralizes all Sarvam API
  calls (chat completion, language identification, translation). Swap models
  or endpoints by editing `.env` only — no code changes needed elsewhere.
- **RAG**: policy documents live in ChromaDB with local sentence-transformer
  embeddings (`all-MiniLM-L6-v2`) for fast, free, offline-capable embedding.
  You can point `get_embedding_function()` at a hosted embedding API instead.
- **Multi-step reasoning**: `agent/router.py` is the single place where
  language detection → intent classification → retrieval → grounded
  generation → back-translation happens. This is intentionally a plain
  Python function (not a heavyweight agent framework) so it's easy to trace,
  test, and debug.
- **RBAC**: `require_roles([...])` in `auth.py` is a dependency factory used
  to protect admin/receptionist-only routes (e.g., creating doctors).
- **Security**: passwords are hashed with bcrypt; JWTs are short-lived access
  tokens + longer-lived refresh tokens; never commit your real `.env`.

## Next Steps / Production Hardening Ideas

- Add Alembic migrations instead of `create_all()`.
- Add rate limiting (e.g., slowapi) on `/chat` and `/auth/login`.
- Add a proper conversation memory store (Redis) keyed by `session_id` for
  true multi-turn context beyond a single request.
- Add doctor slot-availability computation (currently appointments only check
  for exact datetime clashes, not full slot-grid availability).
- Add automated tests (pytest + httpx TestClient) for each router.
- Add a `Dockerfile.worker` if you split ChromaDB ingestion into a background
  worker for large document sets.
=======
this is hospital ai chatbot
>>>>>>> 942aceb52c64af6007d90624a0d6f806f01ba3cf
