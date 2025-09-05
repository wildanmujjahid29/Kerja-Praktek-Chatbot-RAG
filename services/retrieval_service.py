import os
from typing import Dict, List

import numpy as np
from langchain_openai import OpenAIEmbeddings

from config import supabase

# OpenAI Embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=os.getenv("OPENAI_API_KEY"))

def normalize_vector(vec):
    vec = np.array(vec)
    norm = np.linalg.norm(vec)
    return (vec / norm).tolist() if norm > 0 else vec.tolist()

def search_similar_documents(
    query: str, 
    match_threshold: float = 0.7, 
    match_count: int = 5
) -> List[Dict]:
    try:
        query_embedding = embeddings.embed_query(query)
        query_embedding = normalize_vector(query_embedding)
        response = supabase.rpc(
            'match_documents',
            {
                'query_embedding' : query_embedding,
                'match_threshold' : match_threshold,
                'match_count' : match_count
            }
        ).execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"Error in similarity search: {e}")
        return []

def get_context_from_results(search_results: List[Dict]) -> str:
    if not search_results:
        return "Tidak ada informasi relevan ditemukan."

    context_parts = []
    for i, result in enumerate(search_results, 1):
        context_parts.append(
            f"[Dokumen {i} - {result['filename']}]\n"
            f"Similarity: {result['similarity']:.2f}\n"
            f"Content: {result['content']}\n"
        )
    
    return "\n---\n".join(context_parts)