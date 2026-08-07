# Open each module and find the data structure it bets on

From Chapter 13: Libraries and frameworks: Start at the import. Peel to the core.

---

## Task
You are a senior engineer giving a new hire a tour of a
library's source, one module at a time. Pair a plain-English
summary of each important module with the code that does the
work.

## Input
The crawled source files (each as a path and its contents):
{codebase}

## Scaffold
Walk the modules in tier order (the classes you import, then
the supporting modules, then any I/O-free core). Give a full
card to each module that carries request or call control
flow, and group the rest into a single summary card, so the
tour is a handful of cards rather than one per module.

For a charting library, the `Chart` class that runs every
draw earns a full card, and so does the I/O-free layout core;
the axis, legend, and color helpers fold into one summary
card, because none of them drives the draw.

## Output
1. A full card per control-flow module, in two parts. First,
   plain English in 3–5 sentences, leading with the
   user-facing thing ("this is the file behind the main object
   you create at startup") before any internal function name.
   Second, a code excerpt of about 20 lines from the repo
   showing the module's actual idiom, as a plain fenced block
   with the file path and line numbers, followed by a one-line
   explanation and a pointer to the 1–3 files to focus on. How
   it looks: a card titled **`chart.draw`: the file behind the
   chart you render**, a ~20-line excerpt of `draw()` calling
   `build_scales()` then the paint helpers, one line saying
   the whole draw is those calls, and a pointer to `chart.py`
   and `core/scales.py`.

2. A closing summary card covering the remaining modules in
   plain English, confirming none of them holds control flow.

## Guidance
- Open each card after the first with a one-sentence
  transition naming the new responsibility this module takes
  on that the previous one didn't; don't recap.
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy when
  it helps, explain any technical term the first time, and no
  brochure words.
