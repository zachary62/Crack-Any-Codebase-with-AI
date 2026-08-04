"""Crawl a backend into the six layers a request flows through (§10.3).

Every backend is the same six layers with different names:
  route → middleware → handler → service → database → response

We classify each source file into a layer by its path, report a file count per
layer (so the prompts can lead with a concrete number, not an adjective), and
build a bundle that includes the 'spine' files in full — routing, middleware,
and the response/decorator helpers, where teams write their custom idioms — plus
a size-capped sample of the handler/service/model files. Nothing calls an LLM.
"""
import os
from collections import Counter

SKIP_DIRS = frozenset({
    '.git', '.hg', '.svn', 'node_modules', 'dist', 'build', '.next', '.nuxt',
    'target', 'vendor', 'venv', '.venv', '__pycache__', '.cache', 'coverage',
    '.turbo', '.yarn', 'test', 'tests', '__tests__', 'migrations', 'static',
    'locale', 'docs', 'frontend_tests', 'node_tests',
})
SRC_EXT = ('.py', '.ts', '.tsx', '.js', '.rb', '.go', '.java', '.php')
# Files where teams most often write custom idioms — always included in full.
SPINE_NAMES = ('urls.py', 'rest.py', 'response.py', 'decorator.py', 'decorators.py',
               'middleware.py', 'computed_settings.py', 'routes.rb', 'application_controller.rb')
# Core-action keywords: sample these files first so the trace has the spine endpoint.
CORE_HINTS = ('message', 'send', 'booking', 'book', 'order', 'checkout', 'create',
              'post', 'auth', 'user', 'session', 'event')


def _walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        yield dirpath, dirnames, filenames


def _read(path, limit=45_000):
    try:
        return open(path, encoding='utf-8', errors='replace').read()[:limit]
    except OSError:
        return ""


def classify(rel):
    """Return the layer a file belongs to, or None."""
    p = rel.replace(os.sep, '/').lower()
    base = os.path.basename(p)
    if not p.endswith(SRC_EXT):
        return None
    if any(m in base for m in ('.test.', '.spec.', '_test.', '.stories.')):
        return None
    # Route
    if (base in ('urls.py', 'routes.rb', 'routes.ts', 'router.ts', 'routes.js', 'router.js')
            or base.endswith('_router.ts') or '/pages/api/' in p or '/routes/' in p or '/urls/' in p):
        return 'route'
    # Middleware (incl. decorators and the settings file that lists MIDDLEWARE)
    if ('middleware' in p or base.endswith(('decorator.py', 'decorators.py'))
            or base in ('computed_settings.py',)):
        return 'middleware'
    # Handler
    if '/views/' in p or '/controllers/' in p or '/handlers/' in p or base.endswith(('view.py', 'controller.rb')):
        return 'handler'
    # Service (business logic)
    if '/actions/' in p or '/services/' in p or '/domain/' in p or '/use' in p and 'case' in p:
        return 'service'
    # Database
    if '/models/' in p or base in ('models.py', 'schema.rb') or '/repositories/' in p or '/repository/' in p:
        return 'database'
    # Response
    if 'serializer' in p or '/serializers/' in p or (base.startswith('response') and base.endswith('.py')):
        return 'response'
    return None


def _priority(rel):
    b = os.path.basename(rel).lower()
    return (0 if any(h in b for h in CORE_HINTS) else 1)


def build_bundle(repo, max_chars=650_000, per_layer_sample=18):
    files_by_layer = {k: [] for k in ('route', 'middleware', 'handler', 'service', 'database', 'response')}
    counts = Counter()
    for dirpath, _dn, filenames in _walk(repo):
        for f in filenames:
            rel = os.path.relpath(os.path.join(dirpath, f), repo)
            layer = classify(rel)
            if layer:
                counts[layer] += 1
                files_by_layer[layer].append(rel)

    # Decide what to include: spine layers in full; handlers/services/models sampled.
    include = []
    for layer in ('route', 'middleware', 'response'):
        include += [(layer, r) for r in sorted(files_by_layer[layer])]
    for layer in ('handler', 'service', 'database'):
        ranked = sorted(files_by_layer[layer], key=lambda r: (_priority(r), r))
        include += [(layer, r) for r in ranked[:per_layer_sample]]

    header = "===== LAYER FILE COUNTS (whole repo) =====\n" + "\n".join(
        f"{layer}: {counts[layer]} files"
        for layer in ('route', 'middleware', 'handler', 'service', 'database', 'response')) + "\n"

    parts, total, kept = [header], len(header), 0
    for layer, rel in include:
        text = _read(os.path.join(repo, rel))
        if not text.strip():
            continue
        block = f"\n===== LAYER {layer.upper()}: {rel} =====\n{text}\n"
        if total + len(block) > max_chars:
            continue
        parts.append(block)
        total += len(block)
        kept += 1

    return "".join(parts), {"counts": dict(counts), "included": kept}
