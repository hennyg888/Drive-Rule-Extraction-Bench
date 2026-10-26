"""Write a readable Markdown page from a rule-language statements file.

The page follows the layout of Henry's "Ontario passing rules.md": statements grouped by
the topic structure, one table per group, modals in bold, a link to the local handbook
for every source, and the verbatim passages at the end. The page is generated: change the
JSON and run this again, never edit the page by hand.

Usage, from the repo root (Ontario):
    python3 tools/render_rules_md.py \
        --statements analysis/passing-rules/mto/rules.json \
        --passages analysis/passing-rules/mto/inputs/passing-passages.json \
                   analysis/passing-rules/mto/inputs/census-sentences.json \
        --structure analysis/passing-rules/mto/inputs/passing-structure.json \
        --handbook-dir handbooks/mto \
        --title "Ontario passing rules" \
        --out analysis/passing-rules/mto/passing-rules.md

California and Texas: the same with ca/ or tx/, no --structure, and handbooks/ca or handbooks/tx.

A passage's link is its `href` when it has one (California, Texas). Otherwise the passage
text is looked up in the pages of --handbook-dir and linked to the nearest h2 above it;
when the text is not found (figures), the passage's page and section names are used.
"""
import argparse
import html
import json
import os
import re
from html.parser import HTMLParser

MODAL = re.compile(r'\b(MUST NOT|SHOULD NOT|MUST|MAY|SHOULD)\b')
FLAG = re.compile(r'\[\?([^\]]+)\]')
STRENGTH = {'LAW': 'Law', 'ADVICE': 'Advice'}
TYPE_WORD = {'FACT': 'Fact', 'DEFINE': 'Definition', 'EXCEPTION': 'Exception'}


def norm(s):
    s = s.replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()


class PageText(HTMLParser):
    """Text of one page, with the offset and id of every h2 that has an id."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.size, self.h2s, self.title = [], 0, [], None
        self._skip = 0
        self._in = None
        self._h2_id = None
        self._buf = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self._skip += 1
        elif tag in ('h1', 'h2'):
            self._in, self._buf = tag, []
            self._h2_id = dict(attrs).get('id') if tag == 'h2' else None

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self._skip -= 1
        elif tag == self._in:
            text = ' '.join(self._buf).strip()
            if tag == 'h1' and self.title is None:
                self.title = text
            elif tag == 'h2' and self._h2_id:
                self.h2s.append((self.size, self._h2_id, text))
            self._in = None

    def handle_data(self, data):
        if self._skip:
            return
        if self._in:
            self._buf.append(data)
        piece = norm(data)
        if piece:
            self.parts.append(piece + ' ')
            self.size += len(piece) + 1

    def text(self):
        return ''.join(self.parts)


def load_pages(folder):
    pages = {}
    for name in sorted(os.listdir(folder)):
        if name.endswith('.html') and name != 'index.html':
            p = PageText()
            with open(os.path.join(folder, name), encoding='utf-8') as f:
                p.feed(f.read())
            pages[name] = (p.text(), p.h2s, p.title or '')
    return pages


def section_name(sec):
    return re.split(r' · | › ', sec or '')[0].strip()


def link_for(passage, pages, base):
    if passage.get('href'):  # recorded from the handbook folder's old name, e.g. ca_drivers_handbook/x.html#y
        href = passage['href']
        return f"{base}/{href.split('/', 1)[1]}" if base and '/' in href else href
    if not pages:
        return None
    probe = norm(passage.get('text', ''))[:80]
    if len(probe) >= 20:
        for name, (text, h2s, _) in pages.items():
            at = text.find(probe)
            if at >= 0:
                above = [h for h in h2s if h[0] <= at]
                return f'{base}/{name}' + (f'#{above[-1][1]}' if above else '')
    # Not found as text (a figure): use the page and section names.
    page = norm(passage.get('page', '').split(' page')[0].split(' · ')[0])
    sec = norm(section_name(passage.get('sec')))
    best = None
    for name, (_, h2s, title) in pages.items():
        words = set(page.split())
        if words and words <= set(norm(title).split()) | set(name[:-5].split('-')):
            for _, hid, htext in h2s:
                if sec and (sec == norm(htext) or norm(htext).endswith(' ' + sec)):
                    return f'{base}/{name}#{hid}'
            best = best or name
    return f'{base}/{best}' if best else None


def cell(s):
    return s.replace('|', '\\|').replace('\n', ' ')


def rule_md(text):
    text = FLAG.sub(lambda m: f'*{m.group(1)}*\u00a0\u2020', text)
    return MODAL.sub(r'**\1**', cell(text))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--statements', required=True)
    ap.add_argument('--passages', nargs='+', required=True)
    ap.add_argument('--structure')
    ap.add_argument('--handbook-dir')
    ap.add_argument('--link-base', help='Path from the output file to --handbook-dir (default: computed)')
    ap.add_argument('--title', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    with open(a.statements, encoding='utf-8') as f:
        data = json.load(f)
    statements = data['statements'] if isinstance(data, dict) else data
    passages = {}
    for path in a.passages:
        with open(path, encoding='utf-8') as f:
            items = json.load(f)
        items = items.get('passages', items) if isinstance(items, dict) else items
        for p in items:
            passages[p.get('m') or p.get('id')] = p

    pages = load_pages(a.handbook_dir) if a.handbook_dir else {}
    base = a.link_base or (os.path.relpath(os.path.abspath(a.handbook_dir), os.path.dirname(os.path.abspath(a.out)))
                           if a.handbook_dir else None)
    links = {pid: link_for(p, pages, base) for pid, p in passages.items()}

    names = {}
    if a.structure:
        with open(a.structure, encoding='utf-8') as f:
            for row in json.load(f):
                for key in ('part', 'group', 'sit'):
                    if row.get(key) and row[key][0]:
                        names[row[key][0]] = row[key][1]

    def unit(sid):  # '3.4.4b' -> '3.4.4', '1a' -> '1'
        return re.sub(r'[a-z]+$', '', sid)

    def group_of(sid):
        u = unit(sid).split('.')
        return '.'.join(u[:2]) if len(u) >= 2 else u[0]

    def place(s):
        """(part heading or None, group heading, situation) of a statement."""
        if names:  # ids follow the topic structure: 3.4.4b is situation 3.4.4 in group 3.4 of part 3
            u, g = unit(s['id']), group_of(s['id'])
            part = f'{g.split(".")[0]} {names.get(g.split(".")[0], "")}'.rstrip() if '.' in g else None
            return part, f'{g} {names.get(g, "")}'.rstrip(), names.get(u, '') if u != g else ''
        # No structure file: group by the page of the first source, situation from its section.
        p = passages.get(s['sources'][0]['id'], {}) if s['sources'] else {}
        sec = (p.get('sec') or '').split(' \u00b7 ')[0]
        return None, re.sub(r'\s*\(Continued\)$', '', p.get('page') or '') or 'Other', sec.split(' \u203a ')[-1]

    out = [f'# {a.title}', '',
           f'Generated from `{a.statements}` by `tools/render_rules_md.py`. Do not edit this page; '
           'change the JSON and run the script again.', '']
    counts = {}
    for s in statements:
        k = STRENGTH.get(s.get('strength'), TYPE_WORD.get(s['type'], s['type']))
        counts[k] = counts.get(k, 0) + 1
    out += [f'{len(statements)} statements: ' + ', '.join(f'{v} {k.lower()}' for k, v in counts.items()) + '.', '',
            'Keywords are in capitals and the modal is in bold. **MUST**, **MUST NOT** and **MAY** are law; '
            '**SHOULD** and **SHOULD NOT** are advice. A word in italics with \u2020 is vague in the handbook '
            'and is kept as written; the notes under each table say why it is flagged.', '']

    defines = [s for s in statements if s['type'] == 'DEFINE']
    if defines:
        out += ['## Terms', '', '| Term | Meaning | ID |', '| --- | --- | --- |']
        for s in defines:
            m = re.match(r'DEFINE (.+?) IS (.+)$', s['text'])
            term, meaning = (m.group(1), m.group(2)) if m else (s['text'], '')
            out.append(f'| {cell(term)} | {rule_md(meaning)} | [{s["id"]}](#{s["id"].replace(".", "")}) |')
        out.append('')

    placed = [(s, *place(s)) for s in statements]
    order = []
    for _, part, group, _ in placed:
        if (part, group) not in order:
            order.append((part, group))

    last_part = None
    for part, group in order:
        if part and part != last_part:
            out += [f'## {part}', '']
            last_part = part
        out += [f'{"###" if part else "##"} {group}', '',
                '| ID | Situation | Statement | Law or advice | Source |', '| --- | --- | --- | --- | --- |']
        notes = []
        for s, sit in [(s, sit) for s, p, g, sit in placed if (p, g) == (part, group)]:
            text = s['text']
            if s.get('steps'):
                text = rule_md(text) + ''.join(f'<br>' + (f'STEP {st["n"]} ' if st['n'].isdigit() else '') + rule_md(st['text']) for st in s['steps'])
            else:
                text = rule_md(text)
            if s.get('note'):
                text += f' *Note:* {cell(s["note"])}'
            kind = STRENGTH.get(s.get('strength'), TYPE_WORD.get(s['type'], s['type']))
            src, done = [], set()
            for so in s['sources']:
                where = so.get('where') or passages.get(so['id'], {}).get('sec') or so['id']
                href = links.get(so['id'])
                key = (where, href)
                if key in done:
                    continue
                done.add(key)
                src.append(f'[{cell(where)}]({href})' if href else cell(where))
            for fig in s.get('see', []):
                img = next((so.get('image') for so in s['sources'] if so['id'] == fig['source'] and so.get('image')), None)
                src.append(f'[{cell(fig["figure"])}]({base}/{img})' if (img and base) else cell(fig['figure']))
            anchor = f'<a id="{s["id"].replace(".", "")}"></a>'
            out.append(f'| {anchor}{s["id"]} | {cell(sit)} | {text} | {kind} | {"; ".join(src)} |')
            for fl in s['flags']:
                notes.append(f'- {s["id"]}, {fl["code"]}, *{fl["span"]}*: {fl["note"]}')
        out.append('')
        if notes:
            out += ['Flags:', ''] + notes + ['']

    cited = []
    for s in statements:
        ids = [so['id'] for so in s['sources']] + [x for st in s.get('steps', []) for x in st['sources']]
        for pid in ids:
            if pid not in cited:
                cited.append(pid)
    out += ['## Source quotes', '', '| Passage | Where | Text |', '| --- | --- | --- |']
    for pid in sorted(cited, key=lambda x: (x[0], int(re.sub(r'\D', '', x) or 0))):
        p = passages.get(pid, {})
        where = ' \u203a '.join(x for x in (p.get('page', '').split(' page')[0], p.get('sec') or '') if x and x != 'None')
        href = links.get(pid)
        where = f'[{cell(where)}]({href})' if href else cell(where)
        out.append(f'| {pid} | {where} | {cell(html.unescape(p.get("text", "")))} |')
    out.append('')

    with open(a.out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    missing = sorted(pid for pid in cited if not links.get(pid))
    print(f'wrote {a.out}: {len(statements)} statements, {len(cited)} passages, '
          f'{len(cited) - len(missing)} linked' + (f'; no link for {", ".join(missing)}' if missing else ''))


if __name__ == '__main__':
    main()
