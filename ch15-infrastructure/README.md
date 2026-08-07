# Chapter 15. Infrastructure: The code everyone ignores (until it breaks)

> The code everyone ignores until it breaks. Three prompts map the five files behind a deploy, read each in boot order, and trace one git push to a live container.

## The prompts

Copy any of these into ChatGPT, Claude, Gemini, or an agent like Claude Code, with the repository you want to read open alongside it. They're reproduced verbatim from the chapter, so what you run is what you read.

- [`01-ask-the-llm-to-map.md`](prompts/01-ask-the-llm-to-map.md) — Ask the LLM to map the five files, read two ways
- [`02-open-each-of-the-five.md`](prompts/02-open-each-of-the-five.md) — Open each of the five files, in boot order
- [`03-trace-one-git-push-through.md`](prompts/03-trace-one-git-push-through.md) — Trace one git push through eight deploy stages

## Running them

Each prompt is self-contained. Point it at one repository at a time and paste in the files it asks for under **Input**; an agent can gather those itself if you give it the repo path.

The chapter walks through the answers these produced on the example repository, pinned to a specific commit. Your repository will differ, which is the point.
