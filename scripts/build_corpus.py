"""Build the corpus: the handbook pages as clean HTML with an id on every block and every sentence.

    python scripts/build_corpus.py             # write corpus/{mto,ca,tx}/
    python scripts/build_corpus.py --check     # rebuild in memory and report any page that would change

For each handbook in handbooks/<name>/ this writes corpus/<name>/:
    <page>.html    one file per handbook page: only the handbook content, with ids
    pages.json     page number, file, title and counts for every page
    screening.md   the places a person should look at (long blocks, figures without a caption,
                   possible sentence-split errors, typed list numbers)
corpus/<name>/manual.yaml holds the manual decisions (see the README).

Ids. Pages are numbered in the order of the handbook's table of contents, starting at 1 for the
cover page. Inside a page every block (heading, paragraph, list item, table row, table caption,
figure) is numbered in document order: "10.22" is block 22 of page 10. A block of more than one
sentence has each sentence wrapped in <span id="10.22.2">; a one-sentence block is its own first
sentence. The ids are written into the corpus files, which are committed: rebuilding is only
done on purpose, and --check shows which ids would move.

Nothing is added, dropped or reordered in the text: the script checks that every page's text is
the same as in handbooks/, and that the sentences of every block add up to the block.
"""
import argparse
import html
import json
import os
import re
import sys

import yaml
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HANDBOOKS = ("mto", "ca", "tx")

KEEP_TAGS = {"h1", "h2", "h3", "h4", "p", "ul", "ol", "li", "table", "caption", "thead", "tbody", "tr",
             "th", "td", "figure", "figcaption", "img", "strong", "em", "b", "i", "br", "sup", "sub"}
KEEP_ATTRS = {"img": {"src", "alt"}, "ol": {"start", "type"}, "td": {"colspan", "rowspan"},
              "th": {"colspan", "rowspan"}}
BLOCK_TAGS = ("h2", "h3", "h4", "p", "li", "tr", "caption", "figure")
TEXT_CONTAINERS = ("p", "li", "figcaption", "td", "th", "caption")  # where sentences are numbered
CAPTION_TEXT = re.compile(r"^(Diagram|Figure|Fig\.)\s+[\w.-]+")

# Sentence ends: . ! ? (with any closing quotes or brackets), then space, then an opening quote,
# bracket, capital letter or digit. Abbreviations that end in a period do not end a sentence.
SENTENCE_END = re.compile(r"[.!?][\"'”’)\]]*(?=\s+[\"“‘(\[]?[A-Z0-9])")
ABBREVIATIONS = {"e.g.", "i.e.", "u.s.", "mr.", "mrs.", "ms.", "dr.", "st.", "no.", "vs.", "approx.", "inc.",
                 "a.m.", "p.m.", "etc.", "fig.", "sec.", "ch.", "chpt.", "jr.", "sr."}


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


# ------------------------------------------------------------------------------------------ pages
def page_order(book):
    """Pages in the order of the table of contents in index.html, with index.html first."""
    found = {f[:-5] for f in os.listdir(book) if f.endswith(".html")}
    order = ["index"] if "index" in found else []
    soup = BeautifulSoup(open(os.path.join(book, "index.html"), encoding="utf-8"), "html.parser")
    for a in soup.select("nav a[href$='.html'], aside a[href$='.html']"):
        slug = a["href"].split("#")[0][:-5]
        if slug in found and slug not in order:
            order.append(slug)
    return order + sorted(found - set(order))


def load_manual(name):
    path = os.path.join(ROOT, "corpus", name, "manual.yaml")
    data = yaml.safe_load(open(path, encoding="utf-8")) if os.path.exists(path) else None
    return data or {}


# ------------------------------------------------------------------------------------ cleaning
def new_tag(name):
    return BeautifulSoup("", "html.parser").new_tag(name)


def is_image_paragraph(el):
    return isinstance(el, Tag) and el.name == "p" and el.find("img") is not None and not el.get_text(strip=True)


def is_caption_paragraph(el):
    if not (isinstance(el, Tag) and el.name == "p") or el.find("img"):
        return False
    return "caption" in (el.get("class") or []) or bool(CAPTION_TEXT.match(el.get_text(strip=True)))


def make_figures(art, caption_before_image):
    """An image alone in a paragraph becomes a <figure>. It takes as its <figcaption> a caption
    paragraph right after it ("Diagram 2-46", or class="caption"), or, on pages listed under
    caption_before_image in manual.yaml, the text paragraph right before it. Order is kept: a
    caption written before its image stays before it inside the figure."""
    for p in list(art.find_all("p")):
        if not is_image_paragraph(p):
            continue
        fig = new_tag("figure")
        prev = p.find_previous_sibling()
        nxt = p.find_next_sibling()
        if caption_before_image and isinstance(prev, Tag) and prev.name == "p" and not prev.find("img") \
                and prev.get_text(strip=True) and prev.parent is p.parent and not prev.find_parent("figure"):
            cap = new_tag("figcaption")
            for child in list(prev.contents):
                cap.append(child.extract())
            fig.append(cap)
            prev.decompose()
        for img in p.find_all("img"):
            fig.append(img.extract())
        if not fig.find("figcaption") and is_caption_paragraph(nxt):
            cap = new_tag("figcaption")
            for child in list(nxt.contents):
                cap.append(child.extract())
            fig.append(cap)
            nxt.decompose()
        p.replace_with(fig)


def clean(art):
    """Keep only content tags and the attributes a reader of the text needs."""
    for el in list(art.find_all(True)):
        if el.name not in KEEP_TAGS:
            el.unwrap()
        else:
            keep = KEEP_ATTRS.get(el.name, set())
            el.attrs = {k: v for k, v in el.attrs.items() if k in keep}


# ----------------------------------------------------------------------------------- sentences
def sentence_ends(text):
    """Offsets just after each sentence end in `text` (not counting the end of the text)."""
    ends = []
    for m in SENTENCE_END.finditer(text):
        before = text[:m.start() + 1]
        word = before.split()[-1]
        if word.lower() in ABBREVIATIONS or re.fullmatch(r"(?:[a-z]\.){2,}", word.lower()):
            continue
        if re.fullmatch(r"[A-Z]\.", word):          # an initial: "Freeman F. Martin"
            continue
        if re.fullmatch(r"\d+\.", word) and not before[:-len(word)].strip():  # a typed list number: "2. Right turn."
            continue
        if re.fullmatch(r"\s*\([^()]{1,25}\)\.?\s*", text[m.end():]):     # a short closing aside: "… ? (Chpt. 5)"
            continue
        ends.append(m.end())
    return ends


def own_children(el):
    """The children of a text container up to its first nested list (that list is numbered itself)."""
    out = []
    for c in el.children:
        if isinstance(c, Tag) and c.name in ("ul", "ol", "table"):
            break
        out.append(c)
    return out


def wrap_sentences(container, block_id, counter):
    """Wrap each sentence of `container` in <span id="block.k">, continuing the block's count.
    A sentence end that falls inside an inline tag (rare) is skipped, so tags are never split."""
    kids = own_children(container)
    text = "".join(k if isinstance(k, NavigableString) else k.get_text() for k in kids)
    if not text.strip():
        return counter
    cuts = sentence_ends(text)
    pieces, pos = [[]], 0
    for k in kids:
        t = str(k) if isinstance(k, NavigableString) else k.get_text()
        start, end = pos, pos + len(t)
        if isinstance(k, NavigableString):
            inner = [c - start for c in cuts if start < c < end]
            prev = 0
            for c in inner:
                pieces[-1].append(NavigableString(t[prev:c]))
                pieces.append([])
                prev = c
            pieces[-1].append(NavigableString(t[prev:]))
            if end in cuts:
                pieces.append([])
        else:
            pieces[-1].append(k)
            if end in cuts:
                pieces.append([])
        pos = end
    pieces = [p for p in pieces if "".join(x if isinstance(x, NavigableString) else x.get_text() for x in p).strip()]
    if len(pieces) <= 1 and counter == 0 and container.name not in ("td", "th"):
        return counter + 1
    anchor = kids[-1].next_sibling if kids else None
    for k in kids:
        k.extract()
    nodes = []
    for p in pieces:
        counter += 1
        lead = ""
        if isinstance(p[0], NavigableString):  # keep the space between sentences outside the span
            s = str(p[0])
            lead, p[0] = s[:len(s) - len(s.lstrip())], NavigableString(s.lstrip())
        trail = ""
        if isinstance(p[-1], NavigableString):
            s = str(p[-1])
            trail, p[-1] = s[len(s.rstrip()):], NavigableString(s.rstrip())
        span = new_tag("span")
        span["id"] = f"{block_id}.{counter}"
        for x in p:
            span.append(x)
        nodes += ([NavigableString(lead)] if lead else []) + [span] + ([NavigableString(trail)] if trail else [])
    for n in nodes:
        if anchor is not None:
            anchor.insert_before(n)
        else:
            container.append(n)
    return counter


def text_containers(block):
    """The containers whose sentences belong to `block`, in order."""
    if block.name in ("p", "li", "caption"):
        return [block]
    if block.name == "figure":
        return block.find_all("figcaption")
    if block.name == "tr":
        return block.find_all(["td", "th"], recursive=False)
    return []


def blocks_of(art):
    for el in art.find_all(BLOCK_TAGS):
        if el.name == "p" and el.find_parent(["li", "td", "th", "figure", "caption"]):
            continue
        yield el


def own_sentences(block):
    """The sentence spans of this block itself (a nested list's items are blocks of their own)."""
    return [s for s in block.find_all("span", id=True) if s["id"].rsplit(".", 1)[0] == block["id"]]


def sentence_count(block):
    """Headings have no sentences; a text block has its spans, or one sentence if it has no spans."""
    if block.name in ("h2", "h3", "h4"):
        return 0
    spans = own_sentences(block)
    if spans:
        return len(spans)
    return 1 if any(norm(c.get_text()) for c in text_containers(block)) else 0


def number_page(art, page_no):
    blocks = list(blocks_of(art))
    for n, block in enumerate(blocks, 1):
        bid = f"{page_no}.{n}"
        block["id"] = bid
        counter = 0
        for c in text_containers(block):
            counter = wrap_sentences(c, bid, counter)
    return len(blocks), sum(sentence_count(b) for b in blocks)


# -------------------------------------------------------------------------------------- output
def serialize(art, name, slug, page_no, title):
    title = html.escape(title, quote=False)
    body = str(art)
    body = re.sub(r"(<(?:h[1-4]|p|ul|ol|li|table|caption|tr|figure)[ >])", r"\n\1", body)
    body = re.sub(r"(</(?:ul|ol|table)>)", r"\n\1", body)
    body = re.sub(r"\n+", "\n", body).strip()
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            f"<title>{title}</title>\n"
            f"<base href=\"../../handbooks/{name}/\">  <!-- image paths are relative to the handbook folder -->\n"
            f"<meta name=\"source\" content=\"handbooks/{name}/{slug}.html\">\n</head>\n<body>\n"
            f"<h1 id=\"{page_no}.0\">{title}</h1>\n{body}\n</body>\n</html>\n")


def build_page(name, slug, page_no, manual):
    book = os.path.join(ROOT, "handbooks", name)
    soup = BeautifulSoup(open(os.path.join(book, slug + ".html"), encoding="utf-8"), "html.parser")
    art = soup.find("article", class_="content")
    h1 = soup.find("h1")
    title = norm(h1.get_text(" ")) if h1 else slug
    if art is None:
        art = BeautifulSoup("<article></article>", "html.parser").article
    before = norm(art.get_text(" "))
    make_figures(art, slug in (manual.get("caption_before_image") or []))
    clean(art)
    art.name = "article"
    art.attrs = {"data-handbook": name, "data-page": str(page_no), "data-file": slug}
    blocks, sentences = number_page(art, page_no)
    after = norm(art.get_text(" "))
    if re.sub(r"\s", "", before) != re.sub(r"\s", "", after):
        raise SystemExit(f"{name}/{slug}: the text changed while building the corpus")
    return art, {"page": page_no, "file": slug, "title": title, "blocks": blocks, "sentences": sentences,
                 "images": len(art.find_all("img"))}, serialize(art, name, slug, page_no, title)


# ----------------------------------------------------------------------------------- screening
GENERIC_ALT = re.compile(r"^(a |an )?(regulatory|warning|temporary condition|information|guide) sign$|^image$|^$", re.I)


def screening(name, pages):
    lines = [f"# Screening: {name}", "",
             "Places in the corpus a person should look at before the handbook is used. Generated by "
             "`scripts/build_corpus.py`; decisions go into `manual.yaml` in this folder.", ""]
    long_blocks, figs, short_sents, typed = [], [], [], []
    for art, meta in pages:
        blocks = list(blocks_of(art))
        for i, b in enumerate(blocks):
            words = len(b.get_text(" ").split())
            spans = b.find_all("span", id=True)
            if b.name != "figure" and (len(spans) > 3 or words > 80):
                long_blocks.append((b["id"], len(spans) or 1, words, norm(b.get_text(" "))[:90]))
            if b.name == "figure" and not b.find("figcaption"):
                for img in b.find_all("img"):
                    if GENERIC_ALT.match(norm(img.get("alt", ""))):
                        prev = blocks[i - 1] if i > 0 else None
                        nxt = blocks[i + 1] if i + 1 < len(blocks) else None
                        figs.append((b["id"], img["src"], img.get("alt", ""),
                                     norm(prev.get_text(" "))[:60] if prev else "",
                                     norm(nxt.get_text(" "))[:60] if nxt else ""))
            for s in spans:
                if len(s.get_text().split()) < 3 and not s.find_parent(["td", "th"]):  # cells are often labels
                    short_sents.append((s["id"], norm(s.get_text())))
            if b.name == "p" and re.match(r"^\d+\.\s", b.get_text(strip=True)):
                typed.append((b["id"], norm(b.get_text(" "))[:80]))

    def table(title, intro, head, rows, fmt):
        out = [f"## {title} ({len(rows)})", "", intro, ""]
        if rows:
            out += [head, "|" + "---|" * (head.count("|") - 1)] + [fmt(r) for r in rows]
        return out + [""]

    lines += table("Figures with no caption and an alt text that names no sign",
                   "A model that does not see the image cannot tell what these show. If the text before or after "
                   "describes the image, pair them in `manual.yaml`.",
                   "| Figure | Image | Alt text | Text before | Text after |",
                   figs, lambda r: f"| `{r[0]}` | `{r[1]}` | {r[2] or '(empty)'} | {r[3]} | {r[4]} |")
    lines += table("Long blocks", "Blocks of more than 3 sentences or more than 80 words. Their sentences have ids, "
                   "so a rule can still cite one sentence; split a block only if its sentences belong to different topics.",
                   "| Block | Sentences | Words | Starts with |",
                   long_blocks, lambda r: f"| `{r[0]}` | {r[1]} | {r[2]} | {r[3]} |")
    lines += table("Very short sentences", "Sentences of one or two words outside tables: usually a short command "
                   "(\"Stop.\"), sometimes a label or a split in the wrong place.",
                   "| Sentence | Text |", short_sents, lambda r: f"| `{r[0]}` | {r[1]} |")
    lines += table("Paragraphs that start with a typed number", "Probably list items written as paragraphs.",
                   "| Block | Starts with |", typed, lambda r: f"| `{r[0]}` | {r[1]} |")
    return "\n".join(lines)


# ----------------------------------------------------------------------------------------- main
def build(name, write, check):
    manual = load_manual(name)
    out_dir = os.path.join(ROOT, "corpus", name)
    pages, metas, changed = [], [], []
    for page_no, slug in enumerate(page_order(os.path.join(ROOT, "handbooks", name)), 1):
        art, meta, html = build_page(name, slug, page_no, manual)
        pages.append((art, meta))
        metas.append(meta)
        path = os.path.join(out_dir, slug + ".html")
        if check and (not os.path.exists(path) or open(path, encoding="utf-8").read() != html):
            changed.append(slug)
        if write:
            os.makedirs(out_dir, exist_ok=True)
            open(path, "w", encoding="utf-8").write(html)
    if write:
        json.dump(metas, open(os.path.join(out_dir, "pages.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        open(os.path.join(out_dir, "screening.md"), "w", encoding="utf-8").write(screening(name, pages) + "\n")
    blocks, sents = sum(m["blocks"] for m in metas), sum(m["sentences"] for m in metas)
    print(f"{name}: {len(metas)} pages, {blocks:,} blocks, {sents:,} sentences"
          + (f"; would change: {', '.join(changed) or 'nothing'}" if check else f" -> corpus/{name}/"))
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report pages whose corpus file would change; write nothing")
    ap.add_argument("--only", choices=HANDBOOKS)
    a = ap.parse_args()
    changed = [build(n, write=not a.check, check=a.check) for n in ([a.only] if a.only else HANDBOOKS)]
    if a.check and any(changed):
        sys.exit(1)


if __name__ == "__main__":
    main()
