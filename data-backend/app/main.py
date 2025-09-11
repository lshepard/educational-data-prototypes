from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session, joinedload
from typing import List
from .database import get_db
from .models import Student, Enrollment, Assignment, Submission, Class, Teacher, School, StudentAppData
from .schemas import (
    StudentProfile, 
    StudentDashboard, 
    EnrollmentWithClass, 
    AssignmentWithClass,
    SubmissionWithAssignment,
    StudentAppDataCreate,
    StudentAppDataUpdate,
    StudentAppDataResponse
)
from .auth import get_current_student, get_current_user
from typing import Optional
import uuid as uuid_lib
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
    allow_origin_regex=r"https://.*\.vusercontent\.net|https://.*\.vercel\.app|https://.*\.railway\.app|https://.*\.sandbox\.lovable\.dev|https://.*\.lovable\.app|http://localhost:3000|http://127\.0\.0\.1:3000",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount CRUDAdmin - disabled due to async connection issues
# app.include_router(admin.router, prefix="/admin")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the public landing page"""
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.get("/api")
async def api_info():
    """API information endpoint"""
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


# Student App Data endpoints
@app.post("/student/app-data", response_model=StudentAppDataResponse)
async def store_app_data(
    app_data: StudentAppDataCreate,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Store or update app data for the authenticated student"""
    # Check if data already exists
    existing_data = db.query(StudentAppData).filter(
        StudentAppData.student_id == current_student.id,
        StudentAppData.app_key == app_data.app_key,
        StudentAppData.data_key == app_data.data_key
    ).first()
    
    if existing_data:
        # Update existing data
        existing_data.data_value = app_data.data_value
        db.commit()
        db.refresh(existing_data)
        return StudentAppDataResponse(
            app_key=existing_data.app_key,
            data_key=existing_data.data_key,
            data_value=existing_data.data_value,
            created_at=existing_data.created_at,
            updated_at=existing_data.updated_at
        )
    else:
        # Create new data
        db_app_data = StudentAppData(
            student_id=current_student.id,
            app_key=app_data.app_key,
            data_key=app_data.data_key,
            data_value=app_data.data_value
        )
        db.add(db_app_data)
        db.commit()
        db.refresh(db_app_data)
        return StudentAppDataResponse(
            app_key=db_app_data.app_key,
            data_key=db_app_data.data_key,
            data_value=db_app_data.data_value,
            created_at=db_app_data.created_at,
            updated_at=db_app_data.updated_at
        )


@app.get("/student/app-data/{app_key}", response_model=List[StudentAppDataResponse])
async def get_app_data_by_app(
    app_key: str,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get all data for a specific app for the authenticated student"""
    app_data = db.query(StudentAppData).filter(
        StudentAppData.student_id == current_student.id,
        StudentAppData.app_key == app_key
    ).all()
    
    return [
        StudentAppDataResponse(
            app_key=data.app_key,
            data_key=data.data_key,
            data_value=data.data_value,
            created_at=data.created_at,
            updated_at=data.updated_at
        ) for data in app_data
    ]


@app.get("/student/app-data/{app_key}/{data_key}", response_model=StudentAppDataResponse)
async def get_specific_app_data(
    app_key: str,
    data_key: str,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get specific data for an app and key for the authenticated student"""
    app_data = db.query(StudentAppData).filter(
        StudentAppData.student_id == current_student.id,
        StudentAppData.app_key == app_key,
        StudentAppData.data_key == data_key
    ).first()
    
    if not app_data:
        raise HTTPException(status_code=404, detail="App data not found")
    
    return StudentAppDataResponse(
        app_key=app_data.app_key,
        data_key=app_data.data_key,
        data_value=app_data.data_value,
        created_at=app_data.created_at,
        updated_at=app_data.updated_at
    )


@app.put("/student/app-data/{app_key}/{data_key}", response_model=StudentAppDataResponse)
async def update_app_data(
    app_key: str,
    data_key: str,
    update_data: StudentAppDataUpdate,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Update specific app data for the authenticated student"""
    app_data = db.query(StudentAppData).filter(
        StudentAppData.student_id == current_student.id,
        StudentAppData.app_key == app_key,
        StudentAppData.data_key == data_key
    ).first()
    
    if not app_data:
        raise HTTPException(status_code=404, detail="App data not found")
    
    app_data.data_value = update_data.data_value
    db.commit()
    db.refresh(app_data)
    
    return StudentAppDataResponse(
        app_key=app_data.app_key,
        data_key=app_data.data_key,
        data_value=app_data.data_value,
        created_at=app_data.created_at,
        updated_at=app_data.updated_at
    )


@app.delete("/student/app-data/{app_key}/{data_key}")
async def delete_app_data(
    app_key: str,
    data_key: str,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Delete specific app data for the authenticated student"""
    app_data = db.query(StudentAppData).filter(
        StudentAppData.student_id == current_student.id,
        StudentAppData.app_key == app_key,
        StudentAppData.data_key == data_key
    ).first()
    
    if not app_data:
        raise HTTPException(status_code=404, detail="App data not found")
    
    db.delete(app_data)
    db.commit()
    
    return {"message": "App data deleted successfully"}


@app.delete("/student/app-data/{app_key}")
async def delete_app_data_by_app(
    app_key: str,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Delete all data for a specific app for the authenticated student"""
    app_data_count = db.query(StudentAppData).filter(
        StudentAppData.student_id == current_student.id,
        StudentAppData.app_key == app_key
    ).count()
    
    if app_data_count == 0:
        raise HTTPException(status_code=404, detail="No app data found for this app")
    
    db.query(StudentAppData).filter(
        StudentAppData.student_id == current_student.id,
        StudentAppData.app_key == app_key
    ).delete()
    db.commit()
    
    return {"message": f"Deleted {app_data_count} app data records"}


# Cross-user app data endpoints (for teachers accessing student data)
@app.post("/app-data/{student_id}", response_model=StudentAppDataResponse)
async def store_student_app_data(
    student_id: str,
    app_data: StudentAppDataCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Store or update app data for any student (teachers can access student data)"""
    # Verify student exists
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if data already exists
    existing_data = db.query(StudentAppData).filter(
        StudentAppData.student_id == student_id,
        StudentAppData.app_key == app_data.app_key,
        StudentAppData.data_key == app_data.data_key
    ).first()
    
    if existing_data:
        # Update existing data
        existing_data.data_value = app_data.data_value
        db.commit()
        db.refresh(existing_data)
        return StudentAppDataResponse(
            app_key=existing_data.app_key,
            data_key=existing_data.data_key,
            data_value=existing_data.data_value,
            created_at=existing_data.created_at,
            updated_at=existing_data.updated_at
        )
    else:
        # Create new data
        db_app_data = StudentAppData(
            student_id=student_id,
            app_key=app_data.app_key,
            data_key=app_data.data_key,
            data_value=app_data.data_value
        )
        db.add(db_app_data)
        db.commit()
        db.refresh(db_app_data)
        return StudentAppDataResponse(
            app_key=db_app_data.app_key,
            data_key=db_app_data.data_key,
            data_value=db_app_data.data_value,
            created_at=db_app_data.created_at,
            updated_at=db_app_data.updated_at
        )


@app.get("/app-data/{student_id}/{app_key}", response_model=List[StudentAppDataResponse])
async def get_student_app_data_by_app(
    student_id: str,
    app_key: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all app data for a specific student and app (teachers can access student data)"""
    # Verify student exists
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    app_data = db.query(StudentAppData).filter(
        StudentAppData.student_id == student_id,
        StudentAppData.app_key == app_key
    ).all()
    
    return [
        StudentAppDataResponse(
            app_key=data.app_key,
            data_key=data.data_key,
            data_value=data.data_value,
            created_at=data.created_at,
            updated_at=data.updated_at
        ) for data in app_data
    ]


@app.get("/app-data/{student_id}/{app_key}/{data_key}", response_model=StudentAppDataResponse)
async def get_specific_student_app_data(
    student_id: str,
    app_key: str,
    data_key: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific app data for any student (teachers can access student data)"""
    app_data = db.query(StudentAppData).filter(
        StudentAppData.student_id == student_id,
        StudentAppData.app_key == app_key,
        StudentAppData.data_key == data_key
    ).first()
    
    if not app_data:
        raise HTTPException(status_code=404, detail="App data not found")
    
    return StudentAppDataResponse(
        app_key=app_data.app_key,
        data_key=app_data.data_key,
        data_value=app_data.data_value,
        created_at=app_data.created_at,
        updated_at=app_data.updated_at
    )


@app.get("/students", response_model=List[StudentProfile])
async def get_all_students(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all students (for teachers to see their students)"""
    students = db.query(Student).options(
        joinedload(Student.school)
    ).all()
    
    return students


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)