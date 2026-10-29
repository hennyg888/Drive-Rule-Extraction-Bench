"""Text and image statistics of the offline handbooks (handbooks/<id>/), for the README.

Counts what is inside each page's <article class="content">, the handbook text a model is given:
text blocks (paragraphs, list items, table rows), sentences, words and tokens, and images with
their sizes and an estimate of the tokens they cost a vision-language model.

Tokens: counted with a Hugging Face tokenizer when `transformers` and the model files are available
(default Qwen/Qwen3.8-27B-FP8, read from the local cache only); otherwise estimated as 1.3 tokens
per word, and the tables say so.
Image tokens: estimated the way Qwen-VL models encode images, one token per 28 x 28 pixel patch after
rounding each side to a multiple of 28 (at least 4 tokens). Other models differ: Claude, for example,
uses about width x height / 750, which gives about 1.05 times as many.

Sentences here use a simpler split than the corpus (sentences.py); the README table was made with it.
"""
import os
import re
import statistics

from bs4 import Tag
from PIL import Image

from . import handbooks
from .handbooks import norm

DEFAULT_TOKENIZER = "Qwen/Qwen3.8-27B-FP8"
SENTENCE_END = re.compile(r"(?<=[.!?])[\"”’)]*\s+(?=[\"“(]?[A-Z0-9])")


def sentences(text):
    return [s for s in SENTENCE_END.split(text) if s.strip()]


def image_tokens(w, h, patch=28):
    return max(4, round(w / patch) * round(h / patch))


def load_tokenizer(name=DEFAULT_TOKENIZER):
    try:
        from transformers import AutoTokenizer
        return AutoTokenizer.from_pretrained(name, local_files_only=True)
    except Exception:
        return None


def page_stats(hb, slug, tok):
    title, art = handbooks.read_page(hb, slug)
    st = {"page": slug, "title": title, "headings": 0, "blocks": [], "images": [], "text": ""}
    texts = []
    for el in art.find_all(["h2", "h3", "h4", "p", "li", "tr", "img"]):
        if el.name in ("h2", "h3", "h4"):
            st["headings"] += 1
            texts.append(norm(el.get_text(" ")))
        elif el.name == "img":
            w, h = Image.open(os.path.join(hb.folder, el["src"])).size
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


def handbook_stats(handbook_id, tok):
    hb = handbooks.get(handbook_id)
    pages = [page_stats(hb, s, tok) for s in handbooks.page_order(hb)]
    blocks = [b for p in pages for b in p["blocks"]]
    images = [i for p in pages for i in p["images"]]
    words = [len(b.split()) for b in blocks]
    sents = [len(sentences(b)) for b in blocks]
    q = sorted(words)
    return {
        "pages": len(pages), "headings": sum(p["headings"] for p in pages),
        "blocks": len(blocks), "sentences": sum(sents), "words": sum(p["words"] for p in pages),
        "text_tokens": sum(p["tokens"] for p in pages),
        "block_words_median": statistics.median(words), "block_words_p90": q[int(0.9 * (len(q) - 1))],
        "block_words_max": max(words), "blocks_over_3_sentences": sum(n > 3 for n in sents),
        "blocks_over_80_words": sum(w > 80 for w in words),
        "images": len(images), "image_files": len({i["src"] for i in images}),
        "image_megapixels": round(sum(i["w"] * i["h"] for i in images) / 1e6, 1),
        "image_median_size": "{} x {}".format(round(statistics.median(i["w"] for i in images)),
                                              round(statistics.median(i["h"] for i in images))) if images else "-",
        "image_tokens": sum(image_tokens(i["w"], i["h"]) for i in images),
        "per_page": [{"page": p["page"], "title": p["title"], "words": p.get("words", 0),
                      "tokens": p.get("tokens", 0), "images": len(p["images"]),
                      "image_tokens": sum(image_tokens(i["w"], i["h"]) for i in p["images"])} for p in pages],
    }


def fmt(n):
    if isinstance(n, float) and not n.is_integer():
        return f"{n:,.1f}"
    return f"{int(n):,}" if isinstance(n, (int, float)) else str(n)


def markdown(stats, tokenizer_note):
    names = list(stats)
    labels = [handbooks.get(n).label for n in names]
    rows = [
        ("Pages", "pages"), ("Headings", "headings"),
        ("Text blocks (paragraphs, list items, table rows)", "blocks"), ("Sentences", "sentences"),
        ("Words", "words"), ("Text tokens", "text_tokens"),
        ("Words per block: median / 90th percentile / max", None),
        ("Blocks with more than 3 sentences", "blocks_over_3_sentences"),
        ("Blocks with more than 80 words", "blocks_over_80_words"),
        ("Images (distinct files)", None), ("Image median size (px)", "image_median_size"),
        ("Image pixels (millions)", "image_megapixels"), ("Image tokens (estimate)", "image_tokens"),
    ]
    out = ["| | " + " | ".join(labels) + " |", "|---|" + "---:|" * len(names)]
    for label, key in rows:
        if key:
            cells = [fmt(stats[n][key]) for n in names]
        elif label.startswith("Words per block"):
            cells = [f"{fmt(stats[n]['block_words_median'])} / {stats[n]['block_words_p90']} / {stats[n]['block_words_max']}" for n in names]
        else:  # Images (distinct files)
            cells = [f"{stats[n]['images']} ({stats[n]['image_files']})" for n in names]
        out.append(f"| {label} | " + " | ".join(cells) + " |")
    out.append("")
    out.append(tokenizer_note)
    for n, label in zip(names, labels):
        out += ["", f"<details><summary>{label}: per page</summary>", "",
                "| Page | Words | Text tokens | Images | Image tokens |", "|---|---:|---:|---:|---:|"]
        for p in stats[n]["per_page"]:
            out.append(f"| `{p['page']}` | {p['words']:,} | {p['tokens']:,} | {p['images']} | {p['image_tokens']:,} |")
        out += ["", "</details>"]
    return "\n".join(out)


def report(handbook_ids=tuple(handbooks.HANDBOOKS), tokenizer=DEFAULT_TOKENIZER):
    """(markdown, stats) for the README."""
    tok = load_tokenizer(tokenizer)
    stats = {n: handbook_stats(n, tok) for n in handbook_ids}
    note = (f"Text tokens counted with the {tokenizer} tokenizer." if tok else
            "Text tokens estimated as 1.3 tokens per word (no tokenizer available).") + (
        " Image tokens estimated as one per 28 x 28 pixel patch, as Qwen-VL models encode images;"
        " other models differ (Claude: about width x height / 750).")
    return markdown(stats, note), stats
