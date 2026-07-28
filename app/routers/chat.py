from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ChatRequest, ChatResponse
from app.agent.router import handle_message
from app.models import ChatLog

router = APIRouter(prefix="/chat", tags=["AI Assistant"])


@router.post("/", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    try:
        result = handle_message(db, payload.message)
    except RuntimeError as e:
        # Sarvam API unreachable / quota exceeded / bad key, etc.
        raise HTTPException(
            status_code=503,
            detail=f"AI assistant is temporarily unavailable: {e}",
        )

    log = ChatLog(
        session_id=payload.session_id,
        user_message=payload.message,
        detected_language=result["detected_language"],
        detected_intent=result["detected_intent"],
        assistant_response=result["reply"],
    )
    db.add(log)
    db.commit()

    return ChatResponse(
        reply=result["reply"],
        detected_language=result["detected_language"],
        detected_intent=result["detected_intent"],
        sources=result.get("sources"),
    )
