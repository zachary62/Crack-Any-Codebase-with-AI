# Open one screen and read the component tree

From Chapter 12: Frontend: Every UI is the same component tree

---

## Task
You are a senior frontend engineer writing a teaching
artifact for a new hire. Pick the busiest screen from the
screen inventory and return three lined-up views of it: a
wireframe, a component tree, and the root component's JSX.

## Input
The crawled source files (each as a path and its contents):
{codebase}

## Scaffold
A screen's visual hierarchy is its component hierarchy: a box
that holds three smaller boxes on screen is a parent that
renders three children in the code. Line up three views so
each labelled rectangle maps to a named component and to the
JSX that draws it.

For an online shop's product page, the outer card holds an
image gallery, a title-and-price block, and an "Add to cart"
button; in the tree those are three child components under
one parent, and the JSX nests them in that same order.

## Output
1. A wireframe outline: the screen's visible regions as
   nested indented rectangles, each labelled by what the user
   sees (form, button, header) with the component name in
   parens. Use indentation to show nesting. For example: a
   **Product card** (`<ProductCard>`) rectangle holding an
   **Image gallery** (`<Gallery>`) and an **Add-to-cart
   button** (`<Button>`), each indented under it.

2. The component tree: the same nesting as an indented list
   of component names with the file path next to each. How it
   looks: `<Gallery>` (`src/components/shop/Gallery.tsx`), one
   line per component, indented to match the wireframe.

3. A JSX excerpt: about 20 lines from the root component
   file, as a plain fenced code block with the right language
   tag, nesting in the same shape as the wireframe, followed
   by a one-line explanation of how it maps to the rectangles.

4. A 1–2 sentence takeaway naming the architectural pattern
   that organises the screen this way, leading with what the
   visible layout reveals before any library or convention.

## Guidance
- Every label in the wireframe and tree should match a
  visible UI region (form, button, header) before naming any
  internal component or hook.
- Lead with what it means for the user or product before
  naming the code behind it.
- Write for a curious beginner: plain words, an analogy when
  it helps, explain any technical term the first time, and no
  brochure words.
