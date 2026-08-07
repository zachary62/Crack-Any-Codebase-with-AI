# Ask the LLM to map the five files, read two ways

From Chapter 15: Infrastructure: The code everyone ignores (until it breaks)

---

## Task
You are a senior engineer mapping an infrastructure
repo for the first time. Put the whole deployment on
one page, split into two readings:
  (A) the config that RUNS the platform itself
  (B) the code the platform RUNS to deploy an app

## Input
The crawled infrastructure files (Compose, Dockerfiles, CI, deploy scripts, env):
{codebase}

## Scaffold
Most deployable repos answer a handful of
infrastructure questions, but every repo answers them
with different files and some skip a few. Treat the
list as a checklist, not a required set: cover
whatever this repo has, note what it lacks, and
decide what is worth showing.

  1. What runs?         the running services or
     processes (a Compose file, k8s manifests, a
     Procfile, a systemd unit).
  2. Image / build?     how the app becomes a
     runnable artifact (a Dockerfile, a buildpack,
     Nix, a plain build script).
  3. CI?                what builds, tests, and
     publishes (GitHub Actions, GitLab CI, a
     Makefile).
  4. Deploy?            what ships a new version to
     production (a deploy script, a job, a Terraform
     or Ansible run, a platform webhook).
  5. Config & secrets?  where settings and secrets
     live (env files, a secrets manager, config
     files).

For a plain web app, the (A) side might be a
docker-compose.yml of 3 services plus a
.github/workflows/deploy.yml, while the (B) side is
empty because the app deploys itself and never
provisions anything for a user, which is worth saying
out loud.

## Output
A map of whichever questions this repo answers. For
each question, give the file that answers it, its
most distinctive count (services, files, workflows,
vars), and which reading (A or B) it belongs to. If the repo has no
answer to one of them, say so in a line and what that
absence implies (no CI usually means deploys are
manual). Then answer the two questions a reader
actually has before opening anything: where does the
config live, and where does the deploy logic run?
For example:

    | # | File | Count | Reading |
    |---|---|---|---|
    | 1 | `docker-compose.yml` | 3 services: web, db, cache | (A) runs the app |

## Guidance
- Lead with what it means for the user or product
  before naming the code behind it.
- Write for a curious beginner: plain words, an
  analogy when it helps, explain any technical term
  the first time, and no brochure words.
