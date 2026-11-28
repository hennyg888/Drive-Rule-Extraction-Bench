# Notes on the all-formal-rules prompt

This prompt extracts **every** rule of the road in a handbook (the "all rules" gold-set scope in
`goldset_check_pipeline_plan.md`), in the grammar of the legacy Ontario passing rules
(`legacy/ontario_passing_rules.yaml`), as JSON that follows `schema.json`. It started as a copy of
`../overtaking-formal-rules/`; the grammar, force/modal table, citations, vocabulary, vague-word
and note instructions, and `schema.json` are unchanged. This file is not sent to the model.

## Files

| File | Contents |
|---|---|
| `system.md` | Background only: what the rules are for, and how the corpus HTML is laid out (table of contents, `<article data-page>`, block ids, figures). Same as the overtaking prompt. |
| `task.md` | All the instructions, placed after the handbook pages: what counts as a rule, scope, rule grammar, vocabulary, force and modal, numbering, citations, vague words, the example, and the answer instructions. |
| `schema.json` | The answer: `{scope, vocabulary, rules}`. Same as the overtaking prompt. |

## Differences from overtaking-formal-rules

- **Scope section** (new): every rule a driving model can recognize and act on, on any topic.
  Negative examples of what is out: licensing and tests, licence-level conditions (blood alcohol
  level, accompanying driver), the driver's own fitness to drive, paperwork, and things done
  before driving (maintenance, seatbelts, child seats). Road-test pages are cited alongside the
  main rule, not repeated.
- **Topic codes vary per rule and are chosen by the model.** `topic` is no longer one code for
  the run. The model picks broad topic codes itself (examples given: TURN, PARK); only PASS is
  fixed, with the overtaking groups (GEN, PROC, LOC, MARK, SIDE, USER, BEING), so all-rules PASS
  rules line up with the overtaking gold set for the reuse step in the plan. Other topic codes
  may differ between runs. A fixed 21-code table was tried and dropped as too restrictive.
- **One shared vocabulary** across all topics.
- **Ordering:** topic by topic, then group, then handbook order.
- **Example:** same three PASS rules, with `scope` set to `"all rules of the road"`.
- **No topic line:** the overtaking prompt's final `Topic: ...` line is removed; the first
  sentence and the Scope section say what to extract.

## Running it

```
python tools/run_extraction.py --model anthropic/claude-opus-5-5 --handbook mto --prompt all-formal-rules
```

A dry run of the whole MTO handbook is ~169K input tokens (30 pages, 245 images).

## Things to know

- **The answer is long.** The whole MTO handbook will likely give several hundred rules. The MTO
  overtaking run used 26.6K output tokens (7.4K reasoning) for 68 rules, about 280 answer tokens
  per rule, so Opus's 128K limit holds roughly 350-400 rules after reasoning. The OpenRouter
  Qwen/Gemini/GPT presets allow only 32K (about 80-100 rules), the local vLLM Qwen presets 64K,
  and Qwen's thinking takes a large share of that. `drbench/run.py` prints a WARNING and records
  `"truncated": true` in meta.json when a reply stops at the limit; if that happens, split the
  run by `--pages`.
- **Prefer the direct `anthropic/` preset over `openrouter/`** for this prompt: the Anthropic
  client streams, while the OpenRouter client waits for the whole reply in one request
  (~85 tokens/s, so a full 128K reply takes ~25 minutes). If a single response can't hold it, run page ranges with `--pages` and merge;
  topic codes and vocabulary would then need reconciling by hand, since each run picks its own.
- **Not yet tried on a model.**
- **Citations are block ids only.** A rule resting on a diagram alone says what the diagram shows in
  its `note`. Figures are `21.7`, captions `21.7-c`, images in a table row `6.35-f1`.
- **This file is copied into each run folder** along with the prompt, but it isn't part of
  the prompt hash and doesn't change what the model sees.
