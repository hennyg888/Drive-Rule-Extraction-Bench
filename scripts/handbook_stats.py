"""Text and image statistics of the offline handbooks (handbooks/<name>/), for the README.

Counts what is inside each page's <article class="content">, the handbook text a model is given:
text blocks (paragraphs, list items, table rows), sentences, words and tokens, and images with
their sizes and an estimate of the tokens they cost a vision-language model.

Usage:
    python scripts/handbook_stats.py                 # Markdown tables for all handbooks
    python scripts/handbook_stats.py --json out.json # also write the numbers as JSON

Tokens: counted with a Hugging Face tokenizer when `transformers` and the model files are available
(--tokenizer, default Qwen/Qwen3.8-27B-FP8, read from the local cache only); otherwise estimated as
1.3 tokens per word, and the tables say so.
Image tokens: estimated the way Qwen-VL models encode images, one token per 28 x 28 pixel patch after
rounding each side to a multiple of 28 (at least 4 tokens). Other models differ: Claude, for example,
uses about width x height / 750, which gives about 1.05 times as many.
"""
import argparse
import json
import math
import os
import re
import statistics

from bs4 import BeautifulSoup, Tag
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HANDBOOKS = [("mto", "Ontario (MTO)"), ("ca", "California (DMV)"), ("tx", "Texas (DPS)")]
GENERIC_ALT = re.compile(r"^(a |an )?(regulatory|warning|temporary condition|information) sign$|^image$|^$", re.I)
SENTENCE_END = re.compile(r"(?<=[.!?])[\"”’)]*\s+(?=[\"“(]?[A-Z0-9])")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def sentences(text):
    return [s for s in SENTENCE_END.split(text) if s.strip()]


def image_tokens(w, h, patch=28):
    return max(4, round(w / patch) * round(h / patch))


def load_tokenizer(name):
    try:
        from transformers import AutoTokenizer
        return AutoTokenizer.from_pretrained(name, local_files_only=True)
    except Exception:
        return None


def page_order(book):
    """Content pages in the order of the table of contents in index.html, index first."""
    found = {f[:-5] for f in os.listdir(book) if f.endswith(".html")}
    order = ["index"] if "index" in found else []
    soup = BeautifulSoup(open(os.path.join(book, "index.html"), encoding="utf-8"), "html.parser")
    for a in soup.select("nav a[href$='.html'], aside a[href$='.html']"):
        slug = a["href"].split("#")[0][:-5]
        if slug in found and slug not in order:
            order.append(slug)
    return order + sorted(found - set(order))


def page_stats(book, slug, tok):
    soup = BeautifulSoup(open(os.path.join(book, slug + ".html"), encoding="utf-8"), "html.parser")
    art = soup.find("article", class_="content")
    h1 = soup.find("h1")
    st = {"page": slug, "title": norm(h1.get_text()) if h1 else slug, "headings": 0, "blocks": [],
          "images": [], "text": ""}
    if art is None:
        return st
    texts = []
    for el in art.find_all(["h2", "h3", "h4", "p", "li", "tr", "img"]):
        if el.name in ("h2", "h3", "h4"):
            st["headings"] += 1
            texts.append(norm(el.get_text(" ")))
        elif el.name == "img":
            w, h = Image.open(os.path.join(book, el["src"])).size
            st["images"].append({"src": el["src"], "w": w, "h": h, "alt": norm(el.get("alt", ""))})
        elif el.name == "li" and el.find(["ul", "ol"]):
            # count the item's own text, not its nested list (those items are counted themselves)
            own = norm(" ".join(t for t in el.find_all(string=True, recursive=False)) + " " +
                       " ".join(c.get_text(" ") for c in el.children
                                if isinstance(c, Tag) and c.name not in ("ul", "ol")))
            if own:
                st["blocks"].append(own)
                texts.append(own)
        elif el.name == "tr":
            cells = [norm(c.get_text(" ")) for c in el.find_all(["td", "th"])]
            if el.find("td") and any(cells):
                st["blocks"].append(" | ".join(c for c in cells if c))
                texts.append(st["blocks"][-1])
        elif el.name == "p" and not el.find_parent(["li", "td", "th"]):
            t = norm(el.get_text(" "))
            if t:
                st["blocks"].append(t)
                texts.append(t)
        elif el.name == "li":
            t = norm(el.get_text(" "))
            if t:
                st["blocks"].append(t)
                texts.append(t)
    st["text"] = "\n".join(texts)
    st["words"] = len(st["text"].split())
    st["tokens"] = len(tok.encode(st["text"], add_special_tokens=False)) if tok else round(st["words"] * 1.3)
    return st


def handbook_stats(name, tok):
    book = os.path.join(ROOT, "handbooks", name)
    pages = [page_stats(book, s, tok) for s in page_order(book)]
    blocks = [b for p in pages for b in p["blocks"]]
    images = [i for p in pages for i in p["images"]]
    words = [len(b.split()) for b in blocks]
    sents = [len(sentences(b)) for b in blocks]
    img_tok = sum(image_tokens(i["w"], i["h"]) for i in images)
    txt_tok = sum(p["tokens"] for p in pages)
    q = sorted(words)
    return {
        "pages": len(pages), "headings": sum(p["headings"] for p in pages),
        "blocks": len(blocks), "sentences": sum(sents), "words": sum(p["words"] for p in pages),
        "text_tokens": txt_tok,
        "block_words_median": statistics.median(words), "block_words_p90": q[int(0.9 * (len(q) - 1))],
        "block_words_max": max(words), "blocks_over_3_sentences": sum(n > 3 for n in sents),
        "blocks_over_80_words": sum(w > 80 for w in words),
        "images": len(images), "image_files": len({i["src"] for i in images}),
        "image_megapixels": round(sum(i["w"] * i["h"] for i in images) / 1e6, 1),
        "image_median_size": "{} x {}".format(round(statistics.median(i["w"] for i in images)),
                                              round(statistics.median(i["h"] for i in images))) if images else "-",
        "image_tokens": img_tok,
        "images_generic_alt": sum(bool(GENERIC_ALT.match(i["alt"])) for i in images),
        "text_share_of_tokens": round(txt_tok / (txt_tok + img_tok), 3) if txt_tok + img_tok else None,
        "per_page": [{"page": p["page"], "title": p["title"], "words": p.get("words", 0),
                      "tokens": p.get("tokens", 0), "images": len(p["images"]),
                      "image_tokens": sum(image_tokens(i["w"], i["h"]) for i in p["images"])} for p in pages],
    }


def fmt(n):
    if isinstance(n, float) and not n.is_integer():
        return f"{n:,.1f}"
    return f"{int(n):,}" if isinstance(n, (int, float)) else str(n)


def markdown(stats, tokenizer_note):
    names = [n for n, _ in HANDBOOKS]
    rows = [
        ("Pages", "pages"), ("Headings", "headings"),
        ("Text blocks (paragraphs, list items, table rows)", "blocks"), ("Sentences", "sentences"),
        ("Words", "words"), ("Text tokens", "text_tokens"),
        ("Words per block: median / 90th percentile / max", None),
        ("Blocks with more than 3 sentences", "blocks_over_3_sentences"),
        ("Blocks with more than 80 words", "blocks_over_80_words"),
        ("Images (distinct files)", None), ("Image median size (px)", "image_median_size"),
        ("Image pixels (millions)", "image_megapixels"), ("Image tokens (estimate)", "image_tokens"),
        ("Images whose alt text says nothing specific", "images_generic_alt"),
        ("Text share of all tokens", None),
    ]
    out = ["| | " + " | ".join(label for _, label in HANDBOOKS) + " |", "|---|" + "---:|" * len(names)]
    for label, key in rows:
        if key:
            cells = [fmt(stats[n][key]) for n in names]
        elif label.startswith("Words per block"):
            cells = [f"{fmt(stats[n]['block_words_median'])} / {stats[n]['block_words_p90']} / {stats[n]['block_words_max']}" for n in names]
        elif label.startswith("Images ("):
            cells = [f"{stats[n]['images']} ({stats[n]['image_files']})" for n in names]
        else:
            cells = [f"{stats[n]['text_share_of_tokens'] * 100:.0f}%" for n in names]
        out.append(f"| {label} | " + " | ".join(cells) + " |")
    out.append("")
    out.append(tokenizer_note)
    for n, label in HANDBOOKS:
        out += ["", f"<details><summary>{label}: per page</summary>", "",
                "| Page | Words | Text tokens | Images | Image tokens |", "|---|---:|---:|---:|---:|"]
        for p in stats[n]["per_page"]:
            out.append(f"| `{p['page']}` | {p['words']:,} | {p['tokens']:,} | {p['images']} | {p['image_tokens']:,} |")
        out += ["", "</details>"]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokenizer", default="Qwen/Qwen3.8-27B-FP8")
    ap.add_argument("--json")
    a = ap.parse_args()
    tok = load_tokenizer(a.tokenizer)
    stats = {n: handbook_stats(n, tok) for n, _ in HANDBOOKS}
    note = (f"Text tokens counted with the {a.tokenizer} tokenizer." if tok else
            "Text tokens estimated as 1.3 per word (no tokenizer available).") + (
        " Image tokens estimated as one per 28 x 28 pixel patch, as Qwen-VL models encode images;"
        " other models differ (Claude: about width x height / 750).")
    print(markdown(stats, note))
    if a.json:
        json.dump(stats, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
