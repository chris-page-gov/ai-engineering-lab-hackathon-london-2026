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
import check_gov_ckan_performance as performance_checker  # noqa: E402


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

    def test_malformed_ckan_resource_url_does_not_abort_normalisation(self) -> None:
        malformed = "[wpdm_package id='15516']"
        self.assertEqual(builder.host_for_url(malformed), "")
        self.assertIsNone(builder.govuk_content_path_for_url(malformed))
        resource = builder.normalize_resource({"id": "bad-url", "url": malformed}, "dataset-name")
        self.assertEqual(resource["url"], malformed)
        self.assertEqual(resource["host"], "")
        self.assertEqual(resource["govuk_content_path"], "")

    def test_local_file_uri_is_scrubbed_from_ckan_metadata(self) -> None:
        text = 'See <a href="file:///C:/Users/name/AppData/Local/file.docx">draft</a>'
        self.assertNotIn("/Users/", builder.compact_text(text))
        self.assertIn("[local file path removed]", builder.compact_text(text))

    def test_duplicate_dataset_names_get_unique_routes(self) -> None:
        first = {"id": "id-1", "name": "duplicate-name", "source_api_url": "old"}
        second = {"id": "id-2", "name": "duplicate-name", "source_api_url": "old"}
        resources = [{"dataset": "duplicate-name"}]
        used: set[str] = set()
        builder.ensure_unique_dataset_route(first, [], used, "https://example.test/api/action")
        builder.ensure_unique_dataset_route(second, resources, used, "https://example.test/api/action")
        self.assertEqual(first["name"], "duplicate-name")
        self.assertEqual(second["ckan_name"], "duplicate-name")
        self.assertEqual(second["name"], "duplicate-name-id-2")
        self.assertEqual(resources[0]["dataset"], "duplicate-name-id-2")
        self.assertEqual(second["source_api_url"], "https://example.test/api/action/package_show?id=id-2")

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
        self.assertIn("function formatList", html)
        self.assertIn("function cleanText", html)
        self.assertIn("function loadChunks", html)
        self.assertIn("overviewData=await loadJson(manifest.indexes.overview", html)
        self.assertIn("function needsFullIndexFromLocation", html)
        self.assertIn("async function loadFullIndex", html)
        self.assertIn("Overview payload only", html)
        self.assertIn("renderFacetPreviews", html)
        self.assertIn("const CHUNK_BATCH_SIZE=4,JSON_RETRIES=4", html)
        self.assertIn("function isRetryableLoadError", html)
        self.assertIn("retry=${Date.now()}-${attempt}", html)
        self.assertIn("function requestRelationships", html)
        self.assertIn("relationshipsLoaded=false", html)
        self.assertIn("Loading graph relationships", html)
        self.assertNotIn("relationships=await loadChunks(manifest.chunks.relationships)", html)
        self.assertIn("function applyFacet", html)
        self.assertIn("e.ctrlKey||e.metaKey", html)
        self.assertIn('"publisher_state"', html)
        self.assertIn("function selectionMatchesVisible", html)
        self.assertIn("inspected=null", html)
        self.assertIn("function inspectId", html)
        self.assertIn("function inspectConcept", html)
        self.assertIn("function graphNodeDblAction", html)
        self.assertIn("function bindDetailActions", html)
        self.assertIn("function clearInspection", html)
        self.assertIn("Back to selected card", html)
        self.assertIn("function renderTimeline", html)
        self.assertIn("function renderResourceStack", html)
        self.assertIn("data-overview-facet", html)
        self.assertIn("function loadApiJson", html)
        self.assertIn("function localPackageJson", html)
        self.assertIn("Showing static bundle JSON", html)
        self.assertIn("Live package_show JSON could not be fetched", html)
        self.assertIn("Local normalized dataset JSON", html)
        self.assertIn("function markdownToHtml", html)
        self.assertIn("function openMarkdownDoc", html)
        self.assertIn("notesButton", html)
        self.assertIn("function setTheme", html)
        self.assertIn("themeToggle", html)
        self.assertIn("function toggleBothPanels", html)
        self.assertIn("leftPanelToggle", html)
        self.assertIn("rightPanelToggle", html)
        self.assertIn("leftFolded", html)
        self.assertIn("rightFolded", html)
        self.assertIn("ondblclick", html)
        self.assertIn('class="navGroup" aria-label="Navigation"', html)
        self.assertIn('class="modeGroup" aria-label="Canvas views"', html)
        self.assertIn('let byDataset=new Map()', html)
        self.assertIn('openFacet=""', html)
        self.assertIn("function toggleFacet", html)
        self.assertIn("class=\"facet ${isOpen?\"open\":\"collapsed\"}\"", html)
        self.assertIn("class=\"facetActive\"", html)
        self.assertIn("function summaryFor", html)
        self.assertIn("shown resources", html)
        self.assertIn('class="modeBtn" data-mode="force">Graph', html)
        self.assertIn("function breadcrumbText", html)
        self.assertIn("function labelLayers", html)
        self.assertIn("function nodeBox", html)
        self.assertIn("function labelCandidates", html)
        self.assertIn("function clearOf", html)
        self.assertIn("stable:true", html)
        self.assertIn("setInterval", html)
        self.assertIn("Selected item relationship graph", html)
        self.assertIn("function graphLegend", html)
        self.assertIn("function graphRelationshipPanel", html)
        self.assertIn("function edgeKindLabels", html)
        self.assertIn("function graphNodeAction", html)
        self.assertIn("data-graph-facet", html)
        self.assertIn("nodeHit", html)
        self.assertIn("graphZoomIn", html)
        self.assertIn("function setGraphZoom", html)
        self.assertIn("function beginGraphPan", html)
        self.assertIn("Drag the graph to pan", html)
        self.assertIn("Labels without conflicts remain visible", html)
        self.assertNotIn("labels.has(n.id)", html)
        self.assertNotIn('data-open="${attr(n.open||"overview")}"', html)
        self.assertIn('if(mode==="overview")renderOverview', html)
        self.assertNotIn('if(mode==="overview"||!selected)', html)
        self.assertNotIn('${(d.formats||[]).join(", ")}', html)
        self.assertIn("avoids opening on a full hairball", html)

    def test_graph_index_is_compact_summary_not_edge_duplicate(self) -> None:
        dataset, resources, publisher = builder.normalize_dataset(fixture_package(), "https://example.test/api/action")
        publisher["dataset_count"] = 1
        publisher["resource_count"] = len(resources)
        relationships = builder.build_relationships([dataset], resources, {})
        graph = builder.build_graph([dataset], resources, {publisher["name"]: publisher}, relationships)
        self.assertEqual(graph["node_counts"]["datasets"], 1)
        self.assertEqual(graph["node_counts"]["resources"], 1)
        self.assertIn({"kind": "has resource", "count": 1}, graph["edge_counts"])
        self.assertNotIn("edges", graph)
        self.assertNotIn("nodes", graph)

    def test_overview_recent_datasets_ignore_placeholder_dates(self) -> None:
        def dataset(name: str, timestamp: str, metadata_modified: str) -> dict[str, Any]:
            return {
                "name": name,
                "title": name.replace("-", " ").title(),
                "publisher": "publisher",
                "publisher_title": "Publisher",
                "resource_count": 1,
                "formats": ["CSV"],
                "timestamp": timestamp,
                "metadata_modified": metadata_modified,
                "metadata_created": "2025-01-01T00:00:00",
            }

        manifest = {
            "title": "Test bundle",
            "generated_at": "2026-07-01T00:00:00Z",
            "source": {},
            "counts": {},
            "performance": {},
        }
        overview = builder.build_overview(
            manifest,
            [
                dataset("placeholder-template", "{{modified:toISO}}", "2026-06-01T00:00:00"),
                dataset("new-real-date", "2026-07-02T00:00:00", "2026-07-02T00:00:00"),
                dataset("tbc-fallback", "TBC", "2026-07-01T00:00:00"),
            ],
            {},
            {},
        )
        self.assertEqual(
            [item["name"] for item in overview["recent_datasets"]],
            ["new-real-date", "tbc-fallback", "placeholder-template"],
        )

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
                self.assertEqual(manifest["indexes"]["overview"], "data/overview.json")
                self.assertTrue((out_dir / "index.html").exists())
                self.assertTrue((out_dir / "okf-explorer.json").exists())
                self.assertTrue((out_dir / "data" / "overview.json").exists())
                self.assertTrue((out_dir / "wiki" / "performance.md").exists())
                self.assertEqual(checker.main([str(out_dir)]), 0)
                self.assertEqual(performance_checker.main([str(out_dir)]), 0)
        finally:
            builder.iter_packages = original_iter_packages  # type: ignore[assignment]
            builder.fetch_govuk_content = original_fetch_govuk_content  # type: ignore[assignment]


if __name__ == "__main__":
    unittest.main()
