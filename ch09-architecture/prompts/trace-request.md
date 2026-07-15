## Task
You are a senior engineer walking a new developer through
what a codebase does when one real user triggers the
product's core action, hop by hop, with a file name for each
step. Keep it warm and concrete.

## Input
The architecture bundle, and the node inventory from the
first prompt:
{codebase}

Node inventory: {inventory}

## Scaffold
Trace the one action the product exists for — the action
that, if it broke, would make the whole product feel broken —
end to end through the nodes from the inventory, and mark the
moment the user stops waiting.

For an online shop that action is placing an order: the
browser posts the cart, the order service writes the row and
charges the card while the shopper watches a spinner, the
`200` comes back, and only then do the receipt email and the
shipping webhook fire in the background.

## Output

1. A `### The trace` card: a numbered bulleted list of ordered
   hops. Each bullet is bold-headlined with the hop number and
   the node it lands on (`**Hop 3 — node 5 · postgres**`),
   then one sentence a new hire could read cold, then in
   parens whether the user waits or it's queued for a worker,
   then the `file:line` that proves it. For example:

       **Hop 2 — node 4 · postgres** *(user waits)* — writes
       the order row inside one transaction
       (`orders/create.ts:187`).

2. Then three or more variants of the same action the codebase
   naturally has — a different user state, plan, or entry
   point. Each variant is its own `### Variant — <name>` card,
   2-3 sentences. For example:

       ### Variant — Guest checkout
       A shopper with no account skips the account and loyalty
       nodes; the order still commits in one transaction, but
       the receipt goes to a one-off email instead of a saved
       profile.

3. A final `### What the variants reveal` card: one or two
   sentences on how the architecture is assembled at request
   time, from runtime state, not fixed in a file.

## Guidance
- Mark every hop as either user-waits or queued-for-a-worker,
  and name the `file:line` that proves it; that boundary is
  the trace's whole payoff.
- For the variants, lead with the user-facing difference (free
  vs. paid, browser vs. API client) before the nodes that
  change.
- Open each variant after the first with a one-sentence
  transition naming the new scenario it covers. Write for a
  curious beginner: plain words, an analogy when it helps, no
  brochure words.
