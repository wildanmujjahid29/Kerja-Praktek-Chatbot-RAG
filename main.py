from fastapi import FastAPI

# from fastapi.middleware.cors import CORSMiddleware
from api.chat_router import router as chat_router
from api.dashboard_router import router as dashboard_router
from api.document_router import router as document_router
from api.prompt_router import router as prompt_router
from api.rag_router import router as rag_router

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/", include_in_schema=False)
def root():
    return {
        "message": "Haloo! Semoga harimu menyenangkan",
        "app": "Backend Chatbot RAG",
        "tips": "Gunakan endpoint /docs untuk eksplorasi API ini!"
    } 
    
app.include_router(chat_router, tags=["Chat"])
app.include_router(rag_router, tags=["RAG"], include_in_schema=False)
app.include_router(dashboard_router, tags=["Dashboard"])
app.include_router(document_router, tags=["Documents"])
app.include_router(prompt_router, tags=["Chatbot Config"])