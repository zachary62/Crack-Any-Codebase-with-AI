# Skill: API Map

Agent equivalent of Chapter 8's interface reader. Drop into `.claude/skills/api-map/SKILL.md` (Claude Code) or paste into a Cursor rule.

---
name: api-map
description: Read a codebase's interface — the doors where every change request starts. Find the route manifest, group hundreds of endpoints into a feature menu, trace one user action across services (swimlanes), and diagram one endpoint request-to-response. The surface is 1% of the code but the only part that says what the product does.
---

When the user asks "what endpoints exist", "which handler runs when I click X", or anything about the API surface, run these three views. The prompts are the chapter; use the exact rules in each.

## First, find the route manifest

The file that lists entry points is a framework convention:

| Stack | Where the routes live |
|---|---|
| Rails | `config/routes.rb` |
| Django | `**/urls.py` |
| Express / Fastify | `**/routes.ts`, `**/router.ts` |
| Next.js | `**/pages/api/**`, `**/app/**/route.ts` (path IS the URL) |
| tRPC | `**/_router.ts` |
| GraphQL / gRPC | `**/*.graphql`, `**/*.proto` (one line per operation) |
| Go / CLI | `**/cmd/*.go`, `cobra.Command` / `argparse` trees |
| Library | the public exports (`__init__.py`, `package.json` `main`, `pub` items) |

The surface is ~1% of the lines but the only part that says what the product *does*. A mature codebase mixes conventions (a public REST API next to a private tRPC one) — collect them all.

## Pipeline

### 1. Feature menu + tour (§8.3)

Feed the surface files to [`../prompts/api-menu.md`](../prompts/api-menu.md). Output: a product name + one-line surprise, then one group per feature **sorted by endpoint count, largest first**, listing *every* endpoint with its method, path, and auth tier (public / user / admin), then a 3-6 step tour of the most revealing groups. The public-to-admin ratio is the clearest signal of what the product really is (Cal.com: only ~17% of endpoints are scheduling). This pass produces a long reply — give it a generous output-token budget or it truncates mid-menu.

### 2. Trace a user action (§8.4)

Feed the surface + the feature groups to [`../prompts/trace-action.md`](../prompts/trace-action.md). Output: 4-8 user actions as swimlane flows — the services are lanes, the calls fire left to right. Cover the range: a read-only flow, a write-heavy flow, a scheduled job (no user), an admin flow. Say which lane blocks the spinner and which fire *after* the response. Most actions split into three phases: edge gating, a critical DB section, and an async fan-out.

### 3. Diagram one endpoint (§8.5)

Pick the most illustrative endpoint (one that fans out to several services), read its handler + the functions it calls, and feed them to [`../prompts/endpoint-sequence.md`](../prompts/endpoint-sequence.md). Output: a Mermaid `sequenceDiagram` with one lifeline per service, plus a numbered message list with `file:line` refs. Find the response arrow first — it splits work the user waits for from the async fan-out that can fail without them knowing. **Every participant must be declared** (external services too); never reference an inline participant, or the diagram won't parse.

## Output format

Write to `docs/api-map.md` in the target repo: the feature menu, the flows, then the sequence diagram. Ask the user which endpoint or flow to expand.

## Cardinal rules

- **Read the surface as a product menu, not a file listing.** Group by feature, sort by count, tag every endpoint's auth tier.
- **Start at the door.** Every service call, query, and external API call is downstream of some endpoint; start there and every downstream call arrives with its context.
- **Watch three contracts a diagram hides:** idempotency (what stops a double-click double-booking?), failure paths (does a crash after COMMIT lose the fan-out?), and concurrency (what resolves a write race — a lock, a version, or a unique constraint?).
- **Write for a beginner.** Gloss every HTTP term the first time; no brochure words.
