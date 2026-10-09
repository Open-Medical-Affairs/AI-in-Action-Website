"""Render mission graphs (data/mission-graphs.json) to inline SVG at build time. Standard library only."""
import html, json, textwrap

E = lambda s: html.escape(str(s), quote=True)
NAVY, TEAL, TEAL_SOFT, ORANGE, INK2, MUTED = "#0B2545", "#0E9AA7", "#E3F5F3", "#E07A2F", "#2B4262", "#5B6E86"
POD = {"Strategy & Evidence": "#0E9AA7", "Narrative & Communication": "#3B82C4", "External Engagement": "#14B8A6",
       "Answer & Protect": "#E07A2F", "Measure & Govern": "#13315C", "Independent": "#8A5CF6", "The coordinator": NAVY}


def wrap(s, n, maxl=3):
    lines = textwrap.wrap(str(s), n) or [""]
    if len(lines) > maxl:
        lines = lines[:maxl]; lines[-1] = lines[-1][: n - 1].rstrip() + "…"
    return lines


def text(x, y, lines, size=13, weight=500, fill=NAVY, anchor="middle", lh=None, mono=False, cls=""):
    lh = lh or size * 1.3
    fam = ' font-family="var(--f-mono)"' if mono else ""
    c = f' class="{cls}"' if cls else ""
    spans = "".join(f'<tspan x="{x:.0f}" dy="{0 if i == 0 else lh:.1f}">{E(l)}</tspan>' for i, l in enumerate(lines))
    return f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{fam}{c}>{spans}</text>'


def arrow(x1, y1, x2, y2, color=TEAL, dash=False, width=1.6, marker="a-teal", curve=True):
    d = f"M{x1:.0f},{y1:.0f} C{x1:.0f},{(y1 + y2) / 2:.0f} {x2:.0f},{(y1 + y2) / 2:.0f} {x2:.0f},{y2:.0f}" if curve else f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}"
    da = ' stroke-dasharray="5 5"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{da} marker-end="url(#{marker})"/>'


def defs(uid):
    return (f'<defs><marker id="a-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{TEAL}"/></marker>'
            f'<marker id="a-orange" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ORANGE}"/></marker>'
            f'<marker id="a-navy" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{NAVY}"/></marker>'
            f'<linearGradient id="g-lead-{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#13315C"/><stop offset="1" stop-color="{NAVY}"/></linearGradient></defs>')


def chips_band(x, y, w, title, items, fill, stroke, ink, cls):
    """A labelled band of chips; returns (svg, height)."""
    out, cx, cy, rowh = [], x + 18, y + 40, 28
    for it in items:
        cw = min(len(it) * 6.6 + 22, w - 36)
        if cx + cw > x + w - 18:
            cx, cy = x + 18, cy + rowh + 6
        out.append(f'<rect x="{cx:.0f}" y="{cy:.0f}" width="{cw:.0f}" height="{rowh}" rx="14" fill="#fff" stroke="{stroke}" stroke-opacity=".5"/>')
        label = it if len(it) * 6.6 + 22 <= w - 36 else it[: int((w - 60) / 6.6)] + "…"
        out.append(text(cx + cw / 2, cy + 18.5, [label], 11.5, 500, ink, mono=cls == "in"))
        cx += cw + 8
    h = cy + rowh + 16 - y
    band = f'<rect x="{x}" y="{y}" width="{w}" height="{h:.0f}" rx="18" fill="{fill}" stroke="{stroke}" stroke-opacity=".35"/>'
    head = text(x + 18, y + 25, [title], 11, 700, ink, anchor="start", cls="g-cap")
    return f'<g class="g-band g-band--{cls}">{band}{head}{"".join(out)}</g>', h


def gate(cx, y, w, label, detail):
    h = 38
    return (f'<g class="g-gate" tabindex="0" role="button" aria-label="Human checkpoint: {E(label)}. {E(detail)}" data-gate="{E(label)}" data-detail="{E(detail)}">'
            f'<title>{E(detail)}</title>'
            f'<rect x="{cx - w / 2:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="19" fill="#FFF4EB" stroke="{ORANGE}" stroke-width="1.6"/>'
            f'<path transform="translate({cx - w / 2 + 22:.0f},{y + 19}) rotate(45)" d="M-6,-6 h12 v12 h-12z" fill="{ORANGE}"/>'
            + text(cx + 10, y + 24, [label], 13, 650, "#9A4A12") + "</g>"), h


def node(x, y, w, h, nid, kicker, title, sub, kind="worker", color=TEAL):
    fill = f"url(#g-lead-{nid.split('|')[0]})" if kind == "lead" else "#fff"
    ink = "#fff" if kind == "lead" else NAVY
    kink = "#8FE3DA" if kind == "lead" else color
    stroke = "none" if kind == "lead" else color
    parts = [f'<g class="gnode gnode--{kind}" tabindex="0" role="button" data-node="{E(nid)}" aria-label="{E(kicker)}: {E(title)}. Show details">',
             f'<rect class="gn-bg" x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>']
    if kind != "lead":
        parts.append(f'<rect x="{x:.0f}" y="{y + 12:.0f}" width="4" height="{h - 24:.0f}" rx="2" fill="{color}"/>')
    kk = kicker.upper(); ks = 9.5 if len(kk) * 6.6 < w - 14 else 8
    if len(kk) * (ks * .66) > w - 14: kk = kk[: int((w - 14) / (ks * .66)) - 1] + "…"
    parts.append(text(x + w / 2, y + 20, [kk], ks, 700, kink, cls="g-cap"))
    tl = wrap(title, max(10, int(w / 7.6)), 2)
    parts.append(text(x + w / 2, y + 39, tl, 13.5 if kind == "lead" else 12.5, 650, ink))
    if sub:
        parts.append(text(x + w / 2, y + 39 + 16 * len(tl) + 2, wrap(sub, max(10, int(w / 6.6)), 1), 10.5, 400, "#BFD7E8" if kind == "lead" else MUTED, mono=True))
    parts.append("</g>")
    return "".join(parts)


def pill(x, y, nid, label):
    w = len(label) * 6.2 + 22
    return (f'<g class="gnode gnode--support" tabindex="0" role="button" data-node="{E(nid)}" aria-label="Also loads {E(label)}. Show details">'
            f'<rect class="gn-bg" x="{x - w / 2:.0f}" y="{y}" width="{w:.0f}" height="24" rx="12" fill="#F9FBFB" stroke="{MUTED}" stroke-opacity=".45" stroke-dasharray="3 3"/>'
            + text(x, y + 16, [label], 10.5, 500, INK2, mono=True) + "</g>"), w


def render_team(g, S, uid, show_support=True):
    W, P = 980, 20
    out, nodes, y = [], {}, P
    cx = W / 2
    band, h = chips_band(P, y, W - 2 * P, f"DATA IN · {len(g['inputs'])} SYNTHETIC FILES (any therapy pack)", g["inputs"], "#EEF3F3", NAVY, NAVY, "in")
    out.append(band); y += h
    out.append(arrow(cx, y, cx, y + 26, NAVY, marker="a-navy", curve=False)); y += 28
    gs, gh = gate(cx, y, 300, g["gates"][0]["label"], g["gates"][0]["detail"]); out.append(gs); y += gh
    out.append(arrow(cx, y, cx, y + 26, NAVY, marker="a-navy", curve=False)); y += 28
    ms = g["skills"]; lead = ms[0]; workers = ms[1:]
    LW, LH = 330, 82
    out.append(node(cx - LW / 2, y, LW, LH, f"{uid}|{lead}", "Lead · coordinator" if workers else "Lead skill", lead, S[lead]["tier"] + " skill", "lead"))
    nodes[f"{uid}|{lead}"] = {"kicker": "Lead skill", "skills": [lead]}
    lead_y = y; y += LH
    pos = {lead: (cx, lead_y, LH)}
    sup_owner = {}
    for s in (ms if show_support else []):
        for r in S[s]["requires"]:
            if r != "medical-affairs-foundations" and r not in ms:
                sup_owner.setdefault(s, []).append(r)
    bottom_nodes = [lead]
    if workers:
        n = len(workers); gap = 22
        ww = min(250, (W - 2 * P - gap * (n - 1)) / n)
        tot = n * ww + gap * (n - 1); x0 = cx - tot / 2
        wy = y + 74
        for i, s in enumerate(workers):
            x = x0 + i * (ww + gap)
            rel = next((h for h in g["handoffs"] if h["from"] == lead and h["to"] == s), None)
            out.append(arrow(cx, y, x + ww / 2, wy - 2, ORANGE if rel else TEAL, dash=bool(rel), marker="a-orange" if rel else "a-teal"))
            out.append(node(x, wy, ww, 82, f"{uid}|{s}", f"Sub-worker {i + 1}", s, S[s]["tier"] + " skill", "worker", TEAL))
            nodes[f"{uid}|{s}"] = {"kicker": f"Sub-worker {i + 1}", "skills": [s]}
            pos[s] = (x + ww / 2, wy, 82)
        mid = y + 30
        out.append(f'<rect x="{cx + 8:.0f}" y="{mid - 9:.0f}" width="182" height="18" rx="9" fill="#F6F8F8"/>')
        out.append(text(cx + 16, mid + 4, ["delegates with a context packet"], 10.5, 500, TEAL, anchor="start", cls="g-cap g-edge-lbl"))
        y = wy + 82
        bottom_nodes = workers
        # worker → worker hand-offs
        for h in g["handoffs"]:
            if h["from"] in workers and h["to"] in workers:
                (x1, y1, h1), (x2, y2, h2) = pos[h["from"]], pos[h["to"]]
                yy = y1 + h1
                out.append(f'<path d="M{x1:.0f},{yy:.0f} C{x1:.0f},{yy + 38:.0f} {x2:.0f},{yy + 38:.0f} {x2:.0f},{yy + 4:.0f}" fill="none" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="5 5" marker-end="url(#a-orange)"/>')
                out.append(text((x1 + x2) / 2, yy + 46, ["hands off"], 10, 600, ORANGE, cls="g-cap"))
    # support pills (requires) beneath their owners
    sy = y + 16
    maxrows = 0
    for s in bottom_nodes + ([] if not workers else [lead]):
        reqs = sup_owner.get(s, [])
        if not reqs:
            continue
        px, py, ph = pos[s]
        if s == lead and workers:
            # lead's own requires go beside it
            for j, r in enumerate(reqs[:3]):
                pw = len(r) * 6.2 + 22
                ps, _ = pill(px + LW / 2 + 22 + pw / 2, py + 4 + j * 28, f"{uid}|{r}", r)
                out.append(f'<path d="M{px + LW / 2:.0f},{py + LH / 2:.0f} L{px + LW / 2 + 18:.0f},{py + 16 + j * 28:.0f}" stroke="{MUTED}" stroke-opacity=".5" stroke-dasharray="2 3"/>')
                out.append(ps); nodes[f"{uid}|{r}"] = {"kicker": f"Loaded by {s}", "skills": [r]}
            continue
        for j, r in enumerate(reqs[:3]):
            ps, _ = pill(px, sy + 22 + j * 30, f"{uid}|{r}", r)
            out.append(ps); nodes[f"{uid}|{r}"] = {"kicker": f"Loaded by {s}", "skills": [r]}
        out.append(f'<path d="M{px:.0f},{py + ph:.0f} L{px:.0f},{sy + 22:.0f}" stroke="{MUTED}" stroke-opacity=".5" stroke-dasharray="2 3"/>')
        out.append(text(px + 6, sy + 14, ["loads"], 9.5, 600, MUTED, anchor="start", cls="g-cap"))
        maxrows = max(maxrows, min(3, len(reqs)))
    if maxrows:
        y = sy + 22 + maxrows * 30 + 4
    else:
        y += 12 if not workers else 40
    # challenge
    ry = y + 30
    for s in bottom_nodes:
        px = pos[s][0]
        out.append(arrow(px, y - (0 if maxrows else 0), cx, ry - 2, TEAL))
    RW = 330
    out.append(node(cx - RW / 2, ry, RW, 70, f"{uid}|{g['reviewer']}", "Challenge · independent check", g["reviewer"], "", "review", "#8A5CF6"))
    nodes[f"{uid}|{g['reviewer']}"] = {"kicker": "Challenge step (AGENTS.md step 5)", "skills": [g["reviewer"]]}
    y = ry + 70
    for gt in g["gates"][1:]:
        out.append(arrow(cx, y, cx, y + 26, NAVY, marker="a-navy", curve=False)); y += 28
        gs, gh = gate(cx, y, 320, gt["label"], gt["detail"]); out.append(gs); y += gh
    out.append(arrow(cx, y, cx, y + 26, NAVY, marker="a-navy", curve=False)); y += 28
    band, h = chips_band(P, y, W - 2 * P, "DELIVERABLES OUT · DRAFTS FOR HUMAN REVIEW", g["deliverables"], TEAL_SOFT, TEAL, "#0A7480", "out")
    out.append(band); y += h + 14
    fid = f"{uid}|medical-affairs-foundations"
    out.append(f'<g class="gnode gnode--foundation" tabindex="0" role="button" data-node="{fid}" aria-label="Foundation skill loaded by every worker. Show details">'
               f'<rect class="gn-bg" x="{P}" y="{y}" width="{W - 2 * P}" height="34" rx="10" fill="{NAVY}" fill-opacity=".05" stroke="{NAVY}" stroke-opacity=".15"/>'
               + text(cx, y + 22, ["FOUNDATION · every worker loads  medical-affairs-foundations  (house rules, safety scan, provenance)"], 11, 600, INK2, cls="g-cap") + "</g>")
    nodes[fid] = {"kicker": "Always loaded", "skills": ["medical-affairs-foundations"]}
    y += 34 + P
    return wrap_svg(uid, W, y, out, g), nodes


def render_swarm(g, S, uid):
    W, P, LBL = 1060, 20, 168
    out, nodes, y = [], {}, P
    cx = W / 2
    band, h = chips_band(P, y, W - 2 * P, f"DATA IN · {len(g['inputs'])} SYNTHETIC FILES (any therapy pack) · each worker gets only its slice", g["inputs"], "#EEF3F3", NAVY, NAVY, "in")
    out.append(band); y += h
    out.append(arrow(cx, y, cx, y + 24, NAVY, marker="a-navy", curve=False)); y += 26
    gs, gh = gate(cx, y, 300, g["gates"][0]["label"], g["gates"][0]["detail"]); out.append(gs); y += gh
    out.append(arrow(cx, y, cx, y + 24, NAVY, marker="a-navy", curve=False)); y += 26
    # human director
    HW = 420
    out.append(f'<g class="g-human"><rect x="{cx - HW / 2:.0f}" y="{y}" width="{HW}" height="50" rx="25" fill="#FFF4EB" stroke="{ORANGE}" stroke-width="1.6"/>'
               + text(cx, y + 21, ["HUMAN · FINAL JUDGE"], 9.5, 700, ORANGE, cls="g-cap") + text(cx, y + 39, ["Launch Medical Director"], 13.5, 650, "#9A4A12") + "</g>")
    y += 50
    roles = {w["role"]: w for w in g["workers"]}
    pos = {}
    lane_x0 = P + LBL
    for wv in g["waves"]:
        if wv["kind"] == "gate":
            y += 18
            gw = W - 2 * P
            out.append(f'<g class="g-gate" tabindex="0" role="button" aria-label="{E(wv["label"])}: {E(wv["who"])}. {E(wv["why"])}" data-gate="{E(wv["label"])}" data-detail="{E(wv["who"] + ". " + wv["why"])}">'
                       f'<rect x="{P}" y="{y}" width="{gw}" height="44" rx="22" fill="#FFF4EB" stroke="{ORANGE}" stroke-width="1.6"/>'
                       f'<path transform="translate({P + 28},{y + 22}) rotate(45)" d="M-7,-7 h14 v14 h-14z" fill="{ORANGE}"/>'
                       + text(P + 50, y + 27, [f"{wv['label'].upper()} · {wv['who']}"], 13, 700, "#9A4A12", anchor="start")
                       + text(W - P - 20, y + 27, [wv["why"]], 11, 500, "#9A4A12", anchor="end") + "</g>")
            y += 44
            continue
        members = wv["members"]
        per = 5
        rows = [members[i:i + per] for i in range(0, len(members), per)]
        y += 22
        lane_h = len(rows) * 96 + (len(rows) - 1) * 14 + 24
        out.append(f'<rect x="{P}" y="{y}" width="{W - 2 * P}" height="{lane_h}" rx="18" fill="#FFFFFF" stroke="{NAVY}" stroke-opacity=".08"/>')
        out.append(text(P + 18, y + 30, [wv["label"].upper()], 12, 750, TEAL, anchor="start", cls="g-cap"))
        out.append(text(P + 18, y + 50, wrap(wv["why"], 24, 4), 10.5, 450, MUTED, anchor="start"))
        ry = y + 12
        for row in rows:
            n = len(row); gap = 14
            ww = min(200, (W - lane_x0 - P - 12 - gap * (n - 1)) / n)
            tot = n * ww + gap * (n - 1); x0 = lane_x0 + (W - lane_x0 - P - 12 - tot) / 2
            for i, role in enumerate(row):
                w = roles.get(role)
                if role == g.get("lead_role"):
                    sk = [g["lead"]]; kind, color, pod = "lead", NAVY, "The coordinator"
                else:
                    sk = w["skills"] if w else []; pod = w["pod"] if w else ""
                    kind, color = ("review" if pod == "Independent" else "worker"), POD.get(pod, TEAL)
                x = x0 + i * (ww + gap)
                nid = f"{uid}|{role}"
                out.append(node(x, ry, ww, 96, nid, pod or "Worker", role, sk[0] if sk else "", kind, color))
                if len(sk) > 1:
                    out.append(text(x + ww / 2, ry + 86, [f"+ {len(sk) - 1} more skill{'s' if len(sk) > 2 else ''}"], 9.5, 600, color if kind != "lead" else "#8FE3DA", cls="g-cap"))
                nodes[nid] = {"kicker": f"{wv['label']} · {pod}", "role": role, "skills": sk,
                              "context": (w or {}).get("context", ""), "consumes": (w or {}).get("consumes", [])}
                pos[role] = (x + ww / 2, ry, 96)
            ry += 96 + 14
        y += lane_h
    # hand-offs: dashed orange arcs from producer bottom to consumer top
    for h in g["handoffs"]:
        if h["from"] not in pos or h["to"] not in pos or h["from"] == g.get("lead_role"):
            continue
        (x1, y1, h1), (x2, y2, _) = pos[h["from"]], pos[h["to"]]
        if y2 <= y1:
            continue
        out.append(f'<path class="g-hand" d="M{x1:.0f},{y1 + h1:.0f} C{x1:.0f},{y1 + h1 + 60:.0f} {x2:.0f},{y2 - 60:.0f} {x2:.0f},{y2 - 2:.0f}" fill="none" stroke="{ORANGE}" stroke-width="1.5" stroke-dasharray="5 5" stroke-opacity=".8" marker-end="url(#a-orange)"/>')
    y += 14
    out.append(arrow(cx, y, cx, y + 24, NAVY, marker="a-navy", curve=False)); y += 26
    band, h = chips_band(P, y, W - 2 * P, "DELIVERABLES OUT · DRAFTS FOR HUMAN DECISION", g["deliverables"], TEAL_SOFT, TEAL, "#0A7480", "out")
    out.append(band); y += h + 14
    fid = f"{uid}|medical-affairs-foundations"
    out.append(f'<g class="gnode gnode--foundation" tabindex="0" role="button" data-node="{fid}" aria-label="Foundation skill loaded by every worker. Show details">'
               f'<rect class="gn-bg" x="{P}" y="{y}" width="{W - 2 * P}" height="34" rx="10" fill="{NAVY}" fill-opacity=".05" stroke="{NAVY}" stroke-opacity=".15"/>'
               + text(cx, y + 22, ["FOUNDATION · every worker loads  medical-affairs-foundations  + its skills' requires · dashed orange = hand-off of an upstream output"], 11, 600, INK2, cls="g-cap") + "</g>")
    nodes[fid] = {"kicker": "Always loaded", "skills": ["medical-affairs-foundations"]}
    y += 34 + P
    return wrap_svg(uid, W, y, out, g), nodes


def wrap_svg(uid, W, H, parts, g):
    return (f'<svg class="mgraph" viewBox="0 0 {W} {H:.0f}" width="{W}" height="{H:.0f}" role="group" aria-label="Org chart for mission {E(g["title"])}: lead skill, sub-workers, hand-offs, human checkpoints, data in and deliverables out" xmlns="http://www.w3.org/2000/svg">'
            + defs(uid) + "".join(parts) + "</svg>")


def render(g, S, show_support=True):
    uid = g["id"]
    return render_swarm(g, S, uid) if g["structure"] == "swarm" else render_team(g, S, uid, show_support)


def mini(g):
    """Small abstract version for cards: data → gate → lead → workers → review → gate → out."""
    W, H = 300, 150
    o = [f'<svg class="mmini" viewBox="0 0 {W} {H}" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">']
    o.append(f'<rect x="20" y="8" width="260" height="14" rx="7" fill="#EEF3F3" stroke="{NAVY}" stroke-opacity=".15"/>')
    o.append(f'<path transform="translate(150,34) rotate(45)" d="M-5,-5 h10 v10 h-10z" fill="{ORANGE}"/>')
    o.append(f'<rect x="110" y="46" width="80" height="20" rx="6" fill="{NAVY}"/>')
    if g["structure"] == "swarm":
        groups = [w for w in g["waves"]]
        yy = 72
        for wv in groups[1:]:
            if wv["kind"] == "gate":
                o.append(f'<rect x="40" y="{yy}" width="220" height="5" rx="2.5" fill="{ORANGE}"/>'); yy += 9; continue
            n = len(wv["members"]); bw = min(34, 220 / n - 4); x0 = 150 - (n * (bw + 4) - 4) / 2
            for i in range(n):
                o.append(f'<rect x="{x0 + i * (bw + 4):.1f}" y="{yy}" width="{bw:.1f}" height="10" rx="3" fill="{TEAL if wv["label"] != "Wave 4" else "#8A5CF6"}" fill-opacity=".85"/>')
            o.append(f'<path d="M150,{yy - 4} L150,{yy}" stroke="{TEAL}"/>'); yy += 15
        o.append(f'<rect x="20" y="{min(yy + 2, 136)}" width="260" height="12" rx="6" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-opacity=".4"/>')
    else:
        ws = g["skills"][1:]; n = len(ws)
        if n:
            bw = min(70, 240 / n - 8); x0 = 150 - (n * (bw + 8) - 8) / 2
            for i in range(n):
                x = x0 + i * (bw + 8)
                o.append(f'<path d="M150,66 C150,76 {x + bw / 2:.0f},74 {x + bw / 2:.0f},84" fill="none" stroke="{TEAL}" stroke-width="1.4"/>')
                o.append(f'<rect x="{x:.1f}" y="84" width="{bw:.1f}" height="18" rx="5" fill="#fff" stroke="{TEAL}" stroke-width="1.4"/>')
        else:
            sup = len([r for r in g["support"]][:3])
            for i in range(sup):
                o.append(f'<rect x="{150 - (sup * 54 - 8) / 2 + i * 54:.0f}" y="86" width="46" height="12" rx="6" fill="#F9FBFB" stroke="{MUTED}" stroke-dasharray="2 2"/>')
        o.append(f'<rect x="115" y="110" width="70" height="12" rx="6" fill="#fff" stroke="#8A5CF6"/>')
        o.append(f'<path transform="translate(150,{128}) rotate(45)" d="M-4,-4 h8 v8 h-8z" fill="{ORANGE}"/>')
        o.append(f'<rect x="20" y="136" width="260" height="10" rx="5" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-opacity=".4"/>')
    o.append("</svg>")
    return "".join(o)


def panel_data(nodes, S):
    used = {s for n in nodes.values() for s in n["skills"]}
    return json.dumps({"nodes": nodes, "skills": {k: {kk: S[k][kk] for kk in ("summary", "tier", "url", "requires")} for k in used if k in S}}, ensure_ascii=False).replace("</", "<\\/")
