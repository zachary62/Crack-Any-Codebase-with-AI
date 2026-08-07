# Trace one real request through the modules

From Chapter 13: Libraries and frameworks: Start at the import. Peel to the core.

---

## Task
You are a senior engineer tracing one request through a
library's source, end to end, from the entry point's first
call into the library to the final bytes going back out.

## Input
The crawled source files (each as a path and its contents):
{codebase}

## Scaffold
Trace the common-case operation the library exists to serve,
the one it handles thousands of times a day: for a web
framework a plain route hit like `GET /users/<id>`, for a
parser one document, for an HTTP client one GET. If more than
one fits, pick the most central and say so.

For a charting library, the call to trace is `chart.draw()`
on a typical bar chart: it is what the library exists to do,
runs on nearly every use, and touches the scale math, the
layout, and the renderer in turn.

## Output
1. A numbered trace from the entry point's first call to the
   final bytes (or value) going back out. Each step is
   bold-headlined with what happens in plain terms (the
   request comes in, the context goes live, the view runs),
   then a roughly 6-line code excerpt, then the file path,
   line number, and which module or tier the step is in,
   followed by a one-line explanation. For example:

       **2. The draw spine takes over** (`chart.py` L88, tier
       1): a ~6-line excerpt of `draw()` building the scales
       then painting, plus one line noting one method owns the
       whole draw.

2. Three or more variant requests the codebase naturally
   supports. For each, name which steps light up differently
   and why. For example: for a charting library, a pie chart
   skips the axis steps, an animated draw adds a timer loop
   around the paint step, and a redraw on new data reuses
   the cached scales.

## Guidance
- Open each step after the first with a one-sentence
  transition naming the boundary it crosses that the previous
  one didn't: entering the engine, crossing into the context,
  reaching your code; don't recap.
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy when
  it helps, explain any technical term the first time, and no
  brochure words.
