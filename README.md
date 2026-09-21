# Quantum Ready Academy

*("Curious to Capable" — the course's working tagline, from quantumreadyea.org's own "quantum-curious to quantum-capable" line.)*

A gated, video-based course adapted from Sundeep's book, delivered at `quantumreadyea.org/academy`. Lessons are generated from the book via an LLM pipeline, narrated by an AI avatar (HeyGen), hosted on Cloudflare Stream, and served through a Next.js app backed by Supabase (auth, enrollment, progress) and Stripe (payment).

**Start here:** [`docs/DEV_GUIDE.md`](docs/DEV_GUIDE.md)

## Repo layout

```
Quantumready-academy/
├── apps/web/          # Next.js app — lesson pages, auth, Stripe checkout/webhook (Pranav's lane)
├── pipeline/           # Python content pipeline — book ingestion, script/quiz generation,
│                       #   HeyGen avatar video automation, review dashboard (Pallavi's lane)
├── supabase/           # Postgres schema (migrations) shared by both lanes
├── docs/                # Dev guide, architecture, manifest contract, task mapping
└── .github/workflows/   # CI stubs
```

## Status

Scaffold stage — directory structure, stubbed routes/schema/pipeline modules with real contracts and TODOs, not yet wired to live credentials. See `docs/DEV_GUIDE.md` for setup and `docs/engineering-tasks.md` for how this maps to the ClickUp task lists.

## Related project docs
- ClickUp task breakdown: `curious-to-capable-intern-tasks.md` (QuantumReady-Tech project)
- Stack rationale: `book-to-course-lms-stack-and-tasks.md` (QuantumReady-Tech project)
