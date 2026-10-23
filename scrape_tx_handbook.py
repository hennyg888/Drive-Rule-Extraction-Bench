"""Download the Texas Driver Handbook (DL-7, Texas DPS) and convert the PDF into local,
cleanly formatted HTML in the same format as the MTO copy (scrape_mto_handbook.py).

Output: tx_drivers_handbook/
    source/DL-7.pdf                   the downloaded PDF (the download is skipped if it exists)
    index.html                        cover, front matter and the table of contents
    <chapter-slug>.html ...           one file per chapter / appendix, plus back-cover.html
    images/                           figures and signs rendered from the PDF as PNG
    style.css                         the MTO stylesheet plus a few rules for notes and captions

How the PDF is read
    DL-7.pdf is a tagged InDesign export without bookmarks. MuPDF's structured text
    (TEXT_COLLECT_STRUCTURE) exposes the structure tree, so reading order and the InDesign
    paragraph style of every paragraph come straight from the tags:
        Ch_Head -> h1 (one page per chapter), Ch_Subhead -> h2, Ch_section -> h3,
        Ch_sec_sub -> h4, body/bullet styles -> p / li, Table/TR/TD -> table,
        SN_Head/SN_text -> "Special Note" call-outs, TOCI -> contents entries.
    The style names agree one to one with font size and weight (Frutiger Black 14 / Bold 12 /
    Bold 9 / Bold Italic 8.5); front and back matter carry no styles and use the fonts.
    Figures and signs are untagged vector art with no alt text. They are found geometrically
    (clusters of drawings and images, minus table rules and note backgrounds), rendered to
    PNG and placed in the reading flow by position. Text inside a figure becomes its caption.
    Every img says where its alt came from in data-alt-source: "caption" (the figure's own
    label text, or a sign's description cell), "nearby" (closest heading or label), or "manual"
    (MANUAL_ALT below: sign lettering that exists only as vector outlines). Every content
    block carries data-pdf-page (1-based) and data-page-label (printed page) when they differ.

Usage
    python scrape_tx_handbook.py              download (if needed) and convert
    python scrape_tx_handbook.py --verify     convert, then print text-coverage and image checks
"""
import argparse
import datetime
import html
import os
import re
import sys
from collections import Counter, defaultdict

import pymupdf
import requests
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True  # importing the MTO script must not leave a __pycache__ in the repo
sys.path.insert(0, HERE)
from scrape_mto_handbook import CSS as MTO_CSS, pager_html, pretty, toc_html  # noqa: E402

PDF_URL = "https://www.dps.texas.gov/internetforms/Forms/DL-7.pdf"
BOOK_TITLE = "Texas Driver Handbook"
OUT = os.path.join(HERE, "tx_drivers_handbook")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}

FRONT_PAGES = range(1, 7)     # cover, introduction, letter, table of contents (PDF pages 1-6)
TOC_PAGES = range(4, 7)
COVER_PAGE = 1
ZOOM = 2.0                    # figures are rendered at 144 dpi

HEAD_STYLES = {"Ch_Head": 1, "Ch_Subhead": 2, "Ch_section": 3, "Ch_section_pg22": 3,
               "Ch_sec_sub": 4, "App_Letter": 2}
PARA_STD = {"P", "TOCI"}       # structure roles that hold one paragraph of text
LIST_STYLES = {"body_bullet__", "body_bullet___1st", "body_bullet_l", "App_bullet", "App_C_body"}
HEADER_STYLES_IN_TABLE = {"Table_head", "App_B_Title"}

# A few sign images carry no text at all in the PDF (their lettering is vector outlines) and
# no caption. Their alt text is written by hand from the rendered image and marked as such.
# Key: (PDF page, approximate x0, approximate y0) of the rendered figure.
MANUAL_ALT = {
    (3, 233, 80): "Portrait photo of Colonel Freeman F. Martin, Texas Department of Public Safety",
    (3, 94, 548): "Signature of Freeman F. Martin",
    (29, 54, 634): "Sign: YIELD HERE TO (pedestrian symbol), the “Yield Here to Pedestrians” sign",
    (30, 198, 67): "Sign: STATE LAW – YIELD TO PEDESTRIANS (overhead pedestrian crossing sign)",
    (31, 54, 502): "Sign: LEFT TURN YIELD ON GREEN (with a green ball)",
    (44, 455, 452): "Sign: LEFT LANE FOR PASSING ONLY",
    # core passing diagrams (no caption in the PDF)
    (39, 205, 227): "Diagram: two-lane road with a broken yellow center line, one car in each direction",
    (39, 235, 605): "Diagram: four-lane highway with a double solid yellow center line and broken white lane lines",
    (40, 206, 90): "Diagram: two-way roads with solid and broken yellow center lines; a car crosses the broken line",
    (42, 54, 287): "Barricade rail and vertical panel with orange and white stripes sloping downward to the right",
    (42, 54, 346): "Barricade rail and vertical panel with orange and white stripes sloping downward to the left",
    (45, 198, 218): "Diagram: a car passes another car on a two-lane road, moving into the left lane and back to the right lane",
    (67, 504, 121): "Sign: PUSH BUTTON FOR GREEN (pedestrian push-button sign)",
    # Table 21 (Construction and Maintenance Signs) has signs only, no descriptions
    (41, 147, 520): "Sign: SHOULDER WORK (orange diamond)",
    (41, 234, 520): "Sign: ROAD CLOSED 1000 FT (orange diamond)",
    (41, 322, 520): "Sign: DETOUR 1000 FT (orange diamond)",
    (41, 409, 536): "Sign: END CONSTRUCTION (orange rectangle)",
    (41, 147, 592): "Sign: ONE LANE ROAD 1000 FT (orange diamond)",
    (41, 234, 592): "Sign: NARROW LANES AHEAD (orange diamond)",
    (41, 322, 592): "Sign: ROAD WORK 1 MILE (orange diamond)",
    (41, 409, 608): "Sign: SLOW TRAFFIC AHEAD (orange rectangle)",
    (41, 155, 664): "Sign: flagger symbol with a 500 FEET plaque (orange diamond)",
    (41, 234, 664): "Sign: ROAD CONSTRUCTION AHEAD (orange diamond)",
    (41, 322, 664): "Sign: FRESH OIL (orange diamond)",
    (41, 407, 665): "Sign: DETOUR with a DETOUR arrow plaque (orange)",
    (91, 413, 183): "Photos of DPS patrol cars, a helicopter, a patrol boat and an aircraft",
    (91, 36, 516): "Photo of Driver License Division staff",
    (91, 339, 562): "Photo of a driver license office building",
}

session = requests.Session()
session.headers.update(UA)


def manual_alt(pno, bbox):
    return next((v for (pp, x, y), v in MANUAL_ALT.items()
                 if pp == pno and abs(x - bbox[0]) <= 12 and abs(y - bbox[1]) <= 12), None)


# ---------------------------------------------------------------- download
def download(pdf_path):
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
        print(f"PDF already present: {pdf_path}")
        return
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    print(f"Downloading {PDF_URL}")
    tmp = pdf_path + ".part"
    with session.get(PDF_URL, timeout=300, stream=True) as r:
        r.raise_for_status()
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    with open(tmp, "rb") as f:
        if f.read(5) != b"%PDF-":
            raise RuntimeError("downloaded file is not a PDF")
    os.replace(tmp, pdf_path)


# ---------------------------------------------------------------- small helpers
def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"


def valid_bbox(b):
    return b is not None and b[0] < 1e8 and b[2] > b[0] - 1e-6


def y_overlap(a, b):
    return min(a[3], b[3]) - max(a[1], b[1])


def rect_gap(a, b):
    """Euclidean gap between two rectangles (0 if they touch or overlap)."""
    dx = max(b[0] - a[2], a[0] - b[2], 0)
    dy = max(b[1] - a[3], a[1] - b[3], 0)
    return (dx * dx + dy * dy) ** 0.5


def union(boxes):
    boxes = [b for b in boxes if b is not None]
    if not boxes:
        return None
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


def span_is_bold(s):
    f = s["font"]
    return "Bold" in f or "Black" in f or "SemiBold" in f or "Semibold" in f


def span_is_italic(s):
    f = s["font"]
    return "Italic" in f or "Itali" in f or "Oblique" in f


def is_artifact_line(line):
    """Running header (top of page) and page number (bottom of page)."""
    s = line["spans"][0]
    txt = "".join(sp["text"] for sp in line["spans"]).strip()
    x0, y0, x1, y1 = line["bbox"]
    if y1 < 40 and s["font"].startswith("FrutigerLTStd-Roman"):
        return True
    if y0 > 740 and s["font"].startswith("FrutigerLTStd-Roman") and abs(s["size"] - 10) < 0.3 \
            and re.fullmatch(r"[0-9ivxlcIVXLC]+", txt):
        return True
    return False


# ---------------------------------------------------------------- text runs
def clean_text(t):
    return t.replace("\x07", " ").replace("\x08", " ").replace("\t", " ")


def join_lines(lines, breaks=False):
    """Join the lines of one paragraph into formatted runs [text, bold, italic].

    Lines on the same baseline are joined with or without a space depending on the gap
    (MuPDF splits a visual line at every span/tag change); a real line wrap becomes a space,
    except after a soft hyphen (removed) or after a hard hyphen inside a compound word."""
    runs = []
    prev = None
    for ln in lines:
        spans = [s for s in ln["spans"] if s["text"]]
        if not spans:
            continue
        if prev is not None and runs:
            pb, cb = prev["bbox"], ln["bbox"]
            h = min(pb[3] - pb[1], cb[3] - cb[1])
            same_row = y_overlap(pb, cb) > 0.5 * h and cb[0] >= pb[2] - 2
            last = runs[-1][0]
            first = spans[0]["text"]
            if same_row:
                if cb[0] - pb[2] > 1.2 and not last.endswith((" ", "\t", "\xad")) and not first.startswith((" ", "\t")):
                    runs[-1][0] = last + " "
            elif breaks:
                runs[-1][0] = last.rstrip() + "\n"
            else:
                stripped = last.rstrip(" \t\n")
                if stripped.endswith("\xad"):
                    runs[-1][0] = stripped[:-1]
                elif re.search(r"[A-Za-z]-$", stripped) and re.match(r"\s*[A-Za-z]", first) \
                        and not re.match(r"\s*(or|and|to)\b", first):
                    runs[-1][0] = stripped          # compound word broken after its hyphen
                else:
                    runs[-1][0] = stripped + " "
        for s in spans:
            runs.append([s["text"], span_is_bold(s), span_is_italic(s)])
        prev = ln
    return normalize_runs(runs, breaks)


def normalize_runs(runs, breaks=False):
    out = []
    for t, b, i in runs:
        t = clean_text(t).replace("\xad", "")
        t = re.sub(r"[  ]+", " ", t) if breaks else re.sub(r"\s+", " ", t.replace(" ", " "))
        if out and out[-1][1] == b and out[-1][2] == i:
            out[-1][0] += t
        else:
            out.append([t, b, i])
    # collapse whitespace across run boundaries
    for k in range(1, len(out)):
        if out[k - 1][0].endswith((" ", "\n")) and out[k][0].startswith(" "):
            out[k][0] = out[k][0].lstrip(" ")
    out = [r for r in out if r[0]]
    if out:
        out[0][0] = out[0][0].lstrip()
        out[-1][0] = out[-1][0].rstrip()
    if breaks:
        for r in out:
            r[0] = re.sub(r" *\n *", "\n", r[0])
    # whitespace-only runs never carry formatting
    for r in out:
        if not r[0].strip():
            r[1] = r[2] = False
    return [r for r in out if r[0]]


def runs_text(runs):
    return "".join(r[0] for r in runs)


def strip_prefix(runs, n):
    """Remove the first n characters (a list marker) from the runs."""
    out = []
    for t, b, i in runs:
        if n >= len(t):
            n -= len(t)
            continue
        out.append([t[n:], b, i])
        n = 0
    if out:
        out[0][0] = out[0][0].lstrip()
    return [r for r in out if r[0]]


URL_RE = re.compile(r"(?:https?://|www\.)[^\s<>\"“”]+")


def linkify(escaped):
    def sub(m):
        url = m.group(0)
        tail = ""
        while url and url[-1] in ".,;:)]":
            tail = url[-1] + tail
            url = url[:-1]
        href = url if url.startswith("http") else "http://" + url
        return f'<a href="{href}">{url}</a>{tail}'
    return URL_RE.sub(sub, escaped)


def runs_html(runs, plain=False):
    """Formatted runs -> inline HTML. Bold/italic only where it differs from the paragraph."""
    if not runs:
        return ""
    all_bold = all(r[1] for r in runs if r[0].strip())
    all_italic = all(r[2] for r in runs if r[0].strip())
    parts = []
    for t, b, i in runs:
        lead = t[: len(t) - len(t.lstrip(" "))]
        trail = t[len(t.rstrip(" ")):]
        core = t.strip(" ")
        h = linkify(html.escape(core, quote=False)).replace("\n", "<br/>")
        if not plain and core:
            if i and not all_italic:
                h = f"<em>{h}</em>"
            if b and not all_bold:
                h = f"<strong>{h}</strong>"
        parts.append(lead + h + trail)
    return "".join(parts).strip()


# ---------------------------------------------------------------- structure-tree walk
class Para:
    """One leaf paragraph of the structure tree, on one page."""

    def __init__(self, page, path, style, lines):
        self.page, self.path, self.style = page, path, style
        self.lines = lines
        self.bbox = union([tuple(l["bbox"]) for l in lines])
        self.ctx = None

    @property
    def key(self):
        return tuple((r, i) for r, s, i in self.path)


class Cell:
    def __init__(self, header, paras, bbox):
        self.header, self.paras, self.bbox = header, paras, bbox
        self.image = None      # (src, w, h, alt, alt_source) once art is assigned
        self.colspan = 1

    @property
    def lines(self):
        return [l for p in self.paras for l in p.lines]

    @property
    def text(self):
        return runs_text(join_lines(self.lines)).strip()


class Table:
    def __init__(self, page, path, rows):
        self.page, self.path, self.rows = page, path, rows   # rows: list of list[Cell]
        self.caption = None
        self.row_pages = [page] * len(rows)

    @property
    def key(self):
        # InDesign sometimes splits one table into sibling Table elements (e.g. the last row of
        # Table 18 on PDF page 35), so a table is identified by its enclosing element.
        return tuple((r, i) for r, s, i in self.path[:-1])

    @property
    def bbox(self):
        return union([c.bbox for row in self.rows for c in row if c.bbox and c.lines])


def collect_lines(block):
    out = []

    def rec(bs):
        for x in bs:
            if x["type"] == 2:
                rec(x.get("blocks", []))
            elif x["type"] == 0:
                out.extend(x["lines"])
    rec(block.get("blocks", []))
    return out


def has_inner(blocks):
    for x in blocks:
        if x["type"] == 2 and (x["std"] in PARA_STD or x["raw"] == "Table" or has_inner(x.get("blocks", []))):
            return True
    return False


def clean_lines(lines):
    """Drop running headers/page numbers and duplicated lines (shadowed note headings)."""
    out, seen = [], set()
    for l in lines:
        if is_artifact_line(l):
            continue
        txt = "".join(s["text"] for s in l["spans"])
        if not txt:
            continue
        k = (txt, round(l["bbox"][0]), round(l["bbox"][1]))
        if k in seen:
            continue
        seen.add(k)
        out.append(l)
    return out


def parse_table(tb, path, page):
    rows = []

    def find_rows(bs):
        for x in bs:
            if x["type"] != 2:
                continue
            if x["raw"] == "TR":
                cells = {}
                for c in x.get("blocks", []):
                    if c["type"] == 2 and c["raw"] in ("TD", "TH"):
                        paras = []
                        style = None
                        for p in leaf_paras(c, path, page):
                            style = style or p.style
                            p.lines = clean_lines(p.lines)
                            paras.append(p)
                        header = c["raw"] == "TH" or (style in HEADER_STYLES_IN_TABLE)
                        cell = Cell(header, [p for p in paras if p.lines], tuple(c["bbox"]) if valid_bbox(c["bbox"]) else None)
                        cell.style = style
                        cells[c["index"]] = cell
                # MuPDF leaves out cells with no content at all (the sign/colour column);
                # their TD index shows where they were
                n = max(cells) + 1 if cells else 0
                row = []
                for k in range(n):
                    if k not in cells:
                        cells[k] = Cell(False, [], None)
                        cells[k].style = None
                    row.append(cells[k])
                rows.append(row)
            else:
                find_rows(x.get("blocks", []))
    find_rows(tb.get("blocks", []))
    return Table(page, path, rows)


def leaf_paras(block, path, page):
    """Leaf paragraphs below a struct element (used inside table cells)."""
    out = []

    def rec(b, p):
        for x in b.get("blocks", []):
            if x["type"] == 2:
                np_ = p + [(x["raw"], x["std"], x["index"])]
                if x["std"] in PARA_STD and not has_inner(x.get("blocks", [])):
                    out.append(Para(page, np_, x["raw"], collect_lines(x)))
                else:
                    rec(x, np_)
            elif x["type"] == 0:
                out.append(Para(page, p, None, x["lines"]))
    rec(block, path)
    return out


def walk_page(dd, page):
    """Return ('para', Para) and ('table', Table) items in structure order."""
    items = []

    def rec(blocks, path):
        for b in blocks:
            if b["type"] == 2:
                np_ = path + [(b["raw"], b["std"], b["index"])]
                if b["raw"] == "Table":
                    items.append(("table", parse_table(b, np_, page)))
                elif b["std"] in PARA_STD and not has_inner(b.get("blocks", [])):
                    lines = clean_lines(collect_lines(b))
                    if lines:
                        items.append(("para", Para(page, np_, b["raw"], lines)))
                else:
                    rec(b.get("blocks", []), np_)
            elif b["type"] == 0:
                lines = clean_lines(b["lines"])
                if lines:
                    items.append(("para", Para(page, path, None, lines)))
    rec(dd["blocks"], [])
    return items


def classify(p, page_kind):
    raws = [r for r, s, i in p.path]
    if p.style in ("SN_Head", "SN_text"):
        return "note"
    if p.style == "TOCI" or "TOCI" in raws:
        return "toc"
    if "Figure" in raws or "body_table" in raws[:-1] or p.style == "body_table":
        return "label"
    if page_kind == "chapter" and p.style in ("_No_paragraph_style_", None):
        return "label"
    return "flow"


# ---------------------------------------------------------------- blocks
class Block:
    """A content block in reading order: h, p, li, table, figure, note, caption."""

    def __init__(self, kind, page, bbox, **kw):
        self.kind, self.page, self.bbox = kind, page, bbox
        self.page_end = page
        self.runs = []
        self.level = 0
        self.list_type = None
        self.number = None
        self.style = None
        self.key = None
        self.cont = False
        self.is_float = False
        self.table = None
        self.image = None
        self.caption_runs = None
        self.cls = None
        self.lines = []
        self.__dict__.update(kw)

    @property
    def top(self):
        return self.bbox[1] if self.bbox else 0

    @property
    def text(self):
        return runs_text(self.runs)


MARKER_RE = re.compile(
    r"^\s*(?:(?P<bul>[•●▪■])\s*|(?P<num>\d{1,2})\.[\s\x07]+|(?P<alpha>[a-z])\.[\s\x07]+|(?P<dash>[-–])[\s\x07]+)")


def list_marker(raw_text, style):
    if style in HEAD_STYLES or style == "Table_Title":
        return None
    m = MARKER_RE.match(raw_text)
    if not m:
        return None
    if (m.group("alpha") or m.group("dash")) and style not in LIST_STYLES and "\x07" not in m.group(0):
        return None
    if m.group("bul"):
        kind = ("ul", None, None)
    elif m.group("dash"):
        kind = ("ul", None, None)
    elif m.group("num"):
        kind = ("ol", "1", int(m.group("num")))
    else:
        kind = ("ol", "a", ord(m.group("alpha")) - 96)
    return m, kind


def front_heading_level(p):
    spans = [s for l in p.lines for s in l["spans"] if s["text"].strip()]
    if not spans or not all(span_is_bold(s) for s in spans):
        return 0
    size = max(s["size"] for s in spans)
    font = spans[0]["font"]
    if font.startswith("FrutigerLTStd-Bold") and size >= 13.5:
        return 2
    if font.startswith("MartelSans-Bold") and 19.5 <= size <= 21:
        return 2
    if font.startswith("MartelSans-Bold") and 9.5 <= size <= 11.5:
        return 3
    return 0


def para_to_block(p, page_kind):
    raw = "".join(s["text"] for l in p.lines for s in l["spans"])
    lines = p.lines
    style = p.style
    b = Block("p", p.page, p.bbox, style=style, key=p.key, lines=lines)
    if style in HEAD_STYLES:
        b.kind, b.level = "h", HEAD_STYLES[style]
        b.runs = join_lines(lines)
        if style == "App_Letter":
            b.runs = [[runs_text(b.runs).strip(" -"), False, False]]
        return b
    if page_kind != "chapter":
        lvl = front_heading_level(p)
        if lvl and not MARKER_RE.match(raw):
            b.kind, b.level = "h", lvl
            b.runs = join_lines(lines)
            return b
    if style == "Table_Title":
        b.kind = "table_title"
        b.runs = join_lines(lines)
        return b
    if style == "Address":
        b.runs = join_lines(lines, breaks=True)
        return b
    runs = join_lines(lines)
    mk = list_marker(raw, style)
    if mk:
        m, (lt, ls, num) = mk
        # the marker regex ran on raw text; strip the same marker from the cleaned runs
        m2 = MARKER_RE.match(runs_text(runs))
        runs = strip_prefix(runs, m2.end()) if m2 else runs
        x0 = lines[0]["bbox"][0]
        b.kind = "li"
        b.list_type, b.list_style, b.number = lt, ls, num
        b.level = 1 if x0 < 66 else (2 if x0 < 78 else 3)
        if style == "body_bullet_l" and b.level == 1:
            b.level = 2
        b.runs = runs
        return b
    b.runs = runs
    words = runs_text(runs).split()
    if runs and all(r[1] for r in runs if r[0].strip()) and 0 < len(words) <= 6 \
            and not runs_text(runs).rstrip().endswith(".") and style in ("body", "body_1st_par"):
        b.kind, b.level = "h", 4          # bold one-line lead-in such as "Do's" / "Don'ts"
    return b


# ---------------------------------------------------------------- figures (geometry)
def page_art_rects(page, text_boxes, note_boxes):
    """Candidate figure parts: vector drawings and images that are not backgrounds of text."""
    W, H = page.rect.width, page.rect.height
    parts = []
    for d in page.get_drawings():
        r = d["rect"]
        if r.width > 0.85 * W and r.height > 0.85 * H:
            continue                                    # page background
        vis = r & page.rect
        if r.x0 < -1 or r.y0 < -1 or r.x1 > W + 1 or r.y1 > H + 1:
            if vis.is_empty or vis.width * vis.height < 0.5 * r.width * r.height:
                continue                                # artwork left on the pasteboard
        if r.y1 < 42 and r.height < 2:
            continue                                    # rule under the running header
        if d.get("fill") == (1.0, 1.0, 1.0) and not d.get("color") and r.width * r.height > 2000:
            continue                                    # white frame backgrounds
        parts.append((r.x0, r.y0, r.x1, r.y1, "d"))
    for im in page.get_image_info():
        r = pymupdf.Rect(im["bbox"]) & page.rect
        if r.is_empty:
            continue
        parts.append((r.x0, r.y0, r.x1, r.y1, "i"))
    keep = []
    for (x0, y0, x1, y1, t) in parts:
        r = (x0, y0, x1, y1)
        area = max((x1 - x0), 0.5) * max((y1 - y0), 0.5)
        bad = False
        for tb in text_boxes:            # drawn under/over body text -> background or underline
            ix = min(x1, tb[2] - 1) - max(x0, tb[0] + 1)
            iy = min(y1, tb[3] - 1) - max(y0, tb[1] + 1)
            if ix > 0 and iy > 0:
                bad = True
                break
        if not bad:
            for nb in note_boxes:        # sticky-note artwork behind "Special Note" text
                ix = min(x1, nb[2] + 12) - max(x0, nb[0] - 12)
                iy = min(y1, nb[3] + 12) - max(y0, nb[1] - 12)
                if ix > 0 and iy > 0 and ix * iy > 0.3 * area:
                    bad = True
                    break
        if not bad:
            keep.append(r)
    return keep


def cluster(rects, gap):
    """Union-find clustering of rectangles closer than gap."""
    n = len(rects)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    order = sorted(range(n), key=lambda i: rects[i][0])
    for a_i, i in enumerate(order):
        ri = rects[i]
        for j in order[a_i + 1:]:
            rj = rects[j]
            if rj[0] > ri[2] + gap:
                break
            if rect_gap(ri, rj) <= gap:
                pi, pj = find(i), find(j)
                if pi != pj:
                    parent[pi] = pj
    groups = defaultdict(list)
    for i in range(n):
        groups[find(i)].append(rects[i])
    return [union(g) for g in groups.values()]


def merge_overlapping(boxes, pad=2):
    boxes = list(boxes)
    changed = True
    while changed:
        changed = False
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                if rect_gap(boxes[i]["bbox"], boxes[j]["bbox"]) <= pad:
                    boxes[i]["bbox"] = union([boxes[i]["bbox"], boxes[j]["bbox"]])
                    boxes[i]["labels"] += boxes[j]["labels"]
                    del boxes[j]
                    changed = True
                    break
            if changed:
                break
    return boxes


class Renderer:
    def __init__(self, doc, img_dir):
        self.doc, self.img_dir = doc, img_dir
        self.count = Counter()
        self.files = []

    def render(self, pno, bbox, pad=3, name=None):
        page = self.doc[pno - 1]
        r = pymupdf.Rect(bbox[0] - pad, bbox[1] - pad, bbox[2] + pad, bbox[3] + pad) & page.rect
        self.count[pno] += 1
        name = name or f"p{pno:03d}-{self.count[pno]:02d}.png"
        pix = page.get_pixmap(matrix=pymupdf.Matrix(ZOOM, ZOOM), clip=r, alpha=False)
        pix.save(os.path.join(self.img_dir, name))
        self.files.append(name)
        return f"images/{name}", round(r.width * 4 / 3), round(r.height * 4 / 3)


def label_units_text(labels):
    """Text of the labels inside a figure, in reading order.

    Every line is a unit; wrapped lines of one label (left- or centre-aligned, directly
    below each other) are joined, then units are ordered by rows, top to bottom and left
    to right, and joined with " · "."""
    units = []
    for p in labels:
        for l in p.lines:
            raw = "".join(s["text"] for s in l["spans"]).replace("\x07", " ").replace("\x08", " ")
            pieces = [re.sub(r"\s+", " ", x).strip() for x in raw.split("\t")]
            text = " · ".join(x for x in pieces if x)
            if text:
                size = max(s["size"] for s in l["spans"])
                units.append([tuple(l["bbox"]), text, size])
    units.sort(key=lambda u: (u[0][1], u[0][0]))
    # fragments of one visual line (MuPDF splits lines at span/tag changes)
    merged = []
    for u in units:
        m = next((v for v in merged if y_overlap(v[0], u[0]) > 0.6 * (u[0][3] - u[0][1])
                  and -1 <= u[0][0] - v[0][2] <= 6), None)
        if m:
            m[1] = m[1] + ("" if m[1].endswith("\xad") else " ") + u[1]
            m[0] = union([m[0], u[0]])
        else:
            merged.append(u)
    # wrapped lines of one label
    out = []
    for u in merged:
        h = u[0][3] - u[0][1]
        m = None
        for v in out:
            gap = u[0][1] - v[0][3]
            aligned = abs(v[0][0] - u[0][0]) < 4 or abs((v[0][0] + v[0][2]) - (u[0][0] + u[0][2])) < 16
            if aligned and -2 <= gap <= 0.6 * h and abs(v[2] - u[2]) < 0.6:
                m = v
        if m:
            sep = "" if m[1].endswith("\xad") else " "
            m[1] = m[1].rstrip("\xad") + sep + u[1]
            m[0] = union([m[0], u[0]])
        else:
            out.append(u)
    rows = []
    for bb, t, _ in sorted(out, key=lambda u: (u[0][1], u[0][0])):
        if rows and y_overlap(rows[-1][0], bb) > 0.4 * (bb[3] - bb[1]):
            rows[-1][0] = union([rows[-1][0], bb])
            rows[-1][1].append((bb, t))
        else:
            rows.append([bb, [(bb, t)]])
    texts = []
    for _, row in rows:
        for bb, t in sorted(row, key=lambda u: u[0][0]):
            t = t.replace("\xad", "")
            if t not in texts:
                texts.append(t)
    return " · ".join(texts)


def short_alt(text, limit=220):
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    for sep in (" · ", ". ", "; ", ", ", " "):
        k = cut.rfind(sep)
        if k > limit * 0.5:
            return cut[:k].rstrip(" ·;,") + " …"
    return cut + " …"


# ---------------------------------------------------------------- per-page conversion
class Converter:
    def __init__(self, pdf_path, out_dir):
        self.doc = pymupdf.open(pdf_path)
        self.out = out_dir
        self.img_dir = os.path.join(out_dir, "images")
        os.makedirs(self.img_dir, exist_ok=True)
        for f in os.listdir(self.img_dir):
            if f.endswith(".png"):
                os.remove(os.path.join(self.img_dir, f))
        self.renderer = Renderer(self.doc, self.img_dir)
        self.toc_entries = []
        self.cover = None
        self.figure_log = []
        self.page_label = {i + 1: self.doc[i].get_label() or str(i + 1) for i in range(self.doc.page_count)}
        flags = (pymupdf.TEXTFLAGS_DICT & ~pymupdf.TEXT_PRESERVE_IMAGES) | pymupdf.TEXT_COLLECT_STRUCTURE
        self.flags = flags

    def page_kind(self, pno):
        if pno in FRONT_PAGES:
            return "front"
        if pno == self.doc.page_count:
            return "back"
        return "chapter"

    def convert_page(self, pno):
        page = self.doc[pno - 1]
        kind = self.page_kind(pno)
        dd = page.get_textpage(flags=self.flags).extractDICT()
        items = walk_page(dd, pno)
        paras = [x for t, x in items if t == "para"]
        tables = [x for t, x in items if t == "table"]
        for p in paras:
            p.ctx = classify(p, kind)

        if pno in TOC_PAGES:
            self.toc_entries += [p for p in paras if p.ctx == "toc"]
            return []

        flow = [p for p in paras if p.ctx == "flow"]
        notes = [p for p in paras if p.ctx == "note"]
        labels = [p for p in paras if p.ctx == "label"]

        # geometry of text that must not be swallowed by figures
        text_boxes = [tuple(l["bbox"]) for p in flow for l in p.lines]
        table_text = [tuple(l["bbox"]) for t in tables for row in t.rows for c in row for l in c.lines]
        note_boxes = []
        for key, grp in self.group_notes(notes):
            note_boxes.append(union([p.bbox for p in grp]))

        blocks_flow = [para_to_block(p, kind) for p in flow]
        floats = []

        if pno == COVER_PAGE:
            src, w, h = self.renderer.render(pno, tuple(page.rect), pad=0, name="p001-cover.png")
            alt = "Cover of the Texas Driver Handbook (DL-7): " + " · ".join(
                runs_text(join_lines(p.lines)) for p in flow)
            img = Block("figure", pno, (0, 0, 0, 0), image=(src, w, h, short_alt(alt), "caption"))
            self.cover = [b.text for b in blocks_flow]
            return [img] + blocks_flow

        # ---- art: drawings/images that are not table rules, note art or text backgrounds
        tables = self.merge_page_tables(tables)
        art = page_art_rects(page, text_boxes + table_text, note_boxes)
        free_art = self.place_table_art(pno, page, tables, art, text_boxes)
        figs, orphan = self.find_figures(free_art, labels)

        for f in sorted(figs, key=lambda f: (f["bbox"][1], f["bbox"][0])):
            src, w, h = self.renderer.render(pno, f["bbox"])
            cap = label_units_text(f["labels"])
            manual = manual_alt(pno, f["bbox"])
            if manual:
                alt, alt_src = manual, "manual"
            elif cap:
                alt, alt_src = short_alt(cap), "caption"
            else:
                alt, alt_src = None, "nearby"   # filled in later from the nearest heading
            b = Block("figure", pno, f["bbox"], image=[src, w, h, alt, alt_src], is_float=True)
            if cap:
                b.caption_runs = [[cap, False, False]]
            floats.append(b)
            self.figure_log.append((pno, tuple(round(v) for v in f["bbox"]), src, alt_src, cap[:60]))

        for lp in orphan:                       # labels with no artwork nearby: keep as text
            b = para_to_block(lp, kind)
            b.kind = "p" if b.kind not in ("li",) else b.kind
            b.is_float = True
            floats.append(b)

        for t in tables:
            if not t.rows:
                continue
            b = Block("table", pno, t.bbox or (0, 0, 0, 0), table=t, key=t.key, is_float=True)
            floats.append(b)

        for key, grp in self.group_notes(notes):
            head = [p for p in grp if p.style == "SN_Head"]
            body = [p for p in grp if p.style == "SN_text"]
            htxt = runs_text(join_lines(head[0].lines)).strip() if head else "Special Note:"
            runs = [[htxt, True, False], [" ", False, False]] + join_lines([l for p in body for l in p.lines])
            b = Block("p", pno, union([p.bbox for p in grp]), runs=normalize_runs(runs), cls="note", is_float=True)
            floats.append(b)

        return self.place_floats(blocks_flow, floats)

    @staticmethod
    def merge_page_tables(tables):
        out = []
        for t in tables:
            if out and out[-1].key == t.key:
                out[-1].rows += t.rows
                out[-1].row_pages += t.row_pages
            else:
                out.append(t)
        return out

    def place_table_art(self, pno, page, tables, art, text_boxes):
        """Assign art inside tables to their empty cells; return the art outside tables."""
        rules = [d["rect"] for d in page.get_drawings() if d["rect"].y1 >= 42]
        regions = []
        for t in tables:
            tb = t.bbox
            if tb is None:
                continue
            frame = [tuple(r) for r in rules
                     if y_overlap(tuple(r), tb) > 0 and min(r.x1, tb[2]) - max(r.x0, tb[0]) > 0]
            reg = union([tb] + frame)
            has_empty = any(not c.lines and not c.header for row in t.rows for c in row)
            if has_empty:
                # rows with no text at all (Table 21) can lie below the last text: extend the
                # region down to the next body text under the table
                below = [b[1] for b in text_boxes if b[1] > tb[3] and min(b[2], reg[2]) - max(b[0], reg[0]) > 0]
                reg = (reg[0], reg[1], reg[2], max(reg[3], (min(below) - 2) if below else 750))
            regions.append((t, reg, has_empty))
        line_like = lambda r: (r[2] - r[0] < 1.6 or r[3] - r[1] < 1.6)
        free, inside = [], defaultdict(list)
        for r in art:
            cx, cy = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2
            hit = next((t for t, reg, e in regions
                        if reg[0] - 4 <= cx <= reg[2] + 4 and reg[1] - 4 <= cy <= reg[3] + 4), None)
            if hit is None:
                free.append(r)
            elif not line_like(r):
                inside[id(hit)].append(r)
        for t, reg, has_empty in regions:
            clusters = cluster(inside[id(t)], 3.0)
            if has_empty:
                clusters = self.assign_table_art(pno, t, clusters)
            free += clusters
        return free

    @staticmethod
    def find_figures(free_art, labels):
        """Cluster free art into figures and attach the label text that belongs to them."""
        figs = [{"bbox": b, "labels": []} for b in cluster(free_art, 16.0)]
        figs = [f for f in figs if (f["bbox"][2] - f["bbox"][0]) > 3 and (f["bbox"][3] - f["bbox"][1]) > 3]
        # labels travel as groups: all text of one tagged label story / figure element
        groups = defaultdict(list)
        for lp in labels:
            path = [(r, i) for r, st, i in lp.path]
            cut = max((k for k, (r, i) in enumerate(path) if r in ("Story", "Figure")), default=len(path) - 1)
            groups[tuple(path[:cut + 1])].append(lp)
        orphan = []
        for grp in groups.values():
            gb = union([lp.bbox for lp in grp])
            best, bd = None, 1e9
            for f in figs:
                g = rect_gap(gb, f["bbox"])
                horiz = min(gb[2], f["bbox"][2]) - max(gb[0], f["bbox"][0]) > 0
                if g < bd and (g <= 14 or (horiz and g <= 40)):
                    best, bd = f, g
            if best is None:
                orphan += grp
            else:
                best["labels"] += grp
        for f in figs:
            f["bbox"] = union([f["bbox"]] + [lp.bbox for lp in f["labels"]])
        figs = merge_overlapping(figs, pad=8)
        keep = []
        for f in figs:
            w, h = f["bbox"][2] - f["bbox"][0], f["bbox"][3] - f["bbox"][1]
            if f["labels"] or (w * h > 60 and min(w, h) >= 6):
                keep.append(f)
        return keep, orphan

    @staticmethod
    def group_notes(notes):
        groups = defaultdict(list)
        for p in notes:
            key = tuple(x for x in p.path if x[0] == "Story")[:1] + (round(p.bbox[0] / 40),)
            groups[key].append(p)
        return list(groups.items())

    def assign_table_art(self, pno, t, clusters):
        """Put sign/colour/shape graphics into the empty cells of a table; return leftovers.

        A graphic belongs to the empty cell whose description (the next text cell in the
        row) is right of it and closest in height; a sign made of several pieces (e.g. a
        route marker with an arrow plaque) gets all of them. Rows without any text
        (Table 21) are filled row by row, left to right, from the remaining graphics."""
        empties = []
        for ri, row in enumerate(t.rows):
            for ci, c in enumerate(row):
                if not c.lines and not c.header:
                    right = [x for x in row[ci + 1:] if x.lines]
                    anchor = union([l["bbox"] for l in right[0].lines]) if right else None
                    empties.append((ri, ci, anchor))
        if not empties:
            return clusters
        assigned = defaultdict(list)
        left = []
        for cl in clusters:
            best, bs = None, 1e9
            for ri, ci, anchor in empties:
                if anchor is None or cl[2] > anchor[0] + 2 or anchor[0] - cl[2] > 90:
                    continue
                d = abs((cl[1] + cl[3]) / 2 - (anchor[1] + anchor[3]) / 2)
                if d < bs and d < 45:
                    best, bs = (ri, ci), d
            if best:
                assigned[best].append(cl)
            else:
                left.append(cl)
        unfilled = [(ri, ci) for ri, ci, a in empties if (ri, ci) not in assigned and a is None]
        if unfilled and left:
            # a sign and the plaque stacked under it form one graphic
            stacked = True
            while stacked:
                stacked = False
                for a in left:
                    for b in left:
                        if a is b:
                            continue
                        xo = min(a[2], b[2]) - max(a[0], b[0])
                        if xo > 0.5 * min(a[2] - a[0], b[2] - b[0]) and 0 <= b[1] - a[3] <= 12:
                            left.remove(a)
                            left.remove(b)
                            left.append(union([a, b]))
                            stacked = True
                            break
                    if stacked:
                        break
            left.sort(key=lambda b: (b[1], b[0]))
            rows = []
            for b in left:
                if rows and y_overlap(rows[-1][0], b) > 0.3 * (b[3] - b[1]):
                    rows[-1][0] = union([rows[-1][0], b])
                    rows[-1][1].append(b)
                else:
                    rows.append([b, [b]])
            seq = [b for _, r in rows for b in sorted(r, key=lambda b: b[0])]
            for (ri, ci), b in zip(unfilled, seq):
                assigned[(ri, ci)].append(b)
                left.remove(b)
        for (ri, ci) in sorted(assigned):
            self.fill_cell(pno, t, ri, ci, union(assigned[(ri, ci)]))
        return left

    def fill_cell(self, pno, t, ri, ci, bbox):
        src, w, h = self.renderer.render(pno, bbox, pad=2)
        row = t.rows[ri]
        desc = " ".join(c.text for c in row[ci + 1:] if c.lines) or ""
        head = None
        for r in t.rows:
            if r and all(c.header for c in r if c.lines) and any(c.lines for c in r):
                if ci < len(r) and r[ci].lines:
                    head = r[ci].text
                break
        manual = manual_alt(pno, bbox)
        if manual:
            row[ci].image = (src, w, h, manual, "manual")
        elif desc:
            alt = short_alt(f"{head or 'Sign'}: {desc}")
            row[ci].image = (src, w, h, alt, "caption")
        else:
            row[ci].image = (src, w, h, None, "nearby")
        self.figure_log.append((pno, tuple(round(v) for v in bbox), src, "table-cell", desc[:60]))

    @staticmethod
    def place_floats(flow, floats):
        """Insert figures, tables and notes into the reading flow by position.

        A float beside text (vertical overlap with flow blocks) goes after the first block it
        sits beside; a float between blocks goes after the last block that starts above it.
        Floats beside a list are moved after the list so it is not broken up."""
        seq = list(flow)
        for f in sorted(floats, key=lambda b: b.top):
            fb = f.bbox
            beside = [i for i, b in enumerate(seq) if not b.is_float and b.bbox and y_overlap(b.bbox, fb) > 2
                      and (min(b.bbox[2], fb[2]) - max(b.bbox[0], fb[0]) < 2)]
            if beside and f.kind != "table":
                idx = beside[0] + 1
                if seq[idx - 1].kind == "h" and idx in beside:
                    idx += 1            # heading and its paragraph both sit beside the float
                while 0 < idx < len(seq) and seq[idx - 1].kind == "li" and seq[idx].kind == "li":
                    idx += 1
            else:
                idx = 0
                for i, b in enumerate(seq):
                    if b.bbox and b.top <= f.top + 2:
                        idx = i + 1
            seq.insert(idx, f)
        return seq

    # ------------------------------------------------------------ whole book
    def run(self):
        seq = []
        for pno in range(1, self.doc.page_count + 1):
            seq += self.convert_page(pno)
        seq = self.attach_table_titles(seq)
        seq = self.merge_continuations(seq)
        return seq

    @staticmethod
    def attach_table_titles(seq):
        out = []
        for i, b in enumerate(seq):
            if b.kind == "table_title":
                nxt = next((x for x in seq[i + 1:] if x.kind != "p" or x.cls != "note"), None)
                if nxt is not None and nxt.kind == "table" and nxt.page == b.page and nxt.table.caption is None:
                    nxt.table.caption = b.runs
                    nxt.table.caption_page = b.page
                    continue
                b.kind = "p"
            out.append(b)
        # titles stored as the first row of a table (one Table_Title cell) become the caption
        for b in out:
            if b.kind == "table":
                t = b.table
                first = [c for c in t.rows[0] if c.lines] if t.rows else []
                ncols = max((len(r) for r in t.rows), default=0)
                is_title = len(first) == 1 and (first[0].style in ("Table_Title", "App_B_Title") or (
                    ncols > 1 and all(span_is_bold(sp) for l in first[0].lines for sp in l["spans"] if sp["text"].strip())))
                if is_title and len(t.rows) > 1:
                    t.rows[0] = first
                    if t.caption is None:
                        t.caption = join_lines(t.rows[0][0].lines)
                    t.rows = t.rows[1:]
                    t.row_pages = t.row_pages[1:]
        return out

    @staticmethod
    def merge_continuations(seq):
        out = []
        for b in seq:
            if b.kind in ("p", "li", "h") and not b.is_float and b.key is not None:
                prev = next((x for x in reversed(out) if not x.is_float and x.kind in ("p", "li", "h")), None)
                if prev is not None and prev.key == b.key and prev.page < b.page and prev.page_end == b.page - 1:
                    runs = prev.runs + [[" ", False, False]] + b.runs
                    last = prev.runs[-1][0] if prev.runs else ""
                    if prev.lines and b.lines:
                        runs = join_lines(prev.lines + b.lines)
                        if prev.kind == "li":
                            m2 = MARKER_RE.match(runs_text(runs))
                            runs = strip_prefix(runs, m2.end()) if m2 else runs
                    prev.runs = runs
                    prev.lines = prev.lines + b.lines
                    prev.page_end = b.page
                    continue
            if b.kind == "table":
                prev = next((x for x in reversed(out) if x.kind == "table"), None)
                if prev is not None and prev.key == b.key and prev.table.page < b.page:
                    head = prev.table.rows[0] if prev.table.rows else []
                    rows = b.table.rows
                    pages = b.table.row_pages
                    if rows and head and [c.text for c in rows[0]] == [c.text for c in head]:
                        rows, pages = rows[1:], pages[1:]
                    prev.table.rows += rows
                    prev.table.row_pages += pages
                    prev.page_end = b.page
                    # drop a "(Continued)" title that preceded the continuation
                    if out and out[-1].kind == "p" and re.search(r"\(Continued\)\s*$", out[-1].text):
                        out.pop()
                    continue
            out.append(b)
        # remove "(Continued)" table titles left as plain paragraphs
        return [b for b in out if not (b.kind == "p" and b.style == "Table_Title"
                                       and re.search(r"\(Continued\)\s*$", b.text))]


# ---------------------------------------------------------------- HTML rendering
def page_attrs(b, page_label):
    a = f' data-pdf-page="{b.page}"'
    if page_label.get(b.page) != str(b.page):
        a += f' data-page-label="{page_label[b.page]}"'
    if b.page_end != b.page:
        a += f' data-pdf-page-end="{b.page_end}"'
    return a


def img_tag(image, attrs=""):
    src, w, h, alt, alt_src = image
    alt = html.escape(alt or "", quote=True)
    return f'<img alt="{alt}" data-alt-source="{alt_src}" height="{h}" src="{src}" width="{w}"{attrs}/>'


def table_html(b, page_label):
    t = b.table
    keep = [(r, pg) for r, pg in zip(t.rows, t.row_pages) if any(c.lines or c.image for c in r)]
    rows = [r for r, pg in keep]
    row_pages = [pg for r, pg in keep]
    ncols = max((len(r) for r in rows), default=1)
    # column left edges from the fullest rows, to place cells of sparse rows
    full = [r for r in rows if len(r) == ncols]
    edges = []
    for ci in range(ncols):
        xs = sorted((c.bbox[0] + c.bbox[2]) / 2 for r in full for c in [r[ci]] if c.bbox and c.lines)
        edges.append(xs[len(xs) // 2] if xs else None)
    parts = [f"<table{page_attrs(b, page_label)}>"]
    if t.caption:
        parts.append(f"<caption>{runs_html(t.caption, plain=True)}</caption>")
    header_done = False
    for r, pg in zip(rows, row_pages):
        cells = list(r)
        text_cells = [c for c in cells if c.lines]
        bold = text_cells and all(all(span_is_bold(sp) for l in c.lines for sp in l["spans"] if sp["text"].strip())
                                  for c in text_cells)
        is_head = (not header_done and text_cells and len(text_cells) > 1 and r is rows[0]
                   and (all(c.header for c in text_cells) or bold)) or \
                  (not header_done and text_cells and all(c.header for c in text_cells))
        if len(cells) == 1 and ncols > 1:
            cells[0].colspan = ncols
        elif len(cells) < ncols and all(edges) and all(c.bbox for c in cells if c.lines):
            slots = [None] * ncols
            for c in cells:
                x = (c.bbox[0] + c.bbox[2]) / 2 if c.bbox else None
                k = 0
                if x is not None:
                    k = min(range(ncols), key=lambda j: abs(edges[j] - x))
                while k < ncols and slots[k] is not None:
                    k += 1
                if k < ncols:
                    slots[k] = c
            if sum(1 for s in slots if s) == len(cells):
                cells = [s if s else Cell(False, [], None) for s in slots]
        label = page_label.get(pg)
        rattr = f' data-pdf-page="{pg}"' + (f' data-page-label="{label}"' if label != str(pg) else "")
        tds = []
        for c in cells:
            tag = "th" if (c.header or is_head) and c.lines else "td"
            span = f' colspan="{c.colspan}"' if c.colspan > 1 else ""
            inner = ""
            if c.image:
                inner = img_tag(c.image)
            if c.lines:
                inner += runs_html(join_lines(c.lines), plain=(tag == "th"))
            tds.append(f"<{tag}{span}>{inner}</{tag}>")
        parts.append(f"<tr{rattr}>" + "".join(tds) + "</tr>")
        if is_head:
            header_done = True
    parts.append("</table>")
    return "".join(parts)


def lists_html(items, page_label):
    """Consecutive li blocks -> nested ul/ol HTML.

    Nesting follows the indentation level; an ordered list restarts when the numbering does
    not continue, and a deeper item opens a list inside the previous item."""
    roots = []
    stack = []   # open lists, innermost last: dict(level, type, style, last, items=[[li_html, children]])

    def new_list(b):
        return {"level": b.level, "type": b.list_type, "style": b.list_style, "start": b.number,
                "last": b.number, "items": []}

    def continues(lst, b):
        if lst["type"] != b.list_type or lst["style"] != b.list_style:
            return False
        if b.list_type == "ol" and b.number is not None and lst["last"] is not None:
            return b.number == lst["last"] + 1
        return True

    for b in items:
        item = [f"<li{page_attrs(b, page_label)}>{runs_html(b.runs)}", []]
        while len(stack) > 1 and stack[-1]["level"] > b.level:
            stack.pop()
        if stack and stack[-1]["level"] > b.level:
            stack[-1]["level"] = b.level        # outermost list was deeper: same level now
        if stack and stack[-1]["level"] == b.level and continues(stack[-1], b):
            stack[-1]["items"].append(item)
            stack[-1]["last"] = b.number
            continue
        lst = new_list(b)
        lst["items"].append(item)
        if stack and stack[-1]["level"] < b.level:
            stack[-1]["items"][-1][1].append(lst)      # nested inside the previous item
            stack.append(lst)
        elif len(stack) > 1:                            # sibling list at a nested level
            stack.pop()
            stack[-1]["items"][-1][1].append(lst)
            stack.append(lst)
        else:
            roots.append(lst)
            stack = [lst]

    def render(lst):
        attrs = ""
        if lst["type"] == "ol":
            if lst["style"] == "a":
                attrs += ' type="a"'
            if lst["start"] and lst["start"] != 1:
                attrs += f' start="{lst["start"]}"'
        inner = "".join(head + "".join(render(c) for c in kids) + "</li>" for head, kids in lst["items"])
        return f"<{lst['type']}{attrs}>{inner}</{lst['type']}>"
    return "".join(render(r) for r in roots)


def blocks_html(blocks, page_label, used_ids):
    parts, headings = [], []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        if b.kind == "li":
            j = i
            while j < len(blocks) and blocks[j].kind == "li":
                j += 1
            parts.append(lists_html(blocks[i:j], page_label))
            i = j
            continue
        if b.kind == "h":
            text = runs_text(b.runs).strip()
            base = slugify(text)
            hid, n = base, 2
            while hid in used_ids:
                hid, n = f"{base}-{n}", n + 1
            used_ids.add(hid)
            lvl = min(max(b.level, 2), 4)
            parts.append(f'<h{lvl} id="{hid}"{page_attrs(b, page_label)}>{html.escape(text, quote=False)}</h{lvl}>')
            if lvl == 2:
                headings.append((hid, text))
            b.anchor = hid
        elif b.kind == "p":
            cls = f' class="{b.cls}"' if b.cls else ""
            parts.append(f"<p{cls}{page_attrs(b, page_label)}>{runs_html(b.runs)}</p>")
        elif b.kind == "figure":
            parts.append(f"<p{page_attrs(b, page_label)}>{img_tag(b.image)}</p>")
            if b.caption_runs:
                parts.append(f'<p class="caption"{page_attrs(b, page_label)}>{runs_html(b.caption_runs, plain=True)}</p>')
        elif b.kind == "table":
            parts.append(table_html(b, page_label))
        i += 1
    return "\n".join(parts), headings


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Texas Driver Handbook</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="site-header"><a href="index.html">Texas Driver Handbook (DL-7), Texas Department of Public Safety</a></header>
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
<p class="source">Source: <a href="{source}">{source}</a> ({pages})</p>
</main>
</div>
</body>
</html>
"""

EXTRA_CSS = """
/* additions for the PDF-derived Texas handbook */
.content p.note { background:#fff8c5; border-left:4px solid #e0b400; padding:8px 12px; border-radius:4px; }
.content p.caption { color:var(--muted); font-size:15px; margin-top:-6px; }
.content caption { font-weight:600; text-align:left; padding:6px 0; }
.content td img { display:block; max-width:140px; }
"""


def nearby_alts(blocks, chapter_title):
    """Figures without a caption get alt text from nearby labels or the closest preceding heading."""
    # k uncaptioned figures followed by an untitled one-row table of k labels (the field-of-vision
    # diagrams on PDF page 51): each figure takes the label below it
    for i, b in enumerate(blocks):
        rows = [r for r in b.table.rows if any(c.lines for c in r)] if b.kind == "table" else []
        if b.kind == "table" and b.table.caption is None and len(rows) == 1:
            cells = [c for c in rows[0] if c.lines]
            figs = []
            j = i - 1
            while j >= 0 and blocks[j].kind == "figure" and blocks[j].image[3] is None:
                figs.insert(0, blocks[j])
                j -= 1
            if cells and len(figs) == len(cells):
                for f, c in zip(figs, cells):
                    f.image[3], f.image[4] = short_alt(c.text), "nearby"
    last = chapter_title
    for b in blocks:
        if b.kind == "h":
            last = runs_text(b.runs).strip()
        if b.kind == "figure" and b.image[3] is None:
            b.image[3] = f"Illustration in the handbook section “{last}” (no caption in the PDF)"
        if b.kind == "table":
            for row in b.table.rows:
                for c in row:
                    if c.image and c.image[3] is None:
                        cap = runs_text(b.table.caption).strip() if b.table.caption else last
                        c.image = (*c.image[:3], f"Sign from {cap} (no description in the PDF)", "nearby")
        if b.kind == "figure":
            b.image = tuple(b.image)


def build_site(conv, seq, out_dir):
    page_label = conv.page_label
    meta = conv.doc.metadata
    # ---- split into pages: front matter, one page per Ch_Head, back cover
    front, chapters, back = [], [], []
    current = None
    for b in seq:
        if b.page == conv.doc.page_count:
            back.append(b)
        elif b.kind == "h" and b.level == 1:
            current = {"title": runs_text(b.runs).strip(), "blocks": [], "page": b.page, "h1": b}
            chapters.append(current)
        elif current is None:
            front.append(b)
        else:
            current["blocks"].append(b)
    for ch in chapters:
        ch["slug"] = slugify(ch["title"])
        ch["page_end"] = max([b.page_end for b in ch["blocks"]] + [ch["page"]])

    cover_text = " ".join(conv.cover or [])
    m = re.search(r"Revised\s+([A-Z][a-z]+\s+\d{4})", cover_text)
    revised = m.group(1) if m else "unknown"
    created = meta.get("creationDate", "")
    cm = re.match(r"D:(\d{4})(\d{2})(\d{2})", created)
    created = f"{cm.group(1)}-{cm.group(2)}-{cm.group(3)}" if cm else "unknown"
    today = datetime.date.today().isoformat()
    dates = (f'<p class="dates">Revised: {revised} (edition printed on the cover) &middot; '
             f'PDF created: {created} &middot; Converted from the PDF: {today}</p>')

    # ---- table of contents (sidebar) and contents list (index page)
    title_index = BOOK_TITLE
    pages = [(title_index, "index")] + [(ch["title"], ch["slug"]) for ch in chapters] + [("Back cover", "back-cover")]
    toc = [(t, s, []) for t, s in pages]

    def pages_note(p0, p1):
        l0, l1 = page_label[p0], page_label[p1]
        span = f"PDF page {p0}" if p0 == p1 else f"PDF pages {p0}–{p1}"
        lab = f"printed page {l0}" if p0 == p1 else f"printed pages {l0}–{l1}"
        return f"{span}, {lab}"

    # ---- render chapters first (heading ids are needed for the contents links)
    rendered = {}
    for k, ch in enumerate(chapters):
        nearby_alts(ch["blocks"], ch["title"])
        used = set()
        content, heads = blocks_html(ch["blocks"], page_label, used)
        ch["heads"] = [(b.anchor, runs_text(b.runs).strip(), b.level) for b in ch["blocks"] if b.kind == "h"]
        rendered[ch["slug"]] = (content, heads)

    # ---- contents entries from the PDF's table of contents
    toc_items = []
    cur_ch = None
    for p in conv.toc_entries:
        raw = runs_text(join_lines(p.lines)).strip()
        mm = re.match(r"^(.*?)\s*\.{2,}\s*(\d+)\s*$", raw)
        title, num = (mm.group(1).strip(), mm.group(2)) if mm else (raw, "")
        is_ch = any(s["size"] > 10 for l in p.lines for s in l["spans"] if s["text"].strip())
        target = None
        if is_ch:
            cur_ch = next((c for c in chapters if slugify(c["title"]).startswith(slugify(title)) or
                           slugify(title).startswith(slugify(c["title"]))), None)
            target = f"{cur_ch['slug']}.html" if cur_ch else None
        elif cur_ch:
            want = slugify(title)
            hit = next((a for a, t, l in cur_ch["heads"] if slugify(t) == want), None)
            if hit is None:
                hit = next((a for a, t, l in cur_ch["heads"] if slugify(t).startswith(want[:25])), None)
            target = f"{cur_ch['slug']}.html" + (f"#{hit}" if hit else "")
        toc_items.append((is_ch, title, num, target, p.page))

    # ---- index page
    nearby_alts(front, BOOK_TITLE)
    used = set()
    content, heads = blocks_html(front, page_label, used)
    lis, open_ch = [], False
    for is_ch, title, num, target, pg in toc_items:
        attrs = f' data-pdf-page="{pg}" data-page-label="{page_label[pg]}"'
        link = f'<a href="{target}">{html.escape(title)}</a>' if target else html.escape(title)
        item = f"<li{attrs}>{link} {num}".rstrip()
        if is_ch:
            if open_ch:
                lis.append("</ul></li>")
            lis.append(item + "<ul>")
            open_ch = True
        else:
            if not open_ch:
                lis.append(item + "</li>")
            else:
                lis.append(item + "</li>")
    if open_ch:
        lis.append("</ul></li>")
    toc_title_page = TOC_PAGES[0]
    contents = (f'<h2 id="table-of-contents" data-pdf-page="{toc_title_page}" data-page-label="{page_label[toc_title_page]}">'
                f'Table of Contents</h2>\n<ul>' + "".join(lis) + "</ul>")
    contents = str(BeautifulSoup(contents, "html.parser"))
    content = content + "\n" + contents
    heads = heads + [("table-of-contents", "Table of Contents")]
    write_page(out_dir, "index", BOOK_TITLE, content, heads, toc, None, pages[1], dates,
               PDF_URL, pages_note(1, TOC_PAGES[-1]))

    for k, ch in enumerate(chapters):
        content, heads = rendered[ch["slug"]]
        prev = pages[k]
        nxt = pages[k + 2] if k + 2 < len(pages) else None
        write_page(out_dir, ch["slug"], ch["title"], content, heads, toc, prev, nxt, dates,
                   f"{PDF_URL}#page={ch['page']}", pages_note(ch["page"], ch["page_end"]))

    nearby_alts(back, "Back cover")
    content, heads = blocks_html(back, page_label, set())
    last = conv.doc.page_count
    write_page(out_dir, "back-cover", "Back cover", content, heads, toc, pages[-2], None, dates,
               f"{PDF_URL}#page={last}", pages_note(last, last))

    with open(os.path.join(out_dir, "style.css"), "w", encoding="utf-8") as f:
        f.write(MTO_CSS + EXTRA_CSS)
    return chapters


def write_page(out_dir, slug, title, content, heads, toc, prev, nxt, dates, source, pages_note):
    soup = BeautifulSoup(content, "html.parser")
    body = "\n".join(line for c in soup.children for line in pretty(c))
    onpage = ""
    if len(heads) > 1:
        items = "".join(f'<li><a href="#{i}">{html.escape(t, quote=False)}</a></li>' for i, t in heads)
        onpage = f'<nav class="on-this-page"><h2>On this page</h2><ol>{items}</ol></nav>'
    page = PAGE.format(title=html.escape(title, quote=False), intro="", toc=toc_html(toc, slug),
                       pager=pager_html(prev, nxt), onpage=onpage, content=body, dates=dates,
                       source=html.escape(source, quote=True), pages=pages_note)
    with open(os.path.join(out_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(page)


# ---------------------------------------------------------------- verification
def words(text):
    text = text.replace("\xad", "").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text.lower())


def verify(out_dir, pdf_path, min_run=4):
    """Bag-of-words coverage of the article text against the PDF text (running headers and
    page numbers removed), missing passages per PDF page, and image references."""
    doc = pymupdf.open(pdf_path)
    page_words = {}
    for i, page in enumerate(doc):
        lines = []
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                if not is_artifact_line(l):
                    lines.append("".join(s["text"] for s in l["spans"]))
        text = re.sub(r"\xad\s*\n", "", "\n".join(lines))          # soft hyphen at line end
        page_words[i + 1] = words(text)
    pdf_words = Counter(w for ws in page_words.values() for w in ws)

    html_words, alt_words, marker_words, by_page = Counter(), Counter(), Counter(), defaultdict(Counter)
    img_refs, missing_imgs = [], []
    for fn in sorted(os.listdir(out_dir)):
        if not fn.endswith(".html"):
            continue
        soup = BeautifulSoup(open(os.path.join(out_dir, fn), encoding="utf-8").read(), "html.parser")
        art = soup.select_one("article.content")
        html_words.update(words(art.get_text(" ")))
        for el in art.find_all(attrs={"data-pdf-page": True}):
            if el.find(attrs={"data-pdf-page": True}):
                inner = el.find_all(attrs={"data-pdf-page": True})
                txt = el.get_text(" ")
                for x in inner:
                    txt = txt.replace(x.get_text(" "), " ", 1)
            else:
                txt = el.get_text(" ")
            p0 = int(el["data-pdf-page"])
            p1 = int(el.get("data-pdf-page-end", p0))
            for pg in range(p0, p1 + 1):
                by_page[pg].update(words(txt))
        for ol in art.find_all("ol"):          # numbers/letters a browser renders for <ol>
            start = int(ol.get("start", 1))
            for k, li in enumerate(ol.find_all("li", recursive=False)):
                n = start + k
                marker_words.update([chr(96 + n) if ol.get("type") == "a" and n <= 26 else str(n)])
        for img in art.find_all("img"):
            alt_words.update(words(img.get("alt", "")))
            img_refs.append((fn, img["src"]))
            if not os.path.exists(os.path.join(out_dir, img["src"])):
                missing_imgs.append((fn, img["src"]))
    total = sum(pdf_words.values())
    covered = sum(min(c, html_words[w]) for w, c in pdf_words.items())
    covered_ol = sum(min(c, html_words[w] + marker_words[w]) for w, c in pdf_words.items())
    covered_alt = sum(min(c, html_words[w] + marker_words[w] + alt_words[w]) for w, c in pdf_words.items())
    extra = sum(max(0, c - pdf_words[w]) for w, c in html_words.items())
    print(f"\nText coverage (bag of words of article.content vs PDF text without running headers "
          f"and page numbers): {covered}/{total} = {100 * covered / total:.2f}%")
    print(f"   counting the numbers/letters rendered by <ol>: {100 * covered_ol / total:.2f}%;"
          f" plus img alt text: {100 * covered_alt / total:.2f}%")
    left = Counter({w: c - html_words[w] - marker_words[w] for w, c in pdf_words.items()
                    if c > html_words[w] + marker_words[w]})
    print(f"   most frequent uncovered words: {left.most_common(25)}")
    print(f"Words in the HTML beyond the PDF's counts: {extra}")

    # missing passages: runs of >= min_run PDF words of a page not found among that page's blocks
    print(f"Missing passages ({min_run}+ consecutive words of a PDF page not in that page's HTML blocks):")
    n_runs = 0
    for pg, ws in page_words.items():
        avail = Counter(by_page[pg]) + Counter(by_page[pg - 1]) + Counter(by_page[pg + 1])
        run = []
        for w in ws + [None]:
            if w is not None and avail[w] <= 0:
                run.append(w)
                continue
            if w is not None:
                avail[w] -= 1
            if len(run) >= min_run:
                n_runs += 1
                print(f"   PDF page {pg}: {' '.join(run)[:200]}")
            run = []
    print(f"   ({n_runs} runs)")
    files = set(os.listdir(os.path.join(out_dir, "images")))
    print(f"Images: {len(img_refs)} img references, {len(set(s for _, s in img_refs))} distinct files, "
          f"{len(files)} files in images/, missing files: {len(missing_imgs)}, "
          f"unreferenced files: {len(files - set(os.path.basename(s) for _, s in img_refs))}")
    for x in missing_imgs[:20]:
        print("   MISSING", x)
    return covered / total


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=OUT, help="output directory (default: tx_drivers_handbook/)")
    ap.add_argument("--verify", action="store_true", help="print coverage and image checks after converting")
    args = ap.parse_args()
    out_dir = os.path.abspath(args.out)
    pdf_path = os.path.join(out_dir, "source", "DL-7.pdf")
    download(pdf_path)
    conv = Converter(pdf_path, out_dir)
    seq = conv.run()
    chapters = build_site(conv, seq, out_dir)
    print(f"Saved {len(chapters) + 2} pages ({len(chapters)} chapters/appendices + index + back cover) "
          f"and {len(conv.renderer.files)} images to {out_dir}")
    if args.verify:
        verify(out_dir, pdf_path)


if __name__ == "__main__":
    main()
