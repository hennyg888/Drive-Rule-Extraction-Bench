Write the formal rules that the handbook pages above state about the topic named in the last line.
The rules are to be output in JSON format.

## What counts as a rule

A rule says what a driver or other road user must, must not, should, should not or may do, and in
what situation. Include advice as well as obligations, conditions and exceptions, and rules shown
only by a sign, a road marking, a diagram, a table or a list. Leave out text that states no rule:
introductions, history, statistics, explanations of why a rule exists, and contact details. Do not
add rules the handbook does not state, even ones that are true elsewhere.

## Rule grammar

Every rule's `statement` is one sentence in this grammar. Words in CAPITALS are terms from your 
vocabulary or predefined keywords.

```
RULE      := "WHEN" CONDITION "," "the" ACTOR MODAL ACTION ["," "UNLESS" EXCEPTION] "."
CONDITION := FACT { ("AND" | "OR") FACT }
EXCEPTION := FACT { ("AND" | "OR") FACT }
ACTOR     := a defined term for who acts, e.g. DRIVER, PASSER, CYCLIST; may be qualified:
             "DRIVER of a large truck"
MODAL     := MUST | MUST NOT | SHOULD | SHOULD NOT | MAY | MAY ONLY
```

The fields `when`, `actor`, `modal`, `action` and `unless` are the parts of `statement`: filling
them into the grammar gives the statement word for word. Use `""` for `unless` when there is no
exception.

- Write one rule per entry. Keep apart rules that apply to different situations, but do not split
  one rule into pieces. Include each rule's conditions and exceptions with it as one entry.
- Make each rule stand on its own: name the situation instead of writing "in this case" or "as
  above".

## Vocabulary

List in `vocabulary` every term written in CAPITALS in your rules (apart from the predefined
keywords WHEN, AND, OR, UNLESS and the modals), with a one-sentence definition. These are 
non-trivial key terms that must have a strict definition for the rules to be formal. 
Simple terms such as "up" or "street light" do not need to be explicitly defined in this 
vocabulary section. When the handbook defines the term, cite the block that defines it as
evidence. When you define it yourself (for example PASSER, "the driver making a pass"), leave 
`evidence` empty. For every rule that they appear in, the same key term should have 
the same meaning as they are defined in the vocabulary section. Only generate self-defined
key terms as necessary. Do not come up with unfounded definitions for terms from the handbook
that have been intentionally left vague.

## Strength: force and modal

`force` records how the handbook words the severity of the rule. It decides which modals the rule may use.

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

Each rule is numbered with three fields:

- `topic` (TOPIC): a 2 to 5 letter code for the topic in the last line, such as PASS for
  overtaking. It is the same for every rule.
- `group` (GROUP): a 2 to 5 letter code for a set of related rules that you choose. For
  overtaking, the groups might be GEN (general), PROC (how to pass), LOC (places where passing is
  not allowed), MARK (pavement markings), SIDE (passing on the right), USER (passing cyclists,
  buses, other users) and BEING (being passed).
- `number` (NN): two digits counting from `"01"` within each group.

`id` is these three put together, in that order, separated by `-`: TOPIC-GROUP-NN, for example
`PASS-LOC-01` for topic PASS, group LOC and number 01. List the rules group by group, and within a
group in the handbook's order. Give each rule a short `title`.

## Evidence and citations

A rule's `evidence` is a list of one or more block ids, such as `["21.6", "21.7"]`. A cited block
can be:

- a text block: a paragraph, list item, table row or table caption, such as `"10.22"`;
- a figure, which holds one image, such as `"21.7"`, or `"6.35-f1"` for an image inside a table
  row or paragraph (`-f2`, `-f3` for more images in the same block);
- a figure's caption, whose id is the figure's id followed by `-c`, such as `"21.7-c"`.

Cite a figure when its image supports the rule, and its caption when the caption's words are directly
relevant to the rule; cite both when both are relevant. Copy each id exactly as it appears in an `id` 
attribute.

A rule that draws on several blocks (a rule and its exception, a list and the line that introduces
it, a passage and its diagram, the same rule on two pages) lists each of them. Cite only the
materials directly relevant to the rule. Do not cite unrelated text and diagrams unless they are in
the same block as the relevant materials. 

## Vague words

The driving model needs to know where the handbook leaves a judgement to the driver. Keep the
handbook's own words in the rule; do not make up numbers or definitions to replace them. Then list
each vague word or phrase in `vague_terms`:

- `term`: the words exactly as they appear in the statement.
- `explanation`: why the words are vague, that is what they leave open, in a few words, such as
  "no distance given".

A rule with no vague words has an empty list. Numbers the handbook gives (30 metres, 1 metre) are
not vague; keep their units. If the vague term appears in the cited handbook evidence but does not
in the rule then there is no need for an entry. If a vague word from the handbook is already defined
in `vocabulary`, use that vocabulary term in the rule instead of listing it here.

## Notes

Use `note` for anything a checker should know: a rule inferred from two places, a rule resting on
a diagram alone (say what the diagram shows), a reason the handbook gives, or wording that could be
read two ways. Otherwise `""`.

## Examples

An abridged answer from the Ontario handbook, for the topic "overtaking": two vocabulary entries
(one the handbook defines, one defined for the rule set) and three rules. `...` marks entries left
out. Follow its form, not its content:

```json
{"scope": "overtaking (passing another vehicle, and being passed)",
 "vocabulary": [
   {"term": "PASS", "definition": "Changing lanes to move past a slower vehicle, then returning to the original lane.",
    "evidence": ["10.14"]},
   {"term": "PASSER", "definition": "The driver making a PASS.", "evidence": []},
   ...],
 "rules": [
   {"id": "PASS-LOC-01", "topic": "PASS", "group": "LOC", "number": "01", "title": "No passing near a pedestrian crossover",
    "force": "REQUIREMENT", "modal": "MUST NOT", "actor": "PASSER",
    "when": "within 30 metres of a PEDESTRIAN CROSSOVER", "action": "pass any vehicle", "unless": "",
    "statement": "WHEN within 30 metres of a PEDESTRIAN CROSSOVER, the PASSER MUST NOT pass any vehicle.",
    "penalty": "", "vague_terms": [],
    "note": "Stated on two pages, both times as a prohibition.",
    "evidence": ["10.22", "8.37"]},
   ...,
   {"id": "PASS-MARK-02", "topic": "PASS", "group": "MARK", "number": "02", "title": "Broken line: passing allowed",
    "force": "PERMISSION", "modal": "MAY", "actor": "PASSER",
    "when": "there is a BROKEN LINE at the left of the PASSER's lane AND the way is clear AND enough broken line remains ahead to complete the PASS",
    "action": "pass", "unless": "",
    "statement": "WHEN there is a BROKEN LINE at the left of the PASSER's lane AND the way is clear AND enough broken line remains ahead to complete the PASS, the PASSER MAY pass.",
    "penalty": "",
    "vague_terms": [
      {"term": "the way is clear", "explanation": "no gap or sight distance given"},
      {"term": "enough broken line remains ahead", "explanation": "length not given"}],
    "note": "",
    "evidence": ["21.6", "21.7"]},
   ...,
   {"id": "PASS-USER-01", "topic": "PASS", "group": "USER", "number": "01", "title": "Cyclists: one metre",
    "force": "REQUIREMENT", "modal": "MUST", "actor": "DRIVER of a motor vehicle",
    "when": "passing a CYCLIST", "action": "keep at least 1 metre between the vehicle and the CYCLIST, where practical", "unless": "",
    "statement": "WHEN passing a CYCLIST, the DRIVER of a motor vehicle MUST keep at least 1 metre between the vehicle and the CYCLIST, where practical.",
    "penalty": "A fine and two demerit points.",
    "vague_terms": [{"term": "where practical", "explanation": "does not say when 1 metre is impractical"}],
    "note": "The same block states the penalty, and advises changing lanes to pass whenever possible; that is a separate ADVICE rule.",
    "evidence": ["6.32"]},
   ...]}
```

## Answer

Answer with JSON only, in the form of the example: `scope` is the topic in the last line,
`vocabulary` lists every defined term, and `rules` lists every rule. Write out every entry; do not
use `...`.

Before you answer, go through the pages again, block by block, and check that every rule they
state about the topic is in your list. Leaving out a rule is worse than writing one rule twice.

Topic: extract formal rules about overtaking (passing another vehicle, and being passed) only.
