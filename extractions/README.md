# Passing rules extracted on 23 October 2026

The passing rules of the Ontario, California and Texas handbooks, each extracted once with the extraction prompt (`prompts/extract-rules.md`, then called `prompts/extract-rules.fixed-v1.md`), by Claude, in the same way as the check in `provenance/prompt-check/`. michael asked for this on 23 October, after choosing that prompt for every new extraction, with the Qwen runs on hold. Until 26 October this folder was `extractions/fixed-v1/{ontario,california,texas}/`.

- California and Texas: the statements of `output.json` are each handbook's current draft of the passing rules, in `analysis/passing-rules/{ca,tx}/rules.json`. They replaced the earlier drafts (68 and 65 statements, made with an older prompt), which are in the git history as `analysis/passing-rules/{ca,tx}/passing-rules.v1.json`. No person has reviewed either yet.
- Ontario: the reference stays the 88 statements in `analysis/passing-rules/mto/rules.json`. The run here is a check of the prompt on the corrected inputs, the clean repeat of `provenance/prompt-check/`, whose two runs had two faults in their inputs.

`output.json` is kept as the run wrote it, with the field names of the time: `force` and `force_from`, with `LEGAL` and `ADVISORY`. In `rules.json` the same statements have the current names, `strength` and `strength_from` with `LAW` and `ADVICE`, and three Texas statements are written with `EITHER … OR`, which the rule language gained on 26 October: p95b, p110b and p118d said "SHOULD either … or …" in plain words. Nothing else differs.

Model: michael adds the name and version here: `__________`

## How each run was made

1. **Handbook.** Only the local copy on the server: `handbooks/mto/`, `handbooks/ca/` and `handbooks/tx/` (called `mto_drivers_handbook/`, `ca_drivers_handbook/` and `tx_drivers_handbook/` when the runs were made, and moved on 23 October in commit 74ebb7e without changing any file). Ontario's 272 files are in `provenance/SHA256SUMS`; `inputs.sha256` in each folder lists the passage files, the images sent, the prompt and the topic file. The prompt line keeps the file's name and sha256 at the time (`prompts/extract-rules.fixed-v1.md`, `6cc989f4…`): that version is in the git history, and its rendered text is `prompt.md`. Every other line checks against the current files with `sha256sum -c`.
2. **Passages.** Ontario: michael's 96 passages and the 9 census sentences. California (105) and Texas (145): chosen with `prompts/select-passages.md` and built by `tools/make_passages.py` from `analysis/segments/`. On 23 October `tools/segment_handbook.py` rebuilt all three segment files, and `tools/make_passages.py` both passage files, byte for byte.
3. **Prompt.** `provenance/scripts/render_prompt.py` filled the prompt; `messages.json` is the exact system and user message, and `prompt.md` the same text as one readable file. Only `id`, `page`, `sec`, `kind`, `text`, `cap` and `image` are sent; selection fields (`part`, `why`, `seg`, `href`, `pdf_page`) are dropped. All three share the topic `passing` and the scope in `prompts/topics/passing.txt` (then `passing.fixed-v1.txt`). The handbook lines were:
   - Ontario: `Ontario MTO Driver's Handbook (ontario.ca, offline copy checked 2026-10-06)`
   - California: `California Driver's Handbook (California DMV, DL 600 Rev. 6/2025; offline copy of dmv.ca.gov saved 2026-10-20)`
   - Texas: `Texas Driver Handbook (Texas DPS, DL-7 revised January 2026; offline copy converted from the PDF, saved 2026-10-20)`
4. **Run.** For each handbook, a fresh Claude subagent with no other context read `prompt.md` and looked at every figure's image (Ontario 12, California 7, Texas 23), and nothing else. It wrote the statements as JSON Lines in parts, and assembled them into `output.json`. Its brief is in `brief.md`, verbatim. Runs started at 18:26 (Ontario) and 18:30 (California, Texas) UTC and took 17 to 22 minutes.
5. **Check.** `provenance/scripts/score_extraction.py`. Ontario is scored against the reference (`score.md`). California and Texas have no reviewed reference, so their output is compared with the earlier drafts (`compare-drafts.md`): that measures agreement between two extractions, not correctness. The scores were made again on 26 October with the current scorer and reference; only Ontario's clause keywords moved (60 to 59 of 86, from the change to 3.4.4b).

To render a prompt with the current prompt file, from the repo root:

```
python3 provenance/scripts/render_prompt.py --passages analysis/passing-rules/ca/inputs/passing-passages.json \
    --handbook "California Driver's Handbook (California DMV, DL 600 Rev. 6/2025; offline copy of dmv.ca.gov saved 2026-10-20)" \
    --topic passing --scope-file prompts/topics/passing.txt --out /tmp/ca-messages.json
```

The user message is the same as in `ca/messages.json`; the system message is the current prompt, which differs from the one the run received only in the rule language's 26 October changes (strength, `EITHER … OR`). For Ontario give both input files (`passing-passages.json`, then `census-sentences.json`); for Texas use `analysis/passing-rules/tx/inputs/passing-passages.json` and its handbook line.

## Results

| | Ontario | California | Texas |
|---|---|---|---|
| Passages sent | 105 | 105 | 145 |
| Statements | 102 | 83 | 104 |
| RULE, FACT, DEFINE, PROCEDURE, EXCEPTION | 80, 16, 3, 2, 1 | 66, 9, 3, 4, 1 | 82, 15, 3, 2, 2 |
| Law and advice, on rules and procedures | 24 and 58 | 17 and 53 | 37 and 47 |
| Compared with | reference, 88 | earlier draft, 68 | earlier draft, 65 |
| Of those, paired by shared sources | 86 (98%) | 66 (97%) | 63 (97%) |
| Own statements paired | 84% | 80% | 61% |
| Same type, on pairs | 98% | 94% | 100% |
| Law or advice agrees, on paired rules and procedures | 69 of 71 | 57 of 57 | 49 of 50 |
| Same set of modals | 91% | 89% | 94% |
| Same clause keywords | 69% | 71% | 71% |
| Inline flags (J, S, R, G), F1 | 0.80 | 0.71 | 0.70 |
| Schema errors, quotes not verbatim, "you", stray capitals | 0 | 0 | 0 |
| Numbers not in the cited sources | 0 | 0 | 1 (Texas p102a) |

Ontario, compared with the check in `provenance/prompt-check/`: 3.4.1a (parked vehicles), 1a and 3.4.5c now have pairs. The two reference statements without one are 3.4.3b and 3.4.3c (c6 and c7, staying behind a smaller vehicle turning left).

## For the reviewer

- **Texas writes many more statements than its earlier draft (104 against 65).** Of the 41 without a pair, 33 are on passages the draft also cites, which the run splits more finely or reads differently. The other 8 come from six passages the draft does not cite (p43, p44, p57, p58, p97, p117): double white lines, a solid white or yellow edge line, leaving room to pass when parking on a rural highway, and a truck backing into a loading area. Larger groups of extra statements: driving on the left side of the road (p64 to p70, the Texas form of no-passing zones), a cyclist's lane position (p119 to p123), and truck blind spots (p110, p116 to p118). Whether these belong to the passing topic is a scope question for the reviewer.
- **California p63a** (pull over and stop for an emergency vehicle): the passage gives the duty as an imperative and adds "Failure to pull over may result in a ticket". The run wrote advice (SHOULD) with an `IF VIOLATED` clause and an M flag. The prompt does not say whether a penalty in the same passage makes an imperative a legal duty; Ontario's 3.4.5b ("the required two metres") is the same question.
- **Texas p102a** uses "20 mph below the speed limit" from p101 but cites only p100 and p102.
- **Ontario 3.6.1a** (move right to let faster traffic pass) and **3.4.5b** are law (MUST) in this run and advice in the reference.

## Files in each folder

| File | What it is |
|---|---|
| `messages.json` | The rendered system and user messages, with the prompt's sha256 and the passage count |
| `prompt.md` | The same text as one readable file, as the run received it |
| `brief.md` | The brief the run received, verbatim, with its start time |
| `inputs.sha256` | sha256 of the passage files, every image sent, the prompt and the topic file |
| `output.json` | The statements as the run wrote them, `{"statements": [...]}`, with the field names of the time (`force`, `force_from`); renamed to `strength` and `strength_from`, they are valid against `analysis/passing-rules/statements.schema.json` |
| `score.md`, `score.json` | Ontario: the score against the reference, every disagreeing pair and the unpaired statements |
| `compare-drafts.md`, `compare-drafts.json` | California and Texas: the same comparison against the earlier draft |
