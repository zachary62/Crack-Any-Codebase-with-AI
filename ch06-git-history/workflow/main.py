"""CLI for Chapter 6's git-history reader.

Usage:
    python main.py path/to/repo
    python main.py path/to/repo --out ../output/ghost-history
    python main.py path/to/repo --max-graves 4 --grave-min-files 10

Point it at any local clone (`git clone https://github.com/TryGhost/Ghost`).
It reads the log only; nothing in the repo changes. Output is a timeline of
named eras (each with its cast and mood) plus a graveyard of killed features,
written as both index.md and a self-contained index.html.
"""
import argparse, os
from flow import create_history_flow
from render import render_html, render_markdown


def main():
    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=__doc__)
    ap.add_argument("repo_path")
    ap.add_argument("--out", default=None)
    ap.add_argument("--max-graves", type=int, default=6,
                    help="most graveyard entries to write (default 6)")
    ap.add_argument("--grave-min-files", type=int, default=8,
                    help="a deletion counts as a killed feature at this many files (default 8)")
    args = ap.parse_args()

    assert os.path.isdir(os.path.join(args.repo_path, ".git")) or os.path.isdir(args.repo_path), \
        f"{args.repo_path} is not a directory"

    name = os.path.basename(os.path.abspath(args.repo_path).rstrip('/'))
    base_out = args.out or os.path.join(os.path.dirname(__file__), "..", "output", f"{name}-history")
    os.makedirs(base_out, exist_ok=True)

    shared = {
        "repo_path": args.repo_path,
        "max_graves": args.max_graves,
        "grave_min_files": args.grave_min_files,
    }
    create_history_flow().run(shared)

    md_path = os.path.join(base_out, "index.md")
    html_path = os.path.join(base_out, "index.html")
    open(md_path, "w").write(render_markdown(name, shared))
    open(html_path, "w").write(render_html(name, shared))

    print(f"\nWrote {md_path}")
    print(f"Wrote {html_path}")
    print(f"  Open {html_path} in a browser")


if __name__ == "__main__":
    main()
