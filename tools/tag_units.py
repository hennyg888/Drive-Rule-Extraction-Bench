"""Stage 2, tagging: hand a handbook's sentences and figures to a model, check its tags, store them.

    python3 tools/tag_units.py shard mto on-tag-1 --shards 8
        Writes runs/on-tag-1/prompt.md (prompts/tag-units.md with the topics filled in) and
        runs/on-tag-1/input/shard-NN.jsonl: every paragraph of the handbook, in reading order, from the
        database. A model answers each shard into runs/on-tag-1/output/shard-NN.jsonl.
    python3 tools/tag_units.py check on-tag-1 [NN]
        Checks the answers against the shards: one line per sentence and figure, tags from the fixed
        lists, vague words copied exactly. Exit 1 on a problem.
    python3 tools/tag_units.py load on-tag-1 --model NAME --date YYYY-MM-DD
        Checks, then writes the run and its tags to the database, replacing the handbook's earlier tags.
"""
import argparse
import glob
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db as dbtool  # noqa: E402

PROMPT = os.path.join('prompts', 'tag-units.md')
TOPICS = os.path.join('prompts', 'topics')
TYPES = {'RULE', 'STEP', 'DEFINE', 'FACT', 'CONSEQ', 'META', 'FIGURE'}
MODALS = {'MUST', 'MUST NOT', 'MAY', 'SHOULD', 'SHOULD NOT', 'IMPERATIVE', 'IMPERATIVE NOT', 'NONE'}
CODES = {'J', 'M', 'S', 'R', 'D', 'G'}


def run_dir(run):
    return os.path.join(dbtool.ROOT, 'runs', run)


def topics():
    out = {}
    for f in sorted(glob.glob(os.path.join(dbtool.ROOT, TOPICS, '*.txt'))):
        out[os.path.basename(f)[:-4]] = open(f, encoding='utf-8').read().strip()
    return out


def shard(a):
    db = dbtool.connect()
    q = lambda sql, *x: db.execute(sql, x).fetchall()  # noqa: E731
    source = f'{a.folder}-handbook'
    order = {r['id']: r['position'] for r in q('SELECT * FROM page WHERE source_id = ?', source)}
    sents = {}
    for s in q("SELECT * FROM unit WHERE source_id = ? AND kind = 'sentence' ORDER BY id", source):
        sents.setdefault(s['parent_id'], []).append({'id': s['id'], 'text': s['text']})
    paras = sorted(q("SELECT * FROM unit WHERE source_id = ? AND kind = 'paragraph'", source),
                   key=lambda p: (order[p['page']], p['id']))
    lines, pages = [], []
    for p in paras:
        if p['image']:
            line = {'para': p['id'], 'where': p['locator'], 'figure': p['text']}
        elif p['id'] in sents:
            line = {'para': p['id'], 'where': p['locator'], 'sentences': sents[p['id']]}
        else:
            continue
        if not pages or pages[-1][0] != p['page']:
            pages.append((p['page'], []))
        pages[-1][1].append(line)
    # Whole pages per shard, about the same number of tags in each.
    size = lambda ls: sum(len(x.get('sentences', [1])) for x in ls)  # noqa: E731
    total, per = sum(size(ls) for _, ls in pages), None
    per = total / a.shards
    shards, cur = [], []
    for _, ls in pages:
        if cur and size(cur) + size(ls) / 2 > per and len(shards) < a.shards - 1:
            shards.append(cur)
            cur = []
        cur += ls
    shards.append(cur)
    d = run_dir(a.run)
    os.makedirs(os.path.join(d, 'input'), exist_ok=True)
    os.makedirs(os.path.join(d, 'output'), exist_ok=True)
    raw = open(os.path.join(dbtool.ROOT, PROMPT), encoding='utf-8').read()
    text = raw.split('<!-- PROMPT -->', 1)[1].strip() + '\n'
    block = '\n'.join(f'- `{name}`: {scope}' for name, scope in topics().items())
    open(os.path.join(d, 'prompt.md'), 'w', encoding='utf-8').write(text.replace('{{TOPICS}}', block))
    for i, ls in enumerate(shards, 1):
        with open(os.path.join(d, 'input', f'shard-{i:02d}.jsonl'), 'w', encoding='utf-8') as f:
            for x in ls:
                f.write(json.dumps(x, ensure_ascii=False) + '\n')
    json.dump({'prompt': PROMPT, 'prompt_sha256': hashlib.sha256(raw.encode('utf-8')).hexdigest(), 'source': source},
              open(os.path.join(d, 'run.json'), 'w', encoding='utf-8'), indent=1)
    print(f'{a.run}: {total} sentences and figures in {len(shards)} shards: ' +
          ', '.join(str(size(s)) for s in shards))


def read(run, which=None):
    """{shard: (inputs by id, answers)} for the run's shards, or only the named one."""
    d = run_dir(run)
    out = {}
    for f in sorted(glob.glob(os.path.join(d, 'input', 'shard-*.jsonl'))):
        n = os.path.basename(f)[6:8]
        if which and n not in which:
            continue
        want = {}
        for line in open(f, encoding='utf-8'):
            x = json.loads(line)
            if 'figure' in x:
                want[x['para']] = {'text': x['figure'], 'figure': True}
            for s in x.get('sentences', []):
                want[s['id']] = {'text': s['text'], 'figure': False}
        ans = os.path.join(d, 'output', f'shard-{n}.jsonl')
        out[n] = (want, open(ans, encoding='utf-8').read().splitlines() if os.path.exists(ans) else None)
    return out


def problems(want, lines, names):
    errs, seen = [], {}
    if lines is None:
        return ['no answer file'], seen
    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            x = json.loads(line)
        except json.JSONDecodeError as e:
            errs.append(f'line {i}: not JSON ({e})')
            continue
        uid = x.get('id')
        if uid not in want:
            errs.append(f'line {i}: {uid} is not in the shard')
            continue
        if uid in seen:
            errs.append(f'line {i}: {uid} answered twice')
        seen[uid] = x
        if set(x) != {'id', 'type', 'modal', 'caution', 'topics', 'vague'}:
            errs.append(f'{uid}: keys must be id, type, modal, caution, topics, vague')
            continue
        fig = want[uid]['figure']
        if x['type'] not in TYPES or (x['type'] == 'FIGURE') != fig:
            errs.append(f'{uid}: type {x["type"]!r}' + (' (a figure is FIGURE)' if fig else ''))
        if x['modal'] not in MODALS or (fig and x['modal'] != 'NONE'):
            errs.append(f'{uid}: modal {x["modal"]!r}')
        if x['caution'] not in (0, 1) or (fig and x['caution']):
            errs.append(f'{uid}: caution {x["caution"]!r}')
        if not isinstance(x['topics'], list) or not set(x['topics']) <= names or len(set(x['topics'])) != len(x['topics']):
            errs.append(f'{uid}: topics {x["topics"]!r}; the names are {sorted(names)}')
        if not isinstance(x['vague'], list) or (fig and x['vague']):
            errs.append(f'{uid}: vague {x["vague"]!r}')
            continue
        for v in x['vague']:
            if not (isinstance(v, list) and len(v) == 2 and v[0] in CODES and isinstance(v[1], str) and v[1].strip()):
                errs.append(f'{uid}: vague entry {v!r}')
            elif v[1] not in want[uid]['text']:
                errs.append(f'{uid}: vague words {v[1]!r} are not copied exactly from the sentence')
    for uid in want:
        if uid not in seen:
            errs.append(f'{uid}: no answer')
    return errs, seen


def check(a):
    names, bad = set(topics()), 0
    for n, (want, lines) in read(a.run, a.shard).items():
        errs, _ = problems(want, lines, names)
        bad += len(errs)
        print(f'shard {n}: {len(want)} to tag, ' + ('ok' if not errs else f'{len(errs)} problems'))
        for e in errs[:40]:
            print('  ' + e)
        if len(errs) > 40:
            print(f'  … and {len(errs) - 40} more')
    sys.exit(1 if bad else 0)


def load(a):
    names = set(topics())
    tags = {}
    for n, (want, lines) in read(a.run).items():
        errs, seen = problems(want, lines, names)
        if errs:
            sys.exit(f'shard {n} has {len(errs)} problems; run check')
        tags.update(seen)
    meta = json.load(open(os.path.join(run_dir(a.run), 'run.json'), encoding='utf-8'))
    db = dbtool.connect()
    old = [r[0] for r in db.execute('SELECT DISTINCT t.run_id FROM unit_tag t JOIN unit u ON u.id = t.unit_id '
                                    'WHERE u.source_id = ?', (meta['source'],))]
    for r in old + [a.run]:
        db.execute('DELETE FROM unit_vague WHERE unit_id IN (SELECT unit_id FROM unit_tag WHERE run_id = ?)', (r,))
        db.execute('DELETE FROM unit_topic WHERE unit_id IN (SELECT unit_id FROM unit_tag WHERE run_id = ?)', (r,))
        db.execute('DELETE FROM unit_tag WHERE run_id = ?', (r,))
    db.execute('DELETE FROM run WHERE id = ?', (a.run,))
    db.execute('INSERT INTO run (id, stage, source_id, prompt, prompt_sha256, model, date, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
               (a.run, 'tag', meta['source'], meta['prompt'], meta['prompt_sha256'], a.model, a.date, a.note))
    for uid, x in tags.items():
        db.execute('INSERT INTO unit_tag VALUES (?, ?, ?, ?, ?)', (uid, a.run, x['type'], x['modal'], x['caution']))
        db.executemany('INSERT INTO unit_topic VALUES (?, ?)', [(uid, t) for t in x['topics']])
        db.executemany('INSERT INTO unit_vague VALUES (?, ?, ?, ?)', [(uid, i, c, w) for i, (c, w) in enumerate(x['vague'])])
    db.commit()
    print(f'{a.run}: {len(tags)} tags written' + (f'; replaced the tags of {", ".join(old)}' if old else ''))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='command', required=True)
    p = sub.add_parser('shard')
    p.add_argument('folder')
    p.add_argument('run')
    p.add_argument('--shards', type=int, default=8)
    p = sub.add_parser('check')
    p.add_argument('run')
    p.add_argument('shard', nargs='*')
    p = sub.add_parser('load')
    p.add_argument('run')
    p.add_argument('--model', required=True)
    p.add_argument('--date', required=True)
    p.add_argument('--note')
    a = ap.parse_args()
    {'shard': shard, 'check': check, 'load': load}[a.command](a)


if __name__ == '__main__':
    main()
