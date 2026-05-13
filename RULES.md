# RULES — Operating Rules for AI Tools on the Flock Project

Any AI tool / chat working on this project must follow these rules.

---

## ⚡ Top rules (never break these)

### Rule 0 — Do everything you can yourself
Never ask the user to copy, paste, log in, click, or perform any task you can do via tools (git, GitHub MCP, file edits, web fetches, code execution). Drive every step to completion. Ask the user only when you genuinely need a decision or external information that's unavailable to you.

### Rule 1 — Scale-ready, not over-engineered
Build with the assumption this template system will extend to other marketing and sales collateral. But ship the immediate Flock pitch card fast. Push back any time we start:
- Adding abstractions for hypothetical future use cases
- Building "platform" features before the first artifact is shipped
- Choosing complex tooling when a simple file solves it
- Designing schemas richer than current needs

Concrete heuristic: if a feature isn't needed for the Flock pitch card v1, it waits.

### Rule 2 — Concise, comparative, recommended
- Always lead with the answer or recommendation
- For any comparison, use a **table**, not prose paragraphs
- Always recommend the best **long-term option** (call it out explicitly)
- No long exposition. No thinking-out-loud. No filler paragraphs.
- One-sentence wrap-up at the end of non-trivial responses

User is non-technical. Define jargon once or avoid it.

---

## A. Reading order (every session)

1. `PROMPT.md`
2. `context/STRATEGY.md`, `DECISIONS.md`, `BRAND.md`, `PEOPLE.md`, `GLOSSARY.md`
3. `context/ARCHITECTURE.md` if doing technical work
4. `markup/field_specs.csv` if discussing fields

## B. Communication

- Plain language. No emojis unless requested.
- Short paragraphs. Bullets. Tables.
- Don't restate the question.
- Don't pad with caveats.

## C. Decision-making

- Propose one option with rationale; don't dump matrices unless asked for a comparison
- When asked to compare: table, recommendation, done
- Use AskUserQuestion only for genuine ambiguity

## D. In scope

- HTML/CSS template, brand styling, image handling
- PDF rendering (Puppeteer)
- Brand kit files
- Spec maintenance (`markup/field_specs.csv`)
- Context maintenance (`context/`)
- Git, GitHub, file ops, code execution

## E. Out of scope

- Writing per-account text content (Joe's pipeline does this)
- Inventing brand colors / fonts / photography style without user direction
- Reproducing verbatim copy from the reference PDF beyond brief illustrative snippets (IP)
- Destructive git ops without confirmation
- Touching files outside this repo

## F. End-of-session ritual (REQUIRED)

At the end of every meaningful chat:
1. 1-line session summary
2. Propose addition to `context/DECISIONS.md`
3. Note updates to BRAND / STRATEGY / GLOSSARY if relevant
4. Add entries to `context/OPEN_QUESTIONS.md` if any
5. Commit + push

Non-optional.

## G. File conventions

- Markdown for context files
- Lowercase-hyphens for assets; UPPERCASE for root docs
- Decisions append-only, never delete
- Dates in `YYYY-MM-DD`
- Reference relevant context file in commit messages

## H. Visual / design

- Pixel-match reference PDF unless told otherwise
- Brand colors from `brand/brand.css` only — never invent hex
- Images from `brand/assets/` or per-piece URLs — never inline base64
- Fonts licensed and in `brand/assets/fonts/` or a documented web font
- Template must absorb 25% text-length variance without breaking

## I. Data

- `markup/field_specs.csv` is canonical
- All 83 rows always visible
- Mode counts: 6 Locked, 66 Default, 11 Per-piece — flag any change
- One input row = one PDF. Flat model.

## J. Code

- Semantic HTML + CSS custom properties for theming
- Puppeteer (Chromium headless) for rendering
- Runnable from fresh clone with documented dependencies
- No hardcoded secrets — use `.env` + `.env.example`

## K. Confidentiality

- Flock brand + reference material is proprietary
- Repo stays private
- Don't share content outside this repo / conversation
- No public package publishing

## L. Mistakes

If you made an error in a prior turn: acknowledge, fix, log to DECISIONS.md, move on. Don't over-apologize.

---

## Resolved policy (per Kim, 2026-05-13)

- ✅ **Auto PR test (render a PDF on each PR):** Yes — add once template exists
- ❌ **Backup beyond git:** No, git is enough
- ✅ **Solo review on visual changes:** Yes, no two-person review needed
