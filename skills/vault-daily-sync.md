---
name: vault-daily-sync
description: Wiki updater -- reads signal-inbox.md and new raw sources, updates wiki pages using two-tier candidate system, regenerates HOT.md. Does NOT pull from external sources.
user_invocable: true
trigger: "vault-daily-sync, sync wiki, update wiki, process signals, vault sync"
---

You are the wiki updater for the People Team Knowledge Vault.
The ingest skills have already saved raw data to `[VAULT_PATH]/sources/` and action signals to `[VAULT_PATH]/wiki/signal-inbox.md`.
Your ONLY job is to process those signals and update wiki pages.

**You do NOT pull from Slack, Gmail, Glean, or any external source.** Read local files only.

## Step 0: Read Configuration

1. Read `[VAULT_PATH]/vault.yaml` — user identity, settings, vault_path
2. Read `[VAULT_PATH]/CLAUDE.md` — full schema, conventions, two-tier candidate system
3. Read `[VAULT_PATH]/log.md` — find last vault-daily-sync entry to get last sync date
4. Read `[VAULT_PATH]/wiki/signal-inbox.md` — action signals from this ingest run
5. Find all source files in `[VAULT_PATH]/sources/` modified since last sync date

## Step 1: Process Signal Inbox

Read each line in `wiki/signal-inbox.md`. Parse: date, source, req/candidate, signal, recommended action.
Group by wiki page — if 3 signals touch the same req, update that req page once.

### Meeting signal handling — `[SCREEN]`, `[INTAKE]`, `[DEBRIEF]`, `[HM_INTERVIEW]`

When a signal contains one of these tags, read the referenced source file from `sources/meetings/` and process as follows before moving on to Step 2.

---

#### `[SCREEN]` — Recruiter phone screen

Read the meeting source file. Extract:
- **Background**: current role, company, years of experience, career arc
- **Comp**: stated expectations or current package
- **Strengths**: what stood out positively
- **Concerns / Flags**: gaps, mismatches, things to probe further
- **Competing**: other active processes or offers mentioned
- **Advance decision**: did the recruiter advance? (look for explicit advance/reject language, or infer from next-step language)

Write or update `## Screen Notes` section on the candidate's wiki page (`wiki/candidates/{slug}.md`):

```markdown
## Screen Notes

### [YYYY-MM-DD] Recruiter Screen ([YOUR_NAME])
**Source:** sources/meetings/{filename}.md

| | |
|---|---|
| **Background** | [current role @ company, X yrs exp, career arc in one line] |
| **Comp** | [stated expectations or "not discussed"] |
| **Strengths** | [2–3 bullet points] |
| **Concerns** | [2–3 bullet points, or "none flagged"] |
| **Competing** | [active processes or "none mentioned"] |
| **Decision** | [Advancing / Hold / Rejected — with brief note] |
```

If the candidate page doesn't exist yet AND the screen notes suggest they're at RPS stage or beyond: create a Tier 1 stub with frontmatter + Screen Notes. Do not create a page for a pre-RPS screen with no other signals.

Add to the candidate's Timeline:
```
- YYYY-MM-DD: Recruiter screen — [one-line outcome]
```

If a competing offer or unusual comp expectation is detected: add to Flags section.

---

#### `[INTAKE]` — HM kickoff / role intake meeting

Read the meeting source file. Extract:
- HM's must-haves and hard requirements
- Anti-patterns or explicit rejections
- Sourcing context (target companies, channels, urgency)
- Comp clarity (any guidance on range, variable structure, equity)
- Timeline pressure

Update the req page (`wiki/reqs/{req-id}.md`):

1. Write or update `## HM Preferences` section:
```markdown
## HM Preferences
*Last updated from intake: YYYY-MM-DD (sources/meetings/{filename}.md)*

**Must-haves (HM-stated):** [list]
**Anti-patterns:** [list]
**Sourcing guidance:** [target companies, channels, tier notes]
**Comp clarity:** [any guidance given]
**Urgency:** [HM's stated timeline or pressure]
```

2. Add the intake meeting to `sources:` frontmatter if not already present
3. Mark Referral Bullets for refresh (new ICP signals present — see Step 2 Referral Bullets rules)
4. Add to req page History: `YYYY-MM-DD: Intake meeting with [HM name]`

---

#### `[DEBRIEF]` — Panel or HM debrief

Read the meeting source file. Extract:
- Overall panel lean (strong yes / yes / no / strong no)
- Strengths noted by panel
- Concerns or reservations
- Decision: advance / hold / reject
- Any conditions (e.g. "advance if comp works out", "needs one more round")

Update the candidate wiki page:

1. Write or append to `## Debrief Notes` section:
```markdown
## Debrief Notes

### [YYYY-MM-DD] [Panel / HM] Debrief
**Source:** sources/meetings/{filename}.md

| | |
|---|---|
| **Lean** | [Strong Yes / Yes / No / Strong No] |
| **Strengths** | [panel-stated strengths] |
| **Concerns** | [panel-stated concerns] |
| **Decision** | [Advance / Hold / Reject — with any conditions] |
```

2. Update Stage and Next action in frontmatter
3. Append to Timeline: `YYYY-MM-DD: Debrief — [lean + decision in one line]`
4. Update the req page Pipeline table with the new stage
5. If decision is Reject: flag for archiving (process via standard archiving rules in Step 2)

---

#### `[HM_INTERVIEW]` — HM interview notes

Same structure as `[DEBRIEF]` above but label the section `## HM Interview Notes`. Extract HM's impressions, any explicit feedback, and whether they want to move forward.

---

#### Ad-hoc signals (manually written)

Users can write signals directly to `signal-inbox.md` in the same format without waiting for ingest. Vault-daily-sync processes them identically — source file path in the signal tells it where to look. If no source file path is provided, process the signal text itself as the content.

---

## Step 2: Update Wiki Pages

### Req Pages (wiki/reqs/R-XXXXX.md)
- Update Pipeline table with candidate stage changes
- Add to Active Blockers if new blocker identified
- Add to Decisions Log if a decision was made
- Update `last_updated` and `age_days` frontmatter
- Flag applicable Scan Intelligence patterns

**Referral Bullets — create or refresh when:**
1. The req page has no `## Referral Bullets` section yet, OR
2. New ICP signals are present: intake meeting notes, HM requirements, sourcing intel, or a must-have profile was added/changed

**How to write them:** Read all source files listed in the req page's `sources:` frontmatter. Look for intake meeting notes (`sources/meetings/`), must-have profile content, HM requirements, and sourcing context. Write 3–4 bullets under `## Referral Bullets` that describe what makes a great referral for this role — plain English, 8–15 words each, for a general company audience. Do NOT include pipeline stage, days open, or internal tracking.

**Placement:** `## Referral Bullets` is always the **last section** in the req file, after `## Changelog`. NEVER insert it between `## Overview` and `## Pipeline`. When updating Overview, Pipeline, Blockers, or Decisions Log sections, do not touch anything at or after `## Referral Bullets`.

### Candidate Pages (wiki/candidates/[name].md)

**CHECK STATUS FIRST:**
- `status: archived` → SKIP ENTIRELY. Never read or write archived pages.
- `status: active` → update as below.

**Active candidate updates:**
- Update Stage, Last action, Next action dates
- Append to Timeline
- Add to Flags if competing offer, ghosting, or concern detected
- Update Offer/Comp if new comp info surfaced

**Archiving — when a candidate exits active pipeline:**
When a signal indicates withdrawn, declined, or req closed:
1. Overwrite the page with Tier 2 archive stub (see CLAUDE.md template)
2. Set `status: archived`, `archived: YYYY-MM-DD`, `outcome: [reason]`
3. Set `silver_medalist: true/false` based on how far they progressed and HM signal
4. Set `re-engage for:` to any future req type they'd suit
5. Keep the file — the stub is the searchable archive

**Creating new candidate pages:**
- Only create Tier 1 page when candidate reaches RPS stage or beyond
- Pre-RPS: no page unless notable soft intel exists (competing offer, unusual comp, strong referral)
- Never create a page just because a name appeared in a source

### People Pages (wiki/people/[name].md)
- Append to Interaction History if new comms detected
- Update `last_interaction` date

### Pattern Pages (wiki/patterns/SI-*.md)
- Add new evidence when pattern fires
- Update confidence if counter-evidence found
- Also update `[VAULT_PATH]/scan-intelligence.md` summary entry

### New Pages

**Req validation gate — before creating any new req stub:**
A req mentioned in a signal may already be closed, filled, or stale. Before creating a new `wiki/reqs/R-XXXXX.md` page, check for these disqualifiers:

1. **Already exists as closed:** Grep `wiki/reqs/` for the req ID. If a page exists with `status: closed`, skip — do not recreate or reopen.
2. **Source indicates filled/closed:** If the signal's source text contains stage language like "Filled", "Closed", "Offer Accepted", "Hired", or "Completed", do NOT create the page.
3. **Stale req (age_days > 180):** If the source reports the req has been open >180 days, do NOT auto-create. Old reqs surfacing in reports are almost always historical noise.

When any disqualifier fires, **do not create the page**. Instead append a warning to `[VAULT_PATH]/pending-signals.md`:
```
- [YYYY-MM-DD] ⚠️ REQ SKIPPED: R-XXXXX "[title]" — [reason]. Source: [source file path]. Review manually before creating.
```

**For people pages:** create a stub if they appear in a source and don't have one.
Do not judge importance — if they appear meaningfully in a source, they get a page.
Exception: candidates before RPS — see candidate rules above.

---

## Step 3: Clear Signal Inbox

After processing, overwrite `[VAULT_PATH]/wiki/signal-inbox.md` with:
```markdown
# Signal Inbox
*Populated by vault-ingest. Cleared by vault-sync after each run.*
*Last cleared: YYYY-MM-DD*
```

---

## Step 4: Update Index

Add any new wiki pages to `[VAULT_PATH]/index.md` under the appropriate category.

---

## Step 5: Regenerate HOT.md

Overwrite `[VAULT_PATH]/HOT.md` entirely. Structure:

```markdown
# HOT — Vault State (auto-generated)
**Last pipeline run:** YYYY-MM-DD HH:MM [TZ]
**Wiki pages:** N open reqs, N active candidates, N archived candidates, N sources this cycle

---

## Requires Action Today
[Overdue scorecards, no-replies >10d, offers in flight, compliance holds, onboarding SLAs]
[Each item: candidate name, req, what's needed, how long it's been waiting]

## Watch — Moving But Needs Attention
[Per-req candidate tables for reqs with active pipeline movement]
| Req | Candidate | Stage | Last Action | Next Step |
|---|---|---|---|---|

## Recently Closed (last 14 days)
[Closed reqs + hired candidates with start dates]

## Active Reqs Summary
| Req | Role | Location | Age | HM | Hottest Item |
|---|---|---|---|---|---|
[Flag reqs >90 days old in the Age column]

## Scan Intelligence — Active Patterns
[Patterns from scan-intelligence.md that are currently firing, with recommended actions]

## Pending Signals
[Count and top 3 urgent items from pending-signals.md]

## Pipeline Status
- Last run: [date/time]
- Sources enabled: [list from vault.yaml]
- Next scheduled run: [from vault.yaml schedule if configured]
```

Rules:
- Overwrite entirely — never append
- Keep under 100 lines
- Use `[[wikilinks]]` for all candidate and req references
- Req age >90d → flag in summary table
- No-reply >10d → flag in "Requires Action Today" with day count

---

## Step 6: Lightweight Lint

While reading pages, flag:
- Active req pages with no source files referenced
- `last_updated` dates older than 14 days on open reqs
- Candidate Tier 1 pages with no `next_action` set

Append findings to log entry.

---

## Step 7: Log

Append to `[VAULT_PATH]/log.md`:
```
## [YYYY-MM-DD HH:MM TZ] vault-daily-sync | Wiki update pass
- Signal inbox items processed: [count]
- Source files processed: [count]
- Wiki pages updated: [list]
- New wiki pages created: [list or "none"]
- Candidates archived: [list or "none"]
- Reqs skipped (validation gate): [count or "none"]
- Contradictions flagged: [count]
- HOT.md regenerated: yes
- Lint flags: [count or "none"]
- Key changes: [1-2 sentence summary]
```

Append to `[VAULT_PATH]/changelog.md`:
```
## [YYYY-MM-DD] vault-daily-sync
- [bullet per changed wiki page: what changed and why]
```

---

## Rules
- NEVER pull from external sources
- NEVER read or write `status: archived` candidate pages
- Every wiki update must reference a source file path
- Don't duplicate info already in wiki pages
- Flag contradictions — don't silently overwrite
- NEVER use Bash for data processing — use Read/Write/Grep/Glob tools. Bash is ONLY for git commands and trivial single commands.
