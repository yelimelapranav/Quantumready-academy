# Engineering tasks — mapping to ClickUp

This repo's structure mirrors the ClickUp task breakdown in the QuantumReady-Tech project (`curious-to-capable-intern-tasks.md`). Each task below links the ClickUp card to the file(s) it corresponds to, so picking up a card means knowing exactly where to start.

## Pallavi Reddy — Content, Script & Video Pipeline
[ClickUp list](https://app.clickup.com/90141438920/v/l/li/901421363690)

| ClickUp task | Starts here |
|---|---|
| Book ingestion & chunking pipeline | `pipeline/ingest/chunk_book.py` — implement `extract_chapters()` |
| LLM script-generation pipeline | `pipeline/scripts_gen/generate_scripts.py` + `prompts/lesson_script_prompt.txt` |
| Auto quiz-generation per lesson | `pipeline/quiz_gen/generate_quiz.py` |
| Internal review/QA dashboard | `pipeline/review_dashboard/app.py` |
| HeyGen avatar video generation automation | `pipeline/video_gen/heygen_client.py`, `cloudflare_stream.py` |
| [Shared] Batch-render all lessons & hand off manifest | `pipeline/video_gen/render_lesson.py` (loop over all approved scripts) + `pipeline/manifest/validate_manifest.py` before handoff |

## Pranav Yelimela — Platform, Backend & Delivery
[ClickUp list](https://app.clickup.com/90141438920/v/l/li/901421363694)

| ClickUp task | Starts here |
|---|---|
| Supabase schema | `supabase/migrations/0001_init.sql` (already drafted — review, adjust, apply) |
| Stripe Checkout integration + webhook | `apps/web/src/app/api/checkout/route.ts`, `api/stripe/webhook/route.ts` |
| Next.js lesson pages | `apps/web/src/app/academy/page.tsx`, `academy/[lessonId]/page.tsx` |
| Supabase Auth flow + access gating | Not yet stubbed — add to `apps/web/src/lib/supabase/` and gate the academy routes |
| CI/CD + deployment pipeline | `.github/workflows/ci.yml` (lint/build stub exists — add deploy step once hosting target is chosen) |
| Completion certificate flow | Not yet stubbed — new route + a PDF/HTML generation approach, TBD |
| [Stretch] "Ask the Book" RAG assistant backend | `book_chunks` table exists in the migration; no code yet — new module, likely `apps/web/src/app/api/ask/route.ts` + an embedding step (could live in `pipeline/` since it's a one-time batch job over the book, or in `apps/web` if done at query time) |
| [Shared] End-to-end integration & full course QA | Manual — full run-through once both lanes are wired to a real Supabase project |

## Manifest import (unowned — needs a decision)

Nothing currently reads `pipeline/output/manifest.json` and writes it into the `lessons` table. This is a small script (upsert by `slug`, service-role client) that could live in either lane — flagged in `docs/manifest-schema.md` as a TODO. Whoever picks it up, keep it a standalone script (`pipeline/manifest/import_to_supabase.py` or an `apps/web` admin script) rather than folding it into either the pipeline or a page route, since it needs to run on demand, not on every request.
