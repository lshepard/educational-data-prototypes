#!/usr/bin/env python3
"""
Simple test script to display demo data using Supabase client
Shows the seeded data from Lincoln Elementary School
"""

import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

def create_supabase_client():
    """Create Supabase client"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    return create_client(url, key)

def print_markdown_table(headers, rows, title):
    """Print a markdown formatted table"""
    print(f"\n## {title}\n")
    
    if not rows:
        print("*No data available*\n")
        return
    
    # Headers
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join(["---"] * len(headers)) + " |")
    
    # Rows
    for row in rows:
        print("| " + " | ".join(str(cell) if cell is not None else "N/A" for cell in row) + " |")

def main():
    """Main function to display all demo data"""
    supabase = create_supabase_client()
    
    print("# Educational Data Backend - Demo Data")
    print("*Generated from Lincoln Elementary School database*\n")
    
    try:
        # Schools
        response = supabase.table('schools').select('*').execute()
        schools = response.data
        
        school_data = []
        for school in schools:
            school_data.append([school['name'], school.get('district', 'N/A')])
        
        print_markdown_table(
            ["School Name", "District"],
            school_data,
            "Schools"
        )
        
        # Teachers
        response = supabase.table('teachers').select('*').execute()
        teachers = response.data
        
        teacher_data = []
        for teacher in teachers:
            teacher_data.append([
                f"{teacher['first_name']} {teacher['last_name']}",
                teacher['email']
            ])
        
        print_markdown_table(
            ["Teacher Name", "Email"],
            teacher_data,
            "Teachers"
        )
        
        # Classes with teacher info
        response = supabase.table('classes').select('*, teachers(first_name, last_name)').execute()
        classes = response.data
        
        class_data = []
        for cls in classes:
            teacher_name = f"{cls['teachers']['first_name']} {cls['teachers']['last_name']}"
            class_data.append([
                cls['name'],
                cls.get('subject', 'General Elementary'),
                teacher_name,
                cls.get('semester', 'N/A'),
                cls.get('academic_year', 'N/A')
            ])
        
        print_markdown_table(
            ["Class Name", "Subject", "Teacher", "Semester", "Academic Year"],
            class_data,
            "Classes"
        )
        
        # Students
        response = supabase.table('students').select('*').execute()
        students = response.data
        
        student_data = []
        for student in students:
            student_data.append([
                f"{student['first_name']} {student['last_name']}",
                student['email'],
                student.get('student_number', 'N/A'),
                f"Grade {student['grade_level']}" if student.get('grade_level') else "N/A"
            ])
        
        print_markdown_table(
            ["Student Name", "Email", "Student Number", "Grade Level"],
            student_data,
            "Students"
        )
        
        # Assignments
        response = supabase.table('assignments').select('*, classes(name)').execute()
        assignments = response.data
        
        assignment_data = []
        for assignment in assignments:
            assignment_data.append([
                assignment['name'],
                assignment.get('assignment_type', 'N/A'),
                assignment['classes']['name'],
                assignment.get('due_date', 'N/A')[:10] if assignment.get('due_date') else 'N/A',  # Just date part
                assignment.get('points_possible', 'N/A')
            ])
        
        print_markdown_table(
            ["Assignment Name", "Type", "Class", "Due Date", "Points"],
            assignment_data,
            "Assignments"
        )
        
        # Sample submissions
        response = supabase.table('submissions').select('''
            *, 
            students(first_name, last_name), 
            assignments(name)
        ''').limit(10).execute()
        submissions = response.data
        
        submission_data = []
        for submission in submissions:
            student_name = f"{submission['students']['first_name']} {submission['students']['last_name']}"
            submission_data.append([
                student_name,
                submission['assignments']['name'],
                submission.get('score', 'N/A'),
                submission.get('letter_grade', 'N/A'),
                submission.get('submitted_at', 'N/A')[:10] if submission.get('submitted_at') else 'N/A'
            ])
        
        print_markdown_table(
            ["Student", "Assignment", "Score", "Letter Grade", "Submitted"],
            submission_data,
            "Sample Submissions"
        )
        
        print(f"\n---")
        print(f"*Total: {len(schools)} school(s), {len(teachers)} teacher(s), {len(classes)} class(es), {len(students)} student(s)*")
        print(f"*{len(assignments)} assignment(s), {len(submissions)} submission(s) shown*")
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        print("Make sure your .env file has the correct SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY")

if __name__ == "__main__":
    main()