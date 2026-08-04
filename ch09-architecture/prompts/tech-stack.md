## Task
You are a senior engineer documenting the tech stack behind
each box on the architecture map. Open each node from the
inventory and turn its generic label ("the queue", "the
cache") into the specific technology it is built from, so a
teammate can open the right file without guessing. Keep it
friendly enough for someone who's never seen the code.

## Input
The architecture bundle, and the node inventory from the
previous prompt:
{codebase}

Node inventory: {inventory}

## Output
For each node, a card starting with a `### N · name — <one-line
role>` header (reuse the same N and name from the inventory),
then three short paragraphs separated by blank lines:

1. One friendly sentence (analogy welcome) on what the node
   is and does for the product, for someone who's never seen
   it.
2. 2-3 sentences on its actual construction — name the
   specific libraries, frameworks, storage systems, and
   protocols, and point out anything surprising.
3. A short ```<lang> code block of 1-4 REAL lines that prove
   the tech — the SDK import, the client construction, or the
   config line from the bundle (the "SDK IMPORT LINES" section
   gives you real `file:line: import …` rows to quote). Skip
   the block only for a node with no code to show (a rented
   database).
4. One sentence pointing at the file paths (and line numbers
   if you have them) that prove the description.

For example:

    ### 7 · job queue — runs work after checkout
    The "do it later" pile: it lets the shopper get an instant
    "Order placed" while the receipt email goes out in the
    background.

    Under the hood it's a Redis list that a separate worker
    container pops from; anything that fails five times lands
    on a dead-letter list for a human to look at.

    ```ts
    import { Queue } from "bullmq";
    export const emails = new Queue("emails", { connection });
    ```

    See `queue/worker.ts` and `queue/dead-letter.ts`.

## Guidance
- Turn every generic label into the specific technology: not
  "it uses a queue," but which queue — "a Redis list popped by
  one worker container."
- Call out the surprises: a "search service" that's really a
  SQL `LIKE`, a "CDN" that's a single nginx box, a "message
  broker" that's a database table drained by a cron job.
- Keep the first paragraph in plain product terms; name
  libraries and protocols only in the second.
- Open each card after the first with a one-sentence
  transition naming the new role this node plays. Write for a
  curious beginner: plain words, an analogy when it helps, no
  brochure words.
