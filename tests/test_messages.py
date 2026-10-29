from drbench import messages, prompts


def test_message_is_toc_then_pages_then_task():
    task = prompts.load("extract-rules").task
    [m] = messages.build("mto", {10}, task=task)
    text = messages.preview(m["content"])
    assert text.index("<nav>") < text.index('<article data-page="10">') < text.index(task)
    assert m["content"][-1]["text"].strip() == task
    assert 'id="10.7"' in text and '<span id="10.7.1">' not in text      # block ids kept, sentence spans removed
    for i, part in enumerate(m["content"]):
        if part["type"] == "image":                                       # each image follows its <img> tag
            assert m["content"][i - 1]["text"].rstrip().endswith(">") and part["src"] in m["content"][i - 1]["text"]


def test_every_prompt_loads():
    for name in ("extract-rules", "smoke-test"):
        p = prompts.load(name)
        assert p.system and p.task and p.schema["type"] == "object" and len(p.sha256) == 64
