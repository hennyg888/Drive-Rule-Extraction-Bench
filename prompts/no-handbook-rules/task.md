Write the formal rules of the road about the topic named at the end, as they apply in the region
named at the end. The rules are to be output in JSON format.

## What counts as a rule

A rule says what a driver or other road user must, must not, should, should not or may do, and in
what situation. Include advice as well as obligations, conditions and exceptions, and rules shown
by a sign or a road marking. Include the rules that the region's traffic law and regulations set,
and the advice its official driver's handbook gives. Leave out history, statistics and
explanations of why a rule exists. Do not add rules you do not believe apply in the region, even
ones that are true elsewhere.

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
vocabulary section. Where the region's law or official handbook defines a term, use its definition.
Otherwise define the term yourself (for example PASSER, "the driver making a pass"). For every rule
that they appear in, the same key term should have the same meaning as they are defined in the
vocabulary section. Only generate self-defined key terms as necessary. Do not make up precise
definitions for terms the region's law or handbook leaves vague.

## Strength: force and modal

`force` records how strongly the region states the rule. It decides which modals the rule may use.

| force | How the region states it | modal |
| --- | --- | --- |
| REQUIREMENT | set by law or regulation: "must", "required", "not permitted", "may not", "not allowed", "unlawful", "illegal"; a regulatory sign; a penalty | MUST, MUST NOT |
| INSTRUCTION | a plain command in the official handbook that is not stated as law: "do", "don't", "never", "use", "watch", "stay" | MUST, MUST NOT |
| ADVICE | softer wording: "should", "avoid", "be careful", "it is unsafe", a description of good practice | SHOULD, SHOULD NOT |
| PERMISSION | "may", "you can"; something the law allows | MAY, MAY ONLY |

- MAY ONLY means "allowed when the condition holds, and not otherwise".
- Keep the region's strength. Do not turn advice into an obligation or an obligation into advice.
- `penalty`: only when you know the penalty the region sets for this rule (a fine, demerit points,
  suspension), in a few words. Otherwise `""`.

## Numbering

Each rule is numbered with three fields:

- `topic` (TOPIC): a 2 to 5 letter code for the topic named at the end, such as PASS for
  overtaking. It is the same for every rule.
- `group` (GROUP): a 2 to 5 letter code for a set of related rules that you choose. For
  overtaking, the groups might be GEN (general), PROC (how to pass), LOC (places where passing is
  not allowed), MARK (pavement markings), SIDE (passing on the right), USER (passing cyclists,
  buses, other users) and BEING (being passed).
- `number` (NN): two digits counting from `"01"` within each group.

`id` is these three put together, in that order, separated by `-`: TOPIC-GROUP-NN, for example
`PASS-LOC-01` for topic PASS, group LOC and number 01. List the rules group by group. Give each
rule a short `title`.

## Vague words

The driving model needs to know where the rules leave a judgement to the driver. Keep the vague
wording the region's rules use; do not make up numbers or definitions to replace it. Then list
each vague word or phrase in `vague_terms`:

- `term`: the words exactly as they appear in the statement.
- `explanation`: why the words are vague, that is what they leave open, in a few words, such as
  "no distance given".

A rule with no vague words has an empty list. Numbers the region sets (30 metres, 1 metre) are not
vague; keep their units. If a vague word is already defined in `vocabulary`, use that vocabulary
term in the rule instead of listing it here.

## Notes

Use `note` for anything a checker should know: a detail of the rule you are unsure of (a number, a
penalty, whether it is law or advice), a rule that applies only on some roads or to some vehicles
in the region, a reason the region gives, or wording that could be read two ways. Otherwise `""`.

## Examples

An abridged answer for the topic "overtaking" in Ontario, Canada: two vocabulary entries and three
rules. `...` marks entries left out. Follow its form, not its content:

```json
{"scope": "overtaking (passing another vehicle, and being passed)",
 "region": "Ontario, Canada",
 "vocabulary": [
   {"term": "PASS", "definition": "Changing lanes to move past a slower vehicle, then returning to the original lane."},
   {"term": "PASSER", "definition": "The driver making a PASS."},
   ...],
 "rules": [
   {"id": "PASS-LOC-01", "topic": "PASS", "group": "LOC", "number": "01", "title": "No passing near a pedestrian crossover",
    "force": "REQUIREMENT", "modal": "MUST NOT", "actor": "PASSER",
    "when": "within 30 metres of a PEDESTRIAN CROSSOVER", "action": "pass any vehicle", "unless": "",
    "statement": "WHEN within 30 metres of a PEDESTRIAN CROSSOVER, the PASSER MUST NOT pass any vehicle.",
    "penalty": "", "vague_terms": [],
    "note": ""},
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
    "note": ""},
   ...,
   {"id": "PASS-USER-01", "topic": "PASS", "group": "USER", "number": "01", "title": "Cyclists: one metre",
    "force": "REQUIREMENT", "modal": "MUST", "actor": "DRIVER of a motor vehicle",
    "when": "passing a CYCLIST", "action": "keep at least 1 metre between the vehicle and the CYCLIST, where practical", "unless": "",
    "statement": "WHEN passing a CYCLIST, the DRIVER of a motor vehicle MUST keep at least 1 metre between the vehicle and the CYCLIST, where practical.",
    "penalty": "A fine and two demerit points.",
    "vague_terms": [{"term": "where practical", "explanation": "does not say when 1 metre is impractical"}],
    "note": "Changing lanes to pass a cyclist whenever possible is advised as well; that is a separate ADVICE rule."},
   ...]}
```

## Answer

Answer with JSON only, in the form of the example: `scope` is the topic named at the end, `region`
is the region named at the end, `vocabulary` lists every defined term, and `rules` lists every
rule. Write out every entry; do not use `...`.

Before you answer, go through the topic again, situation by situation ({{situations}}), and
check that every rule the region has about the topic is in your list. Leaving out a rule is worse
than writing one rule twice, but do not write a rule you do not believe the region has.

Topic: {{topic}} only.
Region: {{region}}
