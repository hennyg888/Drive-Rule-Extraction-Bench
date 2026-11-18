"""Stage 2 of the goldset check pipeline: atomic checks (see goldset_check_pipeline_plan.md).

One LLM call per rule, with the rule in isolation: no corpus, no other rules. Each call gets
    the judge's system prompt (prompts/atomic/system.md)
    the extractor's instructions (prompts/formal-rules: system.md + task.md)   } the same in every call:
    the judge's task (prompts/atomic/task.md)                                   } cached (prompt caching)
    the rule
    the vocabulary entries the rule uses, with the handbook blocks that define them
    each cited block alone (with its page and section heading), and only the images inside it
The first call runs alone to write the cache; the rest run in parallel and read it.
and answers, following prompts/atomic/schema.json, with a list of findings (title, category,
severity, free-text description quoting the handbook, free-text suggested fix, confidence).

The check is fixed: no error taxonomy or other material that changes between runs goes into the
request, so different rule sets and goldset versions are checked the same way.

Usage:
  python error_check_pipelines/goldset/check_atomic.py <rules.json> [--handbook mto]
         [--model anthropic/claude-opus-5-5] [--rules ID ...] [--workers 4] [--dry-run]
         [--set key=value ...] [--skip-format-check] [--out-dir DIR] [--previous OLD_RULES.json]

--previous skips rules already checked in an earlier round: a rule is skipped when OLD_RULES.json has
a rule with the same fields (ignoring id and number, so renumbered rules match) that uses the same
vocabulary entries. Rules that are new, edited, or use a changed vocabulary entry are checked.

Writes the report next to the rules file (or in --out-dir), named by step when the input is
(a1_format.json -> a2_atomic_report.md; see goldset_check_pipeline_plan.md §A2), else
<rules file>_atomic_report.md; and everything else in runs/<time>-check-atomic-<scope>-<step>/
(or runs/<time>-check-atomic-<rules file>/):
    meta.json        what was run (model, prompt and input hashes, git commit) and per-call usage
    prompt/          a copy of the judge prompt used
    <rule id>/       request.md, response.json, output.txt, reasoning.txt, output.json (or error.txt)
    findings.jsonl   one finding per line, with finding_id, stage, rules, detector
    triage.csv       one row per finding, with empty decision / notes columns for the human
    report.md        a copy of the report

--dry-run builds and saves every request without calling the model (and estimates its size).
Stage 1 (check_format.py) must pass first, unless --skip-format-check.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path[:0] = [ROOT, HERE]

from bs4 import BeautifulSoup  # noqa: E402

import check_format  # noqa: E402
from drbench import messages, prompts  # noqa: E402
from drbench.corpus import load_pages  # noqa: E402
from drbench.models import ModelError, get_model  # noqa: E402
from drbench.run import git_commit, parse_json  # noqa: E402

JUDGE_PROMPT = os.path.join(HERE, "prompts", "atomic")
EXTRACTION_PROMPT = "formal-rules"
DEFAULT_MODEL = "anthropic/claude-opus-5-5"  # Opus 5.5, medium effort, on the Anthropic API (same model as openrouter/claude-opus-5.5, which the draft goldset was extracted with)
RUNS = os.path.join(ROOT, "runs")


# ---------------------------------------------------------------- handbook sections

@lru_cache(maxsize=None)
def page_blocks(handbook, page_no):
    """The page as the extractor saw it, split into the <article>'s top-level elements."""
    meta = next((p for p in load_pages(handbook) if p["page"] == page_no), None)
    if meta is None:
        return None, []
    art = BeautifulSoup(messages.page_html(handbook, meta), "html.parser").find("article")
    return meta, [k for k in art.children if getattr(k, "name", None)]


def top_index(kids, block_id):
    """Index of the top-level element that is, or contains, the element with this id."""
    for i, k in enumerate(kids):
        if k.get("id") == block_id or k.find(id=block_id) is not None:
            return i
    return None


def page_of(block_id):
    try:
        return int(block_id.split(".")[0])
    except ValueError:
        return None


def cited_block(handbook, block_id):
    """The cited element alone, wrapped with where it sits: <block id page section>. A figure brings
    its image and caption; a caption id (-c) brings the caption only; a text block brings any image
    inside it. None if the block is not found."""
    meta, kids = page_blocks(handbook, page_of(block_id))
    i = top_index(kids, block_id) if kids else None
    if i is None:
        return None
    el = kids[i] if kids[i].get("id") == block_id else kids[i].find(id=block_id)
    head = next((kids[j] for j in range(i, -1, -1) if kids[j].name in ("h1", "h2")), None)
    page_title = kids[0].get_text(" ", strip=True) if kids[0].name == "h1" else meta.get("title", "")
    section = head.get_text(" ", strip=True) if head is not None and head.name == "h2" else ""
    attrs = f'id="{block_id}" page="{meta["page"]}: {page_title}"' + (f' section="{section}"' if section else "")
    return f"<block {attrs}>\n{el}\n</block>"


def block_parts(handbook, ids):
    """Parts (text and images) for the blocks with these ids, and the ids not found."""
    parts, missing = [], []
    for e in ids:
        html = cited_block(handbook, e)
        if html is None:
            missing.append(e)
        else:
            parts += messages.to_parts(handbook, html + "\n", images=True)
    return parts, missing


# ---------------------------------------------------------------- one request

def vocab_used(rule, vocab):
    """Vocabulary entries whose term appears in the rule's statement (longest terms first)."""
    s, used = rule.get("statement", ""), []
    for v in sorted(vocab, key=lambda v: len(v["term"]), reverse=True):
        pat = check_format.term_pattern(v["term"])
        if pat.search(s):
            used.append(v)
            s = pat.sub(" ", s)
    order = {v["term"]: i for i, v in enumerate(vocab)}
    return sorted(used, key=lambda v: order[v["term"]])


def fixed_prefix(extraction, judge):
    """The part of the user message that is the same for every rule: the extractor's instructions
    and the judge's task. Marked as a cache breakpoint, so with the system prompt it is cached once
    and read back by every later call."""
    text = (f"<extractor_instructions>\n<system>\n{extraction.system}\n</system>\n<task>\n{extraction.task}\n</task>\n"
            f"</extractor_instructions>\n\n<judge_task>\n{judge.task}\n</judge_task>\n\n")
    return [{"type": "text", "text": text, "cache": True}]


def build_content(rule, vocab, handbook, extraction, judge):
    """The user message for one rule, as drbench parts: the cached fixed prefix, then the rule, the
    vocabulary entries it uses with their defining blocks, and the blocks it cites."""
    parts = fixed_prefix(extraction, judge)
    text = f"<rule>\n{json.dumps(rule, ensure_ascii=False, indent=1)}\n</rule>\n\n<vocabulary_used>\n"
    for v in vocab_used(rule, vocab):
        text += json.dumps(v, ensure_ascii=False) + "\n"
        vparts, vmissing = block_parts(handbook, v.get("evidence", []))
        parts.append({"type": "text", "text": text})
        parts += vparts
        text = "".join(f"[block {e} not found]\n" for e in vmissing)
    text += "</vocabulary_used>\n\n"

    cited = rule.get("evidence", [])
    bparts, missing = block_parts(handbook, cited)
    text += f"<cited_blocks>\nThe rule cites: {', '.join(cited) or '(nothing)'}. Each cited block is shown alone.\n"
    if missing:
        text += f"Not found in the handbook: {', '.join(missing)}\n"
    parts.append({"type": "text", "text": text})
    parts += bparts
    parts.append({"type": "text", "text": "</cited_blocks>\n\nReview the rule against the judge task above. Answer with JSON only."})
    return parts


# ---------------------------------------------------------------- calls and outputs

def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def sha256_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run_one(model, rule, content, judge, folder):
    """Call the judge on one rule; save everything in folder. Returns (record, findings)."""
    rid = rule["id"]
    rec = {"rule": rid}
    try:
        r = model.complete(content, system=judge.system, json_schema=judge.schema)
    except ModelError as e:
        write(os.path.join(folder, "error.txt"), str(e) + "\n")
        return {**rec, "error": str(e)}, []
    json.dump(r.raw, open(os.path.join(folder, "response.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    write(os.path.join(folder, "output.txt"), r.text)
    if r.reasoning:
        write(os.path.join(folder, "reasoning.txt"), r.reasoning)
    rec.update({"stop_reason": r.stop_reason, "input_tokens": r.input_tokens, "cache_write_tokens": r.cache_write_tokens,
                "cache_read_tokens": r.cache_read_tokens, "output_tokens": r.output_tokens,
                "reasoning_tokens": r.reasoning_tokens, "seconds": r.seconds, "cost_usd": model.cost(r),
                "request_id": r.request_id})
    data = parse_json(r.text)
    if not isinstance(data, dict) or not isinstance(data.get("findings"), list):
        rec["error"] = "answer is not the findings JSON"
        return rec, []
    json.dump(data, open(os.path.join(folder, "output.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rec["findings"] = len(data["findings"])
    return rec, data["findings"]


def write_outputs(folder, results, rules_by_id, detector):
    """findings.jsonl, triage.csv and report.md from [(rule, record, findings)] in rule order."""
    rows, n = [], 0
    for rule, rec, findings in results:
        for f in findings:
            n += 1
            rows.append({"finding_id": f"S2-{n:03d}", "stage": 2, "rules": [rule["id"]], "detector": detector,
                         "call": rule["id"], **f})
    with open(os.path.join(folder, "findings.jsonl"), "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    cols = ["finding_id", "stage", "rules", "title", "category", "severity", "confidence", "description",
            "suggested_fix", "decision", "notes"]
    with open(os.path.join(folder, "triage.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for row in rows:
            w.writerow({c: ("; ".join(row[c]) if isinstance(row.get(c), list) else row.get(c, "")) for c in cols})
    return rows


def report_md(meta, results, rows):
    t = meta["totals"]
    sev = {s: sum(1 for r in rows if r["severity"] == s) for s in ("major", "minor")}
    lines = [f"# Atomic check (stage 2): {meta['input']}", "",
             f"Judge: {meta['preset']} · run folder: `runs\\{meta['run']}` (requests, responses, findings.jsonl, triage.csv) · "
             f"{t['calls']} rules checked, {t['failed']} failed calls"
             + (f" · ${t['cost_usd']}" if t.get("cost_usd") is not None else ""), ""]
    if meta.get("skipped"):
        lines += [f"Skipped {len(meta['skipped'])} rules already checked: identical to a rule in "
                  f"`{meta['previous']}` (ignoring id and number), with the same vocabulary entries. "
                  f"{', '.join(meta['skipped'])}", ""]
    lines += [f"**{len(rows)} findings** ({sev['major']} major, {sev['minor']} minor) "
              f"in {len({r['call'] for r in rows})} rules.", ""]
    clean = []
    for rule, rec, findings in results:
        if rec.get("error"):
            lines += [f"## {rule['id']}: {rule.get('title', '')}", "", f"- Call failed: {rec['error']}", ""]
            continue
        if not findings:
            clean.append(rule["id"])
            continue
        lines += [f"## {rule['id']}: {rule.get('title', '')}", "", f"> {rule.get('statement', '')}", ""]
        for row in (r for r in rows if r["call"] == rule["id"]):
            lines += [f"### {row['finding_id']}. {row.get('title', '')}", "",
                      f"*{row['category']}* · {row['severity']} · {row['confidence']} confidence", "",
                      row["description"], "",
                      f"- Fix: {row['suggested_fix']}", ""]
    if clean:
        lines += [f"## No findings ({len(clean)} rules)", "", ", ".join(clean), ""]
    return "\n".join(lines)


# ---------------------------------------------------------------- main

def stage2_step(stem):
    """The step id stage 2 writes, from the input's step (goldset_check_pipeline_plan.md §A2):
    a1_format -> a2, a0_freeform -> a2; a step at or past stage 2 (a2.., a3_corpus) -> the next
    round's b2. None when the input is not named by step."""
    m = re.match(r"^([a-z])(\d+)(?:\.\d+)?_", stem)
    if not m:
        return None
    letter, stage = m.group(1), int(m.group(2))
    if stage < 2:
        return f"{letter}2"
    if letter == "z":
        return None
    return f"{chr(ord(letter) + 1)}2"


def rule_key(rule, vocab):
    """What the judge sees of a rule, minus its id and number (so a renumbered rule still matches):
    the rule's other fields plus the vocabulary entries it uses."""
    body = {k: v for k, v in rule.items() if k not in ("id", "number")}
    return json.dumps([body, vocab_used(rule, vocab)], sort_keys=True, ensure_ascii=False)


def split_checked(rules, vocab, prev):
    """Split rules into (to_check, skipped, why) against an earlier rule set already checked.
    A rule is skipped when some earlier rule has the same fields (ignoring id and number) and uses the
    same vocabulary entries. why maps each rule to check to "new", "edited" or "vocabulary changed"."""
    prev_vocab = prev.get("vocabulary", [])
    seen = {rule_key(r, prev_vocab) for r in prev.get("rules", [])}
    bodies = {json.dumps({k: v for k, v in r.items() if k not in ("id", "number")}, sort_keys=True, ensure_ascii=False)
              for r in prev.get("rules", [])}
    prev_titles = {r.get("title") for r in prev.get("rules", [])}  # ids shift when rules are renumbered
    to_check, skipped, why = [], [], {}
    for r in rules:
        if rule_key(r, vocab) in seen:
            skipped.append(r)
            continue
        body = json.dumps({k: v for k, v in r.items() if k not in ("id", "number")}, sort_keys=True, ensure_ascii=False)
        why[r["id"]] = ("vocabulary changed" if body in bodies
                        else "edited" if r.get("title") in prev_titles else "new or retitled")
        to_check.append(r)
    return to_check, skipped, why


def parse_value(v):
    try:
        return json.loads(v)
    except ValueError:
        return v


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("rules", help="rules JSON file")
    ap.add_argument("--handbook", default="mto")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"preset in drbench/models/models.yaml (default {DEFAULT_MODEL})")
    ap.add_argument("--rules", dest="only", nargs="+", metavar="ID", help="check only these rule ids")
    ap.add_argument("--workers", type=int, default=4, help="calls in parallel (default 4)")
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE", help="override a model param")
    ap.add_argument("--dry-run", action="store_true", help="build and save the requests without calling the model")
    ap.add_argument("--skip-format-check", action="store_true")
    ap.add_argument("--allow-lowercase", nargs="*", default=check_format.ALLOW_LOWERCASE, metavar="WORD",
                    help="for the stage 1 check: vocab terms allowed in lowercase (default: pass)")
    ap.add_argument("--out-dir", help="where to write the report (default: the rules file's folder)")
    ap.add_argument("--previous", metavar="RULES_JSON",
                    help="an earlier rule set already checked: skip rules identical to one of its rules "
                         "(ignoring id and number) that use the same vocabulary entries")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    path = os.path.abspath(a.rules)
    data = json.load(open(path, encoding="utf-8"))
    if not a.skip_format_check:
        schema = json.load(open(os.path.join(ROOT, "prompts", EXTRACTION_PROMPT, "schema.json"), encoding="utf-8"))
        out = check_format.check(data, schema, check_format.corpus_ids(a.handbook), a.allow_lowercase)
        if any(out.values()):
            text, n = check_format.report(path, data, out, a.handbook)
            sys.exit(text + "\n\nStage 1 must pass before stage 2 (or use --skip-format-check).")

    rules = data["rules"]
    if a.only:
        unknown = set(a.only) - {r["id"] for r in rules}
        if unknown:
            sys.exit(f"no such rule id(s): {', '.join(sorted(unknown))}")
        rules = [r for r in rules if r["id"] in a.only]
    skipped, why = [], {}
    if a.previous:
        prev_path = os.path.abspath(a.previous)
        prev = json.load(open(prev_path, encoding="utf-8"))
        rules, skipped, why = split_checked(rules, data["vocabulary"], prev)
        counts = {k: sum(1 for v in why.values() if v == k) for k in ("new or retitled", "edited", "vocabulary changed")}
        print(f"against {os.path.relpath(prev_path, ROOT)}: {len(rules)} to check "
              f"({counts['new or retitled']} new or retitled, {counts['edited']} edited, "
              f"{counts['vocabulary changed']} vocabulary changed), "
              f"{len(skipped)} skipped as already checked")
        for r in rules:
            print(f"  check {r['id']}: {why[r['id']]}")
        if not rules:
            sys.exit("nothing to check")

    judge = prompts.load(JUDGE_PROMPT)
    extraction = prompts.load(EXTRACTION_PROMPT)
    overrides = dict(kv.split("=", 1) for kv in a.set)
    model = get_model(a.model, **{k: parse_value(v) for k, v in overrides.items()})

    stem = os.path.splitext(os.path.basename(path))[0]
    step = stage2_step(stem)
    label = f"{os.path.basename(os.path.dirname(path))}-{step}" if step else stem
    name = f"{time.strftime('%Y%m%d-%H%M%S')}-check-atomic-{label}" + ("-dry" if a.dry_run else "")
    folder = os.path.join(RUNS, name)
    os.makedirs(folder)
    shutil.copytree(JUDGE_PROMPT, os.path.join(folder, "prompt"))
    meta = {"run": name, "stage": 2, "started": time.strftime("%Y-%m-%d %H:%M:%S"), "git": git_commit(),
            "input": os.path.relpath(path, ROOT), "input_sha256": sha256_file(path), "handbook": a.handbook,
            **model.describe(), "judge_prompt_sha256": judge.sha256,
            "extraction_prompt": extraction.name, "extraction_prompt_sha256": extraction.sha256,
            "rules": [r["id"] for r in rules], "dry_run": a.dry_run}
    if a.previous:
        meta.update({"previous": os.path.relpath(prev_path, ROOT), "previous_sha256": sha256_file(prev_path),
                     "skipped": [r["id"] for r in skipped], "why_checked": why})

    # build every request first (cheap), so a broken one fails before any money is spent
    jobs = []
    for r in rules:
        sub = os.path.join(folder, r["id"])
        os.makedirs(sub)
        content = build_content(r, data["vocabulary"], a.handbook, extraction, judge)
        write(os.path.join(sub, "request.md"), f"# system\n\n{judge.system}\n\n# user\n\n" + messages.preview(content))
        jobs.append((r, content, sub))

    if a.dry_run:
        chars = [sum(len(p["text"]) for p in c if p["type"] == "text") + len(judge.system) for _, c, _ in jobs]
        imgs = [sum(1 for p in c if p["type"] == "image") for _, c, _ in jobs]
        json.dump(meta, open(os.path.join(folder, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{name}: {len(jobs)} requests built, not sent")
        print(f"  text per request: ~{min(chars) // 4:,}-{max(chars) // 4:,} tokens (avg ~{sum(chars) // 4 // len(chars):,}), "
              f"images per request: {min(imgs)}-{max(imgs)}")
        print(f"-> {os.path.relpath(folder, ROOT)}")
        return

    print(f"{name}: {len(jobs)} rules, judge {a.model}, {a.workers} in parallel")
    done = [0]

    def work(job):
        r, content, sub = job
        rec, findings = run_one(model, r, content, judge, sub)
        done[0] += 1
        status = rec.get("error") or f"{len(findings)} finding(s)"
        print(f"  [{done[0]}/{len(jobs)}] {r['id']}: {status}" + (f", ${rec['cost_usd']}" if rec.get("cost_usd") else ""))
        return r, rec, findings

    # the first call alone writes the cached prefix; the rest, in parallel, read it
    results = [work(jobs[0])]
    with ThreadPoolExecutor(max_workers=max(1, a.workers)) as ex:
        results += list(ex.map(work, jobs[1:]))

    ok = [rec for _, rec, _ in results if "input_tokens" in rec]
    meta["calls"] = [rec for _, rec, _ in results]
    meta["totals"] = {"calls": len(results), "failed": sum(1 for _, rec, _ in results if rec.get("error")),
                      "input_tokens": sum(c["input_tokens"] for c in ok),
                      "cache_write_tokens": sum(c["cache_write_tokens"] for c in ok),
                      "cache_read_tokens": sum(c["cache_read_tokens"] for c in ok),
                      "output_tokens": sum(c["output_tokens"] for c in ok),
                      "reasoning_tokens": sum(c["reasoning_tokens"] for c in ok),
                      "cost_usd": round(sum(c["cost_usd"] or 0 for c in ok), 4) if model.price else None}
    rows = write_outputs(folder, results, {r["id"]: r for r in rules}, f"llm:{a.model}")
    meta["totals"]["findings"] = len(rows)
    json.dump(meta, open(os.path.join(folder, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    report = report_md(meta, results, rows)
    out_dir = os.path.abspath(a.out_dir) if a.out_dir else os.path.dirname(path)
    report_path = os.path.join(out_dir, f"{step}_atomic_report.md" if step else f"{stem}_atomic_report.md")
    write(os.path.join(folder, "report.md"), report)
    write(report_path, report)
    print(f"-> report: {os.path.relpath(report_path, ROOT)}")
    print(f"-> run folder: {os.path.relpath(folder, ROOT)}  {len(rows)} findings, totals: {meta['totals']}")


if __name__ == "__main__":
    main()
