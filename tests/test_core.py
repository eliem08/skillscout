import os
import tempfile
import unittest

from skill_g2 import Catalog, index_dir

GOOD = """---
name: pdf
description: Use this skill whenever the user wants to fill, merge, split or extract text from PDF files, including forms.
version: 1.2.0
tags: [pdf, documents, forms]
---
# PDF

## Steps
1. Detect form fields
2. Fill them

```python
fill(form)
```
"""
WEAK = """---
name: notes
description: notes stuff
---
TODO
"""
NODESC = "# no frontmatter here"


class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        for name, content in [("pdf", GOOD), ("notes", WEAK), ("broken", NODESC)]:
            d = os.path.join(self.tmp.name, name)
            os.makedirs(d)
            with open(os.path.join(d, "SKILL.md"), "w") as fh:
                fh.write(content)
        os.makedirs(os.path.join(self.tmp.name, "pdf", "scripts"))
        self.skills = index_dir(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_index_and_parse(self):
        names = {s.name: s for s in self.skills}
        self.assertEqual(set(names), {"pdf", "notes"})
        self.assertEqual(names["pdf"].tags, ["pdf", "documents", "forms"])
        self.assertTrue(names["pdf"].has_scripts)

    def test_quality_ordering(self):
        q = {s.name: s.quality for s in self.skills}
        self.assertGreater(q["pdf"], 70)
        self.assertLess(q["notes"], 20)

    def test_search_rate_compare_roundtrip(self):
        cat = Catalog(self.skills)
        self.assertEqual(cat.search("fill pdf forms")[0][0], "pdf")
        self.assertEqual(cat.search("kubernetes"), [])
        cat.rate("pdf", "alice", 5)
        cat.rate("pdf", "alice", 4)  # one rating per user
        self.assertEqual(len(cat.skills["pdf"].ratings), 1)
        with self.assertRaises(ValueError):
            cat.rate("pdf", "bob", 9)
        path = os.path.join(self.tmp.name, "cat.json")
        cat.save(path)
        rows = Catalog.load(path).compare(["pdf", "notes"])
        self.assertEqual(rows[0]["reviews"], 1)


if __name__ == "__main__":
    unittest.main()
