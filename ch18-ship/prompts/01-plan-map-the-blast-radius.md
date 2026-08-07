# Plan: Map the blast radius, build the test, decide the scope

From Chapter 18: Ship: You've understood enough. Now ship.

---

## Task
You are a senior engineer about to fix a bug in an
unfamiliar codebase. Produce a Plan card with exactly
five sections.

## Input
The repo to work in:
{repo_path}

The bug report:
{bug_report}

## Scaffold
Map the change's blast radius as four rings expanding
out from the method you'll edit: ring 1 is every file
that imports or calls it directly, ring 2 is every file
that calls those, ring 3 is the tests that touch any of
them, and ring 4 is the user-facing or stored surfaces
affected (UI components, DB tables, API responses, CLI
output).

For an online shop, a fix to `charge()` might ripple
out from the 6 checkout files that call it (ring 1), to
the 20 files that call those (ring 2), to 4 test files
(ring 3), out to the order-confirmation page and the
`orders` table (ring 4).

## Output
Return JSON with five sections. `target`: file path +
line range of the one method you'll edit. `signature`:
the public signature of that method, copied verbatim.
`summary`: one paragraph in plain English on what the
method does. `rings`: the four lists of files above, in
order of distance. `risk`: one of LOW / MED / HIGH plus
one sentence why. For example:

    {
      "target": "src/checkout/charge.ts:40-78",
      "signature": "async function charge(order: Order):
        Promise<Receipt>",
      "summary": "Takes an order, calls the payment
        provider, and returns a receipt.",
      "rings": {
        "ring1": ["src/checkout/cart.ts"],
        "ring2": ["src/api/orders.ts"],
        "ring3": ["test/checkout/charge.test.ts"],
        "ring4": ["the order-confirmation page",
          "the orders table"]
      },
      "risk": "MED — only the cart calls this directly,
        but a changed receipt shape breaks the
        order-confirmation page"
    }

## Guidance
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy
  when it helps, explain any technical term the first
  time, and no brochure words.
