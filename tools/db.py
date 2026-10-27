"""The rules database: load it from db/tables/, dump it back, check it, export rules.json.

The database (db/rules.sqlite, not in git) is the master copy of the handbooks' sentences, the
statements, the rule language vocabulary, the laws and the grounding of flagged words. Git holds
one JSONL file per table in db/tables/, so every change shows as a diff and the database can be
rebuilt exactly. Query, insert, update and delete with SQL; then check and dump.

Usage, from the repo root:
    python3 tools/db.py load                 # db/tables/*.jsonl -> db/rules.sqlite
    sqlite3 db/rules.sqlite                  # or Python's sqlite3: query and edit
    python3 tools/db.py check                # every validation in db/README.md; exit 1 on an error
    python3 tools/db.py dump                 # db/rules.sqlite -> db/tables/*.jsonl, then commit
    python3 tools/db.py export --write       # rewrite analysis/passing-rules/*/rules.json from it

Two tables are derived and never dumped: passage_part (which sentences or paragraphs a topic
passage covers, matched by text) and statement_part (each statement split at its keywords).
load and check rebuild them.
"""
import argparse
import collections
import hashlib
import json
import os
import re
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, 'db', 'rules.sqlite')
TABLES = os.path.join(ROOT, 'db', 'tables')
FOLDERS = {'on': 'mto', 'ca': 'ca', 'tx': 'tx'}  # jurisdiction -> analysis/passing-rules folder
# Key order of a statement in each rules.json, so an export writes the file byte for byte.
KEY_ORDER = {
    'on': ('id', 'section', 'type', 'strength', 'strength_from', 'text', 'sources', 'flags', 'note', 'links', 'steps',
           'see'),
    'ca': ('id', 'type', 'strength', 'strength_from', 'text', 'steps', 'sources', 'see', 'flags', 'links', 'note'),
}
KEY_ORDER['tx'] = KEY_ORDER['ca']

# Master tables in load order (parents first), each with the columns that order its dump.
MASTER = [
    ('source', 'id'),
    ('unit', 'id'),
    ('sentence_label', 'unit_id'),
    ('sentence_word', 'unit_id, kind, position'),
    ('vocabulary', 'kind, word'),
    ('statement', 'id'),
    ('statement_step', 'statement_id, position'),
    ('statement_source', 'statement_id, position'),
    ('step_source', 'statement_id, step, position'),
    ('statement_link', 'from_id, position'),
    ('statement_figure', 'statement_id, position'),
    ('statement_basis', 'statement_id, unit_id'),
    ('term', 'id'),
    ('occurrence', 'id'),
    ('grounding', 'occurrence_id'),
    ('grounding_link', 'occurrence_id, unit_id'),
]
DERIVED = ('passage_part', 'statement_part')

KEYWORD = re.compile(r'\b(MUST NOT|SHOULD NOT|MUST|MAY|SHOULD|ONLY IF|IF VIOLATED|DONE WHEN|WHEN|WHILE|UNLESS|UNTIL|'
                     r'BECAUSE|IF|THEN)\b')
MODALS = {'MUST': 'LAW', 'MUST NOT': 'LAW', 'MAY': 'LAW', 'SHOULD': 'ADVICE', 'SHOULD NOT': 'ADVICE'}
INLINE = set('JSRG')


def norm(s):
    s = (s or '').replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()


def connect(path=DB):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    return db


def columns(db, table):
    return [r[1] for r in db.execute(f'PRAGMA table_info({table})')]


# Derived tables ---------------------------------------------------------------------------------

def derive(db):
    db.execute('DELETE FROM passage_part')
    db.execute('DELETE FROM statement_part')
    units = [dict(r) for r in db.execute('SELECT * FROM unit')]
    by_id = {u['id']: u for u in units}
    paras = collections.defaultdict(list)    # source -> paragraphs
    sents = collections.defaultdict(list)    # paragraph -> sentences
    for u in units:
        if u['kind'] == 'paragraph':
            paras[u['source_id']].append(u)
        elif u['kind'] == 'sentence' and u['parent_id']:
            sents[u['parent_id']].append(u)
    rows = set()
    for p in (u for u in units if u['kind'] == 'passage'):
        parts = []
        if p['parent_id']:                   # recorded when the passage names its paragraph or sentence
            parts = [by_id[p['parent_id']]]
        elif p['image']:
            parts = [q for q in paras[p['source_id']] if q['image'] == p['image']]
        else:
            t = norm(p['text'])
            found = [q for q in paras[p['source_id']] if q['image'] is None and norm(q['text']) and
                     (t in norm(q['text']) or norm(q['text']) in t)]
            # Keep one page: the one where the passage matches the most text, then the one under the
            # passage's own heading, so a word like "Stop" elsewhere in the handbook does not count.
            score = collections.Counter()
            for q in found:
                score[q['page']] += min(len(t), len(norm(q['text'])))
                score[q['page']] += 0.5 if q['locator'].split(' › ')[-1] in (p['locator'] or '') else 0
            best = min(score, key=lambda page: (-score[page], page)) if score else None
            parts = [q for q in found if q['page'] == best]
        for q in parts:                      # go down to the sentences the passage holds, if any
            inside = [x for x in sents.get(q['id'], []) if norm(x['text']) in norm(p['text'])]
            for x in inside or [q]:
                rows.add((p['id'], x['id']))
    db.executemany('INSERT INTO passage_part VALUES (?, ?)', sorted(rows))

    parts = []
    for s in db.execute('SELECT id, text FROM statement'):
        parts += [(s['id'], None, i, k, t) for i, (k, t) in enumerate(split(s['text']))]
    for st in db.execute('SELECT statement_id, position, text FROM statement_step'):
        parts += [(st['statement_id'], st['position'], i, k, t) for i, (k, t) in enumerate(split(st['text']))]
    db.executemany('INSERT INTO statement_part VALUES (?, ?, ?, ?, ?)', parts)


def split(text):
    """'a driver MUST stop WHEN x' -> [('HEAD', 'a driver'), ('MUST', 'stop'), ('WHEN', 'x')]."""
    out, last, key = [], 0, 'HEAD'
    for m in KEYWORD.finditer(text):
        if '[?' in text[last:m.start()] and ']' not in text[text.rfind('[?', 0, m.start()):m.start()]:
            continue                          # a keyword inside [?…] is part of the flagged phrase
        out.append((key, text[last:m.start()].strip()))
        key, last = m.group(1), m.end()
    out.append((key, text[last:].strip()))
    return [(k, t) for k, t in out if t or k != 'HEAD']


# Load and dump ---------------------------------------------------------------------------------------

def load(path=DB, tables=TABLES):
    if os.path.exists(path):
        os.remove(path)
    db = connect(path)
    with open(os.path.join(ROOT, 'db', 'schema.sql'), encoding='utf-8') as f:
        db.executescript(f.read())
    db.execute('PRAGMA foreign_keys = OFF')  # a passage may sort before the sentence it names; checked below
    for table, _ in MASTER:
        file = os.path.join(tables, f'{table}.jsonl')
        if not os.path.exists(file):
            continue
        cols = columns(db, table)
        with open(file, encoding='utf-8') as f:
            rows = [json.loads(line) for line in f if line.strip()]
        db.executemany(f'INSERT INTO {table} ({", ".join(cols)}) VALUES ({", ".join("?" * len(cols))})',
                       [tuple(r.get(c) for c in cols) for r in rows])
    db.commit()
    db.execute('PRAGMA foreign_keys = ON')
    broken = db.execute('PRAGMA foreign_key_check').fetchall()
    if broken:
        sys.exit(f'{len(broken)} rows refer to rows that do not exist, for example {tuple(broken[0])}')
    derive(db)
    db.commit()
    return db


def dump(db, tables=TABLES):
    os.makedirs(tables, exist_ok=True)
    counts = {}
    for table, order in MASTER:
        cols = columns(db, table)
        rows = db.execute(f'SELECT {", ".join(cols)} FROM {table} ORDER BY {order}').fetchall()
        with open(os.path.join(tables, f'{table}.jsonl'), 'w', encoding='utf-8') as f:
            for r in rows:
                f.write(json.dumps(dict(zip(cols, r)), ensure_ascii=False) + '\n')
        counts[table] = len(rows)
    return counts


# Export to rules.json -----------------------------------------------------------------------------

def export(db, jurisdiction):
    out = []
    q = db.execute
    for s in q('SELECT * FROM statement WHERE jurisdiction = ? ORDER BY position', (jurisdiction,)):
        d = {'id': s['local_id']}
        if s['section'] is not None:
            d['section'] = s['section']
        d.update(type=s['type'], strength=s['strength'], strength_from=s['strength_from'], text=s['text'])
        d['sources'] = []
        for so in q('SELECT * FROM statement_source WHERE statement_id = ? ORDER BY position', (s['id'],)):
            x = {'id': so['unit_id'].split(':', 2)[2], 'quote': so['quote']}
            for k in ('where_text', 'census_id', 'image'):
                if so[k] is not None:
                    x['where' if k == 'where_text' else k] = so[k]
            d['sources'].append(x)
        d['flags'] = []
        for o in q('SELECT * FROM occurrence WHERE statement_id = ? ORDER BY position', (s['id'],)):
            x = {'code': o['code'], 'span': o['span'], 'note': o['note']}
            if o['note_zh'] is not None:
                x['zh'] = o['note_zh']
            d['flags'].append(x)
        d['note'] = s['note']
        d['links'] = [r['to_id'].split(':', 1)[1] for r in
                      q('SELECT to_id FROM statement_link WHERE from_id = ? ORDER BY position', (s['id'],))]
        steps = q('SELECT * FROM statement_step WHERE statement_id = ? ORDER BY position', (s['id'],)).fetchall()
        if steps:
            d['steps'] = [{'n': st['n'], 'text': st['text'], 'sources': [
                r['unit_id'].split(':', 2)[2] for r in
                q('SELECT unit_id FROM step_source WHERE statement_id = ? AND step = ? ORDER BY position',
                  (s['id'], st['position']))]} for st in steps]
        see = q('SELECT * FROM statement_figure WHERE statement_id = ? ORDER BY position', (s['id'],)).fetchall()
        if see:
            d['see'] = [{'figure': r['figure'], 'source': r['unit_id'].split(':', 2)[2]} for r in see]
        out.append({k: d[k] for k in KEY_ORDER[jurisdiction] if k in d})
    return out


def rules_json(rows):
    return json.dumps(rows, ensure_ascii=False, indent=1)


# Checks ---------------------------------------------------------------------------------------

def unknown(tokens, words):
    """The capitalised tokens left after taking the longest vocabulary phrases from the left."""
    out, i = [], 0
    while i < len(tokens):
        n = next((n for n in range(len(tokens) - i, 0, -1) if ' '.join(tokens[i:i + n]) in words), 0)
        if not n:
            out.append(tokens[i])
        i += n or 1
    return out


def check(db):
    errors, warnings, info = [], [], []
    q = lambda sql, *a: db.execute(sql, a).fetchall()

    for r in q('PRAGMA foreign_key_check'):
        errors.append(f'foreign key: {tuple(r)}')

    # Local copies of laws and standards: hash, and every provision word for word.
    texts = {}
    for s in q("SELECT * FROM source WHERE kind != 'handbook' AND path IS NOT NULL"):
        full = os.path.join(ROOT, s['path'])
        if not os.path.exists(full):
            warnings.append(f'source {s["id"]}: no local copy at {s["path"]}; its provisions were not checked')
            continue
        raw = open(full, 'rb').read()
        if s['sha256'] and hashlib.sha256(raw).hexdigest() != s['sha256']:
            errors.append(f'source {s["id"]}: sha256 of {s["path"]} does not match')
        texts[s['id']] = norm(raw.decode('utf-8', 'replace'))
    for u in q("SELECT * FROM unit WHERE kind = 'provision'"):
        if u['source_id'] in texts and norm(u['text']) not in texts[u['source_id']]:
            errors.append(f'unit {u["id"]}: not found word for word in its source')

    # Statements and their sources.
    for r in q("SELECT ss.statement_id, ss.unit_id, ss.quote, u.text, u.kind FROM statement_source ss "
               "JOIN unit u ON u.id = ss.unit_id"):
        if r['kind'] != 'passage':
            errors.append(f'{r["statement_id"]}: source {r["unit_id"]} is not a passage')
        elif r['quote'] and norm(r['quote']) not in norm(r['text']):
            warnings.append(f'{r["statement_id"]}: quote is not word for word in {r["unit_id"]}')
    for r in q("SELECT id FROM unit WHERE kind = 'passage' AND id NOT IN (SELECT passage_id FROM passage_part)"):
        warnings.append(f'{r["id"]}: passage matches no handbook sentence or paragraph')

    words = {r['word'] for r in q('SELECT word FROM vocabulary')}
    for s in q('SELECT * FROM statement'):
        modals = [p['keyword'] for p in q("SELECT keyword FROM statement_part WHERE statement_id = ? AND step IS NULL "
                                          "AND keyword IN ('MUST', 'MUST NOT', 'MAY', 'SHOULD', 'SHOULD NOT')", s['id'])]
        want = {MODALS[m] for m in modals}
        if s['type'] in ('RULE', 'EXCEPTION') and modals:
            if len(want) > 1:
                warnings.append(f'{s["id"]}: mixes law and advice modals {modals}')
            elif s['strength'] not in want:
                errors.append(f'{s["id"]}: strength {s["strength"]} but modal {modals[0]}')
        if s['type'] in ('DEFINE', 'FACT') and s['strength'] is not None:
            errors.append(f'{s["id"]}: a {s["type"]} has strength {s["strength"]}')
        for cap in re.findall(r'\b[A-Z]{2,}(?: [A-Z]{2,})*\b', re.sub(r'\[\?[^\]]*\]|"[^"]*"', '', s['text'])):
            for w in unknown(cap.split(), words):
                warnings.append(f'{s["id"]}: "{w}" is not in the vocabulary')
    # A flag's span must be words of the statement, its steps, or the passages they cite.
    for o in q('SELECT * FROM occurrence'):
        where = [r[0] for r in q("SELECT text FROM statement WHERE id = ?1 UNION ALL "
                                 "SELECT text FROM statement_step WHERE statement_id = ?1 UNION ALL "
                                 "SELECT u.text FROM statement_source x JOIN unit u ON u.id = x.unit_id "
                                 "WHERE x.statement_id = ?1 UNION ALL "
                                 "SELECT u.text FROM step_source x JOIN unit u ON u.id = x.unit_id "
                                 "WHERE x.statement_id = ?1", o['statement_id'])]
        if o['code'] in INLINE and not any(norm(o['span']) in norm(t) for t in where):
            warnings.append(f'{o["id"]}: its span is not in the statement, its steps or its sources')
    for r in q("SELECT l.from_id, l.to_id, l.kind, s.text FROM statement_link l JOIN statement s ON s.id = l.from_id"):
        local = r['to_id'].split(':', 1)[1]
        if r['kind'] != 'REFERS TO' and f'{r["kind"]} {local}' not in r['text']:
            errors.append(f'{r["from_id"]}: link {r["kind"]} {local} is not in its text')

    # The law behind statements, and groundings: each link points at the right kind of unit.
    for r in q("SELECT b.statement_id, b.unit_id FROM statement_basis b JOIN unit u ON u.id = b.unit_id "
               "WHERE u.kind != 'provision'"):
        errors.append(f'{r["statement_id"]}: basis {r["unit_id"]} is not a provision')
    want = {'law': ('statute', 'regulation'), 'standard': ('standard',), 'model': ('model',), 'handbook': ('handbook',)}
    for r in q("SELECT l.occurrence_id, l.unit_id, l.role, u.kind, s.kind AS source_kind FROM grounding_link l "
               "JOIN unit u ON u.id = l.unit_id JOIN source s ON s.id = u.source_id"):
        if r['source_kind'] not in want[r['role']] or (r['role'] != 'handbook' and r['kind'] != 'provision'):
            errors.append(f'grounding {r["occurrence_id"]}: {r["unit_id"]} is not a {r["role"]} provision')
    for g in q("SELECT g.* FROM grounding g WHERE g.status LIKE 'LAW_%' AND NOT EXISTS "
               "(SELECT 1 FROM grounding_link l WHERE l.occurrence_id = g.occurrence_id AND l.role = 'law')"):
        errors.append(f'grounding {g["occurrence_id"]}: {g["status"]} needs a law provision')
    for g in q("SELECT g.* FROM grounding g WHERE g.status = 'STANDARD' AND NOT EXISTS "
               "(SELECT 1 FROM grounding_link l WHERE l.occurrence_id = g.occurrence_id "
               "AND l.role IN ('standard', 'model'))"):
        errors.append(f'grounding {g["occurrence_id"]}: STANDARD needs a standard or model')

    # rules.json must equal the database.
    for jur, folder in FOLDERS.items():
        path = os.path.join(ROOT, 'analysis', 'passing-rules', folder, 'rules.json')
        if os.path.exists(path) and q('SELECT 1 FROM statement WHERE jurisdiction = ? LIMIT 1', jur):
            if open(path, encoding='utf-8').read() != rules_json(export(db, jur)):
                errors.append(f'{os.path.relpath(path, ROOT)} differs from the database; run export --write')

    # Coverage, reported, never an error.
    for jur in FOLDERS:
        n = q("SELECT COUNT(*) FROM statement WHERE jurisdiction = ?", jur)[0][0]
        if not n:
            continue
        flags = q("SELECT COALESCE(g.status, 'not grounded') AS st, COUNT(*) AS n FROM occurrence o "
                  "JOIN statement s ON s.id = o.statement_id LEFT JOIN grounding g ON g.occurrence_id = o.id "
                  "WHERE s.jurisdiction = ? GROUP BY st ORDER BY st", jur)
        info.append(f'{jur}: {n} statements; flags: ' + ', '.join(f'{r["st"]} {r["n"]}' for r in flags))
    for jur in FOLDERS:
        law = q("SELECT COUNT(*) FROM statement WHERE jurisdiction = ? AND strength = 'LAW'", jur)[0][0]
        if not law or not q("SELECT 1 FROM statement_basis b JOIN statement s ON s.id = b.statement_id "
                            "WHERE s.jurisdiction = ? LIMIT 1", jur):
            continue
        bare = q("SELECT COUNT(*) FROM law_without_basis WHERE jurisdiction = ?", jur)[0][0]
        advice = q("SELECT COUNT(DISTINCT statement_id) FROM advice_with_law WHERE jurisdiction = ?", jur)[0][0]
        info.append(f'{jur}: {law - bare} of {law} LAW statements cite a provision (view law_without_basis); '
                    f'{advice} ADVICE statements have a provision behind them (view advice_with_law)')
    used = q("SELECT COUNT(DISTINCT u.id) FROM unit u JOIN sentence_label l ON l.unit_id = u.id "
             "JOIN unit_use x ON x.unit_id = u.id")[0][0]
    total = q("SELECT COUNT(*) FROM sentence_label")[0][0]
    passing = q("SELECT COUNT(*) FROM sentence_label WHERE passing = 1")[0][0]
    unused = q("SELECT COUNT(*) FROM passing_sentence_unused")[0][0]
    for jur, folder in FOLDERS.items():
        idle = q("SELECT COUNT(*) FROM passage_unused WHERE source_id = ?", f'{folder}-handbook')[0][0]
        if idle:
            info.append(f'{jur}: {idle} topic passages are cited by no statement (view passage_unused)')
    if total:
        info.append(f'on: {used} of {total} handbook sentences are cited; {passing - unused} of the {passing} the '
                    f'census marked as about passing are cited, {unused} are not (view passing_sentence_unused)')
    return errors, warnings, info


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('command', choices=['load', 'dump', 'check', 'export'])
    ap.add_argument('--db', default=DB)
    ap.add_argument('--write', action='store_true', help='export: write the rules.json files')
    a = ap.parse_args()

    if a.command == 'load':
        db = load(a.db)
        counts = {t: db.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0] for t, _ in MASTER + [(d, '') for d in DERIVED]}
        print(f'loaded {os.path.relpath(a.db, ROOT)}: ' + ', '.join(f'{t} {n}' for t, n in counts.items()))
        return
    if not os.path.exists(a.db):
        sys.exit(f'{a.db} does not exist; run load first')
    db = connect(a.db)
    if a.command == 'dump':
        counts = dump(db)
        print('dumped db/tables/: ' + ', '.join(f'{t} {n}' for t, n in counts.items()))
    elif a.command == 'check':
        derive(db)
        db.commit()
        errors, warnings, info = check(db)
        for line in info:
            print(line)
        for w in warnings:
            print('warning:', w)
        for e in errors:
            print('error:', e)
        print(f'{len(errors)} errors, {len(warnings)} warnings')
        sys.exit(1 if errors else 0)
    elif a.command == 'export':
        for jur, folder in FOLDERS.items():
            rows = export(db, jur)
            if not rows:
                continue
            path = os.path.join(ROOT, 'analysis', 'passing-rules', folder, 'rules.json')
            same = os.path.exists(path) and open(path, encoding='utf-8').read() == rules_json(rows)
            if a.write and not same:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(rules_json(rows))
            print(f'{os.path.relpath(path, ROOT)}: {len(rows)} statements, '
                  + ('same as the database' if same else 'written' if a.write else 'differs from the database'))


if __name__ == '__main__':
    main()
