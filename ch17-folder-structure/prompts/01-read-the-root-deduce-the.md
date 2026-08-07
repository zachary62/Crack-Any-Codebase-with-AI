# Read the root: Deduce the layout pattern

From Chapter 17: Folder structure: The floor plan of your codebase

---

## Task
You are a senior engineer reading an unfamiliar repo
for the first time. Produce an annotated directory tree
from the `tree -L 2 -d` output below, then name the
layout pattern.

## Input
The output of `tree -L 2 -d` on the repo root:

{tree_output}

## Scaffold
Read the root folders for what they reveal about the
team's organizing choice. Layer-based roots group code
by technical role (`models/`, `controllers/`,
`views/`); feature-based roots group by product domain
(`billing/`, `auth/`); a hybrid puts features outside
and layers inside; a monorepo holds several deployable
apps under `apps/` and `packages/`.

For an online shop laid out as `catalog/`,
`checkout/`, and `shipping/`, the pattern is FEATURE,
because the folders name parts of the business, not
technical roles.

## Output
Return JSON. For each top-level folder, give `name`
(the folder name as it appears), `role` (one of MODEL,
VIEW, CTRL, CFG, TEST, BUILD, DOCS, OTHER), and `desc`
(one plain-English sentence on what the folder holds).
Then give `pattern` (one of LAYER, FEATURE, HYBRID,
MONOREPO, the best match), `reasoning` (one sentence
why), and `first_file` (the single file a new reader
should open first, the table of contents for the whole
app). For example:

    {
      "folders": [
        {"name": "catalog", "role": "OTHER", "desc":
          "product listings, search, and pricing"},
        {"name": "config", "role": "CFG", "desc":
          "environment and deploy settings"}
      ],
      "pattern": "FEATURE",
      "reasoning": "folders name product domains, not
        technical roles",
      "first_file": "app.ts"
    }

## Guidance
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy
  when it helps, explain any technical term the first
  time, and no brochure words.
