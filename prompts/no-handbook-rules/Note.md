# Notes on the no-handbook formal-rules prompt

A closed-book version of `../no-image-rules`. No handbook is sent. The model is given
only a topic and a region, and writes the rules from memory, in the same grammar. There are no
citations. This file is not sent to the model.

## Files

| File | Contents |
|---|---|
| `system.md` | Background only: what the rules are for, and that no document is given. The model works from its knowledge of the region's traffic law and official driver's handbook, and must not carry over rules from other regions. |
| `task.md` | All the instructions: rule grammar, numbering, force and modal, vocabulary, vague words, an example, and the topic and region lines at the end. |
| `schema.json` | `{scope, region, vocabulary, rules}`. Same as `formal-rules`, but with no `evidence` field on vocabulary or rules, and with a `region` field added. |

## Changing the topic or region

The last two lines of `task.md` are templates, filled in from `drbench/prompts.py`:

```
Topic: {{topic}} only.
Region: {{region}}
```

`--topic` (`overtaking`, `turning`, `parking`) fills `{{topic}}` from `TOPICS`, and also
`{{situations}}`, the topic's list of situations in the final check. `--region` (`ca`, `tx`,
`mto`) fills `{{region}}` from `REGIONS` (California, United States / Texas, United States /
Ontario, Canada). Only this prompt takes `--region`; it defaults to `--handbook`. The hash is of
the filled prompt.

## Changes from no-image-rules

- `system.md`: the "handbook text" section (TOC, articles, block ids, missing images) became "What
  you are given": a topic and a region, nothing else.
- `task.md`: every mention of the handbook pages is now about the region's law and official
  handbook. The "Evidence and citations" section and all `evidence` fields are gone.
- Force: REQUIREMENT means set by law or regulation (or a regulatory sign, or a penalty), and
  INSTRUCTION means a plain command in the official handbook that isn't stated as law.
- `note` now also covers details the model is unsure of (a number, a penalty, law or advice).
- The final check goes through the topic situation by situation instead of block by block, and
  warns against writing rules the region doesn't have.
- Example: `evidence` removed, `region` added, the notes no longer mention pages or diagrams.

## Checked so far

- The example in `task.md`, with its `...` removed, fits `schema.json`, and each example
  `statement` is exactly its fields filled into the grammar.
- **Not yet tried on a model.**

## Things to know

- **Closed book in the runner:** a prompt whose `task.md` has `{{region}}` is sent as `task.md`
  alone, with no pages, images or TOC (`messages.build(closed_book=True)`), e.g.
  `python tools/run_extraction.py --model anthropic/claude-opus-5-5 --prompt no-handbook-rules --region tx --topic turning`.
- **The example is Ontario overtaking content.** Its three rules (pedestrian crossover 30 m, broken
  line, cyclists 1 m) are real Ontario rules, so an Ontario run is handed those three. For a fair
  closed-book test, use an example from a different region or topic, or count those three
  separately when scoring.
- **Scoring:** with no evidence, outputs can only be matched to the gold set by rule content, not
  by cited blocks. `grounding.py` skips entries without `evidence`.
