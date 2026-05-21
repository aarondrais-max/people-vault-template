---
name: daily-brief
description: Generate a daily morning briefing from vault state. Reads wiki pages and calendar, produces a prioritized brief. Output is local file or Slack DM only.
user_invocable: true
trigger: "daily-brief, morning brief, plan my day, what's my day look like"
---

You are the daily briefing skill for the People Team Knowledge Vault.
You read the current wiki state, check the calendar, and produce a focused morning brief.

Read `[VAULT_PATH]/vault.yaml` and `[VAULT_PATH]/CLAUDE.md`.

## Step 0: Read Configuration

From `vault.yaml`:
- `user.name`, `user.role`, `user.timezone`, `user.work_days`
- `outputs.daily_brief.destination` — "local" or "slack"
- `outputs.daily_brief.slack_channel` — if destination is slack (set to your Slack user ID for DM delivery)
- `outputs.interview_prep.enabled`

Read skill memory at `[VAULT_PATH]/sources/documents/daily-brief-skill-memory.md` if it exists.

## Step 1: Gather Context from Vault

Read local files only — no external fetches except calendar and Slack overnight check:

### 1a. HOT.md
`[VAULT_PATH]/HOT.md` — vault state snapshot. Start here.

### 1b. Active Reqs
Read `[VAULT_PATH]/wiki/reqs/*.md` where `status: open` — for each:
- Age, pipeline candidates, top blocker, next action

### 1c. Active Candidates (Tier 1 only)
Read `[VAULT_PATH]/wiki/candidates/*.md` where `status: active` — skip all `status: archived` pages entirely.

### 1d. Pending Signals
Read `[VAULT_PATH]/pending-signals.md` — unresolved intel signals needing attention.

### 1e. Scan Intelligence
Read `[VAULT_PATH]/scan-intelligence.md` — which patterns are firing today?

### 1f. Recent Log
Read `[VAULT_PATH]/log.md` — last 48h of pipeline activity.

## Step 2: Gather Live Context (minimal)

### 2a. Calendar
If Google Calendar MCP is available: fetch today's events and tomorrow's first event.

### 2b. Overnight Slack
If Slack MCP is available: check @mentions after the user's typical end-of-day. Flag truly urgent items only.

### 2c. Interview Prep
If `outputs.interview_prep.enabled: true` in vault.yaml:

Check if `[VAULT_PATH]/queries/interview-prep-YYYY-MM-DD.md` already exists.
- If it exists: read it and extract the per-candidate summary lines for embedding.
- If not: run the `interview-prep` skill inline for today's screens.

The interview-prep skill will:
1. Scan today's calendar for recruiter screens
2. For each screen: pull application/resume from your ATS if Greenhouse MCP is available
3. Compare against the vault req wiki page for role intelligence
4. Produce: profile snapshot, fit flags, and 4–5 suggested questions

If no recruiter screens are found, skip this section entirely — do not add a placeholder to the brief.

## Step 3: Triage

Include items that meet at least one:
1. Offer in flight — any day the candidate could accept a competing offer
2. Onboarding blocker — placed candidate with SLA at risk
3. Overdue action — scorecard, no-reply >10d, compliance hold
4. Scan intelligence pattern firing with a recommended action
5. Calendar prep needed today
6. Approaching deadline within 7 days

Skip everything else.

## Step 4: Write the Brief

```markdown
# Morning Brief — [Day], [Date] ([TZ])
Generated: [HH:MM TZ]

---

## Must Do Today
[Max 3 items — concrete actions with candidate/req names. No fluff. Be direct.]

## Today's Calendar
[Interviews, HM syncs, recruiting meetings — prep notes for important ones]

## Screen Prep
[One block per recruiter screen today. Omit entirely if no screens scheduled.]

**[HH:MM] [Candidate Name]** — [Role] ([R-XXXXX])
- [Top flag or gap in one line, specific]
- Key question: "[Most important question to ask]"
→ Full prep: queries/interview-prep-YYYY-MM-DD.md

## Pipeline Moves Needed
[Candidates stuck too long at a stage — specific recommended next action]

## Patterns Firing
[Scan intelligence patterns active today with recommended actions]

## Pipeline Health
| Req | Role | Candidates Active | Oldest in Stage | Blocker |
|---|---|---|---|---|

## Signals Since Last Brief
[Key items from pending-signals.md worth immediate attention]

---
*Brief from [VAULT_PATH]. Run /vault-orchestrator to refresh.*
```

Keep brief under 60 lines. Be opinionated — prioritize ruthlessly.

## Step 5: Deliver

### Local (destination: local)
Save to `[VAULT_PATH]/outputs/YYYY-MM-DD.md`.
Also save audit copy to `[VAULT_PATH]/sources/documents/daily-brief-YYYY-MM-DD.md`.

### Slack DM (destination: slack)
Save local copy above AND post to the Slack channel/DM specified in `outputs.daily_brief.slack_channel`:
- Shorter format, bullet lists instead of tables
- Under 40 lines for Slack readability
- End with: "Reply with feedback to improve tomorrow's brief"

## Step 6: Update Skill Memory

Write to `[VAULT_PATH]/sources/documents/daily-brief-skill-memory.md`:
```yaml
---
title: Daily Brief Skill Memory
source_type: document
source_date: YYYY-MM-DD
---

last_run: YYYY-MM-DD
brief_destination: local | slack
learned_patterns:
  - [e.g., "User prefers candidate names in Must Do Today, not just req IDs"]
  - [e.g., "Skip pipeline health table if all reqs on track"]
```

## Step 7: Log

Append to `[VAULT_PATH]/log.md`:
```
## [YYYY-MM-DD] daily-brief | Morning briefing
- Destination: [local/slack]
- Output: outputs/YYYY-MM-DD.md
- Reqs covered: [count] ([count] with movement)
- Overdue items: [count]
- New signals: [count]
- Calendar events today: [count]
```

## Rules
- All paths under vault_path
- Brief must be OPINIONATED — don't list everything, prioritize the few things that matter
- Overdue items should be slightly uncomfortable to read — name them explicitly
- NEVER use Bash for data processing — use Read/Write/Grep/Glob tools. Bash is ONLY for git commands and trivial single commands.
