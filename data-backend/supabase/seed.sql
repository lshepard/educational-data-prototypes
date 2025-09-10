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

-- Sample students - one from each grade plus Maya who's in both classes
INSERT INTO public.students (id, school_id, supabase_user_id, email, first_name, last_name, student_number, grade_level, created_at, updated_at) VALUES
  ('00000000-0000-4000-8000-000000003001', '00000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000009001', 'emma.wilson@demo.test', 'Emma', 'Wilson', '2025001', 3, NOW(), NOW()),
  ('00000000-0000-4000-8000-000000003006', '00000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000009006', 'ethan.garcia@demo.test', 'Ethan', 'Garcia', '2025006', 5, NOW(), NOW()),
  ('00000000-0000-4000-8000-000000003020', '00000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000009020', 'maya.chen@demo.test', 'Maya', 'Chen', '2025020', 4, NOW(), NOW());

-- Enroll students in their respective classes
INSERT INTO public.enrollments (student_id, class_id, enrollment_status, enrolled_at) VALUES
  -- Emma in 3rd Grade
  ('00000000-0000-4000-8000-000000003001', '00000000-0000-4000-8000-000000002001', 'active', NOW()),
  -- Ethan in 5th Grade
  ('00000000-0000-4000-8000-000000003006', '00000000-0000-4000-8000-000000002002', 'active', NOW()),
  -- Maya in both classes (shows cross-grade enrollment)
  ('00000000-0000-4000-8000-000000003020', '00000000-0000-4000-8000-000000002001', 'active', NOW()),
  ('00000000-0000-4000-8000-000000003020', '00000000-0000-4000-8000-000000002002', 'active', NOW());

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
  ('00000000-0000-4000-8000-000000004008', '00000000-0000-4000-8000-000000002002', 'Geography Map Project', 'Create a map of your state with key landmarks', '2025-10-01 15:30:00+00', 75, 'project', NOW(), NOW()),

-- Additional assignments to show Maya's strengths and weaknesses
-- Math assignments (where Maya excels)
  ('00000000-0000-4000-8000-000000004020', '00000000-0000-4000-8000-000000002001', 'Multiplication Tables Quiz', 'Times tables 1-12 quiz', '2025-09-12 10:00:00+00', 25, 'quiz', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000004021', '00000000-0000-4000-8000-000000002001', 'Word Problems Practice', 'Mixed addition, subtraction, multiplication word problems', '2025-09-08 15:30:00+00', 30, 'homework', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000004022', '00000000-0000-4000-8000-000000002002', 'Decimal Operations Test', 'Adding, subtracting, multiplying decimals', '2025-09-10 10:00:00+00', 40, 'test', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000004023', '00000000-0000-4000-8000-000000002002', 'Geometry Shapes Quiz', 'Identifying angles, perimeter, area', '2025-09-07 10:00:00+00', 35, 'quiz', NOW(), NOW()),

-- Reading assignments (where Maya struggles)  
  ('00000000-0000-4000-8000-000000004024', '00000000-0000-4000-8000-000000002001', 'Vocabulary Test', 'Weekly vocabulary words with definitions', '2025-09-11 09:00:00+00', 20, 'test', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000004025', '00000000-0000-4000-8000-000000002002', 'Reading Comprehension Assessment', 'Multiple choice questions on assigned reading', '2025-09-09 10:00:00+00', 50, 'test', NOW(), NOW());

-- Sample submissions with age-appropriate grades
INSERT INTO public.submissions (student_id, assignment_id, score, letter_grade, submitted_at, created_at, updated_at) VALUES
-- Emma's submissions (3rd grade) - sample performance
  ('00000000-0000-4000-8000-000000003001', '00000000-0000-4000-8000-000000004001', 18.00, 'A', '2025-09-14 20:15:00+00', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000003001', '00000000-0000-4000-8000-000000004002', 23.00, 'A', '2025-09-18 09:45:00+00', NOW(), NOW()),

-- Ethan's submissions (5th grade) - sample performance
  ('00000000-0000-4000-8000-000000003006', '00000000-0000-4000-8000-000000004005', 28.00, 'A', '2025-09-15 21:00:00+00', NOW(), NOW()),
  ('00000000-0000-4000-8000-000000003006', '00000000-0000-4000-8000-000000004007', 38.00, 'A', '2025-09-22 09:55:00+00', NOW(), NOW()),

-- MAYA'S SUBMISSIONS - Shows math strengths and reading challenges
-- Maya's MATH assignments (A's and B's - her strength)
  ('00000000-0000-4000-8000-000000003020', '00000000-0000-4000-8000-000000004001', 19.00, 'A', '2025-09-14 19:45:00+00', NOW(), NOW()), -- Math Facts Practice (3rd)
  ('00000000-0000-4000-8000-000000003020', '00000000-0000-4000-8000-000000004005', 29.00, 'A', '2025-09-16 20:30:00+00', NOW(), NOW()), -- Fractions Worksheet (5th)
  ('00000000-0000-4000-8000-000000003020', '00000000-0000-4000-8000-000000004020', 24.00, 'A', '2025-09-12 09:45:00+00', NOW(), NOW()), -- Multiplication Tables Quiz
  ('00000000-0000-4000-8000-000000003020', '00000000-0000-4000-8000-000000004021', 27.00, 'A', '2025-09-08 14:20:00+00', NOW(), NOW()), -- Word Problems Practice
  ('00000000-0000-4000-8000-000000003020', '00000000-0000-4000-8000-000000004022', 36.00, 'A', '2025-09-10 09:55:00+00', NOW(), NOW()), -- Decimal Operations Test
  ('00000000-0000-4000-8000-000000003020', '00000000-0000-4000-8000-000000004023', 32.00, 'B', '2025-09-07 09:50:00+00', NOW(), NOW()), -- Geometry Shapes Quiz

-- Maya's READING assignments (C's and D's - her challenge area)
  ('00000000-0000-4000-8000-000000003020', '00000000-0000-4000-8000-000000004002', 16.00, 'D', '2025-09-18 09:30:00+00', NOW(), NOW()), -- Reading Comprehension Quiz (3rd)
  ('00000000-0000-4000-8000-000000003020', '00000000-0000-4000-8000-000000004006', 68.00, 'C', '2025-09-25 15:45:00+00', NOW(), NOW()), -- Book Report: Wonder (5th)
  ('00000000-0000-4000-8000-000000003020', '00000000-0000-4000-8000-000000004024', 14.00, 'C', '2025-09-11 08:45:00+00', NOW(), NOW()), -- Vocabulary Test
  ('00000000-0000-4000-8000-000000003020', '00000000-0000-4000-8000-000000004025', 32.00, 'D', '2025-09-09 10:15:00+00', NOW(), NOW()); -- Reading Comprehension Assessment