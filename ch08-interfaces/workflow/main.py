"""CLI for Chapter 8's interface reader.

Usage:
    python main.py path/to/repo
    python main.py path/to/repo --out ../output/cal.com-interfaces

It finds the route/surface files itself (Rails, Django, Next.js, tRPC, GraphQL,
gRPC) and produces three views — a feature menu + tour, user-action swimlane
flows, and a per-endpoint sequence diagram — as a self-contained index.html plus
index.md.
"""
import argparse, os

# The feature-menu pass lists every one of a product's ~300 endpoints in one
# reply — far more output than the default cap allows, so a chatty model
# truncates mid-menu. A higher cap costs nothing extra (you're billed for tokens
# generated, not the ceiling). Respect an explicit override.
os.environ.setdefault("LLM_MAX_OUTPUT_TOKENS", "32768")

from flow import create_interface_flow
from render import render_html, render_markdown


def main():
    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=__doc__)
    ap.add_argument("repo_path")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    assert os.path.isdir(args.repo_path), f"{args.repo_path} is not a directory"

    name = os.path.basename(os.path.abspath(args.repo_path).rstrip('/'))
    out_dir = args.out or os.path.join(os.path.dirname(__file__), "..", "output", f"{name}-interfaces")
    os.makedirs(out_dir, exist_ok=True)

    shared = {"repo_path": args.repo_path}
    create_interface_flow().run(shared)

    md_path = os.path.join(out_dir, "index.md")
    html_path = os.path.join(out_dir, "index.html")
    open(md_path, "w").write(render_markdown(name, shared))
    open(html_path, "w").write(render_html(name, shared))

    print(f"\nWrote {md_path}")
    print(f"Wrote {html_path}")
    print(f"  Open {html_path} in a browser")


if __name__ == "__main__":
    main()
