---
name: vault-boot
description: Load vault context at the start of a new chat -- reads CLAUDE.md, HOT.md, and pending-signals.md, reports what's urgent and whether the pipeline has run today.
user_invocable: true
trigger: "vault-boot, boot vault, load vault, start vault, vault context"
---

*Run this at the start of any new chat to load vault context.*

Read vault.yaml first to get `vault_path`. Then read these files in order:

1. `[VAULT_PATH]/CLAUDE.md` — schema, conventions, key relationships, file paths
2. `[VAULT_PATH]/HOT.md` — current pipeline state, active reqs, urgent items
3. `[VAULT_PATH]/pending-signals.md` — unresolved signals needing triage
4. `[VAULT_PATH]/log.md` — last entry only, to check when the pipeline last ran

Then respond with:
- What's urgent today (from HOT.md — items in the "Requires Action Today" section)
- Any pending signals that need immediate attention
- Whether the pipeline has run today (compare log.md last entry date vs today's date)
- If no pipeline run today, offer to run `/vault-orchestrator`

Keep the boot response brief — 10–20 lines maximum. The user will ask follow-up questions to go deeper.

## Rules
- NEVER use Bash for data processing — use Read/Write/Grep/Glob tools
- Do not read individual wiki pages on boot — HOT.md is the summary
- If HOT.md says "Not yet generated", say so and offer to run `/vault-orchestrator` immediately
