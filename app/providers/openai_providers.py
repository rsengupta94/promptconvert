import requests

from app.config import Settings
from app.providers.base import ModelProvider
from app.system_prompt import SYSTEM_PROMPT, USER_INSTRUCTION_SUFFIX


class _BaseOpenAIClient:
    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, user_prompt: str) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"{user_prompt.strip()}\n\n{USER_INSTRUCTION_SUFFIX}",
            },
        ]
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0,
        }
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        if resp.status_code != 200:
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text
            raise ValueError(
                f"Model API error (status {resp.status_code}): {detail}"
            )

        data = resp.json()
        choices = data.get("choices") or []
        if not choices:
            raise ValueError("Model API returned no choices.")
        message = choices[0].get("message") or {}
        content = message.get("content")
        if not content:
            raise ValueError("Model API returned empty content.")
        return content.strip()


class OpenAIProvider(ModelProvider):
    def __init__(self, settings: Settings):
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY must be set for OpenAI provider.")
        self.client = _BaseOpenAIClient(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
            model=settings.openai_model,
        )

    def generate_system_prompt(self, user_prompt: str) -> str:
        return self.client.generate(user_prompt)
