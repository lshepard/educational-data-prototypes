from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from typing import Optional
from .database import get_db
from .models import Student, Teacher
from sqlalchemy.orm import Session

load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
security = HTTPBearer()


def verify_token(token: str) -> dict:
    """Verify JWT token and return payload"""
    if not JWT_SECRET_KEY:
        raise HTTPException(
            status_code=500,
            detail="JWT secret not configured"
        )
    
    try:
        payload = jwt.decode(
            token, 
            JWT_SECRET_KEY, 
            algorithms=["HS256"],
            options={"verify_signature": True, "verify_exp": True, "verify_aud": False}
        )
        return payload
    except JWTError as e:
        # Log the specific error for debugging
        print(f"JWT verification error: {str(e)}")
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
    
    # Extract role from user_metadata or app_metadata
    user_metadata = payload.get("user_metadata", {})
    app_metadata = payload.get("app_metadata", {})
    
    role = user_metadata.get("role") or app_metadata.get("role") or "student"
    
    return {
        "user_id": user_id,
        "email": payload.get("email"),
        "role": role
    }


async def get_current_student(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Student:
    """Get current student from database using user metadata or direct assignment"""
    token = credentials.credentials
    payload = verify_token(token)
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    # First try direct supabase_user_id match
    student = db.query(Student).filter(
        Student.supabase_user_id == user_id
    ).first()
    
    if student:
        return student
    
    # Check if user has student assignment in metadata
    user_metadata = payload.get("user_metadata", {})
    app_metadata = payload.get("app_metadata", {})
    
    # Try student_id from metadata
    student_id = user_metadata.get("student_id") or app_metadata.get("student_id")
    if student_id:
        student = db.query(Student).filter(Student.id == student_id).first()
        if student:
            return student
    
    # Try username from metadata
    username = user_metadata.get("username") or app_metadata.get("username")
    if username:
        student = db.query(Student).filter(Student.username == username).first()
        if student:
            return student
    
    # Try role-based assignment
    role = user_metadata.get("role") or app_metadata.get("role")
    if role != "student":
        raise HTTPException(
            status_code=403,
            detail=f"Access denied. User role is '{role}', expected 'student'"
        )
    
    raise HTTPException(
        status_code=404,
        detail="Student profile not found. User needs to be assigned to a student account via metadata."
    )


def require_student_access():
    """Dependency to ensure user is a student"""
    return get_current_student


def require_admin_access():
    """Dependency to ensure user has admin privileges (future implementation)"""
    # For now, just return current user - expand later for admin roles
    return get_current_user