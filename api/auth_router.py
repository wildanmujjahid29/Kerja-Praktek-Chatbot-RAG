from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from services.auth_service import (
    get_admin_from_token, login_admin,
    register_admin
)

security = HTTPBearer()

router = APIRouter(prefix="/auth")

@router.post("/register")
def register(username: str, email: str, password: str, full_name: str = None, role: str = "admin"):
    try:
        admin = register_admin(username, email, password, full_name, role)
        return {"status": "success", "admin": admin}
    except Exception as e:
        raise HTTPException(400, str(e))
    
@router.post("/login")
def login(username: str, password: str):
    result = login_admin(username, password)
    if not result:
        raise HTTPException(401, "Invalid username or password")
    return result

@router.get("/me")
def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    print(f"Token extracted: {token[:50]}...")  # Debug line (partial token)
    admin = get_admin_from_token(token)
    if not admin:
        raise HTTPException(401, "Invalid or expired token")
    return admin