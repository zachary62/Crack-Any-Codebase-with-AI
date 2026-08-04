"""Ch5 nodes: extract a product story from a codebase.

Four independent extractions (§5.1 to §5.4 of the chapter):
  - Pain scene (Curse of Knowledge)
  - Variant sentence (reproduce-it test)
  - Competitive positioning (counter-positioning)
  - Surprises and absences (Slack-and-Flickr signals)

Each is its own node with max_retries so bad LLM output retries cleanly.
"""
import os, re, sys, yaml
from pocketflow import Node

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils import call_llm, call_image, crawl  # noqa: E402

PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')


def load_prompt(name):
    return open(os.path.join(PROMPTS_DIR, name)).read()


def parse_yaml(text):
    m = re.search(r"```yaml\s*\n(.*?)```", text, re.DOTALL)
    assert m, f"LLM response missing ```yaml fence. Got:\n{text[:500]}"
    return yaml.safe_load(m.group(1))


def yaml_call(prompt, normalize, retries=4):
    """Call the model, parse its YAML, and validate/normalize it.

    On a bad reply (a flaky model sometimes emits invalid YAML, e.g. an
    unescaped quote inside a quoted string), retry with a changed prompt tail.
    The tail both dodges the response cache — so the retry is a genuinely fresh
    generation, not a replay of the cached miss — and nudges the model to fix
    its quoting. Network errors bubble up to the node's own max_retries."""
    last = None
    for k in range(retries):
        tail = "" if k == 0 else (
            f"\n\nReturn VALID YAML: put every string value in double quotes and "
            f"escape any double quote inside it as \\\". (retry {k})")
        try:
            return normalize(parse_yaml(call_llm(prompt + tail)))
        except (AssertionError, yaml.YAMLError, ValueError, KeyError) as e:
            last = e
    raise AssertionError(f"yaml_call gave up after {retries} tries. Last error: {last}")


class FetchRepo(Node):
    def prep(self, shared):
        return {
            "repo_path": shared["repo_path"],
            "include": shared.get("include") or None,
            "exclude": shared.get("exclude") or None,
        }

    def exec(self, ctx):
        return crawl(ctx["repo_path"], include=ctx["include"], exclude=ctx["exclude"])

    def post(self, shared, prep_res, exec_res):
        shared["codebase"] = exec_res
        print(f"  Crawled {len(exec_res):,} chars from {prep_res['repo_path']}")


class PainScene(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return load_prompt("pain-scene.md").format(codebase=shared["codebase"])

    def exec(self, prompt):
        return call_llm(prompt).strip()

    def post(self, shared, prep_res, exec_res):
        shared["pain"] = exec_res
        print(f"  Pain scene ({len(exec_res)} chars)")


class VariantSentence(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return load_prompt("variant-sentence.md").format(codebase=shared["codebase"])

    def exec(self, prompt):
        return call_llm(prompt).strip()

    def post(self, shared, prep_res, exec_res):
        shared["variant"] = exec_res
        print(f"  Variant sentence: {exec_res[:80]}...")


class CompetitivePositioning(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return load_prompt("competitive-positioning.md").format(codebase=shared["codebase"])

    def exec(self, prompt):
        def normalize(result):
            assert "competitors" in result and len(result["competitors"]) >= 2
            assert "dimensions" in result and len(result["dimensions"]) >= 3
            for k in ("sacrifices", "gains", "why_incumbents_cannot_copy"):
                assert k in result, f"missing {k} in positioning"
            # Each cell must be {verdict, detail}. Reject the old flat-string shape so a retry kicks in.
            for c in result["competitors"]:
                for cell in c.get("cells", []):
                    assert isinstance(cell, dict) and "verdict" in cell and "detail" in cell, \
                        f"cell missing verdict/detail in {c['name']}: {cell!r}"
            return result
        return yaml_call(prompt, normalize)

    def post(self, shared, prep_res, exec_res):
        shared["positioning"] = exec_res
        print(f"  Positioning: {len(exec_res['competitors'])} competitors, "
              f"{len(exec_res['dimensions'])} dimensions")


class IllustratePain(Node):
    """Generate a before/after cartoon illustration for the pain scene.

    Two steps:
      1. LLM writes a detailed image prompt from pain + variant.
      2. Image model renders it.

    THIS NODE IS OPTIONAL. The story renders fine without an image. Three
    paths land at "no image, story still complete":

      - No GEMINI_API_KEY in env. We never call the image model. The user is
        on a non-Gemini provider (Anthropic, OpenAI) and explicitly chose
        text-only.
      - CH5_NO_IMAGE=1 in env. Explicit opt-out, useful for CI or fast iter.
      - Image model call fails after retries (network, quota, model error,
        safety filter, whatever). We catch via exec_fallback and skip.

    In all three cases shared["pain_image_path"] ends up None, and the
    renderer omits the image cleanly.
    """
    def __init__(self):
        super().__init__(max_retries=2, wait=2)

    def prep(self, shared):
        return {
            "pain": shared["pain"],
            "variant": shared["variant"],
            "out_path": shared["pain_image_path_target"],
            "skip": not os.environ.get("GEMINI_API_KEY") or bool(os.environ.get("CH5_NO_IMAGE")),
        }

    def exec(self, ctx):
        if ctx["skip"]:
            # Don't regenerate, but keep any image a previous run already wrote —
            # so re-rendering the story (new prose, same repo) doesn't drop the art.
            return ctx["out_path"] if os.path.exists(ctx["out_path"]) else None
        prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')
        template = open(os.path.join(prompts_dir, "pain-illustration.md")).read()
        image_prompt = call_llm(template.format(pain=ctx["pain"], variant=ctx["variant"])).strip()
        return call_image(image_prompt, ctx["out_path"])

    def exec_fallback(self, prep_res, exc):
        # Retries are exhausted. The story is the point; the image is decoration.
        # Reuse an existing image if there is one; otherwise continue without art.
        print(f"  Illustration: failed after retries ({type(exc).__name__}: {exc}).")
        return prep_res["out_path"] if os.path.exists(prep_res["out_path"]) else None

    def post(self, shared, prep_res, exec_res):
        shared["pain_image_path"] = exec_res
        if exec_res:
            print(f"  Illustration: {os.path.basename(exec_res)}")
        elif prep_res["skip"]:
            reason = ("no GEMINI_API_KEY (image gen requires Gemini)"
                      if not os.environ.get("GEMINI_API_KEY")
                      else "CH5_NO_IMAGE=1 set")
            print(f"  Illustration: skipped ({reason})")
        # else: exec_fallback already printed the failure reason


class SurprisesAndAbsences(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return load_prompt("surprises-and-absences.md").format(codebase=shared["codebase"])

    def exec(self, prompt):
        def normalize(result):
            assert "present" in result and "absent" in result
            for p in result["present"]:
                for k in ("headline", "where", "bet"):
                    assert k in p, f"present item missing {k}: {p!r}"
            for a in result["absent"]:
                for k in ("headline", "evidence", "tradeoff"):
                    assert k in a, f"absent item missing {k}: {a!r}"
            return result
        return yaml_call(prompt, normalize)

    def post(self, shared, prep_res, exec_res):
        shared["surprises"] = exec_res
        print(f"  Surprises: {len(exec_res['present'])} present, "
              f"{len(exec_res['absent'])} absent")
