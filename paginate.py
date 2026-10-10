"""Split the rendered single-page site into separate pages with a left sidebar, and add mission org-chart pages.

Called from build.py after render(). Input: the files dict (index.html, agents.md, llms.txt, ...).
Output: the same dict plus <page>.html files and missions/<id>.html. Standard library only.
"""
import html, json, re
from pathlib import Path
import mission_svg as MS

E = lambda s: html.escape(str(s), quote=True)
HERE = Path(__file__).resolve().parent

# slug, label, sections on the page, page title, one-line purpose (shown in the sidebar tooltip and page <meta>)
PAGES = [
    ("", "Home", ["hero", "start"], "Home", "Start here: what this is, and Instructions for agents"),
    ("deck", "The deck", ["deck"], "AI in Action — Vivek's Deck", "The keynote slides: view online or download PDF / PowerPoint"),
    ("agenda", "Agenda", ["agenda"], "Agenda", "Two days in Philadelphia, session by session"),
    ("hackathon", "Hackathon", ["hackathon"], "Hackathon", "Hack the workflow: two-day plan, four verticals, final presentation template"),
    ("ideas", "Ideas", ["ideas"], "Big ideas", "The ideas behind the keynote"),
    ("inside", "Inside", ["inside"], "What's inside", "What the skills library contains"),
    ("missions", "Missions", ["mission-maps", "missions"], "Missions", "Every mission as an org chart of skills, plus copy-ready prompts"),
    ("prompts", "Prompts", ["prompts"], "Prompts", "Copy-ready prompts"),
    ("optimizer", "Optimizer", ["optimizer"], "Prompt optimizer", "Turn a short ask into a full agent prompt"),
    ("data", "Data", ["data"], "Data", "Synthetic datasets and public data sources"),
    ("grokbot", "Grok Bot", ["grokbot"], "Grok Bot setup", "Set up Grok Bot or another agent"),
    ("agents", "For agents", ["agents"], "Instructions for agents", "The playbook your AI agent follows"),
    ("skills", "Skills", ["skills"], "Skills", "All skills in the library"),
]
ICONS = {  # 24px line icons
    "": '<path d="M4 11l8-6 8 6v8a1 1 0 0 1-1 1h-4v-6h-6v6H5a1 1 0 0 1-1-1z"/>',
    "deck": '<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M12 16v4M8 20h8M7 12l3-3 2 2 4-4"/>',
    "hackathon": '<path d="M13 3L5 13h6l-1 8 8-10h-6z"/>',
    "agenda": '<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/>',
    "ideas": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
    "inside": '<path d="M4 7l8-4 8 4-8 4z"/><path d="M4 12l8 4 8-4M4 17l8 4 8-4"/>',
    "missions": '<circle cx="12" cy="5" r="2.2"/><circle cx="5" cy="18" r="2.2"/><circle cx="12" cy="18" r="2.2"/><circle cx="19" cy="18" r="2.2"/><path d="M12 7.2v8.6M12 10c-6 0-7 3-7 5.8M12 10c6 0 7 3 7 5.8"/>',
    "prompts": '<path d="M5 5h14v10H9l-4 4z"/><path d="M9 9h6M9 12h4"/>',
    "optimizer": '<path d="M12 3l1.8 4.2L18 9l-4.2 1.8L12 15l-1.8-4.2L6 9l4.2-1.8z"/><path d="M18 15l.9 2.1L21 18l-2.1.9L18 21l-.9-2.1L15 18l2.1-.9z"/>',
    "data": '<ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v6c0 1.7 3.1 3 7 3s7-1.3 7-3V6M5 12v6c0 1.7 3.1 3 7 3s7-1.3 7-3v-6"/>',
    "grokbot": '<rect x="5" y="8" width="14" height="11" rx="3"/><path d="M12 4v4M9 13h.01M15 13h.01M3 13v2M21 13v2"/>',
    "agents": '<path d="M4 6h16M4 12h10M4 18h7"/><path d="M16 15l2 2 4-4"/>',
    "skills": '<path d="M7 4h10v16l-5-3-5 3z"/>',
}


def url(slug):
    return "/" + slug


def split_sections(index_html):
    head = re.search(r"<head>(.*?)</head>", index_html, re.S).group(1)
    body = re.search(r"<body>(.*)</body>", index_html, re.S).group(1)
    pre = body[: body.index('<header class="nav"')]
    pre = re.sub(r'<a class="skip" href="#main">Skip to content</a>', "", pre)
    main = re.search(r'<main id="main">(.*)</main>', body, re.S).group(1)
    foot = re.search(r'(<footer class="foot">.*?</footer>)', body, re.S).group(1)
    tail = body[body.index("</footer>") + len("</footer>"):]
    chunks, ids = {}, []
    parts = re.split(r'(?=^<section )', main, flags=re.M)
    for p in parts:
        if not p.strip():
            continue
        m = re.match(r'<section (?:id="([a-z0-9-]+)"|class="hero")', p)
        sid = (m.group(1) if m and m.group(1) else "hero") if m else None
        if sid is None:
            continue
        chunks[sid] = p.rstrip() + "\n"
        ids.append(sid)
    return head, pre, chunks, ids, foot, tail


def sidebar(cur, ev):
    items = []
    for i, (slug, label, _, _, blurb) in enumerate(PAGES):
        on = slug == cur
        cls = ' class="is-active"' if on else ""
        cur_attr = ' aria-current="page"' if on else ""
        extra = ' data-agents="1"' if slug == "agents" else ""
        items.append(f'<li><a href="{url(slug)}"{cls}{cur_attr}{extra} title="{E(blurb)}"><svg class="sn-ic" viewBox="0 0 24 24" aria-hidden="true">{ICONS[slug]}</svg><span>{E(label)}</span></a></li>')
    return f'''<aside class="sb-side" id="sb-side" aria-label="Site navigation">
  <a class="brand sb-brand" href="/" aria-label="AI in Action for Medical Affairs, home"><span class="brand-mark" aria-hidden="true"><svg viewBox="0 0 32 32"><path d="M8 21l5-10 4 7 2-3 4 6"/></svg></span><span class="brand-t">AI in Action<span class="brand-sub">for Medical Affairs</span></span></a>
  <nav class="sb-nav" aria-label="Pages"><ul>{"".join(items)}</ul></nav>
  <div class="sb-foot"><p class="sb-when">{E(ev.get("dates", ""))}<br>{E(ev.get("venue", ""))}</p><a class="sb-agent" href="/agents.md">Agents: read /agents.md</a></div>
</aside>
<div class="sb-scrim" id="sb-scrim" hidden></div>'''


def mbar():
    return '''<header class="mbar">
  <button class="mbar-btn" id="sb-open" type="button" aria-controls="sb-side" aria-expanded="false" aria-label="Open menu"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  <a class="brand" href="/" aria-label="AI in Action for Medical Affairs, home"><span class="brand-mark" aria-hidden="true"><svg viewBox="0 0 32 32"><path d="M8 21l5-10 4 7 2-3 4 6"/></svg></span><span class="brand-t">AI in Action<span class="brand-sub">for Medical Affairs</span></span></a>
</header>'''


def absolutize(h):
    h = re.sub(r'\b(href|src|data-manifest)="(?!https?:|/|#|mailto:|data:|javascript:)([^"]+)"', r'\1="/\2"', h)
    return h


def relink(h, here_ids, id_page):
    def sub(m):
        x = m.group(1)
        if x in here_ids or x not in id_page:
            return m.group(0)
        pg = id_page[x]
        return f'href="{url(pg)}"' if x in SECTION_IDS.get(pg, ()) else f'href="{url(pg)}#{x}"'
    return re.sub(r'href="#([A-Za-z0-9_-]+)"', sub, h)


SECTION_IDS = {}


def page_head(head, title, desc, canon, extra_css):
    h = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", head, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(desc)}">', h)
    h = absolutize(h)
    h += f'<link rel="canonical" href="{E(canon)}">\n<link rel="stylesheet" href="/assets/sidebar.css">\n' + "".join(f'<link rel="stylesheet" href="/assets/{c}">\n' for c in extra_css)
    return h


def assemble(head, pre, slug, ev, main_html, foot, tail, body_cls="", extra_js=()):
    js = "".join(f'<script src="/assets/{j}" defer></script>\n' for j in ("sidebar.js",) + tuple(extra_js))
    tail = absolutize(tail).replace("</body>", "").replace("</html>", "")
    return (f'<!doctype html>\n<html lang="en">\n<head>{head}</head>\n<body class="sb {body_cls}" data-page="{slug or "home"}">\n{pre}'
            f'<a class="skip" href="#main">Skip to content</a>\n{sidebar(slug, ev)}\n<div class="sb-main">\n{mbar()}\n<main id="main">\n{main_html}</main>\n'
            f'{absolutize(foot)}\n</div>\n{tail}{js}</body>\n</html>\n')


def pager(slug):
    order = [p[0] for p in PAGES]
    i = order.index(slug)
    prev_ = PAGES[i - 1] if i > 0 else None
    next_ = PAGES[i + 1] if i + 1 < len(PAGES) else None
    a = f'<a class="pg-prev" href="{url(prev_[0])}"><span>Previous</span>{E(prev_[1])}</a>' if prev_ else "<span></span>"
    b = f'<a class="pg-next" href="{url(next_[0])}"><span>Next</span>{E(next_[1])}</a>' if next_ else "<span></span>"
    return f'<nav class="pager wrap" aria-label="Previous and next page">{a}{b}</nav>\n'


LEVELS = {
    1: ("Starter", "One skill handles the whole task. No hand-offs."),
    2: ("Pair", "A lead skill hands part of the work to one sub-worker."),
    3: ("Team", "A lead skill coordinates two or more sub-workers."),
    4: ("Swarm", "Waves of digital workers, each with its own context, with human gates between waves."),
}


def level(g):
    """Complexity from the repository metadata: swarm structure = 4; otherwise by the number of skills the mission runs."""
    if g["structure"] == "swarm":
        return 4
    n = len(g["skills"])
    return 1 if n == 1 else 2 if n == 2 else 3


def loaded_count(g):
    names = set(g["skills"]) | set(g["support"]) | {s for w in g["workers"] for s in w.get("skills", [])}
    names |= {"medical-affairs-foundations", g["reviewer"]}
    if g["structure"] == "swarm":
        names.add(g["lead"])
    return len(names)


def level_badge(lv):
    dots = "".join(f'<i class="lv-d{" is-on" if k <= lv else ""}"></i>' for k in range(1, 5))
    return f'<span class="lv lv-{lv}" title="Level {lv} of 4: {E(LEVELS[lv][0])}"><span class="lv-dots" aria-hidden="true">{dots}</span>Level {lv} · {E(LEVELS[lv][0])}</span>'


def you_get(g):
    d = g["deliverables"]
    return d[0] + (f" + {len(d) - 1} more" if len(d) > 1 else "")


def sorted_missions(G):
    return sorted(G["missions"], key=lambda g: (level(g), loaded_count(g), len(g["handoffs"]), g["title"]))


def maps_section(G):
    groups = []
    for lv in (1, 2, 3, 4):
        ms = [g for g in sorted_missions(G) if level(g) == lv]
        if not ms:
            continue
        cards = "".join(f'''<a class="mm-card mm-card--l{lv}" href="/missions/{E(g['id'])}">
  <div class="mm-body"><h3>{E(g['title'])}</h3>
  <p class="mm-get">You get: {E(you_get(g))}</p>
  <p class="mm-meta">{level_badge(lv)}<span class="mm-n">{loaded_count(g)} skills</span></p></div>
  <div class="mm-thumb" aria-hidden="true">{MS.mini(g)}</div>
</a>''' for g in ms)
        groups.append(f'''<div class="mm-level" id="level-{lv}"><div class="mm-lh"><h3>{level_badge(lv)}</h3><p>{E(LEVELS[lv][1])}</p></div><div class="mm-grid">{cards}</div></div>''')
    return f'''<section id="mission-maps" class="section section--maps" aria-labelledby="maps-h">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">Missions</p><h2 id="maps-h">Pick a mission. <em>Start simple.</em></h2>
    <p class="sec-sub">{len(G['missions'])} missions, from one skill doing one task to a full launch-planning swarm. Each one opens with the prompt to paste into Grok Bot, the steps, and where you decide.</p></div>
    {"".join(groups)}
  </div>
</section>
'''


def mission_page(g, G, idx, prompt_fig, ta_switch):
    S = G["skills"]
    lv = level(g)
    svg_simple, nodes = MS.render(g, S, show_support=False)
    svg_full, nodes_full = MS.render(g, S, show_support=True)
    nodes.update(nodes_full)
    has_support = svg_simple != svg_full
    short = lambda s: S.get(s, {}).get("summary", "")
    # steps, from the same metadata as the chart
    steps = [f"Paste the prompt into Grok Bot (or any agent). It loads <code>medical-affairs-foundations</code> and the lead skill <code>{E(g['lead'])}</code>."]
    steps.append("It scans the data for possible safety findings first and tells you about any before doing anything else.")
    if g["structure"] == "swarm":
        for w in g["waves"]:
            if w["kind"] == "wave":
                steps.append(f"<strong>{E(w['label'])}:</strong> {E(', '.join(w['members']))}. {E(w['why'])}.")
            else:
                steps.append(f"<strong>{E(w['label'])} (you decide):</strong> {E(w['who'].replace('Human: ', ''))}. {E(w['why'])}.")
    else:
        steps.append(f"<code>{E(g['lead'])}</code> does the core task: {E(short(g['lead']))}")
        for w in g["workers"]:
            s0 = w["skills"][0]
            steps.append(f"It hands off to <code>{E(s0)}</code>: {E(short(s0))}")
        steps.append(f"<code>{E(g['reviewer'])}</code> checks the draft independently and the agent fixes what it finds.")
    steps.append("It hands you the deliverables as designed files, marked as drafts. You review and decide.")
    gates = "".join(f'<li><strong>{E(x["label"])}</strong> {E(x["detail"])}</li>' for x in g["gates"])
    files = "".join(f"<li><code>{E(f)}</code></li>" for f in g["inputs"][:8]) + (f'<li class="muted">+ {len(g["inputs"]) - 8} more</li>' if len(g["inputs"]) > 8 else "")
    loaded, seen = [], set()
    for n in nodes.values():
        for s in n["skills"]:
            if s in seen or s not in S:
                continue
            seen.add(s)
            loaded.append(f'<li><a href="{E(S[s]["url"])}" target="_blank" rel="noopener"><code>{E(s)}</code></a><span>{E(S[s]["summary"])}</span></li>')
    order = sorted_missions(G); k = [m["id"] for m in order].index(g["id"])
    prev_ = order[k - 1] if k > 0 else None
    next_ = order[k + 1] if k + 1 < len(order) else None
    pg = ((f'<a class="pg-prev" href="/missions/{prev_["id"]}"><span>Simpler</span>{E(prev_["title"])}</a>' if prev_ else '<a class="pg-prev" href="/missions"><span>Back</span>All missions</a>')
          + (f'<a class="pg-next" href="/missions/{next_["id"]}"><span>Next level up</span>{E(next_["title"])}</a>' if next_ else '<a class="pg-next" href="/missions"><span>Back</span>All missions</a>'))
    how = ("Read the waves top to bottom: the Launch Lead staffs the chart, each worker gets only its context packet, and nothing in Wave 2 starts until a person approves Gate 1. Dashed orange arrows show which worker uses whose output."
           if g["structure"] == "swarm" else
           "The lead skill runs the mission and hands each sub-worker a context packet. Dashed orange arrows are hand-offs named in the skills' metadata. A safety scan comes first and you decide at the end.")
    toggle = ('<label class="md-toggle"><input type="checkbox" id="md-sup"> Show the skills each worker loads</label>' if has_support else "")
    graph = (f'<div class="md-scroll md-v md-v--simple">{svg_simple}</div><div class="md-scroll md-v md-v--full" hidden>{svg_full}</div>' if has_support else f'<div class="md-scroll">{svg_full}</div>')
    return f'''<section id="mission" class="section section--mission" aria-labelledby="md-h">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/missions">Missions</a><span aria-hidden="true">/</span><span>{E(g['id'])}</span></nav>
    <div class="md-top">{level_badge(lv)}<span class="mm-n">{loaded_count(g)} skills</span></div>
    <h1 id="md-h" class="md-h">{E(g['title'])}</h1>
    <p class="md-what"><strong>What it does.</strong> {E(g['objective'])}</p>
    <div class="md-dir">
      <div class="md-card md-card--run"><h2 class="md-h2"><span class="md-k">1</span>Paste this into Grok Bot</h2>
        <p class="muted md-ta-l">Pick the practice data, then copy.</p>{ta_switch}{prompt_fig or ""}</div>
      <div class="md-card"><h2 class="md-h2"><span class="md-k">2</span>What you need</h2>
        <ul class="md-need"><li>Grok Bot, or any agent that can read GitHub (<a href="/grokbot">set-up</a>).</li><li>Nothing to download: the agent fetches the synthetic files itself (<a href="/data">data</a>).</li><li>About {"45" if lv == 4 else "30" if lv == 3 else "15–20"} minutes.</li></ul>
        <p class="md-sm">Files it reads ({len(g['inputs'])}):</p><ul class="md-files">{files}</ul></div>
    </div>
    <div class="md-dir">
      <div class="md-card"><h2 class="md-h2"><span class="md-k">3</span>The steps</h2><ol class="md-steps">{"".join(f"<li>{x}</li>" for x in steps)}</ol></div>
      <div class="md-card md-card--gate"><h2 class="md-h2"><span class="md-k">4</span>Where you decide</h2><ul class="md-gates">{gates}</ul>
        <h3 class="md-sm">You get</h3><ul class="chips">{"".join(f"<li>{E(d)}</li>" for d in g["deliverables"])}</ul></div>
    </div>
    <h2 class="md-h2 md-h2--big" id="how">How the agents work together</h2>
    <div class="mm-legend" aria-hidden="true"><span><i class="lg lg-lead"></i>Lead skill</span><span><i class="lg lg-worker"></i>Sub-worker skill</span>{'<span><i class="lg lg-support"></i>Loaded with it</span>' if has_support else ''}<span><i class="lg lg-review"></i>Independent check</span><span><i class="lg lg-gate"></i>You decide</span><span><i class="lg lg-hand"></i>Hand-off</span><span class="mm-hint">Click any skill</span></div>
    {toggle}
    <figure class="md-graph" aria-describedby="md-how">
      {graph}
      <p class="md-swipe" aria-hidden="true">← Swipe sideways to see the whole chart →</p>
      <figcaption id="md-how">{E(how)}</figcaption>
    </figure>
    <aside class="md-panel" id="md-panel" aria-live="polite" hidden>
      <button class="md-close" type="button" aria-label="Close details">×</button>
      <div id="md-detail"></div>
    </aside>
    <script type="application/json" id="md-data">{MS.panel_data(nodes, S)}</script>
    <details class="md-more"><summary>All {len(loaded)} skills this mission loads</summary><ul class="md-skills">{"".join(loaded)}</ul></details>
    <nav class="pager pager--in" aria-label="Previous and next mission">{pg}</nav>
  </div>
</section>
'''


def deck_section(ev):
    p = HERE / "deck" / "deck.json"
    if not p.exists():
        return ""
    D = json.loads(p.read_text(encoding="utf-8"))
    S = D["slides"]; n = len(S)
    mb = lambda b: f"{b / 1e6:.0f} MB"
    first = S[0]
    thumbs = "".join(f'<li><button type="button" class="dk-th" data-i="{i}" aria-label="Slide {s["n"]}"{" aria-current=\"true\"" if i == 0 else ""}><img src="{E(s["thumb"])}" alt="" loading="lazy" decoding="async" width="160" height="90"><span>{s["n"]}</span></button></li>' for i, s in enumerate(S))
    return f'''<section id="deck" class="section section--deck" aria-labelledby="deck-h">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">The deck</p><h1 class="md-h" id="deck-h">AI in Action — <em>Vivek’s Deck</em></h1>
      <p class="sec-sub">{n} slides. The opening keynote, Oct 13. Use the arrow keys or swipe to move through it.</p>
      <div class="dk-dl"><a class="btn-primary" href="{E(D["pdf"])}" download>Download PDF <small>{mb(D["pdf_bytes"])}</small></a><a class="btn-ghost" href="{E(D["pptx"])}" download>Download PowerPoint (.pptx) <small>{mb(D["pptx_bytes"])}</small></a></div>
    </div>
    <div class="dk" data-slides="{E(json.dumps([s["src"] for s in S]))}">
      <div class="dk-stage" tabindex="0" aria-roledescription="carousel" aria-label="Slides">
        <img class="dk-img" src="{E(first["src"])}" alt="Slide 1 of {n}" width="{first["w"]}" height="{first["h"]}" decoding="async" fetchpriority="high">
        <button type="button" class="dk-nav dk-prev" aria-label="Previous slide"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>
        <button type="button" class="dk-nav dk-next" aria-label="Next slide"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>
      </div>
      <div class="dk-bar"><span class="dk-count" aria-live="polite"><b>1</b> / {n}</span><button type="button" class="dk-fs" aria-label="Full screen">Full screen</button></div>
      <ol class="dk-thumbs" aria-label="All slides">{thumbs}</ol>
    </div>
  </div>
</section>
'''


def paginate(files, cfg, graphs_path=HERE / "data/mission-graphs.json"):
    import wording
    G = json.loads(wording.soften(Path(graphs_path).read_text(encoding="utf-8")))
    ev = cfg.get("event", {})
    site = (cfg.get("site_url") or "").rstrip("/")
    head, pre, chunks, ids, foot, tail = split_sections(files["index.html"])
    chunks["mission-maps"] = maps_section(G)
    chunks["deck"] = deck_section(ev)
    import hackathon_pages as HK
    hk_pages = HK.pages()
    if hk_pages:
        chunks["hackathon"] = hk_pages[0][3]
        chunks["hero"] = re.sub(r'(<a class="btn-ghost" href="[^"]*optimizer">Optimize a prompt</a>)', r'<a class="btn-ghost" href="/hackathon">Hackathon guide</a>\1', chunks["hero"], count=1)
        chunks["agenda"] = chunks["agenda"].replace('<span class="ag-title">Build the AI worker</span>', '<span class="ag-title">Build the AI worker</span><a class="ag-link" href="/hackathon">Hackathon guide: the afternoon flow and your vertical →</a>', 1)
        chunks["agenda"] = chunks["agenda"].replace('<span class="ag-title">Hackathon + demo presentations</span>', '<span class="ag-title">Hackathon + demo presentations</span><a class="ag-link" href="/hackathon#final-presentation">Teams present in order 01→04, about 20 minutes each →</a>', 1)
    if chunks["deck"]:
        chunks["hero"] = re.sub(r'(<a class="btn-ghost" href="[^"]*optimizer">Optimize a prompt</a>)', r'\1<a class="btn-ghost" href="/deck">See the deck</a>', chunks["hero"], count=1)
    # the original prompt grid stays reachable (ids and links) but folded away under the team missions
    chunks["missions"] = re.sub(r'<h3 class="sub-h">All (\d+) workshop missions</h3>\s*<div class="mcs">(.*?)</div>\s*</div>\s*</section>',
        lambda m: f'<details class="mm-all"><summary>All {m.group(1)} mission prompts on one page</summary><div class="mcs">{m.group(2)}</div></details>\n  </div>\n</section>', chunks["missions"], count=1, flags=re.S)
    chunks["missions"] = chunks["missions"].replace('<h2 id="missions-h">Pick a task. <em>Copy. Paste. Go.</em></h2>', '<h2 id="missions-h">Team missions. <em>For the hackathon.</em></h2>')
    # add org-chart links to the existing mission prompt cards
    m_ids = {g["id"] for g in G["missions"]}
    chunks["missions"] = re.sub(r'(<article class="mc[^"]*" id="m-([a-z0-9-]+)">\s*<div class="mc-top">)(.*?)(</div>)',
                                lambda m: m.group(1) + m.group(3) + (f'<a class="mc-map" href="/missions/{m.group(2)}">Open mission →</a>' if m.group(2) in m_ids else "") + m.group(4),
                                chunks["missions"], flags=re.S)
    placed = {s for p in PAGES for s in p[2]}
    leftovers = [s for s in ids if s not in placed]
    if leftovers:  # anything new in build.py lands on the home page rather than vanishing
        PAGES[0] = (PAGES[0][0], PAGES[0][1], PAGES[0][2] + leftovers, PAGES[0][3], PAGES[0][4])
    id_page = {}
    for slug, _, secs, _, _ in PAGES:
        SECTION_IDS[slug] = set(secs)
        for s in secs:
            for x in re.findall(r'\bid="([A-Za-z0-9_-]+)"', chunks.get(s, "")):
                id_page.setdefault(x, slug)
            id_page.setdefault(s, slug)
    id_page["top"] = ""
    out = {}
    for slug, label, secs, title, blurb in PAGES:
        body = "".join(chunks.get(s, "") for s in secs)
        here = set(re.findall(r'\bid="([A-Za-z0-9_-]+)"', body)) | set(secs)
        body = relink(absolutize(body), here, id_page) + pager(slug)
        full_title = f"{title} · {ev.get('name', 'AI in Action')}" if slug else re.search(r"<title>(.*?)</title>", head).group(1)
        desc = f"{blurb}. AI agents: read /agents.md (Instructions for agents) and follow it."
        extra_css = ["missions.css"] if slug == "missions" else ["deck.css"] if slug == "deck" else ["hackathon.css"] if slug == "hackathon" else []
        hd = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', head, flags=re.S) if slug == "hackathon" else head  # no clock times on hackathon pages
        out[f"{slug or 'index'}.html"] = assemble(page_head(hd, full_title, desc, f"{site}{url(slug)}", extra_css), pre, slug, ev, body, foot, tail, extra_js=("deck.js",) if slug == "deck" else ())
    # mission detail pages
    tsw = re.search(r'<div class="ta-switch".*?</button></div>', chunks["missions"], re.S)
    ta_html = tsw.group(0) if tsw else ""
    for i, g in enumerate(G["missions"]):
        fig = re.search(rf'<article class="mc[^"]*" id="m-{re.escape(g["id"])}">.*?(<figure class="prompt.*?</figure>)', chunks["missions"], re.S)
        body = mission_page(g, G, i, absolutize(fig.group(1)) if fig else "", ta_html)
        body = relink(body, set(re.findall(r'\bid="([A-Za-z0-9_-]+)"', body)), id_page)
        h = page_head(head, f"{g['title']} · Mission map · {ev.get('name', 'AI in Action')}", f"Org chart for the {g['id']} mission: lead skill, sub-workers, hand-offs and human checkpoints. AI agents: read /agents.md.", f"{site}/missions/{g['id']}", ["missions.css"])
        out[f"missions/{g['id']}.html"] = assemble(h, pre, "missions", ev, body, foot, tail, "is-mission", ("mission-graph.js",))
    # hackathon vertical pages
    for path, title, desc, html_ in hk_pages[1:]:
        body = relink(absolutize(html_), set(re.findall(r'\bid="([A-Za-z0-9_-]+)"', html_)), id_page)
        h = page_head(re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', head, flags=re.S), f"{title} · {ev.get('name', 'AI in Action')}", desc + " AI agents: read /agents.md.", f"{site}/{path}", ["hackathon.css"])
        out[f"{path}.html"] = assemble(h, pre, "hackathon", ev, body, foot, tail, "is-hackathon")
    # 404
    nf = ('<section class="section"><div class="wrap"><div class="sec-head"><p class="kicker">404</p><h1 class="md-h">That page isn’t here.</h1>'
          '<p class="sec-sub">Use the menu, or start at <a href="/">Home</a>. Agents: read <a href="/agents.md">/agents.md</a>.</p></div></div></section>\n')
    out["404.html"] = assemble(page_head(head, "Not found · " + ev.get("name", ""), "Page not found.", f"{site}/404", []), pre, "__none__", ev, nf, foot, tail)
    files.update(out)
    # agent-readable docs: page URLs instead of #anchors, and a page list
    pages_md = ["## Pages on this site", "Each section is its own page (deep-linkable):"] + [f"- {label}: {site}{url(slug)} ({blurb})" for slug, label, _, _, blurb in PAGES] + \
               ["", "Mission pages (directions first: prompt to paste, what you need, steps, where the human decides; then the org chart of skills). Levels: 1 Starter = one skill, 2 Pair = lead + one sub-worker, 3 Team = lead + two or more sub-workers, 4 Swarm = waves of digital workers with human gates:"] + \
               [f"- Level {level(g)} {LEVELS[level(g)][0]} · {g['id']}: {site}/missions/{g['id']}" for g in sorted_missions(G)] + \
               [f"- Machine-readable graph data: {site}/data/mission-graphs.json", ""] + \
               (["Hackathon vertical guides (Day 1 agenda, missions, data, AI ideas, swarm shape, human gates, copyable prompts, impact worksheet, facilitator questions):"] +
                [f"- 0{v[0]} {v[3]}: {site}/hackathon/{v[1]} (Markdown: {site}/hackathon/files/{v[2]})" for v in HK.VERTICALS] + [""] if hk_pages else [])
    block = "\n".join(pages_md) + "\n"
    for name in ("agents.md", "llms.txt"):
        t = files[name]
        t = re.sub(re.escape(site) + r"/#([a-z0-9-]+)", lambda m: f"{site}{url(id_page.get(m.group(1), ''))}" + ("" if m.group(1) in SECTION_IDS.get(id_page.get(m.group(1), ""), ()) else f"#{m.group(1)}"), t)
        anchor = "\n## 2. Greet, then ask" if name == "agents.md" else "\n## Data repository"
        if anchor in t and "## Pages on this site" not in t:
            t = t.replace(anchor, "\n" + block + anchor, 1)
        files[name] = t
    return files
