"""Stage 5, resolving flags: write what the rest of the handbook and the law say about each flag, and the verdict.

    python3 tools/resolve_flags.py runs/resolve-1/resolved.json

The file is {"provisions": [...], "flags": [...]}. A provision row adds a law provision the database
does not have yet: {"id", "source", "locator", "heading", "text"}, the text copied word for word
from the local copy of the law (db.py check compares them). A flag row is

    {"id": "<occurrence id>",
     "handbook": {"finding": "DEFINES|STATES|REPEATS|SILENT", "says": "...", "units": ["<sentence or figure ids>"]},
     "law": {"finding": ..., "says": ..., "units": ["<provision ids>"]},
     "standard": {...}  (optional: an engineering standard or safety model),
     "verdict": "RESOLVED|PARTIAL|OPEN", "definition": ..., "effect": ..., "note": ...}

Each flag in the file replaces whatever grounding that flag had; flags not in the file are left as
they are. Run tools/db.py check afterwards.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db as dbtool  # noqa: E402

SIDES = ('handbook', 'law', 'standard')
FINDINGS = {'DEFINES', 'STATES', 'REPEATS', 'SILENT'}
VERDICTS = {'RESOLVED', 'PARTIAL', 'OPEN'}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('file')
    a = ap.parse_args()
    data = json.load(open(a.file, encoding='utf-8'))
    db = dbtool.connect()
    q = lambda sql, *x: db.execute(sql, x).fetchall()  # noqa: E731
    errs = []

    for p in data.get('provisions', []):
        old = q('SELECT text FROM unit WHERE id = ?', p['id'])
        if old and dbtool.norm(old[0][0]) != dbtool.norm(p['text']):
            errs.append(f'provision {p["id"]}: already in the database with other text')
        elif not old:
            db.execute("INSERT INTO unit (id, source_id, kind, locator, heading, text) VALUES (?, ?, 'provision', ?, ?, ?)",
                       (p['id'], p['source'], p['locator'], p.get('heading'), p['text']))

    kind = {r['id']: (r['ukind'], r['skind']) for r in
            q('SELECT u.id, u.kind AS ukind, s.kind AS skind FROM unit u JOIN source s ON s.id = u.source_id')}
    want = {'handbook': lambda k: k[1] == 'handbook' and k[0] in ('sentence', 'paragraph'),
            'law': lambda k: k[1] in ('statute', 'regulation') and k[0] == 'provision',
            'standard': lambda k: k[1] in ('standard', 'model') and k[0] == 'provision'}
    occurrences = {r[0] for r in q('SELECT id FROM occurrence')}
    rows, finds, links = [], [], []
    for f in data['flags']:
        oid = f['id']
        if oid not in occurrences:
            errs.append(f'{oid}: no such flag')
            continue
        if f['verdict'] not in VERDICTS:
            errs.append(f'{oid}: verdict {f["verdict"]!r}')
        rows.append((oid, f['verdict'], f.get('definition'), f.get('effect'), f.get('note')))
        seen = {}
        for side in SIDES:
            x = f.get(side)
            if x is None:
                continue
            if x['finding'] not in FINDINGS:
                errs.append(f'{oid}: {side} finding {x["finding"]!r}')
            finds.append((oid, side, x['finding'], x.get('says')))
            for u in x.get('units', []):
                if u not in kind or not want[side](kind[u]):
                    errs.append(f'{oid}: {u} is not a {side} unit')
                elif u in seen:
                    errs.append(f'{oid}: {u} is cited by both the {seen[u]} and the {side}')
                else:
                    seen[u] = side
                    links.append((oid, u, side if side != 'standard' else 'model' if kind[u][1] == 'model' else 'standard'))
    if errs:
        db.rollback()
        sys.exit('\n'.join(errs))

    ids = [r[0] for r in rows]
    for table in ('grounding_link', 'grounding_finding', 'grounding'):
        db.executemany(f'DELETE FROM {table} WHERE occurrence_id = ?', [(i,) for i in ids])
    db.executemany('INSERT INTO grounding VALUES (?, ?, ?, ?, ?)', rows)
    db.executemany('INSERT INTO grounding_finding VALUES (?, ?, ?, ?)', finds)
    db.executemany('INSERT INTO grounding_link VALUES (?, ?, ?)', links)
    db.commit()
    runs = sorted({r[0] for r in q('SELECT DISTINCT s.run_id FROM occurrence o JOIN statement s ON s.id = o.statement_id '
                                   f'WHERE o.id IN ({",".join("?" * len(ids))})', *ids)}) if ids else []
    for run in runs:
        left = q('SELECT COUNT(*) FROM occurrence o JOIN statement s ON s.id = o.statement_id WHERE s.run_id = ? '
                 'AND o.id NOT IN (SELECT occurrence_id FROM grounding)', run)[0][0]
        print(f'{run}: {left} flags not resolved')
    print(f'{len(rows)} flags resolved, {len(finds)} findings, {len(links)} links, '
          f'{len(data.get("provisions", []))} provisions in the file')


if __name__ == '__main__':
    main()
