"""Write the census shards: the handbook's sentence units, in book order, as numbered text for labelling.

Usage: python3 provenance/scripts/make_census_shards.py UNITS.jsonl CHAPTERS.json OUT_DIR [--shards 8] [--skip-page test-yourself-sample-knowledge-test-questions]
UNITS.jsonl and CHAPTERS.json are written by segment_sentences.py. Pages follow the book's table of contents.
Writes shardN.txt (what a labeller reads) and shardN.ids (the ids it must label) for N = 1..shards.
Headings are context lines, not labelled. Units of a skipped page are left out. A shard ends at the first
heading after it reaches its share of the units, so a section is not split between labellers.
"""
import argparse, json, os

ap = argparse.ArgumentParser()
ap.add_argument('units'); ap.add_argument('chapters'); ap.add_argument('out')
ap.add_argument('--shards', type=int, default=8)
ap.add_argument('--skip-page', action='append', default=['test-yourself-sample-knowledge-test-questions'])
a = ap.parse_args()

units = [json.loads(l) for l in open(a.units, encoding='utf-8') if l.strip()]
toc = list(json.load(open(a.chapters, encoding='utf-8')))  # page slugs in table-of-contents order
units = sorted((u for u in units if u['page'] not in a.skip_page), key=lambda u: (toc.index(u['page']), u['id']))  # ids sort as text
labelled = [u for u in units if u['kind'] != 'heading']
size = -(-len(labelled) // a.shards)  # each shard takes at least this many units

def tag(u):
    if u['kind'] in ('item', 'step'):
        lead = (u.get('list_lead') or '')[:160]
        return f'({u["kind"]} {u["item_no"]}; lead: "{lead}")' if lead else f'({u["kind"]} {u["item_no"]})'
    return f'({u["kind"]})'

shard_of, cur, k = {}, 1, 0
first_heading = {}
for u in units:
    if u['kind'] == 'heading':
        if k >= size and cur < a.shards:
            cur, k = cur + 1, 0
        first_heading.setdefault(u['id'], cur)
        continue
    shard_of[u['id']] = cur
    k += 1
for s in range(1, a.shards + 1):
    lines, ids, page = [], [], None
    for u in units:
        if (shard_of.get(u['id']) or first_heading.get(u['id'])) != s:
            continue
        if u['page'] != page:
            lines += ['', f'## PAGE {u["page"]} — "{u["page_title"]}" (Chapter {u["chapter"]}: {u["chapter_title"]})']
            page = u['page']
        if u['kind'] == 'heading':
            lines.append(f'### {u["section"]}')
            continue
        lines.append(f'[{u["id"]}] {tag(u)} {u["text"]}')
        ids.append(u['id'])
    open(os.path.join(a.out, f'shard{s}.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    open(os.path.join(a.out, f'shard{s}.ids'), 'w', encoding='utf-8').write('\n'.join(ids) + '\n')
print(len(labelled), 'units in', a.shards, 'shards:', [sum(1 for v in shard_of.values() if v == n) for n in range(1, a.shards + 1)])
