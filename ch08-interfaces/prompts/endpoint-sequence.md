## Task
You are a senior engineer documenting one API endpoint for a
new developer: show the exact order of messages between
services, from the request arriving to the response going
back. Keep it friendly enough that a beginner follows it.

## Input
The route definition, the flow it belongs to, and the
handler's source code:
{routes}

The flow it belongs to: {flow}

Handler source:
{handler_source}

## Scaffold
An endpoint runs in two halves split by the moment it answers
the user. Everything above the response line is work the user
waits for: gateway checks, validation, the database read and
write. Everything below it fans out after the user already
has their answer: emails, webhooks, calls to other companies'
APIs.

For a shop's `POST /checkout`, the split falls right after
the order row commits: validating the cart, charging the
card, and writing the order all run above the line, while the
receipt email and the warehouse webhook fire below it, after
the shopper sees "Order placed."

## Output, in this exact order

1. Two lines naming the endpoint and what it does, then a
   one-line subtitle with the participant and message counts:

       **Endpoint:** `POST /book/event`
       **Title:** A single "Confirm" click triggers a chain of
       services.
       **Subtitle:** 6 participants, 16 messages.

2. A Mermaid `sequenceDiagram` in a ```mermaid fence: one
   participant per service (client, gateway, main service,
   database, plus the external services it fans out to), one
   message per arrow. Sync messages are solid arrows (`->>`),
   async ones dashed (`-->>`); time flows top to bottom, and
   the response arrow back to the client divides the
   synchronous section from the async fan-out. Cap it at about
   5-7 participants so it stays readable. Follow these rules
   EXACTLY or the diagram breaks and gets dropped:
   - Declare EVERY participant up top with a short alias:
     `participant BK as Booking Service`. Include external
     services (Stripe, Daily.co, an email provider) as their
     own declared participants.
   - Every arrow's two ends must be declared aliases — e.g.
     `BK->>EX: ...`. NEVER write an inline participant like
     `BK->>(External Webhook): ...`; declare `EX as External
     Webhook` first and use `EX`.
   - Message labels are plain text — no parentheses, colons,
     brackets, or quotes inside a label. Put file refs in the
     numbered list below, not in the diagram.
   - Use a `Note over BK,EX: async fan-out` line to mark the
     split if it helps.

3. A `### Messages` header, then the messages as a numbered
   list — the key hops in full, trailing off with
   `(... K more)` if it runs long. Each is
   `**N. From -> To**: short label (file:line)`. For example:

       1. **Client -> Gateway**: POST /book/event (event.ts:17)

4. A `### Description` header with 1-2 sentences naming the
   sync/async split, then a `### Key takeaway` header with one
   line naming the pattern (respond fast, fan out later) and
   its cost: a failure in the async steps doesn't roll back
   the core write.

## Guidance
- Put the response arrow on the line that truly divides sync
  from async; treat everything below it as best-effort that
  can fail without the user knowing.
- Lead each message label and paragraph with the user-visible
  effect before naming the internal service. Write for a
  curious beginner: plain words, an analogy when it helps, no
  brochure words.
