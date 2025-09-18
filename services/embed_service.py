import re
import unicodedata

import numpy as np
from chonkie import SentenceChunker
from langchain_community.document_loaders import (Docx2txtLoader, PyPDFLoader,
                                                  TextLoader)
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import get_api_key, supabase

# OpenAI Embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=get_api_key())

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


def load_text_from_input():
    # placeholder (unused) – keeping for backward compatibility if referenced elsewhere
    raise NotImplementedError("Use direct content string instead of load_text_from_input()")

def preprocess_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)  # normalisasi unicode
    text = re.sub(r"[^a-zA-Z0-9.,;:!?()\-\s]", "", text)  # hilangkan karakter aneh
    text = re.sub(r"\s+", " ", text)  # rapikan spasi
    return text.strip()

def normalize_vector(vec):
    vec = np.array(vec)
    norm = np.linalg.norm(vec)
    return (vec / norm).tolist() if norm > 0 else vec.tolist()


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100):
    chunker = SentenceChunker(
        tokenizer_or_token_counter="gpt2",
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        min_sentences_per_chunk=1
    )
    return [chunk.text for chunk in chunker.chunk(text)]


def embedding_text_from_file(file_path: str, original_filename: str, service_tag: str = None):
    extension = original_filename.split(".")[-1].lower()

    # Load & preprocess
    text = load_text_from_file(file_path)
    text = preprocess_text(text)

    # Chunk pakai Chonkie
    chunks = chunk_text(text)

    result = []
    for chunk in chunks:
        if not chunk.strip():
            continue

        # Embedding
        vector = embeddings.embed_documents([chunk])[0]
        vector = normalize_vector(vector)

        # Simpan ke Supabase
        data = {
            "content": chunk,
            "embedding": vector,
            "filename": original_filename,
            "file_type": extension,
            "service_tag": service_tag
        }
        supabase.table(TABLE_NAME).insert(data).execute()
        result.append(data)

    return result


def embedding_text_from_input(content: str, virtual_filename: str = None, service_tag: str = None):
    """Embedding untuk input teks langsung (tanpa file fisik).

    virtual_filename: nama simbolis (misal "manual-input" atau title) untuk konsistensi penyimpanan.
    """
    if not content or not content.strip():
        return []

    virtual_filename = virtual_filename or "manual-input.txt"
    extension = virtual_filename.split('.')[-1].lower() if '.' in virtual_filename else 'txt'

    # preprocess & chunk
    text = preprocess_text(content)
    chunks = chunk_text(text)

    result = []
    for chunk in chunks:
        if not chunk.strip():
            continue
        vector = embeddings.embed_documents([chunk])[0]
        vector = normalize_vector(vector)
        data = {
            "content": chunk,
            "embedding": vector,
            "filename": virtual_filename,
            "file_type": extension,
            "service_tag": service_tag
        }
        supabase.table(TABLE_NAME).insert(data).execute()
        result.append(data)
    return result
