# Miscellaneous

## Git Commands

### Make Git Repo

```bash
cd path\to\your\project
git init
```

### Create a `.gitignore` file

In the root to avoid pushing unnecessary files:

```gitignore
__pycache__/
*.pyc
*.pyo
*.idea/
.env
```

### Initial Commit

```bash
git add .
git commit -m "Initial commit"
```

### Push to GitHub

1. Go to GitHub → click **New Repository**.
2. Enter repo name (e.g., `my-python-project`).
3. Choose **Private**.
4. Don’t tick “Initialize with README” (we already have files locally).
5. Click **Create Repository**.

GitHub will now show you commands like:

```bash
git remote add origin https://github.com/username/my-python-project.git
git branch -M main
git push -u origin main
```

### Example:

```bash
git remote add origin https://github.com/USERNAME/my-python-project.git
git branch -M main
git push -u origin main
```

### Remove Already-Tracked Files from Git (but keep locally)

```bash
git rm -r --cached data/
git rm -r --cached .idea

git commit -m "Removed data folder from Git tracking and added to .gitignore"
git push
```
