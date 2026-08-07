# Map what's tested, and what isn't

From Chapter 16: Tests: The only docs that don't lie

---

## Task
You are a senior engineer reading a test suite for the
first time. Answer one question: what do they test?

## Input
The crawled test suite (test files and their helpers):
{codebase}

## Scaffold
Pair each source folder with its matching test folder,
however this repo lays them out (`src/` ↔ `tests/`,
`app/` ↔ `spec/`, co-located `*_test.go`, and so on).
A test count is the clearest proxy for what the team is
most afraid of breaking, so for each pair report the
count and its tier.

For an online shop, the pairing might run: `src/cart`
↔ `tests/cart` at 120 tests, `src/checkout` ↔
`tests/checkout` at 1,400 tests, plus a lone
`tests/performance` folder that benchmarks page-load
times and pairs with no single source folder.

## Output
Return JSON with three keys. `pairs`: one entry per
source-folder ↔ test-folder pair, each with the test
count (it-blocks, test functions, `test(...)` cases,
whatever the framework uses) and a tier — HOT (1000+),
WARM (100-999), or COOL (<100). `unpaired`: any test
folder that does not pair one-to-one with a source
folder, with one line on what it tests instead.
`untested`: any source folder with no tests at all.
For example:

    {
      "pairs": [
        {"source": "src/checkout", "test":
          "tests/checkout", "count": 1400,
          "tier": "HOT"},
        {"source": "src/cart", "test": "tests/cart",
          "count": 120, "tier": "WARM"}
      ],
      "unpaired": [{"folder": "tests/performance",
        "tests": "page-load benchmarks that span many
        modules"}],
      "untested": ["src/legacy/coupons"]
    }

## Guidance
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy
  when it helps, explain any technical term the first
  time, and no brochure words.
