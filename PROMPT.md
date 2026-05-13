# Flock Collateral — Operating Prompt

You are working on the **Flock Safety pitch-card collateral generator**. Before responding to any new request, read these files in order:

1. `context/STRATEGY.md` — why this project exists, who it serves, what success looks like
2. `context/DECISIONS.md` — running journal of choices made and their rationale
3. `context/BRAND.md` — brand rules, voice, visual direction
4. `context/PEOPLE.md` — who is involved and their role
5. `markup/field_specs.csv` — the canonical 83-field spec (the artifact map)

All four context files are short. Read them all every session.

## Project at a glance

We're turning a fixed 3-page Flock Safety pitch-card PDF into a template that mass-produces **custom per-account** versions. The text content is written upstream (by another project) and fed in per-piece. **My job is the visual side**: HTML/CSS template, brand styling, image handling, PDF rendering.

## Repo conventions

- All work lands on the active development branch
- Spec lives in `markup/field_specs.csv` (canonical) and `field_specs.xlsx` (derived view)
- Context lives in `context/` — append-only journal of decisions
- Brand assets land in `brand/` once we have them
- HTML template lives in `template/` (once built)

## Working style

- Be concise. User is non-technical — explain in plain language.
- One flat data model, not relational. Each PDF = one row of inputs.
- All 83 fields stay visible in the spec table even if locked.
- Iterate visually through code (live PDF render), not Figma.

## End-of-session ritual

At the end of any meaningful conversation, propose a diff to `context/DECISIONS.md` summarizing what was decided. User approves → commit.
