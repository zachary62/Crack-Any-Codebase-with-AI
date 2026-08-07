# Read one real test by its arrange-act-assert shape

From Chapter 16: Tests: The only docs that don't lie

---

## Task
You are a senior engineer reading a test suite for the
first time. Answer one question: how is a test written?
Pick a handful of real tests that together cover every
idiom a new reader must recognize.

## Input
The crawled test suite (test files and their helpers):
{codebase}

## Scaffold
Most suites have some version of the idioms below; cover
the ones this suite actually uses and skip the ones it
doesn't.

  - a unit test of one class or function.
  - an integration test that hits a real API or
    database.
  - an end-to-end test that drives the whole app.
  - the test-data factory they all use.
  - one test showing the shared-setup pattern (a
    fixture, a let/before block, a setup method).
  - a plugin or module test, if the repo has them.

For an online shop, the unit test might check a
discount function, the integration test might POST to
`/checkout` and read the new order row, and the
end-to-end test might click through the cart in a
browser.

## Output
Return JSON. For each idiom you pick, return four
fields: `idiom`, named in the suite's own terms
(model spec, request spec, system spec, factory,
shared-setup, plugin); `location`,
`path/to/spec:line`; `code`, the real test body copied
verbatim; and `orientation`, one or two sentences a
junior dev could read about what it arranges, acts on,
and asserts. For example:

    {
      "idiom": "integration",
      "location": "tests/checkout/discount_test.rb:42",
      "code": "it 'applies a coupon' do ... end",
      "orientation": "Builds a cart with two items,
        applies a 10% coupon at checkout, and asserts
        the order total drops."
    }

## Guidance
- Open each spec after the first with a one-sentence
  transition naming what changes from the previous one;
  don't recap.
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy
  when it helps, explain any technical term the first
  time, and no brochure words.
