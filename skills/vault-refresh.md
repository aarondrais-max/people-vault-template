---
name: vault-refresh
description: Sync current chat after another chat did work -- re-reads HOT.md, pending-signals.md, and recent log entries, reports what changed.
user_invocable: true
trigger: "vault-refresh, refresh vault, sync vault, what changed in vault"
---

*Run this after another chat has done work — pipeline run, wiki edits, etc.*

Read `[VAULT_PATH]/vault.yaml` to confirm vault path.

Then re-read these files to sync current chat context:

1. `[VAULT_PATH]/HOT.md` — regenerated state snapshot
2. `[VAULT_PATH]/pending-signals.md` — may have new signals
3. `[VAULT_PATH]/log.md` — last 5 entries to see what changed

Then respond with a short summary:
- What changed since last read (diff vs what you knew before in this conversation)
- Anything new that needs attention
- Whether the pipeline ran since boot (compare log entry timestamps)

Keep the refresh response brief — 10–15 lines. The user will ask follow-up questions to go deeper.

## Rules
- NEVER use Bash for data processing — use Read/Write/Grep/Glob tools
- Do not read individual wiki pages — HOT.md is the summary
