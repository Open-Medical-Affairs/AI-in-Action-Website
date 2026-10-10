"""Tiny Markdown -> HTML for the hackathon pack (headings, paragraphs, lists, tables, blockquotes, fenced code, inline links/bold/italic/code).
Standard library only. Code blocks become copyable prompt figures (the site's existing Copy buttons)."""
import html, re, itertools

E = lambda s: html.escape(s, quote=True)
_ids = itertools.count(1)


def inline(t, link):
    out, pos = [], 0
    tok = re.compile(r"\[(`?)([^\]]+?)\1\]\(([^)\s]+)\)|\*\*([^*]+)\*\*|`([^`]+)`|(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])")
    for m in tok.finditer(t):
        out.append(E(t[pos:m.start()]))
        if m.group(3):
            href = link(m.group(3)); txt = E(m.group(2))
            if m.group(1): txt = f"<code>{txt}</code>"
            ext = href.startswith("http")
            out.append(f'<a href="{E(href)}"' + (' target="_blank" rel="noopener"' if ext else "") + f">{txt}</a>")
        elif m.group(4): out.append(f"<strong>{inline(m.group(4), link)}</strong>")
        elif m.group(5): out.append(f"<code>{E(m.group(5))}</code>")
        else: out.append(f"<em>{inline(m.group(6), link)}</em>")
        pos = m.end()
    out.append(E(t[pos:]))
    return "".join(out)


def code_block(code, label, prefix):
    pid = f"{prefix}-{next(_ids)}"
    return (f'<figure class="prompt hk-code"><div class="prompt-head"><span class="prompt-title">{E(label)}</span>'
            f'<button type="button" class="btn-copy" data-copy="#{pid}" aria-label="Copy {E(label.lower())}"><svg class="i-copy" aria-hidden="true"><use href="#ic-copy"/></svg>'
            f'<svg class="i-check" aria-hidden="true"><use href="#ic-check"/></svg><span class="lbl">Copy</span></button></div>'
            f'<pre id="{pid}" class="prompt-text"><code>{E(code)}</code></pre></figure>')


def render(md, link=lambda u: u, prefix="hk", shift=0, copy_all=False):
    """Returns HTML. `link` rewrites hrefs; `shift` demotes headings (## -> h(2+shift))."""
    lines = md.replace("\r", "").split("\n")
    out, i, last_para = [], 0, ""
    while i < len(lines):
        ln = lines[i]
        if ln.lstrip().startswith("```") and len(ln) - len(ln.lstrip()) <= 4:
            ind = len(ln) - len(ln.lstrip())
            j = i + 1
            while j < len(lines) and not lines[j].lstrip().startswith("```"): j += 1
            code = "\n".join(l[ind:] if l[:ind].strip() == "" else l for l in lines[i + 1:j])
            label = "Prompt to paste"
            lp = re.sub(r"<[^>]+>", "", last_para).strip()
            if re.search(r"prompt|paste|instruction|Grok Bot", lp, re.I) and len(lp) < 140:
                label = lp.rstrip(":").strip() or label
            elif not copy_all and not re.search(r"\b(paste|prompt|assignment|use https)\b", code[:400], re.I):
                out.append(f'<pre class="hk-pre"><code>{E(code)}</code></pre>'); i = j + 1; continue
            out.append(code_block(code, label, prefix)); i = j + 1; last_para = ""; continue
        m = re.match(r"(#{1,6}) (.*)", ln)
        if m:
            lv = min(6, len(m.group(1)) + shift)
            txt = m.group(2)
            sid = prefix + "-" + re.sub(r"[^a-z0-9]+", "-", re.sub(r"^\d+\.\s*", "", txt.lower())).strip("-")[:48]
            out.append(f'<h{lv} id="{sid}">{inline(txt, link)}</h{lv}>'); i += 1; continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            head, body = rows[0], [r for r in rows[1:] if not all(re.fullmatch(r":?-+:?", c) for c in r if c)]
            th = "".join(f"<th>{inline(c, link)}</th>" for c in head) if any(head) else ""
            tb = "".join("<tr>" + "".join(f"<td>{inline(c, link)}</td>" for c in r) + "</tr>" for r in body)
            out.append(f'<div class="hk-table"><table>{f"<thead><tr>{th}</tr></thead>" if th else ""}<tbody>{tb}</tbody></table></div>'); continue
        if ln.startswith(">"):
            q = []
            while i < len(lines) and lines[i].startswith(">"):
                q.append(lines[i][1:].strip()); i += 1
            txt = " ".join(q)
            cls = "hk-note hk-note--warn" if re.search(r"ILLUSTRATIVE|Timing", txt) else "hk-note"
            out.append(f'<blockquote class="{cls}"><p>{inline(txt, link)}</p></blockquote>'); continue
        if re.match(r"\s*([-*]|\d+\.) ", ln):
            ordered = bool(re.match(r"\s*\d+\. ", ln)); items = []
            start = int(re.match(r"\s*(\d+)", ln).group(1)) if ordered else 1
            while i < len(lines) and re.match(r"\s*([-*]|\d+\.) ", lines[i]):
                items.append(re.sub(r"^\s*([-*]|\d+\.) ", "", lines[i])); i += 1
                while i < len(lines) and lines[i].startswith("   ") and lines[i].strip():
                    items[-1] += " " + lines[i].strip(); i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}" + (f' start="{start}"' if start != 1 else "") + ">" + "".join(f"<li>{inline(x, link)}</li>" for x in items) + f"</{tag}>"); continue
        if ln.strip() in ("", "---"):
            i += 1; continue
        para = [ln]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"(#{1,6} |```|\||>|\s*([-*]|\d+\.) )", lines[i]):
            para.append(lines[i]); i += 1
        last_para = inline(" ".join(para), link)
        out.append(f"<p>{last_para}</p>")
    return "\n".join(out)
