from drbench import corpus, messages
from drbench.handbooks import HANDBOOKS


def test_corpus_is_up_to_date():
    """Rebuilding gives the committed corpus files byte for byte (so no id has moved)."""
    for hb in HANDBOOKS:
        assert corpus.build(hb, write=False, check=True, log=lambda *_: None) == []


def test_parse_pages():
    assert corpus.parse_pages("9-11,changing-positions", "mto") == {9, 10, 11}
    assert corpus.parse_pages("", "mto") is None


def test_message_has_toc_then_page_with_images_in_place():
    [m] = messages.build("mto", {10})
    text = messages.preview(m["content"])
    assert text.index("<nav>") < text.index('<article data-page="10">')
    assert 'id="10.7"' in text and '<span id="10.7.1">' not in text      # block ids kept, sentence spans removed
    for i, part in enumerate(m["content"]):
        if part["type"] == "image":                                       # each image follows its <img> tag
            assert m["content"][i - 1]["text"].rstrip().endswith(">") and part["src"] in m["content"][i - 1]["text"]
