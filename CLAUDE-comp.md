# People Team Knowledge Vault — Claude Schema (Comp & Total Rewards)

This is a local Comp & Total Rewards knowledge vault maintained by Claude. When operating in this project, follow all conventions below exactly.

## Vault Owner Context
- **Name:** [YOUR_NAME]
- **Role:** [YOUR_ROLE] (e.g., Senior Compensation Analyst, Director of Total Rewards)
- **Org:** [YOUR_ORG] (e.g., People & Culture, Acme Corp)
- **Timezone:** [YOUR_TIMEZONE] (e.g., America/New_York, Europe/London, Asia/Tokyo)
- **Slack ID:** [YOUR_SLACK_ID]
- **Job Families Supported:** [list your scope, e.g., all company-wide, or GTM + Engineering]

## Vault Location
`[VAULT_PATH]` (e.g., `~/Documents/my-comp-vault`) — all paths are relative to this root.

---

## What This Vault Tracks

You work in Compensation and Total Rewards. Your vault captures:
- Offer decisions and their economics (not candidates — the comp side of offers)
- Compensation benchmarks by job family and level
- Comp review cycles: annual, semi-annual, focal, equity refresh
- Exception requests and the precedents they set
- Market data refresh status by job family
- Key stakeholder relationships (finance BPs, legal, HMs who bring comp questions)

**What this vault does NOT track:** Candidate profiles or recruiting pipeline status. Those belong in the recruiting vault.

---

## Directory Structure

```
vault/
├── CLAUDE.md             ← this file
├── vault.yaml            ← config + pipeline settings
├── HOT.md                ← auto-regenerated state snapshot (read this first each session)
├── pending-signals.md    ← raw signals awaiting triage
├── index.md              ← cross-reference index of all wiki pages
├── log.md                ← pipeline run log
├── changelog.md          ← wiki change history
│
├── sources/              ← immutable raw ingest records
│   ├── slack/
│   ├── gmail/
│   ├── meetings/
│   └── documents/
│
├── wiki/                 ← maintained structured pages
│   ├── offers/           ← pending and recent offer decisions (comp economics, not candidates)
│   ├── benchmarks/       ← job family comp ranges, market data, internal equity
│   ├── decisions/        ← exceptions approved, comp philosophy calls, equity grants
│   ├── cycles/           ← annual review, focal, equity refresh — timeline and status
│   ├── people/           ← key stakeholders (CFO, finance BPs, legal, HMs who ask a lot)
│   └── projects/         ← job architecture, comp system implementations, audits
│
├── queries/              ← on-demand query results
├── outputs/              ← daily briefs archive
└── skills/               ← pipeline skill definitions
```

---

## Wiki Page Templates

### wiki/offers/[YYYY-MM-DD-role-level].md
```markdown
---
type: offer
date: YYYY-MM-DD
role: [Job Title]
level: [Level — e.g., L4, Senior, P3]
job_family: [Job Family]
location: [City / Country]
status: pending | approved | declined | rescinded
exception: true | false
last_updated: YYYY-MM-DD
---

# Offer: [Role] — [Level] — [YYYY-MM-DD]

## Offer Economics
| Component | Proposed | Range Min | Range Mid | Range Max | % of Range |
|---|---|---|---|---|---|
| Base Salary | | | | | |
| Target Bonus | | | | | |
| Equity (shares / value) | | | | | |
| Total Comp | | | | | |

## Market Reference
**Data source(s):** [e.g., Radford Q1 2025, Levels.fyi, internal equity analysis]
**Peer comparisons:** [any comparable internal offers or benchmarks used]
**Compa-ratio:** [if applicable]

## Decision
**Outcome:** [approved / declined / pending / exception required]
**Decision by:** [approver]
**Date:** YYYY-MM-DD
**Notes:** [rationale, any caveats, conditions]

## Exception Notes
*Only if exception: true*
[What made this an exception — above range, off-cycle, equity override, etc.]
[Precedent implications: does this set a new bar? What constraints apply?]

## Context
[Any relevant context — competing offer, critical hire, backfill urgency, HM pressure]
```

---

### wiki/benchmarks/[job-family].md
```markdown
---
type: benchmark
job_family: [Job Family Name — e.g., "Software Engineering", "Account Executive"]
last_updated: YYYY-MM-DD
data_sources: []
refresh_due: YYYY-MM-DD
---

# Benchmark: [Job Family Name]

## Compensation Ranges by Level
| Level | Base Min | Base Mid | Base Max | OTE/Bonus | Equity Range | Notes |
|---|---|---|---|---|---|---|
| [L1 / Junior] | | | | | | |
| [L2 / Mid] | | | | | | |
| [L3 / Senior] | | | | | | |
| [L4 / Staff/Principal] | | | | | | |

**Location adjustment:** [note any geo-banding or location multipliers in use]

## Data Sources
- [Source name]: [vintage/date, coverage, weight in our model]

## Internal Equity Notes
[Any known internal equity issues, outliers, or compression concerns at specific levels]

## Outliers
[Employees or offers that fall significantly outside range, and why they were approved]

## Refresh Notes
- **Last refresh:** YYYY-MM-DD
- **Next scheduled refresh:** YYYY-MM-DD
- **Action needed:** [what needs to be done at next refresh]
```

---

### wiki/cycles/[cycle-name].md
```markdown
---
type: cycle
name: [Cycle Name — e.g., "FY25 Annual Review", "Q2 Equity Refresh"]
cycle_type: annual | semi-annual | focal | equity-refresh | ad-hoc
status: planning | active | complete
start_date: YYYY-MM-DD
end_date: YYYY-MM-DD
last_updated: YYYY-MM-DD
---

# Cycle: [Name]

## Overview
[Scope, purpose, and key parameters of this cycle]

## Timeline
| Milestone | Date | Status | Owner |
|---|---|---|---|
| [Planning kickoff] | YYYY-MM-DD | | |
| [Manager calibration] | YYYY-MM-DD | | |
| [Letters delivered] | YYYY-MM-DD | | |
| [Effective date] | YYYY-MM-DD | | |

## Scope
**Eligible population:** [who is in scope — headcount, job families, geos]
**Budget:** [% increase budget, equity pool, or "TBD"]
**Exclusions:** [who is excluded and why]

## Key Decisions
- YYYY-MM-DD: [decision — e.g., "focal budget set at 3.5%"]

## Status & Blockers
[Current status and any blockers or risks to timeline]

## Notes
[Anything else worth tracking — system dependencies, legal reviews, exec approvals needed]
```

---

### wiki/decisions/[YYYY-MM-DD-topic].md
```markdown
---
type: decision
date: YYYY-MM-DD
topic: [short topic name]
job_family: [if applicable]
decision_type: exception | philosophy | equity-grant | range-change | policy
status: final | pending-approval | escalated
---

# Decision: [Topic]

## Context
[What situation or question led to this decision — the business need or case brought forward]

## Decision Made
[What was decided — be specific. Include numbers where relevant.]

## Rationale
[Why this was approved — market data, internal equity, business case, precedent]

## Approvers
[Who approved, at what level, on what date]

## Precedent Implications
[Does this set a precedent? What constraints does it create for future similar requests?]
[Should this go into benchmark or philosophy documentation?]

## Follow-up Required
- [Action item, owner, due date]
```

---

## Pipeline Conventions

### Sources
- Raw ingest files go in `sources/[type]/YYYY-MM-DD-[source]-[topic].md`
- **Never edit source files** — they are immutable records
- Each source file has frontmatter: `source`, `date`, `type`, `processed: true/false`

### Wiki Updates
- The pipeline reads sources, synthesizes, and updates wiki pages
- Changes are appended to `changelog.md` with date + skill that made the change
- Pipeline runs are logged in `log.md`
- HOT.md is regenerated at end of every pipeline run

### Signal Inbox
- Ingest skills write action signals to `wiki/signal-inbox.md`
- Format: `- [YYYY-MM-DD] [source] [job-family/cycle/offer] [signal text] → [recommended action]`
- `vault-daily-sync` reads and clears the inbox each run

### pending-signals.md
- Unclassified ingest signals land here for triage
- Format: `- [YYYY-MM-DD] [source] [signal text] → [suggested action]`
- Cleared during vault-daily-sync

---

## HOT.md — What to Surface

The HOT.md snapshot for Comp & TR should highlight:
- **Offers pending approval:** role, level, proposed comp, exception flag, who needs to approve
- **Cycle milestones coming up this week or next:** what's due, who owns it, what's at risk
- **Recent exceptions that set precedent:** brief summary for awareness
- **Benchmark data needing refresh:** job families where data is stale (>6 months)
- **Pending decisions or escalations:** anything waiting on finance, legal, or exec sign-off

---

## Key Relationships Reference
*Replace with your actual stakeholders*

| Name | Role | Signal Priority |
|---|---|---|
| [Manager Name] | Your direct manager | HIGH |
| [CFO / Finance Leader] | Budget authority | HIGH — comp decisions |
| [HR Leader Name] | CHRO / Head of People | HIGH — philosophy calls |
| [Legal Contact] | Employment law / equity | MEDIUM — equity grants, offer letters |
| [Finance BP Name] | Business unit finance | MEDIUM — headcount budget |
| [HM Name] | Frequent requester | MEDIUM |

---

## Skills Reference

**Use these skills:**
- `vault-boot` — Start of any new chat session
- `vault-daily-sync` — Update wiki from latest signals
- `vault-hot` — Regenerate HOT.md
- `process-meeting-note` — Process a calibration session, offer discussion, or stakeholder meeting
- `daily-brief` — Morning brief of what needs attention
- `ingest-slack` — Pull latest Slack signals (Full Pipeline)
- `ingest-gmail` — Pull latest Gmail signals (Full Pipeline)
- `ingest-granola` — Pull latest meeting notes (Full Pipeline)

**Not applicable to this role:**
- `interview-prep` — Recruiting-specific, not needed
- `ingest-glean` — Less relevant without recruiting workflows; optional

---

## Session Boot Sequence
1. Read `HOT.md` — get current vault state
2. Check for offers pending approval and any cycle milestones due this week
3. Check `pending-signals.md` for any exception requests or urgent decisions
4. If today is a pipeline day and no run yet — offer to run `/vault-orchestrator`
5. Report what needs action today

Do NOT re-read all wiki pages on boot — HOT.md is the summary. Only pull individual wiki pages when asked about a specific offer, benchmark, cycle, or decision.
