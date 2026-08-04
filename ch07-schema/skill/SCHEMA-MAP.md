# Skill: Schema Map

Agent equivalent of Chapter 7's schema reader. Drop into `.claude/skills/schema-map/SKILL.md` (Claude Code) or paste into a Cursor rule.

---
name: schema-map
description: Read a codebase's schema as a map of the business, not an inventory. Find the schema file, tour it as a story with an ERD, trace user actions across tables, deep-dive columns and indexes, and mine the migration history. Tables are nouns, foreign keys are relationships, indexes are the hot queries.
---

When the user asks "what does this app store", "what's the data model", or anything about the schema, run these four views in order. The prompts are the chapter; use the exact rules in each.

## First, find the schema file

The schema is almost never a file called `schema`. Look, in order:

| Stack | File | What you're reading |
|---|---|---|
| Prisma (Node/TS) | `**/schema.prisma` | one typed DSL file of `model` blocks |
| Rails (Ruby) | `db/schema.rb` | one auto-generated file |
| Django (Python) | `**/models.py` | classes inheriting `models.Model` |
| SQLAlchemy | `**/models.py` or `**/schema.py` | classes with `Column(...)` |
| Raw SQL | `**/migrations/*.sql`, `schema.sql` | the truth, spread across files |
| Library / CLI (no DB) | `types.ts`, `config.schema.json` | core types, or a config schema |

Don't read it top to bottom (it's alphabetical). Find the **spine** — the table with the most incoming foreign keys — and follow its keys one hop out. Those ~6 tables explain 80% of the product.

## Pipeline

### 1. Tour + ERD (§7.4)

Paste the whole schema into [`../prompts/schema-tour.md`](../prompts/schema-tour.md). Output: the product name, a one-line surprise, a Mermaid `erDiagram` of the ~20 core tables, and a 6-8 step story that introduces them in the order a new developer meets the product. The story explains the *reasoning*; the ERD shows the *shape*. Ask for both.

### 2. Trace user actions (§7.5)

Feed the schema + the tour's ~20 tables to [`../prompts/trace-flows.md`](../prompts/trace-flows.md). Output: 3-6 real user actions, each a numbered trace of which tables are read, written, and which external services are called, in runtime order. This exposes the read/write order and failure modes a static schema hides (e.g. which step is outside the transaction).

### 3. Deep-dive columns + indexes (§7.5)

For the same ~20 tables, use [`../prompts/table-deep-dive.md`](../prompts/table-deep-dive.md), **a few tables at a time** (a single call for 20 detailed cards overflows the output budget). Output per table: the interesting columns (skip auto-IDs/timestamps), 2-5 takeaways, the composite `@@index` lines and the query each makes fast, and one honest line of critique. Columns are decisions; indexes are the hot queries.

### 4. Mine the migration history (§7.6)

Feed the timestamped migration folder names to [`../prompts/migration-acts.md`](../prompts/migration-acts.md). Output: 4-6 named acts, each a product era. The migration log dates what the live schema flattens — e.g. a twenty-month gap between "Teams" and "Organizations" marks the pivot from startups to enterprise. **Skip this if the history is squashed** (few migrations in an old repo) — an LLM will invent a fictional roadmap. Fall back to `git log --follow` on the schema file.

## Output format

Write to `docs/schema-map.md` in the target repo: the ERD + tour, the flows, the per-table deep dive, then the migration acts. Ask the user which table or flow to expand.

## Cardinal rules

- **Read the schema as a map of the business.** Tables are nouns, foreign keys are relationships, enums are state machines, indexes are the hot queries.
- **Every claim cites the schema.** A column name, an index, a table.
- **Watch the two invisible rules:** normalization (is a fact stored once, or copied for read speed?) and tenancy (what keeps one customer's rows out of another's query — often a single `WHERE`).
- **Write for a beginner.** Gloss every term the first time; no brochure words.
