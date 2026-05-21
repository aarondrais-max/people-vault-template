---
name: process-meeting-note
description: Ad-hoc processing of a meeting note file into wiki updates. Use when you have a meeting note that wasn't picked up by ingest-granola, or for notes captured outside of Granola.
user_invocable: true
trigger: "process-meeting-note, process meeting, process this note, update wiki from this meeting"
---

You are processing a meeting note into wiki updates for the People Team Knowledge Vault.

Read `[VAULT_PATH]/vault.yaml` and `[VAULT_PATH]/CLAUDE.md`.

## Step 0: Identify the Meeting Note

If the user provides a file path: read that file directly.
If the user pastes text inline: treat that text as the source content.
If neither: ask the user to provide the meeting note or file path.

## Step 1: Classify the Meeting

Determine meeting type:
- **[SCREEN]** — Recruiter phone screen (you organized, candidate was the subject)
- **[INTAKE]** — HM kickoff / role intake meeting
- **[DEBRIEF]** — Panel or HM debrief / decision meeting
- **[HM_INTERVIEW]** — HM interview round (you attended or took notes)
- **[SYNC]** — Team sync, HM sync, or stakeholder meeting (not directly about a candidate)
- **[OTHER]** — Something else

Also identify:
- Candidate name (if applicable)
- Req ID or role (if applicable)
- Meeting date
- Participants

## Step 2: Save Raw Source

Save the meeting note to `[VAULT_PATH]/sources/meetings/YYYY-MM-DD-[type]-[subject].md`:

```yaml
---
source: manual-upload
source_type: meeting
source_date: YYYY-MM-DD
meeting_type: [SCREEN|INTAKE|DEBRIEF|HM_INTERVIEW|SYNC|OTHER]
candidate: [Name or "n/a"]
req_id: [R-XXXXX or "n/a"]
participants: []
processed: false
---
```

Then append the meeting note content.

After saving, set `processed: true` in the frontmatter.

## Step 3: Process by Meeting Type

Follow the processing rules from `vault-daily-sync.md` for the detected meeting type:

- **[SCREEN]**: Extract background, comp, strengths, concerns, competing offers, advance decision. Write/update `## Screen Notes` on candidate page. Create Tier 1 candidate page if at RPS stage and page doesn't exist.
- **[INTAKE]**: Extract must-haves, anti-patterns, sourcing guidance, comp clarity, urgency. Update `## HM Preferences` on req page. Trigger Referral Bullets refresh.
- **[DEBRIEF]**: Extract panel lean, strengths, concerns, decision. Write/update `## Debrief Notes` on candidate page. Update stage and req Pipeline table. If reject: archive candidate to Tier 2.
- **[HM_INTERVIEW]**: Same structure as debrief, label section `## HM Interview Notes`.
- **[SYNC]**: Extract action items, decisions, and any candidate/req signals. Route to appropriate wiki pages (req Decisions Log, people page Interaction History).
- **[OTHER]**: Extract any actionable signals and route to appropriate pages or pending-signals.md.

## Step 4: Update Index

If new wiki pages were created, add them to `[VAULT_PATH]/index.md`.

## Step 5: Log

Append to `[VAULT_PATH]/log.md`:
```
## [YYYY-MM-DD] process-meeting-note | Manual meeting note processing
- Meeting type: [type]
- Subject: [candidate/req or description]
- Source saved: sources/meetings/[filename].md
- Wiki pages updated: [list]
- New pages created: [list or "none"]
```

Append to `[VAULT_PATH]/changelog.md`:
```
## [YYYY-MM-DD] process-meeting-note
- [bullet per wiki page changed]
```

## Rules
- Save to sources/ FIRST before touching wiki/ — raw source is immutable record
- NEVER read or write `status: archived` candidate pages
- Every wiki update must reference the source file path
- NEVER use Bash for data processing — use Read/Write/Grep/Glob tools. Bash is ONLY for git commands and trivial single commands.
