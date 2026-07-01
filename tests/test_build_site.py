from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_site  # noqa: E402


class BuildSiteTest(unittest.TestCase):
    def test_pages_bundle_includes_challenge2_raw_source_trees(self) -> None:
        self.assertIn("challenge-2/structured_files", build_site.PUBLIC_TREES)
        self.assertIn("challenge-2/unstructured_files", build_site.PUBLIC_TREES)

    def test_pages_bundle_includes_gov_ckan_bundle(self) -> None:
        self.assertIn("gov-ckan", build_site.PUBLIC_TREES)

    def test_pages_bundle_excludes_gov_ckan_scratch_outputs(self) -> None:
        self.assertTrue(build_site.is_forbidden(Path("gov-ckan/raw/package-search.json")))
        self.assertTrue(build_site.is_forbidden(Path("gov-ckan/downloads/resource.csv")))
        self.assertTrue(build_site.is_forbidden(Path("gov-ckan/resource-bodies/body.html")))

    def test_copy_public_tree_skips_ignored_scratch_folders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "gov-ckan"
            target = root / "_site" / "gov-ckan"
            (source / "data").mkdir(parents=True)
            (source / "raw").mkdir()
            (source / "downloads").mkdir()
            (source / "resource-bodies").mkdir()
            (source / "data" / "manifest.json").write_text("{}", encoding="utf-8")
            (source / "raw" / "package-search.json").write_text("{}", encoding="utf-8")
            (source / "downloads" / "resource.csv").write_text("x", encoding="utf-8")
            (source / "resource-bodies" / "body.html").write_text("<p>x</p>", encoding="utf-8")

            build_site.copy_public_tree(source, target)

            self.assertTrue((target / "data" / "manifest.json").exists())
            self.assertFalse((target / "raw" / "package-search.json").exists())
            self.assertFalse((target / "downloads" / "resource.csv").exists())
            self.assertFalse((target / "resource-bodies" / "body.html").exists())


if __name__ == "__main__":
    unittest.main()
