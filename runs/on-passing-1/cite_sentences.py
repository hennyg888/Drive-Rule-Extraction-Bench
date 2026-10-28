"""Cite sentences instead of whole paragraphs in the statements of on-passing-1.

on-passing-1 was answered with the prompt of before 28 October 2026, whose statements quote each source
passage (a paragraph) in full. sentences.json gives each statement the sentences (and figures) it comes
from, in citing order, chosen by hand from its text, steps and paragraphs; the prompt now has the model
cite them itself. This script checks that the sentences lie in the paragraphs each statement and step
cited, then replaces its statement_source and step_source rows. The statements and their grounding stay
as they are. Run from the repo root; running it again changes nothing.

    python3 -I -B runs/on-passing-1/cite_sentences.py
"""
import json
import sys

sys.path.insert(0, 'tools')
import db as dbtool  # noqa: E402
import extract_rules  # noqa: E402

RUN = 'on-passing-1'
db = dbtool.connect()
q = lambda s, *a: db.execute(s, a).fetchall()  # noqa: E731
msg = json.load(open(f'runs/{RUN}/messages.json', encoding='utf-8'))
cite = extract_rules.citable(extract_rules.passages(db, msg['selection']), 'sentence')
want = json.load(open(f'runs/{RUN}/sentences.json', encoding='utf-8'))
para = {r['id']: r['parent_id'] if r['kind'] == 'sentence' else r['id'] for r in q('SELECT id, kind, parent_id FROM unit')}

statements = q('SELECT id, local_id FROM statement WHERE run_id = ? ORDER BY position', RUN)
errs = [f'{k}: not a statement of {RUN}' for k in set(want) - {s['local_id'] for s in statements}]
errs += [f'{s["local_id"]}: missing from sentences.json' for s in statements if s['local_id'] not in want]
rows, steps = [], []
for s in statements:
    w = want.get(s['local_id'], {})
    for x in w.get('sources', []) + [x for ids in w.get('steps', {}).values() for x in ids]:
        if x not in cite:
            errs.append(f'{s["local_id"]}: {x} is not a sentence or figure of the selection')
    if errs:
        continue
    had = {para[r[0]] for r in q('SELECT unit_id FROM statement_source WHERE statement_id = ?', s['id'])}
    now = {para[cite[x][0]] for x in w['sources']}
    if had != now:
        errs.append(f'{s["local_id"]}: cites paragraphs {sorted(now)}, not {sorted(had)}')
    rows += [(s['id'], i, cite[x][0], cite[x][1]) for i, x in enumerate(w['sources'])]
    for st in q('SELECT position, n FROM statement_step WHERE statement_id = ? ORDER BY position', s['id']):
        ids = w.get('steps', {}).get(st['n'], [])
        had = {para[r[0]] for r in q('SELECT unit_id FROM step_source WHERE statement_id = ? AND step = ?',
                                     s['id'], st['position'])}
        if had != {para[cite[x][0]] for x in ids}:
            errs.append(f'{s["local_id"]}: step {st["n"]} cites other paragraphs than before')
        steps += [(s['id'], st['position'], j, cite[x][0]) for j, x in enumerate(ids)]
    if set(w.get('steps', {})) != {r[0] for r in q('SELECT n FROM statement_step WHERE statement_id = ?', s['id'])}:
        errs.append(f'{s["local_id"]}: the steps in sentences.json are not its steps')
if errs:
    sys.exit('\n'.join(errs))

ids = [s['id'] for s in statements]
marks = ','.join('?' * len(ids))
db.execute(f'DELETE FROM step_source WHERE statement_id IN ({marks})', ids)
db.execute(f'DELETE FROM statement_source WHERE statement_id IN ({marks})', ids)
db.executemany('INSERT INTO statement_source (statement_id, position, unit_id, quote) VALUES (?, ?, ?, ?)', rows)
db.executemany('INSERT INTO step_source VALUES (?, ?, ?, ?)', steps)
dbtool.derive(db)
db.commit()
kinds = q("SELECT u.kind, COUNT(*) FROM statement_source x JOIN unit u ON u.id = x.unit_id JOIN statement s "
          "ON s.id = x.statement_id WHERE s.run_id = ? GROUP BY u.kind", RUN)
print(f'{RUN}: {len(rows)} sources (' + ', '.join(f'{k} {n}' for k, n in kinds) + f'), {len(steps)} step sources')
