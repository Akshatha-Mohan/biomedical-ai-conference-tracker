# Biomedical AI — Conference & Deadline Tracker

A self-updating dashboard for biomedical AI / medical imaging conferences and
workshops. It recomputes deadline countdowns every day, flags broken links, and
surfaces newly discovered venues for you to review — all hosted free on GitHub
Pages, no server to run.

![status: card + table dashboard](https://img.shields.io/badge/dashboard-GitHub%20Pages-blue)

## How it works

```
data/conferences.yml      ← the one file you edit (the source of truth)
        │
        ▼
scripts/update.py         ← recomputes days-left / status / -7,-14 alerts, checks every link
scripts/discover.py       ← best-effort scan for new biomedical venues (non-authoritative)
        │
        ▼
site/data.json            ← generated; the dashboard reads this
site/index.html           ← the dashboard (summary cards + sortable/filterable table)
        │
        ▼
.github/workflows/update.yml  ← runs daily at 06:00 UTC, commits data.json, deploys Pages
```

There is no live conference API, so the design is deliberately honest:

- **Countdowns and status are fully reliable** — recomputed from the dates in
  `conferences.yml` every day.
- **Link health is reliable** — every official URL is tested daily; broken ones
  show a ⚠ badge and appear in the "Broken links" card. This is the fix for the
  stale-link problem.
- **Auto-discovery is best-effort.** It reads the community-maintained
  `ai-deadlines` dataset and lists biomedical matches you don't already track,
  in a separate "Discovered — review" panel. Nothing is added automatically;
  you copy across the ones you want. Treat it as a prompt, not a source of truth.

Each deadline carries a `deadline_confidence` flag — `confirmed` (from the
official site), `estimated` (inferred from the venue's historical pattern, so
verify), or `tbd` (not yet announced).

## One-time setup

You need [Git](https://git-scm.com/) and a GitHub account. The
[`gh` CLI](https://cli.github.com/) makes this two commands; manual steps follow
if you prefer the website.

### Option A — with the `gh` CLI (fastest)

```bash
cd biomedical-ai-conference-tracker
git init && git add . && git commit -m "Initial commit: biomedical AI conference tracker"

# Creates the repo under your account and pushes in one go:
gh repo create biomedical-ai-conference-tracker --public --source=. --push

# Turn on Pages (served by GitHub Actions):
gh api -X POST repos/:owner/biomedical-ai-conference-tracker/pages \
  -f build_type=workflow
```

### Option B — manual

1. Create a new **empty** public repo on github.com named
   `biomedical-ai-conference-tracker` (no README/license — this folder has them).
2. Push this folder:

   ```bash
   cd biomedical-ai-conference-tracker
   git init && git add . && git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/<your-username>/biomedical-ai-conference-tracker.git
   git push -u origin main
   ```

3. In the repo: **Settings → Pages → Build and deployment → Source = GitHub Actions**.

### Then

- Go to the **Actions** tab and run **"Update dashboard"** once (the
  `workflow_dispatch` button) to generate the first `data.json` and deploy.
- Your dashboard will be live at
  `https://<your-username>.github.io/biomedical-ai-conference-tracker/`.

After that it refreshes itself every day at 06:00 UTC. Change the time by editing
the `cron` line in `.github/workflows/update.yml`.

## Day-to-day use

- **Add or fix a conference:** edit `data/conferences.yml`, commit, push. The
  push triggers a rebuild; the dashboard updates within a minute.
- **Fix a broken link:** the dashboard's "Broken links" card names the offenders;
  update their `url` in the YAML.
- **Add a discovered venue:** copy the entry from the "Discovered" panel into
  `conferences.yml`, fill in the fields, commit.

## Run it locally (optional)

```bash
pip install -r requirements.txt
python scripts/update.py        # writes site/data.json
python scripts/discover.py      # writes site/discovered.json (needs internet)
python -m http.server -d site   # open http://localhost:8000
```

## Data notes

Conference data was verified June 2026. Editions in 2027 are frequently
unannounced at that point, so their deadlines are marked `estimated` or `tbd` —
confirm against the official call for papers before relying on them. The daily
link check will tell you when a `tbd` venue's site goes live.
