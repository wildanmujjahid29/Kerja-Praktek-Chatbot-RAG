from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

from api.document_router import router as document_router
from api.service_router import router as service_router
from api.prompt_router import router as prompt_router
from api.retrieval_router import router as retrieval_router
from api.rag_router import router as rag_router
from api.dashboard_router import router as dashboard_router

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
    
app.include_router(rag_router, tags=["RAG"])
app.include_router(dashboard_router, tags=["Dashboard"])
app.include_router(document_router, tags=["Documents"])
app.include_router(retrieval_router, tags=["Retrieval"])
app.include_router(service_router, tags=["Services"])
app.include_router(prompt_router, tags=["Prompts"])