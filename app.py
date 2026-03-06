import streamlit as st
from file_reader import read_file
from vector_store import create_vector_store

st.set_page_config(page_title="AI File Chatbot", layout="wide")

st.title("🤖 AI File Assistant")

# Store database in session
if "db" not in st.session_state:
    st.session_state.db = None

# Upload files
uploaded_files = st.file_uploader(
    "Upload files",
    accept_multiple_files=True
)

# Process files
if uploaded_files:

    text = ""

    for file in uploaded_files:
        file_text = read_file(file)

        if file_text:
            text += file_text + "\n"

    db = create_vector_store(text)

    if db:
        st.session_state.db = db
        st.success("✅ Files processed successfully!")
    else:
        st.warning("⚠️ No readable text found in files")

# Chat input
query = st.chat_input("Ask a question")

if query:

    st.write("### 💬 You:")
    st.write(query)

    db = st.session_state.db

    if db:

        docs = db.similarity_search(query)

        if docs:
            context = docs[0].page_content

            st.write("### 📄 Answer from document:")
            st.write(context)

        else:
            st.write("No relevant information found in uploaded files.")

    else:
        st.write("### 🤖 Assistant:")
        st.write("Please upload files so I can answer from them.")