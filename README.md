# IssueOps JSON Database Template
> **A fully GitHub-hosted, CRUD-compatible JSON database.**
> *Created by [Tim Korelov (@lifestreamy)](https://github.com/lifestreamy)*

A completely free, generalized template that leverages GitHub Actions and IssueOps to manage a serverless JSON data collection.

This repository is designed to be used as a **GitHub Template**. Generate your own repository from this one to instantly set up a backend for portfolios, showcases, link trees, and directory sites.

---

## Table of Contents
- [Work in Progress (WIP) Disclaimer](#work-in-progress-wip-disclaimer)
- [Features](#features)
- [Consuming the Database](#consuming-the-database)
- [Repository Structure](#repository-structure)
- [How to Use & Tailoring Guide](#how-to-use--tailoring-guide)

---

> ### Work in Progress (WIP) Disclaimer
> **This template is currently in its V1 state.**
> While fully functional, it requires manual editing of several files to tailor it to your specific data schema. In the future, this repository will feature an automated workflow driven by a single `schema.yml` file, along with automated data-migration tools. For now, please follow the "Tailoring Guide" below to adapt this database for your needs.

---

## Features
* **Serverless CRUD:** Submit, approve, and revoke entries directly through GitHub Issues.
* **JSON Data Store:** Submissions are automatically parsed and saved into a clean `data.json` file.
* **GitHub CDN Integration:** Image URLs are validated and securely hosted via GitHub's native issue attachment CDN.
* **Concurrency Safe:** Built-in lock mechanisms prevent race conditions when multiple entries are processed simultaneously.

---

## Consuming the Database
Because the database is hosted natively on GitHub, you do not need a traditional backend API to read the data. You can fetch the JSON array directly into your frontend (e.g., React, Vue, or Kobweb applications) using GitHub's Raw Content URL.

To get the URL for your database:
1. Navigate to `resources/db/data.json` in your repository.
2. Click the **"Raw"** button in the top right corner of the file viewer.
3. Copy the URL from your browser. It will look like this:
   `https://raw.githubusercontent.com/[YOUR_USERNAME]/[REPO_NAME]/main/resources/db/data.json`

You can now use a simple HTTP GET request (`fetch()`) to pull this JSON into your frontend application! *(Note: Your repository must be Public for this URL to be accessible without authentication headers).*

---

## Repository Structure

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── submit-entry.yml    # The frontend form users fill out to submit data
│   ├── scripts/
│   │   ├── approve_entry.py    # Parses the issue body and adds it to the JSON db
│   │   ├── common.py           # Shared helper functions (JSON loading/saving, errors)
│   │   ├── config.py           # Single source of truth for paths, CDN rules, and messages
│   │   └── revoke_entry.py     # Removes an entry from the JSON db by Issue Number
│   └── workflows/
│       ├── approve.yml         # Triggers on '/approve' issue comment
│       └── revoke.yml          # Triggers on '/revoke' issue comment
├── resources/
│   └── db/
│       └── data.json           # The actual database (starts as an empty array `[]`)
├── LICENSE
├── NOTICE
└── README.md
```

---

## How to Use & Tailoring Guide
To start using this database, you must generate a copy and tailor the python parsing logic to match the fields you want to collect.

**1. Generate the Repository**
Click **Use this template** -> **Create a new repository** at the top of this page.

**2. Define your Schema (The Issue Form)**
Open `.github/ISSUE_TEMPLATE/submit-entry.yml`. This YAML file defines the fields users will fill out. You can add or remove fields (e.g., changing `entry-url` to `github-link`). **Take note of the `id` you assign to each field.**

**3. Update the Python Logic**
Open `.github/scripts/approve_entry.py`. You must map the `id` fields from your YAML file to your desired JSON keys.
* Find the section where data is extracted: `get_text(parsed_data, 'entry-url')`. Change `'entry-url'` to match the new `id` from your YAML file.
* Find the `new_entry = { ... }` dictionary definition. Add, remove, or rename the JSON keys to match your desired database structure.

**4. Update Configuration (Optional)**
Open `.github/scripts/config.py`. Here you can customize the success/error messages the GitHub Action bot will comment on the issue, or change the `DB_FILE_PATH` if you prefer to store your JSON file elsewhere.

**5. Start Collecting Data**
* Users submit new entries by filling out the **Submit New Entry** issue form.
* Maintainers review the issue and reply with an `/approve` or `/revoke` comment.
* GitHub Actions automatically process the command, commit the changes, and update the `data.json` database.

*(Note: Future versions of this template will automate Steps 2 and 3 by generating the form and python mappings from a single config file!)*