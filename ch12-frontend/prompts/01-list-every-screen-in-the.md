# List every screen in the app

From Chapter 12: Frontend: Every UI is the same component tree

---

## Task
You are a senior frontend engineer mapping the user-facing
surface of a codebase. Walk the most central user flow
(signup, checkout, the one the product exists for) as a
first-time user, and list every screen they move through in
the order a typical user meets them.

## Input
The crawled source files (each as a path and its contents):
{codebase}

## Scaffold
A screen is a visual state, not a URL: the same URL can host
several screens when a page has steps or modes. Count by what
the user sees, and name the root component that mounts each
screen so the map stays tied to the code.

For an online shop, the `/checkout` URL might hold three
screens — review the cart, enter the address, then pay —
switched by a step variable rather than by the URL. Listing
them by route would find one screen; listing them by what's
on screen finds three.

## Output
1. One bold-headline paragraph per screen, 3–5 sentences.
   The headline names the step number, the screen name, the
   URL pattern, and the root component (React, Vue, or Svelte)
   that mounts there; the body describes what the user sees
   and can do, leading with the visible UI before any
   component, hook, or store. For example:

       **Screen 1 — Cart review (`/checkout`, root
       `<CartReview>`).** The first thing the shopper sees: a
       list of items with quantities and a running total, plus
       a "Continue to address" button. Only quantity is
       editable so far.

2. A Mermaid `stateDiagram-v2` alongside the paragraphs: one
   state per screen, transitions labelled by the click or
   submit that moves the user forward. Keep it readable on one
   screen.

## Guidance
- Where a screen's rendering style matters, mark it server- or
  browser-rendered in a short phrase, so the reader knows where
  its data-fetching lives; don't force it on every screen.
- Open each screen after the first with a one-sentence
  transition naming the new state or affordance it adds that
  the previous didn't: a new piece of URL state, a new form,
  or a new server query; don't recap.
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy when
  it helps, explain any technical term the first time, and no
  brochure words.
