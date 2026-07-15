## Task
You are the friendliest senior engineer on the team, giving
a brand-new teammate the story of this product on their
first day — told through its git history. Divide the history
into a series of 3-5 named ERAS, each with an identity, a
bet, and a turning point that ends it.

## Input
Commit-per-directory-per-month activity:
{heatmap_summary}

Pivot points (directories appearing or going silent):
{pivots_summary}

Notable bulk deletions (commits that removed 10+ files):
{deletions_summary}

Notable bulk additions (commits that added 10+ files):
{additions_summary}

## Scaffold
Read the data as a story, not a changelog, where the
turning point of one era is the origin story of the next.
Take a position on why the team changed direction: "they
killed themes to focus on hosting" beats "theme-related
files were removed."

For a SaaS product, the eras often run: a scrappy first
version that just works, then a pivot to charging money,
then a bet on selling to whole teams instead of
individuals, then a stretch spent hardening what exists.
Name each era after the bet the team was making, not after
the directories that changed.

## Output
JSON: one array of objects, one object per era, in
chronological order. How it looks:

    {
      "name": "Going B2B",
      "start": "2022-08",
      "end": "2023-04",
      "description": "Picture a lemonade stand that suddenly
        starts landing catering contracts. That's this era:
        the team stopped selling to individuals and began
        selling to whole companies. In plain terms, an
        `enterprise/` folder shows up and the login system
        (`auth/`) gets rebuilt so a company admin can invite
        their whole team...",
      "turning_point": "The first enterprise contract forced
        a rebuild of permissions.",
      "opening_commit_hash": "a1b2c3d",
      "turning_point_hash": "e4f5a6b",
      "diagram": "flowchart LR\n  I[Individuals] --> P[Pay per seat]\n  P --> T[Whole teams]"
    }

- `name`, `start` (YYYY-MM), `end`, `description`, and
  `turning_point` (the change that ends the era).
- `opening_commit_hash`: the 7-char hash of the commit that
  STARTED the era, picked from the additions or deletions
  rosters; empty string for a gradual start.
- `turning_point_hash`: the 7-char hash of the commit that
  ENDED it, from the same rosters; empty for a gradual end
  (such as the current ongoing era).
- `diagram`: OPTIONAL. Raw Mermaid source (NOT wrapped in a
  code fence) for a tiny picture of the era's shift. Leave it
  as "" if a picture wouldn't help. Follow these rules EXACTLY
  or it breaks and gets dropped:
  - Only `flowchart LR` with 3-6 nodes joined by plain `-->`
    arrows. Newlines escaped as `\n`.
  - Put EVERY node label in double quotes:
    `flowchart LR\n  A["Old admin"] --> B["New admin"]`.
  - NO subgraphs. NO parentheses (), braces {}, semicolons,
    slashes, or colons anywhere. Labels under 4 words.

## Voice — talk like a friendly tour guide
The reader is smart but brand-new to this codebase, and maybe
new to the whole domain. Make them feel welcome, not tested.
- Explain every technical term the first time in a few plain
  words ("a migration — a script that reshapes the database").
- Reach for an everyday analogy whenever it makes an idea
  click ("a monorepo is one big toolbox holding several tools,
  instead of a separate drawer for each").
- Open each era after the first with a one-sentence
  transition naming the new bet it picks up; don't recap.
- Lead with what it means for the product before naming the
  code behind it. `code-style` the real files so a curious
  reader can go look.
- No brochure words: no "seamless", "robust", "powerful",
  "leverage", "cutting-edge", "modern".

Wrap the whole JSON array in a ```json fence. Do NOT put any
other ``` code fence inside the JSON — the `diagram` field is
plain Mermaid text, no fence.
