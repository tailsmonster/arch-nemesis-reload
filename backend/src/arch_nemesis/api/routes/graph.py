from fastapi import APIRouter
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse

from arch_nemesis.graph.builder import get_graph_mermaid, get_graph_spec

router = APIRouter()
graph_page_router = APIRouter()


def render_graph_html() -> str:
    spec = get_graph_spec()
    mermaid = get_graph_mermaid()
    executable = spec["executable_langgraph"]
    nodes = "".join(
        f"<li><code>{node['id']}</code> <strong>{node['kind']}</strong>: {node['description']}</li>"
        for node in spec["nodes"]
    )
    edges = "".join(
        f"<li><code>{edge['from']}</code> → <code>{edge['to']}</code> <em>{edge.get('label', '')}</em></li>"
        for edge in spec["edges"]
    )
    executable_nodes = "".join(f"<li><code>{node}</code></li>" for node in executable["nodes"])
    return f"""
    <!doctype html>
    <html>
      <head>
        <title>{spec['title']}</title>
        <script type="module">import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs'; mermaid.initialize({{ startOnLoad: true }});</script>
        <style>
          body {{ font-family: sans-serif; margin: 2rem; line-height: 1.4; }}
          .mermaid {{ padding: 1rem; border: 1px solid #ddd; overflow-x: auto; }}
          code {{ background: #f1f3f5; padding: 0.1rem 0.25rem; border-radius: 0.25rem; }}
          .meta {{ background: #f8f9fa; border: 1px solid #dee2e6; padding: 1rem; margin: 1rem 0; }}
        </style>
      </head>
      <body>
        <h1>{spec['title']}</h1>
        <p>Version: {spec['version']}</p>
        <div class="meta">
          <h2>Executable LangGraph</h2>
          <p>Builder: <code>{executable['builder']}</code></p>
          <p>Function: <code>{executable['function']}()</code></p>
          <p>Add node call: <code>{executable['add_node_lines']}</code></p>
          <p>Entry point: <code>{executable['entry_point']}</code></p>
          <h3>Executable turn nodes</h3>
          <ul>{executable_nodes}</ul>
        </div>
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
