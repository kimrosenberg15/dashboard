# Flock Collateral — Claude Code Context
_Last auto-refreshed: 2026-05-16. Do not edit manually._

## What This Is
Kim's pitch-card PDF generator for **Flock Safety** — a transit technology company.
Builds dynamic, data-driven 3-page PDF pitch cards for transit agencies and other verticals, customized per sales rep and account.

- **Repo:** github.com/kimrosenberg15/dashboard (private, main = source of truth)
- **Stack:** HTML/CSS template + Puppeteer (headless Chromium) for PDF rendering
- **Canonical data:** `markup/field_specs.csv` — 83 fields, never contradict it
- **Domain docs:** `context/` folder (STRATEGY, BRAND, PEOPLE, DECISIONS, GLOSSARY)
- **Session memory:** `memory/` folder — read at start, update at end

## Session Start (every session, no exceptions)
1. Read this file
2. Read `memory/MEMORY.md` — full index, quick-start, session protocol
3. Read `memory/project.md`, `memory/preferences.md`, `memory/profile.md`
4. Read `context/DECISIONS.md` to see what has been decided
5. Read `context/WORKFLOW.md` — full outbound system architecture (SSOT for the pipeline)
6. Read `context/BRAND_ASSETS.md` — SSOT for brand assets, Drive folder IDs, logo usage. **Update in the same commit whenever touching a brand asset.**
7. Read `markup/field_specs.csv` if the session involves fields

## Key Architecture
- **3-page pitch card:** Page 1 (headline/brand panel), Page 2 (products grid), Page 3 (feature table + CTA)
- **83 fields:** Locked (6) | Default (66) | Per-piece (11)
- **Airtable schema (planned):** Verticals / Products / FeatureRows / Testimonials / Reps / Collateral
- **One input row = one PDF** — flat data model, not relational
- **Brand:** Colors from `brand/brand.css` only — never invent hex values

## How to Edit & Push
- All edits via GitHub API, github.dev, or bash sandbox — never ask Kim to do manual steps
- Patch via targeted edits — never rewrite whole files unless asked
- Commit directly to `main`; PRs only for large changes
- Reference the relevant context file in every commit message

## Kim's Rules

### Non-negotiable
- **Do everything yourself** — never ask Kim to copy, paste, click, or take manual steps
- **Ship the current thing first** — no abstractions for hypothetical future use cases; if not needed for Flock pitch card v1, it waits
- **Lead with the answer** — one recommendation with rationale; no option matrices unless a comparison is specifically requested

### Communication
- Short and direct — no padding, no restating the question, no thinking-out-loud
- Define jargon once or avoid it — Kim is non-technical
- Tables for comparisons, bullets for lists — no long prose paragraphs
- Send the direct link when something is built — don't describe it

### End of Session (required — every meaningful session, do silently)
1. Update `memory/changelog.md` — one entry at top, bullets per change
2. Propose additions to `context/DECISIONS.md`
3. Commit + push all context updates
Mention it in one line at the end. Do not ask permission.

### Out of Scope
- Writing per-account text content (that is a separate upstream system)
- Inventing brand colors or fonts without direction
- Destructive git ops without confirmation
- Touching files outside this repo

## Key Decisions (resolved)
| Decision | Status |
|---|---|
| Auto PR test (render PDF on each PR) | Yes — once template exists |
| Backup beyond git | No |
| Solo review on visual changes | Yes, no two-person review needed |

## Spec Docs
- Field spec (canonical): `markup/field_specs.csv`
- Session memory: `memory/` folder
- Domain context: `context/` folder
- Full operating rules: `RULES.md`
- Term definitions: `GLOSSARY.md`
