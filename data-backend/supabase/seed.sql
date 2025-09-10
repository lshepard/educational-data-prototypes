-- Seed data for educational data backend demo
-- Elementary school focus with 3rd and 5th grade classes

-- Insert demo school
INSERT INTO public.schools (id, name, district, created_at, updated_at) VALUES
  ('00000000-0000-4000-8000-000000000001', 'Lincoln Elementary School', 'Riverside District', NOW(), NOW());

-- Insert demo teachers
INSERT INTO public.teachers (id, school_id, email, first_name, last_name, created_at, updated_at) VALUES
  ('00000000-0000-4000-8000-000000001001', '00000000-0000-4000-8000-000000000001', 'ms.garcia@lincoln.edu', 'Maria', 'Garcia', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000001002', '00000000-0000-4000-8000-000000000001', 'mr.thompson@lincoln.edu', 'James', 'Thompson', NOW(), NOW());

-- Insert demo classes
INSERT INTO public.classes (id, school_id, teacher_id, name, subject, semester, academic_year, created_at, updated_at) VALUES
  ('00000000-0000-4000-8000-000000002001', '00000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000001001', 'Mrs. Garcia''s 3rd Grade', 'General Elementary', 'Fall 2025', '2024-25', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000002002', '00000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000001002', 'Mr. Thompson''s 5th Grade', 'General Elementary', 'Fall 2025', '2024-25', NOW(), NOW());

-- Demo students (these would typically be created when users sign up via Supabase Auth)
-- For demo purposes, creating placeholder student records
-- In production, these would be linked to actual Supabase auth users

-- 3rd Grade Students
INSERT INTO public.students (id, school_id, supabase_user_id, email, first_name, last_name, student_number, grade_level, created_at, updated_at) VALUES
  ('00000000-0000-4000-8000-000000003001', '00000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000009001', 'emma.wilson@student.lincoln.edu', 'Emma', 'Wilson', '2025001', 3, NOW(), NOW()),
  ('00000000-0000-4000-8000-000000003002', '00000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000009002', 'liam.brown@student.lincoln.edu', 'Liam', 'Brown', '2025002', 3, NOW(), NOW()),
  ('00000000-0000-4000-8000-000000003003', '00000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000009003', 'sophia.davis@student.lincoln.edu', 'Sophia', 'Davis', '2025003', 3, NOW(), NOW()),
  ('00000000-0000-4000-8000-000000003004', '00000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000009004', 'noah.miller@student.lincoln.edu', 'Noah', 'Miller', '2025004', 3, NOW(), NOW()),
  ('00000000-0000-4000-8000-000000003005', '00000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000009005', 'olivia.jones@student.lincoln.edu', 'Olivia', 'Jones', '2025005', 3, NOW(), NOW()),

-- 5th Grade Students
  ('00000000-0000-4000-8000-000000003006', '00000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000009006', 'ethan.garcia@student.lincoln.edu', 'Ethan', 'Garcia', '2025006', 5, NOW(), NOW()),
  ('00000000-0000-4000-8000-000000003007', '00000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000009007', 'ava.rodriguez@student.lincoln.edu', 'Ava', 'Rodriguez', '2025007', 5, NOW(), NOW()),
  ('00000000-0000-4000-8000-000000003008', '00000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000009008', 'mason.martinez@student.lincoln.edu', 'Mason', 'Martinez', '2025008', 5, NOW(), NOW()),
  ('00000000-0000-4000-8000-000000003009', '00000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000009009', 'isabella.lopez@student.lincoln.edu', 'Isabella', 'Lopez', '2025009', 5, NOW(), NOW()),
  ('00000000-0000-4000-8000-000000003010', '00000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000009010', 'jacob.gonzalez@student.lincoln.edu', 'Jacob', 'Gonzalez', '2025010', 5, NOW(), NOW());

-- Enroll students in their respective classes
-- 3rd Grade enrollments
INSERT INTO public.enrollments (student_id, class_id, enrollment_status, enrolled_at) VALUES
  ('00000000-0000-4000-8000-000000003001', '00000000-0000-4000-8000-000000002001', 'active', NOW()),
  ('00000000-0000-4000-8000-000000003002', '00000000-0000-4000-8000-000000002001', 'active', NOW()),
  ('00000000-0000-4000-8000-000000003003', '00000000-0000-4000-8000-000000002001', 'active', NOW()),
  ('00000000-0000-4000-8000-000000003004', '00000000-0000-4000-8000-000000002001', 'active', NOW()),
  ('00000000-0000-4000-8000-000000003005', '00000000-0000-4000-8000-000000002001', 'active', NOW()),

-- 5th Grade enrollments
  ('00000000-0000-4000-8000-000000003006', '00000000-0000-4000-8000-000000002002', 'active', NOW()),
  ('00000000-0000-4000-8000-000000003007', '00000000-0000-4000-8000-000000002002', 'active', NOW()),
  ('00000000-0000-4000-8000-000000003008', '00000000-0000-4000-8000-000000002002', 'active', NOW()),
  ('00000000-0000-4000-8000-000000003009', '00000000-0000-4000-8000-000000002002', 'active', NOW()),
  ('00000000-0000-4000-8000-000000003010', '00000000-0000-4000-8000-000000002002', 'active', NOW());

-- Insert elementary-appropriate assignments

-- 3rd Grade assignments
INSERT INTO public.assignments (id, class_id, name, description, due_date, points_possible, assignment_type, created_at, updated_at) VALUES
  ('00000000-0000-4000-8000-000000004001', '00000000-0000-4000-8000-000000002001', 'Math Facts Practice', 'Addition and subtraction practice worksheet', '2025-09-15 15:30:00+00', 20, 'homework', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000004002', '00000000-0000-4000-8000-000000002001', 'Reading Comprehension Quiz', 'Quiz on "Charlotte''s Web" chapters 1-3', '2025-09-18 10:00:00+00', 25, 'quiz', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000004003', '00000000-0000-4000-8000-000000002001', 'Science Project: Plants', 'Observe and draw plant growth over 2 weeks', '2025-09-30 15:30:00+00', 50, 'project', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000004004', '00000000-0000-4000-8000-000000002001', 'Spelling Test', 'Weekly spelling words 1-20', '2025-09-20 09:00:00+00', 20, 'test', NOW(), NOW()),

-- 5th Grade assignments
  ('00000000-0000-4000-8000-000000004005', '00000000-0000-4000-8000-000000002002', 'Fractions Worksheet', 'Adding and subtracting fractions', '2025-09-16 15:30:00+00', 30, 'homework', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000004006', '00000000-0000-4000-8000-000000002002', 'Book Report: Wonder', 'Written report on "Wonder" by R.J. Palacio', '2025-09-25 15:30:00+00', 100, 'project', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000004007', '00000000-0000-4000-8000-000000002002', 'Solar System Quiz', 'Quiz on planets and their characteristics', '2025-09-22 10:00:00+00', 40, 'quiz', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000004008', '00000000-0000-4000-8000-000000002002', 'Geography Map Project', 'Create a map of your state with key landmarks', '2025-10-01 15:30:00+00', 75, 'project', NOW(), NOW());

-- Sample submissions with age-appropriate grades
INSERT INTO public.submissions (student_id, assignment_id, score, letter_grade, submitted_at, created_at, updated_at) VALUES
-- Emma's submissions (3rd grade)
  ('00000000-0000-4000-8000-000000003001', '00000000-0000-4000-8000-000000004001', 18.00, 'A', '2025-09-14 20:15:00+00', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000003001', '00000000-0000-4000-8000-000000004002', 23.00, 'A', '2025-09-18 09:45:00+00', NOW(), NOW()),

-- Liam's submissions (3rd grade)
  ('00000000-0000-4000-8000-000000003002', '00000000-0000-4000-8000-000000004001', 16.00, 'B', '2025-09-15 19:30:00+00', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000003002', '00000000-0000-4000-8000-000000004002', 20.00, 'B', '2025-09-18 09:50:00+00', NOW(), NOW()),

-- Ethan's submissions (5th grade)
  ('00000000-0000-4000-8000-000000003006', '00000000-0000-4000-8000-000000004005', 28.00, 'A', '2025-09-15 21:00:00+00', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000003006', '00000000-0000-4000-8000-000000004007', 38.00, 'A', '2025-09-22 09:55:00+00', NOW(), NOW()),

-- Ava's submissions (5th grade)
  ('00000000-0000-4000-8000-000000003007', '00000000-0000-4000-8000-000000004005', 25.00, 'B', '2025-09-16 18:45:00+00', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000003007', '00000000-0000-4000-8000-000000004007', 35.00, 'B', '2025-09-22 10:02:00+00', NOW(), NOW());