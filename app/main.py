from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

from app.config import settings
from app.database import Base, engine
from app.routers import auth_routes, doctors, appointments, chat

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Bilingual (Tamil + English) Hospital AI Assistant — powered by Sarvam AI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(chat.router)


@app.on_event("startup")
def auto_load_policy_docs():
    """Auto-ingest PDFs from policy_docs/ on every startup if not already indexed."""
    try:
        from app.rag.chroma_store import policy_store
        from app.rag.document_loader import load_directory

        policy_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "policy_docs")

        if not os.path.isdir(policy_dir):
            print(f"[startup] policy_docs/ folder not found at {policy_dir} — skipping RAG load.")
            return

        existing = policy_store.count()
        if existing > 0:
            print(f"[startup] RAG already has {existing} chunks — skipping re-index. "
                  f"Delete chroma_store/ folder to force re-index.")
            return

        print(f"[startup] Indexing policy_docs/ into ChromaDB ...")
        load_directory(policy_dir)
        print(f"[startup] Done — {policy_store.count()} chunks indexed.")

    except Exception as e:
        print(f"[startup] WARNING: Could not auto-load policy docs: {e}")
        print("[startup] Server will still run — policy queries will redirect to hospital contact.")


@app.get("/", response_class=FileResponse, tags=["UI"])
def serve_ui():
    ui_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chat_ui.html")
    return FileResponse(ui_path)


@app.get("/health", tags=["System"])
def health_check():
    from app.rag.chroma_store import policy_store
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "env": settings.ENV,
        "rag_chunks_indexed": policy_store.count(),
    }
