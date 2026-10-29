from drbench import corpus
from drbench.handbooks import HANDBOOKS


def test_corpus_is_up_to_date():
    """Rebuilding gives the committed corpus files byte for byte (so no id has moved)."""
    for hb in HANDBOOKS:
        assert corpus.build(hb, write=False, check=True, log=lambda *_: None) == []


def test_parse_pages():
    assert corpus.parse_pages("9-11,changing-positions", "mto") == {9, 10, 11}
    assert corpus.parse_pages("", "mto") is None
