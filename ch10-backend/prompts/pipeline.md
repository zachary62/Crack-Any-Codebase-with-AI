## Task
You are the friendliest senior backend engineer on the team,
mapping a codebase's request pipeline for a new developer:
the six layers every request flows through, with a count and
the standout item for each.

## Input
The crawled source files, grouped by layer, with a file count
per layer at the top:
{codebase}

## Scaffold
Every backend request flows through the same six layers in
order: Route → Middleware → Handler → Service → Database →
Response. The route matches the URL, the middleware runs
shared checks (auth, rate limits), the handler validates the
one request, the service runs the business rule, the database
reads or writes, and the response packages the result.

For an online shop's `POST /checkout`, the route binds the
URL to one function, middleware checks the shopper is signed
in, the handler validates the cart, the service applies
"don't sell out-of-stock items," the database commits the
order row, and the response returns the order id.

## Output, in this exact order

1. A Mermaid `flowchart LR` in a ```mermaid fence: one node
   per layer (Route → Middleware → Handler → Service →
   Database → Response), each labeled with the layer name,
   its count, and its key helper, plus an `on_commit` dashed
   arrow (`-.->`) to whatever async work runs AFTER the
   response. Rules:
   - Node IDs are simple identifiers; the label goes in
     brackets. You MAY use `<br/>` for line breaks inside a
     label and `classDef`/`:::style` for color.
   - No quotes, parentheses, colons, or slashes inside label
     text — plain words and `<br/>` only.

2. One card per layer, each starting with a `### Layer N —
   <Name>: <one-line claim with the concrete COUNT and the
   standout item>` header. The body is 3-5 sentences: what
   the team picked, the three biggest items named as prose,
   and it ENDS with one shell command in inline `code` the
   reader could run to find this layer in their own repo. For
   example:

       ### Layer 1 — Route: 80 endpoints across 12 routers, `payments` the biggest
       Each feature folder registers its own router... Shell
       trick: `grep -rn "router.post" src/ | wc -l`.

## Guidance
- Lead each layer's claim with a concrete count, not an
  adjective: "80 endpoints across 12 routers," not "the
  routing is well-organized." You can't fake a number — use
  the file counts provided, and the code you can see.
- The `on_commit` dashed arrow is the part worth drawing: the
  fork between "the user waits" and "this runs after the
  response."
- End each layer with a shell command to find it in any repo.
- Open each layer after the first with a one-sentence
  transition naming the new piece it adds. Write for a
  curious beginner: plain words, an analogy when it helps, no
  brochure words.
