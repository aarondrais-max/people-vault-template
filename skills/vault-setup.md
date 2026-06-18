---
name: vault-setup
description: Interactive setup wizard — asks role, name, timezone, integrations, and vault path, then generates personalized CLAUDE.md and vault.yaml
user_invocable: true
trigger: "set up the vault, vault setup, configure my vault, initialize vault"
---

# vault-setup — Interactive Setup Wizard

You are running the People Team Knowledge Vault setup wizard. Your job is to ask the user a short series of questions and then generate their personalized `CLAUDE.md` and `vault.yaml` files.

Work through the questions conversationally — ask one or two at a time, not all at once. Confirm answers before moving on. At the end, write both files and confirm what was created.

---

## Step 1 — Welcome

Greet the user and explain what's about to happen:

> "Welcome to the People Team Knowledge Vault setup. I'll ask you a few quick questions, then generate your personalized config files. This takes about 5 minutes."

---

## Step 2 — Role

Ask:

> "First — what's your role on the People team? Pick the one that fits best:
> 1. Recruiter / Talent Acquisition
> 2. HRBP / People Partner
> 3. Compensation & Benefits
> 4. L&D / Enablement
> 5. People Operations / Generalist
> 6. Facilities / Workplace
> 7. Other (describe it)"

Map their answer to one of these role keys:
- 1 → `recruiter`
- 2 → `hrbp`
- 3 → `comp`
- 4 → `ld`
- 5 → `people-ops`
- 6 → `facilities`
- 7 → `generic`

Store the role key — you will use it to select the right CLAUDE.md template below.

---

## Step 3 — Name, Org, and Timezone

Ask:

> "What's your name, your team or org name, and your timezone? (e.g., 'Alex Rivera, Talent Acquisition at Acme Corp, America/Chicago')"

Parse out:
- `YOUR_NAME` — their full name
- `YOUR_ROLE` — their role title (derive from their role key + any detail they give — e.g., "Senior Recruiter, APAC" or "HRBP, Europe")
- `YOUR_ORG` — team/org name
- `YOUR_TIMEZONE` — timezone string (accept city names and convert: "Tokyo" → "Asia/Tokyo", "London" → "Europe/London", "New York" → "America/New_York", "Chicago" → "America/Chicago", "LA" or "Los Angeles" → "America/Los_Angeles", "Sydney" → "Australia/Sydney", "Singapore" → "Asia/Singapore", "Paris" → "Europe/Paris")

If their role title isn't clear, ask a quick follow-up: "What's your actual job title?" Keep it brief.

---

## Step 4 — Vault Location

Ask:

> "Where do you want to store the vault on your machine? If you're running me inside the vault folder right now, just say 'here'. Otherwise, give me the path — e.g., `~/Documents/PeopleVault`."

If they say "here", use the current working directory. Otherwise use the path they give.

Store as `VAULT_PATH`.

---

## Step 5 — Integrations

Ask:

> "Which of these tools do you have connected to Claude? Check all that apply — just list the ones you have.
> - Slack
> - Gmail
> - Glean
> - Granola
> - Google Drive
> - Confluence
> - Linear / Jira
> - Notion"

Map their answer to `enabled: true` or `enabled: false` in vault.yaml for each source. Granola is recruiter-leaning — if role is not `recruiter`, default it to `false` unless the user explicitly includes it.

If the role is `recruiter`, do NOT ask about the ATS or pipeline sheet here — that's handled in the recruiter step below. There is no direct ATS ingest; Greenhouse data flows in via the pipeline sheet.

If they say "I'm not sure" or "none", enable Slack and Gmail only — they're the lowest-friction pair.

---

## Step 6 — Slack setup (if Slack enabled)

Ask:

> "For Slack: what channels do you want to monitor? Give me the channel names (without the #). Also, any key contacts whose DMs you want tracked — name and Slack user ID if you have it."

If they don't know Slack user IDs, note: "You can find them by clicking someone's profile in Slack → More → Copy member ID. You can add them to vault.yaml later."

Store channel list and DM contacts.

If Slack is not enabled, skip this step.

---

## Step 6b — Recruiter deep config (recruiter role only)

**Only run this step if the role key is `recruiter`. For every other role, skip it entirely and go to Step 7.**

Tell the user: "A few recruiter-specific questions so the vault and the TA Toolkit work the way you do. All optional — press enter to take the default."

Ask these conversationally, a couple at a time. Store each answer for Step 9.

**a. Stack**
> "Which ATS does your team use — Greenhouse, Ashby, or other? And your main sourcing tool — Juicebox, Findem, LinkedIn Recruiter, or other?"
- Store `ats` and `sourcing_tool`.

**b. Pipeline sheet (source of truth)**
> "Do you have a Greenhouse report feeding a Google Sheet with your pipeline — the same report-connector setup as the ELT sheet? If so, paste the sheet URL and I'll read it as your authoritative pipeline (stage straight from the ATS). If not, the walkthrough has the setup steps — you can add it later."
- If they paste a URL: set `pipeline_sheet.enabled: true` and `pipeline_sheet.sheet_url`. Confirm they've granted the Google Drive/Sheets connector access to that sheet.
- If not: leave `pipeline_sheet.enabled: false`. Note that pipeline will be comms-derived until they add it.

**c. Candidate tiering**
> "When should I create a full candidate page — at recruiter screen (the default), or a different stage? And should I track strong non-hires as silver medalists for future re-engagement? (default: yes)"
- Store `candidate_tiering.tier1_stage` (default `rps`) and `track_silver_medalists` (default `true`).

**d. Tracked reqs**
> "Should I track every req in your pipeline sheet (default), or a specific list of req IDs?"
- Store `tracked_reqs` — `from_sheet` or the list.

**e. Hiring managers & stakeholders**
> "Who are your key hiring managers and stakeholders? For each: name, role, and Slack ID if you have it. I'll pre-load them so people pages and HM-aware skills work from day one."
- Store the list for the `## Key Relationships Reference` table in CLAUDE.md.

---

## Step 6c — Link the TA Toolkit (recruiter role only, optional)

**Only run if role is `recruiter`.** This is the step that lights up the toolkit's vault-aware skills.

Explain: "If you use the Amplitude TA Toolkit, I can connect it to this vault so skills like hm-update, candidate-summary, intake-brief, and candidate-profile-scoring read your reqs, candidates, and pipeline automatically — instead of you pasting context every time."

Check whether `~/.amplitude-ta-toolkit.yaml` exists:

- **If it exists:** "I found your toolkit profile. Want me to set `uses_vault: true`, `vault_path: [VAULT_PATH]`, and `level: advanced` so the vault-aware skills turn on? (recommended)"
  - **Ask before writing.** If yes: update only those three keys in `~/.amplitude-ta-toolkit.yaml`, preserving everything else. Also mirror `ats` and `sourcing_tool` from Step 6b into the profile if those keys are present. Set `recruiter.toolkit_linked: true` in vault.yaml.
  - If no: leave it; note they can flip `uses_vault: true` themselves later.
- **If it does NOT exist:** "I don't see the TA Toolkit installed yet. Once you've run `/setup-ta-toolkit`, re-run me — or edit `~/.amplitude-ta-toolkit.yaml` and set `uses_vault: true` + `vault_path: [VAULT_PATH]`. Leaving it unlinked for now." Leave `toolkit_linked: false`.

Never write the toolkit profile without explicit confirmation.

---

## Step 7 — Existing daily workflow

Ask:

> "Do you already have a system for reviewing priorities each morning — a task manager, a Slack channel you check, a Notion board, anything like that? Or do you not have a set routine?"

Based on their answer:

- **They have an existing system** → ask: "Should the vault brief slot in alongside that — just new signals and urgent flags — or would you prefer it to be a full daily summary you can work from directly?"
  - Alongside → `brief_mode: supplement`
  - Full summary → `brief_mode: primary`
- **No existing system** → set `brief_mode: primary`
- **Not sure** → default to `brief_mode: primary` and note they can change it in vault.yaml later

Store as `BRIEF_MODE`.

---

## Step 8 — Daily brief delivery

Ask:

> "Do you want your daily brief delivered to Slack (as a DM to yourself) or saved locally in the vault? If Slack: what's your Slack member ID? (Slack → Profile → More → Copy member ID)"

- If Slack: set `destination: slack` and `slack_channel: [their ID]`
- If local: set `destination: local`

---

## Step 9 — Write the files

Now generate both files.

### 9a — Select the right CLAUDE.md template

Based on their role key, use the matching template file:
- `recruiter` → `CLAUDE-recruiter.md`
- `hrbp` → `CLAUDE-hrbp.md`
- `comp` → `CLAUDE-comp.md`
- `ld`, `people-ops`, `facilities`, `generic` → `CLAUDE-generic.md`

Read the selected template file. Make the following substitutions throughout:
- `[YOUR_NAME]` → their name
- `[YOUR_ROLE]` → their role title
- `[YOUR_ORG]` → their org
- `[YOUR_TIMEZONE]` → their timezone
- `[YOUR_SLACK_ID]` → their Slack ID (if provided, otherwise leave placeholder)
- `[VAULT_PATH]` → their vault path

Write the result to `CLAUDE.md` in the vault root.

If the user's role key is `recruiter`, also delete `CLAUDE-hrbp.md`, `CLAUDE-comp.md`, and `CLAUDE-generic.md` from the vault. If `hrbp`, delete the others. And so on — keep only the one that was used, plus `CLAUDE-generic.md` as a fallback. Actually: just delete all `CLAUDE-[role].md` variant files after writing `CLAUDE.md`. The user doesn't need them.

### 9b — Write vault.yaml

**Edit the `vault.yaml` that ships with the vault in place** — replace placeholder values and flip `enabled` flags from their answers. Do NOT regenerate the file from scratch: the shipped file carries the full comments, the recruiter block, and the `pipeline_sheet` source, all of which must be preserved. The structure below is for reference only:

```yaml
---
# People Team Knowledge Vault — Configuration
# Generated by vault-setup wizard.

user:
  name: "[SUBSTITUTED_NAME]"
  role: "[SUBSTITUTED_ROLE]"
  org: "[SUBSTITUTED_ORG]"
  timezone: "[SUBSTITUTED_TIMEZONE]"
  work_days: [Mon, Tue, Wed, Thu, Fri]
  slack_user_id: "[SUBSTITUTED_SLACK_ID]"

vault_path: "[SUBSTITUTED_VAULT_PATH]"

ingests:

  slack:
    enabled: [true|false]
    lookback_hours: 48
    channels:
      [CHANNEL_LIST or empty]
    dm_contacts:
      [DM_CONTACT_LIST or empty]

  gmail:
    enabled: [true|false]
    lookback_hours: 48
    ingest_sent: true
    ingest_received: true

  glean:
    enabled: [true|false]
    lookback_hours: 48

  granola:
    enabled: [true|false]
    lookback_hours: 72

  gdrive:
    enabled: [true|false]

  confluence:
    enabled: [true|false]

  linear:
    enabled: [true|false]

  jira:
    enabled: false

  notion:
    enabled: [true|false]

  claude_conversations:
    enabled: false

outputs:
  daily_brief:
    enabled: true
    mode: [primary|supplement]   # primary = full daily summary | supplement = new signals + urgent only
    destination: [local|slack]
    [slack_channel line if slack]

  interview_prep:
    enabled: true
    include_tomorrow: false

mode:
  light: false

validation:
  glean_sweep: [true if glean enabled, else false]
  sweep_days: [Mon, Wed, Fri]

git:
  snapshot: true

wiki:
  page_types:
    - reqs
    - candidates
    - people
    - patterns
    - decisions
    - concepts
    - projects
    - threads
```

---

### 9c — Recruiter writes (recruiter role only)

If the role is `recruiter`, also:

1. **vault.yaml `recruiter:` block** — fill `ats`, `sourcing_tool`, `candidate_tiering.tier1_stage`, `candidate_tiering.track_silver_medalists`, `tracked_reqs`, and `toolkit_linked` from Steps 6b/6c.
2. **vault.yaml `ingests.pipeline_sheet`** — if they gave a sheet URL, set `enabled: true` and `sheet_url`. Otherwise leave `enabled: false`.
3. **CLAUDE.md `## Key Relationships Reference` table** — replace the placeholder rows with the hiring managers and stakeholders from Step 6b(e). Keep the table format (Name | Role | Signal Priority); mark managers/headcount authorities HIGH, HMs MEDIUM.
4. **TA Toolkit profile** — only if they confirmed in Step 6c: edit `~/.amplitude-ta-toolkit.yaml`, setting `uses_vault: true`, `vault_path: [VAULT_PATH]`, `level: advanced`, preserving all other keys. If the file doesn't exist, skip and remind them to run `/setup-ta-toolkit` then re-link.

---

## Step 10 — Confirm

After writing both files, confirm with a summary like:

> "Your vault is ready. Here's what I set up:
>
> - **CLAUDE.md** — [Role] config for [Name], timezone [Timezone]
> - **vault.yaml** — ingests enabled: [list], brief goes to [local/Slack]
> - **Vault path:** [path]
>
> To start using the vault, open Claude and say 'boot the vault' — or if you're in Claude Code, type `/vault-boot`.
>
> To run the full pipeline for the first time: `/vault-orchestrator`"

**Recruiter role — add to the summary:**
> - **Pipeline source:** [sheet connected — authoritative stage from Greenhouse / comms-derived (no sheet yet)]
> - **TA Toolkit:** [linked — vault-aware skills are on / not linked — run /setup-ta-toolkit then re-run me]
> - **Hiring managers loaded:** [count]
>
> Try it: run `/hm-update` for one of your reqs — it'll pull straight from your pipeline, no pasting."

---

## Error handling

- If the user doesn't know their Slack ID, leave the placeholder and note they can add it to `vault.yaml` later.
- If the user skips a question, use sensible defaults (local brief, no DM contacts, standard channels empty).
- If a template file doesn't exist for their role, fall back to `CLAUDE-generic.md`.
- If the user is running this in Claude chat (not Claude Code), you cannot write files directly. In that case: display the final content of both files in code blocks and ask the user to save them manually to the vault folder.
