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

## Endpoint API

<!-- ### Chat

| Method                                                 | Endpoint                             | Deskripsi                  |
| ------------------------------------------------------ | ------------------------------------ | -------------------------- |
| ![POST](https://img.shields.io/badge/POST-brightgreen) | `/chat/session`                      | Membuat sesi chat baru     |
| ![GET](https://img.shields.io/badge/GET-blue)          | `/chat/session/{session_id}`         | Mengambil detail sesi chat |
| ![DELETE](https://img.shields.io/badge/DELETE-red)     | `/chat/session/{session_id}`         | Menghapus sesi chat        |
| ![GET](https://img.shields.io/badge/GET-blue)          | `/chat/sessions/{service_id}`        | Melihat daftar sesi chat   |
| ![POST](https://img.shields.io/badge/POST-brightgreen) | `/chat/session/{session_id}/message` | Mengirim pesan ke chatbot  | -->

### RAG

| Method                                                 | Endpoint            | Deskripsi               |
| ------------------------------------------------------ | ------------------- | ----------------------- |
| ![POST](https://img.shields.io/badge/POST-brightgreen) | `/rag/{service_id}` | Jawaban RAG (retrieval) |

### Documents

| Method                                                 | Endpoint                            | Deskripsi                   |
| ------------------------------------------------------ | ----------------------------------- | --------------------------- |
| ![POST](https://img.shields.io/badge/POST-brightgreen) | `/document/embed`                   | Melakukan embed dokumen     |
| ![GET](https://img.shields.io/badge/GET-blue)          | `/document/{service_id}`            | Melihat daftar dokumen unik |
| ![DELETE](https://img.shields.io/badge/DELETE-red)     | `/document/{service_id}/{filename}` | Menghapus dokumen           |

### Retrieval

| Method                                                 | Endpoint                  | Deskripsi             |
| ------------------------------------------------------ | ------------------------- | --------------------- |
| ![POST](https://img.shields.io/badge/POST-brightgreen) | `/retrieval/{service_id}` | Tes retrieval dokumen |

### Services

| Method                                                 | Endpoint                | Deskripsi                |
| ------------------------------------------------------ | ----------------------- | ------------------------ |
| ![GET](https://img.shields.io/badge/GET-blue)          | `/service`              | Melihat daftar service   |
| ![POST](https://img.shields.io/badge/POST-brightgreen) | `/service`              | Membuat service baru     |
| ![GET](https://img.shields.io/badge/GET-blue)          | `/service/{service_id}` | Mengambil detail service |
| ![PUT](https://img.shields.io/badge/PUT-yellow)        | `/service/{service_id}` | Mengubah data service    |
| ![DELETE](https://img.shields.io/badge/DELETE-red)     | `/service/{service_id}` | Menghapus service        |

### Prompts

| Method                                                 | Endpoint               | Deskripsi           |
| ------------------------------------------------------ | ---------------------- | ------------------- |
| ![POST](https://img.shields.io/badge/POST-brightgreen) | `/prompt`              | Membuat prompt baru |
| ![GET](https://img.shields.io/badge/GET-blue)          | `/prompt/{service_id}` | Mengambil prompt    |
| ![PUT](https://img.shields.io/badge/PUT-yellow)        | `/prompt/{prompt_id}`  | Mengubah prompt     |
| ![DELETE](https://img.shields.io/badge/DELETE-red)     | `/prompt/{prompt_id}`  | Menghapus prompt    |

## Struktur Folder

| Nama/Folder        | Keterangan                                     |
| ------------------ | ---------------------------------------------- |
| `main.py`          | Entry point aplikasi (FastAPI app)             |
| `config.py`        | Konfigurasi aplikasi & koneksi Supabase/OpenAI |
| `api/`             | Kumpulan file router/endpoint API              |
| `schemas/`         | Skema data (Pydantic models)                   |
| `services/`        | Logic utama: akses database, RAG, embed, dsb   |
| `requirements.txt` | Daftar dependencies Python                     |
| `README.md`        | Dokumentasi proyek                             |
