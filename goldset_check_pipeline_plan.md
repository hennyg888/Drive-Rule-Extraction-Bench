# Gold set construction and evaluation: plan

How draft rules extracted by Opus 5.5 become ground-truth gold sets, one for each of two scopes (overtaking and all rules; see "Two scopes, one procedure"). The first is overtaking: `gold_set\mto\overtaking\00_raw_rules.json`, identical to `extraction_outputs\anthropic\claude-opus-5.5\mto_2026_11_14.json`, now refined into `gold_set\mto\overtaking\gold_set.json`. The plan also covers how those gold sets are then used to evaluate other extractions (Qwen VL models, several input modalities: text only, text and images, whole pages as images).

## The basic idea

There are two parts with opposite goals:

| | Part A: gold set construction | Part B: evaluation |
|---|---|---|
| Input | the Opus 5.5 draft only | every extraction, **including the raw Opus draft again**, every Qwen model, every modality |
| Goal | find and fix as many errors as possible | measure extractions comparably |
| Checks | **flexible**: a freeform Claude Code check opens each round, then the format, atomic and aggregate checks; prompts may improve as errors are discovered | **fixed and constant**: one frozen protocol, versioned |
| Semantic errors | open-ended judging against the handbook | **cheap comparison against the gold set**: no open-ended judging, no corpus in context |
| Fixes | yes (human triage, Claude Code applies) | none, report only |
| Runs per input | as many rounds as needed | **once** per protocol version |

Part A doesn't need to be comparable, because comparability comes from Part B: the raw Opus draft is evaluated again with the same frozen protocol as every Qwen output. Part A doesn't need to discover every error type either: it only has to make the gold set correct. Error types that only Qwen makes are discovered inside Part B's single evaluation run (§B6), so no output is checked twice.

## Two scopes, one procedure

Gold sets are built for exactly two rule scopes: **overtaking**, a small set of rules, and **all rules**. Part A and Part B are the same for both. Each scope has its own folder, `gold_set\<handbook>\<scope>\` (e.g. `gold_set\mto\overtaking\`, `gold_set\mto\all\`), which holds its round files, its reports and its triage records (`allow_list.md`, `error_set.md`).

**Merging is dropped.** It was originally planned as a third scope, but it is no longer being done, for two reasons:
- It overlaps heavily with overtaking (lane changes, passing lanes, lane-ending merges), so it would add little that overtaking doesn't already test.
- Three handbooks × three scopes would mean nine gold sets, which is more than there are people to build. Two scopes means six.

Everything that differs between scopes should live in one config file per scope, so scripts and judge prompts don't change (planned, not built yet):

`gold_set\mto\<scope>\scope.yaml`:

| Key | What it is | Overtaking example |
|---|---|---|
| `topic` | the extraction prompt's topic line (the judges see it, since the extraction prompt is in every request) | "overtaking (passing another vehicle, and being passed)" |
| `topic_code` | the rule-id topic code | `PASS` |
| `allow_lowercase` | format-check allowlist: verbs spelled like a vocab term | `[pass]` |
| `scope_notes` | where the scope's boundary lies, written before discovery; boundary cases decided at triage go into `allow_list.md` | e.g. is "being passed" in scope? (yes) |

The judge prompts are identical across scopes.

**Order:**

1. **Overtaking:** the pilot; the procedure settled here (rounds a–c, §A2).
2. **All rules:** the same procedure at a larger scale. This also tests whether the procedure carries over unchanged. Any change it needs is recorded as a change to the procedure, which then applies to both scopes.

**The all-rules scope at scale** (likely several times more rules than overtaking's 75):

- The atomic check's cost grows linearly with the number of rules checked; `--previous` keeps later rounds to the rules that changed.
- The aggregate check's single call may outgrow one response; split the rule set by group, and find pairs that cross groups by shared citations or shared terms.
- The freeform check is split by page range or group, across several Claude Code sessions.
- Triage is the real bottleneck: sort by severity and confidence, major findings first, and use automated proposed triages (§A1) for the long reports.

**Reuse across scopes:** the overtaking rules are a subset of the all-rules scope. When building the all-rules gold set, first compare its draft against the finished overtaking gold set with Part B's semantic comparison (§B4):

- **Matched rules** adopt the verified gold wording. They still go through the format check and the consistency check below.
- **Unmatched or conflicting rules** go through the full Part A.

This saves most of the cost for the overlapping rules, and it keeps scopes consistent. The overtaking `allow_list.md` and `error_set.md` are a starting point for the all-rules ones: general rulings carry over; scope-specific ones (e.g. what counts as overtaking) do not.

**Consistency check:** once the all-rules gold set exists, every overtaking gold rule should be covered by it with the same meaning. Each difference is decided by a human: fix whichever side is wrong, and bump that gold set's version.

**Part B per scope:** each extraction is scored against the gold set of its own scope. Since the overtaking gold set is a subset of the all-rules one, one comparison comes free: does an all-rules extraction cover overtaking as well as a targeted overtaking extraction does?

---

# Part A: gold set construction (flexible)

## A1. The loop

Each round runs four checks in order, and the round repeats until the stopping condition (§A4) is met:

```
freeform (stage 0)  →  format (stage 1)  →  atomic (stage 2)  →  aggregate (stage 3)  →  next round, if needed
```

Every check runs the same loop:

```
detect (Claude Code / script / LLM judge)  →  triage (human)  →  Claude Code fixes  →  next check
```

- **Triage (human):** each finding gets a decision, written as a **Triage** line directly under the finding in its report (not in a combined table at the end):
  - **fixed** (as proposed, or **partly**, or differently: say how);
  - **rejected:** not an error, often because an earlier triage settled it;
  - **ignored:** perhaps an error, but too minor or out of scope to act on.
  A short note at the top of the report records only cross-cutting facts: the target file, rules added, merged or renumbered, and the format check result after the fixes.
- **Automated proposed triages (optional):** Claude Code can draft a **Proposed triage** line under every finding, drawing on `allow_list.md`, `error_set.md` and the past reports' triages. This is most useful for the long reports the atomic check produces (60–100 findings). It speeds triage up but **does not replace human review**: the human reads each proposal, accepts or changes it, and only then are fixes applied. Proposals relabelled as accepted become **Triage** lines. A proposal that would reopen an earlier decision says so, so the human can decide.
- **Fix (Claude Code):** applies the accepted fixes to a copy of the input, which becomes the step's rules file (§A2). Small edits only, nothing broader than the finding asks for. Every statement a fix touches is rebuilt from its fields, and the format check runs on the result.
- **Triage records:** after each round, decisions that set a precedent go into the scope folder's two lists:
  - `error_set.md`: kinds of error that were confirmed and fixed, with examples (step and finding id);
  - `allow_list.md`: kinds of finding that were rejected or ignored, with examples, so later findings of the same kind can be rejected by pointing there. This includes "re-raising a settled triage": rejected unless new evidence is given.

## A2. Stages, rounds and file names

Two terms:

- **Stage** (a number): a kind of check. 0 freeform, 1 format, 2 atomic, 3 aggregate.
- **Round** (a letter): one pass through the four stages. Round `a` is the first pass; `b`, `c`, … follow until the stopping condition is met.

| Stage | Name in files | Detector |
|---|---|---|
| 0 | `freeform` | Claude Code, freeform |
| 1 | `format` | script |
| 2 | `atomic` | LLM judge, one call per rule |
| 3 | `aggregate` | LLM judge, one call with the whole corpus and rule set |

Each step is named **round letter + stage number**: `a2` is round a, stage 2. Every step writes a matching pair:

- `<step>_<name>_report.<md|txt>`: what the check found, run on the previous step's rules (the report's header names its input file), with a Triage line under each finding;
- `<step>_<name>.json`: the rules after that step's accepted fixes. It is written even when nothing changed, so every report has a matching rules file and the highest step is always the latest version. The final freeform check (§A4) may write only its report.

The overtaking progression, as built in `gold_set\mto\overtaking\`:

```
00_raw_rules.json                                  the Opus draft, never edited
a0_freeform_report.md     a0_freeform.json         round a
a1_format_report.txt      a1_format.json
a2_atomic_report.md       a2_atomic.json
a3_aggregate_report.md    a3_aggregate.json
b0_freeform_report.md     b0_freeform.json         round b
b1_format_report.txt      b1_format.json
b2_atomic_report.md       b2_atomic.json
b3_aggregate_report.md    b3_aggregate.json
c0_freeform_report.md                              final freeform check: no major errors, minor ones ignored
gold_set.json                                      a copy of b3_aggregate.json, frozen
allow_list.md   error_set.md                       triage records for this handbook and scope
```

The names sort in order of progression: `00_` first, then `a0` … `a3`, `b0` …, then `gold_`.

- **Partial re-checks within a step** add a dot number: `a2.2_atomic_report.md`, `a2.2_atomic.json`.
- **The step id is used everywhere** a check or fix is named: report headers, triage records (`a0 M2`, `b2 S2-038`), run folders (`runs\<time>-check-atomic-<scope>-b2\`).
- **Finding ids** repeat across rounds (each atomic report starts at S2-001), so the triage records cite them with the step (`b2 S2-028`).

### The raw draft (`00_raw_rules.json`)

Comes before round a. `tools/extract.sh` sends one handbook's whole corpus (`corpus\<handbook>\`, every page and image) with the `formal-rules` prompt to Opus 5.5 (medium effort, 128K output tokens) in a single request. It can be run from any folder:

```
tools/extract.sh ca --dry-run     # build the message and show its size and input cost, call nothing
tools/extract.sh ca               # the real call; handbook: mto, ca or tx (default mto)
```

Anything after the handbook is passed on to `tools/run_extraction.py` (e.g. `--set extra_body.reasoning.effort=high`). The topic comes from the extraction prompt (`prompts\formal-rules\task.md`), so the overtaking topic is the default.

- The answer is saved as `extraction_outputs\claude-opus-5-5\<handbook>_<YYYY_MM_DD>.json`, and the whole call goes to `runs\<time>-anthropic_claude-opus-5-5-<handbook>-draft-gold\`. (The script's header comment names `extraction_outputs\anthropic\claude-opus-5.5\`, where the MTO draft is, but the current `--model anthropic/claude-opus-5-5` saves it to the folder above.)
- Copy the answer unchanged into the scope folder as `gold_set\<handbook>\<scope>\00_raw_rules.json`. It is never edited; round a0 works on a copy.
- Optionally, run the format check on it at once (`check_format.py ... --handbook <handbook>`) for an early view of its mechanical errors. The format check that counts is still a1.

Measured: CA, 23 pages and 74 images, 80.6k input and 17.5k output tokens, 133 s, $0.67 (42 rules, 14 vocabulary terms).

### Stage 0: freeform (Claude Code)

Opens every round. A Claude Code session reads the whole rule set against the handbook, with in its context:

- **the corpus:** `corpus\<handbook>\` (the handbook pages as the extractor saw them, with block ids and images);
- **the rules:** the latest rules file of the scope folder;
- **the extraction prompt:** `prompts\formal-rules\` (system.md, task.md, schema.json), which defines what a correct rule is;
- **past triages, if any:** the scope folder's earlier reports (their Triage lines), `allow_list.md` (what is not an error) and `error_set.md` (confirmed error types). Findings of a kind the allow list rejects are not raised again unless there is new evidence.

The check is open-ended: faithfulness, strength, conditions and exceptions, grammar and vocabulary, citations, vague terms, notes, coverage and conflicts between rules. It writes `<round>0_freeform_report.md`, with findings in the same form as the other checks (severity, quotes as `id`: "text", a suggested fix) and grouped by severity. Because it reads the whole set against the whole handbook, it implicitly covers much of what the format, atomic and aggregate checks do, which is why a round can end on it (§A4).

In round `a` it fixes obvious errors early, so the judges in stages 2–3 don't spend tokens on them, and it shows early which kinds of errors the draft has. In later rounds it also checks that the previous round's fixes are consistent with each other and that conventions decided at triage are applied everywhere.

### Stage 1: format (script)

`python error_check_pipelines/goldset/check_format.py <rules.json> [--handbook mto] [--allow-lowercase pass ...] [-o report.txt]`. Mechanical checks only:

1. valid JSON that matches `prompts/formal-rules/schema.json`;
2. `statement` is exactly the fields filled into the grammar;
3. `id` = `topic-group-number`; one topic; group codes of 2–5 letters; ids unique; groups contiguous; numbers `01, 02, …` in order within each group;
4. `force` allows the `modal`;
5. every rule has evidence; every cited id (rules and vocab) exists in the corpus; no duplicate ids in a list;
6. every vague term appears word for word in its statement;
7. every capitalized term has a vocab entry; every vocab entry is used; no duplicate vocab terms;
8. no vocab term is written in lowercase in a statement, apart from a fixed allowlist (default `pass`, the verb, as in the extraction prompt's example; plurals included).

The output is a short readable report (`-o <round>1_format_report.txt`); the exit code is 1 when there are errors. The atomic and aggregate checks refuse input that fails it. It also runs after every set of fixes, so no fix breaks the format.

### Stage 2: atomic (one LLM call per rule, no corpus)

`python error_check_pipelines/goldset/check_atomic.py <rules.json> [--previous OLD_RULES.json] [--rules ID ...] [--workers 4] [--dry-run] [--out-dir DIR]`. Each rule is judged in isolation. Each call contains, in this order:

- the judge's system prompt (`prompts\atomic\system.md`);
- the extraction prompt (`prompts/formal-rules` system.md + task.md, verbatim) and the judge's task (`prompts\atomic\task.md`). These are the same in every call, so they are marked as a **prompt-cache breakpoint**: the first call runs alone to write the cache, and the rest run in parallel and read it;
- the rule;
- the vocabulary entries it uses, with the blocks that define them;
- **each cited block alone**, labelled with its page and section heading, with only the images inside it (a cited figure brings its image and caption; a caption id brings only the caption). The surrounding section is not sent.

The judge is asked an open question (what is wrong with this rule?), and answers with findings in a general form: a title, a category, severity, a free-text description that quotes the handbook as `id`: "text", a free-text suggested fix, and confidence. A rule whose support isn't in its cited blocks is reported as "unsupported by its citations".

**`--previous`** skips rules already checked in an earlier round: a rule is skipped when the earlier file has a rule with the same fields (ignoring id and number, so renumbered rules match) that uses the same vocabulary entries. Rules that are new, edited, or use a changed vocabulary entry are checked. The usual choice is the previous round's format output (round b's atomic check ran with `--previous a1_format.json` and checked 54 of 74 rules).

Judge: `anthropic/claude-opus-5-5` (Opus 5.5, medium effort). Measured cost before caching and the cited-blocks-only context: $3.81 for 72 rules (a2), $2.96 for 54 rules (b2), about $0.05 per rule. With both changes, the input per call drops from about 8,200 to about 4,500 tokens, most of it read from the cache, so a call should cost about half as much (output then dominates); this is not measured yet. The report goes next to the input, named by step (`a1_format.json` → `a2_atomic_report.md`); requests, responses, `findings.jsonl`, `triage.csv` and `meta.json` (with cache write and read tokens) go in `runs\<time>-check-atomic-<scope>-<step>\`.

Trade-off of the narrower context: the judge no longer sees the sentences around a cited block, so a condition or exception stated next to it but not cited is left to the freeform and aggregate checks.

### Stage 3: aggregate (one call, whole corpus and rule set)

`python error_check_pipelines/goldset/check_aggregate.py <rules.json> [--dry-run] [--no-images] [--out-dir DIR]`. One call with the extractor's instructions, the whole corpus as the extractor saw it (table of contents, every page, images) and the whole rule set. The judge looks for:

- **coverage:** in-scope rules, conditions, exceptions or diagrams the set does not capture, and supporting passages elsewhere that are not cited;
- **conflicts:** rules that contradict each other, overlap at different strengths, duplicate each other, or use terms inconsistently;
- anything else wrong with the set as a whole.

It answers in the atomic check's findings form, with `kind` (coverage / conflict / other) and `rules`. About 200k input tokens per call; measured $0.95 (a3) and $0.96 (b3) per run. The report is named by step (`a2_atomic.json` → `a3_aggregate_report.md`); the run folder is `runs\<time>-check-aggregate-<scope>-<step>\`. New or changed rules from its fixes go through the format check; the next round's atomic check covers them.

## A3. How discovery feeds back

After each confirmed error is fixed, ask: **could an earlier check have caught this kind of error in general?** The answer becomes a check, never a list of past answers:

| What was learned | Where it goes | Example |
|---|---|---|
| Something a script can decide | a new format check | lowercase vocab terms → check 8 |
| A *kind* of checking the judge skips | a general change to the judge prompt (never an instance example) | the required terms review |
| Something that is not an error | `allow_list.md` (and the format-check allowlist, if a script can enforce it) | the verb "pass" in lowercase |
| A new kind of error | `error_set.md` | as they come up |

The judge prompts never include the triage records or a growing list of examples, so they stay general; only the freeform check reads them. The prompts may still improve between rounds; each change is a new prompt version (hash in `meta.json`). Part A's prompts and format script are the starting point for Part B's frozen protocol.

## A4. When to stop

Stop iterating when the latest round is quiet:

1. **few major errors:** each check of the round reported and led to fixing only a few major errors (e.g. **3 or fewer**);
2. **isolated fixes:** the fixes are local. They don't introduce many new rules, and they don't change vocabulary terms in ways that affect other rules or terms.

Then end the refinement cycle on a **final freeform check** (the next round's stage 0) instead of running the full round again: the freeform check implicitly does much of what the format, atomic and aggregate checks do. If it finds no major errors, freeze the latest rules file as `gold_set.json`. Minor findings in the final check can be ignored if they are too minor to act on (recorded as Triage lines).

Record the frozen file's hash, the prompt versions, the date and the finding counts per round. The overtaking scope took two full rounds (a, b) and a final freeform check (c0).

## A5. Rule ids across versions

Splits, merges and added rules renumber ids. Fixes avoid renumbering where they can (a new rule goes at the end of its group; rule order within a group is not an error). Where renumbering happens, the report's top note lists the old and new ids, and the triage records give rule ids as they were at that step. A planned `id_map.json` would record, for each raw rule, the gold rule(s) it became, or "removed" with a reason; Part B's validation (§B7) should rediscover these mappings.

## A6. The error log

Today the log is the reports themselves: every finding with its Triage line, plus `allow_list.md` and `error_set.md`. A planned `corrections.jsonl` would add one machine-readable line per confirmed error:

```json
{"raw_rules": ["PASS-PROC-07"], "gold_rules": ["PASS-PROC-07"], "found_by": "a0|a1|a2|a3|b0|…",
 "category": "clarity and ambiguity", "subtype": "polarity", "meaning_changing": true,
 "before": {...}, "after": {...}, "decision": "fixed"}
```

It would give:

- **a labelled test set for Part B:** comparing the raw draft against gold should flag every `meaning_changing: true` correction, and nothing for wording-only ones;
- **the error types' evidence:** real examples and counts per subtype;
- **which check found what:** if the freeform check keeps finding a kind of error, an earlier check needs a general check for it;
- **judge precision:** rejected findings (in each run's `triage.csv` and the reports) are its false positives.

It can be backfilled from the reports' Triage lines.

## A7. Supporting details

**Findings format** (judges and freeform checks):

```json
{"rules": ["PASS-PROC-07"], "title": "Lowercase \"not\" inside a MUST action mixes a ban with a duty",
 "category": "clarity and ambiguity", "severity": "major|minor",
 "description": "... quoting handbook blocks as `id`: \"text\" ...",
 "suggested_fix": "...", "confidence": "high|medium|low"}
```

The run folder adds `finding_id`, `stage`, `detector` and `call`.

**Triage file:** each judge run also writes `triage.csv` (`finding_id, stage, rules, title, category, severity, confidence, description, suggested_fix, decision, notes`). In practice decisions are recorded as Triage lines in the report.

**Prompt caching:** `drbench/models/claude.py` supports a cache breakpoint on any content part, and cost estimates price cache writes at 1.25× input and cache reads at the preset's cache-read price (`models.yaml`). The atomic check uses it; the aggregate check is a single call, so caching helps it only when it is re-run on the same corpus within the cache's lifetime.

**Run folders:** `runs\<time>-check-<stage name>-<scope>-<step>\` with `meta.json` (preset and params, prompt and input hashes, git commit, tokens, cost), the prompt copy, one subfolder per call, `findings.jsonl` and `triage.csv`.

**Error taxonomy:** `error_check_pipelines\goldset\error_taxonomy.md` holds general categories and conventions for analysis. It is **not given to any judge**. The per-scope `allow_list.md` and `error_set.md` are the working triage records.

---

# Part B: evaluation (fixed)

## B1. Frozen protocol

When gold v1 is frozen, the evaluation protocol is frozen as **v1**: format script version, judge prompts, judge model and settings, the scoring rules, all hashed. Every extraction is evaluated with it **once**:

- the raw Opus draft (`00_raw_rules.json`), again, as an ordinary contestant;
- every Qwen model, every input modality.

The protocol changes version only when **detection** changes (§B6), and then every set is re-run.

## B2. Format errors: the format script

The same script as stage 1 (frozen version). Format errors are counted per check, the same way for every model. Smaller models will likely fail here most: broken or truncated JSON, schema violations, invented block ids, statements that don't match the grammar. Needs one decision before the freeze: how to score output that won't parse at all (zero, or partial credit for the parseable part).

## B3. Vocabulary mapping

Before comparing rules, map the extraction's vocab terms onto the gold set's by meaning (e.g. OVERTAKER → PASSER, or "no gold equivalent"), so naming differences are not counted as meaning differences. The mapping is reported too (invented terms, one gold term split in two).

## B4. Semantic comparison against the gold set

Rules are compared by **meaning**, not field by field. The test: *would a driving model following the extracted rule do the same thing, in the same situations, as one following the gold rule?* Different wording, conditions placed in other fields, other vocab names and different granularity are not errors.

Matching is many-to-many: a gold rule can be covered by two extracted rules (split), or one extracted rule can cover two gold rules (merged). Shared cited block ids give cheap candidate pairs; the judge confirms.

Outcomes:

- each **gold rule**: covered / partially covered (the core is there, but a condition, exception, actor or strength is off) / not covered;
- each **extracted rule**: matches gold / conflicts with gold / unmatched.

For each difference the judge records:

- **dimension** (fixed list, scored): situation (conditions), exception, actor, required behaviour, strength; plus missing, invented, conflicting, out of scope;
- **description** (free text): what differs, quoting both rules;
- **suggested subtype** (free text).

No corpus is in context: the gold set and the extraction are each about 12k tokens.

## B5. Unmatched extracted rules

The only place that needs the handbook. Each unmatched rule is checked against its cited blocks (like the atomic check: isolated, cheap): invented / out of scope / **a real rule the gold set missed**. The gold set is assumed complete, but a real rule it missed is confirmed by a human, added in gold v1.1, and every set is re-scored against it.

## B6. New error types without re-checking

Detection does not depend on knowing error types: a never-seen Qwen error still shows up as a difference in meaning. Error types only affect how differences are **named**:

- scores use only the fixed **dimensions**, so they stay comparable whatever new errors appear;
- new types show up in the stored descriptions; the taxonomy grows by **relabelling the stored findings** (by hand, or one cheap text-only call over the findings alone), never by re-evaluating an output;
- the protocol version changes only if the *way of detecting* changes (e.g. the meaning test was wrong), and then every set is re-run.

So there is no separate discovery pass on Qwen outputs: each output is evaluated once.

## B7. Validating the protocol before using it

Run protocol v1 on the raw Opus draft first. The overtaking reports' Triage lines (or `corrections.jsonl`, once backfilled) say exactly which differences between the draft and gold change meaning. The comparison should flag those, and nothing for wording-only corrections. This measures the protocol's recall and precision on known errors before any Qwen output is evaluated, and costs one comparison of one rule set. Running the comparison twice on one set also shows how stable the judge is.

## B8. Scores per extraction

- **coverage (recall):** share of gold rules covered, partially covered, not covered;
- **precision:** share of extracted rules that match gold; conflicting, invented and out-of-scope counts;
- **meaning errors** per fixed dimension (subtypes as a descriptive breakdown);
- **format errors** per format check, reported separately from meaning;
- **citations:** overlap with the gold set's citations (depends on the modality; see open questions).

## B9. Cost

Each extraction: the format script (free), one vocabulary mapping and a few comparison calls on two rule sets of ~12k tokens each, plus small calls for the unmatched rules. No corpus, so no caching needed. Total tokens: one Opus discovery (Part A), one validation run (§B7), and one evaluation per extraction.

---

# Current state and next steps

Built:

- `error_check_pipelines\goldset\check_format.py` (stage 1, 8 checks);
- `error_check_pipelines\goldset\check_atomic.py` with `prompts\atomic\` (stage 2; `--previous`, prompt caching, cited blocks only);
- `error_check_pipelines\goldset\check_aggregate.py` with `prompts\aggregate\` (stage 3);
- prompt-cache support and cache-aware cost estimates in `drbench\models\`;
- `error_check_pipelines\goldset\error_taxonomy.md` (categories and conventions; not given to judges).

Overtaking (`gold_set\mto\overtaking\`): done. Rounds a and b ran all four checks; the final freeform check `c0_freeform_report.md` found no major errors, and its 4 minor findings were ignored. The gold set is frozen as `gold_set.json` (75 rules, 20 vocabulary terms), a copy of `b3_aggregate.json`. The triage records are `allow_list.md` and `error_set.md`. Superseded test files are in `archive\`.

California overtaking (`gold_set\ca\overtaking\`): the raw draft `00_raw_rules.json` was extracted on 2026-11-18 (42 rules, 14 vocabulary terms). A first format check found 5 errors: one cited id that isn't in the corpus, `HOV` with no vocabulary entry, and "driver" in lowercase three times. Round a is next.

Next:

1. Record `gold_set.json`'s hash, the prompt versions and the date (§A4).
2. Measure the new atomic check's cost on a few rules (`--rules`), and confirm cache reads in `meta.json`.
3. Optional: add `scope.yaml` and have the scripts read it (topic, allowlist) in place of the hard-coded `pass` default; have `check_format.py` name its output by step as the judge scripts do (today it writes only with `-o`); backfill `corrections.jsonl` and `id_map.json` from the reports.
4. All rules: extract, compare against the overtaking gold set (reuse matched rules), then Part A on the rest (freeform → format → atomic → aggregate, repeated until §A4 holds), seeding its `allow_list.md` and `error_set.md` with the general overtaking rulings; consistency check → `gold_set\mto\all\gold_set.json`.
5. Part B: freeze protocol v1, build the comparison, validate on the raw drafts (§B7), then evaluate the Qwen outputs per scope.

# Open questions

- **Is the raw Opus draft a reported contestant** in the benchmark, or only the validation set for Part B?
- **Citations for whole-page-image input:** the model can't see block ids. Should citations then be page-level, matched to blocks by quote (`drbench/grounding.py` already does this), or shown as ids drawn on the images?
- **Part B judge:** Opus 5.5 for every evaluation (paid, the same for all sets), or a local Qwen judge (free, weaker, and Qwen judging Qwen)?
- **Output that won't parse:** scored zero, or partial credit for the parseable part?
- **Reuse for the all-rules scope:** adopt the verified gold wording for matched rules (recommended), or run every all-rules rule through the full Part A for strict independence?
- **Aggregate check at scale:** one call per group for the all-rules scope, or the full rule set in one call while it fits?
