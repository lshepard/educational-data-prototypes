from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from typing import Optional
from .database import get_db
from .models import Student
from sqlalchemy.orm import Session

load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or SUPABASE_ANON_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
security = HTTPBearer()


def verify_token(token: str) -> dict:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(
            token, 
            JWT_SECRET_KEY, 
            algorithms=["HS256"],
            options={"verify_signature": True, "verify_exp": True}
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> dict:
    """Get current authenticated user"""
    token = credentials.credentials
    payload = verify_token(token)
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )
    
    return {
        "user_id": user_id,
        "email": payload.get("email"),
        "role": payload.get("role", "student")
    }


async def get_current_student(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Student:
    """Get current student from database"""
    student = db.query(Student).filter(
        Student.supabase_user_id == current_user["user_id"]
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )
    
    return student


def require_student_access():
    """Dependency to ensure user is a student"""
    return get_current_student


def require_admin_access():
    """Dependency to ensure user has admin privileges (future implementation)"""
    # For now, just return current user - expand later for admin roles
    return get_current_user