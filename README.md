# System Prompt Generator

A localhost tool that turns messy/casual user prompts into production-grade system prompts using a fixed architect template. Runs with your own API keys. Supports OpenAI (GPT 4o mini) and Gemini (Google AI Studio - Gemini 2.5 flash) (configurable via `.env`).

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
OPENAI_MODEL=gpt-4o-mini
# Optional: override base URL if you proxy
# OPENAI_BASE_URL=https://api.openai.com/v1
```

- **Gemini** (Google AI Studio API key)

```
MODEL_PROVIDER=gemini
GEMINI_API_KEY=your-key-here
GEMINI_MODEL=gemini-2.5-flash
# Optional: override base URL if needed
# GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
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

- The backend sends:
  - a fixed architect template as the "system instruction"
  - your messy prompt + a short instruction to return only the crafted system prompt
- Providers:
  - `openai` → uses `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_BASE_URL`.
  - `gemini` → uses `GEMINI_API_KEY` (AI Studio key), `GEMINI_MODEL`, `GEMINI_BASE_URL`.
- The response is the model-generated system prompt, shown in the UI with a Copy button.

## Project layout

```
app/
  main.py               # FastAPI app serving UI + /api/convert
  config.py             # Env-driven settings and validation
  system_prompt.py      # Architect template constants
  providers/
    base.py             # Provider interface
    openai_providers.py # OpenAI implementation
    gemini_provider.py  # Gemini (Google AI Studio) implementation
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

For any feedback, feel free to reach out to me. Cheers! - Rajarshi (https://github.com/rsengupta94)
