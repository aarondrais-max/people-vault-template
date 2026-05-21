# People Team Knowledge Vault — Claude Schema (People Ops / General)

This is a local People team knowledge vault maintained by Claude. When operating in this project, follow all conventions below exactly.

## Vault Owner Context
- **Name:** [YOUR_NAME]
- **Role:** [YOUR_ROLE] (e.g., People Ops Manager, L&D Lead, Facilities & Workplace, HR Coordinator)
- **Org:** [YOUR_ORG] (e.g., People & Culture, Acme Corp)
- **Timezone:** [YOUR_TIMEZONE] (e.g., America/New_York, Europe/London, Asia/Tokyo)
- **Slack ID:** [YOUR_SLACK_ID]
- **Focus Areas:** [what you own — e.g., "onboarding + HRIS", "office + vendor management", "manager training programs"]

## Vault Location
`[VAULT_PATH]` (e.g., `~/Documents/my-people-vault`) — all paths are relative to this root.

---

## What This Vault Tracks

This vault is a flexible knowledge base for People team members whose work is primarily project- and process-driven. It captures:
- Projects and programs you're running or contributing to
- Key stakeholder and vendor relationships
- Decisions you've made (and why)
- Documented processes, workflows, and runbooks
- Active conversations and issues to track over time

The vault is primarily a **meeting note processor and decision log**. You put context in, Claude helps you keep it organised and surfaced.

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
│   ├── projects/         ← initiatives, programs, workstreams
│   ├── people/           ← key stakeholders, vendors, partners
│   ├── decisions/        ← key decisions and their rationale
│   ├── processes/        ← documented workflows, runbooks, SOPs
│   └── threads/          ← active conversations and issues to track
│
├── queries/              ← on-demand query results
├── outputs/              ← daily briefs archive
└── skills/               ← pipeline skill definitions
```

---

## Wiki Page Templates

Pages are intentionally flexible. Every page has the same core structure — adapt the sections as needed for your specific context.

### wiki/projects/[project-name].md
```markdown
---
type: project
name: [Project Name]
status: planning | active | complete | paused | blocked
owner: [YOUR_NAME]
stakeholders: []
started: YYYY-MM-DD
target_completion: YYYY-MM-DD
last_updated: YYYY-MM-DD
---

# [Project Name]

## Overview
[What this project is, why it exists, and what success looks like]

## Status
**Current status:** [planning / active / complete / paused / blocked]
[1-2 sentences on where things stand right now]

## Key Contacts
| Name | Role in Project | Contact |
|---|---|---|
| | | |

## Decisions Log
- YYYY-MM-DD: [decision made, by whom, rationale]

## Next Steps
- [YYYY-MM-DD due]: [action item, owner]

## Notes & History
- YYYY-MM-DD: [update, milestone, or context]
```

---

### wiki/people/[firstname-lastname].md
```markdown
---
type: person
name: [Full Name]
relationship: stakeholder | vendor | partner | manager | executive
org: [their company or department]
slack_handle: @handle
last_interaction: YYYY-MM-DD
---

# [Full Name]

## Role & Context
[Title, org, why they matter to your work]

## Interaction History
*Most recent first*
- YYYY-MM-DD: [interaction summary — meeting, email, decision made, request]

## Key Notes
[Communication style, what they care about, useful context for working with them]

## Active Threads
[Any open issues, requests, or follow-ups with this person]
```

---

### wiki/decisions/[YYYY-MM-DD-topic].md
```markdown
---
type: decision
date: YYYY-MM-DD
topic: [short topic name]
project: [related project if applicable]
status: final | pending | escalated
---

# Decision: [Topic]

## Context
[What situation or question led to this decision]

## Decision Made
[What was decided — be specific]

## Rationale
[Why this was the right call — factors considered, alternatives rejected]

## People Involved
[Who was part of making or approving this decision]

## Follow-up Required
- [Action item, owner, due date]

## Notes
[Anything else relevant — does this set a precedent? Related policies?]
```

---

### wiki/processes/[process-name].md
```markdown
---
type: process
name: [Process Name]
owner: [YOUR_NAME]
last_updated: YYYY-MM-DD
status: current | draft | deprecated
---

# Process: [Process Name]

## Purpose
[What this process is for and when to use it]

## Steps
1. [Step one]
2. [Step two]
3. [Step three]

## Key Contacts
[Who to involve or notify at each step]

## Tools & Systems
[What systems, forms, or templates are used]

## Notes & Exceptions
[Any exceptions, edge cases, or things people commonly get wrong]

## Changelog
- YYYY-MM-DD: [what changed]
```

---

### wiki/threads/[thread-name].md
```markdown
---
type: thread
name: [Short descriptive name]
status: active | resolved | paused
started: YYYY-MM-DD
last_updated: YYYY-MM-DD
people_involved: []
---

# Thread: [Name]

## Summary
[1-2 sentences: what is this thread about and where does it stand]

## Timeline
- YYYY-MM-DD: [what happened]
- YYYY-MM-DD: [what happened]

## Next Step
[What needs to happen next and by when]

## Notes
[Anything else relevant]
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
- Format: `- [YYYY-MM-DD] [source] [project/person/thread] [signal text] → [recommended action]`
- `vault-daily-sync` reads and clears the inbox each run

### pending-signals.md
- Unclassified ingest signals land here for triage
- Format: `- [YYYY-MM-DD] [source] [signal text] → [suggested action]`
- Cleared during vault-daily-sync

---

## HOT.md — What to Surface

The HOT.md snapshot should highlight:
- **Active projects with upcoming milestones:** what's due this week or at risk
- **Open threads needing action:** conversations or issues with no recent progress
- **Pending decisions:** things waiting on approval or input from someone else
- **Recent signals from stakeholders:** anything flagged from Slack, email, or meetings
- **Follow-up commitments:** what you promised someone and when it's due

---

## Key Relationships Reference
*Replace with your actual stakeholders*

| Name | Role | Signal Priority |
|---|---|---|
| [Manager Name] | Your direct manager | HIGH |
| [HR Leader Name] | Head of People / CHRO | HIGH |
| [Stakeholder Name] | Key business partner | MEDIUM |
| [Vendor Name] | Key vendor or partner | MEDIUM |

---

## Skills Reference

**Use these skills:**
- `vault-boot` — Start of any new chat session
- `vault-daily-sync` — Update wiki from latest signals
- `vault-hot` — Regenerate HOT.md
- `process-meeting-note` — Process a meeting note into wiki updates
- `daily-brief` — Morning brief of what needs attention
- `ingest-slack` — Pull latest Slack signals (Full Pipeline)
- `ingest-gmail` — Pull latest Gmail signals (Full Pipeline)
- `ingest-granola` — Pull latest meeting notes (Full Pipeline)

**Not applicable to this role:**
- `interview-prep` — Recruiting-specific, not needed
- `ingest-glean` — Less relevant without ATS/recruiting workflows; skip unless you use Glean heavily

---

## Session Boot Sequence
1. Read `HOT.md` — get current vault state
2. Check for active project milestones or threads that need attention today
3. Check `pending-signals.md` for any urgent follow-ups
4. If today is a pipeline day and no run yet — offer to run `/vault-orchestrator`
5. Report what needs action today

Do NOT re-read all wiki pages on boot — HOT.md is the summary. Only pull individual wiki pages when asked about a specific project, person, decision, or process.
