# Strategy

## What we're building
A system that mass-produces **custom Flock Safety pitch-card PDFs** — one per prospect account. Each PDF follows the same 3-page layout but the text and key images are tailored to that specific account's circumstances.

## Why
Flock's sales reps need to send tailored collateral to prospects. Hand-crafting each piece in design software doesn't scale. A spreadsheet-driven template lets us produce hundreds of personalized PDFs without designer time.

## Who it's for
Flock Safety sales reps (the senders). Prospects in transit, K-12, retail, healthcare, and other verticals (the recipients).

## What success looks like
- A new account → a finished, brand-compliant PDF in under 5 minutes
- Text content fed in cleanly from upstream pipeline (no manual layout work)
- Visual fidelity matches or exceeds the current hand-built collateral
- Brand always stays consistent (no drift)

## What's in scope
- HTML/CSS template that pixel-matches the reference design
- Brand kit (colors, logo, fonts, image library)
- PDF rendering pipeline (Puppeteer or equivalent)
- Image handling for per-account customization

## What's out of scope (for now)
- Writing the per-account text content (handled upstream)
- A UI for end users (data lives in a spreadsheet/Airtable)
- Multi-language support
- Variants beyond the current 3-page format
