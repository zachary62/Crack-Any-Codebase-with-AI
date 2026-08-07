# Identify the runner, lifecycle, and fixtures

From Chapter 16: Tests: The only docs that don't lie

---

## Task
You are a senior engineer reading a test suite for the
first time. Find where the tests live (a `tests/`,
`spec/`, or `__tests__/` tree, or test files sitting
next to source), then answer one question: how is
testing wired?

## Input
The crawled test suite (test files and their helpers):
{codebase}

## Scaffold
List the test framework and the libraries around it.
Treat the list below as a checklist of common roles,
not a required set: cover whatever this suite has and
skip the roles it doesn't use.

  - runner: the framework that finds and runs the tests.
  - test-data builder: how tests construct objects
    (a factory, fixtures, inline literals).
  - browser driver: whatever drives a real browser for
    end-to-end specs, if any.
  - network stubbing: how outbound calls get faked so a
    test never hits a live service.
  - anything else it leans on: assertion helpers,
    coverage, a parallel runner.

For an online shop, the wiring might read: Jest finds
and runs the specs, a factory builds the test orders,
Playwright drives the checkout in a real browser, and
nock blocks any call to the live payment service.

## Output
Return JSON. For each role the suite uses, name the
library and say in one line why this team picked it.
Add two more keys: `lifecycle`, the phases one test
runs through in order, from the runner starting up to
the report printed; and `shared_setup`, the setup
helpers every test inherits and the file they live in.
For example:

    {
      "runner": "Jest — zero-config watch mode on a
        JavaScript stack",
      "test_data": "a factory in tests/factories, so
        each test builds only the fields it needs",
      "lifecycle": ["load config", "before-each: seed a
        cart", "run the example", "after-each: roll back
        the DB", "print pass/fail"],
      "shared_setup": "tests/setup.js — signs in a fake
        user before every spec"
    }

## Guidance
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy
  when it helps, explain any technical term the first
  time, and no brochure words.
