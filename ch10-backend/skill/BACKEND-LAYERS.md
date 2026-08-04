# Skill: Backend Layers

Agent equivalent of Chapter 10's backend reader. Drop into `.claude/skills/backend-layers/SKILL.md` (Claude Code) or paste into a Cursor rule.

---
name: backend-layers
description: Read any backend as the same six layers a request flows through — route, middleware, handler, service, database, response. Draw the pipeline with a count per layer, read the code only where the team broke from the framework, and trace the core request end to end. The order of the layers is the product.
---

When the user asks "what runs when I hit this endpoint", "where's the permission check", or anything about backend control flow, run these three passes.

## The six layers (every framework, every language)

| Layer | What it does | Django | Express | Rails | FastAPI |
|---|---|---|---|---|---|
| 1 Route | URL → function | `urls.py` | `app.post` | `routes.rb` | `@app.post` |
| 2 Middleware | shared checks (auth, rate limit) | `MIDDLEWARE` + decorators | `app.use` | `before_action` | `Depends` |
| 3 Handler | the one function for this URL | `views/` | `(req,res)=>` | controller | `async def` |
| 4 Service | business rule, no HTTP | `actions/`, `services/` | `services/` | `app/services/` | `services/` |
| 5 Database | read/write | ORM `.objects` | Prisma/Knex | ActiveRecord | SQLAlchemy |
| 6 Response | package the result | `JsonResponse` | `res.json` | `render json` | `return x` |

The names move; the six layers are constant. Switching frameworks becomes a spelling change.

## Pipeline

### 1. Draw the pipeline (§10.3)

Feed the source (grouped by layer) to [`../prompts/pipeline.md`](../prompts/pipeline.md). Output: a Mermaid `flowchart LR` of the six layers **plus an `on_commit` dashed arrow** to whatever runs after the response, and one card per layer with a **concrete count** (650 endpoints in one file), its three biggest items, and a shell command to find that layer in any repo. Demand a count — "the routing is well-organized" says nothing; "650 endpoints in one `urls.py`" says everything. The dashed fork between "the user waits" and "this runs after the 200" is the part worth drawing.

### 2. Read only the custom code (§10.4)

Feed the source to [`../prompts/layer-code.md`](../prompts/layer-code.md). For each layer, decide *novel* (a wrapper or idiom a new hire couldn't predict) or *standard* (textbook framework). Show ~20 real lines only for the novel ones; give the rest a one-line "standard" note. Most of a backend is boilerplate you already understand — the one or two novel layers are the only code worth reading closely. Letting a layer be *standard* is as useful as an excerpt: it tells you where **not** to look.

### 3. Trace the core request (§10.5)

Feed the source to [`../prompts/trace.md`](../prompts/trace.md). Trace the one endpoint the product exists to serve (Zulip's `POST /json/messages`, Cal.com's `POST /api/book/event`) through all six layers with a `file:line` each, **flagging every foreign-state boundary** (a DB write, an external call). Then 3+ variants (a direct message vs. a stream message, an edit, a rate-limited sender) that light up different layers. The commit boundary — where the data becomes durable, before the 200 goes out — is the one fact a trace shows that a static diagram can't.

## Output format

Write to `docs/backend-layers.md` in the target repo: the pipeline + counts, the custom-code excerpts, then the trace. Ask the user which layer or variant to expand.

## Cardinal rules

- **The order of the six layers is the product.** "Charge then book" is a different business from "book then charge"; the pipeline is where that order is enforced.
- **Lead every layer with a count, not an adjective.** You can't fake a number.
- **Find the one or two novel layers; skip the four standard ones.** Reading boilerplate teaches you nothing.
- **The commit boundary is the payoff.** Name where the transaction commits and what the 200 promises. Write for a beginner; no brochure words.
