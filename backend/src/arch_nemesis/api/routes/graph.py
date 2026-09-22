from fastapi import APIRouter
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse

from arch_nemesis.graph.builder import get_graph_mermaid, get_graph_spec

router = APIRouter()
graph_page_router = APIRouter()


def render_graph_html() -> str:
    spec = get_graph_spec()
    mermaid = get_graph_mermaid()
    nodes = "".join(f"<li>{node['id']}</li>" for node in spec["nodes"])
    edges = "".join(f"<li>{edge['from']} → {edge['to']}</li>" for edge in spec["edges"])
    return f"""
    <!doctype html>
    <html>
      <head>
        <title>{spec['title']}</title>
        <script type="module">import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs'; mermaid.initialize({{ startOnLoad: true }});</script>
        <style>body {{ font-family: sans-serif; margin: 2rem; }} .mermaid {{ padding: 1rem; border: 1px solid #ddd; }}</style>
      </head>
      <body>
        <h1>{spec['title']}</h1>
        <p>Version: {spec['version']}</p>
        <div class="mermaid">{mermaid}</div>
        <h2>Nodes</h2><ul>{nodes}</ul>
        <h2>Edges</h2><ul>{edges}</ul>
        <p><a href="/api/graph/spec">JSON spec</a> · <a href="/api/graph/mermaid">Mermaid source</a></p>
      </body>
    </html>
    """


@graph_page_router.get("/graph", response_class=HTMLResponse)
def graph_page() -> str:
    return render_graph_html()


@router.get("")
def api_graph_page_redirect():
    return RedirectResponse(url="/graph")


@router.get("/spec")
def graph_spec() -> dict:
    return get_graph_spec()


@router.get("/mermaid", response_class=PlainTextResponse)
def graph_mermaid() -> str:
    return get_graph_mermaid()
