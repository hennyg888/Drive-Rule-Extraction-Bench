"""Run a model on handbook pages with a prompt, and save everything in runs/.

    python tools/run_extraction.py --model anthropic/claude-opus-5-5 --handbook mto --pages 10
    python tools/run_extraction.py --model anthropic/claude-haiku-5-5 --handbook ca --dry-run   # count tokens, call nothing
    python tools/run_extraction.py --model openrouter/gemini-3.8-flash --handbook tx --set max_tokens=16000
    python tools/run_extraction.py --model anthropic/claude-opus-5-5 --handbook mto --save-to extraction_outputs

The chosen pages (the whole handbook by default) go in one request, with their images and the
table of contents. It can be run from any folder; runs/ and --save-to are relative to the
repository root.

--model     a preset in drbench/models/models.yaml (python tools/models.py lists them)
--prompt    a folder in prompts/ (default formal-rules): system.md, task.md, schema.json
--set       changes a model setting for this run: --set effort=low,
            --set extra_body.chat_template_kwargs.enable_thinking=false
--save-to   also copies the answer to <dir>/<model>/<handbook>_<YYYY_MM_DD>.json (_2, _3 ... when a
            file of that name exists), e.g. --save-to extraction_outputs, and the run's meta.json
            next to it as <handbook>_<YYYY_MM_DD>.meta.json (runs/ is not in git; this is the record
            of the model, its settings and the prompt version that made the answer). A preset with
            a `mode` (its thinking mode, e.g. thinking or no-thinking) saves to
            <dir>/<model>/<mode>/, so one model's modes are kept apart.
Each run writes runs/<time>-<preset>-<handbook>/: meta.json (settings, tokens, time, cost, citation
matches), a copy of the prompt, the request as text, the response, the answer as JSON, and
grounded.json (every cited block with its kind and sentence ids). See the README.
tools/extract.sh runs the draft gold-set extraction with these options set.
Code: drbench/run.py, drbench/models/, drbench/grounding.py.
"""
import argparse
import os
import shutil
import sys
import time

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the repository root, for drbench

from drbench import corpus, handbooks, messages, prompts
from drbench.handbooks import ROOT
from drbench.models import ModelError, credential_status, get_model, presets
from drbench.run import run


def parse_sets(items):
    """--set key=value pairs; values are read as YAML (false, 0.5, {"a": 1} ...)."""
    out = {}
    for item in items or []:
        if "=" not in item:
            raise SystemExit(f"--set wants key=value, not {item!r}")
        k, v = item.split("=", 1)
        out[k] = yaml.safe_load(v)
    return out


def dry_run(a, pages):
    model = get_model(a.model, **parse_sets(a.set))
    p = prompts.load(a.prompt)
    for m in messages.build(a.handbook, pages, task=p.task):
        line = f"pages {m['pages'][0]}..{m['pages'][-1]}: {messages.summary(m['content'])}"
        if hasattr(model, "count_tokens"):          # Claude: exact and free
            n = model.count_tokens(m["content"], p.system)
            line += f", {n:,} input tokens" + (f" (${n * model.price[0] / 1e6:.3f} input)" if model.price else "")
        print(line)


def save_answer(folder, out_dir, model_id, handbook_id, mode=None):
    """Copy a run's answer to <out_dir>/<model>[/<mode>]/<handbook>_<YYYY_MM_DD>.json, numbering on
    (_2, _3 ...) rather than overwriting, and its meta.json next to it as <...>.meta.json. Returns
    the answer's path."""
    answer = os.path.join(folder, "output.json")
    if not os.path.exists(answer):
        raise SystemExit(f"no JSON answer to save; see {os.path.relpath(folder, ROOT)} (error.txt or output.txt)")
    out = os.path.join(out_dir, model_id, mode or "")
    stem = f"{handbook_id}_{time.strftime('%Y_%m_%d')}"
    path, n = os.path.join(out, stem + ".json"), 2
    while os.path.exists(path):
        path, n = os.path.join(out, f"{stem}_{n}.json"), n + 1
    os.makedirs(out, exist_ok=True)
    shutil.copyfile(answer, path)
    shutil.copyfile(os.path.join(folder, "meta.json"), path[:-len(".json")] + ".meta.json")
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", help="a preset in drbench/models/models.yaml")
    ap.add_argument("--handbook", choices=sorted(handbooks.HANDBOOKS))
    ap.add_argument("--pages", help="page numbers or files: 10, 9-11, changing-positions (default: all)")
    ap.add_argument("--prompt", default=prompts.DEFAULT, help=f"a folder in prompts/ (default {prompts.DEFAULT})")
    # ap.add_argument("--per-page", action="store_true", help="one call per page")
    # ap.add_argument("--no-images", action="store_true")
    # ap.add_argument("--no-toc", action="store_true")
    ap.add_argument("--set", action="append", metavar="KEY=VALUE", help="change a model setting for this run")
    ap.add_argument("--label", help="added to the run folder name")
    ap.add_argument("--save-to", metavar="DIR", help="also copy the answer to DIR/<model>/<handbook>_<YYYY_MM_DD>.json")
    ap.add_argument("--dry-run", action="store_true", help="build the messages and count tokens; call no model")
    # ap.add_argument("--reground", metavar="RUN_DIR", help="resolve the citations of a finished run again")
    a = ap.parse_args()
    if not (a.model and a.handbook):
        ap.error("--model and --handbook are needed")
    if a.model not in presets():
        raise SystemExit(f"error: no preset {a.model!r} in drbench/models/models.yaml")
    status = credential_status(presets()[a.model])
    if not (status.startswith("ok") or status == "local"):
        raise SystemExit(f"error: {a.model} {status}: put it in .env at the repository root (or run `ant auth login`)")
    pages = corpus.parse_pages(a.pages, a.handbook)
    try:
        if a.dry_run:
            dry_run(a, pages)
            return
        folder = run(a.model, a.handbook, pages, prompt=a.prompt, overrides=parse_sets(a.set), label=a.label)
    except ModelError as e:
        raise SystemExit(f"error: {e}")
    if a.save_to:
        preset = presets()[a.model]
        path = save_answer(folder, os.path.join(ROOT, a.save_to), preset["model"], a.handbook, preset.get("mode"))
        print(f"-> {os.path.relpath(path, ROOT)}")


if __name__ == "__main__":
    main()
