"""Corpus pages -> the content of one user message for a vision-language model.

The content follows the handbook: first a table of contents (each page and its sections, with
their ids), then each page in order as HTML, with every image placed right after its <img> tag.
Block ids (10.22) are kept; the sentence <span>s of the corpus are removed, since a model cites a
block id with the quoted sentence and grounding.py finds the sentence ids.

Content is a list of parts in a form that belongs to no API:
    {"type": "text", "text": "..."}
    {"type": "image", "media_type": "image/png", "data": "<base64>", "src": "images/x.png"}
Each model provider (models/) turns these parts into its own API's format.
"""
import base64
import io
import os
import re

from bs4 import BeautifulSoup
from PIL import Image

from . import handbooks
from .corpus import load_pages, page_soup

IMG_TAG = re.compile(r"<img\b[^>]*>")
LABEL = re.compile(r"^(sign|shape|diagram|image|figure)\s*:\s*", re.I)
MEDIA_TYPES = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}


def _same(a, b):
    def n(s):
        return re.sub(r"\s+", " ", LABEL.sub("", s or "")).strip().lower()
    return n(a) == n(b)


def page_html(handbook_id, meta):
    """One page as the model sees it: <article data-page> with the title and blocks, no sentence spans."""
    soup = page_soup(handbook_id, meta)
    for span in soup.find_all("span", id=True):
        span.unwrap()
    for img in soup.find_all("img"):                 # drop alt text that only repeats the caption or cell text
        fig, row = img.find_parent("figure"), img.find_parent("tr")
        if fig is not None and fig.find("figcaption"):
            near = fig.find("figcaption").get_text(" ")
        elif row is not None:
            near = " ".join(c.get_text(" ") for c in row.find_all(["td", "th"]) if c is not img.parent)
        else:
            near = None
        if near is not None and img.get("alt") and _same(img["alt"], near):
            img["alt"] = ""
    h1, art = soup.find("h1"), soup.find("article")
    body = "\n".join(str(x) for x in [h1, *art.contents] if str(x).strip())
    return f'<article data-page="{meta["page"]}">\n{body}\n</article>'


def contents_html(handbook_id, pages):
    """The table of contents: every page with its sections (h2), and their ids."""
    items = []
    for meta in pages:
        soup = page_soup(handbook_id, meta)
        secs = "".join(f'<li data-ref="{h["id"]}">{h.get_text(" ", strip=True)}</li>' for h in soup.find_all("h2"))
        items.append(f'<li data-page="{meta["page"]}">{meta["title"]}' + (f"<ul>{secs}</ul>" if secs else "") + "</li>")
    name = handbooks.get(handbook_id).name
    return f"<nav>\n<h1>Contents: {name}</h1>\n<ol>\n" + "\n".join(items) + "\n</ol>\n</nav>"


def image_part(handbook_id, src):
    """The image file as a part. GIF images are sent as PNG (their first frame), which every API accepts."""
    path = os.path.join(handbooks.get(handbook_id).folder, src)
    ext = os.path.splitext(src)[1].lower()
    if ext == ".gif":
        buf = io.BytesIO()
        Image.open(path).convert("RGBA").save(buf, "PNG")
        data, media_type = buf.getvalue(), "image/png"
    else:
        data, media_type = open(path, "rb").read(), MEDIA_TYPES[ext]
    return {"type": "image", "media_type": media_type, "data": base64.b64encode(data).decode("ascii"), "src": src}


def to_parts(handbook_id, html, images=True):
    """Split the HTML after every <img> tag and put the image there. Without images, one text part
    (the <img> tags stay, with their alt text)."""
    if not images:
        return [{"type": "text", "text": html}]
    parts, pos = [], 0
    for m in IMG_TAG.finditer(html):
        parts.append({"type": "text", "text": html[pos:m.end()]})
        parts.append(image_part(handbook_id, BeautifulSoup(m.group(0), "html.parser").img["src"]))
        pos = m.end()
    if html[pos:].strip():
        parts.append({"type": "text", "text": html[pos:]})
    return parts


def build(handbook_id, page_numbers=None, images=True, per_page=False, toc=True):
    """[{"pages": [10], "content": [parts]}]: one message for the chosen pages (all if None), or
    one per page with per_page. Every message starts with the table of contents unless toc=False."""
    pages = load_pages(handbook_id)
    chosen = [p for p in pages if page_numbers is None or p["page"] in page_numbers]
    if not chosen:
        raise SystemExit(f"{handbook_id}: no pages chosen")
    groups = [[p] for p in chosen] if per_page else [chosen]
    out = []
    for group in groups:
        html = "\n\n".join(([contents_html(handbook_id, pages)] if toc else [])
                           + [page_html(handbook_id, p) for p in group])
        out.append({"pages": [p["page"] for p in group], "content": to_parts(handbook_id, html, images)})
    return out


def preview(content):
    """The content as text for people: the HTML, and [image: src] where each image goes."""
    return "".join(p["text"] if p["type"] == "text" else f"\n[image: {p.get('src', '')}]\n" for p in content)


def summary(content):
    n_img = sum(1 for p in content if p["type"] == "image")
    n_chr = sum(len(p["text"]) for p in content if p["type"] == "text")
    return f"{n_chr:,} characters of HTML, {n_img} images"
