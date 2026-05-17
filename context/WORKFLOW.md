# Flock outbound system — workflow

_Captured 2026-05-16. Source of truth for every future Claude Code session._

---

## Executive summary

A scaled outbound machine that turns structured account data into coordinated, multi-channel outreach at 2000-account scale. Not a CRM. Not an insights tool. The production layer between research and send.

**Inputs.** Per-account text, per-account assets, and structured AI research on each account (local news, laws, politics, initiatives, crime) plus a Vertical Library of reusable building blocks (taglines, intros, product mixes, feature rows) that fill gaps when account-specific content is thin.

**Outputs per account.** One row of data produces five coordinated artifacts:

1. 3-page pitch card PDF (emailed)
2. Printable folder version (mailed day 2)
3. Account microsite with deep-dive links
4. Personalized outreach email (PDF + microsite link)
5. Day-2 physical drop (printed folder + swag)

**Four pillars.** Every campaign: clearly defined inputs → a template per artifact → email send → coordinated physical delivery. Once built, swapping a template or audience is days, not weeks.

**Why it scales.** Templates are version-locked and char-capped so layouts cannot break. AI research lands as structured columns, not loose docs. Only changed rows re-render. Same machine handles 2000 accounts as comfortably as 50.

**What's locked.** Render pipeline (Playwright + Drive sync) is live as draft PR #2. The 83-field template hardening starts now, one field at a time.

---

## 1. What the system is

A production line. One end takes in structured account data and AI research. The other end ships coordinated, multi-channel outreach at scale.

The pitch card PDF is the first artifact off the line. The full outreach moment per account is five coordinated outputs:

1. **Pitch card PDF** — emailed to the prospect.
2. **Print folder version** — 4-page foldable with back cover, mailed day 2.
3. **Account microsite** — same content with deep-dive links from every claim.
4. **Personalized email** — references local context, PDF attached, microsite linked.
5. **Day-2 physical drop** — printed folder + swag, mailed to the office.

One row in. Five coordinated outputs out. Sent and shipped on a synchronized schedule.

---

## 2. The four pillars

Every campaign uses the same anatomy:

**1. Clearly defined inputs.**
Per-account text + AI account research + per-account assets. Typed, validated cells. Not loose docs.

**2. A template per artifact.**
One HTML template per output. Char-capped, version-locked, visually unbreakable. Edit once, all outputs update.

**3. Email send capability.**
Personalized drafts ready in the mail client. PDF attached. Microsite linked. Subject + opening line drawn from the same row.

**4. Coordinated physical delivery.**
Daily manifest to the print and swag vendors. Account address, contact, send window. Vendors ship; delivery confirmations feed back.

Future campaigns use the same four pillars with different content.

---

## 3. Data model

Account-first. Verticals serve as a reusable library, not the primary axis.

| Table | Role | What it holds |
|---|---|---|
| **Accounts** | Primary entity | 2000 rows. Name, contact, address, vertical tag, regional stat, account-specific quote, AI-research columns (local news, laws, politics, initiatives, crime, leadership), per-account images |
| **Vertical Library** | Reusable building blocks | Tagline options, intro paragraph variants, default product mixes, feature row sets, proof points |
| **Products** | Flock catalog | Name, description, icon, deep-dive URL |
| **Testimonials** | Reusable quote pool | Linked to account, vertical, or generic |
| **Reps** | Sender records | Name, region, phone, email, QR codes |
| **Campaigns** | Batch definition | What ships when, to whom, with what swag |
| **Outputs** | State tracker | One row per (account × artifact). Drafted / approved / rendered / sent / delivered |

The Vertical Library is leverage. When account-specific content is rich, it overrides defaults. When it's thin, the library fills the gaps.

---

## 4. The pipeline, end to end

Every campaign runs the same loop: **Validate → Render → Pack → Ship.**

### Validate

Walk every account row in the campaign. Check:

- All required per-piece fields filled
- Char counts within the caps from `field_specs.csv`
- Linked vertical-library content complete
- Required images present in Drive
- Contact valid for email + mailing address

Output: a "ready / blocked" punch list. Blocked rows don't render — the report shows exactly which cells or assets need attention. Bad data never reaches the render layer.

### Render

Five renderers consume the same Account row:

| Output | Renderer | Template |
|---|---|---|
| Pitch card PDF | Playwright → PDF | `pitch-card-template.html` |
| Print folder PDF | Playwright → PDF, fold-safe layout | `pitch-card-print.html` |
| Account microsite | Static site, deep-dive links | `microsite-template.html` |
| Personalized email | Markdown personalization | `email-template.md` |
| Mailer manifest entry | CSV row | `mailer-manifest.csv` |

All five regenerate when the data changes. Only the affected template's output regenerates when a template changes.

### Pack

Bundle outputs per account. PDF + microsite URL + email draft + mailer line item all stamped with the same Account ID. Status moves to `rendered`.

### Ship

- **Day 0:** Email lands in drafts (or auto-sends). PDF attached, microsite linked. Status → `sent`.
- **Day 1:** Print and swag vendors receive the daily manifest. They print, pack, and ship the folder + goodie to the account address.
- **Day 2+:** Delivery confirmations feed back into the Outputs table. Status → `delivered`.

A campaign is just: "render this slice of accounts, send Tuesday at 9am ET, mail Wednesday." Approval triggers the batch.

---

## 5. Why it scales

- **One template, many outputs.** Fix once = all 2000 fixed. Templates are the leverage point; no artifact is ever hand-edited.
- **Hard input limits at the cell.** Each per-piece field has a char cap matching a CSS clamp. The renderer enforces it. The layout holds, even on rows no human eyeballed.
- **Only changed rows re-render.** Add 50 accounts → render 50. Update a Vertical Library tagline → re-render only the accounts using it.
- **Sample-set guardrail.** Any template change triggers a 20-row torture test (longest name, shortest, accents, missing logo, longest quote) before the full run. Catches regressions in 60 seconds.
- **AI research is structured, not loose.** It lands as columns. That's what makes it usable by templates.
- **Vendors are an output, not a person.** Daily CSV to print + swag vendors. No one addresses envelopes.

---

## 6. What we are deliberately not building

- **Not a CRM.** Existing sales tools own deal stages, activities, forecasts.
- **Not an insights generator.** AI research and Flock's analysis tools own that. We consume outputs.
- **Not a marketing automation platform.** We don't build 12-touch nurtures. We ship coordinated, high-craft outreach moments at scale.
- **Not a creative tool.** Templates are designed once and held stable. The system makes the same beautiful artifact 2000 times, not 2000 different artifacts.

This restraint is what keeps the marginal cost of a new campaign low.

---

## 7. Same machine, other campaign types

Once the pipe is live, marginal cost of a new campaign type is days:

| Campaign | Reuse |
|---|---|
| **Top-of-funnel cold outbound** (this project) | Full stack |
| **Trade-show follow-up** | Same templates, smaller batch, different swag |
| **Post-demo follow-up** | Recap PDF template + email template |
| **Customer expansion** | Different content, same machine |

Each one is the same four pillars with different inputs and a different template.

---

## 8. Next steps

### Now

1. **Field hardening, one at a time.** Walk all 83 fields in `field_specs.csv`. For each: agree the hard cap, update the CSV, update the template CSS, model the worst case. Field 1 (Flock logo) queued for "lock as-is." Field 2 (vertical headline phrase) is next.
2. **Render pipeline PR.** Open as draft #2. First CI run proves plumbing with fallback fonts. Goes fully green when Drive service account is wired up (see `markup/RENDER_SETUP.md`).

### Soon

3. **Airtable schema** — draft the 7 tables for review.
4. **Vertical Library seeded** — start with transit baseline pulled from the reference values already in `field_specs.csv`.
5. **Account intake structure** — 2000 rows, per-piece text columns + AI research columns, inline char caps shown.

### Once the pitch card PDF is locked

6. **Print/folder template** — back cover + fold-safe margins.
7. **Microsite template** — deep-dive links per claim, anchor links per section.
8. **Email draft renderer** — personalized markdown drafts.
9. **Mailer manifest** — daily CSV for print + swag vendors.

### When the loop is closed end-to-end

10. **First full campaign.** Pick a 50-account slice. Run the full pipe. Measure opens, microsite clicks, day-2 delivery confirmations, replies. Use results to plan the broader push.

---

## 9. The principle to hold

> Inputs are structured. Templates are unbreakable. Send is automated. Delivery is coordinated. Every action in the pipeline is leverage, not labor.

Every feature either reinforces that or it doesn't ship.

---

## 10. Agent roster

The pipeline is the architecture. **Agents are the workers** that do the heavy craft work inside it. Each agent is a specialized AI assistant with a narrow job, a defined set of tools, and a clear "done" criterion. Agents are swappable — improve one without touching the others.

### QA agents (run before Ship)

| Agent | Job | Reads | Writes |
|---|---|---|---|
| **Grammar / copy QA** | Proof every per-piece text cell. Catch typos, punctuation, voice drift. Suggest concise rewrites where wordy. | Account row text fields, brand voice notes | A "suggested edits" column per row; flags blockers |
| **Brand / font QA** | Verify rendered output uses correct colors, font weights, lockups. Catch substitution issues, brand drift on edited templates. | Rendered PDF, brand guidelines | Pass/fail + annotated diff for any deviation |
| **Image QA** | Source new images, size them, save with the right filename, ensure visual quality (crop, contrast, subject prominence). Flag low-res or off-brand assets. | Account row image refs, Drive asset folders | New/replacement images in Drive, sizing report |
| **Sizing / spacing QA** | Look at rendered output for layout problems a human would notice: clipped text, awkward line breaks, alignment drift, empty cells. | Rendered PDF + the source HTML | Visual issues list, suggested CSS or content fixes |

### Content agents (run during Render)

| Agent | Job |
|---|---|
| **Research agent** | Given an account name + city, pull local news, recent council votes, crime stats, leadership changes. Write structured columns on the Account row. |
| **Drafter agent** | Given an account row + research columns, draft the per-piece text (intro paragraph, regional stat, CTA reference) using the Vertical Library as a baseline. |
| **Email drafter agent** | Given the same row, write the personalized opening line and full outreach email. |
| **Validator agent** | Read each row, flag problems in plain English ("intro is 340 chars, cap is 280, here's a 270-char trim"). |

### Operations agents (run during Ship)

| Agent | Job |
|---|---|
| **Vendor coordination agent** | Build the daily print + swag manifest, push to vendors, watch for delivery confirmations, flag exceptions. |

### Design agent (separate workflow, on demand)

A creative collaborator, not part of the production line.

- Helps draft new collateral templates (recap PDFs, microsites, mailers, internal decks).
- Helps improve existing templates (proposes layout refinements, tests them against the sample-set torture test, never breaks brand).
- Reads the brand system, existing templates, and brand voice. Outputs new HTML/CSS templates ready to plug into the pipeline.
- Triggered by us, not by data events.

---

## 11. Agent setup — high level

Each agent is a few hundred lines of config, not a multi-week build. The pattern is the same every time:

1. **Define the job** — one sentence: "Proof every per-piece text cell for grammar and Flock voice." If it takes more than a sentence, split it into two agents.
2. **Pick the tools it can use** — read this Airtable view, write to this column, look at this image, render a sample PDF. Tools are narrow on purpose; the agent can't reach outside its lane.
3. **Set the trigger** — runs on a schedule (daily), on an event (new row added), or on demand (when we approve a batch).
4. **Define "done"** — what status it sets when finished, what it does when it can't decide (flag for human review, never silently fail).
5. **Run on a small sample first** — 20 rows. Read the output. Tune the instructions. Then scale.
6. **Add it to the pipeline** — slot it into Validate, Render, or Ship. The pipeline doesn't change; we just hand more work to the agent layer.

**Stack:** Agents run on the **Claude Agent SDK** (the same engine powering this conversation). Each agent lives as a small repo file describing its job, tools, and triggers. Pipeline events fire agents; agents write back to Airtable and Drive. No new infrastructure — same GitHub Actions runner, same Airtable, same Drive.

**Order of operations:**

- **First agent to build: Validator.** Highest leverage, lowest risk. Saves hours of cleanup on every batch.
- **Then Image QA.** Unlocks the 2000-account run by industrializing asset prep.
- **Then Drafter + Email Drafter.** Now the system writes for us, we edit.
- **Then Grammar QA + Brand QA.** Catches what humans miss when reviewing 2000 outputs.
- **Then Design agent.** Once we're shipping outbound, expand to new collateral types.
- **Then Research + Vendor Coordination.** Last because they touch external systems and need stable upstream first.

Each agent ships when it can run unattended on a sample-set torture test without producing garbage. None of them require ripping anything up to add the next one.
