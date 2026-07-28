from sqlalchemy.orm import Session
from app.agent.language_detector import detect_language, to_english, to_user_language
from app.agent.intent_classifier import classify_intent
from app.rag.chroma_store import policy_store
from app.models import Doctor
import re

HOSPITAL_CONTACT = "📞 Please contact Nithishkumar Hospital at +91-44-2345-6789 or visit us at Porur, Chennai - 600001."

def _lookup_doctors(db, specialization=None):
    query = db.query(Doctor).filter(Doctor.is_active == True)
    if specialization:
        query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))
    return query.limit(5).all()


def _doctor_card(d):
    days = d.available_days or "Mon-Fri"
    qual = f" | {d.qualification}" if d.qualification else ""
    return f"Dr. {d.name} | {d.specialization}{qual} | {days} {d.slot_start_time}–{d.slot_end_time}"


def _clean_rag_answer(chunks, query):
    query_words = set(re.findall(r'\w+', query.lower()))
    
    all_sentences = []
    for chunk in chunks:
        parts = re.split(r'[\n●•*]|(?<=[.!?])\s+', chunk)
        for part in parts:
            part = part.strip().strip('*-•●').strip()
            if len(part) < 15:
                continue
            part_words = set(re.findall(r'\w+', part.lower()))
            score = len(query_words & part_words)
            first_words = set(re.findall(r'\w+', part[:50].lower()))
            if query_words & first_words:
                score += 3
            all_sentences.append((score, part))

    if not all_sentences:
        return ""

    all_sentences.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 2 sentences if they are related
    results = []
    top_score = all_sentences[0][0]
    for score, sent in all_sentences[:5]:
        if score >= top_score - 1:
            results.append(sent)
        if len(results) == 2:
            break

    return " ".join(results) if results else ""

def handle_message(db, message):
    lang = detect_language(message)
    english_text = to_english(message, lang)
    intent_result = classify_intent(english_text)
    intent = intent_result["intent"]
    entities = intent_result.get("entities", {})
    reply = ""
    sources = []

    if intent in ("check_doctor_availability", "book_appointment", "reschedule_appointment"):
        spec = entities.get("specialization")
        if not spec:
          reply_en = f"Appointments can be booked by calling +91-44-2345-6789 or visiting www.nithishkumarhospital.com. Walk-in is also available at Nithishkumar Hospital, Porur, Chennai."
        else:
            doctors = _lookup_doctors(db, spec)
            if doctors:
                cards = "\n".join(_doctor_card(d) for d in doctors)
                reply_en = f"{spec.title()} doctors:\n{cards}"
                sources = ["doctors_db"]
            else:
                reply_en = f"No {spec} doctors found. {HOSPITAL_CONTACT}"
        reply = to_user_language(reply_en, lang)

    elif intent == "cancel_appointment":
        reply_en = f"To cancel your appointment please provide your appointment ID or registered phone number. {HOSPITAL_CONTACT}"
        reply = to_user_language(reply_en, lang)

    elif intent == "general_greeting":
        reply_en = "Hello! Welcome to Nithishkumar Hospital AI Assistant. I can help you find doctors by specialization or answer questions about hospital services. How can I help you today?"
        reply = to_user_language(reply_en, lang)

    else:
        rag = policy_store.query(english_text, top_k=3)
        docs = rag["documents"] if rag["documents"] else []
        sources = [m.get("source", "policy") for m in rag["metadatas"]]
        if docs:
            english_reply = _clean_rag_answer(docs, english_text)
            if not english_reply or len(english_reply) < 10:
                english_reply = f"I don't have specific information on that. {HOSPITAL_CONTACT}"
        else:
            english_reply = f"I'm not able to answer that. {HOSPITAL_CONTACT}"
        reply = to_user_language(english_reply, lang)

    return {
        "reply": reply,
        "detected_language": lang,
        "detected_intent": intent,
        "entities": entities,
        "sources": sources,
    }