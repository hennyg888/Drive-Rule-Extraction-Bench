"""Stage 5, grounding: carry what was already checked for one run over to another run of the same topic.

Statements are paired as tools/compare_runs.py pairs them. For each pair:
  - a flag of the new statement with the same code and the same words as a flag of its pair gets
    that flag's grounding and links;
  - when the two statements agree on type, strength, modals and clause keywords, the new statement
    gets its pair's provisions (statement_basis) and law lines (statement_law, statement_law_ref).
Every carried row says in its note which statement it came from. Rows already there are kept, so it
can run again after grounding by hand. Nothing is carried for a statement or a flag with no match;
those are listed for grounding by hand.

    python3 tools/carry_grounding.py on-passing-1 --from on-passing-ref [--report runs/on-passing-1/grounding-left.md]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compare_runs  # noqa: E402
import db as dbtool  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('run')
    ap.add_argument('--from', dest='source', required=True)
    ap.add_argument('--report')
    a = ap.parse_args()
    db = dbtool.connect()
    q = lambda sql, *x: db.execute(sql, x).fetchall()  # noqa: E731
    A, B = compare_runs.statements(db, a.run), compare_runs.statements(db, a.source)
    pairs = compare_runs.pair(A, B)
    mark = lambda note, j: ((note or '').rstrip() + f' (Carried from {j}.)').strip()  # noqa: E731

    # Rows already there, carried or written by hand, stay as they are: only what is missing is carried.
    grounded = {r[0] for r in q('SELECT occurrence_id FROM grounding')}
    has_basis = {r[0] for r in q('SELECT DISTINCT statement_id FROM statement_basis')}

    flags = basis = law = 0
    review = []
    for i, j in pairs:
        theirs = {(o['code'], dbtool.norm(o['span'])): o for o in q('SELECT * FROM occurrence WHERE statement_id = ?', j)}
        for o in q('SELECT * FROM occurrence WHERE statement_id = ?', i):
            src = theirs.get((o['code'], dbtool.norm(o['span'])))
            g = src and o['id'] not in grounded and q('SELECT * FROM grounding WHERE occurrence_id = ?', src['id'])
            if g:
                g = g[0]
                db.execute('INSERT INTO grounding VALUES (?, ?, ?, ?, ?)',
                           (o['id'], g['status'], g['definition'], g['effect'], mark(g['note'], j)))
                db.executemany('INSERT INTO grounding_link VALUES (?, ?, ?)',
                               [(o['id'], l['unit_id'], l['role']) for l in q('SELECT * FROM grounding_link WHERE occurrence_id = ?', src['id'])])
                flags += 1
        x, y = A[i]['row'], B[j]['row']
        same = (x['type'] == y['type'] and x['strength'] == y['strength'] and
                compare_runs.modals(x) == compare_runs.modals(y) and compare_runs.clauses(x['text']) == compare_runs.clauses(y['text']))
        rows = q('SELECT * FROM statement_basis WHERE statement_id = ?', j)
        if i in has_basis:
            continue
        if rows and not same:
            review.append((i, j))
            continue
        db.executemany('INSERT INTO statement_basis VALUES (?, ?, ?, ?)', [(i, r['unit_id'], r['relation'], mark(r['note'], j)) for r in rows])
        basis += len(rows)
        for r in q('SELECT * FROM statement_law WHERE statement_id = ? ORDER BY position', j):
            db.execute('INSERT INTO statement_law VALUES (?, ?, ?, ?)', (i, r['position'], r['text'], mark(r['note'], j)))
            db.executemany('INSERT INTO statement_law_ref VALUES (?, ?, ?)',
                           [(i, r['position'], u[0]) for u in q('SELECT unit_id FROM statement_law_ref WHERE statement_id = ? AND position = ?',
                                                                  j, r['position'])])
            law += 1
    db.commit()

    left = q('SELECT o.statement_id, o.code, o.span FROM occurrence o JOIN statement s ON s.id = o.statement_id '
             'WHERE s.run_id = ? AND o.id NOT IN (SELECT occurrence_id FROM grounding) ORDER BY s.position, o.position', a.run)
    paired = {i for i, _ in pairs}
    based = {r[0] for r in q('SELECT DISTINCT statement_id FROM statement_basis')}
    no_pair = [s for s in A.values() if s['row']['id'] not in paired | based and s['row']['strength'] == 'LAW']
    print(f'{a.run}: carried {flags} flag groundings, {basis} provisions and {law} law lines from {a.source}; '
          f'{len(left)} flags left, {len(review)} paired statements with provisions to review, '
          f'{len(no_pair)} LAW statements with no pair and no provision')
    if a.report:
        local = lambda sid: sid.split(':', 1)[1]  # noqa: E731
        total = q('SELECT COUNT(*) FROM occurrence o JOIN statement s ON s.id = o.statement_id WHERE s.run_id = ?', a.run)[0][0]
        out = [f'# Grounding left to do for {a.run}', '',
               f'Written by `tools/carry_grounding.py {a.run} --from {a.source}`, which carries grounding from paired statements; '
               f'the rest is grounded by hand. {total - len(left)} of {total} flags are grounded.', '',
               f'## Flags with no grounding ({len(left)})', '', '| Statement | Code | Words |', '|---|---|---|']
        out += [f'| {local(r[0])} | {r[1]} | {r[2]} |' for r in left]
        out += ['', f'## Paired statements that differ from their pair, whose provisions were not carried ({len(review)})', '',
                f'| {a.run} | {a.source} | {a.run} text | {a.source} text |', '|---|---|---|---|']
        out += [f'| {local(i)} | {local(j)} | {A[i]["row"]["text"]} | {B[j]["row"]["text"]} |' for i, j in review]
        out += ['', f'## LAW statements with no pair and no provision ({len(no_pair)})', '']
        out += [f'- {s["row"]["local_id"]}: {s["row"]["text"]}' for s in no_pair] or ['- none']
        open(os.path.join(dbtool.ROOT, a.report), 'w', encoding='utf-8').write('\n'.join(out) + '\n')


if __name__ == '__main__':
    main()
