"""Check rule-language v1 statements: schema, keywords, force, clauses, flags, quotes, numbers, links.

Usage:
    python tools/check_statements.py STATEMENTS.json --passages P1.json [P2.json ...] [--quiet]

STATEMENTS.json is {"statements": [...]} (model output) or a plain list (reference files).
Passage files are lists of {"m": id, "text": ..., "cap": ...} or {"id": ..., "text": ...}
(the inputs in analysis/passing-rules/inputs/, or example passages). Prints one line per
problem and a count per check; exits 1 if any error was found.
"""
import argparse
import json
import os
import re
import sys

import jsonschema

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = os.path.join(ROOT, "analysis", "passing-rules", "statements.schema.json")
DISPLAY_ONLY = {"section", "see", "zh", "note_zh"}
SOURCE_DISPLAY_ONLY = {"where", "image", "census_id", "zh"}
FLAG_DISPLAY_ONLY = {"zh"}

KEYWORDS = ["ALSO CALLED", "MUST NOT", "SHOULD NOT", "WATCH FOR", "ONLY IF", "IF VIOLATED", "DONE WHEN",
            "EXCEPTION TO", "SPECIALIZES", "DEFINE", "IS", "THAT", "FACT", "MUST", "MAY", "SHOULD",
            "WHEN", "WHILE", "UNLESS", "UNTIL", "BECAUSE", "AND", "OR", "NOT", "TO", "IF", "THEN"]
MODALS = ["MUST NOT", "SHOULD NOT", "MUST", "SHOULD", "MAY"]
LEGAL = {"MUST", "MUST NOT", "MAY"}
CLAUSE_ORDER = ["WHEN", "WHILE", "ONLY IF", "UNLESS", "UNTIL", "BECAUSE", "IF VIOLATED"]
INLINE_CODES = {"J", "S", "R", "G"}
# A statement id after EXCEPTION TO or SPECIALIZES; ids may hold a colon (p05:3.2.3a), and the
# exception form ends the id with ": ".
LINK_RE = r"\b(?:EXCEPTION TO|SPECIALIZES) (\S+?)(?=:\s|:$|\s|$)"
BASES = ("text", "imperative", "caution", "context", "implied", "default")
NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
                "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "fifteen": 15, "twenty": 20,
                "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "hundred": 100}


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip()


def strip_display(st):
    st = {k: v for k, v in st.items() if k not in DISPLAY_ONLY}
    st["sources"] = [{k: v for k, v in s.items() if k not in SOURCE_DISPLAY_ONLY} for s in st.get("sources", [])]
    st["flags"] = [{k: v for k, v in f.items() if k not in FLAG_DISPLAY_ONLY} for f in st.get("flags", [])]
    return st


def outside_quotes(text):
    """Text with quoted sign wording and [?…] spans removed, for keyword and case checks."""
    text = re.sub(r"\[\?[^\]]*\]", " ", text)
    return re.sub(r"\"[^\"]*\"|“[^”]*”", " ", text)


def capital_tokens(text):
    """Runs of capitalised words that are not abbreviations of 1 letter + digits (G1) etc."""
    out = []
    for tok in re.findall(r"\b[A-Z][A-Z]+\b|\b[A-Z]\b", outside_quotes(text)):
        out.append(tok)
    return out


def clause_sequence(text):
    """Clause keywords in order of appearance (after the main action)."""
    seq = []
    for m in re.finditer(r"\b(IF VIOLATED|ONLY IF|WHEN|WHILE|UNLESS|UNTIL|BECAUSE)\b", outside_quotes(text)):
        seq.append(m.group(1))
    return seq


FRACTION_WORDS = {"half": 2, "third": 3, "quarter": 4, "fourth": 4}


def numbers_in(text):
    vals = set()
    for a, b in re.findall(r"\b(\d+)/(\d+)\b", text):
        vals.add(round(int(a) / int(b), 4))
    text = re.sub(r"\b\d+/\d+\b", " ", text)
    for w, d in FRACTION_WORDS.items():
        for m in re.finditer(rf"\b(?:(one|two|three|a)[- ])?{w}s?\b", text, re.I):
            num = {"two": 2, "three": 3}.get((m.group(1) or "one").lower(), 1)
            vals.add(round(num / d, 4))
    for n in re.findall(r"\d+(?:\.\d+)?", text):
        vals.add(float(n))
    for w, v in NUMBER_WORDS.items():
        if re.search(rf"\b{w}\b(?!-)", text, re.I):
            vals.add(float(v))
    return vals


def load_passages(paths):
    passages = {}
    for p in paths:
        data = json.load(open(p, encoding="utf-8"))
        if isinstance(data, dict) and "examples" in data:
            data = [ps for ex in data["examples"] for ps in ex["passages"]]
        for x in data:
            pid = x.get("m") or x.get("id")
            passages[pid] = x
    return passages


def check(statements, passages, headings=None):
    """Return a list of (check, statement id, message)."""
    problems = []
    schema = json.load(open(SCHEMA))
    ids = [s.get("id") for s in statements]
    idset = set(ids)
    for dup in {i for i in ids if ids.count(i) > 1}:
        problems.append(("ids", dup, "duplicate id"))

    validator = jsonschema.Draft202012Validator(schema)
    for err in validator.iter_errors({"statements": [strip_display(s) for s in statements]}):
        where = list(err.absolute_path)
        sid = statements[where[1]].get("id") if len(where) > 1 else "-"
        problems.append(("schema", sid, f"{'/'.join(map(str, where[2:]))}: {err.message[:160]}"))

    for st in statements:
        sid, typ, text = st.get("id"), st.get("type"), st.get("text", "")
        texts = [text] + [s.get("text", "") for s in st.get("steps", []) or []]
        full = " ".join(texts)

        # keywords and case
        for tok in capital_tokens(full):
            if tok not in {w for k in KEYWORDS for w in k.split()} and len(tok) > 1 and not re.fullmatch(r"[A-Z]{2,5}", tok):
                problems.append(("keywords", sid, f"unknown capitalised word {tok!r}"))
        if re.search(r"\b(you|your|yours|yourself)\b", outside_quotes(full), re.I):
            problems.append(("role", sid, "statement uses you/your"))

        # type-specific shape
        if typ == "DEFINE" and not re.match(r"DEFINE .+ IS .+ THAT ", text):
            problems.append(("shape", sid, "DEFINE does not match 'DEFINE term IS kind THAT …'"))
        if typ == "FACT" and not text.startswith("FACT "):
            problems.append(("shape", sid, "FACT text does not start with 'FACT '"))
        if typ == "PROCEDURE":
            if not text.startswith("TO "):
                problems.append(("shape", sid, "PROCEDURE text does not start with 'TO '"))
            if not st.get("steps"):
                problems.append(("shape", sid, "PROCEDURE has no steps"))
        if typ == "EXCEPTION" and not re.match(r"EXCEPTION TO \S+ WHEN ", text):
            problems.append(("shape", sid, "EXCEPTION text is not 'EXCEPTION TO <id> WHEN …'"))
        if typ != "PROCEDURE" and st.get("steps"):
            problems.append(("shape", sid, "steps on a non-PROCEDURE statement"))

        # modal and force
        body = re.sub(r"^EXCEPTION TO \S+:\s*", "", text)
        modals = re.findall(r"\b(MUST NOT|SHOULD NOT|MUST|SHOULD|MAY)\b", outside_quotes(body))
        force = st.get("force")
        if typ == "RULE":
            if not modals:
                problems.append(("force", sid, "RULE has no modal"))
            kinds = {"LEGAL" if m in LEGAL else "ADVISORY" for m in modals}
            if len(kinds) == 1 and force not in kinds:
                problems.append(("force", sid, f"force {force} but modal(s) {modals}"))
            if len(kinds) > 1:
                problems.append(("force", sid, f"mixes legal and advisory modals {modals} (force {force})"))
            if text.startswith("EXCEPTION TO") and not st.get("links"):
                problems.append(("links", sid, "EXCEPTION TO … rule without links"))
        if typ in ("DEFINE", "FACT", "EXCEPTION") and (force is not None or st.get("force_from") is not None):
            problems.append(("force", sid, f"{typ} should have force and force_from null"))
        if typ in ("RULE", "PROCEDURE"):
            ff = st.get("force_from") or ""
            if not ff.startswith(BASES):
                problems.append(("force_from", sid, f"force_from {ff!r} does not start with a basis {BASES}"))

        # clause order and repetition
        for t in texts:
            seq = clause_sequence(re.sub(r"^IF .*? THEN ", "", t))
            ranks = [CLAUSE_ORDER.index(c) for c in seq]
            if ranks != sorted(ranks):
                problems.append(("clauses", sid, f"clause order {seq}"))
            for c in set(seq):
                if seq.count(c) > 1:
                    problems.append(("clauses", sid, f"clause {c} used {seq.count(c)} times"))

        # flags and inline marks
        inline = re.findall(r"\[\?([^\]]+)\]", full)
        flags = st.get("flags", [])
        spans = [f.get("span") for f in flags if f.get("code") in INLINE_CODES]
        for sp in inline:
            if sp not in [f.get("span") for f in flags]:
                problems.append(("flags", sid, f"[?{sp}] has no flag with that span"))
        # A J/S/R/G span may name source words the statement rewrote away; it needs a mark
        # only when the words are still in the statement text.
        unmarked = re.sub(r"\[\?[^\]]*\]", " ", full)
        for sp in spans:
            if sp not in inline and sp and re.search(rf"(?<![\w-]){re.escape(sp)}(?![\w-])", unmarked):
                problems.append(("flags", sid, f"vague span {sp!r} is in the text without a [?…] mark"))

        # sources and quotes
        src_text = []
        for s in st.get("sources", []):
            p = passages.get(s.get("id"))
            if p is None:
                problems.append(("sources", sid, f"unknown passage {s.get('id')}"))
                continue
            ptext = " ".join(x for x in (p.get("text"), p.get("cap")) if x)
            src_text.append(ptext + " " + (p.get("sec") or "") + " " + (p.get("page") or ""))
            q = s.get("quote", "")
            if q not in ptext:
                kind = "quote-normalised" if norm(q) in norm(ptext) else "quote"
                problems.append((kind, sid, f"{s.get('id')}: quote not found verbatim: {q[:80]!r}"))
        for step in st.get("steps", []) or []:
            for pid in step.get("sources", []):
                if pid not in passages:
                    problems.append(("sources", sid, f"step {step.get('n')}: unknown passage {pid}"))
                else:
                    src_text.append(" ".join(x for x in (passages[pid].get("text"), passages[pid].get("cap"), passages[pid].get("sec")) if x))

        # numbers (statement ids after EXCEPTION TO / SPECIALIZES are not numbers)
        allowed = numbers_in(" ".join(src_text))
        bare = re.sub(LINK_RE, " ", full)
        for n in numbers_in(re.sub(r"\b\d+\.\d+[a-z]?\b|\b\d+(\.\d+)*[a-z]\b", " ", bare)):
            if n not in allowed:
                problems.append(("numbers", sid, f"number {n:g} not in its sources"))

        # links
        for l in st.get("links", []):
            if l not in idset:
                problems.append(("links", sid, f"link to unknown id {l}"))
        for m in re.finditer(LINK_RE, text):
            if m.group(1) not in st.get("links", []):
                problems.append(("links", sid, f"{m.group(0)} not listed in links"))
    return problems


def check_notes(notes, statements):
    """Coverage of a model answer's reading notes: every passage noted as about the topic is cited."""
    problems = []
    cited = set()
    for st in statements:
        cited |= {s.get("id") for s in st.get("sources", [])}
        for step in st.get("steps", []) or []:
            cited |= set(step.get("sources", []))
    ids = [n.get("id") for n in notes]
    for dup in {i for i in ids if ids.count(i) > 1}:
        problems.append(("notes", dup, "passage noted more than once"))
    for n in notes:
        if n.get("about_topic") and n.get("id") not in cited:
            problems.append(("coverage", n.get("id"), f"noted as about the topic but cited by no statement: {n.get('says', '')[:80]}"))
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("statements")
    ap.add_argument("--passages", nargs="+", required=True)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    data = json.load(open(a.statements, encoding="utf-8"))
    statements = data["statements"] if isinstance(data, dict) else data
    problems = check(statements, load_passages(a.passages))
    if isinstance(data, dict) and "passages" in data:
        problems += check_notes(data["passages"], statements)
    counts = {}
    for c, sid, msg in problems:
        counts[c] = counts.get(c, 0) + 1
        if not a.quiet:
            print(f"{c:16} {sid:10} {msg}")
    print(f"{len(statements)} statements, {len(problems)} problems" +
          (": " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) if counts else ""))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
