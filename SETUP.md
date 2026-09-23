# Setup

About 30 minutes. A setup wizard does the configuration, so you are not editing config files by hand.

If you prefer a visual version of this guide, open `walkthrough.html` in a browser.

---

## Before you start

You need two things:

| | What | Why |
|---|---|---|
| **Required** | An AI agent that can read and write local files | This is what maintains the vault. Claude Code (in the Claude desktop app, Code tab) is the reference setup. Codex CLI, Cursor, Gemini CLI and others work too, see [PORTABILITY.md](PORTABILITY.md). |
| **Recommended** | [Obsidian](https://obsidian.md) (free) | How you read and browse your wiki. The vault is plain markdown, so any editor works, but Obsidian renders the links between pages. |

Optional, and only for the automated pipeline: connections to the tools you want the vault to read from (Slack, Gmail, calendar, meeting notes, your ATS). You can set these up later. The vault is useful without any of them.

---

## Step 1 — Get the vault

Download this repo as a ZIP (green **Code** button, then **Download ZIP**) and unzip it somewhere permanent.

A good spot: `~/Documents/PeopleVault`

Do not leave it in Downloads. The vault grows over time and you want it somewhere stable.

---

## Step 2 — Open it in Obsidian and your agent

**Obsidian:** open it, choose **Open folder as vault**, pick the folder you just unzipped.

**Your agent:** open the Claude desktop app, click the **Code** tab, start a new session, and select that same folder. (On a different agent, open that folder as your working directory.)

---

## Step 3 — Run the setup wizard

In your agent session, paste this:

```
Please read skills/vault-setup/SKILL.md and run the setup wizard for me.
```

The wizard asks a short set of questions: your role, name, timezone, which tools you have connected, and how you want your brief delivered. It then writes your `AGENTS.md` and `vault.yaml` for you.

**Which role you pick matters.** It selects one of four variants from `roles/` and determines what your vault tracks:

| Role | Tracks |
|---|---|
| `recruiter` | Reqs, candidates, pipeline, hiring managers |
| `hrbp` | Manager relationships, team health, ER cases, people initiatives |
| `comp` | Comp cycles, benchmarks, offers, pay decisions |
| `generic` | Meetings, decisions, projects, commitments (People Ops, L&D, Facilities) |

If you are a recruiter you get extra questions about your ATS, pipeline sheet, and an offer to link the TA Toolkit so its skills read your vault.

---

## Step 4 — Run it

Still in your agent session:

```
Read skills/vault-orchestrator/SKILL.md and run the full pipeline.
```

In Claude Code you can shortcut this to `/vault-orchestrator`.

The agent pulls from your connected tools, builds your wiki pages, and writes your first brief. The first run takes a few minutes because it is reaching back over recent history and building pages from scratch.

**Check it worked.** Open `HOT.md` in Obsidian. That is your live state snapshot: what is pending, who is waiting on you, what moved. If it still shows template placeholder text, check `log.md` for errors.

---

## Your daily rhythm

1. Start a session in the vault folder.
2. `Read skills/vault-boot/SKILL.md` (or `/vault-boot`). This loads your current state in a few seconds.
3. Ask questions in plain English. *"What's stuck?"* *"Who am I waiting on?"* *"What happened with the Singapore role this week?"*
4. After a meeting or a call, paste your notes and ask the agent to update the right page.

The pipeline handles ingest and page updates. You handle questions and decisions.

---

## Optional extras

### Version history

Git gives you a rollback if a pipeline run ever writes something wrong.

```bash
cd ~/Documents/PeopleVault
git init
git add AGENTS.md CLAUDE.md vault.yaml HOT.md pending-signals.md index.md log.md changelog.md scan-intelligence.md wiki/ skills/ roles/ scripts/ .gitignore
git commit -m "vault: initial setup"
```

`sources/` is excluded by `.gitignore` because it holds raw personal data (emails, Slack messages). Keep it local.

Set `git.snapshot: true` in `vault.yaml` to have the pipeline commit after each run. Commits stay local unless you deliberately push.

### Run it automatically each morning

Ask your agent:

```
Help me schedule the vault pipeline to run each morning.
```

It will set up a scheduled task or a cron entry for you. Do this only after you have run the pipeline manually a few times and are happy with the output.

---

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| **"Tool not found"** | The connection for that source is not set up. Check which tools your agent has connected, or set `enabled: false` for that source in `vault.yaml`. |
| **Ingest returns nothing** | Either the connection is not working, or there genuinely was no activity in the lookback window. Check `sources/` for files with today's date. |
| **Pipeline runs but wiki pages do not change** | Look at `wiki/signal-inbox.md`. If it is empty after ingest, the ingest found nothing to act on. If it has entries that are not clearing, `vault-daily-sync` is failing. Check `log.md`. |
| **`HOT.md` is not regenerating** | `vault-daily-sync` did not finish. `log.md` will say why. |
| **Everything is slow or expensive** | Set `mode.light: true` in `vault.yaml` to skip ingests and only re-sync the wiki from sources you already have. |

Before sharing or after editing the template itself, run `python3 scripts/check_template.py` to confirm nothing is broken.

---

## Moving to a different agent

The vault is deliberately not tied to Claude. See [PORTABILITY.md](PORTABILITY.md) for what transfers (all of your data, config, and instructions) and what needs re-checking (tool connections).
