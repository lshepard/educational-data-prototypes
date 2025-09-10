#!/usr/bin/env python3
"""
Script to create test Supabase auth users with metadata linking to students/teachers
Creates demo accounts that correspond to the database users without sending emails
"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

def create_supabase_admin_client():
    """Create Supabase client with service role permissions"""
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    return create_client(url, service_key)

def main():
    supabase = create_supabase_admin_client()
    
    print("🎓 Creating Test Users for Educational Data Backend")
    print("=" * 60)
    
    # Get student and teacher data
    students_resp = supabase.table('students').select('id, first_name, last_name, username, grade_level').execute()
    teachers_resp = supabase.table('teachers').select('id, first_name, last_name, username').execute()
    
    students = students_resp.data
    teachers = teachers_resp.data
    
    print(f"Found {len(students)} students and {len(teachers)} teachers in database")
    print("Students:", [f"{s['first_name']} {s['last_name']}" for s in students])
    print()
    
    # Create test user accounts
    created_users = []
    
    # Create student accounts
    print("👨‍🎓 Creating Student Accounts:")
    print("=" * 30)
    
    for i, student in enumerate(students, 1):
        email = f"student{i}@demo.test"
        password = "demo123456"  # Simple demo password
        
        try:
            # Create auth user with metadata
            auth_response = supabase.auth.admin.create_user({
                "email": email,
                "password": password,
                "email_confirm": True,  # Skip email confirmation
                "user_metadata": {
                    "role": "student",
                    "student_id": student['id'],
                    "username": student['username'],
                    "full_name": f"{student['first_name']} {student['last_name']}",
                    "grade_level": student['grade_level']
                }
            })
            
            if auth_response.user:
                print(f"✅ Created: {student['first_name']} {student['last_name']}")
                print(f"   📧 Email: {email}")
                print(f"   🔑 Password: {password}")
                print(f"   👤 Username: {student['username']}")
                print(f"   🎯 Student ID: {student['id']}")
                print()
                
                created_users.append({
                    "type": "student",
                    "name": f"{student['first_name']} {student['last_name']}",
                    "email": email,
                    "password": password,
                    "username": student['username'],
                    "auth_user_id": auth_response.user.id
                })
                
                # Update the student record to link to auth user
                supabase.table('students').update({
                    "supabase_user_id": auth_response.user.id
                }).eq('id', student['id']).execute()
                
        except Exception as e:
            print(f"❌ Error creating student {student['first_name']}: {str(e)}")
    
    # Create teacher accounts  
    print("\n👨‍🏫 Creating Teacher Accounts:")
    print("=" * 30)
    
    for i, teacher in enumerate(teachers, 1):
        email = f"teacher{i}@demo.test"
        password = "demo123456"  # Simple demo password
        
        try:
            # Create auth user with metadata
            auth_response = supabase.auth.admin.create_user({
                "email": email,
                "password": password,
                "email_confirm": True,  # Skip email confirmation
                "user_metadata": {
                    "role": "teacher",
                    "teacher_id": teacher['id'],
                    "username": teacher['username'],
                    "full_name": f"{teacher['first_name']} {teacher['last_name']}"
                }
            })
            
            if auth_response.user:
                print(f"✅ Created: {teacher['first_name']} {teacher['last_name']}")
                print(f"   📧 Email: {email}")
                print(f"   🔑 Password: {password}")
                print(f"   👤 Username: {teacher['username']}")
                print(f"   🎯 Teacher ID: {teacher['id']}")
                print()
                
                created_users.append({
                    "type": "teacher", 
                    "name": f"{teacher['first_name']} {teacher['last_name']}",
                    "email": email,
                    "password": password,
                    "username": teacher['username'],
                    "auth_user_id": auth_response.user.id
                })
                
                # Update the teacher record to link to auth user
                supabase.table('teachers').update({
                    "supabase_user_id": auth_response.user.id
                }).eq('id', teacher['id']).execute()
                
        except Exception as e:
            print(f"❌ Error creating teacher {teacher['first_name']}: {str(e)}")
    
    # Create summary
    print("\n" + "=" * 60)
    print("📋 SUMMARY - Test User Accounts Created")
    print("=" * 60)
    
    students_created = [u for u in created_users if u['type'] == 'student']
    teachers_created = [u for u in created_users if u['type'] == 'teacher']
    
    print(f"👨‍🎓 Students: {len(students_created)}/{len(students)}")
    print(f"👨‍🏫 Teachers: {len(teachers_created)}/{len(teachers)}")
    print()
    
    print("🔐 Login Credentials (for testing):")
    print("-" * 40)
    
    print("\n📚 STUDENTS:")
    for user in students_created:
        print(f"  {user['name']:<20} | {user['email']:<20} | demo123456")
    
    print("\n🏫 TEACHERS:")
    for user in teachers_created:
        print(f"  {user['name']:<20} | {user['email']:<20} | demo123456")
    
    print(f"\n✨ All accounts use password: demo123456")
    print(f"🌐 Test these at: http://127.0.0.1:8001/auth/test")
    print(f"📖 API docs: http://127.0.0.1:8001/docs")

if __name__ == "__main__":
    main()