from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
import uuid


class SchoolBase(BaseModel):
    name: str
    district: Optional[str] = None


class School(SchoolBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StudentBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    student_number: Optional[str] = None
    grade_level: Optional[int] = None


class Student(StudentBase):
    id: uuid.UUID
    school_id: uuid.UUID
    supabase_user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StudentProfile(Student):
    school: School


class TeacherBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class Teacher(TeacherBase):
    id: uuid.UUID
    school_id: uuid.UUID
    supabase_user_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ClassBase(BaseModel):
    name: str
    subject: Optional[str] = None
    semester: Optional[str] = None
    academic_year: Optional[str] = None


class Class(ClassBase):
    id: uuid.UUID
    school_id: uuid.UUID
    teacher_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ClassWithTeacher(Class):
    teacher: Teacher


class EnrollmentBase(BaseModel):
    enrollment_status: str = "active"


class Enrollment(EnrollmentBase):
    id: uuid.UUID
    student_id: uuid.UUID
    class_id: uuid.UUID
    enrolled_at: datetime
    
    class Config:
        from_attributes = True


class EnrollmentWithClass(Enrollment):
    class_: ClassWithTeacher


class AssignmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    points_possible: Optional[int] = None
    assignment_type: Optional[str] = None


class Assignment(AssignmentBase):
    id: uuid.UUID
    class_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AssignmentWithClass(Assignment):
    class_: Class


class SubmissionBase(BaseModel):
    score: Optional[Decimal] = None
    letter_grade: Optional[str] = None
    submitted_at: Optional[datetime] = None


class Submission(SubmissionBase):
    id: uuid.UUID
    student_id: uuid.UUID
    assignment_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SubmissionWithAssignment(Submission):
    assignment: AssignmentWithClass


class StudentDashboard(BaseModel):
    student: StudentProfile
    enrolled_classes: List[EnrollmentWithClass]
    recent_assignments: List[AssignmentWithClass]
    recent_submissions: List[SubmissionWithAssignment]