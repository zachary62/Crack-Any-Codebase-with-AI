"""Find a repo's interface: the files that declare its entry points (§8.2).

A route manifest is rarely named `api`; its location is a framework convention.
We collect the surface files across the common conventions:

  Rails            config/routes.rb
  Django           **/urls.py
  Express/Fastify  **/routes.ts, **/router.ts
  Next.js          **/pages/api/**/*.ts, **/app/**/route.ts   (path IS the URL)
  tRPC             **/_router.ts
  GraphQL / gRPC   **/*.graphql, **/*.proto
  Go               **/cmd/*.go

`crawl_routes` concatenates them (capped) into the `{routes}` the prompts read.
`read_files` resolves an LLM-picked list of source paths for the sequence view.
Nothing here calls an LLM.
"""
import os

SKIP_DIRS = frozenset({
    '.git', '.hg', '.svn', 'node_modules', 'dist', 'build', '.next', '.nuxt',
    'target', 'vendor', 'venv', '.venv', '__pycache__', '.cache', 'coverage',
    'test', 'tests', '__tests__', 'examples', 'docs', '.turbo', '.storybook',
})

_TEST_MARKERS = ('.test.', '.spec.', '_test.', '.stories.')
_ROUTE_BASENAMES = frozenset({
    'routes.rb', 'urls.py', 'routes.ts', 'router.ts', 'routes.js', 'router.js',
    'schema.graphql',
})


def _walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        yield dirpath, dirnames, filenames


def is_route_file(rel):
    """True if `rel` (a repo-relative path) declares entry points."""
    p = rel.replace(os.sep, "/")
    base = os.path.basename(p)
    if any(m in base for m in _TEST_MARKERS):
        return False
    if base in _ROUTE_BASENAMES:
        return True
    if base.endswith("_router.ts") or base.endswith(".proto") or base.endswith(".graphql"):
        return True
    if "/pages/api/" in p and p.endswith((".ts", ".js", ".tsx")):
        return True
    if "/app/" in p and base in ("route.ts", "route.js", "route.tsx"):
        return True
    if "/cmd/" in p and p.endswith(".go"):
        return True
    return False


def find_route_files(repo):
    out = []
    for dirpath, _dirnames, filenames in _walk(repo):
        for f in filenames:
            rel = os.path.relpath(os.path.join(dirpath, f), repo)
            if is_route_file(rel):
                out.append(rel)
    return sorted(out)


def _read(path):
    try:
        return open(path, encoding='utf-8', errors='replace').read()
    except OSError:
        return ""


def crawl_routes(repo, max_chars=900_000):
    """Concatenate the surface files with path headers, capped at max_chars.
    tRPC aggregators and Rails/Django manifests come first (they list many
    endpoints per file), so a cap trims single Next.js handlers, not the map."""
    files = find_route_files(repo)

    def priority(rel):
        base = os.path.basename(rel)
        if base in _ROUTE_BASENAMES or base.endswith(("_router.ts", ".proto", ".graphql")):
            return 0  # aggregators / manifests first
        return 1

    files.sort(key=lambda r: (priority(r), r))
    parts, total, kept = [], 0, 0
    for rel in files:
        text = _read(os.path.join(repo, rel))
        if not text.strip():
            continue
        block = f"{'=' * 60}\nFile: {rel}\n{'=' * 60}\n{text}\n"
        if total + len(block) > max_chars:
            continue
        parts.append(block)
        total += len(block)
        kept += 1
    return "\n".join(parts), files, kept


def read_files(repo, paths, max_chars=120_000, max_files=8):
    """Read an LLM-picked list of source paths for the sequence-diagram view.

    Resolves each path exactly if it exists, else by a suffix match against the
    repo (the model often gives a path that's right but for a leading dir)."""
    index = None
    resolved, parts, total = [], [], 0
    for raw in paths[:max_files]:
        rel = raw.strip().strip("`").lstrip("/")
        full = os.path.join(repo, rel)
        if not os.path.isfile(full):
            if index is None:
                index = []
                for dp, dn, fn in _walk(repo):
                    dn[:] = dn  # already filtered by _walk
                    for f in fn:
                        index.append(os.path.relpath(os.path.join(dp, f), repo))
            key = rel.replace(os.sep, "/")
            match = next((r for r in index if r.replace(os.sep, "/").endswith(key)), None)
            if not match:
                continue
            full, rel = os.path.join(repo, match), match
        text = _read(full)
        if not text.strip():
            continue
        block = f"{'=' * 60}\nFile: {rel}\n{'=' * 60}\n{text[:40_000]}\n"
        if total + len(block) > max_chars:
            break
        resolved.append(rel)
        parts.append(block)
        total += len(block)
    return "\n".join(parts), resolved
