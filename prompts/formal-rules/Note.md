# Notes on the formal-rules prompt

This prompt writes rules in the grammar of the legacy Ontario passing rules
(`legacy/ontario_passing_rules.yaml`), as JSON that follows `schema.json`. It is laid out as
`../Prompt_Notes.md` recommends. This file is not sent to the model.

## Files

| File | Contents |
|---|---|
| `system.md` | Background only: what the rules are for, and how the corpus HTML is laid out (table of contents, `<article data-page>`, block ids, figures). |
| `task.md` | All the instructions, placed after the handbook pages: rule grammar, numbering, force and modal, citations, vocabulary, vague words, three examples, and the topic line at the end. |
| `schema.json` | The answer: `{scope, vocabulary, rules}`. Evidence entries keep the `{block, quote}` shape, so `grounding.py` checks them unchanged. |

## Changing the topic

The last line of `task.md` sets the topic:

```
Topic: extract formal rules about overtaking (passing another vehicle, and being passed) only.
```

To change the topic, edit only that line, e.g. `Topic: extract formal rules about turning at
intersections only.` or `Topic: extract all rules of the road.` Ids and groups adapt to it, because
the prompt asks for a topic code rather than hard-coding PASS.

## Running it

```
python run_extraction.py --model anthropic/claude-opus-5-5 --handbook mto --pages 10 --prompt formal-rules
```

## Checked so far

- The prompt loads, and the example answer in `task.md` (two vocabulary entries, three rules) fits
  `schema.json` once its `...` placeholders are removed.
- Each example rule's `statement` is exactly its fields filled into the grammar.
- All seven example quotes match the MTO corpus exactly (blocks 10.14, 10.22, 8.37, 21.6, 21.7,
  6.32).
- **Not yet tried on a model.**

## Things to know

- **Changing the topic line changes the prompt hash.** Runs on different topics are recorded as
  different prompt versions. If topics will be switched often, the topic could become a
  `--topic` flag instead.
- **The six vague-word labels are new.** DISTANCE, TIME, SPEED, QUANTITY, JUDGEMENT and HEDGE were
  added for this prompt. The legacy rules only noted vague wording in free text.
- **The schema uses `$ref`.** One evidence definition is shared through `$ref`/`$defs`. Claude
  handles this. If a local vLLM model rejects it, write the definition out in both places instead.
- **This file is copied into each run folder** along with the prompt, but it isn't part of
  the prompt hash and doesn't change what the model sees.
