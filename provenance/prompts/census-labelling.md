# Census labelling prompt (10 October 2026)

The census labelled all 3,444 handbook sentences (every unit of `units.jsonl` except headings and the sample-test page) against the v0 grammar. Eight labellers ran in parallel, each a Claude subagent started from the main working session with the prompt below. The eight prompts are identical except for the shard number `{N}`; the text below is shard 1's prompt with `1` replaced by `{N}`, and the check that substituting 1 to 8 gives back each prompt exactly passed.

The labelling instrument itself, which the prompt tells each labeller to follow, is `analysis/census/census-guidelines.md`. The paths are the working session's scratch folder and the project's shared folder at the time; in the repo the same files are:

| Path in the prompt | In the repo |
|---|---|
| `/mnt/project-files/Wise Lab/analysis/census/census-guidelines.md` | `analysis/census/census-guidelines.md` |
| `…/scratchpad/census/shard{N}.txt`, `shard{N}.ids` | rebuilt byte for byte by `provenance/scripts/make_census_shards.py` (sha256 in `provenance/SHA256SUMS`) |
| `…/scratchpad/census/validate.py` | `provenance/scripts/validate_labels.py` |
| `…/scratchpad/census/out{N}.jsonl` | merged into `analysis/census/census-labels.jsonl` |

| Shard | Sentences | Started (UTC) | Finished (UTC) |
|---|---|---|---|
| 1 | 438 | 22:14:10 | 22:40:47 |
| 2 | 432 | 22:14:17 | 22:52:52 |
| 3 | 437 | 22:14:25 | 22:48:50 |
| 4 | 431 | 22:14:32 | 22:46:34 |
| 5 | 437 | 22:14:39 | 22:43:49 |
| 6 | 432 | 22:14:46 | 22:49:29 |
| 7 | 447 | 22:14:54 | 22:48:34 |
| 8 | 390 | 22:15:02 | 22:47:54 |

## Prompt

```
You are labelling one shard of a sentence-level census of the Ontario MTO Driver's Handbook for a research project. Do NOT call any mcp__hearthbot__ tools. Do not install packages. Do not edit any file except your own output files listed below.

Read these first, fully:
1. Guidelines (the labelling instrument, follow it exactly): /mnt/project-files/Wise Lab/analysis/census/census-guidelines.md
2. Your shard: /tmp/claude-0/-home-claude/46a3f50f-176e-5b40-9875-68ebad1b6086/scratchpad/census/shard{N}.txt  (the ids you must label are listed in shard{N}.ids in the same folder)

Task: output one JSON object per labelled line of the shard (every `[id]` line; skip `##`/`###` heading lines), with exactly the keys in the guidelines, in shard order. Read each sentence in its section context (headings and list leads matter). Label carefully and consistently; for RULE/STEP/DEFINE/CONSEQ write the one-line v0 rewrite `v` and judge `fit` honestly after trying the rewrite.

Writing: write the output in parts with the Write tool, about 60 lines per part, to files named
/tmp/claude-0/-home-claude/46a3f50f-176e-5b40-9875-68ebad1b6086/scratchpad/census/out{N}.part01.jsonl, out{N}.part02.jsonl, ... (zero-padded). When all parts are written, concatenate them in order into out{N}.jsonl in the same folder (e.g. `cat out{N}.part*.jsonl > out{N}.jsonl`), then run:
python3 -I /tmp/claude-0/-home-claude/46a3f50f-176e-5b40-9875-68ebad1b6086/scratchpad/census/validate.py /tmp/claude-0/-home-claude/46a3f50f-176e-5b40-9875-68ebad1b6086/scratchpad/census/shard{N}.ids /tmp/claude-0/-home-claude/46a3f50f-176e-5b40-9875-68ebad1b6086/scratchpad/census/out{N}.jsonl
Fix every reported problem (missing ids, bad enum values, missing rewrites) and re-run until it reports 0 missing and 0 errors.

Final report (under 250 words): counts by `t` and by `fit`; the 5 most frequent `need` tags with 2 example ids each; any construct you repeatedly couldn't express in v0; and the ids of any passing/overtaking-related sentences that are NOT in a section obviously about passing.
```
