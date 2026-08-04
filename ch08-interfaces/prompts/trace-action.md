## Task
You are a senior engineer tracing a single user action
through a product's API for a new developer: one gesture,
many endpoints, in the order they fire. Explain it warmly, so
a beginner follows every hop.

## Input
The crawled API routes, and the feature groups from the menu:
{routes}

Feature groups: {groups}

## Scaffold
Pick 4-8 user actions whose API paths differ in kind, not
just in detail, and cover the range: at least one read-only
flow, one write-heavy flow, one flow no user triggers (a
scheduled job firing on its own), and one admin-only flow.

For an online shop, a good spread is browsing the catalog
(read-only), placing an order (write-heavy), a nightly job
that emails abandoned-cart reminders (no user in the loop),
and an admin issuing a refund (admin-only) — four gestures
that each light up a different set of services.

## Output
One card per action, each starting with a `###` header naming
the flow: `### Book a 30-min intro call`. Then, on the next
lines, three labels:

    **Flow:** <the flow name again>
    **Title:** <one line: what the user is doing>
    **Sub:** <one line: the lane count, the event count, and
    which lane the user waits on>

Right after those three lines, add a small ```mermaid
flowchart LR of the lanes in the order they fire, with a
dashed `-.->` into the lanes that run AFTER the response
returns — e.g. `Slots --> Bots --> Booking --> Calendar --> Video`
then `Booking -.-> Email` and `Booking -.-> Webhooks`. Use
plain single-word lane names and `-->` / `-.->` arrows only —
no parentheses, colons, or semicolons in labels.

Then the flow as bold-headline lane paragraphs, in the order
they fire. Each lane is 3-5 sentences naming the service or
feature group that handles it and the endpoint calls inside
it (method, path, one-line description). For example:

    **Lane 1 · Cart.** The shopper's saved items load when the
    page opens. `GET /cart` reads the cart rows; this lane is
    read-only and the only one a logged-out visitor can reach.

## Guidance
- Keep the lanes in the order they actually fire; this is a
  runtime trace, top to bottom, not a grouping.
- Say which lane blocks the spinner and which run AFTER the
  response returns; that line is the whole point of the trace.
- Open each flow after the first with a one-sentence
  transition naming the new kind of action it covers — a read
  instead of a write, a job with no user, an admin path; don't
  recap.
- Lead with what it means for the user or product before
  naming the code behind it. Write for a curious beginner:
  plain words, an analogy when it helps, no brochure words.
