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
        self.assertIn("labelLayerCount=1", template)
        self.assertIn("function labelLayers(ids,pos)", template)
        self.assertIn("function labelSet(ids,pos)", template)
        self.assertIn("const active=layers.length?(layers[labelPhase%labelLayerCount]||[]):[]", template)
        self.assertIn('setInterval(()=>{if(currentView==="graph"&&labelLayerCount>1)', template)
        self.assertIn("labelPhase=(labelPhase+1)%labelLayerCount", template)
        self.assertNotIn('if(graphMode==="focus"&&ids.length<=18)return new Set(ids)', template)

    def test_graph_template_collapses_reciprocal_duplicate_edge_labels(self) -> None:
        template = update_viewer.VIEWER_TEMPLATE

        self.assertIn("function edgePairKey(edge)", template)
        self.assertIn("function edgeLabelPlan(items)", template)
        self.assertIn("group.length>1&&labels.length===1", template)
        self.assertIn("show:item.i===first.i", template)
        self.assertIn("group.length>1 ? .34 : .5", template)

    def test_graph_template_includes_explicit_zoom_controls(self) -> None:
        template = update_viewer.VIEWER_TEMPLATE

        self.assertIn('id="zoomOut"', template)
        self.assertIn('id="zoomReset"', template)
        self.assertIn('id="zoomIn"', template)
        self.assertIn("function setGraphZoom(value)", template)
        self.assertIn('graph.setAttribute("viewBox",graphViewBox(w,h))', template)
        self.assertIn('graph.addEventListener("wheel"', template)

    def test_graph_template_includes_drag_pan_controls(self) -> None:
        template = update_viewer.VIEWER_TEMPLATE

        self.assertIn("-webkit-user-select:none", template)
        self.assertIn("graphPanX=0,graphPanY=0,graphDrag=null,graphSuppressClick=false", template)
        self.assertIn("padX=w*.35,padY=h*.35", template)
        self.assertIn("function beginGraphPan(e)", template)
        self.assertIn("function moveGraphPan(e)", template)
        self.assertIn("graphSuppressClick=true", template)
        self.assertIn("function suppressGraphClick(e)", template)
        self.assertIn("graphPanX=graphDrag.panX-dx/z", template)
        self.assertIn('graph.addEventListener("pointerdown",beginGraphPan)', template)
        self.assertIn('graph.addEventListener("click",suppressGraphClick,true)', template)
        self.assertIn('graph.addEventListener("dragstart",e=>e.preventDefault())', template)
        self.assertIn('zoomReset.onclick=resetGraphView', template)

    def test_mobile_detail_panel_is_a_touch_scroll_surface(self) -> None:
        template = update_viewer.VIEWER_TEMPLATE

        self.assertIn("-webkit-overflow-scrolling:touch", template)
        self.assertIn("touch-action:pan-y", template)
        self.assertIn(".right #detail{height:100%;max-height:100%;overflow:auto}", template)
        self.assertIn(".right{height:70vh;height:70dvh;min-height:360px;max-height:none}", template)


if __name__ == "__main__":
    unittest.main()
