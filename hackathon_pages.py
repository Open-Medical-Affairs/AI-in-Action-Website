"""Build /hackathon and /hackathon/<vertical> from the published pack in hackathon/files/ (see tools/build_hackathon.py)."""
import html, json, re
from pathlib import Path
import mdlite

E = lambda s: html.escape(str(s), quote=True)
HERE = Path(__file__).resolve().parent
FILES = HERE / "hackathon" / "files"
SITE = "https://aiinaction.up.railway.app"
VERTICALS = [  # number, slug (route), md file, name, one line, slot
    (1, "publications-brain", "01-publications-brain.md", "Publications Brain", "What to publish, what to stop, and keeping every output consistent.", ""),
    (2, "insights-engine", "02-insights-engine.md", "Insights Engine", "From field insights to care and knowledge gaps to curated HCP content for each persona and stage.", ""),
    (3, "congress-monitor", "03-congress-monitor.md", "Congress Monitor", "The congress just ended. What changed, and what do we do about it?", ""),
    (4, "field-intelligence-engine", "04-field-intelligence-engine.md", "Field Intelligence Engine", "Walk into every HCP conversation prepared, and close the loop after.", ""),
]
FACIL = {2: "John and Anjali"}  # named facilitators per vertical
# Hackathon teams (handwritten sign-up sheet, Day 1). Key: vertical number -> (team number, members, facilitators)
TEAMS = {
    4: (1, ["Nandini Sabharwal", "Jason Lebowitz", "Tom Canavela", "Allison McMullen", "Andy Yan", "Paul Minen", "Tony Rebelo", "Michelle Vichnin"], ()),
    2: (2, ["Anjali Mishra", "John Hannis", "Kara Koehler", "Brianna Cauley", "Chris Herold", "Mamta Parikh", "Liz Hernandez", "Chris Miller"], ("Anjali Mishra", "John Hannis")),
    1: (3, ["Pooja Smith", "Vijay Krishnan", "Richa Garg", "Bennie Coccia", "Lucie Vu", "Charlene Wong", "Megan Kinnett", "Jonathan Weimer"], ()),
    3: (4, ["Nita Thingalaya", "Kristina Kipp", "Michelle Cho", "Yusuke Sasaki", "Stefanie Maurer", "Chelsea Bennheisel", "Jackie Armani", "Susan Connelly"], ()),
}
TEAMDECK = "teams/AI-in-Action-Hackathon-Teams"
F = lambda p: f"/hackathon/files/{p}"
FACILITATOR = ("walk-around question bank", "common pitfalls")


def available():
    return (FILES / "README.md").exists()


def mb(n):
    return f"{n / 1e6:.1f} MB" if n >= 1e6 else f"{max(1, round(n / 1e3))} KB"


def sizes():
    try:
        return json.loads((HERE / "hackathon" / "pack.json").read_text())["sizes"]
    except Exception:
        return {}


def link(u):
    if u.startswith(SITE):
        return u[len(SITE):] or "/"
    if not re.match(r"[a-z]+:", u) and not u.startswith(("/", "#")):
        return F(u)
    return u


def dl(path, label, primary=False, note=""):
    s = sizes().get(path)
    cls = "btn-primary" if primary else "btn-ghost"
    return f'<a class="{cls} hk-dl" href="{F(path)}" download>{E(label)}{f" <small>{mb(s)}</small>" if s else ""}</a>'


def guide_name(v):
    return f"0{v[0]}-{v[3].replace(' ', '-')}-Facilitator-Guide.pdf"


def guide_btn(v, primary=True, short=False):
    path = f"guides/{guide_name(v)}"
    label = (f"0{v[0]} {v[3]}" if short else "Download facilitator guide (PDF)")
    if (FILES / path).exists():
        return dl(path, label, primary)
    return f'<span class="{"btn-primary" if primary else "btn-ghost"} hk-dl is-soon" aria-disabled="true">{E(label)} <small>coming soon</small></span>'


def vertical_card(v):
    n, slug, md, name, line, slot = v
    t = (FILES / md).read_text(encoding="utf-8")
    warm = re.search(r"\| Warm-up missions \| (.*?) \|\n", t)
    warm_ids = re.findall(r"\[`([a-z0-9-]+)`\]", warm.group(1)) if warm else []
    lead = re.search(r"\| Lead skill for the hack \| \[`([a-z0-9-]+)`\]", t)
    thumb = f"guides/{guide_name(v).replace('.pdf', '-p1.jpg')}"
    img = (f'<img class="hk-thumb" src="{F(thumb)}" alt="Page 1 of the {E(name)} facilitator guide" loading="lazy">' if (FILES / thumb).exists() else "")
    return (f'<div class="hk-cardwrap"><a class="hk-card hk-card--{n}" href="/hackathon/{slug}">{img}<span class="hk-num">0{n}</span><h3>{E(name)}</h3><p>{E(line)}</p>'
            f'<dl><div><dt>Warm-ups</dt><dd>{" · ".join(f"<code>{E(w)}</code>" for w in warm_ids)}</dd></div>'
            + (f'<div><dt>Team</dt><dd>Team {TEAMS[n][0]} · {len(TEAMS[n][1])} members</dd></div>' if n in TEAMS else '')
            + (f'<div><dt>Facilitators</dt><dd>{E(FACIL[v[0]])}</dd></div>' if v[0] in FACIL else '') +
            f'<div><dt>Lead skill</dt><dd><code>{E(lead.group(1) if lead else "")}</code></dd></div>'
            f'<div><dt>Presents</dt><dd>Day 2 · {["first", "second", "third", "fourth"][n - 1]}, about 20 min</dd></div></dl><span class="hk-go">Open the guide →</span></a>{guide_btn(v, False)}</div>')


def howto_block():
    p = FILES / "how-to-use-template.md"
    if p.exists():
        t = re.sub(r"\A# .*\n+", "", p.read_text(encoding="utf-8"))
        body = mdlite.render(t, link, "hkt", shift=1, copy_all=True)
        more = f'<p class="hk-aside"><a href="{F("how-to-use-template.md")}">how-to-use-template.md</a></p>'
    else:
        body = ('<ol class="hk-steps">'
                '<li><b>Day 1, near the end of Grok Bot setup.</b> Copy the agent instructions below and paste them into your team’s Grok Bot conversation.</li>'
                '<li><b>As you work.</b> Say “log that” and upload screenshots; the agent keeps <code>capture-log.md</code>.</li>'
                '<li><b>At the start of Day 2.</b> Download the template, attach it in Grok Bot and say <em>“Build the final deck now.”</em> Review every slide before you present.</li></ol>')
        more = ""
    return f'<div class="hk-howto" id="how-to-use-the-template"><p class="kicker">Step by step</p><h3>How to use the template with Grok Bot</h3>{body}{more}</div>'


def final_block():
    instr = (FILES / "final-presentation-agent-instructions.md").read_text(encoding="utf-8")
    return f'''<section class="section hk-final" id="final-presentation" aria-labelledby="hk-final-h">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">Day 2</p><h2 id="hk-final-h">Final presentation</h2>
      <p class="sec-sub">About 20 minutes per team, give or take, including a few questions. Teams present in order 01→04 on Day 2. Grok Bot keeps a capture log as you work on Day 1 and, on Day 2, fills the template into your final deck.</p></div>
    <div class="hk-final-grid">
      <div class="hk-final-main">
        <figure class="hk-sheet"><a href="{F("template/template-contact-sheet.jpg")}" target="_blank" rel="noopener"><img src="{F("template/template-contact-sheet.jpg")}" alt="All slides of the final presentation template" loading="lazy"></a>
          <figcaption>The final presentation template. Every slide has [bracket] placeholders and notes on what to fill in.</figcaption></figure>
        <div class="hk-btns">
          {dl("template/AI-in-Action-Final-Presentation-Template.pptx", "Download the template (.pptx)", True)}
          {dl("capture-log-template.md", "Capture log template (.md)")}
        </div>
      </div>
      <div class="hk-final-side">
        {howto_block()}
        <div class="hk-agent"><h3>Agent instructions</h3><p>The full recorder and deck-builder instructions for Grok Bot (or any agent).</p>
          <div class="hk-btns">
            <button type="button" class="btn-primary hk-copy" data-copy="#hk-agent-instr" aria-label="Copy agent instructions"><svg class="i-copy" aria-hidden="true"><use href="#ic-copy"/></svg><svg class="i-check" aria-hidden="true"><use href="#ic-check"/></svg><span class="lbl">Copy agent instructions</span></button>
            {dl("final-presentation-agent-instructions.md", "Download (.md)")}
          </div>
          <details class="hk-instr"><summary>Read the agent instructions</summary><pre id="hk-agent-instr" class="prompt-text"><code>{E(instr)}</code></pre></details></div>
      </div>
    </div>
  </div>
</section>
'''


def downloads_block():
    return f'''<section class="section hk-dls" id="hackathon-downloads" aria-labelledby="hk-dl-h">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">Downloads</p><h2 id="hk-dl-h">The whole pack</h2></div>
    <div class="hk-dl-grid">
      <div class="hk-dl-card"><h3>Facilitator guides (PDF)</h3><p>One designed guide per vertical: agenda, missions, data, ideas, swarm shape, gates, prompts, questions and impact worksheet.</p><div class="hk-guides">{"".join(guide_btn(v, False, True) for v in VERTICALS)}</div></div>
      <div class="hk-dl-card"><h3>Hackathon kickoff deck</h3><p>Hack the workflow: what a hack is, Efficiency vs Opportunity AI, the four challenges and the rules.</p>
        <div class="hk-btns">{dl("kickoff/AI-in-Action-Hackathon-Intro.pdf", "PDF", True)}{dl("kickoff/AI-in-Action-Hackathon-Intro.pptx", "PowerPoint (.pptx)")}</div></div>
      {f'<div class="hk-dl-card"><h3>Team map</h3><p>All four teams around their vertical hubs, one slide per team with every member.</p><div class="hk-btns">{dl(TEAMDECK + ".pdf", "PDF", True)}{dl(TEAMDECK + ".pptx", "PowerPoint (.pptx)")}</div></div>' if (FILES / (TEAMDECK + ".pdf")).exists() else ""}
      <div class="hk-dl-card"><h3>Closing session slides</h3><p>Panel and audience questions for the Day 2 close (Moderator: Vivek). Notes stripped.</p>
        <div class="hk-btns">{dl("closing/AI-in-Action-Closing-Session.pdf", "PDF", True)}{dl("closing/AI-in-Action-Closing-Session.pptx", "PowerPoint (.pptx)")}</div></div>
      <div class="hk-dl-card"><h3>Guides as Markdown</h3><p>For agents and for editing.</p><ul class="hk-mdlist">{"".join(f'<li><a href="{F(v[2])}">{E(v[2])}</a></li>' for v in VERTICALS)}<li><a href="{F("README.md")}">README.md</a></li></ul></div>
    </div>
  </div>
</section>
'''


def team_list(n, cls="hk-members"):
    num, members, leads = TEAMS[n]
    return f'<ul class="{cls}">' + "".join(
        f'<li class="{"is-lead" if m in leads else ""}"><span class="hk-ini" aria-hidden="true">{E(m.split()[0][0] + m.split()[-1][0])}</span>{E(m)}{"<small>Facilitator</small>" if m in leads else ""}</li>'
        for m in members) + "</ul>"


def team_dl_btns():
    if not (FILES / f"{TEAMDECK}.pdf").exists():
        return ""
    return f'<div class="hk-btns">{dl(TEAMDECK + ".pdf", "Download the team map (PDF)", True)}{dl(TEAMDECK + ".pptx", "PowerPoint (.pptx)")}</div>'


def teams_block():
    if not TEAMS:
        return ""
    total = sum(len(t[1]) for t in TEAMS.values())
    cells = "".join(f'<a class="hk-tm hk-tm--{v[0]}" href="/hackathon/teams#team-{TEAMS[v[0]][0]}"><span class="hk-num">Vertical 0{v[0]} · Team {TEAMS[v[0]][0]}</span><b>{E(v[3])}</b><span>{len(TEAMS[v[0]][1])} members</span></a>'
                    for v in VERTICALS if v[0] in TEAMS)
    return (f'<div class="hk-teams" id="teams"><div class="hk-teams-head"><div><p class="kicker">Teams</p><h2 class="hk-h2">Find your team</h2>'
            f'<p class="hk-aside">{len(TEAMS)} teams, {total} hackers, one vertical each. <a href="/hackathon/teams">See every team and its members →</a></p></div>{team_dl_btns()}</div>'
            f'<div class="hk-tm-grid">{cells}</div></div>')


def teams_page():
    total = sum(len(t[1]) for t in TEAMS.values())
    img = f"{TEAMDECK.rsplit('/', 1)[0]}/team-map-overview.jpg"
    fig = (f'<figure class="hk-sheet hk-tm-fig"><a href="{F(TEAMDECK + ".pdf")}" target="_blank" rel="noopener"><img src="{F(img)}" alt="Team map: four teams around four vertical hubs" loading="lazy"></a>'
           f'<figcaption>The team map deck: an overview, then one slide per team with its members around the vertical’s hub.</figcaption></figure>' if (FILES / img).exists() else "")
    blocks = ""
    for v in VERTICALS:
        n, slug, md, name, line, slot = v
        if n not in TEAMS:
            continue
        num, members, leads = TEAMS[n]
        blocks += (f'<article class="hk-team hk-team--{n}" id="team-{num}"><header><p class="kicker">Vertical 0{n} · presents {["first", "second", "third", "fourth"][n - 1]} on Day 2</p>'
                   f'<h2>{E(name)}</h2><p class="hk-team-sub">Team {num} · {len(members)} members{f" · facilitators {E(FACIL[n])}" if n in FACIL else ""}</p><p class="hk-team-line">{E(line)}</p></header>'
                   f'{team_list(n)}<a class="hk-go" href="/hackathon/{slug}">Open the {E(name)} guide →</a></article>')
    return f'''<section class="section hk-teams-page" id="hackathon-teams" aria-labelledby="hkt-h">
  <div class="wrap">
    <p class="hk-crumb"><a href="/hackathon">Hackathon</a> / Teams</p>
    <div class="sec-head"><p class="kicker">Hackathon · Team map</p><h1 class="md-h" id="hkt-h">Four teams, <em>four verticals</em>.</h1>
      <p class="sec-sub">{total} hackers in {len(TEAMS)} teams. Each team works one Medical Affairs vertical: find your name, then open your vertical’s guide.</p>
      {team_dl_btns()}</div>
    <div class="hk-team-grid">{blocks}</div>
    {fig}
    <p class="hk-aside">Names were transcribed from the handwritten sign-up sheet. Spot a typo? Tell a facilitator.</p>
  </div>
</section>
<nav class="pager wrap" aria-label="Hackathon"><a class="pg-prev" href="/hackathon"><span>Back to</span>Hackathon</a><a class="pg-next" href="/hackathon/{VERTICALS[0][1]}"><span>Vertical 01</span>{E(VERTICALS[0][3])}</a></nav>
'''


def hub():
    cards = "".join(vertical_card(v) for v in VERTICALS)
    return f'''<section id="hackathon" class="section hk-hub" aria-labelledby="hackathon-h">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">Hackathon · Oct 13–14</p><h1 class="md-h" id="hackathon-h">Hack the <em>workflow</em>.</h1>
      <p class="sec-sub">For two days, you are hackers: prototype fast with practice data, prove it works, harden it later. Four teams, four Medical Affairs challenges, one AI workforce each, with a person deciding at every gate.</p></div>
    <div class="hk-two">
      <article class="hk-ai hk-ai--eff"><p class="kicker">Efficiency AI</p><h3>Do today’s work better</h3><p>Faster, cheaper, better processes: the same work, done with less effort per output. The foundation of most AI adoption.</p></article>
      <span class="hk-vs" aria-hidden="true">+</span>
      <article class="hk-ai hk-ai--opp"><p class="kicker">Opportunity AI</p><h3>Do what was never possible</h3><p>New work and new value: “What might we do now that we never would have considered before?” Build it on top of efficiency.</p></article>
    </div>
    <p class="hk-credit">Framework: Nathaniel Whittemore (NLW), The AI Daily Brief. Hack for opportunity, not just efficiency.</p>

    <h2 class="hk-h2">The two days</h2>
    <div class="hk-days">
      <div class="hk-day"><p class="kicker">Day 1 · Tue Oct 13 · afternoon · suggested, optional</p>
        <ol class="hk-flow">
          <li><i class="hk-dur">about 30 min</i><b>Set up Grok Bot</b><span>sign in, load the skills, read one practice file, start the capture log</span></li>
          <li><i class="hk-dur">about 40 min</i><b>Warm-up missions</b><span>two pairs run two easier missions, then swap</span></li>
          <li><i class="hk-dur">about 45 min</i><b>Workflow ideation</b><span>map today’s workflow, choose one problem, Efficiency or Opportunity</span></li>
          <li><i class="hk-dur">about 1½ hours</i><b>The hack</b><span>build the swarm, stop at both human gates, capture screenshots and timings</span></li>
        </ol>
        <p class="hk-aside">Facilitators circulate and ask questions all afternoon. There is no formal share-out; the day ends with the cocktail reception.</p></div>
      <div class="hk-day"><p class="kicker">Day 2 · Wed Oct 14 · morning</p>
        <ol class="hk-flow">
          <li><i class="hk-dur">about 30–40 min</i><b>Final build and rehearsal</b><span>one last fix, the agent fills the template, review and rehearse</span></li>
          <li><i class="hk-dur">about 20 min</i><b>01 Publications Brain</b><span>presents first, including a few questions</span></li>
          <li><i class="hk-dur">about 20 min</i><b>02 Insights Engine</b><span>presents second</span></li>
          <li><i class="hk-dur">about 20 min</i><b>03 Congress Monitor</b><span>presents third</span></li>
          <li><i class="hk-dur">about 20 min</i><b>04 Field Intelligence Engine</b><span>presents fourth, then the WPP demo</span></li>
        </ol>
        <p class="hk-aside">Each talk tells one story: problem, workflow redesign, human gates, a live swarm demo, impact. <a href="#final-presentation">Final presentation template ↓</a></p></div>
    </div>

    <h2 class="hk-h2">Pick your vertical</h2>
    <div class="hk-cards">{cards}</div>
    {teams_block()}

    <div class="hk-rules"><p class="kicker">Rules of the hack</p><ol>
      <li><b>Practice data only.</b> Fictional Nordvant Biopharma, or your own non-confidential data. Never patient or confidential data. <a href="/data">Data →</a></li>
      <li><b>Human at the helm, AI in the loop.</b> A person reviews and decides at every gate.</li>
      <li><b>Ship something that works.</b> Prototype fast. Harden later.</li></ol>
      <p>Start with <a href="/grokbot">Grok Bot setup</a> · browse <a href="/missions">missions</a> · build a missing skill with the <a href="/optimizer">Skill creator</a> · agents: <a href="/agents.md">/agents.md</a></p></div>
  </div>
</section>
''' + final_block() + downloads_block()


def vertical_page(v):
    n, slug, md, name, line, slot = v
    t = (FILES / md).read_text(encoding="utf-8")
    t = re.sub(r"\A# .*\n+(\*\*AI in Action.*\n+)?", "", t)
    assumption = ""
    m = re.match(r"> \*\*Assumption:\*\*(.*)\n+", t)
    if m:
        assumption = m.group(1).strip(); t = t[m.end():]
    parts = re.split(r"(?m)^(?=## )", t)
    main, fac = [], []
    for p in parts:
        if not p.strip():
            continue
        head = p.split("\n", 1)[0].lower()
        if "practice data" in head and head.startswith("## "):
            p = p.replace("\n", "\n\nGet direct links for any of these files on the [Data page](/data) (Copy link or Copy for Grok Bot).\n", 1)
        (fac if any(k in head for k in FACILITATOR) else main).append(p)
    pre = f"hk{n}"
    body = mdlite.render("\n".join(main), link, pre)
    facil = mdlite.render("\n".join(fac), link, pre + "f")
    d1 = re.search(r'<h2 id="(' + pre + r'-day-1[^"]*)"', body)
    day1 = d1.group(1) if d1 else ""
    prev_ = VERTICALS[n - 2] if n > 1 else None
    next_ = VERTICALS[n] if n < 4 else None
    nav = (f'<nav class="pager wrap" aria-label="Other verticals">' +
           (f'<a class="pg-prev" href="/hackathon/{prev_[1]}"><span>Previous vertical</span>0{prev_[0]} {E(prev_[3])}</a>' if prev_ else '<a class="pg-prev" href="/hackathon"><span>Back to</span>Hackathon</a>') +
           (f'<a class="pg-next" href="/hackathon/{next_[1]}"><span>Next vertical</span>0{next_[0]} {E(next_[3])}</a>' if next_ else '<a class="pg-next" href="/hackathon#final-presentation"><span>Next</span>Final presentation</a>') + "</nav>\n")
    return f'''<section class="section hk-v hk-v--{n}" id="hackathon-{slug}" aria-labelledby="hkv-h">
  <div class="wrap hk-v-wrap">
    <p class="hk-crumb"><a href="/hackathon">Hackathon</a> / Vertical 0{n}</p>
    <div class="sec-head"><p class="kicker">Vertical 0{n} · presents {["first", "second", "third", "fourth"][n - 1]} on Day 2</p><h1 class="md-h" id="hkv-h">{E(name)}</h1><p class="sec-sub">{E(line)}</p>{f'<p class="hk-facil">Facilitators: <b>{E(FACIL[n])}</b>, insights pillar leads</p>' if n in FACIL else ''}{f'<p class="hk-facil">Team {TEAMS[n][0]}: {E(", ".join(TEAMS[n][1]))} · <a href="/hackathon/teams#team-{TEAMS[n][0]}">Team map →</a></p>' if n in TEAMS else ''}
      <div class="hk-btns">{guide_btn(v)}<a class="btn-ghost" href="#{day1}">Day 1 agenda</a><a class="btn-ghost" href="/hackathon#final-presentation">Final presentation</a><a class="btn-ghost" href="#for-facilitators">For facilitators</a><a class="btn-ghost" href="{F(md)}">Markdown</a></div>
      {f'<p class="hk-aside"><b>Assumption:</b> {E(assumption)}</p>' if assumption else ""}</div>
    <div class="hk-md">{body}</div>
    <section class="hk-fac" id="for-facilitators" aria-labelledby="hkf-h"><p class="kicker">For facilitators</p><h2 id="hkf-h">Walk-around questions and unblocks</h2>
      <p class="hk-aside">There is no formal share-out on Day 1, so these questions are the feedback loop. Ask one or two per visit, then leave.</p>
      <div class="hk-md">{facil}</div></section>
  </div>
</section>
''' + nav


def pages():
    """[(path, title, description, html)]"""
    if not available():
        return []
    out = [("hackathon", "Hackathon", "Hack the workflow: the two-day plan, four verticals, final presentation template and downloads.", hub())]
    if TEAMS:
        out.append(("hackathon/teams", "Teams · Hackathon", "Hackathon team map: four teams, each listed under its Medical Affairs vertical, with the team map deck to download.", teams_page()))
    for v in VERTICALS:
        out.append((f"hackathon/{v[1]}", f"0{v[0]} {v[3]} · Hackathon", f"Hackathon guide for {v[3]}: agenda, missions, data, AI ideas, swarm shape, human gates, prompts, impact worksheet, facilitator notes.", vertical_page(v)))
    return out
