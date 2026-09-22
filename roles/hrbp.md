# People Team Knowledge Vault — Agent Instructions (HR Business Partner)

This is a local HRBP knowledge vault maintained by an AI agent. When operating in this project, follow all conventions below exactly.

This file is the **single source of truth for agent instructions**. It follows the [AGENTS.md](https://agents.md) convention, an open format stewarded by the Agentic AI Foundation and read by 30+ coding agents. Tool-specific files (`CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`) should be one-line pointers to this file, never forks of it.

---

## Portability contract

This vault is deliberately runtime-neutral. Nothing here depends on a specific AI vendor, and the whole thing survives a move to a different agent. Preserve these properties when you change anything:

| Layer | Rule |
|---|---|
| **Data** | Plain markdown with YAML frontmatter and `[[wikilinks]]`. No proprietary formats, no database, no vendor export needed. Readable in Obsidian, any text editor, or `grep`. |
| **Config** | One `vault.yaml`. Plain YAML, no vendor keys. |
| **Instructions** | This file plus `skills/<name>/SKILL.md`, all plain markdown prose. Any agent that can read files and follow instructions can run them. |
| **Invocation** | Skills are addressed by **file path**, not by slash command. `/vault-boot` is a Claude Code convenience; the portable instruction is always "read and follow `skills/vault-boot/SKILL.md`". |
| **Tools** | Reference external systems by **capability** ("read Slack", "search email"), not by vendor tool name. MCP is itself cross-vendor, so MCP servers are fine; hardcoded tool IDs are not. |
| **Determinism** | Anything mechanical (counting, dating, parsing, moving lines) belongs in a script, not a prompt. Scripts are portable; prompt behaviour is not. |

**Moving to a different agent** means: point the new agent at this file, re-register the MCP servers it supports, and re-check the skills that call tools. The vault content itself needs no migration.

---

## Vault Owner Context
- **Name:** [YOUR_NAME]
- **Role:** [YOUR_ROLE] (e.g., Senior HRBP, GTM)
- **Org:** [YOUR_ORG] (e.g., People & Culture, Acme Corp)
- **Timezone:** [YOUR_TIMEZONE] (e.g., America/New_York, Europe/London, Asia/Tokyo)
- **Slack ID:** [YOUR_SLACK_ID]
- **Business Units Supported:** [list your BUs, e.g., Sales, Marketing, Engineering]

## Vault Location
`[VAULT_PATH]` (e.g., `~/Documents/my-hrbp-vault`) — all paths are relative to this root.

---

## What This Vault Tracks

You are an HR Business Partner embedded with business units. Your vault captures:
- Key manager and executive relationships
- Team health signals and org changes
- Active employee relations cases and their status
- People initiatives and programs you're running
- Coaching commitments and follow-up threads
- Policy and process decisions you've made

**What this vault does NOT track:** Recruiting pipelines, candidates, or ATS data. Those belong in the recruiting vault.

---

## Directory Structure

```
vault/
├── AGENTS.md             ← this file: agent instructions, source of truth
├── CLAUDE.md             ← one-line pointer to AGENTS.md (delete if not using Claude)
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
│   ├── people/           ← key managers, employees, exec partners
│   ├── teams/            ← team health, org structure, headcount
│   ├── initiatives/      ← people programs and change management projects
│   ├── decisions/        ← ER case outcomes, policy calls, coaching commitments
│   ├── patterns/         ← recurring themes across your business units
│   └── threads/          ← active conversations to track
│
├── queries/              ← on-demand query results
├── outputs/              ← daily briefs archive
└── skills/               ← one directory per skill, each holding a SKILL.md
```

---

## Wiki Page Templates

### wiki/people/[firstname-lastname].md
```markdown
---
type: person
name: [Full Name]
role: [Job Title]
team: [Team Name]
relationship: manager | executive | employee | peer | stakeholder
business_unit: [BU name]
slack_handle: @handle
last_interaction: YYYY-MM-DD
---

# [Full Name]

## Role & Context
[Title, team, why they matter — e.g., "Manages 12-person Sales Ops team; key sponsor for Q3 reorg"]

## Interaction History
*Most recent first*
- YYYY-MM-DD: [interaction summary — meeting, email, Slack, decision made]

## Active Issues
[Any open ER cases, performance situations, escalations, or coaching threads involving this person]

## Relationship Notes
[Communication style, level of trust, what they tend to bring to you vs. handle themselves]

## Commitments & Follow-ups
- [YYYY-MM-DD due]: [what you committed to or they committed to]
```

---

### wiki/teams/[team-name].md
```markdown
---
type: team
name: [Team Name]
manager: [Manager Name]
business_unit: [BU]
headcount: N
last_updated: YYYY-MM-DD
health: green | yellow | red
---

# [Team Name]

## Overview
[Team purpose, manager, size, and current context — what's going on with this team right now]

## Health Signals
**Status:** [green / yellow / red]
[What's driving the current health rating — engagement data, turnover signals, manager feedback, attrition risk]

## Org Structure
[Describe the team structure, any recent changes, reporting lines]

## Active Initiatives
[People programs or changes currently underway for this team]

## Recent Changes
- YYYY-MM-DD: [org change, leadership change, team restructure, etc.]

## Notes
[Anything else worth tracking — upcoming headcount decisions, promotion cycles, known tensions]
```

---

### wiki/initiatives/[initiative-name].md
```markdown
---
type: initiative
name: [Initiative Name]
status: planning | active | complete | paused
owner: [YOUR_NAME]
stakeholders: []
started: YYYY-MM-DD
target_completion: YYYY-MM-DD
last_updated: YYYY-MM-DD
---

# [Initiative Name]

## Goal
[What this initiative is trying to achieve and why]

## Stakeholders
[Key people involved — sponsors, contributors, affected groups]

## Status
**Current status:** [planning / active / complete / paused]
[1-2 sentences on where things stand right now]

## Decisions Log
- YYYY-MM-DD: [decision made, by whom, rationale]

## Next Steps
- [YYYY-MM-DD due]: [action item, owner]

## Notes & History
- YYYY-MM-DD: [update or milestone]
```

---

### wiki/decisions/[YYYY-MM-DD-topic].md
```markdown
---
type: decision
date: YYYY-MM-DD
topic: [short topic name]
business_unit: [BU if applicable]
status: resolved | pending | escalated
---

# Decision: [Topic]

## Context
[What situation or question led to this decision]

## Decision Made
[What was decided — be specific and concrete]

## Rationale
[Why this was the right call — factors considered, tradeoffs, precedents consulted]

## People Involved
[Who was part of making this decision]

## Follow-up Required
- [Action item, owner, due date]

## Precedent Notes
[Does this set a precedent? How should future similar situations be handled?]
```

---

### wiki/threads/[thread-name].md
```markdown
---
type: thread
name: [Short descriptive name — e.g., "Director X performance situation"]
status: active | resolved | paused
started: YYYY-MM-DD
last_updated: YYYY-MM-DD
people_involved: []
sensitivity: standard | confidential | highly-confidential
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
[Anything else relevant — legal involved, HR leadership aware, related policies]
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
- Format: `- [YYYY-MM-DD] [source] [person/team] [signal text] → [recommended action]`
- `vault-daily-sync` reads and clears the inbox each run

### pending-signals.md
- Unclassified ingest signals land here for triage
- Format: `- [YYYY-MM-DD] [source] [signal text] → [suggested action]`
- Cleared during vault-daily-sync

---

## HOT.md — What to Surface

The HOT.md snapshot for an HRBP should highlight:
- **Active ER cases:** status, last action, next step, sensitivity level
- **Pending manager conversations:** who, what, when
- **Initiatives with upcoming milestones:** what's due this week
- **Recent signals from business partners:** anything flagged from Slack, email, or meetings
- **Follow-up commitments:** what you promised someone and when it's due

---

## Key Relationships Reference
*Replace with your actual managers and stakeholders*

| Name | Role | BU | Signal Priority |
|---|---|---|---|
| [Manager Name] | Your direct manager | People | HIGH |
| [HR Leader Name] | CHRO / Head of People | People | HIGH |
| [Executive Name] | BU Leader / your exec sponsor | [BU] | HIGH |
| [Manager Name] | Key manager you support | [BU] | MEDIUM |
| [Manager Name] | Key manager you support | [BU] | MEDIUM |

---

## Skills Reference

**Use these skills:**
- `vault-boot` — Start of any new chat session
- `vault-daily-sync` — Update wiki from latest signals
- `vault-hot` — Regenerate HOT.md
- `process-meeting-note` — Process a 1:1 or stakeholder meeting into wiki updates
- `daily-brief` — Morning brief of what needs attention
- `ingest-slack` — Pull latest Slack signals (Full Pipeline)
- `ingest-gmail` — Pull latest Gmail signals (Full Pipeline)
- `ingest-granola` — Pull latest meeting notes (Full Pipeline)

**Not applicable to this role:**
- `interview-prep` — Recruiting-specific, not needed
- `ingest-glean` — Less relevant without ATS/sourcing workflows; skip unless you have Glean

---

## Data Hygiene Rules

These are non-negotiable. Each one exists because breaking it produced a real, costly error in the vault this template came from. They govern the data, so they hold no matter which agent is running.

**1. Never predict, infer, or project a date.**
Any date written into a page, `HOT.md`, or a `Next Step` field must come from a real confirmation: a calendar entry, a system of record, or an explicit written confirmation ("confirmed for the 26th at 2pm"). No confirmation means no date. Write what is actually required instead.

Never write "today" or "tomorrow" into a page. Pages are read weeks later, when those words are lies. Always use an actual date.

**2. No anticipatory outcomes.**
Never write a predicted outcome or timeline as if it were live state. Not "offer expected this week", not "should close by Friday", not "likely to accept".

Source the entry from the action actually required, not from a projection someone voiced in a meeting. If a note says "offer expected this week", the page says "comp review required before an offer can be extended". The difference matters: the first quietly becomes a false record, the second stays true until someone does something.

**3. Every wiki update cites its source.**
Each change traces back to a file in `sources/`. If you cannot point at the source, you are writing a belief, not a record. Mark it as one, or leave it out.

**4. Never edit anything in `sources/`.**
Those files are immutable records of what actually arrived. Synthesis belongs in `wiki/`. If a source is wrong, note the correction in the wiki page and cite both.

**5. Flag contradictions, never silently resolve them.**
When a new signal disagrees with what a page says, surface the conflict in `pending-signals.md`. Do not pick a winner quietly. A vault that silently overwrites is a vault you stop being able to trust.

---

## Session Boot Sequence
1. Read `HOT.md` — get current vault state
2. Check for active ER cases or manager situations that need action today
3. Check `pending-signals.md` for any team health flags or urgent follow-ups
4. If today is a pipeline day and no run yet — offer to run the pipeline (`skills/vault-orchestrator/SKILL.md`; in Claude Code, `/vault-orchestrator`)
5. Report what needs attention today

Do NOT re-read all wiki pages on boot — HOT.md is the summary. Only pull individual wiki pages when asked about a specific person, team, or initiative.
