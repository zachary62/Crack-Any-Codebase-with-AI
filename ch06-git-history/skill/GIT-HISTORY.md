# Skill: Git History

Agent equivalent of Chapter 6's git-history reader. Drop into `.claude/skills/git-history/SKILL.md` (Claude Code) or paste into a Cursor rule.

---
name: git-history
description: Read a product's story out of its git log. Name the eras, profile each era's cast and mood, and dig up the graveyard of killed features. The commit log is the most honest strategy document a team keeps.
---

When the user asks "how did this codebase get here", "what changed over the years", or anything about a project's history, run these three passes in order against the local git log. The prompts are the chapter; use the exact rules in each.

## First, pick the right zoom level

Reading git history is two independent choices: how much to show per commit, and which commits to show.

| Granularity | Command | What you get per commit |
|---|---|---|
| commit | `git log` | hash, author, date, message |
| file | `git log --name-only` | the above, plus files each commit touched |
| code | `git show <hash>` (or `git log -p`) | the above, plus lines added / removed |

Filter with `--diff-filter=A` (only commits that added files) or `--diff-filter=D` (only deletions). Each pass below needs one specific combination; the wrong one either buries you in routine refactors or flies you over the pivots.

Every command here is read-only. Nothing in the repo changes.

## Pipeline

### 1. Name the eras (bird's-eye, §6.3)

Compress the whole history into a bird's-eye view first: per-directory activity by month, when each directory was born or went silent (`git log --name-only`), plus the biggest bulk additions and deletions (`--diff-filter=A`/`D`, 10+ files). Feed that to [`../prompts/name-eras.md`](../prompts/name-eras.md). Output: 3-5 named eras as JSON, each with a bet, a turning point, and the commit hash that ends it. Name each era after the bet, not the folders that changed.

### 2. Profile cast and mood (commit level, §6.4)

Take **one era at a time**. Feed every commit in that era as `month | author | scope | subject`, plus five landmark diffs (`git show`) sampled across its arc: opening, a peak in each third, closing. Use [`../prompts/profile-era.md`](../prompts/profile-era.md). Output: the top 4-5 contributors (cast) and the 3-5 dominant work patterns (mood) as JSON, each with a percentage. Treat the diffs as the source of truth — commit subjects alone let you pattern-match to a confident wrong answer.

### 3. Read the graveyard (code level, §6.5)

Find bulk deletions: 8+ files removed from a single folder in one commit (`git log --diff-filter=D --name-only`). For each, pull the full `git show` diff and feed it to [`../prompts/graveyard-entry.md`](../prompts/graveyard-entry.md). Output: a dated entry for each killed feature — what it was, what the team believed, why it died, what it signals. Read the deleted code; file names tell you what was removed, only the source tells you what it did.

## Output format

Write to `docs/git-history.md` in the target repo: the era timeline, each era's cast and mood, then the graveyard. Then ask the user if they want any era or grave expanded.

## Cardinal rules

- **The log is the source of truth, not the README.** Every claim traces to a commit hash, a date, or a file path.
- **Name eras after bets, not directories.** "The Membership Pivot" beats "the members/ folder grew."
- **Read deleted code before you describe a killed feature.** A `loyalty/` folder might be a finished program or an empty stub; only the diff says which.
- **Write for a curious beginner.** Gloss any git or domain term the first time; no brochure words.
