"""Find and read a repo's schema, plus its migration history.

The schema is almost never a file literally called `schema` (§7.3). Most repos
follow one of a few conventions, so we look for them in priority order:

  Prisma (Node/TS)     packages/**/schema.prisma        one typed DSL file
  Rails (Ruby)         db/schema.rb                     one auto-generated file
  Raw SQL              schema.sql                        one dumped file
  Django / SQLAlchemy  **/models.py                      classes, many files

`find_schema` returns the single most-schema-like text it can (concatenating the
Django/SQLAlchemy model files when there's no single-file schema). `find_migrations`
returns the timestamped migration names — the chronological record §7.6 mines.

Everything here is plain filesystem walking; nothing calls an LLM.
"""
import os
import re

# Directories that never hold a schema (mirrors utils.crawl's skip set, minus
# `migrations`, which we DO want to find).
SKIP_DIRS = frozenset({
    '.git', '.hg', '.svn', 'node_modules', 'dist', 'build', '.next', '.nuxt',
    'target', 'vendor', 'venv', '.venv', '__pycache__', '.cache', 'coverage',
    'test', 'tests', '__tests__', 'examples', 'docs', '.turbo',
})

TIMESTAMP_RE = re.compile(r'^\d{6,}[_-]')  # 20210605225044_init, 0001_initial, ...


def _walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        yield dirpath, dirnames, filenames


def _read(path):
    try:
        return open(path, encoding='utf-8', errors='replace').read()
    except OSError:
        return ""


def find_schema(repo, override=None):
    """Return {kind, path(s), text}. `override` forces a specific file."""
    if override:
        p = override if os.path.isabs(override) else os.path.join(repo, override)
        return {"kind": "override", "path": os.path.relpath(p, repo), "text": _read(p)}

    prisma, rails, sql, models = [], [], [], []
    for dirpath, _dirnames, filenames in _walk(repo):
        for f in filenames:
            full = os.path.join(dirpath, f)
            if f == "schema.prisma":
                prisma.append(full)
            elif f == "schema.rb" and os.path.basename(dirpath) == "db":
                rails.append(full)
            elif f == "schema.sql":
                sql.append(full)
            elif f == "models.py":
                models.append(full)

    if prisma:
        # Prefer the largest schema.prisma (the app's, not a package fixture).
        path = max(prisma, key=lambda p: os.path.getsize(p))
        return {"kind": "prisma", "path": os.path.relpath(path, repo), "text": _read(path)}
    if rails:
        path = rails[0]
        return {"kind": "rails", "path": os.path.relpath(path, repo), "text": _read(path)}
    if sql:
        path = max(sql, key=lambda p: os.path.getsize(p))
        return {"kind": "sql", "path": os.path.relpath(path, repo), "text": _read(path)}
    if models:
        # No single-file schema: concatenate the model files (Django/SQLAlchemy).
        models = sorted(models, key=lambda p: os.path.getsize(p), reverse=True)[:40]
        parts = [f"# ===== {os.path.relpath(p, repo)} =====\n{_read(p)}" for p in models]
        return {"kind": "models", "path": f"{len(models)} models.py files", "text": "\n\n".join(parts)}

    return {"kind": None, "path": None, "text": ""}


def find_migrations(repo):
    """Return (dir_relpath, [names oldest-first]) for the repo's migration history.

    Handles Prisma (a `migrations/` dir of timestamped subfolders), Rails
    (`db/migrate/*.rb`), and Django (`**/migrations/0*.py`). Picks the migration
    directory with the most timestamped entries."""
    best = None  # (count, reldir, names)
    for dirpath, _dirnames, filenames in _walk(repo):
        base = os.path.basename(dirpath)
        if base not in ("migrations", "migrate"):
            continue
        entries = sorted(os.listdir(dirpath))
        names = [e for e in entries if TIMESTAMP_RE.match(e)]
        # Prisma: subdirs. Rails/Django: files. Strip a file extension for display.
        names = [os.path.splitext(n)[0] if "." in n else n for n in names]
        names = [n for n in names if n and not n.startswith("__")]
        if len(names) > (best[0] if best else 0):
            best = (len(names), os.path.relpath(dirpath, repo), names)
    if not best:
        return None, []
    return best[1], best[2]
