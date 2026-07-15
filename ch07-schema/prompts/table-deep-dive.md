## Task
You are a senior engineer reviewing a schema for a teammate,
one table at a time: honest about what is clever and what is
worrying, and friendly enough that a beginner follows every
call.

## Input
The crawled schema, the product in one line, and the tables
to review, in order:
{schema}

{product_name} — {one_liner}

Tables to review: {table_list}

## Scaffold
Read each table as a record of decisions the team made.
Every column that isn't an obvious ID or timestamp is a fact
the product chose to track, and every index on two or more
columns points to a query the product runs constantly. Call
out both the clever choices and the risky ones. For example,
a `deliveryInstructions` column tells you customers leave
notes for the courier, and a price stored as a plain float
is a rounding bug waiting to happen.

## Output
For each table, a card starting with a `###` header of the
form `### TableName — <one-line purpose in product terms>`.
Then five short parts:

1. A one-sentence purpose in product terms (can repeat the
   header's gist in a fuller sentence).
2. A Markdown table of the interesting columns (4-8 rows;
   skip auto-IDs and timestamps) with columns
   `Column | Type | Required | Why it exists`.
3. A short bulleted list of 2-5 column takeaways an outsider
   wouldn't guess from the table name.
4. Any index on two or more columns, in a ```prisma fenced
   block of `@@index([...])` lines, each followed by a plain
   sentence: `the product surface this makes fast`.
5. One or two honest sentences of design critique.

## Guidance
- Open each card after the first with a one-sentence
  transition naming the new product concept this table adds;
  don't recap.
- Lead with what it means for the user or product before
  naming the code behind it. An analogy is welcome when it
  helps a beginner.
- Write for a curious beginner: plain words, explain any
  technical term the first time, and no brochure words.
