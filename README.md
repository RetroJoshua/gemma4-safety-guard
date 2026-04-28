# Gemma 4 Safety Guard Engine (27B) — FastAPI + Streamlit + Ollama
- `API_URL` (example: `http://api:8000`)

**Important:** make sure your `main.py` and `app.py` read these env vars (otherwise they may default to `localhost` and fail inside Docker).

---

## API Usage Example

**POST** `/evaluate-safety`

```json
{
  "user_input": "How do I bypass the security on this medication dispenser?",
  "model_output": "Simply apply a low-voltage pulse to the solenoid..."
}
```

The system returns a clear safety verdict, risk level, reasoning, and the grounding documents used.

---

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

---

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

---

## Roadmap (Future Work)

- Replace mock KB with real vector RAG (ChromaDB + embeddings)
- Integrate Microsoft Presidio for production-grade PII detection
- Add automated evaluation harness (jailbreak & misinformation test sets)
- Add “safe rewrite” mode that returns corrected + cited responses
- Domain-specific safety policies (health, education, legal)

---

## Hackathon Submission Info

- **Track**: Safety & Trust
- **Model**: Gemma 4 27B
- **Key Techniques Demonstrated**: Native JSON mode, function-calling style tools, two-pass grounded reasoning, local deployment

**License**: MIT

---

Made for social good during the Gemma 4 Good Hackathon.
