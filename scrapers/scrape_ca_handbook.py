"""Download the California DMV Driver's Handbook (dmv.ca.gov) as local, cleanly formatted HTML.

Same output format as scrape_mto_handbook.py, so one segmenter can read both handbooks.

Output: handbooks/ca/
    index.html, <page-slug>.html ...   one file per handbook web page, in the handbook's order
    images/                            every image referenced by the content
    style.css                          shared stylesheet
Every heading (h2/h3/h4) gets a stable slug id. Links between handbook pages are rewritten to
the local files; all other links are made absolute so they still resolve.

The site is WordPress: each page's handbook text is in div.handbook-page-content. The page
title is h2.handbook-section__title (the h1 is the same "California Driver's Handbook" banner
on every page). The page order is the site's own table of contents, which matches the
Previous/Next chain. The "-cont1"/"-cont2" pages are separate web pages and stay separate files.
"""
import datetime
import html
import json
import os
import re
import sys
import time
from urllib.parse import urljoin, urlparse, unquote

import requests
from bs4 import BeautifulSoup, NavigableString, Comment, Tag

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True  # don't leave a __pycache__ in the repo from this import
# generic helpers shared with the MTO copy (page shell pieces, stylesheet, block/void tag sets)
from scrape_mto_handbook import BLOCK, VOID, CSS as MTO_CSS, _open, pager_html, toc_html  # noqa: E402

BASE = "https://www.dmv.ca.gov"
BOOK = "/portal/handbook/california-driver-handbook"
HOSTS = {"www.dmv.ca.gov", "dmv.ca.gov"}
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "handbooks", "ca")
IMG_DIR = os.path.join(OUT, "images")
DELAY = 1.0  # seconds between requests to the server
PDF_URL = BASE + "/portal/file/california-driver-handbook-pdf/"

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"
_last_request = 0.0


def fetch(url):
    """GET with retries, sequential and rate limited."""
    global _last_request
    for attempt in range(4):
        wait = DELAY - (time.time() - _last_request)
        if wait > 0:
            time.sleep(wait)
        try:
            r = session.get(url, timeout=60)
            _last_request = time.time()
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            _last_request = time.time()
            if attempt == 3:
                raise
            print(f"  retry {url}: {e}")
            time.sleep(2 * (attempt + 1))


def get_soup(url):
    r = fetch(url)
    r.encoding = "utf-8"
    return BeautifulSoup(r.text, "html.parser")


def page_url(slug):
    return BASE + BOOK + "/" + ("" if slug == "index" else slug + "/")


def slug_of(path):
    """'/portal/handbook/california-driver-handbook/foo/' -> 'foo'; book root -> 'index'."""
    path = path.rstrip("/")
    if path == BOOK:
        return "index"
    if path.startswith(BOOK + "/"):
        rest = path[len(BOOK) + 1:]
        return rest if rest and "/" not in rest else None
    return None


def esc(text):
    return html.escape(text, quote=False)


# ---------------------------------------------------------------- table of contents
def read_toc(soup):
    """Return [(title, slug)] from the site's table of contents (two <ul> columns)."""
    items = []
    for a in soup.select("nav#handbook-toc ul.toc-menu > li a[href]"):
        slug = slug_of(urlparse(urljoin(BASE, a["href"])).path)
        if slug:
            items.append((a.get_text(" ", strip=True), slug))
    return items


# ---------------------------------------------------------------- images
_img_cache = {}  # absolute url -> "images/<name>"


def local_image(src, page):
    """Download an image once, return its path relative to the page."""
    url = urljoin(page, src)
    if url in _img_cache:
        return _img_cache[url]
    name = unquote(os.path.basename(urlparse(url).path)) or "image"
    name = re.sub(r"[^\w.\-]", "_", name)
    stem, ext = os.path.splitext(name)
    used = {os.path.basename(v) for v in _img_cache.values()}
    candidate, n = name, 1
    while candidate in used:
        candidate = f"{stem}_{n}{ext}"
        n += 1
    path = os.path.join(IMG_DIR, candidate)
    if not os.path.exists(path):
        data = fetch(url).content
        with open(path, "wb") as f:
            f.write(data)
    _img_cache[url] = f"images/{candidate}"
    return _img_cache[url]


IMG_EXT = re.compile(r"\.(png|jpe?g|gif|svg|webp)$", re.I)


# ---------------------------------------------------------------- content cleanup
KEEP_ATTRS = {
    "a": {"href", "title"},
    "img": {"src", "alt", "width", "height", "title"},
    "td": {"colspan", "rowspan"},
    "th": {"colspan", "rowspan", "scope"},
    "ol": {"start", "type", "reversed"},
    "h2": {"id"}, "h3": {"id"}, "h4": {"id"}, "h5": {"id"}, "h6": {"id"},
}
UNWRAP = ["body", "div", "section", "span", "font", "center"]


def slugify(text):
    t = text.lower().replace("’", "").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-") or "section"


def clean_content(body, slug, soup):
    """Reduce the WordPress block markup to plain h2-h4/p/ul/ol/li/table/img. Returns headings."""
    page = page_url(slug)
    for t in body.find_all(["script", "style", "noscript", "iframe", "svg", "button", "form",
                            "input", "select", "template"]):
        t.decompose()
    for c in body.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    # responsive table-cell labels: hidden on desktop, repeat the column header on phones
    for t in body.select("span.mobile-title"):
        t.decompose()
    # "Note" / "Important" call-out badges -> <strong>Note</strong> text
    for t in body.select("span.format-label__text"):
        t.name = "strong"
        t.attrs = {}

    # figures: tables are unwrapped; images become <p><img></p> with the caption in the next <p>
    for fig in body.find_all("figure"):
        if fig.find("table"):
            fig.unwrap()
            continue
        imgs = fig.find_all("img")
        cap = fig.find("figcaption")
        new = []
        if imgs:
            p = soup.new_tag("p")
            for i in imgs:
                p.append(i.extract())
            new.append(p)
        if cap and cap.get_text(strip=True):
            cap.name = "p"
            new.append(cap.extract())
        for n in reversed(new):
            fig.insert_after(n)
        fig.decompose()

    for t in body.find_all(UNWRAP):
        t.unwrap()
    for h in body.find_all(["h2", "h3", "h4", "h5", "h6"]):
        for t in h.find_all(["strong", "b"]):
            t.unwrap()

    for img in body.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if src:
            img["src"] = local_image(src, page)

    for a in body.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("#", "mailto:", "tel:")):
            a["href"] = href
            continue
        absolute = urljoin(page, href)
        parsed = urlparse(absolute)
        target = slug_of(parsed.path) if parsed.netloc in HOSTS else None
        if target:
            a["href"] = ("" if target == slug and parsed.fragment else f"{target}.html") + \
                        (f"#{parsed.fragment}" if parsed.fragment else "")
        elif IMG_EXT.search(parsed.path) and parsed.netloc in HOSTS:
            a["href"] = local_image(absolute, page)  # link to a larger image version
        else:
            a["href"] = absolute

    # keep only meaningful attributes (drops class, style, data-*, role, srcset, loading, ...)
    for t in body.find_all(True):
        keep = KEEP_ATTRS.get(t.name, set())
        t.attrs = {k: v for k, v in t.attrs.items() if k in keep}

    # drop empty spacer paragraphs and empty inline wrappers
    for t in body.find_all(["strong", "em", "b", "i", "a"]):
        if not t.get_text(strip=True) and not t.find("img"):
            t.unwrap() if t.name != "a" else t.decompose()
    for p in body.find_all("p"):
        if not p.get_text(strip=True) and not p.find("img"):
            p.decompose()
    body.smooth()

    # stable slug id on every heading (ids already on the site, e.g. #rightofway, are kept)
    used = set()
    headings = []
    for h in body.find_all(["h2", "h3", "h4", "h5", "h6"]):
        text = h.get_text(" ", strip=True)
        base = h.get("id") or slugify(text)
        hid, n = base, 2
        while hid in used:
            hid, n = f"{base}-{n}", n + 1
        h["id"] = hid
        used.add(hid)
        headings.append((int(h.name[1]), hid, text))
    return headings


# ---------------------------------------------------------------- pretty printing
def _inline(nodes):
    s = re.sub(r"\s+", " ", "".join(str(n) for n in nodes)).strip()
    return s


def pretty(node, depth=0):
    """Indent block-level structure; keep each run of inline content on one line.

    Like the MTO helper, but a run of text and inline tags that sits next to a nested block
    (e.g. '<li>Text <strong>x</strong> more<ul>...') stays together on one line, so no
    spacing is added or lost between inline pieces.
    """
    ind = "  " * depth
    if isinstance(node, NavigableString):
        text = str(node)
        return [ind + re.sub(r"\s+", " ", text).strip()] if text.strip() else []
    if node.name in VOID:
        return [ind + str(node)]
    has_block = any(isinstance(c, Tag) and c.name in BLOCK for c in node.children)
    if not has_block:
        return [ind + _open(node) + _inline(node.children) + f"</{node.name}>"]
    lines = [ind + _open(node)]
    run = []
    for c in list(node.children) + [None]:
        if c is None or (isinstance(c, Tag) and c.name in BLOCK):
            text = _inline(run)
            if text:
                lines.append(ind + "  " + text)
            run = []
            if c is not None:
                lines += pretty(c, depth + 1)
        else:
            run.append(c)
    lines.append(ind + f"</{node.name}>")
    return lines


# ---------------------------------------------------------------- page assembly
PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | California Driver's Handbook</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="site-header"><a href="index.html">California Driver’s Handbook (California DMV)</a></header>
<div class="layout">
<nav class="book-toc" aria-label="Table of contents">
<h2>Table of contents</h2>
{toc}
</nav>
<main>
<h1>{title}</h1>
{pager}
{onpage}
<article class="content">
{content}
</article>
{dates}
{pager}
<p class="source">Source: <a href="{source}">{source}</a></p>
</main>
</div>
</body>
</html>
"""

CSS = MTO_CSS + """.on-this-page ol ol { columns:1; margin:2px 0 6px; font-size:.95em; }
.content td img { display:block; margin:0 auto; }
"""


def onpage_html(headings):
    """'On this page' list: h2 entries with their h3 sub-sections nested (h3s before any h2 stay top level)."""
    top = []
    for level, hid, text in headings:
        if level == 2 or (level == 3 and not top):
            top.append([hid, text, []])
        elif level == 3:
            top[-1][2].append((hid, text))
    if sum(1 + len(kids) for _, _, kids in top) < 2:
        return ""
    items = []
    for hid, text, kids in top:
        sub = "<ol>" + "".join(f'<li><a href="#{k}">{esc(t)}</a></li>' for k, t in kids) + "</ol>" if kids else ""
        items.append(f'<li><a href="#{hid}">{esc(text)}</a>{sub}</li>')
    return f'<nav class="on-this-page"><h2>On this page</h2><ol>{"".join(items)}</ol></nav>'


def fmt_date(iso):
    d = datetime.date.fromisoformat(iso[:10])
    return f"{d:%B} {d.day}, {d.year}"


def page_dates(soup):
    """(published, modified) ISO strings from the page metadata (the site does not print them)."""
    published = modified = None
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(s.string or "")
        except ValueError:
            continue
        for node in data.get("@graph", [data]) if isinstance(data, dict) else []:
            if isinstance(node, dict) and "WebPage" in str(node.get("@type")):
                published = published or node.get("datePublished")
                modified = modified or node.get("dateModified")
    meta = soup.find("meta", property="article:modified_time")
    if not modified and meta:
        modified = meta.get("content")
    return published, modified


def scrape_page(slug):
    url = page_url(slug)
    print(f"[{slug}] {url}")
    soup = get_soup(url)
    t = soup.select_one("h2.handbook-section__title")
    title = t.get_text(" ", strip=True) if t else soup.find("h1").get_text(" ", strip=True)
    bodies = soup.select("div.handbook-page-content")
    if len(bodies) != 1:
        raise RuntimeError(f"{url}: expected one div.handbook-page-content, found {len(bodies)}")
    body = bodies[0]
    nxt = soup.select_one("nav.handbook-pagination a.btn-next[href]")
    next_slug = slug_of(urlparse(urljoin(url, nxt["href"])).path) if nxt else None
    headings = clean_content(body, slug, soup)
    published, modified = page_dates(soup)
    content = "\n".join(line for c in body.children for line in pretty(c))
    return dict(slug=slug, url=url, title=title, headings=headings, content=content,
                published=published, modified=modified, next_slug=next_slug)


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    with open(os.path.join(OUT, "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    retrieved = datetime.date.today().isoformat()

    cover = page_url("index")
    toc_soup = get_soup(cover)
    slugs = list(dict.fromkeys(["index"] + [s for _, s in read_toc(toc_soup)]))

    pages = [scrape_page(s) for s in slugs]

    # the TOC order should match the site's Previous/Next chain
    for a, b in zip(pages, pages[1:] + [None]):
        expected = b["slug"] if b else None
        if a["next_slug"] != expected:
            print(f"  WARNING: {a['slug']} 'Next' points to {a['next_slug']}, TOC says {expected}")

    toc = [(esc(p["title"]), p["slug"], []) for p in pages]
    entries = [(esc(p["title"]), p["slug"]) for p in pages]
    for i, p in enumerate(pages):
        prev = entries[i - 1] if i > 0 else None
        nxt = entries[i + 1] if i + 1 < len(entries) else None
        bits = []
        if p["modified"]:
            bits.append(f"Updated: {fmt_date(p['modified'])}")
        if p["published"]:
            bits.append(f"Published: {fmt_date(p['published'])}")
        bits.append(f"Retrieved: {fmt_date(retrieved)}")
        dates = '<p class="dates">' + " &middot; ".join(bits) + "</p>"
        out = PAGE.format(title=esc(p["title"]), toc=toc_html(toc, p["slug"]), pager=pager_html(prev, nxt),
                          onpage=onpage_html(p["headings"]), content=p["content"], dates=dates, source=p["url"])
        with open(os.path.join(OUT, f"{p['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(out)

    print(f"\nSaved {len(pages)} pages and {len(_img_cache)} images to {OUT}")

    # The official PDF of the same handbook (DL 600), kept beside the web copy for reference.
    pdf = os.path.join(OUT, "source", "DL-600.pdf")
    if not os.path.exists(pdf):
        os.makedirs(os.path.dirname(pdf), exist_ok=True)
        with open(pdf, "wb") as f:
            f.write(fetch(PDF_URL).content)
        print(f"Saved the PDF edition to {pdf}")


if __name__ == "__main__":
    main()
