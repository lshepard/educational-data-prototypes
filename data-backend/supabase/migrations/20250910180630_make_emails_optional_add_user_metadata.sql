-- Make emails optional and update existing data with fake emails
-- This allows user assignment via metadata rather than email matching

-- Make email optional for students
ALTER TABLE public.students ALTER COLUMN email DROP NOT NULL;

-- Make email optional for teachers  
ALTER TABLE public.teachers ALTER COLUMN email DROP NOT NULL;

-- Remove the unique constraint on student email since we'll allow nulls
ALTER TABLE public.students DROP CONSTRAINT IF EXISTS students_email_key;

-- Update existing students with fake emails or null
UPDATE public.students SET email = 
  CASE 
    WHEN first_name = 'Emma' THEN 'demo.student1@test.local'
    WHEN first_name = 'Liam' THEN 'demo.student2@test.local'  
    WHEN first_name = 'Sophia' THEN 'demo.student3@test.local'
    WHEN first_name = 'Noah' THEN 'demo.student4@test.local'
    WHEN first_name = 'Olivia' THEN 'demo.student5@test.local'
    WHEN first_name = 'Ethan' THEN 'demo.student6@test.local'
    WHEN first_name = 'Ava' THEN 'demo.student7@test.local'
    WHEN first_name = 'Mason' THEN 'demo.student8@test.local'
    WHEN first_name = 'Isabella' THEN 'demo.student9@test.local'
    WHEN first_name = 'Jacob' THEN 'demo.student10@test.local'
    ELSE NULL
  END;

-- Update existing teachers with fake emails
UPDATE public.teachers SET email = 
  CASE 
    WHEN first_name = 'Maria' THEN 'demo.teacher1@test.local'
    WHEN first_name = 'James' THEN 'demo.teacher2@test.local'
    ELSE NULL
  END;

-- Add a username field for easier identification (optional)
ALTER TABLE public.students ADD COLUMN username VARCHAR(50);
ALTER TABLE public.teachers ADD COLUMN username VARCHAR(50);

-- Set usernames based on names  
UPDATE public.students SET username = 
  CASE 
    WHEN first_name = 'Emma' THEN 'emma.wilson'
    WHEN first_name = 'Liam' THEN 'liam.brown'
    WHEN first_name = 'Sophia' THEN 'sophia.davis' 
    WHEN first_name = 'Noah' THEN 'noah.miller'
    WHEN first_name = 'Olivia' THEN 'olivia.jones'
    WHEN first_name = 'Ethan' THEN 'ethan.garcia'
    WHEN first_name = 'Ava' THEN 'ava.rodriguez'
    WHEN first_name = 'Mason' THEN 'mason.martinez'
    WHEN first_name = 'Isabella' THEN 'isabella.lopez'
    WHEN first_name = 'Jacob' THEN 'jacob.gonzalez'
    ELSE NULL
  END;

UPDATE public.teachers SET username = 
  CASE 
    WHEN first_name = 'Maria' THEN 'maria.garcia'
    WHEN first_name = 'James' THEN 'james.thompson'
    ELSE NULL
  END;