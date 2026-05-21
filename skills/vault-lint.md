---
name: vault-lint
description: Weekly vault maintenance -- check for stale reqs, ghost candidates, broken links, orphan pages, duplicate candidates, and index drift. Saves lint report to queries/.
user_invocable: true
trigger: "vault-lint, lint vault, vault health, check vault"
---

You are running a weekly maintenance pass on the People Team Knowledge Vault.

Read `[VAULT_PATH]/CLAUDE.md` and `[VAULT_PATH]/vault.yaml` first.

## Checks to Run

### 1. Source Traceability (MOST IMPORTANT)

Every active wiki page should have a non-empty `sources:` array.

- Glob `[VAULT_PATH]/wiki/**/*.md` and read each page's frontmatter
- Skip pages with `status: archived` — archived candidates have no sources by design
- Flag active pages where `sources: []` — no evidence trail
- Flag pages where a source path doesn't resolve to an actual file in `sources/`
- Count: pages with sources vs without

### 2. Ghost Candidates

Active candidates showing no movement.

- Read all `[VAULT_PATH]/wiki/candidates/*.md` where `status: active`
- Flag where `last_action` is more than 10 days ago with no `next_action` set
- Flag where stage is `offer` with no movement in 3+ days
- Recommend: final outreach or archive to Tier 2

### 3. Req Age Warnings

- Read all `[VAULT_PATH]/wiki/reqs/*.md` where `status: open`
- Flag reqs where `age_days` > 90 — recommend parallel re-sourcing
- Flag reqs where `age_days` > 60 with no candidate past RPS — pipeline may be stalled

### 4. Stale Wiki Pages

Active pages not updated in 14+ days.

- For each active req or candidate page, check `last_updated`
- If older than 14 days, check if any source file with a more recent date references this entity
- Flag stale pages that should have been updated by the pipeline

### 5. Unlinked Source Files

Every source file should be referenced by at least one wiki page.

- Glob `[VAULT_PATH]/sources/**/*.md` (exclude `.last-ingest` and sweep files)
- For each, grep across `wiki/**/*.md` to see if any wiki page references it
- Flag source files not referenced anywhere — unprocessed intel

### 6. Broken Wikilinks

- For each wiki page, extract all `[[wikilink]]` references
- Check if a corresponding wiki page exists
- Flag broken links

### 7. Duplicate Candidate Check

Detect possible duplicate candidate pages.

- Look for candidates with very similar names (e.g., "Jordan Smith" and "J Smith")
- Look for two active candidate pages referencing the same req with very similar stages
- Report merge candidates

### 8. Silver Medalist Index

- Read all `[VAULT_PATH]/wiki/candidates/*.md` where `status: archived` and `silver_medalist: true`
- Group by `re-engage for:` field
- Report: "X silver medalists available for [role type]"
- This is the talent bank summary for future reqs — high value output

### 9. Index Drift

Check if `[VAULT_PATH]/index.md` matches actual pages on disk.

- Pages on disk not in index → missing entries
- Pages in index not on disk → phantom entries
- Auto-fix: update index.md to match reality

### 10. Scan Intelligence Validation

- Read `[VAULT_PATH]/scan-intelligence.md`
- For each pattern, check if it has been observed in the last 30 days
- Flag patterns with no recent evidence — may be stale
- Flag patterns marked "low confidence" with 3+ evidence items — should be upgraded to medium

## Output

Create lint report at `[VAULT_PATH]/queries/vault-lint-YYYY-MM-DD.md`:

```yaml
---
title: Vault Lint Report -- YYYY-MM-DD
type: query
created: YYYY-MM-DD
---
```

Prioritize findings by severity:
- **CRITICAL**: Phantom source references, duplicate candidates, broken links on active pages
- **HIGH**: Ghost candidates (no movement >10d), stale req pages, unlinked sources
- **MEDIUM**: Req age warnings, stale wiki pages
- **LOW**: Index drift, stale scan intelligence patterns

## Auto-Fix (lightweight)

Fix automatically:
- **Index drift**: Add missing pages to index.md, remove phantom entries

For everything else, report but don't fix — the vault owner reviews and decides.

## Log Entry

Append to `[VAULT_PATH]/log.md`:
```
## [YYYY-MM-DD] vault-lint | Weekly maintenance
- Source traceability: X/Y active pages have sources
- Ghost candidates: X flagged
- Req age warnings: X (>90d: X, >60d stalled: X)
- Stale pages: X
- Unlinked sources: X
- Broken links: X
- Duplicate candidates: X
- Silver medalists indexed: X across Y req types
- Full report: queries/vault-lint-YYYY-MM-DD.md
```

## Rules
- Skip `status: archived` candidate pages in all checks except silver medalist index
- NEVER use Bash for data processing — use Read/Write/Grep/Glob tools. Bash is ONLY for git commands and trivial single commands.
