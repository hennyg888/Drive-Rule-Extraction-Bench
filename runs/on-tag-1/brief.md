# Brief given to each tagging run

Each shard went to a fresh Claude subagent with no other context, with this brief, NN replaced by the shard number. R is the repo root of the working copy that ran it.

```text
You are tagging one shard of a driver's handbook for a research pipeline. Follow the tagging prompt exactly.

Rules:
- Do NOT call any mcp__hearthbot__ tools. Do not install packages. Do not use web search or fetch.
- Read only R/runs/on-tag-1/prompt.md and R/runs/on-tag-1/input/shard-NN.jsonl. Do not open any other file of the repo.
- Write files only in R/runs/on-tag-1/output/.

Steps:
1. Read prompt.md in full, then the shard in full (several reads if needed).
2. Tag every sentence id and every figure's para id, in input order, as the prompt says. Write the answer lines in parts of about 100 lines: output/parts-NN/p01.jsonl, p02.jsonl, … (zero-padded), with the Write tool.
3. Join and check them:
   cat R/runs/on-tag-1/output/parts-NN/p*.jsonl > R/runs/on-tag-1/output/shard-NN.jsonl && python3 -I -B R/tools/tag_units.py check on-tag-1 NN
4. Fix every problem it lists (edit the part files, join and check again) until it prints "ok".

Final reply: only "shard NN ok" and the number of lines, or what is still wrong.
```
