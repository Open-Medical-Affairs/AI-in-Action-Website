#!/usr/bin/env python3
"""Extract mission graphs from the Medical-Affairs-Skills repository into data/mission-graphs.json.

    python3 tools/extract_mission_graphs.py --repo /path/to/Medical-Affairs-Skills   # a checkout of the default branch

Everything comes from the repository, nothing is hand-written:
  * missions: workshop/catalog.json (id, title, objective, inputs, skills in order, deliverables)
  * skills:   skills/<name>/SKILL.md front matter (description, tier, metadata.requires, metadata.suggests)
  * swarm:    for a lead skill with references/digital-workers.md, the worker roster
              ("### Role — `skill` (+ `extra`)" under "## Pod N — Name"), each worker's Context line
              (files and upstream workers it consumes), and the wave/gate table in its SKILL.md
  * gates:    the repository's AGENTS.md rules (safety scan before analysis; challenge with
              deliverable-quality-review; designed delivery for human review) plus explicit gate rows
Standard library only.
"""
import argparse, json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GH = "https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills"


def front(text):
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    fm = m.group(1) if m else ""
    d = {}
    desc = re.search(r"^description:\s*(>-?|\|)?\s*\n((?:[ ]{2,}.*\n?)+)", fm, re.M)
    if desc:
        d["description"] = " ".join(l.strip() for l in desc.group(2).splitlines())
    else:
        one = re.search(r"^description:\s*(.+)$", fm, re.M)
        d["description"] = one.group(1).strip().strip("\"'") if one else ""
    t = re.search(r"^\s+tier:\s*(\S+)", fm, re.M); d["tier"] = t.group(1) if t else ""
    for key in ("requires", "suggests"):
        block = re.search(rf"^\s+{key}:\s*\n((?:\s+-\s*\S+\n?)+)", fm, re.M)
        d[key] = re.findall(r"-\s*([\w-]+)", block.group(1)) if block else []
    return d


def first_sentence(s):
    s = re.sub(r"\s+", " ", s).strip()
    m = re.match(r"(.+?[.!?])(\s|$)", s)
    out = m.group(1) if m else s
    return out if len(out) <= 320 else out[:317].rsplit(" ", 1)[0] + "…"


def _unused_git_ls(repo, ref, path):
    try:
        out = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", ref, path], capture_output=True, text=True, check=True).stdout
        return set(out.split())
    except Exception:
        return None


def _unused_git_show(repo, ref, path):
    try:
        return subprocess.run(["git", "-C", repo, "show", f"{ref}:{path}"], capture_output=True, text=True, check=True).stdout
    except Exception:
        return None


def parse_workers(text):
    workers, pod = [], None
    blocks = re.split(r"^### ", text, flags=re.M)
    for chunk in [text.split("\n### ")[0]] + blocks[1:]:
        pass
    pod_of = {}
    cur = None
    for line in text.splitlines():
        pm = re.match(r"^## (?:Pod \d+ — )?(.+)$", line)
        if pm:
            cur = pm.group(1).strip()
        wm = re.match(r"^### (.+?) — (.+)$", line)
        if wm:
            skills = re.findall(r"`([\w-]+)`", wm.group(2))
            workers.append({"role": wm.group(1).strip(), "skills": skills, "pod": cur, "context": "", "consumes": []})
        cm = re.match(r"^- \*\*Context:\*\*\s*(.*)$", line)
        if cm and workers:
            workers[-1]["context"] = cm.group(1)
            workers[-1]["_ctx_open"] = True
            continue
        if workers and workers[-1].get("_ctx_open"):
            if line.startswith("  ") and not line.strip().startswith("- **"):
                workers[-1]["context"] += " " + line.strip()
            else:
                workers[-1]["_ctx_open"] = False
    roles = [w["role"] for w in workers]
    for w in workers:
        w.pop("_ctx_open", None)
        ctx = w["context"]
        w["files"] = sorted(set(re.findall(r"`([\w.-]+\.(?:md|csv|json))`", ctx)))
        for other in workers:
            if other is w:
                continue
            short = other["role"].replace(" worker", "").replace("Launch ", "")
            if re.search(rf"\b{re.escape(short)}(?: worker)?'s\b", ctx, re.I):
                w["consumes"].append(other["role"])
        if re.search(r"approved platform", ctx, re.I):
            nar = next((o["role"] for o in workers if o["skills"] and o["skills"][0] == "scientific-platform"), None)
            if nar and nar != w["role"] and nar not in w["consumes"]:
                w["consumes"].append(nar)
        w["context"] = re.sub(r"\s+", " ", ctx).strip()
    return workers


def parse_waves(skill_md, workers):
    rows = re.findall(r"^\|\s*(\*\*Gate \d+\*\*|\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$", skill_md, re.M)
    waves = []
    for a, b, c in rows:
        if a.startswith("**Gate"):
            waves.append({"kind": "gate", "label": a.strip("*"), "who": b.strip("*").strip(), "why": c.strip()})
        else:
            names = [n.strip() for n in b.split("·")]
            members = []
            for n in names:
                hit = next((w["role"] for w in workers if w["role"] == n or w["role"].startswith(n) or n.startswith(w["role"].split(" worker")[0])), None)
                members.append(hit or n)
            waves.append({"kind": "wave", "label": f"Wave {a}", "members": members, "why": c.strip()})
    return waves


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="checkout of Medical-Affairs-Skills (the --ref state)")
    ap.add_argument("--ref", default="HEAD", help="ref used in GitHub links (HEAD = the repository's default branch)")
    a = ap.parse_args()
    repo = Path(a.repo)
    cat = json.loads((repo / "workshop/catalog.json").read_text(encoding="utf-8"))
    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()

    skills = {}
    for p in sorted((repo / "skills").glob("*/SKILL.md")):
        name = p.parent.name
        fm = front(p.read_text(encoding="utf-8"))
        skills[name] = {"name": name, "summary": first_sentence(fm["description"]), "tier": fm["tier"],
                        "requires": fm["requires"], "suggests": fm["suggests"],
                        "url": f"{GH}/blob/{a.ref}/skills/{name}/SKILL.md"}

    def closure(names):
        seen, stack = [], list(names)
        while stack:
            n = stack.pop(0)
            for r in skills.get(n, {}).get("requires", []):
                if r not in seen and r not in names:
                    seen.append(r); stack.append(r)
        return seen

    missions = []
    for m in cat["missions"]:
        ms = m["skills"]
        lead, rest = ms[0], ms[1:]
        g = {"id": m["id"], "title": m["title"], "objective": m["objective"], "skills": ms,
             "inputs": [i.split("/")[-1] for i in m["inputs"]], "deliverables": m["deliverables"],
             "lead": lead, "workers": [], "support": [], "handoffs": [], "waves": [], "structure": "team"}
        dw = repo / "skills" / lead / "references" / "digital-workers.md"
        if dw.exists():
            g["structure"] = "swarm"
            workers = parse_workers(dw.read_text(encoding="utf-8"))
            g["lead_role"] = next((w["role"] for w in workers if w["skills"] and w["skills"][0] == lead), "Lead")
            g["workers"] = [w for w in workers if not (w["skills"] and w["skills"][0] == lead)]
            g["waves"] = parse_waves((repo / "skills" / lead / "SKILL.md").read_text(encoding="utf-8"), workers)
            g["handoffs"] = [{"from": c, "to": w["role"]} for w in g["workers"] for c in w["consumes"]]
            used = sorted({s for w in workers for s in w["skills"]})
            g["support"] = [s for s in closure(used) if s != "medical-affairs-foundations"]
            g["source"] = f"skills/{lead}/references/digital-workers.md and skills/{lead}/SKILL.md (Stage 2 waves)"
        else:
            g["workers"] = [{"role": s, "skills": [s]} for s in rest]
            for s in ms:
                for t in ms:
                    if s != t and (t in skills.get(s, {}).get("requires", []) or t in skills.get(s, {}).get("suggests", [])):
                        g["handoffs"].append({"from": s, "to": t, "kind": "requires" if t in skills[s]["requires"] else "suggests"})
            g["support"] = [s for s in closure(ms) if s != "medical-affairs-foundations"]
            g["source"] = "workshop/catalog.json skills (in order) and each SKILL.md metadata.requires / suggests"
        g["gates"] = [
            {"at": "start", "label": "Safety scan first", "detail": "Scan human-sourced records for possible safety, PQC or special-situation findings before analysis (AGENTS.md)."},
        ] + ([{"at": "mid", "label": w["label"], "detail": f"{w['who']}: {w['why']}"} for w in g["waves"] if w["kind"] == "gate"]) + [
            {"at": "end", "label": "You decide", "detail": "Outputs are drafts for qualified human review; the human is the final judge (AGENTS.md)."},
        ]
        g["reviewer"] = "deliverable-quality-review"
        missions.append(g)

    out = {"source": GH, "ref": a.ref, "commit": head,
           "always_loaded": "medical-affairs-foundations", "skills": skills, "missions": missions}
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data/mission-graphs.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(missions)} missions, {len(skills)} skills from {repo} @ {head}")


if __name__ == "__main__":
    main()
