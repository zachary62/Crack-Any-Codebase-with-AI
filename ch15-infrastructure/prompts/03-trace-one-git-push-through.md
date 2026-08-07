# Trace one git push through eight deploy stages

From Chapter 15: Infrastructure: The code everyone ignores (until it breaks)

---

## Task
You are a senior engineer tracing one deploy through
an infrastructure repo. Pick one representative
deploy and follow it end to end, from the trigger to
"new version live, old one retired".

## Input
The crawled infrastructure files (Compose, Dockerfiles, CI, deploy scripts, env):
{codebase}

## Scaffold
Pick one representative deploy this repo performs. A
typical one starts when a change is pushed (a git
push, a tagged release, or a manual deploy command),
a trigger fires (a webhook, a CI run, a queued job),
and several steps later a new version is taking
traffic while the old one is gone. If the repo
deploys more than one way, pick the most common and
say so.

For a plain web app, the trace might run: push to
main, the CI workflow fires, the image builds, it
gets pushed to the registry, the server pulls the new
image and restarts the app, the health check passes,
and the old container is stopped. Seven hops from
trigger to live traffic.

## Output
Walk the trace from the trigger to "new version live,
old one retired" as a numbered bulleted list, one
bullet per hop. Follow the steps the deploy code
actually runs; don't pad or merge them, and let the
real flow set the number of hops. Each bullet is
bold-headlined with the hop number and a short label
for what runs. After the headline, give the concrete
data or call at this step in backticks (the endpoint
hit, the function called, the command run), in parens
the file path and line number, and which
infrastructure concern this step touches (what-runs,
image, CI, deploy, or config). After the list, write
a 2–3 sentence "what this trace reveals" paragraph
about deploy pipeline architecture. For example:

    - **Hop 4 (build the image)**: with the code on disk, this hop turns it into a runnable artifact. `docker build -t app:sha .` (`scripts/deploy.sh:42`), touches image.

## Guidance
- Open each hop after the first with a one-sentence
  transition naming the new deploy responsibility
  this hop owns that the previous didn't; don't recap.
- Lead with what it means for the user or product
  before naming the code behind it.
- Write for a curious beginner: plain words, an
  analogy when it helps, explain any technical term
  the first time, and no brochure words.
