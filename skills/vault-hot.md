---
name: vault-hot
description: Regenerate HOT.md -- the vault state snapshot. Reads active reqs, candidates, scan intelligence, and recent pipeline log. Can be run standalone or as part of vault-daily-sync.
user_invocable: true
trigger: "vault-hot, regenerate hot, refresh hot, vault state"
---

You regenerate `[VAULT_PATH]/HOT.md` — the vault state snapshot every new Claude session reads first.

Read `[VAULT_PATH]/vault.yaml` to get `vault_path` and user identity.
Read `[VAULT_PATH]/CLAUDE.md` for conventions.

## What to Read

1. `[VAULT_PATH]/wiki/reqs/*.md` — all reqs where `status: open` — deadline, pipeline, blockers
2. `[VAULT_PATH]/wiki/candidates/*.md` — all where `status: active` only (skip archived entirely)
3. `[VAULT_PATH]/scan-intelligence.md` — which patterns are currently active
4. `[VAULT_PATH]/log.md` — last 3–5 pipeline entries
5. `[VAULT_PATH]/pending-signals.md` — unresolved signals
6. `[VAULT_PATH]/wiki/threads/*.md` — active tracked conversations
7. `[VAULT_PATH]/outputs/` — most recent brief file for calendar/don't-forget items

## Output Structure

Overwrite `[VAULT_PATH]/HOT.md` entirely:

```markdown
# HOT — Vault State (auto-generated)
**Last pipeline run:** YYYY-MM-DD HH:MM [TZ]
**Wiki pages:** N open reqs, N active candidates, N archived candidates, N sources this cycle

---

## Requires Action Today
[Overdue scorecards, no-replies >10d, offers in flight, onboarding SLAs, compliance holds]
[Each item: candidate name, req, what's needed, how long it's been waiting]

## Watch — Moving But Needs Attention
[Per-req candidate tables for reqs with active pipeline movement]
| Req | Candidate | Stage | Last Action | Next Step |
|---|---|---|---|---|

## Recently Closed (last 14 days)
[Closed reqs + hired candidates with start dates]

## Active Reqs Summary
| Req | Role | Location | Age | HM | Hottest Item |
|---|---|---|---|---|---|
[Flag reqs >90 days old — note the age visibly]

## Scan Intelligence — Active Patterns
[Patterns from scan-intelligence.md that are currently firing, with recommended actions]

## Pending Signals
[Count and top 3 urgent items from pending-signals.md]

## Pipeline Status
- Last run: [date/time from log.md]
- Sources enabled: [list from vault.yaml]
- Next scheduled run: [from vault.yaml schedule if configured]
```

## Rules
- Overwrite entirely on each run — never append
- Keep under 100 lines
- Use `[[wikilinks]]` for all candidate and req references
- Req age >90d → flag clearly in summary table
- No-reply >10d → flag in "Requires Action Today" with day count
- Skip candidate counts for `status: archived` in the active count (include in archived count only)
- NEVER use Bash for data processing — use Read/Write/Grep/Glob tools. Bash is ONLY for git commands and trivial single commands.
