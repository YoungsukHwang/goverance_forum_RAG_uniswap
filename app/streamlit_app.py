import streamlit as st
from src.rag_pipeline import GovernanceRAG

st.set_page_config(page_title="🦄 Uniswap Governance RAG (POC)", layout="wide")
st.title("🦄 Uniswap Governance RAG (POC)")

user_query = st.text_input("Ask about Uniswap Governance:", "")

if user_query:
    with st.spinner("Thinking..."):
        rag = GovernanceRAG(st=st)
        answer = rag.query(user_query, k=5)
        st.markdown("### 🤖 Answer")
        st.write(answer)

st.info("This demo uses Uniswap governance forum data (last 6 months).")
