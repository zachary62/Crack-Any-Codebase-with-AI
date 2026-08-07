# Map every module into the library's own tiers

From Chapter 13: Libraries and frameworks: Start at the import. Peel to the core.

---

## Task
You are a senior engineer opening a library's source for the
first time. Draw the module dependency map — which file
imports which — then sort every module into tiers, letting
the library's own structure decide the tiers rather than any
standard layout.

## Input
The crawled source files (each as a path and its contents):
{codebase}

## Scaffold
A tier is defined by who depends on a module, not by a
folder name. Most libraries fall into a handful of common
tiers; use this as a guide, cover the ones this library has,
and let its structure decide the rest:
  1. The classes or functions your own code imports
  2. Everything else the library ships internally
  3. Any I/O-free core (pure logic a fork or an alternate
     runtime could reuse)
  4. The outside libraries it depends on

For a charting library, tier 1 might be the `Chart` class you
construct; tier 2 the axis, legend, and tooltip modules that
run on every draw; tier 3 the pure scale-and-layout math with
no canvas calls; and tier 4 a color library it depends on.

## Output
1. One section per tier the library has. Start each tier with
   a one-sentence headline naming what the tier is for, then
   give each module a short paragraph: the file path and line
   count, what it does for the library's user in plain
   English, and the one design choice a reader should know.
   End each tier with a shell command the reader could run to
   list its files. For example:

       **Tier 3 — the I/O-free core: the math, kept off the
       canvas so any renderer can reuse it.** `scales.py` (210
       LOC) turns data values into pixel positions; the choice
       to know is that it never touches the canvas, so an SVG
       backend reuses it unchanged. List the tier: `ls
       src/charts/core/*.py`.

2. An engine call-out: name the one or two modules that hold
   the engine (the code that does the real work when a request
   or call comes in) and say why.

## Guidance
- Open each tier after the first with a one-sentence
  transition naming the role it plays that the previous tier
  didn't; don't recap.
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy when
  it helps, explain any technical term the first time, and no
  brochure words.
