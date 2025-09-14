from config import supabase
from utils.auth_utils import hash_password, verify_password, create_jwt_token, decode_jwt_token
from datetime import datetime

def register_admin(username, email, password, full_name=None, role="admin"):
    # Cek username sudah ada?
    result = supabase.table("admins").select("id").eq("username", username).execute()
    if result.data:
        raise Exception("Username already exists")
    # Cek email sudah ada?
    result = supabase.table("admins").select("id").eq("email", email).execute()
    if result.data:
        raise Exception("Email already exists")
    hashed = hash_password(password)
    data = {
        "username": username,
        "email": email,
        "password_hash": hashed,
        "full_name": full_name,
        "role": role,
        "created_at": datetime.utcnow().isoformat()
    }
    result = supabase.table("admins").insert(data).execute()
    return result.data[0]

def login_admin(username, password):
    # .single() boleh dipakai kalau yakin username unik, dan pasti ada
    result = supabase.table("admins").select("*").eq("username", username).eq("is_active", True).single().execute()
    admin = result.data
    if not admin or not verify_password(password, admin["password_hash"]):
        return None
    supabase.table("admins").update({"last_login": datetime.utcnow().isoformat()}).eq("id", admin["id"]).execute()
    token = create_jwt_token(admin["id"], admin["username"])
    admin.pop("password_hash", None)
    return {"admin": admin, "token": token}

def get_admin_from_token(token):
    payload = decode_jwt_token(token)
    if not payload:
        return None
    admin = supabase.table("admins").select("*").eq("id", payload["admin_id"]).eq("is_active", True).single().execute().data
    if admin:
        admin.pop("password_hash", None)
    return admin