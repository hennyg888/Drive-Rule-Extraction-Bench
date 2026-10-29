"""Side-by-side comparison of a T2 run with the reference, as Markdown, for error analysis.

Each reference statement is shown next to the model statement paired with it (same pairing as
score_t2.py), with the differences that matter marked: type, force, modal, force basis, clauses,
vague spans. Then the reference statements the model missed and the model statements with no
reference partner.

Usage:
    python qwen/compare_t2.py runs/t2/mto/<model>/<mode>/seed1/statements.json [--handbook mto] [--out report.md]
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_t2 import PASSAGES, REFERENCE, ROOT, basis, inline_spans, modals, pair, sources_of  # noqa: E402

CLAUSES = ["WHEN", "WHILE", "ONLY IF", "UNLESS", "UNTIL", "BECAUSE", "IF VIOLATED"]


def clauses(st):
    text = " ".join([st.get("text", "")] + [s.get("text", "") for s in st.get("steps", []) or []])
    return [c for c in CLAUSES if re.search(rf"\b{c}\b", re.sub(r"\"[^\"]*\"", " ", text))]


def show(st):
    lines = [f"`{st['id']}` {st.get('type')} · {st.get('force')} · {st.get('force_from')}", "", f"> {st.get('text')}"]
    for step in st.get("steps", []) or []:
        lines.append(f"> {step.get('n')}. {step.get('text')}")
    flags = ", ".join(f"{f.get('code')} “{f.get('span')}”" for f in st.get("flags", []))
    lines.append("")
    lines.append(f"sources {', '.join(sorted(sources_of(st)))}" + (f" · flags {flags}" if flags else ""))
    return "\n".join(lines)


def differences(r, m):
    out = []
    if r["type"] != m.get("type"):
        out.append(f"type {r['type']} → {m.get('type')}")
    if r.get("force") != m.get("force"):
        out.append(f"force {r.get('force')} → {m.get('force')}")
    if modals(r) != modals(m):
        out.append(f"modal {' '.join(modals(r)) or '-'} → {' '.join(modals(m)) or '-'}")
    if basis(r) != basis(m):
        out.append(f"basis {basis(r)} → {basis(m)}")
    rc, mc = clauses(r), clauses(m)
    if set(rc) - set(mc):
        out.append("missing clause " + ", ".join(c for c in rc if c not in mc))
    if set(mc) - set(rc):
        out.append("extra clause " + ", ".join(c for c in mc if c not in rc))
    rs, ms = inline_spans(r), inline_spans(m)
    if rs - ms:
        out.append("vague not marked: " + ", ".join(sorted(rs - ms)))
    if ms - rs:
        out.append("vague extra: " + ", ".join(sorted(ms - rs)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("statements")
    ap.add_argument("--handbook", default="mto", choices=sorted(REFERENCE))
    ap.add_argument("--only-seen", action="store_true",
                    help="compare only reference statements whose sources were all in the run's batches")
    ap.add_argument("--out")
    a = ap.parse_args()
    ref = json.load(open(os.path.join(ROOT, REFERENCE[a.handbook]), encoding="utf-8"))
    data = json.load(open(a.statements, encoding="utf-8"))
    model = data["statements"] if isinstance(data, dict) else data
    if a.only_seen:
        # the passages the run actually saw, from its batch files
        seen = set()
        run_dir = os.path.dirname(os.path.abspath(a.statements))
        for f in os.listdir(run_dir):
            if re.match(r"\d\d-.*\.json$", f):
                seen |= set(json.load(open(os.path.join(run_dir, f)))["passages"])
        ref = [r for r in ref if sources_of(r) <= seen]
    pairs = pair(ref, model)
    lines = [f"# T2 comparison: {os.path.relpath(a.statements, ROOT)}", "",
             f"Reference {len(ref)} · model {len(model)} · paired {len(pairs)}", ""]
    n_diff = 0
    lines += ["## Paired statements", ""]
    for i, r in enumerate(ref):
        if i not in pairs:
            continue
        j, sim = pairs[i]
        diff = differences(r, model[j])
        n_diff += bool(diff)
        lines += [f"### {r['id']} ↔ {model[j]['id']} (wording similarity {sim:.2f})", "",
                  ("**Differences:** " + "; ".join(diff)) if diff else "**No structural differences.**", "",
                  "Claude:", "", show(r), "", "Model:", "", show(model[j]), ""]
    missed = [r for i, r in enumerate(ref) if i not in pairs]
    extra = [m for j, m in enumerate(model) if j not in {j for j, _ in pairs.values()}]
    lines += [f"## Reference statements with no model partner ({len(missed)})", ""]
    for r in missed:
        lines += [show(r), ""]
    lines += [f"## Model statements with no reference partner ({len(extra)})", ""]
    for m in extra:
        lines += [show(m), ""]
    lines.insert(4, f"Paired statements with at least one difference: {n_diff} of {len(pairs)}")
    text = "\n".join(lines)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text)
        print(f"wrote {a.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
