import os
import re
import unicodedata

import numpy as np
from langchain_community.document_loaders import (Docx2txtLoader, PyPDFLoader,
                                                  TextLoader)
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
        docs = loader.load()
        return "\n".join([doc.page_content for doc in docs])
    elif file_extension == 'docx':
        loader = Docx2txtLoader(file_path)
        docs = loader.load()
        return "\n".join([doc.page_content for doc in docs])
    elif file_extension == 'txt':
        # Custom text loading with encoding handling
        try:
            # Try UTF-8 first
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            try:
                # Try UTF-8 with ignore errors
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    return file.read()
            except:
                try:
                    # Try cp1252 (Windows encoding)
                    with open(file_path, 'r', encoding='cp1252') as file:
                        return file.read()
                except:
                    # Last resort - latin-1
                    with open(file_path, 'r', encoding='latin-1') as file:
                        return file.read()
    else:
        raise ValueError("Unsupported file type. Please provide a PDF, DOCX, or TXT file.")


def preprocess_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)  # normalisasi unicode
    text = re.sub(r"[^a-zA-Z0-9.,;:!?()\-\s]", "", text)  # hilangkan karakter aneh
    text = re.sub(r"\s+", " ", text)  # rapikan spasi
    return text.strip()


def normalize_vector(vec):
    vec = np.array(vec)
    norm = np.linalg.norm(vec)
    return (vec / norm).tolist() if norm > 0 else vec.tolist()


def embedding_text_from_file(file_path: str, original_filename: str, service_tag: str = None):
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
            "content": chunk,
            "embedding": vector,
            "filename": original_filename,
            "file_type": extension,
            "service_tag": service_tag  # Optional tag for admin categorization
        }
        supabase.table(TABLE_NAME).insert(data).execute()
        result.append(data)

    return result
