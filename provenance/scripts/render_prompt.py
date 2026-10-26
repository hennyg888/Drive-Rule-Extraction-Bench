"""Fill the extraction prompt with passages and write the chat messages.

Usage (from the repo root):
  python3 provenance/scripts/render_prompt.py --passages analysis/passing-rules/mto/inputs/passing-passages.json \
      --passages analysis/passing-rules/mto/inputs/census-sentences.json \
      --handbook "Ontario MTO Driver's Handbook (ontario.ca, offline copy checked 2026-10-06)" \
      --topic passing --scope-file prompts/topics/passing.txt \
      --out runs/example/messages.json [--page "Signs"] [--preview runs/example/prompt.md]

Writes {"prompt": <prompt file>, "prompt_sha256": ..., "messages": [{"role": "system", ...}, {"role": "user", ...}]}.
Only id, page, sec, kind, text, cap and image are sent; grouping fields such as part and cls are dropped,
because they would give away which passages were excluded.
"""
import argparse, hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))  # this file is in provenance/scripts/
DEFAULT_PROMPT = os.path.join(ROOT, 'prompts', 'extract-rules.md')
KEEP = ('id', 'page', 'sec', 'kind', 'text', 'cap', 'image')


def load_passages(paths):
    out = []
    for p in paths:
        data = json.load(open(p, encoding='utf-8'))
        for x in data:
            y = dict(x)
            if 'id' not in y:  # passing inputs use "m" for the id and "src" for the image
                y['id'] = y.pop('m')
            if 'src' in y and 'image' not in y:
                y['image'] = y.pop('src')
            out.append({k: y[k] for k in KEEP if y.get(k) not in (None, '')} | {'sec': y.get('sec') or ''})
    return out


def split_prompt(path):
    raw = open(path, encoding='utf-8').read()
    head, rest = raw.split('\n<!-- SYSTEM -->\n', 1)  # the markers on lines of their own
    system, user = rest.split('\n<!-- USER -->\n', 1)
    return raw, system.strip() + '\n', user.strip() + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prompt', default=DEFAULT_PROMPT)
    ap.add_argument('--passages', action='append', required=True)
    ap.add_argument('--handbook', required=True)
    ap.add_argument('--topic', required=True)
    ap.add_argument('--scope', default=None)
    ap.add_argument('--scope-file', default=None)
    ap.add_argument('--page', action='append', help='keep only passages on these pages (repeatable)')
    ap.add_argument('--out', required=True)
    ap.add_argument('--preview', default=None, help='also write the filled prompt as one readable file')
    a = ap.parse_args()

    scope = a.scope if a.scope is not None else open(a.scope_file, encoding='utf-8').read().strip()
    passages = load_passages(a.passages)
    if a.page:
        passages = [p for p in passages if p['page'] in a.page]
    order = ('id', 'page', 'sec', 'kind', 'text', 'cap', 'image')
    lines = '\n'.join(json.dumps({k: p[k] for k in order if k in p}, ensure_ascii=False) for p in passages)

    raw, system, user = split_prompt(a.prompt)
    user = (user.replace('{{HANDBOOK}}', a.handbook).replace('{{TOPIC}}', a.topic)
                .replace('{{TOPIC_SCOPE}}', scope).replace('{{PASSAGES}}', lines))
    assert '{{' not in user, 'unfilled slot in the user message'
    msg = {
        'prompt': os.path.relpath(a.prompt, ROOT),
        'prompt_sha256': hashlib.sha256(raw.encode('utf-8')).hexdigest(),
        'n_passages': len(passages),
        'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}],
    }
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(msg, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if a.preview:
        open(a.preview, 'w', encoding='utf-8').write('# SYSTEM\n\n' + system + '\n# USER\n\n' + user)
    print(f'{len(passages)} passages -> {a.out} (prompt sha256 {msg["prompt_sha256"][:12]})')


if __name__ == '__main__':
    main()
