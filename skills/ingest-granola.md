---
name: ingest-granola
description: Ingest Granola meeting notes into vault sources/meetings/. Identifies recruiter screens, intakes, and debriefs. Writes structured signals to signal-inbox.md.
user_invocable: false
trigger: "ingest-granola"
---

You are the Granola ingest skill for the People Team Knowledge Vault.
You read recent meeting notes from Granola, classify them by type, save them to sources/meetings/, and write structured signals to signal-inbox.md.

**You do NOT update wiki pages.** That is vault-daily-sync's job.

Read `[VAULT_PATH]/vault.yaml` and `[VAULT_PATH]/CLAUDE.md`.

## Step 0: Configuration

From `vault.yaml`, read:
- `user.name`
- `ingests.granola.lookback_hours` — default 72 (meetings need more lookback than messages)

Check `[VAULT_PATH]/sources/meetings/.last-ingest` for the timestamp of the last run.

## Step 1: Fetch Recent Meetings

Use Granola MCP (`list_meetings` then `get_meetings`) to fetch meetings since last ingest.

Filter to recruiting-relevant meetings:
- Meetings where the vault owner was an organizer or participant
- Meetings with titles containing recruiting signals: "screen", "interview", "debrief", "intake", "sync" with a candidate or HM name
- Any meeting that included a candidate name from `[VAULT_PATH]/wiki/candidates/*.md`

## Step 2: Classify Each Meeting

For each qualifying meeting, determine type:

| Signal tag | Criteria |
|---|---|
| `[SCREEN]` | Recruiter phone/video screen — you organized, candidate was the subject |
| `[INTAKE]` | HM kickoff or role intake meeting |
| `[DEBRIEF]` | Panel debrief or hiring decision meeting |
| `[HM_INTERVIEW]` | HM interview round you attended or have notes from |
| `[SYNC]` | Team sync, HM sync, or stakeholder meeting with recruiting content |

If type is unclear, default to `[SYNC]`.

## Step 3: Extract and Save Meeting Content

For each qualifying meeting:

1. Fetch full meeting notes using `get_meetings` or `get_meeting_transcript`
2. Save to `[VAULT_PATH]/sources/meetings/YYYY-MM-DD-[type-slug]-[subject-slug].md`:

```yaml
---
source: granola
source_type: meeting
source_date: YYYY-MM-DD
meeting_type: [SCREEN|INTAKE|DEBRIEF|HM_INTERVIEW|SYNC]
meeting_title: [Granola meeting title]
participants: [list]
candidate: [name or "n/a"]
req_id: [R-XXXXX or "n/a"]
processed: true
---
```

Then include the full meeting notes content.

## Step 4: Write Signals to Inbox

For each saved meeting, write a signal to `[VAULT_PATH]/wiki/signal-inbox.md`:

For typed meetings (`[SCREEN]`, `[INTAKE]`, `[DEBRIEF]`, `[HM_INTERVIEW]`):
```
- [YYYY-MM-DD] [SCREEN] [Candidate Name] [R-XXXXX] → sources/meetings/[filename].md
- [YYYY-MM-DD] [INTAKE] [R-XXXXX] [Role Title] → sources/meetings/[filename].md
- [YYYY-MM-DD] [DEBRIEF] [Candidate Name] [R-XXXXX] → sources/meetings/[filename].md
```

For SYNC meetings: extract any action items, decisions, or candidate/req signals and write them as individual signals:
```
- [YYYY-MM-DD] granola:[SYNC] R-XXXXX [brief signal from meeting] → [recommended action]
```

**Key signals to extract from SYNC meetings:**
- HM decisions about pipeline advancement or rejection
- Comp exception discussions or approvals
- Headcount changes (req approved/closed/paused)
- Timeline pressure or deadlines mentioned
- New sourcing direction or ICP refinements

## Step 5: Update Last Ingest Timestamp

Write current timestamp to `[VAULT_PATH]/sources/meetings/.last-ingest`.

## Step 6: Return Summary

Return:
- Meetings scanned: [count]
- Qualifying meetings: [count]
  - Screens: [count]
  - Intakes: [count]
  - Debriefs: [count]
  - HM Interviews: [count]
  - Syncs: [count]
- Source files written: [count]
- Signals written to inbox: [count]
- Key signals: [top 3]

## Rules
- ONLY write to `sources/meetings/` and `wiki/signal-inbox.md`. Never touch wiki pages directly.
- Save full meeting notes — vault-daily-sync will read them for the detailed processing
- The signal in signal-inbox.md is a pointer to the source file, not a summary of it
- If a meeting references a candidate not in the vault, still write the signal — vault-daily-sync will decide whether to create a page
- NEVER use Bash for data processing — use Read/Write/Grep/Glob tools. Bash is ONLY for git commands and trivial single commands.
