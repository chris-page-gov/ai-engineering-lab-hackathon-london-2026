from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_gov_ckan_bundle as builder  # noqa: E402
import check_gov_ckan_bundle as checker  # noqa: E402


def fixture_package() -> dict[str, Any]:
    return {
        "id": "pkg-1",
        "name": "planning-applications-2026",
        "title": "Planning applications 2026",
        "notes": "Metadata about planning applications.",
        "url": "https://www.gov.uk/government/collections/planning-data",
        "isopen": True,
        "license_id": "uk-ogl",
        "license_title": "UK Open Government Licence",
        "metadata_created": "2026-01-01T00:00:00",
        "metadata_modified": "2026-06-30T12:00:00",
        "organization": {
            "id": "org-1",
            "name": "department-for-levelling-up-housing-and-communities",
            "title": "Department for Levelling Up, Housing and Communities",
            "description": "Publisher description.",
            "state": "active",
        },
        "tags": [{"name": "planning"}, {"display_name": "housing"}],
        "groups": [{"name": "government"}],
        "extras": [{"key": "dcat_modified", "value": "2026-06-30"}],
        "resources": [
            {
                "id": "res-1",
                "name": "CSV extract",
                "url": "https://www.gov.uk/government/statistical-data-sets/planning-applications",
                "format": "CSV",
                "resource_type": "data",
                "position": 0,
                "last_modified": "2026-06-30",
            }
        ],
    }


class GovCkanBundleTest(unittest.TestCase):
    def test_extras_to_dict_compacts_ckan_extras(self) -> None:
        extras = builder.extras_to_dict(
            [
                {"key": "theme-primary", "value": "Planning"},
                {"key": "", "value": "ignored"},
                {"value": "missing key"},
            ]
        )
        self.assertEqual(extras, {"theme-primary": "Planning"})

    def test_govuk_content_path_detection_is_exact(self) -> None:
        self.assertEqual(
            builder.govuk_content_path_for_url("https://www.gov.uk/government/collections/planning-data"),
            "government/collections/planning-data",
        )
        self.assertIsNone(builder.govuk_content_path_for_url("https://assets.publishing.service.gov.uk/file.csv"))
        self.assertIsNone(builder.govuk_content_path_for_url("https://example.com/government/collections/planning-data"))

    def test_normalize_dataset_keeps_metadata_and_routes(self) -> None:
        dataset, resources, publisher = builder.normalize_dataset(fixture_package(), "https://example.test/api/action")
        self.assertEqual(dataset["name"], "planning-applications-2026")
        self.assertEqual(dataset["publisher"], "department-for-levelling-up-housing-and-communities")
        self.assertEqual(dataset["formats"], ["CSV"])
        self.assertEqual(dataset["source_api_url"], "https://example.test/api/action/package_show?id=planning-applications-2026")
        self.assertEqual(resources[0]["govuk_content_path"], "government/statistical-data-sets/planning-applications")
        self.assertEqual(publisher["dataset_count"], 0)

    def test_content_api_status_classification(self) -> None:
        ok_body = json.dumps(
            {
                "content_id": "content-1",
                "base_path": "/government/collections/planning-data",
                "title": "Planning data",
                "description": "Collection description.",
                "document_type": "collection",
                "schema_name": "collection",
                "links": {"organisations": []},
            }
        )
        ok = builder.classify_content_api_result(200, {}, ok_body, "government/collections/planning-data")
        self.assertEqual(ok["status"], 200)
        self.assertEqual(ok["web_url"], "https://www.gov.uk/government/collections/planning-data")
        self.assertEqual(ok["link_types"], ["organisations"])
        self.assertEqual(
            builder.classify_content_api_result(303, {"location": "/new"}, "", "old"),
            {"path": "old", "status": 303, "redirect": "/new"},
        )
        self.assertEqual(builder.classify_content_api_result(404, {}, "", "missing"), {"path": "missing", "status": 404})
        self.assertEqual(builder.classify_content_api_result(410, {}, "", "gone"), {"path": "gone", "status": 410})

    def test_static_viewer_declares_ui_contract(self) -> None:
        html = builder.render_viewer()
        self.assertIn("#overview", html)
        self.assertIn("Publisher x Format", html)
        self.assertIn("aria-live", html)
        self.assertIn("setSpotlight", html)
        self.assertIn("ontouchstart", html)
        self.assertIn("localStorage", html)
        self.assertIn('params.get("mode")', html)
        self.assertIn('params.getAll("pin")', html)
        self.assertIn("avoids opening on a full hairball", html)

    def test_fixture_build_and_checker_validate_bundle(self) -> None:
        original_iter_packages = builder.iter_packages
        original_fetch_govuk_content = builder.fetch_govuk_content
        try:
            builder.iter_packages = lambda config: ([fixture_package()], 58461)  # type: ignore[assignment]
            builder.fetch_govuk_content = lambda path: {  # type: ignore[assignment]
                "path": path,
                "status": 200,
                "content_id": "content-1",
                "base_path": f"/{path}",
                "title": "Planning data",
                "description": "Collection description.",
                "document_type": "collection",
                "schema_name": "collection",
                "web_url": f"https://www.gov.uk/{path}",
                "link_types": [],
            }
            with tempfile.TemporaryDirectory() as tmp:
                out_dir = Path(tmp) / "gov-ckan"
                manifest = builder.build_bundle(
                    builder.HarvestConfig(sample=1, chunk_size=1, generated_at="2026-07-01T00:00:00Z"),
                    out_dir,
                )
                self.assertEqual(manifest["counts"]["datasets"], 1)
                self.assertEqual(manifest["source"]["ckan_reported_count"], 58461)
                self.assertEqual(checker.main([str(out_dir)]), 0)
        finally:
            builder.iter_packages = original_iter_packages  # type: ignore[assignment]
            builder.fetch_govuk_content = original_fetch_govuk_content  # type: ignore[assignment]


if __name__ == "__main__":
    unittest.main()
