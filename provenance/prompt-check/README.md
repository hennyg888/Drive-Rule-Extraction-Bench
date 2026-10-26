# Check of the extraction prompt on the passing passages, 23 October 2026

Two blind runs of the extraction prompt (`prompts/extract-rules.md`, then called `prompts/extract-rules.fixed-v1.md`) on the 105 passing passages (m1 to m96 and c1 to c9), and one re-run of the Signs page, scored against the reference `analysis/passing-rules/mto/rules.json` with `provenance/scripts/score_extraction.py`. The folder was called `provenance/fixed-v1-check/` until 26 October.

## Setup

- `messages.json` is the rendered prompt (system and user messages), made with `provenance/scripts/render_prompt.py`; `prompt-passing.md` is the same text as one readable file. At the time of the runs the prompt file was called `prompts/extract-rules.v1.md` (sha256 `c6c469dae40f…`). It was renamed to `prompts/extract-rules.fixed-v1.md` on the same day so that it does not clash with `prompts/archive/extract-rules.v1.md`, and its header (which is not sent) now names the new paths. Rendering the renamed file with the same inputs gave byte-identical messages. On 26 October the prompt took the current rule language (the field `force` became `strength`, with `LAW` and `ADVICE`; `EITHER … OR` was added), so the text these runs saw is the one in `prompt-passing.md`, and the file itself is in the git history. The outputs keep the field names they were written with; the scorer reads `force` as `strength`.
- Each run was a fresh Claude subagent that saw only `prompt-passing.md` and the 12 figure images, wrote its statements as JSON Lines and assembled them into `output.json`. It had no access to the reference, the review page, the census or any other file. Both ran at the same time, from 17:41 to about 17:59 UTC.
- The model was the one that made the reference. These runs test whether the prompt alone carries the reference's conventions; a run of another model on the same `messages.json` is the comparison that matters for the trials.

## Two faults in the runs' inputs

Both were found after the runs had started and are fixed in the repo; the files here are kept as the runs saw them.

1. **Three wrong sign images.** The passages came from `passing-passages.json` before its 23 October correction, so m25, m30 and m74 showed the image of the sign before each (`images/3-1-21.jpg`, `3-1-32.jpg`, `3-1-82.jpg` instead of `3-1-22.jpg`, `3-1-33.jpg`, `3-1-83.jpg`). The Signs-page re-run uses the right images.
2. **The topic scope left out parked vehicles.** The scope said a vehicle "travelling, or stopped in traffic", so both runs treated m50 ("When passing parked vehicles, watch carefully for people suddenly opening doors…") as outside the topic, and the reference statement 3.4.1a has no pair in either run. `prompts/topics/passing.txt` now says "travelling, stopped in traffic or parked".

## Results

| | Run 1 | Run 2 |
|---|---|---|
| Statements written | 104 | 106 |
| Reference statements paired | 85 of 88 (97%) | 86 of 88 (98%) |
| Run statements paired | 85 of 104 (82%) | 86 of 106 (81%) |
| Same type, on paired statements | 99% | 98% |
| Law or advice (strength), on paired rules and procedures | 70 of 72 | 68 of 72 |
| Same set of modals | 91% | 87% |
| Same clause keywords | 75% | 70% |
| Same sources | 84% | 86% |
| Same links | 98% | 97% |
| Inline flags (J, S, R, G), F1 | 0.79 | 0.77 |
| Schema errors, quotes not verbatim, "you", stray capitals, numbers not in the sources | 0 | 0 |

The Signs-page re-run (11 passages, right images) paired all 6 reference statements on that page, with the same type, strength, modals and clause keywords in each.

The scores were made again on 26 October against the current reference. The only change that moves a number is 3.4.4b, whose "where practical" is now a `WHEN` clause (`analysis/rule-language.md` §1): both runs kept it as a bare `[?where practical]`, so each loses one statement on clause keywords (76% and 71% before).

What the differences are:

- **No pair in either run:** 3.4.1a (m50, the scope fault) and 1a, the definition of changing position from m1. Both runs used m1 only as the source of "the move" in 2.1a's condition.
- **The streetcar-stop exception:** both runs wrote the second sentence of m63 ("This rule does not apply at stops where…") as an `UNLESS` inside 3.4.5b's statement; the reference has it as a separate statement, 3.4.5c. The prompt says what to do with an exception in the same sentence (`UNLESS`) and in a different passage (a separate statement), but not with one in the next sentence of the same passage. Run 1 leaves 3.4.5c unpaired; run 2 pairs it with a different statement (m64a).
- **Extra statements (19 and 20):** mostly FACTs and finer splits that the reference leaves out or merges, such as m3 ("a driver following slow-moving vehicles may want to pass them"), m28 ("some roads have special passing or climbing lanes"), m36 ("passing on the right can be more dangerous") and a definition of the truck passing lane from m90. The prompt's rules allow them; a reviewer should decide whether the reference should have them.
- **Sign rules:** run 2 gave advice instead of law for 3.1.7a and 3.2.1d, and both runs wrote `[?this sign]` in 3.4.10a. These are the three passages whose images were wrong. With the right images all three match the reference.
- **3.4.5b (stay 2 m behind a streetcar's rear doors):** both runs say MUST, because the Diagram 2-49 caption says "the required two metres" and the prompt's first modal line counts "required" as legal wording. The reference says SHOULD. The runs follow the prompt here; the reference should be reviewed.
- **Clause keywords** are the weakest measure. Typical differences: `WHEN` against `WHILE` for "while passing", a `BECAUSE` left out, and "make sure you have enough time" written as `ONLY IF` in the reference but as `WHEN` plus an action in the runs. The grammar allows most of these both ways.
- **Modals:** the grammar lets a modal repeat after `AND` or not (`SHOULD signal AND [SHOULD] pull over`), so the scorer compares the set of modals. Compared as sequences, the runs matched 85% and 81%.

The prompt was not changed after the check until 26 October, when it took the current rule language. Two input files were changed after the check: the sign images in `passing-passages.json` and the passing scope.

## Files

| File | What it is |
|---|---|
| `messages.json`, `prompt-passing.md` | The rendered prompt both runs received |
| `run1/output.json`, `run2/output.json` | The statements each run wrote |
| `run1/score.md`, `run2/score.md` | Scores, every disagreeing pair, and the unpaired statements on both sides |
| `run1/score.json`, `run2/score.json` | The same as data |
| `signs/` | The Signs-page re-run with the right images: `messages.json`, `prompt-signs.md`, `output.json`, `reference-signs.json` (the 6 reference statements whose sources are all on that page), `score.md`, `score.json` |

To score again from the repo root: `python3 provenance/scripts/score_extraction.py --output provenance/prompt-check/run1/output.json --report /tmp/run1-score.md --json /tmp/run1-score.json`.
