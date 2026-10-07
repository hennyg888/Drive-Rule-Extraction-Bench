"""Download the Official MTO Driver's Handbook (ontario.ca) as local, cleanly formatted HTML.

Output: mto_drivers_handbook/
    index.html, <chapter-slug>.html ...   one file per handbook page
    images/                               every image referenced by the content
    style.css                             shared stylesheet
Links between handbook pages are rewritten to the local files; all other links
are kept (made absolute so they still resolve).
"""
import os
import re
import time
from urllib.parse import urljoin, urlparse, unquote

import requests
from bs4 import BeautifulSoup, NavigableString, Comment, Tag

BASE = "https://www.ontario.ca"
BOOK = "/document/official-mto-drivers-handbook"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mto_drivers_handbook")
IMG_DIR = os.path.join(OUT, "images")

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"

BLOCK = {"html", "head", "body", "header", "footer", "nav", "main", "aside", "section", "article",
         "div", "ul", "ol", "li", "table", "thead", "tbody", "tfoot", "tr", "td", "th", "figure",
         "figcaption", "blockquote", "dl", "dt", "dd", "p", "h1", "h2", "h3", "h4", "h5", "h6",
         "details", "summary", "caption", "colgroup", "title", "meta", "link", "hr", "picture"}
VOID = {"meta", "link", "hr", "br", "img", "col", "source", "input"}


def fetch(url):
    for attempt in range(4):
        try:
            r = session.get(url, timeout=60)
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            if attempt == 3:
                raise
            print(f"  retry {url}: {e}")
            time.sleep(2 * (attempt + 1))


def get_soup(url):
    r = fetch(url)
    r.encoding = "utf-8"
    return BeautifulSoup(r.text, "html.parser")


def slug_of(path):
    """'/document/official-mto-drivers-handbook/foo' -> 'foo'; book root -> 'index'."""
    path = path.rstrip("/")
    if path == BOOK:
        return "index"
    if path.startswith(BOOK + "/"):
        return path[len(BOOK) + 1:]
    return None


# ---------------------------------------------------------------- table of contents
def read_toc(soup):
    """Return nested list of (title, slug, children) from the book's TOC tree."""
    def parse(ul):
        items = []
        for li in ul.find_all("li", recursive=False):
            a = li.find("a", recursive=False)
            if not a:
                continue
            slug = slug_of(urlparse(a["href"]).path)
            sub = li.find("ul", recursive=False)
            items.append((a.get_text(strip=True), slug, parse(sub) if sub else []))
        return items
    return parse(soup.find("ul", class_="book__tree_toc-main"))


def flatten(toc):
    for title, slug, kids in toc:
        yield title, slug
        yield from flatten(kids)


def toc_html(toc, current):
    def build(items):
        lis = []
        for title, slug, kids in items:
            cls = ' class="current"' if slug == current else ""
            sub = build(kids) if kids else ""
            lis.append(f'<li><a href="{slug}.html"{cls}>{title}</a>{sub}</li>')
        return "<ul>" + "".join(lis) + "</ul>"
    return build(toc)


# ---------------------------------------------------------------- images
_img_cache = {}


def local_image(src):
    """Download an image once, return its path relative to the page."""
    url = urljoin(BASE, src)
    if url in _img_cache:
        return _img_cache[url]
    name = unquote(os.path.basename(urlparse(url).path)) or "image"
    name = re.sub(r"[^\w.\-]", "_", name)
    stem, ext = os.path.splitext(name)
    candidate, n = name, 1
    while candidate in _img_cache.values() or candidate in {os.path.basename(v) for v in _img_cache.values()}:
        candidate = f"{stem}_{n}{ext}"
        n += 1
    path = os.path.join(IMG_DIR, candidate)
    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(fetch(url).content)
    _img_cache[url] = f"images/{candidate}"
    return _img_cache[url]


IMG_EXT = re.compile(r"\.(png|jpe?g|gif|svg|webp)$", re.I)


# ---------------------------------------------------------------- content cleanup
def clean_content(body, slug):
    for t in body.find_all(["script", "style", "noscript", "iframe"]):
        t.decompose()
    for c in body.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()

    for img in body.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if src:
            img["src"] = local_image(src)
        for attr in ("data-src", "srcset", "data-srcset", "sizes"):
            img.attrs.pop(attr, None)
    for source in body.find_all("source"):
        source.decompose()

    for a in body.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
            continue
        absolute = urljoin(BASE + BOOK + "/" + slug, href)
        parsed = urlparse(absolute)
        target = slug_of(parsed.path) if parsed.netloc == "www.ontario.ca" else None
        if target:
            a["href"] = ("" if target == slug and parsed.fragment else f"{target}.html") + \
                        (f"#{parsed.fragment}" if parsed.fragment else "")
        elif IMG_EXT.search(parsed.path) and parsed.netloc.endswith("ontario.ca"):
            a["href"] = local_image(absolute)  # link to a larger image version
        else:
            a["href"] = absolute

    # strip site-specific presentation attributes we don't style
    for t in body.find_all(True):
        for attr in [a for a in t.attrs if a == "style" or a.startswith("data-")]:
            t.attrs.pop(attr)

    # give headings ids so the "On this page" list can link to them
    used = {t["id"] for t in body.find_all(id=True)}
    headings = []
    for h in body.find_all("h2"):
        if not h.get("id"):
            base = re.sub(r"[^a-z0-9]+", "-", h.get_text().lower()).strip("-") or "section"
            hid, n = base, 2
            while hid in used:
                hid, n = f"{base}-{n}", n + 1
            h["id"] = hid
            used.add(hid)
        headings.append((h["id"], h.get_text(" ", strip=True)))
    return headings


# ---------------------------------------------------------------- pretty printing
def pretty(node, depth=0):
    """Indent block-level structure; keep inline content on one line so spacing is preserved."""
    ind = "  " * depth
    if isinstance(node, NavigableString):
        text = str(node)
        return [ind + text.strip()] if text.strip() else []
    if node.name in VOID:
        return [ind + str(node)]
    has_block = any(isinstance(c, Tag) and c.name in BLOCK for c in node.children)
    if not has_block or node.name in ("pre", "textarea"):
        inner = "".join(str(c) for c in node.children)
        if node.name not in ("pre", "textarea"):
            inner = re.sub(r"\s+", " ", inner).strip()
        return [ind + _open(node) + inner + f"</{node.name}>"]
    lines = [ind + _open(node)]
    for c in node.children:
        lines += pretty(c, depth + 1)
    lines.append(ind + f"</{node.name}>")
    return lines


def _open(tag):
    s = str(tag)
    return s[: s.index(">") + 1]


# ---------------------------------------------------------------- page assembly
PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | The Official MTO Driver's Handbook</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="site-header"><a href="index.html">The Official Ministry of Transportation (MTO) Driver's Handbook</a></header>
<div class="layout">
<nav class="book-toc" aria-label="Table of contents">
<h2>Table of contents</h2>
{toc}
</nav>
<main>
<h1>{title}</h1>
{intro}
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


def pager_html(prev, nxt):
    p = f'<a class="prev" href="{prev[1]}.html">&larr; {prev[0]}</a>' if prev else "<span></span>"
    n = f'<a class="next" href="{nxt[1]}.html">{nxt[0]} &rarr;</a>' if nxt else "<span></span>"
    return f'<nav class="pager">{p}<a href="index.html">Contents</a>{n}</nav>'


def build_page(slug, title, prev, nxt, toc):
    url = BASE + BOOK + ("" if slug == "index" else "/" + slug)
    print(f"[{slug}] {url}")
    soup = get_soup(url)
    h1 = soup.find("main").find("h1")
    title = h1.get_text(" ", strip=True) if h1 else title
    body = soup.select_one("div.book__inner-wrapper div.main-content div.body-field")
    headings = clean_content(body, slug)

    # short intro shown under the title (only some pages, e.g. the cover page, have one)
    intro = ""
    intro_el = soup.select_one("span.book__intro div.intro__text")
    if intro_el and intro_el.get_text(strip=True):
        clean_content(intro_el, slug)
        intro = '<div class="intro">\n' + "\n".join(
            line for c in intro_el.find_all("p") for line in pretty(c, 1)) + "\n</div>"

    onpage = ""
    if len(headings) > 1:
        items = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in headings)
        onpage = f'<nav class="on-this-page"><h2>On this page</h2><ol>{items}</ol></nav>'
    dates_el = soup.find(class_="book__dates--wrapper")
    dates = ""
    if dates_el:
        dates = '<p class="dates">' + " &middot; ".join(s.get_text(strip=True) for s in dates_el.find_all("small")) + "</p>"

    content = "\n".join(line for c in body.children for line in pretty(c))
    html = PAGE.format(title=title, intro=intro, toc=toc_html(toc, slug), pager=pager_html(prev, nxt),
                       onpage=onpage, content=content, dates=dates, source=url)
    # re-indent the shell (head, nav, pager) without touching the already formatted content
    with open(os.path.join(OUT, f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(html)


CSS = """:root { --fg:#1a1a1a; --muted:#5c5c5c; --accent:#0066cc; --border:#d6d6d6; --bg:#fff; --soft:#f3f5f7; }
* { box-sizing: border-box; }
body { margin:0; font:17px/1.6 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; color:var(--fg); background:var(--bg); }
a { color:var(--accent); }
.site-header { background:#1a1a1a; padding:14px 24px; }
.site-header a { color:#fff; text-decoration:none; font-weight:600; }
.layout { display:flex; max-width:1300px; margin:0 auto; }
.book-toc { flex:0 0 300px; padding:24px; border-right:1px solid var(--border); font-size:15px;
            position:sticky; top:0; align-self:flex-start; max-height:100vh; overflow:auto; }
.book-toc h2 { font-size:16px; margin-top:0; }
.book-toc ul { list-style:none; padding-left:0; margin:0; }
.book-toc ul ul { padding-left:16px; }
.book-toc li { margin:4px 0; }
.book-toc a { text-decoration:none; }
.book-toc a.current { font-weight:700; color:var(--fg); }
main { flex:1; min-width:0; padding:24px 40px 60px; max-width:900px; }
h1 { font-size:2.1em; line-height:1.2; }
.intro { font-size:1.15em; color:var(--muted); }
.on-this-page { background:var(--soft); padding:12px 20px; border-radius:6px; margin-bottom:24px; }
.on-this-page h2 { font-size:1em; margin:0 0 6px; }
.on-this-page ol { margin:0; columns:2; }
.pager { display:flex; justify-content:space-between; gap:12px; margin:20px 0; padding:12px 0;
         border-top:1px solid var(--border); border-bottom:1px solid var(--border); font-size:15px; }
.content img { max-width:100%; height:auto; }
.content table { border-collapse:collapse; width:100%; margin:16px 0; }
.content th, .content td { border:1px solid var(--border); padding:8px; vertical-align:top; text-align:left; }
.content th { background:var(--soft); }
.content .hidden, .content .show-for-sr { position:absolute; left:-9999px; }
.dates, .source { color:var(--muted); font-size:14px; }
@media (max-width:900px) {
  .layout { display:block; }
  .book-toc { position:static; max-height:none; border-right:0; border-bottom:1px solid var(--border); }
  main { padding:16px; }
  .on-this-page ol { columns:1; }
}
@media print { .book-toc, .pager, .site-header { display:none; } }
"""


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    with open(os.path.join(OUT, "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)

    toc_soup = get_soup(BASE + BOOK)
    title = toc_soup.find("main").find("h1").get_text(" ", strip=True)
    toc = [(title, "index", [])] + read_toc(toc_soup)
    pages = list(dict.fromkeys(flatten(toc)))  # ordered, de-duplicated

    for i, (t, slug) in enumerate(pages):
        prev = pages[i - 1] if i > 0 else None
        nxt = pages[i + 1] if i + 1 < len(pages) else None
        build_page(slug, t, prev, nxt, toc)

    print(f"\nSaved {len(pages)} pages and {len(_img_cache)} images to {OUT}")


if __name__ == "__main__":
    main()
