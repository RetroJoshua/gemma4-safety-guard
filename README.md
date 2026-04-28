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