"""Calling a model. Every model is a preset in models.yaml (repository root); code asks for it by name:

    from drbench.models import get_model
    model = get_model("anthropic/claude-opus-5-5", effort="low")    # keyword arguments override params
    response = model.complete(content, system=prompt, json_schema=schema)

Switching model is switching the preset name. To add a model, add a preset (see the comments at
the top of models.yaml); a new kind of API needs a new ChatModel subclass in this folder
and a branch in _provider.

Keys are read from the environment, and from .env at the repository root (KEY=value lines; the
file is ignored by git).
"""
import os

import yaml

from ..handbooks import ROOT
from .base import ChatModel, ModelError, ModelResponse

PRESETS_FILE = os.path.join(ROOT, "models.yaml")
ENV_FILE = os.path.join(ROOT, ".env")
SETTINGS = ("base_url", "api_key_env", "timeout", "max_retries")


def _provider(name):
    if name == "anthropic":
        from .claude import ClaudeModel
        return ClaudeModel
    if name == "openai":
        from .openai_compat import OpenAICompatibleModel
        return OpenAICompatibleModel
    raise ModelError(f"unknown provider {name!r} (anthropic or openai)")


def load_env(path=ENV_FILE):
    """Read KEY=value lines of .env into the environment; variables already set win."""
    if not os.path.exists(path):
        return
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def presets():
    return yaml.safe_load(open(PRESETS_FILE, encoding="utf-8")) or {}


def set_param(params, key, value):
    """Set a param; a dotted key goes into nested dicts: extra_body.chat_template_kwargs.enable_thinking."""
    *path, last = key.split(".")
    d = params
    for k in path:
        d = d.setdefault(k, {})
    d[last] = value


def get_model(name, **overrides):
    """The model of a preset, with params overridden by keyword arguments (dotted keys allowed)."""
    load_env()
    table = presets()
    if name not in table:
        raise ModelError(f"no preset {name!r} in models.yaml; `python models.py` lists them")
    p = table[name]
    params = yaml.safe_load(yaml.safe_dump(p.get("params") or {}))   # a deep copy
    for k, v in overrides.items():
        set_param(params, k, v)
    cls = _provider(p["provider"])
    return cls(name, p["model"], params=params, vision=p.get("vision", True), price=p.get("price"),
               **{k: p[k] for k in SETTINGS if k in p})


def credential_status(preset):
    """Whether the key a preset needs is there: "ok", "local" or what is missing."""
    load_env()
    if preset["provider"] == "anthropic":
        if os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"):
            return "ok"
        creds = os.path.join(os.path.expanduser("~"), ".config", "anthropic", "credentials")
        return "ok (ant login)" if os.path.isdir(creds) and os.listdir(creds) else "needs ANTHROPIC_API_KEY"
    env = preset.get("api_key_env")
    if not env:
        return "local"
    return "ok" if os.environ.get(env) else f"needs {env}"


__all__ = ["ChatModel", "ModelError", "ModelResponse", "get_model", "presets", "credential_status", "load_env"]
