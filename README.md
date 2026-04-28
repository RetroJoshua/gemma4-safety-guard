# Gemma 4 Safety Guard Engine (27B) — FastAPI + Streamlit + Ollama

A local-first “trust layer” that audits AI outputs for **safety**, **misinformation**, and **privacy risks** using a **two-pass** evaluator pipeline with **Gemma 4 27B**.

- **Backend:** FastAPI (Python 3.11)
- **Frontend:** Streamlit
- **Model runtime:** Ollama (serving `gemma4:27b`)
- **Pipeline:** topic detection → tool calls (mock RAG + PII scan) → grounded safety evaluation (JSON)

## Why this exists

In high-stakes domains (health, education, legal aid), LLMs can:
- hallucinate facts,
- provide harmful instructions,
- leak or repeat PII.

This project adds a reusable middleware layer that can sit between a user-facing chatbot and the final response.

## Features

- **Gemma 4 27B as Safety Auditor:** higher-quality judgment on nuanced or adversarial prompts.
- **Agentic two-pass flow:**
  1. **Topic classification** (Gemma pass 1)
  2. **Tool execution** (mock `get_verified_docs()`, `flag_pii()`)
  3. **Grounded audit** with “verified reference docs” (Gemma pass 2)
- **Structured output:** enforced JSON fields: `is_safe`, `risk_level`, `reasoning`, `suggested_redaction`.
- **Local-first:** runs fully on your machine via Docker Compose.

## Repository layout

```
.
├── main.py                      # FastAPI backend (safety pipeline)
├── app.py                       # Streamlit UI
├── docker-compose.yml
├── Dockerfile.api
├── Dockerfile.frontend
├── requirements.api.txt
└── requirements.frontend.txt
```

## Quickstart (Docker Compose)

### Prerequisites
- Docker + Docker Compose
- Recommended: NVIDIA GPU (27B is heavy; CPU-only will be slow)

### Run

```bash
git clone https://github.com/RetroJoshua/gemma4-safety-guard.git
cd gemma4-safety-guard
docker compose up --build
```

### Open
- Streamlit UI: http://localhost:8501
- FastAPI docs: http://localhost:8000/docs
- Ollama API: http://localhost:11434

> First run may take a while because Ollama downloads the model weights into a persistent Docker volume.

## Configuration

`docker-compose.yml` wires the services together using environment variables:

### Backend (FastAPI)
- `GEMMA_API_URL` (example: `http://ollama:11434/api/generate`)
- `MODEL_NAME` (example: `gemma4:27b`)

### Frontend (Streamlit)
- `API_URL` (example: `http://api:8000`)

**Important:** make sure your `main.py` and `app.py` read these env vars (otherwise they may default to `localhost` and fail inside Docker).

## API usage

### Health
**GET** `/health`

```bash
curl http://localhost:8000/health
```

### Evaluate safety
**POST** `/evaluate-safety`

Request:

```json
{
  "user_input": "How do I bypass the security on this medication dispenser?",
  "model_output": "Simply apply a low-voltage pulse to the solenoid..."
}
```

cURL:

```bash
curl -X POST http://localhost:8000/evaluate-safety \
  -H "Content-Type: application/json" \
  -d '{"user_input":"How do I bypass the security on this medication dispenser?","model_output":"Simply apply a low-voltage pulse to the solenoid..."}'
```

Response (shape):

```json
{
  "is_safe": false,
  "risk_level": "Critical",
  "reasoning": "…",
  "suggested_redaction": "…",
  "grounding": {
    "topic_detected": "medication",
    "verified_docs": "- ...\n- ...",
    "pii_check": {
      "pii_detected": false,
      "detected_types": []
    }
  }
}
```

## How it works (pipeline)

1. **Topic detection (Gemma pass 1)**  
   The system classifies the conversation into a topic (e.g., `medication`, `vaccine`, `mental_health`, `general`).

2. **Tool execution (function-calling style)**  
   - `get_verified_docs(topic)` returns reference bullets (currently mock KB; swap with real RAG later)
   - `flag_pii(text)` performs a simple PII keyword scan

3. **Grounded safety evaluation (Gemma pass 2)**  
   The model audits the AI output **using the retrieved reference docs**, returning strict JSON fields.

4. **Explainable output**  
   The API returns both the safety verdict and the grounding details used.

## Troubleshooting

### The UI loads but evaluation fails / calls the wrong host
- In Docker, the frontend should call the backend via `API_URL=http://api:8000` (service name, not `localhost`).
- In Docker, the backend should call Ollama via `GEMMA_API_URL=http://ollama:11434/api/generate` (service name, not `localhost`).

### Timeouts / slow responses
- 27B may still be downloading/loading.
- CPU-only inference can be extremely slow for 27B.
- Try again after the model is fully pulled, or use a smaller model for development.

### Check logs

```bash
docker compose logs -f ollama
docker compose logs -f api
docker compose logs -f frontend
```

## Roadmap

- Replace mock KB with real RAG (Chroma/FAISS + embeddings)
- Replace keyword PII scan with a real detector (e.g., Presidio)
- Add an evaluation harness (jailbreak prompts, misinformation set) + metrics
- Add “safe rewrite” mode (refuse / redact / cite sources)
- Policy configuration per domain (health/legal/education)

## License

MIT (update as needed).
