# Skill: Architecture Map

Agent equivalent of Chapter 9's architecture reader. Drop into `.claude/skills/architecture-map/SKILL.md` (Claude Code) or paste into a Cursor rule.

---
name: architecture-map
description: Map a multi-service system as a graph of programs and the wires between them. Inventory every node sorted by who runs it (run/rent/call/client), open each box to its real tech stack, and trace the core request hop by hop. The edge type, not the node, is what fails.
---

When the user asks "what talks to what", "how is this deployed", or anything about the service graph, run these three passes.

## First: one process, or many?

A library, a CLI, or a single-binary tool (PocketBase) is **one process** — its "architecture" is the module graph inside it (read ch13 instead). This skill is for systems that boot several programs and wire them together. "This is one box" is a finding, not a dead end.

## Then: overlay the four sources

No single file holds the architecture. Overlay four, each blind to the others:

| Source | What it shows | What it hides |
|---|---|---|
| `docker-compose.yml` / Procfile / k8s | the services you **run** | every external API you call |
| `.env` (names only) | the services you're configured to **call** | which keys are still live |
| application code (SDK imports) | the calls that are actually **live** | anything provisioned but unused |
| IaC (`*.tf`) | the managed cloud resources | the app processes inside them |

## Pipeline

### 1. Inventory + graph (§9.3)

Feed the four sources to [`../prompts/inventory.md`](../prompts/inventory.md). Output: a one-line shape verdict, then every node sorted into four **bands** — `RUN` (your code, your machine), `RENT` (vendor code, your machine), `CALL` (vendor code, vendor machine), `CLIENT` (your code, their machine) — each with a stable ID and its downstream edges tagged `(sync|async, internal|public)`, then a Mermaid `flowchart LR` with one subgraph per band. The band tells you what you can do when it breaks: edit RUN, reconfigure RENT, only retry/route-around CALL.

### 2. Open each box (§9.4)

Feed the sources + the inventory to [`../prompts/tech-stack.md`](../prompts/tech-stack.md). Output: per node, what it is in plain English, what it's actually built from (the specific libraries/protocols), and the `file:line` that proves it. This is where "the queue" becomes "a Postgres `Task` table drained by a cron route, three retries per row."

### 3. Trace the core request (§9.5)

Feed the sources + the inventory to [`../prompts/trace-request.md`](../prompts/trace-request.md). Output: the product's core action traced hop by hop (each hop tagged *user-waits* or *queued*, with a `file:line`), then 3+ variants (free vs. paid, guest vs. member) that add or drop nodes. The variants prove the execution graph is assembled from runtime state (database rows), not fixed in a file.

## Output format

Write to `docs/architecture-map.md` in the target repo: the graph + inventory, the per-node tech stack, then the trace. Ask the user which node or path to expand.

## Cardinal rules

- **The edge type, not the node, is what fails.** Tag every wire sync/async and internal/public.
- **Code is the only proof.** Treat compose and `.env` as claims; an SDK import is evidence a connection is live.
- **Be specific, not vague.** "A `Task` table drained by a cron job, three retries," never "event orchestration platform." No brochure words.
- **Ask the three follow-ups the graph hides:** decomposition (why N deploy units?), failure isolation (if one node dies, what fraction of users notice?), and build-vs-buy (why run this instead of renting it?).
