#!/usr/bin/env python3
"""Generate the passing-rules review pages, one per jurisdiction, from data.

The look and behaviour come from the hand-built Ontario page, pages/passing-rules.html: its CSS,
JavaScript, the Rule language panel and the Census panel are copied from it unchanged
(`--vendor` copies them into tools/rules_page_assets/; the first build does this by itself).
Everything else is generated from data, in the markup the page's script expects:

  Ontario     analysis/passing-rules/inputs/passing-passages.json   (m1 ...)
              analysis/passing-rules/inputs/census-sentences.json   (c1 ..., optional)
              analysis/passing-rules/passing-rules.v1.json
  California  <data-root>/ca/meta.json, <data-root>/ca/passing-rules.v1.json,
              <data-root>/ca/inputs/passing-passages.json
  Texas       <data-root>/tx/...                (data-root defaults to analysis/passing-rules)

Output: <out-dir>/passing-rules-{ontario,california,texas}.html (out-dir defaults to pages/), each with a
tab bar linking the three. A jurisdiction whose files are missing gets a disabled "in progress" tab
and no page.

The handbook column is rebuilt from the passages; when a segment file of the handbook is available
(analysis/segments/<name>.jsonl, see tools/segment_handbook.py) it also gives the paragraph and list
structure, the "…" gaps around partial paragraphs, the chapters and the skipped sections.

Usage:
  python tools/build_rules_page.py                       build every jurisdiction that has data
  python tools/build_rules_page.py --check               also compare the Ontario page with the original
  python tools/build_rules_page.py --vendor              refresh tools/rules_page_assets/ from the original
  python tools/build_rules_page.py --data-root DIR --out-dir DIR     other CA/TX data, e.g. a test fixture
"""
import argparse
import html
import json
import os
import re
import struct
import sys
import unicodedata
from collections import Counter, OrderedDict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGINAL = os.path.join(REPO, "pages", "passing-rules.html")
ASSETS = os.path.join(REPO, "tools", "rules_page_assets")
RULES_ROOT = os.path.join(REPO, "analysis", "passing-rules")
SEGMENTS_DIR = os.path.join(REPO, "analysis", "segments")

# The three tabs, in order. Ontario's data sits at the top of analysis/passing-rules/, the others in a folder.
JURISDICTIONS = [
    {"key": "ontario", "dir": None, "short": "Ontario", "zh_short": "安大略省"},
    {"key": "california", "dir": "ca", "short": "California", "zh_short": "加州"},
    {"key": "texas", "dir": "tx", "short": "Texas", "zh_short": "德州"},
]

# Ontario's meta.json equivalent (the other jurisdictions ship a meta.json next to their rules).
ONTARIO_META = {
    "name": "Ontario MTO Driver’s Handbook",
    "zh_name": "安大略省 MTO 駕駛手冊",
    "short": "Ontario",
    "edition": "Updated August 26, 2022 · Published November 28, 2016",
    "source_url": "https://www.ontario.ca/document/official-mto-drivers-handbook",
    "scraped": "2026-10-06",
    "units": "metric",
    "handbook_dir": "handbooks/mto",
    "segments": "analysis/segments/mto.jsonl",
}

PAGE_FILE = "passing-rules-{}.html"

# The handbooks moved into handbooks/ on 23 Oct 2026. Passage files keep their old `href` values (other
# sessions pin them by hash), so old folder names are translated when links are built.
MOVED_DIRS = {"mto_drivers_handbook": "handbooks/mto", "ca_drivers_handbook": "handbooks/ca",
              "tx_drivers_handbook": "handbooks/tx"}


def current_path(path):
    """A repo path with a pre-move handbook folder name replaced by its folder under handbooks/."""
    head, sep, rest = (path or "").partition("/")
    return MOVED_DIRS[head] + sep + rest if head in MOVED_DIRS else path


def esc(s):
    return html.escape("" if s is None else str(s), quote=True)


def L(zh, en):
    """A bilingual pair; both arguments are HTML."""
    return f'<span data-l="zh" lang="zh-Hant">{zh}</span><span data-l="en" lang="en">{en}</span>'


# ------------------------------------------------------------------------------------------------ fixed strings
# Every fixed UI string below is copied, zh and en, from pages/passing-rules.html.

FLAG_NAMES = OrderedDict([   # the order of the register and of the rule language's flag table
    ("J", ("判斷詞", "Judgment term")),
    ("S", ("範圍含糊", "Hedged scope")),
    ("R", ("指涉不明", "Unclear reference")),
    ("G", ("目標與手段不一致", "Goal vs means")),
    ("D", ("隱含預設", "Implicit default")),
    ("M", ("法律效力不明", "Unclear legal force")),
    ("V", ("用詞不一致", "Wording drift")),
    ("X", ("跨頁重複", "Repeated elsewhere")),
])

FORCE_FROM = {   # the first word of force_from -> the label shown under "Force from"
    "imperative": ("祈使句，預設為 SHOULD", "Bare imperative, so SHOULD by default"),
    "caution": ("提醒句，預設為 SHOULD", "Caution, so SHOULD by default"),
    "text": ("原文用語", "Wording"),
    "default": ("預設解讀", "Default reading"),
    "context": ("所在段落", "Section context"),
    "implied": ("隱含，未明寫", "Implied, not stated"),
}

FORCE_CHIP = {"law": ("法規", "Legal"), "adv": ("建議", "Advisory")}

# section titles used when neither the original page nor meta.json names a section
FALLBACK_TITLES = {"1": ("主題介紹", "Topic introduction"), "2": ("一般指引", "General guidance"),
                   "3": ("特定情境下的指引", "Situation-specific guidance"),
                   # sections the outline in prompts/topics/passing.md added after Ontario
                   "3.1.8": ("交叉路口與車道出入口", "Crossroads and driveways"),
                   "3.1.9": ("圓環", "Roundabouts"),
                   "3.2.5": ("讓車彎", "Turnouts"),
                   "3.4.14": ("安全島旁的公車、路面電車與無軌電車", "Buses, streetcars and trolleys at safety zones"),
                   "3.4.15": ("機車車道分享", "Lane splitting"),
                   "2.3": ("盲點：不要停留在他車旁邊", "Blind spots"),
                   "3.4.16": ("停靠中的郵務、送貨與垃圾車", "Stopped mail, delivery and trash vehicles"),
                   "3.4.17": ("分心的駕駛人", "Distracted drivers")}

KEY_LEGEND = (
    '<ul class="key"><li><span class="sw law"></span>' + L("法規", "Law") +
    ' <b class="kw law">MUST</b> <b class="kw law">MUST NOT</b> <b class="kw law">MAY</b></li>'
    '<li><span class="sw adv"></span>' + L("建議", "Advice") + ' <b class="kw adv">SHOULD</b> <b class="kw adv">SHOULD NOT</b></li>'
    '<li><span class="sw desc"></span>' + L("定義與事實", "Definitions and facts") + '</li>'
    '<li><span class="sw exc"></span>' + L("例外", "Exceptions") + '</li>'
    '<li><span class="sw vg"></span>' + L("模糊用字", "Vague wording") + '</li></ul>')

PN_PREV = '<span class="pn-k">← ' + L("上一頁", "Previous") + '</span>'
PN_NEXT = '<span class="pn-k">' + L("下一頁", "Next") + ' →</span>'

SVG_ATTR = 'viewBox="0 0 20 20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
    "overview": f'<svg {SVG_ATTR}><path d="M3.5 8.6 10 3.5l6.5 5.1V16a1 1 0 0 1-1 1h-3.3v-4.4H7.8V17H4.5a1 1 0 0 1-1-1z"/></svg>',
    "doc": f'<svg {SVG_ATTR}><rect x="2.5" y="3.5" width="15" height="13" rx="2"/><path d="M10 3.5v13M5.2 7.2h2.3M5.2 10h2.3M12.5 7.2h2.3M12.5 10h2.3M12.5 12.8h2.3"/></svg>',
    "register": f'<svg {SVG_ATTR}><path d="M3 8.5c1.4-1.9 2.9-1.9 4.3 0s2.9 1.9 4.3 0 2.9-1.9 4.3 0"/><path d="M3.5 14h13" stroke-dasharray=".1 2.6" stroke-width="1.9"/></svg>',
    "files": f'<svg {SVG_ATTR}><path d="M2.5 6.2c0-.9.7-1.7 1.7-1.7h3.2l1.8 1.9h6.6c.9 0 1.7.7 1.7 1.7v6.3c0 .9-.7 1.6-1.7 1.6H4.2c-.9 0-1.7-.7-1.7-1.6z"/></svg>',
    "panel": f'<svg class="i-panel" {SVG_ATTR}><rect x="2.5" y="3.5" width="15" height="13" rx="2.5"/><path d="M7.5 3.5v13"/></svg>',
    "close": f'<svg class="i-close" {SVG_ATTR}><path d="M5 5l10 10M15 5 5 15"/></svg>',
    "menu": f'<svg {SVG_ATTR}><path d="M3.5 6h13M3.5 10h13M3.5 14h13"/></svg>',
    "logo": '<svg class="logo" viewBox="0 0 28 28" aria-hidden="true"><rect width="28" height="28" rx="7"/><path class="lane" d="M14 4.5v19"/>'
            '<path d="M18.5 23V18.4c0-2.6-9-3.2-9-6.6V6.6M6.8 9.3l2.7-2.7 2.7 2.7"/></svg>',
}

LANG_PARTS = [   # the rule language panel's six parts, for the navigation panel
    ("l-anatomy", "01", "一條規則的結構", "Anatomy of a rule"),
    ("l-types", "02", "敘述類型", "Statement types"),
    ("l-grammar", "03", "關鍵字與文法", "Keywords and grammar"),
    ("l-modal", "04", "情態詞怎麼選", "Choosing the modal"),
    ("l-wording", "05", "用詞規範", "Wording"),
    ("l-flags", "06", "模糊用字與標記", "Vague words and flags"),
]

# Added for the generated pages (not in the original): the jurisdiction tabs, the handbook facts and
# counts on the Overview, and links from passages to the offline handbook copy.
EXTRA_CSS = """
/* added by tools/build_rules_page.py: jurisdiction tabs, the handbook and counts on the Overview,
   and links from a passage to the offline copy of the handbook */
.jur-wrap { padding-top: 14px; }
.jur-tabs { display: flex; flex-wrap: wrap; gap: 2px 4px; margin: 0; padding: 0; list-style: none; border-bottom: 1px solid var(--line); }
.jur-tabs .jt { display: inline-flex; align-items: baseline; gap: 7px; margin-bottom: -1px; padding: 8px 14px 9px; border-bottom: 2px solid transparent;
                color: var(--ink-2); font-size: .93rem; font-weight: 600; text-decoration: none; }
.jur-tabs a.jt:hover { color: var(--ink); border-bottom-color: var(--line-2); }
.jur-tabs a.jt[aria-current="page"] { color: var(--ink); border-bottom-color: var(--ink); }
.jur-tabs .jt.off { color: var(--muted); cursor: default; }
.jur-tabs .jt-s { padding: 0 6px; border: 1px dashed var(--line-2); border-radius: 5px; font-size: .7rem; font-weight: 600; color: var(--muted); }
.ov-src { margin: 14px 0 0; font-size: .86rem; color: var(--ink-2); }
.ov-src a { color: var(--ink); text-decoration: underline; text-decoration-color: var(--line-2); text-underline-offset: 3px; }
.ov-src .sep { margin: 0 6px; color: var(--line-2); }
.ov-stats { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin: 0; padding: 26px 0 0; list-style: none; }
.ov-stats > li { padding: 12px 14px 13px; border-radius: 12px; background: var(--card); }
.ov-stats h3 { margin: 0 0 6px; font-size: .74rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }
.ov-stats dl { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 2px 10px; margin: 0; font-size: .86rem; color: var(--ink-2); }
.ov-stats dd { margin: 0; font-weight: 650; color: var(--ink); font-variant-numeric: tabular-nums; text-align: right; }
.ov-stats dt .chip { margin-right: 6px; }
.col-orig .where a, .col-orig .sec-name a, .col-orig .pg-h a { color: inherit; text-decoration: underline; text-decoration-color: var(--line-2); text-underline-offset: 3px; }
.col-orig .where a:hover, .col-orig .sec-name a:hover, .col-orig .pg-h a:hover { color: var(--ink); text-decoration-color: currentColor; }
@media (max-width: 900px) { .ov-stats { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 520px) { .jur-tabs .jt { padding-inline: 10px; } .ov-stats { grid-template-columns: minmax(0, 1fr); } }
"""


# ------------------------------------------------------------------------------------------------ vendoring
def _block(s, start, tag):
    """The element that starts at s[start] (a <tag ...>), up to its matching close tag."""
    depth = 0
    for m in re.compile(r"<(/?)%s\b" % tag).finditer(s, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return s[start:s.index(">", m.end()) + 1]
    raise ValueError(f"unclosed <{tag}> at {start}")


def _find(s, needle, after=0):
    i = s.find(needle, after)
    if i < 0:
        raise ValueError(f"not found in the original page: {needle!r}")
    return i


def vendor(original=ORIGINAL, out=ASSETS):
    """Copy the fixed parts of the hand-built page into tools/rules_page_assets/."""
    from bs4 import BeautifulSoup
    s = open(original, encoding="utf-8").read()
    os.makedirs(out, exist_ok=True)

    def write(name, text):
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write(text)

    head_style = re.search(r"<head>.*?<style>(.*?)</style>", s, re.S).group(1)
    write("base.css", head_style)
    write("fonts.html", "\n".join(re.findall(r'<link rel="(?:preconnect|stylesheet)"[^>]*>', s)) + "\n")
    i = _find(s, "<style>\n/* Layout")
    write("style.css", s[i + len("<style>"):_find(s, "</style>", i)])
    page = _find(s, '<div class="page"')
    i = _find(s, "<script>", page)
    write("boot.js", s[i + len("<script>"):_find(s, "</script>", i)])
    i = s.rfind("<script>")
    write("app.js", s[i + len("<script>"):_find(s, "</script>", i)])
    write("language.html", _block(s, _find(s, '<section class="intro panel" id="language"'), "section") + "\n")
    write("overview-lang.html", _block(s, _find(s, '<section class="ov-lang"'), "section") + "\n")
    write("ontario-census.html", _block(s, _find(s, '<section class="panel" id="census"'), "section") + "\n")
    write("ontario-census-nav.html", _block(s, _find(s, '<li class="nv-i" data-for="census">'), "li") + "\n")
    write("ontario-files.html", _block(s, _find(s, '<footer class="band foot" id="files"'), "footer") + "\n")

    soup = BeautifulSoup(s, "html.parser")
    # a translation memory: every English string of the page with its Chinese, for data-driven text
    # (notes, labels) that comes without a translation
    tm, clash = {}, set()
    for zh in soup.select('[data-l="zh"]'):
        en = zh.find_next_sibling()
        if en is None or en.get("data-l") != "en":
            continue
        pairs = [(en.get_text(), zh.decode_contents())]
        if en.select_one(".badge") and zh.select_one(".badge"):     # a chapter heading: also without its badge
            pairs.append((en.get_text()[len(en.select_one(".badge").get_text()):],
                          zh.decode_contents().split("</span>", 1)[1]))
        for k, v in pairs:
            k = k.strip()
            if not k or k == v:
                continue
            if k in tm and tm[k] != v:
                clash.add(k)
            tm.setdefault(k, v)
    for k in clash:
        tm.pop(k, None)

    # the rule sections' titles (1, 2.1, 3.4.4 ...) with their Chinese
    sections = OrderedDict()
    for h in soup.select("#doc .col-rules [data-sec]"):
        t = h.select_one(".ttl")
        sections[h["data-sec"]] = {"zh": t.select_one('[data-l="zh"]').decode_contents(),
                                   "en": t.select_one('[data-l="en"]').decode_contents()}
    # Ontario only: why each left-out passage is not a rule, and the left-out group's title
    left_out = OrderedDict()
    for d in soup.select("#doc .stmt.excl"):
        m = d["data-ms"]
        exn = d.select_one(".exn")
        mark = soup.select_one(f'#doc .col-orig [data-m="{m}"]')
        left_out[m] = {"text": mark.get_text() if mark else None,
                       "zh": exn.select_one('[data-l="zh"]').decode_contents(),
                       "en": exn.select_one('[data-l="en"]').decode_contents()}
    x = soup.select_one('#doc #sec-x')
    x_title = {"zh": x.select_one(".ttl [data-l=zh]").decode_contents(),
               "en": x.select_one(".ttl [data-l=en]").decode_contents()} if x else None
    strings = {"source": os.path.relpath(original, REPO), "sections": sections,
               "ontario": {"left_out": left_out, "left_out_title": x_title}, "tm": tm}
    write("strings.json", json.dumps(strings, ensure_ascii=False, indent=1) + "\n")
    print(f"vendored {shown(original)} -> {shown(out)}/ "
          f"({len(sections)} section titles, {len(tm)} translations)", file=sys.stderr)


class Assets:
    NAMES = ["base.css", "fonts.html", "style.css", "boot.js", "app.js", "language.html", "overview-lang.html",
             "ontario-census.html", "ontario-census-nav.html", "ontario-files.html", "strings.json"]

    def __init__(self, path=ASSETS):
        if not all(os.path.exists(os.path.join(path, n)) for n in self.NAMES):
            vendor(out=path)
        for n in self.NAMES:
            text = open(os.path.join(path, n), encoding="utf-8").read()
            setattr(self, re.sub(r"\W", "_", n.rsplit(".", 1)[0]), text)
        self.strings = json.loads(self.strings)
        self.tm = self.strings["tm"]
        self.sections = self.strings["sections"]


# ------------------------------------------------------------------------------------------------ helpers
def image_size(path):
    """(width, height) of a JPEG, PNG, GIF, WebP or SVG file, or None."""
    try:
        data = open(path, "rb").read()
    except OSError:
        return None
    try:
        if data[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", data[16:24])
        if data[:6] in (b"GIF87a", b"GIF89a"):
            return struct.unpack("<HH", data[6:10])
        if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
            if data[12:16] == b"VP8X":
                return (int.from_bytes(data[24:27], "little") + 1, int.from_bytes(data[27:30], "little") + 1)
            if data[12:16] == b"VP8 ":
                w, h = struct.unpack("<HH", data[26:30])
                return (w & 0x3FFF, h & 0x3FFF)
            if data[12:16] == b"VP8L":
                b = int.from_bytes(data[21:25], "little")
                return ((b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1)
        if data[:2] == b"\xff\xd8":
            i = 2
            while i + 9 < len(data):
                if data[i] != 0xFF:
                    i += 1
                    continue
                m = data[i + 1]
                if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7 or m == 0xFF:
                    i += 1 if m == 0xFF else 2
                    continue
                if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                    h, w = struct.unpack(">HH", data[i + 5:i + 9])
                    return (w, h)
                i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
        if path.lower().endswith(".svg"):
            t = data[:4000].decode("utf-8", "ignore")
            w, h = re.search(r'\bwidth="([\d.]+)', t), re.search(r'\bheight="([\d.]+)', t)
            if w and h:
                return (round(float(w.group(1))), round(float(h.group(1))))
    except (struct.error, IndexError):
        pass
    return None


def norm_text(s):
    s = unicodedata.normalize("NFKC", s or "")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip()


def num_key(sec):
    return [(0, int(x)) if x.isdigit() else (1, x) for x in str(sec).split(".")]


def shown(path):
    """A path for messages: relative inside the repository, absolute elsewhere."""
    path = os.path.abspath(path)
    return os.path.relpath(path, REPO) if path.startswith(REPO + os.sep) else path


def dedup(xs):
    return list(OrderedDict.fromkeys(x for x in xs if x))


def plural(n, one, many):
    return one if n == 1 else many


def split_sec(sec):
    """'Fog › DO · item 5' -> ('Fog › DO', 'item 5'); 'Passing' -> ('Passing', None)."""
    if not sec:
        return None, None
    if " · " in sec:
        a, b = sec.rsplit(" · ", 1)
        return a, b
    return sec, None


def stmt_kind(st):
    if st["type"] == "EXCEPTION":
        return "exc"
    if st["type"] in ("DEFINE", "FACT"):
        return "desc"
    return "law" if st.get("force") == "LEGAL" else "adv"


KIND_RANK = {"law": 0, "adv": 1, "exc": 2, "desc": 3}


# ------------------------------------------------------------------------------------------------ the data
class Jurisdiction:
    def __init__(self, spec, data_root, ontario_root):
        self.key, self.short, self.zh_short = spec["key"], spec["short"], spec["zh_short"]
        self.out_name = PAGE_FILE.format(self.key)
        self.is_ontario = spec["dir"] is None
        self.ok, self.missing = False, []
        if spec["dir"] is None:
            root = ontario_root
            files = {"passages": os.path.join(root, "inputs", "passing-passages.json"),
                     "rules": os.path.join(root, "passing-rules.v1.json")}
            self.meta = dict(ONTARIO_META)
        else:
            root = os.path.join(data_root, spec["dir"])
            files = {"passages": os.path.join(root, "inputs", "passing-passages.json"),
                     "rules": os.path.join(root, "passing-rules.v1.json"),
                     "meta": os.path.join(root, "meta.json")}
        self.root = root
        self.missing = [shown(p) for p in files.values() if not os.path.exists(p)]
        if self.missing:
            return
        try:
            if "meta" in files:
                self.meta = json.load(open(files["meta"], encoding="utf-8"))
            self.passages = json.load(open(files["passages"], encoding="utf-8"))
            self.statements = json.load(open(files["rules"], encoding="utf-8"))
            census_file = os.path.join(root, "inputs", "census-sentences.json")
            self.census = json.load(open(census_file, encoding="utf-8")) if os.path.exists(census_file) else []
        except (OSError, ValueError) as e:
            self.missing = [f"unreadable data: {e}"]
            return
        self.short = self.meta.get("short") or self.short
        self.zh_short = self.meta.get("zh_short") or self.zh_short
        self.ok = True


class Model:
    """Everything the page shows, derived once from a jurisdiction's data."""

    def __init__(self, jur, assets):
        self.j, self.a = jur, assets
        self.meta = jur.meta
        self.hb_dir = current_path(self.meta.get("handbook_dir") or "")
        self.meta = dict(self.meta, handbook_dir=self.hb_dir) if self.hb_dir else self.meta
        for p in jur.census:
            p.setdefault("part", "census")
        self.passages = [dict(p) for p in jur.passages] + [dict(p) for p in jur.census]
        self.P = OrderedDict((p["m"], p) for p in self.passages)
        self.S = jur.statements
        self.warnings = []
        # who cites each passage
        self.cited_by = {}
        self.src_info = {}     # passage id -> a statement source naming it (where, quote, image)
        for st in self.S:
            for x in st.get("sources") or []:
                self.src_info.setdefault(x["id"], x)
                if x.get("image"):
                    self.src_info[x["id"]] = {**self.src_info[x["id"]], "image": x["image"]}
            for m in self.all_ids(st):
                self.cited_by.setdefault(m, []).append(st)
                if m not in self.P:
                    self.warnings.append(f"{st['id']} cites {m}, which is not among the passages")
        self.left_out = [p for p in self.passages if p.get("part") == "excluded" or p["m"] not in self.cited_by]
        self.segments, self.seg_of, self.toc = {}, {}, {}
        self.load_segments()
        self.load_toc()

    # ---- statements
    @staticmethod
    def all_ids(st):
        return dedup([x["id"] for x in st.get("sources") or []] +
                     [m for s in st.get("steps") or [] for m in s.get("sources") or []])

    def force_class(self, m):
        sts = self.cited_by.get(m)
        if not sts or self.P.get(m, {}).get("part") == "excluded":
            return "excl"
        return min((stmt_kind(s) for s in sts), key=KIND_RANK.get)

    def image_of(self, m):
        """The picture of a figure passage: the one a statement cites if any (it can correct the passage), else its src."""
        info = self.src_info.get(m) or {}
        return info.get("image") or (self.P.get(m) or {}).get("src")

    def img_src(self, rel):
        return "../" + "/".join(x for x in (self.hb_dir, rel) if x)

    def img_size(self, rel):
        return image_size(os.path.join(REPO, self.hb_dir, rel)) if rel else None

    def where(self, m):
        info = self.src_info.get(m)
        if info and info.get("where"):
            return info["where"]
        p = self.P.get(m) or {}
        page = re.sub(r"\s+page\s+·.*$", "", p.get("page") or "")
        return " › ".join(x for x in (page, p.get("sec")) if x)

    def tr(self, en, zh=None):
        """A data-driven string in both languages: its own zh, else the original page's, else English twice."""
        if en is None:
            return ""
        if zh:
            return L(esc(zh), esc(en))
        return L(self.a.tm.get(en.strip(), esc(en)), esc(en))

    # ---- the handbook copy: segments (paragraphs, list items, figures) and its table of contents
    def load_segments(self):
        path = self.meta.get("segments")
        cands = [os.path.join(REPO, path)] if path else []
        if self.j.key != "ontario":
            name = os.path.basename(self.j.root.rstrip("/"))
            cands += [os.path.join(self.j.root, "segments.jsonl"), os.path.join(SEGMENTS_DIR, name + ".jsonl")]
            if self.hb_dir:
                cands.append(os.path.join(SEGMENTS_DIR, os.path.basename(self.hb_dir) + ".jsonl"))
        path = next((c for c in cands if os.path.exists(c)), None)
        if not path:
            return
        segs = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
        self.segments = OrderedDict((s["id"], s) for s in segs)
        self.seg_order = {sid: i for i, sid in enumerate(self.segments)}
        by_text = {}
        for s in segs:
            s["_n"] = norm_text(s.get("text"))
            if s.get("src"):
                by_text.setdefault(("src", s["src"]), []).append(s)
        prev = -1
        for p in self.passages:
            # a passage names its segment (CA, TX); Ontario's are found by their text (census ids use an older numbering)
            seg = self.segments.get(p.get("seg")) or self.match_segment(p, by_text, prev)
            if seg is not None:
                self.seg_of[p["m"]] = seg
                prev = self.seg_order[seg["id"]]

    def match_segment(self, p, by_text, prev):
        heading, _ = split_sec(p.get("sec"))
        page = norm_text(re.sub(r"\s+page\s+·.*$", "", p.get("page") or "")).lower()
        if p.get("kind") == "figure":
            img = self.image_of(p["m"])
            cands = by_text.get(("src", img), []) + by_text.get(("src", p.get("src")), [])
        else:
            t = norm_text(p.get("text"))
            if not t:
                return None
            cands = [s for s in self.segments.values() if t in s["_n"]]
        if not cands:
            return None

        def score(s):
            path = " › ".join(s.get("path") or [])
            seg_head = split_sec(s.get("sec"))[0]
            title = norm_text(s.get("page_title")).lower()
            return (
                0 if heading and heading in (path, seg_head) else 1,
                0 if page and (page in title or title in page) else 1,
                0 if self.seg_order[s["id"]] > prev else 1,
                self.seg_order[s["id"]],
            )
        return min(cands, key=score)

    def load_toc(self):
        """page slug -> (chapter number, chapter title), from the handbook's table of contents if it nests."""
        index = os.path.join(REPO, self.hb_dir, "index.html") if self.hb_dir else None
        if not index or not os.path.exists(index):
            return
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(open(index, encoding="utf-8").read(), "html.parser")
        toc = soup.select_one("nav.book-toc > ul")
        if toc is None:
            return
        tops = [li for li in toc.find_all("li", recursive=False)
                if li.a and li.a.get("href", "").split("#")[0] != "index.html"]
        if not any(li.find("ul") for li in tops):
            return
        for n, li in enumerate(tops, 1):
            title = re.sub(r"\s+", " ", li.a.get_text()).strip()
            for a in li.find_all("a"):
                self.toc.setdefault(a["href"].split("#")[0][:-5], (n, title))

    def slug_of(self, p):
        seg = self.seg_of.get(p["m"])
        if seg:
            return seg["page"]
        if p.get("href"):
            return os.path.basename(p["href"].split("#")[0])[:-5]
        return None


# ------------------------------------------------------------------------------------------------ statements
MODALS = {"MUST NOT": "law", "MUST": "law", "MAY": "law", "SHOULD NOT": "adv", "SHOULD": "adv"}
CLAUSES = ["IF VIOLATED", "ONLY IF", "DONE WHEN", "WHEN", "WHILE", "UNLESS", "UNTIL", "BECAUSE"]
GENERAL_KW = ["IF VIOLATED", "ONLY IF", "DONE WHEN", "MUST NOT", "SHOULD NOT", "WATCH FOR", "ALSO CALLED",
              "EXCEPTION TO", "SPECIALIZES", "MUST", "MAY", "SHOULD", "WHEN", "WHILE", "UNLESS", "UNTIL",
              "BECAUSE", "AND", "OR", "NOT"]
KW_RE = re.compile(r"(?<![A-Za-z])(%s)(?![A-Za-z])" % "|".join(re.escape(k) for k in GENERAL_KW))
ROW_STARTERS = set(CLAUSES) | {"ALSO CALLED", "SPECIALIZES", "THEN"}


class StatementRenderer:
    def __init__(self, model):
        self.m = model

    # -- text -> tokens: ("t", text) | ("k", word, class) | ("v", vague words)
    def tokens(self, text, st, mode):
        out = []
        parts = re.split(r"(\[\?.*?\])", text)
        define = 0     # in a DEFINE: 1 while IS is still to come, 2 while THAT is, 3 after both
        then_done = False
        for i, part in enumerate(parts):
            if part.startswith("[?") and part.endswith("]"):
                out.append(("v", part[2:-1]))
                continue
            pos = 0
            if i == 0:   # statement-type keywords open the text
                for kw, ok in (("EXCEPTION TO", True), ("DEFINE", True), ("FACT", True),
                               ("TO", mode == "procedure"), ("IF", mode == "if")):
                    if ok and re.match(re.escape(kw) + r"(?![A-Za-z])", part):
                        out.append(("k", kw, "cl" if kw == "IF" else "st"))
                        pos = len(kw)
                        define = 1 if kw == "DEFINE" else 0
                        break
            chunk = part[pos:]
            hits = [(m.start(), m.end(), m.group(0)) for m in KW_RE.finditer(chunk)]
            at = 0
            while 0 < define < 3:   # the first IS, then the first THAT after it
                kw = "IS" if define == 1 else "THAT"
                m = re.compile(r"(?<![A-Za-z])%s(?![A-Za-z])" % kw).search(chunk, at)
                if not m:
                    break
                hits.append((m.start(), m.end(), kw))
                at, define = m.end(), define + 1
            if mode == "if" and not then_done:
                m = re.search(r"(?<![A-Za-z])THEN(?![A-Za-z])", chunk)
                if m:
                    hits.append((m.start(), m.end(), "THEN"))
                    then_done = True
            last = 0
            for start, end, w in sorted(hits):
                if start < last:
                    continue
                if start > last:
                    out.append(("t", chunk[last:start]))
                if w in MODALS:
                    cls = MODALS[w]
                elif w == "WATCH FOR":
                    cls = None   # set from the modal before it
                elif w in ("AND", "OR", "NOT"):
                    cls = "cn"
                elif w in ("ALSO CALLED", "EXCEPTION TO", "SPECIALIZES", "IS", "THAT"):
                    cls = "st"
                else:
                    cls = "cl"
                out.append(("k", w, cls))
                last = end
            if last < len(chunk):
                out.append(("t", chunk[last:]))
        modal = "law" if st.get("force") == "LEGAL" else "adv"
        for i, t in enumerate(out):
            if t[0] == "k" and t[1] in MODALS:
                modal = t[2]
            if t[0] == "k" and t[1] == "WATCH FOR":
                out[i] = ("k", "WATCH FOR", modal)
        return out

    # -- tokens -> rows: the first line, then one row per clause keyword
    @staticmethod
    def rows(toks):
        rows = [[None, []]]
        for i, t in enumerate(toks):
            start = False
            if t[0] == "k" and t[1] in ROW_STARTERS:
                start = True
            elif t[0] == "k" and t[1] == "AND":
                nxt = next((u for u in toks[i + 1:] if not (u[0] == "t" and not u[1].strip())), None)
                start = bool(nxt and nxt[0] == "k" and nxt[1] in MODALS)
            if start and (rows[-1][1] or rows[-1][0]):
                rows.append([t, []])
            else:
                rows[-1][1].append(t)
        # a condition with a group in brackets shows its top-level AND / OR parts one per row
        out = []
        for head, body in rows:
            if head is None or head[2] != "cl" or not any(u[0] == "t" and "(" in u[1] for u in body):
                out.append([head, body])
                continue
            depth, cur = 0, [head, []]
            for u in body:
                if u[0] == "k" and u[1] in ("AND", "OR") and depth == 0 and cur[1]:
                    out.append(cur)
                    cur = [u, []]
                    continue
                if u[0] == "t":
                    depth += u[1].count("(") - u[1].count(")")
                cur[1].append(u)
            out.append(cur)
        return out

    def flag_for(self, st, words, seen):
        flags = [f for f in st.get("flags") or [] if f.get("span") == words]
        if not flags:
            flags = [f for f in st.get("flags") or [] if (f.get("span") or "").lower() == words.lower()]
        if not flags:
            self.m.warnings.append(f"{st['id']}: no flag for the vague words [?{words}]")
            return {"code": "J", "span": words, "note": None}
        k = seen.get(words, 0)
        seen[words] = k + 1
        return flags[min(k, len(flags) - 1)]

    def vague(self, words, flag):
        code = flag.get("code", "J")
        zh_name, en_name = FLAG_NAMES.get(code, (code, code))
        note_en = flag.get("note")
        note_zh = flag.get("zh")
        if not note_zh and note_en and note_en in self.m.a.tm:   # the translation memory holds HTML
            note_zh = html.unescape(re.sub(r"<[^>]+>", "", self.m.a.tm[note_en]))
        tip_en = f"{en_name}: {note_en}" if note_en else en_name
        tip_zh = f"{zh_name}：{note_zh or note_en}" if (note_zh or note_en) else zh_name
        return (f'<span class="vg" data-code="{esc(code)}" title="{esc(tip_en)}" data-tip-en="{esc(tip_en)}" '
                f'data-tip-zh="{esc(tip_zh)}">{esc(words)}<sup>{esc(code)}</sup></span>')

    def tok_html(self, toks, st, seen):
        out = []
        for t in toks:
            if t[0] == "t":
                out.append(esc(t[1]))
            elif t[0] == "k":
                out.append(f'<b class="kw {t[2]}">{t[1]}</b>')
            else:
                out.append(self.vague(t[1], self.flag_for(st, t[1], seen)))
        return "".join(out).strip()

    def lines(self, text, st, seen, mode="rule"):
        rows = self.rows(self.tokens(text, st, mode))
        out = []
        for head, body in rows:
            inner = self.tok_html(body, st, seen)
            if head is None:
                out.append(f'<span class="ln">{inner}</span>')
            else:
                out.append(f'<span class="cl-row"><span class="cl-k"><b class="kw {head[2]}">{head[1]}</b></span>'
                           f'<span class="cl-t">{inner}</span></span>')
        return "".join(out)

    # -- a statement
    def figure_alt(self, m, info):
        p = self.m.P.get(m) or {}
        return (info or {}).get("quote") or p.get("text") or ""

    def src_quote(self, m, info):
        p = self.m.P.get(m) or {}
        figure = p.get("kind") == "figure" or (info or {}).get("image")
        if not figure:
            return (info or {}).get("quote") or p.get("text") or ""
        label = next((c.strip() for c in (p.get("cap") or "").split("|")
                      if c.strip() and not c.strip().lower().startswith("alt text")), None)
        return f"{label or 'Picture'}, alt text: {self.figure_alt(m, info)}"

    def render(self, st):
        m = self.m
        kind = stmt_kind(st)
        sources = st.get("sources") or []
        info = OrderedDict((x["id"], x) for x in sources)
        see = st.get("see") or []
        see_ids = [x.get("source") for x in see]
        main_ms = [x["id"] for x in sources if x["id"] not in see_ids] or [x["id"] for x in sources]
        all_ids = m.all_ids(st)
        seen = {}
        # header: id, type, force, one chip per kind of flag, and "Added" for sentences from the census
        chips = [f'<span class="sid">{esc(st["id"])}</span><span class="chip t">{esc(st["type"])}</span>']
        if st["type"] in ("RULE", "PROCEDURE") and st.get("force"):
            fc = "law" if st["force"] == "LEGAL" else "adv"
            chips.append(f'<span class="chip f {fc}">{L(*FORCE_CHIP[fc])}</span>')
        for code in dedup(f.get("code") for f in st.get("flags") or []):
            chips.append(f'<span class="chip vgc" title="{esc(FLAG_NAMES.get(code, (code, code))[1])}">{esc(code)}</span>')
        if any(x.get("census_id") for x in sources):
            chips.append(f'<span class="chip addc" title="Added from the census">{L("補上", "Added")}</span>')
        # body: the statement, its steps, its pictures
        mode = "procedure" if st["type"] == "PROCEDURE" else "rule"
        body = [f'<div class="rl tgt" data-ms="{esc(" ".join(main_ms))}" data-f="{kind}">{self.lines(st["text"], st, seen, mode)}</div>']
        if st.get("steps"):
            lis = []
            for s in st["steps"]:
                n, text = str(s.get("n", "")), s.get("text", "")
                if n.upper() == "IF" or text.startswith("IF "):
                    cls, sn, md = "k-if", "", "if"
                elif n.upper() == "DONE" or text.startswith("DONE WHEN"):
                    cls, sn, md = "k-done", "", "rule"
                else:
                    cls, sn, md = "k-step", n, "rule"
                lis.append(f'<li class="pst {cls} tgt" data-ms="{esc(" ".join(s.get("sources") or []))}" data-f="{kind}">'
                           f'<span class="sn">{esc(sn)}</span><span class="rl">{self.lines(text, st, seen, md)}</span></li>')
            body.append(f'<ol class="psteps">{"".join(lis)}</ol>')
        for x in see:
            sid = x.get("source")
            img = m.image_of(sid)
            if not img:
                m.warnings.append(f"{st['id']}: SEE {x.get('figure')!r} has no picture")
                continue
            size = m.img_size(img)
            wh = f' width="{size[0]}" height="{size[1]}"' if size else ""
            body.append(f'<figure class="see tgt" data-ms="{esc(sid)}" data-f="{kind}"><figcaption><b class="kw st">SEE</b> '
                        f'{esc(x.get("figure"))}</figcaption><span class="frame"><img src="{esc(m.img_src(img))}" '
                        f'alt="{esc(self.figure_alt(sid, info.get(sid)))}"{wh} loading="lazy" decoding="async"></span></figure>')
        # details: force, flags, note, sources
        ann = []
        ff = st.get("force_from")
        if ff:
            cat = ff.split(" ", 1)[0].split("(", 1)[0]
            label = FORCE_FROM.get(cat)
            rest = ff[ff.index("(") + 1:ff.rindex(")")] if "(" in ff and ")" in ff else ""
            if label is None:
                label, rest = (ff, ff), ""
            ann.append('<p class="an-row"><span class="an-k">' + L("效力來源", "Force from") + '</span><span><b class="bk">' +
                       L(*label) + "</b>" + (f" · {esc(rest)}" if rest else "") + "</span></p>")
        for f in st.get("flags") or []:
            code = f.get("code", "?")
            name = FLAG_NAMES.get(code, (code, code))
            span = f'“{esc(f["span"])}”: ' if f.get("span") else ""
            ann.append(f'<p class="an-row"><span class="an-k"><span class="chip vgc">{esc(code)}</span> {L(*name)}</span>'
                       f'<span>{span}{m.tr(f.get("note") or "", f.get("zh"))}</span></p>')
        if st.get("note"):
            ann.append('<p class="an-row"><span class="an-k">' + L("備註", "Note") + f'</span><span>{m.tr(st["note"], st.get("note_zh"))}</span></p>')
        lis = []
        for sid in all_ids:
            loc, q = m.where(sid), self.src_quote(sid, info.get(sid) or m.src_info.get(sid))
            lis.append(f'<li><button type="button" class="srcb" data-jump="{esc(sid)}" title="{esc(loc)}">'
                       f'<span class="loc">{esc(loc)}</span><q class="srcq">{esc(q)}</q></button></li>')
        ann.append('<div class="an-row"><span class="an-k">' + L("出處", "Source") + f'</span><ul class="srcl">{"".join(lis)}</ul></div>')
        return (f'<article class="stmt {kind}" id="r-{esc(st["id"])}" data-all="{esc(" ".join(all_ids))}">'
                f'<header class="sh">{"".join(chips)}</header><div class="sb">{"".join(body)}</div>'
                f'<div class="ann">{"".join(ann)}</div></article>')


# ------------------------------------------------------------------------------------------------ the page
class PageBuilder:
    def __init__(self, model, jurs):
        self.m, self.j, self.a, self.jurs = model, model.j, model.a, jurs
        self.sr = StatementRenderer(model)
        self.census = self.j.is_ontario
        self.sections = self.section_tree()

    # ---- sections
    def title(self, sec):
        own = (self.m.meta.get("sections") or {}).get(sec)
        if isinstance(own, dict):
            return L(esc(own.get("zh") or own.get("en")), esc(own.get("en")))
        if isinstance(own, str):
            return L(self.a.tm.get(own, esc(own)), esc(own))
        t = self.a.sections.get(sec)
        if t:
            return L(t["zh"], t["en"])
        if sec in FALLBACK_TITLES:
            return L(*FALLBACK_TITLES[sec])
        head = self.heading_title(sec)
        if head:
            self.m.warnings.append(f"section {sec} is not in the Ontario template; titled after the handbook heading "
                                   f"{head!r} (name it under \"sections\" in meta.json)")
            return L(self.a.tm.get(head, esc(head)), esc(head))
        self.m.warnings.append(f"no title for section {sec}")
        return L("（未命名）", "(untitled)")

    def heading_title(self, sec):
        """The handbook heading the section's statements cite most, preferring a specific one to the topic's own."""
        c = Counter()
        for k, sts in self.sections.items():
            if k == sec or k.startswith(sec + "."):
                for st in sts:
                    for m in self.m.all_ids(st):
                        h = (split_sec((self.m.P.get(m) or {}).get("sec"))[0] or "").split(" › ")[-1].strip()
                        if h:
                            c[h] += 1
        ranked = [h for h, _ in c.most_common()]
        specific = [h for h in ranked if not re.fullmatch(r"(?i)intro|passing|overtaking", h)]
        return (specific or ranked or [None])[0]

    def section_tree(self):
        by_sec = OrderedDict()
        for st in self.m.S:
            by_sec.setdefault(str(st.get("section") or st["id"].rstrip("abcdefghijklmnopqrstuvwxyz")), []).append(st)
        return OrderedDict(sorted(by_sec.items(), key=lambda kv: num_key(kv[0])))

    @staticmethod
    def kind_counts(sts):
        c = Counter()
        for st in sts:
            if st["type"] == "PROCEDURE":
                c["proc-" + stmt_kind(st)] += 1
            else:
                c[stmt_kind(st)] += 1
        out = []
        if c["law"]:
            out.append(("law", f'{c["law"]} 條法規', f'{c["law"]} {plural(c["law"], "legal rule", "legal rules")}'))
        if c["adv"]:
            out.append(("adv", f'{c["adv"]} 條建議', f'{c["adv"]} {plural(c["adv"], "advice rule", "advice rules")}'))
        for k in ("law", "adv"):
            n = c["proc-" + k]
            if n:
                out.append((k, f"{n} 個程序", f'{n} {plural(n, "procedure", "procedures")}'))
        if c["exc"]:
            out.append(("exc", f'{c["exc"]} 條例外', f'{c["exc"]} {plural(c["exc"], "exception", "exceptions")}'))
        if c["desc"]:
            out.append(("desc", f'{c["desc"]} 條定義與事實', f'{c["desc"]} {plural(c["desc"], "definition or fact", "definitions and facts")}'))
        return out

    def rules_column(self):
        out = ['<div class="col col-rules"><p class="col-h">' + L("規則", "Rules") + "</p>"]
        done = set()
        for sec, sts in self.sections.items():
            parts = sec.split(".")
            for lv in range(1, len(parts) + 1):
                s = ".".join(parts[:lv])
                if s in done:
                    continue
                done.add(s)
                under = [x for k, v in self.sections.items() if k == s or k.startswith(s + ".") for x in v]
                if lv == 1:
                    meta = "".join(f'<span class="mp {c}">{L(esc(zh), esc(en))}</span>' for c, zh, en in self.kind_counts(under))
                    out.append(f'<div class="r-part" id="sec-{s}" data-sec="{s}" data-lv="1"><p class="eb">'
                               f'{L(f"第 {s} 部分", f"Part {s}")}</p><h3 class="ttl">{self.title(s)}</h3>'
                               f'<p class="meta">{meta}</p></div>')
                elif lv == 2:
                    n = len(under)
                    cnt = L(f"{n} 條", f"{n} " + plural(n, "statement", "statements"))
                    out.append(f'<div class="r-group" id="sec-{s}" data-sec="{s}" data-lv="2"><h4><span class="num">{s}</span>'
                               f'<span class="ttl">{self.title(s)}</span></h4><span class="cnt">{cnt}</span></div>')
                else:
                    out.append(f'<h5 class="r-sit" id="sec-{s}" data-sec="{s}" data-lv="3"><span class="num">{s}</span>'
                               f'<span class="ttl">{self.title(s)}</span></h5>')
            for st in sts:
                out.append(self.sr.render(st))
        if self.m.left_out:
            n = len(self.m.left_out)
            t = self.a.strings["ontario"].get("left_out_title") if self.j.is_ontario else None
            title = L(t["zh"], t["en"]) if t else L("未納入", "Left out")
            cnt = L(f"{n} 段", f"{n} " + plural(n, "passage", "passages"))
            out.append(f'<div class="r-part" id="sec-x" data-sec="x" data-lv="1"><p class="eb">{L("未納入", "Not included")}</p>'
                       f'<h3 class="ttl">{title}</h3><p class="meta"><span class="mp none">{cnt}</span></p></div>')
            reasons = self.a.strings["ontario"]["left_out"] if self.j.is_ontario else {}
            for p in self.m.left_out:
                mid = p["m"]
                why = ""
                r = reasons.get(mid)
                if p.get("part") != "excluded":
                    why = L("沒有任何敘述引用這段。", "No statement cites this passage.")
                elif p.get("why"):     # the passage selection's reason for leaving it out
                    why = self.m.tr(p["why"], p.get("why_zh"))
                elif r and norm_text(r.get("text")) == norm_text(p.get("text")):
                    why = L(r["zh"], r["en"])
                exn = f'<p class="exn">{why}</p>' if why else ""
                out.append(f'<div class="stmt excl tgt" data-ms="{esc(mid)}" data-all="{esc(mid)}" data-f="excl"><header class="sh">'
                           f'<span class="sid">{esc(mid)}</span><span class="chip t">{L("不寫成規則", "Not a rule here")}</span></header>{exn}</div>')
        out.append("    </div>")
        return "\n".join(out)

    # ---- the handbook column
    def heading_link(self, text, p):
        if p and p.get("href"):
            return f'<a href="../{esc(current_path(p["href"]))}" target="_blank" rel="noopener">{esc(text)}</a>'
        return esc(text)

    def mark(self, p):
        f = self.m.force_class(p["m"])
        w = f' data-w="{esc(p["w"])}"' if p.get("w") not in (None, "") else ""
        return f'<mark class="q {f}" data-f="{f}" data-m="{esc(p["m"])}"{w} tabindex="0">{esc(p.get("text"))}</mark>'

    def figure(self, p):
        f = self.m.force_class(p["m"])
        w = f' data-w="{esc(p["w"])}"' if p.get("w") not in (None, "") else ""
        img = self.m.image_of(p["m"])
        size = self.m.img_size(img)
        wh = f' height="{size[1]}"' if size else ""
        wd = f' width="{size[0]}"' if size else ""
        caps = []
        for c in (p.get("cap") or "").split("|"):
            c = c.strip()
            if c:
                caps.append(f'<span class="alt">{esc(c)}</span>' if c.lower().startswith("alt text") else f"<span>{esc(c)}</span>")
        return (f'<figure class="fig thumb" data-f="{f}" data-m="{esc(p["m"])}"{w}><img alt="{esc(p.get("text"))}"{wh} '
                f'loading="lazy" src="{esc(self.m.img_src(img))}"{wd}/><figcaption>{"".join(caps)}</figcaption></figure>')

    def para_key(self, p):
        seg = self.m.seg_of.get(p["m"])
        return seg["id"] if seg else (p.get("seg") or p.get("sec") or p["m"])

    def kind_of(self, p):
        if p.get("kind") == "figure":
            return "figure"
        seg = self.m.seg_of.get(p["m"])
        k = (seg or {}).get("kind") or p.get("kind") or "para"
        return {"text": "para", "caption": "para"}.get(k, k)

    def with_gaps(self, ps):
        """Marks of one paragraph, with "…" where the handbook paragraph has text they leave out."""
        seg = self.m.seg_of.get(ps[0]["m"])
        n = seg["_n"] if seg else None
        spans = []
        if n:
            at = 0
            for p in ps:
                t = norm_text(p.get("text"))
                i = n.find(t, at) if t else -1
                if i < 0:
                    i = n.find(t) if t else -1
                if i < 0:
                    spans = None
                    break
                spans.append((i, i + len(t)))
                at = i + len(t)
        out = []
        for k, p in enumerate(ps):
            if spans:
                before = n[:spans[0][0]] if k == 0 else n[spans[k - 1][1]:spans[k][0]]
                if re.search(r"\w", before):
                    out.append('<span class="gap">…</span>')
            out.append(self.mark(p))
        if spans and re.search(r"\w", n[spans[-1][1]:]):
            out.append('<span class="gap">…</span>')
        return " ".join(out)

    def blocks(self, ps):
        """Consecutive passages of one paragraph or item together."""
        out = []
        for p in ps:
            k = (self.para_key(p), self.kind_of(p))
            if out and out[-1][0] == k and k[1] != "figure":
                out[-1][1].append(p)
            else:
                out.append((k, [p]))
        return out

    def home_group(self, ps, label):
        o = ['<div class="grp home">', f'<p class="grp-h">{label}</p>',
             f'<p class="grp-sub">{L("手冊放 Passing 章節的那一頁。", "The page that holds the handbook’s Passing section.")}</p>']
        # the page's own sections, for the ones the topic skips
        slug = next((self.m.slug_of(p) for p in ps if self.m.slug_of(p)), None)
        page_heads = []
        if slug and self.m.segments:
            for s in self.m.segments.values():
                if s["page"] == slug:
                    h = (s.get("path") or [None])[0]
                    if h and (not page_heads or page_heads[-1] != h):
                        page_heads.append(h)
        used = set()
        for p in ps:
            seg = self.m.seg_of.get(p["m"])
            used.add((seg.get("path") or [None])[0] if seg else split_sec(p.get("sec"))[0])
        hi = 0

        def skip_to(h):
            nonlocal hi
            if h not in page_heads[hi:]:
                return
            j = page_heads.index(h, hi)
            run = [x for x in page_heads[hi:j] if x not in used]
            if run:
                name = run[0] if len(run) == 1 else f"{run[0]} … {run[-1]}"
                o.append(f'<p class="skip">{esc(name)} · {L("不屬於這個主題", "not part of this topic")}</p>')
            hi = j + 1

        cur = object()
        lst = None
        for (key, kind), grp in self.blocks(ps):
            p = grp[0]
            seg = self.m.seg_of.get(p["m"])
            top = (seg.get("path") or [None])[0] if seg else split_sec(p.get("sec"))[0]
            head = split_sec(p.get("sec"))[0]
            if head == "Intro":
                head = None
            if head != cur:
                if lst:
                    o.append(lst[1])
                    lst = None
                if top:
                    skip_to(top)
                if head:
                    o.append(f'<p class="sec-name">{self.heading_link(head, p)}</p>')
                cur = head
            if kind in ("item", "step"):
                tag = "ol" if kind == "step" else "ul"
                if lst and lst[0] != tag:
                    o.append(lst[1])
                    lst = None
                if not lst:
                    o.append(f'<{tag} class="ex">')
                    lst = (tag, f"</{tag}>")
                o.append(f"<li>{self.with_gaps(grp)}</li>")
                continue
            if lst:
                o.append(lst[1])
                lst = None
            o.append(self.figure(p) if kind == "figure" else f'<p class="ex">{self.with_gaps(grp)}</p>')
        if lst:
            o.append(lst[1])
        if page_heads:
            run = [x for x in page_heads[hi:] if x not in used]
            if run:
                name = run[0] if len(run) == 1 else f"{run[0]} … {run[-1]}"
                o.append(f'<p class="skip">{esc(name)} · {L("不屬於這個主題", "not part of this topic")}</p>')
        o.append("</div>")
        return "\n".join(o)

    def pages_group(self, ps, cls, head, sub):
        o = [f'<div class="grp {cls}">', f'<p class="grp-h">{head}</p>', f'<p class="grp-sub">{sub}</p>']
        chapter, page = None, None
        for (key, kind), grp in self.blocks(ps):
            p = grp[0]
            ch = self.m.toc.get(self.m.slug_of(p) or "")
            if ch and ch != chapter:
                if page is not None:
                    o.append("</div>")
                    page = None
                n, t = ch
                zh = '<span class="badge">第 %s 章</span>%s' % (n, self.a.tm.get(t, esc(t)))
                en = '<span class="badge">Ch %s</span>%s' % (n, esc(t))
                o.append(f'<p class="ch-h">{L(zh, en)}</p>')
                chapter = ch
            if p.get("page") != page:
                if page is not None:
                    o.append("</div>")
                o.append(f'<div class="pg">\n<p class="pg-h">{esc(p.get("page"))}</p>')
                page = p.get("page")
            if p.get("sec"):
                o.append(f'<p class="where">{self.heading_link(p["sec"], p)}</p>')
            o.append(self.figure(p) if kind == "figure" else f'<p class="ex">{self.with_gaps(grp)}</p>')
        if page is not None:
            o.append("</div>")
        o.append("</div>")
        return "\n".join(o)

    def handbook_column(self):
        ps = [p for p in self.m.passages if p.get("part") != "census"]
        added = [p for p in self.m.passages if p.get("part") == "census"]
        if any(p.get("grp") for p in ps):
            home = [p for p in ps if p.get("grp") == "home"]
        else:
            # the page whose own section is about passing (meta.json can name it), else the page with most passages
            def top(p):
                seg = self.m.seg_of.get(p["m"])
                if seg and seg.get("path"):
                    return seg["path"][0]
                return (split_sec(p.get("sec"))[0] or "").split(" › ")[0]
            about = Counter(p.get("page") for p in ps if re.match(r"(?i)(passing|overtaking)\b", top(p)))
            hp = (self.m.meta.get("home_page") or (about.most_common(1) or [(None,)])[0][0]
                  or (Counter(p.get("page") for p in ps).most_common(1) or [(None,)])[0][0])
            home = [p for p in ps if p.get("page") == hp]
        others = [p for p in ps if p not in home]
        out = ['    <div class="col col-orig">', f'<p class="col-h">{L("手冊原文", "Handbook text")}</p>']
        if home:
            page = home[0].get("page") or ""
            out.append(self.home_group(home, self.m.tr(page)))
        if others:
            n = len(dedup(p.get("page") for p in others))
            chs = len(dedup(self.m.toc.get(self.m.slug_of(p) or "") for p in others))
            zh, en = f"其他 {n} 頁", f"{n} other {plural(n, 'page', 'pages')}"
            if chs:
                zh, en = zh + f" · {chs} 個章節", en + f" · {chs} {plural(chs, 'chapter', 'chapters')}"
            out.append(self.pages_group(others, "other", L(zh, en),
                                        L("同一個主題，分散在手冊各處。", "The same topic, spread across the handbook.")))
        if added:
            # pages in the order the group above shows them, then any others; passages keep their order within a page
            seen = dedup([p.get("page") for p in others] + [p.get("page") for p in added])
            added = sorted(added, key=lambda p: seen.index(p.get("page")))
            k = len([p for p in added if p.get("kind") != "figure"])
            n = len(dedup(p.get("page") for p in added))
            out.append(self.pages_group(
                added, "added",
                L(f"全書掃描補上的 {k} 句 · {n} 頁", f"{k} {plural(k, 'sentence', 'sentences')} added from the census · {n} {plural(n, 'page', 'pages')}"),
                L("不在你的 Passing 頁上，是你選「加入」後補進來的；上面的段落維持原樣。",
                  "Not on your Passing page. Added after you chose to include them; the passages above are unchanged.")))
        out.append("</div>")
        return "\n".join(out)

    # ---- panels
    def pnav(self, prev=None, nxt=None):
        def a(cls, href, k, t, n=None):
            num = f'<span class="n">{n}</span>' if n else ""
            return f'<a class="pn {cls}" href="#{href}">{k}<span class="pn-t">{num}{t}</span></a>'
        parts = []
        if prev:
            parts.append(a("prev", prev[0], PN_PREV, prev[1], prev[2] if len(prev) > 2 else None))
        if nxt:
            parts.append(a("next", nxt[0], PN_NEXT, nxt[1], nxt[2] if len(nxt) > 2 else None))
        return f'  <nav class="pnav" aria-label="Previous and next page">{"".join(parts)}</nav>'

    def doc_panel(self):
        n = len([p for p in self.m.passages if p.get("part") != "census"])
        k = len([p for p in self.m.passages if p.get("part") == "census" and p.get("kind") != "figure"])
        zh_more, en_more = (f"，加上全書掃描補進的 {k} 句", f", plus {k} {plural(k, 'sentence', 'sentences')} added from the census") if k else ("", "")
        # Ontario's passages are michael's own selection; the other handbooks' were selected by Claude
        if self.j.is_ontario:
            zh_whose, en_whose = f"你的 {n} 段", f"your {n} {plural(n, 'passage', 'passages')}"
        else:
            zh_whose, en_whose = f"從全書選出的 {n} 段", f"{n} {plural(n, 'passage', 'passages')} selected from the whole handbook"
        lede_side = L(f"左邊是手冊原文（{zh_whose}{zh_more}），右邊是規則；每條線把原文連到它寫成的規則，滑鼠移到任一邊會標出兩端，點一下就跳到另一端。手冊的圖放在用到它的規則底下。",
                      f"Left: the handbook text ({en_whose}{en_more}). Right: the rules. Each line joins a passage to its rules; hover either side to light up both ends, click to jump to the other end. The handbook’s pictures sit under the rules that use them.")
        lede_rules = L("每條規則附上原句、效力來源與標記；手冊的圖放在用到它的規則底下。",
                       "Each rule with its source sentence, legal force and flags; the handbook’s pictures sit under the rules that use them.")
        return "\n".join([
            '<section class="doc panel" id="doc" aria-labelledby="doc-h" data-view="side">',
            '  <header class="phead">',
            f'    <p class="eb">{L("手冊", "Handbook")}</p>',
            f'    <h2 id="doc-h">{L("規則對照", "Rules")}</h2>',
            f'    <p class="lede vi-side">{lede_side}</p>',
            f'    <p class="lede vi-rules">{lede_rules}</p>',
            f"    {KEY_LEGEND}",
            "  </header>",
            '  <div class="toolbar">',
            '    <div class="seg" role="group" aria-label="View">',
            f'      <button type="button" data-view="side" aria-pressed="true">{L("左右對照", "Side by side")}</button>',
            f'      <button type="button" data-view="rules" aria-pressed="false">{L("只看規則", "Rules only")}</button>',
            "    </div>",
            '    <div class="crumb" aria-label="Current section"></div>',
            f'    <label class="switch" for="annot"><input type="checkbox" id="annot"><span class="lbl-l">{L("顯示效力來源、標記與出處", "Show force, flags and sources")}</span>'
            f'<span class="lbl-s">{L("詳細資訊", "Details")}</span></label>',
            "  </div>",
            '  <div class="align-scroll"><div class="align" id="align">',
            self.handbook_column(),
            '    <svg class="wires" aria-hidden="true"></svg>',
            self.rules_column(),
            "  </div></div>",
            self.pnav(("l-flags", L("模糊用字與標記", "Vague words and flags"), "06"), ("register", L("模糊用字", "Vague wording"))),
            "</section>",
        ])

    def flags_by_code(self):
        by = OrderedDict((c, []) for c in FLAG_NAMES)
        for st in self.m.S:
            for f in st.get("flags") or []:
                by.setdefault(f.get("code", "?"), []).append((st, f))
        return OrderedDict((c, v) for c, v in by.items() if v)

    def register_panel(self):
        by = self.flags_by_code()
        total = sum(len(v) for v in by.values())
        o = ['<section class="panel" id="register" aria-labelledby="reg-h">', '  <header class="phead">',
             f'    <p class="eb">{L("手冊", "Handbook")}</p>',
             f'    <h2 id="reg-h">{L("模糊與不確定的用字", "Vague and uncertain wording")}</h2>',
             '    <p class="lede">' + L(f'規則保留原文用字並標記，不自己發明門檻。這裡依類別列出全部 {total} 個標記，方便之後逐類處理；各類的意思見<a href="#l-flags">規則語言 › 模糊用字與標記</a>。',
                                       f'The rules keep the handbook’s words and flag them instead of inventing thresholds. All {total} flags, by kind, so each kind can be handled later; what each kind means is under <a href="#l-flags">Rule language › Vague words and flags</a>.') + "</p>",
             "  </header>", "  "]
        grid = []
        for code, items in by.items():
            name = L(*FLAG_NAMES.get(code, (code, code)))
            h = f'<h3 class="rg-h"><span class="chip vgc">{esc(code)}</span> {name} <span class="cnt">{len(items)}</span></h3>'
            if code == "J":
                words = OrderedDict()
                for st, f in items:
                    words.setdefault((f.get("span") or "").lower(), [f.get("span") or "", []])[1].append(st["id"])
                rows = sorted(words.values(), key=lambda w: (-len(w[1]), w[0].lower()))
                lis = "".join(f'<li><span class="rw">{esc(w)}</span>' + " ".join(f'<a href="#r-{esc(i)}" class="rid">{esc(i)}</a>' for i in dedup(ids)) + "</li>"
                              for w, ids in rows)
                o.append(f'<section class="rg rg-j" id="rg-J">{h}<p class="rg-d">' +
                         L("每個字與用到它的規則；模糊的原因記在各規則的詳細資訊裡。", "Each word with the rules that use it; why it is vague is noted in each rule’s details.") +
                         f'</p><ul class="rg-words">{lis}</ul></section>')
            else:
                lis = "".join(f'<li><a href="#r-{esc(st["id"])}" class="rid">{esc(st["id"])}</a><span class="rg-x"><span class="rg-t">{esc(f.get("span") or "")}</span>'
                              f'<span class="rg-n">{self.m.tr(f.get("note") or "", f.get("zh"))}</span></span></li>' for st, f in items)
                grid.append(f'<section class="rg" id="rg-{esc(code)}">{h}<ul class="rg-rows">{lis}</ul></section>')
        if grid:
            o.append('<div class="rg-grid">' + "\n".join(grid) + "</div>")
        o.append(self.pnav(("doc", L("規則對照", "Rules")), ("census", L("全書掃描", "Census")) if self.census else None))
        o.append("</section>")
        return "\n".join(o)

    def counts(self):
        S = self.m.S
        cited = [m for m in self.m.cited_by if m in self.m.P]
        return {
            "statements": len(S), "passages": len(cited),
            "legal": sum(1 for s in S if s.get("force") == "LEGAL"),
            "advice": sum(1 for s in S if s["type"] == "RULE" and s.get("force") == "ADVISORY"),
            "flags": sum(len(s.get("flags") or []) for s in S),
        }

    def overview_panel(self):
        c = self.counts()
        meta, S = self.m.meta, self.m.S
        def en(n, one, many):
            return f"<b>{n}</b> " + plural(n, one, many)
        facts = [L(f'<b>{c["statements"]}</b> 條敘述，來自 <b>{c["passages"]}</b> 段原文',
                   en(c["statements"], "statement", "statements") + " from " + en(c["passages"], "passage", "passages")),
                 L(f'<b>{c["legal"]}</b> 條法規', en(c["legal"], "legal rule", "legal rules")),
                 L(f'<b>{c["advice"]}</b> 條建議', en(c["advice"], "advice rule", "advice rules")),
                 L(f'<b>{c["flags"]}</b> 處模糊用字', en(c["flags"], "vague spot flagged", "vague spots flagged"))]
        name = meta.get("name") or self.j.short
        src = []
        if meta.get("source_url"):
            src.append(L("來源", "Source") + f': <a href="{esc(meta["source_url"])}" target="_blank" rel="noopener">{esc(name)}</a>')
        if meta.get("edition"):
            src.append(L("版本", "Edition") + f": {esc(meta['edition'])}")
        if meta.get("scraped"):
            src.append(L("離線副本", "Offline copy") + f": {esc(meta['scraped'])}" +
                       (f' (<a href="../{esc(meta["handbook_dir"])}/index.html" target="_blank" rel="noopener"><code>{esc(meta["handbook_dir"])}/</code></a>)' if meta.get("handbook_dir") else ""))
        if meta.get("units"):
            src.append(L("單位", "Units") + f": {self.m.tr(meta['units'])}")
        types = Counter(s["type"] for s in S)
        force = Counter(s.get("force") or "none" for s in S)
        flags = self.flags_by_code()
        n_src = sum(len(self.m.all_ids(s)) for s in S)
        figs = len([m for m in self.m.cited_by if (self.m.P.get(m) or {}).get("kind") == "figure"])
        added = len([m for m in self.m.cited_by if (self.m.P.get(m) or {}).get("part") == "census"])

        def card(title, rows):
            dl = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows)
            return f"<li><h3>{title}</h3><dl>{dl}</dl></li>"
        type_rows = [(f'<span class="chip t">{t}</span>', types[t]) for t in ("RULE", "PROCEDURE", "EXCEPTION", "DEFINE", "FACT") if types[t]]
        type_rows += [(f'<span class="chip t">{esc(t)}</span>', n) for t, n in types.items() if t not in ("RULE", "PROCEDURE", "EXCEPTION", "DEFINE", "FACT")]
        force_rows = [(f'<span class="chip f law">{L("法規", "Legal")}</span>', force["LEGAL"]),
                      (f'<span class="chip f adv">{L("建議", "Advisory")}</span>', force["ADVISORY"]),
                      (L("無（定義、事實、例外）", "None (definitions, facts, exceptions)"), force["none"])]
        flag_rows = [(f'<span class="chip vgc">{esc(code)}</span>{L(*FLAG_NAMES.get(code, (code, code)))}', len(v)) for code, v in flags.items()]
        src_rows = [(L("手冊段落", "Handbook passages"), len(self.m.P)), (L("被引用的段落", "Passages cited"), c["passages"]),
                    (L("出處連結", "Source links"), n_src), (L("引用的圖", "Pictures cited"), figs)]
        if added:
            src_rows.append((L("全書掃描補上的", "Added from the census"), added))
        if self.m.left_out:
            src_rows.append((L("未納入", "Left out"), len(self.m.left_out)))
        stats = ('<ul class="ov-stats" aria-label="Counts">' +
                 card(L("敘述類型", "Statement types"), type_rows) + card(L("效力", "Force"), force_rows) +
                 card(L("模糊用字", "Vague wording"), flag_rows or [(L("無", "None"), 0)]) + card(L("出處", "Sources"), src_rows) + "</ul>")
        return "\n".join([
            '<section class="panel ov" id="overview" aria-labelledby="ov-h">',
            '  <header class="hero">',
            f'    <p class="eyebrow">{L("Wise Lab · " + esc(meta.get("zh_name") or name), "Wise Lab · " + esc(name))}</p>',
            f'    <h1 id="ov-h">Passing<small>{L("超車規則 · v1", "rules · v1")}</small></h1>',
            f'    <p class="lede">{L("把手冊裡的超車內容寫成形式化規則：一套小而固定、讀起來仍像英文的規則語言，每條都連回它來自的原句。", "The handbook’s passing content as formal rules, in a small rule language that still reads like English. Every rule links back to the sentence it came from.")}</p>',
            '    <p class="ov-src">' + '<span class="sep" aria-hidden="true">·</span>'.join(src) + "</p>" if src else "",
            '    <ul class="facts">',
            "      " + "".join(f"<li>{x}</li>" for x in facts),
            "    </ul>",
            f"    {KEY_LEGEND}",
            f"    {stats}",
            "  </header>",
            "  " + self.a.overview_lang.strip(),
            self.pnav(None, ("l-anatomy", L("一條規則的結構", "Anatomy of a rule"), "01")),
            "</section>",
        ])

    def files_footer(self):
        if self.j.is_ontario:
            return self.a.ontario_files.strip()
        analysis = os.path.join(REPO, "analysis")
        root = os.path.abspath(self.j.root)
        rel = (os.path.relpath(root, analysis) if root.startswith(analysis + os.sep)
               else "passing-rules/" + os.path.basename(root.rstrip(os.sep)))
        rows = [("rule-language-v1.md", "規則語言 v1 的完整定義", "the full definition of rule language v1"),
                (f"{rel}/passing-rules.v1.json", "本頁的規則（機器可讀）", "the rules on this page, machine-readable"),
                (f"{rel}/inputs/passing-passages.json", "本頁左邊的手冊段落", "the handbook passages in the left column"),
                (f"{rel}/meta.json", "手冊名稱、版本與來源", "the handbook’s name, edition and source")]
        lis = "\n".join(f"    <li><code>{esc(p)}</code> · {L(zh, en)}</li>" for p, zh, en in rows)
        return "\n".join(['<footer class="band foot" id="files" aria-labelledby="files-h">',
                          f'  <h2 class="sec-h" id="files-h">{L("檔案（Wise Lab/analysis/）", "Files (Wise Lab/analysis/)")}</h2>',
                          '  <ul class="files">', lis, "  </ul>", "</footer>"])

    # ---- navigation
    def nav(self):
        def nv(zh, en):
            return f'<span class="nv-l">{L(zh, en)}</span>'
        doc_toc = []
        parts = OrderedDict()
        for sec in self.sections:
            p = sec.split(".")
            parts.setdefault(p[0], [])
            if len(p) > 1 and ".".join(p[:2]) not in parts[p[0]]:
                parts[p[0]].append(".".join(p[:2]))
        for part, groups in parts.items():
            sub = ""
            if groups:
                sub = "<ol>" + "".join(f'<li class="lv2"><a href="#sec-{g}" data-sec="{g}"><span class="num">{g}</span><span class="ttl">{self.title(g)}</span></a></li>'
                                       for g in groups) + "</ol>"
            doc_toc.append(f'<li class="lv1"><a href="#sec-{part}" data-sec="{part}"><span class="num">{part}</span><span class="ttl">{self.title(part)}</span></a>{sub}</li>')
        if self.m.left_out:
            doc_toc.append(f'<li class="lv1"><a href="#sec-x" data-sec="x"><span class="num">×</span><span class="ttl">{L("未納入", "Left out")}</span></a></li>')
        by = self.flags_by_code()
        reg = "".join(f'<li><a href="#rg-{esc(c)}"><span class="num"><span class="chip vgc">{esc(c)}</span></span><span class="ttl">{L(*FLAG_NAMES.get(c, (c, c)))}</span>'
                      f'<span class="cnt">{len(v)}</span></a></li>' for c, v in by.items())
        lang = "".join(f'<li class="nv-i" data-for="{k}"><a class="nv-a" href="#{k}" data-open-part="{k}"><span class="nv-n">{n}</span>{nv(zh, en)}</a></li>'
                       for k, n, zh, en in LANG_PARTS)
        census = self.a.ontario_census_nav.strip() if self.census else ""
        return "".join([
            '<nav class="nav" id="nav" aria-label="Pages" tabindex="-1"><div class="nav-top">',
            f'<a class="brand" href="#overview" data-open-tab="overview">{ICONS["logo"]}<span class="brand-t"><b>{L("超車規則", "Passing rules")}</b>'
            f'<small>{L("規則語言 v1", "Rule language v1")}</small></span></a>',
            f'<button type="button" class="icon-btn nav-x" aria-controls="nav">{ICONS["panel"]}{ICONS["close"]}<span class="sr">{L("收起導覽", "Hide navigation")}</span></button></div>',
            '<div class="nav-body"><ul class="nv">',
            f'<li class="nv-i" data-for="overview"><a class="nv-a" href="#overview" data-open-tab="overview">{ICONS["overview"]}{nv("總覽", "Overview")}</a></li></ul>',
            f'<p class="nv-h" id="nv-lang">{L("規則語言", "Rule language")}</p><ul class="nv" aria-labelledby="nv-lang">{lang}</ul>',
            f'<p class="nv-h" id="nv-hb">{L("手冊", "Handbook")}</p><ul class="nv" aria-labelledby="nv-hb">',
            f'<li class="nv-i" data-for="doc"><a class="nv-a" href="#doc" data-open-tab="doc">{ICONS["doc"]}{nv("規則對照", "Rules")}<span class="nv-c">{len(self.m.S)}</span></a>'
            f'<ol class="nv-sub nv-doc">{"".join(doc_toc)}</ol></li>',
            f'<li class="nv-i" data-for="register"><a class="nv-a" href="#register" data-open-tab="register">{ICONS["register"]}{nv("模糊用字", "Vague wording")}'
            f'<span class="nv-c">{sum(len(v) for v in by.values())}</span></a><ol class="nv-sub">{reg}</ol></li>',
            census,
            "</ul></div>",
            f'<div class="nav-foot"><a class="nv-a nv-files" href="#files">{ICONS["files"]}{nv("檔案", "Files")}</a>',
            '<div class="seg nav-lang" role="group" aria-label="Language"><button type="button" data-lang-btn="en" aria-pressed="true">English</button>'
            '<button type="button" data-lang-btn="zh" aria-pressed="false">中文</button></div></div></nav>',
        ])

    def appbar(self):
        return "\n".join([
            '<header class="appbar">',
            f'  <button type="button" class="icon-btn nav-open" aria-controls="nav" aria-expanded="false">{ICONS["menu"]}<span class="sr">{L("顯示導覽", "Show navigation")}</span></button>',
            f'  <p class="ab-t"><span class="ab-brand">{L("超車規則", "Passing rules")}</span><span class="ab-sep" aria-hidden="true">/</span><span class="ab-page"></span></p>',
            '  <div class="seg lang-bar" role="group" aria-label="Language"><button type="button" data-lang-btn="en" aria-pressed="true">English</button><button type="button" data-lang-btn="zh" aria-pressed="false">中文</button></div>',
            "</header>",
        ])

    def jur_tabs(self):
        tabs = []
        for j in self.jurs:
            name = L(esc(j.zh_short), esc(j.short))
            if j.key == self.j.key:
                tabs.append(f'<li><a class="jt" href="{esc(j.out_name)}" aria-current="page">{name}</a></li>')
            elif j.ok:
                tabs.append(f'<li><a class="jt" href="{esc(j.out_name)}">{name}</a></li>')
            else:
                tabs.append(f'<li><span class="jt off" aria-disabled="true" title="in progress">{name}<span class="jt-s">{L("進行中", "in progress")}</span></span></li>')
        return (f'<div class="wrap jur-wrap"><nav aria-label="Jurisdiction"><ul class="jur-tabs">{"".join(tabs)}</ul></nav></div>')

    def build(self):
        a = self.a
        panels = ["overview", "language", "doc", "register"] + (["census"] if self.census else [])
        boot = a.boot.replace("['overview', 'language', 'doc', 'register', 'census']", repr(panels).replace('"', "'"))
        language = a.language.strip()
        if not self.j.is_ontario:
            # the rule language's examples are Ontario's rules: link them to the Ontario page
            onto = next((x for x in self.jurs if x.key == "ontario"), None)
            target = onto.out_name if onto and onto.ok else "passing-rules.html"
            language = re.sub(r'href="#(r-[^"]+)"', lambda mm: f'href="{target}#{mm.group(1)}"', language)
        title = f"Passing Rules · {self.j.short}"
        body = "\n".join([
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">',
            f"<title>{esc(title)}</title>",
            f'<meta name="generator" content="tools/build_rules_page.py from {esc(self.a.strings.get("source", "pages/passing-rules.html"))}">',
            a.fonts.strip(),
            f"<style>{a.base}</style>",
            f"<style>{a.style}</style>",
            f"<style>{EXTRA_CSS}</style>",
            "</head><body>",
            '<div class="page" data-lang="en" data-tab="overview" data-part="l-anatomy">',
            f"<script>{boot}</script>",
            '<div class="shell">',
            self.nav(),
            '<div class="scrim" aria-hidden="true"></div>',
            '<div class="main" id="main">',
            self.appbar(),
            self.jur_tabs(),
            '<div class="wrap">',
            "",
            self.overview_panel(),
            "",
            language,
            "",
            self.doc_panel(),
            "",
            self.register_panel(),
            "",
            a.ontario_census.strip() if self.census else "",
            "",
            self.files_footer(),
            "</div>", "</div>", "</div>", "</div>",
            f"<script>{a.app}</script>",
            "</body></html>",
            "",
        ])
        return body


# ------------------------------------------------------------------------------------------------ checking
def compare_with_original(generated_path, original=ORIGINAL):
    """Compare the generated Ontario page with the hand-built one; returns a list of report lines."""
    from bs4 import BeautifulSoup

    def load(p):
        return BeautifulSoup(open(p, encoding="utf-8").read(), "html.parser")

    def text(el):   # the words, with element boundaries counted as spaces
        return re.sub(r"\s+", " ", el.get_text(" ")).strip() if el is not None else None

    def flat(el):   # the text exactly as rendered inline (tags stripped, nothing added)
        return re.sub(r"\s+", " ", el.get_text()).strip() if el is not None else None

    a, b = load(original), load(generated_path)
    out = []

    def stmts(s):
        return OrderedDict((x["id"][2:], x) for x in s.select("#doc .col-rules article.stmt"))
    sa, sb = stmts(a), stmts(b)
    out.append(f"statements: original {len(sa)}, generated {len(sb)}; ids identical and in the same order: {list(sa) == list(sb)}")
    if set(sa) != set(sb):
        out.append(f"  only in original: {sorted(set(sa) - set(sb))}; only in generated: {sorted(set(sb) - set(sa))}")
    pa = [x["data-m"] for x in a.select("#doc .col-orig [data-m]")]
    pb = [x["data-m"] for x in b.select("#doc .col-orig [data-m]")]
    out.append(f"passages: original {len(pa)}, generated {len(pb)}; same ids: {sorted(pa) == sorted(pb)}; same order: {pa == pb}")
    if sorted(pa) != sorted(pb):
        out.append(f"  only in original: {sorted(set(pa) - set(pb))}; only in generated: {sorted(set(pb) - set(pa))}")
    fa = {x["data-m"]: x.get("data-f") for x in a.select("#doc .col-orig [data-m]")}
    fb = {x["data-m"]: x.get("data-f") for x in b.select("#doc .col-orig [data-m]")}
    diff_f = [m for m in fa if fa[m] != fb.get(m)]
    out.append(f"passage colours (data-f) that differ: {diff_f or 'none'}")

    def flags(art):
        rows = []
        for r in art.select(".ann > p.an-row"):
            chip = r.select_one(".an-k .chip.vgc")
            if chip:
                rows.append((chip.get_text(), text(r.find_all("span", recursive=False)[-1])))
        return rows

    def vgs(art):
        return [(v.get("data-code"), text(v), v.get("data-tip-en"), v.get("data-tip-zh")) for v in art.select(".sb .vg")]

    def sources(art):
        return [(x.get("data-jump"), x.get("title"), text(x.select_one(".srcq"))) for x in art.select(".srcb")]

    def wiring(art):
        return [(t.name, " ".join(t.get("class", [])), t.get("data-ms"), t.get("data-f")) for t in art.select(".tgt")] + [("all", art.get("data-all"))]

    def chips(art):
        return [(" ".join(c.get("class", [])), text(c), c.get("title")) for c in art.select(".sh .chip")]

    def figs(art):
        return [(i.get("src"), i.get("alt"), i.get("width"), i.get("height")) for i in art.select("img")]

    def html_norm(el):
        return re.sub(r"\s+", " ", BeautifulSoup(str(el), "html.parser").decode()).replace("> <", "><")

    checks = OrderedDict([("flags", flags), ("vague marks", vgs), ("source buttons", sources), ("wiring (data-ms/data-f/data-all)", wiring),
                          ("chips", chips), ("pictures", figs)])
    bad = {k: [] for k in checks}
    text_diff, layout_diff, html_same = [], [], 0
    nflags = nsrc = 0
    for sid, x in sa.items():
        y = sb.get(sid)
        if y is None:
            continue
        for k, f in checks.items():
            if f(x) != f(y):
                bad[k].append(sid)
        nflags += len(flags(x))
        nsrc += len(sources(x))
        ta, tb = text(x.select_one(".sb")), text(y.select_one(".sb"))
        if ta != tb:
            text_diff.append((sid, ta, tb))
        elif flat(x.select_one(".sb")) != flat(y.select_one(".sb")):
            layout_diff.append(sid)
        if html_norm(x) == html_norm(y):
            html_same += 1
    out.append(f"flags compared: {nflags}; statements whose flag rows differ: {bad['flags'] or 'none'}")
    out.append(f"source buttons compared: {nsrc}; statements whose source buttons differ: {bad['source buttons'] or 'none'}")
    for k in ("vague marks", "wiring (data-ms/data-f/data-all)", "chips", "pictures"):
        out.append(f"{k}: statements that differ: {bad[k] or 'none'}")
    out.append(f"statement texts (tags stripped) identical: {len(sa) - len(text_diff)} of {len(sa)}")
    for sid, ta, tb in text_diff:
        out.append(f"  {sid}:\n    original : {ta}\n    generated: {tb}")
    out.append(f"statements with the same words but rows broken differently: {layout_diff or 'none'}")
    out.append(f"statements whose whole markup is identical (after normalising whitespace and escaping): {html_same} of {len(sa)}")
    ra = [(x.get("href"), text(x)) for x in a.select("#register a.rid")]
    rb = [(x.get("href"), text(x)) for x in b.select("#register a.rid")]
    out.append(f"register links: original {len(ra)}, generated {len(rb)}, identical: {ra == rb}")
    rga = [(s.get("id"), text(s)) for s in a.select("#register section.rg")]
    rgb = [(s.get("id"), text(s)) for s in b.select("#register section.rg")]
    out.append(f"register sections identical (text): {rga == rgb}")
    if rga != rgb:
        for (ia, ta), (ib, tb) in zip(rga, rgb):
            if ta != tb:
                out.append(f"  {ia}: original {ta[:200]!r}\n        generated {tb[:200]!r}")
    for sel, name in (("#overview .facts", "overview facts"), ("#nav .nv-doc", "rules table of contents"), ("#nav .nv-i[data-for=register]", "register nav"),
                      ("#doc .col-rules .r-part, #doc .col-rules .r-group, #doc .col-rules .r-sit", "section headings")):
        ta = [text(x) for x in a.select(sel)]
        tb = [text(x) for x in b.select(sel)]
        out.append(f"{name} identical: {ta == tb}")
        if ta != tb:
            for u, v in zip(ta, tb):
                if u != v:
                    out.append(f"  original : {u[:300]}\n  generated: {v[:300]}")
    for sel, name in (("#language", "rule language panel"), ("#census", "census panel")):
        out.append(f"{name} identical: {html_norm(a.select_one(sel)) == html_norm(b.select_one(sel))}")
    # the handbook column, block by block
    ca = [text(x) for x in a.select("#doc .col-orig .grp > *, #doc .col-orig .pg > *")]
    cb = [text(x) for x in b.select("#doc .col-orig .grp > *, #doc .col-orig .pg > *")]
    import difflib
    sm = difflib.SequenceMatcher(None, ca, cb, autojunk=False)
    out.append(f"handbook column blocks: original {len(ca)}, generated {len(cb)}, matching {sum(t.size for t in sm.get_matching_blocks())}")
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            out.append(f"  {op}: original {[s[:90] for s in ca[i1:i2]]}\n        generated {[s[:90] for s in cb[j1:j2]]}")
    return out


# ------------------------------------------------------------------------------------------------ main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-root", default=RULES_ROOT, help="folder holding ca/ and tx/ (default: analysis/passing-rules)")
    ap.add_argument("--ontario-root", default=RULES_ROOT, help="folder holding Ontario's data (default: analysis/passing-rules)")
    ap.add_argument("--out-dir", default=os.path.join(REPO, "pages"), help="where the pages go (default: pages/)")
    ap.add_argument("--assets", default=ASSETS, help="vendored parts of the original page (default: tools/rules_page_assets)")
    ap.add_argument("--vendor", action="store_true", help="copy the fixed parts of pages/passing-rules.html into --assets first")
    ap.add_argument("--check", action="store_true", help="compare the generated Ontario page with pages/passing-rules.html")
    ap.add_argument("--only", help="comma-separated jurisdictions to write (ontario, california, texas)")
    args = ap.parse_args(argv)

    if args.vendor:
        vendor(out=args.assets)
    assets = Assets(args.assets)
    jurs = [Jurisdiction(spec, os.path.abspath(args.data_root), os.path.abspath(args.ontario_root)) for spec in JURISDICTIONS]
    only = set(args.only.split(",")) if args.only else None
    os.makedirs(args.out_dir, exist_ok=True)
    written = {}
    for j in jurs:
        if not j.ok:
            print(f"{j.short}: no page (in progress; missing {', '.join(j.missing)})", file=sys.stderr)
            continue
        if only and j.key not in only:
            continue
        model = Model(j, assets)
        page = PageBuilder(model, jurs).build()
        path = os.path.join(args.out_dir, j.out_name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)
        written[j.key] = path
        located = len(model.seg_of)
        print(f"{j.short}: wrote {shown(path)} ({len(model.S)} statements, {len(model.P)} passages, "
              f"{located} placed in the handbook's paragraphs)", file=sys.stderr)
        for w in dedup(model.warnings):
            print(f"  warning: {w}", file=sys.stderr)
    if args.check:
        if "ontario" not in written:
            print("--check needs the Ontario page", file=sys.stderr)
            return 1
        print("\n".join(compare_with_original(written["ontario"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
