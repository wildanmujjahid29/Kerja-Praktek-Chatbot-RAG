from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from services.auth_service import get_admin_from_token

security = HTTPBearer()

def admin_required(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    admin = get_admin_from_token(token)
    if not admin:
        raise HTTPException(status_code=401, detail="Unauthorized or invalid token")
    return admin
