"""Stage 1, import: put one handbook into the database, one row per piece, word for word.

From the handbook's segment file (analysis/segments/<folder>.jsonl, made from its HTML by
tools/segment_handbook.py) it writes:
  - page: every page, in reading order, with its title;
  - unit, kind paragraph: every paragraph, list item, step and figure, with its page, heading path
    (locator), anchor, and for a figure its image and caption (in heading);
  - unit, kind sentence (with --sentences): every sentence of every text paragraph, numbered under
    its paragraph: mto:para:changing-positions:012 holds mto:sent:changing-positions:012.1, .2, ...

Nothing is interpreted: the sentence split is a fixed rule (split() below), so the same paragraphs
always give the same sentences, and a paragraph's sentences joined with spaces give its text back.
Run it again and nothing changes. Rows that pointed at a sentence a new split replaces (a passage
that names one, a grounding link) move to the new sentence with the same words in the same paragraph.

Usage, from the repo root, after tools/db.py load:
    python3 tools/import_handbook.py mto --sentences
    python3 tools/db.py check && python3 tools/db.py dump
"""
import argparse
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db as dbtool  # noqa: E402

# A sentence ends at . ! or ? (or one followed by a closing quote or bracket), before a space and a
# capital, a digit, an opening quote or a bracket; never after one of these abbreviations.
ABBR = r'(?:e\.g|i\.e|etc|a\.m|p\.m|No|St|Mr|Mrs|Dr|vs|approx|U\.S|km/h)'


def split(text):
    t = re.sub(r'\s+', ' ', text).strip()
    if not t:
        return []
    kept = re.sub(r'\b(' + ABBR + r')\.', lambda m: m.group(1).replace('.', '§') + '§', t)
    parts = re.split(r'(?:(?<=[.!?])|(?<=[.!?]["”’)]))\s+(?=[A-Z0-9“"(])', kept)
    return [p.replace('§', '.').strip() for p in parts if p.strip()]


def unit_row(**u):
    return {c: u.get(c) for c in ('id', 'source_id', 'kind', 'parent_id', 'page', 'locator', 'heading', 'anchor',
                                  'image', 'valid_from', 'valid_to', 'text')}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('folder', help="the handbook's folder name: mto, ca or tx")
    ap.add_argument('--sentences', action='store_true', help='also split its text paragraphs into sentences')
    a = ap.parse_args()
    db = dbtool.connect()
    q = lambda sql, *x: db.execute(sql, x).fetchall()  # noqa: E731
    source = f'{a.folder}-handbook'
    if not q('SELECT 1 FROM source WHERE id = ?', source):
        sys.exit(f'no source {source}')
    meta = json.load(open(os.path.join(dbtool.ROOT, 'analysis', 'passing-rules', a.folder, 'meta.json'), encoding='utf-8'))
    path = os.path.join(dbtool.ROOT, meta.get('segments') or f'analysis/segments/{a.folder}.jsonl')
    segs = [json.loads(line) for line in open(path, encoding='utf-8') if line.strip()]

    pages, paras = {}, []
    for seg in segs:
        pages.setdefault(seg['page'], seg.get('page_title') or seg['page'])
        paras.append(unit_row(id=f'{a.folder}:para:{seg["id"]}', source_id=source, kind='paragraph', page=seg['page'],
                              locator=' › '.join(x for x in (seg.get('page_title'), seg.get('sec')) if x),
                              heading=seg.get('cap') if seg.get('src') else None, anchor=seg.get('anchor'),
                              image=seg.get('src'), text=seg['text']))
    sents = []
    if a.sentences:
        for p in paras:
            if p['image']:
                continue
            parts = split(p['text'])
            if ' '.join(parts) != re.sub(r'\s+', ' ', p['text']).strip():
                sys.exit(f'{p["id"]}: its sentences do not join back into its text')
            sents += [unit_row(id=f'{a.folder}:sent:{p["id"].split(":", 2)[2]}.{k}', source_id=source, kind='sentence',
                               parent_id=p['id'], page=p['page'], locator=p['locator'], anchor=p['anchor'], text=s)
                      for k, s in enumerate(parts, 1)]

    db.execute('PRAGMA foreign_keys = OFF')
    db.execute('DELETE FROM passage_part')    # derived from paragraphs and sentences; rebuilt below
    db.execute('DELETE FROM page WHERE source_id = ?', (source,))
    db.executemany('INSERT INTO page VALUES (?, ?, ?, ?)', [(source, p, i, t) for i, (p, t) in enumerate(pages.items())])

    # Paragraphs: the same ids as before, so a changed one is updated in place.
    old = {r['id']: dict(r) for r in q("SELECT * FROM unit WHERE source_id = ? AND kind = 'paragraph'", source)}
    cols = list(paras[0])
    changed = [p for p in paras if old.get(p['id']) != p]
    db.executemany(f'INSERT OR REPLACE INTO unit ({", ".join(cols)}) VALUES ({", ".join("?" * len(cols))})',
                   [tuple(p[c] for c in cols) for p in changed])
    gone = set(old) - {p['id'] for p in paras}
    if gone:
        sys.exit(f'{len(gone)} paragraphs in the database are not in {os.path.relpath(path, dbtool.ROOT)}, '
                 f'for example {sorted(gone)[0]}')

    # Sentences: each old one goes to the new sentence with the same words in its paragraph, or on its page.
    moved = {}
    if a.sentences:
        old_s = {r['id']: r for r in q("SELECT * FROM unit WHERE source_id = ? AND kind = 'sentence'", source)}
        by_text = collections.defaultdict(list)
        for s in sents:
            by_text[(s['parent_id'], dbtool.norm(s['text']))].append(s['id'])
            by_text[(s['page'], dbtool.norm(s['text']))].append(s['id'])
        for oid, o in old_s.items():
            to = by_text.get((o['parent_id'], dbtool.norm(o['text']))) or by_text.get((o['page'], dbtool.norm(o['text'])))
            if to:
                moved[oid] = to[0]
        refs = [('unit', 'parent_id'), ('grounding_link', 'unit_id'), ('unit_tag', 'unit_id')]
        for table, col in refs:
            for (uid,) in q(f'SELECT DISTINCT {col} FROM {table} WHERE {col} IN ({",".join("?" * len(old_s))})', *old_s):
                if uid not in moved:
                    sys.exit(f'{table}.{col} = {uid}: no sentence with the same words after the split')
        # One statement per column, so an id that is both a new id and another sentence's old id is
        # not renamed twice.
        db.execute('CREATE TEMP TABLE moved (old TEXT PRIMARY KEY, new TEXT NOT NULL)')
        db.executemany('INSERT INTO moved VALUES (?, ?)', [(o, n) for o, n in moved.items() if n != o])
        for table, col in refs:
            db.execute(f'UPDATE {table} SET {col} = (SELECT new FROM moved WHERE old = {col}) '
                       f'WHERE {col} IN (SELECT old FROM moved)')
        db.execute('DROP TABLE moved')
        db.execute("DELETE FROM unit WHERE source_id = ? AND kind = 'sentence'", (source,))
        db.executemany(f'INSERT INTO unit ({", ".join(cols)}) VALUES ({", ".join("?" * len(cols))})',
                       [tuple(s[c] for c in cols) for s in sents])
    db.execute('PRAGMA foreign_keys = ON')
    broken = q('PRAGMA foreign_key_check')
    if broken:
        db.rollback()
        sys.exit(f'{len(broken)} rows refer to rows that do not exist, for example {tuple(broken[0])}')
    dbtool.derive(db)
    db.commit()
    print(f'{source}: {len(pages)} pages, {len(paras)} paragraphs ({len(changed)} new or changed)' +
          (f', {len(sents)} sentences ({sum(1 for o, n in moved.items() if n != o)} kept their words under a new id)'
           if a.sentences else ''))


if __name__ == '__main__':
    main()
