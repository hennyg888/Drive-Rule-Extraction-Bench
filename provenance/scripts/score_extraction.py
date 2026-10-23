"""Score a model's Rule Language v1 output against the reference ruleset.

Usage (from the repo root):
  python3 provenance/scripts/score_extraction.py --output runs/<run>/output.json \
      [--ref analysis/passing-rules/passing-rules.v1.json] \
      [--passages analysis/passing-rules/inputs/passing-passages.json --passages analysis/passing-rules/inputs/census-sentences.json] \
      [--report runs/<run>/score.md] [--json runs/<run>/score.json]

Pairing: a model statement and a reference statement are candidates when they cite at least one
passage in common (top-level sources and step sources). Pairs are taken greedily, best first, by
source overlap (Jaccard), then same type, then word overlap of the text. Every score below is
agreement with the reference, not correctness: read the unmatched and disagreeing statements
before counting them as errors.

For a handbook with no reviewed reference, --ref can name another extraction (an earlier draft) to
compare two extractions; give that handbook's passages with --passages. The hard cases and the
no-rule passages are Ontario ids, so they are reported only when the reference cites Ontario passages.
"""
import argparse, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))  # this file is in provenance/scripts/
REF = os.path.join(ROOT, 'analysis/passing-rules/passing-rules.v1.json')
PASSAGES = [os.path.join(ROOT, 'analysis/passing-rules/inputs/passing-passages.json'),
            os.path.join(ROOT, 'analysis/passing-rules/inputs/census-sentences.json')]
SCHEMA = os.path.join(ROOT, 'analysis/passing-rules/statements.schema.json')

MODAL_RE = re.compile(r'\b(MUST NOT|MUST|MAY|SHOULD NOT|SHOULD)\b')
CLAUSES = ['ONLY IF', 'IF VIOLATED', 'WHEN', 'WHILE', 'UNLESS', 'UNTIL', 'BECAUSE']
KEYWORDS = {'DEFINE', 'IS', 'THAT', 'ALSO', 'CALLED', 'FACT', 'TO', 'SPECIALIZES', 'STEP', 'DONE', 'IF', 'THEN',
            'EXCEPTION', 'MUST', 'NOT', 'MAY', 'SHOULD', 'WATCH', 'FOR', 'WHEN', 'WHILE', 'ONLY', 'UNLESS',
            'UNTIL', 'BECAUSE', 'VIOLATED', 'AND', 'OR'}
# all-caps tokens that are ordinary words in the handbook, not keywords
ALLOWED_CAPS = {'LCV', 'HOV', 'HOT', 'GPS', 'ATV', 'MTO', 'G1', 'G2', 'M1', 'M2', 'RV', 'EDR', 'U', 'X'}
NUMBER_WORDS = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
                'ten': 10, 'eleven': 11, 'twelve': 12, 'fifteen': 15, 'twenty': 20, 'thirty': 30, 'forty': 40,
                'fifty': 50, 'sixty': 60, 'hundred': 100, 'first': 1, 'second': 2, 'third': 3}
HARD = {
    'condition only in a heading': '3.1.7a 3.2.1d 3.2.2a 3.3.1b 3.3.2a 3.3.2b 3.3.3a 3.3.3b 3.4.4a 3.4.4c 3.4.5d 3.4.7a 3.4.8a 3.5.2a 3.6.1d',
    'condition only in a neighbouring passage': '2.2b 3.1.4a',
    'legal force set only by a heading': '3.1.7a 3.2.1d 3.6.1c',
    'link between different passages': '2.2b 3.3.1b 3.4.12e',
    'duty written apart from its penalty': '3.4.4b 3.4.12b 3.4.13a 3.4.13b',
    'sources on two pages': '3.1.1a 3.4.13a 3.4.13b 3.6.1a 3.6.3a 3.6.3b',
}
NO_RULE_PASSAGES = ['m92', 'm93', 'm94', 'm95', 'm96']


def srcs(s):
    out = {x['id'] for x in s.get('sources', [])}
    for st in s.get('steps') or []:
        out |= set(st.get('sources', []))
    return out


def words(t):
    return set(re.findall(r'[a-z0-9]+', (t or '').lower()))


def body(s):
    t = s.get('text') or ''
    if t.startswith('EXCEPTION TO') and ':' in t:
        t = t.split(':', 1)[1]
    return t


def modals(s):
    # the set of modals: the grammar lets a modal repeat after AND or not ("SHOULD signal AND [SHOULD] pull over")
    return sorted(set(MODAL_RE.findall(body(s)))) if s.get('type') in ('RULE',) else []


def clauses(s):
    t = re.sub(r'\[\?[^\]]*\]', ' ', body(s))
    found = []
    for c in CLAUSES:
        n = len(re.findall(r'\b' + c + r'\b', t))
        if n:
            found.append(c)
            t = re.sub(r'\b' + c + r'\b', ' ', t)
    return sorted(found)


def inline_spans(s):
    out = []
    for f in s.get('flags', []):
        if f['code'] in 'JSRG':
            out.append((f['code'], f['span'].strip().lower()))
    return out


def numbers_ok(s, passage_text):
    text = re.sub(r'\b\d+[a-z]\b|\b[a-z]?\d+\.\d+[a-z]?\b', ' ', s.get('text') or '')  # drop statement ids such as 3.2.3a
    for st in s.get('steps') or []:
        text += ' ' + st['text']
    text = re.sub(r'(?<=\d),(?=\d{3}\b)', '', text)  # thousands separators: $1,000 and $1000 are the same number
    nums = set(re.findall(r'(?<![\w.-])\d+(?:\.\d+)?(?![\w.-])', text))
    src = re.sub(r'(?<=\d),(?=\d{3}\b)', '', ' '.join(passage_text.get(i, '') for i in srcs(s)).lower())
    have = set(re.findall(r'\d+(?:\.\d+)?', src)) | {str(v) for k, v in NUMBER_WORDS.items() if re.search(r'\b' + k + r'\b', src)}
    if re.search(r'\bone and one-half\b', src):
        have.add('1.5')
    return sorted(n for n in nums if n not in have)


def stray_caps(s):
    text = (s.get('text') or '') + ' ' + ' '.join(st['text'] for st in s.get('steps') or [])
    text = re.sub(r'\[\?[^\]]*\]|"[^"]*"|\([^)]*\)', ' ', text)
    toks = re.findall(r'\b[A-Z][A-Z0-9-]*[A-Z0-9]\b', text)  # a token ends in a letter or digit, so "U-turn" is not caught
    return sorted({t for t in toks if t not in KEYWORDS and t not in ALLOWED_CAPS})


def pair(model, ref):
    cands = []
    for i, m in enumerate(model):
        sm = srcs(m)
        for j, r in enumerate(ref):
            sr = srcs(r)
            inter = sm & sr
            if not inter:
                continue
            jac = len(inter) / len(sm | sr)
            wm, wr = words(body(m)), words(body(r))
            wj = len(wm & wr) / max(1, len(wm | wr))
            cands.append((jac + 0.5 * (m.get('type') == r.get('type')) + wj, i, j))
    cands.sort(reverse=True)
    used_m, used_r, pairs = set(), set(), []
    for sc, i, j in cands:
        if i in used_m or j in used_r:
            continue
        used_m.add(i); used_r.add(j); pairs.append((i, j))
    return pairs


def pct(a, b):
    return f'{a}/{b} ({100 * a / b:.0f}%)' if b else f'{a}/0'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    ap.add_argument('--ref', default=REF)
    ap.add_argument('--passages', action='append')
    ap.add_argument('--report')
    ap.add_argument('--json')
    a = ap.parse_args()

    ref = json.load(open(a.ref, encoding='utf-8'))
    ref = ref['statements'] if isinstance(ref, dict) else ref
    model = json.load(open(a.output, encoding='utf-8'))['statements']
    passages = []
    for p in a.passages or PASSAGES:
        passages += json.load(open(p, encoding='utf-8'))
    ptext = {(p.get('id') or p.get('m')): p['text'] for p in passages}
    pfull = {(p.get('id') or p.get('m')): ' '.join(x for x in (p.get('sec'), p['text'], p.get('cap')) if x) for p in passages}

    res = {'n_ref': len(ref), 'n_model': len(model)}
    lines = [f'# Score: {os.path.relpath(a.output, ROOT)} against {os.path.relpath(a.ref, ROOT)}', '']

    # validity
    schema_errors = []
    try:
        import jsonschema
        v = jsonschema.Draft202012Validator(json.load(open(SCHEMA)))
        schema_errors = [f'{"/".join(map(str, e.path))}: {e.message[:120]}' for e in v.iter_errors({'statements': model})]
    except ImportError:
        schema_errors = ['jsonschema not installed; schema not checked']
    ids = [m['id'] for m in model]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    bad_links = [(m['id'], l) for m in model for l in m.get('links', []) if l not in ids]
    bad_quotes = [(m['id'], x['id']) for m in model for x in m.get('sources', []) if ptext.get(x['id']) is not None and x['quote'] != ptext[x['id']]]
    unknown_src = sorted({i for m in model for i in srcs(m) if i not in ptext})
    you = [m['id'] for m in model if re.search(r'\byou(r)?\b', (m.get('text') or '') + ' '.join(s['text'] for s in m.get('steps') or []), re.I)]
    stray = {m['id']: stray_caps(m) for m in model if stray_caps(m)}
    numbers = {m['id']: numbers_ok(m, pfull) for m in model if numbers_ok(m, pfull)}
    res.update(schema_errors=len(schema_errors), duplicate_ids=dup, bad_links=bad_links, quotes_not_verbatim=len(bad_quotes),
               unknown_sources=unknown_src, uses_you=you, stray_caps=stray, numbers_not_in_sources=numbers)

    # pairing and agreement
    pairs = pair(model, ref)
    res['matched'] = len(pairs)
    agree = Counter()
    rows = []
    rid_of = {}
    for i, j in pairs:
        m, r = model[i], ref[j]
        rid_of[m['id']] = r['id']
    for i, j in pairs:
        m, r = model[i], ref[j]
        a_type = m['type'] == r['type']
        a_force = m.get('force') == r.get('force')
        a_modal = modals(m) == modals(r)
        a_clause = clauses(m) == clauses(r)
        a_src = srcs(m) == srcs(r)
        a_links = sorted(rid_of.get(l, '?') for l in m.get('links', [])) == sorted(r.get('links', []))
        for k, v in (('type', a_type), ('force', a_force), ('modal', a_modal), ('clauses', a_clause), ('sources', a_src), ('links', a_links)):
            agree[k] += v
        rows.append(dict(ref=r['id'], model=m['id'], type=a_type, force=a_force, modal=a_modal, clauses=a_clause,
                         sources=a_src, links=a_links, ref_text=r['text'], model_text=m['text'],
                         ref_clauses=clauses(r), model_clauses=clauses(m), ref_modals=modals(r), model_modals=modals(m)))
    res['agreement'] = dict(agree)
    rules = [(i, j) for i, j in pairs if ref[j]['type'] in ('RULE', 'PROCEDURE')]
    res['force_on_rules'] = sum(model[i].get('force') == ref[j].get('force') for i, j in rules)
    res['n_rule_pairs'] = len(rules)

    # flags on matched pairs
    tp = fp = fn = code_ok = 0
    for i, j in pairs:
        ms, rs = inline_spans(model[i]), inline_spans(ref[j])
        rem = list(rs)
        for code, span in ms:
            hit = next((x for x in rem if x[1] == span or x[1] in span or span in x[1]), None)
            if hit:
                tp += 1; code_ok += code == hit[0]; rem.remove(hit)
            else:
                fp += 1
        fn += len(rem)
    prec = tp / (tp + fp) if tp + fp else 0
    rec = tp / (tp + fn) if tp + fn else 0
    res['flags'] = dict(tp=tp, fp=fp, fn=fn, precision=round(prec, 3), recall=round(rec, 3),
                        f1=round(2 * prec * rec / (prec + rec), 3) if prec + rec else 0, code_agreement_on_matched=code_ok)

    # passage coverage
    ref_cited = set().union(*(srcs(r) | {x['source'] for x in r.get('see') or []} for r in ref))
    mod_cited = set().union(*(srcs(m) | {x['source'] for x in m.get('see') or []} for m in model)) if model else set()
    res['passages_missed'] = sorted(ref_cited - mod_cited)
    res['passages_extra'] = sorted(mod_cited - ref_cited)
    # the hard cases and no-rule passages are Ontario ids; other handbooks' passages are p1, p2, ...
    ontario = bool(ref_cited) and all(re.fullmatch(r'[mc]\d+', x) for x in ref_cited)
    res['no_rule_passages_cited'] = [p for p in NO_RULE_PASSAGES if p in mod_cited] if ontario else []

    # hard cases
    matched_ref = {ref[j]['id']: rows[k] for k, (i, j) in enumerate(pairs)}
    hard = {}
    for name, idl in (HARD.items() if ontario else []):
        ids_ = idl.split()
        got = [x for x in ids_ if x in matched_ref]
        full = [x for x in got if matched_ref[x]['clauses'] and matched_ref[x]['modal'] and matched_ref[x]['force']]
        hard[name] = dict(n=len(ids_), matched=len(got), clauses_modal_force_agree=len(full),
                          missing=[x for x in ids_ if x not in matched_ref])
    res['hard_cases'] = hard

    unmatched_ref = [r for j, r in enumerate(ref) if j not in {jj for _, jj in pairs}]
    unmatched_model = [m for i, m in enumerate(model) if i not in {ii for ii, _ in pairs}]
    res['unmatched_ref'] = [r['id'] for r in unmatched_ref]
    res['unmatched_model'] = [m['id'] for m in unmatched_model]

    # report
    tm = Counter(m['type'] for m in model); tr = Counter(r['type'] for r in ref)
    lines += [
        '## Summary', '',
        f'- Statements: model {len(model)} ({", ".join(f"{k} {v}" for k, v in sorted(tm.items()))}); reference {len(ref)} ({", ".join(f"{k} {v}" for k, v in sorted(tr.items()))}).',
        f'- Paired by shared sources: {len(pairs)}. Reference recall {pct(len(pairs), len(ref))}; model precision {pct(len(pairs), len(model))}.',
        f'- On paired statements: type {pct(agree["type"], len(pairs))}, force {pct(agree["force"], len(pairs))}, modal {pct(agree["modal"], len(pairs))}, clause keywords {pct(agree["clauses"], len(pairs))}, same sources {pct(agree["sources"], len(pairs))}, links {pct(agree["links"], len(pairs))}.',
        f'- Law or advice on paired rules and procedures: {pct(res["force_on_rules"], len(rules))}.',
        f'- Inline flags (J, S, R, G) on paired statements: precision {prec:.2f}, recall {rec:.2f}, F1 {res["flags"]["f1"]:.2f}; same code on {code_ok} of {tp} matched spans.',
        f'- Passages the reference cites and the model does not: {", ".join(res["passages_missed"]) or "none"}.',
        f'- Passages the model cites and the reference does not: {", ".join(res["passages_extra"]) or "none"}.',
        '',
        '## Validity', '',
        f'- Schema errors: {len(schema_errors)}' + (f' (first: {schema_errors[0]})' if schema_errors else ''),
        f'- Duplicate ids: {dup or "none"}; links to missing ids: {bad_links or "none"}; unknown source ids: {unknown_src or "none"}.',
        f'- Quotes that are not the full passage text: {len(bad_quotes)}.',
        f'- Statements using "you": {you or "none"}.',
        f'- Capitalised words that are not keywords: {stray or "none"}.',
        f'- Numbers not found in the sources: {numbers or "none"}.',
        '',
    ]
    if ontario:
        lines += ['## Hard cases', '',
                  '| Case | Reference statements | Paired | Clauses, modal and force agree | Not paired |', '|---|---|---|---|---|']
        for name, h in hard.items():
            lines.append(f'| {name} | {h["n"]} | {h["matched"]} | {h["clauses_modal_force_agree"]} | {" ".join(h["missing"]) or "-"} |')
        lines += ['', f'Passages that should give no passing rule (m92 to m96) cited by the model: {", ".join(res["no_rule_passages_cited"]) or "none"}.', '']
    lines += ['## Paired statements that disagree', '',
              '| Reference | Model | Differs in | Reference text | Model text |', '|---|---|---|---|---|']
    for row in rows:
        diff = [k for k in ('type', 'force', 'modal', 'clauses', 'links') if not row[k]]
        if diff:
            lines.append(f'| {row["ref"]} | {row["model"]} | {", ".join(diff)} | {row["ref_text"]} | {row["model_text"]} |')
    lines += ['', '## Reference statements with no pair', '']
    lines += [f'- {r["id"]} ({r["type"]}, sources {", ".join(sorted(srcs(r)))}): {r["text"]}' for r in unmatched_ref] or ['- none']
    lines += ['', '## Model statements with no pair', '']
    lines += [f'- {m["id"]} ({m["type"]}, sources {", ".join(sorted(srcs(m)))}): {m["text"]}' for m in unmatched_model] or ['- none']
    report = '\n'.join(lines) + '\n'
    if a.report:
        open(a.report, 'w', encoding='utf-8').write(report)
    if a.json:
        res['pairs'] = rows
        json.dump(res, open(a.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\n'.join(lines[:16]))


if __name__ == '__main__':
    main()
