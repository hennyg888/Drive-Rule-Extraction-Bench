"""Stage 1 of the goldset check pipeline: format checks (see goldset_check_pipeline_plan.md).

Mechanical checks only, no LLM:
  1. valid JSON that matches the prompt's schema.json
  2. statement is exactly the fields filled into the grammar
  3. id = topic-group-number; one topic; group codes of 2-5 letters; ids unique;
     groups contiguous; numbers 01, 02, ... in order within each group
  4. force allows the modal
  5. every rule has evidence; every cited id (rules and vocab) exists in the corpus;
     no duplicate ids in an evidence list
  6. every vague term appears word for word in its statement
  7. every capitalized term (apart from keywords and modals) has a vocab entry;
     every vocab entry is used; no duplicate vocab terms
  8. no vocab term is written in lowercase in a statement, apart from the allowed lowercase forms
     (--allow-lowercase, default: pass, the verb, as in the extraction prompt's example; plurals
     of an allowed form are allowed too)

Usage:
  python error_check_pipelines/goldset/check_format.py <rules.json> [--handbook mto]
         [--schema prompts/formal-rules/schema.json] [--allow-lowercase pass ...] [-o report.txt]

Prints a short report of the errors found. Exit code 1 if there are any, 0 if none.
"""
import argparse
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

FORCE_MODALS = {
    "REQUIREMENT": {"MUST", "MUST NOT"},
    "INSTRUCTION": {"MUST", "MUST NOT"},
    "ADVICE": {"SHOULD", "SHOULD NOT"},
    "PERMISSION": {"MAY", "MAY ONLY"},
}
KEYWORDS = {"WHEN", "AND", "OR", "UNLESS", "MUST", "NOT", "SHOULD", "MAY", "ONLY"}
ALLOW_LOWERCASE = ["pass"]  # the verb "pass": the extraction prompt's example writes "the PASSER MAY pass"
CAPS_WORD = r"\b[A-Z][A-Z'\-]*[A-Z]\b"  # 2+ letters, all caps
CAPS_PHRASE = re.compile(CAPS_WORD + r"(?: " + CAPS_WORD + r")*")


def corpus_ids(handbook):
    """Block, figure and caption ids in the corpus (sentence <span> ids are not citable blocks)."""
    ids = set()
    for path in glob.glob(os.path.join(ROOT, "corpus", handbook, "*.html")):
        html = open(path, encoding="utf-8").read()
        ids |= set(re.findall(r'<(?!span\b)[a-zA-Z0-9]+\b[^>]*\bid="([^"]+)"', html))
    return ids


def term_pattern(term):
    """A vocab term as it may appear in rule text: as is, plural (S/ES), or possessive."""
    return re.compile(r"(?<![A-Za-z])" + re.escape(term) + r"(?:S|ES)?(?![A-Za-z])")


def check(data, schema, ids, allow_lowercase=ALLOW_LOWERCASE):
    """Returns {check name: [problem, ...]} for all eight checks, in order."""
    out = {name: [] for name in (
        "1. Schema", "2. Statement matches fields", "3. Ids and numbering", "4. Force and modal",
        "5. Evidence", "6. Vague terms", "7. Vocabulary", "8. Lowercase vocab terms")}

    # 1. schema
    try:
        import jsonschema
        for e in sorted(jsonschema.Draft7Validator(schema).iter_errors(data), key=lambda e: list(e.path)):
            where = "/".join(str(p) for p in e.path) or "(top level)"
            out["1. Schema"].append(f"{where}: {e.message}")
    except ImportError:
        out["1. Schema"].append("jsonschema is not installed; schema not checked (pip install jsonschema)")

    rules = [r for r in data.get("rules", []) if isinstance(r, dict)]
    vocab = [v for v in data.get("vocabulary", []) if isinstance(v, dict)]
    g = lambda r, k: r.get(k, "") if isinstance(r.get(k, ""), str) else ""

    # 2. statement
    for r in rules:
        exp = f"WHEN {g(r, 'when')}, the {g(r, 'actor')} {g(r, 'modal')} {g(r, 'action')}"
        if g(r, "unless"):
            exp += f", UNLESS {g(r, 'unless')}"
        exp += "."
        if exp != g(r, "statement"):
            out["2. Statement matches fields"].append(
                f"{r.get('id', '?')}\n      expected: {exp}\n      actual:   {g(r, 'statement')}")

    # 3. ids and numbering
    p = out["3. Ids and numbering"]
    topics = Counter(g(r, "topic") for r in rules)
    if len(topics) > 1:
        p.append("more than one topic: " + ", ".join(f"{t} ({n} rules)" for t, n in topics.items()))
    for rid, n in Counter(g(r, "id") for r in rules).items():
        if n > 1:
            p.append(f"{rid}: id used {n} times")
    order, nums = [], defaultdict(list)
    for r in rules:
        rid, grp, num = g(r, "id"), g(r, "group"), g(r, "number")
        if rid != f"{g(r, 'topic')}-{grp}-{num}":
            p.append(f"{rid}: id is not topic-group-number ({g(r, 'topic')}-{grp}-{num})")
        if not re.fullmatch(r"[A-Z]{2,5}", grp):
            p.append(f"{rid}: group code '{grp}' is not 2-5 capital letters")
        if not order or order[-1] != grp:
            order.append(grp)
        nums[grp].append(num)
    for grp, n in Counter(order).items():
        if n > 1:
            p.append(f"group {grp} is split into {n} separate runs (groups must be contiguous)")
    for grp, got in nums.items():
        want = [f"{i:02d}" for i in range(1, len(got) + 1)]
        if got != want:
            p.append(f"group {grp}: numbers {', '.join(got)} (expected {', '.join(want)})")

    # 4. force and modal
    for r in rules:
        f, m = g(r, "force"), g(r, "modal")
        if f in FORCE_MODALS and m not in FORCE_MODALS[f]:
            out["4. Force and modal"].append(
                f"{r.get('id', '?')}: force {f} does not allow modal {m} (allowed: {', '.join(sorted(FORCE_MODALS[f]))})")

    # 5. evidence
    p = out["5. Evidence"]
    items = [(r.get("id", "?"), r.get("evidence", [])) for r in rules] + \
            [(f"vocab {v.get('term', '?')}", v.get("evidence", [])) for v in vocab]
    for r in rules:
        if not r.get("evidence"):
            p.append(f"{r.get('id', '?')}: no evidence")
    for who, ev in items:
        ev = ev if isinstance(ev, list) else []
        missing = [e for e in ev if e not in ids]
        if missing:
            p.append(f"{who}: cited id(s) not in corpus: {', '.join(map(str, missing))}")
        dup = [e for e, n in Counter(ev).items() if n > 1]
        if dup:
            p.append(f"{who}: cited more than once: {', '.join(map(str, dup))}")

    # 6. vague terms
    for r in rules:
        for vt in r.get("vague_terms", []) or []:
            t = vt.get("term", "") if isinstance(vt, dict) else ""
            if t not in g(r, "statement"):
                out["6. Vague terms"].append(f"{r.get('id', '?')}: '{t}' is not in the statement")

    # 7. vocabulary
    p = out["7. Vocabulary"]
    terms = [g(v, "term") for v in vocab]
    for t, n in Counter(terms).items():
        if n > 1:
            p.append(f"'{t}' is defined {n} times")
    pats = {t: term_pattern(t) for t in sorted(set(terms), key=len, reverse=True)}
    used, undefined = Counter(), defaultdict(list)
    for r in rules:
        s = g(r, "statement")
        for t, pat in pats.items():  # longest terms first, so PASSING LANE is not read as PASS
            if pat.search(s):
                used[t] += 1
                s = pat.sub(" ", s)
        for phrase in CAPS_PHRASE.findall(s):  # adjacent caps words form one term, split at keywords
            run = []
            for w in phrase.split() + ["WHEN"]:
                if w in KEYWORDS:
                    if run:
                        undefined[" ".join(run)].append(r.get("id", "?"))
                    run = []
                else:
                    run.append(w)
    for w, rids in sorted(undefined.items()):
        p.append(f"'{w}' is capitalized but has no vocab entry: {', '.join(dict.fromkeys(rids))}")
    for t in terms:
        if t and not used[t]:
            p.append(f"'{t}' is in the vocabulary but used in no statement")

    # 8. vocab terms written in lowercase (longest terms first, so "truck passing lane" is one match)
    p = out["8. Lowercase vocab terms"]
    allowed = {w.lower() + suffix for w in allow_lowercase for suffix in ("", "s", "es")}
    for r in rules:
        s, taken = g(r, "statement"), []
        for t in sorted({t for t in terms if t}, key=len, reverse=True):
            pat = re.compile(r"(?<![A-Za-z])" + re.escape(t) + r"(?:S|ES)?(?![A-Za-z])", re.I)
            for m in pat.finditer(s):
                if any(m.start() < b and a < m.end() for a, b in taken):
                    continue
                taken.append((m.start(), m.end()))
                found = m.group(0)
                if found == found.upper() or found.lower() in allowed:
                    continue
                a, b = max(0, m.start() - 30), min(len(s), m.end() + 30)
                ctx = ("…" if a else "") + s[a:b] + ("…" if b < len(s) else "")
                p.append(f"{r.get('id', '?')}: '{found}' is the vocab term {t} in lowercase: \"{ctx}\"")
    return out


def report(path, data, out, handbook):
    n_err = sum(len(v) for v in out.values())
    lines = [f"Format check (stage 1): {os.path.relpath(path, ROOT)}",
             f"{len(data.get('rules', []))} rules, {len(data.get('vocabulary', []))} vocab terms, corpus: {handbook}",
             ""]
    for name, probs in out.items():
        if probs:
            lines.append(f"FAIL  {name} ({len(probs)})")
            lines += [f"    - {x}" for x in probs]
    passed = [name for name, probs in out.items() if not probs]
    if passed:
        lines.append("ok    " + "; ".join(passed))
    lines += ["", f"{n_err} error(s)" if n_err else "No format errors."]
    return "\n".join(lines), n_err


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("rules", help="rules JSON file")
    ap.add_argument("--handbook", default="mto", help="corpus folder under corpus/ (default mto)")
    ap.add_argument("--schema", default=os.path.join(ROOT, "prompts", "formal-rules", "schema.json"))
    ap.add_argument("--allow-lowercase", nargs="*", default=ALLOW_LOWERCASE, metavar="WORD",
                    help=f"vocab terms allowed in lowercase (default: {' '.join(ALLOW_LOWERCASE)}; give none to allow none)")
    ap.add_argument("-o", "--out", help="also write the report to this file")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    path = os.path.abspath(a.rules)
    try:
        data = json.load(open(path, encoding="utf-8"))
    except ValueError as e:
        print(f"Format check (stage 1): {a.rules}\nFAIL  1. Schema: not valid JSON: {e}")
        sys.exit(1)
    if not isinstance(data, dict):
        print(f"Format check (stage 1): {a.rules}\nFAIL  1. Schema: top level is not a JSON object")
        sys.exit(1)

    schema = json.load(open(a.schema, encoding="utf-8"))
    ids = corpus_ids(a.handbook)
    if not ids:
        sys.exit(f"no corpus found at corpus/{a.handbook}/")
    text, n_err = report(path, data, check(data, schema, ids, a.allow_lowercase), a.handbook)
    print(text)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
