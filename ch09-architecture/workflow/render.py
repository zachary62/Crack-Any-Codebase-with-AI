"""Render the three architecture views as a self-contained HTML page + md twin.

One section per pass: the inventory (a service graph + a card per node), each
node's tech stack, and a trace of the core request. The service graph renders
via Mermaid with a parse-guard (a diagram the model gets wrong is dropped, not
shown as an error). Config snippets are syntax-highlighted.
"""
import html as _html
import os
import re
import sys

from markdown_it import MarkdownIt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

_MD = MarkdownIt("commonmark", {"html": False, "linkify": True, "breaks": False}).enable(["table"])


def _mermaidize(rendered_html):
    return re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        lambda m: f'<pre class="mermaid">{_html.unescape(m.group(1))}</pre>',
        rendered_html, flags=re.DOTALL,
    )


def md(text):
    if text is None:
        return ""
    out = _MD.render(str(text).strip()).strip()
    if out.startswith("<p>") and out.endswith("</p>") and out.count("<p>") == 1:
        return out[3:-4]
    return out


def md_rich(text):
    return _mermaidize(_MD.render(str(text or "").strip()))


def _esc(s):
    return _html.escape(str(s).strip())


def extract_mermaid(text):
    m = re.search(r"```mermaid\s*\n(.*?)```", text or "", re.DOTALL)
    return m.group(1).strip() if m else ""


def split_cards(markdown):
    cards, title, body = [], None, []
    for line in (markdown or "").splitlines():
        m = re.match(r'^###\s+(.*)', line)
        if m:
            if title is not None:
                cards.append((title.strip(), "\n".join(body).strip()))
            title, body = m.group(1), []
        elif title is not None:
            body.append(line)
    if title is not None:
        cards.append((title.strip(), "\n".join(body).strip()))
    return cards


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name}: architecture</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github-dark.min.css">
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>
  if (window.mermaid) mermaid.initialize({{ startOnLoad: false, theme: 'neutral', securityLevel: 'loose' }});
</script>
<script>
  window.addEventListener('load', async function () {{
    if (window.hljs) {{ try {{ hljs.highlightAll(); }} catch (e) {{}} }}
    if (!window.mermaid) return;
    var blocks = document.querySelectorAll('pre.mermaid');
    for (var i = 0; i < blocks.length; i++) {{
      var el = blocks[i], src = el.textContent;
      try {{
        if ((await mermaid.parse(src, {{ suppressErrors: true }})) === false) {{ el.remove(); continue; }}
        var out = await mermaid.render('mmd' + i, src);
        el.innerHTML = out.svg;
      }} catch (e) {{ el.remove(); }}
    }}
  }});
</script>
<style>
  :root {{
    --bg: #f7f8fa; --surface: #fff; --text: #101828; --muted: #667085;
    --faint: #98a2b3; --rule: #e4e7ec; --line: #eef0f3;
    --accent: #d97706; --accent-soft: #fffbeb; --good: #16a34a; --stone: #9aa4b2;
    --stone-bg: #f2f4f7; --shadow: 0 1px 2px rgba(16,24,40,.05); --radius: 12px;
  }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
    font-size: 13.5px; line-height: 1.5; background: var(--bg); color: var(--text); margin: 0;
    -webkit-font-smoothing: antialiased; }}
  code, .mono {{ font-family: 'JetBrains Mono', ui-monospace, Consolas, monospace; }}
  main {{ max-width: 1280px; margin: 0 auto; padding: 0 24px 56px; }}

  .hero {{ background: radial-gradient(120% 140% at 50% 0%, #3a2607 0%, #1c1203 70%);
    color: #fff; padding: 46px 20px 42px; text-align: center; }}
  .hero-inner {{ max-width: 1120px; margin: 0 auto; }}
  .hero-diagram {{ margin: 18px 0 4px; }}
  .hero-diagram-cap {{ font-size: .7rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase;
    color: var(--accent); margin: 0 2px 9px; }}
  .eyebrow {{ display: inline-flex; align-items: center; gap: 7px; color: #fcd34d;
    font-size: .68rem; font-weight: 700; letter-spacing: .18em; text-transform: uppercase; }}
  .eyebrow::before {{ content: ''; width: 16px; height: 2px; background: #f59e0b; border-radius: 2px; }}
  .hero h1 {{ font-size: 1.9rem; font-weight: 800; letter-spacing: -.025em; margin: 12px 0 10px; }}
  .hero .sub {{ font-size: .94rem; color: #eee0c4; margin: 0 auto; line-height: 1.6; }}

  .sec-head {{ display: flex; align-items: baseline; gap: 10px; margin: 42px 2px 14px; }}
  .sec-n {{ font-family: 'JetBrains Mono', monospace; font-size: .68rem; font-weight: 700; color: var(--accent); }}
  .sec-label {{ display: flex; align-items: center; gap: 9px; font-size: .68rem; font-weight: 700;
    letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }}
  .sec-label::before {{ content: ''; width: 3px; height: 14px; background: var(--accent); border-radius: 2px; }}
  .sec-note {{ font-size: .8rem; color: var(--faint); }}
  .scroll-hint {{ margin-left: auto; font-size: .68rem; font-weight: 600; color: var(--faint); }}

  /* Friendly "start here" welcome + per-section intros */
  .intro {{ background: var(--surface); border: 1px solid var(--rule); border-left: 4px solid var(--accent);
    border-radius: var(--radius); box-shadow: var(--shadow); padding: 20px 24px; margin: 30px 0 4px; }}
  .intro-label {{ font-size: .68rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase;
    color: var(--accent); margin-bottom: 10px; }}
  .intro p {{ margin: .5em 0; font-size: .96rem; color: #344054; line-height: 1.7; }}
  .intro p:first-child {{ margin-top: 0; }}
  .intro strong {{ color: var(--text); }}
  .sec-intro {{ font-size: .9rem; color: #475467; line-height: 1.6; margin: -4px 2px 12px; }}
  .sec-intro p {{ margin: 0; }}

  .verdict {{ background: var(--accent-soft); border: 1px solid #fde68a; border-radius: var(--radius);
    padding: 12px 16px; margin-bottom: 14px; font-size: .9rem; color: #713f12; }}
  .verdict strong {{ color: #78350f; }}

  .diagram {{ background: var(--surface); border: 1px solid var(--rule); border-radius: var(--radius);
    box-shadow: var(--shadow); padding: 16px; margin-bottom: 16px; overflow-x: auto; }}
  .diagram pre.mermaid {{ margin: 0; text-align: center; background: transparent; }}
  .diagram pre.mermaid svg {{ max-width: 100%; height: auto; }}

  .rail {{ display: flex; gap: 16px; align-items: stretch; overflow-x: auto;
    scroll-snap-type: x proximity; padding: 4px 2px 18px; margin: 0; list-style: none; }}
  .rail::-webkit-scrollbar {{ height: 9px; }}
  .rail::-webkit-scrollbar-track {{ background: var(--line); border-radius: 5px; }}
  .rail::-webkit-scrollbar-thumb {{ background: #cbd2dc; border-radius: 5px; }}

  .scroll {{ flex: 1; overflow-y: auto; overscroll-behavior: contain; }}
  .scroll::-webkit-scrollbar {{ width: 9px; }}
  .scroll::-webkit-scrollbar-thumb {{ background: #dce0e7; border-radius: 5px; }}

  .card {{ scroll-snap-align: start; background: var(--surface); border: 1px solid var(--rule);
    border-radius: var(--radius); box-shadow: var(--shadow); border-top: 3px solid var(--accent);
    display: flex; flex-direction: column; overflow: hidden; max-height: 72vh; }}
  .card-top {{ flex-shrink: 0; padding: 14px 18px 12px; border-bottom: 1px solid var(--line);
    background: linear-gradient(180deg, #fffdf7, #fff); font-weight: 700; font-size: .96rem; line-height: 1.35; }}
  .card-top code {{ font-size: .82em; }}
  .card-body {{ padding: 13px 18px 16px; font-size: .84rem; }}
  .card-body p {{ margin: .5em 0; color: #344054; line-height: 1.6; }}
  .card-body p:first-child {{ margin-top: 0; }}
  .card-body strong {{ color: var(--text); }}
  .card-body em {{ color: var(--muted); }}
  .card-body ul, .card-body ol {{ margin: .5em 0; padding-left: 1.3em; }}
  .card-body li {{ margin: .28em 0; color: #344054; line-height: 1.55; }}

  .rail.inv .card {{ flex: 0 0 380px; width: 380px; }}
  .rail.tech .card {{ flex: 0 0 420px; width: 420px; }}
  .rail.trace .card {{ flex: 0 0 460px; width: 460px; }}

  pre {{ background: #0f172a; color: #e2e8f0; border-radius: 8px; padding: 11px 13px; overflow-x: auto; margin: 10px 0; }}
  pre code {{ padding: 0; font-size: .74rem; line-height: 1.5; }}
  pre code.hljs {{ background: transparent; padding: 0; color: #e2e8f0; }}
  code {{ font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: .84em;
    background: var(--stone-bg); color: var(--text); padding: 1px 5px; border-radius: 4px; }}

  footer {{ color: var(--faint); font-size: .74rem; text-align: center; margin-top: 44px;
    padding-top: 18px; border-top: 1px solid var(--rule); }}
  @media (max-width: 560px) {{ .card {{ flex-basis: 86vw !important; width: 86vw !important; }} }}
</style>
</head>
<body>
  <header class="hero">
    <div class="hero-inner">
      <span class="eyebrow">Architecture</span>
      <h1>{name}</h1>
      <p class="sub">{subtitle}</p>
    </div>
  </header>
  <main>
{intro}
{sections}
    <footer>Overlaid from {n_config} config files, {n_deps} dependencies, {n_int} integrations.</footer>
  </main>
</body>
</html>
"""


def _card(header_md, body_md):
    return (
        '      <li class="card">\n'
        f'        <div class="card-top">{md(header_md)}</div>\n'
        f'        <div class="scroll"><div class="card-body">{md_rich(body_md)}</div></div>\n'
        '      </li>'
    )


def _section(n, label, note, rail_class, cards_html, prefix_html="", intro=""):
    intro_html = f'    <div class="sec-intro">{intro}</div>\n' if intro else ""
    return (
        '    <div class="sec-head">\n'
        f'      <span class="sec-n">{n}</span>\n'
        f'      <div class="sec-label">{label}</div>\n'
        f'      <div class="sec-note">{note}</div>\n'
        '      <div class="scroll-hint">swipe &rarr;</div>\n'
        '    </div>\n'
        f'{intro_html}{prefix_html}'
        f'    <ul class="rail {rail_class}">\n{cards_html}\n    </ul>'
    )


def _welcome_html(shared):
    w = (shared.get("overview") or {}).get("welcome", "")
    if not w:
        return ""
    return ('    <section class="intro">\n'
            '      <div class="intro-label">The big picture</div>\n'
            f'      {md_rich(w)}\n'
            '    </section>')


def _intro(shared, title):
    text = (shared.get("overview") or {}).get("intros", {}).get(title, "")
    return md_rich(text) if text else ""


def render_html(name, shared):
    verdict = shared.get("shape_verdict", "")
    # The big-picture summary IS the hero subtitle (no duplicate card).
    welcome = (shared.get("overview") or {}).get("welcome", "")
    subtitle = md(welcome) or md(verdict) or "A multi-service architecture, read three ways."

    # The service graph is the "big picture" — promoted above the sections.
    diagram = shared.get("arch_diagram", "")
    hero_diagram = (
        '    <section class="hero-diagram">\n'
        '      <div class="hero-diagram-cap">The whole system on one map</div>\n'
        f'      <div class="diagram"><pre class="mermaid">{diagram}</pre></div>\n'
        '    </section>\n'
    ) if diagram else ""

    sections = []

    # 01 — Inventory: node cards (graph now lives in the hero above)
    inv_cards = "\n".join(_card(h, b) for h, b in split_cards(shared.get("inventory_md", "")))
    sections.append(_section("01", "The inventory", "every node, sorted by band: run · rent · call · client",
                             "inv", inv_cards, intro=_intro(shared, "The inventory")))

    tech_cards = "\n".join(_card(h, b) for h, b in split_cards(shared.get("techstack_md", "")))
    sections.append(_section("02", "Tech stack", "open each box: the real technology inside the label",
                             "tech", tech_cards, intro=_intro(shared, "Tech stack")))

    trace_cards = "\n".join(_card(h, b) for h, b in split_cards(shared.get("trace_md", "")))
    sections.append(_section("03", "The trace", "one request, hop by hop, and how each variant differs",
                             "trace", trace_cards, intro=_intro(shared, "The trace")))

    stats = shared.get("arch_stats", {})
    return HTML_TEMPLATE.format(
        name=_esc(name),
        subtitle=subtitle,
        intro=hero_diagram,
        sections="\n".join(sections),
        n_config=stats.get("config_files", 0),
        n_deps=stats.get("deps", 0),
        n_int=stats.get("integrations", 0),
    )


def render_markdown(name, shared):
    parts = [f"# {name}: architecture\n"]
    if shared.get("shape_verdict"):
        parts.append(f"**Shape verdict:** {shared['shape_verdict']}\n")
    if (shared.get("overview") or {}).get("welcome"):
        parts.append(shared["overview"]["welcome"].strip() + "\n")
    parts.append("## The inventory\n")
    parts.append(shared.get("inventory_md", "").strip() + "\n")
    parts.append("## Tech stack\n")
    parts.append(shared.get("techstack_md", "").strip() + "\n")
    parts.append("## The trace\n")
    parts.append(shared.get("trace_md", "").strip() + "\n")
    return "\n".join(parts)
