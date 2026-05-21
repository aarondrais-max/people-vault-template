# Setup Guide — Standard (No Code Required)

This guide is for TA and People team professionals using Claude.ai in the browser with Obsidian for notes. No terminal, no CLI, no technical setup required.

---

## Step 1: Get the vault files

**Option A: Download a ZIP**
1. On GitHub, click the green "Code" button → "Download ZIP"
2. Unzip the folder somewhere you'll remember (e.g., `Documents/my-recruiting-vault`)

**Option B: Clone with GitHub Desktop**
If you have GitHub Desktop installed: File → Clone Repository → paste the repo URL.

---

## Step 2: Open in Obsidian

[Obsidian](https://obsidian.md) is a free markdown editor that lets you browse, search, and link your vault files. It's optional but highly recommended.

1. Download and install Obsidian from [obsidian.md](https://obsidian.md) (free)
2. Open Obsidian → "Open folder as vault"
3. Select the folder you downloaded (e.g., `my-recruiting-vault`)
4. You'll see the file tree on the left — your vault is ready to browse

You don't need to use Obsidian for the AI features. It's just a nice way to read and edit the files.

---

## Step 3: Personalize CLAUDE.md

Open `CLAUDE.md` in Obsidian (or any text editor) and replace all placeholders:

| Placeholder | Replace with |
|---|---|
| `[YOUR_NAME]` | Your full name |
| `[YOUR_ROLE]` | Your job title (e.g., Senior Recruiter, EMEA) |
| `[YOUR_ORG]` | Your team name |
| `[YOUR_TIMEZONE]` | Your timezone (e.g., Europe/London, America/Chicago) |
| `[YOUR_SLACK_ID]` | Your Slack member ID (Settings → Profile → copy from URL or "More" menu) |

The Key Relationships table at the bottom of CLAUDE.md is where you list your hiring managers and key stakeholders. Fill in their names and why they matter.

---

## Step 4: Configure vault.yaml

Open `vault.yaml` and fill in your details:

**User identity section:**
```yaml
user:
  name: Your Name
  role: Your Job Title
  timezone: America/New_York  # your timezone
  slack_user_id: UXXXXXXXXXX  # your Slack member ID
```

**Slack channels to monitor:**
```yaml
ingests:
  slack:
    channels:
      - name: recruiting-team       # replace with your actual channels
      - name: hiring-managers
      - name: headcount-planning
```

**DM contacts** (hiring managers and key stakeholders you DM regularly):
```yaml
    dm_contacts:
      - name: Alex Chen
        user_id: UXXXXXXXXXX        # their Slack member ID
        why: hiring manager, EMEA Sales
```

To find a Slack member ID: open Slack → click their profile → "More" → "Copy member ID".

You don't need to change anything else in vault.yaml for the standard setup. Leave `enabled: true/false` as-is.

---

## Step 5: Delete the EXAMPLE files (after reviewing them)

The `wiki/` directories contain example files showing the expected format:
- `wiki/reqs/EXAMPLE-req.md`
- `wiki/candidates/EXAMPLE-candidate.md`
- `wiki/people/EXAMPLE-stakeholder.md`

Read these to understand the format, then delete them (or rename them by removing the `EXAMPLE-` prefix if you want to use them as templates).

---

## Step 6: Use with Claude.ai

The standard approach is to paste skill content into Claude.ai as your opening message.

### Starting a session

1. Open [Claude.ai](https://claude.ai)
2. Open `skills/vault-boot.md` in Obsidian or a text editor
3. Copy the full file contents (everything after the `---` frontmatter block)
4. Paste it as your first message to Claude
5. Claude will read your vault files and report what's urgent

### Updating wiki pages manually

When you want Claude to update a wiki page:
1. Tell Claude what happened: "Jordan Smith withdrew from the Senior AE role. They had a competing offer from Workday."
2. Claude will ask for the relevant files or you can paste the content
3. Claude will draft the updated page or archive entry — review and copy it back to your file

### Getting a morning brief

1. Copy the contents of `skills/daily-brief.md`
2. Paste into Claude.ai
3. Attach your current HOT.md and any pending-signals.md content
4. Claude will generate your brief

---

## Step 7: Building your wiki

**Starting from scratch:** Create your first req page.

1. In Obsidian, right-click `wiki/reqs/` → New Note
2. Name it `R-[your-req-id].md` (use your ATS req ID)
3. Copy the template from CLAUDE.md (the `wiki/reqs/R-XXXXX.md` section)
4. Paste it into the new file
5. Fill in the overview and pipeline table

Repeat for each active req. This is the initial investment — once pages exist, Claude maintains them.

**Adding a candidate:** When a candidate reaches phone screen stage:
1. Create `wiki/candidates/[firstname-lastname].md`
2. Use the Tier 1 template from CLAUDE.md
3. Fill in what you know from the ATS

---

## Tips for getting value without automation

Even without the automated pipeline, you get significant value:

- **Before any candidate conversation:** Ask Claude to read the candidate page and prep suggested questions
- **After a screen:** Paste your notes and ask Claude to update the candidate wiki page
- **Weekly:** Ask Claude to read all your req pages and tell you what's stuck or overdue
- **For referrals:** Ask Claude to read a req page and write 3 bullets describing the ideal referral profile

The vault is most valuable when you treat it as a conversation with Claude, not a form to fill out.

---

## Moving to the Tech setup later

If you later want the automated pipeline, your work here transfers directly. The wiki pages, vault.yaml, and CLAUDE.md you've built are exactly what the tech setup uses. See SETUP-TECH.md when you're ready.
