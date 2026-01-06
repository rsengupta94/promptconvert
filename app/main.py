from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.config import Settings
from app.providers.base import ModelProvider
from app.providers.openai_providers import (
    OpenAICompatibleProvider,
    OpenAIProvider,
)


dist_dir = Path(__file__).resolve().parent.parent
static_dir = dist_dir / "static"
templates_dir = dist_dir / "templates"

app = FastAPI(title="promptconvert", version="0.1.0")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


class ConvertRequest(BaseModel):
    prompt: str = Field(..., description="Messy or casual user prompt")


class ConvertResponse(BaseModel):
    system_prompt: str


settings = Settings.load()
settings.validate_for_provider()

if settings.model_provider == "openai":
    provider: ModelProvider = OpenAIProvider(settings)
elif settings.model_provider == "openai_compatible":
    provider = OpenAICompatibleProvider(settings)
else:
    raise RuntimeError(f"Unsupported provider: {settings.model_provider}")


@app.get("/")
def serve_index() -> FileResponse:
    index_path = templates_dir / "index.html"
    return FileResponse(index_path)


@app.post("/api/convert", response_model=ConvertResponse)
def convert_prompt(req: ConvertRequest) -> ConvertResponse:
    if not req.prompt or not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt must not be empty.")
    try:
        system_prompt = provider.generate_system_prompt(req.prompt)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - runtime safety
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    return ConvertResponse(system_prompt=system_prompt)
