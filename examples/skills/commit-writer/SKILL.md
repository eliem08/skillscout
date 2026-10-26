---
name: commit-writer
description: Use this skill whenever the user asks for a commit message: it reads the staged diff and writes a Conventional Commits message that matches the repository's history.
version: 2.0.1
tags: [git, commits, writing]
author: devtools
---
# Commit Writer

## When to use
After staging changes, before `git commit`.

## Steps
1. Run `git diff --staged` and `git log -20 --oneline`.
2. Pick the type (feat, fix, chore...) from what changed, not from file names.
3. Keep the subject under 72 characters and explain why in the body.

```bash
git diff --staged --stat
```
