# Chapter 16. Tests: The only docs that don't lie

> A test suite is an executable spec the build keeps re-checking. Three prompts identify how a suite is wired, map what it covers and what it skips, and read one real test by its arrange-act-assert shape.

## The prompts

Copy any of these into ChatGPT, Claude, Gemini, or an agent like Claude Code, with the repository you want to read open alongside it. They're reproduced verbatim from the chapter, so what you run is what you read.

- [`01-identify-the-runner-lifecycle-and.md`](prompts/01-identify-the-runner-lifecycle-and.md) — Identify the runner, lifecycle, and fixtures
- [`02-map-what-s-tested-and.md`](prompts/02-map-what-s-tested-and.md) — Map what's tested, and what isn't
- [`03-read-one-real-test-by.md`](prompts/03-read-one-real-test-by.md) — Read one real test by its arrange-act-assert shape

## Running them

Each prompt is self-contained. Point it at one repository at a time and paste in the files it asks for under **Input**; an agent can gather those itself if you give it the repo path.

The chapter walks through the answers these produced on the example repository, pinned to a specific commit. Your repository will differ, which is the point.
