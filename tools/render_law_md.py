"""Write one jurisdiction's statements with the law added under them, from the rules database.

Every statement appears as extracted, with its flags and their notes unchanged. Under it come what
the law adds: how far a formal source settles each flag, the law lines in the rule language, and
the provisions behind the statement and how the statement compares with each. Every provision is
quoted word for word at the end, with a link to its line in the local copy of the law and to the
official page. tools/db.py export --write writes it to analysis/passing-rules/<folder>/passing-rules-law.md
and tools/db.py check fails while the page differs from the database; never edit it by hand.
"""
import bisect
import collections
import os
import re

STATUS = [
    ('LAW_DEFINES', 'the law gives the definition or the number'),
    ('LAW_STATES', 'the law states the duty itself, which settles its strength, scope or reference'),
    ('LAW_REPEATS', 'the law uses the same open word, so the vagueness is in the law too'),
    ('STANDARD', 'an engineering standard or safety model gives an operational definition'),
    ('HANDBOOK', 'another part of the handbook settles it'),
    ('OPEN', 'no formal source settles it'),
]
RELATION = [
    ('SAME', 'the provision states the same duty'),
    ('BROADER', 'the statement applies in more cases than the provision (it drops a condition)'),
    ('NARROWER', 'the statement applies in fewer cases than the provision'),
    ('DIFFERENT', 'the statement and the provision disagree'),
    ('PENALTY', 'the provision sets the penalty'),
]
SHORT = {'on-hta': 'HTA', 'on-reg-339-94': 'O. Reg. 339/94', 'on-reg-455-07': 'O. Reg. 455/07',
         'on-reg-608': 'Reg. 608', 'on-reg-615': 'Reg. 615'}
LAW_MODAL = re.compile(r'\b(MUST NOT|MUST|MAY)\b')


def anchor(unit_id):
    return re.sub(r'[^a-z0-9]+', '-', unit_id.lower()).strip('-')


def norm_line(s):
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()


class Copy:
    """A law's local copy, to find the line a provision starts on (spacing and curly quotes aside)."""

    def __init__(self, path):
        self.text, self.starts, self.lines = '', [], []
        for n, line in enumerate(open(path, encoding='utf-8', errors='replace'), 1):
            t = norm_line(line)
            if t:
                self.starts.append(len(self.text) + (1 if self.text else 0))
                self.lines.append(n)
                self.text += (' ' if self.text else '') + t

    def line(self, provision):
        i = self.text.find(norm_line(provision))
        return None if i < 0 else self.lines[bisect.bisect_right(self.starts, i) - 1]


def render(db, jurisdiction, title, root, folder):
    """The page for one jurisdiction; folder is where it goes, from the repo root, for its relative links."""
    q = lambda sql, *a: db.execute(sql, a).fetchall()  # noqa: E731
    page = os.path.join(root, folder)
    sources = {s['id']: s for s in q("SELECT * FROM source WHERE kind != 'handbook' AND jurisdiction = ?", jurisdiction)}
    copies = {k: Copy(os.path.join(root, s['path'])) for k, s in sources.items()
              if s['path'] and os.path.exists(os.path.join(root, s['path']))}
    units = {}

    def cite(unit_id):
        u = units.setdefault(unit_id, q('SELECT * FROM unit WHERE id = ?', unit_id)[0])
        return f'[{SHORT.get(u["source_id"], sources[u["source_id"]]["citation"])} {u["locator"].removeprefix("s. ")}](#{anchor(unit_id)})'

    mine = 'run_id IN (SELECT id FROM run WHERE rules_json = 1)'
    statements = q(f"SELECT * FROM statement WHERE jurisdiction = ? AND {mine} ORDER BY position", jurisdiction)
    lines = q(f"SELECT g.* FROM statement_law g JOIN statement s ON s.id = g.statement_id WHERE s.jurisdiction = ? "
              f"AND s.{mine}", jurisdiction)
    duty = {r['statement_id'] for r in lines if LAW_MODAL.search(r['text'])} & \
        {s['id'] for s in statements if s['strength'] == 'ADVICE'}
    flags = collections.Counter(r[0] or 'not grounded' for r in q(
        "SELECT g.status FROM occurrence o JOIN statement s ON s.id = o.statement_id "
        f"LEFT JOIN grounding g ON g.occurrence_id = o.id WHERE s.jurisdiction = ? AND s.{mine}", jurisdiction))

    out = [f'# {title}', '',
           'Generated from the rules database (`db/`) by `python3 tools/db.py export --write`. Do not edit by hand.', '',
           'Each statement is shown as extracted from the handbook, with its flags and their notes unchanged: it is '
           'the reference the extraction is scored against. What the law adds comes under it:', '',
           '- under each flag, how far a formal source settles it, and the provisions or handbook sentences that do;',
           '- **Law**: what the law says on the statement\'s subject, in the rule language, with the provisions it '
           'cites. A word the law leaves as open as the handbook keeps its `[?…]` mark;',
           '- **Compared with the law**: each provision behind the statement and how the statement compares with it.',
           '',
           'Every provision is quoted word for word under [Provisions](#provisions), with a link to its line in the '
           'local copy of the law (`statutes/`, checked by `tools/db.py check`) and to the official page on e-Laws.', '',
           '## Summary', '',
           f'{len(statements)} statements. Law lines are added under {len({r["statement_id"] for r in lines})} of them '
           f'({len(lines)} lines); for {len(duty)}, the handbook words as advice what the law makes a duty.', '',
           '| Flags | | |', '|---|---|---|']
    out += [f'| `{k}` | {flags[k]} | {meaning} |' for k, meaning in STATUS if flags[k]]
    if flags['not grounded']:
        out.append(f'| not grounded | {flags["not grounded"]} | |')
    out += ['', '| Compared with the law | |', '|---|---|']
    out += [f'| `{k}` | {meaning} |' for k, meaning in RELATION]
    out += ['', '## Statements', '']

    for s in statements:
        where = [r[0] for r in q('SELECT u.locator FROM statement_source x JOIN unit u ON u.id = x.unit_id '
                                 'WHERE x.statement_id = ? ORDER BY x.position', s['id'])]
        out += [f'### {s["local_id"]}', '', f'> {s["text"]}', '',
                f'{s["type"]}' + (f', {s["strength"]}' if s['strength'] else '') +
                (f'. Handbook: {"; ".join(dict.fromkeys(where))}' if where else '') + '.', '']
        if s['note']:
            out += [f'_{s["note"]}_', '']
        occ = q('SELECT o.*, g.status, g.definition, g.effect, g.note AS gnote FROM occurrence o '
                'LEFT JOIN grounding g ON g.occurrence_id = o.id WHERE o.statement_id = ? ORDER BY o.position', s['id'])
        if occ:
            out += ['**Flags**', '']
            for o in occ:
                out.append(f'- {o["code"]} "{o["span"]}": {o["note"]}')
                if o['status']:
                    refs = q("SELECT l.unit_id, l.role FROM grounding_link l WHERE l.occurrence_id = ? ORDER BY l.unit_id",
                             o['id'])
                    law = [cite(r['unit_id']) for r in refs if r['role'] != 'handbook']
                    book = [f'handbook {r["unit_id"].split(":", 2)[2]}' for r in refs if r['role'] == 'handbook']
                    said = ' '.join(x for x in (o['definition'], o['effect'], o['gnote']) if x)
                    out.append(f'  - `{o["status"]}`' + (f': {said}' if said else '') +
                               (f' ({", ".join(law + book)})' if law or book else ''))
            out.append('')
        rows = q('SELECT * FROM statement_law WHERE statement_id = ? ORDER BY position', s['id'])
        if rows:
            out += ['**Law**', '']
            for r in rows:
                refs = [x[0] for x in q('SELECT unit_id FROM statement_law_ref WHERE statement_id = ? AND position = ? '
                                        'ORDER BY unit_id', s['id'], r['position'])]
                out.append(f'- `{r["text"]}`')
                out.append('  - ' + ', '.join(cite(u) for u in refs) + (f'. {r["note"]}' if r['note'] else ''))
            out.append('')
        basis = q("SELECT * FROM statement_basis WHERE statement_id = ? ORDER BY relation = 'PENALTY', unit_id", s['id'])
        if basis:
            out += ['**Compared with the law**', '']
            out += [f'- `{b["relation"]}` {cite(b["unit_id"])}' + (f': {b["note"]}' if b['note'] else '') for b in basis]
            out.append('')

    out += ['## Provisions', '']
    for unit_id in sorted(units, key=lambda x: (units[x]['source_id'], x)):
        u, src = units[unit_id], sources[units[unit_id]['source_id']]
        dates = f' (in force from {u["valid_from"]})' if u['valid_from'] else f' (until {u["valid_to"]})' if u['valid_to'] else ''
        heading = f', {u["heading"]}' if u['heading'] else ''
        link = []
        if u['source_id'] in copies:
            n = copies[u['source_id']].line(u['text'])
            if n:
                path = os.path.relpath(os.path.join(root, src['path']), page).replace(os.sep, '/')
                link.append(f'[{os.path.basename(src["path"])}, line {n}]({path}#L{n})')
        if src['url']:
            link.append(f'[e-Laws]({src["url"]})')
        out += [f'<a id="{anchor(unit_id)}"></a>**{src["citation"]}, {u["locator"]}{heading}**{dates}' +
                (f' · {" · ".join(link)}' if link else ''), '', f'> {u["text"]}', '']
    return '\n'.join(out)
