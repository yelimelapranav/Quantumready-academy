# Dev Guide — Quantum Ready Academy

Welcome. This repo has two independent lanes that meet at one file (the manifest — see below). Read the section for your lane; skim the other so you know what you're plugging into.

## Repo layout

```
Quantumready-academy/
├── apps/web/       Next.js app — lesson pages, auth, Stripe checkout/webhook   (Pranav)
├── pipeline/        Python — book ingestion, script/quiz generation,           (Pallavi)
│                    HeyGen avatar video automation, review dashboard
├── supabase/        Postgres schema (migrations) — shared by both lanes
└── docs/            You are here
```

## The one thing to understand before writing any code

The pipeline (Pallavi) produces `pipeline/output/manifest.json`. The platform (Pranav) imports that file into the `lessons` table. That's the entire interface between the two lanes — full shape and field-by-field notes are in **`docs/manifest-schema.md`**. If you're ever unsure whether something is "your lane's problem," check whether it's upstream or downstream of the manifest.

The system diagram is in `docs/architecture.md`, and the ClickUp-task-to-file mapping is in `docs/engineering-tasks.md` — start there once you know which card you're picking up.

## Prerequisites (both lanes)

- Node.js 20+ and npm
- Python 3.11+
- A Supabase project (free tier is fine to start) — https://supabase.com
- Accounts/API keys as you reach the tasks that need them: Stripe, HeyGen, Cloudflare (Stream), Anthropic (or whichever LLM the team settles on)

Copy `.env.example` at the repo root and read it — it documents every credential either lane needs and which lane uses it. Never commit a real `.env` file; `.gitignore` already excludes them.

## Setting up `apps/web` (Pranav)

```bash
cd apps/web
npm install
cp .env.example .env.local   # fill in real values
npm run dev                  # http://localhost:3000
```

Apply the Supabase schema before the app will have anything to render:

```bash
# From the Supabase dashboard's SQL editor, or via the Supabase CLI:
supabase db push   # applies supabase/migrations/0001_init.sql
psql "$SUPABASE_DB_URL" -f supabase/seed.sql   # optional: one placeholder lesson for local dev
```

Route map so far (all stubbed, see `docs/engineering-tasks.md` for what's left):
- `GET /academy` — lesson list
- `GET /academy/[lessonId]` — single lesson (video + quiz)
- `POST /api/checkout` — creates a Stripe Checkout session
- `POST /api/stripe/webhook` — Stripe calls this on payment completion

## Setting up `pipeline/` (Pallavi)

```bash
cd pipeline
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in real values
```

Pipeline stages run in order, each a separate script so you can inspect output between steps (especially the human-review checkpoint after script generation):

```bash
python -m pipeline.ingest.chunk_book --input path/to/book.pdf
python -m pipeline.scripts_gen.generate_scripts
# --- review every file in pipeline/output/scripts/ before continuing ---
python -m pipeline.quiz_gen.generate_quiz --script pipeline/output/scripts/lesson-00.txt   # repeat per lesson, or wrap in a loop once the shape feels right
python -m pipeline.video_gen.render_lesson --script pipeline/output/scripts/lesson-00.txt --slug lesson-00-welcome --order 0 --title "Welcome"
python -m pipeline.manifest.validate_manifest
```

Run the review dashboard any time to see what's been generated so far:

```bash
streamlit run pipeline/review_dashboard/app.py
```

## Branching & PRs

- Branch off `main`: `feature/<short-description>` (e.g. `feature/quiz-generation`).
- Open a PR into `main` even for small changes — CI (`.github/workflows/ci.yml`) runs lint on both lanes.
- If a PR changes the manifest shape, update `docs/manifest-schema.md` in the same PR — it's the source of truth and it's easy for it to drift silently otherwise.
- Tag the other person for review on anything that touches the manifest boundary, even if it's "just" your own lane's code — a silent shape change on one side breaks the other side without warning.

## Where things stand right now

This is a scaffold: real file/route/schema structure with working contracts, but no code has been run against live credentials yet. Every file with a `TODO(name)` comment is an open task — cross-reference with `docs/engineering-tasks.md` and the ClickUp lists to see what's next.

## Questions / decisions still open

See `docs/architecture.md`'s "Open decisions" section — LLM provider choice, where `apps/web` ultimately gets mounted relative to quantumreadyea.org, and RAG-assistant timing are all flagged there rather than assumed.
