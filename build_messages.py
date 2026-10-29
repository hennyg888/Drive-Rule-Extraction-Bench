"""Write out the exact request a model gets, to read it before running anything.

    python build_messages.py mto --pages 10                          # with the default prompt (extract-rules)
    python build_messages.py mto --pages 10 --prompt smoke-test
    python build_messages.py ca --per-page --no-images               # one message per page, text only

The request is:
    system   prompts/<prompt>/system.md
    user     the table of contents, the pages as HTML with every image right after its <img> tag,
             then prompts/<prompt>/task.md
Writes build/messages/<name>.md (the request as text, with [image: src] where each image goes) and
<name>.json (the same, with the images in base64).
Code: drbench/messages.py (the user message), drbench/prompts.py (the prompt folders).
"""
import argparse
import json
import os

from drbench import corpus, handbooks, messages, prompts
from drbench.handbooks import ROOT


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("handbook", choices=sorted(handbooks.HANDBOOKS))
    ap.add_argument("--pages", help="page numbers or files: 10, 9-11, changing-positions (default: all)")
    ap.add_argument("--prompt", default=prompts.DEFAULT, help=f"a folder in prompts/ (default {prompts.DEFAULT})")
    ap.add_argument("--no-images", action="store_true", help="text only: keep the <img> tags, send no images")
    ap.add_argument("--per-page", action="store_true", help="one message per page instead of one for all")
    ap.add_argument("--no-toc", action="store_true", help="leave out the table of contents")
    ap.add_argument("--out", help="output path without extension (default build/messages/<handbook>...)")
    a = ap.parse_args()
    p = prompts.load(a.prompt)
    pages = corpus.parse_pages(a.pages, a.handbook)
    msgs = messages.build(a.handbook, pages, images=not a.no_images, per_page=a.per_page, toc=not a.no_toc,
                          task=p.task)
    out = a.out or os.path.join(ROOT, "build", "messages", a.handbook + ("-text" if a.no_images else "")
                                + (f"-p{a.pages}" if a.pages else ""))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    json.dump({"handbook": a.handbook, "pages": sorted(pages) if pages else "all", "images": not a.no_images,
               "prompt": p.name, "system": p.system, "schema": p.schema, "messages": msgs},
              open(out + ".json", "w", encoding="utf-8"), ensure_ascii=False)
    with open(out + ".md", "w", encoding="utf-8") as f:
        f.write(f"<!-- system: prompts/{p.name}/system.md -->\n{p.system}\n\n")
        for m in msgs:
            f.write(f"<!-- user message: pages {m['pages']} -->\n{messages.preview(m['content'])}\n\n")
    for m in msgs:
        print(f"pages {m['pages'][0]}..{m['pages'][-1]}: {messages.summary(m['content'])}")
    print(f"-> {os.path.relpath(out, ROOT)}.md, .json")


if __name__ == "__main__":
    main()
