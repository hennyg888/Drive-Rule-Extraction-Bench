"""The corpus: the handbook pages as clean HTML with an id on every block and every sentence.

For each handbook in handbooks/<id>/, `build` writes corpus/<id>/:
    <page>.html    one file per handbook page: only the handbook content, with ids
    pages.json     page number, file, title and counts for every page
    screening.md   places a person should look at (see screening.py)
corpus/<id>/manual.yaml holds the manual decisions (see the README).

Ids. Pages are numbered in the order of the handbook's table of contents, starting at 1 for the
cover page. Inside a page every block (heading, paragraph, list item, table row, table caption,
figure) is numbered in document order: "10.22" is block 22 of page 10. A block of more than one
sentence has each sentence wrapped in <span id="10.22.2">; a one-sentence block is its own first
sentence. The ids are written into the corpus files, which are committed: rebuilding is only
done on purpose, and `check` shows which ids would move.

Nothing is added, dropped or reordered in the text: every page's text is checked against
handbooks/, and the sentences of every block add up to the block.

The readers at the end (load_pages, page_soup, blocks_of, ...) are what the other modules use.
"""
import html
import json
import os
import re

import yaml
from bs4 import BeautifulSoup, Tag

from . import handbooks, sentences
from .handbooks import norm

KEEP_TAGS = {"h1", "h2", "h3", "h4", "p", "ul", "ol", "li", "table", "caption", "thead", "tbody", "tr",
             "th", "td", "figure", "figcaption", "img", "strong", "em", "b", "i", "br", "sup", "sub"}
KEEP_ATTRS = {"img": {"src", "alt"}, "ol": {"start", "type"}, "td": {"colspan", "rowspan"},
              "th": {"colspan", "rowspan"}}
BLOCK_TAGS = ("h2", "h3", "h4", "p", "li", "tr", "caption", "figure")
CAPTION_TEXT = re.compile(r"^(Diagram|Figure|Fig\.)\s+[\w.-]+")


def load_manual(hb):
    path = os.path.join(hb.corpus_folder, "manual.yaml")
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


# ------------------------------------------------------------------------------------- numbering
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
            counter = sentences.wrap(c, bid, counter, always=c.name in ("td", "th"))
    return len(blocks), sum(sentence_count(b) for b in blocks)


# -------------------------------------------------------------------------------------- building
def serialize(art, hb_id, slug, page_no, title):
    title = html.escape(title, quote=False)
    body = str(art)
    body = re.sub(r"(<(?:h[1-4]|p|ul|ol|li|table|caption|tr|figure)[ >])", r"\n\1", body)
    body = re.sub(r"(</(?:ul|ol|table)>)", r"\n\1", body)
    body = re.sub(r"\n+", "\n", body).strip()
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            f"<title>{title}</title>\n"
            f"<base href=\"../../handbooks/{hb_id}/\">  <!-- image paths are relative to the handbook folder -->\n"
            f"<meta name=\"source\" content=\"handbooks/{hb_id}/{slug}.html\">\n</head>\n<body>\n"
            f"<h1 id=\"{page_no}.0\">{title}</h1>\n{body}\n</body>\n</html>\n")


def build_page(hb, slug, page_no, manual):
    """(article, page meta, corpus file text) of one page."""
    title, art = handbooks.read_page(hb, slug)
    before = norm(art.get_text(" "))
    make_figures(art, slug in (manual.get("caption_before_image") or []))
    clean(art)
    art.name = "article"
    art.attrs = {"data-handbook": hb.id, "data-page": str(page_no), "data-file": slug}
    blocks, sents = number_page(art, page_no)
    after = norm(art.get_text(" "))
    if re.sub(r"\s", "", before) != re.sub(r"\s", "", after):
        raise SystemExit(f"{hb.id}/{slug}: the text changed while building the corpus")
    meta = {"page": page_no, "file": slug, "title": title, "blocks": blocks, "sentences": sents,
            "images": len(art.find_all("img"))}
    return art, meta, serialize(art, hb.id, slug, page_no, title)


def build(handbook_id, write=True, check=False, log=print):
    """Build one handbook's corpus. With write, write corpus/<id>/; with check, return the pages
    whose corpus file differs from what would be written now."""
    from .screening import screening
    hb = handbooks.get(handbook_id)
    manual = load_manual(hb)
    pages, metas, changed = [], [], []
    for page_no, slug in enumerate(handbooks.page_order(hb), 1):
        art, meta, text = build_page(hb, slug, page_no, manual)
        pages.append((art, meta))
        metas.append(meta)
        path = os.path.join(hb.corpus_folder, slug + ".html")
        if check and (not os.path.exists(path) or open(path, encoding="utf-8").read() != text):
            changed.append(slug)
        if write:
            os.makedirs(hb.corpus_folder, exist_ok=True)
            open(path, "w", encoding="utf-8").write(text)
    if write:
        json.dump(metas, open(os.path.join(hb.corpus_folder, "pages.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        open(os.path.join(hb.corpus_folder, "screening.md"), "w", encoding="utf-8").write(screening(hb, pages) + "\n")
    blocks, sents = sum(m["blocks"] for m in metas), sum(m["sentences"] for m in metas)
    log(f"{hb.id}: {len(metas)} pages, {blocks:,} blocks, {sents:,} sentences"
        + (f"; would change: {', '.join(changed) or 'nothing'}" if check else f" -> corpus/{hb.id}/"))
    return changed


# --------------------------------------------------------------------------------------- reading
def load_pages(handbook_id):
    """The entries of corpus/<id>/pages.json: page, file, title, blocks, sentences, images."""
    hb = handbooks.get(handbook_id)
    return json.load(open(os.path.join(hb.corpus_folder, "pages.json"), encoding="utf-8"))


def page_soup(handbook_id, meta):
    """The parsed corpus file of one page (`meta`: an entry of pages.json)."""
    hb = handbooks.get(handbook_id)
    return BeautifulSoup(open(os.path.join(hb.corpus_folder, meta["file"] + ".html"), encoding="utf-8"),
                         "html.parser")


def parse_pages(spec, handbook_id):
    """Page numbers from "10", "9-11", a page file name ("changing-positions"), or a comma list of
    these. None or "" means all pages (returns None)."""
    if not spec:
        return None
    by_file = {p["file"]: p["page"] for p in load_pages(handbook_id)}
    nums = set()
    for item in str(spec).split(","):
        item = item.strip()
        if re.fullmatch(r"\d+-\d+", item):
            a, b = map(int, item.split("-"))
            nums |= set(range(a, b + 1))
        elif item.isdigit():
            nums.add(int(item))
        elif item in by_file:
            nums.add(by_file[item])
        else:
            raise SystemExit(f"{handbook_id}: no page {item!r}")
    return nums
