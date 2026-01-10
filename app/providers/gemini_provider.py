import requests

from app.config import Settings
from app.providers.base import ModelProvider
from app.system_prompt import SYSTEM_PROMPT, USER_INSTRUCTION_SUFFIX


class GeminiProvider(ModelProvider):
    """
    Gemini provider using the official Google AI Studio (Generative Language) API key.
    """

    def __init__(self, settings: Settings):
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY must be set for gemini provider.")
        if not settings.gemini_model:
            raise ValueError("GEMINI_MODEL must be set for gemini provider.")
        if not settings.gemini_base_url:
            raise ValueError("GEMINI_BASE_URL must be set for gemini provider.")

        self.api_key = settings.gemini_api_key
        self.model = settings.gemini_model
        self.base_url = settings.gemini_base_url.rstrip("/")

    def generate_system_prompt(self, user_prompt: str) -> str:
        url = f"{self.base_url}/models/{self.model}:generateContent"
        payload = {
            "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": f"{user_prompt.strip()}\n\n{USER_INSTRUCTION_SUFFIX}",
                        }
                    ],
                }
            ],
            "generationConfig": {
                "temperature": 0,
                "candidateCount": 1,
                "maxOutputTokens": 2048,
            },
        }

        resp = requests.post(url, params={"key": self.api_key}, json=payload, timeout=60)
        if resp.status_code != 200:
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text
            raise ValueError(f"Gemini API error (status {resp.status_code}): {detail}")

        data = resp.json()
        candidates = data.get("candidates") or []
        if not candidates:
            raise ValueError("Gemini API returned no candidates.")
        content = (candidates[0].get("content") or {}).get("parts") or []
        if not content:
            raise ValueError("Gemini API returned empty content.")

        text_parts: list[str] = []
        for part in content:
            if isinstance(part, dict) and part.get("text"):
                text_parts.append(part["text"])
        result = "".join(text_parts).strip()
        if not result:
            raise ValueError("Gemini API returned empty text.")
        return result
