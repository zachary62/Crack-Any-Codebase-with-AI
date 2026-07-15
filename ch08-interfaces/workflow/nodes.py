"""Ch8 nodes: read an API surface at three levels of zoom.

One node per prompt in the chapter (§8.3-8.5):
  1. FindRoutes        collect the surface files (the route manifest)
  2. ApiMenu           group ~300 endpoints into a feature menu + a tour
  3. TraceActions      trace 4-8 user gestures across services (swimlanes)
  4. EndpointSequence  pick one endpoint, read its handler, draw a sequence diagram

EndpointSequence runs after the menu and flows because it reuses them: it picks
the most illustrative endpoint from the menu, then reads its handler source (an
extra LLM call picks the files) to draw the diagram.
"""
import os
import re
import sys

import yaml
from pocketflow import Node

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils import call_llm, read_prompt, fill  # noqa: E402
import routes_find as rf  # noqa: E402

PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')


def load_prompt(name):
    return read_prompt(PROMPTS_DIR, name)


def parse_yaml(text):
    m = re.search(r"```yaml\s*\n(.*?)```", text, re.DOTALL)
    blob = m.group(1) if m else text
    return yaml.safe_load(blob)


def split_menu(md):
    """Split the menu output into (opener, groups_md, tour_md)."""
    tour_match = re.search(r'^##\s+.*tour.*$', md, re.IGNORECASE | re.MULTILINE)
    if tour_match:
        head, tour_md = md[:tour_match.start()], md[tour_match.end():]
    else:
        head, tour_md = md, ""
    first_card = re.search(r'^###\s', head, re.MULTILINE)
    if first_card:
        opener, groups_md = head[:first_card.start()].strip(), head[first_card.start():]
    else:
        opener, groups_md = head.strip(), ""
    return opener, groups_md.strip(), tour_md.strip()


def first_card(md):
    """The first `### ` card (header + body) of a markdown blob, as one string."""
    m = re.search(r'^###\s+(.*)', md, re.MULTILINE)
    if not m:
        return md[:1500]
    rest = md[m.start():]
    nxt = re.search(r'^###\s', rest[3:], re.MULTILINE)
    return (rest[:nxt.start() + 3] if nxt else rest)[:2500]


class FindRoutes(Node):
    def prep(self, shared):
        return shared["repo_path"]

    def exec(self, repo):
        routes, files, kept = rf.crawl_routes(repo)
        return routes, files, kept

    def post(self, shared, prep_res, exec_res):
        routes, files, kept = exec_res
        assert routes.strip(), (
            "No route/surface files found. This chapter expects a web API "
            "(Rails routes, Django urls, Next.js pages/api, tRPC, GraphQL, gRPC).")
        shared["routes"] = routes
        shared["route_files"] = files
        print(f"  Surface: {kept} route files ({len(routes):,} chars)")


class ApiMenu(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return fill(load_prompt("api-menu.md"), routes=shared["routes"])

    def exec(self, prompt):
        md = call_llm(prompt).strip()
        assert "###" in md, "menu produced no `###` feature-group cards"
        return md

    def post(self, shared, prep_res, exec_res):
        opener, groups_md, tour_md = split_menu(exec_res)
        names = re.findall(r'^###\s+(.+?)\s*$', groups_md, re.MULTILINE)
        shared["menu_md"] = exec_res
        shared["opener"] = opener
        shared["groups_md"] = groups_md
        shared["tour_md"] = tour_md
        shared["group_names"] = names
        print(f"  Menu: {len(names)} feature groups"
              + (f", {tour_md.count('###')} tour steps" if tour_md else ""))


class TraceActions(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        groups = "\n".join(shared["group_names"]) or shared.get("groups_md", "")[:4000]
        return fill(load_prompt("trace-action.md"),
                    routes=shared["routes"], groups=groups)

    def exec(self, prompt):
        md = call_llm(prompt).strip()
        assert "###" in md, "trace produced no `###` flow cards"
        return md

    def post(self, shared, prep_res, exec_res):
        shared["flows_md"] = exec_res
        print(f"  Flows: {exec_res.count(chr(35) + '##')} actions traced")


_PICK_PROMPT = """From this API surface and its feature menu, pick the SINGLE most
illustrative endpoint to draw as a sequence diagram: one that fans out to several
services (a database write plus external calls), not a simple read.

Return YAML in a ```yaml fence:

```yaml
endpoint: "POST /api/..."          # method + path
files:                              # repo-relative source paths whose code shows
  - path/to/the/handler.ts          # this endpoint's real flow: the route handler
  - path/to/core/logic.ts           # and the main functions it calls (up to 6)
```

Feature menu:
{menu}

API surface (route files):
{routes}
"""


class EndpointSequence(Node):
    """Two steps: an LLM picks the endpoint + its source files, we read them, then
    an LLM draws the sequence diagram. If the pick is unusable, fall back to the
    largest route handler so the diagram still renders."""
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return {
            "repo": shared["repo_path"],
            "routes": shared["routes"],
            "menu": shared["menu_md"],
            "flow": first_card(shared.get("flows_md", "")),
            "route_files": shared["route_files"],
        }

    def exec(self, ctx):
        # Step 1 — pick the endpoint and the files that show its flow.
        endpoint, paths = "", []
        try:
            picked = parse_yaml(call_llm(fill(_PICK_PROMPT, menu=ctx["menu"], routes=ctx["routes"])))
            endpoint = str(picked.get("endpoint", "")).strip()
            paths = [str(p) for p in (picked.get("files") or []) if p]
        except Exception:
            pass
        handler_source, resolved = rf.read_files(ctx["repo"], paths)
        if not handler_source.strip():
            # Fallback: the largest Next.js handler on disk.
            candidates = [f for f in ctx["route_files"] if "/pages/api/" in f.replace(os.sep, "/")]
            if candidates:
                big = max(candidates, key=lambda f: os.path.getsize(os.path.join(ctx["repo"], f)))
                handler_source, resolved = rf.read_files(ctx["repo"], [big])
                endpoint = endpoint or big

        # Step 2 — draw the diagram from the handler source.
        prompt = fill(load_prompt("endpoint-sequence.md"),
                      routes=ctx["routes"][:60_000], flow=ctx["flow"],
                      handler_source=handler_source or "(handler source unavailable)")
        md = call_llm(prompt).strip()
        assert "```mermaid" in md or "sequenceDiagram" in md, "no sequence diagram produced"
        return {"md": md, "endpoint": endpoint, "files": resolved}

    def post(self, shared, prep_res, exec_res):
        shared["sequence_md"] = exec_res["md"]
        shared["sequence_endpoint"] = exec_res["endpoint"]
        shared["sequence_files"] = exec_res["files"]
        print(f"  Sequence: {exec_res['endpoint'] or 'endpoint'} "
              f"(from {len(exec_res['files'])} source files)")


def overview_spec(shared):
    """Chapter-specific bits for the shared OverviewNode (utils/nodes.py)."""
    name = os.path.basename(shared["repo_path"].rstrip("/")) or shared["repo_path"]
    return {
        "name": name,
        "what": "a product's API surface — every door into the system",
        "sections": [
            ("Feature menu", "every endpoint grouped by feature, biggest group first, each tagged public/user/admin"),
            ("The tour", "a short walk through the groups that say the most about the product"),
            ("Action flows", "which services fire, in order, for one user gesture"),
            ("Endpoint sequence", "a message-by-message diagram of one endpoint, request to response"),
        ],
        "facts": (f"{shared.get('opener', '')[:400]} "
                  f"{len(shared.get('group_names', []))} feature groups. "
                  f"Endpoint diagrammed: {shared.get('sequence_endpoint', '')}."),
    }
