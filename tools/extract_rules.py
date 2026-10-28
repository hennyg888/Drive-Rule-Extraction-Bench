"""Stage 4, formalization: fill the extraction prompt with a selection's passages, then store the statements.

    python3 tools/extract_rules.py render on-passing-1 --selection on-passing-select-1
        Writes runs/on-passing-1/messages.json (the prompt's system and user messages, as
        provenance/scripts/render_prompt.py writes them), prompt.md (the same, readable) and
        images.txt (the figure images to show the model), reading the passages from the database.
        A model answers into runs/on-passing-1/output.json: {"statements": [...]}.
    python3 tools/extract_rules.py check on-passing-1
        Checks the answer against the prompt's output format and the passages. Exit 1 on a problem.
    python3 tools/extract_rules.py load on-passing-1 --model NAME --date YYYY-MM-DD
        Checks, then writes the run and its statements to the database, replacing an earlier load of it.
"""
import argparse
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db as dbtool  # noqa: E402

PROMPT = os.path.join('prompts', 'extract-rules.md')
TYPES = {'DEFINE', 'FACT', 'RULE', 'PROCEDURE', 'EXCEPTION'}
CODES = set('JSRGMDVX')
KEYS = {'id', 'type', 'strength', 'strength_from', 'text', 'sources', 'flags', 'links', 'note'}
JURISDICTION = {'mto-handbook': 'on', 'ca-handbook': 'ca', 'tx-handbook': 'tx'}


def run_dir(run):
    return os.path.join(dbtool.ROOT, 'runs', run)


def passages(db, selection):
    q = lambda sql, *x: db.execute(sql, x).fetchall()  # noqa: E731
    titles = {r['id']: r['title'] for r in q('SELECT p.* FROM page p JOIN run r ON r.source_id = p.source_id WHERE r.id = ?',
                                               selection)}
    out = []
    for r in q('SELECT l.local_id, u.* FROM selection l JOIN unit u ON u.id = l.unit_id WHERE l.run_id = ? '
               'ORDER BY l.position', selection):
        title = titles[r['page']]
        sec = r['locator'][len(title) + 3:] if r['locator'].startswith(title + ' › ') else ''
        p = {'id': r['local_id'], 'page': title, 'sec': sec, 'kind': 'figure' if r['image'] else 'text', 'text': r['text']}
        if r['image']:
            if r['heading']:
                p['cap'] = r['heading']
            p['image'] = r['image']
        out.append((p, r['id']))
    return out


def render(a):
    db = dbtool.connect()
    sel = db.execute("SELECT * FROM run WHERE id = ? AND stage = 'select'", (a.selection,)).fetchone()
    if not sel:
        sys.exit(f'{a.selection} is not a selection run')
    src = db.execute('SELECT * FROM source WHERE id = ?', (sel['source_id'],)).fetchone()
    scope = open(os.path.join(dbtool.ROOT, 'prompts', 'topics', f'{sel["topic"]}.txt'), encoding='utf-8').read().strip()
    ps = passages(db, a.selection)
    raw = open(os.path.join(dbtool.ROOT, PROMPT), encoding='utf-8').read()
    head, rest = raw.split('\n<!-- SYSTEM -->\n', 1)
    system, user = rest.split('\n<!-- USER -->\n', 1)
    system, user = system.strip() + '\n', user.strip() + '\n'
    handbook = a.handbook or f'{src["title"]} ({src["version"] or "offline copy"})'
    lines = '\n'.join(json.dumps(p, ensure_ascii=False) for p, _ in ps)
    user = (user.replace('{{HANDBOOK}}', handbook).replace('{{TOPIC}}', sel['topic'])
                .replace('{{TOPIC_SCOPE}}', scope).replace('{{PASSAGES}}', lines))
    assert '{{' not in user, 'unfilled slot in the user message'
    d = run_dir(a.run)
    os.makedirs(d, exist_ok=True)
    msg = {'prompt': PROMPT, 'prompt_sha256': hashlib.sha256(raw.encode('utf-8')).hexdigest(), 'selection': a.selection,
           'n_passages': len(ps), 'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}]}
    json.dump(msg, open(os.path.join(d, 'messages.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(d, 'prompt.md'), 'w', encoding='utf-8').write('# SYSTEM\n\n' + system + '\n# USER\n\n' + user)
    folder = src['path'] or ''
    open(os.path.join(d, 'images.txt'), 'w', encoding='utf-8').write(
        ''.join(f'{p["id"]} {os.path.join(folder, p["image"])}\n' for p, _ in ps if p.get('image')))
    print(f'{a.run}: {len(ps)} passages from {a.selection} (prompt sha256 {msg["prompt_sha256"][:12]})')


def problems(statements, ps):
    errs = []
    text = {p['id']: p['text'] for p, _ in ps}
    figure = {p['id'] for p, _ in ps if p['kind'] == 'figure'}
    ids = [s.get('id') for s in statements]
    for s in statements:
        sid = s.get('id')
        if not KEYS <= set(s) or not set(s) <= KEYS | {'steps', 'see'}:
            errs.append(f'{sid}: keys {sorted(s)}')
            continue
        if ids.count(sid) > 1:
            errs.append(f'{sid}: id used twice')
        if s['type'] not in TYPES:
            errs.append(f'{sid}: type {s["type"]!r}')
        if s['strength'] not in ('LAW', 'ADVICE', None) or (s['strength'] is None) != (s['strength_from'] is None):
            errs.append(f'{sid}: strength {s["strength"]!r} with strength_from {s["strength_from"]!r}')
        if not s['sources']:
            errs.append(f'{sid}: no sources')
        for so in s['sources']:
            if so.get('id') not in text:
                errs.append(f'{sid}: source {so.get("id")!r} is not a passage')
            elif dbtool.norm(so.get('quote')) != dbtool.norm(text[so['id']]):
                errs.append(f'{sid}: the quote of {so["id"]} is not the passage\'s full text')
        for st in s.get('steps', []):
            for x in st.get('sources', []):
                if x not in text:
                    errs.append(f'{sid}: step {st.get("n")} source {x!r} is not a passage')
        if (s['type'] == 'PROCEDURE') != bool(s.get('steps')):
            errs.append(f'{sid}: steps are for a PROCEDURE, and a PROCEDURE has them')
        for se in s.get('see', []):
            if se.get('source') not in figure:
                errs.append(f'{sid}: see {se.get("source")!r} is not a figure passage')
        for f in s['flags']:
            if f.get('code') not in CODES or not f.get('span') or not f.get('note'):
                errs.append(f'{sid}: flag {f!r}')
        for to in s['links']:
            if to not in ids:
                errs.append(f'{sid}: links to {to!r}, which it did not write')
            elif not re.search(rf'\b(EXCEPTION TO|SPECIALIZES) {re.escape(to)}\b', s['text']):
                errs.append(f'{sid}: links to {to}, but its text does not name it')
    return errs


def answer(run):
    path = os.path.join(run_dir(run), 'output.json')
    if not os.path.exists(path):
        sys.exit(f'no {os.path.relpath(path, dbtool.ROOT)}')
    msg = json.load(open(os.path.join(run_dir(run), 'messages.json'), encoding='utf-8'))
    return msg, json.load(open(path, encoding='utf-8'))['statements']


def check(a):
    msg, statements = answer(a.run)
    errs = problems(statements, passages(dbtool.connect(), msg['selection']))
    for e in errs:
        print(e)
    print(f'{len(statements)} statements, {len(errs)} problems')
    sys.exit(1 if errs else 0)


def load(a):
    msg, statements = answer(a.run)
    db = dbtool.connect()
    ps = passages(db, msg['selection'])
    errs = problems(statements, ps)
    if errs:
        sys.exit(f'{len(errs)} problems; run check')
    unit = {p['id']: uid for p, uid in ps}
    sel = db.execute('SELECT * FROM run WHERE id = ?', (msg['selection'],)).fetchone()
    jur = JURISDICTION[sel['source_id']]
    sid = lambda local: f'{a.run}:{local}'  # noqa: E731

    old = [r[0] for r in db.execute('SELECT id FROM statement WHERE run_id = ?', (a.run,))]
    db.execute('PRAGMA foreign_keys = OFF')
    for table, col in (('grounding_link', 'occurrence_id'), ('grounding', 'occurrence_id')):
        db.execute(f'DELETE FROM {table} WHERE {col} IN (SELECT id FROM occurrence WHERE statement_id IN '
                   f'(SELECT id FROM statement WHERE run_id = ?))', (a.run,))
    for table, col in (('occurrence', 'statement_id'), ('statement_law_ref', 'statement_id'), ('statement_law', 'statement_id'),
                       ('statement_basis', 'statement_id'), ('statement_figure', 'statement_id'), ('statement_link', 'from_id'),
                       ('step_source', 'statement_id'), ('statement_source', 'statement_id'), ('statement_step', 'statement_id'),
                       ('statement_part', 'statement_id')):
        db.execute(f'DELETE FROM {table} WHERE {col} IN (SELECT id FROM statement WHERE run_id = ?)', (a.run,))
    db.execute('DELETE FROM statement WHERE run_id = ?', (a.run,))
    db.execute('DELETE FROM run WHERE id = ?', (a.run,))
    db.execute('INSERT INTO run (id, stage, source_id, topic, input_run, prompt, prompt_sha256, model, date, note) '
               'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
               (a.run, 'extract', sel['source_id'], sel['topic'], sel['id'], msg['prompt'], msg['prompt_sha256'],
                a.model, a.date, a.note))
    for pos, s in enumerate(statements):
        db.execute('INSERT INTO statement (id, run_id, jurisdiction, local_id, position, topic, section, type, strength, '
                   'strength_from, text, note) VALUES (?, ?, ?, ?, ?, ?, NULL, ?, ?, ?, ?, ?)',
                   (sid(s['id']), a.run, jur, s['id'], pos, sel['topic'], s['type'], s['strength'], s['strength_from'],
                    s['text'], s['note']))
        db.executemany('INSERT INTO statement_source (statement_id, position, unit_id, quote) VALUES (?, ?, ?, ?)',
                       [(sid(s['id']), i, unit[so['id']], so['quote']) for i, so in enumerate(s['sources'])])
        for i, st in enumerate(s.get('steps', [])):
            db.execute('INSERT INTO statement_step VALUES (?, ?, ?, ?)', (sid(s['id']), st['n'], i, st['text']))
            db.executemany('INSERT INTO step_source VALUES (?, ?, ?, ?)',
                           [(sid(s['id']), i, j, unit[x]) for j, x in enumerate(st.get('sources', []))])
        for i, to in enumerate(s['links']):
            kind = next((k for k in ('EXCEPTION TO', 'SPECIALIZES') if f'{k} {to}' in s['text']), 'REFERS TO')
            db.execute('INSERT INTO statement_link VALUES (?, ?, ?, ?)', (sid(s['id']), i, sid(to), kind))
        db.executemany('INSERT INTO statement_figure VALUES (?, ?, ?, ?)',
                       [(sid(s['id']), i, unit[se['source']], se['figure']) for i, se in enumerate(s.get('see', []))])
        for i, f in enumerate(s['flags']):
            term = f'{jur}:{f["span"].lower()}' if f['code'] == 'J' else None
            if term:
                db.execute('INSERT OR IGNORE INTO term VALUES (?, ?, ?)', (term, jur, f['span'].lower()))
            db.execute('INSERT INTO occurrence VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                       (f'{sid(s["id"])}|{f["code"]}|{f["span"]}', sid(s['id']), i, f['code'], f['span'], f['note'],
                        f.get('zh'), term))
    db.execute('PRAGMA foreign_keys = ON')
    broken = db.execute('PRAGMA foreign_key_check').fetchall()
    if broken:
        db.rollback()
        sys.exit(f'{len(broken)} rows refer to rows that do not exist, for example {tuple(broken[0])}')
    dbtool.derive(db)
    db.commit()
    print(f'{a.run}: {len(statements)} statements written' + (f' (replacing {len(old)})' if old else ''))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='command', required=True)
    p = sub.add_parser('render')
    p.add_argument('run')
    p.add_argument('--selection', required=True)
    p.add_argument('--handbook', help='the handbook name the prompt shows')
    p = sub.add_parser('check')
    p.add_argument('run')
    p = sub.add_parser('load')
    p.add_argument('run')
    p.add_argument('--model', required=True)
    p.add_argument('--date', required=True)
    p.add_argument('--note')
    a = ap.parse_args()
    {'render': render, 'check': check, 'load': load}[a.command](a)


if __name__ == '__main__':
    main()
