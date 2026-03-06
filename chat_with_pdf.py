import streamlit as st
import requests
import os
import time
import numpy as np
import faiss
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

st.set_page_config(page_title="Industry AI Assistant", page_icon="🤖", layout="wide")

st.sidebar.title("🏆 Industry-Level AI")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF(s)",
    type="pdf",
    accept_multiple_files=True
)

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []

st.title("🏆 Industry-Level RAG Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "index" not in st.session_state:
    st.session_state.index = None
    st.session_state.chunks = None

# ----------- Embedding Model (Local) -----------

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ----------- Extract + Chunk -----------

def extract_text(files):
    text = ""
    for file in files:
        reader = PdfReader(file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    return text

def chunk_text(text, chunk_size=500):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

# ----------- Build Vector Index -----------

if uploaded_files:
    raw_text = extract_text(uploaded_files)
    chunks = chunk_text(raw_text)

    embeddings = embedding_model.encode(chunks)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    st.session_state.index = index
    st.session_state.chunks = chunks

    st.success("✅ Documents indexed successfully!")

# ----------- Display Mode Badge -----------

if st.session_state.index:
    st.markdown("🟢 **PDF RAG Mode (Vector Search Enabled)**")
else:
    st.markdown("🔵 **Normal Chat Mode**")

st.markdown("---")

# ----------- Display Chat History -----------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask your question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # ----------- VECTOR SEARCH -----------

    if st.session_state.index:
        question_embedding = embedding_model.encode([user_input])
        D, I = st.session_state.index.search(
            np.array(question_embedding), k=5
        )

        relevant_chunks = [st.session_state.chunks[i] for i in I[0]]

        context = "\n\n".join(relevant_chunks)

        system_prompt = f"""
        Answer the question using ONLY the context below.
        If not found, say it's not in the document.

        Context:
        {context}
        """
    else:
        system_prompt = "You are a helpful AI assistant."

    messages_to_send = [
        {"role": "system", "content": system_prompt}
    ] + st.session_state.messages

    data = {
        "model": "qwen/qwen-turbo",
        "messages": messages_to_send
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if "error" in result:
        answer = result["error"]["message"]
    else:
        answer = result["choices"][0]["message"]["content"]

    # ----------- Streaming Effect -----------

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for char in answer:
            full_response += char
            message_placeholder.markdown(full_response)
            time.sleep(0.003)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )