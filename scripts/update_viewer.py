#!/usr/bin/env python3
"""Generate root viewer.html from the public wiki Markdown corpora."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
VIEWER = ROOT / "viewer.html"
LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
NOTE_TYPE_LABELS = {
    "architecture": "Architecture",
    "data-readme": "Data Index",
    "demo-guide": "Guide",
    "entity": "Entity",
    "evaluation-benchmark": "Evaluation",
    "index": "Index",
    "interface": "Interface",
    "lint-report": "Lint Report",
    "log": "Log",
    "map": "Map",
    "topic": "Topic",
}


@dataclass(frozen=True)
class Corpus:
    id: str
    label: str
    title: str
    subtitle: str
    root: Path
    source_root: str
    required_files: tuple[str, ...]
    preferred_sections: tuple[str, ...]
    markdown_url: str


CORPORA = [
    Corpus(
        id="postmortem",
        label="Postmortem",
        title="AI Coding Assistant Postmortem Wiki",
        subtitle="Public, redacted conversation wiki following the Challenge 2 AI coding assistant work",
        root=ROOT / "postmortem-public" / "wiki",
        source_root="postmortem-public/wiki",
        required_files=(
            "index.md",
            "postmortem.md",
            "conversation-summary.md",
            "walkthrough.md",
            "architecture.md",
            "decisions.md",
            "repository-evidence.md",
        ),
        preferred_sections=("root", "readers", "exchanges", "sources", "topics", "maps", "data"),
        markdown_url="postmortem-public/wiki/index.md",
    ),
    Corpus(
        id="challenge2",
        label="Challenge 2 Wiki",
        title="Challenge 2 Knowledge Base",
        subtitle="Generated dark-data LLM Wiki over the synthetic Challenge 2 source corpus",
        root=ROOT / "challenge-2" / "wiki",
        source_root="challenge-2/wiki",
        required_files=(
            "index.md",
            "architecture.md",
            "demonstration-guide.md",
            "workbench.md",
            "evaluation-benchmark.md",
            "lint-report.md",
        ),
        preferred_sections=("root", "sources", "topics", "entities", "maps", "data"),
        markdown_url="challenge-2/wiki/index.md",
    ),
]


def rel_to_corpus(corpus: Corpus, path: Path) -> str:
    return path.relative_to(corpus.root).as_posix()


def iter_markdown(corpus: Corpus) -> list[Path]:
    return sorted(corpus.root.rglob("*.md"), key=lambda path: rel_to_corpus(corpus, path))


def parse_frontmatter(corpus: Corpus, path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    rel = f"{corpus.source_root}/{rel_to_corpus(corpus, path)}"
    if not text.startswith("---\n"):
        raise ValueError(f"{rel} is missing YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError(f"{rel} has unterminated YAML frontmatter")
    raw = text[4:end]
    body = text[end + 4 :].lstrip("\n").strip("\n")
    meta: dict[str, str] = {}
    current_key: str | None = None
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value.startswith(("'", '"')) and value.endswith(("'", '"')):
                value = value[1:-1]
            meta[key] = value
            current_key = key
        elif current_key and stripped.startswith("-"):
            value = stripped[1:].strip().strip("'\"")
            prior = meta.get(current_key, "")
            meta[current_key] = ";".join(x for x in [prior, value] if x)
    return meta, body


def plain(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text.strip(" #`*_")


def title_for(path_id: str, meta: dict[str, str], body: str) -> str:
    if meta.get("title"):
        return plain(meta["title"])
    match = HEADING_RE.search(body)
    if match:
        return plain(match.group(1))
    return Path(path_id).stem.replace("-", " ").replace("_", " ").title()


def description_for(meta: dict[str, str], body: str) -> str:
    if meta.get("description"):
        return plain(meta["description"])
    for paragraph in re.split(r"\n\s*\n", body):
        stripped = paragraph.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("- ") or stripped.startswith("|"):
            continue
        return plain(stripped.splitlines()[0])[:260]
    return ""


def type_for(path_id: str, meta: dict[str, str]) -> str:
    if meta.get("type"):
        return meta["type"]
    if meta.get("note_type") in NOTE_TYPE_LABELS:
        return NOTE_TYPE_LABELS[meta["note_type"]]
    if meta.get("source_id"):
        return "Source"
    return path_id.split("/", 1)[0].replace("-", " ").title() if "/" in path_id else "Document"


def section_for(path_id: str) -> str:
    return path_id.split("/", 1)[0] if "/" in path_id else "root"


def resolve_link(corpus: Corpus, source_id: str, href: str) -> tuple[str | None, bool]:
    href = href.strip()
    if not href or href.startswith("#"):
        return None, False
    if "[" in href or "]" in href:
        return None, False
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", href):
        return None, False
    href = unquote(href.split("#", 1)[0].split("?", 1)[0])
    if not href:
        return None, False

    source_path = corpus.root / source_id
    target_path = (source_path.parent / href).resolve()
    try:
        target_id = target_path.relative_to(corpus.root.resolve()).as_posix()
    except ValueError:
        return None, False
    return os.path.normpath(target_id).replace("\\", "/"), True


def find_edges(corpus: Corpus, path_id: str, body: str, known_ids: set[str]) -> tuple[set[tuple[str, str]], list[str]]:
    edges: set[tuple[str, str]] = set()
    errors: list[str] = []
    for match in LINK_RE.finditer(body):
        target, inside_corpus = resolve_link(corpus, path_id, match.group(2))
        if not target or not target.endswith(".md"):
            continue
        if target in known_ids:
            edges.add((path_id, target))
        elif inside_corpus:
            errors.append(f"{corpus.source_root}/{path_id} links to missing Markdown file {corpus.source_root}/{target}")
    return edges, errors


def build_corpus(corpus: Corpus) -> tuple[dict[str, object], list[str]]:
    nodes: dict[str, dict[str, str]] = {}
    parsed: dict[str, tuple[dict[str, str], str]] = {}
    errors: list[str] = []

    for path in iter_markdown(corpus):
        path_id = rel_to_corpus(corpus, path)
        try:
            meta, body = parse_frontmatter(corpus, path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        parsed[path_id] = (meta, body)
        nodes[path_id] = {
            "id": path_id,
            "type": type_for(path_id, meta),
            "title": title_for(path_id, meta, body),
            "description": description_for(meta, body),
            "timestamp": meta.get("timestamp") or meta.get("updated") or meta.get("generated_at") or "",
            "aliases": meta.get("aliases", ""),
            "tags": meta.get("tags", ""),
            "section": section_for(path_id),
            "source": f"{corpus.source_root}/{path_id}",
            "body": body,
        }

    for path_id in sorted(set(corpus.required_files).difference(nodes)):
        errors.append(f"{corpus.source_root}/{path_id} is missing from the viewer graph")

    known_ids = set(nodes)
    edge_set: set[tuple[str, str]] = set()
    for path_id, (_meta, body) in parsed.items():
        edges, link_errors = find_edges(corpus, path_id, body, known_ids)
        edge_set.update(edges)
        errors.extend(link_errors)

    sections = sorted({node["section"] for node in nodes.values()})
    ordered_sections = [section for section in corpus.preferred_sections if section in sections]
    ordered_sections.extend(section for section in sections if section not in ordered_sections)
    graph = {
        "id": corpus.id,
        "label": corpus.label,
        "title": corpus.title,
        "subtitle": corpus.subtitle,
        "root": "index.md",
        "source_root": corpus.source_root,
        "markdown_url": corpus.markdown_url,
        "sections": ordered_sections,
        "nodes": nodes,
        "edges": [list(edge) for edge in sorted(edge_set)],
    }
    return graph, errors


def build_graph() -> tuple[dict[str, object], list[str]]:
    corpora: dict[str, object] = {}
    errors: list[str] = []
    for corpus in CORPORA:
        graph, corpus_errors = build_corpus(corpus)
        corpora[corpus.id] = graph
        errors.extend(corpus_errors)

    bundle = {
        "meta": {
            "title": "AI Engineering Lab Public Wiki",
            "default_corpus": "postmortem",
            "generated_by": "scripts/update_viewer.py",
            "corpus_order": [corpus.id for corpus in CORPORA],
            "local_workbench": {
                "label": "Local Workbench",
                "url": "http://localhost:5173/?pack=hmrc-narrative",
                "challenge_url": "http://localhost:5173/",
                "command": "cd challenge-2/workbench && pnpm dev -- --host 127.0.0.1",
            },
        },
        "corpora": corpora,
    }
    return bundle, errors


def rendered_viewer(graph: dict[str, object]) -> str:
    graph_json = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))
    return VIEWER_TEMPLATE.replace("__GRAPH_JSON__", graph_json)


def graph_stats(bundle: dict[str, object]) -> str:
    corpora = bundle["corpora"]
    assert isinstance(corpora, dict)
    parts: list[str] = []
    for corpus_id in bundle["meta"]["corpus_order"]:  # type: ignore[index]
        corpus = corpora[corpus_id]
        assert isinstance(corpus, dict)
        parts.append(f"{corpus['label']}: {len(corpus['nodes'])} pages, {len(corpus['edges'])} links")
    return "; ".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if viewer.html is not synchronized")
    args = parser.parse_args(argv)

    graph, errors = build_graph()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    rendered = rendered_viewer(graph)
    if args.check:
        if not VIEWER.exists() or VIEWER.read_text(encoding="utf-8") != rendered:
            print("viewer.html is not synchronized; run python3 scripts/update_viewer.py", file=sys.stderr)
            return 1
        print(f"viewer.html is synchronized with {graph_stats(graph)}")
        return 0

    if VIEWER.exists() and VIEWER.read_text(encoding="utf-8") == rendered:
        print(f"viewer.html already synchronized with {graph_stats(graph)}")
    else:
        VIEWER.write_text(rendered, encoding="utf-8")
        print(f"updated viewer.html with {graph_stats(graph)}")
    return 0


VIEWER_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Engineering Lab Public Wiki</title>
<style>
:root{color-scheme:dark;--bg:#0f1215;--panel:#171c22;--panel2:#222932;--panel3:#2c3540;--line:#3b4653;--text:#f2f5f8;--muted:#a8b2bf;--accent:#4cc9a7;--accent2:#7aa7ff;--warn:#f2bd63}
*{box-sizing:border-box}html,body{height:100%;margin:0}body{height:100dvh;background:var(--bg);color:var(--text);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;overflow:hidden}.shell{height:100dvh;display:flex;flex-direction:column;min-height:0}
header{flex:0 0 auto;min-height:70px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:12px;padding:10px 14px;background:#11161b;min-width:0}.titleblock{min-width:240px}h1{font-size:18px;line-height:1.12;margin:0}.sub{color:var(--muted);font-size:12px;max-width:760px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.spacer{flex:1}.btn{height:34px;border:1px solid var(--line);border-radius:7px;background:var(--panel2);color:var(--text);padding:0 11px;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;gap:6px;font-weight:650}.btn:hover{border-color:var(--accent)}.btn.on{background:var(--accent);border-color:var(--accent);color:#06130f}.nav{display:flex;gap:7px;align-items:center;flex-wrap:wrap;min-width:0}.iconbtn{width:34px;height:34px;border:1px solid var(--line);border-radius:7px;background:var(--panel2);color:var(--text);cursor:pointer;font-size:18px;font-weight:750;display:inline-flex;align-items:center;justify-content:center}.iconbtn:hover{border-color:var(--accent)}
.app{flex:1;min-height:0;display:grid;grid-template-columns:minmax(270px,340px) minmax(360px,1fr) minmax(360px,520px);min-width:0}.app.nav-collapsed{grid-template-columns:42px minmax(360px,1fr) minmax(360px,520px)}
aside{min-width:0;min-height:0;background:var(--panel);border-right:1px solid var(--line);display:flex;flex-direction:column;overflow:hidden}.left{position:relative}.right{border-right:0;border-left:1px solid var(--line)}.navFull{flex:1;min-height:0;display:flex;flex-direction:column}.navRail{display:none;position:relative;width:42px;height:100%;border:0;border-right:1px solid var(--line);background:var(--panel2);color:var(--text);cursor:pointer;overflow:hidden}.navRail:hover{background:var(--panel3)}.navRail span{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(90deg);transform-origin:center;white-space:nowrap;max-width:calc(100dvh - 180px);overflow:hidden;text-overflow:ellipsis;font-size:13px;font-weight:750;letter-spacing:.02em}.nav-collapsed .left{width:42px}.nav-collapsed .navFull{display:none}.nav-collapsed .navRail{display:block}
.searchWrap{flex:0 0 auto;padding:12px 12px 8px;display:grid;grid-template-columns:minmax(0,1fr) 34px;gap:7px}#q{width:100%;padding:10px 11px;border:1px solid var(--line);border-radius:7px;background:var(--panel2);color:var(--text);outline:none}#q:focus{border-color:var(--accent)}
#list{flex:1;min-height:0;overflow:auto;overscroll-behavior:contain;padding:0 8px 18px}.group{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:13px 8px 5px}.item{display:grid;grid-template-columns:12px 1fr;gap:8px;padding:8px;border-radius:7px;cursor:pointer}.item:hover{background:var(--panel2)}.item.active{background:#273442}.dot{width:10px;height:10px;border-radius:50%;margin-top:5px}.name{font-size:13px;line-height:1.32}.meta{font-size:11px;color:var(--muted);margin-top:2px;word-break:break-word}
.stage{position:relative;min-width:0;min-height:0;background:radial-gradient(circle at 50% 45%,#1d2832 0,#101418 48%);overflow:hidden}#graph{width:100%;height:100%;display:block}.edge{stroke:#7d8796;stroke-width:1.25;opacity:.38}.node{cursor:pointer}.node circle{stroke:#0f1215;stroke-width:2.5}.node text{font-size:11px;fill:#edf4fb;paint-order:stroke;stroke:#0f1215;stroke-width:4px;stroke-linejoin:round;pointer-events:none}.node.active circle{stroke:#fff;stroke-width:3.5}.toolbar{position:absolute;top:12px;left:12px;display:flex;gap:6px;flex-wrap:wrap}.count{position:absolute;right:12px;bottom:12px;color:var(--muted);background:rgba(15,18,21,.84);border:1px solid var(--line);border-radius:7px;padding:6px 9px;font-size:12px}
#detail{flex:1;min-height:0;overflow:auto;overscroll-behavior:contain;padding:18px 22px 34px}.badge{display:inline-block;border:1px solid var(--line);border-radius:999px;background:var(--panel2);padding:2px 8px;font-size:11px;color:#d8e8ff}.path{font-size:12px;color:var(--muted);word-break:break-all;margin:8px 0 12px}.path a{color:var(--accent2)}.desc{color:var(--muted);font-style:italic;margin:8px 0 14px}
#detail h2.title{font-size:24px;line-height:1.18;margin:8px 0 6px}.md h1{font-size:21px}.md h2{font-size:17px;color:var(--accent);margin-top:22px}.md h3{font-size:15px;color:var(--accent2);margin-top:18px}.md p{margin:9px 0}.md ul,.md ol{padding-left:22px}.md li{margin:4px 0}.md code{background:var(--panel2);border:1px solid var(--line);border-radius:4px;padding:1px 4px}.md pre{white-space:pre-wrap;background:var(--panel2);border:1px solid var(--line);border-radius:7px;padding:10px;overflow:auto}.md a{color:var(--accent2);text-decoration:none}.md a:hover{text-decoration:underline}.md img{display:block;max-width:100%;height:auto;border:1px solid var(--line);border-radius:8px;margin:12px 0;background:#0b0e11}.md .mermaid-lite{display:block;width:100%;height:auto;min-height:220px;border:1px solid var(--line);border-radius:8px;background:#111820;margin:12px 0}.md .mermaid-node rect{fill:#26313d;stroke:#7aa7ff;stroke-width:1.4}.md .mermaid-node text{fill:#f2f5f8;font-size:12px}.md .mermaid-edge{stroke:#91a0b4;stroke-width:1.5;fill:none}.md .mermaid-arrow{fill:#91a0b4}.chips{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0}.chip{border:1px solid var(--line);background:var(--panel2);border-radius:999px;color:#dbeafe;padding:4px 9px;font-size:12px;cursor:pointer}.chip:hover{border-color:var(--accent)}.notice{border:1px solid var(--line);border-radius:8px;background:rgba(76,201,167,.08);padding:10px 12px;margin:12px 0;color:#dceee9}
@media (max-width:1120px){header{align-items:flex-start;flex-wrap:wrap}.sub{white-space:normal}.app{grid-template-columns:300px 1fr}.app.nav-collapsed{grid-template-columns:42px 1fr}.right{grid-column:1 / -1;border-left:0;border-top:1px solid var(--line);max-height:48vh}.stage{min-height:54vh}}
@media (max-width:760px){body{overflow:auto}.shell{height:auto;min-height:100dvh}.app,.app.nav-collapsed{display:block}.stage{height:58vh}.searchWrap,#list,#detail{max-height:none}aside{height:auto;max-height:48vh;border-right:0;border-bottom:1px solid var(--line)}.nav-collapsed .left{width:auto;height:44px;max-height:44px}.nav-collapsed .navRail{width:100%;height:44px;border-right:0}.nav-collapsed .navRail span{transform:translate(-50%,-50%);max-width:calc(100vw - 28px)}.right{max-height:none}.nav{width:100%}.btn{height:36px}}
</style>
</head>
<body>
<div class="shell">
<header>
<button class="btn" id="home">Home</button>
<div class="titleblock"><h1 id="title">AI Engineering Lab Public Wiki</h1><div class="sub" id="subtitle"></div></div>
<nav class="nav" id="corpusNav"></nav>
<div class="spacer"></div>
<a class="btn" id="workbench" href="http://localhost:5173/?pack=hmrc-narrative">Local Workbench</a>
<a class="btn" id="markdown" href="postmortem-public/wiki/index.md">Markdown</a>
</header>
<main class="app" id="app">
<aside class="left" id="navPane"><button class="navRail" id="navRail" title="Show navigation" aria-label="Show navigation"><span id="railLabel">Index</span></button><div class="navFull"><div class="searchWrap"><input id="q" placeholder="Search pages, tags, source IDs"><button class="iconbtn" id="collapseNav" title="Collapse navigation" aria-label="Collapse navigation">‹</button></div><div id="list"></div></div></aside>
<section class="stage">
<svg id="graph" role="img" aria-label="Wiki graph"></svg>
<div class="toolbar"><button class="btn on" id="graphMode">Focus Graph</button><button class="btn on" id="showLinks">Links</button></div>
<div class="count" id="count"></div>
</section>
<aside class="right"><article id="detail"></article></aside>
</main>
</div>
<script>
const B=__GRAPH_JSON__;
const SECTION_COLORS={root:"#8a93ad",readers:"#22a06b",exchanges:"#7aa7ff",sources:"#d97706",topics:"#3b82f6",entities:"#22a06b",maps:"#a855f7",data:"#64748b"};
let corpusId=new URLSearchParams(location.search).get("corpus")||B.meta.default_corpus;
if(!B.corpora[corpusId])corpusId=B.meta.default_corpus;
let G,paths,bySection,out,inc,selected,showLinks=true,graphMode="focus",navCollapsed=false;
const app=document.getElementById("app"),title=document.getElementById("title"),subtitle=document.getElementById("subtitle"),corpusNav=document.getElementById("corpusNav"),q=document.getElementById("q"),list=document.getElementById("list"),detail=document.getElementById("detail"),graph=document.getElementById("graph"),count=document.getElementById("count"),markdown=document.getElementById("markdown"),collapseNav=document.getElementById("collapseNav"),navRail=document.getElementById("navRail"),railLabel=document.getElementById("railLabel");
function esc(s){return String(s||"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));}
function attr(s){return esc(s).replace(/'/g,"&#39;");}
function color(section){return SECTION_COLORS[section]||"#94a3b8";}
function sortedTitle(ids){return [...ids].sort((a,b)=>G.nodes[a].title.localeCompare(G.nodes[b].title));}
function setNavCollapsed(flag){navCollapsed=flag;app.classList.toggle("nav-collapsed",flag);navRail.setAttribute("aria-expanded",String(!flag));if(G)requestAnimationFrame(renderGraph);}
function updateRailLabel(){railLabel.textContent=G&&G.nodes[selected]?G.nodes[selected].title:"Index";}
function setCorpus(id,pickRoot=true){corpusId=id;G=B.corpora[id];paths=Object.keys(G.nodes);bySection={};paths.forEach(pid=>{const s=G.nodes[pid].section||"root";(bySection[s]||(bySection[s]=[])).push(pid);});out={};inc={};paths.forEach(pid=>{out[pid]=new Set();inc[pid]=new Set();});G.edges.forEach(([a,b])=>{if(out[a]&&inc[b]){out[a].add(b);inc[b].add(a);}});selected=pickRoot?(G.root||paths[0]):(G.nodes[selected]?selected:(G.root||paths[0]));title.textContent=G.title;subtitle.textContent=G.subtitle;markdown.href=G.markdown_url;renderCorpusNav();renderList();renderDetail();renderGraph();const url=new URL(location.href);url.searchParams.set("corpus",id);history.replaceState(null,"",url);}
function renderCorpusNav(){corpusNav.innerHTML="";for(const id of B.meta.corpus_order){const c=B.corpora[id];const b=document.createElement("button");b.className="btn"+(id===corpusId?" on":"");b.textContent=c.label;b.onclick=()=>setCorpus(id,true);corpusNav.appendChild(b);}}
function nodeMatches(id,term){const n=G.nodes[id];return !term||[id,n.title,n.type,n.description,n.aliases,n.tags,n.source].join(" ").toLowerCase().includes(term);}
function pick(id){if(!G.nodes[id])return;selected=id;renderList();renderDetail();renderGraph();}
function renderList(){const term=q.value.trim().toLowerCase();list.innerHTML="";let shown=0;for(const section of G.sections){const ids=(bySection[section]||[]).filter(id=>nodeMatches(id,term)).sort((a,b)=>G.nodes[a].title.localeCompare(G.nodes[b].title));if(!ids.length)continue;const g=document.createElement("div");g.className="group";g.textContent=section;list.appendChild(g);for(const id of ids){shown++;const n=G.nodes[id];const row=document.createElement("div");row.className="item"+(id===selected?" active":"");row.onclick=()=>pick(id);row.innerHTML=`<span class="dot" style="background:${color(n.section)}"></span><div><div class="name">${esc(n.title)}</div><div class="meta">${esc(n.type)} - ${esc(id)}</div></div>`;list.appendChild(row);}}count.textContent=`${G.label}: ${shown} shown - ${paths.length} pages - ${G.edges.length} links`;}
function normalizeParts(basePath,href){const stack=basePath.split("/");stack.pop();for(const part of href.split("#")[0].split("?")[0].split("/")){if(!part||part===".")continue;if(part==="..")stack.pop();else stack.push(decodeURIComponent(part));}return stack.join("/");}
function targetFromHref(href){if(!href||href.startsWith("#")||/^[a-zA-Z][a-zA-Z0-9+.-]*:/.test(href))return null;const target=normalizeParts(selected,href);return G.nodes[target]?target:null;}
function sourceHref(href){if(!href||href.startsWith("#"))return href||"#";if(/^[a-zA-Z][a-zA-Z0-9+.-]*:/.test(href))return href;return normalizeParts(G.nodes[selected].source,href);}
function linkFor(href,label){const target=targetFromHref(href);if(target)return `<a href="#" data-page="${attr(target)}">${label}</a>`;return `<a href="${attr(sourceHref(href))}">${label}</a>`;}
function imageFor(label,href){return `<img src="${attr(sourceHref(href))}" alt="${attr(label)}">`;}
function inline(s){return esc(s).replace(/!\\[([^\\]]*)\\]\\(([^)]+)\\)/g,(_,label,href)=>imageFor(label,href)).replace(/`([^`]+)`/g,"<code>$1</code>").replace(/\\*\\*([^*]+)\\*\\*/g,"<strong>$1</strong>").replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g,(_,label,href)=>linkFor(href,esc(label)));}
function mermaidNodeToken(token,nodes){const clean=token.trim().replace(/;$/,"");const m=/^([A-Za-z][A-Za-z0-9_-]*)(?:\\[\\"?([^\\]]+?)\\"?\\]|\\((?:\\"?)([^)]+?)(?:\\"?)\\))?$/.exec(clean);if(!m)return null;const id=m[1];const label=(m[2]||m[3]||id).replace(/^"|"$/g,"").replace(/\\\\n/g,"\\n");nodes[id]=nodes[id]||{id,label};return id;}
function wrapMermaidLabel(label){const parts=String(label||"").split("\\n");const lines=[];for(const part of parts){let current="";for(const word of part.split(/\\s+/)){if(!word)continue;if((current+" "+word).trim().length>24){if(current)lines.push(current);current=word;}else current=(current+" "+word).trim();}if(current)lines.push(current);}return lines.length?lines:[String(label||"")];}
function mermaidLite(diagram){const lines=String(diagram||"").split("\\n").map(line=>line.trim()).filter(line=>line&&!line.startsWith("%%"));const head=lines.shift()||"";const mode=/^(?:flowchart|graph)\\s+(LR|RL|TD|TB)$/i.exec(head);if(!mode)return `<pre><code>${esc(diagram)}</code></pre>`;const nodes={},edges=[];for(const line of lines){const parts=line.replace(/;$/,"").split(/\\s*(?:-->|==>|-.->)\\s*/);if(parts.length<2)continue;const ids=parts.map(part=>mermaidNodeToken(part,nodes));for(let i=0;i<ids.length-1;i++){if(ids[i]&&ids[i+1])edges.push([ids[i],ids[i+1]]);}}const ids=Object.keys(nodes);if(!ids.length)return `<pre><code>${esc(diagram)}</code></pre>`;const incoming=Object.fromEntries(ids.map(id=>[id,0]));edges.forEach(([,b])=>incoming[b]=(incoming[b]||0)+1);const rank=Object.fromEntries(ids.map(id=>[id,0]));const queue=ids.filter(id=>!incoming[id]);const visit=queue.length?queue:[...ids];let guard=0;for(let i=0;i<visit.length&&guard<ids.length*ids.length*4;i++,guard++){const id=visit[i];for(const [a,b] of edges){const nextRank=Math.min(ids.length-1,rank[a]+1);if(a===id&&rank[b]<nextRank){rank[b]=nextRank;visit.push(b);}}}const ranks=[...new Set(ids.map(id=>rank[id]||0))].sort((a,b)=>a-b);const groups=Object.fromEntries(ranks.map(r=>[r,ids.filter(id=>(rank[id]||0)===r)]));const horizontal=mode[1].toUpperCase()==="LR"||mode[1].toUpperCase()==="RL";const nodeW=190,nodeH=76,gapX=62,gapY=34,pad=28;const maxGroup=Math.max(...ranks.map(r=>groups[r].length));const w=horizontal?pad*2+ranks.length*nodeW+Math.max(0,ranks.length-1)*gapX:pad*2+maxGroup*nodeW+Math.max(0,maxGroup-1)*gapX;const h=horizontal?pad*2+maxGroup*nodeH+Math.max(0,maxGroup-1)*gapY:pad*2+ranks.length*nodeH+Math.max(0,ranks.length-1)*gapY;const pos={};ranks.forEach((r,ri)=>{groups[r].forEach((id,i)=>{pos[id]=horizontal?{x:pad+ri*(nodeW+gapX),y:pad+i*(nodeH+gapY)}:{x:pad+i*(nodeW+gapX),y:pad+ri*(nodeH+gapY)};});});let hash=0;for(const ch of diagram)hash=(hash*31+ch.charCodeAt(0))|0;const marker=`mermaid-arrow-${Math.abs(hash)}`;let svg=`<svg class="mermaid-lite" viewBox="0 0 ${w} ${h}" role="img" aria-label="Mermaid flowchart"><defs><marker id="${marker}" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path class="mermaid-arrow" d="M0,0 L10,4 L0,8 Z"></path></marker></defs>`;for(const [a,b] of edges){const pa=pos[a],pb=pos[b];if(!pa||!pb)continue;const sx=horizontal?pa.x+nodeW:pa.x+nodeW/2,sy=horizontal?pa.y+nodeH/2:pa.y+nodeH,tx=horizontal?pb.x:pb.x+nodeW/2,ty=horizontal?pb.y+nodeH/2:pb.y;const c1x=horizontal?sx+gapX*.45:sx,c1y=horizontal?sy:sy+gapY*.45,c2x=horizontal?tx-gapX*.45:tx,c2y=horizontal?ty:ty-gapY*.45;svg+=`<path class="mermaid-edge" d="M${sx} ${sy} C${c1x} ${c1y}, ${c2x} ${c2y}, ${tx} ${ty}" marker-end="url(#${marker})"></path>`;}for(const id of ids){const p=pos[id];const labelLines=wrapMermaidLabel(nodes[id].label);const startY=p.y+nodeH/2-(labelLines.length-1)*7;svg+=`<g class="mermaid-node"><rect x="${p.x}" y="${p.y}" width="${nodeW}" height="${nodeH}" rx="7"></rect><text text-anchor="middle">`;labelLines.slice(0,4).forEach((line,i)=>{svg+=`<tspan x="${p.x+nodeW/2}" y="${startY+i*15}">${esc(line)}</tspan>`;});svg+="</text></g>";}return svg+"</svg>";}
function md(text){const lines=String(text||"").split("\\n");let html="",inList=false,inCode=false,codeLang="",buf=[];function closeList(){if(inList){html+="</ul>";inList=false;}}function flushCode(){if(inCode){const code=buf.join("\\n");html+=codeLang==="mermaid"?mermaidLite(code):`<pre><code>${esc(code)}</code></pre>`;buf=[];inCode=false;codeLang="";}}for(const line of lines){if(line.startsWith("```")){if(inCode)flushCode();else{closeList();inCode=true;codeLang=line.slice(3).trim().toLowerCase();buf=[];}continue;}if(inCode){buf.push(line);continue;}if(!line.trim()){closeList();continue;}let m;if((m=/^###\\s+(.+)/.exec(line))){closeList();html+=`<h3>${inline(m[1])}</h3>`;}else if((m=/^##\\s+(.+)/.exec(line))){closeList();html+=`<h2>${inline(m[1])}</h2>`;}else if((m=/^#\\s+(.+)/.exec(line))){closeList();html+=`<h1>${inline(m[1])}</h1>`;}else if((m=/^-\\s+(.+)/.exec(line))){if(!inList){html+="<ul>";inList=true;}html+=`<li>${inline(m[1])}</li>`;}else{closeList();html+=`<p>${inline(line)}</p>`;}}flushCode();closeList();return html;}
function renderDetail(){const n=G.nodes[selected];updateRailLabel();const outgoing=sortedTitle(out[selected]);const incoming=sortedTitle(inc[selected]);const local=B.meta.local_workbench;const workbenchNotice=selected==="walkthrough.md"?`<div class="notice"><strong>Local SeeLinks-style Workbench:</strong> this static page cannot start a local server, but on this machine you can run <code>${esc(local.command)}</code> and then open <a href="${attr(local.url)}">${esc(local.url)}</a>.</div>`:"";detail.innerHTML=`<span class="badge">${esc(n.type)}</span><h2 class="title">${esc(n.title)}</h2><div class="path"><a href="${attr(n.source)}">${esc(n.source)}</a></div><p class="desc">${esc(n.description)}</p>${workbenchNotice}<div class="chips">${outgoing.slice(0,18).map(id=>`<button class="chip" data-page="${attr(id)}">out: ${esc(G.nodes[id].title)}</button>`).join("")}${incoming.slice(0,18).map(id=>`<button class="chip" data-page="${attr(id)}">in: ${esc(G.nodes[id].title)}</button>`).join("")}</div><div class="md">${md(n.body)}</div>`;detail.querySelectorAll("[data-page]").forEach(a=>a.addEventListener("click",e=>{e.preventDefault();pick(a.dataset.page);}));}
function visibleGraphIds(){if(graphMode==="overview")return paths;const ids=new Set([selected]);for(const id of sortedTitle(out[selected]))ids.add(id);for(const id of sortedTitle(inc[selected]))ids.add(id);const section=G.nodes[selected].section;for(const id of sortedTitle(bySection[section]||[])){if(ids.size>=28)break;ids.add(id);}return [...ids].slice(0,72);}
function graphPositions(ids,w,h){const cx=w/2,cy=h/2,pos={};if(graphMode==="focus"){pos[selected]={x:cx,y:cy};const others=ids.filter(id=>id!==selected);const inner=others.filter(id=>out[selected].has(id)||inc[selected].has(id));const outer=others.filter(id=>!inner.includes(id));inner.forEach((id,i)=>{const a=Math.PI*2*i/Math.max(1,inner.length)-Math.PI/2;pos[id]={x:cx+Math.cos(a)*Math.min(w,h)*.28,y:cy+Math.sin(a)*Math.min(w,h)*.28};});outer.forEach((id,i)=>{const a=Math.PI*2*i/Math.max(1,outer.length)-Math.PI/2;pos[id]={x:cx+Math.cos(a)*Math.min(w,h)*.43,y:cy+Math.sin(a)*Math.min(w,h)*.43};});return pos;}const sections=G.sections;sections.forEach((section,si)=>{const group=ids.filter(id=>G.nodes[id].section===section).sort();const colCount=Math.max(1,Math.ceil(Math.sqrt(group.length)));const bandW=w/Math.max(1,sections.length);const startX=bandW*si+bandW*.18;group.forEach((id,i)=>{const col=i%colCount,row=Math.floor(i/colCount);pos[id]={x:startX+col*(bandW*.68/Math.max(1,colCount-1||1)),y:70+row*30};});});return pos;}
function renderGraph(){const w=graph.clientWidth||900,h=graph.clientHeight||650;graph.setAttribute("viewBox",`0 0 ${w} ${h}`);const ids=visibleGraphIds();const visible=new Set(ids);const pos=graphPositions(ids,w,h);let svg="";if(showLinks){for(const [a,b] of G.edges){if(visible.has(a)&&visible.has(b)&&pos[a]&&pos[b])svg+=`<line class="edge" x1="${pos[a].x}" y1="${pos[a].y}" x2="${pos[b].x}" y2="${pos[b].y}"/>`;}}for(const id of ids){const n=G.nodes[id],p=pos[id]||{x:w/2,y:h/2};const active=id===selected;const related=out[selected].has(id)||inc[selected].has(id);const r=active?13:(related?8:5);const label=active||related||ids.length<=34;svg+=`<g class="node ${active?"active":""}" data-page="${attr(id)}"><circle cx="${p.x}" cy="${p.y}" r="${r}" fill="${color(n.section)}"/><title>${esc(n.title)}</title>${label?`<text x="${p.x+r+6}" y="${p.y+4}">${esc(n.title).slice(0,54)}</text>`:""}</g>`;}graph.innerHTML=svg;graph.querySelectorAll("[data-page]").forEach(el=>el.addEventListener("click",()=>pick(el.dataset.page)));}
collapseNav.onclick=()=>setNavCollapsed(true);navRail.onclick=()=>setNavCollapsed(false);document.getElementById("home").onclick=()=>pick(G.root||"index.md");document.getElementById("graphMode").onclick=e=>{graphMode=graphMode==="focus"?"overview":"focus";e.currentTarget.textContent=graphMode==="focus"?"Focus Graph":"Overview Graph";renderGraph();};document.getElementById("showLinks").onclick=e=>{showLinks=!showLinks;e.currentTarget.classList.toggle("on",showLinks);renderGraph();};q.addEventListener("input",renderList);window.addEventListener("resize",renderGraph);
setCorpus(corpusId,true);
</script>
</body>
</html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
