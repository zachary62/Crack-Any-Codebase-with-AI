# Open each folder: Contract or junk drawer?

From Chapter 17: Folder structure: The floor plan of your codebase

---

## Task
You are a senior engineer giving a new hire a tour of
this repo, one top-level folder at a time.

## Input
The crawled source files (each as a path and its contents):
{codebase}

## Scaffold
Go in the order a developer would explore: the heart
first (most code), then config, data, tests, and the
catch-all last. Stop drilling into a folder once you
hit a detail a junior dev couldn't predict from the
name.

For an online shop, you'd open `src/` first because it
holds most of the code, and you'd note that its
`routes/` folder is a framework contract, not just a
label: the router registers every file there as a live
endpoint.

## Output
Return one card per top-level folder, in explore order.
Lead each card with a bold headline naming the folder
and its role, like `**app/ — the heart, 70% of the
code.**`, then three points: `purpose`, what the folder
is for in one sentence; `contract`, whether a framework
or tool looks for files here (the rule it enforces) or
the name is just a label the team chose; and
`open_first`, the single file inside worth opening first
and why a newcomer couldn't have guessed it from
outside. For example:

    **routes/ — the URL surface.**
    - Purpose: one file per group of endpoints.
    - Contract: a framework contract — the router
      registers every file here as a live endpoint.
    - Open first: orders.ts, the resource every other
      route links back to.

## Guidance
- Open each folder after the first with a one-sentence
  transition naming what changes from the previous one;
  don't recap.
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy
  when it helps, explain any technical term the first
  time, and no brochure words.
