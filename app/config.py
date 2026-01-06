import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


SUPPORTED_PROVIDERS = {"openai", "openai_compatible"}


def _get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    return os.environ.get(key) or default


@dataclass
class Settings:
    model_provider: str
    openai_api_key: Optional[str]
    openai_model: Optional[str]
    openai_base_url: Optional[str]
    llm_api_key: Optional[str]
    llm_model: Optional[str]
    llm_base_url: Optional[str]

    @classmethod
    def load(cls) -> "Settings":
        # Load from .env if present
        load_dotenv()

        provider = (_get_env("MODEL_PROVIDER", "openai_compatible") or "").strip()
        if provider not in SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported MODEL_PROVIDER '{provider}'. Supported: {sorted(SUPPORTED_PROVIDERS)}"
            )

        return cls(
            model_provider=provider,
            openai_api_key=_get_env("OPENAI_API_KEY"),
            openai_model=_get_env("OPENAI_MODEL", "gpt-3.5-turbo"),
            openai_base_url=_get_env("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            llm_api_key=_get_env("LLM_API_KEY"),
            llm_model=_get_env("LLM_MODEL", "gpt-3.5-turbo"),
            llm_base_url=_get_env("LLM_BASE_URL"),
        )

    def validate_for_provider(self) -> None:
        if self.model_provider == "openai":
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required for provider 'openai'.")
            if not self.openai_model:
                raise ValueError("OPENAI_MODEL is required for provider 'openai'.")
        elif self.model_provider == "openai_compatible":
            if not self.llm_api_key:
                raise ValueError("LLM_API_KEY is required for provider 'openai_compatible'.")
            if not self.llm_base_url:
                raise ValueError("LLM_BASE_URL is required for provider 'openai_compatible'.")
            if not self.llm_model:
                raise ValueError("LLM_MODEL is required for provider 'openai_compatible'.")
        else:
            raise ValueError(f"Unknown model provider '{self.model_provider}'.")
