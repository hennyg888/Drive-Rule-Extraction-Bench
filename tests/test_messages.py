import pytest

from drbench import messages, prompts


def test_message_is_toc_then_pages_then_task():
    task = prompts.load(topic="overtaking").task
    [m] = messages.build("mto", {10}, task=task)
    text = messages.preview(m["content"])
    assert text.index("<nav>") < text.index('<article data-page="10">') < text.index(task)
    assert m["content"][-1]["text"].strip() == task
    assert 'id="10.7"' in text and '<span id="10.7.1">' not in text      # block ids kept, sentence spans removed
    assert 'id="10.12"' in text and 'id="10.12-c"' in text              # figure and caption ids kept
    for i, part in enumerate(m["content"]):
        if part["type"] == "image":                                       # each image follows its <img> tag
            assert m["content"][i - 1]["text"].rstrip().endswith(">") and part["src"] in m["content"][i - 1]["text"]


def test_every_prompt_loads():
    assert prompts.DEFAULT == "formal-rules"
    for name, kw in (("formal-rules", {"topic": "overtaking"}), ("no-image-rules", {"topic": "overtaking"}),
                     ("no-handbook-rules", {"topic": "overtaking", "region": "mto"}), ("smoke-test", {})):
        p = prompts.load(name, **kw)
        assert p.system and p.task and p.schema["type"] == "object" and len(p.sha256) == 64
        assert "{{" not in p.task


def test_topic_and_region_fill_the_last_lines():
    for topic in prompts.TOPICS:
        for region in prompts.REGIONS:
            task = prompts.load("no-handbook-rules", topic=topic, region=region).task
            assert task.endswith("Topic: " + prompts.TOPICS[topic]["topic"] + " only.\n"
                                 + "Region: " + prompts.REGIONS[region])
        assert prompts.load(topic=topic).task.endswith(f"Topic: extract formal rules about {prompts.TOPICS[topic]['topic']} only.")


def test_topic_and_region_are_checked():
    with pytest.raises(SystemExit):
        prompts.load()                                          # formal-rules needs a topic
    with pytest.raises(SystemExit):
        prompts.load(topic="overtaking", region="mto")          # and takes no region
    with pytest.raises(SystemExit):
        prompts.load("no-handbook-rules", topic="overtaking")   # closed book needs a region
    with pytest.raises(SystemExit):
        prompts.load("smoke-test", topic="overtaking")          # no {{topic}} to fill


def test_no_image_prompt_removes_every_figure():
    p = prompts.load("no-image-rules", topic="overtaking")
    assert not p.figures and prompts.load(topic="overtaking").figures
    [m] = messages.build("mto", {10}, task=p.task, figures=p.figures)
    text = messages.preview(m["content"])
    assert all(part["type"] == "text" for part in m["content"])
    assert "<figure" not in text and "<img" not in text and "<figcaption" not in text
    assert 'id="10.12"' not in text and 'id="10.12-c"' not in text and 'id="10.7"' in text


def test_closed_book_sends_the_task_alone():
    p = prompts.load("no-handbook-rules", topic="parking", region="ca")
    assert p.closed_book
    [m] = messages.build("ca", None, task=p.task, closed_book=True)
    assert m["pages"] == [] and m["content"] == [{"type": "text", "text": p.task}]
