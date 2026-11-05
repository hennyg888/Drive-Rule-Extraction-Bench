# Notes on the formal-rules prompt

This prompt writes rules in the grammar of the legacy Ontario passing rules
(`legacy/ontario_passing_rules.yaml`), as JSON that follows `schema.json`. It is laid out as
`../Prompt_Notes.md` recommends. This file is not sent to the model.

## Files

| File | Contents |
|---|---|
| `system.md` | Background only: what the rules are for, and how the corpus HTML is laid out (table of contents, `<article data-page>`, block ids, figures). |
| `task.md` | All the instructions, placed after the handbook pages: rule grammar, numbering, force and modal, citations, vocabulary, vague words, three examples, and the topic line at the end. |
| `schema.json` | The answer: `{scope, vocabulary, rules}`. Evidence is a list of block ids (text, figure or caption blocks), which `grounding.py` checks. |

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
- Every block id cited in the example exists in the MTO corpus (10.14, 10.22, 8.37, 21.6, 21.7,
  6.32), and 21.7 is a figure.
- **Not yet tried on a model.**

## Things to know

- **Changing the topic line changes the prompt hash.** Runs on different topics are recorded as
  different prompt versions. If topics will be switched often, the topic could become a
  `--topic` flag instead.
- **Vague words** are listed per rule as `{term, explanation}`: the words as they appear in the
  statement, and why they are vague.
- **Citations are block ids only.** There are no quotes, and no image descriptions in the evidence.
  A rule resting on a diagram alone says what the diagram shows in its `note`.
- **Figures and captions have their own ids:** `21.7` is the figure and `21.7-c` its caption. An
  image inside a table row or paragraph is `6.35-f1`. See `drbench/corpus.py`.
- **This file is copied into each run folder** along with the prompt, but it isn't part of
  the prompt hash and doesn't change what the model sees.
