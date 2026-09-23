# Portability

This vault is built so that the AI agent maintaining it is a replaceable part. If you switch from Claude to something else, you keep everything.

That is a deliberate design constraint, not a happy accident. This page explains what makes it true and what to do if you switch.

---

## What you actually own

Everything of value in this vault is in formats that predate AI agents and will outlast them:

| Layer | Format | Locked in? |
|---|---|---|
| Your knowledge | Markdown files with YAML frontmatter and `[[wikilinks]]` | No. Open in Obsidian, Notepad, VS Code, or `grep`. |
| Your raw records | Markdown in `sources/`, one file per ingest | No. Immutable, plain text, dated. |
| Your config | One `vault.yaml` | No. Plain YAML, no vendor keys. |
| Your automations | Markdown prose in `skills/<name>/SKILL.md` | No. Instructions in English, not code against an API. |
| Your instructions | `AGENTS.md` | No. Open convention, read by 30+ agents. |

There is no database, no proprietary file format, no export step, and no account that holds your data hostage. If every AI vendor disappeared tomorrow you would still have a well organised, searchable, human-readable knowledge base.

---

## The four design rules that keep it that way

Follow these when you change anything, or portability quietly erodes.

**1. `AGENTS.md` is the only instruction file.**
[AGENTS.md](https://agents.md) is an open convention stewarded by the Agentic AI Foundation under the Linux Foundation, the same body that stewards MCP. It is read by Codex CLI, Cursor, Gemini CLI, Jules, Aider, Zed, Copilot, Windsurf, Devin and others.

Tool-specific files are **pointers, never copies**. This repo's `CLAUDE.md` is three lines that say "read AGENTS.md". If you add `.cursorrules` or `.github/copilot-instructions.md`, make them pointers too. The moment you copy content into a second file, the two drift and you have vendor-specific behaviour.

**2. Skills are addressed by path, not by slash command.**
`/vault-boot` is a Claude Code convenience. The portable instruction is always *"read and follow `skills/vault-boot/SKILL.md`"*. Every skill works in any agent that can read a file, and in a plain chat window if you paste the contents.

The `skills/<name>/SKILL.md` directory layout is the emerging standard, so skills are also portable between agents as units.

**3. Name capabilities, not vendor tools.**
Write *"read the team's Slack channels"*, not a hardcoded tool ID. MCP itself is cross-vendor and fine to depend on; specific tool identifiers are not. This is what lets the same skill run against a different agent's Slack connector without an edit.

**4. Anything mechanical goes in a script.**
Counting, date maths, parsing, moving lines between files: put these in `scripts/`, called in one line. Scripts run identically everywhere. Prompt behaviour does not, and it is the first thing to change when you swap models. It is also far cheaper.

---

## Switching agents

The vault content needs no migration at all. The work is entirely in reconnecting tools.

1. **Point the new agent at the folder.** If it reads `AGENTS.md`, you are done. If it uses a different convention, add a pointer file for it, three lines, pointing at `AGENTS.md`.

2. **Re-register your connections.** Slack, email, calendar, meeting notes, ATS. This is the real work, and how long it takes depends entirely on which connectors the new agent supports. Check this *before* you commit to a switch.

3. **Re-test the skills that call tools.** The ingest skills (`skills/ingest-*/SKILL.md`) are the ones that touch external systems. Skills that only read and write local files (`vault-boot`, `vault-hot`, `vault-lint`, `vault-daily-sync`) will just work.

4. **Re-check scheduling.** However you automated the morning run, the new agent will do it differently. This is config, not content.

5. **Run `python3 scripts/check_template.py`** to confirm nothing broke structurally.

---

## The honest caveats

Portability of the *data* is absolute. Portability of the *behaviour* is not, and it would be misleading to claim otherwise.

- **Connector coverage is the real constraint.** Not every agent has a Slack or Greenhouse connector. If the new agent cannot read a source, that ingest stops working no matter how portable the markdown is. Check coverage first.
- **Instruction-following quality varies.** These skills are long prose instructions. A weaker model will follow them less reliably, especially the multi-step ones like `vault-orchestrator`. Expect to tighten prompts after a switch.
- **Scheduled, unattended runs differ most.** Running a prompt headless on a timer is where agents diverge most sharply in permissions, cost, and reliability.
- **Cost changes.** The pipeline's cost is dominated by how much text the agent reads each run. A different model changes that number, in either direction.

None of these put your knowledge at risk. They affect how much re-tuning a switch costs, which is worth knowing up front rather than discovering mid-migration.
