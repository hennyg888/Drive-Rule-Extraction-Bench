"""Draw pipeline/pipeline.svg. Usage: python3 -I make_pipeline_svg.py OUT.svg"""
import sys
from xml.sax.saxutils import escape as esc

W, H = 1510, 780
BW, GAP, X0 = 186, 24, 32
Y1, BH1 = 118, 176
C = {  # fill, stroke, text accent
    'hb': ('#EAF2FB', '#2F6DB5', '#1F4E86'),
    'run': ('#EAF6EE', '#2E8B57', '#1E6A40'),
    'once': ('#F1EDF9', '#6A4BB0', '#4B3285'),
    'down': ('#F4F4F4', '#777777', '#444444'),
}
out = []
def box(x, y, w, h, kind, num, title, lines, dashed=False, person=False):
    f, s, a = C[kind]
    dash = ' stroke-dasharray="7 5"' if dashed else ''
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{f}" stroke="{s}" stroke-width="{3 if person else 1.6}"{dash}/>')
    ty = y + 28
    label = f'{num}  {title}' if num else title
    out.append(f'<text x="{x + 14}" y="{ty}" class="t" fill="{a}">{esc(label)}</text>')
    if person:
        out.append(f'<g transform="translate({x + w - 32},{y + h - 34})" fill="{s}"><circle cx="8" cy="5" r="5"/><path d="M0 22 Q8 8 16 22 Z"/></g>')
    ty += 10
    for kind_, txt in lines:
        ty += 19 if kind_ != 'gap' else 8
        if kind_ == 'gap':
            continue
        cls = {'tool': 'm', 'out': 'o', 'note': 'n'}[kind_]
        out.append(f'<text x="{x + 14}" y="{ty}" class="{cls}">{esc(txt)}</text>')

def arrow(d, label=None, lx=0, ly=0, anchor='middle', color='#555'):
    out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.8" marker-end="url(#ah)"/>')
    if label:
        out.append(f'<text x="{lx}" y="{ly}" class="a" text-anchor="{anchor}">{esc(label)}</text>')

xs = [X0 + i * (BW + GAP) for i in range(7)]
steps = [
    ('hb', '1', 'Acquire', [('tool', 'scrape_<x>_handbook.py'), ('gap', ''), ('out', 'HTML pages, images'), ('out', 'source PDF'), ('note', 'Ontario, California,'), ('note', 'Texas: one layout')], False),
    ('hb', '2', 'Parse', [('tool', 'segment_handbook.py'), ('gap', ''), ('out', 'block passages with'), ('out', 'heading path'), ('out', 'analysis/segments/'), ('note', 'census: sentences')], False),
    ('run', '3', 'Select passages', [('tool', 'a person (Ontario)'), ('tool', 'select-passages.md'), ('gap', ''), ('out', 'passages JSON'), ('out', 'topic text'), ('note', 'ON 105, CA 105, TX 145')], True),
    ('run', '4', 'Extract', [('tool', 'fixed-v1 prompt'), ('tool', '+ any model'), ('gap', ''), ('out', 'statements JSON'), ('out', 'raw output, prompt'), ('out', 'one folder per run')], False),
    ('run', '5', 'Validate, score', [('tool', 'check_statements.py'), ('tool', 'score_t2.py'), ('gap', ''), ('out', 'schema and syntax'), ('out', 'agreement report'), ('out', 'hard cases')], False),
    ('run', '6', 'Review', [('tool', 'a person, side by side'), ('tool', 'passing-rules-*.html'), ('gap', ''), ('out', 'accepted statements'), ('out', 'corrections, notes')], True),
    ('once', '7', 'Reference set', [('tool', 'frozen, versioned'), ('gap', ''), ('out', 'Ontario: 88 statements'), ('out', 'CA 83, TX 104: drafts'), ('out', 'provenance/'), ('out', 'SHA256SUMS')], False),
]
for i, (k, n, t, ls, p) in enumerate(steps):
    box(xs[i], Y1, BW, BH1, k, n, t, ls, person=p)
for i in range(6):
    arrow(f'M{xs[i] + BW + 2} {Y1 + BH1 / 2} L{xs[i + 1] - 4} {Y1 + BH1 / 2}')

# row 2
Y2, BH2 = 392, 150
cx, cw = xs[1], BW * 2 + GAP - 56
box(cx, Y2, cw, BH2, 'hb', 'C', 'Census (optional per handbook)', [('tool', 'segment_sentences.py, make_census_shards.py'), ('tool', '8 labellers, census-guidelines.md'), ('gap', ''), ('out', 'Ontario: 3,444 labelled sentences,'), ('out', 'type, modal, clauses, vague words')], dashed=True)
lx, lw = xs[3] + 44, BW * 2 + GAP - 44
box(lx, Y2, lw, BH2, 'once', 'L', 'Rule language, prompt and schema', [('tool', 'frozen; a change makes a new version'), ('gap', ''), ('out', 'rule-language-v1.md, statements.schema.json'), ('out', 'prompt: extract-rules.fixed-v1.md'), ('out', '(chosen 23 October; v2.1 kept as a variant)')])

# arrows between rows
px = xs[1] + BW / 2
arrow(f'M{px} {Y1 + BH1 + 2} L{px} {Y2 - 4}', 'units', px + 8, (Y1 + BH1 + Y2) / 2 + 4, 'start')
sx = xs[2] + BW / 2
arrow(f'M{sx} {Y2 - 2} L{sx} {Y1 + BH1 + 4}', 'topic sentences', sx + 8, (Y1 + BH1 + Y2) / 2 + 4, 'start')
arrow(f'M{cx + cw + 2} {Y2 + 75} L{lx - 4} {Y2 + 75}', 'fit, force,', (cx + cw + lx) / 2, Y2 + 61)
out.append(f'<text x="{(cx + cw + lx) / 2}" y="{Y2 + 95}" class="a" text-anchor="middle">vague words</text>')
ex = xs[3] + BW / 2
arrow(f'M{ex} {Y2 - 2} L{ex} {Y1 + BH1 + 4}', 'prompt', ex + 8, (Y1 + BH1 + Y2) / 2 + 4, 'start')
vx = xs[4] + BW / 2
arrow(f'M{vx} {Y2 - 2} L{vx} {Y1 + BH1 + 4}', 'schema', vx + 8, (Y1 + BH1 + Y2) / 2 + 4, 'start')

# feedback: reference -> score
rx = xs[6] + BW / 2
arrow(f'M{rx} {Y1 - 2} C{rx} {Y1 - 52} {vx} {Y1 - 52} {vx} {Y1 - 6}', None, color='#6A4BB0')
out.append(f'<text x="{(rx + vx) / 2}" y="{Y1 - 46}" class="a" text-anchor="middle" fill="#4B3285">ground truth for scoring later runs</text>')

# downstream
Y3, BH3 = 610, 112
dx = xs[5]
box(dx, Y3, BW * 2 + GAP, BH3, 'down', '', 'Downstream', [('out', 'Qwen trials: T2 runs on the Ontario passages,'), ('out', 'scored against the reference (qwen/)'), ('out', 'Driving VLA: retrieve, ground, check, cite')])
arrow(f'M{rx} {Y1 + BH1 + 2} L{rx} {Y3 - 4}', 'rules as context', rx + 8, Y3 - 16, 'start')

# legend
lg = [('hb', 'Once per handbook'), ('run', 'Per topic and run'), ('once', 'Fixed, versioned'), ('down', 'Uses the rules')]
lx0 = X0
ly0 = Y3 + 8
out.append(f'<text x="{lx0}" y="{ly0 + 6}" class="t" fill="#333">Key</text>')
for i, (k, t) in enumerate(lg):
    f, s, a = C[k]
    yy = ly0 + 22 + i * 24
    out.append(f'<rect x="{lx0}" y="{yy}" width="28" height="16" rx="4" fill="{f}" stroke="{s}" stroke-width="1.6"/>')
    out.append(f'<text x="{lx0 + 38}" y="{yy + 13}" class="m">{t}</text>')
yy = ly0 + 22 + 4 * 24
out.append(f'<rect x="{lx0}" y="{yy}" width="28" height="16" rx="4" fill="#fff" stroke="#555" stroke-width="1.4" stroke-dasharray="5 4"/><text x="{lx0 + 38}" y="{yy + 13}" class="m">Optional</text>')
out.append(f'<g transform="translate({lx0 + 200},{ly0 + 20})" fill="#2E8B57"><circle cx="8" cy="5" r="5"/><path d="M0 22 Q8 8 16 22 Z"/></g><text x="{lx0 + 224}" y="{ly0 + 38}" class="m">Done by a person</text>')
out.append(f'<text x="{lx0 + 200}" y="{ly0 + 70}" class="n">Steps 1, 2 and C repeat for a new handbook;</text>')
out.append(f'<text x="{lx0 + 200}" y="{ly0 + 89}" class="n">3 to 6 repeat for each topic and model;</text>')
out.append(f'<text x="{lx0 + 200}" y="{ly0 + 108}" class="n">L changes only as a new version.</text>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="context-stroke"/></marker>
<style>.t{{font-size:17px;font-weight:700}} .m{{font-size:13px;fill:#333}} .o{{font-size:13.5px;fill:#111}} .n{{font-size:13px;fill:#555;font-style:italic}} .a{{font-size:12.5px;fill:#444}} .h{{font-size:22px;font-weight:700;fill:#111}} .s{{font-size:14px;fill:#555}}</style></defs>
<rect width="{W}" height="{H}" fill="#ffffff"/>
<text x="{X0}" y="40" class="h">Handbook rule extraction pipeline</text>
<text x="{X0}" y="64" class="s">Drive-Rule-Extraction-Bench · current procedure as of 23 October 2026</text>
{chr(10).join(out)}
</svg>
'''
open(sys.argv[1], 'w').write(svg)
print('wrote', sys.argv[1])
