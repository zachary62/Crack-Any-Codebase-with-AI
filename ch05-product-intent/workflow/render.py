"""Render the product story as markdown and clean HTML.

HTML stays self-contained: one file, embedded CSS, fonts via CDN (Inter for
body, JetBrains Mono for code). No JS framework, no build step. Visual style
inspired by a polished product brief: dark gradient hero, eyebrow-style
section labels with accent bars, cards with subtle shadows, numbered badges
on surprises, amber "on purpose" badges on absences.
"""
import html as _html
import os
import sys

from markdown_it import MarkdownIt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

_MD = MarkdownIt(
    "commonmark", {"html": False, "linkify": True, "breaks": False}
).enable(["table"])


def md(text):
    """Inline markdown to HTML for a short string. Strips the wrapping <p>...</p>."""
    if text is None:
        return ""
    rendered = _MD.render(str(text).strip())
    rendered = rendered.strip()
    if rendered.startswith("<p>") and rendered.endswith("</p>") and rendered.count("<p>") == 1:
        return rendered[3:-4]
    return rendered


def md_block(text):
    """Full markdown to HTML for a multi-paragraph string."""
    return _MD.render(str(text or "").strip())


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name}: product story</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>
  // Disable auto-run synchronously so our loop controls rendering (see ch06).
  if (window.mermaid) mermaid.initialize({{ startOnLoad: false, theme: 'neutral', securityLevel: 'loose' }});
</script>
<script>
  window.addEventListener('load', async function () {{
    if (!window.mermaid) return;
    var blocks = document.querySelectorAll('pre.mermaid');
    for (var i = 0; i < blocks.length; i++) {{
      var el = blocks[i], src = el.textContent;
      try {{
        // Validate first, so a diagram the model got wrong is dropped silently
        // (no "Syntax error" box) instead of rendered.
        if ((await mermaid.parse(src, {{ suppressErrors: true }})) === false) {{ el.remove(); continue; }}
        var out = await mermaid.render('mmd' + i, src);
        el.innerHTML = out.svg;
      }} catch (e) {{ el.remove(); }}
    }}
  }});
</script>
<style>
  :root {{
    --bg: #f8fafc;
    --surface: #fff;
    --text: #0f172a;
    --muted: #64748b;
    --rule: #e2e8f0;
    --accent: #3b82f6;
    --accent-soft: #eff6ff;
    --good: #22c55e;
    --warn: #f59e0b;
    --warn-soft: #fffbeb;
    --warn-ink: #92400e;
    --danger: #ef4444;
    --shadow: 0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
    --shadow-lg: 0 8px 24px rgba(15,23,42,.08), 0 2px 6px rgba(15,23,42,.04);
    --radius: 10px;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
    background: var(--bg); color: var(--text); margin: 0;
    line-height: 1.6; -webkit-font-smoothing: antialiased;
  }}
  code, .mono {{ font-family: 'JetBrains Mono', ui-monospace, Consolas, monospace; }}
  main {{ max-width: 920px; margin: 0 auto; padding: 0 24px 48px; }}

  /* Hero */
  .hero {{
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #fff; padding: 56px 24px 48px; text-align: center;
    border-bottom: 1px solid var(--rule);
  }}
  .hero-inner {{ max-width: 920px; margin: 0 auto; }}
  .eyebrow {{
    display: inline-flex; align-items: center; gap: 8px;
    color: #93c5fd; font-size: .72rem; font-weight: 700;
    letter-spacing: .18em; text-transform: uppercase;
  }}
  .eyebrow::before {{ content: ''; width: 18px; height: 2px; background: var(--accent); }}
  .hero h1 {{
    font-size: 2.4rem; font-weight: 800; letter-spacing: -.025em;
    margin: 16px 0 14px; color: #fff;
  }}
  .hero h1 .name {{ color: #60a5fa; }}
  .hero .sub {{
    font-size: 1.05rem; color: #cbd5e1; max-width: 760px;
    margin: 0 auto; line-height: 1.65;
  }}

  /* Section labels */
  .sec {{ margin: 40px 0 0; }}
  .sec:first-of-type {{ margin-top: 32px; }}
  .sec-label {{
    display: flex; align-items: center; gap: 10px;
    font-size: .72rem; font-weight: 700; letter-spacing: .14em;
    text-transform: uppercase; color: var(--muted); margin-bottom: 14px;
  }}
  .sec-label::before {{
    content: ''; width: 3px; height: 16px;
    background: var(--accent); border-radius: 2px;
  }}
  .sec-intro {{ color: var(--muted); font-size: .92rem; margin: -4px 0 16px; }}

  /* Pain card */
  .pain-card {{
    background: var(--surface); border: 1px solid var(--rule);
    border-radius: var(--radius); padding: 18px 22px;
    box-shadow: var(--shadow); border-left: 3px solid var(--danger);
  }}
  .pain-card .pain-label {{
    font-size: .65rem; font-weight: 700; letter-spacing: .14em;
    color: var(--danger); text-transform: uppercase; margin-bottom: 8px;
  }}
  .pain-card .pain-body {{
    display: grid; grid-template-columns: 1fr; gap: 16px; align-items: center;
  }}
  .pain-card.has-image .pain-body {{ grid-template-columns: 1fr 280px; }}
  @media (max-width: 640px) {{
    .pain-card.has-image .pain-body {{ grid-template-columns: 1fr; }}
  }}
  .pain-card p {{
    font-size: 1.02rem; line-height: 1.65; color: #334155;
    margin: 0;
  }}
  .pain-card img.pain-illustration {{
    width: 100%; height: auto; border-radius: 8px;
    border: 1px solid var(--rule); background: #fff;
  }}

  /* Two column cards (sacrifices / gains) */
  .two-col {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 16px;
  }}
  @media (max-width: 720px) {{ .two-col {{ grid-template-columns: 1fr; }} }}
  .pos-card {{
    background: var(--surface); border: 1px solid var(--rule);
    border-radius: var(--radius); padding: 16px 18px;
    box-shadow: var(--shadow);
  }}
  .pos-card h3 {{
    margin: 0 0 12px; font-size: .95rem; font-weight: 700;
    display: flex; align-items: center; gap: 8px;
  }}
  .pos-card.sacrifices h3 {{ color: var(--warn-ink); }}
  .pos-card.sacrifices h3::before {{
    content: '–'; display: inline-flex; align-items: center; justify-content: center;
    width: 22px; height: 22px; background: var(--warn-soft);
    color: var(--warn); border-radius: 50%; font-weight: 800;
  }}
  .pos-card.gains h3 {{ color: #166534; }}
  .pos-card.gains h3::before {{
    content: '+'; display: inline-flex; align-items: center; justify-content: center;
    width: 22px; height: 22px; background: #f0fdf4;
    color: var(--good); border-radius: 50%; font-weight: 800;
  }}
  .pos-card ul {{ margin: 0; padding-left: 1.1em; }}
  .pos-card li {{ margin: .4em 0; color: #334155; font-size: .92rem; line-height: 1.55; }}

  /* Callout (why incumbents can't copy) */
  .callout {{
    background: var(--warn-soft); border-left: 3px solid var(--warn);
    border-radius: var(--radius); padding: 16px 20px; margin-top: 16px;
  }}
  .callout-label {{
    font-size: .65rem; font-weight: 700; letter-spacing: .14em;
    color: var(--warn-ink); text-transform: uppercase; margin-bottom: 6px;
  }}
  .callout p {{ margin: .4em 0 0; color: #422006; font-size: .95rem; line-height: 1.65; }}

  /* Counter-positioning diagram */
  .trap-diagram {{ margin-top: 16px; background: var(--surface); border: 1px solid var(--rule);
    border-radius: var(--radius); box-shadow: var(--shadow); padding: 16px; }}
  .trap-diagram .diagram-label {{ font-size: .65rem; font-weight: 700; letter-spacing: .14em;
    color: var(--muted); text-transform: uppercase; margin-bottom: 10px; }}
  pre.mermaid {{ background: transparent; text-align: center; margin: 0; padding: 4px; }}
  pre.mermaid svg {{ max-width: 100%; height: auto; }}

  /* Competitor matrix */
  .dim-defs {{
    background: var(--surface); border: 1px solid var(--rule);
    border-radius: var(--radius); padding: 14px 18px; margin-bottom: 12px;
    box-shadow: var(--shadow); list-style: none;
  }}
  .dim-defs li {{ margin: .35em 0; font-size: .9rem; color: #475569; }}
  .dim-defs li strong {{ color: var(--text); font-weight: 700; }}
  .matrix-wrap {{
    border: 1px solid var(--rule); border-radius: var(--radius);
    overflow: hidden; box-shadow: var(--shadow); background: var(--surface);
  }}
  table.matrix {{
    width: 100%; border-collapse: separate; border-spacing: 0;
    font-size: .88rem;
  }}
  table.matrix th, table.matrix td {{
    padding: 12px 14px; text-align: left; vertical-align: top;
    border-bottom: 1px solid var(--rule);
  }}
  table.matrix tr:last-child td {{ border-bottom: none; }}
  table.matrix th {{
    background: #f1f5f9; color: var(--muted);
    font-size: .68rem; font-weight: 700; letter-spacing: .08em;
    text-transform: uppercase;
  }}
  table.matrix td.row-head {{
    background: #fafbfc; font-weight: 700; color: var(--text);
    white-space: nowrap; font-size: .95rem;
  }}
  table.matrix td .verdict {{
    display: block; font-weight: 700; color: var(--text);
    font-size: .92rem; margin-bottom: 3px;
  }}
  table.matrix td .detail {{
    display: block; color: var(--muted); font-size: .82rem; line-height: 1.5;
  }}
  table.matrix tr.you td {{ background: var(--accent-soft); }}
  table.matrix tr.you td.row-head {{ color: var(--accent); }}
  table.matrix tr.you td .verdict {{ color: var(--accent); }}

  /* Horizontal scrollable card rails for surprises and absences. */
  .scroll-hint {{
    font-size: .68rem; color: var(--muted); margin-left: auto;
    text-transform: none; letter-spacing: 0; font-weight: 500;
  }}
  .card-rail {{
    display: flex; gap: 12px; overflow-x: auto;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    padding: 2px 2px 14px; margin: 0;
    list-style: none;
  }}
  .card-rail::-webkit-scrollbar {{ height: 7px; }}
  .card-rail::-webkit-scrollbar-track {{ background: transparent; }}
  .card-rail::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 4px; }}
  .card-rail::-webkit-scrollbar-thumb:hover {{ background: #94a3b8; }}
  .card-rail > li {{
    scroll-snap-align: start;
    min-width: 300px; max-width: 300px; flex-shrink: 0;
    background: var(--surface); border: 1px solid var(--rule);
    border-radius: var(--radius); padding: 14px 16px;
    box-shadow: var(--shadow);
    display: flex; flex-direction: column; gap: 8px;
  }}
  .card-rail.surprises > li {{ border-left: 3px solid var(--accent); }}
  .card-rail.absences > li {{ border-left: 3px solid var(--warn); }}
  .card-rail .head {{
    display: flex; align-items: flex-start; gap: 10px;
  }}
  .card-rail .num {{
    display: inline-flex; align-items: center; justify-content: center;
    width: 22px; height: 22px; border-radius: 50%;
    font-weight: 700; font-size: .72rem; flex-shrink: 0; margin-top: 1px;
    color: #fff;
  }}
  .card-rail.surprises .num {{ background: var(--accent); }}
  .card-rail.absences .num {{ background: var(--warn); }}
  .card-rail .headline {{
    font-weight: 700; font-size: .98rem; line-height: 1.35;
  }}
  .card-rail .where {{
    font-family: 'JetBrains Mono', monospace;
    font-size: .7rem; color: var(--muted); line-height: 1.5;
    word-break: break-word;
  }}
  .card-rail .body {{
    color: #475569; font-size: .88rem; line-height: 1.55;
    margin-top: auto;
  }}

  /* Inline code in body text */
  code {{
    font-family: 'JetBrains Mono', ui-monospace, Consolas, monospace;
    font-size: .85em; background: #f1f5f9; color: var(--text);
    padding: 1px 6px; border-radius: 4px;
  }}
  .surprise-list code, .absence-list code {{ font-size: .82em; }}

  footer {{
    color: var(--muted); font-size: .78rem; text-align: center;
    margin-top: 48px; padding-top: 20px; border-top: 1px solid var(--rule);
  }}
</style>
</head>
<body>
  <header class="hero">
    <div class="hero-inner">
      <span class="eyebrow">Product Story</span>
      <h1><span class="name">{name}</span></h1>
      <p class="sub">{variant}</p>
    </div>
  </header>

  <main>
    <section class="sec">
      <div class="sec-label">The Pain</div>
      <div class="pain-card{pain_card_mod}">
        <div class="pain-label">↳ Why this exists</div>
        <div class="pain-body">
          <p>{pain}</p>
{pain_image_html}
        </div>
      </div>
    </section>

    <section class="sec">
      <div class="sec-label">Where it sits</div>
      <p class="sec-intro">The trade it makes versus the dominant alternative.</p>
      <div class="two-col">
        <div class="pos-card sacrifices">
          <h3>What it gives up</h3>
          <ul>
{sacrifices_html}
          </ul>
        </div>
        <div class="pos-card gains">
          <h3>What it gets in return</h3>
          <ul>
{gains_html}
          </ul>
        </div>
      </div>
      <div class="callout">
        <div class="callout-label">Why incumbents can't copy this</div>
{why_html}
      </div>
{trap_diagram_html}
    </section>

    <section class="sec">
      <div class="sec-label">Side by Side</div>
      <p class="sec-intro">Four dimensions that actually split the field.</p>
      <ul class="dim-defs">
{dim_defs_html}
      </ul>
      <div class="matrix-wrap">
        <table class="matrix">
          <thead><tr><th>Product</th>{dim_headers}</tr></thead>
          <tbody>
{competitor_rows}
          </tbody>
        </table>
      </div>
    </section>

    <section class="sec">
      <div class="sec-label">What the Code Reveals<span class="scroll-hint">scroll →</span></div>
      <p class="sec-intro">Features hiding in the codebase that the README doesn't advertise. Each one is a bet about where the product is going.</p>
      <ul class="card-rail surprises">
{present_items}
      </ul>
    </section>

    <section class="sec">
      <div class="sec-label">Missing on Purpose<span class="scroll-hint">scroll →</span></div>
      <p class="sec-intro">Features every competitor ships that this codebase deliberately doesn't. Strategy is choosing what not to do.</p>
      <ul class="card-rail absences">
{absent_items}
      </ul>
    </section>

    <footer>Reverse engineered from the codebase.</footer>
  </main>
</body>
</html>
"""


def _esc(s):
    return _html.escape(str(s).strip())


def render_html(name, shared):
    positioning = shared["positioning"]
    surprises = shared["surprises"]
    pain_img = shared.get("pain_image_path")

    if pain_img and os.path.exists(pain_img):
        # The HTML lives in the same folder as the image (output/<name>-story/),
        # so a basename src works without any path math.
        pain_image_html = f'          <img class="pain-illustration" src="{os.path.basename(pain_img)}" alt="before and after illustration">'
        pain_card_mod = ' has-image'
    else:
        pain_image_html = ""
        pain_card_mod = ""

    dims = positioning["dimensions"]
    dim_defs = "\n".join(
        f'        <li><strong>{_esc(d["name"])}</strong>: {md(d["definition"])}</li>'
        for d in dims
    )
    dim_headers = "".join(f'<th>{_esc(d["name"])}</th>' for d in dims)

    competitor_rows = []
    for i, c in enumerate(positioning["competitors"]):
        cells = "".join(
            f'<td><span class="verdict">{md(cell["verdict"])}</span>'
            f'<span class="detail">{md(cell["detail"])}</span></td>'
            for cell in c.get("cells", [])
        )
        # First row is the product itself; highlight it.
        row_class = ' class="you"' if i == 0 else ''
        competitor_rows.append(
            f'            <tr{row_class}><td class="row-head">{_esc(c["name"])}</td>{cells}</tr>'
        )
    competitor_rows = "\n".join(competitor_rows)

    sacrifices_html = "\n".join(
        f'            <li>{md(s)}</li>' for s in positioning.get("sacrifices", [])
    )
    gains_html = "\n".join(
        f'            <li>{md(g)}</li>' for g in positioning.get("gains", [])
    )
    why_html = md_block(positioning.get("why_incumbents_cannot_copy", ""))

    diagram_src = str(positioning.get("diagram", "") or "").strip()
    trap_diagram_html = (
        '      <div class="trap-diagram">\n'
        '        <div class="diagram-label">The trap, in one picture</div>\n'
        f'        <pre class="mermaid">{diagram_src}</pre>\n'
        '      </div>'
    ) if diagram_src else ""

    present_items = "\n".join(
        f'        <li>'
        f'<div class="head"><span class="num">{i+1}</span>'
        f'<div class="headline">{md(p["headline"])}</div></div>'
        f'<div class="where">{md(p["where"])}</div>'
        f'<div class="body">{md(p["bet"])}</div>'
        f'</li>'
        for i, p in enumerate(surprises["present"])
    )
    absent_items = "\n".join(
        f'        <li>'
        f'<div class="head"><span class="num">{i+1}</span>'
        f'<div class="headline">{md(a["headline"])}</div></div>'
        f'<div class="where">{md(a["evidence"])}</div>'
        f'<div class="body">{md(a["tradeoff"])}</div>'
        f'</li>'
        for i, a in enumerate(surprises["absent"])
    )

    return HTML_TEMPLATE.format(
        name=_esc(name),
        variant=md(shared["variant"]),
        pain=md(shared["pain"]),
        pain_image_html=pain_image_html,
        pain_card_mod=pain_card_mod,
        dim_defs_html=dim_defs,
        dim_headers=dim_headers,
        competitor_rows=competitor_rows,
        sacrifices_html=sacrifices_html,
        gains_html=gains_html,
        why_html=why_html,
        trap_diagram_html=trap_diagram_html,
        present_items=present_items,
        absent_items=absent_items,
    )


def render_markdown(name, shared):
    positioning = shared["positioning"]
    surprises = shared["surprises"]

    parts = [f"# {name}\n"]
    parts.append("_A product story reverse engineered from the codebase._\n")

    parts.append("## The pitch\n")
    parts.append(f"> {shared['variant']}\n")

    parts.append("## The pain\n")
    parts.append(f"> {shared['pain']}\n")

    parts.append("## Where it sits\n")
    parts.append("### What it gives up\n")
    for s in positioning.get("sacrifices", []):
        parts.append(f"- {s}")
    parts.append("")
    parts.append("### What it gets in return\n")
    for g in positioning.get("gains", []):
        parts.append(f"- {g}")
    parts.append("")
    parts.append("### Why incumbents can't copy this\n")
    parts.append(positioning.get("why_incumbents_cannot_copy", "").strip() + "\n")
    if positioning.get("diagram"):
        parts.append("```mermaid\n" + str(positioning["diagram"]).strip() + "\n```\n")

    parts.append("### Side by side\n")
    parts.append("**Dimensions**\n")
    for d in positioning["dimensions"]:
        parts.append(f"- **{d['name']}**: {d['definition']}")
    parts.append("")
    headers = ["Product"] + [d["name"] for d in positioning["dimensions"]]
    parts.append("| " + " | ".join(headers) + " |")
    parts.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for c in positioning["competitors"]:
        cells = [f"**{c['name']}**"]
        for cell in c.get("cells", []):
            verdict = str(cell.get("verdict", "")).replace("\n", " ")
            detail = str(cell.get("detail", "")).replace("\n", " ")
            cells.append(f"**{verdict}**. {detail}")
        parts.append("| " + " | ".join(cells) + " |")
    parts.append("")

    parts.append("## Hiding in the code\n")
    for p in surprises["present"]:
        parts.append(f"### {p['headline']}")
        parts.append(f"_{p['where']}_")
        parts.append("")
        parts.append(p["bet"])
        parts.append("")

    parts.append("## Missing on purpose\n")
    for a in surprises["absent"]:
        parts.append(f"### {a['headline']}")
        parts.append(f"_{a['evidence']}_")
        parts.append("")
        parts.append(a["tradeoff"])
        parts.append("")

    return "\n".join(parts)
