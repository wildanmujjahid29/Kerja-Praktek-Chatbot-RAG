import os
from typing import Any, Dict, List

from openai import OpenAI

from services.prompt_service import get_prompt_db
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
        else "Kamu adalah asisten yang membantu. Hanya jawab menggunakan konteks yang diberikan. Jangan jawab pertanyaan diluar konteks. Jika jawaban tidak ada dalam konteks, katakan bahwa kamu tidak memiliki informasi yang cukup."

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

def check_restricted_topics(query: str) -> bool:
    # Daftar kata kunci sensitif yang di-hardcode di backend
    restricted_keywords = [
        # Politik
        'jokowi', 'widodo', 'megawati', 'prabowo', 'subianto', 'anies', 'baswedan', 
        'ganjar', 'pranowo', 'ahok', 'ridwan kamil', 'sandi', 'sandiaga', 'maruf', 'amin',
        'surya paloh', 'airlangga', 'puan maharani', 'muhaimin', 'cak imin',
        'presiden', 'wakil presiden', 'menteri', 'gubernur', 'bupati', 'walikota',
        'dpr', 'dprd', 'mpr', 'kpu', 'pemilu', 'pilpres', 'pilgub', 'pilkada',
        'partai', 'politik', 'pemerintah', 'kabinet', 'koalisi', 'oposisi',
        'pdip', 'gerindra', 'golkar', 'nasdem', 'pks', 'pan', 'ppp', 'demokrat',
        
        # SARA dan konten sensitif
        'rasis', 'rasisme', 'sara', 'suku', 'agama', 'ras', 'antar golongan',
        'islam', 'kristen', 'katolik', 'hindu', 'buddha', 'konghucu',
        'teroris', 'terorisme', 'radikal', 'radikalisme', 'ekstremis',
        
        # Konten dewasa/tidak pantas
        'seks', 'pornografi', 'telanjang', 'bugil', 'porno',
        'narkoba', 'drugs', 'ganja', 'marijuana', 'kokain', 'heroin',
        'kekerasan', 'pembunuhan', 'bunuh', 'mati', 'suicide', 'bunuh diri',
        
        # Hate speech
        'benci', 'kebencian', 'sarkasme', 'hinaan', 'caci maki',
        'bodoh', 'tolol', 'goblok', 'idiot', 'bangsat'
    ]
    
    # Ubah query ke lowercase untuk pencocokan
    query_lower = query.lower()
    print(f"DEBUG: query_lower='{query_lower}'")
    
    # Periksa setiap kata kunci sensitif
    for keyword in restricted_keywords:
        if keyword in query_lower:
            print(f"DEBUG: RESTRICTED TOPIC FOUND! keyword='{keyword}' detected in query")
            return True
    
    print("DEBUG: No restricted topic found")
    return False

def run_rag(query: str, k: int, min_similarity: float = 0.5) -> Dict[str, Any]:
    # Cek apakah query mengandung topik sensitif/terlarang
    if check_restricted_topics(query):
        return {
            "answer": "Maaf saya tidak bisa menjawab pertanyaan anda",
            "sources": [],
            "used_k": 0,
            "query": query,
            "is_restricted_topic": True
        }
    
    # Ambil Primary Prompt & Fallback Response dari DB
    prompt_data = get_prompt_db()
    if not prompt_data:
        return {
            "answer": "Maaf, saya tidak dapat menjawab pertanyaan Anda saat ini.",
            "sources": [],
            "used_k": 0,
            "query": query,
            "is_fallback": True
        }

    primary_prompt = prompt_data.get("prompt", "")
    fallback_response = prompt_data.get("fallback_response")

    # Retrieval dokumen (Top-K)
    hits = search_similar_documents(
        query=query,
        match_threshold=min_similarity,
        match_count=k
    ) or []

    # Kalau tidak ada dokumen yang match → fallback response dari database
    if not hits:
        final_fallback = fallback_response if fallback_response else "Maaf, saya tidak dapat menjawab pertanyaan Anda saat ini."
        return {
            "answer": final_fallback,
            "sources": [],
            "used_k": 0,
            "query": query,
            "is_fallback": True
        }

    # Ada dokumen → build context dan panggil LLM
    context_blocks = build_context_block(hits)
    completion = llm_model.chat.completions.create(
        model="gpt-4o-mini",
        messages=build_messages(primary_prompt, query, context_blocks),
        max_tokens=400,
        temperature=0.2,
    )
    answer = completion.choices[0].message.content.strip()

    sources = [
        {
            "index": i + 1,
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
        "is_fallback": False
    }
