# Chapter 13. Libraries and frameworks: Start at the import. Peel to the core.

> Start at the import, peel to the core. Three prompts sort a library's modules into tiers, open the ones that matter, and trace one real request through them.

## The prompts

Copy any of these into ChatGPT, Claude, Gemini, or an agent like Claude Code, with the repository you want to read open alongside it. They're reproduced verbatim from the chapter, so what you run is what you read.

- [`01-map-every-module-into-the.md`](prompts/01-map-every-module-into-the.md) — Map every module into the library's own tiers
- [`02-open-each-module-and-find.md`](prompts/02-open-each-module-and-find.md) — Open each module and find the data structure it bets on
- [`03-trace-one-real-request-through.md`](prompts/03-trace-one-real-request-through.md) — Trace one real request through the modules

## Running them

Each prompt is self-contained. Point it at one repository at a time and paste in the files it asks for under **Input**; an agent can gather those itself if you give it the repo path.

The chapter walks through the answers these produced on the example repository, pinned to a specific commit. Your repository will differ, which is the point.
