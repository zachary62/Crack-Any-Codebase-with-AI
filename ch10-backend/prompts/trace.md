## Task
You are a senior backend engineer tracing one HTTP request
through the backend end to end for a new developer: the most
central endpoint, the one POST or mutation every user hits at
least once. Keep it warm and concrete.

## Input
The crawled source files, grouped by layer:
{codebase}

## Scaffold
Walk the same six layers (Route → Middleware → Handler →
Service → Database → Response) for one real request, and flag
the moment it crosses into foreign state — a database write
or an external API call — since that's where a failure
actually costs something.

For an online shop's `POST /checkout`, layers 1-3 only read
and validate, layer 4 calls the payment provider to charge
the card (the first foreign-state boundary), layer 5 commits
the order row (the second), and the receipt email after the
response is best-effort.

## Output, in this exact order

1. Two lines naming the endpoint and the action:

       **Endpoint:** `POST /json/messages`
       **Action:** a logged-in user submits a chat message.

2. A `### The trace` card. Start it with a small ```mermaid
   flowchart LR of the path this request takes through the
   layers, marking where the response returns — e.g.
   `Route --> Middleware --> Handler --> Service --> Database --> Response`
   with a dashed `-.->` to any async work after the 200 (plain
   single-word node names, `-->` arrows only, no parentheses
   or colons in labels). Then the six layers as a bulleted
   list in order: each bullet is bold-headlined with a short
   label for what happens at that layer, then one sentence
   naming what runs for THIS specific request, then the
   `file:line` in parens. Flag any foreign-state boundary
   inline. For example:

       - **Layer 5 — Database** *writes the order row inside
       one transaction — the first foreign-state boundary*
       (`orders/create.ts:187`).

3. A `### What this trace reveals` card: 2-3 sentences on the
   codebase's architecture (where the commit boundary sits,
   what the 200 promises).

4. Three or more `### Variant — <name>` cards, each 2-3
   sentences: a different user state, plan, request type, or
   rejected request. Name the user kind, then which layers
   light up differently and why. For example:

       ### Variant — Guest checkout
       Layer 2 skips the sign-in check; layer 4 creates the
       order under a temporary guest record instead of a
       member account.

## Guidance
- Flag every foreign-state boundary (a database write, an
  external call) inline; naming where state changes is what
  makes the trace debuggable.
- Pick variants that exercise DIFFERENT layers — a different
  plan, a different request type, a rejected request — not
  minor field changes.
- Open each variant after the first with a one-sentence
  transition. Write for a curious beginner: plain words, an
  analogy when it helps, no brochure words.
