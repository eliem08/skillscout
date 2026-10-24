---
name: pdf
description: Use this skill whenever the user wants to fill, merge, split or extract text and tables from PDF files, including fillable forms.
version: 1.2.0
tags: [pdf, documents, forms]
---
# PDF

## When to use
Any task that reads or writes a `.pdf`.

## Steps
1. Detect whether the PDF has fillable form fields.
2. Fill fields by name, or overlay text for flat forms.
3. Validate the output opens and fields are populated.

```python
from pypdf import PdfReader
fields = PdfReader("form.pdf").get_fields()
```
