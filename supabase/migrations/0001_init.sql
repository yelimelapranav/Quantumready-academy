-- Quantum Ready Academy — initial schema
-- Applies on top of Supabase's built-in `auth.users` table.

create extension if not exists "pgvector";

-- One row per lesson, populated from the content pipeline's manifest hand-off
-- (see docs/manifest-schema.md). This is the hard interface between the two lanes.
create table if not exists lessons (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,               -- e.g. "lesson-01-bits-vs-qubits"
  order_index int not null,
  title text not null,
  cloudflare_video_id text,                 -- set once the pipeline uploads the rendered video
  duration_seconds int,
  transcript text,
  quiz jsonb,                               -- [{ "question": "...", "choices": [...], "answer_index": 0 }, ...]
  published boolean not null default false,
  created_at timestamptz not null default now()
);

create table if not exists enrollments (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  stripe_checkout_session_id text,
  status text not null default 'pending' check (status in ('pending', 'active', 'refunded', 'cancelled')),
  enrolled_at timestamptz,
  created_at timestamptz not null default now(),
  unique (user_id)
);

create table if not exists lesson_progress (
  user_id uuid not null references auth.users(id) on delete cascade,
  lesson_id uuid not null references lessons(id) on delete cascade,
  watched boolean not null default false,
  quiz_score numeric,                       -- fraction correct, e.g. 0.8
  completed_at timestamptz,
  updated_at timestamptz not null default now(),
  primary key (user_id, lesson_id)
);

-- Stretch goal: "Ask the Book" RAG assistant — chunked book text + embeddings.
create table if not exists book_chunks (
  id uuid primary key default gen_random_uuid(),
  chapter text,
  chunk_index int,
  content text not null,
  embedding vector(1536),                   -- adjust dimension to match the embedding model used
  created_at timestamptz not null default now()
);

-- Row-level security: every table above holds per-user or content data.
alter table enrollments enable row level security;
alter table lesson_progress enable row level security;
alter table lessons enable row level security;

create policy "users read own enrollment"
  on enrollments for select
  using (auth.uid() = user_id);

create policy "users read own progress"
  on lesson_progress for select
  using (auth.uid() = user_id);

create policy "users upsert own progress"
  on lesson_progress for insert
  with check (auth.uid() = user_id);

create policy "users update own progress"
  on lesson_progress for update
  using (auth.uid() = user_id);

create policy "published lessons are readable by enrolled users"
  on lessons for select
  using (
    published = true
    and exists (
      select 1 from enrollments
      where enrollments.user_id = auth.uid() and enrollments.status = 'active'
    )
  );

-- TODO(Pranav): service-role writes to `lessons` (from the pipeline manifest importer) and
-- the Stripe webhook's writes to `enrollments` both go through the service-role key, which
-- bypasses RLS by design — no policy needed for those paths.
