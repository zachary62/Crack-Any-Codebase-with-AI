"""Shared plumbing for the LLM-calling nodes in every chapter.

Each chapter's `nodes.py` used to redefine the same handful of helpers — fill a
prompt's `{slots}`, pull a fenced ```json / ```yaml / ```mermaid block, and retry
a structured call when a flaky model drops a field. They're identical across
chapters and are infrastructure, not teaching content, so they live here once.

The chapter-specific *analysis* nodes (SchemaTour, TraceFlows, …) stay in each
chapter's `nodes.py`, where a reader expects to find them.
"""
import json
import os
import re

import yaml

from .call_llm import call_llm


def read_prompt(prompts_dir, name):
    """Read a prompt file. `prompts/` stays the source of truth for every prompt."""
    return open(os.path.join(prompts_dir, name)).read()


def fill(template, **kwargs):
    """Fill {key} slots by literal replacement.

    Unlike str.format, this leaves the prompts' literal JSON/Mermaid examples
    (which contain `{ }`) untouched, so the prompt files stay clean copies."""
    for k, v in kwargs.items():
        template = template.replace("{" + k + "}", str(v))
    return template


def extract_mermaid(md, kind=None):
    """Pull the first ```mermaid block (optionally of a given diagram type)."""
    for m in re.finditer(r"```mermaid\s*\n(.*?)```", md or "", re.DOTALL):
        body = m.group(1).strip()
        if kind is None or body.startswith(kind):
            return body
    return ""


def parse_json(text):
    """Decode the first JSON value in a reply. Starts after a ```json fence if
    present, but uses raw_decode (not a closing-fence regex) so a nested code or
    ```mermaid block inside a string value can't truncate the parse. Raises so a
    bad reply retries."""
    m = re.search(r"```json[ \t]*\n", text)
    search = text[m.end():] if m else text
    decoder = json.JSONDecoder()
    for i, ch in enumerate(search):
        if ch in "[{":
            try:
                obj, _ = decoder.raw_decode(search[i:])
                return obj
            except ValueError:
                continue
    raise AssertionError(f"No JSON found in LLM response. Got:\n{text[:500]}")


def parse_yaml(text):
    """Extract and parse a ```yaml fenced block. Raises so a bad reply retries."""
    m = re.search(r"```yaml\s*\n(.*?)```", text, re.DOTALL)
    assert m, f"LLM response missing ```yaml fence. Got:\n{text[:500]}"
    return yaml.safe_load(m.group(1))


def json_call(prompt, normalize, retries=4):
    """Call the model, parse its JSON, and validate/normalize it.

    On a bad or incomplete reply (a flaky model occasionally drops a required
    field on a very large prompt), retry with a changed prompt tail — which both
    dodges the response cache (so the retry is genuinely fresh, not a replay of
    the cached miss) and nudges the model to return the whole schema. Network
    errors are NOT caught here; they bubble up to the node's own max_retries."""
    last = None
    for k in range(retries):
        tail = "" if k == 0 else f"\n\nReturn COMPLETE JSON with every required top-level field. (retry {k})"
        try:
            return normalize(parse_json(call_llm(prompt + tail)))
        except (AssertionError, ValueError, KeyError, json.JSONDecodeError) as e:
            last = e
    raise AssertionError(f"json_call gave up after {retries} tries. Last error: {last}")


def yaml_call(prompt, normalize, retries=4):
    """Like json_call, but for YAML replies (retry nudges the model to fix its
    quoting — an unescaped quote inside a quoted string is the common failure)."""
    last = None
    for k in range(retries):
        tail = "" if k == 0 else (
            f"\n\nReturn VALID YAML: put every string value in double quotes and "
            f"escape any double quote inside it as \\\". (retry {k})")
        try:
            return normalize(parse_yaml(call_llm(prompt + tail)))
        except (AssertionError, yaml.YAMLError, ValueError, KeyError) as e:
            last = e
    raise AssertionError(f"yaml_call gave up after {retries} tries. Last error: {last}")
