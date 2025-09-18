from functools import lru_cache
from typing import Dict, List, Optional

import numpy as np
from langchain_openai import OpenAIEmbeddings

from config import get_api_key, supabase


@lru_cache(maxsize=1)
def get_embeddings() -> Optional[OpenAIEmbeddings]:
    api_key = get_api_key()
    if not api_key:
        return None
    return OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)

def normalize_vector(vec: List[float]) -> List[float]:
    vec = np.array(vec)
    norm = np.linalg.norm(vec)
    return (vec / norm).tolist() if norm > 0 else vec.tolist()

def search_similar_documents(
    query: str,
    match_threshold: float = 0.4,
    match_count: int = 5
) -> List[Dict]:
    try:
        # Pastikan API key tersedia
        embedder = get_embeddings()
        if embedder is None:
            print("Embeddding model tidak tersedia karena API key tidak diset.")
            return []

        # Buat embedding untuk query
        query_embedding = embedder.embed_query(query)
        query_embedding = normalize_vector(query_embedding)

        # Panggil Postgres function match_documents
        response = supabase.rpc(
            'match_documents',
            {
                'query_embedding': query_embedding,
                'match_threshold': match_threshold,
                'match_count': match_count
            }
        ).execute()

        results = response.data if response.data else []

        # Filter manual untuk lebih ketat
        filtered_results = [
            r for r in results if r.get("similarity", 0) >= match_threshold
        ]

        return filtered_results
    except Exception as e:
        print(f"Error in similarity search: {e}")
        return []

def get_context_from_results(search_results: List[Dict]) -> str:
    if not search_results:
        return ""

    context_parts = []
    for i, result in enumerate(search_results, 1):
        context_parts.append(
            f"[Dokumen {i} - {result.get('filename', 'unknown')}]\n"
            f"Similarity: {result.get('similarity', 0):.2f}\n"
            f"Content: {result.get('content', '')}\n"
        )

    return "\n---\n".join(context_parts)
