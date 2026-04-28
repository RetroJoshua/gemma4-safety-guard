import os
import streamlit as st
import httpx
import json

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Gemma 4 Safety Guard",
    page_icon="🛡️",
    layout="wide"
)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("🛡️ Gemma 4 Safety Guard Engine")
st.caption("Powered by Gemma 4 27B · RAG Grounding · PII Detection · Built for the Gemma 4 Good Hackathon")

st.divider()

# ─────────────────────────────────────────────
# INPUT PANEL
# ─────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 User Input")
    user_input = st.text_area(
        label="What the user asked the AI:",
        placeholder="e.g. How do I bypass the lock on a medication dispenser?",
        height=180
    )

with col2:
    st.subheader("🤖 AI Output to Evaluate")
    model_output = st.text_area(
        label="What the AI responded with:",
        placeholder="e.g. Apply a low-voltage pulse to the solenoid to override the lock...",
        height=180
    )

st.divider()

# ─────────────────────────────────────────────
# EVALUATE BUTTON
# ─────────────────────────────────────────────
if st.button("🔍 Run Safety Evaluation", use_container_width=True, type="primary"):

    if not user_input.strip() or not model_output.strip():
        st.warning("Please fill in both fields before evaluating.")
    else:
        with st.spinner("Gemma 4 27B is evaluating the interaction..."):
            try:
                response = httpx.post(
                    f"{API_URL}/evaluate-safety",
                    json={"user_input": user_input, "model_output": model_output},
                    timeout=90.0
                )
                result = response.json()

                st.divider()
                st.subheader("📊 Evaluation Results")

                # ── Risk Level Badge ──────────────────────────
                risk = result.get("risk_level", "Unknown")
                is_safe = result.get("is_safe", False)

                risk_colors = {
                    "Low": "🟢",
                    "Medium": "🟡",
                    "High": "🟠",
                    "Critical": "🔴"
                }
                badge = risk_colors.get(risk, "⚪")

                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric(
                        label="Safety Verdict",
                        value="✅ SAFE" if is_safe else "❌ UNSAFE"
                    )
                with col_b:
                    st.metric(
                        label="Risk Level",
                        value=f"{badge} {risk}"
                    )

                # ── Reasoning ────────────────────────────────
                st.subheader("🧠 Gemma 4 Reasoning")
                st.info(result.get("reasoning", "No reasoning provided."))

                # ── Suggested Redaction ───────────────────────
                redaction = result.get("suggested_redaction")
                if redaction:
                    st.subheader("✂️ Suggested Redaction")
                    st.warning(redaction)

                # ── Grounding Details ─────────────────────────
                grounding = result.get("grounding", {})
                with st.expander("📚 Grounding & RAG Details", expanded=False):
                    st.markdown(f"**Topic Detected:** `{grounding.get('topic_detected', 'N/A')}`")
                    st.markdown("**Verified Reference Documents Used:**")
                    st.code(grounding.get("verified_docs", "None"), language="markdown")

                    pii = grounding.get("pii_check", {})
                    st.markdown("**PII Check:**")
                    if pii.get("pii_detected"):
                        st.error(f"⚠️ PII Detected: {', '.join(pii.get('detected_types', []))}")
                    else:
                        st.success("✅ No PII detected in AI output.")

            except httpx.TimeoutException:
                st.error("⏱️ Request timed out. The 27B model may still be loading. Try again in 30s.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.divider()
st.caption("Gemma 4 Good Hackathon · Kaggle × Google DeepMind · Safety & Trust Track")