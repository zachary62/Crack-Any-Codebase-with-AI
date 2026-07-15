"""Write the technical-but-friendly copy that wraps a chapter's HTML page.

Every chapter's page is a stack of dense analysis panels. This helper asks the
model, in one call, for two kinds of "big picture" copy:

  - a page **welcome**: a sharp, specific technical read on what this codebase
    is and what it reveals (think "a multi-tenant scheduling system with audit
    trails, granular access control, and per-seat billing"), and
  - a short **intro for each section**: one or two concrete sentences before the
    cards, saying what that section shows and the thing worth noticing.

The register is a knowledgeable colleague giving a crisp rundown — specific and
technical, but friendly and clear. Not a pep talk, not marketing. Both are
grounded in the real findings, so the page reads as this repo's story.
"""
import re

from .call_llm import call_llm

_PROMPT = """You are a senior engineer writing the overview at the top of a page
that maps {what} for a codebase called "{name}". Your reader is another engineer
who just opened this repo — smart and capable, and they want the real technical
picture fast, not a pep talk.

What the analysis actually found about {name}:
{facts}

Write markdown using ONLY these `## ` headers, in this order:

## Welcome
2-3 sentences that state, specifically and technically, what {name} is and what
this codebase reveals. Lead with the subject itself — "{name} is…", "The schema
reveals…", "The API is…" — NOT with "This page/document maps…". Name the real
architectural characteristics the analysis surfaced — e.g. "a multi-tenant
scheduling system with audit trails, granular access control, and per-seat
billing." Friendly and clear, but dense with real detail. This paragraph is the
page's headline summary, so make it stand on its own. NO greetings, no "welcome
to the team", no hype.

Then one block per section below. Use each section's EXACT name as a `## `
header, and under it write ONE or TWO sentences that say, concretely, what that
section shows and the specific thing worth noticing — grounded in the findings,
technical but easy to read. Here are the headers to use, in order:
{headers}

The sections and what each contains:
{sections}

Rules: write like a knowledgeable colleague giving a crisp rundown — specific,
technical, and friendly, never chatty or salesy. Prefer concrete nouns (tables,
endpoints, migrations, transactions, indexes) over adjectives. Explain a term in
a few words only if a junior engineer would miss it. Precise technical
descriptors are good ("multi-tenant", "normalized", "idempotent", "audit
trail"); empty marketing words are banned ("seamless", "powerful", "leverage",
"cutting-edge", "world-class", "robust" when it means nothing). No greetings, no
bullet lists, no sub-headers of your own."""


def write_overview(name, what, sections, facts=""):
    """Return {"welcome": md, "intros": {section_title: md}}.

    name     : the repo / product name
    what     : one clause naming what this page maps ("a database schema…")
    sections : list of (title, gist) tuples, in page order. `title` must match
               the section label the renderer uses.
    facts    : the real findings, so the copy is specific to this repo.
    """
    titles = [t for t, _ in sections]
    slist = "\n".join(f"- {t}: {g}" for t, g in sections)
    headers = "\n".join(f"## {t}" for t in titles)
    raw = call_llm(_PROMPT.format(
        name=name, what=what, facts=facts.strip() or "(no extra facts)",
        sections=slist, headers=headers))

    blocks = {}
    for m in re.finditer(r'^##[ \t]+(.+?)[ \t]*\n(.*?)(?=^##[ \t]|\Z)', raw, re.MULTILINE | re.DOTALL):
        blocks[m.group(1).strip().lower()] = m.group(2).strip()

    return {
        "welcome": blocks.get("welcome", ""),
        # fall back to the plain gist if the model skipped a section header
        "intros": {t: blocks.get(t.lower(), g) for t, g in sections},
    }
