"""The model layer without calling any API."""
import pytest

from drbench.models import ModelError, get_model, presets
from drbench.models.claude import to_blocks
from drbench.models.openai_compat import to_openai

PARTS = [{"type": "text", "text": "<p>hi</p><img src='a.png'>"},
         {"type": "image", "media_type": "image/png", "data": "QUJD", "src": "a.png"}]


def test_parts_to_each_api():
    assert to_blocks(PARTS)[1] == {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": "QUJD"}}
    assert to_openai(PARTS)[1] == {"type": "image_url", "image_url": {"url": "data:image/png;base64,QUJD"}}
    assert to_blocks(PARTS)[0] == to_openai(PARTS)[0] == {"type": "text", "text": PARTS[0]["text"]}


def test_every_preset_loads():
    for name in presets():
        model = get_model(name)
        assert model.model and model.provider in ("anthropic", "openai")


def test_overrides_and_dotted_keys():
    m = get_model("local/qwen3.8-27b-nothink", temperature=0.1, **{"extra_body.top_k": 20})
    assert m.params["temperature"] == 0.1
    assert m.params["extra_body"] == {"chat_template_kwargs": {"enable_thinking": False}, "top_k": 20}
    assert get_model("local/qwen3.8-27b-nothink").params["temperature"] == 0.7   # the preset is unchanged


def test_claude_request():
    kw = get_model("anthropic/claude-opus-5-5", effort="low").request(PARTS, system="sys", json_schema={"type": "object"})
    assert kw["model"] == "claude-opus-5-5" and kw["system"] == "sys"
    assert kw["output_config"] == {"effort": "low", "format": {"type": "json_schema", "schema": {"type": "object"}}}
    assert kw["thinking"]["type"] == "adaptive" and "fallbacks" not in kw   # fallbacks go with the beta call


def test_openai_request():
    kw = get_model("local/qwen3.8-27b-nothink").request(PARTS, system="sys", json_schema={"type": "object"})
    assert kw["messages"][0] == {"role": "system", "content": "sys"}
    assert kw["response_format"]["json_schema"]["schema"] == {"type": "object"}
    assert kw["extra_body"]["chat_template_kwargs"]["enable_thinking"] is False


def test_unknown_preset_and_text_only_model():
    with pytest.raises(ModelError):
        get_model("nope/nothing")
    m = get_model("local/qwen3.5-0.8b")
    m.vision = False
    with pytest.raises(ModelError):
        m.request(PARTS)
