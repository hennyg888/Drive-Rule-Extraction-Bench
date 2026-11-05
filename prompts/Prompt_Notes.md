# Prompt notes

How Anthropic recommends laying out prompts for Claude, and what to watch for when editing the
prompts in this folder. Checked against the Claude API guidance in November 2026, for the current
models (Opus 5.5, Sonnet 5.5, Haiku 5.5).

## System prompt vs. user message

- **System prompt (`system.md`):** sets the role and background: who the model is working for,
  why the task exists, what the input looks like. Claude reads it before anything else and gives
  it somewhat more authority than the user turn.
- **User message:** carries the material and the task. Anthropic suggests putting task-specific
  instructions here, not in the system prompt.
- **A filler system prompt** such as "You are a helpful assistant" adds nothing. Leave
  `system.md` empty instead: the loader then sends no system prompt at all.
- **Other models:** OpenRouter and vLLM send `system.md` as a `{"role": "system"}` message. Most
  models accept it, but a few have no system role. Putting everything in the user message works
  the same on every model.

## Long documents: material first, request last

- Put the long material (the handbook pages) at the top of the user message, and the question or
  instructions after it. Anthropic reports that this order noticeably improves answers on long
  inputs.
- `messages.build()` already does this: table of contents, then the pages, then `task.md` as the
  last text.
- Instructions the model should act on at the end, such as the "go through the pages again"
  check, work better in `task.md` (after the pages) than in `system.md`, which the model reads
  hundreds of thousands of tokens earlier.
- Put each image next to the text it belongs to, not in a pile at the start or end.
  `to_parts()` places each image right after its `<img>` tag.

## Assistant messages (prefill)

- **Prefill is not supported.** On current models (Opus 5.5, Sonnet 5.5, Haiku 5.5 and the 4.6+
  family), a request ending with a partial assistant message (e.g. `{"role": "assistant",
  "content": "{"}` to force JSON) returns a 400.
- To control the output format, use structured outputs (`schema.json`, sent as
  `output_config.format`) or ask for the format in the prompt.
- These runs send a single user turn, so there is no assistant message at all.

## Structured output (`schema.json`)

- **Claude** enforces the schema (`output_config.format`). The schema needs `required` and
  `"additionalProperties": false` on every object, as `formal-rules/schema.json` already has.
- **vLLM** enforces it through `response_format`. Other OpenRouter models may only treat it as a
  request, so keep the JSON shape in `task.md` too.
- **Citations:** structured outputs cannot be combined with Claude's built-in document citations
  (that returns a 400). This is one reason the repo asks for `{"block", "quote"}` evidence in the
  JSON instead.

## Thinking and effort

- **Thinking can't be turned off on Opus 5.5.** `{"type": "disabled"}` and `budget_tokens` both
  return a 400. Opus 5.5 and Haiku 5.5 always use adaptive thinking, and Sonnet 5.5 uses it by
  default.
- **Effort is the main control** (`output_config.effort`: low, medium, high, xhigh, max).
  **Opus 5.5 and Haiku 5.5 default to `medium`**, so set it explicitly. The presets in
  `models.yaml` do (`effort: high` for Opus and Sonnet).
- **Fewer rules:** prompts written for older models are often too prescriptive for current ones.
  Long lists of "always / never / IMPORTANT" rules can lower quality. Explain the goal and the
  reason (as the "Why" section does) rather than adding more rules.
- **Thinking text:** it is only returned when `display: "summarized"` is set, which `claude.py`
  does. Without it, thinking blocks come back empty but are still billed.

## Prompt caching

- **Caching matches the start of the request.** The cache works on the request read in order
  `tools`, `system`, `messages`. Any change to an earlier byte invalidates everything after it.
- **Keep the stable parts stable.** `system.md`, the table of contents and the page HTML must be
  byte-identical between runs to be read from the cache. Never put dates, run ids or random order
  into them.
- **Short prompts don't cache.** There is a minimum length (512 to 4096 tokens depending on the
  model). Below it, nothing is cached and no error is raised.
- **Check it worked:** `usage.cache_read_input_tokens` in `response.json` should be above zero
  on the second run over the same pages. The `cache: true` param turns caching on.
- **Changing the prompt starts over.** Any edit to `system.md` changes the cached part, so the
  next run pays the cache-writing price (1.25 times) once.

## Comparing prompt versions

- To test a different wording, copy the folder (e.g. `prompts/formal-rules-v2/`), edit it, and
  run it with `--prompt formal-rules-v2`. Each run saves a copy of the prompt folder and
  `prompt_sha256` in `meta.json`, so results from different versions stay apart.
- Change one thing at a time, and run each version on the same pages and model.
