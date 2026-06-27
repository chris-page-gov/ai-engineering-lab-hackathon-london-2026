#!/usr/bin/env python3
"""Generate root viewer.html from the Challenge 2 wiki Markdown corpus."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "challenge-2" / "wiki"
VIEWER = ROOT / "viewer.html"
REQUIRED_FILES = {
    "index.md",
    "architecture.md",
    "demonstration-guide.md",
    "workbench.md",
    "evaluation-benchmark.md",
    "lint-report.md",
}
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


def rel_to_wiki(path: Path) -> str:
    return path.relative_to(WIKI).as_posix()


def iter_wiki_markdown() -> list[Path]:
    return sorted(WIKI.rglob("*.md"), key=rel_to_wiki)


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"challenge-2/wiki/{rel_to_wiki(path)} is missing YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError(f"challenge-2/wiki/{rel_to_wiki(path)} has unterminated YAML frontmatter")
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
    if "/" not in path_id:
        return "root"
    return path_id.split("/", 1)[0]


def resolve_link(source_id: str, href: str) -> tuple[str | None, bool]:
    href = href.strip()
    if not href or href.startswith("#"):
        return None, False
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", href):
        return None, False
    href = unquote(href.split("#", 1)[0].split("?", 1)[0])
    if not href:
        return None, False

    source_path = WIKI / source_id
    target_path = (source_path.parent / href).resolve()
    try:
        target_id = target_path.relative_to(WIKI.resolve()).as_posix()
    except ValueError:
        return None, False
    return os.path.normpath(target_id).replace("\\", "/"), True


def find_edges(path_id: str, body: str, known_ids: set[str]) -> tuple[set[tuple[str, str]], list[str]]:
    edges: set[tuple[str, str]] = set()
    errors: list[str] = []
    for match in LINK_RE.finditer(body):
        target, inside_wiki = resolve_link(path_id, match.group(2))
        if not target or not target.endswith(".md"):
            continue
        if target in known_ids:
            edges.add((path_id, target))
        elif inside_wiki:
            errors.append(f"challenge-2/wiki/{path_id} links to missing wiki Markdown file challenge-2/wiki/{target}")
    return edges, errors


def build_graph() -> tuple[dict[str, object], list[str]]:
    nodes: dict[str, dict[str, str]] = {}
    parsed: dict[str, tuple[dict[str, str], str]] = {}
    errors: list[str] = []

    for path in iter_wiki_markdown():
        path_id = rel_to_wiki(path)
        try:
            meta, body = parse_frontmatter(path)
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
            "section": section_for(path_id),
            "source": f"challenge-2/wiki/{path_id}",
            "body": body,
        }

    for path_id in sorted(REQUIRED_FILES.difference(nodes)):
        errors.append(f"challenge-2/wiki/{path_id} is missing from the viewer graph")

    known_ids = set(nodes)
    edge_set: set[tuple[str, str]] = set()
    for path_id, (_meta, body) in parsed.items():
        edges, link_errors = find_edges(path_id, body, known_ids)
        edge_set.update(edges)
        errors.extend(link_errors)

    sections = sorted({node["section"] for node in nodes.values()})
    preferred = ["root", "sources", "topics", "entities", "maps", "data"]
    ordered_sections = [section for section in preferred if section in sections]
    ordered_sections.extend(section for section in sections if section not in ordered_sections)
    graph = {
        "meta": {
            "title": "Challenge 2 Knowledge Base",
            "subtitle": "OKF-style static viewer for the generated dark-data LLM Wiki",
            "root": "index.md",
            "source_root": "challenge-2/wiki",
            "generated_by": "scripts/update_viewer.py",
            "sections": ordered_sections,
        },
        "nodes": nodes,
        "edges": [list(edge) for edge in sorted(edge_set)],
    }
    return graph, errors


def rendered_viewer(graph: dict[str, object]) -> str:
    graph_json = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))
    return VIEWER_TEMPLATE.replace("__GRAPH_JSON__", graph_json)


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
        print(f"viewer.html is synchronized with {len(graph['nodes'])} pages and {len(graph['edges'])} links")
        return 0

    if VIEWER.exists() and VIEWER.read_text(encoding="utf-8") == rendered:
        print(f"viewer.html already synchronized with {len(graph['nodes'])} pages and {len(graph['edges'])} links")
    else:
        VIEWER.write_text(rendered, encoding="utf-8")
        print(f"updated viewer.html with {len(graph['nodes'])} pages and {len(graph['edges'])} links")
    return 0


VIEWER_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Challenge 2 Knowledge Base Viewer</title>
<style>
:root{color-scheme:dark;--bg:#101214;--panel:#191d21;--panel2:#22272e;--line:#343b45;--text:#eef2f6;--muted:#a7b0bd;--accent:#4cc9a7;--accent2:#7aa7ff;--warn:#f2bd63}
*{box-sizing:border-box}html,body{height:100%;margin:0}body{background:var(--bg);color:var(--text);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;overflow:hidden}
header{height:58px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:12px;padding:10px 14px;background:#12161b}
h1{font-size:17px;line-height:1.1;margin:0}.sub{color:var(--muted);font-size:12px}.spacer{flex:1}.btn{height:32px;border:1px solid var(--line);border-radius:6px;background:var(--panel2);color:var(--text);padding:0 10px;cursor:pointer}.btn:hover{border-color:var(--accent)}.btn.on{background:var(--accent);border-color:var(--accent);color:#07120f;font-weight:700}
.app{height:calc(100% - 58px);display:grid;grid-template-columns:310px 1fr 440px;min-width:0}
aside{min-width:0;background:var(--panel);border-right:1px solid var(--line);display:flex;flex-direction:column}.right{border-right:0;border-left:1px solid var(--line)}
#q{margin:12px;padding:9px 10px;border:1px solid var(--line);border-radius:7px;background:var(--panel2);color:var(--text);outline:none}#q:focus{border-color:var(--accent)}
#list{overflow:auto;padding:0 8px 18px}.group{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:13px 8px 5px}.item{display:grid;grid-template-columns:11px 1fr;gap:8px;padding:7px 8px;border-radius:7px;cursor:pointer}.item:hover{background:var(--panel2)}.item.active{background:#26313c}.dot{width:9px;height:9px;border-radius:50%;margin-top:5px}.name{font-size:13px;line-height:1.35}.meta{font-size:11px;color:var(--muted);margin-top:2px}
.stage{position:relative;min-width:0;background:radial-gradient(circle at top left,#182027 0,#101214 42%);overflow:hidden}#graph{width:100%;height:100%;display:block}.edge{stroke:#596270;stroke-width:1;opacity:.28}.node{cursor:pointer}.node circle{stroke:#101214;stroke-width:2}.node text{font-size:10px;fill:#dce5ee;paint-order:stroke;stroke:#101214;stroke-width:3px;stroke-linejoin:round;pointer-events:none}.node.active circle{stroke:#fff;stroke-width:3}.toolbar{position:absolute;top:12px;left:12px;display:flex;gap:6px;flex-wrap:wrap}.count{position:absolute;right:12px;bottom:12px;color:var(--muted);background:rgba(16,18,20,.76);border:1px solid var(--line);border-radius:7px;padding:5px 8px;font-size:12px}
#detail{overflow:auto;padding:18px 22px 32px}.badge{display:inline-block;border:1px solid var(--line);border-radius:999px;background:var(--panel2);padding:2px 8px;font-size:11px;color:#d8e8ff}.path{font-size:12px;color:var(--muted);word-break:break-all;margin:8px 0 12px}.path a{color:var(--accent2)}.desc{color:var(--muted);font-style:italic;margin:8px 0 14px}
#detail h2.title{font-size:22px;line-height:1.2;margin:8px 0 6px}.md h1{font-size:20px}.md h2{font-size:16px;color:var(--accent);margin-top:20px}.md h3{font-size:14px;color:var(--accent2);margin-top:16px}.md p{margin:8px 0}.md ul,.md ol{padding-left:22px}.md li{margin:3px 0}.md code{background:var(--panel2);border:1px solid var(--line);border-radius:4px;padding:1px 4px}.md pre{white-space:pre-wrap;background:var(--panel2);border:1px solid var(--line);border-radius:7px;padding:10px;overflow:auto}.md a{color:var(--accent2);text-decoration:none}.md a:hover{text-decoration:underline}.chips{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0}.chip{border:1px solid var(--line);background:var(--panel2);border-radius:999px;color:#dbeafe;padding:3px 8px;font-size:12px;cursor:pointer}.chip:hover{border-color:var(--accent)}
@media (max-width:980px){body{overflow:auto}.app{height:auto;min-height:calc(100vh - 58px);grid-template-columns:1fr}aside{max-height:42vh;border-right:0;border-bottom:1px solid var(--line)}.right{max-height:none;border-left:0}.stage{height:52vh}}
</style>
</head>
<body>
<header>
<button class="btn" id="home">Home</button>
<div><h1>Challenge 2 Knowledge Base</h1><div class="sub">OKF-style static graph and Markdown viewer</div></div>
<div class="spacer"></div>
<a class="btn" href="challenge-2/wiki/index.md">Markdown</a>
</header>
<main class="app">
<aside><input id="q" placeholder="Search pages, tags, source IDs"><div id="list"></div></aside>
<section class="stage">
<svg id="graph" role="img" aria-label="Wiki graph"></svg>
<div class="toolbar"><button class="btn on" id="fit">Fit</button><button class="btn" id="showLinks">Links</button></div>
<div class="count" id="count"></div>
</section>
<aside class="right"><article id="detail"></article></aside>
</main>
<script>
const G=__GRAPH_JSON__;
const SECTION_COLORS={root:"#8a93ad",sources:"#d97706",topics:"#3b82f6",entities:"#22a06b",maps:"#a855f7",data:"#64748b"};
const paths=Object.keys(G.nodes);
const bySection={};paths.forEach(id=>{const s=G.nodes[id].section||"root";(bySection[s]||(bySection[s]=[])).push(id);});
const out={},inc={};paths.forEach(id=>{out[id]=new Set();inc[id]=new Set();});
G.edges.forEach(([a,b])=>{if(out[a]&&inc[b]){out[a].add(b);inc[b].add(a);}});
let selected=G.meta.root||paths[0],showLinks=true;
const q=document.getElementById("q"),list=document.getElementById("list"),detail=document.getElementById("detail"),graph=document.getElementById("graph"),count=document.getElementById("count");
function esc(s){return String(s||"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));}
function color(section){return SECTION_COLORS[section]||"#94a3b8";}
function nodeMatches(id,term){const n=G.nodes[id];return !term||[id,n.title,n.type,n.description,n.aliases,n.source].join(" ").toLowerCase().includes(term);}
function pick(id){selected=id;renderList();renderDetail();renderGraph();}
function renderList(){const term=q.value.trim().toLowerCase();list.innerHTML="";let shown=0;for(const section of G.meta.sections){const ids=(bySection[section]||[]).filter(id=>nodeMatches(id,term)).sort((a,b)=>G.nodes[a].title.localeCompare(G.nodes[b].title));if(!ids.length)continue;const g=document.createElement("div");g.className="group";g.textContent=section;list.appendChild(g);for(const id of ids){shown++;const n=G.nodes[id];const row=document.createElement("div");row.className="item"+(id===selected?" active":"");row.onclick=()=>pick(id);row.innerHTML=`<span class="dot" style="background:${color(n.section)}"></span><div><div class="name">${esc(n.title)}</div><div class="meta">${esc(n.type)} - ${esc(id)}</div></div>`;list.appendChild(row);}}count.textContent=`${shown} shown - ${paths.length} pages - ${G.edges.length} links`;}
function linkFor(href,label){if(/^https?:|^mailto:/.test(href))return `<a href="${esc(href)}">${label}</a>`;const clean=href.split("#")[0].split("?")[0];const target=normalizePath(selected,clean);if(G.nodes[target])return `<a href="#" data-page="${esc(target)}">${label}</a>`;return `<a href="${esc(href)}">${label}</a>`;}
function normalizePath(base,href){if(!href)return base;const stack=base.split("/");stack.pop();for(const part of href.split("/")){if(!part||part===".")continue;if(part==="..")stack.pop();else stack.push(decodeURIComponent(part));}return stack.join("/");}
function inline(s){return esc(s).replace(/`([^`]+)`/g,"<code>$1</code>").replace(/\\*\\*([^*]+)\\*\\*/g,"<strong>$1</strong>").replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g,(_,label,href)=>linkFor(href,esc(label)));}
function md(text){const lines=String(text||"").split("\\n");let html="",inList=false,inCode=false,buf=[];function closeList(){if(inList){html+="</ul>";inList=false;}}function flushCode(){if(inCode){html+=`<pre><code>${esc(buf.join("\\n"))}</code></pre>`;buf=[];inCode=false;}}for(const line of lines){if(line.startsWith("```")){if(inCode)flushCode();else{closeList();inCode=true;buf=[];}continue;}if(inCode){buf.push(line);continue;}if(!line.trim()){closeList();continue;}let m;if((m=/^###\\s+(.+)/.exec(line))){closeList();html+=`<h3>${inline(m[1])}</h3>`;}else if((m=/^##\\s+(.+)/.exec(line))){closeList();html+=`<h2>${inline(m[1])}</h2>`;}else if((m=/^#\\s+(.+)/.exec(line))){closeList();html+=`<h1>${inline(m[1])}</h1>`;}else if((m=/^-\\s+(.+)/.exec(line))){if(!inList){html+="<ul>";inList=true;}html+=`<li>${inline(m[1])}</li>`;}else{closeList();html+=`<p>${inline(line)}</p>`;}}flushCode();closeList();return html;}
function renderDetail(){const n=G.nodes[selected];const outgoing=[...out[selected]].sort();const incoming=[...inc[selected]].sort();detail.innerHTML=`<span class="badge">${esc(n.type)}</span><h2 class="title">${esc(n.title)}</h2><div class="path"><a href="${esc(n.source)}">${esc(n.source)}</a></div><p class="desc">${esc(n.description)}</p><div class="chips">${outgoing.slice(0,16).map(id=>`<button class="chip" data-page="${esc(id)}">out: ${esc(G.nodes[id].title)}</button>`).join("")}${incoming.slice(0,16).map(id=>`<button class="chip" data-page="${esc(id)}">in: ${esc(G.nodes[id].title)}</button>`).join("")}</div><div class="md">${md(n.body)}</div>`;detail.querySelectorAll("[data-page]").forEach(a=>a.addEventListener("click",e=>{e.preventDefault();pick(a.dataset.page);}));}
function renderGraph(){const w=graph.clientWidth||800,h=graph.clientHeight||600,cx=w/2,cy=h/2;graph.setAttribute("viewBox",`0 0 ${w} ${h}`);const ids=paths,sections=G.meta.sections;const pos={};sections.forEach((section,si)=>{const group=(bySection[section]||[]).slice().sort();const angle=(Math.PI*2*si/Math.max(1,sections.length))-Math.PI/2;const gx=cx+Math.cos(angle)*w*.28,gy=cy+Math.sin(angle)*h*.28;group.forEach((id,i)=>{const row=Math.floor(i/9),col=i%9;pos[id]={x:gx+(col-4)*26,y:gy+(row-(group.length/9)/2)*24};});});let svg="";if(showLinks){for(const [a,b] of G.edges){if(pos[a]&&pos[b])svg+=`<line class="edge" x1="${pos[a].x}" y1="${pos[a].y}" x2="${pos[b].x}" y2="${pos[b].y}"/>`;}}for(const id of ids){const n=G.nodes[id],p=pos[id]||{x:cx,y:cy};const r=id===selected?8:5;svg+=`<g class="node ${id===selected?"active":""}" data-page="${esc(id)}"><circle cx="${p.x}" cy="${p.y}" r="${r}" fill="${color(n.section)}"/><title>${esc(n.title)}</title>${id===selected?`<text x="${p.x+11}" y="${p.y+4}">${esc(n.title)}</text>`:""}</g>`;}graph.innerHTML=svg;graph.querySelectorAll("[data-page]").forEach(el=>el.addEventListener("click",()=>pick(el.dataset.page)));}
document.getElementById("home").onclick=()=>pick(G.meta.root||"index.md");document.getElementById("fit").onclick=renderGraph;document.getElementById("showLinks").onclick=e=>{showLinks=!showLinks;e.currentTarget.classList.toggle("on",showLinks);renderGraph();};q.addEventListener("input",renderList);window.addEventListener("resize",renderGraph);
renderList();renderDetail();renderGraph();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
