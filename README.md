# Kobweb Showcase Database
> **A fully GitHub-hosted CRUD-compatible JSON database powering the official Kobweb Showcase.**
> *Tailored from the [IssueOps JSON Database Template](https://github.com/lifestreamy/issueops-json-db-template) made by Tim Korelov.*
>
> 💡 **Build your own:** You can use the original template linked above to instantly set up a completely free,
>  serverless backend for your own portfolios, directory sites, or collections!

A serverless JSON database that leverages GitHub Actions and IssueOps to manage website submissions for the Kobweb Showcase frontend.

---

## Table of Contents
- [How to Submit Your Website](#how-to-submit-your-website)
- [The User Submission Pipeline](#the-user-submission-pipeline)
- [Showcase Management Commands](#showcase-management-commands)
- [Image Parsing & Validation](#image-parsing--validation)
- [Directory Structure](#directory-structure)

---

## How to Submit Your Website

If you are a developer looking to get your Kobweb project featured on the official showcase, you are in the right place!

1. Navigate to the **Issues** tab at the top of this repository.
2. Click the green **New issue** button.
3. Click the "Submit a Kobweb Project" option.
4. Fill out the required fields (Name, Live URL, Screenshot, Description, and Site Type).
5. Click **Submit new issue**.

*(A maintainer will review your submission shortly. Once approved, the automated bot will instantly add it to the database!)*

> <img width="1981" height="440" alt="image" src="https://github.com/user-attachments/assets/aab20763-65f9-4e38-b8eb-532422d6fbdb" />


---

## The User Submission Pipeline

Instead of hosting a custom web form and external database, this repository relies entirely on **user-created GitHub Issues** for data entry.
When a developer wants to submit a website to the showcase, they simply fill out the repository's structured Issue Form.

`resources/db/showcased-sites.json` acts as the persistent database storing these user submissions.
It is not modified manually, but rather through automated workflows triggered by maintainer comments on the user's issue.

---

## Showcase Management Commands

Maintainers review submissions and use specific commands to trigger database updates.
Execution is strictly limited to users with **OWNER**, **COLLABORATOR**, or **MEMBER** roles.

> **Note on Workflow Concurrency:** The `/approve` and `/revoke` workflows are concurrency-locked at the job-level. This ensures safe sequential execution, preventing `git push` race conditions when multiple issues are managed simultaneously. `/check` runs asynchronously.

<details>
<summary><b><code>/check</code> (Dry Run & Validation)</b></summary>

Parses the issue form and dry-runs validation logic without touching the database. Outputs the resulting JSON for visual inspection.

| Outcome | Bot Response |
| :--- | :--- |
| **Passed** | ✅ Validation Passed! The form is correctly filled... |
| **Failed** | ❌ Check Failed. Please fix the following issues: [List] |
</details>

<details>
<summary><b><code>/approve</code> (Database Mutation)</b></summary>

Parses the form, validates all fields, and commits the data to the JSON file.

| Outcome | Bot Response |
| :--- | :--- |
| **Added** | ✅ The site has been approved and added to the showcase. |
| **Updated** | ✅ The site has been successfully updated in the showcase. |
| **Unchanged** | ✅ Nothing has changed since the last submission... |
| **Failed** | ❌ Approval Failed. Please fix the following issues: [List] |
</details>

<details>
<summary><b><code>/revoke</code> (Database Deletion)</b></summary>

Locates the dictionary matching the current issue ID and removes it from the JSON file.

| Outcome | Bot Response |
| :--- | :--- |
| **Revoked** | ✅ The site has been successfully revoked and removed... |
| **Not Found** | ✅ There is no submission to revoke for this issue. |
</details>

---

## Image Parsing & Validation

The automation script extracts the primary image directly from the raw markdown body by searching for the auto-generated `src=` HTML attribute wrapping the image link.
For security and performance, image URLs are strictly validated against a whitelist of approved GitHub CDN prefixes (e.g., `https://github.com/user-attachments/assets/`).

---

## Directory Structure

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── submit-entry.yml    # The frontend form users fill out to submit their site
│   ├── scripts/
│   │   ├── approve_entry.py    # Mutates the JSON database (Appends/Updates)
│   │   ├── check_entry.py      # Dry-runs validation and outputs the parsed dictionary
│   │   ├── common.py           # Shared helper functions (JSON loading/saving, errors)
│   │   ├── config.py           # Enums, CDN rules, messages, and UI-to-DB string mapping
│   │   ├── revoke_entry.py     # Removes an entry from the JSON db by Issue Number
│   │   └── validator.py        # Pure function that parses form data and batches errors
│   └── workflows/
│       ├── approve.yml         # Triggers on `/approve` issue comment
│       ├── check.yml           # Triggers on `/check` issue comment
│       └── revoke.yml          # Triggers on `/revoke` issue comment
├── docs/
│   └── testing_github_actions.md # Guide on safely testing workflows using a public fork
├── resources/
│   └── db/
│       └── showcased-sites.json  # The database! Stores all approved Kobweb submissions
└── README.md
```
