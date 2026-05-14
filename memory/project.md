# Flock Collateral — Project Spec
_Last updated: 2026-05-14_

## What It Is
A dynamic pitch-card PDF generator for **Flock Safety**, a transit technology company.
Generates customized 3-page pitch cards for transit agency sales — customized per vertical, rep, and account.

## Pitch Card Structure
- **Page 1:** Brand hero — headline, tagline, body copy, Flock Advantage items, Proven at Scale stats panel
- **Page 2:** Products grid — intro text, 8 products per vertical
- **Page 3:** Feature table + CTA — feature comparison rows, CTA block (eyebrow, booking heading/blurb, testimonial photo/quote, QR code)

## Field System (83 fields — `markup/field_specs.csv` is canonical)
| Mode | Count | Meaning |
|------|-------|---------|
| Locked | 6 | Fixed content, never changes |
| Default | 66 | Vertical-level default, can be overridden |
| Per-piece | 11 | Changes per rep/account/collateral piece |

Column structure: #, Type, Mode, Table, Field Name, Account Data, Input Prompt, Constraint, Example, Notes

## Airtable Schema (planned)
| Table | Purpose |
|-------|---------|
| Verticals | Per-vertical defaults (transit, etc.) |
| Products | Product grid content per vertical |
| FeatureRows | Feature comparison table rows |
| Testimonials | Customer quotes + photos |
| Reps | Sales rep info (name, booking link, etc.) |
| Collateral | Per-piece output record |

## Tech Stack
- **Template:** Semantic HTML + CSS custom properties for theming
- **Rendering:** Puppeteer (headless Chromium)
- **Brand colors:** `brand/brand.css` only — never hardcode hex
- **Images:** `brand/assets/` or per-piece URLs — no inline base64
- **Model:** One input row = one PDF (flat, not relational)

## Current Status (2026-05-14)
| Component | Status |
|-----------|--------|
| 83 fields in `markup/field_specs.csv` | Done |
| `markup/PitchCard_MARKED.pdf` — numbered markup | Done |
| `markup/FIELD_LEGEND.md` — field table + Airtable schema | Done |
| `context/` folder (STRATEGY, BRAND, PEOPLE, DECISIONS, GLOSSARY) | Done |
| HTML/CSS template | Not yet built |
| Puppeteer renderer | Not yet built |
| Airtable base | Not yet built |
| Auto PDF render on PR | Planned once template exists |

## File Structure
```
dashboard/
├── CLAUDE.md              <- Start here every session
├── RULES.md               <- Full operating rules
├── GLOSSARY.md            <- Plain-English definitions
├── markup/
│   ├── field_specs.csv    <- CANONICAL (83 fields)
│   ├── field_specs.xlsx
│   ├── FIELD_LEGEND.md
│   ├── PitchCard_MARKED.pdf
│   └── page-1/2/3.png
├── context/
│   ├── STRATEGY.md
│   ├── BRAND.md
│   ├── PEOPLE.md
│   ├── DECISIONS.md
│   └── GLOSSARY.md
├── memory/
│   ├── MEMORY.md          <- Session index
│   ├── project.md         <- This file
│   ├── preferences.md
│   ├── profile.md
│   └── changelog.md
├── brand/                 <- Brand assets (planned)
└── .github/workflows/
    └── refresh-claude-md.yml
```

## Open Questions
- Always 8 products on page 2, or variable count?
- Always 8 feature rows on page 3, or variable count?
- Accent color per vertical or always brand green?
- QR code scope: per-rep, per-collateral, or per-campaign?
- Sensor diagram: swaps per region?
