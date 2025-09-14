from fastapi import FastAPI
from fastapi.security import HTTPBearer

from api.auth_router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from api.chat_router import router as chat_router
from api.config_router import router as config_router
from api.dashboard_router import router as dashboard_router
from api.document_router import router as document_router
from api.prompt_router import router as prompt_router
from api.rag_router import router as rag_router

# Security scheme for Swagger UI
security = HTTPBearer()

app = FastAPI(
    title="Chatbot RAG API",
    description="Backend API untuk Chatbot dengan Retrieval Augmented Generation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def root():
    return {
        "message": "Haloo! Semoga harimu menyenangkan",
        "app": "Backend Chatbot RAG",
        "tips": "Gunakan endpoint /docs untuk eksplorasi API ini!"
    } 
    
app.include_router(chat_router, tags=["Chat Management"])
app.include_router(dashboard_router, tags=["Dashboard Management"])
app.include_router(document_router, tags=["Knowledge Base Management"])
app.include_router(prompt_router, tags=["AI Configuration Management"])
app.include_router(config_router, tags=["Token Configuration"])
app.include_router(rag_router, tags=["Test Message RAG"])
app.include_router(auth_router, tags=["Admin Auth"])