"""Run a model on handbook pages with a prompt, and save everything in runs/.

    python run_extraction.py --model anthropic/claude-opus-5-5 --handbook mto --pages 10
    python run_extraction.py --model local/qwen3.8-27b --handbook mto --per-page
    python run_extraction.py --model anthropic/claude-haiku-5-5 --handbook ca --dry-run   # count tokens, call nothing
    python run_extraction.py --model openrouter/gemini-3.8-flash --handbook tx --set max_tokens=16000
    python run_extraction.py --reground runs/<run>                                        # resolve citations again

--model     a preset in models.yaml (python models.py lists them)
--prompt    a folder in prompts/ (default extract-rules): system.md, task.md, schema.json
--set       changes a model setting for this run: --set effort=low,
            --set extra_body.chat_template_kwargs.enable_thinking=false
Each run writes runs/<time>-<preset>-<handbook>/: meta.json (settings, tokens, time, cost, citation
matches), a copy of the prompt, the request as text, the response, the answer as JSON, and
grounded.json (every cited quote with its sentence ids). See the README.
Code: drbench/run.py, drbench/models/, drbench/grounding.py.
"""
import argparse
import json

import yaml

from drbench import corpus, handbooks, messages, prompts
from drbench.models import ModelError, get_model
from drbench.run import reground, run


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
    for m in messages.build(a.handbook, pages, images=not a.no_images, per_page=a.per_page, toc=not a.no_toc,
                            task=p.task):
        line = f"pages {m['pages'][0]}..{m['pages'][-1]}: {messages.summary(m['content'])}"
        if hasattr(model, "count_tokens"):          # Claude: exact and free
            n = model.count_tokens(m["content"], p.system)
            line += f", {n:,} input tokens" + (f" (${n * model.price[0] / 1e6:.3f} input)" if model.price else "")
        print(line)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", help="a preset in models.yaml")
    ap.add_argument("--handbook", choices=sorted(handbooks.HANDBOOKS))
    ap.add_argument("--pages", help="page numbers or files: 10, 9-11, changing-positions (default: all)")
    ap.add_argument("--prompt", default=prompts.DEFAULT, help=f"a folder in prompts/ (default {prompts.DEFAULT})")
    ap.add_argument("--per-page", action="store_true", help="one call per page")
    ap.add_argument("--no-images", action="store_true")
    ap.add_argument("--no-toc", action="store_true")
    ap.add_argument("--set", action="append", metavar="KEY=VALUE", help="change a model setting for this run")
    ap.add_argument("--label", help="added to the run folder name")
    ap.add_argument("--dry-run", action="store_true", help="build the messages and count tokens; call no model")
    ap.add_argument("--reground", metavar="RUN_DIR", help="resolve the citations of a finished run again")
    a = ap.parse_args()
    if a.reground:
        print(json.dumps(reground(a.reground), indent=1))
        return
    if not (a.model and a.handbook):
        ap.error("--model and --handbook are needed")
    pages = corpus.parse_pages(a.pages, a.handbook)
    try:
        if a.dry_run:
            dry_run(a, pages)
        else:
            run(a.model, a.handbook, pages, prompt=a.prompt, images=not a.no_images, toc=not a.no_toc,
                per_page=a.per_page, overrides=parse_sets(a.set), label=a.label)
    except ModelError as e:
        raise SystemExit(f"error: {e}")


if __name__ == "__main__":
    main()
