<div align="center">

# 🧠 Biomedical AI Conference & Deadline Tracker

### Never miss a MICCAI, ISBI, MIDL, or SPIE deadline again.

A self-updating dashboard that tracks submission deadlines for **medical imaging, healthcare, and biomedical AI** conferences — with live countdowns, smart alerts, and automatic broken-link detection. Zero servers, zero maintenance, 100% free.

[**🚀 View the live dashboard →**](https://akshatha-mohan.github.io/biomedical-ai-conference-tracker/)

[![Daily auto-update](https://github.com/Akshatha-Mohan/biomedical-ai-conference-tracker/actions/workflows/update.yml/badge.svg)](https://github.com/Akshatha-Mohan/biomedical-ai-conference-tracker/actions/workflows/update.yml)
[![GitHub Pages](https://img.shields.io/badge/dashboard-live-success?logo=github)](https://akshatha-mohan.github.io/biomedical-ai-conference-tracker/)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#-contribute-a-conference)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Akshatha-Mohan/biomedical-ai-conference-tracker?style=social)](https://github.com/Akshatha-Mohan/biomedical-ai-conference-tracker/stargazers)

⭐ **If this saves you from a missed deadline, please [star the repo](https://github.com/Akshatha-Mohan/biomedical-ai-conference-tracker) — it helps other researchers find it.**

</div>

---

## Why this exists

If you do research in medical imaging or health AI, your deadlines are scattered across a dozen conference sites that redesign their URLs every year. Generic deadline trackers bury MICCAI under hundreds of NLP and robotics venues, and the links rot the moment a new edition goes live.

This is a focused, **biomedical-only** tracker that you own. It lives in a GitHub repo, deploys itself to GitHub Pages, and refreshes every single day — so the countdowns are always right and dead links get flagged automatically instead of surprising you the week before a deadline.

## ✨ Features

- **🗓️ Live countdowns & status** — every venue shows exact days-left and an at-a-glance status: `Upcoming`, `Far Out`, `TBD`, or `Past Due`, color-coded like a traffic light.
- **🔔 Deadline alerts** — built-in 7-day and 14-day alert windows surface what's urgent right now.
- **🔗 Automatic broken-link detection** — every official URL is tested daily; dead links get a ⚠ badge and a count on the dashboard, so the data never silently rots.
- **🔍 New-venue discovery** — a daily best-effort scan of community deadline datasets surfaces biomedical conferences you're not tracking yet, in a separate "review & add" panel.
- **🎯 Confidence flags** — each deadline is tagged `confirmed`, `estimated`, or `tbd`, so you always know what to double-check before relying on it.
- **🔎 Search, sort & filter** — find any venue instantly; sort by deadline, track, or status; hide past-due events with one click.
- **⚙️ Truly zero-maintenance** — GitHub Actions + GitHub Pages do everything. No server, no database, no cost.
- **📝 One file to rule them all** — add or edit a conference by changing a single human-readable YAML file.

## 📸 Dashboard

> Summary cards on top (next deadline, alerts, broken links) and a sortable, filterable, color-coded table below.

<!-- Tip: take a screenshot of your live dashboard, drag it into this section on GitHub, and it'll embed automatically. A screenshot dramatically increases stars. -->

[**→ Open the live dashboard**](https://akshatha-mohan.github.io/biomedical-ai-conference-tracker/)

## 🏛️ Conferences tracked

Medical imaging & biomedical AI venues including **MICCAI · ISBI · IPMI · MIDL · SPIE Medical Imaging · SASHIMI · AAPM · RSNA · EMBC · MLHC · ML4H**, plus the major general ML/CV conferences with growing medical tracks (**NeurIPS · ICML · ICLR · CVPR · ICCV · ECCV · WACV**).

Missing your favorite? [**Add it in 2 minutes →**](#-contribute-a-conference)

## 🚀 Use it yourself (fork in 5 minutes)

Want your own copy? You'll have a live, self-updating dashboard in a few clicks:

1. **[Fork this repo](https://github.com/Akshatha-Mohan/biomedical-ai-conference-tracker/fork)** (or use it as a template).
2. In your fork: **Settings → Actions → General → Workflow permissions → Read and write permissions**.
3. **Settings → Pages → Source → GitHub Actions**.
4. **Actions tab → "Update dashboard