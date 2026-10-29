"""The offline handbooks in handbooks/<id>/: which there are, their page order, and their pages.

Every handbook folder has the same layout (made by scrapers/): one HTML file per page with the
handbook text inside <article class="content">, a table of contents in index.html, and images/.
"""
import os
import re
from dataclasses import dataclass

from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@dataclass(frozen=True)
class Handbook:
    id: str      # short id used in paths and commands: mto, ca, tx
    name: str    # full name, used in messages and reports
    label: str   # short label for tables

    @property
    def folder(self):
        return os.path.join(ROOT, "handbooks", self.id)

    @property
    def corpus_folder(self):
        return os.path.join(ROOT, "corpus", self.id)


HANDBOOKS = {
    "mto": Handbook("mto", "Official MTO Driver's Handbook (Ontario)", "Ontario (MTO)"),
    "ca": Handbook("ca", "California Driver's Handbook (DMV, DL 600)", "California (DMV)"),
    "tx": Handbook("tx", "Texas Driver Handbook (DPS, DL-7)", "Texas (DPS)"),
}


def get(handbook_id):
    try:
        return HANDBOOKS[handbook_id]
    except KeyError:
        raise SystemExit(f"unknown handbook {handbook_id!r}; choose from {', '.join(HANDBOOKS)}")


def norm(s):
    """Collapse whitespace."""
    return re.sub(r"\s+", " ", s or "").strip()


def page_order(hb):
    """Page files (without .html) in table-of-contents order, index first; pages not in the
    table of contents follow in alphabetical order."""
    found = {f[:-5] for f in os.listdir(hb.folder) if f.endswith(".html")}
    order = ["index"] if "index" in found else []
    soup = BeautifulSoup(open(os.path.join(hb.folder, "index.html"), encoding="utf-8"), "html.parser")
    for a in soup.select("nav a[href$='.html'], aside a[href$='.html']"):
        slug = a["href"].split("#")[0][:-5]
        if slug in found and slug not in order:
            order.append(slug)
    return order + sorted(found - set(order))


def read_page(hb, slug):
    """(title, article) of one page: the <h1> text and the <article class="content"> element
    (an empty <article> if the page has none)."""
    soup = BeautifulSoup(open(os.path.join(hb.folder, slug + ".html"), encoding="utf-8"), "html.parser")
    h1 = soup.find("h1")
    art = soup.find("article", class_="content")
    if art is None:
        art = BeautifulSoup("<article></article>", "html.parser").article
    return (norm(h1.get_text(" ")) if h1 else slug), art
