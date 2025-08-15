import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.title("LLM Research Assistant")

with st.expander("Ingest papers"):
    q = st.text_input("arXiv query", value="large language models evaluation")
    n = st.number_input("max results", 1, 100, 20)
    if st.button("Ingest"):
        r = requests.post(f"{API_URL}/ingest", json={"query": q, "max_results": int(n)})
        st.write(r.json())

st.subheader("Ask a question")
question = st.text_input("Question", value="What are current best practices for RAG evaluation?")
k = st.slider("Top-K", 1, 10, 5)
if st.button("Ask"):
    r = requests.post(f"{API_URL}/ask", json={"question": question, "k": int(k)})
    if r.status_code != 200:
        st.error(r.text)
    else:
        data = r.json()
        st.markdown("### Answer")
        st.write(data["answer"])
        st.markdown("### Sources")
        for i, s in enumerate(data["sources"], 1):
            st.markdown(f"**[{i}] {s['title']}**  \n{s['link']}  \n{s['published']}  \n{', '.join(s['authors'])}")
