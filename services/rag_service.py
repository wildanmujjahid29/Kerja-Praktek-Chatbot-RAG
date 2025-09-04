import os
import re
from typing import Any, Dict, List, Tuple

from openai import OpenAI

from services.prompt_service import get_prompt_db
from services.restricted_topics_service import get_active_topics_db
from services.retrieval_service import search_similar_documents

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

def check_restricted_topics(prompt_id: str, query: str) -> bool:
    # Ambil daftar topik aktif yang terlarang
    restricted_topics = get_active_topics_db(prompt_id)
    if not restricted_topics:
        return False
    
    # Ubah query ke lowercase untuk pencocokan yang lebih baik
    query_lower = query.lower()
    print(f"DEBUG - Memeriksa query: '{query_lower}' untuk topik terlarang")
    
    # Periksa setiap topik terlarang
    for topic_data in restricted_topics:
        topic = topic_data.get("topic", "").lower()
        if not topic:
            continue
            
        print(f"DEBUG - Memeriksa topik: '{topic}'")
        
        # Cek apakah topik disebutkan dalam query
        if topic in query_lower:
            print(f"DEBUG - Topik terlarang '{topic}' ditemukan dalam query")
            return True
    
    print(f"DEBUG - Tidak ada topik terlarang dalam query")
    return False

def run_rag(service_id: str, query: str, k: int, min_similarity: float=0.5) -> Dict[str, Any]:
    # Ambil Primary Prompt dan Fallback Response
    prompt_data = get_prompt_db(service_id)
    if not prompt_data:
        return {
            "answer": "Maaf, saya tidak dapat menjawab pertanyaan Anda saat ini.",
            "sources": [],
            "used_k": 0,
            "query": query,
            "is_fallback": True
        }
    
    prompt_id = prompt_data.get("id")
    primary_prompt = prompt_data.get("prompt", "")
    fallback_response = prompt_data.get("fallback_response")
    
    # Periksa topik terlarang
    if check_restricted_topics(prompt_id, query):
        print(f"DEBUG - Query '{query}' mengandung topik terlarang - mengirim pesan penolakan")
        return {
            "answer": "Maaf saya tidak bisa menjawab pertanyaan anda",
            "sources": [],
            "used_k": 0,
            "query": query,
            "is_restricted_topic": True
        }
    
    # Retrieval top-K
    hits = search_similar_documents(
        service_id=service_id, 
        query=query, 
        match_threshold=min_similarity, 
        match_count=k
    ) or []

    # Susun context
    context_blocks = build_context_block(hits)
    
    # Gunakan fallback jika tidak ada hasil yang cocok
    if not hits:
        # Langsung gunakan fallback response dari database tanpa proses_fallback_response
        final_fallback = fallback_response if fallback_response else "Maaf, saya tidak dapat menjawab pertanyaan Anda saat ini."
        print(f"DEBUG - Tidak ada dokumen relevan - menggunakan fallback response: '{final_fallback[:50]}...'")
        return {
            "answer": final_fallback,
            "sources": [],
            "used_k": 0,
            "query": query,
            "is_fallback": True
        }
    
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
