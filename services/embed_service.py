import os

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

def embedding_text_from_file(service_id:str, file_path: str, original_filename: str):
    extension = original_filename.split(".")[-1].lower()
    text = load_text_from_file(file_path)
    # Chunking
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    result = []
    for chunk in chunks:
        # Generate Embedding
        vector = embeddings.embed_query(chunk)
        # Store in Supabase
        data = {
            "service_id": service_id,
            "content": chunk,
            "embedding": vector,
            "filename" : original_filename,
            "file_type": extension
        }
        supabase.table(TABLE_NAME).insert(data).execute()
        result.append(data)
    return result
