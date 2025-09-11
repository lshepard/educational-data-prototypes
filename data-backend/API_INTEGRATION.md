# Educational Data Backend API Integration

## Overview
FERPA-compliant educational data API for student-facing applications. Provides secure access to student profiles, classes, assignments, and grades.

## Base URL
- **Local Development**: `http://127.0.0.1:8001`
- **Production (Railway)**: `https://your-app.railway.app`

## Authentication
All endpoints require **Supabase JWT token** in the Authorization header:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### User Roles
The API supports two user roles stored in JWT `user_metadata`:
- **Students**: `"role": "student"` - Can access their own academic data
- **Teachers**: `"role": "teacher"` - Can access any student's data (simplified for prototype)

### Data Access Permissions
**For Prototype Purposes**: Any authenticated user can access any student's data through cross-user endpoints. In production, this would be restricted to appropriate teacher-student relationships.

### Role Detection
Use the `/auth/test` endpoint to determine the current user's role:
```http
GET /auth/test
Authorization: Bearer <token>
```
**Response:**
```json
{
  "message": "Authentication successful",
  "user": {
    "user_id": "uuid",
    "email": "student1@demo.test",
    "role": "student"
  }
}
```

## API Endpoints

### 1. Public Landing Page
```http
GET /
```
**Response:** HTML landing page with project overview, prototype links, and API documentation access.

### 2. API Info
```http
GET /api
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
    "student_dashboard": "/student/dashboard",
    "student_app_data": "/student/app-data"
  }
}
```

### 3. Student Profile
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
  "email": "student1@demo.test",
  "student_number": "2025001",
  "grade_level": 3,
  "school": {
    "id": "uuid",
    "name": "Lincoln Elementary School",
    "district": "Riverside District"
  }
}
```

### 4. Student Classes
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
        "email": "teacher1@demo.test"
      }
    }
  }
]
```

### 5. Student Assignments
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

### 6. Student Grades
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

### 7. Student Dashboard
```http
GET /student/dashboard
Authorization: Bearer <token>
```
**Response:** Combined data from all above endpoints in a single request.

## Student App Data Storage

### 8. Store App Data (Upsert)
```http
POST /student/app-data
Authorization: Bearer <token>
Content-Type: application/json
```
**Request Body:**
```json
{
  "app_key": "edubot",
  "data_key": "chat_history",
  "data_value": {
    "messages": [
      {"role": "user", "content": "Help with math"},
      {"role": "assistant", "content": "I can help with that!"}
    ],
    "last_updated": "2025-01-15T10:30:00Z"
  }
}
```
**Response:**
```json
{
  "app_key": "edubot",
  "data_key": "chat_history",
  "data_value": {
    "messages": [...],
    "last_updated": "2025-01-15T10:30:00Z"
  },
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

### 9. Get All App Data for an Application
```http
GET /student/app-data/{app_key}
Authorization: Bearer <token>
```
**Example:** `GET /student/app-data/edubot`

**Response:**
```json
[
  {
    "app_key": "edubot",
    "data_key": "chat_history",
    "data_value": {"messages": [...]},
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:30:00Z"
  },
  {
    "app_key": "edubot", 
    "data_key": "user_preferences",
    "data_value": {"theme": "dark"},
    "created_at": "2025-01-15T10:31:00Z",
    "updated_at": "2025-01-15T10:31:00Z"
  }
]
```

### 10. Get Specific App Data
```http
GET /student/app-data/{app_key}/{data_key}
Authorization: Bearer <token>
```
**Example:** `GET /student/app-data/edubot/chat_history`

**Response:**
```json
{
  "app_key": "edubot",
  "data_key": "chat_history", 
  "data_value": {
    "messages": [
      {"role": "user", "content": "Help with math"},
      {"role": "assistant", "content": "I can help with that!"}
    ]
  },
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

### 11. Update Specific App Data
```http
PUT /student/app-data/{app_key}/{data_key}
Authorization: Bearer <token>
Content-Type: application/json
```
**Request Body:**
```json
{
  "data_value": {
    "updated_field": "new_value",
    "timestamp": "2025-01-15T11:00:00Z"
  }
}
```

### 12. Delete Specific App Data
```http
DELETE /student/app-data/{app_key}/{data_key}
Authorization: Bearer <token>
```
**Response:**
```json
{
  "message": "App data deleted successfully"
}
```

### 13. Delete All Data for an Application
```http
DELETE /student/app-data/{app_key}
Authorization: Bearer <token>
```
**Response:**
```json
{
  "message": "Deleted 3 app data records"
}
```

## Cross-User Data Access (Teachers & Students)

### 14. Get All Students
```http
GET /students
Authorization: Bearer <token>
```
**Response:** Array of all students with their profiles (for teachers to see available students)

### 15. Store App Data for Any Student
```http
POST /app-data/{student_id}
Authorization: Bearer <token>
Content-Type: application/json
```
**Request Body:**
```json
{
  "app_key": "edubot",
  "data_key": "teacher_notes",
  "data_value": {
    "notes": "Student needs extra help with fractions",
    "created_by": "teacher1@demo.test",
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```
**Example:** `POST /app-data/00000000-0000-4000-8000-000000003020`

### 16. Get Student's App Data by Application
```http
GET /app-data/{student_id}/{app_key}
Authorization: Bearer <token>
```
**Example:** `GET /app-data/00000000-0000-4000-8000-000000003020/edubot`

### 17. Get Specific Student App Data
```http
GET /app-data/{student_id}/{app_key}/{data_key}
Authorization: Bearer <token>
```
**Example:** `GET /app-data/00000000-0000-4000-8000-000000003020/edubot/chat_history`

## Demo Data Available

- **Lincoln Elementary School** 
- **3 Demo Students**:
  - Emma Wilson (3rd grade) - `student1@demo.test`
  - Ethan Garcia (5th grade) - `student2@demo.test` 
  - Maya Chen (4th grade, enrolled in both classes) - `student3@demo.test`
- **2 Classes**: Mrs. Garcia's 3rd Grade and Mr. Thompson's 5th Grade
- **Multiple Assignments**: Math, reading, and general assignments with varied difficulty
- **Sample submissions** with realistic grades showing academic patterns
- **Maya Chen Special Case**: Demonstrates math strengths (A's & B's) and reading challenges (C's & D's)

## Test User Credentials
All demo accounts use password: `demo123456`

**Students:**
- `student1@demo.test` - Emma Wilson (3rd grade)
- `student2@demo.test` - Ethan Garcia (5th grade)  
- `student3@demo.test` - Maya Chen (4th grade, both classes)

**Teachers:**
- `teacher1@demo.test` - Maria Garcia (3rd grade teacher)
- `teacher2@demo.test` - James Thompson (5th grade teacher)

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

## App Data Storage Use Cases

### For EduBot:
```javascript
// Store chat conversation
await fetch('/student/app-data', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    app_key: 'edubot',
    data_key: 'chat_history',
    data_value: {
      messages: chatMessages,
      last_active: new Date().toISOString()
    }
  })
});

// Retrieve chat history
const response = await fetch('/student/app-data/edubot/chat_history', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const chatData = await response.json();
```

### For Learning Dashboard:
```javascript
// Store user preferences
await fetch('/student/app-data', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    app_key: 'learning_dashboard',
    data_key: 'preferences',
    data_value: {
      theme: 'dark',
      notifications: true,
      default_view: 'assignments'
    }
  })
});
```

### For Teachers Accessing Student Data:
```javascript
// Get all students
const studentsResponse = await fetch('/students', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const students = await studentsResponse.json();

// Store teacher notes for a specific student
await fetch(`/app-data/${studentId}`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    app_key: 'teacher_dashboard',
    data_key: 'student_notes',
    data_value: {
      notes: 'Needs extra help with reading comprehension',
      created_by_teacher: teacherEmail,
      last_updated: new Date().toISOString()
    }
  })
});

// Retrieve student's EduBot chat history (for teacher review)
const chatResponse = await fetch(`/app-data/${studentId}/edubot/chat_history`, {
  headers: { 'Authorization': `Bearer ${token}` }
});
const chatHistory = await chatResponse.json();
```

## CORS Configuration
The API allows requests from:
- `http://localhost:3000` (local development)
- `https://*.vercel.app` (Vercel deployments)
- `https://*.railway.app` (Railway deployments)
- `https://*.vusercontent.net` (Claude Artifacts)

## Interactive Documentation
Visit `/docs` endpoint for full OpenAPI/Swagger documentation with request/response examples and testing interface.

## Security Notes
- **FERPA Compliant**: All student data is scoped by authentication token
- **Row-Level Security**: Database policies ensure students only access their own data
- **JWT Authentication**: Tokens must be valid and not expired
- **App Data Isolation**: Student app data is automatically scoped to the authenticated user
- **Secure Storage**: App data uses JSONB with proper indexing for performance
- **Audit Trail**: All app data includes created_at/updated_at timestamps
- **Environment Variables**: API requires `SUPABASE_JWT_SECRET` for token verification