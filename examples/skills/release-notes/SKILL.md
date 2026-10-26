---
name: release-notes
description: Use this skill when preparing a release: it groups merged pull requests since the last tag into user-facing release notes.
version: 1.3.2
tags: [releases, changelog, git]
author: devtools
---
# Release Notes

## When to use
Cutting a tagged release.

## Steps
1. Find the previous tag with `git describe --tags --abbrev=0`.
2. Group merged PRs into Added, Fixed and Changed.
3. Rewrite titles for customers, not engineers.

```bash
git log $(git describe --tags --abbrev=0)..HEAD --merges --oneline
```
