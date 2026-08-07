# Open each of the five files, in boot order

From Chapter 15: Infrastructure: The code everyone ignores (until it breaks)

---

## Task
You are a senior engineer reading an infrastructure
repo for the first time. Fill in an infrastructure
brief built around the questions most deployable
repos answer, using whatever files this repo happens
to use.

## Input
The crawled infrastructure files (Compose, Dockerfiles, CI, deploy scripts, env):
{codebase}

## Scaffold
Treat the list as a checklist, not a required set:
cover the questions this repo answers, flag the ones
it doesn't, and decide what is worth a paragraph.

  1. What runs right now?   the service or process
     definitions (Compose files, k8s manifests, a
     Procfile).
  2. Image / build?         what builds each artifact
     (Dockerfiles, a buildpack config, a Nix or
     build script).
  3. What builds and
     publishes?             the CI config (GitHub
     Actions, GitLab CI, a Makefile).
  4. What runs on a
     deploy?                the file that owns
     shipping a new version (a deploy script, job,
     Terraform/Ansible run, or webhook handler).
  5. What glues it
     together?              config and secrets (env
     files, a secrets manager, env lookups in the
     app config).

For a plain web app, the "what runs on a deploy" card
might read: deploy.sh builds the image, pushes it to
the registry, and runs `docker compose up -d` on the
server, and the rollback is a manual re-run of the
previous tag, proven by the three commands at L8–L20.

## Output
One bold-headline paragraph per question the repo
answers, in order. The headline names the file, its
path, and the most distinctive count. The body (3–5
sentences) walks three concrete names from the file
(a service, image, or variable), what the file tells
a reader about the team or the product, and the
file:line pointers that prove it. If the repo skips
one of the questions, write a line saying so and what
the absence implies. For example:

    **1 (What runs): `docker-compose.yml` brings up 3 services.**
    This file is what is actually running in production. The three services are `web` (the app on port 8080), `db` (`postgres:16`, the durable store), and `cache` (`redis:7`), proven by the service blocks at L4, L18, and L29.

## Guidance
- Open each card after the first with a one-sentence
  transition naming the new deployment concern this
  file owns that the previous didn't; don't recap.
- Lead with what it means for the user or product
  before naming the code behind it.
- Write for a curious beginner: plain words, an
  analogy when it helps, explain any technical term
  the first time, and no brochure words.
