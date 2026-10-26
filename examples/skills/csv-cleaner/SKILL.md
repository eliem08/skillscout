---
name: csv-cleaner
description: Use this skill when the user wants to clean, dedupe or normalise a CSV or spreadsheet export before analysis or import.
version: 1.4.0
tags: [csv, data, cleaning]
author: data-team
---
# Csv Cleaner

## When to use
Messy exports from CRMs, billing tools or forms.

## Steps
1. Detect the delimiter and encoding.
2. Trim whitespace, normalise dates to ISO 8601 and phone numbers to E.164.
3. Drop exact duplicates and report near-duplicates for review.

```python
import csv
rows = list(csv.DictReader(open('in.csv', newline='')))
```
