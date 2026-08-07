# Ask the LLM to map the async architecture

From Chapter 11: Queues, jobs, and events: What happens after the response?

---

## Task
You are a senior backend engineer reading a codebase's
async layer for the first time. Map the design choices
behind its background work before anyone opens a single job.

## Input
The crawled source files (each as a path and its contents):
{codebase}

## Scaffold
Sort the async work into five lanes, in this order:
background jobs, scheduled tasks (cron), outbound webhooks,
real-time connections, and side-effect cascades (in-process
events). Each lane is defined by its trigger, the thing that
kicks the work into motion. If a lane is empty in this
codebase, fill its slot with the heaviest async sub-system
that doesn't fit the others (an email-send pipeline, say)
and label it that way.

For an online shop, the lanes might fill out like this: a
background job emails the receipt after checkout; a nightly
cron rebuilds the best-sellers list; an outbound webhook
tells a shipping partner an order is ready; a real-time
connection streams the driver's location to the buyer; and
one `order.placed` event wakes the inventory, loyalty-points,
and fraud-check listeners at once.

## Output
1. An architectural-choice opener: the one design decision
   that frames the whole async layer, in 2–3 sentences, with
   what's unusual about how the team set it up. For example:

       **Split by workload.** The team runs the web tier and
       a worker fleet as separate processes behind a Redis
       queue, so a runaway image-resize job can't stall
       checkout, at the cost of two deploys and two log
       streams to watch.

2. One paragraph per lane, about 5–7 sentences: what the lane
   does in plain English, the specific tool or convention the
   team picked (the library, the file, the helper), the
   textbook alternative, and why the team passed on it. End
   each paragraph with the file paths. For example:

       **Background jobs — Redis queue, separate workers.**
       After checkout the shop emails a receipt off the
       request thread, via a Redis-backed queue a worker
       process drains. The textbook alternative, sending
       inline, was dropped because a slow mail provider would
       stall checkout. Files: `lib/jobs/receipt.ts`.

3. A Mermaid `flowchart LR` of the architecture: one bordered
   subgraph for the in-process box (one node per lane plus the
   request entry), external nodes for the database and any
   third-party services, and arrows showing who calls whom.
   Cap the nodes so it stays readable on one screen.

## Guidance
- Open each lane after the first with a one-sentence
  transition naming what changes from the previous one: the
  trigger, the direction the work flows, or who owns the
  destination; don't recap.
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy when
  it helps, explain any technical term the first time, and no
  brochure words.
