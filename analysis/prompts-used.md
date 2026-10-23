# Prompts and inputs behind the Ontario passing rules

Written on 23 October 2026 by the Claude Code session that made the 88 Ontario passing statements (the passing-rules thread of the Wise Lab project on claude.ai), so that every session working in this repo knows exactly what was used. All times are UTC.

## Summary

| | Output | When | Who | Instructions |
|---|---|---|---|---|
| (a) | michael's 96 passing passages, m1 to m96 (`analysis/passing-rules/inputs/passing-passages.json`) | His page existed before 10 Oct; copied into JSON on 10 Oct, 22:15 to 22:20 | michael, outside this session | None from this session: see (a) |
| (b) | Census labels for 3,444 handbook sentences (`analysis/census/census-labels.jsonl`) | 10 Oct, 22:14 to 22:53 | 8 Claude subagents started by this session | The labelling prompt in (b), plus `analysis/census/census-guidelines.md` |
| (c) | The 88 passing statements (`analysis/passing-rules/passing-rules.v1.json`) | 10 Oct 22:15 to 11 Oct 03:03 | This session, working interactively with michael | No single prompt: michael's messages (Appendix A) and one decision he made. See (c) |
| (d) | Rule language v1 (`analysis/rule-language-v1.md`) | First version 10 Oct, 22:55 to 23:10; grammar and wording rules added 11 Oct, 01:48 to 02:17 | This session | michael's messages and his template table, a prior-work search (Appendix B) and the census findings. See (d) |

**Model.** Every step Claude did above, in the main session and in all its subagents, ran on the same Claude model; the subagents' transcripts record it and the session is configured for it. This session keeps model names out of files it writes to the repo, so michael adds the name and version here: `__________`.

## Which handbook text

All four used the local HTML in this repo's `mto_drivers_handbook/`. Neither the live ontario.ca site nor the PDF was used.

- The session read a copy of `mto_drivers_handbook/` placed in the project's shared files on 10 Oct at 21:40 (index, 29 pages, 241 images, `style.css`). On 23 October all 272 files of that copy were byte-identical to this repo's `mto_drivers_handbook/` (sha256 of every file compared).
- The census sentences were split from those HTML files by `provenance/scripts/segment_sentences.py` (called `segment_handbook.py` on 10 October; not the same script as `tools/segment_handbook.py`), which reads nothing else. Re-running it on 23 Oct reproduced the 10 Oct `units.jsonl` (3,956 units), `figures.jsonl` (245) and `chapters.json` byte for byte.
- All 105 passage texts (m1 to m96 and c1 to c9) occur word for word in the local HTML, once curly quotes and whitespace are normalised (checked 23 Oct).
- Figure paths (`src`) point into `mto_drivers_handbook/images/`.
- michael's first message linked the ontario.ca Changing positions page; the session worked from the local copy of that page. The PDF was never opened.
- On 23 October, after these records were written, the handbook folders moved into `handbooks/` (commit 74ebb7e, renames only): `mto_drivers_handbook/` is now `handbooks/mto/`, and the PDF is `handbooks/mto/source/MTO-drivers-handbook-ontario.ca.pdf`. The paths above keep the names used at the time.

## (a) michael's 96 passing passages

This session did not choose, write or edit these passages. michael's first message (10 Oct 21:42, Appendix A) pointed to his Passing Topic Comparison page (https://claude.ai/artifact/A8gZroLVV8miAsmAym44C6), which already held the 96 passages with his grouping into sections and his notes. The session read the page at 21:47 and copied its data unchanged into JSON between 22:15 and 22:20:

- `passing-passages.json`: 96 passages (85 text, 11 figures) with `m`, `page`, `sec`, `text` and `kind`; figures add `src` and `cap`; `part`, `cls`, `w` and `grp` keep his grouping (`part: excluded` marks m92 to m96).
- `passing-structure.json`: his outline, 86 groups, each with its passage ids. The reference statement ids come from it.
- `passing-page-notes.json`: his note and content-type tag for 85 passages.

How the page itself was made is not in this session's records; michael knows. The only change since 10 Oct is the three image paths corrected on 23 Oct (see "Changes after the 20 October snapshot").

## (b) Census labels

1. `segment_sentences.py` split the handbook HTML into 3,956 units (22:13). 3,444 were labelled: all except 460 headings and the 52 units of the sample knowledge-test page.
2. `make_census_shards.py` cut them into 8 shards in table-of-contents order, each with page and heading lines for context. It reproduces all 8 shard files byte for byte.
3. Eight subagents ran in parallel, each with the prompt below (identical except for the shard number `{N}`), and each checked its own output with the validator until it reported 0 missing and 0 errors.
4. The eight outputs were merged into `analysis/census/census-labels.jsonl`; `census-summary.json` and `census-report.md` were written from it (22:55 to 23:10).

The labelling instrument is `analysis/census/census-guidelines.md`, last changed at 22:13, before any labeller started. It labels against the v0 grammar in `analysis/rule-template-plan.md`, not v1.

| Shard | Sentences | Started | Finished |
|---|---|---|---|
| 1 | 438 | 22:14:10 | 22:40:47 |
| 2 | 432 | 22:14:17 | 22:52:52 |
| 3 | 437 | 22:14:25 | 22:48:50 |
| 4 | 431 | 22:14:32 | 22:46:34 |
| 5 | 437 | 22:14:39 | 22:43:49 |
| 6 | 432 | 22:14:46 | 22:49:29 |
| 7 | 447 | 22:14:54 | 22:48:34 |
| 8 | 390 | 22:15:02 | 22:47:54 |

The prompt, verbatim. Paths are the session's scratch folder at the time: `shard{N}.txt` and `.ids` are what `make_census_shards.py` writes, `validate.py` is `provenance/scripts/validate_labels.py`, and `out{N}.jsonl` was merged into `census-labels.jsonl`.

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

## (c) The 88 passing statements

There was no extraction prompt. The session wrote the statements itself, directly as structured data, following michael's messages (Appendix A) and the rule language as it was being designed, then revised them three times. Its own reasoning was not saved; its instructions and every draft were.

What it worked from:

- The passages, outline and notes in (a), and michael's template table (posted in the project chat at 21:47).
- The plan v0 (`analysis/rule-template-plan.md`), then rule language v1 once it existed.
- The census labels, which found 8 passing sentences on other pages (c1 to c9 in `analysis/passing-rules/inputs/census-sentences.json`, with one sign image).

| When | Version | Statements | What changed |
|---|---|---|---|
| 10 Oct 22:41 | Draft 1 | 80 | First full set, written against the v0 plan |
| 10 Oct 23:07 | Draft 2 | 81 | 2.2b split out of the passing procedure; 13 statements reworded to fit v1 (UNTIL, WHEN for events, BECAUSE, `[?…]` marks) |
| 10 Oct 23:04 to 23:11 | Draft 3 | 88 | michael chose "加入" on a decision card (Appendix A), so the census sentences became 7 statements: 3.4.3b, 3.4.3c, 3.4.12b to 3.4.12e, 3.6.1d |
| 11 Oct 02:17 | Draft 4 | 88 | 6 statements reworded to the v1 wording rules: overtake to pass (1a, 3.4.4d), right lane to right-hand lane (3.2.1d), night procedure step 4 (3.3.1b), THAT only as a DEFINE keyword (3.4.6c, 3.5.2b) |
| 11 Oct 03:03 | Final JSON | 88 | Draft 4 plus full quotes, locations, figures and Chinese flag notes. No statement has changed since |

The final file's sha256 is `30e79a16653945e2487733bc1399faba80baed5708993bc5d237b02534197042`: 71 RULE, 9 FACT, 4 DEFINE, 2 PROCEDURE, 2 EXCEPTION. Statement ids are michael's outline section plus a letter (`3.4.4b`), and each quote is the full passage text. The set has not yet been reviewed line by line by a person.

On 23 October the team made these 88 statements the reference ruleset. This session has since written a fixed extraction prompt that puts its format, force rules, vocabulary and worked examples into one self-contained prompt, and checked it against the 88: two blind runs on the 105 passing passages paired 85 and 86 of them. It is `prompts/extract-rules.fixed-v1.md`, with the passing topic in `prompts/topics/passing.fixed-v1.txt`, and the check is in `provenance/fixed-v1-check/`. It is not the same file as this repo's `prompts/extract-rules.md` (v2.1) or `prompts/archive/extract-rules.v1.md`. On 23 October michael chose fixed-v1 as the prompt for new handbooks. The same day it was used to extract the passing rules of California and Texas, and of Ontario again as a check; each run, with its exact prompt, brief and input hashes, is in `extractions/fixed-v1/`. The Qwen runs are on hold.

## (d) Rule language v1

The instructions were michael's messages in Appendix A: write rules in a natural-language-like style, not LTL (21:42); start from his template table (21:47); use a minimal set of fixed wordings, as SQL does, chosen after scanning the whole book, and highlight vague content (21:57); look at prior work (21:58); his four decisions on the plan (22:09); and add an overall introduction to the templates and wording (11 Oct 01:46).

| When | Step | Output |
|---|---|---|
| 10 Oct 21:58 to 22:02 | One subagent searched for prior designs with the prompt in Appendix B | Report used in §5 of the plan |
| 10 Oct 21:59 | Keyword scan of all pages (`provenance/scripts/scan_keywords.py`): counts of modal, condition and vague words | Not saved as a file |
| 10 Oct 22:04 | Plan v0 | `analysis/rule-template-plan.md` |
| 10 Oct 22:09 | michael's decisions: cautions as SHOULD WATCH FOR; bare imperatives default to SHOULD; UNLESS within a sentence, EXCEPTION TO across passages; start from passing but scan the whole book first | |
| 10 Oct 22:14 to 22:53 | Census of every sentence against v0 (b) | Where v0 did not fit, and how often |
| 10 Oct 22:55 to 23:10 | Rule language v1, first version, from the census findings | `analysis/rule-language-v1.md`, `analysis/census/census-report.md` |
| 11 Oct 01:48 to 02:17 | Grammar, wording rules and the template introduction added | `analysis/rule-language-v1.md`, unchanged since 02:17 |

## Changes after the 20 October "Qwen Trial Files" snapshot

Unchanged: `passing-rules.v1.json` (same sha256 as above), `rule-language-v1.md`, `census-sentences.json`, everything in `analysis/census/` and `analysis/vla/`, `pages/` and `qwen-trial-handoff.md`.

Changed (both in this repo since 23 October):

- `analysis/passing-rules/inputs/passing-passages.json`: three image paths corrected: m25 `images/3-1-21.jpg` to `3-1-22.jpg` ("do not pass" sign), m30 `3-1-32.jpg` to `3-1-33.jpg` ("keep right except to pass"), m74 `3-1-82.jpg` to `3-1-83.jpg` (pilot vehicle "do not pass when flashing"). On michael's page each of these figures took the image of the sign before it, because in the handbook HTML each caption comes before its image. The 88 statements already cited the right images. **Any run that sent the 20 October images to a model showed the wrong sign for these three passages.** The Qwen T2 runs sent no images and are not affected.
- `analysis/passing-rules/statements.schema.json`: an optional `see` list (`{figure, source}`) for statements that point to a figure, and a new title that names no prompt file. Output that was valid before is still valid.

New, added without overwriting anything already here:

- `prompts/extract-rules.fixed-v1.md` and `prompts/topics/passing.fixed-v1.txt`: the fixed-v1 prompt and its passing topic, see (c)
- `provenance/`: how the reference was made, michael's messages verbatim, the census and prior-work prompts, drafts 1 to 4, the template table, the fixed-v1 check, sha256 sums of the inputs, and in `provenance/scripts/` the scripts this session used: `segment_sentences.py`, `make_census_shards.py`, `validate_labels.py`, `scan_keywords.py`, `render_prompt.py`, `score_extraction.py`
- `pipeline/`: the pipeline write-up and its figure
- `extractions/fixed-v1/`: the passing rules of Ontario, California and Texas extracted with fixed-v1 on 23 October, each run with its rendered prompt, brief, input hashes, output and comparison
- `analysis/passing-rules/inputs/passing-structure.json` and `passing-page-notes.json` from (a)

## Appendix A: michael's messages, verbatim

These are the messages from the passing-rules thread that shaped (c) and (d). His later messages (10 Oct 23:24, 11 Oct 02:27 to 04:37) asked for changes to the review page and changed no statement.

### 10 Oct 21:42

```text
This is a lab project that the objective is to extract ("transform") driving rules from MTO Driver's handbook into a set of "formal rules".

- Formal rules mean there are some predefined syntax and template for representing the rule instructions. Such as SQL for database language and LTL for some symbolic language.
- However, in this project, I just want to get rid of the LTL-style formalized rules, since I think it isn't a good representation for LLM/VLM to reason over compared to "natural-language"-like styles.

We can start from the overtaking (passing) section inside the handbook. https://www.ontario.ca/document/official-mto-drivers-handbook/changing-positions

My current idea is to first understand and analysis the content structure of the handbook. I hypothsize that it was written in some principles.
For example,
- https://www.ontario.ca/document/official-mto-drivers-handbook/changing-positions 像這一頁就有很明確的 instruction (rules) 。
- 我想先試圖理解他這個 driving handbook 的 "content structure"，他們應該有個 "predefined" 的編寫架構與組織
- 以這個 passing 來說，他們會先講說明一些 "formal definition"，再來介紹一下 "passing" 的 general concept 是什麼、正常過程應該怎麼做 (steps for passing a vehicle)。有什麼限制與注意事項："Passing within 30 metres of a pedestrian crossover is not permitted. Passing left of a centreline is not permitted 30 metres from a bridge, viaduct or tunnel. Don't attempt to pass when approaching the crest of a hill or on a curve where your vision of oncoming traffic is obstructed and there is not enough clear distance ahead to pass in safety.
  When passing parked vehicles, watch carefully for people suddenly opening doors or for doors opened to load and unload.
  Motorcycles, bicycles, limited-speed motorcycles and mopeds often need to pull to the left or right side of their lane to avoid dangerous road conditions or to be seen by other drivers. Do not take this as an invitation to pass in the same lane. If you do want to pass these vehicles, do so by changing lanes.
  When faster traffic wants to pass you, move to the right and let it pass in safety. When being passed on an undivided road where the passing driver has pulled into the opposite lane, pay attention to oncoming traffic and move closer to the right side of the lane. Be prepared to slow down to let the passing driver get in front of you more quickly to prevent a collision.
  On many high-speed roads with three or more lanes in each direction, trucks are not allowed to drive in the far left-hand lane. This means that the lane next to it is the truck passing lane. If you are in this lane and a truck wants to pass, move into the right-hand lane as soon as you can."
- 有了以上的 “general concept” 之後，才接著列舉說 passing 的其他 special condition? 會有哪些情況，以及各個情況各自的 condition 是什麼、注意事項、操作流程是什麼、能 or 不能怎麼做
先來跟我一起整理一下這個 content structure 出來？我們一步一步把它 structure 化

---
已經有整理出目前的版本了：https://claude.ai/artifact/A8gZroLVV8miAsmAym44C6，你可以看一下

我跟我組員也討論了一下，他覺得應該可以把我們現在做的這個 preprocessing 的事情當作 human verification 的內容。這些 preprocessing 應該可以直接包在 VLM extraction，變成是把整個 handbook 直接丟給 VLM，讓他自己做這些 cross-reference linking、information gathering 之類的事情，然後直接得到 formalized rules
```

### 10 Oct 21:57

```text
* 那我們現在要做的事情就是先規劃一些 formal rule templates (similar to SQL style, with specific/predefined patterns and wordings.)。我希望是 natural-language-like style，不是 LTL 那種 symbolic style，因為 LLM is better at reason over natural-language-like context
* 但我們要決定的 rule templates 可能需要掃完整本 handbook 才知道我們要設計哪些 patterns/wordings? 我希望用一個最小的 set 去做到，就像 SQL 也是用一些小集合的 wording 去設計他們的 syntax。
* content in the handbook 可能會有一些模糊的地方，可以先 highlight 起來我們之後再來想怎麼處理

你可以先幫我規劃或是完善一下這個計畫，我們先討論看看有什麼好的做法與 rule template
```

### 10 Oct 21:58

```text
以及過去的文章有沒有可以參考的設計，也需要你去 search 一下 recent & prior relevant works
```

### 10 Oct 22:09

This answers four questions at the end of Claude's plan (`analysis/rule-template-plan.md` §7): 1. make cautions their own type, or fold them into `SHOULD WATCH FOR`; 2. default bare imperatives to SHOULD, raising to MUST only on legal wording; 3. write exceptions with UNLESS in the same sentence and EXCEPTION TO across passages; 4. scope (chapters 2 and 3 first?).

```text
1. 可以先併進去 should watch for
2. ok
3. ok
4. 一樣先從 overtaking (passing) 開始做就好，但你的 keyword 仍然需要先去做 full book scanning 去規劃 wording & template you are going to use。


你整理完的 rule 我希望可以用我們剛剛產生的: https://claude.ai/artifact/A8gZroLVV8miAsmAym44C6 頁面一樣，可以左右對照著看
```

### 11 Oct 01:46

```text
要不要在前面先有一個 overall 的 template, wording 介紹？畢竟我們的重點也在提出一個好的 natural-language-like formal rule
```

### 10 Oct 23:00, decision card (Claude asked, michael chose)

```text
Question: 加入全書掃描找到、不在你 96 段裡的 8 句超車規則?

Context: 這 8 句在其他頁。Stopping 頁 5 句校車規則:校車上方紅燈閃時必須停車、從後方來要停在 20 m 外、等校車開走或燈停才能走、有中央分隔島時只有後方來車要停、違規記 6 點。Changing directions 頁 2 句:左轉時不要開到前面轉彎的機車或腳踏車旁邊一起轉。Signs 頁 1 句:多車道上的慢車必須靠右。目前規則集裡校車只有一句 FACT(可以檢舉違規超越校車的車),真正的法規不在裡面。

- 加入: 我把 8 句寫成規則放進對應段落,左欄最後加一區「其他頁」,用同一個連結更新頁面和 JSON。
- 先不加: 規則集維持你 96 段的範圍,這 8 句留在頁面的「全書掃描找到的」區。
```

michael chose "加入" at 23:04. The 8 sentences became 7 statements: 3.4.3b, 3.4.3c, 3.4.12b to 3.4.12e and 3.6.1d (inputs c1 to c9, with the sign image as c9).

## Appendix B: prior-work search prompt, verbatim

A Claude subagent ran this from 21:58 to 22:02 on 10 Oct; its report fed §5 of `analysis/rule-template-plan.md`.

```
Research task (do NOT call any mcp__hearthbot__ tools; just return a report to me). Do not install packages.

Context: a lab project converts the Ontario MTO Driver's Handbook into "formal rules" written in a natural-language-like controlled template language (not LTL/symbolic), designed as a MINIMAL set of fixed keywords/patterns (like SQL's small keyword set) so an LLM/VLM can reason over them. Content types seen in the handbook: obligations/prohibitions (must, must not, illegal), permissions (may, only if), advisory (should, avoid, never as advice), cautions (watch for, be prepared), procedures (ordered steps with done-conditions and fallbacks), definitions, background facts, exceptions (unless/except), reasons (because), penalties (fines, demerit points), vague/judgment terms (safe, enough, if in doubt, as soon as you can).

Use WebSearch (and WebFetch where useful) to find prior designs we can borrow from. For each, give: name, citation/URL, what its keywords/patterns are (quote the actual pattern set where possible), and what specifically we could borrow or what to avoid. Cover at least:
1. EARS (Easy Approach to Requirements Syntax, Mavin et al.) – its 5-6 patterns.
2. SBVR (OMG Semantics of Business Vocabulary and Rules) Structured English and RuleSpeak – modal keywords (It is obligatory that / permitted / necessary), vocabulary/term definitions.
3. Logical English (Kowalski) and Catala (legal programming language with default/exception logic).
4. Attempto Controlled English (ACE) and other CNLs for rules; Gherkin Given/When/Then briefly.
5. LegalRuleML / deontic modelling of obligations, permissions, prohibitions, defeasibility.
6. Traffic-rule formalization work: Rulebooks (Censi et al. 2019, rule hierarchy/priorities), Rizaldi et al. Isabelle formalization of traffic rules for overtaking (German StVO / Vienna Convention), Maierhofer et al. formalization of interstate traffic rules (overtaking), any work on traffic rules in Metric Temporal Logic, and recent (2023-2026) LLM-based traffic rule extraction/formalization or LLM driving with traffic-rule knowledge retrieval (e.g. papers that convert driving handbooks/regulations into structured rules with LLMs; "driving with regulation", "LLM traffic rules", "LeGEND", etc.). Note how they handle vague terms (e.g. "safe distance") and exceptions.
7. Any work on handling vagueness/open-texture in legal rule formalization (e.g. marking judgment predicates, "open texture").

Keep the report under ~1500 words, structured, with URLs. Clearly mark anything you couldn't verify.
```
