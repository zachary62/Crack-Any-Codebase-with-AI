# Verify: Prove it works, then ship

From Chapter 18: Ship: You've understood enough. Now ship.

---

## Task
You are a senior engineer who just shipped a fix.
Produce a Verification card with the exact, re-runnable
evidence for four steps. Show commands and their
output, not a claim that the fix passes.

## Output
Format as a shell session with comments, covering four
steps. `char_test`: the command to run the new
characterization test slice, and its green output.
`build`: the command that compiles the project, showing
no new type errors. `staging`: a staging or end-to-end
run that exercises the exact path you changed (simulate
the failure your fix handles), showing the fix behave
and the expected side effect land exactly once, with no
duplicate. `rollout`: one line on the flag and canary
plan, and the rollback. For example:

    $ npm test src/checkout/order-form.test.ts
      PASS ignores a duplicate submit (0.4s)
    $ npm run build   # tsc clean, no new errors
    # staging: click Place Order twice, fast
    [checkout] duplicate submit ignored
    [checkout] order 4471 placed · 1 orders row written
    Behind flag `dedupe-submit` (default OFF). Canary
    10%, error rate flat. Rollback = flip flag.

## Guidance
- Show the command and its real output, not an assertion
  like "the fix looks correct."
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy
  when it helps, explain any technical term the first
  time, and no brochure words.
