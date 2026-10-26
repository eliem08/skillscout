import contextlib
import io
import os
import tempfile
import unittest

from skillscout.__main__ import main
from skillscout.core import Catalog


class SeedCatalogTests(unittest.TestCase):
    def test_bundled_catalog_has_safe_and_flagged_skills_without_local_paths(self):
        cat = Catalog.seed()
        self.assertGreaterEqual(len(cat.skills), 12)
        flagged = {n for n, s in cat.skills.items() if s.risks}
        self.assertEqual(flagged, {"quick-installer", "helpful-assistant-plus"})
        self.assertTrue(all(s.path.startswith("seed/") for s in cat.skills.values()))

    def test_safe_skill_outranks_risky_one_on_the_same_words(self):
        cat = Catalog.seed()
        cat.skills["csv-cleaner"].description += " install"
        ranked = [n for n, _ in cat.search("install")]
        self.assertLess(ranked.index("csv-cleaner"), ranked.index("quick-installer"))

    def test_compare_shows_risks(self):
        rows = Catalog.seed().compare(["csv-cleaner", "quick-installer"])
        self.assertEqual(rows[0]["risks"], "none found")
        self.assertIn("pipe_to_shell", rows[1]["risks"])

    def test_cli_works_before_any_index_and_rating_saves_the_catalog(self):
        with tempfile.TemporaryDirectory() as t:
            path = os.path.join(t, "skills.json")
            out = io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(["search", path, "clean csv"]), 0)
                self.assertEqual(main(["rate", path, "csv-cleaner", "5", "--user", "dana"]), 0)
            self.assertIn("csv-cleaner", out.getvalue())
            self.assertEqual(len(Catalog.load(path).skills["csv-cleaner"].ratings), 1)


if __name__ == "__main__":
    unittest.main()
