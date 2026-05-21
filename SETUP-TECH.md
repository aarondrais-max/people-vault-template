# Setup Guide — Tech (Claude Code + Automated Pipeline)

This guide is for users with Claude Code CLI installed who want the full automated pipeline: scheduled ingest, wiki updates, and daily briefs running hands-free.

---

## Prerequisites

Before starting, confirm you have:

- [ ] Claude Code CLI installed (`claude --version` should return a version number)
- [ ] At least one MCP integration configured (Slack, Gmail, Glean, or Granola)
- [ ] Obsidian installed (optional but recommended for browsing the vault)
- [ ] Git installed (optional but recommended for snapshots)

If you don't have Claude Code CLI, install it via the [Anthropic documentation](https://docs.anthropic.com/claude-code).

---

## Step 1: Clone or download the template

```bash
git clone https://github.com/[repo-url] ~/Documents/my-recruiting-vault
cd ~/Documents/my-recruiting-vault
```

Or download and unzip — the tech setup works either way.

---

## Step 2: Open in Obsidian (optional)

1. Open Obsidian → "Open folder as vault"
2. Select `~/Documents/my-recruiting-vault`

This gives you a nice browser for the wiki pages while Claude Code handles the pipeline.

---

## Step 3: Configure CLAUDE.md

Open `CLAUDE.md` and replace all placeholders:

| Placeholder | Replace with |
|---|---|
| `[YOUR_NAME]` | Your full name |
| `[YOUR_ROLE]` | Your job title |
| `[YOUR_ORG]` | Your team/organization |
| `[YOUR_TIMEZONE]` | Timezone string (e.g., `America/New_York`, `Europe/London`, `Asia/Tokyo`) |
| `[YOUR_SLACK_ID]` | Your Slack member ID |

Also fill in the **Key Relationships** table with your hiring managers and key stakeholders.

---

## Step 4: Configure vault.yaml

Open `vault.yaml` — every field has an inline comment explaining it. At minimum, fill in:

### Identity
```yaml
user:
  name: Your Name
  role: Senior Recruiter, EMEA
  timezone: Europe/London
  slack_user_id: UXXXXXXXXXX
```

### Vault path
```yaml
vault_path: ~/Documents/my-recruiting-vault  # full path to your vault
```

### Slack channels
```yaml
ingests:
  slack:
    channels:
      - name: recruiting-team
      - name: your-team-channel
      - name: headcount-channel
```

### DM contacts (hiring managers you DM regularly)
```yaml
    dm_contacts:
      - name: Alex Chen
        user_id: UXXXXXXXXXX  # their Slack member ID
        why: hiring manager, EMEA Sales
```

### Disable ingests you don't have
If you don't have Granola, set `ingests.granola.enabled: false`. Same for any other source you're not using.

---

## Step 5: Update .claude/settings.json with your MCP tool IDs

The `.claude/settings.json` file controls which MCP tool calls Claude is allowed to make without prompting you each time.

MCP tool names include a UUID that's specific to your Claude installation. You need to replace the placeholder UUIDs with your actual ones.

**To find your MCP tool names:**
1. Open Claude Code: `claude`
2. Type `/tools` or check `~/.claude/mcp.json` for your configured servers
3. The tool names follow this pattern: `mcp__[UUID]__[tool_name]`

Open `.claude/settings.json` and replace each `[SLACK-UUID]`, `[GMAIL-UUID]` etc. with the UUID from your installation.

Example — if your Slack MCP UUID is `abc123`, change:
```json
"mcp__[SLACK-UUID]__slack_search_public_and_private"
```
to:
```json
"mcp__abc123__slack_search_public_and_private"
```

You can also add permissions interactively: run `claude` and when prompted to allow a tool, choose "Always allow" — it will be added to settings.json automatically.

---

## Step 6: Set vault_path in skills

Open each skill file in `skills/` and verify the vault path references match your actual vault location. By default they use `[VAULT_PATH]` as a placeholder — the orchestrator reads this from vault.yaml and passes it to each agent. If you're using the skills standalone (in Claude chat mode), you'll need to update these paths manually.

Quickest approach: do a find-and-replace for `[VAULT_PATH]` → your actual path (e.g., `~/Documents/my-recruiting-vault`) across all files in the `skills/` directory.

---

## Step 7: Run the first pipeline

```bash
cd ~/Documents/my-recruiting-vault
claude
```

In the Claude Code session:
```
/vault-orchestrator
```

This runs:
1. Glean sweep (if today is Mon/Wed/Fri and Glean is enabled)
2. All enabled ingests in parallel
3. Wiki update pass
4. Validation (if sweep ran and issues found)
5. Daily brief
6. Git snapshot (if `git.snapshot: true`)

The first run will take longer than subsequent runs — it's pulling 48 hours of history from each source and building your initial wiki pages.

---

## Step 8: Git setup (recommended)

If you want version control on your vault (highly recommended for rollback safety):

```bash
cd ~/Documents/my-recruiting-vault
git init
git add CLAUDE.md vault.yaml HOT.md pending-signals.md index.md log.md changelog.md scan-intelligence.md wiki/ skills/ .gitignore
git commit -m "vault: initial setup"
```

Note: `sources/` is excluded by `.gitignore` — it contains raw personal data (emails, Slack messages). Keep it local only.

Set `git.snapshot: true` in vault.yaml to have the pipeline auto-commit after each run.

---

## Step 9: Schedule automated runs (optional)

To have the pipeline run automatically each morning, use your OS task scheduler.

### macOS — cron
Open crontab: `crontab -e`

Add these lines (adjust times and path to match your timezone and vault location):
```
# Morning pipeline — weekdays at 7:00am local time
0 7 * * 1-5 cd ~/Documents/my-recruiting-vault && claude --dangerously-skip-permissions -p "run /vault-orchestrator" > ~/Documents/my-recruiting-vault/outputs/cron-last-run.log 2>&1

# Midday update — weekdays at 1:00pm local time
0 13 * * 1-5 cd ~/Documents/my-recruiting-vault && claude --dangerously-skip-permissions -p "run /vault-orchestrator" > ~/Documents/my-recruiting-vault/outputs/cron-midday.log 2>&1
```

Note: `--dangerously-skip-permissions` bypasses interactive prompts for unattended runs. Only use this once your settings.json allowlist is fully configured (Step 5), so Claude only calls tools you've explicitly allowed.

### macOS — launchd (more reliable than cron)
Create a `.plist` file in `~/Library/LaunchAgents/`. Ask Claude to help you generate this if needed.

---

## Step 10: Verify the setup

After the first pipeline run, check:

- [ ] `HOT.md` has content (not just the template placeholder)
- [ ] At least one file exists in `sources/slack/` or another enabled source
- [ ] `log.md` has a pipeline entry from today
- [ ] `outputs/` has a brief file (if `daily_brief.enabled: true`)

If anything is missing, check `log.md` for error entries and review the relevant skill file in `skills/`.

---

## Daily workflow

Once set up, your daily workflow is:

1. Open Claude Code in the vault directory: `claude`
2. Run `/vault-boot` — loads current state from HOT.md
3. Ask questions in plain English: "What's the status on the Senior AE req?" / "Who do I need to follow up with today?"
4. After interviews, paste notes and ask Claude to update the relevant candidate page

The pipeline handles ingest and wiki updates automatically. You only interact with Claude for questions and decisions.

---

## Troubleshooting

**"MCP tool not found" errors:** Check that the UUID in settings.json matches your installation. Run `/tools` in Claude Code to see available tools.

**Ingest returns no results:** Verify the MCP integration is configured and connected. Check `~/.claude/mcp.json`.

**Pipeline runs but wiki pages aren't updating:** Check `wiki/signal-inbox.md` — if it's empty after ingest, the ingest skill found nothing new. Check source files in `sources/` to confirm data was written.

**HOT.md not regenerating:** Check that `vault-daily-sync` completed successfully in `log.md`.
