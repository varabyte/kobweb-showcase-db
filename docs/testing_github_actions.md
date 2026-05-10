# Testing GitHub Actions (Database Automation)

This repo uses GitHub Actions triggered by issue comments (`issue_comment`).
Testing changes off the `main` branch normally won't work.

Ways to test:
- Use CLI tools like `nektos/act` (runs actions locally in Docker).
- Change workflow files to target a test branch instead of `main`.
- Clone to a separate dummy repo to test safely.
- Create a public fork (our chosen method).

Here is how to test using a fork:

### 1. Create a Public Fork
Click "Fork" (top right). Ensure "Copy the main branch only" is checked.

### 2. Enable Issues
GitHub hides the Issues tab on forks by default.
- Go to fork **Settings** -> **General**.
- Scroll to **Features**.
- Check the **Issues** box.

### 3. Enable Workflows
GitHub pauses Actions on new forks for security.
- Go to the **Actions** tab.
- Click **"I understand my workflows, go ahead and enable them."**

### 4. Test
1. Go to the **Issues** tab.
2. Open a dummy issue.
3. Comment `/check`, `/approve`, or `/revoke`.
4. Watch the **Actions** tab to verify execution and DB updates.

### 5. Keep History Clean
- Use local Git to squash or remove commits created by the GitHub Action bot during testing before opening a Pull Request.