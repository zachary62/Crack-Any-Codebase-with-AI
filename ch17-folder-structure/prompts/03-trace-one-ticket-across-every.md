# Trace one ticket across every layer it touches

From Chapter 17: Folder structure: The floor plan of your codebase

---

## Task
You are a senior engineer scoping one representative
ticket this repo would handle, end to end. Pick the
ticket, say which one, and list every file you'd touch
to ship it.

## Input
The crawled source files (each as a path and its contents):
{codebase}

## Scaffold
A good ticket is a small feature or bug fix that
crosses several layers, like "let a shopper add a gift
note to an order: capture it at checkout, store it on
the order, and print it on the packing slip." Find the
files by following imports and references from the
feature's entry point, not by listing whatever sits in
the same folder.

For an online shop, that gift-note ticket might flow:
the route that accepts the note, the controller that
validates it, the model and migration that store it,
the job that renders the packing slip, then the tests
for each.

## Output
Return the ordered file list, entry point first and
tests last. Order them the way the request actually
flows through this repo's layers (entry point → handler
→ business logic → data → background work → output,
then the tests), using whatever layer names this repo
uses. For each file, give the folder, the file, and the
one line of work it does, on one line. For example:

    routes/orders.ts — declare POST /orders/:id/gift-note
    controllers/orders.ts — validate the note, save it
      on the order
    tests/orders.test.ts — assert the note lands on the
      order row

## Guidance
- Trace files by dependency, not proximity: follow the
  imports and references out from the entry point, not
  the files that merely share a folder. Proximity gives
  you a neighborhood; dependency gives you the real
  blast radius.
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy
  when it helps, explain any technical term the first
  time, and no brochure words.
