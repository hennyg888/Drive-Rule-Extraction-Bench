"""One run: build the message from the corpus, call a model, save everything, resolve the citations.

A run writes runs/<time>-<preset>-<handbook>[-<label>]/:
    meta.json       what was run (preset, params, handbook, pages, prompt and its sha256, git commit)
                    and what happened (tokens, seconds, estimated cost, stop reason, citation matches)
    system.md       the system prompt sent
    request.md      the user message as text, with [image: src] where each image was
    response.json   the whole API response
    output.txt      the answer as returned
    reasoning.txt   the model's reasoning, when the API returns it
    output.json     the answer parsed as JSON, when it is JSON
    grounded.json   output.json with "sentences" and "match" added to every {"block", "quote"}
    error.txt       instead of the above, when the call failed
With per_page, each page gets its own subfolder p<page>/ with these files (meta.json stays at the top).
"""
import hashlib
import json
import os
import re
import subprocess
import time

from . import grounding, messages
from .handbooks import ROOT
from .models import ModelError, get_model

RUNS = os.path.join(ROOT, "runs")


def git_commit():
    try:
        head = subprocess.run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
        dirty = subprocess.run(["git", "-C", ROOT, "status", "--porcelain", "--untracked-files=no"],
                               capture_output=True, text=True).stdout.strip()
        return head + ("+changes" if dirty else "")
    except OSError:
        return ""


def parse_json(text):
    """The answer as JSON: the whole text, or the text inside a ```json fence, or from the first { to
    the last }. None if none of these parse."""
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    for candidate in (text, m.group(1) if m else None, text[text.find("{"):text.rfind("}") + 1]):
        if candidate:
            try:
                return json.loads(candidate)
            except ValueError:
                pass
    return None


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def call(model, handbook_id, message, system, schema, folder, log=print):
    """Send one message and save what comes back in `folder`. Returns the record for meta.json."""
    os.makedirs(folder, exist_ok=True)
    write(os.path.join(folder, "request.md"), messages.preview(message["content"]))
    rec = {"pages": message["pages"]}
    try:
        r = model.complete(message["content"], system=system, json_schema=schema)
    except ModelError as e:
        write(os.path.join(folder, "error.txt"), str(e) + "\n")
        log(f"  pages {message['pages']}: failed: {e}")
        return {**rec, "error": str(e)}
    json.dump(r.raw, open(os.path.join(folder, "response.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    write(os.path.join(folder, "output.txt"), r.text)
    if r.reasoning:
        write(os.path.join(folder, "reasoning.txt"), r.reasoning)
    rec.update({"model": r.model, "stop_reason": r.stop_reason, "input_tokens": r.input_tokens,
                "output_tokens": r.output_tokens, "reasoning_tokens": r.reasoning_tokens, "seconds": r.seconds, "cost_usd": model.cost(r),
                "request_id": r.request_id})
    data = parse_json(r.text)
    rec["json"] = data is not None
    if data is not None:
        json.dump(data, open(os.path.join(folder, "output.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        rec["citations"] = grounding.resolve_output(handbook_id, data)
        json.dump(data, open(os.path.join(folder, "grounded.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    log(f"  pages {message['pages']}: {r.input_tokens:,} in / {r.output_tokens:,} out tokens, {r.seconds}s, "
        f"stop: {r.stop_reason}" + (f", ${rec['cost_usd']}" if rec["cost_usd"] is not None else "")
        + (f", citations: {rec['citations']}" if rec.get("citations") else "") + ("" if rec["json"] else ", answer is not JSON"))
    return rec


def run(model_name, handbook_id, pages=None, prompt=None, schema=None, images=True, toc=True, per_page=False,
        overrides=None, label=None, out_root=RUNS, log=print):
    """Run a model on handbook pages (page numbers; None for all). `prompt` and `schema` are file
    paths (the system prompt; a JSON schema the answer must follow). Returns the run folder."""
    model = get_model(model_name, **(overrides or {}))
    system = open(prompt, encoding="utf-8").read() if prompt else None
    json_schema = json.load(open(schema, encoding="utf-8")) if schema else None
    msgs = messages.build(handbook_id, pages, images=images, per_page=per_page, toc=toc)
    name = f"{time.strftime('%Y%m%d-%H%M%S')}-{model_name.replace('/', '_')}-{handbook_id}" + (f"-{label}" if label else "")
    folder = os.path.join(out_root, name)
    os.makedirs(folder)
    meta = {"run": name, "started": time.strftime("%Y-%m-%d %H:%M:%S"), "git": git_commit(), **model.describe(),
            "handbook": handbook_id, "pages": sorted(pages) if pages else "all", "images": images, "toc": toc,
            "per_page": per_page,
            "prompt": os.path.relpath(prompt, ROOT) if prompt else None,
            "prompt_sha256": hashlib.sha256(system.encode()).hexdigest() if system else None,
            "schema": os.path.relpath(schema, ROOT) if schema else None}
    if system:
        write(os.path.join(folder, "system.md"), system)
    log(f"{name}: {len(msgs)} call(s)")
    calls = []
    for m in msgs:
        sub = folder if len(msgs) == 1 else os.path.join(folder, f"p{m['pages'][0]:02d}")
        calls.append(call(model, handbook_id, m, system, json_schema, sub, log))
        meta["calls"] = calls
        json.dump(meta, open(os.path.join(folder, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ok = [c for c in calls if "error" not in c]
    meta["totals"] = {"calls": len(calls), "failed": len(calls) - len(ok),
                      "input_tokens": sum(c["input_tokens"] for c in ok),
                      "output_tokens": sum(c["output_tokens"] for c in ok),
                      "reasoning_tokens": sum(c["reasoning_tokens"] for c in ok),
                      "seconds": round(sum(c["seconds"] for c in ok), 1),
                      "cost_usd": round(sum(c["cost_usd"] for c in ok), 4) if ok and model.price else None}
    json.dump(meta, open(os.path.join(folder, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    log(f"-> {os.path.relpath(folder, ROOT)}  totals: {meta['totals']}")
    return folder


def reground(folder, handbook_id=None):
    """Resolve the citations of a finished run again (after the corpus or grounding changed)."""
    meta = json.load(open(os.path.join(folder, "meta.json"), encoding="utf-8"))
    handbook_id = handbook_id or meta["handbook"]
    out = {}
    for root, _, files in os.walk(folder):
        if "output.json" in files:
            data = json.load(open(os.path.join(root, "output.json"), encoding="utf-8"))
            out[os.path.relpath(root, folder)] = grounding.resolve_output(handbook_id, data)
            json.dump(data, open(os.path.join(root, "grounded.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return out
