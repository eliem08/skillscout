---
name: invoice-extractor
description: Use this skill to extract vendor, dates, line items, tax and totals from invoice PDFs or images into structured JSON for accounting imports.
version: 1.1.0
tags: [pdf, invoices, accounting, extraction]
author: finops-labs
---
# Invoice Extractor

## When to use
Accounts payable inboxes, expense reports, bookkeeping imports.

## Steps
1. Extract text; fall back to OCR for scanned pages.
2. Locate totals first, then reconcile line items against them.
3. Flag any invoice where line items do not sum to the total.

```json
{"vendor": "Acme", "total": 1250.00, "currency": "USD"}
```
