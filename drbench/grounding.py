"""A model's citation -> sentence ids in the corpus.

A model cites the handbook with a block id and a quote copied from that block:
    {"block": "10.22", "quote": "Never pass on the right unless ..."}
`resolve` finds the quote among the sentences of block 10.22 and returns the ids of the sentences
it covers, with how it was found:
    exact         the quote is in the block (after evening out case, spaces, curly quotes and dashes);
                  a quote with "..." in it is matched piece by piece
    fuzzy         not word for word, but most of the quote is in a sentence, or most of a sentence
                  is in the quote
    other-block   the quote is not in the cited block but in another block of the same page
                  (its id is given as "found_in")
    heading       the quote is the cited heading (headings have no sentence ids)
    not-found     the quote is not on the page
    no-block      the page or the block does not exist
`resolve_output` does this for every {"block", "quote"} object in a model's answer, whatever the
rest of the answer looks like.
"""
import difflib
import re
from collections import Counter
from functools import lru_cache

from .corpus import blocks_of, load_pages, own_sentences, page_soup, text_containers
from .sentences import own_children

SAME = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", " ": " "})
ELLIPSIS = re.compile(r"\s*(?:\.\.\.|…)\s*")


def canon(s):
    return re.sub(r"\s+", " ", (s or "").translate(SAME)).strip().lower()


def _own_text(container):
    return "".join(str(k) if isinstance(k, str) else k.get_text() for k in own_children(container))


@lru_cache(maxsize=None)
def page_blocks(handbook_id, page_no):
    """{block id: {"tag", "text", "sentences": [(sentence id, text)]}} of one page; None if no such page."""
    meta = next((p for p in load_pages(handbook_id) if p["page"] == page_no), None)
    if meta is None:
        return None
    out = {}
    for b in blocks_of(page_soup(handbook_id, meta).find("article")):
        spans = own_sentences(b)
        text = " ".join(_own_text(c) for c in text_containers(b)) if b.name not in ("h2", "h3", "h4") else b.get_text()
        if spans:
            sents = [(s["id"], s.get_text()) for s in spans]
        elif b.name in ("h2", "h3", "h4") or not text.strip():
            sents = []
        else:
            sents = [(f"{b['id']}.1", text)]
        out[b["id"]] = {"tag": b.name, "text": text, "sentences": sents}
    return out


def _exact(block, pieces):
    """Sentence ids covered by the pieces of a quote, found in order in the block; None if one is missing."""
    joined, spans = "", []
    for sid, t in block["sentences"]:
        start = len(joined)
        joined += canon(t)
        spans.append((sid, start, len(joined)))
        joined += " "
    ids, pos = [], 0
    for q in pieces:
        i = joined.find(q, pos)
        if i < 0:
            return None
        ids += [sid for sid, a, b in spans if a < i + len(q) and i < b and sid not in ids]
        pos = i + len(q)
    return ids


def _fuzzy(block, q, share=0.85):
    ids = []
    for sid, t in block["sentences"]:
        s = canon(t)
        if not s:
            continue
        m = difflib.SequenceMatcher(None, q, s, autojunk=False)
        same = sum(b.size for b in m.get_matching_blocks() if b.size >= 4)
        if same >= share * len(s) or same >= share * len(q):
            ids.append(sid)
    return ids


def resolve(handbook_id, block, quote):
    """{"sentences": [ids], "match": kind} for one citation (plus "found_in" for other-block)."""
    try:
        page_no = int(str(block).split(".")[0])
    except ValueError:
        return {"sentences": [], "match": "no-block"}
    page = page_blocks(handbook_id, page_no)
    if not page or block not in page:
        return {"sentences": [], "match": "no-block"}
    pieces = [canon(p).strip(" \"'") for p in ELLIPSIS.split(quote or "")]
    pieces = [p for p in pieces if p]
    if not pieces:
        return {"sentences": [], "match": "not-found"}
    cited = page[block]
    if cited["tag"] in ("h2", "h3", "h4"):
        if all(p in canon(cited["text"]) for p in pieces):
            return {"sentences": [], "match": "heading"}
    ids = _exact(cited, pieces)
    if ids:
        return {"sentences": ids, "match": "exact"}
    ids = _fuzzy(cited, " ".join(pieces))
    if ids:
        return {"sentences": ids, "match": "fuzzy"}
    for bid, other in page.items():
        ids = _exact(other, pieces)
        if ids:
            return {"sentences": ids, "match": "other-block", "found_in": bid}
    return {"sentences": [], "match": "not-found"}


def resolve_output(handbook_id, data):
    """Add "sentences" and "match" to every {"block", "quote"} object in `data` (changed in place);
    return the count of each kind of match."""
    counts = Counter()

    def walk(x):
        if isinstance(x, dict):
            if isinstance(x.get("block"), str) and isinstance(x.get("quote"), str):
                x.update(resolve(handbook_id, x["block"], x["quote"]))
                counts[x["match"]] += 1
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(data)
    return dict(counts)
