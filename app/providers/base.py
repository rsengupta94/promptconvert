from abc import ABC, abstractmethod
from typing import Protocol


class ModelProvider(ABC):
    @abstractmethod
    def generate_system_prompt(self, user_prompt: str) -> str:
        """
        Take a messy/casual user prompt and return a crafted system prompt string.
        """
        raise NotImplementedError


class ProviderFactory(Protocol):
    def __call__(self) -> ModelProvider:  # pragma: no cover - structural typing hint
        ...
