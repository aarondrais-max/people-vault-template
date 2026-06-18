# People Team Knowledge Vault — Claude Schema (Recruiter)

This is a local recruiting knowledge vault maintained by Claude. When operating in this project, follow all conventions below exactly.

## Vault Owner Context
- **Name:** [YOUR_NAME]
- **Role:** [YOUR_ROLE] (e.g., Senior Recruiter, EMEA)
- **Org:** [YOUR_ORG] (e.g., Talent Acquisition, Acme Corp)
- **Timezone:** [YOUR_TIMEZONE] (e.g., America/New_York, Europe/London, Asia/Tokyo)
- **Slack ID:** [YOUR_SLACK_ID]
- **ATS:** Greenhouse (default — update if different)

## Vault Location
`[VAULT_PATH]` (e.g., `~/Documents/my-recruiting-vault`) — all paths are relative to this root.

---

## Directory Structure

```
vault/
├── CLAUDE.md             ← this file
├── vault.yaml            ← config + pipeline settings
├── HOT.md                ← auto-regenerated state snapshot (read this first each session)
├── scan-intelligence.md  ← learned recruiting patterns, updated by pipeline
├── pending-signals.md    ← raw signals awaiting triage
├── index.md              ← cross-reference index of all wiki pages
├── log.md                ← pipeline run log
├── changelog.md          ← wiki change history
│
├── sources/              ← immutable raw ingest records
│   ├── slack/
│   ├── gmail/
│   ├── glean/
│   ├── meetings/
│   └── documents/
│
├── wiki/                 ← maintained structured pages
│   ├── reqs/             ← one page per open requisition
│   ├── candidates/       ← one page per candidate (active or archived)
│   ├── people/           ← stakeholders, HMs, key relationships
│   ├── patterns/         ← scan intelligence patterns (cross-req)
│   ├── decisions/        ← key decisions with rationale
│   ├── concepts/         ← market intel, comp benchmarks, process notes
│   ├── projects/         ← cross-functional TA projects
│   └── threads/          ← active tracked conversations
│
├── queries/              ← on-demand query results
├── outputs/              ← daily briefs archive
└── skills/               ← pipeline skill definitions
```

---

## Wiki Page Templates

### wiki/reqs/R-XXXXX.md
```markdown
---
type: req
req_id: R-XXXXX
title: [Role Title] [Location]
status: open | closed | on-hold
hm: [Hiring Manager Name]
stakeholders: []
location: [City / Country / Region]
opened: YYYY-MM-DD
age_days: N
last_updated: YYYY-MM-DD
slack_channel: [channel-name without #]
---

# R-XXXXX — [Role Title] [Location]

## Overview
[1-2 sentence summary of the role and current state]

## Pipeline
| Candidate | Stage | Last Action | Next Step | Owner | Notes |
|---|---|---|---|---|---|

## Active Blockers
-

## Decisions Log
-

## HM Preferences
*Last updated from intake: YYYY-MM-DD (sources/meetings/{filename}.md)*

**Must-haves (HM-stated):** [list]
**Anti-patterns:** [list]
**Sourcing guidance:** [target companies, channels, tier notes]
**Comp clarity:** [any guidance given]
**Urgency:** [HM's stated timeline or pressure]

## Scan Intelligence Triggers
[Patterns from scan-intelligence.md that apply to this req]

## History
- YYYY-MM-DD: [event]

## Changelog
- YYYY-MM-DD: [what changed and why]

## Referral Bullets
*Maintained by vault-daily-sync. Do not edit manually — update source intel and let the pipeline refresh.*
- [Plain-language bullet describing ideal referral profile, 8–15 words]
- [Bullet 2]
- [Bullet 3]
```

**Referral Bullets placement:** Always the **last section** in the file, after `## Changelog`. This keeps it out of the pipeline's active editing zone.

**Referral Bullets maintenance rule:** `vault-daily-sync` owns the `## Referral Bullets` section. When creating a new req page OR when new ICP signals arrive (intake meeting, HM requirements, sourcing intel), regenerate this section. Write 3–4 plain-language bullets for a general company audience — what should a teammate look for in a referral? Pull from HM Preferences, intake meeting notes, and sourcing context. Do NOT include pipeline stage, days open, or internal tracking. Each bullet: 8–15 words, plain English, referral-audience-friendly.

---

### wiki/candidates/[firstname-lastname].md

Two tiers. Use the correct one based on stage.

---

**TIER 1 — Active candidate (RPS and beyond)**
Full page. Pipeline maintains this. Soft intel that the ATS doesn't capture.

```markdown
---
type: candidate
status: active
name: [Full Name]
req_id: R-XXXXX
req_title: [Role]
location: [City, Country]
stage: rps | hm | final | offer
last_action: YYYY-MM-DD
next_action: YYYY-MM-DD
owner: [YOUR_NAME]
---

# [Full Name]

## Current Status
**Stage:** [stage] | **Req:** R-XXXXX — [title]
**Last action:** [description] on YYYY-MM-DD
**Next step:** [description] by YYYY-MM-DD

## Background
[Current role, company, relevant experience — focus on what's NOT in the ATS]

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

## Interview Signal
[What interviewers said beyond the scorecard — tone, fit read, concerns]

## Offer / Comp
[Comp expectations, what they shared vs what's in the ATS, exception details]

## Flags
[Competing offers + deadlines, relocation constraints, visa needs, timeline pressure]

## Meeting Notes
[Meeting title(s) for deeper notes — link to sources/meetings/ files]

## Timeline
- YYYY-MM-DD: [event]
```

---

**TIER 2 — Archived candidate (screened out, withdrawn, closed req)**
Lightweight stub. Written once when candidate exits active pipeline. Never updated by pipeline.

```markdown
---
type: candidate
status: archived
name: [Full Name]
req_id: R-XXXXX
req_title: [Role]
location: [City, Country]
archived: YYYY-MM-DD
outcome: withdrawn | declined | not-progressed | hired
silver_medalist: true | false
---

# [Full Name]

**Req:** R-XXXXX — [Role] | **Location:** [City]
**Outcome:** [1 line — why not progressed or what happened]
**Silver medalist:** [yes/no — why they'd be worth revisiting]
**Re-engage for:** [e.g., "EMEA Enterprise AE if opens", "any APAC SE req"]
**Comp range:** [what they told you]
**Key notes:** [1-2 lines of soft intel worth keeping]
**Meeting notes:** [source file path for deeper reference]
```

---

**Pipeline rules for candidate pages:**
- Create Tier 1 when candidate reaches RPS (recruiter phone screen) stage
- Downgrade to Tier 2 (archive) when candidate exits active pipeline — overwrite content with stub, keep filename
- Early screens (pre-RPS): no page created unless they have notable soft intel worth keeping (competing offer, unusual comp, strong referral)
- Pipeline skips all `status: archived` pages — they are never read or written after creation
- Silver medalist index: any page with `silver_medalist: true` is queryable for future req matching

---

### wiki/people/[name].md
```markdown
---
type: person
name: [Full Name]
relationship: manager | hm | stakeholder | peer | candidate
slack_handle: @handle
last_interaction: YYYY-MM-DD
---

# [Full Name]

## Role & Context
[Title, team, why they matter to your work]

## Interaction History
[Key conversations, decisions, commitments — most recent first]

## Preferences / Style
[Communication style, response patterns, what they care about in hiring]

## Active Reqs
[Reqs they're hiring for or influencing]
```

### wiki/patterns/SI-[pattern-name].md
```markdown
---
type: pattern
name: [Pattern Name]
confidence: low | medium | high
reqs_observed: []
last_updated: YYYY-MM-DD
---

# Pattern: [Name]

## Signal
[What triggers this pattern — what you observe in sources]

## Recommended Action
[What to do when this pattern fires]

## Evidence
- [req / candidate / date]: [what happened]

## Counter-evidence
-
```

---

## Pipeline Conventions

### Sources
- Raw ingest files go in `sources/[type]/YYYY-MM-DD-[source]-[topic].md`
- **Never edit source files** — they are immutable records
- Each source file has frontmatter: `source`, `date`, `type`, `processed: true/false`

### Pipeline Source of Truth
- If `ingests.pipeline_sheet.enabled: true`, the Greenhouse-fed Google Sheet is **authoritative for candidate stage and active/rejected status**. `ingest-pipeline-sheet` snapshots it to `sources/pipeline/` and emits `[PIPELINE]` signals; `vault-daily-sync` reconciles req Pipeline tables from it.
- **Stage precedence:** sheet > comms. When a Slack/email/meeting signal implies a different stage than the sheet, the sheet wins and the conflict is flagged in `pending-signals.md` — never silently overwritten.
- **Comms still own the soft layer:** competing offers, comp asks, sentiment, momentum, "what moved" — none of that is in the ATS, so it stays comms-derived and is never overwritten by a sheet sync.
- If no pipeline sheet is configured, pipeline state is fully comms-derived (as current as the last run, as complete as what surfaced in your comms).
- The Amplitude TA Toolkit reads these same req/candidate pages when its profile has `uses_vault: true` — so authoritative stage + soft context flow into hm-update, candidate-summary, and the other vault-aware skills automatically.

### Wiki Updates
- The pipeline reads sources, synthesizes, and updates wiki pages
- Changes are appended to `changelog.md` with date + skill that made the change
- Pipeline runs are logged in `log.md`
- HOT.md is regenerated at end of every pipeline run

### Scan Intelligence
- Patterns go in `scan-intelligence.md` and in `wiki/patterns/`
- When a pattern fires during ingest, add it to the relevant req and candidate pages

### Signal Inbox
- Ingest skills write action signals to `wiki/signal-inbox.md`
- Format: `- [YYYY-MM-DD] [source] [req/candidate] [signal text] → [recommended action]`
- `vault-daily-sync` reads and clears the inbox each run

### pending-signals.md
- Unclassified ingest signals land here for triage
- Format: `- [YYYY-MM-DD] [source] [signal text] → [suggested action]`
- Cleared during vault-daily-sync

---

## Key Relationships Reference
*Replace with your actual hiring managers and stakeholders*

| Name | Role | Signal Priority |
|---|---|---|
| [Manager Name] | Your direct manager | HIGH — manager comms |
| [HR Leader Name] | Head of People / CHRO | HIGH — org decisions |
| [Stakeholder Name] | Business leader / headcount authority | HIGH — headcount sign-off |
| [HM Name] | Hiring Manager | MEDIUM |
| [HM Name] | Hiring Manager | MEDIUM |

---

## Session Boot Sequence
1. Read `HOT.md` — get current vault state
2. Read `pending-signals.md` — anything urgent needing triage?
3. If today is a pipeline day and no run yet — offer to run `/vault-orchestrator`
4. Answer user questions using wiki pages as context

Do NOT re-read all wiki pages on boot — HOT.md is the summary. Only pull individual wiki pages when asked about a specific req, candidate, or person.
