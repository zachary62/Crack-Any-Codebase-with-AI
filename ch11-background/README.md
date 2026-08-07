# Chapter 11. Queues, jobs, and events: What happens after the response?

> Five async lanes — jobs, cron, webhooks, real-time connections, side-effect cascades. Three prompts map the lanes, read each job as a state machine, and trace one action across every lane it fires.

## The prompts

Copy any of these into ChatGPT, Claude, Gemini, or an agent like Claude Code, with the repository you want to read open alongside it. They're reproduced verbatim from the chapter, so what you run is what you read.

- [`01-ask-the-llm-to-map.md`](prompts/01-ask-the-llm-to-map.md) — Ask the LLM to map the async architecture
- [`02-read-each-background-job-as.md`](prompts/02-read-each-background-job-as.md) — Read each background job as a state machine
- [`03-trace-one-user-action-across.md`](prompts/03-trace-one-user-action-across.md) — Trace one user action across the async lanes it fires

## Running them

Each prompt is self-contained. Point it at one repository at a time and paste in the files it asks for under **Input**; an agent can gather those itself if you give it the repo path.

The chapter walks through the answers these produced on the example repository, pinned to a specific commit. Your repository will differ, which is the point.
