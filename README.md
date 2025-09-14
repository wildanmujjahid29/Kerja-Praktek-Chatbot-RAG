# Chatbot RAG API

Backend API untuk Chatbot dengan Retrieval Augmented Generation (RAG) menggunakan FastAPI, Supabase, dan OpenAI.

## Fitur Utama

- **RAG Chatbot** - Sistem chat dengan retrieval dokumen menggunakan embedding
- **Knowledge Base Management** - Upload dan kelola dokumen (PDF, DOCX, TXT)
- **Admin Authentication** - Sistem login admin dengan JWT token
- **Dashboard Analytics** - Statistik penggunaan chat dan dokumen
- **Configuration Management** - Konfigurasi prompt AI dan API key
- **Content Filtering** - Filter topik sensitif dan tidak pantas

## Instalasi

1. Clone repository ini:

   ```bash
   git clone https://github.com/wildanmujjahid29/Kerja-Praktek-Chatbot-RAG.git chatbot-rag
   cd chatbot-rag
   ```

2. Buat dan aktifkan virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Salin dan konfigurasi environment:
   ```bash
   copy .env.example .env  # Windows
   # cp .env.example .env  # Linux/Mac
   ```

## Konfigurasi Environment

Isi file `.env` dengan variabel berikut:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
OPENAI_API_KEY=your_openai_api_key
JWT_SECRET=your_jwt_secret_key
```

## Menjalankan Aplikasi

```bash
uvicorn main:app --reload
```

API akan tersedia di: `http://127.0.0.1:8000`  
Documentation: `http://127.0.0.1:8000/docs`

## Endpoint API

### Admin Authentication

| Method                                                 | Endpoint         | Deskripsi                    | Auth Required |
| ------------------------------------------------------ | ---------------- | ---------------------------- | ------------- |
| ![POST](https://img.shields.io/badge/POST-brightgreen) | `/auth/register` | Registrasi admin baru        | ❌            |
| ![POST](https://img.shields.io/badge/POST-brightgreen) | `/auth/login`    | Login admin                  | ❌            |
| ![GET](https://img.shields.io/badge/GET-blue)          | `/auth/me`       | Info admin yang sedang login | ✅            |

### Chat Management

| Method                                                 | Endpoint                             | Deskripsi                     | Auth Required |
| ------------------------------------------------------ | ------------------------------------ | ----------------------------- | ------------- |
| ![POST](https://img.shields.io/badge/POST-brightgreen) | `/chat/session`                      | Membuat sesi chat baru        | ❌            |
| ![GET](https://img.shields.io/badge/GET-blue)          | `/chat/session/{session_id}`         | Mengambil detail sesi chat    | ❌            |
| ![POST](https://img.shields.io/badge/POST-brightgreen) | `/chat/session/{session_id}/message` | Mengirim pesan ke chatbot     | ❌            |
| ![GET](https://img.shields.io/badge/GET-blue)          | `/chat/sessions/user/{user_id}`      | Melihat daftar sesi chat user | ❌            |
| ![DELETE](https://img.shields.io/badge/DELETE-red)     | `/chat/session/{session_id}`         | Menghapus sesi chat           | ❌            |

### Dashboard Management

| Method                                        | Endpoint                            | Deskripsi                   | Auth Required |
| --------------------------------------------- | ----------------------------------- | --------------------------- | ------------- |
| ![GET](https://img.shields.io/badge/GET-blue) | `/dashboard/overview`               | Statistik overview aplikasi | ✅            |
| ![GET](https://img.shields.io/badge/GET-blue) | `/dashboard/monthly-analytics`      | Analitik bulanan            | ✅            |
| ![GET](https://img.shields.io/badge/GET-blue) | `/dashboard/monthly-daily-sessions` | Sesi harian per bulan       | ✅            |

### Knowledge Base Management

| Method                                                 | Endpoint                            | Deskripsi                      | Auth Required |
| ------------------------------------------------------ | ----------------------------------- | ------------------------------ | ------------- |
| ![POST](https://img.shields.io/badge/POST-brightgreen) | `/document/embed`                   | Upload & embed dokumen         | ✅            |
| ![GET](https://img.shields.io/badge/GET-blue)          | `/document`                         | Daftar semua dokumen           | ✅            |
| ![GET](https://img.shields.io/badge/GET-blue)          | `/document/service/{service_tag}`   | Dokumen berdasarkan tag        | ✅            |
| ![DELETE](https://img.shields.io/badge/DELETE-red)     | `/document/filename/{filename}`     | Hapus dokumen berdasarkan nama | ✅            |
| ![PUT](https://img.shields.io/badge/PUT-yellow)        | `/document/filename/{filename}/tag` | Update tag dokumen             | ✅            |
| ![DELETE](https://img.shields.io/badge/DELETE-red)     | `/document/filename/{filename}/tag` | Hapus tag dokumen              | ✅            |
| ![GET](https://img.shields.io/badge/GET-blue)          | `/document/tags`                    | Daftar tag dokumen unik        | ✅            |

### AI Configuration Management

| Method                                                 | Endpoint                      | Deskripsi                 | Auth Required |
| ------------------------------------------------------ | ----------------------------- | ------------------------- | ------------- |
| ![POST](https://img.shields.io/badge/POST-brightgreen) | `/chatbot/config`             | Buat konfigurasi prompt   | ✅            |
| ![GET](https://img.shields.io/badge/GET-blue)          | `/chatbot/config`             | Ambil konfigurasi prompt  | ✅            |
| ![PUT](https://img.shields.io/badge/PUT-yellow)        | `/chatbot/config/{config_id}` | Update konfigurasi prompt | ✅            |
| ![DELETE](https://img.shields.io/badge/DELETE-red)     | `/chatbot/config/{config_id}` | Hapus konfigurasi prompt  | ✅            |

### Token Configuration

| Method                                                 | Endpoint  | Deskripsi            | Auth Required |
| ------------------------------------------------------ | --------- | -------------------- | ------------- |
| ![GET](https://img.shields.io/badge/GET-blue)          | `/token/` | Ambil API key OpenAI | ✅            |
| ![POST](https://img.shields.io/badge/POST-brightgreen) | `/token/` | Set API key OpenAI   | ✅            |

### Test & RAG

| Method                                                 | Endpoint                  | Deskripsi               | Auth Required |
| ------------------------------------------------------ | ------------------------- | ----------------------- | ------------- |
| ![POST](https://img.shields.io/badge/POST-brightgreen) | `/rag`                    | Test jawaban RAG        | ✅            |



## Arsitektur Sistem

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │───>│   FastAPI       │───>│   Supabase      │
│   (Client)      │    │   Backend       │    │   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   OpenAI API    │
                       │   (Embeddings   │
                       │   & Chat)       │
                       └─────────────────┘
```

## Struktur Proyek

```
chatbot-rag/
├── main.py                   # Entry point aplikasi FastAPI
├── config.py                 # Konfigurasi database & API
├── requirements.txt          # Dependencies Python
├── README.md                 # Dokumentasi proyek
├── .env.example              # Template environment variables
├── api/                      # Router endpoints
│   ├── auth_router.py        # Authentication endpoints
│   ├── chat_router.py        # Chat management endpoints
│   ├── dashboard_router.py   # Dashboard analytics endpoints
│   ├── document_router.py    # Document management endpoints
│   ├── prompt_router.py      # AI configuration endpoints
│   ├── config_router.py      # API key configuration endpoints
│   ├── rag_router.py         # RAG testing endpoints
│   └── retrieval_router.py   # Document retrieval testing
├── services/                 # Business logic layer
│   ├── auth_service.py       # Authentication logic
│   ├── chat_service.py       # Chat session management
│   ├── dashboard_service.py  # Analytics & statistics
│   ├── document_service.py   # Document CRUD operations
│   ├── embed_service.py      # Document embedding processing
│   ├── prompt_service.py     # AI prompt management
│   ├── config_service.py     # Configuration management
│   ├── rag_service.py        # RAG & AI response logic
│   └── retrieval_service.py  # Document similarity search
├── schemas/                  # Pydantic data models
│   ├── chat_schemas.py       # Chat data structures
│   ├── dashboard_schemas.py  # Analytics data structures
│   ├── document_schemas.py   # Document data structures
│   ├── prompt_schemas.py     # AI config data structures
│   ├── config_schemas.py     # Configuration data structures
│   └── rag_schemas.py        # RAG response data structures
├── dependencies/             # FastAPI dependencies
│   └── auth_deps.py          # Authentication dependencies
└── utils/                    # Utility functions
    └── auth_utils.py         # JWT & password utilities
```

## Fitur Teknis

### Authentication

- **JWT Token** dengan expiration time
- **Password hashing** menggunakan bcrypt
- **Role-based access** untuk admin
- **Protected endpoints** dengan dependency injection

### Document Processing

- **Multi-format support**: PDF, DOCX, TXT
- **Text chunking** dengan overlap untuk konteks
- **Vector embeddings** menggunakan OpenAI text-embedding-3-small
- **Similarity search** dengan normalized vectors
- **Service tagging** untuk organisasi dokumen

### RAG System

- **Semantic search** untuk retrieval dokumen
- **Context building** dengan source attribution
- **Content filtering** untuk topik sensitif
- **Fallback responses** ketika tidak ada konteks
- **Configurable parameters** (k, similarity threshold)

### Analytics

- **Real-time statistics** untuk admin dashboard
- **Monthly trends** untuk usage analytics
- **Daily session tracking** per bulan
- **Document usage** monitoring

### CORS Configuration

- **Cross-Origin Resource Sharing** enabled untuk frontend integration
- **Flexible origins** dengan wildcard support
- **Credentials support** untuk authenticated requests

## Deployment

### Development

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Author

**Wildan Mujjahid** - [@wildanmujjahid29](https://github.com/wildanmujjahid29)
