"""The model presets in models.yaml: list them, check one, or start a local one.

    python models.py                                   # list the presets and whether each one's key is set
    python models.py ping anthropic/claude-haiku-5-5   # a one-line call, to check a key or a server
    python models.py serve local/qwen3.8-27b           # start that preset's local vLLM server
    python models.py serve local/qwen3.8-27b --print   # only print the command

Keys go in .env (ANTHROPIC_API_KEY=..., OPENROUTER_API_KEY=...). The GPUs are shared: stop a local
server (Ctrl-C) when you are done.
Code: drbench/models/ (claude.py for the Anthropic API, openai_compat.py for vLLM and OpenRouter).
"""
import argparse
import os

from drbench.models import ModelError, credential_status, get_model, presets


def list_presets():
    rows = [(name, p["provider"], p["model"], credential_status(p)) for name, p in presets().items()]
    w = [max(len(r[i]) for r in rows) for i in range(3)]
    for r in rows:
        print(f"{r[0]:<{w[0]}}  {r[1]:<{w[1]}}  {r[2]:<{w[2]}}  {r[3]}")


def ping(name):
    r = get_model(name).complete("Reply with the single word: ready")
    print(f"{name}: {r.text.strip()!r} ({r.model}, {r.input_tokens} in / {r.output_tokens} out tokens, {r.seconds}s)")


def serve(name, venv, only_print):
    p = presets().get(name)
    if not p or not p.get("serve"):
        raise SystemExit(f"{name} has no serve command in models.yaml")
    cmd = " ".join(p["serve"].split())
    print(cmd)
    if only_print:
        return
    env = dict(os.environ, PATH=os.path.join(os.path.expanduser(venv), "bin") + os.pathsep + os.environ["PATH"])
    os.execvpe("bash", ["bash", "-c", cmd], env)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("action", nargs="?", choices=["list", "ping", "serve"], default="list")
    ap.add_argument("preset", nargs="?")
    ap.add_argument("--print", action="store_true", help="serve: only print the command")
    ap.add_argument("--venv", default="~/qwen-trial/.venv", help="serve: the virtual environment with vLLM")
    a = ap.parse_args()
    if a.action != "list" and not a.preset:
        ap.error(f"{a.action} needs a preset name")
    try:
        if a.action == "list":
            list_presets()
        elif a.action == "ping":
            ping(a.preset)
        else:
            serve(a.preset, a.venv, a.print)
    except ModelError as e:
        raise SystemExit(f"error: {e}")


if __name__ == "__main__":
    main()
