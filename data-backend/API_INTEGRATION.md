# Educational Data Backend API Integration

## Overview
FERPA-compliant educational data API for student-facing applications. Provides secure access to student profiles, classes, assignments, and grades.

## Base URL
- **Local Development**: `http://127.0.0.1:8001`
- **Production (Railway)**: `https://your-app.railway.app`

## Authentication
All student endpoints require **Supabase JWT token** in the Authorization header:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## API Endpoints

### 1. API Info
```http
GET /
```
**Response:**
```json
{
  "message": "Educational Data Backend API",
  "version": "1.0.0", 
  "docs": "/docs",
  "demo_data_available": true,
  "endpoints": {
    "student_profile": "/student/profile",
    "student_classes": "/student/classes",
    "student_assignments": "/student/assignments", 
    "student_grades": "/student/grades",
    "student_dashboard": "/student/dashboard"
  }
}
```

### 2. Student Profile
```http
GET /student/profile
Authorization: Bearer <token>
```
**Response:**
```json
{
  "id": "uuid",
  "first_name": "Emma",
  "last_name": "Wilson", 
  "email": "emma.wilson@student.lincoln.edu",
  "student_number": "2025001",
  "grade_level": 3,
  "school": {
    "id": "uuid",
    "name": "Lincoln Elementary School",
    "district": "Riverside District"
  }
}
```

### 3. Student Classes
```http
GET /student/classes
Authorization: Bearer <token>
```
**Response:**
```json
[
  {
    "id": "uuid",
    "enrollment_status": "active",
    "enrolled_at": "2024-08-15T00:00:00Z",
    "class_": {
      "id": "uuid", 
      "name": "Mrs. Garcia's 3rd Grade",
      "subject": "General Elementary",
      "semester": "Fall 2025",
      "academic_year": "2024-25",
      "teacher": {
        "first_name": "Maria",
        "last_name": "Garcia",
        "email": "ms.garcia@lincoln.edu"
      }
    }
  }
]
```

### 4. Student Assignments
```http
GET /student/assignments  
Authorization: Bearer <token>
```
**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Math Facts Practice", 
    "description": "Addition and subtraction practice worksheet",
    "due_date": "2025-09-15T15:30:00Z",
    "points_possible": 20,
    "assignment_type": "homework",
    "class_": {
      "name": "Mrs. Garcia's 3rd Grade",
      "subject": "General Elementary"
    }
  }
]
```

### 5. Student Grades
```http
GET /student/grades
Authorization: Bearer <token>
```
**Response:**
```json
[
  {
    "id": "uuid",
    "score": 18.0,
    "letter_grade": "A", 
    "submitted_at": "2025-09-14T20:15:00Z",
    "assignment": {
      "name": "Math Facts Practice",
      "points_possible": 20,
      "class_": {
        "name": "Mrs. Garcia's 3rd Grade"
      }
    }
  }
]
```

### 6. Student Dashboard
```http
GET /student/dashboard
Authorization: Bearer <token>
```
**Response:** Combined data from all above endpoints in a single request.

## Demo Data Available

- **Lincoln Elementary School** with 10 students
- **2 Classes**: 3rd grade (5 students) and 5th grade (5 students)  
- **8 Assignments**: Age-appropriate homework, quizzes, and projects
- **Sample submissions** with realistic grades

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Invalid authentication token"
}
```

### 404 Not Found
```json  
{
  "detail": "Student profile not found"
}
```

## CORS Configuration
The API allows requests from:
- `http://localhost:3000` (local development)
- `https://*.vercel.app` (Vercel deployments)
- `https://*.railway.app` (Railway deployments)

## Interactive Documentation
Visit `/docs` endpoint for full OpenAPI/Swagger documentation with request/response examples and testing interface.

## Security Notes
- All student data is scoped by authentication token (FERPA compliant)
- Row-level security ensures students only see their own data
- JWT tokens must be valid and not expired
- API requires `SUPABASE_JWT_SECRET` environment variable for token verification