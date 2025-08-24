import os
from typing import List, Dict, Any, Tuple
from openai import OpenAI

from services.retrieval_service import search_similar_documents
from services.prompt_service import get_prompt_db

llm_model = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Format context singkat agar muat token
def build_context_block(hits: List[Dict], max_chars_per_block: int = 800) -> List[str]:
    blocks = []
    for i, r in enumerate(hits, 1):
        content = " ".join((r.get("content") or "").split())
        if len(content) > max_chars_per_block:
            content = content[:max_chars_per_block].rstrip() + " ..."
        filename = r.get("filename") or "unknown"
        sim = r.get("similarity", 0.0)
        blocks.append(
            f"[{i}] filename: {filename} | similarity: {sim:.2f}\n{content}"
        )
    return blocks

def build_messages(primary_prompt: str, query: str, context_blocks: List[str]) -> List[Dict[str, str]]:
    system_msg = (
        primary_prompt.strip()
        if primary_prompt and primary_prompt.strip()
        else "Kamu adalah asisten yang membantu. Hanya jawab menggunakan konteks yang diberikan. Jika jawaban tidak ada dalam konteks, katakan bahwa kamu tidak memiliki informasi yang cukup."
    )
    context_joined = "\n\n---\n\n".join(context_blocks) if context_blocks else "(no context)"
    user_msg = (
        "Jawab pertanyaan pengguna HANYA berdasarkan konteks berikut. "
        "Jika tidak ada jawaban di konteks, jawab dengan sopan bahwa informasi tidak tersedia.\n\n"
        f"KONTEKS:\n{context_joined}\n\n"
        f"PERTANYAAN:\n{query}\n\n"
        "Instruksi tambahan:\n"
        "- Sebutkan fakta secara ringkas dan to the point.\n"
    )
    return [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ]

def run_rag(service_id: str, query: str, k: int, min_similarity: float=0.5) -> Dict[str, Any]:
    # Ambil Primary Promt
    prompt = get_prompt_db(service_id)
    primary_prompt = (prompt or {}).get("prompt", "")
    
    # Retrieval top-K
    hits = search_similar_documents(
        service_id=service_id, 
        query=query, 
        match_threshold=min_similarity, 
        match_count=k
    ) or []

    # Susun context
    context_blocks = build_context_block(hits)
    
    # Bangun Message untuk llm
    completion = llm_model.chat.completions.create(
        model="gpt-4o-mini",
        messages=build_messages(primary_prompt, query, context_blocks),
        max_tokens=400,
        temperature=0.2,
    )
    answer = completion.choices[0].message.content.strip()

    # Kembalikan jawaban
    sources = [
        {
            "index" : i + 1,
            "filename": r.get("filename"),
            "similarity": round(r.get("similarity", 0.0), 4),
        }
        for i, r in enumerate(hits)
    ]
    
    return {
        "answer": answer,
        "sources": sources,
        "used_k": len(hits),
        "query": query,
    }
