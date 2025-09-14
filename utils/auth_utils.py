import bcrypt
import jwt
import os
from datetime import datetime, timedelta

JWT_SECRET = os.getenv("JWT_SECRET", "secret")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_jwt_token(admin_id: str, username:str) -> str:
    expired_at = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    payload = {
        "admin_id" : admin_id,
        "username": username,
        "exp": expired_at,
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

def decode_jwt_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except Exception:
        return None
