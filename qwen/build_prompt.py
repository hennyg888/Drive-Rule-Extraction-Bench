"""Build the extraction prompt (trial task T2) for one handbook: a system prompt and one user message per page.

The system prompt is prompts/extract-rules.md with its placeholders filled:
    {{GRAMMAR}}   the grammar block of analysis/rule-language-v1.md, verbatim
    {{TOPIC}}     prompts/topics/<topic>.md
    {{EXAMPLES}}  prompts/examples/extract-examples.json, rendered like a real batch
Each user message holds one handbook page's passages, in handbook order, with only the fields a
model may see: id, page, heading path, kind, text and caption. The model answers with reading notes
for every passage, then the statements (output_schema()).

PROMPT_VERSION names the prompt; runs are saved under it, so versions can be compared.
v1 (prompts/archive/*.v1.*) was case-based; v2 states general principles and adds the reading notes.

Usage:
    python qwen/build_prompt.py --handbook mto --out runs/prompts/mto     # writes system.md, batches.json
"""
import argparse
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPT_VERSION = "v2.1"

HANDBOOKS = {
    "mto": {
        "name": "Official MTO Driver's Handbook (Ontario, Canada)",
        "units": "metric (m, km, km/h)",
        "passages": ["analysis/passing-rules/inputs/passing-passages.json",
                     "analysis/passing-rules/inputs/census-sentences.json"],
        "segments": "analysis/segments/mto.jsonl",
    },
    "ca": {
        "name": "California Driver's Handbook (California DMV, United States)",
        "units": "US customary (ft, mi, mph)",
        "passages": ["analysis/passing-rules/ca/inputs/passing-passages.json"],
        "segments": "analysis/segments/ca.jsonl",
    },
    "tx": {
        "name": "Texas Driver Handbook (Texas DPS, United States)",
        "units": "US customary (ft, mi, mph)",
        "passages": ["analysis/passing-rules/tx/inputs/passing-passages.json"],
        "segments": "analysis/segments/tx.jsonl",
    },
}


def path(p):
    return os.path.join(ROOT, p)


def grammar_block():
    """The grammar of rule language v1, copied verbatim from the spec so the two cannot drift."""
    text = open(path("analysis/rule-language-v1.md"), encoding="utf-8").read()
    m = re.search(r"### Grammar\n.*?(```\n.*?\n```)", text, re.S)
    return m.group(1)


def output_schema(notes=True):
    """The model's answer: reading notes for every passage, then statements in the frozen statement schema.
    With notes=False, the statement schema alone ({"statements": [...]}), for prompts that ask for no notes."""
    statements = json.load(open(path("analysis/passing-rules/statements.schema.json"), encoding="utf-8"))
    if not notes:
        return statements
    note = {"type": "object", "additionalProperties": False, "required": ["id", "about_topic", "says"],
            "properties": {"id": {"type": "string"}, "about_topic": {"type": "boolean"}, "says": {"type": "string"}}}
    return {"$schema": statements["$schema"], "title": "T2 answer: reading notes, then statements",
            "type": "object", "additionalProperties": False, "required": ["passages", "statements"],
            "properties": {"passages": {"type": "array", "items": note},
                           "statements": statements["properties"]["statements"]}}


def render_passage(p):
    pid = p.get("m") or p.get("id")
    head = f"[{pid}] page: {p.get('page') or '-'} | heading: {p.get('sec') or '(top of page)'} | {p.get('kind', 'text')}"
    if p.get("kind") == "figure":
        return f"{head}\nFigure: {p.get('cap') or p.get('text')}"
    return f"{head}\n{p['text']}"


def render_examples():
    ex = json.load(open(path("prompts/examples/extract-examples.json"), encoding="utf-8"))
    out = []
    for i, e in enumerate(ex["examples"], 1):
        passages = "\n\n".join(render_passage(p) for p in e["passages"])
        answer = json.dumps({"passages": e["reading_notes"], "statements": e["statements"]}, ensure_ascii=False, indent=1)
        out.append(f"## Example {i}: {e['title']}\n\nTopic: {e['topic']}\n\nWhat it shows: {e['teaches']}\n\n"
                   f"Input:\n\n```\n{passages}\n```\n\nAnswer:\n\n```json\n{answer}\n```")
    return "\n\n".join(out)


def system_prompt(topic="passing"):
    tpl = open(path("prompts/extract-rules.md"), encoding="utf-8").read()
    out = (tpl.replace("{{GRAMMAR}}", grammar_block())
              .replace("{{TOPIC}}", open(path(f"prompts/topics/{topic}.md"), encoding="utf-8").read().strip())
              .replace("{{EXAMPLES}}", render_examples()))
    assert "{{" not in out, "unfilled placeholder in the prompt"
    return out


def norm(s):
    return re.sub(r"\s+", " ", (s or "").replace("’", "'")).strip()


def load_passages(hb):
    """The handbook's passages, in handbook order, with only the fields a model may see."""
    cfg = HANDBOOKS[hb]
    passages = [p for f in cfg["passages"] for p in json.load(open(path(f), encoding="utf-8"))]
    order = {}
    if os.path.exists(path(cfg["segments"])):
        segs = [json.loads(l) for l in open(path(cfg["segments"]), encoding="utf-8")]
        seg_index = {s["id"]: i for i, s in enumerate(segs)}
        for p in passages:
            if p.get("seg") in seg_index:  # passage files made by tools/make_passages.py
                order[p.get("m") or p.get("id")] = seg_index[p["seg"]]
                continue
            key = norm(p.get("text"))[:60]
            for i, s in enumerate(segs):
                if (p.get("kind") == "figure" and p.get("src") and s.get("src") == p.get("src")) or \
                   (p.get("kind") != "figure" and key and key in norm(s["text"])):
                    order[p.get("m") or p.get("id")] = i
                    break
    visible = []
    for p in passages:
        pid = p.get("m") or p.get("id")
        visible.append({"m": pid, "page": p.get("page"), "sec": p.get("sec"),
                        "kind": "figure" if p.get("kind") == "figure" else p.get("kind", "text"),
                        "text": p.get("text"), "cap": p.get("cap"), "_order": order.get(pid, 10 ** 6)})
    visible.sort(key=lambda p: p["_order"])
    for p in visible:
        del p["_order"]
    return visible


def batches(hb):
    """One batch per handbook page, in the order pages first appear."""
    groups = {}
    for p in load_passages(hb):
        page = re.sub(r" page · Chapter \d+$", "", p["page"] or "-")
        groups.setdefault(page, []).append(p)
    return list(groups.items())


def user_message(hb, page, passages, topic="passing", notes=True):
    """One batch. With notes=False the closing line refers to no section of our prompt, so the
    message also fits other sessions' prompts that ask only for {"statements": [...]}."""
    cfg = HANDBOOKS[hb]
    body = "\n\n".join(render_passage(p) for p in passages)
    ids = ", ".join(p["m"] for p in passages)
    ask = (f"Write the reading notes for all {len(passages)} passages, then the statements, following sections 4 and 5. "
           if notes else "Write everything these passages say about the topic as rule language v1 statements. ")
    return (f"Handbook: {cfg['name']}\nUnits: {cfg['units']}\nTopic: {topic}\n"
            f"Batch: {len(passages)} passages from the page \"{page}\": {ids}.\n\n{body}\n\n"
            f"{ask}Return only the JSON object.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--handbook", default="mto", choices=sorted(HANDBOOKS))
    ap.add_argument("--topic", default="passing")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    system = system_prompt(a.topic)
    open(os.path.join(a.out, "system.md"), "w", encoding="utf-8").write(system)
    out = [{"batch": page, "passages": [p["m"] for p in ps], "user": user_message(a.handbook, page, ps, a.topic)}
           for page, ps in batches(a.handbook)]
    json.dump(out, open(os.path.join(a.out, "batches.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"system prompt: {len(system):,} chars (~{len(system) // 4:,} tokens)")
    for b in out:
        print(f"  {b['batch']:28} {len(b['passages']):3} passages  {len(b['user']):6,} chars")


if __name__ == "__main__":
    main()
