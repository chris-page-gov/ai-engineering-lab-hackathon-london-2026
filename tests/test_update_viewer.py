from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import update_viewer  # noqa: E402


class UpdateViewerGraphTest(unittest.TestCase):
    def test_source_to_source_links_are_typed_as_related_sources(self) -> None:
        self.assertEqual(
            update_viewer.edge_type("Google OKF Standard (GitHub)", "sources/a.md", "sources/b.md"),
            "related source",
        )

    def test_focus_graph_does_not_add_same_section_filler_nodes(self) -> None:
        template = update_viewer.VIEWER_TEMPLATE

        self.assertIn('function visibleGraphIds(){if(graphMode==="overview")return paths;', template)
        self.assertNotIn("ids.size>=28", template)

    def test_graph_template_includes_directional_edges_and_rotating_labels(self) -> None:
        template = update_viewer.VIEWER_TEMPLATE

        self.assertIn('marker-end="url(#${active?"arrowheadActive":"arrowhead"})"', template)
        self.assertIn('class="edgeHit"', template)
        self.assertIn('graphMode==="overview"||incident', template)
        self.assertIn("function labelSet(ids,pos)", template)
        self.assertIn("setInterval(()=>{if(currentView===", template)


if __name__ == "__main__":
    unittest.main()
