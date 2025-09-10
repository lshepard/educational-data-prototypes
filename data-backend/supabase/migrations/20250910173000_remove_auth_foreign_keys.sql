-- Remove foreign key constraints to auth.users for demo purposes
-- This allows us to seed demo data without creating actual auth users

-- Drop the foreign key constraint on students.supabase_user_id
alter table public.students drop constraint if exists students_supabase_user_id_fkey;

-- Drop the foreign key constraint on teachers.supabase_user_id  
alter table public.teachers drop constraint if exists teachers_supabase_user_id_fkey;

-- Keep the columns as UUID but without the foreign key constraint
-- This way we can still use them for linking when real auth users exist