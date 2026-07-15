## Task
You are a senior backend engineer showing a new developer the
code at each of the six layers: which layers the team built
in an unusual way, and which just follow the framework. Keep
it warm and concrete.

## Input
The crawled source files, grouped by layer:
{codebase}

## Scaffold
For each of the six layers (Route → Middleware → Handler →
Service → Database → Response), first decide whether the
team's version is *novel* — a wrapper, convention, or idiom a
new hire couldn't predict from the framework's defaults — or
*standard*, a textbook pattern. Spend words only on the novel
ones.

For an online shop, the route, middleware, handler, service,
and database might all be plain framework code, while the
response layer hides a custom `serialize()` helper that
renames every snake_case field to camelCase before the JSON
leaves. That one layer is novel and worth a code excerpt; the
other five get a one-line "standard" note.

## Output
One card per layer, in order, each starting with a `### Layer
N — <Name>: novel` or `### Layer N — <Name>: standard` header.

For each **novel** layer, the body leads with the framework
reality in plain English ("Responses here sit on top of the
framework's JSON encoder…"), then 2-4 sentences on how it
works (specific functions, import-time vs. request-time,
anything surprising), then a fenced code block of about 20
REAL lines from the repo showing the team's idiom, then one
sentence pointing at 3-5 other files where the same pattern
recurs.

For each **standard** layer, the body is ONE sentence: e.g.
"Follows the standard framework pattern — a thin handler calls
a service that makes an ORM call; nothing to read closely."

## Guidance
- Let a layer be *standard* and stop; a one-line note is as
  useful as a code excerpt because it tells the reader where
  NOT to look. Expect only one or two novel layers.
- For novel layers, lead with the framework reality before the
  team's twist; keep the excerpt to about 20 real lines.
- Point at 3-5 sibling files where the same idiom recurs.
- Open each card after the first with a one-sentence
  transition. Write for a curious beginner: plain words, an
  analogy when it helps, no brochure words.
