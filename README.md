# promptconvert

A localhost tool that turns messy/casual user prompts into production-grade system prompts using a fixed architect template. Runs with your own API keys and supports both OpenAI and any OpenAI-compatible endpoint (configurable via `.env`).

## Quickstart

1) Clone and enter the repo, then set up a virtualenv (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Create a `.env` with your provider settings. Choose **one** of the blocks below.

- **OpenAI**

```
MODEL_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo
# Optional: override base URL if you proxy
# OPENAI_BASE_URL=https://api.openai.com/v1
```

- **OpenAI-compatible endpoint** (self-hosted or third-party that speaks the chat/completions API)

```
MODEL_PROVIDER=openai_compatible
LLM_API_KEY=your-key-here
LLM_MODEL=gpt-3.5-turbo
LLM_BASE_URL=https://your-endpoint/v1
```

> `.env` is gitignored. Keep your keys local.

3) Run the app:

```bash
uvicorn app.main:app --reload
```

4) Open the UI at http://localhost:8000

- Paste a messy prompt, click **Get System Prompt**.
- The backend calls your configured model with a system message containing the architect template and your input as the user message.
- Copy the returned system prompt and use it in your own LLM client.

## How it works

- The server builds a messages array:
  - `system`: the provided architect JSON template (fixed).
  - `user`: your messy prompt + a short instruction to produce only the crafted system prompt.
- Providers:
  - `openai` → uses `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_BASE_URL`.
  - `openai_compatible` → uses `LLM_API_KEY`, `LLM_MODEL`, `LLM_BASE_URL`.
- The response is the model-generated system prompt, shown in the UI with a Copy button.

## Project layout

```
app/
  main.py               # FastAPI app serving UI + /api/convert
  config.py             # Env-driven settings and validation
  system_prompt.py      # Architect template constants
  providers/
    base.py             # Provider interface
    openai_providers.py # OpenAI + OpenAI-compatible implementations
static/
  styles.css
  app.js
templates/
  index.html
requirements.txt
.gitignore
```

## Troubleshooting

- Empty output or 400 error: ensure your `.env` matches the provider you selected and the endpoint is reachable.
- CORS issues: not expected for localhost; if you reverse-proxy, allow `POST /api/convert`.
- Timeouts: the default request timeout is 60s; adjust in `openai_providers.py` if needed.

## Notes

- No data is persisted; requests go directly from your browser to the FastAPI backend, then to your configured model.
- To add another provider, implement `ModelProvider` in `app/providers` and extend the selection logic in `app/main.py`.
