-- Minimal local dev seed — one placeholder lesson so apps/web has something to render
-- before the real pipeline output exists. Safe to re-run (idempotent on slug).

insert into lessons (slug, order_index, title, cloudflare_video_id, duration_seconds, transcript, quiz, published)
values (
  'lesson-00-welcome',
  0,
  'Welcome to Quantum Ready Academy',
  null,                          -- fill in once a real Cloudflare Stream video exists
  180,
  'This is placeholder transcript text for local development.',
  '[{"question": "Is this a placeholder lesson?", "choices": ["Yes", "No"], "answer_index": 0}]'::jsonb,
  true
)
on conflict (slug) do nothing;
