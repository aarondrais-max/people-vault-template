# Skills — How to Use

Skills are instruction files that tell Claude exactly what to do when you invoke them. They contain step-by-step logic for vault operations: reading files, updating wiki pages, generating outputs.

---

## How to invoke skills

### In Claude Code (tech setup)
Type the skill name as a slash command:
```
/vault-boot
/vault-orchestrator
/daily-brief
```

Claude Code reads the skill file from `skills/[skill-name].md` and executes the steps.

### In Claude.ai chat (standard setup)
1. Open the skill file in Obsidian or a text editor
2. Copy everything below the `---` frontmatter block (i.e., the body of the file)
3. Paste it as your first message in a new Claude.ai conversation
4. Attach or paste the relevant vault files Claude will need (HOT.md, specific wiki pages, etc.)
5. Claude will follow the skill instructions

For skills that need to read many files, it works best to paste the HOT.md contents into the conversation and reference specific wiki pages by name — Claude will ask for them if needed.

---

## Skills that work in both chat and Claude Code

| Skill | What it does | Requires external tools? |
|---|---|---|
| `vault-boot` | Load vault context, report what's urgent | No — reads local files only |
| `vault-refresh` | Re-sync context after another session ran the pipeline | No — reads local files only |
| `vault-hot` | Regenerate HOT.md from current wiki state | No — reads local files only |
| `vault-lint` | Weekly health check — flag stale pages, ghost candidates, orphaned sources | No — reads local files only |
| `daily-brief` | Generate morning brief from HOT.md and calendar | Calendar MCP (optional) |
| `interview-prep` | Prep notes for a named candidate + req | Greenhouse MCP (optional) |
| `process-meeting-note` | Process a meeting note file into wiki updates | No — reads local files only |

---

## Skills that require Claude Code

These skills call external APIs (Slack, Gmail, Glean, Granola) and need MCP integrations configured:

| Skill | What it does | Requires |
|---|---|---|
| `vault-orchestrator` | Run the full pipeline — ingest + wiki update + brief | All enabled MCP integrations |
| `vault-daily-sync` | Wiki update only — reads signal inbox, updates pages | No external calls (reads from sources/) |
| `vault-validate` | Validate vault coverage against Glean sweep benchmark | Glean MCP |
| `ingest-slack` | Ingest Slack channels and DMs into sources/ | Slack MCP |
| `ingest-gmail` | Ingest Gmail into sources/ | Gmail MCP |
| `ingest-glean` | Ingest Glean cross-app activity into sources/ | Glean MCP |
| `ingest-granola` | Ingest Granola meeting notes into sources/ | Granola MCP |

---

## Skill dependency order

When running manually (not via orchestrator), run in this order:

1. Ingest skills (parallel — can run at same time)
2. `vault-daily-sync` (needs signal-inbox.md populated by ingest)
3. `vault-hot` (needs wiki pages updated by vault-daily-sync)
4. `daily-brief` (needs HOT.md current)

`vault-orchestrator` handles all of this automatically.

---

## Customizing skills

Skills are plain markdown. If the default behavior doesn't fit your workflow, edit the skill file directly. Common customizations:

- Change the HOT.md output format in `vault-hot.md`
- Adjust the brief format in `daily-brief.md`
- Add or remove pipeline stages in `vault-daily-sync.md`
- Change lookback windows in ingest skills

Every skill file has a `rules:` section at the bottom — read it before customizing to understand what's non-negotiable.
