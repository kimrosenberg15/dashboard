# Flock Collateral — Memory Index
_Last updated: 2026-05-14_

## Files in this folder

| File | Contents |
|------|----------|
| MEMORY.md | This index + quick-start + session protocol |
| project.md | Full project spec — pitch card system, current status, file structure |
| preferences.md | Kim's working style and Claude interaction rules |
| profile.md | Kim's personal context — role, tools, accounts |
| changelog.md | Session-by-session log of what changed |

## Quick-start for a new session
1. Read all files in this folder before doing anything.
2. This repo builds a **pitch card PDF generator for Flock Safety** (transit technology company).
3. Canonical data: `markup/field_specs.csv` — 83 fields, always authoritative.
4. Edit via github.dev, GitHub API, or bash sandbox. Never ask Kim to do manual steps.
5. Kim expects hands-off execution — no check-ins mid-task unless truly ambiguous.
6. Always read memory files first, then ask one focused clarifying question if needed, then execute.

## End-of-session update protocol
At the end of every session where anything changed, update without being asked:

**Always update:**
- `changelog.md` — one entry at top with today's date + bullet per change (keep it short)

**Update if project structure or status changed:**
- `project.md` — update the relevant section only

**Update if Kim's preferences changed:**
- `preferences.md`

**Update if field specs changed:**
- Note in `project.md`, commit updated `markup/field_specs.csv`

**Update if a decision was made:**
- Append to `context/DECISIONS.md`

Do not ask Kim whether to update. Just do it silently and mention it in one line at the end.
