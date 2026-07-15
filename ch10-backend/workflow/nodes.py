"""Ch10 nodes: read a backend as the same six layers, every time (§10.3-10.5).

  1. BuildBundle   crawl the source, grouped into the six layers
  2. Pipeline      draw the six-layer pipeline, a count per layer
  3. LayerCode     show the code only at the layers built in a non-standard way
  4. Trace         trace the core request through all six layers

The three passes are independent reads of the same bundle. Each LLM node uses
Node(max_retries=3, wait=2).
"""
import os
import re
import sys

from pocketflow import Node

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils import call_llm, read_prompt, fill, extract_mermaid  # noqa: E402
import backend_crawl as bc  # noqa: E402

PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')


def load_prompt(name):
    return read_prompt(PROMPTS_DIR, name)


class BuildBundle(Node):
    def prep(self, shared):
        return shared["repo_path"]

    def exec(self, repo):
        return bc.build_bundle(repo)

    def post(self, shared, prep_res, exec_res):
        bundle, stats = exec_res
        assert bundle.strip(), (
            "No backend source found (no routes/views/models). This chapter "
            "expects a server-side backend (Django, Express, Rails, FastAPI, …).")
        shared["codebase"] = bundle
        shared["layer_counts"] = stats["counts"]
        c = stats["counts"]
        print(f"  Bundle: {stats['included']} files ({len(bundle):,} chars). Layers — "
              + ", ".join(f"{k}:{c.get(k, 0)}" for k in
                          ('route', 'middleware', 'handler', 'service', 'database', 'response')))


class Pipeline(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return fill(load_prompt("pipeline.md"), codebase=shared["codebase"])

    def exec(self, prompt):
        md = call_llm(prompt).strip()
        assert "###" in md, "pipeline produced no `### Layer` cards"
        return md

    def post(self, shared, prep_res, exec_res):
        shared["pipeline_md"] = exec_res
        shared["pipeline_diagram"] = extract_mermaid(exec_res)
        n = len(re.findall(r'^###\s', exec_res, re.MULTILINE))
        print(f"  Pipeline: {n} layer cards"
              + (" (diagram drawn)" if shared["pipeline_diagram"] else " (no diagram parsed)"))


class LayerCode(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return fill(load_prompt("layer-code.md"), codebase=shared["codebase"])

    def exec(self, prompt):
        md = call_llm(prompt).strip()
        assert "###" in md, "layer-code produced no `### Layer` cards"
        return md

    def post(self, shared, prep_res, exec_res):
        shared["layercode_md"] = exec_res
        n_novel = len(re.findall(r'###.*novel', exec_res, re.IGNORECASE))
        print(f"  Layer code: {exec_res.count(chr(35) + '##')} layers ({n_novel} novel)")


class Trace(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return fill(load_prompt("trace.md"), codebase=shared["codebase"])

    def exec(self, prompt):
        md = call_llm(prompt).strip()
        assert "###" in md, "trace produced no `###` cards"
        return md

    def post(self, shared, prep_res, exec_res):
        ep = re.search(r"\*\*Endpoint:\*\*\s*(.+)", exec_res)
        shared["trace_md"] = exec_res
        shared["trace_endpoint"] = ep.group(1).strip() if ep else ""
        print(f"  Trace: {exec_res.count(chr(35) + '##')} cards"
              + (f" ({shared['trace_endpoint']})" if shared["trace_endpoint"] else ""))


def overview_spec(shared):
    """Chapter-specific bits for the shared OverviewNode (utils/nodes.py)."""
    name = os.path.basename(shared["repo_path"].rstrip("/")) or shared["repo_path"]
    c = shared.get("layer_counts", {})
    return {
        "name": name,
        "what": "a backend as the six layers every request flows through",
        "sections": [
            ("The pipeline", "the six layers every request flows through, with a count for each"),
            ("The code", "the one or two layers the team built in an unusual way, worth reading closely"),
            ("The trace", "one real request walked through all six layers, and where its data becomes durable"),
        ],
        "facts": (f"Core endpoint: {shared.get('trace_endpoint', '')}. "
                  f"Layer file counts — route {c.get('route', 0)}, middleware {c.get('middleware', 0)}, "
                  f"handler {c.get('handler', 0)}, service {c.get('service', 0)}, "
                  f"database {c.get('database', 0)}, response {c.get('response', 0)}."),
    }
