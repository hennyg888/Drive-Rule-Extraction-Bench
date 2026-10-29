"""Run trial task T2 (extract rules) against a vLLM server and save everything.

For each page batch from build_prompt.py it sends the system prompt and the batch, with the
statements JSON schema enforced by vLLM's structured outputs, and saves the prompt, raw answer,
thinking, usage and parsed statements. It then merges the batches into one statements file and
runs tools/check_statements.py on it.

Usage (server started as in qwen/README.md):
    python qwen/run_extract.py --model qwen3.5-0.8b --handbook mto --seed 1 [--thinking] [--workers 16]
Output: runs/t2/<handbook>/<model>/<think|nothink>/seed<k>/
    system.md, <nn>-<page>.json per batch, statements.json (merged), check.txt
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import subprocess
import sys
import time

from openai import OpenAI

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_prompt  # noqa: E402

ROOT = build_prompt.ROOT

# Sampling from each model card (qwen-trial-handoff.md, Sampling), with presence_penalty 0 for every run.
SAMPLING = {
    ("small", True): dict(temperature=1.0, top_p=0.95, top_k=20),
    ("small", False): dict(temperature=1.0, top_p=1.0, top_k=20),
    ("large", True): dict(temperature=1.0, top_p=0.95, top_k=20),
    ("large", False): dict(temperature=0.7, top_p=0.8, top_k=20),
}


def size_class(model):
    return "small" if re.search(r"(0\.8b|2b)\b", model.lower()) else "large"


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def ask(client, args, messages):
    """One request; returns the answer text, thinking, parsed JSON (or None), parse error, finish reason, usage."""
    s = SAMPLING[(size_class(args.model), args.thinking)]
    r = client.chat.completions.create(
        model=args.model, messages=messages,
        response_format={"type": "json_schema", "json_schema": {"name": "answer", "schema": args.schema}},
        temperature=s["temperature"], top_p=s["top_p"], presence_penalty=0.0,
        max_tokens=args.max_tokens, seed=args.seed,
        extra_body={"top_k": s["top_k"], "chat_template_kwargs": {"enable_thinking": args.thinking}},
    )
    msg = r.choices[0].message
    raw = msg.content or ""
    reasoning = getattr(msg, "reasoning", None) or getattr(msg, "reasoning_content", None)
    try:
        parsed, error = json.loads(raw), None
    except json.JSONDecodeError as e:
        parsed, error = None, str(e)
    return raw, reasoning, parsed, error, r.choices[0].finish_reason, r.usage.model_dump() if r.usage else None


def uncited_notes(parsed):
    """Passages the model's own reading notes call about the topic, but that no statement cites."""
    sts = parsed.get("statements", [])
    cited = {s.get("id") for st in sts for s in st.get("sources", [])}
    cited |= {p for st in sts for step in st.get("steps", []) or [] for p in step.get("sources", [])}
    return [n for n in parsed.get("passages", []) if n.get("about_topic") and n.get("id") not in cited]


def repair(client, args, system, res):
    """Completeness repair: ask the model, in the same conversation, to write the statements its own
    reading notes promised but its answer left out. New statements are appended to the batch."""
    parsed = res.get("parsed")
    missing = uncited_notes(parsed) if parsed else []
    if not missing:
        return res
    n = len(parsed.get("statements", []))
    ids = ", ".join(m["id"] for m in missing)
    request = (f"Your reading notes say that passages {ids} are about the topic, but none of your statements "
               "cites them. Fix this now, following sections 4 and 5. If a passage belongs to a statement you "
               "already wrote (a figure that shows it, a lead sentence or heading that gives its condition or "
               "force), return that statement again, complete, with the same id and the passage added to its "
               f"sources. Otherwise write new statements, numbered from s{n + 1}. Return the same JSON shape: "
               f"reading notes for these {len(missing)} passages only, then only the statements you changed "
               "or added.")
    t0 = time.time()
    raw, reasoning, fix, error, finish, usage = ask(client, args, [
        {"role": "system", "content": system}, {"role": "user", "content": res["user"]},
        {"role": "assistant", "content": res["raw"]}, {"role": "user", "content": request}])
    returned = (fix or {}).get("statements", [])
    statements = [dict(st) for st in parsed.get("statements", [])]
    position = {st.get("id"): k for k, st in enumerate(statements)}
    changed, added = [], []
    for st in returned:  # a returned id replaces that statement; anything else is appended
        if st.get("id") in position:
            statements[position[st["id"]]] = st
            changed.append(st["id"])
        else:
            if st.get("id") in {x.get("id") for x in statements}:
                st["id"] = f"s{len(statements) + 1}"
            statements.append(st)
            added.append(st.get("id"))
    res = dict(res)
    res["parsed"] = {"passages": parsed.get("passages", []), "statements": statements}
    res["repair"] = {"missing": [m["id"] for m in missing], "request": request, "raw": raw, "reasoning": reasoning,
                     "parse_error": error, "finish_reason": finish, "usage": usage,
                     "seconds": round(time.time() - t0, 1), "added": len(added), "changed": changed,
                     "still_missing": [m["id"] for m in uncited_notes(res["parsed"])]}
    return res


def run_batch(client, args, system, batch, previous=None):
    """First pass (or a saved first pass from `previous`), then the completeness repair if asked for."""
    if previous is None:
        t0 = time.time()
        raw, reasoning, parsed, error, finish, usage = ask(client, args, [
            {"role": "system", "content": system}, {"role": "user", "content": batch["user"]}])
        s = SAMPLING[(size_class(args.model), args.thinking)]
        res = {"batch": batch["batch"], "passages": batch["passages"], "user": batch["user"],
               "sampling": s | {"presence_penalty": 0.0, "max_tokens": args.max_tokens, "seed": args.seed,
                                "thinking": args.thinking},
               "finish_reason": finish, "usage": usage, "seconds": round(time.time() - t0, 1),
               "raw": raw, "reasoning": reasoning, "parsed": parsed, "parse_error": error}
    else:
        res = previous
    return repair(client, args, system, res) if args.repair else res


def merge(results):
    """One statements list. Ids clash across pages, so each batch's ids get a page prefix (p03:3.4.12a)."""
    merged = []
    for i, res in enumerate(results, 1):
        sts = (res.get("parsed") or {}).get("statements", [])
        prefix = f"p{i:02d}:"
        local = {st.get("id") for st in sts}
        for st in sts:
            st = dict(st)
            st["id"] = prefix + str(st.get("id"))
            st["links"] = [prefix + l if l in local else l for l in st.get("links", [])]
            st["text"] = re.sub(r"\b(EXCEPTION TO|SPECIALIZES) (\S+?)(?=[:\s]|$)",
                                lambda m: f"{m.group(1)} {prefix + m.group(2) if m.group(2) in local else m.group(2)}",
                                st.get("text", ""))
            merged.append(st)
    return merged


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="the --served-model-name of the running server")
    ap.add_argument("--handbook", default="mto", choices=sorted(build_prompt.HANDBOOKS))
    ap.add_argument("--topic", default="passing")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--thinking", action="store_true")
    ap.add_argument("--max-tokens", type=int, default=16384)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--base-url", default="http://localhost:8000/v1")
    ap.add_argument("--batch", help="run only the batch whose page name contains this text")
    ap.add_argument("--repair", action="store_true",
                    help="after each batch, ask the model to write statements for passages its own notes "
                         "call about the topic but no statement cites (saved under <mode>-repair)")
    ap.add_argument("--system-file", help="use this file, verbatim, as the system prompt instead of building ours "
                                          "(e.g. another session's fixed prompt)")
    ap.add_argument("--no-notes", action="store_true",
                    help="ask only for {\"statements\": [...]}, without the reading notes our prompt asks for")
    ap.add_argument("--tag", help="name for the run folder instead of PROMPT_VERSION (needed with --system-file)")
    ap.add_argument("--reuse", action="store_true",
                    help="with --repair: take the first pass from the saved run without --repair instead of asking again")
    a = ap.parse_args()

    mode = "think" if a.thinking else "nothink"
    if a.system_file and not a.tag:
        ap.error("--system-file needs --tag, so the run is not filed under our own prompt version")
    if a.repair and a.no_notes:
        ap.error("--repair works from the reading notes, so it cannot be used with --no-notes")
    a.schema = build_prompt.output_schema(notes=not a.no_notes)
    base = os.path.join(ROOT, "runs", "t2", a.handbook, a.model, a.tag or build_prompt.PROMPT_VERSION)
    out = os.path.join(base, mode + ("-repair" if a.repair else ""), f"seed{a.seed}")
    previous = {}
    if a.reuse:
        first = os.path.join(base, mode, f"seed{a.seed}")
        for f in sorted(os.listdir(first)):
            if re.match(r"\d\d-.*\.json$", f):
                saved = json.load(open(os.path.join(first, f), encoding="utf-8"))
                previous[saved["batch"]] = saved
    os.makedirs(out, exist_ok=True)
    system = (open(a.system_file, encoding="utf-8").read() if a.system_file
              else build_prompt.system_prompt(a.topic))
    if a.reuse:  # the repair continues the saved conversation, so it must use that run's exact prompt
        system = open(os.path.join(base, mode, f"seed{a.seed}", "system.md"), encoding="utf-8").read()
    open(os.path.join(out, "system.md"), "w", encoding="utf-8").write(system)
    batches = [{"batch": page, "passages": [p["m"] for p in ps],
                "user": build_prompt.user_message(a.handbook, page, ps, a.topic, notes=not a.no_notes)}
               for page, ps in build_prompt.batches(a.handbook)]
    if a.batch:
        batches = [b for b in batches if a.batch.lower() in b["batch"].lower()]

    client = OpenAI(base_url=a.base_url, api_key="EMPTY", timeout=3600)
    results = [None] * len(batches)
    with cf.ThreadPoolExecutor(a.workers) as pool:
        futures = {pool.submit(run_batch, client, a, system, b, previous.get(b["batch"])): i
                   for i, b in enumerate(batches)}
        for f in cf.as_completed(futures):
            i = futures[f]
            res = f.result()
            results[i] = res
            json.dump(res, open(os.path.join(out, f"{i + 1:02d}-{slug(res['batch'])}.json"), "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
            n = len((res["parsed"] or {}).get("statements", []))
            fix = res.get("repair")
            print(f"{res['batch']:28} {n:3} statements  {res['finish_reason']:6} {res['seconds']:6}s"
                  + (f"  PARSE ERROR {res['parse_error']}" if res["parse_error"] else "")
                  + (f"  repair: {len(fix['missing'])} passages, +{fix['added']} new, {len(fix['changed'])} amended, "
                     f"still missing {fix['still_missing'] or 'none'}" if fix else ""))

    merged = merge(results)
    notes = [n for r in results for n in (r.get("parsed") or {}).get("passages", [])]
    json.dump({"passages": notes, "statements": merged}, open(os.path.join(out, "statements.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    capped = sum(r["finish_reason"] == "length" for r in results)
    print(f"{len(merged)} statements from {len(results)} batches; {capped} hit max_tokens -> {out}")
    passages = [os.path.join(ROOT, p) for p in build_prompt.HANDBOOKS[a.handbook]["passages"]]
    chk = subprocess.run([sys.executable, os.path.join(ROOT, "tools/check_statements.py"),
                          os.path.join(out, "statements.json"), "--passages", *passages],
                         capture_output=True, text=True)
    open(os.path.join(out, "check.txt"), "w").write(chk.stdout + chk.stderr)
    print(chk.stdout.strip().splitlines()[-1] if chk.stdout.strip() else chk.stderr[-500:])


if __name__ == "__main__":
    main()
