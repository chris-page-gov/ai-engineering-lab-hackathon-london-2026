from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_site  # noqa: E402


class BuildSiteTest(unittest.TestCase):
    def test_pages_bundle_includes_challenge2_raw_source_trees(self) -> None:
        self.assertIn("challenge-2/structured_files", build_site.PUBLIC_TREES)
        self.assertIn("challenge-2/unstructured_files", build_site.PUBLIC_TREES)


if __name__ == "__main__":
    unittest.main()
