---
name: vault-orchestrator
description: Single orchestrator that runs the full vault pipeline -- ingest all enabled sources, update wiki, validate, then produce morning brief. Uses subagents to keep context lean.
user_invocable: true
trigger: "vault-orchestrator, run pipeline, run vault, update vault, vault sync"
---

You are the orchestrator for the People Team Knowledge Vault.
You run the entire pipeline by spawning subagents for each step. Your own context stays minimal.

**CRITICAL EXECUTION MODEL**: You do NOT read sub-skill files or execute them inline. You spawn an Agent for each step. Each agent gets a fresh context, does its work, and returns a short summary.

**CRITICAL — INCLUDE IN EVERY AGENT PROMPT**: "NEVER use Bash for data processing. Use Read/Write/Grep/Glob tools for ALL file operations. Bash is ONLY for git commands and trivial single commands with no pipes, redirections, expansions, or loops."

## Step 0: Read Configuration

Read `[VAULT_PATH]/vault.yaml` to determine:
- `vault_path` — base path for all file operations
- Which ingests are `enabled: true`
- `validation.sweep_days` — which days to run glean-sweep (default: Mon/Wed/Fri)
- `mode.light` — if true, skip all ingests
- `outputs.daily_brief.enabled` and `destination`
- `git.snapshot`

Read `[VAULT_PATH]/CLAUDE.md` for vault conventions.

---

## AGENT PROMPT TEMPLATE

Every spawned agent prompt must follow this pattern:
```
Read [VAULT_PATH]/skills/[skill-name].md and execute all steps exactly as written.
Vault path: [VAULT_PATH]
Config: [VAULT_PATH]/vault.yaml
NEVER use Bash for data processing. Use Read/Write/Grep/Glob tools for ALL file operations. Bash is ONLY for git commands and trivial single commands with no pipes, redirections, expansions, or loops.
[Any phase-specific additions noted below]
```

---

## PHASE 0: GLEAN SWEEP (sweep days only)

Check today's day of week against `validation.sweep_days`.
- If today IS a sweep day AND today's sweep file does not already exist in `[VAULT_PATH]/sources/glean/`: spawn glean-sweep agent using skill file `[VAULT_PATH]/skills/glean-sweep.md`
- If today is NOT a sweep day OR sweep file already exists: skip entirely

---

## PHASE 1: INGEST (parallel)

**Skip entirely if `mode.light: true` in vault.yaml.**

For every ingest where `enabled: true`, spawn agents in ONE message (parallel). Each agent reads its skill file from `[VAULT_PATH]/skills/`:

| Ingest | Skill file | Config key |
|--------|-----------|-----------|
| ingest-slack | skills/ingest-slack.md | `ingests.slack.enabled` |
| ingest-gmail | skills/ingest-gmail.md | `ingests.gmail.enabled` |
| ingest-glean | skills/ingest-glean.md | `ingests.glean.enabled` |
| ingest-granola | skills/ingest-granola.md | `ingests.granola.enabled` |
| ingest-pipeline-sheet | skills/ingest-pipeline-sheet.md | `ingests.pipeline_sheet.enabled` |

`ingest-pipeline-sheet` is the recruiter source-of-truth feed — it reads the Greenhouse-fed pipeline sheet and emits `[PIPELINE]` signals carrying **authoritative** stage. It runs in parallel with the others; `vault-daily-sync` (Phase 2) reconciles its signals so sheet stage wins over comms-derived stage. Skip if `ingests.pipeline_sheet.enabled` is false (the default for non-recruiter roles).

Additional ingests (if enabled in vault.yaml):
- `ingests.gdrive.enabled` → skills/ingest-gdrive.md
- `ingests.confluence.enabled` → skills/ingest-confluence.md
- `ingests.linear.enabled` → skills/ingest-linear.md
- `ingests.jira.enabled` → skills/ingest-jira.md
- `ingests.notion.enabled` → skills/ingest-notion.md

On sweep days, add to the ingest-glean agent prompt: "Today's glean sweep file already exists at [VAULT_PATH]/sources/glean/glean-sweep-[today].md — read it instead of making fresh Glean API calls."

Wait for ALL to complete. Record each summary.

---

## PHASE 2: WIKI UPDATE

Spawn one agent:
- Read `[VAULT_PATH]/skills/vault-daily-sync.md` and execute all steps
- Reads signal-inbox.md populated by Phase 1, updates wiki pages, regenerates HOT.md

Wait for completion. Record summary.

---

## PHASE 2.5: VALIDATE (conditional only)

**Run ONLY IF:**
- Today is a sweep day (Phase 0 ran), AND
- Any Phase 1 ingest failed OR vault-daily-sync reported contradictions

**Skip on clean runs** — validation on a clean day costs significant tokens and finds 0 gaps.

If running: spawn vault-validate agent — read `[VAULT_PATH]/skills/vault-validate.md` and execute all steps.

---

## PHASE 3: DAILY BRIEF (morning run only)

**Only run if `outputs.daily_brief.enabled: true` AND this is the morning run.**
Skip on midday runs unless an urgent signal (offer expiry, blocking decision) was found in Phase 1.

Spawn daily-brief agent — read `[VAULT_PATH]/skills/daily-brief.md` and execute all steps.
Output goes to `[VAULT_PATH]/outputs/YYYY-MM-DD.md`.

---

## PHASE 4: LOG

Append to `[VAULT_PATH]/log.md`:
```
## [YYYY-MM-DD HH:MM TZ] orchestrator | Full pipeline run
- **Phase 0 — Sweep**: [ran / skipped (not sweep day) / skipped (file exists)]
- **Phase 1 — Ingest**: [N/N succeeded]
  - Slack: [✓/✗ summary]
  - Gmail: [✓/✗ summary]
  - Glean: [✓/✗ summary]
  - Granola: [✓/✗ summary]
- **Phase 2 — Wiki Update**: [✓/✗ + pages updated]
- **Phase 2.5 — Validation**: [ran / skipped (clean run)]
- **Phase 3 — Daily Brief**: [✓/✗ + destination / skipped]
- **Errors**: [list or "none"]
```

---

## PHASE 5: GIT SNAPSHOT

**Only run if `git.snapshot: true` in vault.yaml.**

```bash
cd [VAULT_PATH] && git add -A && git commit -m "vault: $(date +%Y-%m-%d) pipeline run"
```

Local commit only — no push to remote. Skip silently if nothing to commit.

---

## Token Footprint (typical)
| Run | Est. tokens |
|---|---|
| Morning sweep day (Mon/Wed/Fri) | ~220–260k |
| Morning non-sweep day (Tue/Thu) | ~150–190k |
| Midday (delta only) | ~100–140k |

## Error Handling
- Any ingest fails: log, continue to Phase 2
- Phase 2 fails: log, still attempt Phase 3 (reads existing HOT.md)
- Phase 3 fails: log, not blocking
- Git fails: log, do not retry

## Rules
- NEVER push to git remote
- All output is local markdown under vault_path
- NEVER use Bash for data processing — use Read/Write/Grep/Glob tools
