---
name: translate-docs
description: Use this skill to translate product documentation while keeping code blocks, links and front matter untouched.
version: 1.0.3
tags: [translation, docs, i18n]
author: loc-team
---
# Translate Docs

## Steps
1. Split the document into prose and protected spans (code, URLs, front matter).
2. Translate prose only.
3. Re-assemble and check every link still resolves.

```markdown
<!-- protected: code fences, inline code, URLs -->
```
