## Task
You are a senior engineer reading a codebase's migration
history to reconstruct what the team built and when, and
retelling it as a story a new teammate can follow.

## Input
The timestamped migration folder names, oldest first:
{migration_names}

## Scaffold
Cluster the migrations into 4-6 acts, each a stretch of time
when the team shipped one major business concept. Skip the
migrations that are just renames, type fixes, or new indexes
unless they mark a real product decision. For example, an
online shop's acts might run: a bare catalog and checkout,
then discount codes, then a marketplace where outside
sellers list their own products, then shipping overseas.
Name each act after what the team was selling or solving,
not after the files.

## Output
One card per act, in chronological order, each starting with
a `###` header of the form
`### Act N — <name> (<month range>)` and then, on the next
line, `opener` + the opening migration name in backticks.
The body is 2-6 sentences. For example:

    ### Act 3 — Becoming a marketplace (Mar-May 2022)
    opener `20220314091200_add_seller`
    The shop started letting outside sellers list their own
    products. The new seller and listing tables mean the
    store no longer owns everything it sells, the first sign
    revenue is shifting from sales to commissions.
    ```mermaid
    flowchart LR
      A["Store-owned catalog"] --> B["Seller accounts"]
      B --> C["Marketplace listings"]
    ```

## Modality — don't rely on prose alone
Each act should carry ONE visual beyond its paragraph, so the
page reads as a story, not a wall of text:
- Name the new tables the act introduced in `code` (e.g.
  `Workflow`, `WorkflowStep`), and always cite the opener
  migration name in `code`.
- Add a tiny ```mermaid flowchart LR (2-4 nodes) of the shift
  the act made — the before and after of the product. Follow
  these rules or it breaks and gets dropped: put EVERY label
  in double quotes; no parentheses, colons, semicolons, or
  slashes inside a label.

## Guidance
- Open each act after the first with a one-sentence
  transition naming the new buyer type, way of making money,
  or pivot it introduces; don't recap.
- Lead with what it means for the user or product before
  naming the code behind it. An analogy is welcome when it
  helps a beginner.
- Write for a curious beginner: plain words, explain any
  technical term the first time, and no brochure words.
