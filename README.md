# Crack Any Codebase with AI

Companion repo for the book **Crack Any Codebase with AI**.

> You don't need to understand the code. You need to understand the architecture. Mental models plus AI equals 10x faster codebase comprehension.

Each chapter ships either a small bespoke script or a PocketFlow pipeline with an equivalent agent skill file. The same prompts power both routes, so you can run the script when the repo is huge and use the skill file day to day in your agent.

## Chapter map

### Part 1. The AI Toolkit

| Ch | Title | Code | Format |
| -- | ----- | ---- | ------ |
| 1 | The Shift. Code Is Free Now. Understanding Isn't. | _(narrative only)_ | . |
| 2 | Chat. Paste code, get answers. | [`ch02-chat/`](ch02-chat/) | script |
| 3 | Workflow. From Ad Hoc Questions to Systematic Understanding. | [`ch03-workflow/`](ch03-workflow/) | workflow + skill (base) |
| 4 | Agent. Stop Telling AI What to Read. Let It Decide. | [`ch04-agent/`](ch04-agent/) | script |

### Part 2. Understand the Why

| Ch | Title | Code | Format |
| -- | ----- | ---- | ------ |
| 5 | Product Intent. Reverse Engineer the PRD. | [`ch05-product-intent/`](ch05-product-intent/) | workflow + skill |
| 6 | Git History. Your Product Roadmap Is Already Written. | [`ch06-git-history/`](ch06-git-history/) | workflow + skill |

### Part 3. Understand the What

| Ch | Title | Code | Format |
| -- | ----- | ---- | ------ |
| 7 | Schema. A Fossilized Argument. | [`ch07-schema/`](ch07-schema/) | workflow + skill |
| 8 | Interfaces. Where the Product's Verbs Live. | [`ch08-interfaces/`](ch08-interfaces/) | workflow + skill |
| 9 | Architecture. The Graph of Programs and Wires. | [`ch09-architecture/`](ch09-architecture/) | workflow + skill |

### Part 4. Understand the How

| Ch | Title | Code | Format |
| -- | ----- | ---- | ------ |
| 10 | Backend. The Same Six Layers, Every Time. | [`ch10-backend/`](ch10-backend/) | workflow + skill |

Chapters 11 through 18 follow the same shape: one workflow, one set of prompts, one skill file.

## Install once

```bash
git clone https://github.com/zachary62/Crack-Any-Codebase-with-AI
cd Crack-Any-Codebase-with-AI

pip install -r utils/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # or OPENAI_API_KEY, or GEMINI_API_KEY
```

Smoke test the LLM wrapper:

```bash
python -m utils.call_llm
# prints: ready
```

Then `cd` into any chapter directory and follow its `README.md`.

## Try it on a real repo in three commands

```bash
git clone https://github.com/karpathy/micrograd path/to/repo

cd ch03-workflow/workflow
python main.py path/to/repo --out ../output/micrograd-tour
```

You get `index.md` plus one tutorial chapter per abstraction. A sample run is checked in at [`ch03-workflow/output/micrograd-tour/`](ch03-workflow/output/micrograd-tour/).

For a smaller test that finishes in seconds, point Ch5 at the PocketFlow chat example:

```bash
cd ch05-product-intent/workflow
python main.py path/to/repo --out ../output/pocketflow-chat-prd.md
```

That writes a real one page PRD: see [`ch05-product-intent/output/pocketflow-chat-prd.md`](ch05-product-intent/output/pocketflow-chat-prd.md).

## Caching

`utils/call_llm.py` caches every response to disk under `utils/.cache/` keyed by `sha256(provider + model + prompt)`, so re-running on the same repo replays from disk instead of paying for the same LLM call twice. The directory is gitignored. Disable with `LLM_CACHE=0`; clear with `rm -rf utils/.cache`.

## Shared utilities

Every chapter that calls an LLM imports from the same place:

```python
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils import call_llm, crawl
```

`utils/call_llm.py` picks the provider based on which env var you set (Anthropic, OpenAI, or Gemini). Override with `LLM_PROVIDER=<name>` and `ANTHROPIC_MODEL` / `OPENAI_MODEL` / `GEMINI_MODEL`.

