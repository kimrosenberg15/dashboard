# Decisions Journal

Append-only log of choices made and their rationale. Newest at top.

---

## 2026-05-13 — Context system + prompt scaffolding
Set up `PROMPT.md` + `CLAUDE.md` + `context/` folder so any tool/chat can bootstrap from a single git URL. Pattern: paste raw URL of `PROMPT.md` into any new chat → it reads strategy/decisions/brand/people automatically.

## 2026-05-13 — Visual scope, text out of scope
My (Claude's) work is the **visual side** only: HTML/CSS template, brand styling, images, render pipeline. **Text content for all customizable fields is pre-written upstream** (by Joe's separate project) and fed in per-piece as input. We do not source, manage, or generate copy.

## 2026-05-13 — Single flat data model (no relational tables)
Dropped the multi-table Airtable schema (Verticals / Products / FeatureRows / etc). Reality: each PDF is heavily customized per-account; "vertical" is just one tag, not the driver of content. **One row = one PDF.** All 77 customizable fields are columns on a single sheet.

## 2026-05-13 — Three-state Mode classification
Replaced binary Editable=Yes/No with a 3-state `Mode` column:
- **Locked** (6) — hardcoded in template
- **Default** (66) — has a baked-in value; can be overridden per piece
- **Per-piece** (11) — set on every PDF

## 2026-05-13 — All 83 fields stay visible
The spec table always shows all 83 numbered fields, including the locked ones. Cleaner mental model.

## 2026-05-13 — Stay in git, no Figma
Brand iteration happens through code (HTML/CSS + live PDF render), not Figma. User isn't a designer; describing changes works fine. Brand kit will live in `brand/brand.css` once seeded.

## 2026-05-13 — Architecture: HTML/CSS + Puppeteer
Chose this over fillable PDF (image swaps too fragile) and over SaaS (Bannerbear/Documint — recurring cost, less control). HTML+CSS gives pixel-perfect output, version control, and free renders.

## 2026-05-13 — Field markup + spec sheet
Produced `markup/PitchCard_MARKED.pdf` with 83 numbered red badges identifying every potentially-variable field, plus `markup/field_specs.csv` and `.xlsx` as the canonical spec table. Box coordinates approximate — real coordinates come from rebuilt HTML.

## 2026-05-13 — Repo location
Project lives in `kimrosenberg15/dashboard` for now (originally meant to spin up a separate `flock-collateral` repo but GitHub integration was scoped to dashboard). Migration to a dedicated repo is deferred.
