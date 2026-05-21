# People Team Knowledge Vault

A local markdown knowledge base maintained by Claude — built for TA and People team professionals who want an AI-powered second brain for their recruiting work.

---

## What it is

The People Team Knowledge Vault is a structured set of markdown files that Claude reads, writes, and maintains on your behalf. It lives on your computer (or in a git repo you control), works in Obsidian as a browsable knowledge base, and connects to your existing tools — Slack, Gmail, Glean, meeting notes — to stay current without manual entry.

Think of it as a local database of everything you know: open reqs, active candidates, hiring manager relationships, recruiting patterns. Claude keeps it up to date. You query it in plain English.

---

## What it does

Each pipeline run:

1. **Ingests** from Slack, Gmail, Glean, and meeting notes (Granola) — capturing signals you'd otherwise lose
2. **Updates** structured wiki pages — reqs, candidates, hiring managers — with new information, flagging changes and contradictions
3. **Generates a state snapshot** (HOT.md) that tells you what needs attention today
4. **Produces a morning brief** — prioritized, opinionated, under 60 lines

You start each Claude session by running `/vault-boot`. Claude reads the snapshot and you're in context within seconds.

---

## Two setup paths

### Standard (no code required)
Best for: TA professionals who use Claude.ai in a browser and Obsidian for notes.

- Download or clone this repo
- Open the folder in Obsidian
- Fill in your details in CLAUDE.md and vault.yaml
- Use Claude.ai chat — paste skill files as instructions
- Update wiki pages manually with Claude's help

See **[SETUP-STANDARD.md](SETUP-STANDARD.md)** for step-by-step instructions.

### Tech (Claude Code + automated pipeline)
Best for: users who have Claude Code CLI installed and want a fully automated pipeline.

- Requires: Claude Code CLI, MCP integrations (Slack, Gmail, Glean, Granola, Greenhouse)
- Automated ingest + wiki update on a schedule
- `claude` → `/vault-orchestrator` runs the full pipeline
- Cron-schedulable for hands-free daily runs

See **[SETUP-TECH.md](SETUP-TECH.md)** for step-by-step instructions.

---

## Prerequisites

### Standard path
- [Obsidian](https://obsidian.md) (free) — for browsing and editing the vault
- Claude.ai account (any plan)

### Tech path
- Claude Code CLI (`npm install -g @anthropic-ai/claude-code` or see docs)
- MCP integrations configured for the tools you use (Slack, Gmail, Glean, Granola)
- Git (optional but recommended for snapshots)
- Greenhouse access (optional — for interview prep skill)

---

## Vault structure

```
vault/
├── CLAUDE.md          ← Schema file Claude reads every session
├── vault.yaml         ← Your configuration (channels, contacts, schedule)
├── HOT.md             ← Auto-generated state snapshot — start every session here
├── pending-signals.md ← Unresolved signals needing triage
├── scan-intelligence.md ← Learned recruiting patterns
├── index.md           ← Cross-reference of all wiki pages
├── log.md             ← Pipeline run history
│
├── wiki/              ← Maintained structured pages
│   ├── reqs/          ← One page per requisition
│   ├── candidates/    ← Active (Tier 1) or archived stub (Tier 2)
│   ├── people/        ← Hiring managers, stakeholders, key contacts
│   ├── patterns/      ← Scan intelligence patterns
│   ├── decisions/     ← Key decisions with rationale
│   ├── concepts/      ← Market intel, comp benchmarks, process notes
│   ├── projects/      ← Cross-functional TA projects
│   └── threads/       ← Active tracked conversations
│
├── sources/           ← Immutable raw ingest records (never edit these)
│   ├── slack/
│   ├── gmail/
│   ├── glean/
│   ├── meetings/
│   └── documents/
│
├── outputs/           ← Daily briefs archive
├── queries/           ← On-demand query results
└── skills/            ← Skill instruction files for Claude
```

---

## Designed to work alongside your existing tools

The vault is a complement, not a replacement. It captures soft intel that your ATS (Greenhouse, Lever, etc.) doesn't: what an interviewer said off-scorecard, a candidate's competing offer timeline, a hiring manager's unstated preferences. Your ATS remains the system of record for pipeline stages and compliance data.

The vault integrates with:
- **Greenhouse** — for interview prep (pulls resumes, application data)
- **Slack** — for team signals and hiring manager communications
- **Gmail** — for candidate and stakeholder email
- **Glean** — for cross-app activity and document signals
- **Granola** — for meeting notes from screens, debriefs, and intakes

---

## Example files

The `wiki/` directories contain example files prefixed with `EXAMPLE-`. These show the expected format and structure. Delete them once you've created your own pages.

---

## Skills

The `skills/` directory contains instruction files for each vault operation. See [skills/README.md](skills/README.md) for a full description of each skill and how to use them.

---

## Questions and feedback

This template was built from a working recruiting vault. If something doesn't fit your workflow, the skill files in `skills/` are plain markdown — edit them to match how you actually work.
