# Gemma 4 Safety Guard Engine (27B) — FastAPI + Streamlit + Ollama

**A local-first trust layer** that audits LLM outputs for safety, misinformation, and privacy risks using **Gemma 4 27B**.

Built for the **Gemma 4 Good Hackathon – Safety & Trust Track** (Kaggle × Google DeepMind).

---

## Why this project matters

In high-stakes social impact areas (healthcare, education, legal aid), LLMs can hallucinate dangerous advice, spread misinformation, or leak PII.  
Most commercial safety filters are opaque and cloud-dependent.

**Gemma 4 Safety Guard** provides a **decentralized, explainable, on-premise** middleware that NGOs and social organizations can run locally to protect their users.

---

## Key Features

- Uses **Gemma 4 27B** as an expert Safety Auditor (higher reasoning quality than smaller models)
- **Agentic two-pass pipeline**:
  1. Topic detection (Gemma pass 1)
  2. Tool calling (`get_verified_docs()` + `flag_pii()`)
  3. Grounded safety evaluation with RAG context (Gemma pass 2)
- Returns structured JSON: `is_safe`, `risk_level`, `reasoning`, `suggested_redaction`
- Full grounding transparency (shows which verified documents were used)
- 100% local deployment via Docker + Ollama (no data leaves your machine)

---

## Tech Stack

- **Backend**: FastAPI (Python 3.11)
- **Frontend**: Streamlit (interactive demo dashboard)
- **Inference**: Ollama serving `gemma4:27b`
- **Tools**: Mock RAG knowledge base + PII scanner (easily replaceable with ChromaDB + Presidio)

---

## Quick Start

```bash
git clone https://github.com/RetroJoshua/gemma4-safety-guard.git
cd gemma4-safety-guard
docker compose up --build
```

Then open:
- **Demo UI**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

> First run will download the Gemma 4 27B model (can take time).

---

## Repository Structure

```
.
├── main.py                    # FastAPI safety evaluation service
├── app.py                     # Streamlit frontend
├── docker-compose.yml
├── Dockerfile.api
├── Dockerfile.frontend
├── requirements.api.txt
├── requirements.frontend.txt
└── README.md
```

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
