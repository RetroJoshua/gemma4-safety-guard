# 🛡️ Gemma 4 Safety Guard Engine

### *Transforming AI Safety through Grounded Reasoning and Local Trust*

Built for the **Gemma 4 Good Hackathon (Safety & Trust Track)**, the **Gemma 4 Safety Guard Engine** is a production-ready middleware layer that ensures AI-generated content remains safe, factual, and private. It leverages the reasoning power of the **Gemma 4 27B** model to act as an autonomous auditor and grounding agent.

---

## 🌍 The Mission
As AI is deployed in high-stakes social sectors—such as community health, legal aid, and education—the risk of "hallucinations" or unsafe advice increases. Most current safety solutions depend on opaque, cloud-based filters. 

**Gemma 4 Safety Guard Engine** provides a **decentralized, local-first alternative** that NGOs and social enterprises can run on their own infrastructure to ensure:
1. **Safety:** Identifying harmful instructions or medical misinformation.
2. **Trust:** Grounding claims in verified documents via RAG.
3. **Privacy:** Detecting PII (Personally Identifiable Information) before it leaves the local network.

---

## 🚀 Key Features

- **Gemma 4 27B Auditor:** Uses the high-parameter 27B model for nuanced safety reasoning that smaller models miss.
- **Agentic Two-Pass Pipeline:** 
    - *Pass 1:* Detects the topic and triggers relevant internal functions (Function Calling).
    - *Pass 2:* Re-evaluates content using retrieved "Verified Reference Documents" (Grounding).
- **Native JSON Enforcement:** Uses Gemma 4’s native JSON mode for reliable downstream integration.
- **Privacy-First:** Designed to run entirely on-premise using Docker and Ollama, ensuring sensitive user data never touches the public cloud.

---

## 🛠️ Technical Architecture

The system is built with a modern, decoupled stack:
- **Inference Engine:** [Ollama](https://ollama.com/) serving Gemma 4 27B.
- **Backend API:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11) managing the RAG pipeline and tool execution.
- **Simulation Layer:** Mock RAG knowledge base for medication safety, vaccine facts, and mental health.
- **Frontend:** [Streamlit](https://streamlit.io/) for an interactive "Safety Dashboard" demo.

---

## 📦 Getting Started

### Prerequisites
- Docker & Docker Compose
- *Suggested:* NVIDIA GPU with 16GB+ VRAM (for 27B model inference at reasonable speeds).

### Installation & Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/gemma4-safety-guard.git
   cd gemma4-safety-guard