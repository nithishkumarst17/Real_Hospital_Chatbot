import requests
from typing import Optional
from app.config import settings


class SarvamClient:
    def __init__(self):
        self.api_key = settings.SARVAM_API_KEY
        self.base_url = settings.SARVAM_BASE_URL
        self.headers = {
            "api-subscription-key": self.api_key,
            "Content-Type": "application/json",
        }

    def chat_completion(
        self,
        messages: list,
        temperature: float = 0.2,
        max_tokens: int = 512,
    ) -> str:
        """
        messages: [{"role": "system"|"user"|"assistant", "content": "..."}]
        Returns the assistant's text reply.
        """
        url = f"{self.base_url}{settings.SARVAM_CHAT_ENDPOINT}"
        payload = {
            "model": settings.SARVAM_CHAT_MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        try:
            resp = requests.post(url, headers=self.headers, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            msg = data["choices"][0]["message"]
            content = msg.get("content") or msg.get("reasoning_content") or ""
            return content.strip()
        except requests.RequestException as e:
            raise RuntimeError(f"Sarvam chat completion failed: {e}")

    def identify_language(self, text: str) -> str:
        """
        Returns an ISO-ish language code, e.g. 'ta' (Tamil) or 'en' (English).
        Uses Sarvam's language identification endpoint; falls back to a
        lightweight heuristic (Tamil unicode block detection) if the API
        call fails, so the assistant degrades gracefully.
        """
        url = f"{self.base_url}/text-lid"
        try:
            resp = requests.post(
                url, headers=self.headers, json={"input": text}, timeout=10
            )
            resp.raise_for_status()
            data = resp.json()
            lang_code = data.get("language_code", "en-IN")
            return "ta" if lang_code.startswith("ta") else "en"
        except requests.RequestException:
            # Fallback heuristic: Tamil Unicode block is U+0B80–U+0BFF
            if any("\u0b80" <= ch <= "\u0bff" for ch in text):
                return "ta"
            return "en"

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        source_lang / target_lang use codes like 'ta-IN', 'en-IN'.
        """
        url = f"{self.base_url}{settings.SARVAM_TRANSLATE_ENDPOINT}"
        payload = {
            "input": text,
            "source_language_code": source_lang,
            "target_language_code": target_lang,
        }
        try:
            resp = requests.post(url, headers=self.headers, json=payload, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            return data.get("translated_text", text)
        except requests.RequestException:
            # If translation fails, return original text rather than crashing
            return text


sarvam_client = SarvamClient()
