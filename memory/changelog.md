# Session Changelog

## 2026-05-17 — Render pipeline + Joe's sheet integration
- Confirmed CI is green: render pipeline self-healed, PDF grew from 165KB → 472KB (real assets resolving)
- Added `markup/generate_from_sheet.py`: reads Joe's Pitch Card Spec spreadsheet (account list tab, rows 3-7), generates one `account-<slug>.html` per row, substitutes all `{{PC_*}}` placeholders
- Wired into workflow between fetch_assets and render steps; non-fatal if Sheets API not yet enabled
- RENDER_SETUP.md: added Step 5 (enable Sheets API + share spreadsheet with SA)
- Pending: Kim needs to enable Sheets API in GCP + share spreadsheet with SA email to unlock per-account renders
- Pending: field hardening pass (all 83 fields, one-by-one)

## 2026-05-15 — SCWA pitch card product thumbnail images
- Processed 20/21 product thumbnails (240×240px JPG) for SCWA pitch card Images_Products folder
- Sources: PRODUCTS WIP Drive folder, flocksafety.com CDN, Flock Safety Platform page
- MISSING.txt added for Crash Detection (AVIF CORS block), Professional Services (source too small), Wrong-Way Driving Detection (source too small)
- 1 alternate saved (Analytics & Reporting_A)

## 2026-05-14 — Context structure setup
- Added memory/ folder (MEMORY.md, project.md, preferences.md, profile.md, changelog.md)
- Rewrote CLAUDE.md as comprehensive single-entry-point for any LLM (replaces thin PROMPT.md pointer)
- Added .github/workflows/refresh-claude-md.yml for daily auto-refresh
- Structure now mirrors VFO repo pattern: CLAUDE.md entry point + memory/ for session continuity
