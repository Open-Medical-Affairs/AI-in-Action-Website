#!/usr/bin/env python3
"""Publish Vivek's keynote deck to the site (/deck).

  python3 tools/build_deck.py [--pptx PATH] [--pdf PATH]

- Copies the PowerPoint into deck/ with the SPEAKER NOTES REMOVED (notes slides,
  their relationships and content types are stripped; slides are untouched).
- Uses the PDF if it exists and is newer than the pptx; otherwise exports one
  with LibreOffice (slides only, no notes pages).
- Renders one JPG per slide (1600 px wide) and a 320 px thumbnail, and writes
  deck/deck.json, which build.py / paginate.py read to build /deck.
Needs: pdftoppm (poppler-utils), Pillow, LibreOffice only when no PDF is supplied.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = Path("/workspace/slides/ai-in-action-keynote-DSYHHc")
OUT = ROOT / "deck"
NAME = "AI-in-Action-Vivek-Deck"
WIDTH, THUMB, QUALITY = 1600, 320, 78


def strip_notes(src: Path, dst: Path) -> int:
    """Copy a pptx without speaker notes. Returns how many notes slides were removed."""
    removed = 0
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            n = item.filename
            if n.startswith("ppt/notesSlides/"):
                removed += n.endswith(".xml") and "/_rels/" not in n
                continue
            data = zin.read(n)
            if n == "[Content_Types].xml":
                data = re.sub(rb'<Override[^>]*PartName="/ppt/notesSlides/[^"]*"[^>]*/>', b"", data)
            elif re.match(r"ppt/slides/_rels/slide\d+\.xml\.rels$", n):
                data = re.sub(rb'<Relationship[^>]*Type="[^"]*/notesSlide"[^>]*/>', b"", data)
            zout.writestr(item, data)
    return removed


def slide_count(pptx: Path) -> int:
    with zipfile.ZipFile(pptx) as z:
        return len([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pptx", default=str(SRC / f"{NAME}.pptx"))
    ap.add_argument("--pdf", default=None, help="defaults to the PDF next to the pptx (either capitalisation)")
    a = ap.parse_args()
    pptx = Path(a.pptx)
    if not pptx.exists():
        sys.exit(f"missing {pptx}")
    cands = [Path(a.pdf)] if a.pdf else [pptx.with_suffix(".pdf"), pptx.parent / "AI-in-action-Vivek-Deck.pdf"]
    pdf = next((p for p in cands if p.exists() and p.stat().st_mtime >= pptx.stat().st_mtime - 5), None)

    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("slide-*.jpg"):
        old.unlink()
    for old in OUT.glob("thumb-*.jpg"):
        old.unlink()

    pub_pptx = OUT / f"{NAME}.pptx"
    removed = strip_notes(pptx, pub_pptx)
    n_slides = slide_count(pub_pptx)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        if pdf is None:
            print("No current PDF; exporting one with LibreOffice from the notes-free pptx…")
            subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(tmp), str(pub_pptx)],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
            pdf = tmp / f"{NAME}.pdf"
            source = "LibreOffice export"
        else:
            source = str(pdf)
        shutil.copyfile(pdf, OUT / f"{NAME}.pdf")
        subprocess.run(["pdftoppm", "-jpeg", "-jpegopt", f"quality={QUALITY},optimize=y,progressive=y",
                        "-scale-to-x", str(WIDTH), "-scale-to-y", "-1", str(OUT / f"{NAME}.pdf"), str(tmp / "p")], check=True)
        pages = sorted(tmp.glob("p-*.jpg"), key=lambda p: int(p.stem.split("-")[-1]))
        slides = []
        for i, p in enumerate(pages, 1):
            im = Image.open(p).convert("RGB")
            im.save(OUT / f"slide-{i:02d}.jpg", "JPEG", quality=QUALITY, optimize=True, progressive=True)
            t = im.copy(); t.thumbnail((THUMB, THUMB * 2))
            t.save(OUT / f"thumb-{i:02d}.jpg", "JPEG", quality=70, optimize=True)
            v = lambda f: hashlib.sha1((OUT / f).read_bytes()).hexdigest()[:8]  # cache-buster: changes when the slide changes
            slides.append({"n": i, "src": f"/deck/slide-{i:02d}.jpg?v={v(f'slide-{i:02d}.jpg')}", "thumb": f"/deck/thumb-{i:02d}.jpg?v={v(f'thumb-{i:02d}.jpg')}", "w": im.width, "h": im.height})

    if len(slides) != n_slides:
        print(f"WARNING: PDF has {len(slides)} pages but the pptx has {n_slides} slides (notes pages in the PDF?)", file=sys.stderr)
    meta = {"title": "AI in Action — Vivek's Deck", "slides": slides, "count": len(slides),
            "pdf": f"/deck/{NAME}.pdf", "pptx": f"/deck/{NAME}.pptx",
            "pdf_bytes": (OUT / f"{NAME}.pdf").stat().st_size, "pptx_bytes": pub_pptx.stat().st_size}
    (OUT / "deck.json").write_text(json.dumps(meta, indent=1))
    size = sum(f.stat().st_size for f in OUT.iterdir())
    print(f"deck: {len(slides)} slides from {source}; removed {removed} notes slides; deck/ is {size/1e6:.1f} MB")


if __name__ == "__main__":
    main()
