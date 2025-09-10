from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid


class SchoolCreate(BaseModel):
    name: str
    district: Optional[str] = None


class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    district: Optional[str] = None


class TeacherCreate(BaseModel):
    school_id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str
    supabase_user_id: Optional[uuid.UUID] = None


class TeacherUpdate(BaseModel):
    school_id: Optional[uuid.UUID] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    supabase_user_id: Optional[uuid.UUID] = None


class StudentCreate(BaseModel):
    school_id: uuid.UUID
    supabase_user_id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str
    student_number: Optional[str] = None
    grade_level: Optional[int] = None


class StudentUpdate(BaseModel):
    school_id: Optional[uuid.UUID] = None
    supabase_user_id: Optional[uuid.UUID] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    student_number: Optional[str] = None
    grade_level: Optional[int] = None


class ClassCreate(BaseModel):
    school_id: uuid.UUID
    teacher_id: uuid.UUID
    name: str
    subject: Optional[str] = None
    semester: Optional[str] = None
    academic_year: Optional[str] = None


class ClassUpdate(BaseModel):
    school_id: Optional[uuid.UUID] = None
    teacher_id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    subject: Optional[str] = None
    semester: Optional[str] = None
    academic_year: Optional[str] = None


class EnrollmentCreate(BaseModel):
    student_id: uuid.UUID
    class_id: uuid.UUID
    enrollment_status: Optional[str] = "active"


class EnrollmentUpdate(BaseModel):
    student_id: Optional[uuid.UUID] = None
    class_id: Optional[uuid.UUID] = None
    enrollment_status: Optional[str] = None


class AssignmentCreate(BaseModel):
    class_id: uuid.UUID
    name: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    points_possible: Optional[int] = None
    assignment_type: Optional[str] = None


class AssignmentUpdate(BaseModel):
    class_id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    points_possible: Optional[int] = None
    assignment_type: Optional[str] = None


class SubmissionCreate(BaseModel):
    student_id: uuid.UUID
    assignment_id: uuid.UUID
    score: Optional[float] = None
    letter_grade: Optional[str] = None
    submitted_at: Optional[datetime] = None


class SubmissionUpdate(BaseModel):
    student_id: Optional[uuid.UUID] = None
    assignment_id: Optional[uuid.UUID] = None
    score: Optional[float] = None
    letter_grade: Optional[str] = None
    submitted_at: Optional[datetime] = None