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
    python3 tools/db.py export --write       # rewrite rules.json and passing-rules-law.md from it

Statements belong to runs (table run). Only the statements of a run with rules_json = 1 are a
topic's rules.json; an extraction run of the pipeline (pipeline/PIPELINE.md) is kept beside it.

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
    ('run', 'id'),
    ('page', 'source_id, position'),
    ('unit', 'id'),
    ('unit_tag', 'unit_id'),
    ('unit_topic', 'unit_id, topic'),
    ('unit_vague', 'unit_id, position'),
    ('selection', 'run_id, position'),
    ('vocabulary', 'kind, word'),
    ('statement', 'id'),
    ('statement_step', 'statement_id, position'),
    ('statement_source', 'statement_id, position'),
    ('step_source', 'statement_id, step, position'),
    ('statement_link', 'from_id, position'),
    ('statement_figure', 'statement_id, position'),
    ('statement_basis', 'statement_id, unit_id'),
    ('statement_law', 'statement_id, position'),
    ('statement_law_ref', 'statement_id, position, unit_id'),
    ('term', 'id'),
    ('occurrence', 'id'),
    ('grounding', 'occurrence_id'),
    ('grounding_finding', 'occurrence_id, side'),
    ('grounding_link', 'occurrence_id, unit_id'),
]
DERIVED = ('passage_part', 'statement_part')

KEYWORD = re.compile(r'\b(MUST NOT|SHOULD NOT|MUST|MAY|SHOULD|ONLY IF|IF VIOLATED|DONE WHEN|WHEN|WHILE|UNLESS|UNTIL|'
                     r'BECAUSE|IF|THEN)\b')
IN_RULES_JSON = 'run_id IN (SELECT id FROM run WHERE rules_json = 1)'
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
    for s in q(f'SELECT * FROM statement WHERE jurisdiction = ? AND {IN_RULES_JSON} ORDER BY position', (jurisdiction,)):
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


LAW_PAGE_TITLE = {'on': 'Ontario passing rules, with the law added'}


def outputs(db):
    """Every file made from the database, as {path from the repo root: content}."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import render_law_md
    out = {}
    for jur, folder in FOLDERS.items():
        base = os.path.join('analysis', 'passing-rules', folder)
        rows = export(db, jur)
        if rows:
            out[os.path.join(base, 'rules.json')] = rules_json(rows)
        if db.execute('SELECT 1 FROM statement_law g JOIN statement s ON s.id = g.statement_id '
                      f'WHERE s.jurisdiction = ? AND s.{IN_RULES_JSON} LIMIT 1', (jur,)).fetchone():
            out[os.path.join(base, 'passing-rules-law.md')] = render_law_md.render(db, jur, LAW_PAGE_TITLE[jur], ROOT, base)
    return out


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

    # Statements and their sources. A statement of a run that read a selection cites sentences of the
    # selected paragraphs, or selected figures; one of an earlier run cites its passages.
    for r in q("SELECT s.id FROM statement s WHERE s.id NOT IN (SELECT statement_id FROM statement_source)"):
        errors.append(f'{r["id"]}: cites no source')
    for r in q("SELECT c.statement_id, c.step, c.unit_id, c.quote, u.text, u.kind, u.image, x.input_run, "
               "EXISTS (SELECT 1 FROM selection l WHERE l.run_id = x.input_run "
               "        AND l.unit_id = CASE u.kind WHEN 'sentence' THEN u.parent_id ELSE u.id END) AS selected "
               "FROM (SELECT statement_id, NULL AS step, unit_id, quote FROM statement_source "
               "      UNION ALL SELECT statement_id, step, unit_id, NULL FROM step_source) c "
               "JOIN unit u ON u.id = c.unit_id JOIN statement s ON s.id = c.statement_id "
               "JOIN run x ON x.id = s.run_id"):
        where = f'{r["statement_id"]}' + ('' if r['step'] is None else f' step {r["step"]}')
        if not r['input_run'] and r['kind'] != 'passage':
            errors.append(f'{where}: source {r["unit_id"]} is not a passage')
        elif r['input_run'] and not (r['selected'] and (r['kind'] == 'sentence' or r['image'])):
            errors.append(f'{where}: source {r["unit_id"]} is not a sentence or figure of its run\'s selection')
        elif r['quote'] and norm(r['quote']) not in norm(r['text']):
            warnings.append(f'{where}: quote is not word for word in {r["unit_id"]}')
    for r in q("SELECT id FROM unit WHERE kind = 'passage' AND id NOT IN (SELECT passage_id FROM passage_part)"):
        warnings.append(f'{r["id"]}: passage matches no handbook sentence or paragraph')
    for r in q("SELECT p.id, p.text, p.image, u.id AS uid, u.text AS utext, u.image AS uimage FROM unit p "
               "JOIN unit u ON u.id = p.parent_id WHERE p.kind = 'passage'"):
        if (r['image'] or r['uimage']) and r['image'] != r['uimage']:
            errors.append(f'{r["id"]}: names {r["uid"]}, which is not its figure')
        elif not r['image'] and norm(r['text']) not in norm(r['utext']) and norm(r['utext']) not in norm(r['text']):
            errors.append(f'{r["id"]}: names {r["uid"]}, whose text it does not share')

    # Runs read the stage before theirs; tags only describe their unit; a selection holds paragraphs.
    order = {'tag': None, 'select': 'tag', 'extract': 'select'}
    for r in q('SELECT r.*, i.stage AS input_stage, i.source_id AS input_source FROM run r '
               'LEFT JOIN run i ON i.id = r.input_run'):
        if r['input_run'] and (r['input_stage'] != order[r['stage']] or r['input_source'] != r['source_id']):
            errors.append(f'run {r["id"]}: a {r["stage"]} run cannot read {r["input_run"]}')
    for r in q('SELECT s.id, s.run_id FROM statement s JOIN run r ON r.id = s.run_id WHERE r.stage != \'extract\''):
        errors.append(f'{r["id"]}: its run {r["run_id"]} is not an extraction')
    for t in q('SELECT t.*, u.kind, u.image, r.stage, r.source_id, u.source_id AS unit_source FROM unit_tag t '
               'JOIN unit u ON u.id = t.unit_id JOIN run r ON r.id = t.run_id'):
        if t['stage'] != 'tag' or t['source_id'] != t['unit_source']:
            errors.append(f'tag {t["unit_id"]}: run {t["run_id"]} is not a tagging run of its handbook')
        if not (t['kind'] == 'sentence' or (t['kind'] == 'paragraph' and t['image'])):
            errors.append(f'tag {t["unit_id"]}: only sentences and figures are tagged')
        if (t['type'] == 'FIGURE') != bool(t['image']):
            errors.append(f'tag {t["unit_id"]}: type FIGURE is for figures only, and every figure has it')
    for v in q('SELECT v.*, u.text FROM unit_vague v JOIN unit u ON u.id = v.unit_id'):
        if v['span'] not in v['text']:
            errors.append(f'tag {v["unit_id"]}: vague span "{v["span"]}" is not words of the sentence')
    for r in q("SELECT l.*, u.kind, u.source_id AS unit_source, x.stage, x.source_id FROM selection l "
               "JOIN unit u ON u.id = l.unit_id JOIN run x ON x.id = l.run_id"):
        if r['stage'] != 'select' or r['kind'] != 'paragraph' or r['unit_source'] != r['source_id']:
            errors.append(f'selection {r["run_id"]} {r["local_id"]}: {r["unit_id"]} is not a paragraph of its handbook')

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
    # A flag's span must be words of the statement, its steps, or the passages they cite. An X or V flag
    # may quote another passage instead.
    for o in q('SELECT * FROM occurrence'):
        where = [r[0] for r in q("SELECT text FROM statement WHERE id = ?1 UNION ALL "
                                 "SELECT text FROM statement_step WHERE statement_id = ?1 UNION ALL "
                                 "SELECT u.text FROM statement_source x JOIN unit u ON u.id = x.unit_id "
                                 "WHERE x.statement_id = ?1 UNION ALL "
                                 "SELECT u.text FROM step_source x JOIN unit u ON u.id = x.unit_id "
                                 "WHERE x.statement_id = ?1", o['statement_id'])]
        if o['code'] in INLINE | {'M', 'D'} and not any(norm(o['span']) in norm(t) for t in where):
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
    # Each resolved flag says what the handbook and the law say about it; a finding other than SILENT
    # cites that side's sentences or provisions, SILENT cites none; a verdict other than OPEN rests on
    # a finding that defines or states, and gives the reading.
    side_of = {'law': 'law', 'standard': 'standard', 'model': 'standard', 'handbook': 'handbook'}
    cited = collections.defaultdict(set)
    for r in q('SELECT occurrence_id, role FROM grounding_link'):
        cited[r['occurrence_id']].add(side_of[r['role']])
    found = collections.defaultdict(dict)
    for r in q('SELECT * FROM grounding_finding'):
        found[r['occurrence_id']][r['side']] = r['finding']
    for g in q('SELECT * FROM grounding'):
        oid, f = g['occurrence_id'], found[g['occurrence_id']]
        for side in ('handbook', 'law'):
            if side not in f:
                errors.append(f'grounding {oid}: no {side} finding')
        for side in set(f) | cited[oid]:
            if f.get(side, 'SILENT') == 'SILENT' and side in cited[oid]:
                errors.append(f'grounding {oid}: cites the {side} but finds it {f.get(side, "missing")}')
            elif f.get(side, 'SILENT') != 'SILENT' and side not in cited[oid]:
                errors.append(f'grounding {oid}: {side} {f[side]} cites no {side} source')
        if g['verdict'] != 'OPEN' and not ({'DEFINES', 'STATES'} & set(f.values()) and g['definition']):
            errors.append(f'grounding {oid}: {g["verdict"]} needs a finding that defines or states, and a definition')

    # The law added under statements. Each line is law: law modals only. It cites at least one
    # provision of a statute or regulation that is not a penalty, every provision it cites is a
    # basis row of its statement, a penalty it states cites one, and it does not mark open a word the
    # law settles.
    basis = collections.defaultdict(dict)
    for r in q('SELECT b.*, s.kind AS source_kind FROM statement_basis b JOIN unit u ON u.id = b.unit_id '
               'JOIN source s ON s.id = u.source_id'):
        basis[r['statement_id']][r['unit_id']] = r
    for r in q('SELECT * FROM statement_law'):
        name = f'{r["statement_id"]} law line {r["position"]}'
        modals = [k for k, _ in split(r['text']) if k in MODALS]
        if not modals or any(MODALS[m] != 'LAW' for m in modals):
            errors.append(f'{name}: needs law modals only (MUST, MUST NOT, MAY), has {modals or "none"}')
        refs = [x[0] for x in q('SELECT unit_id FROM statement_law_ref WHERE statement_id = ? AND position = ?',
                                r['statement_id'], r['position'])]
        mine = basis[r['statement_id']]
        for u in refs:
            if u not in mine:
                errors.append(f'{name}: cites {u}, which is not a basis row of its statement')
        if not any(u in mine and mine[u]['relation'] != 'PENALTY' and mine[u]['source_kind'] in ('statute', 'regulation')
                   for u in refs):
            errors.append(f'{name}: cites no provision of a statute or regulation other than a penalty')
        if 'IF VIOLATED' in r['text'] and not any(u in mine and mine[u]['relation'] == 'PENALTY' for u in refs):
            errors.append(f'{name}: states a penalty but cites no PENALTY provision')
        for cap in re.findall(r'\b[A-Z]{2,}(?: [A-Z]{2,})*\b', re.sub(r'\[\?[^\]]*\]|"[^"]*"', '', r['text'])):
            for w in unknown(cap.split(), words):
                warnings.append(f'{name}: "{w}" is not in the vocabulary')
    for o in q("SELECT o.*, f.finding FROM occurrence o JOIN grounding_finding f ON f.occurrence_id = o.id "
               "WHERE f.side = 'law' AND f.finding IN ('DEFINES', 'STATES') AND o.code IN ('J', 'S', 'R', 'G')"):
        for r in q('SELECT position, text FROM statement_law WHERE statement_id = ?', o['statement_id']):
            if f'[?{o["span"]}]' in r['text']:
                errors.append(f'{o["id"]}: the law settles it ({o["finding"]}), but law line {r["position"]} marks it open')

    # The files made from the database must equal it.
    for path, content in outputs(db).items():
        full = os.path.join(ROOT, path)
        if not os.path.exists(full) or open(full, encoding='utf-8').read() != content:
            errors.append(f'{path} differs from the database; run export --write')

    # Coverage, reported, never an error.
    for jur in FOLDERS:
        for r in q("SELECT * FROM run WHERE stage = 'extract' AND id IN (SELECT run_id FROM statement WHERE jurisdiction = ?) "
                   "ORDER BY rules_json DESC, id", jur):
            info += coverage(q, r)
    for jur, folder in FOLDERS.items():
        idle = q("SELECT COUNT(*) FROM passage_unused WHERE source_id = ?", f'{folder}-handbook')[0][0]
        if idle:
            info.append(f'{jur}: {idle} topic passages are cited by no statement (view passage_unused)')
    for r in q("SELECT r.id, COUNT(t.unit_id) AS n FROM run r JOIN unit_tag t ON t.run_id = r.id GROUP BY r.id"):
        topics = q("SELECT p.topic, COUNT(*) AS n FROM unit_topic p JOIN unit_tag t ON t.unit_id = p.unit_id "
                   "WHERE t.run_id = ? GROUP BY p.topic", r['id'])
        info.append(f'{r["id"]}: {r["n"]} sentences and figures tagged' +
                    ''.join(f'; {x["n"]} about {x["topic"]}' for x in topics))
    return errors, warnings, info


def coverage(q, run):
    """What check reports about one extraction run: its flags, its law, and the tagged text it leaves out."""
    rid, out = run['id'], []
    n = q("SELECT COUNT(*) FROM statement WHERE run_id = ?", rid)[0][0]
    flags = q("SELECT COALESCE(g.verdict, 'not resolved') AS st, COUNT(*) AS n FROM occurrence o "
              "JOIN statement s ON s.id = o.statement_id LEFT JOIN grounding g ON g.occurrence_id = o.id "
              "WHERE s.run_id = ? GROUP BY st ORDER BY st", rid)
    out.append(f'{rid}: {n} statements; flags: ' + (', '.join(f'{r["st"]} {r["n"]}' for r in flags) or 'none'))
    for side in ('handbook', 'law'):
        by = q("SELECT f.finding, COUNT(*) AS n FROM grounding_finding f JOIN occurrence o ON o.id = f.occurrence_id "
               "JOIN statement s ON s.id = o.statement_id WHERE s.run_id = ? AND f.side = ? GROUP BY f.finding "
               "ORDER BY f.finding", rid, side)
        if by:
            out.append(f'{rid}: what the {side} says about the flags: ' + ', '.join(f'{r["finding"]} {r["n"]}' for r in by))
    law = q("SELECT COUNT(*) FROM statement WHERE run_id = ? AND strength = 'LAW'", rid)[0][0]
    if law and q("SELECT 1 FROM statement_basis b JOIN statement s ON s.id = b.statement_id WHERE s.run_id = ? LIMIT 1", rid):
        bare = q("SELECT COUNT(*) FROM law_without_basis WHERE run_id = ?", rid)[0][0]
        advice = q("SELECT COUNT(DISTINCT statement_id) FROM advice_with_law WHERE run_id = ?", rid)[0][0]
        out.append(f'{rid}: {law - bare} of {law} LAW statements cite a provision (view law_without_basis); '
                   f'{advice} ADVICE statements have a provision behind them (view advice_with_law)')
        lines, done = q("SELECT COUNT(*), COUNT(DISTINCT g.statement_id) FROM statement_law g JOIN statement s "
                        "ON s.id = g.statement_id WHERE s.run_id = ?", rid)[0]
        left = q("SELECT COUNT(*) FROM law_not_added WHERE run_id = ?", rid)[0][0]
        out.append(f'{rid}: {lines} law lines added under {done} statements; {left} statements with a provision '
                   f'behind them have none (view law_not_added)')
    tagged = q("SELECT COUNT(*) FROM unit_topic t JOIN unit u ON u.id = t.unit_id WHERE t.topic = ? AND u.source_id = ?",
               run['topic'], run['source_id'])[0][0]
    if tagged:
        unused = q("SELECT COUNT(*) FROM topic_unit_unused WHERE run_id = ?", rid)[0][0]
        out.append(f'{rid}: {tagged - unused} of the {tagged} sentences and figures tagged {run["topic"]} are cited, '
                   f'{unused} are not (view topic_unit_unused)')
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('command', choices=['load', 'dump', 'check', 'export'])
    ap.add_argument('--db', default=DB)
    ap.add_argument('--write', action='store_true', help='export: write the files made from the database')
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
        for path, content in outputs(db).items():
            full = os.path.join(ROOT, path)
            same = os.path.exists(full) and open(full, encoding='utf-8').read() == content
            if a.write and not same:
                with open(full, 'w', encoding='utf-8') as f:
                    f.write(content)
            print(f'{path}: ' + ('same as the database' if same else 'written' if a.write else 'differs from the database'))


if __name__ == '__main__':
    main()
