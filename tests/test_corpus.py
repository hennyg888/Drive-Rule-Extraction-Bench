import re

from drbench import corpus
from drbench.grounding import cite
from drbench.handbooks import HANDBOOKS


def test_corpus_is_up_to_date():
    """Rebuilding gives the committed corpus files byte for byte (so no id has moved)."""
    for hb in HANDBOOKS:
        assert corpus.build(hb, write=False, check=True, log=lambda *_: None) == []


def test_parse_pages():
    assert corpus.parse_pages("9-11,changing-positions", "mto") == {9, 10, 11}
    assert corpus.parse_pages("", "mto") is None


def test_every_image_is_a_figure_of_its_own():
    """One image per figure, no figure inside another, and ids unique on every page."""
    for hb in HANDBOOKS:
        for meta in corpus.load_pages(hb):
            art = corpus.page_soup(hb, meta).find("article")
            figures = art.find_all("figure")
            assert len(figures) == len(art.find_all("img")) == meta["images"]
            for fig in figures:
                assert len(fig.find_all("img")) == 1 and fig.find_parent("figure") is None
            ids = [b["id"] for b in corpus.blocks_of(art)]
            assert len(ids) == len(set(ids))


def test_figure_and_caption_ids():
    """A caption is its figure's id + "-c"; a figure inside a text block is that block's id + "-f<n>"."""
    for hb in HANDBOOKS:
        for meta in corpus.load_pages(hb):
            art = corpus.page_soup(hb, meta).find("article")
            for cap in art.find_all("figcaption"):
                assert cap["id"] == cap.find_parent("figure")["id"] + "-c"
            for fig in art.find_all("figure"):
                block = fig.find_parent(corpus.BLOCK_TAGS)
                if block is None:
                    assert re.fullmatch(rf"{meta['page']}\.\d+", fig["id"])
                else:
                    n = block.find_all("figure").index(fig) + 1
                    assert fig["id"] == f"{block['id']}-f{n}"


def test_cite_by_block_id():
    assert cite("mto", "10.22") == {"kind": "text", "sentences": ["10.22.1", "10.22.2", "10.22.3"]}
    assert cite("mto", "21.7") == {"kind": "figure", "sentences": []}
    assert cite("mto", "21.7-c") == {"kind": "caption", "sentences": ["21.7-c.1"]}
    assert cite("tx", "6.35-f1")["kind"] == "figure"
    assert cite("mto", "10.13")["kind"] == "heading"
    for missing in ("10.99999", "999.1", "21.7-f1", "nonsense"):
        assert cite("mto", missing) == {"kind": "no-block", "sentences": []}
