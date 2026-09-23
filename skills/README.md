# Skills

A skill is a markdown file of step-by-step instructions for one vault operation. Each lives at `skills/<name>/SKILL.md`.

They are plain prose, not code. Any agent that can read a file and follow instructions can run them.

---

## Running a skill

**The portable way**, works in any agent:

```
Read skills/vault-boot/SKILL.md and follow it.
```

**In Claude Code**, `/vault-boot` is a shortcut for exactly that.

**In a plain chat window** with no file access: open the `SKILL.md`, copy everything below the frontmatter, paste it as your first message, then paste or attach the vault files it asks for. Start with `HOT.md`.

---

## What each skill does

These need no external connections. They only read and write files in your vault, so they work anywhere.

| Skill | What it does |
|---|---|
| `vault-boot` | Load vault context at the start of a session, report what is urgent |
| `vault-refresh` | Re-sync context after another session ran the pipeline |
| `vault-hot` | Regenerate `HOT.md` from current wiki state |
| `vault-lint` | Weekly health check: stale pages, ghost entries, orphaned sources, broken links |
| `vault-daily-sync` | Update wiki pages from the signal inbox and new source files |
| `vault-setup` | The setup wizard. Run once, at the start |
| `process-meeting-note` | Turn a meeting note into wiki updates |

These reach outside the vault and need the relevant connection configured.

| Skill | Needs |
|---|---|
| `vault-orchestrator` | Runs the full pipeline, so whatever your enabled ingests need |
| `ingest-slack` | Slack |
| `ingest-gmail` | Email |
| `ingest-glean` | Enterprise search |
| `ingest-granola` | Meeting notes |
| `ingest-gh-pipeline-report` | Google Sheets and an ATS report (recruiter only) |
| `vault-validate` | Enterprise search, to benchmark vault coverage |
| `glean-sweep` | Enterprise search |
| `daily-brief` | Calendar, optional |
| `interview-prep` | ATS, optional (recruiter only) |

If you do not have a source, set `enabled: false` for it in `vault.yaml` and the pipeline skips it.

---

## Order of operations

`vault-orchestrator` handles all of this. Only relevant if you are running steps by hand:

1. Ingest skills, all independent, can run at the same time
2. `vault-daily-sync`, needs the signal inbox populated by ingest
3. `vault-hot`, needs pages updated by the sync
4. `daily-brief`, needs `HOT.md` current

---

## Writing or editing a skill

Every `SKILL.md` starts with exactly two frontmatter fields:

```yaml
---
name: skill-name
description: One line on what it does and when to use it.
---
```

`name` must match the directory name. Do not add other fields: they are non-standard, most agents ignore them, and some linters reject them. If the description contains a colon, wrap the value in double quotes.

Common edits: the `HOT.md` layout in `vault-hot`, the brief format in `daily-brief`, lookback windows in the ingest skills.

Two rules worth keeping when you edit:

- **Refer to skills by path**, not by slash command, so they stay portable.
- **Name capabilities, not vendor tools.** Write "read the team's Slack channels", not a specific tool identifier.

Most skills have a `rules:` section at the end. Read it before changing behaviour, it marks what is load-bearing.

After editing, run `python3 scripts/check_template.py` from the vault root.
