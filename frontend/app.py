import streamlit as st
import requests
import os 


st.set_page_config(page_title="VectorMind AI", page_icon="🤖", layout="wide")
st.title("VectorMind AI")

API_BASE = "http://backend:8000"  



# -------------------------
# Sidebar: File ingestion
# -------------------------
with st.sidebar:
    st.header("Ingest Documents")

    uploaded = st.file_uploader("Upload PDF or TXT or DOCX", type=["pdf", "txt", "docx"])
    if uploaded:
        st.write(f"File selected: {uploaded.name}")
        if st.button("Ingest File"):
            try:
                uploaded.seek(0)  
                files = {"file": (uploaded.name, uploaded.read(), uploaded.type)}
                r = requests.post(f"{API_BASE}/ingest/file", files=files)
                if r.status_code == 200:
                    st.success(f"File ingested successfully: {r.json()}")
                else:
                    st.error(f"Failed to ingest file: {r.text}")
            except Exception as e:
                st.error(f"Error: {e}")

# -------------------------
# Raw text ingestion
# -------------------------
st.divider()
text = st.text_area("Add raw text")
if st.button("Ingest Text") and text.strip():
    try:
        r = requests.post(f"{API_BASE}/ingest/text", json=[text.strip()])
        if r.status_code == 200:
            st.success(f"Text ingested successfully: {r.json()}")
        else:
            st.error(f"Failed to ingest text: {r.text}")
    except Exception as e:
        st.error(f"Error: {e}")

# -------------------------
# Chat with the model
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# User input
prompt = st.chat_input("Ask about your documents…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                r = requests.post(f"{API_BASE}/query/", json={"question": prompt, "k": 4})
                if r.status_code == 200:
                    data = r.json()
                    st.markdown(data.get("answer", "No answer returned."))
                    if data.get("sources"):
                        with st.expander("Sources"):
                            for s in data["sources"]:
                                st.write(s)
                else:
                    st.error(f"Query failed: {r.text}")
            except Exception as e:
                st.error(f"Error querying API: {e}")
