from fastapi import APIRouter, HTTPException, Request, Response
from schemas.chat_schemas import (
    ChatResponse, 
    ChatSessionWithMessages,
    SendMessageRequest, 
    SessionResponse
)
from services.chat_service import (
    delete_session, 
    get_or_create_session,
    get_session_with_messages, 
    send_message
)

router = APIRouter()

@router.get("/chat/session")
def get_or_create_chat_session(request: Request, response: Response, session_name: str = "New Chat") -> SessionResponse:
    """
    Ambil session dari cookie kalau sudah ada,
    atau buat session baru kalau belum ada.
    """
    try:
        session_id = request.cookies.get("session_id")
        session, is_new = get_or_create_session(session_id, session_name)

        response.set_cookie(
            key="session_id", 
            value=session.id, 
            max_age=30*24*60*60,
            httponly=True,
            samesite="lax"
        )

        return SessionResponse(
            session_id=session.id,
            session_name=session.session_name,
            created_at=session.created_at,
            is_new=is_new
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/chat/message")
def send_message_cookie_endpoint(request: Request, response: Response, message_request: SendMessageRequest) -> ChatResponse:
    """
    Kirim pesan dengan menggunakan session dari cookie.
    Jika session belum ada, sistem otomatis membuat session baru.
    """
    try:
        session_id = request.cookies.get("session_id")
        session, is_new = get_or_create_session(session_id)

        if is_new:
            response.set_cookie(
                key="session_id", 
                value=session.id, 
                max_age=30*24*60*60,
                httponly=True,
                samesite="lax"
            )

        result = send_message(
            session.id,
            message_request.message,
            message_request.k or 3,
            message_request.min_similarity or 0.3
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/chat/history")
def get_chat_history(request: Request) -> ChatSessionWithMessages:
    """
    Ambil riwayat chat berdasarkan session yang ada di cookie.
    """
    try:
        session_id = request.cookies.get("session_id")
        if not session_id:
            raise HTTPException(status_code=404, detail="Tidak ada session di cookie")

        session = get_session_with_messages(session_id=session_id)
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/chat/session")
def delete_current_session(request: Request, response: Response) -> dict:
    """
    Hapus session yang sedang aktif berdasarkan cookie
    dan sekalian hapus cookie `session_id`.
    """
    try:
        session_id = request.cookies.get("session_id")
        if not session_id:
            raise HTTPException(status_code=404, detail="Tidak ada session di cookie")

        success = delete_session(session_id)

        response.delete_cookie(key="session_id")

        return {"status": "success" if success else "failed", "message": "Session dan cookie berhasil dihapus"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
