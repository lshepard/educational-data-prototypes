-- Initial schema for educational data backend
-- FERPA-compliant design with row-level security

-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- Schools table
create table public.schools (
    id uuid default gen_random_uuid() primary key,
    name varchar(255) not null,
    district varchar(255),
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Teachers table
create table public.teachers (
    id uuid default gen_random_uuid() primary key,
    school_id uuid not null references public.schools(id),
    supabase_user_id uuid references auth.users(id),
    email varchar(255) not null,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null,
    unique(supabase_user_id)
);

-- Students table (linked to Supabase auth users)
create table public.students (
    id uuid default gen_random_uuid() primary key,
    school_id uuid not null references public.schools(id),
    supabase_user_id uuid not null references auth.users(id),
    email varchar(255) not null unique,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    student_number varchar(50),
    grade_level integer,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null,
    unique(supabase_user_id)
);

-- Classes table
create table public.classes (
    id uuid default gen_random_uuid() primary key,
    school_id uuid not null references public.schools(id),
    teacher_id uuid not null references public.teachers(id),
    name varchar(255) not null,
    subject varchar(100),
    semester varchar(50),
    academic_year varchar(10), -- e.g., "2024-25"
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Student enrollments in classes
create table public.enrollments (
    id uuid default gen_random_uuid() primary key,
    student_id uuid not null references public.students(id),
    class_id uuid not null references public.classes(id),
    enrollment_status varchar(20) default 'active',
    enrolled_at timestamp with time zone default timezone('utc'::text, now()) not null,
    unique(student_id, class_id)
);

-- Assignments
create table public.assignments (
    id uuid default gen_random_uuid() primary key,
    class_id uuid not null references public.classes(id),
    name varchar(255) not null,
    description text,
    due_date timestamp with time zone,
    points_possible integer,
    assignment_type varchar(50), -- homework, quiz, test, project
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Student submissions
create table public.submissions (
    id uuid default gen_random_uuid() primary key,
    student_id uuid not null references public.students(id),
    assignment_id uuid not null references public.assignments(id),
    score decimal(5,2),
    letter_grade varchar(5),
    submitted_at timestamp with time zone,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null,
    unique(student_id, assignment_id)
);

-- Create indexes for performance
create index idx_students_supabase_user_id on public.students(supabase_user_id);
create index idx_students_school_id on public.students(school_id);
create index idx_enrollments_student_id on public.enrollments(student_id);
create index idx_enrollments_class_id on public.enrollments(class_id);
create index idx_assignments_class_id on public.assignments(class_id);
create index idx_submissions_student_id on public.submissions(student_id);
create index idx_submissions_assignment_id on public.submissions(assignment_id);

-- Enable Row Level Security (RLS)
alter table public.schools enable row level security;
alter table public.teachers enable row level security;
alter table public.students enable row level security;
alter table public.classes enable row level security;
alter table public.enrollments enable row level security;
alter table public.assignments enable row level security;
alter table public.submissions enable row level security;

-- RLS Policies for FERPA compliance

-- Students can only see their own data
create policy "Students can view own profile" on public.students
    for select using (auth.uid() = supabase_user_id);

create policy "Students can update own profile" on public.students
    for update using (auth.uid() = supabase_user_id);

-- Students can only see enrollments for themselves
create policy "Students can view own enrollments" on public.enrollments
    for select using (
        student_id in (
            select id from public.students where supabase_user_id = auth.uid()
        )
    );

-- Students can see classes they're enrolled in
create policy "Students can view enrolled classes" on public.classes
    for select using (
        id in (
            select class_id from public.enrollments 
            where student_id in (
                select id from public.students where supabase_user_id = auth.uid()
            )
        )
    );

-- Students can see assignments for their classes
create policy "Students can view class assignments" on public.assignments
    for select using (
        class_id in (
            select class_id from public.enrollments 
            where student_id in (
                select id from public.students where supabase_user_id = auth.uid()
            )
        )
    );

-- Students can see their own submissions
create policy "Students can view own submissions" on public.submissions
    for select using (
        student_id in (
            select id from public.students where supabase_user_id = auth.uid()
        )
    );

create policy "Students can insert own submissions" on public.submissions
    for insert with check (
        student_id in (
            select id from public.students where supabase_user_id = auth.uid()
        )
    );

create policy "Students can update own submissions" on public.submissions
    for update using (
        student_id in (
            select id from public.students where supabase_user_id = auth.uid()
        )
    );

-- Teachers can see students in their classes and related data
create policy "Teachers can view own students" on public.students
    for select using (
        school_id in (
            select school_id from public.teachers where supabase_user_id = auth.uid()
        )
        and id in (
            select student_id from public.enrollments
            where class_id in (
                select id from public.classes 
                where teacher_id in (
                    select id from public.teachers where supabase_user_id = auth.uid()
                )
            )
        )
    );

create policy "Teachers can view own classes" on public.classes
    for select using (
        teacher_id in (
            select id from public.teachers where supabase_user_id = auth.uid()
        )
    );

create policy "Teachers can manage own classes" on public.classes
    for all using (
        teacher_id in (
            select id from public.teachers where supabase_user_id = auth.uid()
        )
    );

-- Admins/service role can access all data (for API operations)
create policy "Service role can access all schools" on public.schools
    for all using (auth.role() = 'service_role');

create policy "Service role can access all teachers" on public.teachers
    for all using (auth.role() = 'service_role');

create policy "Service role can access all students" on public.students
    for all using (auth.role() = 'service_role');

create policy "Service role can access all classes" on public.classes
    for all using (auth.role() = 'service_role');

create policy "Service role can access all enrollments" on public.enrollments
    for all using (auth.role() = 'service_role');

create policy "Service role can access all assignments" on public.assignments
    for all using (auth.role() = 'service_role');

create policy "Service role can access all submissions" on public.submissions
    for all using (auth.role() = 'service_role');

-- Function to automatically update updated_at timestamp
create or replace function public.handle_updated_at()
returns trigger as $$
begin
    new.updated_at = timezone('utc'::text, now());
    return new;
end;
$$ language plpgsql;

-- Create triggers for updated_at
create trigger handle_updated_at before update on public.schools
    for each row execute function public.handle_updated_at();

create trigger handle_updated_at before update on public.teachers
    for each row execute function public.handle_updated_at();

create trigger handle_updated_at before update on public.students
    for each row execute function public.handle_updated_at();

create trigger handle_updated_at before update on public.classes
    for each row execute function public.handle_updated_at();

create trigger handle_updated_at before update on public.assignments
    for each row execute function public.handle_updated_at();

create trigger handle_updated_at before update on public.submissions
    for each row execute function public.handle_updated_at();