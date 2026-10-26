---
name: sql-reviewer
description: Use this skill when the user wants a SQL query or migration reviewed for correctness, injection risk, missing indexes and locking problems before it runs in production.
version: 0.9.0
tags: [sql, database, review]
author: db-guild
---
# Sql Reviewer

## When to use
Before merging a migration or running an ad-hoc query on production data.

## Checks
- Unbounded UPDATE or DELETE without WHERE
- String-built queries (injection)
- Full-table locks on large tables
- Missing index for new foreign keys

## Steps
1. Parse the statement.
2. Run each check and explain the fix.
