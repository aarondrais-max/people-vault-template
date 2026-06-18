---
name: ingest-pipeline-sheet
description: Recruiter source-of-truth ingest -- reads the Greenhouse-fed pipeline Google Sheet, writes an immutable snapshot to sources/pipeline/, and emits [PIPELINE] signals with authoritative candidate stage. Requires the Google Drive/Sheets connector. Recruiter role only.
---

You ingest the recruiter's **source-of-truth pipeline** from their Greenhouse-fed Google Sheet.

This is the one ingest that carries **authoritative stage data** (straight from the ATS via Greenhouse's report connector). Every other ingest carries *context* (what people said in Slack/email/meetings). Your snapshot is what `vault-daily-sync` trusts for stage; comms only layer color on top.

**You do NOT write wiki pages.** Like every ingest, you write an immutable record to `sources/` and structured signals to `signal-inbox.md`. `vault-daily-sync` is the only skill that edits req pages.

## Step 0: Read Configuration

1. Read `[VAULT_PATH]/vault.yaml`.
2. Check `ingests.pipeline_sheet.enabled`. If `false` or missing → **skip entirely**, write nothing, return "pipeline_sheet disabled — skipped."
3. Read `ingests.pipeline_sheet.sheet_url`. If empty → skip and note in `[VAULT_PATH]/pending-signals.md`: `- [YYYY-MM-DD] ⚠️ pipeline_sheet enabled but no sheet_url set. Add it to vault.yaml or re-run /vault-setup.`
4. Read `recruiter.tracked_reqs` — `from_sheet` (ingest every req present in the sheet) or an explicit list of req IDs (ingest only those rows).

## Step 1: Read the Sheet

Using your Google Sheets / Google Drive connector, read the sheet at `sheet_url` (resolve the file ID from the URL). Read the **first/primary tab** unless a tab is named in the URL.

If no Drive/Sheets connector is available, or the read fails: **do not guess or fabricate pipeline data.** Write a note to `pending-signals.md` (`- [YYYY-MM-DD] ⚠️ Could not read pipeline sheet — [reason]. Pipeline this run is comms-derived only.`) and return. The vault still works without it.

**Report layout — this is a Greenhouse report-builder export, not a bare table:**
- The first few rows are a **preamble**: report title, `Report Path` (a token), `Last Updated At`, `Report Requested By`, and a one-line filter summary (e.g. "Type is Candidate + Status (Job) is Open + Recruiter is [name]").
- Then the **column header row** (begins `First Name | Last Name | Job Name | Requisition ID | ...`).
- Then candidate rows.
- A **`Filters` block** at the very bottom restates the report filters — stop reading data when you reach it.

Find the header row by locating the row that contains `First Name` and `Requisition ID` — do **not** assume row 1. Capture `Last Updated At` from the preamble as the snapshot's freshness stamp; if it's more than ~24h old, flag that in the snapshot so downstream skills know the ATS data may lag.

## Step 2: Map Columns by Header

These are standard Greenhouse report-builder column names — every recruiter who builds the report the same way gets the same headers. Map by exact name first, with a case-insensitive fuzzy fallback. Expect extra columns (e.g. `Anaplan ID`, `Last Scheduled Interview`) — ignore the ones not listed.

| Vault field | Greenhouse column | Notes |
|---|---|---|
| candidate | `First Name` + `Last Name` | **concatenate and trim** — name is two columns |
| req_title | `Job Name` | |
| req_id | `Requisition ID` | e.g. R-11945 |
| stage | `Stage` | New Applicant, Recruiter Phone Screen, Calibration, Hiring Manager Interview, Panel/Onsite, Offer, … |
| status | `Status` | Active / Rejected (job-level Open/Closed is already filtered server-side) |
| hiring_manager | `Hiring Manager Name` | feeds `wiki/people/` + HM-aware toolkit skills |
| primary_recruiter | `Primary Recruiter` | may differ from the report's recruiter filter — see scope note |
| last_activity | `Last Activity` | |
| last_stage_change | `Last Stage Change` | when they entered the current stage |
| next_interview | `Next Scheduled Interview` | feeds "what's next" in HOT.md — capture when present |
| current_company | `Company` | candidate's current employer (often blank) |
| current_title | `Title` | candidate's current title (often blank) |
| source | `Source` | Referral, LinkedIn, agency name, etc. |
| location | `Location` | |

If `First Name`, `Requisition ID`, or `Stage` can't be found, note it in `pending-signals.md` and stop — don't map blindly.

**Dedupe:** a candidate can appear on more than one req (e.g. the same person under two openings). Key rows by **candidate + req_id**, never name alone.

**Scope.** The report is filtered server-side, so every row is already in the user's scope. But `Primary Recruiter` may name someone else on a req where the user is secondary (e.g. a shared DACH req). Handle by `recruiter.tracked_reqs`:
- `from_sheet` (default): ingest all rows. When `Primary Recruiter` ≠ the vault owner, tag that req `(secondary)` in the snapshot so HOT.md can de-emphasise it rather than drown in another recruiter's pipeline.
- explicit list: keep only those req IDs.

## Step 3: Write the Immutable Snapshot

Write `[VAULT_PATH]/sources/pipeline/YYYY-MM-DD-pipeline-sheet.md` (create `sources/pipeline/` if absent). This is an immutable source record — never edited after writing.

```markdown
---
source: pipeline_sheet
date: YYYY-MM-DD
type: pipeline
processed: false
sheet_url: [sheet_url]
authoritative: true
report_last_updated: [Last Updated At from preamble]
---

# Pipeline Snapshot — YYYY-MM-DD

*Source of truth: Greenhouse report connector → Google Sheet. Stage here overrides comms-derived stage.*
*Report last refreshed: [Last Updated At]. [If >24h old: ⚠️ ATS data may lag.]*

## R-XXXXX — [Req Title] · HM [Hiring Manager] · Primary [Primary Recruiter]
| Candidate | Stage | Status | Next Interview | Last Activity |
|---|---|---|---|---|
| [First Last] | [Stage] | [Status] | [date or —] | [YYYY-MM-DD] |

## R-YYYYY — [Req Title] · HM [Hiring Manager] · Primary [Primary Recruiter] (secondary)
| Candidate | Stage | Status | Next Interview | Last Activity |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
```

Group rows by req — one table per req, with HM and primary recruiter in the heading. Tag reqs the user doesn't primary with `(secondary)`. Order active candidates (Status = Active) above rejected ones within each req. Carry `Hiring Manager Name` into the `[PIPELINE]` reconciliation so `wiki/people/` HM pages and HM-aware skills stay current.

## Step 4: Emit [PIPELINE] Signals

Append one signal per req to `[VAULT_PATH]/wiki/signal-inbox.md`, so `vault-daily-sync` updates the req Pipeline tables from authoritative data:

```
- [YYYY-MM-DD] [pipeline_sheet] R-XXXXX [PIPELINE] Authoritative stages from sheet → reconcile req Pipeline table. Source: sources/pipeline/YYYY-MM-DD-pipeline-sheet.md
```

Do NOT emit a separate signal per candidate — one `[PIPELINE]` signal per req keeps the inbox lean; the snapshot file holds the per-candidate detail.

## Step 5: Return Summary

Return a short summary: reqs ingested, total candidates, any reqs in `tracked_reqs` that were missing from the sheet, and any header-mapping issues.

## Rules
- Authoritative for **stage and active/rejected status only** — not for soft intel (comp asks, competing offers, sentiment). Those stay comms-derived.
- Never write or edit wiki pages — only `sources/pipeline/` and `signal-inbox.md`.
- Never fabricate rows. A missing/unreadable sheet means comms-derived pipeline this run — say so, don't invent.
- Never read or include candidate rows for reqs outside `tracked_reqs` when an explicit list is set.
- NEVER use Bash for data processing — use Read/Write/Grep/Glob and your Sheets connector. Bash is ONLY for git and trivial single commands.
