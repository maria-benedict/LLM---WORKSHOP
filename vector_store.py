from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer


# Wrapper so SentenceTransformer works with LangChain
class SentenceTransformerEmbeddings(Embeddings):

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

    def embed_query(self, text):
        return self.model.encode([text])[0].tolist()


def create_vector_store(text):

    # Safety check
    if text is None or text.strip() == "":
        return None

    # Split text into chunks
    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    # If no chunks created
    if len(chunks) == 0:
        return None

    # Load embedding model
    embeddings = SentenceTransformerEmbeddings()

    # Create FAISS vector database
    db = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )

    return db