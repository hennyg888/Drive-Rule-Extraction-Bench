"""Build corpus/ from handbooks/: the handbook pages as clean HTML with an id on every block and sentence.

    python build_corpus.py              # build all three handbooks into corpus/<id>/
    python build_corpus.py --check      # rebuild in memory and list the pages whose files would change
    python build_corpus.py --only mto   # one handbook
    python build_corpus.py --stats      # the handbook statistics table in the README

The corpus files are committed, so their ids stay fixed: run --check before committing a change
that could move them. Manual decisions go in corpus/<id>/manual.yaml; the build writes the places
to check by hand to corpus/<id>/screening.md.
Code: drbench/corpus.py, drbench/sentences.py, drbench/screening.py, drbench/stats.py.
"""
import argparse
import json
import sys

from drbench import corpus, handbooks, stats


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="write nothing; list pages whose corpus file would change")
    ap.add_argument("--only", choices=sorted(handbooks.HANDBOOKS))
    ap.add_argument("--stats", action="store_true", help="print the handbook statistics (Markdown) instead")
    ap.add_argument("--stats-json", help="with --stats: also write the numbers to this file")
    a = ap.parse_args()
    ids = [a.only] if a.only else sorted(handbooks.HANDBOOKS)
    if a.stats:
        md, data = stats.report(ids)
        print(md)
        if a.stats_json:
            json.dump(data, open(a.stats_json, "w"), indent=1)
        return
    changed = [corpus.build(h, write=not a.check, check=a.check) for h in ids]
    if a.check and any(changed):
        sys.exit(1)


if __name__ == "__main__":
    main()
