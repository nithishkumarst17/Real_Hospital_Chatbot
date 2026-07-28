from app.sarvam_client import sarvam_client


def detect_language(text: str) -> str:
    """
    Returns 'ta' or 'en'. Used to decide which language to reply in
    and whether translation is needed before hitting the RAG store
    (policy documents are indexed in English).
    """
    return sarvam_client.identify_language(text)


def to_english(text: str, source_lang: str) -> str:
    """Translate incoming Tamil text to English for retrieval / reasoning."""
    if source_lang == "en":
        return text
    return sarvam_client.translate(text, source_lang="ta-IN", target_lang="en-IN")


def to_user_language(text: str, target_lang: str) -> str:
    """Translate the final English answer back into Tamil if needed."""
    if target_lang == "en":
        return text
    return sarvam_client.translate(text, source_lang="en-IN", target_lang="ta-IN")
