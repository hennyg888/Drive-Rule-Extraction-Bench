from drbench.sentences import split


def test_plain_sentences():
    assert split("Stop. Look both ways. Then go!") == ["Stop.", "Look both ways.", "Then go!"]


def test_abbreviations_and_initials_do_not_end_a_sentence():
    assert split("Drive in the U.S. carefully. See e.g. the signs.") == ["Drive in the U.S. carefully.", "See e.g. the signs."]
    assert split("Ask Freeman F. Martin. He knows.") == ["Ask Freeman F. Martin.", "He knows."]


def test_typed_list_number_and_closing_aside_stay():
    assert split("2. Right turn. Signal first.") == ["2. Right turn.", "Signal first."]
    assert split("Why do you signal before turning? (Chpt. 5)") == ["Why do you signal before turning? (Chpt. 5)"]


def test_quotes_and_digits_start_a_sentence():
    assert split('Signs say "Stop." "Yield" means give way.') == ['Signs say "Stop."', '"Yield" means give way.']
    assert split("Keep right. 2 lanes merge ahead.") == ["Keep right.", "2 lanes merge ahead."]
