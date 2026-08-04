"""CLI for Chapter 9's architecture reader.

Usage:
    python main.py path/to/repo
    python main.py path/to/repo --out ../output/cal.com-architecture

It overlays the four architecture sources (compose, env, IaC, and the SDK
imports in the code) into one bundle, then produces three views — a node
inventory with a service graph, each node's real tech stack, and a trace of the
product's core request — as a self-contained index.html plus index.md.

This chapter is for multi-service systems. A single-binary tool (a library, a
CLI, PocketBase) is one process with no service graph; read its modules in ch13.
"""
import argparse, os

# The inventory and tech-stack passes emit a card per node — more output than
# the default cap. A higher cap costs nothing extra (billed on tokens produced).
os.environ.setdefault("LLM_MAX_OUTPUT_TOKENS", "32768")

from flow import create_architecture_flow
from render import render_html, render_markdown


def main():
    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=__doc__)
    ap.add_argument("repo_path")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    assert os.path.isdir(args.repo_path), f"{args.repo_path} is not a directory"

    name = os.path.basename(os.path.abspath(args.repo_path).rstrip('/'))
    out_dir = args.out or os.path.join(os.path.dirname(__file__), "..", "output", f"{name}-architecture")
    os.makedirs(out_dir, exist_ok=True)

    shared = {"repo_path": args.repo_path}
    create_architecture_flow().run(shared)

    md_path = os.path.join(out_dir, "index.md")
    html_path = os.path.join(out_dir, "index.html")
    open(md_path, "w").write(render_markdown(name, shared))
    open(html_path, "w").write(render_html(name, shared))

    print(f"\nWrote {md_path}")
    print(f"Wrote {html_path}")
    print(f"  Open {html_path} in a browser")


if __name__ == "__main__":
    main()
