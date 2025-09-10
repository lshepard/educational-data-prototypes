from crudadmin import CRUDAdmin
from .database import SessionLocal, engine
from .models import School, Teacher, Student, Class, Enrollment, Assignment, Submission
from .admin_schemas import (
    SchoolCreate, SchoolUpdate,
    TeacherCreate, TeacherUpdate,
    StudentCreate, StudentUpdate,
    ClassCreate, ClassUpdate,
    EnrollmentCreate, EnrollmentUpdate,
    AssignmentCreate, AssignmentUpdate,
    SubmissionCreate, SubmissionUpdate
)
import os


def get_session():
    """Session factory for CRUDAdmin"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# Initialize CRUDAdmin with PostgreSQL database configuration
# Convert postgresql:// to postgresql+asyncpg:// for async support
database_url = os.getenv("DATABASE_URL")
async_db_url = database_url.replace("postgresql://", "postgresql+asyncpg://") if database_url else None

admin = CRUDAdmin(
    session=get_session,
    SECRET_KEY=os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production"),
    initial_admin={
        "username": "admin",
        "password": "admin123"  # Change this in production!
    },
    # Use the same database connection for admin tables with async driver
    admin_db_url=async_db_url
)

# Add views for all educational data models with basic configuration

# Schools
admin.add_view(
    model=School,
    create_schema=SchoolCreate,
    update_schema=SchoolUpdate
)

# Teachers
admin.add_view(
    model=Teacher,
    create_schema=TeacherCreate,
    update_schema=TeacherUpdate
)

# Students
admin.add_view(
    model=Student,
    create_schema=StudentCreate,
    update_schema=StudentUpdate
)

# Classes
admin.add_view(
    model=Class,
    create_schema=ClassCreate,
    update_schema=ClassUpdate
)

# Enrollments
admin.add_view(
    model=Enrollment,
    create_schema=EnrollmentCreate,
    update_schema=EnrollmentUpdate
)

# Assignments
admin.add_view(
    model=Assignment,
    create_schema=AssignmentCreate,
    update_schema=AssignmentUpdate
)

# Submissions
admin.add_view(
    model=Submission,
    create_schema=SubmissionCreate,
    update_schema=SubmissionUpdate
)