import os
import re
import unicodedata
import numpy as np

from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader,TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import supabase

# OpenAI Embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=os.getenv("OPENAI_API_KEY"))

TABLE_NAME = "documents"

def load_text_from_file(file_path: str):
    file_extension = file_path.split(".")[-1].lower()
    if file_extension == 'pdf':
        loader = PyPDFLoader(file_path)
    elif file_extension == 'docx':
        loader = Docx2txtLoader(file_path)
    elif file_extension == 'txt':
        loader = TextLoader(file_path)
    else:
        raise ValueError("Unsupported file type. Please provide a PDF, DOCX, or TXT file.")
    docs = loader.load()
    return "\n".join([doc.page_content for doc in docs])


def preprocess_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)  # normalisasi unicode
    text = re.sub(r"[^a-zA-Z0-9.,;:!?()\-\s]", "", text)  # hilangkan karakter aneh
    text = re.sub(r"\s+", " ", text)  # rapikan spasi
    return text.strip()


def normalize_vector(vec):
    vec = np.array(vec)
    norm = np.linalg.norm(vec)
    return (vec / norm).tolist() if norm > 0 else vec.tolist()


def embedding_text_from_file(service_id:str, file_path: str, original_filename: str):
    extension = original_filename.split(".")[-1].lower()
    
    # Load and preprocess text
    text = load_text_from_file(file_path)
    text = preprocess_text(text)
    
    # Chunking
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150, separators=["\n\n", "\n", ". ", " ", ""])
    chunks = splitter.split_text(text)
    
    result = []
    for chunk in chunks:
        if not chunk.strip():
            continue
        # Generate Embedding
        vector = embeddings.embed_documents([chunk])[0]
        vector = normalize_vector(vector)  # normalisasi sebelum simpan

        # Store in Supabase
        data = {
            "service_id": service_id,
            "content": chunk,
            "embedding": vector,
            "filename": original_filename,
            "file_type": extension
        }
        supabase.table(TABLE_NAME).insert(data).execute()
        result.append(data)

    return result
