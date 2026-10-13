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


VIDEO_EXT = (".mp4", ".mov", ".m4v", ".avi", ".wmv", ".webm", ".mkv", ".mpg", ".mpeg")


LINK_W, LINK_H = 3383280, 1219200  # 'Watch the clip' card, matches the public PDF


def link_card(sid, x, y, rid, url):
    """Navy card with an orange play button, clickable to the clip URL (no film imagery)."""
    host = "YouTube" if "youtu" in url else "your browser"
    d = 274320
    cx, cy = x + 182880, y + (LINK_H - 640080) // 2
    link = f'<a:hlinkClick r:id="{rid}"/>'
    return (f'<p:grpSp><p:nvGrpSpPr><p:cNvPr id="{sid}" name="Watch the clip link card">{link}</p:cNvPr><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            f'<p:grpSpPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{LINK_W}" cy="{LINK_H}"/><a:chOff x="{x}" y="{y}"/><a:chExt cx="{LINK_W}" cy="{LINK_H}"/></a:xfrm></p:grpSpPr>'
            f'<p:sp><p:nvSpPr><p:cNvPr id="{sid+1}" name="Clip card">{link}</p:cNvPr><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{LINK_W}" cy="{LINK_H}"/></a:xfrm>'
            f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 8000"/></a:avLst></a:prstGeom><a:solidFill><a:srgbClr val="002B55"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>'
            f'<p:txBody><a:bodyPr lIns="1005840" tIns="91440" rIns="137160" bIns="91440" anchor="ctr"/><a:lstStyle/>'
            f'<a:p><a:r><a:rPr lang="en-US" sz="1800" b="1"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></a:rPr><a:t>Watch the clip</a:t></a:r></a:p>'
            f'<a:p><a:r><a:rPr lang="en-US" sz="1100"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></a:rPr><a:t>Opens on {host}</a:t></a:r></a:p></p:txBody></p:sp>'
            f'<p:sp><p:nvSpPr><p:cNvPr id="{sid+2}" name="Play button">{link}</p:cNvPr><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{cx}" y="{cy}"/><a:ext cx="640080" cy="640080"/></a:xfrm>'
            f'<a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="F37021"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr></p:sp>'
            f'<p:sp><p:nvSpPr><p:cNvPr id="{sid+3}" name="Play triangle">{link}</p:cNvPr><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm rot="5400000"><a:off x="{cx + 320040 - d//2 + 27432}" y="{cy + 320040 - d//2}"/><a:ext cx="{d}" cy="{d}"/></a:xfrm>'
            f'<a:prstGeom prst="triangle"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr></p:sp></p:grpSp>')


def strip_video(path, default_url="https://youtu.be/ozS_6vqnJ8w"):
    """Remove embedded/linked video from the public pptx. The video and its poster frame (often a film
    still) are replaced with a 'Watch the clip' link card. Returns the files removed."""
    import re, zipfile, posixpath
    src = zipfile.ZipFile(path)
    items = {i.filename: src.read(i.filename) for i in src.infolist()}
    src.close()
    gone = [n for n in items if n.lower().endswith(VIDEO_EXT)]
    if not gone:
        return []
    for n in gone:
        del items[n]
    posters = set()
    for n in [k for k in items if re.fullmatch(r"ppt/slides/slide\d+\.xml", k)]:
        t = items[n].decode("utf8")
        if "<a:videoFile" not in t and "p14:media" not in t:
            continue
        rn = f"ppt/slides/_rels/{posixpath.basename(n)}.rels"
        rels = items[rn].decode("utf8")
        m = re.search(r"(https?://)?(youtu\.be/[\w-]+|(?:www\.)?youtube\.com/watch\?v=[\w-]+|vimeo\.com/\d+)", t)
        url = ("https://" + m.group(2)) if m else default_url
        ids = [int(i) for i in re.findall(r'<p:cNvPr id="(\d+)"', t)]

        def repl(pm):
            pic = pm.group(0)
            if "<a:videoFile" not in pic and "p14:media" not in pic:
                return pic
            nonlocal rels, ids
            bl = re.search(r'<a:blip r:embed="(rId\d+)"', pic)
            if bl:
                tg = re.search(rf'<Relationship Id="{bl.group(1)}"[^>]*Target="([^"]+)"', rels)
                if tg:
                    posters.add(posixpath.normpath(posixpath.join("ppt/slides", tg.group(1))))
                rels = re.sub(rf'<Relationship Id="{bl.group(1)}"[^>]*/>', "", rels)
            off = re.search(r'<a:off x="(\d+)" y="(\d+)"/><a:ext cx="(\d+)" cy="(\d+)"/>', pic)
            px, py, pw, ph = map(int, off.groups())
            x = max(px, px + pw - LINK_W); y = py + ph + 182880
            rid = "rIdClip%d" % len(ids)
            rels = rels.replace("</Relationships>", f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="{url}" TargetMode="External"/></Relationships>')
            sid = max(ids) + 1; ids += [sid, sid + 1, sid + 2, sid + 3]
            return link_card(sid, x, y, rid, url)

        t = re.sub(r"<p:pic>.*?</p:pic>", repl, t, flags=re.S)
        t = re.sub(r"<a:t>Click the video to play[^<]*</a:t>", "<a:t>Link only: </a:t>", t)
        t = re.sub(r"<p:timing>.*?</p:timing>", lambda m: "" if "<p:video" in m.group(0) else m.group(0), t, flags=re.S)
        items[n] = t.encode("utf8"); items[rn] = rels.encode("utf8")
    for n in list(items):
        if n.endswith(".rels"):
            t = items[n].decode("utf8")
            t = re.sub(r'<Relationship [^>]*Type="[^"]*/(?:video|media)"[^>]*/>', "", t)
            t = re.sub(r'<Relationship [^>]*Target="[^"]*\.(?:mp4|mov|m4v|avi|wmv|webm|mkv|mpg|mpeg)"[^>]*/>', "", t, flags=re.I)
            items[n] = t.encode("utf8")
    for pth in posters:  # drop the poster file if nothing else uses it
        base = posixpath.basename(pth)
        if pth in items and not any(base.encode() in b for k, b in items.items() if k.endswith(".rels")):
            del items[pth]; gone.append(pth)
    ct = items["[Content_Types].xml"].decode("utf8")
    items["[Content_Types].xml"] = re.sub(r'<Default Extension="(?:mp4|mov|m4v|avi|wmv|webm|mkv|mpg|mpeg)"[^>]*/>', "", ct, flags=re.I).encode("utf8")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for n, b in items.items():
            z.writestr(n, b)
    return gone


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
    vids = strip_video(pub_pptx)
    print(f"removed embedded video: {vids or 'none'}")
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
