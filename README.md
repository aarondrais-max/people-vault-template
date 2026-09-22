# People Team Knowledge Vault

A local markdown knowledge base that an AI agent reads, writes, and keeps current for you. Built for People and TA professionals who want a second brain for their work that they actually own.

**New here? Start with [SETUP.md](SETUP.md), or open `walkthrough.html` in a browser for the visual version.**

---

## What it is

A structured set of markdown files on your computer. It opens in Obsidian as a browsable, linked knowledge base, and it connects to the tools you already use so it stays current without you typing things twice.

Think of it as a local database of what you know: the people you work with, the work in flight, the decisions you have made and why. The agent keeps it up to date. You ask it questions in plain English.

It is a complement to your systems of record, not a replacement. Your ATS or HRIS stays authoritative for stages, compliance, and reporting. The vault captures what those systems never hold: what a manager actually meant, the concern someone raised off the record, the context behind a decision six months ago.

## What it does

Each pipeline run:

1. **Ingests** from the sources you connect (Slack, email, meeting notes, your ATS), capturing signals you would otherwise lose.
2. **Updates** structured wiki pages, flagging what changed and what contradicts what.
3. **Regenerates `HOT.md`**, a single snapshot of what needs attention.
4. **Writes a brief**, prioritised and short.

Then you start a session, load context in a few seconds, and ask it things.

## Who it is for

The setup wizard configures the vault for your role:

| Role | Tracks |
|---|---|
| **Recruiter** | Reqs, candidates, pipeline, hiring managers |
| **HR Business Partner** | Manager relationships, team health, ER cases, people initiatives |
| **Comp & Total Rewards** | Comp cycles, benchmarks, offers, pay decisions |
| **Generic** | Meetings, decisions, projects, commitments (People Ops, L&D, Facilities) |

---

## You are not locked in

The agent maintaining this vault is a replaceable part, on purpose.

Everything is plain markdown, plain YAML, and instructions written in English. Instructions live in [`AGENTS.md`](AGENTS.md), the open convention stewarded by the Agentic AI Foundation and read by 30+ agents including Codex CLI, Cursor, Gemini CLI and Aider. `CLAUDE.md` is a three-line pointer to it, not a copy, so the two cannot drift.

Switching agents means reconnecting your tools. Your knowledge transfers untouched. See [PORTABILITY.md](PORTABILITY.md) for the full picture, including the honest caveats.

---

## Structure

```
vault/
├── AGENTS.md            ← agent instructions, single source of truth
├── CLAUDE.md            ← 3-line pointer to AGENTS.md
├── vault.yaml           ← your configuration
├── HOT.md               ← auto-generated state snapshot, start here each session
├── pending-signals.md   ← unresolved signals needing triage
├── index.md             ← cross-reference of all wiki pages
├── log.md               ← pipeline run history
│
├── wiki/                ← your maintained pages
│   ├── reqs/ candidates/ people/      (recruiter)
│   ├── patterns/ decisions/ concepts/
│   └── projects/ threads/
│
├── sources/             ← immutable raw ingest records, never edit
│   └── slack/ gmail/ glean/ meetings/ documents/
│
├── roles/               ← role variants of AGENTS.md, removed after setup
├── skills/              ← one directory per skill, each with a SKILL.md
├── scripts/             ← deterministic checks and helpers
├── outputs/             ← brief archive
└── queries/             ← on-demand query results
```

## Skills

Each skill is a markdown instruction file at `skills/<name>/SKILL.md`. Run one by telling your agent to read and follow it. In Claude Code, `/vault-boot` is a shortcut for the same thing.

See [skills/README.md](skills/README.md) for what each one does and which need external connections.

## Example pages

`wiki/` ships with files prefixed `EXAMPLE-` showing the expected format. Read them, then delete them.

## Maintaining the template

If you edit the template itself, run the health check before sharing it:

```bash
python3 scripts/check_template.py
```

It verifies that referenced paths exist, skill frontmatter is standard, and no stale layout references have crept back in.

---

## Feedback

This template came out of a working vault that runs daily. If something does not fit how you work, the skill files are plain markdown. Edit them.
