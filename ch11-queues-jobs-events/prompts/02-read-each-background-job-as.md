# Read each background job as a state machine

From Chapter 11: Queues, jobs, and events: What happens after the response?

---

## Task
You are a senior backend engineer writing a teaching
artifact for a new hire about to read a repo for the first
time. Walk them through each background job: what it does,
its lifecycle, and the code that drives it.

## Input
The crawled source files (each as a path and its contents):
{codebase}

## Scaffold
Read each background job as a small state machine, and use
the number of states to gauge its risk. A two-state job
(idle → running → idle) is fire-and-forget; a five-state job
with a lock and several failure paths is the riskiest thing
in the repo. Order the jobs from simplest to most complex,
and skip any that just follow a library's defaults with no
novel decision; those are the noise.

For an online shop, the simplest job might be an hourly
refresh of the best-sellers list: two states, and a crash
just leaves a slightly stale list until the next run. The
most complex might be a nightly inventory reconciliation
that locks each product row while it counts, with its own
retry budget for the warehouse API.

## Output
1. A short paragraph per job that leads with what the job
   does for the user or product, names the file path and the
   trigger types (cron, boot, HTTP, inline, offload) as
   natural prose, then calls out the state-machine lifecycle
   and the failure/recovery story when the job throws; a brief
   labeled line for each of those two is fine. For example:

       **Job 1 — refresh the best-sellers list.** An hourly
       sweep recomputes one cached list nobody watches. It
       lives in `jobs/best-sellers.ts` and fires from cron.
       States: idle → running → idle (loops next hour).
       Failure mode: it logs and dies, the stale list
       lingers, and the next hour's run covers for it.

2. A short code excerpt per job, about 20 lines, showing the
   team's idiom (the producer call site plus the worker body,
   or whatever best teaches the pattern), as a plain fenced
   code block with the right language tag, followed by a
   one-line plain explanation of what it shows. For example:
   a `cron.hourly('best-sellers', …)` registration above a
   one-line `db.products.topSellers(…)` body, then one
   sentence noting the whole job is the arrow from idle to
   running and back.

## Guidance
- Open each job after the first with a one-sentence
  transition naming the new failure mode or recovery story it
  introduces that the previous one didn't; don't recap.
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy when
  it helps, explain any technical term the first time, and no
  brochure words.
