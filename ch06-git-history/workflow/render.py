"""Render the git-history read as markdown and a clean, self-contained HTML page.

One HTML section per prompt in the chapter, so the page mirrors the analyses:
  1. The eras       (name-eras)      — a horizontal timeline you swipe through
  2. Cast & mood    (profile-era)    — one card per era: who drove it, what the work was
  3. The graveyard  (graveyard-entry)— tombstones for the killed features

The layout is deliberately left-to-right per section, so you read the big
picture first. Each card is a fixed frame that scrolls up/down inside, so no
card becomes a wall of text. Descriptions render full markdown, including the
friendly ```mermaid diagrams and code blocks the prompts produce.
"""
import html as _html
import os
import re
import sys

from markdown_it import MarkdownIt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

_MD = MarkdownIt("commonmark", {"html": False, "linkify": True, "breaks": False}).enable(["table"])


def md(text):
    """Inline markdown for a short string; strips the wrapping <p>."""
    if text is None:
        return ""
    out = _MD.render(str(text).strip()).strip()
    if out.startswith("<p>") and out.endswith("</p>") and out.count("<p>") == 1:
        return out[3:-4]
    return out


def _mermaidize(rendered_html):
    """markdown-it emits ```mermaid as <pre><code class="language-mermaid">…; the
    Mermaid script wants <pre class="mermaid">…. Rewrite (and un-escape) it."""
    return re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        lambda m: f'<pre class="mermaid">{_html.unescape(m.group(1))}</pre>',
        rendered_html, flags=re.DOTALL,
    )


def md_rich(text):
    """Full markdown to HTML, with ```mermaid fences rewired for the Mermaid JS."""
    return _mermaidize(_MD.render(str(text or "").strip()))


def _mermaid_block(source):
    """Wrap raw Mermaid source (from the era `diagram` field) for the Mermaid JS."""
    src = str(source or "").strip()
    return f'<pre class="mermaid">{src}</pre>' if src else ""


def _esc(s):
    return _html.escape(str(s).strip())


def _pct(v):
    try:
        return max(0, min(100, float(v)))
    except (TypeError, ValueError):
        return 0


def _profiles_by_era(shared):
    """Line up each era with its profile (by order, falling back to name)."""
    eras = shared.get("eras", [])
    profiles = shared.get("profiles", [])
    by_name = {p["era"]["name"]: p for p in profiles}
    paired = []
    for i, era in enumerate(eras):
        p = profiles[i] if i < len(profiles) and profiles[i]["era"]["name"] == era["name"] \
            else by_name.get(era["name"])
        paired.append((era, p))
    return paired


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name}: git history</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github-dark.min.css">
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>
  // Disable auto-run SYNCHRONOUSLY, before DOMContentLoaded — otherwise Mermaid
  // renders every diagram itself, and our loop below would re-process the
  // already-rendered SVG and wipe it.
  if (window.mermaid) mermaid.initialize({{ startOnLoad: false, theme: 'neutral', securityLevel: 'loose' }});
</script>
<script>
  window.addEventListener('load', async function () {{
    // Syntax-highlight code blocks. (Mermaid pres have no <code>, so they're skipped.)
    if (window.hljs) {{ try {{ hljs.highlightAll(); }} catch (e) {{}} }}
    // Render each diagram, but validate first with parse() so a diagram the model
    // got wrong is silently DROPPED — no "Syntax error" box, no orphan graphics.
    // A data-driven page can't guarantee valid Mermaid; a missing diagram beats
    // an error box.
    if (!window.mermaid) return;
    var blocks = document.querySelectorAll('pre.mermaid');
    for (var i = 0; i < blocks.length; i++) {{
      var el = blocks[i], src = el.textContent;
      try {{
        if ((await mermaid.parse(src, {{ suppressErrors: true }})) === false) {{ el.remove(); continue; }}
        var out = await mermaid.render('mmd' + i, src);
        el.innerHTML = out.svg;
      }} catch (e) {{
        el.remove();
      }}
    }}
  }});
</script>
<style>
  :root {{
    --bg: #f7f8fa; --surface: #fff; --text: #101828; --muted: #667085;
    --faint: #98a2b3; --rule: #e4e7ec; --line: #eef0f3;
    --accent: #3b82f6; --accent-soft: #eff6ff;
    --good: #16a34a; --stone: #9aa4b2; --stone-bg: #f2f4f7;
    --shadow: 0 1px 2px rgba(16,24,40,.05); --shadow-lg: 0 8px 26px rgba(16,24,40,.10);
    --radius: 12px;
  }}
  * {{ box-sizing: border-box; }}
  html {{ -webkit-text-size-adjust: 100%; }}
  body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
    font-size: 13.5px; line-height: 1.5; background: var(--bg); color: var(--text);
    margin: 0; -webkit-font-smoothing: antialiased; }}
  code, .mono {{ font-family: 'JetBrains Mono', ui-monospace, Consolas, monospace; }}
  main {{ max-width: 1240px; margin: 0 auto; padding: 0 24px 56px; }}

  /* Hero */
  .hero {{ background: radial-gradient(120% 140% at 50% 0%, #1d2939 0%, #0c111d 70%);
    color: #fff; padding: 46px 20px 42px; text-align: center; }}
  .hero-inner {{ max-width: 1120px; margin: 0 auto; }}
  .hero-diagram {{ margin: 26px 0 4px; }}
  .hero-diagram-cap {{ font-size: .7rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase;
    color: var(--accent); margin: 0 2px 9px; }}
  .timeline {{ display: flex; gap: 4px; align-items: stretch; }}
  .tl-era {{ min-width: 0; padding: 15px 13px; border-radius: 8px; color: #fff; overflow: hidden; }}
  .tl-name {{ font-weight: 800; font-size: .92rem; letter-spacing: -.01em; line-height: 1.2;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  .tl-meta {{ font-size: .66rem; opacity: .9; margin-top: 4px; font-family: 'JetBrains Mono', monospace;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  @media (max-width: 640px) {{ .timeline {{ flex-direction: column; }} }}
  .eyebrow {{ display: inline-flex; align-items: center; gap: 7px; color: #93c5fd;
    font-size: .68rem; font-weight: 700; letter-spacing: .18em; text-transform: uppercase; }}
  .eyebrow::before {{ content: ''; width: 16px; height: 2px; background: var(--accent); border-radius: 2px; }}
  .hero h1 {{ font-size: 1.9rem; font-weight: 800; letter-spacing: -.025em; margin: 12px 0 10px; }}
  .hero .sub {{ font-size: .94rem; color: #cbd5e1; margin: 0 auto; line-height: 1.55; }}

  /* Section header with a scroll hint */
  .sec-head {{ display: flex; align-items: baseline; gap: 10px; margin: 42px 2px 14px; }}
  .sec-n {{ font-family: 'JetBrains Mono', monospace; font-size: .68rem; font-weight: 700;
    color: var(--accent); }}
  .sec-label {{ display: flex; align-items: center; gap: 9px; font-size: .68rem; font-weight: 700;
    letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }}
  .sec-label::before {{ content: ''; width: 3px; height: 14px; background: var(--accent); border-radius: 2px; }}
  .sec-note {{ font-size: .8rem; color: var(--faint); }}
  .scroll-hint {{ margin-left: auto; font-size: .68rem; font-weight: 600; color: var(--faint); letter-spacing: .04em; }}

  /* Friendly "start here" welcome + per-section intros */
  .intro {{ background: var(--surface); border: 1px solid var(--rule); border-left: 4px solid var(--accent);
    border-radius: var(--radius); box-shadow: var(--shadow); padding: 20px 24px; margin: 30px 0 4px; }}
  .intro-label {{ font-size: .68rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase;
    color: var(--accent); margin-bottom: 10px; }}
  .intro p {{ margin: .5em 0; font-size: .96rem; color: #344054; line-height: 1.7; }}
  .intro p:first-child {{ margin-top: 0; }}
  .intro strong {{ color: var(--text); }}
  .sec-intro {{ font-size: .9rem; color: #475467; line-height: 1.6; margin: -6px 2px 12px; }}
  .sec-intro p {{ margin: 0; }}

  /* Horizontal rails */
  .rail {{ display: flex; gap: 16px; align-items: stretch; overflow-x: auto;
    scroll-snap-type: x proximity; -webkit-overflow-scrolling: touch;
    padding: 4px 2px 18px; margin: 0; list-style: none; }}
  .rail::-webkit-scrollbar {{ height: 9px; }}
  .rail::-webkit-scrollbar-track {{ background: var(--line); border-radius: 5px; }}
  .rail::-webkit-scrollbar-thumb {{ background: #cbd2dc; border-radius: 5px; }}
  .rail::-webkit-scrollbar-thumb:hover {{ background: var(--stone); }}

  /* Cards scroll up/down inside a fixed frame */
  .scroll {{ flex: 1; overflow-y: auto; overscroll-behavior: contain; }}
  .scroll::-webkit-scrollbar {{ width: 9px; }}
  .scroll::-webkit-scrollbar-track {{ background: transparent; }}
  .scroll::-webkit-scrollbar-thumb {{ background: #dce0e7; border-radius: 5px; }}
  .scroll::-webkit-scrollbar-thumb:hover {{ background: var(--stone); }}

  /* Shared card frame */
  .card {{ scroll-snap-align: start; background: var(--surface); border: 1px solid var(--rule);
    border-radius: var(--radius); box-shadow: var(--shadow);
    display: flex; flex-direction: column; overflow: hidden; }}
  .card-top {{ flex-shrink: 0; padding: 15px 20px 13px; border-bottom: 1px solid var(--line);
    background: linear-gradient(180deg, #fbfcfe, #fff); }}
  .card-num {{ font-family: 'JetBrains Mono', monospace; font-size: .64rem; font-weight: 700;
    letter-spacing: .12em; color: var(--accent); }}
  .card-name {{ font-size: 1.12rem; font-weight: 800; letter-spacing: -.01em; margin: 3px 0 7px; }}
  .card-meta {{ display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }}
  .chip {{ font-family: 'JetBrains Mono', monospace; font-size: .66rem; color: var(--muted);
    background: var(--stone-bg); padding: 2px 7px; border-radius: 5px; }}

  /* Section 1 — eras (natural height; only scrolls if a description is huge) */
  .era {{ flex: 0 0 500px; width: 500px; }}
  .era .scroll {{ max-height: 72vh; }}
  .era-body {{ padding: 15px 20px 18px; }}
  .era-desc {{ color: #344054; font-size: .85rem; line-height: 1.6; }}
  .era-desc p {{ margin: 0 0 .55em; }}
  .turning {{ font-size: .8rem; color: var(--muted); background: var(--accent-soft);
    border-radius: 8px; padding: 10px 12px; margin: 10px 0 0; }}
  .turning b {{ color: #1e3a8a; }}
  .turning .hash {{ font-family: 'JetBrains Mono', monospace; font-size: .72rem;
    background: #dbeafe; padding: 1px 5px; border-radius: 4px; color: #1e40af; }}

  /* Section 2 — cast & mood (fixed frame, inner scroll) */
  .profile {{ flex: 0 0 440px; width: 440px; height: 66vh; min-height: 460px; max-height: 720px;
    border-top: 3px solid var(--accent); }}
  .cm {{ padding: 6px 20px 16px; }}
  .cm:first-child {{ padding-top: 14px; }}
  .cm h4 {{ font-size: .62rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase;
    color: var(--faint); margin: 14px 0 9px; }}
  .cm:first-child h4 {{ margin-top: 0; }}
  .cm h4 span {{ font-weight: 500; letter-spacing: 0; text-transform: none; font-size: .68rem; }}
  .bar {{ margin: 8px 0; }}
  .bar-top {{ display: flex; justify-content: space-between; gap: 8px; align-items: baseline; }}
  .bar-top .lab {{ font-size: .82rem; font-weight: 600; color: var(--text); }}
  .bar-top .val {{ font-family: 'JetBrains Mono', monospace; font-size: .68rem; color: var(--faint); }}
  .bar-track {{ height: 5px; background: var(--stone-bg); border-radius: 3px; margin: 4px 0 3px; overflow: hidden; }}
  .bar-fill {{ height: 100%; border-radius: 3px; }}
  .cast .bar-fill {{ background: linear-gradient(90deg, #60a5fa, #3b82f6); }}
  .mood .bar-fill {{ background: linear-gradient(90deg, #4ade80, #16a34a); }}
  .bar-note {{ font-size: .76rem; color: var(--muted); line-height: 1.5; }}
  .cm-narr {{ font-size: .78rem; color: var(--faint); font-style: italic; line-height: 1.55;
    margin-top: 10px; padding-top: 9px; border-top: 1px dashed var(--line); }}

  /* Section 3 — graveyard (fixed frame, inner scroll) */
  .grave {{ flex: 0 0 400px; width: 400px; height: 66vh; min-height: 460px; max-height: 720px;
    border-top: 3px solid var(--stone); border-radius: 5px 5px var(--radius) var(--radius); }}
  .grave-meta {{ flex-shrink: 0; font-family: 'JetBrains Mono', monospace; font-size: .66rem;
    color: var(--faint); padding: 14px 18px 11px; border-bottom: 1px solid var(--line); }}
  .grave-body {{ padding: 13px 18px 16px; font-size: .82rem; }}
  .grave-body p {{ margin: .55em 0; color: #344054; line-height: 1.6; }}
  .grave-body p:first-child {{ margin-top: 0; }}
  .grave-body strong {{ color: var(--text); }}
  .grave-body em {{ color: var(--muted); font-style: italic; }}

  /* Code + Mermaid inside cards */
  pre {{ background: #0f172a; color: #e2e8f0; border-radius: 8px; padding: 11px 13px;
    overflow-x: auto; margin: 11px 0; }}
  pre code {{ padding: 0; font-size: .74rem; line-height: 1.55; }}
  /* let highlight.js color the tokens, but keep our own dark pre background */
  pre code.hljs {{ background: transparent; padding: 0; color: #e2e8f0; }}
  pre.mermaid {{ background: var(--stone-bg); color: inherit; text-align: center; padding: 12px; }}
  pre.mermaid svg {{ max-width: 100%; height: auto; }}
  code {{ font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: .84em;
    background: var(--stone-bg); color: var(--text); padding: 1px 5px; border-radius: 4px; }}

  footer {{ color: var(--faint); font-size: .74rem; text-align: center; margin-top: 44px;
    padding-top: 18px; border-top: 1px solid var(--rule); }}
  @media (max-width: 560px) {{
    .era, .profile, .grave {{ flex-basis: 86vw; width: 86vw; }}
  }}
</style>
</head>
<body>
  <header class="hero">
    <div class="hero-inner">
      <span class="eyebrow">Git History</span>
      <h1>{name}</h1>
      <p class="sub">{subtitle}</p>
    </div>
  </header>
  <main>
{welcome}
    <div class="sec-head">
      <span class="sec-n">01</span>
      <div class="sec-label">The eras</div>
      <div class="scroll-hint">swipe &rarr;</div>
    </div>
{eras_intro}
    <ul class="rail eras">
{eras_html}
    </ul>

    <div class="sec-head">
      <span class="sec-n">02</span>
      <div class="sec-label">Cast &amp; mood</div>
      <div class="scroll-hint">swipe &rarr;</div>
    </div>
{profiles_intro}
    <ul class="rail profiles">
{profiles_html}
    </ul>

    <div class="sec-head">
      <span class="sec-n">03</span>
      <div class="sec-label">The graveyard</div>
      <div class="scroll-hint">swipe &rarr;</div>
    </div>
{graves_intro}
    <ul class="rail graves">
{graves_html}
    </ul>

    <footer>Reverse engineered from {n_commits} commits of git history.</footer>
  </main>
</body>
</html>
"""


def _bars(items):
    rows = []
    for it in items:
        label = it.get("name") or it.get("label") or ""
        pct = _pct(it.get("pct"))
        note = it.get("note", "")
        rows.append(
            '          <div class="bar">'
            f'<div class="bar-top"><span class="lab">{_esc(label)}</span>'
            f'<span class="val">{pct:g}%</span></div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{pct:g}%"></div></div>'
            + (f'<div class="bar-note">{md(note)}</div>' if note else '')
            + '</div>'
        )
    return "\n".join(rows)


def _era_card(i, era, prof):
    commits = f'<span class="chip">{prof["commit_count"]:,} commits</span>' if prof else ""
    dates = f'{_esc(era["start"])} &rarr; {_esc(era.get("end") or "present")}'
    tp, tp_hash = era.get("turning_point", ""), era.get("turning_point_hash", "")
    turning = (
        f'<div class="turning"><b>Turning point:</b> {md(tp)}'
        + (f' <span class="hash">{_esc(tp_hash)}</span>' if tp_hash else '')
        + '</div>'
    ) if tp else ""
    return (
        f'      <li class="card era">\n'
        f'        <div class="card-top">\n'
        f'          <div class="card-num">ERA {i+1}</div>\n'
        f'          <div class="card-name">{_esc(era["name"])}</div>\n'
        f'          <div class="card-meta"><span class="chip">{dates}</span>{commits}</div>\n'
        f'        </div>\n'
        f'        <div class="scroll">\n'
        f'          <div class="era-body">\n'
        f'            <div class="era-desc">{md_rich(era.get("description", ""))}</div>\n'
        f'            {_mermaid_block(era.get("diagram"))}\n'
        f'            {turning}\n'
        f'          </div>\n'
        f'        </div>\n'
        f'      </li>'
    )


def _profile_card(i, era, prof):
    if not prof:
        return ""
    cast = prof["profile"].get("cast", {})
    mood = prof["profile"].get("mood", {})
    cast_narr = (f'<div class="cm-narr">{md(cast.get("narrative", ""))}</div>'
                 if cast.get("narrative") else "")
    mood_narr = (f'<div class="cm-narr">{md(mood.get("narrative", ""))}</div>'
                 if mood.get("narrative") else "")
    dates = f'{_esc(era["start"])} &rarr; {_esc(era.get("end") or "present")}'
    return (
        f'      <li class="card profile">\n'
        f'        <div class="card-top">\n'
        f'          <div class="card-num">ERA {i+1}</div>\n'
        f'          <div class="card-name">{_esc(era["name"])}</div>\n'
        f'          <div class="card-meta"><span class="chip">{dates}</span>'
        f'<span class="chip">{prof["commit_count"]:,} commits</span></div>\n'
        f'        </div>\n'
        f'        <div class="scroll">\n'
        f'          <div class="cm cast">\n'
        f'            <h4>Cast <span>&middot; who drove it</span></h4>\n'
        f'{_bars(cast.get("contributors", []))}\n{cast_narr}\n'
        f'          </div>\n'
        f'          <div class="cm mood">\n'
        f'            <h4>Mood <span>&middot; what the work was</span></h4>\n'
        f'{_bars(mood.get("patterns", []))}\n{mood_narr}\n'
        f'          </div>\n'
        f'        </div>\n'
        f'      </li>'
    )


def _grave_card(g):
    c = g["commit"]
    era = g.get("era", {})
    meta = f"&#9738; {c['date']} &middot; {c['hash'][:7]} &middot; {c['count']} files &middot; {_esc(c['scope'])}/"
    if era.get("name"):
        meta += f" &middot; {_esc(era['name'])}"
    return (
        f'      <li class="card grave">\n'
        f'        <div class="grave-meta">{meta}</div>\n'
        f'        <div class="scroll"><div class="grave-body">{md_rich(g["entry_md"])}</div></div>\n'
        f'      </li>'
    )


_ERA_COLORS = ["#3b82f6", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981", "#06b6d4", "#ef4444"]


def _era_timeline(paired):
    """The 'big picture' for a git history: eras as a bar, sized by commit volume."""
    segs = []
    for i, (era, prof) in enumerate(paired):
        commits = prof["commit_count"] if prof else 1
        color = _ERA_COLORS[i % len(_ERA_COLORS)]
        segs.append(
            f'<div class="tl-era" style="flex:{max(commits, 1)};background:{color}">'
            f'<div class="tl-name">{_esc(era["name"])}</div>'
            f'<div class="tl-meta">{_esc(era["start"])} &rarr; {_esc(era.get("end") or "now")} '
            f'&middot; {commits:,} commits</div></div>')
    if not segs:
        return ""
    return (
        '    <section class="hero-diagram">\n'
        f'      <div class="hero-diagram-cap">The product\'s life &mdash; {len(paired)} eras, sized by commit volume</div>\n'
        f'      <div class="timeline">{"".join(segs)}</div>\n'
        '    </section>')


def _intro_html(shared, title):
    text = (shared.get("overview") or {}).get("intros", {}).get(title, "")
    return f'    <div class="sec-intro">{md_rich(text)}</div>' if text else ""


def render_html(name, shared):
    commits = shared.get("commits_asc") or shared.get("commits") or []
    n_commits = len(commits)
    span = f"{commits[0]['month']} to {commits[-1]['month']}" if commits else ""
    paired = _profiles_by_era(shared)
    # The big-picture summary IS the hero subtitle (no duplicate card).
    welcome = (shared.get("overview") or {}).get("welcome", "")
    subtitle = md(welcome) or (
        f"{n_commits:,} commits, {span} &mdash; read as {len(paired)} eras and a graveyard "
        f"of the bets the team walked away from.")

    era_blocks = [_era_card(i, era, prof) for i, (era, prof) in enumerate(paired)]
    profile_blocks = [b for i, (era, prof) in enumerate(paired) if (b := _profile_card(i, era, prof))]
    grave_blocks = [_grave_card(g) for g in shared.get("graves", [])]

    return HTML_TEMPLATE.format(
        name=_esc(name),
        subtitle=subtitle,
        welcome=_era_timeline(paired),
        eras_intro=_intro_html(shared, "The eras"),
        profiles_intro=_intro_html(shared, "Cast & mood"),
        graves_intro=_intro_html(shared, "The graveyard"),
        eras_html="\n".join(era_blocks),
        profiles_html="\n".join(profile_blocks)
        or '      <li class="card profile"><div class="cm">No profiles.</div></li>',
        graves_html="\n".join(grave_blocks)
        or '      <li class="card grave"><div class="grave-body">No bulk deletions found.</div></li>',
        n_commits=f"{n_commits:,}",
    )


def render_markdown(name, shared):
    commits = shared.get("commits_asc") or shared.get("commits") or []
    paired = _profiles_by_era(shared)
    parts = [f"# {name}: git history\n",
             f"_{len(commits):,} commits, read as eras and a graveyard._\n"]

    if (shared.get("overview") or {}).get("welcome"):
        parts.append(shared["overview"]["welcome"].strip() + "\n")

    parts.append("## The eras\n")
    for i, (era, _) in enumerate(paired):
        parts.append(f"### Era {i+1}: {era['name']} ({era['start']} → {era.get('end') or 'present'})\n")
        parts.append(era.get("description", "").strip() + "\n")
        if era.get("diagram"):
            parts.append("```mermaid\n" + str(era["diagram"]).strip() + "\n```\n")
        if era.get("turning_point"):
            h = era.get("turning_point_hash", "")
            parts.append(f"**Turning point:** {era['turning_point'].strip()}" + (f" (`{h}`)" if h else "") + "\n")

    parts.append("## Cast & mood\n")
    for i, (era, prof) in enumerate(paired):
        if not prof:
            continue
        cast = prof["profile"].get("cast", {})
        mood = prof["profile"].get("mood", {})
        parts.append(f"### Era {i+1}: {era['name']}\n")
        parts.append("**Cast:**")
        for c in cast.get("contributors", []):
            note = f" — {c['note']}" if c.get("note") else ""
            parts.append(f"- {c.get('name','')} ({c.get('pct','?')}%){note}")
        if cast.get("narrative"):
            parts.append(f"\n_{cast['narrative'].strip()}_")
        parts.append("\n**Mood:**")
        for p in mood.get("patterns", []):
            note = f" — {p['note']}" if p.get("note") else ""
            parts.append(f"- {p.get('label','')} ({p.get('pct','?')}%){note}")
        if mood.get("narrative"):
            parts.append(f"\n_{mood['narrative'].strip()}_")
        parts.append("")

    parts.append("## The graveyard\n")
    for g in shared.get("graves", []):
        c = g["commit"]
        parts.append(f"### ⚰ {c['subject']}")
        parts.append(f"_{c['date']} · `{c['hash'][:7]}` · {c['count']} files · `{c['scope']}/`_\n")
        parts.append(g["entry_md"].strip() + "\n")

    return "\n".join(parts)
