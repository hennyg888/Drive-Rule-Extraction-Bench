"""Sentence boundaries in handbook text, and wrapping each sentence of an element in <span id>.

A sentence ends at . ! ? (with any closing quotes or brackets) followed by a space and then an
opening quote, bracket, capital letter or digit. These do not end a sentence:
    - an abbreviation: "e.g.", "St.", "Chpt." (see ABBREVIATIONS) or a run of letters "U.S."
    - an initial: "Freeman F. Martin"
    - a typed list number at the start of the text: "2. Right turn."
    - a short closing aside: "... before turning? (Chpt. 5)" stays with its sentence
"""
import re

from bs4 import BeautifulSoup, NavigableString, Tag

SENTENCE_END = re.compile(r"[.!?][\"'”’)\]]*(?=\s+[\"“‘(\[]?[A-Z0-9])")
ABBREVIATIONS = {"e.g.", "i.e.", "u.s.", "mr.", "mrs.", "ms.", "dr.", "st.", "no.", "vs.", "approx.", "inc.",
                 "a.m.", "p.m.", "etc.", "fig.", "sec.", "ch.", "chpt.", "jr.", "sr."}
NESTED = ("ul", "ol", "table")  # a nested list or table is numbered on its own, not as part of its parent


def sentence_ends(text):
    """Offsets in `text` just after each sentence end (the end of the text is not included)."""
    ends = []
    for m in SENTENCE_END.finditer(text):
        before = text[:m.start() + 1]
        word = before.split()[-1].lstrip("\"'“‘([")  # "(Chpt." is checked as "Chpt."
        if word.lower() in ABBREVIATIONS or re.fullmatch(r"(?:[a-z]\.){2,}", word.lower()):
            continue
        if re.fullmatch(r"[A-Z]\.", word):
            continue
        if re.fullmatch(r"\d+\.", word) and not before[:-len(word)].strip():
            continue
        if re.fullmatch(r"\s*\([^()]{1,25}\)\.?\s*", text[m.end():]):
            continue
        ends.append(m.end())
    return ends


def split(text):
    """The sentences of a plain string."""
    out, prev = [], 0
    for end in sentence_ends(text) + [len(text)]:
        piece = text[prev:end].strip()
        if piece:
            out.append(piece)
        prev = end
    return out


def own_children(el):
    """The children of `el` before its first nested list or table."""
    out = []
    for c in el.children:
        if isinstance(c, Tag) and c.name in NESTED:
            break
        out.append(c)
    return out


def _text(node):
    return str(node) if isinstance(node, NavigableString) else node.get_text()


def wrap(container, block_id, counter, always=False):
    """Wrap each sentence of `container` in <span id="{block_id}.{n}">, numbering on from `counter`,
    and return the new count. A container of one sentence is left as it is (and counts one),
    unless `always` (table cells: each cell is wrapped so it can be cited). A sentence end that
    falls inside an inline tag (rare) is skipped, so tags are never split."""
    kids = own_children(container)
    text = "".join(_text(k) for k in kids)
    if not text.strip():
        return counter
    cuts = sentence_ends(text)
    pieces, pos = [[]], 0
    for k in kids:
        t = _text(k)
        start, end = pos, pos + len(t)
        if isinstance(k, NavigableString):
            prev = 0
            for c in (c - start for c in cuts if start < c < end):
                pieces[-1].append(NavigableString(t[prev:c]))
                pieces.append([])
                prev = c
            pieces[-1].append(NavigableString(t[prev:]))
        else:
            pieces[-1].append(k)
        if end in cuts:
            pieces.append([])
        pos = end
    pieces = [p for p in pieces if "".join(_text(x) for x in p).strip()]
    if len(pieces) <= 1 and counter == 0 and not always:
        return counter + 1
    anchor = kids[-1].next_sibling if kids else None
    for k in kids:
        k.extract()
    maker = BeautifulSoup("", "html.parser")
    nodes = []
    for p in pieces:
        counter += 1
        lead = trail = ""
        if isinstance(p[0], NavigableString):  # spaces between sentences stay outside the spans
            s = str(p[0])
            lead, p[0] = s[:len(s) - len(s.lstrip())], NavigableString(s.lstrip())
        if isinstance(p[-1], NavigableString):
            s = str(p[-1])
            trail, p[-1] = s[len(s.rstrip()):], NavigableString(s.rstrip())
        span = maker.new_tag("span")
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
