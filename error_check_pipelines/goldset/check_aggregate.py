"""Stage 3 of the goldset check pipeline: aggregate check (see goldset_check_pipeline_plan.md).

One LLM call on the whole rule set against the whole handbook. The call gets
    the extractor's instructions (prompts/formal-rules: system.md + task.md), which name the topic
    the whole corpus as the extractor saw it (table of contents, every page, images)
    the rule set with its vocabulary
    the judge's instructions (prompts/aggregate/task.md)
and answers, following prompts/aggregate/schema.json, with findings about the set as a whole:
coverage (what the handbook states about the topic that the set leaves out or under-uses) and
conflicts between rules (contradictions, overlaps, duplicates, inconsistent terms or strength),
plus any other error of the set.

The check is fixed: no error taxonomy or other material that changes between runs goes into the
request, so different rule sets and goldset versions are checked the same way.

Usage:
  python error_check_pipelines/goldset/check_aggregate.py <rules.json> [--handbook mto]
         [--model anthropic/claude-opus-5-5] [--no-images] [--dry-run] [--set key=value ...]
         [--skip-format-check] [--out-dir DIR]

Writes the report next to the rules file (or in --out-dir), named by step when the input is
(a2_atomic.json -> a3_aggregate_report.md; see goldset_check_pipeline_plan.md §A2), else
<rules file>_aggregate_report.md; and everything else in runs/<time>-check-aggregate-<scope>-<step>/
(or runs/<time>-check-aggregate-<rules file>/):
    meta.json        what was run (model, prompt and input hashes, git commit) and usage
    prompt/          a copy of the judge prompt used
    request.md, response.json, output.txt, reasoning.txt, output.json (or error.txt)
    findings.jsonl   one finding per line, with finding_id, stage, rules, detector
    triage.csv       one row per finding, with empty decision / notes columns for the human
    report.md        a copy of the report

--dry-run builds and saves the request without calling the model (and estimates its size; with an
Anthropic preset it also counts the input tokens, which is free).
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

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path[:0] = [ROOT, HERE]

import check_format  # noqa: E402
from drbench import messages, prompts  # noqa: E402
from drbench.models import ModelError, get_model  # noqa: E402
from drbench.run import git_commit, parse_json  # noqa: E402

JUDGE_PROMPT = os.path.join(HERE, "prompts", "aggregate")
EXTRACTION_PROMPT = "formal-rules"
DEFAULT_MODEL = "anthropic/claude-opus-5-5"  # Opus 5.5, medium effort, on the Anthropic API
RUNS = os.path.join(ROOT, "runs")
STAGE = 3
KINDS = [("coverage", "Coverage"), ("conflict", "Conflicts"), ("other", "Other")]


# ---------------------------------------------------------------- the request

def build_content(data, handbook, extraction, images=True):
    """The user message, as drbench parts: extractor instructions, corpus, rule set."""
    head = (f"<extractor_instructions>\n<system>\n{extraction.system}\n</system>\n<task>\n{extraction.task}\n</task>\n"
            f"</extractor_instructions>\n\n<handbook>\n")
    corpus = messages.build(handbook, None, images=images, toc=True)[0]["content"]
    rules = {k: data[k] for k in ("scope", "vocabulary", "rules") if k in data}
    tail = f"\n</handbook>\n\n<rule_set>\n{json.dumps(rules, ensure_ascii=False, indent=1)}\n</rule_set>\n\n"
    return [{"type": "text", "text": head}] + corpus + [{"type": "text", "text": tail}]


def stage3_step(stem):
    """The step id stage 3 writes, from the input's step (goldset_check_pipeline_plan.md §A2):
    a2_atomic -> a3 (and a1, a2.2 -> a3); a step at or past stage 3 -> the next round's b3.
    None when the input is not named by step."""
    m = re.match(r"^([a-z])(\d+)(?:\.\d+)?_", stem)
    if not m:
        return None
    letter, stage = m.group(1), int(m.group(2))
    if stage < STAGE:
        return f"{letter}{STAGE}"
    return None if letter == "z" else f"{chr(ord(letter) + 1)}{STAGE}"


# ---------------------------------------------------------------- outputs

def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def sha256_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def write_outputs(folder, findings, detector):
    """findings.jsonl and triage.csv; returns the rows."""
    order = {k: i for i, (k, _) in enumerate(KINDS)}
    findings = sorted(findings, key=lambda f: (order.get(f.get("kind"), 9), f.get("severity") != "major"))
    rows = [{"finding_id": f"S{STAGE}-{i:03d}", "stage": STAGE, "detector": detector, "call": "set", **f}
            for i, f in enumerate(findings, 1)]
    with open(os.path.join(folder, "findings.jsonl"), "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    cols = ["finding_id", "stage", "kind", "rules", "title", "category", "severity", "confidence", "description",
            "suggested_fix", "decision", "notes"]
    with open(os.path.join(folder, "triage.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for row in rows:
            w.writerow({c: ("; ".join(row[c]) if isinstance(row.get(c), list) else row.get(c, "")) for c in cols})
    return rows


def report_md(meta, rows, error=None):
    t = meta["totals"]
    lines = [f"# Aggregate check (stage 3): {meta['input']}", "",
             f"Judge: {meta['preset']} · run folder: `runs\\{meta['run']}` (request, response, findings.jsonl, triage.csv) · "
             f"{meta['n_rules']} rules, whole corpus"
             + (f" · ${t['cost_usd']}" if t.get("cost_usd") is not None else ""), ""]
    if error:
        return "\n".join(lines + [f"Call failed: {error}", ""])
    sev = {s: sum(1 for r in rows if r["severity"] == s) for s in ("major", "minor")}
    lines += [f"**{len(rows)} findings** ({sev['major']} major, {sev['minor']} minor): "
              + ", ".join(f"{sum(1 for r in rows if r['kind'] == k)} {k}" for k, _ in KINDS) + ".", ""]
    for kind, heading in KINDS:
        group = [r for r in rows if r["kind"] == kind]
        if not group:
            continue
        lines += [f"## {heading}", ""]
        for row in group:
            rules = ", ".join(row["rules"]) if row["rules"] else "no rule"
            lines += [f"### {row['finding_id']}. {row['title']}", "",
                      f"*{row['category']}* · {row['severity']} · {row['confidence']} confidence · rules: {rules}", "",
                      row["description"], "",
                      f"- Fix: {row['suggested_fix']}", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------- main

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
    ap.add_argument("--no-images", action="store_true", help="send the corpus without images (alt text stays)")
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE", help="override a model param")
    ap.add_argument("--dry-run", action="store_true", help="build and save the request without calling the model")
    ap.add_argument("--skip-format-check", action="store_true")
    ap.add_argument("--allow-lowercase", nargs="*", default=check_format.ALLOW_LOWERCASE, metavar="WORD",
                    help="for the stage 1 check: vocab terms allowed in lowercase (default: pass)")
    ap.add_argument("--out-dir", help="where to write the report (default: the rules file's folder)")
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
            text, _ = check_format.report(path, data, out, a.handbook)
            sys.exit(text + "\n\nStage 1 must pass before stage 3 (or use --skip-format-check).")

    judge = prompts.load(JUDGE_PROMPT)
    extraction = prompts.load(EXTRACTION_PROMPT)
    overrides = dict(kv.split("=", 1) for kv in a.set)
    model = get_model(a.model, **{k: parse_value(v) for k, v in overrides.items()})

    stem = os.path.splitext(os.path.basename(path))[0]
    step = stage3_step(stem)
    label = f"{os.path.basename(os.path.dirname(path))}-{step}" if step else stem
    name = f"{time.strftime('%Y%m%d-%H%M%S')}-check-aggregate-{label}" + ("-dry" if a.dry_run else "")
    folder = os.path.join(RUNS, name)
    os.makedirs(folder)
    shutil.copytree(JUDGE_PROMPT, os.path.join(folder, "prompt"))
    meta = {"run": name, "stage": STAGE, "started": time.strftime("%Y-%m-%d %H:%M:%S"), "git": git_commit(),
            "input": os.path.relpath(path, ROOT), "input_sha256": sha256_file(path), "handbook": a.handbook,
            "images": not a.no_images, **model.describe(), "judge_prompt_sha256": judge.sha256,
            "extraction_prompt": extraction.name, "extraction_prompt_sha256": extraction.sha256,
            "n_rules": len(data["rules"]), "dry_run": a.dry_run}

    content = build_content(data, a.handbook, extraction, images=not a.no_images)
    content.append({"type": "text", "text": judge.task})
    write(os.path.join(folder, "request.md"), f"# system\n\n{judge.system}\n\n# user\n\n" + messages.preview(content))

    if a.dry_run:
        chars = sum(len(p["text"]) for p in content if p["type"] == "text") + len(judge.system)
        imgs = sum(1 for p in content if p["type"] == "image")
        print(f"{name}: request built, not sent")
        print(f"  {len(data['rules'])} rules; text ~{chars // 4:,} tokens, {imgs} images")
        if hasattr(model, "count_tokens"):
            try:
                meta["input_tokens_counted"] = model.count_tokens(content, system=judge.system)
                print(f"  input tokens (counted by the API): {meta['input_tokens_counted']:,}")
            except Exception as e:  # counting is a convenience; never fail the dry run on it
                print(f"  (token count failed: {e})")
        json.dump(meta, open(os.path.join(folder, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"-> {os.path.relpath(folder, ROOT)}")
        return

    print(f"{name}: {len(data['rules'])} rules against the whole corpus, judge {a.model}")
    rec, rows, error = {}, [], None
    try:
        r = model.complete(content, system=judge.system, json_schema=judge.schema)
    except ModelError as e:
        error = str(e)
        write(os.path.join(folder, "error.txt"), error + "\n")
    else:
        json.dump(r.raw, open(os.path.join(folder, "response.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        write(os.path.join(folder, "output.txt"), r.text)
        if r.reasoning:
            write(os.path.join(folder, "reasoning.txt"), r.reasoning)
        rec = {"stop_reason": r.stop_reason, "input_tokens": r.input_tokens, "output_tokens": r.output_tokens,
               "reasoning_tokens": r.reasoning_tokens, "seconds": r.seconds, "cost_usd": model.cost(r),
               "request_id": r.request_id}
        out = parse_json(r.text)
        if not isinstance(out, dict) or not isinstance(out.get("findings"), list):
            error = f"answer is not the findings JSON (stop: {r.stop_reason})"
        else:
            json.dump(out, open(os.path.join(folder, "output.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            rows = write_outputs(folder, out["findings"], f"llm:{a.model}")

    meta["call"] = {**rec, **({"error": error} if error else {})}
    meta["totals"] = {"findings": len(rows), "failed": bool(error), "cost_usd": rec.get("cost_usd")}
    json.dump(meta, open(os.path.join(folder, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    report = report_md(meta, rows, error)
    out_dir = os.path.abspath(a.out_dir) if a.out_dir else os.path.dirname(path)
    report_path = os.path.join(out_dir, f"{step}_aggregate_report.md" if step else f"{stem}_aggregate_report.md")
    write(os.path.join(folder, "report.md"), report)
    write(report_path, report)
    print(f"-> report: {os.path.relpath(report_path, ROOT)}")
    print(f"-> run folder: {os.path.relpath(folder, ROOT)}  {len(rows)} findings, call: {meta['call']}")
    if error:
        sys.exit(1)


if __name__ == "__main__":
    main()
