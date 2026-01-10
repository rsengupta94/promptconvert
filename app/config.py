import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


SUPPORTED_PROVIDERS = {"openai", "gemini"}


def _get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    return os.environ.get(key) or default


@dataclass
class Settings:
    model_provider: str
    openai_api_key: Optional[str]
    openai_model: Optional[str]
    openai_base_url: Optional[str]
    gemini_api_key: Optional[str]
    gemini_model: Optional[str]
    gemini_base_url: Optional[str]

    @classmethod
    def load(cls) -> "Settings":
        # Load from .env if present
        load_dotenv()

        provider = (_get_env("MODEL_PROVIDER", "openai") or "").strip()
        if provider not in SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported MODEL_PROVIDER '{provider}'. Supported: {sorted(SUPPORTED_PROVIDERS)}"
            )

        return cls(
            model_provider=provider,
            openai_api_key=_get_env("OPENAI_API_KEY"),
            openai_model=_get_env("OPENAI_MODEL", "gpt-4o-mini"),
            openai_base_url=_get_env("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            gemini_api_key=_get_env("GEMINI_API_KEY"),
            gemini_model=_get_env("GEMINI_MODEL", "gemini-2.5-flash"),
            gemini_base_url=_get_env(
                "GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta"
            ),
        )

    def validate_for_provider(self) -> None:
        if self.model_provider == "openai":
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required for provider 'openai'.")
            if not self.openai_model:
                raise ValueError("OPENAI_MODEL is required for provider 'openai'.")
        elif self.model_provider == "gemini":
            if not self.gemini_api_key:
                raise ValueError("GEMINI_API_KEY is required for provider 'gemini'.")
            if not self.gemini_model:
                raise ValueError("GEMINI_MODEL is required for provider 'gemini'.")
            if not self.gemini_base_url:
                raise ValueError("GEMINI_BASE_URL is required for provider 'gemini'.")
        else:
            raise ValueError(f"Unknown model provider '{self.model_provider}'.")
