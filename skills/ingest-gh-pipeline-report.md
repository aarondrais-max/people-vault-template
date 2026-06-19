---
name: ingest-gh-pipeline-report
description: Refresh and ingest your Greenhouse Pipeline Report from Google Sheets. Authoritative, near-zero-token pipeline data source. Requires the Google Drive connector and (recommended) Claude in Chrome for full-sheet refresh + read. Recruiter role only.
---

You are an ingest skill for the People Team Knowledge Vault. Your job is to pull the authoritative Greenhouse pipeline report from a Google Sheet and save it as a raw source file. You do NOT update wiki pages.

Read `[VAULT_PATH]/vault.yaml` and `[VAULT_PATH]/CLAUDE.md` from the vault root.

## Step 0: Read Configuration

- Check `ingests.gh_pipeline_report.enabled`. If `false` or missing → **skip entirely**, return "gh_pipeline_report disabled — skipped." (This is the default for non-recruiter roles.)
- Read `ingests.gh_pipeline_report.sheet_id`. If empty → skip and note in `[VAULT_PATH]/pending-signals.md`: `- [YYYY-MM-DD] ⚠️ gh_pipeline_report enabled but no sheet_id set. Add it to vault.yaml or re-run /vault-setup.`
- Read `sheet_gid` (the data tab; default the first gid in the sheet URL), `refresh_via_chrome`, `refresh_wait_seconds`.
- Read `user.name` (used for the Primary Recruiter check) and `exclusions.reqs`.

## What This Report Is

A "Build your own Candidate Report" in Greenhouse that dumps every field of every candidate across your open reqs, fed into a persistent Google Sheet via the **Greenhouse Report Connector**. The connector refreshes the sheet daily, so the data is current at near-zero token cost. Typical schema is 17 columns:

| Col | Field | Notes |
|-----|-------|-------|
| 1 | First Name | |
| 2 | Last Name | |
| 3 | Job Name | Role title |
| 4 | Requisition ID | R-XXXXX |
| 5 | Last Activity | Date |
| 6 | Hiring Manager Name | |
| 7 | Status | Active / Rejected / … |
| 8 | Last Scheduled Interview | Date |
| 9 | Next Scheduled Interview | Date |
| 10 | Anaplan ID | internal ref (may be blank) |
| 11 | Stage | current pipeline stage |
| 12 | Location | |
| 13 | Primary Recruiter | should be you |
| 14 | Company | candidate's current employer |
| 15 | Title | candidate's current title |
| 16 | Source | how they entered pipeline |
| 17 | Last Stage Change | date of most recent stage transition |

**Report filters (set in GH):** Type=Candidate, Status(Job)=Open, Anonymized=False, Recruiter=[you].

## Step 0b: Refresh the Google Sheet (morning run only)

**Uses Claude in Chrome. If Chrome is unavailable, SKIP to Step 1 — the connector refreshes the sheet daily on its own, so recent data is usually present.**

1. Open `https://docs.google.com/spreadsheets/d/[sheet_id]/edit`
2. **Extensions** → **Greenhouse Report Connector** → **Refresh this sheet**
3. Wait `refresh_wait_seconds` (default 90) for the pull to complete.
4. Verify the data looks current.

If the Extensions menu/connector fails, log a warning and proceed — last refresh data is still valuable.

## Step 1: Read the Sheet

**CRITICAL: Do NOT rely on the Google Drive connector's `read_file_content` for large sheets — it truncates at ~130 rows.** A full pipeline can be 600+ rows. Use the Chrome XHR method below to get everything.

### Method: JavaScript XHR (requires a Chrome tab on the sheet)

After Step 0b the sheet is open in Chrome. Execute JavaScript in that tab.

**Use `XMLHttpRequest` (XHR), NOT `fetch()`.** `fetch()` is blocked by Google's cookie policy in the tab context and returns `[BLOCKED]`. XHR returns the full dataset.

```javascript
(() => {
  const xhr = new XMLHttpRequest();
  const sheetId = '[sheet_id]';
  const gid = '[sheet_gid]'; // the data tab
  const url = `https://docs.google.com/spreadsheets/d/${sheetId}/gviz/tq?tqx=out:csv&gid=${gid}`;
  xhr.open('GET', url, false); // synchronous
  xhr.send();
  return xhr.responseText;
})()
```

Returns the full CSV. Line 0 is a merged metadata row (skip); lines 1+ are data rows. CSV field indices are 0-based (First Name = 0, Last Name = 1, … Last Stage Change = 16); fields past 16 are empty padding.

### If Chrome is not available

Fall back to the Google Drive connector `read_file_content` with `fileId = [sheet_id]`. **This truncates at ~130 rows** — log `⚠ Drive read — data may be incomplete (truncation at ~130 rows). Full data requires Chrome XHR.` Parse whatever rows returned.

## Step 2: Validate Data

- Confirm the header row matches the expected schema.
- Count total rows and rows per Requisition ID.
- Find the report metadata row ("Last Updated At: …"). Extract that timestamp — if >36h old, log `⚠ GH report data is stale ({timestamp}). Sheet may not have refreshed.`

**Req exclusion check:** Drop rows whose Requisition ID is in `vault.yaml → exclusions.reqs`.

**Primary Recruiter check:** Drop rows whose `Primary Recruiter` is a non-empty name other than `user.name` (case-insensitive, trimmed) — reqs handed off to another primary recruiter. Keep rows where Primary Recruiter is blank or matches `user.name`. **Safety net:** if this would drop *every* row (e.g. a name-spelling mismatch), keep all rows instead and log `⚠ Primary Recruiter never matched user.name "[name]" — kept all rows; verify vault.yaml + the report column.` Log how many rows/reqs were dropped as handed-off.

## Step 3: Diff Against Previous Snapshot

Read `[VAULT_PATH]/sources/greenhouse/gh-pipeline-latest.md` if it exists. Compute a diff.

**Counts as a change:** new candidate (name+req not seen before), stage change, status change (e.g. Active → Rejected), new/changed Next Scheduled Interview, completed interview (Last Scheduled Interview changed), Last Activity moved, Last Stage Change moved.
**Ignore:** row ordering, whitespace, candidates Rejected in BOTH snapshots.

Build a structured change list (Stage Changes / New Candidates / Status Changes / Interview Updates / Activity Updates). If no previous snapshot: log "First run — no diff available."

## Step 4: Save Snapshot

**4a — latest (overwritten each run):** `[VAULT_PATH]/sources/greenhouse/gh-pipeline-latest.md`
```yaml
---
title: "GH Pipeline Report — Latest Snapshot"
source_type: greenhouse-report
source_date: YYYY-MM-DD
ingested: YYYY-MM-DD
report_updated: "{Last Updated At}"
total_candidates: N
reqs_covered: [R-XXXXX, ...]
---
```
Then the full candidate table (all columns, all rows).

**4b — dated archive (one per day):** `[VAULT_PATH]/sources/greenhouse/gh-pipeline-YYYY-MM-DD.md` — same frontmatter + table, with the diff appended under `## Changes from Previous Snapshot`. Never modify previous days' files.

## Step 5: Write Signals

If changes were detected, write to `[VAULT_PATH]/wiki/signal-inbox.md` in the standard format:
```
- [YYYY-MM-DD] [gh-report] {signal description} → {suggested action}
```

**Signal priority rules:**
- Stage changes → always signal (these drive pipeline movement)
- New candidates → signal
- Status → Rejected/Withdrawn → signal (pipeline exit)
- Interview scheduled → signal (needs prep)
- Activity-only changes → DO NOT signal (too noisy; kept in snapshot for reference)
- A candidate Rejected in BOTH the old and new snapshot → no signal

## Step 6: Log

Append to `[VAULT_PATH]/log.md`:
```
## [YYYY-MM-DD HH:MM TZ] ingest-gh-pipeline-report | GH Pipeline Report ingest
- Report timestamp: {Last Updated At}
- Total candidates: {N} (dropped handed-off: {n}, excluded reqs: {n})
- Reqs covered: {list}
- Changes detected: {N} (stage: {n}, new: {n}, status: {n}, interview: {n})
- Files created/updated: {list}
```

## Rules
- ONLY write to `sources/greenhouse/` and (for signals) `wiki/signal-inbox.md`. Never touch other wiki pages.
- This is the AUTHORITATIVE pipeline data source — it replaces live ATS calls for candidate stage/status.
- The diff is the primary value — it tells vault-daily-sync exactly what moved since the last run.
- Rejected candidates stay in the snapshot (useful for tracking exits) but don't generate signals if they were already rejected last run.
- If the sheet read fails entirely, log and exit gracefully — other ingests still run.
- NEVER use Bash for data processing — use Read/Write/Grep/Glob and your connectors. Bash is ONLY for git and trivial single commands.
