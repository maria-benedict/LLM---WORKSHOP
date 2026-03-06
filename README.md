# AI File Assistant 🤖📂

An AI-powered file assistant that can read multiple file types and answer questions from them.

Built using **Python, Streamlit, LangChain, FAISS, and Sentence Transformers**.

---

# Features

- Upload multiple files
- Ask questions about documents
- AI-powered semantic search
- Supports multiple file formats

Supported formats:

- PDF
- DOCX
- TXT
- CSV
- Excel
- Images (OCR optional)

---

# Tech Stack

- Python
- Streamlit
- LangChain
- FAISS Vector Database
- Sentence Transformers
- Pandas
- PyPDF
- Python-docx

---

# How it Works

1. User uploads files
2. Files are converted into text
3. Text is split into chunks
4. Chunks are converted into embeddings
5. Stored in FAISS vector database
6. User question is matched with relevant chunks
7. AI generates answer from context

---

# Installation

Clone the repository
