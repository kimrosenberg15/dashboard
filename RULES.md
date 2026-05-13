# RULES — Operating Rules for AI Tools on the Flock Project

Any AI tool / chat working on this project must follow these rules. Pasted into PROMPT.md context on every session.

---

## A. Reading order (always)

1. Read `PROMPT.md` first
2. Then `context/STRATEGY.md`, `context/DECISIONS.md`, `context/BRAND.md`, `context/PEOPLE.md`, `context/GLOSSARY.md`
3. Then `context/ARCHITECTURE.md` if doing technical work
4. Then `markup/field_specs.csv` if discussing fields
5. Only respond after reading the above

## B. Communication style

- Kim is non-technical. Plain language always. No jargon without defining it.
- Concise by default. Short paragraphs, bullet lists, short sentences.
- No emojis unless explicitly requested.
- Don't restate the question.
- Don't pad with caveats. If you're confident, say it.
- One-sentence summary at the end of any non-trivial response.

## C. Decision-making

- When uncertain between two reasonable options, **propose one with rationale** — don't dump a comparison matrix on Kim.
- Use the AskUserQuestion tool only for genuinely ambiguous design decisions, not for things you can decide and let Kim correct.
- Match your action to what was asked. Don't expand scope.

## D. What's in scope for the AI

- Visual design (HTML/CSS template, brand styling, image handling)
- PDF rendering pipeline (Puppeteer or equivalent)
- Brand kit assets (logo, colors, fonts as files)
- Spec maintenance (`markup/field_specs.csv`)
- Context maintenance (`context/` files, end-of-session updates)
- Repo operations (commits, pushes, PRs, file management)

## E. What's NEVER in scope

- Writing the per-account text content for the customizable fields (Joe's pipeline does this)
- Inventing brand colors, fonts, or photography style without explicit user direction
- Reproducing verbatim copy from the reference PDF beyond brief illustrative snippets (IP/copyright)
- Making destructive git ops without confirmation (force push, hard reset, branch deletion)
- Creating new GitHub repos unless asked
- Touching files outside `kimrosenberg15/dashboard` (renamed to Flock-Current)

## F. End-of-session ritual (REQUIRED)

At the end of any meaningful chat, before user signs off, the AI must:
1. Write a 1-line session summary
2. Propose an addition to `context/DECISIONS.md` (date-stamped)
3. Note any updates to other context files (BRAND, STRATEGY, GLOSSARY, etc.)
4. Note any new entries for `context/OPEN_QUESTIONS.md`
5. Ask user to approve → commit

This is non-optional. Without it, context rots.

## G. File conventions

- All context files are markdown (`.md`)
- All file names use lowercase-with-hyphens for assets, UPPERCASE for context/root docs
- Decisions are append-only — never delete, only add
- Dates use ISO format: `YYYY-MM-DD`
- Commits should reference the relevant context file when applicable

## H. Visual / design rules

- Pixel-match the reference PDF unless explicitly told otherwise
- Use brand colors from `brand/brand.css` — never invent hex codes
- All images load from `brand/assets/` or per-piece URLs — never inline base64
- Fonts must be licensed and stored in `brand/assets/fonts/` or via a web font with documented terms
- All text must support 25% length variance without breaking layout (some accounts will have longer/shorter text)

## I. Data rules

- The 83-field spec in `markup/field_specs.csv` is canonical
- All 83 rows always stay visible in any view of the spec
- Three-state Mode (Locked/Default/Per-piece) is the source of truth
- Mode counts: 6 Locked, 66 Default, 11 Per-piece — flag if this changes
- One row of input data = one PDF. No relational tables.

## J. Code rules

- HTML/CSS template uses semantic HTML + CSS custom properties for theming
- Rendering via Puppeteer (Chromium headless) — no proprietary tools
- All scripts must be runnable from a fresh clone with documented dependencies
- No hardcoded secrets in code — use `.env` (and `.env.example` template)

## K. Confidentiality

- Treat all Flock brand assets and reference material as proprietary
- Do not share project content outside this repo or this conversation
- Do not publish to public package registries without permission
- The repo is private; keep it that way

## L. When to push back

If the user requests something that:
- Conflicts with these rules
- Violates the IP/copyright restriction (re-rendering copyrighted text verbatim)
- Risks destructive data loss
- Is architecturally inconsistent with prior decisions in DECISIONS.md

…flag it briefly and propose an alternative. Don't silently comply.

## M. Mistake handling

If you (the AI) made an error in a prior turn:
- Acknowledge it directly
- Propose the fix
- Add an entry to DECISIONS.md noting what went wrong and the correction
- Don't apologize repeatedly — fix it and move on

---

## Open question for the user (mark answered when decided)

- [ ] Should we add automated tests on PR (e.g., render-a-PDF check)? Probably yes once template exists.
- [ ] Backup cadence — is git enough, or do we want periodic exports of context files?
- [ ] Two-person review on visual changes before commit, or solo OK?
