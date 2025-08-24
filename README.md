# Chatbot Rag

Chatbot Rag adalah aplikasi chatbot berbasis Python yang menggunakan Supabase dan OpenAI untuk melakukan retrieval-augmented generation (RAG).

## Instalasi

1. Clone repository ini:
   ```bash
   git clone https://github.com/wildanmujjahid29/Kerja-Praktek-Chatbot-RAG.git chatbot-rag
   ```
   
   ```
   cd chatbot-rag
   ```
2. Buat dan aktifkan virtual environment (opsional tapi direkomendasikan):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Salin file `.env.example` menjadi `.env` dan isi dengan kredensial kamu:
   ```bash
   copy .env.example .env  # Windows
   # cp .env.example .env  # Linux/Mac
   ```

## Konfigurasi Environment

Isi file `.env` dengan variabel berikut:

```
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
OPENAI_API_KEY=your_openai_api_key
```

## Menjalankan Aplikasi

Jalankan aplikasi dengan:

```bash
uvicorn main:app --reload 
```

## Struktur Folder

- `main.py` : Entry point aplikasi
- `config.py` : Konfigurasi aplikasi
- `api/` : Endpoint API
- `schemas/` : Skema data
- `services/` : Logic (Supabase, Embedding, dsb)
