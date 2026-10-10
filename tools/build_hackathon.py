#!/usr/bin/env python3
"""Publish the hackathon facilitation pack to the site (/hackathon).

  python3 tools/build_hackathon.py [--pack /workspace/hackathon-pack] [--kickoff /workspace/slides/hackathon-intro-H0sOFV]

Copies the pack (guides .md, Facilitator Guide .docx, final-presentation template .pptx + contact sheet,
agent instructions, capture log) into hackathon/files/, and the kickoff deck into hackathon/files/kickoff/
with SPEAKER NOTES REMOVED from the public .pptx (same method as tools/build_deck.py). The final-presentation
template keeps its notes: they are fill-in instructions for teams. Then run build.py to regenerate the pages.
"""
import argparse, json, shutil, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_deck import strip_notes, slide_count

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "hackathon" / "files"
FILES = ["README.md", "01-publications-brain.md", "02-insights-engine.md", "03-congress-monitor.md", "04-field-intelligence-engine.md",
         "final-presentation-agent-instructions.md", "capture-log-template.md",
         "template/AI-in-Action-Final-Presentation-Template.pptx", "template/template-contact-sheet.jpg"]
GUIDES = ["01-Publications-Brain-Facilitator-Guide.pdf", "02-Insights-Engine-Facilitator-Guide.pdf",
          "03-Congress-Monitor-Facilitator-Guide.pdf", "04-Field-Intelligence-Engine-Facilitator-Guide.pdf"]
OPTIONAL = ["how-to-use-template.md"] + [f"guides/{g}" for g in GUIDES]  # pages show placeholders until these exist  # rendered on /hackathon beside the template download when present
KICK = "AI-in-Action-Hackathon-Intro"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", default="/workspace/hackathon-pack")
    ap.add_argument("--kickoff", default="/workspace/slides/hackathon-intro-H0sOFV")
    a = ap.parse_args()
    pack, kick = Path(a.pack), Path(a.kickoff)
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "template").mkdir(parents=True); (OUT / "kickoff").mkdir(); (OUT / "guides").mkdir()
    for f in FILES + OPTIONAL:
        if (pack / f).exists():
            shutil.copyfile(pack / f, OUT / f)
        elif f in FILES:
            sys.exit(f"missing {pack / f}")
    pptx = kick / f"{KICK}.pptx"
    removed = strip_notes(pptx, OUT / "kickoff" / f"{KICK}.pptx")
    pdf = kick / f"{KICK}.pdf"
    if pdf.exists() and pdf.stat().st_mtime >= pptx.stat().st_mtime - 5:
        shutil.copyfile(pdf, OUT / "kickoff" / f"{KICK}.pdf")
    else:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, str(OUT / "kickoff" / f"{KICK}.pptx")], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
            shutil.copyfile(Path(tmp) / f"{KICK}.pdf", OUT / "kickoff" / f"{KICK}.pdf")
    sizes = {str(p.relative_to(OUT)): p.stat().st_size for p in OUT.rglob("*") if p.is_file()}
    meta = {"kickoff_slides": slide_count(OUT / "kickoff" / f"{KICK}.pptx"), "sizes": sizes}
    (ROOT / "hackathon" / "pack.json").write_text(json.dumps(meta, indent=1))
    print(f"hackathon pack: {len(sizes)} files, kickoff deck {meta['kickoff_slides']} slides, removed {removed} notes slides")


if __name__ == "__main__":
    main()
