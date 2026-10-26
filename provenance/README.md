# Provenance of the reference ruleset

The reference ruleset is the 88 passing statements in `analysis/passing-rules/mto/rules.json`. On 23 October 2026 the team decided to use it as the ground truth for scoring other extractions (open models, other prompts, other modalities). This folder records how it was made, from which inputs and with which prompts, so a reader can check it and so later runs can be compared with it fairly.

**Read this first.** The 88 statements were not produced by one prompt. Claude wrote them on 10 and 11 October 2026 in one long working session in the project's passing-rules thread, guided by michael's messages, the rule language as it was being designed, the census of the whole handbook, and one decision michael made on a card. Claude wrote the statements directly as structured data, then revised them in three rounds. The instructions that session followed are recorded here verbatim; the session's own reasoning is not. `prompts/extract-rules.md` distils that process into one self-contained prompt; section "Checking the fixed prompt" below says how closely it reproduces the reference. On 23 October michael chose it as the prompt for every new extraction.

On 26 October every file was brought to one current version, with the earlier ones left to the git history: the reference moved from `analysis/passing-rules/passing-rules.v1.json` to `analysis/passing-rules/mto/rules.json` and its inputs into `analysis/passing-rules/mto/inputs/`, the prompt from `prompts/extract-rules.fixed-v1.md` to `prompts/extract-rules.md`, and the fields `force` and `force_from` (`LEGAL`, `ADVISORY`) became `strength` and `strength_from` (`LAW`, `ADVICE`). The timeline below keeps the names used at the time.

Extractor: Claude, in a Claude Code session on claude.ai (model: _fill in_). Model names are kept out of files written for this repo by that session; add the model and version here.

## The reference

| | |
|---|---|
| File | `analysis/passing-rules/mto/rules.json` |
| sha256 | `eb49447d5121f086f445a634b1c15258da90a16ca4a0c09724b7e40856eb7cc2` |
| Last changed | 26 October 2026: fields renamed to `strength` and `strength_from`, and 3.4.4b's "where practical" written as a `WHEN` clause so that it fits the grammar (`analysis/rule-language.md` §1). Before that, 11 October 2026, 03:03 UTC (sha256 `30e79a16…`) |
| Statements | 88: 71 RULE, 9 FACT, 4 DEFINE, 2 PROCEDURE, 2 EXCEPTION |
| Strength | 73 rules and procedures: 19 law (8 MUST, 7 MUST NOT, 4 MAY), 54 advice |
| Flags | 72 flags on 53 statements (40 J); 49 vague spans marked inline as `[?…]` |
| Ids | Section numbers from michael's outline plus a letter (`3.4.4b`); the outline is `analysis/passing-rules/mto/inputs/passing-structure.json` |
| Review | Not yet reviewed line by line by a person |

Fields beyond the output schema (`section`, `where`, `image`, `census_id`, `zh`) are for the review page. With `section` and `zh` dropped and sources and flags cut to the schema's keys, all 88 statements pass `analysis/passing-rules/statements.schema.json`.

## How it was made

All times are UTC. Each step lists who did it and what it read and wrote.

| When | Step | Who | Read | Wrote |
|---|---|---|---|---|
| before 10 Oct | Handbook acquisition | Henry, `scrape_mto_handbook.py` | ontario.ca handbook | `mto_drivers_handbook/` (29 pages, index, 241 images), checked word for word against ontario.ca on 6 Oct; the PDF saved from ontario.ca |
| before 10 Oct | Passing passages | michael | the handbook pages | Passing Topic Comparison page: 96 passages m1 to m96 (85 text, 11 figures), grouped into an outline with notes |
| 10 Oct 21:42 to 21:47 | Request and template table | michael | | thread request; template table (`provenance/inputs/template-table-2026-10-10.png`) |
| 10 Oct 21:46 | Content structure | Claude | the Changing positions page and sibling pages | `analysis/passing-content-structure.md` |
| 10 Oct 21:58 to 22:04 | Prior work and v0 plan | Claude, with one research subagent | the 4 papers in `Paper/`, the web | `analysis/rule-template-plan.md`; prompt in `provenance/prompts/prior-work-search.md` |
| 10 Oct 21:59 | Keyword scan of the whole book | Claude, `provenance/scripts/scan_keywords.py` | `mto_drivers_handbook/*.html` | counts of modal, condition and vague words (not saved as a file) |
| 10 Oct 22:09 | Decisions on the plan | michael | | cautions as `SHOULD WATCH FOR`, imperatives default to SHOULD, UNLESS within a sentence and EXCEPTION TO across passages, start from passing, scan the full book first |
| 10 Oct 22:13 | Sentence split | Claude, `provenance/scripts/segment_sentences.py` | `mto_drivers_handbook/` | 3,956 units with page, chapter and heading path (3,444 labelled, 460 headings, 52 on the sample-test page) |
| 10 Oct 22:14 to 22:53 | Census | 8 Claude subagents, `provenance/scripts/make_census_shards.py`, `provenance/scripts/validate_labels.py` | `analysis/census/census-guidelines.md` and one shard each | `analysis/census/census-labels.jsonl`; prompt in `provenance/prompts/census-labelling.md` |
| 10 Oct 22:15 to 22:20 | Passage data | Claude | michael's page | `analysis/passing-rules/inputs/passing-passages.json`, `passing-structure.json`, `passing-page-notes.json` |
| 10 Oct 22:41 | Draft 1: 80 statements | Claude | passages, outline, notes, v0 plan, census labels so far | `provenance/drafts/draft-1.json` |
| 10 Oct 22:55 to 23:10 | Rule language v1 | Claude | census summary | `analysis/rule-language-v1.md` (first version), `analysis/census/census-report.md` |
| 10 Oct 22:58 to 23:07 | Draft 2: 81 statements, first review page | Claude | draft 1 | `provenance/drafts/draft-2.json`; 2.2b split out of the passing procedure; 13 statements reworded to fit v1 (UNTIL, WHEN for events, BECAUSE, `[?…]` marks) |
| 10 Oct 23:00 to 23:11 | Census additions | michael chose on a card; Claude wrote | 8 census sentences on other pages (c1 to c9 with the sign image) | 7 new statements: 3.4.3b, 3.4.3c, 3.4.12b to 3.4.12e, 3.6.1d (`provenance/drafts/draft-3.json`) |
| 11 Oct 01:48 to 02:17 | Draft 4: wording conformance | Claude, after michael asked for a template introduction | v1 wording rules | 6 statements reworded: overtake to pass (1a, 3.4.4d), right lane to right-hand lane (3.2.1d), night procedure step 4 uses the original lane and the inside mirror (3.3.1b), THAT only as a DEFINE keyword (3.4.6c, 3.5.2b); grammar added to the spec (`provenance/drafts/draft-4.json`) |
| 11 Oct 03:03 | Final JSON | Claude | draft 4 | `passing-rules.v1.json`: the statements of draft 4 with full quotes, locations, figures and Chinese flag notes; no statement changed after 02:17 |
| 11 Oct 05:28 to 05:49 | VLA analysis | Claude | the 88 statements | `analysis/vla/`; no statement changed |
| 20 Oct | Output schema | Claude | the 88 statements | `analysis/passing-rules/statements.schema.json` |

michael's later page requests (chips, tabs, colours, navigation, figures under rules, click to jump) changed the review page only.

## Inputs

All paths are relative to the repo root; sha256 values are in `provenance/SHA256SUMS`. On 23 October the handbook moved from `mto_drivers_handbook/` to `handbooks/mto/` (commit 74ebb7e, renames only, no content changed), and on 26 October the passage files moved into `analysis/passing-rules/mto/inputs/` (no content changed); the timeline above keeps the names used at the time.

| Input | What it is | Where it came from |
|---|---|---|
| `handbooks/mto/` | The handbook as local HTML and images | `scrapers/scrape_mto_handbook.py`; identical to the copy used on 10 October |
| `handbooks/mto/source/MTO-drivers-handbook-ontario.ca.pdf` | The handbook as PDF | saved from ontario.ca; not used for the reference |
| `analysis/passing-rules/mto/inputs/passing-passages.json` | michael's 96 passages: `m`, `page`, `sec`, `text`, `kind`; figures add `src` and `cap`; `part`, `cls`, `w` and `grp` keep his grouping (`part: excluded` marks m92 to m96) | his Passing Topic Comparison page; on 23 October three image paths were corrected (below) |
| `analysis/passing-rules/mto/inputs/passing-structure.json` | His outline: 86 groups in sections 1, 2.1, 2.2, 3.1.1 to 3.6.3 and "Not included", each with its passage ids. The reference ids come from it | the same page |
| `analysis/passing-rules/mto/inputs/passing-page-notes.json` | The page's note and content-type tag for 85 passages (rule, procedure, caution, context, consequence, others, test, definition) | the same page |
| `analysis/passing-rules/mto/inputs/census-sentences.json` | c1 to c9: 8 census sentences and 1 sign image from other pages, added after michael's choice | `analysis/census/census-labels.jsonl` and the Signs page |
| `analysis/census/census-labels.jsonl` | 3,444 labelled sentences | the census |
| `analysis/rule-language-v1.md` (in the git history; the current language is `analysis/rule-language.md`) | The rule language as it stood on 11 October 02:17 | this session |
| `provenance/inputs/template-table-2026-10-10.png` | michael's table of rule templates | project chat, 10 October 21:47 |
| `provenance/requests.md` | michael's messages and the decision, verbatim | the passing-rules thread |

## Prompts

| Prompt | Used for | File |
|---|---|---|
| michael's messages and one decision card | The extraction itself (interactive) | `provenance/requests.md` |
| Census labelling, one template for 8 labellers | Labelling 3,444 sentences against the first draft of the language | `provenance/prompts/census-labelling.md`, with `analysis/census/census-guidelines.md` |
| Prior-work search | The plan's survey of earlier designs | `provenance/prompts/prior-work-search.md` |
| Extraction prompt | Written 23 October from the reference's conventions; chosen the same day as the prompt for every new extraction; brought to the current rule language on 26 October | `prompts/extract-rules.md`, with `prompts/topics/passing.txt` |

## Reproducing the inputs

From a clean clone, with `beautifulsoup4` installed:

```sh
python3 provenance/scripts/segment_sentences.py handbooks/mto /tmp/units   # units.jsonl, figures.jsonl, chapters.json
python3 provenance/scripts/make_census_shards.py /tmp/units/units.jsonl /tmp/units/chapters.json /tmp/units
cd /tmp/units && sha256sum -c <path-to-repo>/provenance/SHA256SUMS --ignore-missing
```

On 23 October 2026 both scripts reproduced the 10 October files byte for byte: `units.jsonl` (3,956 units), `figures.jsonl` (245 figures), `chapters.json`, and all 8 `shardN.txt` and `shardN.ids` files the labellers read.

## Checking the fixed prompt

To see whether one fixed prompt can stand in for the interactive process, the extraction prompt (then `prompts/extract-rules.fixed-v1.md`) was run twice on the 105 passing passages (m1 to m96 and c1 to c9, with the figure images), each run in a fresh Claude subagent that saw only the rendered prompt and the images, and the Signs page was run once more with corrected images. `provenance/scripts/score_extraction.py` compared each output with the reference. The rendered prompts, outputs, scores and a full account are in `provenance/prompt-check/`.

Both runs paired 85 and 86 of the 88 reference statements (97% and 98%), and 82% and 81% of their own statements paired with a reference statement. On paired statements the type agreed 98 to 99% of the time, law or advice on 70 and 68 of 72 rules and procedures, the set of modals on 91% and 87%, and clause keywords on 75% and 70% (76% and 71% before the 26 October change to 3.4.4b); inline flags reached an F1 of 0.79 and 0.77. Neither run had a schema error, a quote that was not the full passage text, "you", a stray capital or a number missing from its sources. Two input faults are counted in these numbers: three wrong sign images, and a topic scope that left out parked vehicles (both now fixed). With the right images, all 6 reference statements on the Signs page matched in type, strength, modals and clauses. The prompt alone therefore reproduces nearly every reference statement and its law or advice; the differences lie mostly in clause wording and in how finely passages are split.

A clean repeat with the corrected images and scope, run on 23 October together with the California and Texas extractions, paired 86 of the 88 reference statements and 84% of its own 102, with law or advice agreeing on 69 of 71 paired rules and procedures and no format errors. Only 3.4.3b and 3.4.3c (c6 and c7) had no pair. It is in `extractions/mto/`.

## Known issues for the reviewer

- `[?clear]` is flagged in 3.4.3c, but "the way is clear" is not flagged in 2.2a, 3.1.6a or 3.3.1b. The fixed prompt treats "the way is clear" as a precise phrase and does not flag it.
- 3.2.3c and 3.2.3d say "the leftmost lane"; the vocabulary's word is "the far-left lane".
- 3.6.1a cites two sample-test passages (m87, m88). Leave them out if that page is used for evaluation.
- Three sign images on michael's page belong to the sign before: in the handbook HTML each caption comes before its image. The reference cites the right images, and on 23 October `passing-passages.json` was corrected to match: m25 `images/3-1-21.jpg` to `3-1-22.jpg` ("do not pass"), m30 `3-1-32.jpg` to `3-1-33.jpg` ("keep right except to pass"), m74 `3-1-82.jpg` to `3-1-83.jpg` (pilot vehicle "do not pass"). `pages/passing-topic-comparison.html` is michael's page as it was and still shows the old images.
- `TAGS` is in the spec but empty in the JSON.
- The reference ids follow michael's outline, which other handbooks will not have. The extraction prompt uses passage-based ids (`m17a`), so compare runs with the reference by their sources, as `provenance/scripts/score_extraction.py` does.
- 3.4.5b (stay 2 m behind a streetcar's rear doors) is advice in the reference, but its source m61, the Diagram 2-49 caption, says "the required two metres". Both check runs, and the Qwen runs with every prompt version, make it law. It should probably be MUST.
- 3.4.5c is a separate EXCEPTION for the second sentence of m63; the language says only that an exception in the same sentence is an `UNLESS` and one in another passage is a separate statement. Decide which form a next-sentence exception takes.
- 1a defines "changing position" from m1, a section introduction. Neither check run wrote it; decide whether such definitions belong in the reference.
