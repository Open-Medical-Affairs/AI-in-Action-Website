#!/usr/bin/env python3
"""Build the AI in Action companion site.

  python3 build.py                                    # re-render from data/content.json + site.config.json
  python3 build.py --repo ../Medical-Affairs-Skills   # re-extract content from a repo checkout first

Pure standard library. Emits static files only (index.html, agents.md, llms.txt,
missions.json, datasets.json, skills.json, prompts.json). Host the folder as-is.
"""
import argparse, csv, html, json, re, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAS = [
    {"id": "oncology-mm", "short": "Oncology", "area": "Relapsed/refractory multiple myeloma", "product": "NORVANTIB"},
    {"id": "immunology-ad", "short": "Immunology", "area": "Moderate-to-severe atopic dermatitis", "product": "DERMALYX"},
    {"id": "cardiometabolic-obesity", "short": "Cardiometabolic", "area": "Obesity", "product": "ADIPOSYN"},
]
TA_BY_ID = {t["id"]: t for t in TAS}

# Plain-language grouping of the 31 per-area pack files (same schema in every area).
PACK_GROUPS = [
    ("field", "Field, experts & conversations", ["field-observations.csv", "interaction-notes.md", "kol-dossiers.md", "field-account-plan.csv", "advisory-board-transcript.md"]),
    ("evidence", "Product, evidence & science", ["product-profile.md", "evidence-landscape.md", "structured-evidence-table.csv", "patient-level-analysis.csv", "congress-abstracts.md", "competitor-announcements.md", "guideline-landscape.md", "manuscript-draft.md", "abstract-poster-brief.md", "plain-language-source.md"]),
    ("plans", "Plans, budgets & strategy", ["medical-plan.md", "publication-plan.md", "integrated-evidence-plan.csv", "iis-proposal.md", "rwe-study-concept.md", "payer-hta-brief.md", "medical-education-needs.md", "launch-readiness-register.md", "medical-impact-metrics.csv", "scientific-platform-draft.md"]),
    ("review", "Medical information, safety & review", ["medical-information-enquiries.csv", "safety-case-series.md", "mlr-review-comments.md", "promotional-claims-review.md", "terminology-coding-queue.csv", "document-ingestion-challenge.md"]),
]
CONNECTED_DESC = {
    "accounts": "Institutions with capacity and scientific need",
    "hcps": "Fictional clinicians, channel preferences and permissions",
    "interactions": "Field interactions with verbatims and source links",
    "enquiries": "Medical information enquiries",
    "content_assets": "Content library with review status and due dates",
    "engagement": "Education engagement: invited, attended, pre/post scores",
    "patient_partnerships": "Patient organization inputs and quote permissions",
    "projects": "Evidence projects with cost, hours and dependencies",
    "access_log": "Institutional access routes and rules",
    "msl_tasks": "MSL task queue with owners and due dates",
    "source_links": "Source registry with file hashes",
}
TEAMS = [
    {"name": "Publications Brain", "blurb": "What to publish, what to stop, and keeping every output consistent.", "team_missions": ["mission-4"], "missions": ["publication"]},
    {"name": "Insights Engine", "blurb": "Turn a quarter of field records into decisions leadership can act on.", "team_missions": ["mission-2"], "missions": ["field-insights", "transcript"]},
    {"name": "Congress Monitor", "blurb": "The congress just ended. What changed, and what do we do about it?", "team_missions": ["mission-3"], "missions": ["congress"]},
    {"name": "Field Intelligence Engine", "blurb": "Walk into every HCP conversation prepared, and close the loop after.", "team_missions": ["mission-1"], "missions": ["msl-pre-call", "msl-post-call", "hcp-access", "msl-admin"]},
]

# ---------------------------------------------------------------- extraction

def first_h1(text):
    m = re.search(r"^# (.+)$", text, re.M)
    return m.group(1).strip() if m else ""

def code_blocks(text, lang="text"):
    return [b.strip("\n") for b in re.findall(r"```%s\n(.*?)```" % lang, text, re.S)]

def md_table_after(text, heading_regex):
    m = re.search(heading_regex, text, re.M)
    if not m:
        return []
    rows, started = [], False
    for line in text[m.start():].splitlines():
        if line.startswith("|"):
            started = True
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                continue
            rows.append(cells)
        elif started:
            break
    return rows[1:]

def clean_md(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return s.replace("**", "").replace("`", "").strip()

def quoted_bullets(text, heading):
    sec = text.split(heading)[1].split("\n## ")[0]
    return [l.strip()[3:].rstrip("”").strip() for l in sec.splitlines() if l.strip().startswith("- “")]

def data_sources_root(repo: Path) -> Path:
    """Open-Medical-Affairs/Data-Sources checkout: <repo>/Data-Sources, ../Data-Sources or $MA_DATA_SOURCES."""
    import os
    for c in ([Path(os.environ["MA_DATA_SOURCES"])] if os.environ.get("MA_DATA_SOURCES") else []) + [repo / "Data-Sources", repo.parent / "Data-Sources"]:
        if (c / "synthetic").is_dir():
            return c.resolve()
    raise SystemExit("Data-Sources checkout not found. Clone https://github.com/Open-Medical-Affairs/Data-Sources into the skills repo as Data-Sources/")

def extract(repo: Path):
    R = lambda p: (repo / p).read_text(encoding="utf-8")
    dsr = data_sources_root(repo)
    D = lambda p: (dsr / p).read_text(encoding="utf-8")
    readme, quick, runbook = R("README.md"), R("workshop/PARTICIPANT-QUICKSTART.md"), R("workshop/OCTOBER-RUNBOOK.md")
    catalog = json.loads(R("workshop/catalog.json"))
    try:
        commit = subprocess.check_output(["git", "-C", str(repo), "log", "-1", "--format=%h|%cs"], text=True).strip().split("|")
    except Exception:
        commit = ["", ""]
    c = {"source_commit": commit[0], "source_date": commit[1]}
    c["starter_prompt"] = code_blocks(readme)[0]
    c["quickstart_prompt"] = code_blocks(quick)[0]
    c["capstone_prompt"], c["change_prompt"] = code_blocks(runbook)[:2]
    c["msl_prompt"] = code_blocks(R("docs/msl-workflow.md"))[0]
    c["next_moves"] = quoted_bullets(quick, "## Your next move")
    c["recovery_prompts"] = quoted_bullets(runbook, "## Recovery prompts")
    sec = quick.split("## If something is missing")[1].split("\n## ")[0]
    c["if_missing"] = [clean_md(" ".join(x.split())) for x in re.split(r"\n- ", "\n" + sec.strip())[1:]]
    c["say_this"] = [{"ask": r[0].strip("“”\""), "prepares": r[1]} for r in md_table_after(readme, r"^## Choose what you want to accomplish")]
    hiw = readme.split("## How it works")[1].split("\n## ")[0].strip().split("\n\n")[0]
    steps = re.findall(r"^\d\. \*\*(.+?)\*\*(.*?)(?=^\d\. |\Z)", hiw, re.S | re.M)
    c["how_it_works"] = [{"title": a.strip(), "text": clean_md(" ".join(b.split()))} for a, b in steps]
    c["missions"] = [{k: m[k] for k in ("id", "title", "objective", "inputs", "skills", "deliverables")} for m in catalog["missions"]]
    c["default_mission"], c["default_ta"] = catalog["default_mission"], catalog["default_ta"]

    tm = []
    for f in sorted((repo / "workshop/missions").glob("mission-*.md")):
        t = f.read_text(encoding="utf-8")
        h2 = re.search(r"^## (.+)$", t, re.M).group(1)
        emoji, headline = h2.split(" ", 1)
        quote = " ".join(l.lstrip(">").strip() for l in re.search(r"((?:^>.*\n)+)", t, re.M).group(1).splitlines())
        quote = quote.replace("**Your mission:**", "").strip()
        have = re.findall(r"^- `([^`]+)` — (.+)$", t, re.M)
        done = t.split('## What "done" looks like')[1].split("\n## ")[0].strip()
        push_sec = t.split("## When it finishes, push on it")[1].split("\n## ")[0]
        pushes = [" ".join(p.replace("\n>", " ").split()) for p in re.findall(r"\*[\"“](.+?)[\"”]\*", push_sec, re.S)]
        think = re.search(r"Think about: (.+?)(?:\n\n|\Z)", t, re.S)
        tm.append({"id": f.stem, "number": int(f.stem.split("-")[1]), "function": first_h1(t).split("—", 1)[1].strip(),
                   "emoji": emoji, "headline": headline.strip(), "mission": quote,
                   "inputs": [{"file": a, "what": b} for a, b in have],
                   "done": clean_md(" ".join(done.split())), "timebox": re.search(r"## Timebox\s+(.+)", t).group(1).strip().rstrip("."),
                   "push": pushes, "house_rules_file": re.search(r"Your file is `([^`]+)`", t).group(1),
                   "think_about": " ".join(think.group(1).split()) if think else "", "path": f"workshop/missions/{f.name}"})
    c["team_missions"] = tm

    cards = []
    for r in md_table_after(R("workshop/change-cards/README.md"), r"^\| Card"):
        mm = re.match(r"\[(.+?)\]\((.+?)\)", r[0])
        p = "workshop/change-cards/" + mm.group(2)
        cards.append({"title": mm.group(1), "path": p, "works_with": r[1], "request": r[2], "headline": first_h1(R(p))})
    c["change_cards"] = cards

    groups = []
    for sec in re.split(r"^## ", R("SKILLS-INDEX.md"), flags=re.M)[1:]:
        title = sec.splitlines()[0].strip()
        rows = []
        for line in sec.splitlines():
            m = re.match(r"\| \[`([^`]+)`\]\(([^)]+)\) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$", line)
            if m:
                first = re.split(r"(?<=[.!?])\s", m.group(3), maxsplit=1)[0]
                rows.append({"name": m.group(1), "path": m.group(2), "summary": first, "produces": m.group(6).strip(" —"),
                             "requires": re.findall(r"`([^`]+)`", m.group(4)), "house_rules": f"house-rules/{m.group(1)}.md"})
        if rows:
            intro = re.sub(r"\s+", " ", sec.split("\n", 1)[1].split("|")[0]).strip()
            groups.append({"title": title, "intro": clean_md(intro), "skills": rows})
    c["skill_groups"] = groups
    c["skill_count"] = sum(len(g["skills"]) for g in groups)

    ds = []
    for ta in TAS:
        d = dsr / "synthetic" / ta["id"]
        desc_tbl = {r[0].strip("`"): r[1] for r in md_table_after(D(f"synthetic/{ta['id']}/README.md"), r"^## What's in here")}
        cats = []
        for cid, ctitle, names in PACK_GROUPS:
            files = []
            for n in names:
                p = d / n
                if not p.exists():
                    continue
                rec = {"name": n, "path": f"Data-Sources/synthetic/{ta['id']}/{n}", "format": n.rsplit(".", 1)[1].upper()}
                if n.endswith(".md"):
                    h = re.sub(r"\s+—\s+(Oncology|Immunology|Cardiometabolic).*$", "", first_h1(p.read_text(encoding="utf-8")))
                    rec["title"] = desc_tbl.get(n) or h
                else:
                    with p.open(encoding="utf-8") as fh:
                        rows_ = list(csv.reader(l for l in fh if not l.startswith("#")))
                    rec["rows"] = max(len(rows_) - 1, 0)
                    rec["columns"] = rows_[0] if rows_ else []
                    rec["title"] = desc_tbl.get(n) or n.rsplit(".", 1)[0].replace("-", " ").capitalize()
                files.append(rec)
            cats.append({"id": cid, "title": ctitle, "files": files})
        listed = {f["name"] for cc in cats for f in cc["files"]}
        extra = sorted(x.name for x in d.iterdir() if x.name not in listed and x.name != "README.md")
        assert not extra, f"unclassified files in {ta['id']}: {extra}"
        ds.append({"id": f"pack-{ta['id']}", "kind": "therapeutic-area-pack", "ta": ta["id"], "title": f"{ta['short']} pack",
                   "subtitle": f"{ta['area']} · fictional product {ta['product']}", "synthetic": True,
                   "readme": f"Data-Sources/synthetic/{ta['id']}/README.md", "folder": f"Data-Sources/synthetic/{ta['id']}/",
                   "count": sum(len(cc["files"]) for cc in cats), "categories": cats})

    dd = json.loads(D("synthetic/connected/data-dictionary.json"))
    cf = [{"name": f"{n}.csv", "path": f"Data-Sources/synthetic/connected/{n}.csv", "format": "CSV", "rows": t["rows"], "columns": t["columns"],
           "title": CONNECTED_DESC.get(n, n.replace("_", " ").capitalize())} for n, t in dd["tables"].items()]
    cf += [{"name": "medical-affairs.sqlite", "path": "Data-Sources/synthetic/connected/medical-affairs.sqlite", "format": "SQLite", "title": "All tables in one database file (no server or login needed)"},
           {"name": "data-dictionary.json", "path": "Data-Sources/synthetic/connected/data-dictionary.json", "format": "JSON", "title": "Fields, joins and row counts"}]
    ds.append({"id": "connected-organization", "kind": "practice-organization", "ta": "all", "title": "Connected practice organization",
               "subtitle": f"A fictional CRM and content library across all three areas · scenario date {dd.get('scenario_date', '')}", "synthetic": True,
               "readme": "Data-Sources/synthetic/connected/README.md", "folder": "Data-Sources/synthetic/connected/", "count": len(cf),
               "categories": [{"id": "tables", "title": "Tables", "files": cf}]})
    pe = []
    for ta in TAS:
        j = json.loads(D(f"public/evidence-snapshots/{ta['id']}.json"))
        pe.append({"name": f"{ta['id']}.json", "path": f"Data-Sources/public/evidence-snapshots/{ta['id']}.json", "format": "JSON", "rows": len(j.get("records", [])),
                   "title": f"{ta['short']}: real bibliographic examples (retrieved {str(j.get('retrieved_at', ''))[:10]})"})
    ds.append({"id": "public-evidence", "kind": "real-public-metadata", "ta": "all", "title": "Real public evidence examples",
               "subtitle": "Real bibliographic metadata, kept separate. Never evidence for the fictional products.", "synthetic": False,
               "readme": "Data-Sources/public/evidence-snapshots/README.md", "folder": "Data-Sources/public/evidence-snapshots/", "count": len(pe),
               "categories": [{"id": "snapshots", "title": "Snapshots", "files": pe}]})
    b = [{"name": f"first-mission-{ta['id']}.md", "path": f"workshop/bundles/first-mission-{ta['id']}.md", "format": "MD",
          "title": f"{ta['short']} starter: one self-contained file to upload"} for ta in TAS]
    ds.append({"id": "starter-bundles", "kind": "starter-bundle", "ta": "all", "title": "Starter bundles",
               "subtitle": "For agents that cannot open GitHub: upload one file and start.", "synthetic": True,
               "folder": "workshop/bundles/", "count": 3, "categories": [{"id": "bundles", "title": "Bundles", "files": b}]})
    cc_ = [{"name": Path(x["path"]).name, "path": x["path"], "format": "MD", "title": x["headline"]} for x in cards]
    ds.append({"id": "change-cards", "kind": "exercise", "ta": "all", "title": "Change cards", "subtitle": "New information that arrives mid-exercise.",
               "synthetic": True, "readme": "workshop/change-cards/README.md", "folder": "workshop/change-cards/", "count": len(cc_),
               "categories": [{"id": "cards", "title": "Cards", "files": cc_}]})
    tpl = [{"name": p.name, "path": f"shared/templates/{p.name}", "format": "MD", "title": first_h1(p.read_text(encoding="utf-8"))}
           for p in sorted((repo / "shared/templates").glob("*.md")) if p.name != "README.md"]
    ds.append({"id": "templates", "kind": "template", "ta": "all", "title": "Deliverable templates", "subtitle": "Blank shapes for common Medical Affairs outputs.",
               "synthetic": False, "readme": "shared/templates/README.md", "folder": "shared/templates/", "count": len(tpl),
               "categories": [{"id": "templates", "title": "Templates", "files": tpl}]})
    ex = [{"name": "advisory-board-deck/deck.json", "path": "examples/advisory-board-deck/deck.json", "format": "JSON", "title": "Synthetic advisory board deck (design exemplar)"},
          {"name": "obesity-advisory-preread/deck.json", "path": "examples/obesity-advisory-preread/deck.json", "format": "JSON", "title": "Obesity advisory board pre-read, rebuilt (exemplar)"}]
    ex += [{"name": f"figures/{p.name}", "path": f"examples/advisory-board-deck/figures/{p.name}", "format": "PNG", "title": "Exemplar figure"}
           for p in sorted((repo / "examples/advisory-board-deck/figures").glob("*.png"))]
    ex.append({"name": "http_cache.json", "path": "shared/fixtures/http_cache.json", "format": "JSON", "title": "Recorded public API responses (test fixture)"})
    ds.append({"id": "examples-fixtures", "kind": "example", "ta": "all", "title": "Examples & fixtures",
               "subtitle": "What finished output looks like, plus recorded API responses for offline tests.", "synthetic": True,
               "folder": "examples/", "count": len(ex), "categories": [{"id": "examples", "title": "Examples", "files": ex}]})
    c["datasets"] = ds
    c["public_sources"] = json.loads(D("public/catalog.json"))
    c["synthetic_index_count"] = json.loads(D("synthetic/index.json"))["count"]
    c["house_rules_count"] = len([p for p in (repo / "house-rules").glob("*.md") if p.name != "README.md"])
    c["connected_counts"] = {k: v["rows"] for k, v in dd["tables"].items()}
    c["skill_names"] = sorted(p.parent.name for p in (repo / "skills").glob("*/SKILL.md"))
    return c

# ---------------------------------------------------------------- prompt optimizer
# Structure: RISEN (Role, Instructions, Steps,
# End goal, Narrowing) + an output contract and constraint pairs, the provider
# "dialects" (universal Markdown vs Claude-style XML), and Loop Engineering's
# PROOF and STOP conditions. Composed deterministically here and in assets/app.js
# from the SAME template data, so nothing calls an API.

OPT_GUARDRAILS = [
    "Do not send, post, publish or change any external system. Prepare drafts only.",
    "Never invent a citation, number or quote. If no source supports a claim, say so and leave it unresolved.",
    "Before any analysis, surface possible safety findings (adverse events, product complaints) with the verbatim and flag them for routing.",
    "Keep any fictional practice data and real evidence clearly separate. Mark every output DRAFT.",
]
OPT_SECTIONS = [
    {"id": "intro", "title": "", "tag": "", "lines": ["# Assignment: {{title}}", "You are {{role}}. This is an assignment, not a question: do the work end to end and hand back finished deliverables, not advice."]},
    {"id": "goal", "title": "Goal: what done looks like", "tag": "end_goal", "needs": ["goal"], "lines": ["{{goal}}"]},
    {"id": "audience", "title": "Who it is for", "tag": "audience", "needs": ["audience"], "lines": ["{{audience}}"]},
    {"id": "context", "title": "Context to use", "tag": "context", "lines": ["- Use {{repo}}. Read AGENTS.md first, then load these skills and their requirements: {{skills}}.", "{{data_line}}", "{{context|list}}"]},
    {"id": "steps", "title": "How to work", "tag": "steps", "lines": ["{{steps|numbered}}"]},
    {"id": "rules", "title": "House rules and boundaries", "tag": "constraints", "lines": ["{{constraints|list}}", "{{guardrails|list}}"]},
    {"id": "deliverable", "title": "Deliverable", "tag": "output_format", "needs": ["deliverable"], "lines": ["{{deliverable|list}}"]},
    {"id": "proof", "title": "Proof of done (verify before you hand over)", "tag": "proof", "needs": ["checks"], "lines": ["{{checks|list}}"]},
    {"id": "stop", "title": "Stop and come back to me before you", "tag": "human_checkpoints", "needs": ["human_stop"], "lines": ["{{human_stop|list}}"]},
    {"id": "close", "title": "When you finish", "tag": "handover", "lines": ["Tell me what you did, what you could not do, and which decisions are still mine. I am the final judge of this work."]},
]
OPT_FIELDS = [
    {"id": "goal", "label": "Goal / outcome", "hint": "The end state, not the question. What will exist when it is done?", "rows": 3},
    {"id": "audience", "label": "Audience", "hint": "Who reads it and what they need to decide.", "rows": 2},
    {"id": "context", "label": "Context & files", "hint": "One per line: files, records, links or background it should use.", "rows": 3},
    {"id": "constraints", "label": "Constraints & house rules", "hint": "One per line. Say why, so it generalizes.", "rows": 3},
    {"id": "deliverable", "label": "Deliverable", "hint": "One per line: the files or sections you expect back.", "rows": 2},
    {"id": "checks", "label": "Checks (proof of done)", "hint": "One per line: what must be true before it hands over.", "rows": 3},
    {"id": "human_stop", "label": "When to stop for a human", "hint": "One per line: decisions or actions that need you.", "rows": 2},
]
COMMON_STEPS_START = ["Inventory the inputs. List what is missing before you start, then continue with what you have.",
                      "Scan human-sourced records for possible safety findings first."]
COMMON_STEPS_END = ["Challenge your own draft with deliverable-quality-review and fix what it finds.",
                    "Deliver designed files where your environment allows; otherwise give the complete content in your reply and say so."]
OPT_TYPES = [
    {"id": "kol-pre-call", "label": "KOL pre-call brief", "mission": "kol-meeting", "skills": ["kol-engagement-brief", "msl-pre-call-planning"],
     "role": "a senior Medical Science Liaison preparing a scientific exchange",
     "steps": ["Gather prior interactions, open commitments and what has changed since the last meeting.", "Identify what this expert genuinely cares about and where our evidence is weak.", "Draft neutral scientific questions to ask, and the hard questions they will likely ask us, with the evidence to have ready."],
     "defaults": {"goal": "Walk into a 30-minute scientific exchange with the first expert in the KOL dossiers fully prepared, including an honest answer to their strongest objection.",
                  "audience": "Me, the MSL, in the ten minutes before the meeting.",
                  "context": "kol-dossiers.md, interaction-notes.md, product-profile.md, evidence-landscape.md",
                  "constraints": "Two pages maximum: it gets read in ten minutes.\nNo promotional language: this is scientific exchange.",
                  "deliverable": "Two-page meeting brief (Word + PDF)\nQuestions to ask, likely questions, evidence and unresolved gaps",
                  "checks": "Every claim about the expert traces to a dossier or interaction note\nUnresolved evidence is stated plainly, not smoothed over\nNo meeting facts are invented",
                  "human_stop": "Contacting the expert or scheduling anything\nAnything that looks like an off-label request"}},
    {"id": "field-insights", "label": "Field insights synthesis", "mission": "field-insights", "skills": ["field-insight-synthesis", "executive-briefing"],
     "role": "a Medical Affairs insights lead reporting to leadership",
     "steps": ["Deduplicate contacts and separate observations from insights.", "Find the three most consequential insights: what is happening, why it matters, what it changes.", "Capture disagreements, weak signals and what the field did not say.", "Recommend one concrete next action per insight with an accountable role."],
     "defaults": {"goal": "Leadership knows the three field insights that should change what we do this quarter, each with an owner and a next action.",
                  "audience": "Medical Affairs leadership, four minutes to read.",
                  "context": "field-observations.csv, medical-plan.md, product-profile.md",
                  "constraints": "Themes with counts are not insights: explain why it matters and what it changes.\nState confidence for each insight and why.",
                  "deliverable": "Leadership brief (Word + PDF)\nInsight table with source record IDs\nSimulated safety escalation and missing-information list",
                  "checks": "Every insight cites source record IDs\nSafety findings appear before the analysis\nEach action names an accountable role",
                  "human_stop": "Routing any safety finding\nSharing the brief beyond our team"}},
    {"id": "congress-readout", "label": "Congress readout", "mission": "congress", "skills": ["congress-intelligence", "competitive-intelligence"],
     "role": "a congress intelligence lead in Medical Affairs",
     "steps": ["State what we expected before the congress.", "Compare what was presented with those expectations and with the current medical plan.", "Apply the same scepticism to our own data as to competitors'.", "Recommend what changes in the plan, what does not, and why."],
     "defaults": {"goal": "Leadership knows in four minutes what changed at the congress and what we should do about it.",
                  "audience": "Medical leadership and brand medical leads.",
                  "context": "congress-abstracts.md, competitor-announcements.md, medical-plan.md, product-profile.md",
                  "constraints": "One page, four sections: what changed, why it matters, what to watch, what we should do.\nA summary of presentations is not intelligence.",
                  "deliverable": "One-page congress readout (Word + PDF)\nChange recommendations with evidence limitations",
                  "checks": "Every 'what changed' item is compared against a stated prior expectation\nEvidence limitations stay attached to each finding\nAnything contradicting a current claim is flagged",
                  "human_stop": "Changing an approved medical plan or claim"}},
    {"id": "mi-response", "label": "Medical information response", "mission": "medical-information", "skills": ["medical-information-response"],
     "role": "a medical information specialist",
     "steps": ["Triage the enquiries by urgency and type.", "Surface potential safety issues before drafting.", "Draft responses supported only by the supplied sources.", "Log every gap where the evidence does not answer the question."],
     "defaults": {"goal": "The enquiry queue is triaged, every answerable enquiry has a draft response, and every gap is logged.",
                  "audience": "The medical information team and the reviewing medical signatory.",
                  "context": "medical-information-enquiries.csv, product-profile.md, structured-evidence-table.csv",
                  "constraints": "Do not infer approval in other countries.\nAnswer the question asked; do not volunteer off-label information.",
                  "deliverable": "Triage register\nDraft responses and gap log\nSimulated safety routing list",
                  "checks": "Every response cites the supporting source\nNo response is marked as sent\nSafety items are routed before drafting",
                  "human_stop": "Sending any response\nAny real (non-simulated) safety case"}},
    {"id": "evidence-gap", "label": "Evidence gap map", "mission": "evidence-investment", "skills": ["evidence-gap-analysis", "integrated-evidence-plan"],
     "role": "an evidence generation strategist",
     "steps": ["List the gaps and, for each, the decision it blocks and whose decision it is.", "Separate evidence gaps from communication gaps.", "Propose the study design that would close each gap that matters, with cost.", "Allocate the budget with an explicit funding line and what is lost below it."],
     "defaults": {"goal": "A ranked evidence gap map with a funded portfolio inside the budget ceiling and an explicit line below which we decline.",
                  "audience": "The evidence planning committee.",
                  "context": "evidence-landscape.md, integrated-evidence-plan.csv, iis-proposal.md, rwe-study-concept.md, payer-hta-brief.md",
                  "constraints": "Do not propose a study just because data are missing: explain the decision it changes.\nCheck what we could answer from data we already hold.",
                  "deliverable": "Ranked gap map (spreadsheet or table)\nCommittee brief with trade-offs",
                  "checks": "Every gap names the decision it blocks\nThe allocation adds up to the ceiling or less\nDuplicated and dependent projects are reconciled",
                  "human_stop": "Committing budget or approving a study"}},
    {"id": "ad-board", "label": "Advisory board package", "mission": "advisory-board", "skills": ["advisory-board-design", "evidence-gap-analysis", "medical-slide-deck"],
     "role": "a medical strategy lead designing an advisory board",
     "steps": ["Identify the unanswered questions that justify seeking external advice.", "Drop any question the evidence does not justify, and say why.", "Write the charter, discussion guide and advisor briefs.", "Build the pre-read deck."],
     "defaults": {"goal": "An advisory board worth holding: five unanswered questions, each tied to a decision, with the full briefing package ready for review.",
                  "audience": "Internal approvers first, then the external advisors.",
                  "context": "advisory-board-transcript.md, field-observations.csv, evidence-landscape.md, kol-dossiers.md, product-profile.md",
                  "constraints": "Questions seek advice, not endorsement.\nApparent consensus in past transcripts is challenged, not assumed.",
                  "deliverable": "Board charter and discussion guide\nPre-read deck (PowerPoint + PDF)\nAdvisor briefs",
                  "checks": "Each question links to a decision and an evidence gap\nNo question is leading or promotional\nAll figures trace to sources",
                  "human_stop": "Inviting advisors or agreeing fees"}},
    {"id": "publication-plan", "label": "Publication plan", "mission": "publication", "skills": ["scientific-communication-strategy", "scientific-manuscript", "plain-language-summary"],
     "role": "a scientific communications lead",
     "steps": ["Work backwards from what each audience is trying to decide.", "Show where we over-communicate and where we are silent.", "Separate evidence gaps (research) from communication gaps (publish).", "Sequence the next 12 months of outputs."],
     "defaults": {"goal": "A 12-month scientific communication strategy we can defend, including what to stop publishing.",
                  "audience": "The publications steering committee.",
                  "context": "publication-plan.md, evidence-landscape.md, field-observations.csv, medical-plan.md, product-profile.md",
                  "constraints": "A strategy, not a list of papers sequenced by data availability.\nNegative and neutral results are planned for, not hidden.",
                  "deliverable": "Strategy brief (Word + PDF)\nPublication roadmap table",
                  "checks": "Each planned output names its audience and the decision it informs\nEvidence gaps and communication gaps are labelled separately\nReported numbers match the source tables",
                  "human_stop": "Submitting or committing to a journal or congress"}},
    {"id": "launch-readiness", "label": "Launch readiness & launch plan", "mission": "launch-readiness", "skills": ["launch-medical-readiness", "mlr-review-readiness", "medical-strategy-plan"],
     "role": "a launch medical readiness lead",
     "steps": ["Assess every launch dependency against the readiness register.", "Never average a critical red dependency into a green score.", "Build the remediation plan with owners and dates.", "Draft the medical launch plan for the first 90 days."],
     "defaults": {"goal": "A clear launch gate verdict, a remediation plan for every red or amber item, and a first-90-days medical launch plan.",
                  "audience": "The launch team and medical leadership.",
                  "context": "launch-readiness-register.md, medical-information-enquiries.csv, mlr-review-comments.md, scientific-platform-draft.md, integrated-evidence-plan.csv",
                  "constraints": "A red safety or regulatory dependency blocks green, whatever the average.\nEvery action has an owner and a date.",
                  "deliverable": "Gate assessment\nRemediation tracker\nLeadership brief and 90-day medical launch plan",
                  "checks": "Every red item has a remediation owner\nThe verdict follows the worst critical dependency\nOpen MLR comments are reflected",
                  "human_stop": "Declaring launch readiness\nAnything that needs MLR approval"}},
    {"id": "plain-language", "label": "Plain-language summary", "mission": "publication", "skills": ["plain-language-summary", "deliverable-quality-review"],
     "role": "a plain-language writer working with patient partners",
     "steps": ["Pull the key findings from the source.", "Rewrite for a lay reader, keeping every limitation and safety finding.", "Check readability and remove jargon.", "Check every number against the source."],
     "defaults": {"goal": "A plain-language summary a patient or caregiver can understand that stays faithful to the study.",
                  "audience": "Patients and caregivers with no medical training.",
                  "context": "plain-language-source.md, structured-evidence-table.csv",
                  "constraints": "No promotional language and no claims beyond the study.\nKeep harms as visible as benefits.",
                  "deliverable": "Plain-language summary (Word + PDF)\nNumber-check log against the source",
                  "checks": "Every number matches the source\nLimitations and safety results are included\nReading level suits a general audience",
                  "human_stop": "Publishing or sharing with patients"}},
    {"id": "agent-swarm", "label": "Agent swarm / coordinator", "mission": "thirty-day-capstone", "skills": ["medical-affairs-orchestrator", "medical-strategy-plan", "field-insight-synthesis", "integrated-evidence-plan", "executive-briefing"],
     "role": "the coordinator of a team of Medical Affairs agents",
     "steps": ["Break the goal into workstreams and assign each to a specialist sub-agent (or run them in sequence if you cannot spawn agents).", "Give each workstream its own inputs, deliverable and proof of done.", "Track which sources each output depends on.", "Merge the work, resolve conflicts between workstreams and keep a change log."],
     "defaults": {"goal": "A coordinated 30-day Medical Affairs plan: leadership brief, action tracker and scientific briefing, with source dependencies so new evidence can update the affected work.",
                  "audience": "Medical Affairs leadership and the workstream owners.",
                  "context": "medical-plan.md, product-profile.md, field-observations.csv, evidence-landscape.md, integrated-evidence-plan.csv, launch-readiness-register.md",
                  "constraints": "Each sub-agent gets only the inputs it needs.\nWhen new information arrives, update only the affected work and preserve the old version.",
                  "deliverable": "Workstream assignment table (agent, inputs, deliverable, proof)\nLeadership brief, 30-day action tracker, scientific briefing\nSource dependency map and change log",
                  "checks": "Every output lists its source dependencies\nConflicts between workstreams are resolved or escalated\nThe tracker has an owner and date per action",
                  "human_stop": "Any trade-off between workstreams that changes priorities\nAnything outside the agreed budget"}},
]
OPT_LIBRARY = [
    {"id": "lib-publications-brain", "team": "Publications Brain", "type": "publication-plan", "ta": "oncology-mm",
     "fields": {"goal": "Decide what we should publish over the next 12 months, what we should stop, and make every scientific output consistent with the source data."}},
    {"id": "lib-insights-engine", "team": "Insights Engine", "type": "field-insights", "ta": "immunology-ad", "fields": {}},
    {"id": "lib-congress-monitor", "team": "Congress Monitor", "type": "congress-readout", "ta": "cardiometabolic-obesity", "fields": {}},
    {"id": "lib-field-intelligence", "team": "Field Intelligence Engine", "type": "kol-pre-call", "ta": "oncology-mm",
     "fields": {"context": "kol-dossiers.md, interaction-notes.md, product-profile.md, evidence-landscape.md\nData-Sources/synthetic/connected/interactions.csv and msl_tasks.csv for open commitments"}},
    {"id": "lib-launch-plan", "team": "Launch planning", "type": "launch-readiness", "ta": "oncology-mm", "fields": {}},
    {"id": "lib-swarm-capstone", "team": "Capstone · agent swarm", "type": "agent-swarm", "ta": "oncology-mm", "fields": {}},
]

def _fill(line, vals):
    def rep(m):
        key, _, flt = m.group(1).partition("|")
        v = vals.get(key, "")
        items = [x.strip().lstrip("-").strip() for x in (v if isinstance(v, list) else str(v).split("\n")) if x.strip()]
        if flt == "list":
            return "\n".join("- " + x for x in items)
        if flt == "numbered":
            return "\n".join(f"{i+1}. {x}" for i, x in enumerate(items))
        return ", ".join(items) if isinstance(v, list) else str(v).strip()
    return re.sub(r"\{\{([a-z_|]+)\}\}", rep, line)

def compose_prompt(type_id, fields, ta, dialect, repo_url):
    t = next(x for x in OPT_TYPES if x["id"] == type_id)
    vals = dict(t["defaults"]); vals.update({k: v for k, v in fields.items() if v is not None})
    if ta in TA_BY_ID:
        tt = TA_BY_ID[ta]
        data_line = (f"- Workshop mode: use the {tt['short'].lower()} synthetic data in Data-Sources/synthetic/{ta}/ "
                     f"(mission `{t['mission']}` in workshop/catalog.json). Read files there by name.")
    else:
        data_line = ("- I have no data yet. Start from public sources where they help, list the data you would need, and ask me before going further." if ta == "none" else
                     "- Use my own data: ask me to attach it or tell you where it lives, and confirm I am allowed to use it. If something you need is missing, list it instead of inventing it.")
    vals.update({"title": t["label"], "role": t["role"], "repo": repo_url, "skills": t["skills"], "data_line": data_line,
                 "steps": COMMON_STEPS_START + t["steps"] + COMMON_STEPS_END, "guardrails": OPT_GUARDRAILS})
    out = []
    for sec in OPT_SECTIONS:
        if any(not str(vals.get(n, "")).strip() for n in sec.get("needs", [])):
            continue
        body = [x for x in (_fill(l, vals) for l in sec["lines"]) if x.strip()]
        if not body:
            continue
        if not sec["title"]:
            out.append("\n".join(body))
        elif dialect == "xml":
            out.append(f"<{sec['tag']}>\n" + "\n".join(body) + f"\n</{sec['tag']}>")
        else:
            out.append(f"## {sec['title']}\n" + "\n".join(body))
    return "\n\n".join(out)

def optimizer_data(cfg):
    return {"about": "Client-side Medical Affairs assignment composer. Structure: RISEN + output contract + constraint pairs, provider dialects, Loop Engineering proof and stop conditions.",
            "repo": cfg["repo"]["url"], "sections": OPT_SECTIONS, "fields": OPT_FIELDS, "guardrails": OPT_GUARDRAILS,
            "common_steps_start": COMMON_STEPS_START, "common_steps_end": COMMON_STEPS_END, "types": OPT_TYPES,
            "library": OPT_LIBRARY, "therapeutic_areas": TAS,
            "dialects": [{"id": "markdown", "label": "Universal (Markdown)"}, {"id": "xml", "label": "Claude-style (XML tags)"}]}

# ---------------------------------------------------------------- helpers

def e(s):
    return html.escape(str(s), quote=True)

def load_cfg():
    return json.loads((HERE / "site.config.json").read_text(encoding="utf-8"))

def ds_repo(cfg, p):
    """Datasets live in Data-Sources (paths 'Data-Sources/...'); bundles, cards and templates stay in the skills repo."""
    s = cfg["datasets_source"]
    pre = s.get("path_prefix_from", "")
    if pre and p.startswith(pre):
        return s, s.get("path_prefix_to", "") + p[len(pre):]
    return cfg["repo"], p

def ds_path(cfg, p):
    return ds_repo(cfg, p)[1]

def ds_links(cfg, p):
    b, q = ds_repo(cfg, p)
    return {"url": b["blob_base"] + q, "raw": b["raw_base"] + q}

def ds_folder(cfg, p):
    b, q = ds_repo(cfg, p)
    return b["tree_base"] + q

def repo_url(cfg, p, raw=False):
    r = cfg["repo"]
    if p.endswith("/"):
        return r["tree_base"] + p
    return (r["raw_base"] if raw else r["blob_base"]) + p

def mission_prompt(cfg, m, ta):
    return (f"Use {cfg['repo']['url']}\n"
            f"Read AGENTS.md. Start the {m['id']} workshop mission from workshop/catalog.json using the {TA_BY_ID[ta]['short'].lower()} synthetic data ({ta}).\n"
            f"Goal: {m['objective']}\n"
            f"Deliver: {'; '.join(m['deliverables'])}.\n"
            "Do not ask me to connect company systems. Use public scientific sources only when useful and keep them separate from fictional workshop data.\n"
            "If you cannot retrieve the repository, tell me which starter file to upload.")

def team_prompt(cfg, m, ta):
    return (f"Use {cfg['repo']['url']}\n"
            f"Read AGENTS.md, then read {m['path']} and run that mission with the {TA_BY_ID[ta]['short'].lower()} synthetic data in Data-Sources/synthetic/{ta}/.\n"
            f"Mission: {m['mission']}\n"
            "Show me a short plan first, then do the work. Do not ask me to connect company systems. Keep public evidence separate from fictional workshop data.")

def round2_prompt(m):
    return (f"Round 2. Read {m['house_rules_file']}. Apply these rules from our team:\n"
            "1. [your rule, with the reason]\n2. [your rule, with the reason]\n3. [your rule, with the reason]\n"
            "Run the same mission again and show me what changed versus the first draft.")

def say_prompt(cfg, s, ta):
    return (f"Use {cfg['repo']['url']}\n"
            f"Read AGENTS.md and work in workshop mode with the {TA_BY_ID[ta]['short'].lower()} synthetic data ({ta}).\n"
            f"{s['ask']}\n"
            f"Prepare: {s['prepares'][0].lower() + s['prepares'][1:]}.\n"
            "Do not ask me to connect company systems. Keep public evidence separate from fictional workshop data.")

def templated(fn, *args):
    return {ta["id"]: fn(*args, ta["id"]) for ta in TAS}

TA_BY_ID["__TA__"] = {"id": "__TA__", "short": "__SHORT__", "area": "", "product": ""}

def ta_tpl(fn, *args):
    """One template for the browser: __TA__ -> id, __short__ -> lower-case short name."""
    return {"tpl": fn(*args, "__TA__"), "default": fn(*args, "oncology-mm")}

def library_items(cfg):
    out = []
    for it in OPT_LIBRARY:
        t = next(x for x in OPT_TYPES if x["id"] == it["type"])
        out.append(dict(it, label=t["label"], prompts={d: compose_prompt(it["type"], it["fields"], it["ta"], d, cfg["repo"]["url"]) for d in ("markdown", "xml")}))
    return out

# ---------------------------------------------------------------- data outputs

PASTE_TEMPLATE = "Go to {site} and follow the Instructions for agents."

def agent_playbook(content, cfg, abs_, raw):
    """The menu-driven playbook at the top of agents.md (also shown on the page)."""
    ev = cfg["event"]; R = cfg["repo"]; site = cfg.get("site_url", "").rstrip("/") or "(this site)"
    ds = cfg["datasets_source"]["repo_url"].rstrip("/")
    latest = ds + "/releases/latest/download/"
    ms = content["missions"]; tm = content["team_missions"]
    swarm = next((m for m in ms if m["id"] == "launch-plan-swarm"), None)
    L = [f"# Instructions for agents: {ev['name']}", "",
         f"You are an AI agent. A person pointed you at {site} . This file tells you exactly what to do.",
         f"The person is a Medical Affairs professional at {ev['name']} ({ev['dates']}, {ev['venue']}, {ev['address']}). They are not technical: give them useful, reviewed results, not repository internals.", "",
         "## Your task in one breath",
         "Read what this site points to, greet the person, ASK what they want to do (offer the numbered menu below), then carry out their choice step by step, checking in at the human-judgment points, and hand back the finished deliverable.", "",
         "## 1. Read first (sources of truth)",
         f"- This site: {abs_('agents.md')} (this file), {abs_('llms.txt')}, {abs_('missions.json')}, {abs_('skills.json')}, {abs_('prompts.json')}, {abs_('datasets.json')}.",
         f"- Skills library: {R['url']} . Default branch: `{cfg['repo'].get('default_branch', 'HEAD')}`. Start with {raw('AGENTS.md')}.",
         f"  The launch-planning swarm (skills medical-launch-plan, launch-timeline-and-governance, launch-field-training and launch-medical-readiness; mission `launch-plan-swarm`; team mission 7) is on the default branch with everything else.",
         f"- Data: {ds} . Manifest of every dataset (synthetic and public, with licence, access type and links): {latest}manifest.json (also manifest.csv). Everything at once: {latest}all-synthetic-data.zip, {latest}all-synthetic.jsonl, {latest}all-data-catalog.zip.",
         f"- Getting data: fetch it straight onto YOUR OWN machine from the manifest URLs; never ask the person to download files to their laptop and upload them. Read {latest}manifest.json, then for each dataset you need where `link_only` is false and `access` is `download`, `api-sample` or `bulk-file`, download `direct_url` (raw.githubusercontent.com or releases/latest/download; follow redirects) into e.g. /workspace/data/<type>/<group>/ and unzip ZIPs. For `official-site` and `link-only` entries, open the official URL and work at the source under its licence; never copy or redistribute link-only data. Confirm synthetic files are labelled SYNTHETIC before using them. The Data page ({site}/data) has a 'Copy link' and a 'Copy for Grok Bot' instruction for every dataset and bundle.",
         f"- Prompt optimizer: POST JSON {{\"goal\": \"<short goal>\", \"mode\": \"single\" or \"swarm\", \"ta\": \"oncology-mm|immunology-ad|cardiometabolic-obesity|own\"}} to {abs_('api/optimize')} (streams Markdown; on error, use the optimizer structure in {abs_('prompts.json')}).", "",
         f"- Skill creator (for workflows the library does not cover): on {site}/optimizer choose 'Skill creator', or POST JSON {{\"workflow\": \"<plain words>\", \"kind\": \"single\" or \"group\", \"data\": \"own|practice|none\", \"data_note\": \"...\", \"audience\": \"...\"}} to {abs_('api/skills')}. It returns files in the Medical-Affairs-Skills format (skills/<name>/SKILL.md with the library's frontmatter, house-rules/<name>.md, README.md; a group adds a lead skill with the org chart, waves and human gates); POST {{\"pack_name\", \"files\"}} to {abs_('api/skills/zip')} for a zip. Or build the skills yourself in that format. Show every SKILL.md to the person and get their approval before using a new skill.",
         "## 2. Greet, then ask",
         f"Say hello in one line, say you have read the {ev['name']} materials, then ask: \"What would you like to do?\" and offer this menu. Wait for the answer. Do not start work before they choose (if they already stated a goal, map it to an option and confirm).", "",
         "1. Set up Grok Bot or another agent with the Medical Affairs skills library",
         f"2. Run a workshop mission ({len(ms)} available, listed below)",
         f"3. Use one specific skill ({content['skill_count']} available: {abs_('skills.json')})",
         "4. Build the launch-planning agent swarm (a full medical launch plan for an upcoming asset)",
         "5. Practise on synthetic data (pick a pack: oncology NORVANTIB, immunology DERMALYX, cardiometabolic ADIPOSYN, or the connected practice CRM)",
         "6. Find and connect real public data sources",
         "7. Write or optimize a prompt for an agent or an agent swarm",
         f"8. Prepare for the hackathon team challenge ({len(tm)} team missions)",
         "9. Something else (tell me)", "",
         "Missions for option 2: " + "; ".join(f"`{m['id']}` ({m['title']})" for m in ms) + ".",
         "Team missions for option 8: " + "; ".join(f"{m['number']}. {m['function']}" for m in tm) + ".", "",
         "## 3. Do it",
         "For every choice: restate the goal as an end state, list the skills and files you will use, give a short plan, then work. Pause at each human checkpoint.", "",
         f"- Option 1 (set up an agent): follow {raw('docs/agents.md')}. Grok Bot is the event sandbox; sign-up links and credit codes are shared at the conference (see {site}/#grokbot). Other hosts: Claude Code (clone and read AGENTS.md, or `/plugin marketplace add Open-Medical-Affairs/Medical-Affairs-Skills`), Codex or Cursor (open the repository, read AGENTS.md), chat-only tools (upload a starter bundle from workshop/bundles/). For one agent per mission, use workshop/grokbot-agents.json and scripts/package_skills.py.",
         f"- Option 2 (mission): ask which therapeutic area (default `{content['default_ta']}`), then follow \"Running a mission, step by step\" below. Inputs and prompts per area: {abs_('missions.json')}.",
         f"- Option 3 (skill): load skills/<name>/SKILL.md plus medical-affairs-foundations and the skill's `requires`, and house-rules/<name>.md. Ask for the person's material or offer synthetic data.",
         "- Option 4 (launch swarm): " + (f"run mission `launch-plan-swarm` ({swarm['title']}). Skills: {', '.join(swarm['skills'])}. " if swarm else "") + "Act as coordinator: build a shared context brief first, give each worker agent only its context packet, merge, have an independent reviewer check, then hand the plan to the person. Default asset: ADIPOSYN (synthetic).",
         f"- Option 5 (practise): pick the pack, filter {latest}manifest.json by `group`, read only the files the task needs, and mark every output SYNTHETIC and DRAFT.",
         f"- Option 6 (public data): choose sources from the manifest (`type: public`) by workflow; use `direct_url` for the official API/download, respect `rate_limit` and `data_policy`; for `link_only: true`, link to it and never copy its data.",
         f"- Option 7 (prompt): ask for a one-line goal and single task vs swarm, call {abs_('api/optimize')}, show the result, and offer to run it. Starter ideas are on {site}/#optimizer.",
         f"- Option 8 (hackathon): ask which team mission, read its brief (missions.json `team_missions`), run it on synthetic data, and prepare the readout the team will present.",
         "- Option 9: map the request to the closest skills via medical-affairs-orchestrator, then proceed as above.", "",
         "Human checkpoints (always stop and ask): before using any data beyond the synthetic packs; when a possible safety finding appears; before final conclusions or recommendations; before sending, sharing, publishing or posting anything.", "",
         "Deliver designed files where your host can (Word/PowerPoint/PDF via the skill's scripts/ma_render.py). If you cannot create files or reach a source, say so plainly and deliver the complete content.", "",
         "## 4. Guardrails",
         "- The human is the final judge. Everything you produce is a draft for qualified review.",
         "- Workshop data is synthetic and fictional (Nordvant Biopharma; NORVANTIB, DERMALYX, ADIPOSYN). Never present it as real or mix it with real evidence.",
         "- No patient-identifiable information and no confidential company data, in prompts, files or public-source queries.",
         "- Verify every citation against its source; never invent references, data or people. List what is missing instead.",
         "- Respect licences: `link-only` sources are linked, never copied.",
         "- Do not send messages, email, post, publish or update external systems without the person's explicit say-so.", "",
         "## 5. Works with any harness",
         "Grok Bot, Claude (Code or Cowork), Microsoft Copilot, ChatGPT, Cursor, Codex or your own agent. Use the tools you actually have (web, files, shell, sub-agents); if you lack one, state the gap and continue with what works. Never claim a search, script or file happened if it did not.", "",
         "---", "", "# Reference", ""]
    return L


REL = "https://github.com/Open-Medical-Affairs/Data-Sources/releases/latest/download/"
# tools/fetch_all.py is not on Data-Sources main yet; switch this to .../HEAD/tools/fetch_all.py once it is.
FETCH_ALL = "https://raw.githubusercontent.com/Open-Medical-Affairs/Data-Sources/get-the-data/tools/fetch_all.py"

def gd_copy_buttons(url, grok, label="Copy link", primary=True):
    """Two copy buttons: the direct URL and a ready-to-paste Grok Bot instruction (handled by assets/get-data.js)."""
    return (f'<button type="button" class="gd-c{" gd-c--main" if primary else ""}" data-copy-text="{e(url)}" data-done="Link copied"><svg aria-hidden="true"><use href="#ic-copy"/></svg><span>{e(label)}</span></button>'
            f'<button type="button" class="gd-c gd-c--grok" data-copy-text="{e(grok)}" data-done="Instruction copied"><span class="gd-c-g" aria-hidden="true">G</span><span>Copy for Grok Bot</span></button>')

def gd_big():
    syn = REL + "all-synthetic-data.zip"
    cat = REL + "all-data-catalog.zip"
    man = REL + "manifest.json"
    g_syn = (f"Download {syn} to your computer (e.g. /workspace/data/all-synthetic-data.zip) and unzip it into /workspace/data/synthetic/. "
             "Confirm the files are labelled SYNTHETIC (fictional workshop data, not real patients or products), list the packs you found, then ask me what I want to do with them.")
    g_cat = (f"Download {cat} to your computer (e.g. /workspace/data/all-data-catalog.zip) and unzip it into /workspace/data/catalog/. "
             "It is the full catalog: manifest.json/.csv, the public source list with licences, and real paper snapshots. Do not download LINK ONLY sources; use them only at their official site. Summarise what is in it, then ask me what I want to do.")
    g_all = (f"Fetch {man} (the Data-Sources manifest). For every dataset where link_only is false and access is download, api-sample or bulk-file, download direct_url onto your own machine under /workspace/data/<type>/<group>/ (keep the file name; unzip ZIPs). "
             "Skip link-only and official-site entries: list them for me with their official URLs and licences instead. Confirm every synthetic file is labelled SYNTHETIC, report what you downloaded and anything that failed, then ask me what I want to do.")
    alts = [("one JSONL file", "all-synthetic.jsonl"), ("combined CSVs", "all-synthetic-combined-csv.zip"), ("oncology", "synthetic-oncology-mm.zip"), ("immunology", "synthetic-immunology-ad.zip"), ("cardiometabolic", "synthetic-cardiometabolic-obesity.zip"), ("practice CRM", "synthetic-connected.zip")]
    alt_html = " · ".join(f'<button type="button" class="gd-mini" data-copy-text="{e(REL + f)}" data-done="Link copied" title="Copy {e(REL + f)}">{e(t)}</button>' for t, f in alts)
    return f'''<div class="gd-big">
        <div class="gd-card gd-card--syn">
          <div class="gd-btn"><span class="gd-ic" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 4v11m0 0l-4.5-4.5M12 15l4.5-4.5M5 19h14"/></svg></span><span><span class="gd-btn-t">All synthetic data <span class="badge badge--syn">Synthetic</span></span><span class="gd-btn-s">Every synthetic file in one .zip: 3 product packs, the practice CRM and its SQLite file</span><code class="gd-url">{e(syn)}</code></span></div>
          <div class="gd-cbar">{gd_copy_buttons(syn, g_syn)}<a class="gd-dl" href="{e(syn)}">or download</a></div>
          <p class="gd-alt">Copy a link to just: {alt_html}</p>
        </div>
        <div class="gd-card gd-card--cat">
          <div class="gd-btn gd-btn--light"><span class="gd-ic" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 5h14M5 10h14M5 15h9M5 20h6"/></svg></span><span><span class="gd-btn-t">Full catalog</span><span class="gd-btn-s">Every dataset with licence and links, the public sources and real paper examples (.zip)</span><code class="gd-url">{e(cat)}</code></span></div>
          <div class="gd-cbar">{gd_copy_buttons(cat, g_cat)}<a class="gd-dl" href="{e(cat)}">or download</a></div>
          <p class="gd-alt">Just the list: <button type="button" class="gd-mini" data-copy-text="{e(man)}" data-done="Link copied">manifest.json</button> · <button type="button" class="gd-mini" data-copy-text="{e(REL + 'manifest.csv')}" data-done="Link copied">manifest.csv</button> · script: <a href="{FETCH_ALL}">fetch_all.py</a></p>
        </div>
      </div>
      <div class="gd-every">
        <div><p class="gd-every-k">Everything, in one instruction</p><p class="gd-every-t">Your agent reads the manifest and pulls every directly downloadable file onto its own machine. Link-only sources are listed, never copied.</p></div>
        <div class="gd-cbar">{gd_copy_buttons(man, g_all, "Copy manifest link")}</div>
      </div>'''

def render(content, cfg):
    Ids.n = 0
    R = cfg["repo"]; ev = cfg["event"]
    site = cfg.get("site_url", "").rstrip("/")
    abs_ = (lambda p: f"{site}/{p}") if site else (lambda p: p)
    raw = lambda p: repo_url(cfg, p, True)
    out = {}
    missions_json = {
        "about": "Workshop missions from the Medical-Affairs-Skills repository, with ready-to-paste prompts per therapeutic area. Synthetic data only.",
        "repository": R["url"], "agent_entry": raw("AGENTS.md"), "catalog": raw("workshop/catalog.json"),
        "source_commit": content["source_commit"], "default_mission": content["default_mission"], "default_ta": content["default_ta"],
        "therapeutic_areas": TAS, "starter_prompt": content["starter_prompt"],
        "team_missions": [dict(m, url=repo_url(cfg, m["path"]), raw=raw(m["path"]), prompts=templated(team_prompt, cfg, m), round2_prompt=round2_prompt(m)) for m in content["team_missions"]],
        "missions": [dict(m, inputs_resolved={ta["id"]: [ds_links(cfg, i.replace("{ta}", ta["id"]))["raw"] for i in m["inputs"]] for ta in TAS},
                          prompts=templated(mission_prompt, cfg, m)) for m in content["missions"]],
        "say_this": [dict(s, prompts=templated(say_prompt, cfg, s)) for s in content["say_this"]],
        "change_cards": [dict(c, url=repo_url(cfg, c["path"]), raw=raw(c["path"])) for c in content["change_cards"]],
        "event_teams": TEAMS,
    }
    datasets_json = {
        "about": "Every dataset for the workshop. Synthetic packs and the public-source catalog live in the Open-Medical-Affairs/Data-Sources repository; starter bundles, change cards, templates and examples stay in Medical-Affairs-Skills. Links are generated from site.config.json.",
        "repositories": {"data_sources": {"url": cfg["datasets_source"]["repo_url"], "clone": cfg["datasets_source"]["repo_url"] + ".git",
                                          "synthetic_index": cfg["datasets_source"]["raw_base"] + "synthetic/index.json",
                                          "public_catalog": cfg["datasets_source"]["raw_base"] + "public/catalog.json",
                                          "agents": cfg["datasets_source"]["raw_base"] + "AGENTS.md"},
                         "skills": {"url": R["url"], "clone": R["url"] + ".git"}},
        "source": {k: v for k, v in cfg["datasets_source"].items() if not k.startswith("_")},
        "warning": "Two truth statuses, never mixed. groups[] with synthetic=true are SYNTHETIC: fictional data for training/workshops, not real patients/products. public_sources and the evidence snapshots are REAL public data: respect each data_policy (link-only = do not copy data). Do not upload real company or patient data.",
        "groups": []}
    for g in content["datasets"]:
        gg = {k: v for k, v in g.items() if k != "categories"}
        gg["folder_url"] = ds_folder(cfg, g["folder"])
        if g.get("readme"):
            gg["readme_raw"] = ds_links(cfg, g["readme"])["raw"]
        gg["categories"] = [{"id": c["id"], "title": c["title"], "files": [dict(f, **ds_links(cfg, f["path"])) for f in c["files"]]} for c in g["categories"]]
        datasets_json["groups"].append(gg)
    ps = content.get("public_sources")
    if ps:
        datasets_json["public_sources"] = {k: ps[k] for k in ("about", "warning", "verified_on", "data_policy_legend", "verification_legend", "counts", "top15", "already_used_by_skills", "groups", "sources")}
        datasets_json["public_sources"]["catalog_raw"] = cfg["datasets_source"]["raw_base"] + "public/catalog.json"
        datasets_json["public_sources"]["catalog_url"] = cfg["datasets_source"]["blob_base"] + "public/catalog.md"
    skills_json = {"count": content["skill_count"], "index": raw("SKILLS-INDEX.md"),
                   "groups": [{"title": g["title"], "intro": g["intro"], "skills": [dict(s, url=repo_url(cfg, s["path"]), raw=raw(s["path"]),
                               house_rules_url=repo_url(cfg, s["house_rules"])) for s in g["skills"]]} for g in content["skill_groups"]]}
    lib = library_items(cfg)
    prompts_json = {
        "about": "Every ready-to-paste prompt on the site, plus the Prompt Optimizer templates. To compose an assignment yourself: start with optimizer.sections, fill each {{field}} from the chosen type's defaults (overridden by the user's answers), apply |list and |numbered filters, drop sections whose 'needs' fields are empty, and render titles as '## Title' (markdown) or <tag>...</tag> (xml).",
        "repository_prompts": {"starter": content["starter_prompt"], "quickstart": content["quickstart_prompt"], "capstone": content["capstone_prompt"],
                               "change_card": content["change_prompt"], "msl_pre_call": content["msl_prompt"],
                               "next_moves": content["next_moves"], "recovery": content["recovery_prompts"]},
        "optimizer": optimizer_data(cfg),
        "library": lib,
    }
    out["missions.json"] = json.dumps(missions_json, indent=2, ensure_ascii=False)
    out["datasets.json"] = json.dumps(datasets_json, indent=2, ensure_ascii=False)
    out["skills.json"] = json.dumps(skills_json, indent=2, ensure_ascii=False)
    out["prompts.json"] = json.dumps(prompts_json, indent=2, ensure_ascii=False)

    L = agent_playbook(content, cfg, abs_, raw) + [
         "## What this is",
         f"This site is a companion to the open repository {R['url']} ({content['skill_count']} Medical Affairs skills, {len(content['missions'])} workshop missions, 3 therapeutic areas, synthetic data). Everything you need is in that repository; this file tells you where to start and how to work.", "",
         "## Running a mission, step by step",
         f"1. Read the repository's agent entry point: {raw('AGENTS.md')} and then {raw('docs/execution.md')}.",
         f"2. For a workshop or first demonstration, load the workshop launcher: {raw('skills/workshop-launcher/SKILL.md')}.",
         f"   For a specific Medical Affairs objective, load the orchestrator: {raw('skills/medical-affairs-orchestrator/SKILL.md')}.",
         f"3. Pick the mission and therapeutic area. Machine-readable list with prompts and resolved input links: {abs_('missions.json')} (source: {raw('workshop/catalog.json')}).",
         f"   If the person does not choose: mission `{content['default_mission']}`, therapeutic area `{content['default_ta']}`.",
         f"4. Read only the inputs that mission lists (replace {{ta}} with oncology-mm, immunology-ad or cardiometabolic-obesity). Every dataset with raw links: {abs_('datasets.json')}. Datasets live in {cfg['datasets_source']['repo_url']} (synthetic/index.json lists every synthetic file).",
         f"5. Load the skills the mission names, plus medical-affairs-foundations (always) and each skill's `requires`. Skill list: {abs_('skills.json')} or {raw('SKILLS-INDEX.md')}.",
         "6. Read house-rules/<skill-name>.md for each selected skill. Rules the person gives you in conversation also apply.",
         "7. Do the work: inventory inputs, retrieve public evidence only when useful (record queries and dates), analyze, then challenge your own draft with deliverable-quality-review.",
         "8. Deliver designed files where your host can (Word + PDF for documents, PowerPoint + PDF for decks, using the skill's scripts/ma_render.py). If you cannot create files, give the complete structured content in your reply and say so.",
         "", "## If the person gives you a vague request",
         f"Turn it into an assignment before you start, using the Prompt Optimizer structure in {abs_('prompts.json')} (`optimizer`): role, goal (end state), audience, context, steps, house rules, deliverable, proof of done, and when to stop for a human. Ready-made assignments for each hackathon team are under `library`.",
         f"On the hosted site you can also POST JSON {{\"goal\": \"<short goal>\", \"mode\": \"single\" or \"swarm\", \"ta\": \"oncology-mm|immunology-ad|cardiometabolic-obesity|own\"}} to {abs_('api/optimize')} and get back an AI-written assignment for Grok Bot or an agent swarm (plain text, streamed). If it answers with an error, use the optimizer structure above.",
         "", "## If you cannot open GitHub", "Ask the person to upload one self-contained starter file:"]
    L += [f"- {t['short']}: {raw('workshop/bundles/first-mission-' + t['id'] + '.md')}" for t in TAS]
    L += [f"- Whole repository ZIP: {R['zip_url']}", "", "If you have a shell:", "```bash", f"git clone {R['url']}.git", "cd Medical-Affairs-Skills",
          "python3 scripts/workshop.py list", "python3 scripts/workshop.py start --mission field-insights --ta oncology-mm", "```", "",
          "## Starter prompt (from the repository README)", "```text", content["starter_prompt"], "```", "", "## Workshop missions", ""]
    L += [f"- `{m['id']}` ({m['title']}): {m['objective']} Deliverables: {'; '.join(m['deliverables'])}. Skills: {', '.join(m['skills'])}." for m in content["missions"]]
    L += ["", "## Team missions (30 minutes each)", ""]
    L += [f"- Mission {m['number']}, {m['function']}: {m['mission']} Brief: {raw(m['path'])}. Round 2 house rules: {m['house_rules_file']}." for m in content["team_missions"]]
    L += ["", "## Event teams", ""] + [f"- {t['name']}: {t['blurb']} Start with: {', '.join(t['team_missions'] + t['missions'])}." for t in TEAMS]
    ps = content.get("public_sources") or {"counts": {"sources": 0}}
    L += ["", "## Data: two repositories, two truth statuses",
          f"- Synthetic workshop data: {cfg['datasets_source']['repo_url']} `synthetic/` (index: {cfg['datasets_source']['raw_base']}synthetic/index.json). Clone it into the skills repo as `Data-Sources/` so paths like `Data-Sources/synthetic/oncology-mm/product-profile.md` resolve, or read the raw links.",
          f"- Real public sources: {ps['counts']['sources']} cataloged in {cfg['datasets_source']['raw_base']}public/catalog.json (grouped by Medical Affairs workflow, top 15 ranked). Respect `rate_limit` and `data_policy`; never copy data from a `link-only` source.",
          f"- Clone both: `git clone {R['url']}.git && cd Medical-Affairs-Skills && git clone {cfg['datasets_source']['repo_url']}.git Data-Sources`"]
    L += ["", "## Rules you must keep",
          "- Workshop data is synthetic and fictional (Nordvant Biopharma; NORVANTIB, DERMALYX, ADIPOSYN). Mark outputs SYNTHETIC and DRAFT.",
          "- Keep real public evidence separate from fictional workshop facts. Never cite real papers as evidence for fictional products.",
          "- Scan human-sourced records for possible safety findings before analysis. In the workshop these are simulated; never enter them into real reporting systems.",
          "- Do not ask the person to connect company systems. Do not send, publish, post or update external systems.",
          "- Never claim a search, script or file happened if it did not. State what you could not do and finish the supported work.",
          "- Outputs are drafts requiring qualified human review. The human is the final judge.", "",
          f"Source: {R['url']} at commit {content['source_commit']} ({content['source_date']}). Apache-2.0.", ""]
    md = "\n".join(L)
    # wrap bare URLs as <autolinks> outside code fences so trailing punctuation is never read as part of a link
    parts = md.split("```")
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"(?<![<(])(https?://[^\s<>()]+?)([.,;:]?)(?=\s|$)", r"<\1>\2", parts[i])
    out["agents.md"] = "```".join(parts)
    cfg["_agents_md"] = out["agents.md"]
    out["llms.txt"] = "\n".join([f"# {ev['name']}", "",
        f"> Companion site for {ev['name']} ({ev['dates']}, {ev['venue']}, {ev['address']}). It turns the open Medical-Affairs-Skills and Data-Sources repositories into copy-ready prompts, missions, datasets and a prompt optimizer for non-technical Medical Affairs professionals and their AI agents. Grok Bot is the event sandbox. All workshop data is synthetic.", "",
        f"Agents: follow the Instructions for agents at {abs_('agents.md')}. In short: read this site and its two repositories, greet the user, ASK what they want to do from a numbered menu (set up an agent, run a mission or skill, build the launch-planning swarm, practise on synthetic data, find public data sources, write or optimize a prompt, prepare for the hackathon team challenge, or something else), then do it step by step. The human is the final judge; workshop data is fictional; never send or publish anything without the user's say-so.", "",
        "## Start here", f"- [Agent instructions]({abs_('agents.md')}): how to run a mission end to end", f"- [Repository]({R['url']}): the source of truth",
        f"- [AGENTS.md (raw)]({raw('AGENTS.md')}): the repository's own agent entry point", "",
        "## Data repository",
        f"- [Data-Sources]({cfg['datasets_source']['repo_url']}): SYNTHETIC workshop datasets and a catalog of {(content.get('public_sources') or {'counts': {'sources': 0}})['counts']['sources']} REAL public sources (separate truth statuses)",
        f"- [synthetic/index.json]({cfg['datasets_source']['raw_base']}synthetic/index.json): every synthetic file with product, therapeutic area and which skills/missions use it",
        f"- [public/catalog.json]({cfg['datasets_source']['raw_base']}public/catalog.json): public sources with access, rate limits, licences and data_policy (link-only = do not copy)",
        f"- [manifest.json]({REL}manifest.json): every dataset with a direct_url. Agents fetch data straight from these URLs onto their own machine (follow redirects; unzip ZIPs); skip link-only entries and use them at the official site. Everything at once: [all-synthetic-data.zip]({REL}all-synthetic-data.zip), [all-data-catalog.zip]({REL}all-data-catalog.zip)", "",
        "## Machine-readable data",
        f"- [missions.json]({abs_('missions.json')}): {len(content['missions'])} catalog missions and {len(content['team_missions'])} team missions with prompts per therapeutic area",
        f"- [datasets.json]({abs_('datasets.json')}): every synthetic data pack (badged synthetic) and every public source, with raw links",
        f"- [skills.json]({abs_('skills.json')}): all {content['skill_count']} skills with summaries and links",
        f"- [prompts.json]({abs_('prompts.json')}): every prompt on the site, the Prompt Optimizer templates and the team prompt library", "",
        f"- [Skill creator]({site}/optimizer): describe a workflow the library does not cover and get a skill pack (single skill, or a group with a lead skill) in the Medical-Affairs-Skills format; API: POST {abs_('api/skills')} then {abs_('api/skills/zip')}",
        "## Starter files (for agents that cannot open GitHub)"] +
        [f"- [{t['short']} starter]({raw('workshop/bundles/first-mission-' + t['id'] + '.md')})" for t in TAS] +
        ["", "## Optional", f"- [Skills index]({raw('SKILLS-INDEX.md')})", f"- [Participant quickstart]({raw('workshop/PARTICIPANT-QUICKSTART.md')})",
         f"- [Workshop catalog]({raw('workshop/catalog.json')})", ""])
    out["index.html"] = render_html(content, cfg, lib)
    return out

# ---------------------------------------------------------------- html pieces

class Ids:
    n = 0
    @classmethod
    def next(cls, p="t"):
        cls.n += 1
        return f"{p}{cls.n}"

ICON_COPY = '<svg class="i-copy" aria-hidden="true"><use href="#ic-copy"/></svg><svg class="i-check" aria-hidden="true"><use href="#ic-check"/></svg>'
SPRITE = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true">'
          '<symbol id="ic-copy" viewBox="0 0 24 24"><rect x="9" y="9" width="11" height="11" rx="2.5"/><path d="M5 15V6.5A2.5 2.5 0 0 1 7.5 4H15"/></symbol>'
          '<symbol id="ic-check" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></symbol></svg>')

def copy_btn(target, label, cls="btn-copy", visible="Copy"):
    return f'<button type="button" class="{cls}" data-copy="#{target}" aria-label="{e(label)}">{ICON_COPY}<span class="lbl">{e(visible)}</span></button>'

def prompt_block(text, label, title=None, compact=False, dark=False):
    pid = Ids.next("p")
    if isinstance(text, dict):
        default, data = text["default"], f' data-ta-tpl="{e(text["tpl"])}"'
    else:
        default, data = text, ""
    cls = "prompt" + (" prompt--compact" if compact else "") + (" prompt--dark" if dark else "")
    if title:
        head = f'<div class="prompt-head"><span class="prompt-title">{e(title)}</span>{copy_btn(pid, "Copy " + label)}</div>'
        return f'<figure class="{cls}">{head}<pre id="{pid}" class="prompt-text"{data}><code>{e(default)}</code></pre></figure>'
    if compact:
        return f'<figure class="{cls}"><pre id="{pid}" class="prompt-text"{data}><code>{e(default)}</code></pre>{copy_btn(pid, "Copy " + label, "btn-copy btn-copy--float")}</figure>'
    return (f'<figure class="{cls}"><pre id="{pid}" class="prompt-text"{data}><code>{e(default)}</code></pre>'
            f'<div class="prompt-foot">{copy_btn(pid, "Copy " + label, "btn-copy btn-copy--solid", "Copy prompt")}</div></figure>')

def placeholder(value, label, kind):
    if value:
        if kind == "url":
            return f'<a class="ph ph--live" href="{e(value)}" target="_blank" rel="noopener">{e(value)}</a>'
        pid = Ids.next("c")
        return f'<span class="ph ph--live"><code id="{pid}">{e(value)}</code>{copy_btn(pid, "Copy credits code", "btn-copy btn-copy--mini")}</span>'
    return f'<span class="ph" role="note"><span class="ph-dot" aria-hidden="true"></span>{e(label)}</span>'

def file_row(cfg, f):
    l = ds_links(cfg, f["path"]); rid = Ids.next("r")
    meta = ([f"{f['rows']} rows"] if f.get("rows") is not None else []) + [f["format"]]
    return (f'<li class="file"><div class="file-main"><span class="file-name">{e(f["name"])}</span><span class="file-desc">{e(f["title"])}</span></div>'
            f'<div class="file-meta">{"".join(f"<span>{e(m)}</span>" for m in meta)}</div>'
            f'<div class="file-actions"><a href="{e(l["url"])}" target="_blank" rel="noopener" aria-label="View {e(f["name"])} on GitHub">View</a>'
            f'<span id="{rid}" hidden>{e(l["raw"])}</span>{copy_btn(rid, "Copy raw link for " + f["name"], "btn-copy btn-copy--mini", "Raw link")}</div></li>')

def optimizer_html(cfg, lib):
    od = optimizer_data(cfg)
    first = OPT_TYPES[1]
    types = "".join(f'<button type="button" role="radio" class="opt-type" data-type="{t["id"]}" aria-checked="{"true" if t is first else "false"}" tabindex="{0 if t is first else -1}">{e(t["label"])}</button>' for t in OPT_TYPES)
    tas = ('<option value="own" selected>My own data (describe it under Context)</option><option value="none">No data yet</option><optgroup label="Practice data (fictional Nordvant Biopharma)">'
           + "".join(f'<option value="{t["id"]}">{e(t["short"])} · {e(t["product"])}</option>' for t in TAS) + "</optgroup>")
    fields = "".join(f'<label class="fld"><span class="fld-l">{e(f["label"])}</span><span class="fld-h" id="h-{f["id"]}">{e(f["hint"])}</span>'
                     f'<textarea name="{f["id"]}" rows="{f["rows"]}" aria-describedby="h-{f["id"]}">{e(first["defaults"][f["id"]])}</textarea></label>' for f in OPT_FIELDS)
    out_default = compose_prompt(first["id"], {}, "own", "markdown", cfg["repo"]["url"])
    libhtml = ""
    for it in lib:
        pid = Ids.next("lib")
        ta = TA_BY_ID.get(it["ta"], {}).get("short", "")
        libhtml += (f'<article class="lib"><p class="kicker">{e(it["label"])} · {e(ta)}</p><h4>{e(it["team"])}</h4>'
                    f'<p class="lib-goal">{e(it["fields"].get("goal") or next(x for x in OPT_TYPES if x["id"] == it["type"])["defaults"]["goal"])}</p>'
                    f'<p class="lib-skills">{" · ".join(e(x) for x in next(x for x in OPT_TYPES if x["id"] == it["type"])["skills"])}</p>'
                    f'<pre id="{pid}" class="lib-text" hidden data-dialects="{e(json.dumps(it["prompts"], ensure_ascii=False))}"><code>{e(it["prompts"]["markdown"])}</code></pre>'
                    f'<div class="lib-actions">{copy_btn(pid, "Copy " + it["team"] + " assignment", "btn-copy btn-copy--solid", "Copy")}'
                    f'<button type="button" class="btn-ghost" data-load-lib="{e(it["id"])}">Open in optimizer</button></div></article>')
    data = json.dumps(od, ensure_ascii=False).replace("</", "<\\/")
    return f'''
<section id="optimizer" class="section section--opt" aria-labelledby="opt-h">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">Prompt Optimizer</p><h2 id="opt-h">Turn a question into <em>an assignment</em>.</h2>
    <p class="sec-sub">Pick the task, answer a few plain questions, and copy a goal-oriented assignment your agent can execute. The AI optimizer sends only your short goal (and, if you add one, your short data description) to this site’s server, which asks the Venice API to write the assignment. The template builder below runs entirely in your browser. Every assignment covers role, end goal, steps, narrowing, proof of done and stop conditions.</p></div>
    <div class="opt" id="opt">
      <form class="opt-form" aria-label="Prompt optimizer inputs" onsubmit="return false">
        <fieldset><legend class="fld-l">1 · The task</legend><div class="opt-types" role="radiogroup" aria-label="Task type">{types}</div></fieldset>
        <div class="opt-row">
          <label class="fld"><span class="fld-l">2 · Data <span class="muted">(optional)</span></span><select name="ta">{tas}</select></label>
          <label class="fld"><span class="fld-l">Format</span><select name="dialect"><option value="markdown">Universal (Markdown)</option><option value="xml">Claude-style (XML tags)</option></select></label>
        </div>
        <p class="fld-l fld-l--sec">3 · Make it yours <span class="muted">(prefilled with a strong default, edit freely)</span></p>
        {fields}
        <button type="button" class="btn-ghost" id="opt-reset">Reset to defaults</button>
      </form>
      <div class="opt-out">
        <div class="opt-out-in">
          <div class="prompt-head prompt-head--dark"><span class="prompt-title">Your optimized assignment</span><span class="opt-meter" id="opt-meter" aria-live="polite"></span>{copy_btn("opt-text", "Copy optimized assignment", "btn-copy btn-copy--solid", "Copy")}</div>
          <pre id="opt-text" class="prompt-text" tabindex="0" aria-label="Optimized assignment"><code>{e(out_default)}</code></pre>
        </div>
      </div>
    </div>
    <h3 class="sub-h">Ready-made assignments for the hackathon teams</h3>
    <div class="libs">{libhtml}</div>
    <script type="application/json" id="opt-data">{data}</script>
  </div>
</section>'''

def render_html(content, cfg, lib):
    R = cfg["repo"]; ev = cfg["event"]; gb = cfg["grokbot"]
    raw = lambda p: repo_url(cfg, p, True)
    blob = lambda p: repo_url(cfg, p)
    nm = len(content["missions"]); ns = content["skill_count"]
    missions_by_id = {m["id"]: m for m in content["missions"]}
    team_by_id = {m["id"]: m for m in content["team_missions"]}
    repo_id = Ids.next("repo")
    starter = prompt_block(content["starter_prompt"], "starter prompt")
    give_text = ("Read {SITE}agents.md and follow it step by step.\n"
                 "It explains how to use the Medical-Affairs-Skills repository and run a\n"
                 "workshop mission with synthetic data. Start with the oncology\n"
                 "field-insights mission unless I choose another.")
    site = (cfg.get("site_url") or "").rstrip("/")
    give_default = give_text.replace("{SITE}", site + "/" if site else "[this site’s address]/")

    ta_switch = ('<div class="ta-switch" role="radiogroup" aria-label="Therapeutic area for all prompts">' +
                 "".join(f'<button type="button" role="radio" aria-checked="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" data-ta="{t["id"]}">'
                         f'<span class="ta-name">{t["short"]}</span><span class="ta-prod">{t["product"]}</span></button>' for i, t in enumerate(TAS)) + '</div>')
    ma_context = ["Field insights", "KOL conversations", "MI enquiries", "Congress intelligence", "Publications", "Advisory boards",
                  "Real-world evidence", "Safety signals", "Guidelines", "Medical plans", "Payer & HTA evidence", "Patient voice"]
    day1 = [("7:45 AM", "Registration & breakfast", ""), ("8:30 AM", "Opening keynote & sandbox intro", ev["host"]),
            ("11:15 AM", "Team creation & function audit", ""), ("1:45 PM", "Build the AI worker", ""), ("5:00 PM", "Cocktail reception", "")]
    day2 = [("8:00 AM", "Breakfast", ""), ("9:00 AM", "Hackathon + demo presentations", ""), ("11:00 AM", "Interactive demo by WPP", ""),
            ("11:50 AM", "Closing panel & deployment commitment", ""), ("1:30 PM", "Event ends", "")]
    day = lambda items: "".join(f'<li><time>{t}</time><div><span class="ag-title">{e(a)}</span>{f"<span class=ag-sub>{e(b)}</span>" if b else ""}</div></li>' for t, a, b in items)

    teams_html = ""
    for i, t in enumerate(TEAMS):
        links = [f'<a href="#{m}">Mission {team_by_id[m]["number"]} · {e(team_by_id[m]["function"])}</a>' for m in t["team_missions"]]
        links += [f'<a href="#m-{m}">{e(missions_by_id[m]["title"])}</a>' for m in t["missions"] if m in missions_by_id]
        teams_html += (f'<article class="team reveal"><span class="team-n">0{i+1}</span><h3>{e(t["name"])}</h3><p>{e(t["blurb"])}</p>'
                       f'<div class="team-links"><span class="kicker">Good places to start</span>{"".join(links)}</div></article>')

    tm_html = ""
    for m in content["team_missions"]:
        pushes = "".join(prompt_block(p, "follow-up question", compact=True) for p in m["push"])
        inputs = "".join(f'<li><code>{e(i["file"])}</code><span>{e(i["what"])}</span></li>' for i in m["inputs"])
        tm_html += f'''
<article class="tm reveal" id="{m['id']}">
  <header class="tm-head"><span class="tm-num">{m['number']:02d}</span><div><p class="kicker">{e(m['function'])} · {e(m['timebox'])}</p>
  <h3><span class="tm-emoji" aria-hidden="true">{e(m['emoji'])}</span>{e(m['headline'])}</h3></div></header>
  <p class="tm-mission">{e(m['mission'])}</p>
  {prompt_block(ta_tpl(team_prompt, cfg, m), "mission " + str(m['number']) + " prompt")}
  <details class="more"><summary>What “done” looks like, inputs and Round 2</summary>
    <div class="more-body">
      <p>{e(m['done'])}</p>
      <h4>What you have</h4><ul class="inputs">{inputs}</ul>
      <h4>When it finishes, push on it</h4>{pushes}
      <h4>Round 2 · teach it your house rules</h4>
      <p class="muted">Your file is <a href="{e(blob(m['house_rules_file']))}" target="_blank" rel="noopener"><code>{e(m['house_rules_file'])}</code></a>. {e(m['think_about'])}</p>
      {prompt_block(round2_prompt(m), "round 2 prompt", compact=True)}
      <p class="src"><a href="{e(blob(m['path']))}" target="_blank" rel="noopener">Open the full brief on GitHub ↗</a></p>
    </div></details>
</article>'''

    cm_html = ""
    for i, m in enumerate(content["missions"]):
        inputs = "".join(f'<li><code data-ta-path="{e(p)}">{e(p.replace("{ta}", "oncology-mm"))}</code></li>' for p in m["inputs"])
        cm_html += f'''
<article class="mc reveal" id="m-{m['id']}">
  <div class="mc-top"><span class="mc-n">{i+1:02d}</span><code class="mc-id">{e(m['id'])}</code></div>
  <h3>{e(m['title'])}</h3>
  <p class="mc-obj">{e(m['objective'])}</p>
  <ul class="chips" aria-label="Deliverables">{"".join(f"<li>{e(d)}</li>" for d in m['deliverables'])}</ul>
  {prompt_block(ta_tpl(mission_prompt, cfg, m), m['title'] + " prompt", compact=True)}
  <details class="more more--small"><summary>Skills and input files</summary><div class="more-body">
    <p class="muted">Skills: {", ".join(f"<code>{e(s)}</code>" for s in m['skills'])}</p><ul class="inputs inputs--plain">{inputs}</ul></div></details>
</article>'''

    say_html = ""
    for s in content["say_this"]:
        pid = Ids.next("s"); v = ta_tpl(say_prompt, cfg, s)
        say_html += (f'<li class="say"><div><p class="say-q">“{e(s["ask"])}”</p><p class="say-a">{e(s["prepares"])}</p></div>'
                     f'<pre id="{pid}" hidden data-ta-tpl="{e(v["tpl"])}">{e(v["default"])}</pre>'
                     f'{copy_btn(pid, "Copy prompt: " + s["ask"], "btn-copy btn-copy--ghost")}</li>')
    more_prompts = (prompt_block(content["capstone_prompt"], "capstone prompt", "Capstone · run the next 30 days") +
                    prompt_block(content["change_prompt"], "change card prompt", "When a change card arrives") +
                    prompt_block(content["msl_prompt"], "MSL pre-call prompt", "MSL · prepare my next HCP engagement"))
    nexts = "".join(f'<li><span>{e(p)}</span><span id="n{i}" hidden>{e(p)}</span>{copy_btn(f"n{i}", "Copy: " + p, "btn-copy btn-copy--mini")}</li>'
                    for i, p in enumerate(content["next_moves"] + content["recovery_prompts"]))
    cards = "".join(f'<li><a href="{e(blob(c["path"]))}" target="_blank" rel="noopener">{e(c["headline"])}</a><span>{e(c["works_with"])}</span></li>' for c in content["change_cards"])

    hiw = "".join(f'<li class="reveal"><span class="hiw-n">{i+1}</span><h4>{e(s["title"])}</h4><p>{e(s["text"])}</p></li>' for i, s in enumerate(content["how_it_works"]))
    cc = content["connected_counts"]

    skills_html = ""
    for g in content["skill_groups"]:
        skills_html += f'<details class="sg"><summary><span>{e(g["title"])}</span><span class="count">{len(g["skills"])}</span></summary><ul class="skill-list">'
        for s in g["skills"]:
            skills_html += (f'<li data-skill="{e(s["name"])} {e(s["summary"].lower())}"><a href="{e(blob(s["path"]))}" target="_blank" rel="noopener"><code>{e(s["name"])}</code></a>'
                            f'<p>{e(s["summary"])}</p></li>')
        skills_html += "</ul></details>"

    packs = [g for g in content["datasets"] if g["kind"] == "therapeutic-area-pack"]
    others = [g for g in content["datasets"] if g["kind"] != "therapeutic-area-pack"]
    tabs = '<div class="tabs" role="tablist" aria-label="Therapeutic area data packs">' + "".join(
        f'<button role="tab" type="button" id="tab-{g["ta"]}" aria-controls="panel-{g["ta"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{e(TA_BY_ID[g["ta"]]["short"])}<span>{e(TA_BY_ID[g["ta"]]["product"])}</span></button>'
        for i, g in enumerate(packs)) + "</div>"
    panels = ""
    for i, g in enumerate(packs):
        allid = Ids.next("all")
        all_raw = "\n".join(ds_links(cfg, f["path"])["raw"] for c in g["categories"] for f in c["files"])
        cats = "".join(f'<div class="cat"><h4>{e(c["title"])} <span class="count">{len(c["files"])}</span></h4><ul class="files">{"".join(file_row(cfg, f) for f in c["files"])}</ul></div>' for c in g["categories"])
        panels += (f'<div class="panel" role="tabpanel" id="panel-{g["ta"]}" aria-labelledby="tab-{g["ta"]}" tabindex="0"{"" if i == 0 else " hidden"}>'
                   f'<div class="panel-head"><div><h3>{e(g["title"])} <span class="badge badge--syn">Synthetic</span></h3><p class="muted">{e(g["subtitle"])} · {g["count"]} files</p></div>'
                   f'<div class="panel-actions"><a class="btn-ghost" href="{e(ds_folder(cfg, g["folder"]))}" target="_blank" rel="noopener">Open folder ↗</a>'
                   f'<pre id="{allid}" hidden>{e(all_raw)}</pre>{copy_btn(allid, "Copy all raw links for " + g["title"], "btn-copy btn-copy--solid", "Copy all " + str(g["count"]) + " links")}</div></div>'
                   f'<div class="cats">{cats}</div></div>')
    other_html = ""
    for g in others:
        files = [f for c in g["categories"] for f in c["files"]]
        allid = Ids.next("all")
        all_raw = "\n".join(ds_links(cfg, f["path"])["raw"] for f in files)
        badge = ('<span class="badge badge--real">Real public metadata</span>' if g["kind"] == "real-public-metadata"
                 else '<span class="badge badge--syn">Synthetic</span>' if g["kind"] in ("practice-organization", "starter-bundle", "exercise") else "")
        other_html += (f'<details class="dg"{" open" if g["id"] == "connected-organization" else ""}><summary><div><h3>{e(g["title"])} {badge}</h3><p class="muted">{e(g["subtitle"])}</p></div><span class="count">{len(files)}</span></summary>'
                       f'<div class="dg-body"><div class="panel-actions"><a class="btn-ghost" href="{e(ds_folder(cfg, g["folder"]))}" target="_blank" rel="noopener">Open folder ↗</a>'
                       f'<pre id="{allid}" hidden>{e(all_raw)}</pre>{copy_btn(allid, "Copy all raw links for " + g["title"], "btn-copy", "Copy all links")}</div>'
                       f'<ul class="files">{"".join(file_row(cfg, f) for f in files)}</ul></div></details>')
    ds_cfg = cfg["datasets_source"]
    repo_rows = [("Data-Sources", ds_cfg["repo_url"], "Synthetic datasets + public source catalog"), ("Medical-Affairs-Skills", R["url"], "Skills, missions, house rules")]
    gd_big_html = gd_big()
    ds_repos_html = '<div class="repo-links">' + "".join(
        (lambda rid: f'<div class="repo-link"><div><span class="kicker">{e(lbl)}</span><code id="{rid}">{e(url)}</code><span class="muted">{e(sub)}</span></div>'
                     f'<div class="repo-link-act"><a class="btn-ghost" href="{e(url)}" target="_blank" rel="noopener">Open ↗</a>{copy_btn(rid, "Copy " + lbl + " link", "btn-copy btn-copy--solid", "Copy link")}</div></div>')(Ids.next("rl"))
        for lbl, url, sub in repo_rows) + '</div>'
    ps = content.get("public_sources")
    pub_html = ""
    if ps:
        by = {x["id"]: x for x in ps["sources"]}
        POL = {"open": ("pol pol--open", "Open"), "check-terms": ("pol pol--check", "Check terms"), "link-only": ("pol pol--link", "Link only · do not copy data")}
        def pol(x):
            c_, t_ = POL[x["data_policy"]]; return f'<span class="{c_}" title="{e(x["data_policy_note"])}">{e(t_)}</span>'
        top = "".join(f'<li class="top"><span class="top-n">{x["rank"]:02d}</span><div><a href="{e(x["url"])}" target="_blank" rel="noopener" class="top-name">{e(x["name"].split(" (")[0])}</a>'
                      f'<p>{e(x.get("why_top15", ""))}</p><div class="top-tags">{pol(x)}{"<span class=pol>JSON API</span>" if x["agent_readiness"]["json_api"] else ""}</div></div></li>'
                      for x in (by[i] for i in ps["top15"]))
        groups = ""
        for g in ps["groups"]:
            rows = ""
            for i in g["source_ids"]:
                x = by[i]
                star = f'<span class="badge badge--top">Top {x["rank"]}</span>' if x["rank"] else ""
                used = '<span class="badge badge--used">In the skills</span>' if x["already_used_by_skills"] else ""
                cav = (f'<span class="src-cav">{e(x["data_policy_note"])}</span>' if x["data_policy"] != "open" else "")
                rows += (f'<li class="src"><div class="src-main"><span class="src-name">{e(x["name"])} {star}{used}</span><span class="src-desc">{e(x["contents"])}</span>{cav}</div>'
                         f'<div class="src-meta">{pol(x)}</div>'
                         f'<div class="file-actions"><a href="{e(x["url"])}" target="_blank" rel="noopener">Open</a><a href="{e(x["api_docs"])}" target="_blank" rel="noopener">Docs</a></div></li>')
            n_lo = sum(by[i]["data_policy"] == "link-only" for i in g["source_ids"])
            groups += (f'<details class="dg"><summary><div><h3>{e(g["title"])}</h3><p class="muted">{e(g["medical_affairs_jobs"])}'
                       f'{f" · {n_lo} link-only" if n_lo else ""}</p></div><span class="count">{len(g["source_ids"])}</span></summary>'
                       f'<div class="dg-body"><ul class="files">{rows}</ul></div></details>')
        cid = Ids.next("cat")
        pub_html = (f'<div class="pub" id="public-sources"><div class="pub-head"><div><p class="kicker">Public sources · real data</p>'
                    f'<h3 class="ds-h">{ps["counts"]["sources"]} public sources, <em>grouped by Medical Affairs workflow</em> <span class="badge badge--real">Real public data</span></h3>'
                    f'<p class="muted">Real and free, from regulators, registries and journals. Linked, never copied. {ps["counts"]["already_used_by_skills"]} are already wired into the skills; '
                    f'{ps["counts"]["link_only"]} are <strong>link only</strong> because their licences restrict copying or commercial use. Checked {e(ps["verified_on"])}.</p></div>'
                    f'<div class="panel-actions"><a class="btn-ghost" href="{e(ds_cfg["blob_base"] + "public/catalog.md")}" target="_blank" rel="noopener">Full catalog ↗</a>'
                    f'<span id="{cid}" hidden>{e(ds_cfg["raw_base"] + "public/catalog.json")}</span>{copy_btn(cid, "Copy raw link to catalog.json", "btn-copy btn-copy--solid", "Copy catalog.json link")}</div></div>'
                    f'<p class="pol-legend"><span class="pol pol--open">Open</span> free with attribution <span class="pol pol--check">Check terms</span> read the licence first <span class="pol pol--link">Link only · do not copy data</span> point to it, never copy it</p>'
                    f'<h4 class="mini-h">Top 15 to start with</h4><ol class="tops">{top}</ol>'
                    f'<h4 class="mini-h">All {ps["counts"]["sources"]}, by workflow</h4><div class="dgs">{groups}</div></div>')
    bundles = "".join(f'<li><a href="{e(blob("workshop/bundles/first-mission-" + t["id"] + ".md"))}" target="_blank" rel="noopener">{t["short"]} starter</a>'
                      f'<span id="b-{t["id"]}" hidden>{e(raw("workshop/bundles/first-mission-" + t["id"] + ".md"))}</span>{copy_btn("b-" + t["id"], "Copy raw link to " + t["short"] + " starter", "btn-copy btn-copy--mini", "Raw link")}</li>' for t in TAS)

    nav = [("start", "Start"), ("agenda", "Agenda"), ("ideas", "Ideas"), ("inside", "Inside"), ("missions", "Missions"),
           ("prompts", "Prompts"), ("optimizer", "Optimizer"), ("data", "Data"), ("grokbot", "Grok Bot"), ("agents", "For agents")]
    navhtml = "".join(f'<a href="#{a}"' + (' class="nav-agents"' if a == "agents" else "") + f'>{b}</a>' for a, b in nav)
    jsonld = json.dumps({"@context": "https://schema.org", "@type": "Event", "name": ev["name"], "startDate": "2026-10-13T07:45:00-04:00",
                         "endDate": "2026-10-14T13:30:00-04:00", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                         "location": {"@type": "Place", "name": "Convene, Two Commerce Square", "address": ev["address"]},
                         "organizer": {"@type": "Organization", "name": ev["organizer"]}, "performer": {"@type": "Person", "name": ev["host"]}}, ensure_ascii=False)
    copy = copy_btn(repo_id, "Copy repository link", "btn-copy btn-copy--solid", "Copy")
    give_copy = copy_btn("give", "Copy instructions for your agent", "btn-copy btn-copy--solid", "Copy")
    agent_site = cfg.get("site_url", "").rstrip("/")
    paste = PASTE_TEMPLATE.format(site=agent_site or "this page")
    paste_copy = copy_btn("ap-paste", "Copy the sentence for your agent", "btn-copy btn-copy--solid", "Copy")
    playbook_md = e(cfg.get("_agents_md", ""))
    signup = placeholder(gb.get("signup_url"), gb["signup_label"], "url")
    credits = placeholder(gb.get("credits_code"), gb["credits_label"], "code")
    return TEMPLATE.format(sprite=SPRITE, **{k: v for k, v in locals().items() if k not in ('ev', 'R', 'gb')}, opt=optimizer_html(cfg, lib), hr=content["house_rules_count"],
                           commit=(f" at {e(content['source_commit'])}, {e(content['source_date'])}" if content["source_commit"] else ""),
                           ctx="".join(f"<li>{e(c)}</li>" for c in ma_context), ifm="".join(f"<li>{e(x)}</li>" for x in content["if_missing"]),
                           d1=day(day1), d2=day(day2), give_tpl=e(give_text), give_def=e(give_default),
                           E={k: e(v) for k, v in ev.items()}, RU=e(R["url"]), ZIP=e(R["zip_url"]), HR_README=e(blob("house-rules/README.md")),
                           GB_AGENTS=e(blob("workshop/grokbot-agents.json")), DS_URL=e(cfg["datasets_source"]["repo_url"]), NPUB=(content.get("public_sources") or {"counts": {"sources": 0}})["counts"]["sources"], DOCS_AGENTS=e(blob("docs/agents.md")), AGENTS_RAW=e(raw("AGENTS.md")),
                           HCPS=cc.get("hcps", ""), INTER=cc.get("interactions", ""))

TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E[name]} · Oct 13–14, 2026 · Philadelphia</title>
<meta name="description" content="Companion site for {E[name]}. Copy-ready prompts, {nm} workshop missions, {ns} Medical Affairs skills, a prompt optimizer and synthetic datasets for you and your AI agent. AI agents: read /agents.md (Instructions for agents) and follow it.">
<meta name="agent-instructions" content="/agents.md">
<meta name="theme-color" content="#F6F8F8">
<link rel="alternate" type="text/markdown" href="/agents.md" title="Instructions for agents">
<link rel="alternate" type="text/plain" href="/llms.txt" title="llms.txt">
<link rel="alternate" type="application/json" href="missions.json" title="Missions">
<link rel="alternate" type="application/json" href="datasets.json" title="Datasets">
<link rel="alternate" type="application/json" href="prompts.json" title="Prompts and optimizer templates">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..700&family=Geist+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css">
<link rel="stylesheet" href="assets/ai-optimizer.css">
<link rel="stylesheet" href="assets/get-data.css">
<link rel="stylesheet" href="assets/agents-panel.css">
<script type="application/ld+json">{jsonld}</script>
</head>
<body>
<!-- AI agents: Instructions for agents are at /agents.md (plain text; also /llms.txt). Read them, greet the user, ask what they want to do from the menu, then do it. Missions, datasets, skills and prompts are at missions.json, datasets.json, skills.json and prompts.json. -->
{sprite}<a class="skip" href="#main">Skip to content</a>
<div class="grain" aria-hidden="true"></div>

<header class="nav" id="top">
  <div class="nav-in">
    <a class="brand" href="#top" aria-label="{E[name]}, back to top"><span class="brand-mark" aria-hidden="true"><svg viewBox="0 0 32 32"><path d="M8 21l5-10 4 7 2-3 4 6"/></svg></span><span class="brand-t">AI in Action<span class="brand-sub">for Medical Affairs</span></span></a>
    <nav aria-label="Sections" class="nav-links">{navhtml}</nav>
    <a class="nav-cta" href="#start">Start now</a>
  </div>
</header>

<main id="main">

<section class="hero" aria-labelledby="hero-h">
  <div class="aurora" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="wrap hero-grid">
    <div class="hero-main">
    <p class="eyebrow reveal"><span class="pulse" aria-hidden="true"></span>Oct 13–14, 2026 · Convene, Philadelphia</p>
    <h1 id="hero-h" class="reveal">Stop asking AI questions.<br><em>Start giving it tasks.</em></h1>
    <p class="lede reveal">The companion to <strong>{E[name]}</strong>. Everything you need to give your agent a real Medical Affairs goal, with {ns} open skills, {nm} missions and a fictional pharma company’s data. No coding. No company systems.</p>
    <div class="hero-cta reveal"><a class="btn-primary" href="#start">Start in three steps</a><a class="btn-ghost" href="#optimizer">Optimize a prompt</a></div>
    <p class="pd-note reveal"><span class="pd-dot" aria-hidden="true"></span>Practice data is fictional and for learning; for real work, bring your own data.</p>
    <dl class="stats reveal">
      <div><dt>Skills</dt><dd>{ns}</dd></div>
      <div><dt>Missions</dt><dd>{nm}</dd></div>
      <div><dt>Therapeutic areas</dt><dd>3</dd></div>
      <div><dt>Company data needed to start</dt><dd>0</dd></div>
    </dl>
    </div>
    <aside class="ap reveal" id="for-agents" aria-labelledby="ap-h">
      <p class="ap-label"><span class="ap-dot" aria-hidden="true"></span>Instructions for agents</p>
      <h2 class="ap-h" id="ap-h">Point your agent at this page and it will take it from here.</h2>
      <div class="ap-paste"><p class="ap-paste-l">Paste this into Grok Bot or any agent</p>
        <div class="ap-paste-row"><code id="ap-paste">{paste}</code>{paste_copy}</div></div>
      <p class="ap-sub">What the agent does</p>
      <ol class="ap-steps">
        <li>Reads this site, the skills library and the data repository.</li>
        <li>Greets you and asks what you want to do, from a numbered menu.</li>
        <li>States a plan and loads the right skills and data.</li>
        <li>Stops for your judgment at every checkpoint.</li>
        <li>Hands back the finished deliverable. You decide.</li>
      </ol>
      <p class="ap-links"><a href="#agents">Read the full instructions</a><a href="/agents.md">agents.md</a><a href="/llms.txt">llms.txt</a></p>
    </aside>
  </div>
</section>

<section id="start" class="section section--start" aria-labelledby="start-h">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">Three steps · start right now</p><h2 id="start-h">From zero to a working agent in <em>two minutes</em>.</h2></div>
    <ol class="steps">
      <li class="step reveal">
        <span class="step-n">1</span>
        <h3>Open Grok Bot</h3>
        <p>Your sandbox for the two days. New to it? <a href="#grokbot">Get set up here</a>.</p>
        <p class="step-ph"><span class="cred-l">Sign-up link</span>{signup}</p>
      </li>
      <li class="step reveal">
        <span class="step-n">2</span>
        <h3>Give it the repository</h3>
        <p>One link holds every skill, mission and dataset.</p>
        <div class="repo-pill"><code id="{repo_id}">{RU}</code>{copy}</div>
      </li>
      <li class="step step--wide reveal">
        <span class="step-n">3</span>
        <h3>Paste the starter prompt. Let it work.</h3>
        <p>Straight from the repository README. It starts an oncology field-insights mission on synthetic data. Add “Use immunology” or “Use cardiometabolic” to switch.</p>
        {starter}
      </li>
    </ol>
    <p class="fine reveal"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg><span>Workshop data is fictional. Do not upload real company or patient data. Outputs are drafts for qualified review: you stay the final judge.</span></p>
  </div>
</section>

<section id="agenda" class="section" aria-labelledby="agenda-h">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">Agenda · all times ET</p><h2 id="agenda-h">Two days. <em>One AI worker</em> per team.</h2>
    <p class="sec-sub">{E[venue]} · {E[address]}</p></div>
    <div class="agenda">
      <section class="day reveal" aria-labelledby="d1"><header><span class="day-n">Day 1</span><h3 id="d1">Tuesday, Oct 13</h3></header><ol>{d1}</ol></section>
      <section class="day reveal" aria-labelledby="d2"><header><span class="day-n">Day 2</span><h3 id="d2">Wednesday, Oct 14</h3></header><ol>{d2}</ol></section>
    </div>
    <h3 class="sub-h">What the teams build</h3>
    <div class="teams">{teams_html}</div>
  </div>
</section>

<section id="ideas" class="section section--ideas" aria-labelledby="ideas-h">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">Why we are here</p><h2 id="ideas-h">Three shifts, <em>one secret sauce</em>.</h2></div>
    <div class="objs">
      <article class="obj reveal">
        <span class="obj-n">01</span><h3>From answers to outcomes</h3>
        <p>Stop using AI only to summarize and find answers. Give it a goal and let it orchestrate and execute the workflow while you judge the result.</p>
        <div class="shift"><div class="shift-from"><span>Before</span>“Summarize these field notes.”</div><div class="shift-arrow" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div><div class="shift-to"><span>Now</span>“Tell leadership what the field is telling us, with sources and next actions.”</div></div>
      </article>
      <article class="obj reveal">
        <span class="obj-n">02</span><h3>Your own workforce</h3>
        <p>The frontier tools are becoming personal agents that plan, use tools and make files. You augment your work with a team of your own.</p>
        <ul class="tools" aria-label="Frontier tools">
          <li>Claude.ai</li><li>Microsoft Copilot</li><li>ChatGPT</li><li class="on">Grok Bot</li><li>Meta Muse</li>
        </ul>
      </article>
      <article class="obj reveal">
        <span class="obj-n">03</span><h3>Have fun building</h3>
        <p>Pick a mission, push on the result, teach it your house rules, run it again. The best ideas show up when you play.</p>
        <ol class="loop" aria-label="The build loop"><li>Build</li><li>Judge</li><li>Teach</li><li>Rerun</li></ol>
      </article>
    </div>
    <div class="ce reveal">
      <div class="ce-copy">
        <p class="kicker kicker--light">The secret sauce</p>
        <h3>Prompt engineering is giving way to <em>context engineering</em>.</h3>
        <p>Clever wording matters less every month. What matters is what the agent knows: your evidence, your house rules, your judgment. Medical Affairs already holds that context.</p>
      </div>
      <div class="ce-visual">
        <div class="ce-from"><span class="ce-lab">Prompt engineering</span><span class="ce-q">“How do I phrase this?”</span></div>
        <div class="ce-to"><span class="ce-lab">Context engineering</span><span class="ce-q">“What does it need to know?”</span>
          <ul class="ce-cloud" aria-label="Context Medical Affairs holds">{ctx}</ul></div>
      </div>
    </div>
  </div>
</section>

<section id="inside" class="section" aria-labelledby="inside-h">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">What’s in the repository</p><h2 id="inside-h">Four ideas. <em>That’s the whole thing.</em></h2>
    <p class="sec-sub">Open source (Apache-2.0) at <a href="{RU}" target="_blank" rel="noopener">Open-Medical-Affairs/Medical-Affairs-Skills</a>.</p></div>
    <div class="bento">
      <article class="bx bx--a reveal"><div class="bx-ic" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h10M4 17h7"/><circle cx="18" cy="16" r="3"/></svg></div>
        <h3>Skills <span class="bx-big">{ns}</span></h3><p>Written know-how for one Medical Affairs task, such as a KOL brief, a congress readout or an MI response. Your agent picks the right ones; you never need to name them.</p>
        <a class="lnk" href="#skills">Browse all {ns} →</a></article>
      <article class="bx bx--b reveal"><div class="bx-ic" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 4h10l4 4v12H5z"/><path d="M9 12h6M9 16h4"/></svg></div>
        <h3>House rules <span class="bx-big">{hr}</span></h3><p>One file per skill where your team writes what an experienced colleague knows, like “MSL briefs are two pages.” Rules beat the defaults, so the agent works your way.</p>
        <a class="lnk" href="{HR_README}" target="_blank" rel="noopener">How to write a rule ↗</a></article>
      <article class="bx bx--c reveal"><div class="bx-ic" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3.5"/></svg></div>
        <h3>Missions <span class="bx-big">{nm}</span></h3><p>Ready-made tasks with a clear goal, the right input files and the deliverables to expect. Plus six 30-minute team missions for the hackathon.</p>
        <a class="lnk" href="#missions">See the missions →</a></article>
      <article class="bx bx--d reveal"><div class="bx-ic" aria-hidden="true"><svg viewBox="0 0 24 24"><ellipse cx="12" cy="6" rx="7" ry="2.5"/><path d="M5 6v12c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5V6M5 12c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5"/></svg></div>
        <h3>Synthetic data <span class="bx-big">3+1</span></h3><p>A fictional company, Nordvant Biopharma, with three products: NORVANTIB, DERMALYX and ADIPOSYN. Field notes, enquiries, plans and manuscripts, plus a practice CRM with {HCPS} clinicians and {INTER} interactions. The flaws are deliberate.</p>
        <a class="lnk" href="#data">Every dataset + {NPUB} public sources →</a></article>
    </div>
    <h3 class="sub-h">How it works</h3>
    <ol class="hiw">{hiw}</ol>
  </div>
</section>

<section id="missions" class="section section--tint" aria-labelledby="missions-h">
  <div class="wrap">
    <div class="sec-head sec-head--row"><div><p class="kicker">Missions</p><h2 id="missions-h">Pick a task. <em>Copy. Paste. Go.</em></h2>
    <p class="sec-sub">Choose your therapeutic area once. Every prompt on the page updates.</p></div>
    {ta_switch}</div>
    <h3 class="sub-h">Team missions · 30 minutes each</h3>
    <div class="tms">{tm_html}</div>
    <h3 class="sub-h">All {nm} workshop missions</h3>
    <div class="mcs">{cm_html}</div>
  </div>
</section>

<section id="prompts" class="section" aria-labelledby="prompts-h">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">Say this to your agent</p><h2 id="prompts-h">Talk about the work, <em>not the tool</em>.</h2>
    <p class="sec-sub">No skill names or technical prompts needed. Each button copies a ready-to-paste prompt for your chosen area.</p></div>
    <ul class="says">{say_html}</ul>
    <div class="prompt-grid">{more_prompts}</div>
    <div class="two">
      <div><h3 class="sub-h">Then push on it</h3><ul class="nexts">{nexts}</ul></div>
      <div><h3 class="sub-h">Change cards</h3><p class="muted">New information the facilitator hands you mid-exercise. Paste the “change card” prompt above with it.</p><ul class="cards">{cards}</ul></div>
    </div>
  </div>
</section>
{opt}
<section id="data" class="section section--tint" aria-labelledby="data-h">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">Datasets</p><h2 id="data-h">Practice on synthetic data. <em>Work with real public sources.</em></h2>
    <p class="sec-sub">All datasets now live in their own repository, <a href="{DS_URL}" target="_blank" rel="noopener">Open-Medical-Affairs/Data-Sources</a>, in two halves that are never mixed. Copy a raw link for your agent, or a whole pack at once. Machine-readable: <a href="datasets.json">datasets.json</a>.</p>
    <p class="pd-note"><span class="pd-dot" aria-hidden="true"></span>Practice data is fictional and for learning; for real work, bring your own data.</p></div>
    {ds_repos_html}
    <div class="gd" id="get-data" aria-labelledby="gd-h">
      <div class="gd-head"><p class="kicker">Get the data</p><h3 class="ds-h" id="gd-h">Copy a link. <em>Your agent fetches it.</em></h3>
      <p class="muted">Nothing needs to land on your laptop. Copy a direct download link (or a ready-to-paste instruction) and give it to Grok Bot or any agent: it downloads the file onto its own machine. Synthetic files are fictional and safe to practise on. Public sources are real: we copy the official link and show the licence, and <strong>Link only</strong> sources must be used at the source, never copied.</p></div>
      {gd_big_html}
      <div class="gd-tools">
        <label class="search gd-search"><span class="sr">Search datasets</span><svg aria-hidden="true" viewBox="0 0 24 24"><circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4-4"/></svg><input id="gd-q" type="search" placeholder="Search, e.g. enquiries, label, payments" autocomplete="off"></label>
        <div class="gd-filters" role="radiogroup" aria-label="Show"><button type="button" role="radio" class="gd-f" data-f="all" aria-checked="true">All</button><button type="button" role="radio" class="gd-f" data-f="synthetic" aria-checked="false">Synthetic</button><button type="button" role="radio" class="gd-f" data-f="public" aria-checked="false">Public</button><button type="button" role="radio" class="gd-f" data-f="direct" aria-checked="false">Direct download</button><button type="button" role="radio" class="gd-f" data-f="linkonly" aria-checked="false">Link only</button></div>
        <span class="gd-count" id="gd-count" aria-live="polite"></span>
      </div>
      <div class="gd-list" id="gd-list" data-manifest="data-manifest.json"><p class="muted">Loading the dataset list… If it does not appear, open <a href="https://github.com/Open-Medical-Affairs/Data-Sources/releases/latest/download/manifest.csv">manifest.csv</a>.</p></div>
      <button type="button" class="btn-ghost gd-more" id="gd-more" hidden>Show all</button>
    </div>
    <div class="syn-head"><p class="kicker">Synthetic datasets · fictional</p><h3 class="ds-h">A pretend company to practise on <span class="badge badge--syn">Synthetic</span></h3>
    <p class="muted">SYNTHETIC — fictional data for training and workshops, not real patients or products. Nordvant Biopharma, NORVANTIB, DERMALYX and ADIPOSYN do not exist. Safe to use in the room.</p></div>
    <div class="packs">{tabs}{panels}</div>
    <div class="dgs">{other_html}</div>
    {pub_html}
  </div>
</section>

<section id="grokbot" class="section" aria-labelledby="gb-h">
  <div class="wrap">
    <div class="gb">
      <div class="gb-copy">
        <p class="kicker">Grok Bot · get started</p>
        <h2 id="gb-h">Your sandbox for <em>the two days</em>.</h2>
        <p class="sec-sub">Grok Bot with internet is the workshop’s target environment. Company connectors and API keys are not needed.</p>
        <div class="creds">
          <div class="cred"><span class="cred-l">Event sign-up link</span>{signup}</div>
          <div class="cred"><span class="cred-l">Credits code</span>{credits}</div>
        </div>
      </div>
      <ol class="gb-steps">
        <li><h3>Get access</h3><p>Open the event sign-up link on your laptop or phone and create your account.</p></li>
        <li><h3>Add your credits</h3><p>Enter the event credits code so your agent can work through full missions.</p></li>
        <li><h3>Start a new conversation</h3><p>Paste the <a href="#start">starter prompt</a>. It reads the repository, picks a mission and starts on synthetic data.</p></li>
        <li><h3>Can’t open GitHub? Upload a starter</h3><p>Upload one self-contained file instead:</p><ul class="bundles">{bundles}</ul>
          <p class="muted">Or the whole repository: <a href="{ZIP}">Download ZIP</a>.</p></li>
        <li><h3>Make it yours</h3><p>Ask for a different therapeutic area or describe your own Medical Affairs goal. The agent chooses the skills.</p></li>
      </ol>
    </div>
    <div class="dgs dgs--gb">
      <details class="dg"><summary><div><h3>If something is missing</h3><p class="muted">From the participant quickstart.</p></div></summary>
        <div class="dg-body"><ul class="ticks">{ifm}</ul></div></details>
      <details class="dg"><summary><div><h3>For facilitators: one Grok Bot agent per mission</h3><p class="muted">Pre-packaged uploads and ready instructions.</p></div></summary>
        <div class="dg-body"><p>Run <code>python3 scripts/package_skills.py</code> in the repository to build a complete upload for each mission (<code>dist/grokbot/agents/&lt;mission&gt;.zip</code>). <a href="{GB_AGENTS}" target="_blank" rel="noopener">grokbot-agents.json</a> holds each agent’s instructions to paste in. Test each agent with one request that must produce a file. See <a href="{DOCS_AGENTS}" target="_blank" rel="noopener">agent setup</a>.</p></div></details>
    </div>
  </div>
</section>

<section id="agents" class="section section--dark" aria-labelledby="agents-h">
  <div class="aurora aurora--dark" aria-hidden="true"><span></span><span></span></div>
  <div class="wrap">
    <div class="sec-head"><p class="kicker kicker--light">Instructions for agents</p><h2 id="agents-h">Give this page <em>to your agent</em>.</h2>
    <p class="sec-sub">This site is agent-ready. Paste the sentence below, or just the page address. Your agent reads the playbook, asks you what you want to do, and then does it with you.</p></div>
    <details class="playbook" id="agent-playbook"><summary><span>Read the full agent playbook</span><span class="playbook-hint">Plain text at <code>/agents.md</code></span></summary>
      <div class="playbook-body"><a class="btn-ghost playbook-raw" href="/agents.md">Open agents.md</a><pre class="prompt-text playbook-text" tabindex="0">{playbook_md}</pre></div>
    </details>
    <div class="give">
      <figure class="prompt prompt--dark"><div class="prompt-head"><span class="prompt-title">Paste into Grok Bot</span>{give_copy}</div>
      <pre id="give" class="prompt-text" data-site-template="{give_tpl}"><code>{give_def}</code></pre></figure>
      <ul class="endpoints">
        <li><a href="/agents.md"><code>agents.md</code><span>Instructions for agents (the playbook)</span></a></li>
        <li><a href="/llms.txt"><code>llms.txt</code><span>Index for language models</span></a></li>
        <li><a href="missions.json"><code>missions.json</code><span>Missions with prompts per area</span></a></li>
        <li><a href="datasets.json"><code>datasets.json</code><span>Synthetic datasets and public sources, with raw links</span></a></li>
        <li><a href="{DS_URL}" target="_blank" rel="noopener"><code>Data-Sources</code><span>The datasets repository</span></a></li>
        <li><a href="prompts.json"><code>prompts.json</code><span>All prompts and optimizer templates</span></a></li>
        <li><a href="skills.json"><code>skills.json</code><span>All {ns} skills</span></a></li>
        <li><a href="{AGENTS_RAW}"><code>AGENTS.md</code><span>The repository’s own entry point</span></a></li>
      </ul>
    </div>
  </div>
</section>

<section id="skills" class="section" aria-labelledby="skills-h">
  <div class="wrap">
    <div class="sec-head sec-head--row"><div><p class="kicker">Reference</p><h2 id="skills-h">All {ns} skills.</h2>
    <p class="sec-sub">You never need to name a skill. This is here for the curious, and for your agent.</p></div>
    <label class="search"><span class="sr">Filter skills</span><svg aria-hidden="true" viewBox="0 0 24 24"><circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4-4"/></svg><input id="skill-filter" type="search" placeholder="Filter, e.g. congress" autocomplete="off"></label></div>
    <div class="sgs">{skills_html}</div>
  </div>
</section>

</main>

<footer class="foot">
  <div class="wrap foot-in">
    <div><p class="foot-brand">{E[name]}</p><p class="muted">{E[dates]} · {E[venue]}, {E[address]}<br>Keynote: {E[host]} · With {E[organizer]}</p></div>
    <div class="muted foot-fine"><p>Built from <a href="{RU}" target="_blank" rel="noopener">Medical-Affairs-Skills</a> (Apache-2.0){commit}. All products, people and results in the workshop data are fictional. Outputs are drafts requiring qualified review; this is not a clinical decision, GxP or pharmacovigilance system.</p></div>
  </div>
</footer>
<div class="toast" role="status" aria-live="polite" id="toast"></div>
<script src="assets/app.js" defer></script>
<script src="assets/optimizer-data.js" defer></script>
<script src="assets/ai-optimizer.js" defer></script>
<script src="assets/skill-creator.js" defer></script>
<script src="assets/get-data.js" defer></script>
</body>
</html>
'''

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", help="path to a Medical-Affairs-Skills checkout to (re)extract content from")
    a = ap.parse_args()
    cpath = HERE / "data/content.json"
    if a.repo:
        content = extract(Path(a.repo).resolve())
        cpath.parent.mkdir(exist_ok=True)
        cpath.write_text(json.dumps(content, indent=2, ensure_ascii=False), encoding="utf-8")
        print("extracted", cpath.relative_to(HERE))
    content = json.loads(cpath.read_text(encoding="utf-8"))
    cfg = load_cfg()
    files = render(content, cfg)
    import paginate  # separate pages + left sidebar + mission org charts (see paginate.py)
    files = paginate.paginate(files, cfg)
    import wording  # no 'job'/'jobs' anywhere on the site (see wording.py)
    files["data/mission-graphs.json"] = (HERE / "data/mission-graphs.json").read_text(encoding="utf-8")
    files = {k: wording.soften(v) for k, v in files.items()}
    left = {k: wording.remaining(v) for k, v in files.items() if wording.remaining(v)}
    if left:
        raise SystemExit(f"'job' wording left in the built site: {left}")
    for name, text in files.items():
        (HERE / name).parent.mkdir(parents=True, exist_ok=True)
        (HERE / name).write_text(text, encoding="utf-8")
        print("wrote", name, f"{len(text):,} chars")

if __name__ == "__main__":
    main()
