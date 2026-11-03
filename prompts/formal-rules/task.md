Write the formal rules that the handbook pages above state about the topic named in the last line.

## What counts as a rule

A rule says what a driver or other road user must, must not, should, should not or may do, and in
what situation. Include advice as well as obligations, conditions and exceptions, and rules shown
only by a sign, a road marking, a diagram, a table or a list. Leave out text that states no rule:
introductions, history, statistics, explanations of why a rule exists, and contact details. Do not
add rules the handbook does not state, even ones that are true elsewhere.

## Rule grammar

Every rule's `statement` is one sentence in this grammar. Words in CAPITALS are keywords or terms
from your vocabulary.

```
RULE      := "WHEN" CONDITION "," "the" ACTOR MODAL ACTION ["," "UNLESS" EXCEPTION] "."
CONDITION := FACT { ("AND" | "OR") FACT }
EXCEPTION := FACT { ("AND" | "OR") FACT }
ACTOR     := a defined term for who acts, e.g. DRIVER, PASSER, CYCLIST; may be qualified:
             "DRIVER of a large truck"
MODAL     := MUST | MUST NOT | SHOULD | SHOULD NOT | MAY | MAY ONLY
```

The fields `actor`, `when`, `action` and `unless` hold the same parts of the sentence, so the
statement can be rebuilt from them. Use `""` for `unless` when there is no exception.

- Write one rule per entry. Keep apart rules that apply to different situations, but do not split
  one rule into pieces. Leave each rule's conditions and exceptions with it.
- Make each rule stand on its own: name the situation instead of writing "in this case" or "as
  above".

## Vocabulary

List in `vocabulary` every term written in CAPITALS in your rules (apart from the keywords WHEN,
AND, OR, UNLESS and the modals), with a one-sentence definition. When the handbook defines the
term, cite that text as evidence. When you define it yourself (for example PASSER, "the driver
making a pass"), leave `evidence` empty. Use each term the same way in every rule.

## Strength: force and modal

`force` records how the handbook words the rule. It decides which modals the rule may use.

| force | Handbook wording | modal |
| --- | --- | --- |
| REQUIREMENT | "must", "required", "not permitted", "may not", "not allowed", "unlawful", "illegal"; a regulatory sign; a stated penalty | MUST, MUST NOT |
| INSTRUCTION | a plain command: "do", "don't", "never", "use", "watch", "stay" | MUST, MUST NOT |
| ADVICE | softer wording: "should", "avoid", "be careful", "it is unsafe", a description of good practice | SHOULD, SHOULD NOT |
| PERMISSION | "may", "you can" | MAY, MAY ONLY |

- MAY ONLY means "allowed when the condition holds, and not otherwise".
- Keep the handbook's strength. Do not turn advice into an obligation or an obligation into advice.
- When two passages word the same rule differently, record the stronger wording and say so in
  `note`.
- `penalty`: only when the handbook states one for this rule (a fine, demerit points,
  suspension), in a few words. Otherwise `""`.

## Numbering

- `id` is `<TOPIC>-<GROUP>-<NN>`, for example `PASS-LOC-01`.
- TOPIC is a 2 to 5 letter code for the topic in the last line, such as PASS for overtaking.
- GROUP is a 2 to 5 letter code for a set of related rules that you choose. For overtaking, the
  groups might be GEN (general), PROC (how to pass), LOC (places where passing is not allowed),
  MARK (pavement markings), SIDE (passing on the right), USER (passing cyclists, buses, other
  users) and BEING (being passed).
- NN counts from 01 within each group. List the rules group by group, and within a group in the
  handbook's order. Give each rule a short `title`.

## Evidence and citations

Every rule has one or more `evidence` entries, and each entry cites one block:

- `block`: the block id, such as `"10.22"`.
- `quote`: words copied exactly from that block, character for character: one or more whole
  sentences, or the part of a sentence that states the rule. Quotes are checked against the
  handbook automatically. For a figure, quote its caption, such as `"Diagram 3-3"`.
- `diagram`: when the block is a figure and its image supports the rule, a sentence on what the
  image shows that matters for the rule. Otherwise `""`.

A rule that draws on several blocks (a rule and its exception, a list and the line that introduces
it, a passage and its diagram, the same rule on two pages) gets one entry per block.

## Vague words

The driving model needs to know where the handbook leaves a judgement to the driver. Keep the
handbook's own words in the rule; do not make up numbers or definitions to replace them. Then list
each vague word or phrase in `vague_terms`:

- `term`: the words exactly as they appear in the statement.
- `kind`: DISTANCE ("close", "enough room"), TIME ("soon", "in time"), SPEED ("slow", "too
  fast"), QUANTITY ("heavy traffic"), JUDGEMENT ("safe", "clear", "carefully") or HEDGE ("where
  practical", "generally", "if possible").
- `note`: what is left open, in a few words, such as "no distance given".

A rule with no vague words has an empty list. Numbers the handbook gives (30 metres, 1 metre) are
not vague; keep their units.

## Notes

Use `note` for anything a checker should know: a rule inferred from two places, a rule resting on
a diagram alone, a reason the handbook gives, or wording that could be read two ways. Otherwise
`""`.

## Examples

Three rules from the Ontario handbook, for the topic "overtaking". Follow their form, not their
content:

```json
{"id": "PASS-LOC-01", "group": "LOC", "title": "No passing near a pedestrian crossover",
 "force": "REQUIREMENT", "modal": "MUST NOT", "actor": "PASSER",
 "when": "within 30 metres of a PEDESTRIAN CROSSOVER", "action": "pass any vehicle", "unless": "",
 "statement": "WHEN within 30 metres of a PEDESTRIAN CROSSOVER, the PASSER MUST NOT pass any vehicle.",
 "penalty": "", "vague_terms": [],
 "note": "Stated on two pages, both times as a prohibition.",
 "evidence": [
   {"block": "10.22", "quote": "Passing within 30 metres of a pedestrian crossover is not permitted.", "diagram": ""},
   {"block": "8.37", "quote": "You must not pass any vehicle within 30 metres of a pedestrian crossover.", "diagram": ""}]}
```

```json
{"id": "PASS-MARK-02", "group": "MARK", "title": "Broken line: passing allowed",
 "force": "PERMISSION", "modal": "MAY", "actor": "PASSER",
 "when": "there is a BROKEN LINE at the left of the PASSER's lane AND the way is clear AND enough broken line remains ahead to complete the PASS",
 "action": "pass", "unless": "",
 "statement": "WHEN there is a BROKEN LINE at the left of the PASSER's lane AND the way is clear AND enough broken line remains ahead to complete the PASS, the PASSER MAY pass.",
 "penalty": "",
 "vague_terms": [
   {"term": "the way is clear", "kind": "JUDGEMENT", "note": "no gap or sight distance given"},
   {"term": "enough broken line remains ahead", "kind": "DISTANCE", "note": "length not given"}],
 "note": "",
 "evidence": [
   {"block": "21.6", "quote": "A broken line at the left of your lane means you may pass if the way is clear.", "diagram": ""},
   {"block": "21.7", "quote": "Diagram 3-3", "diagram": "Car A behind a truck, with a broken yellow line at the left of A's lane."}]}
```

```json
{"id": "PASS-USER-01", "group": "USER", "title": "Cyclists: one metre",
 "force": "REQUIREMENT", "modal": "MUST", "actor": "DRIVER of a motor vehicle",
 "when": "passing a CYCLIST", "action": "keep at least 1 metre between the vehicle and the CYCLIST, where practical", "unless": "",
 "statement": "WHEN passing a CYCLIST, the DRIVER of a motor vehicle MUST keep at least 1 metre between the vehicle and the CYCLIST, where practical.",
 "penalty": "A fine and two demerit points.",
 "vague_terms": [{"term": "where practical", "kind": "HEDGE", "note": "does not say when 1 metre is impractical"}],
 "note": "The same block advises changing lanes to pass whenever possible; that is a separate ADVICE rule.",
 "evidence": [
   {"block": "6.32", "quote": "When passing a cyclist, drivers of motor vehicles must maintain a minimum distance of one metre, where practical between their vehicle and the cyclist.", "diagram": ""},
   {"block": "6.32", "quote": "Failure to do so may result in a fine and an additional two demerit points", "diagram": ""}]}
```

## Answer

Answer with JSON only: `{"scope": "...", "vocabulary": [...], "rules": [...]}`, where `scope` is
the topic in the last line, `vocabulary` entries are `{"term", "definition", "evidence"}`, and
`rules` entries are as in the examples.

Before you answer, go through the pages again, block by block, and check that every rule they
state about the topic is in your list. Leaving out a rule is worse than writing one rule twice.

Topic: extract formal rules about overtaking (passing another vehicle, and being passed) only.
