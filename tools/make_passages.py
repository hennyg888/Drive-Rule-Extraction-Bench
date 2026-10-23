"""Turn a passage selection into the passage file extraction reads.

Usage:
    python tools/make_passages.py --segments analysis/segments/ca.jsonl --handbook-dir handbooks/ca \
        --selection analysis/passing-rules/ca/inputs/selection.json --out analysis/passing-rules/ca/inputs/passing-passages.json

The selection is a list of {"seg": segment id, "part": intro|general|specific|excluded, "why": ...}
(see prompts/select-passages.md). Passages are numbered p1, p2, … in handbook order and carry the
fields of the Ontario passage file plus `href` (a link into the offline handbook) and `seg`.
The California and Texas passage files were made before the handbooks moved into handbooks/
(23 Oct 2026), with --handbook-dir ca_drivers_handbook and tx_drivers_handbook; their `href`
values keep those names, and tools/build_rules_page.py maps them to handbooks/ca and handbooks/tx.
"""
import argparse
import json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--segments", required=True)
    ap.add_argument("--handbook-dir", required=True)
    ap.add_argument("--selection", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    segs = [json.loads(l) for l in open(a.segments, encoding="utf-8")]
    index = {s["id"]: i for i, s in enumerate(segs)}
    selection = json.load(open(a.selection, encoding="utf-8"))
    missing = [x["seg"] for x in selection if x["seg"] not in index]
    if missing:
        raise SystemExit(f"unknown segment ids: {missing}")
    seen, out = set(), []
    for x in sorted(selection, key=lambda x: index[x["seg"]]):
        if x["seg"] in seen:
            continue
        seen.add(x["seg"])
        s = segs[index[x["seg"]]]
        p = {"m": f"p{len(out) + 1}", "part": x["part"], "page": s["page_title"], "sec": s["sec"],
             "kind": s["kind"], "text": s["text"],
             "href": f"{a.handbook_dir}/{s['page']}.html" + (f"#{s['anchor']}" if s.get("anchor") else ""),
             "seg": s["id"], "why": x.get("why")}
        if s["kind"] == "figure":
            p["src"], p["cap"] = s["src"], s["cap"]
        if s.get("pdf_page"):
            p["pdf_page"] = s["pdf_page"]
        out.append(p)
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    parts = {}
    for p in out:
        parts[p["part"]] = parts.get(p["part"], 0) + 1
    print(f"{len(out)} passages -> {a.out}: " + ", ".join(f"{k} {v}" for k, v in sorted(parts.items())))


if __name__ == "__main__":
    main()
