"""Score a T2 run (extracted statements) against the reference, as described in qwen-trial-handoff.md.

Pairing: each reference statement is paired with the model statement that cites at least one of
the same passages and has the closest wording; pairs are taken best-first, one to one.
Scores measure agreement with the reference (Claude's output), not correctness.

Usage:
    python qwen/score_t2.py runs/t2/mto/<model>/<mode>/seed1/statements.json [--handbook mto] [--json out.json]
"""
import argparse
import difflib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from check_statements import check, load_passages  # noqa: E402

REFERENCE = {"mto": "analysis/passing-rules/passing-rules.v1.json",
             "ca": "analysis/passing-rules/ca/passing-rules.v1.json",
             "tx": "analysis/passing-rules/tx/passing-rules.v1.json"}
PASSAGES = {"mto": ["analysis/passing-rules/inputs/passing-passages.json", "analysis/passing-rules/inputs/census-sentences.json"],
            "ca": ["analysis/passing-rules/ca/inputs/passing-passages.json"],
            "tx": ["analysis/passing-rules/tx/inputs/passing-passages.json"]}
# Ontario subsets from qwen-trial-handoff.md and qwen/README.md
SUBSETS_MTO = {
    "heading condition": "3.1.7a 3.2.1d 3.2.2a 3.3.1b 3.3.2a 3.3.2b 3.3.3a 3.3.3b 3.4.4a 3.4.4c 3.4.5d 3.4.7a 3.4.8a 3.5.2a 3.6.1d",
    "neighbour condition": "2.2b 3.1.4a",
    "heading force": "3.1.7a 3.2.1d 3.6.1c",
    "cross-passage link": "2.2b 3.3.1b 3.4.12e",
    "duty apart from penalty": "3.4.4b 3.4.12b 3.4.13a 3.4.13b",
    "sources on two pages": "3.1.1a 3.4.13a 3.4.13b 3.6.1a 3.6.3a 3.6.3b",
    "seen in the spec": "1b 3.1.1a 3.1.3a 3.2.3a 3.2.3b 3.2.4a 3.4.3a 3.4.5a 3.4.6c 3.5.2c",
}
SUBSETS = {
    "mto": SUBSETS_MTO,
    # The DO NOT PASS and SLOWER TRAFFIC KEEP RIGHT signs exist only inside Sign-Sample-1.png;
    # a model given captions alone cannot write these two.
    "ca": {"image only": "3.1.7a 3.6.1b"},
    "tx": {},
}
MODAL_RE =r"\b(MUST NOT|SHOULD NOT|MUST|SHOULD|MAY)\b"


def sources_of(st):
    ids = {s["id"] for s in st.get("sources", [])}
    for step in st.get("steps", []) or []:
        ids |= set(step.get("sources", []))
    return ids


def words(t):
    t = re.sub(r"\[\?([^\]]*)\]", r"\1", t or "")
    return re.sub(r"\s+", " ", t).strip().lower()


def similarity(a, b):
    return difflib.SequenceMatcher(None, words(a["text"]), words(b["text"])).ratio()


def modals(st):
    text = re.sub(r"^EXCEPTION TO \S+:\s*", "", st.get("text", ""))
    return re.findall(MODAL_RE, re.sub(r"\"[^\"]*\"", " ", text))


def basis(st):
    ff = st.get("force_from") or ""
    return ff.split(" (")[0].split(" ")[0] if ff else None


def inline_spans(st):
    full = " ".join([st.get("text", "")] + [s.get("text", "") for s in st.get("steps", []) or []])
    return {words(s) for s in re.findall(r"\[\?([^\]]+)\]", full)}


def jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 0.0


def text_words(st):
    text = re.sub(r"^EXCEPTION TO \S+:\s*", "", st.get("text", ""))
    return set(re.findall(r"[a-z0-9']+", text.lower()))


def fixed_score(r, m):
    """The pairing score of the reference session's scorer (provenance/scripts/score_extraction.py):
    Jaccard of source ids + 0.5 for the same type + Jaccard of the statement texts' words."""
    return (jaccard(sources_of(r), sources_of(m)) + (0.5 if r.get("type") == m.get("type") else 0.0)
            + jaccard(text_words(r), text_words(m)))


PAIRING = "wording"  # "wording": closest wording (difflib); "fixed": the reference session's score


def pair(ref, model):
    score = fixed_score if PAIRING == "fixed" else similarity
    cands = []
    for i, r in enumerate(ref):
        rs = sources_of(r)
        for j, m in enumerate(model):
            if rs & sources_of(m):
                cands.append((score(r, m), i, j))
    cands.sort(reverse=True)
    used_r, used_m, pairs = set(), set(), {}
    for score, i, j in cands:
        if i not in used_r and j not in used_m:
            used_r.add(i), used_m.add(j)
            pairs[i] = (j, score)
    return pairs


def rate(n, d):
    return round(n / d, 3) if d else None


def score(ref, model, passages, excluded):
    pairs = pair(ref, model)
    out = {"reference": len(ref), "model": len(model), "matched": len(pairs),
           "recall": rate(len(pairs), len(ref)), "precision": rate(len(pairs), len(model))}
    agree = {"type": 0, "force": 0, "modal": 0, "modal_set": 0, "force_basis": 0}
    tp = fp = fn = 0
    code_ok = code_n = 0
    sims = []
    for i, (j, s) in pairs.items():
        r, m = ref[i], model[j]
        sims.append(s)
        agree["type"] += r["type"] == m.get("type")
        agree["force"] += r.get("force") == m.get("force")
        agree["modal"] += modals(r) == modals(m)
        agree["modal_set"] += set(modals(r)) == set(modals(m))
        agree["force_basis"] += basis(r) == basis(m)
        rs, ms = inline_spans(r), inline_spans(m)
        tp += len(rs & ms)
        fp += len(ms - rs)
        fn += len(rs - ms)
        rcodes = {words(f["span"]): f["code"] for f in r.get("flags", []) if f["code"] != "X"}
        mcodes = {words(f.get("span")): f.get("code") for f in m.get("flags", [])}
        for span in rs & ms:
            if span in rcodes and span in mcodes:
                code_n += 1
                code_ok += rcodes[span] == mcodes[span]
    for k in agree:
        out[f"{k}_agreement"] = rate(agree[k], len(pairs))
    out["text_similarity_mean"] = round(sum(sims) / len(sims), 3) if sims else None
    p, rcl = rate(tp, tp + fp), rate(tp, tp + fn)
    out["vague_span_f1"] = round(2 * p * rcl / (p + rcl), 3) if p and rcl else 0.0
    out["vague_code_accuracy"] = rate(code_ok, code_n)
    out["statements_from_excluded_passages"] = sum(bool(sources_of(m) & excluded) for m in model)
    # Content coverage at passage level: of the passages the reference draws on, how many the model cites.
    ref_cited = set().union(*(sources_of(r) for r in ref)) if ref else set()
    model_cited = set().union(*(sources_of(m) for m in model)) if model else set()
    out["passage_recall"] = rate(len(ref_cited & model_cited), len(ref_cited))
    out["_passages_missed"] = sorted(ref_cited - model_cited)
    # Content coverage at sentence level: each sentence the reference quotes should appear in some
    # model quote from the same passage.
    def sentences(q):
        return [s for s in (words(x) for x in re.split(r"(?<=[.!?:])\s+", q or "")) if len(s) > 12]
    model_quotes = {}
    for m in model:
        for s in m.get("sources", []):
            model_quotes.setdefault(s.get("id"), []).append(words(s.get("quote")))
    ref_sents = {(s["id"], t) for r in ref for s in r.get("sources", []) for t in sentences(s.get("quote"))}
    covered = {(pid, t) for pid, t in ref_sents if any(t in q or q in t for q in model_quotes.get(pid, []) if len(q) > 12)}
    out["sentence_recall"] = rate(len(covered), len(ref_sents))
    out["_sentences_missed"] = sorted(f"{pid}: {t[:70]}" for pid, t in ref_sents - covered)
    problems = check(model, passages)
    counts = {}
    for c, _, _ in problems:
        counts[c] = counts.get(c, 0) + 1
    out["check_problems"] = counts
    out["_pairs"] = {ref[i]["id"]: (model[j]["id"], round(s, 3)) for i, (j, s) in pairs.items()}
    out["_unmatched_reference"] = [ref[i]["id"] for i in range(len(ref)) if i not in pairs]
    out["_unmatched_model"] = [model[j]["id"] for j in range(len(model)) if j not in {j for j, _ in pairs.values()}]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("statements")
    ap.add_argument("--handbook", default="mto", choices=sorted(REFERENCE))
    ap.add_argument("--json")
    ap.add_argument("--only-seen", action="store_true",
                    help="score only reference statements whose sources were all in the run's batches (for --batch runs)")
    ap.add_argument("--pairing", choices=["wording", "fixed"], default="wording",
                    help="wording: closest wording among statements sharing a source; fixed: the reference "
                         "session's score (source Jaccard + 0.5 same type + word Jaccard)")
    a = ap.parse_args()
    global PAIRING
    PAIRING = a.pairing
    ref = json.load(open(os.path.join(ROOT, REFERENCE[a.handbook]), encoding="utf-8"))
    data = json.load(open(a.statements, encoding="utf-8"))
    model = data["statements"] if isinstance(data, dict) else data
    if a.only_seen:
        run_dir = os.path.dirname(os.path.abspath(a.statements))
        seen = set()
        for f in os.listdir(run_dir):
            if re.match(r"\d\d-.*\.json$", f):
                seen |= set(json.load(open(os.path.join(run_dir, f)))["passages"])
        ref = [r for r in ref if sources_of(r) <= seen]
    pfiles = [os.path.join(ROOT, p) for p in PASSAGES[a.handbook]]
    passages = load_passages(pfiles)
    excluded = {pid for pid, p in passages.items() if p.get("part") == "excluded"}
    result = {"all": score(ref, model, passages, excluded)}
    pairs = result["all"]["_pairs"]
    scored = {r["id"] for r in ref}
    for name, ids in SUBSETS[a.handbook].items():
        ids = [i for i in ids.split() if i in scored]
        if not ids:
            continue
        result[name] = {"n": len(ids), "matched": sum(i in pairs for i in ids),
                        "unmatched": [i for i in ids if i not in pairs]}
    for k, v in result["all"].items():
        if not k.startswith("_"):
            print(f"{k:34} {v}")
    for name, v in result.items():
        if name != "all":
            print(f"subset {name:27} {v['matched']}/{v['n']} matched" + (f"  missing {' '.join(v['unmatched'])}" if v["unmatched"] else ""))
    print("unmatched reference:", " ".join(result["all"]["_unmatched_reference"]) or "-")
    print("passages the reference cites but the model does not:", " ".join(result["all"]["_passages_missed"]) or "-")
    print("sentences the reference quotes but the model does not:")
    for s in result["all"]["_sentences_missed"]:
        print("   ", s)
    if a.json:
        json.dump(result, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
