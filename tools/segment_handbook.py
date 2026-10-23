"""Split an offline handbook copy into passages: one per paragraph, list item, table row or figure.

Reads the clean HTML written by scrape_mto_handbook.py, scrape_ca_handbook.py and
scrape_tx_handbook.py (handbook text inside <article class="content">) and writes JSONL,
one passage per line:

    {"id": "changing-positions:017", "page": "changing-positions", "page_title": "Changing positions",
     "sec": "Passing · ¶6", "path": ["Passing"], "anchor": "passing", "kind": "para",
     "text": "...", "src": null, "cap": null, "pdf_page": null}

`sec` follows the passage files in analysis/passing-rules/inputs/: the heading path joined
with " › ", then the position in that section ("¶3", "item 2", "image", "row 4").

Usage: python tools/segment_handbook.py handbooks/mto > analysis/segments/mto.jsonl
"""
import json
import os
import re
import sys

from bs4 import BeautifulSoup, NavigableString, Tag

HEADINGS = {"h2": 0, "h3": 1, "h4": 2, "h5": 3}
CAPTION = re.compile(r"^(Diagram|Figure|Fig\.|Table|Image|Illustration)\s*[\w.-]+", re.I)


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def pdf_page(el):
    """The PDF page a block came from (PDF-converted handbooks only), from the element or its parent."""
    while isinstance(el, Tag):
        if el.get("data-pdf-page"):
            return el["data-pdf-page"]
        el = el.parent
    return None


def page_order(book):
    """Pages in reading order, from the index's table of contents; any others after."""
    index = os.path.join(book, "index.html")
    found = [f[:-5] for f in sorted(os.listdir(book)) if f.endswith(".html")]
    order = []
    if os.path.exists(index):
        soup = BeautifulSoup(open(index, encoding="utf-8").read(), "html.parser")
        for a in soup.select("nav a[href$='.html'], aside a[href$='.html']"):
            slug = a["href"].split("#")[0][:-5]
            if slug in found and slug not in order:
                order.append(slug)
    return (["index"] if "index" in found else []) + [s for s in order if s != "index"] + \
        [s for s in found if s not in order and s != "index"]


def segment_page(book, slug):
    soup = BeautifulSoup(open(os.path.join(book, slug + ".html"), encoding="utf-8").read(), "html.parser")
    art = soup.find("article", class_="content")
    if art is None:
        return []
    h1 = soup.find("h1")
    title = norm(h1.get_text()) if h1 else slug
    path, anchor = [], None
    counts = {}
    out = []

    def where(kind):
        key = (tuple(path), kind)
        counts[key] = counts.get(key, 0) + 1
        label = {"para": "¶", "item": "item ", "step": "item ", "figure": "image",
                 "table": "row ", "caption": "caption "}[kind]
        pos = label if kind == "figure" else f"{label}{counts[key]}"
        return (" › ".join(path) + " · " if path else "Intro · ") + pos

    def add(kind, el, text, src=None, cap=None):
        text = norm(text)
        if not text and not src:
            return
        out.append({"id": f"{slug}:{len(out) + 1:03d}", "page": slug, "page_title": title,
                    "sec": where(kind), "path": list(path), "anchor": anchor, "kind": kind,
                    "text": text, "src": src, "cap": cap,
                    "pdf_page": pdf_page(el)})

    blocks = [c for c in art.children if isinstance(c, Tag)]
    i = 0
    while i < len(blocks):
        el = blocks[i]
        name = el.name
        if name in HEADINGS:
            level = HEADINGS[name]
            path = path[:level] + [norm(el.get_text())]
            anchor = el.get("id") or anchor
        elif name == "p" and el.find("img"):
            for img in el.find_all("img"):
                cap = None
                nxt = blocks[i + 1] if i + 1 < len(blocks) else None
                if nxt is not None and nxt.name == "p" and not nxt.find("img") and (
                        "caption" in (nxt.get("class") or []) or CAPTION.match(norm(nxt.get_text()))):
                    cap = norm(nxt.get_text())
                    i += 1
                alt = norm(img.get("alt", ""))
                label = " | ".join(x for x in (cap, f"Alt text: “{alt}”" if alt else None) if x)
                add("figure", img, alt, src=img.get("src"), cap=label or None)
        elif name in ("ul", "ol"):
            kind = "step" if name == "ol" else "item"
            for li in el.find_all("li", recursive=False):
                nested = li.find_all(["ul", "ol"], recursive=False)
                for n in nested:
                    n.extract()
                add(kind, li, li.get_text(" "))
                for n in nested:
                    for sub in n.find_all("li"):
                        add(kind, sub, sub.get_text(" "))
        elif name == "table":
            for tr in el.find_all("tr"):
                cells = [norm(c.get_text(" ")) for c in tr.find_all(["td", "th"])]
                for img in tr.find_all("img"):
                    add("figure", img, norm(img.get("alt", "")), src=img.get("src"),
                        cap=" | ".join(c for c in cells if c) or None)
                if any(cells) and tr.find("td"):
                    add("table", tr, " | ".join(cells))
        elif name in ("p", "div", "blockquote", "dl", "figure"):
            text = el.get_text(" ")
            if norm(text):
                add("para", el, text)
        i += 1
    return out


def main():
    book = sys.argv[1].rstrip("/")
    for slug in page_order(book):
        for p in segment_page(book, slug):
            print(json.dumps(p, ensure_ascii=False))


if __name__ == "__main__":
    main()
