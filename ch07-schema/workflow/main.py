"""CLI for Chapter 7's schema reader.

Usage:
    python main.py path/to/repo
    python main.py path/to/repo --out ../output/cal.com-schema
    python main.py path/to/repo --schema packages/prisma/schema.prisma

It finds the schema file itself (Prisma, Rails, raw SQL, or Django/SQLAlchemy
models). Pass --schema to point it at a specific file if the guess is wrong.
Output is four views — a tour with an ERD, user-action flows, a per-table deep
dive, and the migration history — as a self-contained index.html plus index.md.
"""
import argparse, os
from flow import create_schema_flow
from render import render_html, render_markdown


def main():
    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=__doc__)
    ap.add_argument("repo_path")
    ap.add_argument("--out", default=None)
    ap.add_argument("--schema", default=None,
                    help="path to the schema file, relative to the repo (overrides autodetect)")
    args = ap.parse_args()

    assert os.path.isdir(args.repo_path), f"{args.repo_path} is not a directory"

    name = os.path.basename(os.path.abspath(args.repo_path).rstrip('/'))
    out_dir = args.out or os.path.join(os.path.dirname(__file__), "..", "output", f"{name}-schema")
    os.makedirs(out_dir, exist_ok=True)

    shared = {"repo_path": args.repo_path, "schema_override": args.schema}
    create_schema_flow().run(shared)

    md_path = os.path.join(out_dir, "index.md")
    html_path = os.path.join(out_dir, "index.html")
    open(md_path, "w").write(render_markdown(name, shared))
    open(html_path, "w").write(render_html(name, shared))

    print(f"\nWrote {md_path}")
    print(f"Wrote {html_path}")
    print(f"  Open {html_path} in a browser")


if __name__ == "__main__":
    main()
