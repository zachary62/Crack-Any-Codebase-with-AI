"""Ch9 nodes: map a multi-service architecture in three passes (§9.3-9.5).

  1. BuildBundle   assemble the architecture bundle from the four sources
  2. Inventory     name every node, sort into 4 bands, draw the service graph
  3. TechStack     open each box: the specific tech it's built from
  4. TraceRequest  trace the core action hop by hop, plus its variants

Inventory runs first; its numbered node list (stable IDs) is reused by TechStack
and TraceRequest so all three passes talk about the same graph.
"""
import os
import re
import sys

from pocketflow import Node

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils import call_llm, read_prompt, fill, extract_mermaid  # noqa: E402
import arch_crawl as ac  # noqa: E402

PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')


def load_prompt(name):
    return read_prompt(PROMPTS_DIR, name)


class BuildBundle(Node):
    def prep(self, shared):
        return shared["repo_path"]

    def exec(self, repo):
        return ac.build_bundle(repo)

    def post(self, shared, prep_res, exec_res):
        bundle, stats = exec_res
        assert bundle.strip(), (
            "No architecture sources found (no compose/env/package/IaC). "
            "This chapter expects a multi-service app; a single-binary tool "
            "has no service graph to draw (§9.1).")
        shared["codebase"] = bundle
        shared["arch_stats"] = stats
        print(f"  Bundle: {stats['config_files']} config files, {stats['env_vars']} env vars, "
              f"{stats['deps']} deps, {stats['integrations']} integrations, {stats['sdk_lines']} SDK imports")


class Inventory(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return fill(load_prompt("inventory.md"), codebase=shared["codebase"])

    def exec(self, prompt):
        md = call_llm(prompt).strip()
        assert "###" in md, "inventory produced no `### N · node` cards"
        return md

    def post(self, shared, prep_res, exec_res):
        md = exec_res
        verdict = re.search(r"\*\*Shape verdict:\*\*\s*(.+)", md)
        shared["inventory_md"] = md
        shared["arch_diagram"] = extract_mermaid(md)
        shared["shape_verdict"] = verdict.group(1).strip() if verdict else ""
        n_nodes = len(re.findall(r'^###\s', md, re.MULTILINE))
        print(f"  Inventory: {n_nodes} nodes"
              + (" (graph drawn)" if shared["arch_diagram"] else " (no graph parsed)"))


class TechStack(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return fill(load_prompt("tech-stack.md"),
                    codebase=shared["codebase"], inventory=shared["inventory_md"])

    def exec(self, prompt):
        md = call_llm(prompt).strip()
        assert "###" in md, "tech-stack produced no `### N · node` cards"
        return md

    def post(self, shared, prep_res, exec_res):
        shared["techstack_md"] = exec_res
        print(f"  Tech stack: {exec_res.count(chr(35) + '##')} nodes documented")


class TraceRequest(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return fill(load_prompt("trace-request.md"),
                    codebase=shared["codebase"], inventory=shared["inventory_md"])

    def exec(self, prompt):
        md = call_llm(prompt).strip()
        assert "###" in md, "trace produced no `###` cards"
        return md

    def post(self, shared, prep_res, exec_res):
        shared["trace_md"] = exec_res
        print(f"  Trace: {exec_res.count(chr(35) + '##')} cards (trace + variants)")


def overview_spec(shared):
    """Chapter-specific bits for the shared OverviewNode (utils/nodes.py)."""
    name = os.path.basename(shared["repo_path"].rstrip("/")) or shared["repo_path"]
    n_nodes = len(re.findall(r'^###\s', shared.get("inventory_md", ""), re.MULTILINE))
    return {
        "name": name,
        "what": "a multi-service architecture — the graph of programs and the wires between them",
        "sections": [
            ("The inventory", "every service and store on one map, colour-coded by who runs it"),
            ("Tech stack", "what each box on the map is really built from, behind its label"),
            ("The trace", "which services fire when the product's core request runs, and how variants differ"),
        ],
        "facts": f"{shared.get('shape_verdict', '')} {n_nodes} nodes on the map.",
    }
