# The lesson manifest — the contract between the two lanes

This is the one hard interface between the content pipeline (Pallavi) and the platform (Pranav). Both sides should treat this file as the source of truth if code and docs ever disagree — update this doc in the same PR as any schema change.

The pipeline's batch-render step (`pipeline/manifest/schema.py`) emits one JSON object per lesson, in an array, to `pipeline/output/manifest.json`. The platform imports this file to populate the `lessons` table (see `supabase/migrations/0001_init.sql`).

## Shape

```json
{
  "slug": "lesson-02-bits-vs-qubits",
  "order_index": 2,
  "title": "Bits vs. Qubits",
  "transcript": "Full spoken-script text, as narrated...",
  "cloudflare_video_id": "31c9d6e3f4b2...",
  "duration_seconds": 342,
  "quiz": [
    {
      "question": "What can a qubit represent that a classical bit can't?",
      "choices": ["A negative number", "A superposition of 0 and 1", "A decimal value", "A null value"],
      "answer_index": 1
    }
  ]
}
```

## Field notes

- **slug** — stable, human-readable, used as the URL segment (`/academy/lesson-02-bits-vs-qubits`). Never reuse or reorder existing slugs once published; add new ones instead.
- **order_index** — controls display/unlock order. Gaps are fine; ties are not (pipeline should assert uniqueness before emitting).
- **cloudflare_video_id** — set only after the video is actually uploaded to Cloudflare Stream (`pipeline/video_gen/cloudflare_stream.py`). A manifest entry with this null should not be marked `published` on import.
- **quiz** — array, not a single object, even for one question. `answer_index` is 0-based into `choices`.

## Import step (platform side, TODO)

`apps/web` (or a small standalone script) should read `pipeline/output/manifest.json` and upsert into `lessons` by `slug`, using the Supabase **service-role** key (bypasses RLS — this is an admin/import path, never exposed to the browser). Not yet implemented — see `docs/engineering-tasks.md`.
