## Task
Write a GRAVEYARD ENTRY for one bulk-deletion event from
a repo's git history: a dated record of a feature the
team built and then chose to kill.

## Input
COMMIT
  Hash:    {hash}
  Subject: "{subject}" ({author}, {date})

ERA IT BELONGS TO
  "{era_name}" ({era_start} to {era_end})
  {era_description}

FULL DIFF from `git show {hash}`:
{diff}

## Scaffold
Read both the file paths AND the deleted code above. File
names tell you what was removed; only the source tells you
what the feature actually did, so describe its behavior from
the diff, never guess it from the paths.

For a shop's backend, a deleted `loyalty/` folder might look
like a finished rewards program from its name, but the diff
might show it was only ever a stub with no points logic
wired up. The code is what tells you which it was.

## Output
A graveyard entry in four parts, each a short bold headline
plus one sentence, then a name, a tagline, and an epitaph.
For example:

    **What it was: a built-in storefront chat.** A widget,
    a `messages` table, and an admin inbox.
    **What they believed: shoppers wanted to ask before
    buying.** Live chat would lift conversion.
    **Why it died: nobody staffed it.** Unanswered chats
    looked worse than none, so it was cut.
    **What it signals: self-serve over hand-holding.** The
    product bets the page should answer every question.

    *Name:* The Empty Inbox. *Tagline:* When live chat
    needed a human nobody hired. *Epitaph:* A front door
    with no one behind it.

- WHAT IT WAS: a 2-5 word headline plus the concrete pieces
  (routes, models, UI) you can see in the diff.
- WHAT THEY BELIEVED: the original bet — what did the team
  think users wanted, and on what business model?
- WHY IT DIED: what changed — replaced, out-competed, or did
  the team lose faith?
- WHAT IT SIGNALS: what the deletion says about the product's
  direction.
- Then a vivid short NAME, a catchy 5-8 word TAGLINE for the
  death ("When the team bet on revenue over reach"), and a
  one-sentence epitaph.

## Voice — a warm, plain-spoken eulogy for a beginner
The reader is a new teammate who's never seen this feature.
Make them understand what died and why it mattered.
- Lead with what it meant for the user before naming the code
  behind it. Explain any technical term the first time in a
  few plain words.
- Reach for an everyday analogy when it helps ("AMP was like
  keeping a fax machine because one big customer still used
  it — until they stopped").
- No brochure words: no "seamless", "robust", "powerful",
  "leverage", "cutting-edge", "modern".

## Optional picture
If (and only if) it genuinely helps a beginner see what the
feature did or what replaced it, you MAY add ONE small extra,
right after the four headlines and before the Name line:
- a tiny Mermaid diagram in a ```mermaid fence, OR
- a short ```<lang> code block of a few illustrative lines
  pulled from the deleted diff.
Skip it if it would just be decoration.

If you include a Mermaid diagram, follow these rules EXACTLY
or it breaks and gets dropped:
- Only `flowchart LR` with 3-6 nodes joined by plain `-->`
  arrows.
- Put EVERY node label in double quotes:
  `A["Split admin"] --> B["Unified admin"]`.
- NO subgraphs. NO parentheses (), braces {}, semicolons,
  slashes, or colons anywhere. Labels under 4 words.

Respond as plain markdown. No JSON. The only code fences
allowed are the single optional diagram or snippet above.
