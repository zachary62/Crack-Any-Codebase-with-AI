"""Reusable PocketFlow nodes shared across chapters.

So far this holds one node — `OverviewNode`, which writes the friendly-but-
technical page overview (the hero summary + a short intro per section). It's
identical work in every chapter, so it lives here once. Each chapter's flow adds
it at the end and hands it a small `spec(shared)` function that returns the bits
that DO differ per chapter (the product name, what the page maps, the section
list, and a few real findings).

The chapter-specific *analysis* nodes stay in each chapter's own `nodes.py`.
"""
from pocketflow import Node

from .overview import write_overview


class OverviewNode(Node):
    """Write the page's welcome + per-section intros (see utils/overview.py).

    Construct with a `spec` callable: `spec(shared) -> {name, what, sections,
    facts}` (facts optional). Runs last in a chapter's flow and stores the result
    at `shared["overview"]`; the renderer reads it. Optional so a failed call
    just leaves the page without the intro copy rather than killing the run."""

    def __init__(self, spec, max_retries=2, wait=2):
        super().__init__(max_retries=max_retries, wait=wait)
        self._spec = spec

    def prep(self, shared):
        return self._spec(shared)

    def exec(self, spec):
        return write_overview(spec["name"], spec["what"], spec["sections"], spec.get("facts", ""))

    def exec_fallback(self, prep_res, exc):
        return {"welcome": "", "intros": {}}

    def post(self, shared, prep_res, exec_res):
        shared["overview"] = exec_res
        if exec_res.get("welcome"):
            print("  Overview written")
