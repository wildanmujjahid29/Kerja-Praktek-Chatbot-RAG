from typing import Any, Dict, List

from openai import OpenAI

from config import get_api_key
from services.prompt_service import get_prompt_db
from services.retrieval_service import get_context_from_results, search_similar_documents

llm_model = OpenAI(api_key=get_api_key())

def build_context_block(hits: List[Dict], max_chars_per_block: int = 800) -> List[str]:
    blocks = []
    for i, r in enumerate(hits, 1):
        content = " ".join((r.get("content") or "").split())
        if len(content) > max_chars_per_block:
            content = content[:max_chars_per_block].rstrip() + " ..."
        filename = r.get("filename") or "unknown"
        sim = r.get("similarity", 0.0)
        blocks.append(f"[{i}] filename: {filename} | similarity: {sim:.2f}\n{content}")
    return blocks


def build_messages(primary_prompt: str, query: str, context: str, fallback_response: str | None = None) -> List[Dict[str, str]]:
    system_msg = (
        primary_prompt.strip()
        if primary_prompt and primary_prompt.strip()
        else (
            "Kamu adalah asisten yang membantu.\n"
            "Jawab pertanyaan pengguna HANYA berdasarkan konteks berikut.\n"
            "Jika jawaban tidak ada di konteks, jawab dengan sopan bahwa informasi tidak tersedia "
            "dan di akhir tambahkan fallback response.\n"
            "Instruksi tambahan:\n"
            "- Sebutkan fakta secara ringkas dan ramah.\n"
            "- Jangan jawab pertanyaan di luar konteks.\n"
            "- Jangan gunakan karakter yang berlebih dan tidak perlu.\n"
        )
    )

    if not primary_prompt and fallback_response:
        system_msg += f"\nFallback default: {fallback_response}"

    context_final = context if context else "(tidak ada konteks relevan)"

    return [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": f"KONTEKS:\n{context_final}\n\nPERTANYAAN:\n{query}"}
    ]

def check_restricted_topics(query: str) -> bool:
    restricted_keywords = [
        # Politik
        'jokowi', 'widodo', 'megawati', 'prabowo', 'anies', 'baswedan',
        'ganjar', 'pranowo', 'ahok', 'ridwan kamil', 'sandiaga', 'maruf',
        'presiden', 'wakil presiden', 'menteri', 'gubernur', 'bupati',
        'pemilu', 'politik', 'partai',
        # Konten dewasa/narkoba
        'seks', 'pornografi', 'telanjang', 'bugil', 'porno',
        'narkoba', 'ganja', 'kokain', 'heroin', 'drugs',
        # Kekerasan / bunuh diri
        'bunuh', 'bunuh diri', 'suicide', 'pembunuhan', 'violence',
        # Hate speech
        'benci', 'hinaan', 'caci maki', 'bodoh', 'tolol', 'goblok'
    ]
    query_lower = query.lower()
    return any(kw in query_lower for kw in restricted_keywords)


def handle_fallback(query: str, message: str, is_restricted: bool = False) -> Dict[str, Any]:
    return {
        "answer": message,
        "sources": [],
        "used_k": 0,
        "query": query,
        "is_fallback": not is_restricted,
        "is_restricted_topic": is_restricted
    }


def run_rag(query: str, k: int = 5, min_similarity: float = 0.7) -> Dict[str, Any]:
    # Cek topik yang dibatasi lebih dulu
    if check_restricted_topics(query):
        return handle_fallback(
            query=query,
            message="Maaf, pertanyaan Anda termasuk topik yang dibatasi dan tidak dapat saya bahas.",
            is_restricted=True,
        )

    # Ambil Primary Prompt & Fallback dari DB (tahan terhadap None)
    prompt_data = get_prompt_db() or {}
    primary_prompt = prompt_data.get("prompt", "")
    fallback_response = prompt_data.get("fallback_response", "Maaf, saya tidak bisa menjawab pertanyaan Anda.")

    # Retrieval dari Supabase
    hits = search_similar_documents(
        query=query,
        match_threshold=min_similarity,
        match_count=k
    )

    # Kalau kosong Kirimakan fallback
    if not hits:
        return {
            "answer": f"Saya belum menemukan jawaban yang pas dari knowledge base. {fallback_response}",
            "sources": [],
            "used_k": 0,
            "query": query,
            "is_fallback": True
        }

    # Ada hasil format context
    context = get_context_from_results(hits)

    # Panggil LLM
    try:
        completion = llm_model.chat.completions.create(
            model="gpt-4o-mini",
            messages=build_messages(primary_prompt, query, context, fallback_response),
            max_tokens=400,
            temperature=0.2,
        )
        answer = completion.choices[0].message.content.strip()
    except Exception:
        # Jika terjadi error (mis. API key tidak tersedia/koneksi), gunakan fallback
        return {
            "answer": f"Terjadi kendala saat menghasilkan jawaban. {fallback_response}",
            "sources": [],
            "used_k": len(hits),
            "query": query,
            "is_fallback": True
        }

    # Siapkan response
    sources = [
        {
            "index": i + 1,
            "id": r.get("id"),
            "content": r.get("content"),
            "filename": r.get("filename"),
            "tag": r.get("service_tag"),
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