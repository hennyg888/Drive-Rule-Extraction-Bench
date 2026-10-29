"""The drbench command. `drbench <command> --help` explains each command."""
import argparse
import json
import os
import sys

import yaml

from . import handbooks
from .handbooks import ROOT

HB = sorted(handbooks.HANDBOOKS)


def cmd_stats(a):
    from . import stats
    md, data = stats.report(tokenizer=a.tokenizer)
    print(md)
    if a.json:
        json.dump(data, open(a.json, "w"), indent=1)


def cmd_corpus(a):
    from . import corpus
    ids = [a.only] if a.only else HB
    changed = [corpus.build(h, write=a.action == "build", check=a.action == "check") for h in ids]
    if a.action == "check" and any(changed):
        sys.exit(1)


def cmd_messages(a):
    from . import corpus, messages
    pages = corpus.parse_pages(a.pages, a.handbook)
    msgs = messages.build(a.handbook, pages, images=not a.no_images, per_page=a.per_page, toc=not a.no_toc)
    out = a.out or os.path.join(ROOT, "build", "messages", a.handbook + ("-text" if a.no_images else "")
                                + (f"-p{a.pages}" if a.pages else ""))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    json.dump({"handbook": a.handbook, "pages": sorted(pages) if pages else "all", "images": not a.no_images,
               "messages": msgs}, open(out + ".json", "w", encoding="utf-8"), ensure_ascii=False)
    with open(out + ".md", "w", encoding="utf-8") as f:
        for m in msgs:
            f.write(f"<!-- message: pages {m['pages']} -->\n{messages.preview(m['content'])}\n")
    for m in msgs:
        print(f"pages {m['pages'][0]}..{m['pages'][-1]}: {messages.summary(m['content'])}")
    print(f"-> {out}.json, .md")


def cmd_models(a):
    from .models import credential_status, presets
    rows = [(name, p["provider"], p["model"], credential_status(p)) for name, p in presets().items()]
    w = [max(len(r[i]) for r in rows) for i in range(3)]
    for r in rows:
        print(f"{r[0]:<{w[0]}}  {r[1]:<{w[1]}}  {r[2]:<{w[2]}}  {r[3]}")


def cmd_serve(a):
    from .models import presets
    p = presets().get(a.preset)
    if not p or not p.get("serve"):
        raise SystemExit(f"{a.preset} has no serve command in configs/models.yaml")
    cmd = " ".join(p["serve"].split())
    print(cmd)
    if a.print:
        return
    env = dict(os.environ, PATH=os.path.join(os.path.expanduser(a.venv), "bin") + os.pathsep + os.environ["PATH"])
    os.execvpe("bash", ["bash", "-c", cmd], env)


def cmd_ping(a):
    from .models import get_model
    model = get_model(a.model, **parse_sets(a.set))
    r = model.complete("Reply with the single word: ready")
    print(f"{a.model}: {r.text.strip()!r} ({r.model}, {r.input_tokens} in / {r.output_tokens} out tokens, {r.seconds}s)")


def parse_sets(items):
    """--set key=value pairs; values are read as YAML (false, 0.5, {"a": 1} ...)."""
    out = {}
    for item in items or []:
        if "=" not in item:
            raise SystemExit(f"--set wants key=value, not {item!r}")
        k, v = item.split("=", 1)
        out[k] = yaml.safe_load(v)
    return out


def cmd_run(a):
    from . import corpus, messages
    from .models import get_model
    from .run import run
    pages = corpus.parse_pages(a.pages, a.handbook)
    if a.dry_run:
        model = get_model(a.model, **parse_sets(a.set))
        system = open(a.prompt, encoding="utf-8").read() if a.prompt else None
        for m in messages.build(a.handbook, pages, images=not a.no_images, per_page=a.per_page, toc=not a.no_toc):
            line = f"pages {m['pages'][0]}..{m['pages'][-1]}: {messages.summary(m['content'])}"
            if hasattr(model, "count_tokens"):
                n = model.count_tokens(m["content"], system)
                line += f", {n:,} input tokens" + (f" (${n * model.price[0] / 1e6:.3f} input)" if model.price else "")
            print(line)
        return
    run(a.model, a.handbook, pages, prompt=a.prompt, schema=a.schema, images=not a.no_images, toc=not a.no_toc,
        per_page=a.per_page, overrides=parse_sets(a.set), label=a.label)


def cmd_ground(a):
    from . import grounding
    from .run import reground
    if a.run:
        print(json.dumps(reground(a.run), indent=1))
    else:
        print(json.dumps(grounding.resolve(a.handbook, a.block, a.quote), ensure_ascii=False))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="drbench", description="Drive-Rule-Extraction-Bench: handbooks -> corpus -> "
                                 "model messages -> model runs -> grounded citations.")
    sub = ap.add_subparsers(dest="command", required=True)

    p = sub.add_parser("stats", help="text and image statistics of the handbooks (Markdown, for the README)")
    p.add_argument("--tokenizer", default="Qwen/Qwen3.8-27B-FP8")
    p.add_argument("--json", help="also write the numbers to this file")
    p.set_defaults(func=cmd_stats)

    p = sub.add_parser("corpus", help="build corpus/<id>/ from handbooks/<id>/, or check it is up to date")
    p.add_argument("action", choices=["build", "check"])
    p.add_argument("--only", choices=HB)
    p.set_defaults(func=cmd_corpus)

    page_help = "page numbers or files: 10, 9-11, changing-positions (default: all)"
    p = sub.add_parser("messages", help="write the user message(s) for some pages to build/messages/, to look at")
    p.add_argument("handbook", choices=HB)
    p.add_argument("--pages", help=page_help)
    p.add_argument("--no-images", action="store_true", help="text only: keep the <img> tags, send no images")
    p.add_argument("--per-page", action="store_true", help="one message per page instead of one for all")
    p.add_argument("--no-toc", action="store_true", help="leave out the table of contents")
    p.add_argument("--out", help="output path without extension")
    p.set_defaults(func=cmd_messages)

    p = sub.add_parser("models", help="list the model presets in configs/models.yaml and whether their key is set")
    p.set_defaults(func=cmd_models)

    p = sub.add_parser("serve", help="start the local vLLM server of a preset")
    p.add_argument("preset")
    p.add_argument("--print", action="store_true", help="only print the command")
    p.add_argument("--venv", default="~/qwen-trial/.venv", help="the virtual environment with vLLM")
    p.set_defaults(func=cmd_serve)

    p = sub.add_parser("ping", help="send a one-line message to a model, to check the key or server")
    p.add_argument("model")
    p.add_argument("--set", action="append", metavar="KEY=VALUE", help="override a param of the preset")
    p.set_defaults(func=cmd_ping)

    p = sub.add_parser("run", help="run a model on handbook pages and save everything in runs/")
    p.add_argument("--model", required=True, help="a preset name (drbench models)")
    p.add_argument("--handbook", required=True, choices=HB)
    p.add_argument("--pages", help=page_help)
    p.add_argument("--prompt", help="the system prompt, a Markdown file")
    p.add_argument("--schema", help="a JSON schema the answer must follow")
    p.add_argument("--no-images", action="store_true")
    p.add_argument("--no-toc", action="store_true")
    p.add_argument("--per-page", action="store_true", help="one call per page")
    p.add_argument("--set", action="append", metavar="KEY=VALUE", help="override a param of the preset, e.g. effort=low")
    p.add_argument("--label", help="added to the run folder name")
    p.add_argument("--dry-run", action="store_true", help="build the messages and count tokens; call no model")
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("ground", help="resolve citations: one block + quote, or all of a run (--run)")
    p.add_argument("--run", help="a run folder: resolve its output.json again")
    p.add_argument("--handbook", choices=HB)
    p.add_argument("--block")
    p.add_argument("--quote")
    p.set_defaults(func=cmd_ground)

    a = ap.parse_args(argv)
    if a.command == "ground" and not a.run and not (a.handbook and a.block and a.quote):
        ap.error("ground needs --run, or --handbook, --block and --quote")
    from .models import ModelError
    try:
        a.func(a)
    except ModelError as e:
        raise SystemExit(f"error: {e}")
