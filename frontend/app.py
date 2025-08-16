import os
import streamlit as st
import requests

# ---- Configurable API base ----
DEFAULT_API = os.getenv("API_URL", "http://127.0.0.1:8010")  # use 8010, not 8000
if "api_url" not in st.session_state:
    st.session_state.api_url = DEFAULT_API

st.set_page_config(page_title="LLM Research Assistant", layout="centered")
st.title("LLM Research Assistant")

with st.sidebar:
    st.subheader("Backend")
    api_input = st.text_input("API URL", st.session_state.api_url, help="Example: http://127.0.0.1:8010")
    st.session_state.api_url = api_input.rstrip("/")
    # Health check
    try:
        r = requests.get(f"{st.session_state.api_url}/healthz", timeout=5)
        if r.ok:
            st.success(f"Connected: {st.session_state.api_url}")
        else:
            st.error(f"Health check failed: {r.status_code}")
    except Exception as e:
        st.error(f"Cannot reach API: {e}")
    st.caption("Open API docs in a browser to confirm routes exist: "
               f"{st.session_state.api_url}/docs")

API_URL = st.session_state.api_url

def post_json(path: str, payload: dict):
    url = f"{API_URL}{path}"
    try:
        resp = requests.post(url, json=payload, timeout=60)
        data = {}
        try:
            data = resp.json()
        except Exception:
            data = {"raw": resp.text}
        if resp.status_code != 200:
            st.error(f"{resp.status_code} {resp.reason}: {data}")
        return data
    except Exception as e:
        st.error(f"Request failed: {e}")
        return None

# ---- Ingest UI ----
with st.expander("Ingest papers", expanded=True):
    q = st.text_input("arXiv query", value="large language models evaluation")
    n = st.number_input("max results", min_value=1, max_value=100, value=10)
    if st.button("Ingest"):
        data = post_json("/ingest", {"query": q, "max_results": int(n)})
        if data is not None:
            st.json(data)

# ---- Ask UI ----
st.subheader("Ask a question")
question = st.text_input("Question", value="What are current best practices for RAG evaluation?")
k = st.slider("Top-K", 1, 10, 5)
if st.button("Ask"):
    data = post_json("/ask", {"question": question, "k": int(k)})
    if data and "answer" in data:
        st.markdown("### Answer")
        st.write(data["answer"])
        st.markdown("### Sources")
        for i, s in enumerate(data.get("sources", []), start=1):
            title = s.get("title", "Untitled")
            link = s.get("link", "")
            published = s.get("published", "")
            authors = ", ".join(s.get("authors", []))
            st.markdown(f"**[{i}] {title}**  \n{link}  \n{published}  \n{authors}")
