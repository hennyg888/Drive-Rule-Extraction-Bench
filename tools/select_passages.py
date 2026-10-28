"""Stage 3, selection: choose a topic's passages from the tags, by a fixed query.

A paragraph is selected when one of its sentences is tagged with the topic, or when it is a figure
tagged with it (reason 'tag'). A selected list item also brings the paragraph that leads its list,
the one just before the list that ends with a colon (reason 'lead'). A person can add or drop
paragraphs (--add, --drop; reason 'manual'). The passages get ids p1, p2, ... in reading order: the
ids the extraction prompt shows.

    python3 tools/select_passages.py mto passing on-passing-select-1 --tags on-tag-1 [--add ID] [--drop ID]
        Writes the run and its selection to the database, and runs/<run>/selection.md: every
        passage, why it was chosen, and the reference passages on the same paragraph.
"""
import argparse
import collections
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db as dbtool  # noqa: E402


def item_no(locator):
    m = re.search(r'· item (\d+)$', locator or '')
    return int(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('folder')
    ap.add_argument('topic')
    ap.add_argument('run')
    ap.add_argument('--tags', required=True, help='the tagging run to read')
    ap.add_argument('--add', action='append', default=[], help='a paragraph id to add by hand')
    ap.add_argument('--drop', action='append', default=[], help='a paragraph id to drop by hand')
    ap.add_argument('--by', default='query', help='who chose it: "query", or the person who added or dropped')
    a = ap.parse_args()
    db = dbtool.connect()
    q = lambda sql, *x: db.execute(sql, x).fetchall()  # noqa: E731
    source = f'{a.folder}-handbook'
    if not q("SELECT 1 FROM run WHERE id = ? AND stage = 'tag' AND source_id = ?", a.tags, source):
        sys.exit(f'{a.tags} is not a tagging run of {source}')

    order = {r['id']: r['position'] for r in q('SELECT * FROM page WHERE source_id = ?', source)}
    paras = sorted(q("SELECT * FROM unit WHERE source_id = ? AND kind = 'paragraph'", source),
                   key=lambda p: (order[p['page']], p['id']))
    tagged = {r[0] for r in q(
        "SELECT CASE u.kind WHEN 'sentence' THEN u.parent_id ELSE u.id END FROM unit_topic t "
        "JOIN unit_tag g ON g.unit_id = t.unit_id JOIN unit u ON u.id = t.unit_id "
        "WHERE t.topic = ? AND g.run_id = ?", a.topic, a.tags)}
    chosen = {p['id']: 'tag' for p in paras if p['id'] in tagged}
    for i, p in enumerate(paras):
        if p['id'] in chosen and item_no(p['locator']):
            j = i - item_no(p['locator'])         # the paragraph before item 1 of this list
            if j >= 0 and paras[j]['page'] == p['page'] and not item_no(paras[j]['locator']) \
                    and paras[j]['text'].rstrip().endswith(':'):
                chosen.setdefault(paras[j]['id'], 'lead')
    known = {p['id'] for p in paras}
    for uid in a.add:
        if uid not in known:
            sys.exit(f'--add {uid}: not a paragraph of {source}')
        chosen.setdefault(uid, 'manual')
    for uid in a.drop:
        chosen.pop(uid, None)

    rows = [p for p in paras if p['id'] in chosen]
    db.execute('DELETE FROM selection WHERE run_id = ?', (a.run,))
    db.execute('DELETE FROM run WHERE id = ?', (a.run,))
    note = ('Paragraphs with a sentence or figure tagged ' + a.topic + ', and the leads of their lists' +
            (f'; {len(a.add)} added and {len(a.drop)} dropped by {a.by}' if a.add or a.drop else ''))
    db.execute('INSERT INTO run (id, stage, source_id, topic, input_run, prompt, model, date, note) '
               'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
               (a.run, 'select', source, a.topic, a.tags, 'tools/select_passages.py', a.by,
                datetime.date.today().isoformat(), note))
    db.executemany('INSERT INTO selection VALUES (?, ?, ?, ?, ?)',
                   [(a.run, i, p['id'], f'p{i + 1}', chosen[p['id']]) for i, p in enumerate(rows)])
    db.commit()
    reasons = {r: sum(1 for x in chosen.values() if x == r) for r in ('tag', 'lead', 'manual')}
    print(f'{a.run}: {len(rows)} passages (' + ', '.join(f'{k} {v}' for k, v in reasons.items() if v) + ')')

    # How it differs from the paragraphs covered by the passages of the topic's rules.json.
    ref = collections.defaultdict(list)
    for pid, uid in q("SELECT p.id, CASE x.kind WHEN 'sentence' THEN x.parent_id ELSE x.id END FROM passage_part pp "
                      "JOIN unit p ON p.id = pp.passage_id JOIN unit x ON x.id = pp.part_id WHERE p.source_id = ?", source):
        ref[uid].append(pid.split(':')[-1])
    for uid in ref:                           # m3 before m12
        ref[uid] = sorted(set(ref[uid]), key=lambda x: (x[0], int(x[1:])) if x[1:].isdigit() else (x, 0))
    mine = {p['id'] for p in rows}
    if ref:
        print(f'reference passages cover {len(ref)} paragraphs; {len(set(ref) & mine)} of them are selected, '
              f'{len(set(ref) - mine)} are not; {len(mine - set(ref))} selected paragraphs are not in the reference')
    cell = lambda t: (t or '').replace('|', '/').replace('\n', ' ')  # noqa: E731
    out = [f'# Selection {a.run}', '',
           f'Made by `tools/select_passages.py {a.folder} {a.topic} {a.run} --tags {a.tags}` from the database: {note}. '
           'The reference column names the passages of the reviewed set that cover the same paragraph.', '',
           f'{len(rows)} passages: ' + ', '.join(f'{k} {v}' for k, v in reasons.items() if v) +
           (f'. Of the {len(ref)} paragraphs the reference covers, {len(set(ref) - mine)} are not selected (listed at the end).'
            if ref else '.'), '',
           '| Passage | Why | Reference | Where | Text |', '|---|---|---|---|---|']
    for i, p in enumerate(rows):
        text = (f'[figure] {p["heading"] or ""} {p["text"]}' if p['image'] else p['text'])
        out.append(f'| p{i + 1} | {chosen[p["id"]]} | {" ".join(ref.get(p["id"], [])) or "-"} | {cell(p["locator"])} | {cell(text)} |')
    left = [p for p in paras if p['id'] in ref and p['id'] not in mine]
    if left:
        out += ['', '## In the reference, not selected', '', '| Reference | Where | Text |', '|---|---|---|']
        out += [f'| {" ".join(ref[p["id"]])} | {cell(p["locator"])} | {cell(p["text"])} |' for p in left]
    d = os.path.join(dbtool.ROOT, 'runs', a.run)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'selection.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')

if __name__ == '__main__':
    main()
