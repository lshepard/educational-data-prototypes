from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from typing import List
from .database import get_db
from .models import Student, Enrollment, Assignment, Submission, Class, Teacher, School
from .schemas import (
    StudentProfile, 
    StudentDashboard, 
    EnrollmentWithClass, 
    AssignmentWithClass,
    SubmissionWithAssignment
)
from .auth import get_current_student, get_current_user
# from .admin import admin  # CRUDAdmin having async connection issues - disable for now

app = FastAPI(
    title="Educational Data Backend",
    description="FERPA-compliant backend for educational prototypes",
    version="1.0.0"
)

# CORS middleware for frontend apps
def custom_cors_origin_handler(origin: str) -> bool:
    """Allow specific origins including all vusercontent.net subdomains"""
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    # Check exact matches
    if origin in allowed_origins:
        return True
    
    # Check wildcards
    if (origin and 
        (origin.endswith(".vercel.app") or 
         origin.endswith(".railway.app") or
         origin.endswith(".vusercontent.net"))):
        return True
        
    return False

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vusercontent\.net|https://.*\.vercel\.app|https://.*\.railway\.app|http://localhost:3000|http://127\.0\.0\.1:3000",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount CRUDAdmin - disabled due to async connection issues
# app.include_router(admin.router, prefix="/admin")


@app.get("/")
async def root():
    return {
        "message": "Educational Data Backend API", 
        "version": "1.0.0",
        "docs": "/docs",
        "demo_data_available": True,
        "endpoints": {
            "student_profile": "/student/profile",
            "student_classes": "/student/classes", 
            "student_assignments": "/student/assignments",
            "student_grades": "/student/grades",
            "student_dashboard": "/student/dashboard"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Student endpoints
@app.get("/student/profile", response_model=StudentProfile)
async def get_student_profile(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get current student's profile with school information"""
    student_with_school = db.query(Student).options(
        joinedload(Student.school)
    ).filter(Student.id == current_student.id).first()
    
    return student_with_school


@app.get("/student/classes", response_model=List[EnrollmentWithClass])
async def get_student_classes(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get all classes the student is enrolled in"""
    enrollments = db.query(Enrollment).options(
        joinedload(Enrollment.class_).joinedload(Class.teacher)
    ).filter(
        Enrollment.student_id == current_student.id,
        Enrollment.enrollment_status == "active"
    ).all()
    
    return enrollments


@app.get("/student/assignments", response_model=List[AssignmentWithClass])
async def get_student_assignments(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get all assignments for student's enrolled classes"""
    # Get class IDs student is enrolled in
    enrolled_class_ids = db.query(Enrollment.class_id).filter(
        Enrollment.student_id == current_student.id,
        Enrollment.enrollment_status == "active"
    ).subquery()
    
    assignments = db.query(Assignment).options(
        joinedload(Assignment.class_)
    ).filter(
        Assignment.class_id.in_(enrolled_class_ids)
    ).order_by(Assignment.due_date.desc()).all()
    
    return assignments


@app.get("/student/grades", response_model=List[SubmissionWithAssignment])
async def get_student_grades(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get all student's submission history with grades"""
    submissions = db.query(Submission).options(
        joinedload(Submission.assignment).joinedload(Assignment.class_)
    ).filter(
        Submission.student_id == current_student.id
    ).order_by(Submission.submitted_at.desc()).all()
    
    return submissions


@app.get("/student/dashboard", response_model=StudentDashboard)
async def get_student_dashboard(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get comprehensive student dashboard data"""
    # Get student with school
    student_with_school = db.query(Student).options(
        joinedload(Student.school)
    ).filter(Student.id == current_student.id).first()
    
    # Get enrolled classes
    enrollments = db.query(Enrollment).options(
        joinedload(Enrollment.class_).joinedload(Class.teacher)
    ).filter(
        Enrollment.student_id == current_student.id,
        Enrollment.enrollment_status == "active"
    ).all()
    
    # Get recent assignments (last 10)
    enrolled_class_ids = [e.class_id for e in enrollments]
    recent_assignments = db.query(Assignment).options(
        joinedload(Assignment.class_)
    ).filter(
        Assignment.class_id.in_(enrolled_class_ids)
    ).order_by(Assignment.due_date.desc()).limit(10).all()
    
    # Get recent submissions (last 10)
    recent_submissions = db.query(Submission).options(
        joinedload(Submission.assignment).joinedload(Assignment.class_)
    ).filter(
        Submission.student_id == current_student.id
    ).order_by(Submission.submitted_at.desc()).limit(10).all()
    
    return {
        "student": student_with_school,
        "enrolled_classes": enrollments,
        "recent_assignments": recent_assignments,
        "recent_submissions": recent_submissions
    }


# Auth test endpoint
@app.get("/auth/test")
async def test_auth(current_user: dict = Depends(get_current_user)):
    """Test authentication - returns current user info"""
    return {"message": "Authentication successful", "user": current_user}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)