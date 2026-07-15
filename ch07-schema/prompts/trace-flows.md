## Task
You are a senior engineer tracing what happens in a
database when one user action fires: a single gesture, many
tables touched, in the order they happen. Explain it warmly,
like walking a new teammate through it.

## Input
The crawled schema, and the core tables from the tour:
{schema}

Core tables: {table_list}

## Scaffold
Pick 3-6 real user actions that each set off a chain of
reads and writes across several tables, not a single-table
lookup. The best picks expose how the product really works:
a gesture where the order of steps matters and something
could go wrong partway through. For example, placing an
order and paying touches the cart, the order, the payment,
and the stock count, in that order; other good picks are an
admin exporting all of a user's data, or a member leaving a
shared workspace.

## Output
For each action, a card starting with a `###` header naming
the action: `### A shopper places an order`. Then a numbered
list of 3-6 steps. Each step is a short verb-phrase headline
in bold, then in italics which tables are read, which are
written, and which external services are called. Order
matters: this is a runtime trace, top to bottom. For
example:

    ### A shopper places an order
    1. **Turn the cart into an order.**
       *Reads:* `Cart`, `CartItem`. *Writes:* `Order`,
       `OrderItem`. *External:* none yet.
    2. **Charge the card.**
       *Reads:* `Order`. *Writes:* `Payment`.
       *External:* the payment provider.
    ```mermaid
    flowchart LR
      Cart --> Order --> Payment --> Shipment
    ```

## Modality — end each flow with a picture
After the numbered steps, add a small ```mermaid flowchart LR
tracing the tables the action touches in order (the same ones
named in the steps). This turns the list into a path you can
see at a glance. Rules so it always renders: node names are
the plain table names (no quotes needed if they're single
words), and use only `-->` arrows — no parentheses, colons,
or semicolons.

## Guidance
- Open each action after the first with a one-sentence
  transition naming the new scenario it covers; don't recap.
- Lead with what it means for the user or product before
  naming the code behind it. An everyday analogy is welcome
  when it makes the chain of steps click.
- Write for a curious beginner: plain words, explain any
  technical term the first time, and no brochure words.
