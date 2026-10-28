# Brief given to the extraction run on-passing-1

Started 2026-10-28 (UTC). One fresh Claude subagent with no other context received this brief, verbatim except that R stands for the repo root of the working copy that ran it. It follows the brief of the 23 October run (`extractions/mto/brief.md`), with two differences: the passages come from the database (`tools/extract_rules.py render`), and the subagent runs `tools/extract_rules.py check` and fixes what it lists, as the tagging runs did.

```text
You are standing in as the model under test for a fixed rule-extraction prompt. Answer the prompt exactly as a model receiving it would.

Rules for this task:
- Do NOT call any mcp__hearthbot__ tools. Do not install packages. Do not use web search or fetch.
- Read only these files: R/runs/on-passing-1/prompt.md, R/runs/on-passing-1/images.txt, and every image it lists (paths from R, for example R/handbooks/mto/images/2-27a.jpg). Look at every figure's image. Do not open, list or search any other file or folder (not /mnt/project-files, not other runs, not the database). The test is only valid if the prompt file and those images are all you use.
- Write files only in R/runs/on-passing-1/run/ and R/runs/on-passing-1/output.json.

Steps:
1. Read prompt.md in full, in several reads if needed. It has a system message (after "# SYSTEM") and a user message (after "# USER") with 138 passages about passing.
2. Produce the statements the prompt asks for. Work through the passages in order; before writing, go over the prompt's checklist (section 8).
3. Write the statements as JSON Lines, one statement object per line, in parts of about 15 statements each: run/part01.jsonl, run/part02.jsonl, … (zero-padded), using the Write tool.
4. Assemble and check them:
python3 -I -c "import json,glob; d='R/runs/on-passing-1'; S=[json.loads(l) for f in sorted(glob.glob(d+'/run/part*.jsonl')) for l in open(f) if l.strip()]; json.dump({'statements': S}, open(d+'/output.json','w'), ensure_ascii=False, indent=1); print(len(S), 'statements')" && python3 -I -B R/tools/extract_rules.py check on-passing-1
5. The check compares the answer with the prompt's output format and the passages. Fix every problem it lists in the part files, then assemble and check again, until it prints "0 problems".

Final reply: only the count of statements by type, and whether the check passed, in under 40 words.
```
