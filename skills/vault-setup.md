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
> - Greenhouse
> - Google Drive
> - Confluence
> - Linear / Jira
> - Notion"

Map their answer to `enabled: true` or `enabled: false` in vault.yaml for each source. Granola and Greenhouse are recruiter-specific — if role is not `recruiter`, default them to `false` unless the user explicitly includes them.

If they say "I'm not sure" or "none", enable Slack and Gmail only — they're the lowest-friction pair.

---

## Step 6 — Slack setup (if Slack enabled)

Ask:

> "For Slack: what channels do you want to monitor? Give me the channel names (without the #). Also, any key contacts whose DMs you want tracked — name and Slack user ID if you have it."

If they don't know Slack user IDs, note: "You can find them by clicking someone's profile in Slack → More → Copy member ID. You can add them to vault.yaml later."

Store channel list and DM contacts.

If Slack is not enabled, skip this step.

---

## Step 7 — Daily brief delivery

Ask:

> "Do you want your daily brief delivered to Slack (as a DM to yourself) or saved locally in the vault? If Slack: what's your Slack member ID? (Slack → Profile → More → Copy member ID)"

- If Slack: set `destination: slack` and `slack_channel: [their ID]`
- If local: set `destination: local`

---

## Step 8 — Write the files

Now generate both files.

### 8a — Select the right CLAUDE.md template

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

### 8b — Write vault.yaml

Write a complete `vault.yaml` with all their answers substituted in. Use the structure below:

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

## Step 9 — Confirm

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

---

## Error handling

- If the user doesn't know their Slack ID, leave the placeholder and note they can add it to `vault.yaml` later.
- If the user skips a question, use sensible defaults (local brief, no DM contacts, standard channels empty).
- If a template file doesn't exist for their role, fall back to `CLAUDE-generic.md`.
- If the user is running this in Claude chat (not Claude Code), you cannot write files directly. In that case: display the final content of both files in code blocks and ask the user to save them manually to the vault folder.
