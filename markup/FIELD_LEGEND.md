# Pitch Card — Numbered Field Legend

Companion to `PitchCard_MARKED.pdf`. Every potentially variable field is
numbered with a red badge in the PDF. Mark up the PDF (circle / X / strike
through / sticky note) to tell me which ones you want **editable** vs
**locked**, and add any that I missed.

> ⚠️ Box placement is approximate — the badges identify the field; the box
> outlines are within ~50–100 px of true edges. The template build will use
> exact coordinates from the rebuilt HTML, not these markup boxes.

---

## Page 1 — Cover / Headline

| # | Field | Type | Notes |
|---|---|---|---|
| 1 | Flock Safety logo | image | Likely **locked** (brand) |
| 2 | Headline — "Flock Safety for [Vertical]" | text | Variable: only the vertical name swaps |
| 3 | Subheadline tagline | text | 1–2 short sentences |
| 4 | Hero image (header band) | image | Vertical-specific photo |
| 5 | Body paragraph 1 | rich text | "Problem framing" paragraph |
| 6 | Body paragraph 2 | rich text | "How Flock helps" — supports **bold** emphasis |
| 7 | "The Flock Advantage" section header | text | Likely **locked** |
| 8 | Advantage 1 — title | text | |
| 9 | Advantage 1 — description | text | |
| 10 | Advantage 2 — title | text | |
| 11 | Advantage 2 — description | text | |
| 12 | Advantage 3 — title | text | |
| 13 | Advantage 3 — description | text | |
| 14 | Advantage 4 — title | text | |
| 15 | Advantage 4 — description | text | |
| 16 | "Proven at Scale" panel header | text | Likely **locked** |
| 17 | Stat bullet 1 | text | Crime-solved % |
| 18 | Stat bullet 2 | text | Agencies-using-Flock count |
| 19 | Stat bullet 3 | text | Missing-people-reunited count |
| 20 | Stat bullet 4 | text | Officer-usage ratio |
| 21 | Stat bullet 5 | text | Local sensor density (varies by city/region) |
| 22 | Sensor-coverage diagram | image | May be region-specific |
| 23 | Footer — rep name | text | |
| 24 | Footer — rep title / region | text | |
| 25 | Footer — rep phone | text | |
| 26 | Footer — rep email | text | |
| 27 | QR code | image / URL | Generated from URL field |

---

## Page 2 — Products

| # | Field | Type | Notes |
|---|---|---|---|
| 28 | Top hero image | image | |
| 29 | Intro paragraph | rich text | |
| 30 | Section header — "Flock Products for [Vertical]" | text | Mirrors #2 vertical name |
| 31 | Product 1 — icon image | image | |
| 32 | Product 1 — name | text | |
| 33 | Product 1 — description | text | |
| 34 | Product 2 — icon image | image | |
| 35 | Product 2 — name | text | |
| 36 | Product 2 — description | text | |
| 37 | Product 3 — icon image | image | |
| 38 | Product 3 — name | text | |
| 39 | Product 3 — description | text | |
| 40 | Product 4 — icon image | image | |
| 41 | Product 4 — name | text | |
| 42 | Product 4 — description | text | |
| 43 | Product 5 — icon image | image | |
| 44 | Product 5 — name | text | |
| 45 | Product 5 — description | text | |
| 46 | Product 6 — icon image | image | |
| 47 | Product 6 — name | text | |
| 48 | Product 6 — description | text | |
| 49 | Product 7 — icon image | image | |
| 50 | Product 7 — name | text | |
| 51 | Product 7 — description | text | |
| 52 | Product 8 — icon image | image | |
| 53 | Product 8 — name | text | |
| 54 | Product 8 — description | text | |
| 55 | Compliance line | text | Likely **locked** ("…meets NDAA…") |
| 56 | Footer — rep info (repeats #23–26) | text | Driven by same fields |
| 57 | QR code (repeats #27) | image | Same URL |

> **Design question:** is the product grid always exactly 8, or should it
> support 4 / 6 / 8 product variants? Marking that decision changes whether
> products are a fixed object or a linked-records list.

---

## Page 3 — Feature Table + CTA

| # | Field | Type | Notes |
|---|---|---|---|
| 58 | Section title | text | |
| 59 | Table header row ("FEATURE" / "WHY IT MATTERS") | text | Likely **locked** |
| 60 | Row 1 — feature label | text | |
| 61 | Row 1 — why-it-matters | text | |
| 62 | Row 2 — feature label | text | |
| 63 | Row 2 — why-it-matters | text | |
| 64 | Row 3 — feature label | text | |
| 65 | Row 3 — why-it-matters | text | |
| 66 | Row 4 — feature label | text | |
| 67 | Row 4 — why-it-matters | text | |
| 68 | Row 5 — feature label | text | |
| 69 | Row 5 — why-it-matters | text | |
| 70 | Row 6 — feature label | text | |
| 71 | Row 6 — why-it-matters | text | |
| 72 | Row 7 — feature label | text | |
| 73 | Row 7 — why-it-matters | text | |
| 74 | Row 8 — feature label | text | |
| 75 | Row 8 — why-it-matters | text | |
| 76 | CTA tagline | text | Mirrors subheadline style |
| 77 | CTA body | rich text | |
| 78 | Testimonial photo | image | |
| 79 | Testimonial — attribution name | text | |
| 80 | Testimonial — attribution title / dept | text | |
| 81 | Testimonial — pull quote | text | |
| 82 | Footer — rep info (repeats #23–26) | text | |
| 83 | QR code (repeats #27) | image | |

> **Design question:** is the feature table always 8 rows, or variable?

---

## Locked-by-default candidates (confirm)

These I'd treat as **template-locked** unless you tell me otherwise:
- #1 logo, #7 section header, #16 panel header, #59 table header,
  #55 compliance line, all background colors, fonts, layout, dark-green
  panels, "The Flock Advantage" section structure, page numbering.

## Things I want to confirm I haven't missed

- [ ] Color theming (does each vertical get a different accent color, or
      always dark green?)
- [ ] Footer rep info — same on all 3 pages, driven by one Airtable rep
      record?
- [ ] QR code — does each piece get its own tracking URL, or is it
      shared per rep / per campaign?
- [ ] Sensor coverage diagram (#22) — does this swap per region/city?
- [ ] Are there variants of pages 1/2/3 you'd want (e.g. drop a page,
      add a page) or is it always exactly 3?

---

## Proposed Airtable schema

**Base:** `Flock Pitch Cards`

**Table 1 — `Verticals`** (one row per vertical pack, e.g. Transit, K-12, Retail…)
| Field | Type |
|---|---|
| Name | single line (PK) |
| Headline vertical phrase | single line — fills #2 |
| Subheadline | long text — #3 |
| Hero image (cover) | attachment — #4 |
| Hero image (products page) | attachment — #28 |
| Body paragraph 1 | long text — #5 |
| Body paragraph 2 (rich) | long text w/ markdown — #6 |
| Intro paragraph | long text — #29 |
| Stat 1–5 | long text × 5 — #17–21 |
| Sensor diagram | attachment — #22 |
| CTA tagline | single line — #76 |
| CTA body | long text — #77 |
| Products | linked → `Products` (multi, ordered) |
| Feature rows | linked → `FeatureRows` (multi, ordered, ≤8) |
| Testimonial | linked → `Testimonials` (single) |
| Accent color | single select (if needed) |

**Table 2 — `Products`** (~12–20 master rows reused across verticals)
| Field | Type |
|---|---|
| Name | single line — e.g. "LPR Cameras" |
| Icon image | attachment |
| Description | long text |

**Table 3 — `FeatureRows`** (master pool reused/edited per vertical)
| Field | Type |
|---|---|
| Feature | single line |
| Why it matters | long text |

**Table 4 — `Testimonials`**
| Field | Type |
|---|---|
| Quote | long text |
| Name | single line |
| Title | single line |
| Photo | attachment |

**Table 5 — `Reps`**
| Field | Type |
|---|---|
| Name | single line |
| Title / region | single line |
| Phone | phone |
| Email | email |
| QR target URL | URL |

**Table 6 — `Collateral`** ← the table you actually render from
| Field | Type |
|---|---|
| Slug | single line (used in output filename) |
| Vertical | linked → `Verticals` |
| Rep | linked → `Reps` |
| Custom QR URL override | URL (optional, falls back to rep) |
| Status | single select: Draft / Review / Approved / Rendered |
| Rendered PDF | attachment (filled by the renderer) |
| Render trigger | button (calls webhook) |
| Last rendered at | datetime |

The renderer reads one `Collateral` row, joins through to all the linked
data, fills the HTML template, and writes the PDF attachment back.

---

## Next steps

1. **You:** open `PitchCard_MARKED.pdf`, mark up which numbers are
   editable / locked / missing / wrong, send it back.
2. **Me:** lock the field list, then build:
   - The HTML/CSS template (pixel-matches the design)
   - The Airtable base (via MCP)
   - A Node renderer (`render.ts` — Airtable record id → PDF)
   - A small CLI / webhook to trigger renders
