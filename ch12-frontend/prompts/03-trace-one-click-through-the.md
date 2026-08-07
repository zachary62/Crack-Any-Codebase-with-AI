# Trace one click through the five trigger kinds

From Chapter 12: Frontend: Every UI is the same component tree

---

## Task
You are a senior frontend engineer tracing one user action
end to end. Pick the most central action the product exists
for (signup, checkout) and walk it from the first click to
the final UI change.

## Input
The crawled source files (each as a path and its contents):
{codebase}

## Scaffold
Every UI update comes from one of five triggers: a route
change, a click, a form submit, a query result landing, and
an effect firing. Three are fired by the user (route, click,
submit) and two fire on their own (query, effect). Walk the
action so the trace spans all five.

For a social feed, opening `/feed` is a route trigger, tapping
a post's like button is a click, posting a comment is a
submit, the next page of posts arriving as you scroll is a
query, and a scroll-position restore that runs after the list
renders is an effect.

## Output
1. A numbered bulleted trace of at least 5 steps spanning all
   five trigger kinds. Each bullet is bold-headlined with the
   step number, the trigger kind, and a short label for what's
   changing, then a 3–5 sentence body: what the user sees
   before and after in plain terms, the one line of code that
   fires and its file path (inline parens are fine), and what
   the framework is doing underneath. For example:

       **Step 3 — submit: "Post comment" box**
       (`components/CommentBox.tsx`). The box holds the typed
       draft; after Enter it empties and the new comment
       appears at the bottom of the thread. The line that
       fires is `onSubmit={() => addComment(draft)}`, which
       sends the comment and clears the box.

2. A 2–3 sentence "what this trace reveals" paragraph about
   the codebase's architecture.

## Guidance
- Open each step after the first with a one-sentence
  transition naming the new trigger kind or framework
  mechanism it introduces that the previous one didn't; don't
  recap.
- Name React, Next.js, or the data-fetching library directly
  when it's the teaching point, but still lead each step with
  the user-visible effect before the framework mechanic.
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy when
  it helps, explain any technical term the first time, and no
  brochure words.
