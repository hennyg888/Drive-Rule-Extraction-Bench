from drbench.grounding import page_blocks, resolve, resolve_output

# Ontario page 10, "Changing positions". Block 10.7 has three sentences.
BLOCK = "10.7"


def sentences():
    return page_blocks("mto", 10)[BLOCK]["sentences"]


def test_exact_quote_of_one_sentence():
    sid, text = sentences()[1]
    assert resolve("mto", BLOCK, text) == {"sentences": [sid], "match": "exact"}


def test_quote_over_two_sentences_with_different_case_and_quotes():
    (s1, t1), (s2, t2) = sentences()[:2]
    quote = (t1 + "  " + t2).upper().replace("'", "’")
    assert resolve("mto", BLOCK, quote) == {"sentences": [s1, s2], "match": "exact"}


def test_quote_with_ellipsis():
    (s1, t1), _, (s3, t3) = sentences()[:3]
    quote = t1[:30] + " ... " + t3[-25:]
    assert resolve("mto", BLOCK, quote)["sentences"] == [s1, s3]


def test_fuzzy_quote():
    sid, text = sentences()[0]
    words = text.split()
    words[3] = "xyz"                      # one word changed
    assert resolve("mto", BLOCK, " ".join(words)) == {"sentences": [sid], "match": "fuzzy"}


def test_quote_in_another_block():
    sid, text = sentences()[0]
    r = resolve("mto", "10.1", text)
    assert r["match"] == "other-block" and r["found_in"] == BLOCK and r["sentences"] == [sid]


def test_missing():
    assert resolve("mto", "10.99999", "anything")["match"] == "no-block"
    assert resolve("mto", "999.1", "anything")["match"] == "no-block"
    assert resolve("mto", BLOCK, "a quote that is on no page of the handbook")["match"] == "not-found"


def test_resolve_output_finds_citations_anywhere():
    sid, text = sentences()[0]
    data = {"rules": [{"rule": "r", "evidence": [{"block": BLOCK, "quote": text}]}], "other": {"block": 1}}
    assert resolve_output("mto", data) == {"exact": 1}
    assert data["rules"][0]["evidence"][0]["sentences"] == [sid]
