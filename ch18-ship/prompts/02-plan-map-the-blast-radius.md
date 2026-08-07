# Plan: Map the blast radius, build the test, decide the scope

From Chapter 18: Ship: You've understood enough. Now ship.

---

## Task
You are a senior engineer about to change a method.
Produce a Test card with three sections.

## Input
The method you are about to change:
{file_path}:{line_range}

The four-ring blast radius from the planning step is
attached.

## Scaffold
A characterization test pins down what the code does
*today*, bugs and all, so any later change that alters
that behavior turns the test red. Write it to pass on
`main` before you touch anything, capturing the real
return shape on one realistic input.

For an online shop, a characterization test for
`charge()` might assert that a valid order returns one
receipt with a `paid` status and writes exactly one row
to the `orders` table — the current behavior, locked in
before the edit.

## Output
Return markdown with code blocks, in three sections.
`existing_tests`: the test files from ring 3, one line
each on how they exercise the target (direct unit,
integration through HTTP, and so on). `coverage_gap`:
one paragraph on what behavior of the target is NOT
covered, specific about which inputs and outputs have
no assertion. `char_test`: a runnable test in the
repo's framework that pins the current behavior on one
realistic input and captures the return shape as a
snapshot; it should be green BEFORE you change anything
and stay green AFTER. For example:

    **coverage_gap:** nothing asserts what `charge()`
    returns when the provider times out.

    **char_test:**
    ```
    it("returns one paid receipt", async () => {
      const r = await charge(fakeOrder());
      expect(r.status).toBe("paid");
    });
    ```

## Guidance
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy
  when it helps, explain any technical term the first
  time, and no brochure words.
