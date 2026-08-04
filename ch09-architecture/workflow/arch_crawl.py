"""Assemble a compact 'architecture bundle' from a repo's four sources (§9.2).

An architecture never lives in one file; you overlay four sources:
  compose / Procfile / k8s   the services the team RUNS
  .env (names only)          the external services it's configured to CALL
  IaC (*.tf)                 the managed cloud resources underneath
  application code           the imports that PROVE a call is live

Feeding a 600k-line repo whole is impossible, so we build a bundle small enough
for one LLM pass but dense enough to inventory the architecture: the config
files in full, env var NAMES (never values), the union of package.json
dependencies (which name every SDK), the integration directories, and the SDK
`import` lines found by `git grep` (real file paths, proof a connection is live).
Nothing here calls an LLM.
"""
import json
import os
import re
import subprocess

SKIP_DIRS = frozenset({
    '.git', '.hg', '.svn', 'node_modules', 'dist', 'build', '.next', '.nuxt',
    'target', 'vendor', 'venv', '.venv', '__pycache__', '.cache', 'coverage',
    '.turbo', '.yarn', 'test', 'tests', '__tests__',
})

GATEWAY_NAMES = frozenset({
    'kong.yml', 'kong.yaml', 'nginx.conf', 'vercel.json', 'netlify.toml',
    'next.config.js', 'next.config.mjs', 'next.config.ts', 'fly.toml',
    'render.yaml', 'railway.json', 'Procfile',
})

# SDK / client imports that name an external node. Kept broad but specific.
SDK_RE = (r"(stripe|twilio|@?aws-sdk|aws-sdk|googleapis|@google-cloud|ioredis|"
          r"'redis'|\"redis\"|nodemailer|@sendgrid|resend|@slack|slack|openai|"
          r"@sentry|@prisma/client|mongodb|mysql2?|pg|kafkajs|bullmq|amqplib|"
          r"@aws-sdk/client-s3|boto3|sib-api|mailgun|postmark|hubspot|"
          r"@salesforce|algolia|elastic|pusher|ably|firebase)")


def _walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        yield dirpath, dirnames, filenames


def _read(path, limit=200_000):
    try:
        return open(path, encoding='utf-8', errors='replace').read()[:limit]
    except OSError:
        return ""


def _env_names(text):
    """Var NAMES only — never the secret values."""
    names = []
    for line in text.splitlines():
        m = re.match(r'\s*(?:export\s+)?([A-Z][A-Z0-9_]+)\s*=', line)
        if m:
            names.append(m.group(1))
    return names


def _classify(rel):
    p = rel.replace(os.sep, '/')
    base = os.path.basename(p).lower()
    if base.startswith('docker-compose') or base in ('compose.yaml', 'compose.yml'):
        return 'compose'
    if os.path.basename(p) == 'Procfile':
        return 'gateway'
    if base.startswith('.env'):
        return 'env'
    if base.endswith('.tf') or base.endswith('.tfvars'):
        return 'iac'
    if os.path.basename(p) in GATEWAY_NAMES:
        return 'gateway'
    if base == 'package.json':
        return 'package'
    if base.endswith(('.yaml', '.yml')) and any(
            seg in p for seg in ('/k8s/', '/kubernetes/', '/manifests/', '/deploy/', '/charts/', '/helm/')):
        return 'k8s'
    return None


def _sdk_grep(repo, max_lines=400):
    """SDK import lines with file:line, via `git grep` (fast). Real proof + paths."""
    try:
        raw = subprocess.check_output(
            ["git", "-C", repo, "grep", "-nE",
             r"(import .*from ['\"]" + SDK_RE + r"|require\(['\"]" + SDK_RE + r"|new (Stripe|Twilio|Redis|S3Client))",
             "--", "*.ts", "*.tsx", "*.js", "*.py", "*.go"],
            text=True, errors="replace", stderr=subprocess.DEVNULL,
        )
    except Exception:
        return ""
    lines = [l for l in raw.splitlines() if l.strip()]
    return "\n".join(lines[:max_lines])


def _integration_dirs(repo):
    """The long tail of integrations — one dir per external service."""
    for cand in ("packages/app-store", "app-store", "packages/integrations", "integrations"):
        full = os.path.join(repo, cand)
        if os.path.isdir(full):
            subs = sorted(d for d in os.listdir(full)
                          if os.path.isdir(os.path.join(full, d)) and not d.startswith(('_', '.')))
            if subs:
                return cand, subs
    return None, []


def build_bundle(repo, max_chars=500_000):
    """Return (bundle_text, stats)."""
    buckets = {k: [] for k in ('compose', 'k8s', 'gateway', 'iac')}
    env_names, deps = set(), {}
    for dirpath, _dn, filenames in _walk(repo):
        for f in filenames:
            rel = os.path.relpath(os.path.join(dirpath, f), repo)
            kind = _classify(rel)
            if kind is None:
                continue
            full = os.path.join(dirpath, f)
            if kind == 'env':
                env_names.update(_env_names(_read(full, 40_000)))
            elif kind == 'package':
                try:
                    data = json.loads(_read(full, 200_000))
                    for grp in ('dependencies', 'devDependencies'):
                        deps.update(data.get(grp, {}))
                except (ValueError, OSError):
                    pass
            else:
                buckets[kind].append((rel, _read(full)))

    parts = []
    for kind, label in (('compose', 'PROCESS DECLARATION (compose / k8s)'),
                        ('k8s', 'KUBERNETES MANIFESTS'),
                        ('gateway', 'GATEWAY / PLATFORM CONFIG'),
                        ('iac', 'INFRASTRUCTURE-AS-CODE (Terraform)')):
        for rel, text in buckets[kind]:
            if text.strip():
                parts.append(f"===== {label}: {rel} =====\n{text}\n")

    if env_names:
        parts.append("===== ENVIRONMENT VARIABLE NAMES (values omitted) =====\n"
                     + "\n".join(sorted(env_names)) + "\n")
    if deps:
        parts.append("===== PACKAGE DEPENDENCIES (name @ version) =====\n"
                     + "\n".join(f"{k} @ {v}" for k, v in sorted(deps.items())) + "\n")

    idir, isubs = _integration_dirs(repo)
    if isubs:
        parts.append(f"===== INTEGRATION DIRECTORIES ({idir}, {len(isubs)} total) =====\n"
                     + ", ".join(isubs) + "\n")

    sdk = _sdk_grep(repo)
    if sdk:
        parts.append("===== SDK IMPORT LINES (git grep — file:line: import) =====\n" + sdk + "\n")

    bundle = "\n".join(parts)[:max_chars]
    stats = {
        "config_files": sum(len(v) for v in buckets.values()),
        "env_vars": len(env_names),
        "deps": len(deps),
        "integrations": len(isubs),
        "sdk_lines": sdk.count("\n") + 1 if sdk else 0,
    }
    return bundle, stats
