## Task
You are analyzing one era of a product's git history:
era {era_index} of {total_eras}, "{era_name}"
({era_start} to {era_end}). Profile its cast (who did
the work) and its mood (what the work was).

## Input
Era description from the narrative pass:
{era_description}

Prior era summaries (for cross-era contrast):
{prior_summaries}

Every commit in THIS era only, one per line, formatted
as "month | author | scope | subject":
{commit_stream}

Landmark commits from this era, code-level anchors
sampled across its arc:

--- OPENING ({opening_hash}, {opening_date}): {opening_subject} ---
{opening_diff}

--- EARLY PEAK ({early_hash}, {early_date}): {early_subject} ---
{early_diff}

--- MID PEAK ({mid_hash}, {mid_date}): {mid_subject} ---
{mid_diff}

--- LATE PEAK ({late_hash}, {late_date}): {late_subject} ---
{late_diff}

--- CLOSING ({closing_hash}, {closing_date}): {closing_subject} ---
{closing_diff}

## Scaffold
Commit subjects alone let you pattern-match your way to
a confident wrong answer, so treat the landmark diffs as
the source of truth: use them as concrete examples of
what this era's work looks like at different points, and
cross-check every cast-and-mood conclusion against them.
Use specific numbers, and where prior eras are provided,
contrast against them.

For a shop's backend, a cast like "one founder at 40%, then
three contributors near 10% each" reads as founder-led but
widening; a mood like "search and catalog 30%, dependency
bumps 20%, bug fixes 15%" reads as a team building
shopper-facing features while keeping the lights on.

## Output
A single JSON object with EXACTLY two top-level fields, `cast`
and `mood` (both always present, even for a one-person era).
For example:

    {
      "cast": {
        "contributors": [
          {"name": "Dana Lee", "pct": 22,
           "note": "Founder; wrote the original checkout."}
        ],
        "narrative": "Still founder-led, but three new hires
          each cross 10% — the team is widening."
      },
      "mood": {
        "patterns": [
          {"label": "Search & catalog", "pct": 30,
           "note": "Filters, typo-tolerant search."},
          {"label": "Dependency bumps", "pct": 20},
          {"label": "Other", "pct": 15}
        ],
        "narrative": "Shopper-facing features dominate while
          the team keeps dependencies current."
      }
    }

- `cast`: the top 4-5 contributors by share of this era's
  commits, plus a one-sentence narrative on cast shape
  (founder-led? tight core? broad community?).
- `mood`: 3-5 dominant work patterns, each with the % of
  commits it covers, plus a one-sentence narrative on what
  the mood says about the era. Keep "other" under 20%; if a
  bucket is too small or too generic to name, find a better
  label.

## Voice — introduce the team like people, not rows
The reader is a friendly new teammate meeting this cast for
the first time. Keep every `note` and `narrative` warm, plain,
and short.
- In each contributor `note`, say what they OWNED in human
  terms ("kept the payments plumbing alive"), not just where
  they committed.
- Name each work pattern in plain product terms before any
  folder: "subscription billing," not "stripe/ folder churn."
  Explain any technical term the first time in a few words.
- Reach for a quick analogy in a narrative when it helps
  ("a bot topping the commit count is like a Roomba logging
  more miles than anyone in the house — busy, but automated").
- No brochure words: no "seamless", "robust", "powerful",
  "leverage", "cutting-edge", "modern".
- Keep `note` to one sentence and each `narrative` to one
  sentence — these render as small captions, not paragraphs.

Wrap the JSON object in a ```json fence, with EXACTLY the two
top-level keys `cast` and `mood`.
