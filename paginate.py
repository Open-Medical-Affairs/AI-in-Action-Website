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
    ("agenda", "Agenda", ["agenda"], "Agenda", "Two days in Philadelphia, session by session"),
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


def maps_section(G):
    S, cards = G["skills"], []
    for i, g in enumerate(G["missions"], 1):
        n_loaded = len(set(g["skills"]) | set(g["support"]) | {s for w in g["workers"] for s in w.get("skills", [])})
        kind = f'{len(g["workers"])} digital workers in {sum(1 for w in g["waves"] if w["kind"] == "wave")} waves' if g["structure"] == "swarm" else (f'Lead + {len(g["workers"])} sub-worker{"s" if len(g["workers"]) != 1 else ""}' if g["workers"] else "Single lead skill")
        pend = '<span class="mm-pend">Pending merge · PR #8</span>' if g["pending"] else ""
        cards.append(f'''<a class="mm-card{' mm-card--swarm' if g['structure'] == 'swarm' else ''}" href="/missions/{E(g['id'])}">
  <div class="mm-fig">{MS.mini(g)}</div>
  <div class="mm-body"><div class="mm-top"><span class="mc-n">{i:02d}</span><code>{E(g['id'])}</code>{pend}</div>
  <h3>{E(g['title'])}</h3>
  <p class="mm-meta">{E(kind)} · {n_loaded + 2} skills loaded · {len([x for x in g['gates']])} human checkpoints</p>
  <span class="mm-go">Open the org chart →</span></div>
</a>''')
    return f'''<section id="mission-maps" class="section section--maps" aria-labelledby="maps-h">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">Mission maps</p><h2 id="maps-h">Every mission is a <em>team of skills.</em></h2>
    <p class="sec-sub">Each card is an org chart built from the repository itself: the lead skill, the skills it loads as sub-workers, the hand-offs between them, the human checkpoints, and the data in and deliverables out. Open one to click through the workers.</p></div>
    <div class="mm-legend" aria-hidden="true"><span><i class="lg lg-lead"></i>Lead skill</span><span><i class="lg lg-worker"></i>Sub-worker skill</span><span><i class="lg lg-support"></i>Loaded with it</span><span><i class="lg lg-gate"></i>Human checkpoint</span><span><i class="lg lg-hand"></i>Hand-off</span></div>
    <div class="mm-grid">{"".join(cards)}</div>
    <p class="mm-src muted">Built from <code>workshop/catalog.json</code> and each skill's <code>SKILL.md</code> metadata in Medical-Affairs-Skills ({E(G['ref'])} @ {E(G['commit'])}). Missions marked “Pending merge” are in <a href="{E(G['pr'])}" target="_blank" rel="noopener">PR #8</a> and not yet on the default branch. Machine-readable: <a href="/data/mission-graphs.json">/data/mission-graphs.json</a>.</p>
  </div>
</section>
'''


def mission_page(g, G, idx, prompt_fig):
    S = G["skills"]
    svg, nodes = MS.render(g, S)
    pend = (f'<p class="md-pend"><strong>Pending merge.</strong> This mission and the skills marked PENDING live on the <code>{E(G["ref"])}</code> branch in <a href="{E(G["pr"])}" target="_blank" rel="noopener">PR #8</a>; they are not on the default branch yet.</p>' if g["pending"] or any(S.get(s, {}).get("pending") for n in nodes.values() for s in n["skills"]) else "")
    loaded = []
    seen = set()
    for n in nodes.values():
        for s in n["skills"]:
            if s in seen or s not in S:
                continue
            seen.add(s)
            loaded.append(f'<li><a href="{E(S[s]["url"])}" target="_blank" rel="noopener"><code>{E(s)}</code></a>{" <span class=mm-pend>Pending</span>" if S[s]["pending"] else ""}<span>{E(S[s]["summary"])}</span></li>')
    prev_ = G["missions"][idx - 1] if idx > 0 else None
    next_ = G["missions"][idx + 1] if idx + 1 < len(G["missions"]) else None
    pg = ((f'<a class="pg-prev" href="/missions/{prev_["id"]}"><span>Previous mission</span>{E(prev_["title"])}</a>' if prev_ else '<a class="pg-prev" href="/missions"><span>Back</span>All missions</a>')
          + (f'<a class="pg-next" href="/missions/{next_["id"]}"><span>Next mission</span>{E(next_["title"])}</a>' if next_ else '<a class="pg-next" href="/missions"><span>Back</span>All missions</a>'))
    how = ("Read the waves top to bottom: the Launch Lead staffs the chart, each worker gets only its context packet, and nothing in Wave 2 starts until a human approves Gate 1. Dashed orange arrows show which worker consumes whose output."
           if g["structure"] == "swarm" else
           "The lead skill runs the mission and hands each sub-worker skill a context packet; dashed pills are skills they load with them; dashed orange arrows are hand-offs named in the skills' metadata. A safety scan comes first and you decide at the end.")
    return f'''<section id="mission" class="section section--mission" aria-labelledby="md-h">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/missions">Missions</a><span aria-hidden="true">/</span><span>{E(g['id'])}</span></nav>
    <div class="sec-head"><p class="kicker">Mission {idx + 1:02d} · {"Agent swarm" if g['structure'] == 'swarm' else "Skill team"}</p><h1 id="md-h" class="md-h">{E(g['title'])}</h1>
    <p class="sec-sub">{E(g['objective'])}</p></div>
    {pend}
    <div class="mm-legend" aria-hidden="true"><span><i class="lg lg-lead"></i>Lead skill</span><span><i class="lg lg-worker"></i>Sub-worker skill</span><span><i class="lg lg-support"></i>Loaded with it</span><span><i class="lg lg-review"></i>Independent check</span><span><i class="lg lg-gate"></i>Human checkpoint</span><span><i class="lg lg-hand"></i>Hand-off</span><span class="mm-hint">Tip: click any skill or gate</span></div>
    <figure class="md-graph" aria-describedby="md-how">
      <div class="md-scroll">{svg}</div>
      <p class="md-swipe" aria-hidden="true">← Swipe sideways to see the whole chart →</p>
      <figcaption id="md-how">{E(how)}</figcaption>
    </figure>
    <aside class="md-panel" id="md-panel" aria-live="polite" hidden>
      <button class="md-close" type="button" aria-label="Close details">×</button>
      <div id="md-detail"></div>
    </aside>
    <script type="application/json" id="md-data">{MS.panel_data(nodes, S)}</script>
    <div class="md-cols">
      <div><h2 class="sub-h">Skills this mission loads ({len(loaded)})</h2><ul class="md-skills">{"".join(loaded)}</ul></div>
      <div><h2 class="sub-h">Run it</h2>{prompt_fig or ""}<p class="muted md-src">Graph generated from <code>workshop/catalog.json</code> and {E(g['source'])} ({E(G['ref'])} @ {E(G['commit'])}). Data: <a href="/data">synthetic packs</a>.</p></div>
    </div>
    <nav class="pager pager--in" aria-label="Previous and next mission">{pg}</nav>
  </div>
</section>
'''


def paginate(files, cfg, graphs_path=HERE / "data/mission-graphs.json"):
    G = json.loads(Path(graphs_path).read_text(encoding="utf-8"))
    ev = cfg.get("event", {})
    site = (cfg.get("site_url") or "").rstrip("/")
    head, pre, chunks, ids, foot, tail = split_sections(files["index.html"])
    chunks["mission-maps"] = maps_section(G)
    # add org-chart links to the existing mission prompt cards
    m_ids = {g["id"] for g in G["missions"]}
    chunks["missions"] = re.sub(r'(<article class="mc[^"]*" id="m-([a-z0-9-]+)">\s*<div class="mc-top">)(.*?)(</div>)',
                                lambda m: m.group(1) + m.group(3) + (f'<a class="mc-map" href="/missions/{m.group(2)}">Org chart →</a>' if m.group(2) in m_ids else "") + m.group(4),
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
        extra_css = ["missions.css"] if slug == "missions" else []
        out[f"{slug or 'index'}.html"] = assemble(page_head(head, full_title, desc, f"{site}{url(slug)}", extra_css), pre, slug, ev, body, foot, tail)
    # mission detail pages
    for i, g in enumerate(G["missions"]):
        fig = re.search(rf'<article class="mc[^"]*" id="m-{re.escape(g["id"])}">.*?(<figure class="prompt.*?</figure>)', chunks["missions"], re.S)
        body = mission_page(g, G, i, absolutize(fig.group(1)) if fig else "")
        body = relink(body, set(re.findall(r'\bid="([A-Za-z0-9_-]+)"', body)), id_page)
        h = page_head(head, f"{g['title']} · Mission map · {ev.get('name', 'AI in Action')}", f"Org chart for the {g['id']} mission: lead skill, sub-workers, hand-offs and human checkpoints. AI agents: read /agents.md.", f"{site}/missions/{g['id']}", ["missions.css"])
        out[f"missions/{g['id']}.html"] = assemble(h, pre, "missions", ev, body, foot, tail, "is-mission", ("mission-graph.js",))
    # 404
    nf = ('<section class="section"><div class="wrap"><div class="sec-head"><p class="kicker">404</p><h1 class="md-h">That page isn’t here.</h1>'
          '<p class="sec-sub">Use the menu, or start at <a href="/">Home</a>. Agents: read <a href="/agents.md">/agents.md</a>.</p></div></div></section>\n')
    out["404.html"] = assemble(page_head(head, "Not found · " + ev.get("name", ""), "Page not found.", f"{site}/404", []), pre, "__none__", ev, nf, foot, tail)
    files.update(out)
    # agent-readable docs: page URLs instead of #anchors, and a page list
    pages_md = ["## Pages on this site", "Each section is its own page (deep-linkable):"] + [f"- {label}: {site}{url(slug)} ({blurb})" for slug, label, _, _, blurb in PAGES] + \
               ["", "Mission org charts (lead skill, sub-worker skills, hand-offs, human checkpoints), one page per mission:"] + \
               [f"- {g['id']}: {site}/missions/{g['id']}{' (pending merge, PR #8)' if g['pending'] else ''}" for g in G["missions"]] + \
               [f"- Machine-readable graph data: {site}/data/mission-graphs.json", ""]
    block = "\n".join(pages_md) + "\n"
    for name in ("agents.md", "llms.txt"):
        t = files[name]
        t = re.sub(re.escape(site) + r"/#([a-z0-9-]+)", lambda m: f"{site}{url(id_page.get(m.group(1), ''))}" + ("" if m.group(1) in SECTION_IDS.get(id_page.get(m.group(1), ""), ()) else f"#{m.group(1)}"), t)
        anchor = "\n## 2. Greet, then ask" if name == "agents.md" else "\n## Data repository"
        if anchor in t and "## Pages on this site" not in t:
            t = t.replace(anchor, "\n" + block + anchor, 1)
        files[name] = t
    return files
