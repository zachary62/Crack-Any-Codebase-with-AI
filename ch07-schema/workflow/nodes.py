"""Ch7 nodes: project a flat schema file into four focused views.

One node per prompt in the chapter (§7.4-7.6):
  1. FindSchema     locate + read the schema file and migration history
  2. SchemaTour     narrate it as a story + a Mermaid ERD (the spine)
  3. TraceFlows     trace 3-6 user actions across the tables
  4. TableDeepDive  read the columns + indexes of the ~20 core tables
  5. MigrationActs  cluster the migration folder into product eras

SchemaTour runs first because its ERD names the ~20 core tables that the flows
and deep-dive passes then reuse. Each LLM node uses Node(max_retries=3, wait=2).
"""
import os
import re
import sys

from pocketflow import Node

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils import call_llm, read_prompt, fill, extract_mermaid  # noqa: E402
import schema_find as sf  # noqa: E402

PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')


def load_prompt(name):
    return read_prompt(PROMPTS_DIR, name)


def schema_table_names(schema_text):
    """Every table/model name declared in the schema, lowercased, for filtering."""
    names = set()
    for pat in (r'\bmodel\s+(\w+)', r'CREATE\s+TABLE\s+"?(\w+)"?',
                r'class\s+(\w+)\s*\([^)]*Model'):
        names |= {m.group(1).lower() for m in re.finditer(pat, schema_text, re.IGNORECASE)}
    return names


def tables_from_erd(erd, known):
    """Ordered, de-duplicated entity names appearing in an erDiagram's
    relationship lines, kept only if they match a real table in the schema."""
    seen, out = set(), []
    for a, b in re.findall(r'^\s*(\w+)\s+[|}o{.\-]+\s+(\w+)\s*:', erd, re.MULTILINE):
        for name in (a, b):
            if name.lower() in known and name.lower() not in seen:
                seen.add(name.lower())
                out.append(name)
    return out


def tables_from_headers(md):
    """Fallback: backticked table names inside `### Step ... (`A`, `B`)` headers."""
    seen, out = set(), []
    for line in md.splitlines():
        if line.startswith("###"):
            for name in re.findall(r'`(\w+)`', line):
                if name.lower() not in seen:
                    seen.add(name.lower())
                    out.append(name)
    return out


class FindSchema(Node):
    def prep(self, shared):
        return shared["repo_path"], shared.get("schema_override")

    def exec(self, inputs):
        repo, override = inputs
        schema = sf.find_schema(repo, override)
        mig_dir, mig_names = sf.find_migrations(repo)
        return schema, mig_dir, mig_names

    def post(self, shared, prep_res, exec_res):
        schema, mig_dir, mig_names = exec_res
        assert schema["text"], (
            "No schema file found. Point --schema at it "
            "(e.g. packages/prisma/schema.prisma).")
        shared["schema"] = schema["text"]
        shared["schema_kind"] = schema["kind"]
        shared["schema_path"] = schema["path"]
        shared["migration_dir"] = mig_dir
        shared["migration_names"] = mig_names
        print(f"  Schema: {schema['path']} ({schema['kind']}, {len(schema['text']):,} chars); "
              f"{len(mig_names)} migrations")


class SchemaTour(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return fill(load_prompt("schema-tour.md"), schema=shared["schema"])

    def exec(self, prompt):
        md = call_llm(prompt).strip()
        assert "###" in md, "tour produced no `###` step cards"
        return md

    def post(self, shared, prep_res, exec_res):
        md = exec_res
        prod = re.search(r"\*\*Product:\*\*\s*(.+)", md)
        one = re.search(r"\*\*Schema one-?liner:\*\*\s*(.+)", md, re.IGNORECASE)
        erd = extract_mermaid(md, "erDiagram")
        known = schema_table_names(shared["schema"])
        tables = tables_from_erd(erd, known) or tables_from_headers(md)

        shared["product_name"] = prod.group(1).strip() if prod else os.path.basename(shared["repo_path"])
        shared["one_liner"] = one.group(1).strip() if one else ""
        shared["erd"] = erd
        shared["tour_md"] = md
        shared["table_list"] = tables
        print(f"  Tour: {len(tables)} core tables"
              + (f" (ERD: {len(erd.splitlines())} lines)" if erd else " (no ERD parsed)"))


class TraceFlows(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return fill(load_prompt("trace-flows.md"),
                    schema=shared["schema"],
                    table_list=", ".join(f"`{t}`" for t in shared["table_list"]))

    def exec(self, prompt):
        md = call_llm(prompt).strip()
        assert "###" in md, "flows produced no `###` action cards"
        return md

    def post(self, shared, prep_res, exec_res):
        shared["flows_md"] = exec_res
        print(f"  Flows: {exec_res.count(chr(35) + '##')} actions traced")


class TableDeepDive(Node):
    """Review the core tables in small batches, not all at once.

    A single call for 20 detailed cards overflows the model's output budget
    (a chatty model spends most of it 'thinking' and truncates the cards
    mid-table). Batching a few tables per call keeps every card complete."""
    BATCH = 4

    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return {
            "schema": shared["schema"],
            "product_name": shared["product_name"],
            "one_liner": shared["one_liner"],
            "tables": shared["table_list"],
            "template": load_prompt("table-deep-dive.md"),
        }

    def exec(self, ctx):
        tables = ctx["tables"]
        cards = []
        for i in range(0, len(tables), self.BATCH):
            batch = tables[i:i + self.BATCH]
            print(f"  Deep dive: tables {i+1}-{i+len(batch)} of {len(tables)}")
            prompt = fill(ctx["template"],
                          schema=ctx["schema"],
                          product_name=ctx["product_name"],
                          one_liner=ctx["one_liner"],
                          table_list=", ".join(f"`{t}`" for t in batch))
            md = call_llm(prompt).strip()
            assert "###" in md, f"deep-dive produced no `###` cards for {batch}"
            # Keep only from the first card header on, so any preamble is dropped
            # and the batches concatenate into one clean stream of cards.
            cards.append(md[md.index("###"):])
        return "\n\n".join(cards)

    def post(self, shared, prep_res, exec_res):
        shared["deepdive_md"] = exec_res
        print(f"  Deep dive: {exec_res.count(chr(35) + '##')} tables reviewed")


class MigrationActs(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return shared["migration_names"]

    def exec(self, migration_names):
        if len(migration_names) < 4:
            # Too few (or squashed) to reconstruct a roadmap — §7.6 says don't
            # ask the LLM to hallucinate one.
            return None
        prompt = fill(load_prompt("migration-acts.md"),
                      migration_names="\n".join(migration_names))
        return call_llm(prompt).strip()

    def post(self, shared, prep_res, exec_res):
        shared["migration_md"] = exec_res
        if exec_res:
            print(f"  Migrations: {exec_res.count(chr(35) + '##')} acts")
        else:
            print(f"  Migrations: skipped ({len(prep_res)} migrations, too few to cluster)")


def overview_spec(shared):
    """The chapter-specific bits the shared OverviewNode needs (see utils/nodes.py)."""
    name = shared.get("product_name") or os.path.basename(shared["repo_path"].rstrip("/"))
    return {
        "name": name,
        "what": "a database schema as a map of the business",
        "sections": [
            ("The tour", "the schema told as a story, one cluster of tables at a time, with a diagram"),
            ("The flows", "which tables a single user action reads and writes, in order"),
            ("Table deep dive", "the columns and indexes that carry each table's real decisions"),
            ("Migration history", "the product eras the live schema hides"),
        ],
        "facts": (f"{name}: {shared.get('one_liner', '')}. "
                  f"{len(shared.get('table_list', []))} core tables, "
                  f"{len(shared.get('migration_names', []))} migrations."),
    }
