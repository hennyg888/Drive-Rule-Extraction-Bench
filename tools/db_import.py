"""Create the rules database from the files it replaced, once. Kept as the record of how it was made.

Run on 27 October 2026. It reads the handbooks' paragraphs (analysis/segments/), the Ontario census
(analysis/census/census-labels.jsonl), the topic passages and statements
(analysis/passing-rules/{mto,ca,tx}/), and the rule language vocabulary written out below from
analysis/rule-language.md, then writes db/rules.sqlite and dumps db/tables/. The laws, their
provisions, the legal basis of statements and the grounding of flags were added afterwards, through
the database.

Since then the tables in db/tables/ are the master copy: change them through the database
(tools/db.py), not by running this again, which would drop everything added since.

Usage, from the repo root:
    python3 tools/db_import.py
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db as dbtool  # noqa: E402

ROOT = dbtool.ROOT
JURISDICTION = {'mto': 'on', 'ca': 'ca', 'tx': 'tx'}

# The rule language's fixed words (analysis/rule-language.md, the section in the last column).
VOCABULARY = [
    ('type', 'DEFINE', 'A term and what it means', None, None, '§1'),
    ('type', 'FACT', 'Background with no instruction', None, None, '§1'),
    ('type', 'RULE', 'Obligations, prohibitions, permissions, advice, cautions', None, None, '§1'),
    ('type', 'PROCEDURE', 'Ordered steps', None, None, '§1'),
    ('type', 'EXCEPTION', 'A change to a statement written in another passage', None, None, '§1'),
    ('modal', 'MUST', 'Obligation backed by law', 'obligation', 'LAW', '§2'),
    ('modal', 'MUST NOT', 'Prohibition backed by law', 'prohibition', 'LAW', '§2'),
    ('modal', 'MAY', 'Permission backed by law', 'permission', 'LAW', '§2'),
    ('modal', 'SHOULD', 'Obligation as advice', 'obligation', 'ADVICE', '§2'),
    ('modal', 'SHOULD NOT', 'Prohibition as advice', 'prohibition', 'ADVICE', '§2'),
    ('clause', 'WHEN', 'When the statement applies', None, None, '§3'),
    ('clause', 'WHILE', 'A state that lasts for the whole action', None, None, '§3'),
    ('clause', 'ONLY IF', 'A condition that must hold; mostly after MAY', None, None, '§3'),
    ('clause', 'UNLESS', 'An exception inside the same sentence', None, None, '§3'),
    ('clause', 'UNTIL', 'When the duty ends', None, None, '§3'),
    ('clause', 'BECAUSE', 'Why; never changes when the rule applies', None, None, '§3'),
    ('clause', 'IF VIOLATED', 'Fine, demerit points, suspension, impoundment', None, None, '§3'),
    ('connective', 'AND', 'Joins conditions or actions; binds tighter than OR', None, None, '§3'),
    ('connective', 'OR', 'Joins conditions or actions', None, None, '§3'),
    ('connective', 'NOT', 'Negates a condition part', None, None, '§3'),
    ('connective', 'EITHER', 'A duty that is a choice between actions: EITHER a OR b', None, None, '§1'),
    ('link', 'EXCEPTION TO', 'Changes another statement where both apply; the more specific wins', None, None, '§4'),
    ('link', 'SPECIALIZES', 'A variant of another statement for a narrower situation', None, None, '§4'),
    ('link', 'ALSO CALLED', 'A synonym, inside DEFINE', None, None, '§4'),
    ('define', 'IS', 'DEFINE <term> IS <kind>', None, None, '§1'),
    ('define', 'THAT', 'DEFINE <term> IS <kind> THAT <difference>', None, None, '§1'),
    ('procedure', 'TO', 'TO <goal>: the goal of a procedure', None, None, '§1'),
    ('procedure', 'STEP', 'STEP n <action>', None, None, '§1'),
    ('procedure', 'DONE WHEN', 'The state that ends a procedure', None, None, '§1'),
    ('procedure', 'IF', 'IF <event> THEN <action>: a branch inside a procedure', None, None, '§1'),
    ('procedure', 'THEN', 'IF <event> THEN <action>', None, None, '§1'),
    ('action', 'WATCH FOR', 'A caution that names a hazard: SHOULD WATCH FOR <hazard>', None, None, '§2'),
    ('flag', 'J', 'Judgment term: safe, enough, sure, reasonable, as soon as you can', None, None, '§8'),
    ('flag', 'S', 'Hedged scope: usually, often, many, most', None, None, '§8'),
    ('flag', 'R', 'Unclear reference or role', None, None, '§8'),
    ('flag', 'G', 'Goal and means differ', None, None, '§8'),
    ('flag', 'M', 'Unclear legal strength', None, None, '§8'),
    ('flag', 'D', 'Implicit default: a permission that presupposes an unstated prohibition', None, None, '§8'),
    ('flag', 'V', 'Wording drift across passages', None, None, '§8'),
    ('flag', 'X', 'Stated again elsewhere, possibly differently', None, None, '§8'),
    ('comparator', 'at least', None, None, None, '§1'),
    ('comparator', 'at most', None, None, None, '§1'),
    ('comparator', 'within', None, None, None, '§1'),
    ('comparator', 'more than', None, None, None, '§1'),
    ('comparator', 'less than', None, None, None, '§1'),
]
VOCABULARY += [('unit', u, None, None, None, '§1') for u in ('m', 'km', 'km/h', 's', 'mph', 'ft')]
VOCABULARY += [('abbreviation', 'LCV', 'long commercial vehicle', None, None, '§7'),
               ('abbreviation', 'HOV', 'high-occupancy vehicle', None, None, '§7')]
VOCABULARY += [('role', r, None, None, None, '§7') for r in (
    'a driver', 'a driver being passed', 'a driver towing a trailer', 'a truck driver', 'a cyclist')]
VOCABULARY += [('phrase', p, None, None, None, '§7') for p in (
    'pass', 'lane change', 'the vehicle being passed', 'the passing lane', 'the original lane', 'the right-hand lane',
    'the far-left lane', 'the inside mirror', 'oncoming traffic', 'yield the right-of-way to')]
VERBS = {
    'Moving': 'pass, change lanes, move, merge, cut in, cut back, return to, pull out, cross, drive, ride, travel, steer, '
              'go, proceed, approach, follow, stay, remain, keep, leave, take, give, vacate, wait, stop, start',
    'Speed': 'slow down, speed up, brake, tap, maintain',
    'Signals and lights': 'signal, use, sound the horn, switch',
    'Attention': 'look, check, judge, make certain, anticipate, be ready to, be prepared to',
    'Right of way': 'yield the right-of-way to, allow, let',
    'Other': 'attempt, try',
}
VOCABULARY += [('verb', v.strip(), kind, None, None, '§5') for kind, vs in VERBS.items() for v in vs.split(',')]


def read_json(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return json.load(f)


def read_jsonl(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    argparse.ArgumentParser(description=__doc__.split('\n')[0]).parse_args()

    rows = {t: [] for t, _ in dbtool.MASTER}
    rows['vocabulary'] = [dict(kind=k, word=w, meaning=m, modality=mo, strength=st, section=sec)
                          for k, w, m, mo, st, sec in VOCABULARY]
    units = {}

    def unit(**u):
        u.setdefault('parent_id', None)
        for k in ('page', 'heading', 'anchor', 'image', 'valid_from', 'valid_to'):
            u.setdefault(k, None)
        units[u['id']] = u

    for folder, jur in JURISDICTION.items():
        base = f'analysis/passing-rules/{folder}'
        if not os.path.exists(os.path.join(ROOT, base, 'rules.json')):
            continue
        meta = read_json(f'{base}/meta.json')
        hid = f'{folder}-handbook'
        rows['source'].append(dict(id=hid, kind='handbook', jurisdiction=jur, title=meta['name'], citation=None,
                                   version=meta.get('edition'), url=meta.get('source_url'),
                                   path=meta.get('handbook_dir'), sha256=None, retrieved=meta.get('scraped')))

        # Every paragraph, list item, step and figure of the handbook.
        paras, titles = [], {}
        for seg in read_jsonl(meta.get('segments') or f'analysis/segments/{folder}.jsonl'):
            uid = f'{folder}:para:{seg["id"]}'
            titles[seg['page']] = seg.get('page_title') or seg['page']
            unit(id=uid, source_id=hid, kind='paragraph', page=seg['page'], sec=seg.get('sec'),
                 locator=' › '.join(x for x in (seg.get('page_title'), seg.get('sec')) if x),
                 anchor=seg.get('anchor'), image=seg.get('src'), text=seg['text'])
            paras.append(units[uid])

        # Every Ontario sentence, with its census label, under the paragraph that holds it.
        if folder == 'mto':
            by_page = {}
            for p in paras:
                by_page.setdefault(p['page'], []).append(p)

            def heading(h):
                h = re.sub(r'\s*>\s*', ' > ', dbtool.norm(re.sub(r'\s*·.*$', '', h or '').replace('›', '>')))
                return re.sub(r'\s*([():])\s*', r'\1', re.sub(r'(^| > )intro$', '', h))

            for c in read_jsonl('analysis/census/census-labels.jsonl'):
                # The census numbers paragraphs on its own (page:NNN.k); 428 of its numbers differ from
                # the segments'. The parent is the paragraph on the page that holds the sentence; when
                # several do (a sentence like "1." or a repeated tip), the one under the same heading,
                # then the nearest in number.
                t = dbtool.norm(c['text'])
                n = int(c['id'].split(':')[1].split('.')[0])
                held = [p for p in by_page.get(c['page'], []) if p['image'] is None and t in dbtool.norm(p['text'])]
                parent = min(held, key=lambda p: (heading(p['sec']) != heading(c.get('section')),
                                                  abs(int(p['id'].split(':')[-1]) - n)), default=None)
                uid = f'mto:sent:{c["id"]}'
                unit(id=uid, source_id=hid, kind='sentence', parent_id=parent and parent['id'], page=c['page'],
                     locator=' › '.join(x for x in (titles.get(c['page'], c['page']), c.get('section')) if x),
                     anchor=parent and parent['anchor'], text=c['text'])
                lb = c['label']
                rows['sentence_label'].append(dict(unit_id=uid, type=lb.get('t'), role=lb.get('role') or None,
                                                   modal=lb.get('m'), basis=lb.get('b'), caution=int(bool(lb.get('caut'))),
                                                   fit=lb.get('fit'), passing=int(bool(lb.get('pass'))),
                                                   rewrite=lb.get('v') or None))
                words = [('action', [lb['act']] if lb.get('act') else []), ('entity', lb.get('ent', [])),
                         ('dimension', lb.get('dim', [])), ('vague', lb.get('vg', [])), ('clause', lb.get('cl', [])),
                         ('need', lb.get('need', []))]
                for kind, ws in words:
                    for i, w in enumerate(ws):
                        code, w = w if isinstance(w, list) else (None, w)
                        rows['sentence_word'].append(dict(unit_id=uid, kind=kind, position=i, word=w, code=code))

        # The topic passages. Ontario's figure passages carry no image path; the statements that cite
        # them do.
        rules = read_json(f'{base}/rules.json')
        images = {}
        for r in rules:
            for so in r['sources']:
                if so.get('image'):
                    images.setdefault(so['id'], so['image'])
        for name in sorted(os.listdir(os.path.join(ROOT, base, 'inputs'))):
            data = read_json(f'{base}/inputs/{name}')
            items = data.get('passages', data) if isinstance(data, dict) else data
            if not (isinstance(items, list) and items and isinstance(items[0], dict) and 'm' in items[0]):
                continue
            for p in items:
                parent = None
                if p.get('seg'):
                    parent = f'{folder}:para:{p["seg"]}'
                elif p.get('census_id') and '(' not in p['census_id']:
                    parent = f'mto:sent:{p["census_id"]}'
                unit(id=f'{folder}:passage:{p["m"]}', source_id=hid, kind='passage', parent_id=parent,
                     locator=' › '.join(x for x in (p.get('page'), p.get('sec')) if x),
                     image=(p.get('src') or images.get(p['m'])) if p.get('kind') == 'figure' else None, text=p['text'])

        # Statements.
        for pos, s in enumerate(rules):
            sid = f'{folder}:{s["id"]}'
            if 'section' in s and s['section'] is None:
                sys.exit(f'{sid}: section is null; export would drop the key')
            rows['statement'].append(dict(id=sid, jurisdiction=jur, local_id=s['id'], position=pos, topic='passing',
                                          section=s.get('section'), type=s['type'], strength=s.get('strength'),
                                          strength_from=s.get('strength_from'), text=s['text'], note=s.get('note')))
            for i, so in enumerate(s['sources']):
                rows['statement_source'].append(dict(statement_id=sid, position=i, unit_id=f'{folder}:passage:{so["id"]}',
                                                     quote=so.get('quote'), where_text=so.get('where'),
                                                     census_id=so.get('census_id'), image=so.get('image')))
            for i, st in enumerate(s.get('steps', [])):
                rows['statement_step'].append(dict(statement_id=sid, n=st['n'], position=i, text=st['text']))
                for j, x in enumerate(st['sources']):
                    rows['step_source'].append(dict(statement_id=sid, step=i, position=j,
                                                    unit_id=f'{folder}:passage:{x}'))
            for i, to in enumerate(s['links']):
                kind = next((k for k in ('EXCEPTION TO', 'SPECIALIZES') if f'{k} {to}' in s['text']), 'REFERS TO')
                rows['statement_link'].append(dict(from_id=sid, position=i, to_id=f'{folder}:{to}', kind=kind))
            for i, se in enumerate(s.get('see', [])):
                rows['statement_figure'].append(dict(statement_id=sid, position=i,
                                                     unit_id=f'{folder}:passage:{se["source"]}', figure=se['figure']))
            for i, fl in enumerate(s['flags']):
                term = f'{jur}:{fl["span"].lower()}' if fl['code'] == 'J' else None
                rows['occurrence'].append(dict(id=f'{folder}:{s["id"]}|{fl["code"]}|{fl["span"]}', statement_id=sid,
                                               position=i, code=fl['code'], span=fl['span'], note=fl.get('note'),
                                               note_zh=fl.get('zh'), term_id=term))
                if term:
                    rows['term'].append(dict(id=term, jurisdiction=jur, phrase=fl['span'].lower()))

    rows['unit'] = [{k: v for k, v in u.items() if k != 'sec'} for u in units.values()]
    seen = set()
    rows['term'] = [t for t in rows['term'] if not (t['id'] in seen or seen.add(t['id']))]

    tmp = os.path.join(ROOT, 'db', 'tables.import')
    os.makedirs(tmp, exist_ok=True)
    for table, rs in rows.items():
        with open(os.path.join(tmp, f'{table}.jsonl'), 'w', encoding='utf-8') as f:
            for r in rs:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')
    db = dbtool.load(dbtool.DB, tmp)
    for name in os.listdir(tmp):
        os.remove(os.path.join(tmp, name))
    os.rmdir(tmp)
    counts = dbtool.dump(db)
    print('imported: ' + ', '.join(f'{t} {n}' for t, n in counts.items()))


if __name__ == '__main__':
    main()
