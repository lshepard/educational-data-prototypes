-- Student App Data Storage
-- Allows frontend applications to store arbitrary data tied to authenticated students
-- FERPA-compliant with proper RLS policies

-- Create student_app_data table
create table public.student_app_data (
    id uuid default gen_random_uuid() primary key,
    student_id uuid not null references public.students(id) on delete cascade,
    app_key varchar(100) not null, -- Identifies the application (e.g., 'edubot', 'learning_dashboard')
    data_key varchar(200) not null, -- Key for the data (e.g., 'chat_history', 'preferences', 'progress')
    data_value jsonb not null, -- The actual data stored as JSON
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null,
    
    -- Ensure unique combination of student, app, and key
    unique(student_id, app_key, data_key)
);

-- Create indexes for performance
create index idx_student_app_data_student_id on public.student_app_data(student_id);
create index idx_student_app_data_app_key on public.student_app_data(app_key);
create index idx_student_app_data_composite on public.student_app_data(student_id, app_key);
create index idx_student_app_data_created_at on public.student_app_data(created_at);

-- Enable Row Level Security
alter table public.student_app_data enable row level security;

-- RLS Policies for FERPA compliance

-- Students can only access their own app data
create policy "Students can view own app data" on public.student_app_data
    for select using (
        student_id in (
            select id from public.students where supabase_user_id = auth.uid()
        )
    );

create policy "Students can insert own app data" on public.student_app_data
    for insert with check (
        student_id in (
            select id from public.students where supabase_user_id = auth.uid()
        )
    );

create policy "Students can update own app data" on public.student_app_data
    for update using (
        student_id in (
            select id from public.students where supabase_user_id = auth.uid()
        )
    );

create policy "Students can delete own app data" on public.student_app_data
    for delete using (
        student_id in (
            select id from public.students where supabase_user_id = auth.uid()
        )
    );

-- Service role can access all data (for API operations)
create policy "Service role can access all app data" on public.student_app_data
    for all using (auth.role() = 'service_role');

-- Add updated_at trigger
create trigger handle_updated_at before update on public.student_app_data
    for each row execute function public.handle_updated_at();