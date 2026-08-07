# Trace one user action across the async lanes it fires

From Chapter 11: Queues, jobs, and events: What happens after the response?

---

## Task
You are a senior backend engineer tracing one user action
through a codebase's async layer, end to end, from the click
to the side effects that land minutes later.

## Input
The crawled source files (each as a path and its contents):
{codebase}

## Scaffold
Pick one representative action that fans out across several
async lanes: a good one starts with a click in the UI and
ends with side effects landing seconds or minutes later. If
more than one fits, pick the most central and say so. One
action won't touch every lane, so cover only the lanes it
actually fires.

For an online shop, placing an order is the action to trace:
the click commits the order and returns a 200 in a moment,
then a receipt email queues, an outbound webhook tells the
warehouse, and a loyalty-points event updates the buyer's
balance, each landing after the response was already sent.

## Output
1. A bulleted cascade of at least 6 steps. Each bullet is
   bold-headlined with the relative time since the click and
   the lane name, then the file path and line range in parens,
   then one to two sentences on what runs at that step. How it
   looks:

       **t = +200 ms — jobs** (`lib/jobs/receipt.ts` L20–40).
       The order is already saved, so the receipt send is
       queued as a background job and a worker picks it up a
       moment later.

2. A 2–3 sentence "what this trace reveals" paragraph about
   the async architecture, something the per-lane summaries
   alone wouldn't show.
3. Three or more variant actions the codebase naturally has
   (a signup, an inbound payment webhook, a scheduled job
   firing on its own), each walked in 2–3 sentences, led by
   the user-facing trigger before the differing lane.

## Guidance
- Open each variant after the first with a one-sentence
  transition naming the new trigger it covers that the
  previous one didn't; don't recap.
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy when
  it helps, explain any technical term the first time, and no
  brochure words.
