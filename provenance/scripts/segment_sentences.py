"""Split the MTO handbook HTML pages into sentence-level units with structure context.

Usage: python3 provenance/scripts/segment_sentences.py handbooks/mto OUT_DIR   (writes units.jsonl, figures.jsonl, chapters.json)
"""
import re, json, sys, glob, os
from bs4 import BeautifulSoup, NavigableString, Tag

D = sys.argv[1]; OUT = sys.argv[2]

# chapter map from the book TOC in index.html
idx = BeautifulSoup(open(os.path.join(D, 'index.html')).read(), 'html.parser')
toc = idx.find('nav', class_='book-toc').find('ul')
chapters = {}  # slug -> (chapter no, chapter title)
n = 0
for li in toc.find_all('li', recursive=False):
    a = li.find('a'); slug = a['href'].replace('.html', '')
    title = a.get_text(strip=True)
    chapters[slug] = (n, title)
    sub = li.find('ul')
    if sub:
        for a2 in sub.find_all('a'):
            chapters[a2['href'].replace('.html', '')] = (n, title)
    n += 1

ABBR = r'(?:e\.g|i\.e|etc|a\.m|p\.m|No|St|Mr|Mrs|Dr|vs|approx|U\.S|km/h)'
def split_sentences(t):
    t = re.sub(r'\s+', ' ', t).strip()
    if not t: return []
    # protect abbreviations
    prot = re.sub(r'\b(' + ABBR + r')\.', lambda m: m.group(1).replace('.', '§') + '§', t)
    parts = re.split(r'(?:(?<=[.!?])|(?<=[.!?]["”’)]))\s+(?=[A-Z0-9“"(])', prot)
    return [p.replace('§', '.').strip() for p in parts if p.strip()]

def own_text(li):
    # text of an li excluding nested lists
    out = []
    for c in li.children:
        if isinstance(c, Tag) and c.name in ('ul', 'ol'): continue
        out.append(c.get_text(' ') if isinstance(c, Tag) else str(c))
    return re.sub(r'\s+', ' ', ' '.join(out)).strip()

units = []; figs = []
for f in sorted(glob.glob(os.path.join(D, '*.html'))):
    slug = os.path.basename(f)[:-5]
    soup = BeautifulSoup(open(f).read(), 'html.parser')
    art = soup.find('article', class_='content')
    h1 = soup.find('main').find('h1').get_text(' ', strip=True)
    ch_no, ch_title = chapters.get(slug, (-1, '?'))
    path = {'h2': '', 'h3': '', 'h4': ''}
    blk = 0; lead = ''
    def add(kind, text, extra=None):
        global blk
        blk += 1
        for k, s in enumerate(split_sentences(text)):
            u = dict(id=f'{slug}:{blk:03d}.{k+1}', page=slug, page_title=h1, chapter=ch_no, chapter_title=ch_title,
                     section=' > '.join(x for x in (path['h2'], path['h3'], path['h4']) if x),
                     kind=kind, text=s)
            if extra: u.update(extra)
            units.append(u)
    def walk_list(lst, depth, parent_lead):
        ordered = lst.name == 'ol'
        for i, li in enumerate(lst.find_all('li', recursive=False)):
            t = own_text(li)
            if t:
                add('step' if ordered else 'item', t, {'list_lead': parent_lead, 'item_no': i + 1, 'depth': depth})
            for sub in li.find_all(['ul', 'ol'], recursive=False):
                walk_list(sub, depth + 1, t)
    for el in art.children:
        if not isinstance(el, Tag): continue
        if el.name in ('h1', 'h2', 'h3', 'h4'):
            txt = el.get_text(' ', strip=True)
            if el.name == 'h2': path = {'h2': txt, 'h3': '', 'h4': ''}
            elif el.name == 'h3': path['h3'] = txt; path['h4'] = ''
            elif el.name == 'h4': path['h4'] = txt
            add('heading', txt); lead = ''
            continue
        for img in el.find_all('img'):
            figs.append(dict(page=slug, section=path['h2'], alt=img.get('alt', ''), src=img.get('src', '')))
        if el.name == 'p':
            txt = el.get_text(' ', strip=True)
            if not txt: continue
            if re.fullmatch(r'Diagram \S+', txt): continue
            add('para', txt); lead = txt
        elif el.name in ('ul', 'ol'):
            walk_list(el, 1, lead)
        elif el.name in ('figure', 'div'):
            cap = el.find('figcaption')
            txt = (cap.get_text(' ', strip=True) if cap else el.get_text(' ', strip=True))
            if txt and not re.fullmatch(r'Diagram \S+', txt): add('caption', txt)

json.dump(chapters, open(os.path.join(OUT, 'chapters.json'), 'w'), indent=1)
with open(os.path.join(OUT, 'units.jsonl'), 'w') as w:
    for u in units: w.write(json.dumps(u, ensure_ascii=False) + '\n')
with open(os.path.join(OUT, 'figures.jsonl'), 'w') as w:
    for x in figs: w.write(json.dumps(x, ensure_ascii=False) + '\n')
import collections
print('units', len(units), 'figs', len(figs))
print(collections.Counter(u['kind'] for u in units))
print(collections.Counter((u['chapter'], u['chapter_title']) for u in units))
