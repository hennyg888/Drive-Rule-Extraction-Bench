# Notes on the no-image formal-rules prompt

A text-only version of `../formal-rules`. The rule grammar, numbering, force and modal,
vocabulary, vague words and `schema.json` are the same. The difference: the corpus is sent with
every image removed, and with it each `<figure>` block and its caption, so the model sees and cites
text blocks only. This file is not sent to the model.

## Files

| File | Contents |
|---|---|
| `system.md` | Background only: what the rules are for, and how the corpus HTML is laid out (table of contents, `<article data-page>`, block ids). Says that images and captions are removed, block numbers skip where they were, and the text may point to a missing image. |
| `task.md` | All the instructions, placed after the handbook pages: rule grammar, numbering, force and modal, citations (text blocks only), vocabulary, vague words, three examples, and the topic line at the end. |
| `schema.json` | Unchanged from `formal-rules`: `{scope, vocabulary, rules}`. Evidence is a list of block ids, which `grounding.py` checks. |
| `options.yaml` | `figures: false`: the runner sends the corpus with every `<figure>` removed. Not sent to the model. |

## Changes from formal-rules

- `system.md`: the figure, caption and `alt` text bullets are replaced by a note that images and
  their captions are removed and block ids have gaps; the model is told not to guess what a
  missing image shows.
- `task.md`, "What counts as a rule": rules "shown only by a sign, a road marking, a diagram" became
  rules stated in a description of a sign or marking; no details that only a missing image would
  show.
- `task.md`, "Evidence and citations": figure (`21.7`, `6.35-f1`) and caption (`21.7-c`) ids are
  gone; only text blocks are cited, and only ids that appear in the pages.
- `task.md`, "Notes": "a rule resting on a diagram alone" became "a rule whose text points to a
  missing image".
- `task.md`, example: `PASS-MARK-02` cites `["21.6"]` instead of `["21.6", "21.7"]`, and
  `PASS-USER-01`'s note mentions the missing Diagram 2-11.

## Things to know

- **The filtering:** `options.yaml` sets `figures: false`, so `--prompt no-image-rules` builds the
  messages with `messages.build(figures=False)`. That removes every `<figure>` block whole: the
  image, its `<img alt>` text and its `<figcaption>`, including `-f1` figures inside table rows and
  paragraphs (the text around them stays). Checked on all three corpora: no `<figure>`, `<img>` or
  `<figcaption>` is left, and every other word is unchanged. MTO goes from 414,664 characters and
  245 images to 360,064 characters and 0 images (167,881 to 135,442 input tokens). `meta.json`
  records `figures: false`. (`images=False` is different: it drops only the image files and keeps
  the figure markup.)
- **What is lost:** mainly the captions on MTO's `signs` page (112 of them, ~11.5K characters),
  which are the handbook's own description of what each sign means. Other MTO captions are
  "Diagram X-Y" labels; tx captions are lettering from inside the drawings; ca has none.
- **Gold sets cite figures.** Rules in a gold set that rest only on a figure or caption cannot be
  found by this prompt, and figure ids in gold evidence cannot be matched; scoring should allow
  for that.
- **The topic is a `--topic` option** (`{{topic}}` in the last line), as in `formal-rules`.
- **Not yet tried on a model.**
