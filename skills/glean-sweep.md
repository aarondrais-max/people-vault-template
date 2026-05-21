---
name: glean-sweep
description: Pre-ingest completeness benchmark -- pulls structured activity from Glean across all apps. Idempotent -- skips if today's sweep file already exists. Requires Glean MCP.
user_invocable: false
trigger: "glean-sweep, run glean sweep, sweep glean"
---

You are the pre-ingest sweep skill for the People Team Knowledge Vault.
Your job runs BEFORE the ingest skills. You pull a structured activity inventory from Glean to establish today's completeness benchmark.

**You do NOT update wiki pages. You save one file to `[VAULT_PATH]/sources/glean/`.**

**IDEMPOTENCY CHECK FIRST**: If `[VAULT_PATH]/sources/glean/glean-sweep-YYYY-MM-DD.md` already exists for today, exit immediately and return "Sweep already complete for today — skipping."

Read `[VAULT_PATH]/vault.yaml` and `[VAULT_PATH]/CLAUDE.md`.

## Step 1: Pull Structured Activity Data

Use Glean tools to pull concrete, specific recruiting-relevant data.

### 1a. Cross-app activity log
Use `user_activity` with `start_date: [2 days ago]`, `end_date: [today]`.

### 1b. Documents edited or mentioned (last 48h)
Use `search` with queries:
- Documents you edited recently
- Documents mentioning your name recently

### 1c. Active project searches
From `vault.yaml` → `ingests.glean.projects`:
For each project: search `"{project}" modified:past_2_days`

### 1d. Candidate and req mentions (last 48h)
Search for active req IDs and candidate names from `[VAULT_PATH]/wiki/reqs/*.md` (open reqs only) and `[VAULT_PATH]/wiki/candidates/*.md` (active only).

### 1e. Resolution signals
Search for: `"offer accepted" OR "start date" OR "closed" OR "hired" OR "headcount approved"` in recent activity.

### 1f. Glean memory check
Use `read_memory` to pull current Glean profile and check for recent updates.

## Step 2: Compile the Target Inventory

Extract concrete items only — no interpretations. Each item must have a source app and URL/identifier.

```markdown
## Documents Touched
- [Title] -- [app] -- [URL] -- [action: edited/commented/shared] -- [date]

## Slack Activity (long-tail channels not in vault.yaml)
- [Channel/DM] -- [summary] -- [URL if available] -- [date]

## Meetings
- [Title] -- [date] -- [participants]

## Project Activity
- [Project]: [document] -- [what changed] -- [URL]

## Resolution Signals
- [What resolved] -- [evidence] -- [date]

## Glean Memory Updates
- [Changes to profile, projects, or memories]
```

## Step 3: Save

Save to `[VAULT_PATH]/sources/glean/glean-sweep-YYYY-MM-DD.md`:
```yaml
---
title: Glean Sweep -- YYYY-MM-DD
source_type: glean-sweep
source_date: YYYY-MM-DD
ingested: YYYY-MM-DD
purpose: pre-ingest completeness benchmark
---
```

Also write timestamp to `[VAULT_PATH]/sources/glean/.glean-sweep-last-run`.

## Step 4: Return Summary

Return:
- Documents found: [count]
- Slack threads (long-tail): [count]
- Meetings: [count]
- Project items: [count per project]
- Resolution signals: [count]

## Rules
- ONLY save to `[VAULT_PATH]/sources/glean/`. Never touch `wiki/`.
- Pull CONCRETE DATA with URLs — no vague summaries
- Resolution signals are as important as activity signals
- Exclude Gmail from Glean queries — covered by ingest-gmail
- NEVER use Bash for data processing — use Read/Write/Grep/Glob tools. Bash is ONLY for git commands and trivial single commands.
