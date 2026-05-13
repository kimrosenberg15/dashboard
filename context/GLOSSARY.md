# Glossary

Plain-English definitions for every term that comes up on this project. Read once, never ask again.

---

## Flock product terms

| Term | What it means |
|---|---|
| **LPR** | License Plate Recognition. Cameras that read license plates automatically. |
| **DFR** | Drone as First Responder. Pre-positioned drones launched in response to an incident. |
| **PTZ** | Pan-Tilt-Zoom. A camera that can be steered and zoomed remotely. |
| **NDAA compliance** | A U.S. law restricting government use of certain foreign-made cameras. "NDAA compliant" = approved for federal/agency use. |
| **Audio detection** | Microphones that identify gunshots / crashes / distress sounds and alert responders. |
| **Sensor density** | How many Flock cameras / audio detectors exist within a given region. |
| **Pitch card** | The 3-page sales collateral PDF we're templating. |
| **Collateral** | Generic marketing/sales term for any printed or PDF asset (pitch card, one-pager, brochure). |

## Project-specific terms

| Term | What it means |
|---|---|
| **The 83 fields** | Every numbered, identifiable region of the pitch card design. The canonical spec lives in `markup/field_specs.csv`. |
| **Mode** | Each field's editability classification — one of: Locked / Default / Per-piece. |
| **Locked** | Hardcoded in the template. Same on every PDF, never changes. (6 fields.) |
| **Default** | Has a baked-in value but can be overridden per piece. Inherited unless replaced. (66 fields.) |
| **Per-piece** | Set fresh on every PDF — rep info, local stats, QR target, etc. (11 fields.) |
| **Mirror field** | A field that auto-fills from another field — e.g. the footer on page 2 mirrors the footer on page 1. No separate data input. |
| **Vertical** | The industry segment a pitch is aimed at (Transit, K-12, Retail, Healthcare, etc.). Just a tag, not a data driver. |
| **Per-account customization** | The real model — every PDF is tailored to a specific prospect. Text is custom-written per recipient. |
| **Upstream pipeline** | Joe's separate project that writes the per-account text. Outputs feed into this template as inputs. |
| **Render** | The action of turning input data + template into a finished PDF. |

## Technical terms (Kim-friendly definitions)

| Term | Plain English |
|---|---|
| **Git** | A version-control system. Tracks every change to a folder of files so nothing is ever lost and we can see what changed when. |
| **GitHub** | A website that hosts git repos in the cloud. Like Google Drive for code/text. |
| **Repo** (repository) | A single project folder tracked by git. This project is one repo. |
| **Branch** | A parallel working copy of the repo. Lets us experiment without breaking the main version. |
| **Commit** | A saved snapshot of changes. Like "Save" but with a description attached. |
| **Push** | Upload local commits to GitHub so others (including AIs) can see them. |
| **Pull** | Download the latest commits from GitHub. |
| **PR** (pull request) | A proposed batch of changes, reviewed before being merged into the main version. |
| **Raw URL** | A direct link to the contents of a file in a git repo. Lets any tool read the file without using the GitHub UI. |
| **Markdown** | A plain-text format for writing documents. Uses `**bold**`, `# headers`, and `- bullets`. All our context files are markdown. |
| **HTML/CSS** | The languages websites are built in. We're using them to build the pitch-card template, then converting to PDF. |
| **Puppeteer** | A tool that drives an invisible browser (Chrome). We use it to render our HTML template into a PDF. |
| **Hex code** | A color, written as 6 characters after `#`. Example: dark green `#1F3D2B`. |
| **SVG / PNG / JPG** | Image formats. SVG = vector (scales infinitely, used for logos). PNG = lossless raster (used for icons w/ transparency). JPG = compressed raster (used for photos). |
| **DPI** | Dots per inch. Print quality measure. 300 DPI = print-ready. |
| **MCP** | Model Context Protocol. The standard that lets AI tools connect to external services (GitHub, Figma, Airtable, etc.). |
| **API key** | A password that lets a program access a service. Stored in a `.env` file, never in code. |
| **Slug** | A short, URL-safe version of a name. Example: `transit-agencies` for "Transit Agencies". |

## Brand / design terms

| Term | What it means |
|---|---|
| **Voice** | How the brand "sounds" in writing. Flock's voice is direct, outcome-led, no jargon. |
| **Tone** | The mood of a specific piece of writing — formal, urgent, warm, etc. Voice is the constant; tone varies by context. |
| **Typography** | The fonts and how they're used. |
| **Accent color** | A secondary color used sparingly for highlights, buttons, callouts. |
| **Photography direction** | The agreed style for photos — real-world / operational vs. stock / posed, etc. |
| **Pixel-match** | Visually reproduce the reference design exactly. |

## Workflow terms

| Term | What it means |
|---|---|
| **Bootstrap** | The starter file an AI reads first to learn the project (our `PROMPT.md`). |
| **End-of-session ritual** | The required wrap-up: write summary, propose decision log entry, commit. |
| **Stop hook** | A check that runs when a chat ends. Ours blocks ending if files are uncommitted. |
| **Append-only** | A file you only add to, never delete from. `DECISIONS.md` works this way. |
| **One-stop shop** | This repo. Everything for the project lives here. No outside docs to chase. |
| **Pipeline** | A series of automated steps. Joe's pipeline writes text; our pipeline renders PDF. |

---

## Add a term

If you ever ask "what does X mean?" — that term gets added here. Build it up over time.
