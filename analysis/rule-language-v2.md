# Rule language v2

The rule language for turning a driver's handbook into formal rules that still read like English. v2 keeps everything a v1 statement says and changes how the language is named and written down, after review comments on 26 October 2026:

- the modal is named by its technical term, **deontic modality**, and the field v1 called *force* is now **strength** (§2);
- the grammar is written in symbols only, its notes sit apart from it, and **action** has a real production (§1, §5);
- every construct has a reading in **deontic logic**, so the rules can be checked (§9);
- a readable page in the layout of Henry's `Ontario passing rules.md` is **generated** from the JSON (§11).

The statement types, clauses, links, wording rules and flags are those of v1 (`rule-language-v1.md`), with one addition: a choice between actions (`EITHER … OR`, §1). The census that shaped v1 (v1 §8) still holds.

**What stays at v1.** michael chose on 26 October to change the spec and add the readable view, and to keep the JSON, the prompt and the extracted statements as they are. So `passing-rules.v1.json`, `prompts/extract-rules.fixed-v1.md` and the runs in `extractions/fixed-v1/` are unchanged, and the JSON keeps the v1 field names (§10).

---

## 1. Statement types and grammar

| Type | Pattern | Use for |
|---|---|---|
| `DEFINE` | `DEFINE <term> IS <kind> THAT <difference> [ALSO CALLED <term>]` | A term and what it means |
| `FACT` | `FACT <sentence>` | Background with no instruction |
| `RULE` | `<role> <MODAL> <action> [clauses]` | Obligations, prohibitions, permissions, advice, cautions |
| `PROCEDURE` | `TO <goal> [SPECIALIZES <id>] [WHEN …]`, then `STEP n <action> [clauses]` lines, optional `DONE WHEN <state>`, optional `IF <event> THEN <action>` | Ordered steps |
| `EXCEPTION` | `EXCEPTION TO <id>: <rule>` or `EXCEPTION TO <id> WHEN <condition>` | A change to a statement written in another passage |

### Grammar

```
statement  ::= rule | define | fact | procedure | exception
rule       ::= role modal choice { AND [ modal ] choice } { clause }
choice     ::= action | EITHER action OR action { OR action }
modal      ::= MUST | MUST NOT | MAY | SHOULD | SHOULD NOT
action     ::= verb [ thing ] { modifier } | WATCH FOR hazard
modifier   ::= side | distance | place | manner | speed
side       ::= "on the left" | "on the right"
distance   ::= comparator quantity [ "from" thing | "between" thing "and" thing ]
place      ::= ( "into" | "onto" | "in" | "out of" | "behind" | "ahead of" ) thing
manner     ::= "with" phrase | adverb
speed      ::= [ comparator ] quantity [ ( "below" | "above" ) thing ]
comparator ::= "at least" | "at most" | "within" | "more than" | "less than"
quantity   ::= number unit
clause     ::= WHEN condition | WHILE condition | ONLY IF condition
             | UNLESS condition | UNTIL condition
             | BECAUSE reason | IF VIOLATED penalty
condition  ::= all-of { OR all-of }
all-of     ::= part { AND part }
part       ::= [ NOT ] ( phrase | "(" condition ")" )
define     ::= DEFINE term IS kind THAT difference [ ALSO CALLED term ]
fact       ::= FACT sentence { clause }
procedure  ::= TO goal [ SPECIALIZES id ] [ WHEN condition ]
               step { step } [ DONE WHEN state ]
               { IF event THEN action { AND action } }
step       ::= STEP number action { AND action } { clause }
exception  ::= EXCEPTION TO id ( ":" rule | WHEN condition )
```

### Notes on the grammar

Capitals are keywords, quoted words are fixed words, and other lowercase names are symbols. `{ }` repeats, `[ ]` is optional, `|` separates choices and `( )` groups. `AND` binds tighter than `OR`.

| Symbol | What it is | Closed list |
|---|---|---|
| role | Who the statement binds: a driver, a driver being passed, a driver towing a trailer, a truck driver, a cyclist | Yes (§7) |
| verb | The verb that opens an action | Yes (§5) |
| thing, hazard, term, kind | A noun phrase in the one-phrase vocabulary: the passing lane, the vehicle being passed | Yes, grows with each topic (§7) |
| unit | m, km, km/h, s; mph and ft for Texas | Yes |
| adverb | How an action is done: gradually, … | Yes |
| number, id | Digits; a statement id such as `3.4.4b` | Format only |
| phrase, reason, penalty, sentence, goal, state, event, difference | Plain English written by the wording rules (§7) | No: the only free text |

Any phrase or value can be wrapped in `[?…]` and flagged J, S, R or G (§8).

`EITHER … OR` is new in v2. The Texas run has three rules whose duty is a choice ("either pass the other driver or slow down", p95b, p110b, p118d), stored in lowercase because v1 could join actions only with AND.

### One rule parsed

Rule 3.4.4b, written in v2:

`a driver of a motor vehicle MUST keep at least 1 m between the vehicle and a cyclist WHEN [?it is practical] WHILE passing the cyclist IF VIOLATED a fine AND 2 demerit points`

```
rule
  role         a driver of a motor vehicle
  modal        MUST
  choice
    action
      verb     keep
      distance at least 1 m between the vehicle and a cyclist
  clause       WHEN [?it is practical]
  clause       WHILE passing the cyclist
  clause       IF VIOLATED a fine AND 2 demerit points
```

| Part | Derivation |
|---|---|
| `a driver of a motor vehicle` | role |
| `MUST` | modal: obligation, strength LAW (§2) |
| `keep` | verb |
| `at least 1 m between the vehicle and a cyclist` | distance ::= comparator (`at least`) quantity (`1 m`) `between` thing `and` thing |
| `[?it is practical]` | condition › part › phrase, with a J flag |
| `passing the cyclist` | condition › part › phrase |
| `a fine AND 2 demerit points` | penalty, two parts joined by AND |

In `passing-rules.v1.json` the same statement reads "… WHILE passing the cyclist, [?where practical] IF VIOLATED …": the vague phrase follows a comma with no keyword, so it has no place in the grammar. v2 writes it as a WHEN clause. The stored text is left as it is (the JSON stays at v1); a parser over the stored statements would list every statement like it.

## 2. Deontic modality and strength

Each modal keyword names two things. Its **deontic modality** says what the statement does: oblige, prohibit or permit. Its **strength** says whether the law stands behind it.

| Modality | Strength LAW | Strength ADVICE |
|---|---|---|
| Obligation | `MUST` | `SHOULD` |
| Prohibition | `MUST NOT` | `SHOULD NOT` |
| Permission | `MAY` | none: advice never grants a permission |

"Strength" here is not the strong and weak permission of deontic logic (a permission stated outright, or an action that is merely not forbidden); that distinction is what the `D` flag records (§8).

A caution is a rule: `<role> SHOULD WATCH FOR <hazard> [clauses]`. When the handbook says "be careful" without naming a hazard, write `SHOULD <action> with [?extra care]` and flag it.

**Choosing the modal.** Take the first line that applies:

1. **Legal wording** gives `MUST` / `MUST NOT`: must, must not, required, is not permitted, not allowed, illegal, unlawful, prohibited, offence, by law.
2. **Permission wording** gives `MAY`: may, can, allowed, permitted, but only when it grants permission. "May" as possibility ("may want to", "may help") is not a permission; write a `FACT` or a note.
3. **Section context** can give law to the statements under it, when the section says so (the Regulatory signs section: "These signs give a direction that must be obeyed"). A behaviour listed in an offence or sanctions table counts the same way.
4. **Advice wording** gives `SHOULD` / `SHOULD NOT`: should, it is important to, try to, avoid.
5. **Bare imperatives** (do, don't, never, always, be sure) give `SHOULD` / `SHOULD NOT`.
6. **Cautions** (watch for, look out for, be prepared, be alert) give `SHOULD WATCH FOR` when a hazard is named.

When the wording and the default disagree in spirit, keep the default and add an `M` flag. Never raise strength by guessing.

Every rule records why it got its strength in `STRENGTH FROM`: wording, imperative default, caution default, section context, or implied.

## 3. Clauses

As in v1 §3: `WHEN`, `WHILE`, `ONLY IF`, `UNLESS`, `UNTIL`, `BECAUSE`, `IF VIOLATED`, in that order, each applying to the whole statement; capital `AND` / `OR` / `NOT` join conditions, and lowercase "and" / "or" stay inside a noun phrase. `IF … THEN` is only a procedure branch; an event in a rule is `WHEN`. A purpose is a `BECAUSE`. Section §9 gives each clause its logical reading.

## 4. Links between statements

| Link | Meaning |
|---|---|
| `EXCEPTION TO <id>` | Changes another statement where both apply; the more specific statement wins |
| `SPECIALIZES <id>` | A variant of another statement for a narrower situation (passing at night specializes passing) |
| `ALSO CALLED <term>` | A synonym, inside `DEFINE` |

New in v2: **an exception defeats only the statement it names.** `EXCEPTION TO 3.2.3a: a driver MAY pass on the right WHEN the road is multi-lane …` lifts the advice to pass on the left; it does not lift 3.1.1a (no passing within 30 m of a pedestrian crossover), which still applies on a multi-lane road.

## 5. Actions

An action is a verb from the list below, an optional thing, and typed modifiers (grammar in §1). The list is taken from the verbs that open the actions and procedure steps in the Ontario reference and in the California and Texas runs of 23 October; a new verb is added when a reviewer accepts it.

| Kind | Verbs |
|---|---|
| Moving | pass, change lanes, move, merge, cut in, cut back, return to, pull out, cross, drive, ride, travel, steer, go, proceed, approach, follow, stay, remain, keep, leave, take, give, vacate, wait, stop, start |
| Speed | slow down, speed up, brake, tap, maintain |
| Signals and lights | signal, use, sound the horn, switch |
| Attention | look, check, judge, make certain, anticipate, `WATCH FOR`, be ready to, be prepared to |
| Right of way | yield the right-of-way to, allow, let |
| Other | attempt, try |

| Modifier | Form | Example |
|---|---|---|
| side | on the left, on the right | 3.2.3b: pass `on the right` |
| distance | comparator, quantity, from or between things | 3.4.4b: `at least 1 m between the vehicle and a cyclist` |
| place | into, onto, in, out of, behind, ahead of a thing | 3.4.13b: move `into a lane away from the stopped emergency vehicle` |
| manner | with a phrase, or an adverb | 3.4.13a: proceed `with [?caution]` |
| speed | a speed or a change of speed | Texas p102a: `20 mph below the speed limit` |

A verb of attention may take a clause ("judge whether there is [?enough] space to pass"). "be" with a state that is a judgment ("be patient") is flagged J.

The modifiers are what let a checker see that "pass on the right" is a kind of "pass", so a ban on passing also bans passing on the right (§9).

## 6. Metadata

| Field | Content |
|---|---|
| `ID` | Section number plus a letter, following the topic's structure (`3.4.4b`); for handbooks without a topic structure, the passage id plus a letter (`p63a`) |
| `SOURCE` | The verbatim handbook sentence(s) and where they are |
| `STRENGTH FROM` | Rules and procedures only: why the modal is law or advice (§2). Called FORCE FROM in v1 |
| `TAGS` | Situation dimensions: location, road type, lane, light and weather, other road user, own vehicle, traffic control, manoeuvre phase |
| `SEE` | A diagram or sign image that goes with the statement |
| `FLAGS` | Vague or ambiguous content (§8) |

## 7. Wording

As in v1 §6. Roles are introduced with "a" and referred back to with "the", never "you", and are as specific as the source allows. One phrase per concept: pass (not overtake), lane change, the vehicle being passed, the passing lane, the original lane, the right-hand lane, the far-left lane, the inside mirror, oncoming traffic. Quantities in digits with short units. A list lead passes its role, modal and clauses to each item. Two statements in one sentence are split. Vague words stay as written, in `[?…]`, and thresholds are never invented.

## 8. Flags

| Code | Meaning | Where it shows |
|---|---|---|
| `J` | Judgment term: safe, enough, sure, reasonable, as soon as you can | Inline `[?…]` |
| `S` | Hedged scope: usually, often, many, most | Inline |
| `R` | Unclear reference or role: "these areas", "the smaller vehicle" | Inline |
| `G` | Goal and means differ: the rule bans crossing the centreline, not passing as such | Inline |
| `M` | Unclear legal strength | On the statement |
| `D` | Implicit default: a permission that presupposes an unstated prohibition | On the statement |
| `V` | Wording drift across passages: inside mirror / rear-view mirror | On the statement |
| `X` | Stated again elsewhere, possibly differently | On the statement |

## 9. Reading in deontic logic

`MUST`, `MUST NOT` and `MAY` map onto the three operators of standard deontic logic (SDL): O (obligation), F (prohibition) and P (permission). The clauses need the usual extensions of SDL. φ is the action, c the condition.

| Construct | Reading | Logic needed |
|---|---|---|
| `MUST φ` | O φ | SDL |
| `MUST NOT φ` | O ¬φ, also written F φ | SDL |
| `MAY φ` | P φ, which is ¬O ¬φ | SDL |
| `SHOULD φ`, `SHOULD NOT φ` | Oₐ φ, Oₐ ¬φ: a second operator for advice, kept apart from O | SDL axioms for each operator |
| `EITHER φ OR ψ` | O(φ ∨ ψ) | SDL |
| `WHEN c` | O(φ / c): φ is obligatory given c | Dyadic (conditional) deontic logic |
| `UNLESS e` | O(φ / c ∧ ¬e) | Dyadic |
| `MAY φ ONLY IF c` | P(φ / c) and O(¬φ / ¬c) | Dyadic |
| `WHILE s` | φ holds at every moment that s holds | Temporal deontic logic |
| `UNTIL e` | O(φ U e): φ holds until e happens | Temporal (the "until" of linear temporal logic) |
| `IF VIOLATED p` | ¬φ ∧ c leads to p | Anderson's reduction, O φ ≡ □(¬φ → S), with the penalty p as the sanction S |
| `EXCEPTION TO r` | The exception defeats r where both apply (§4) | Defeasible deontic logic |
| `PROCEDURE`, `STEP` | O(α₁ ; α₂ ; … / goal): a sequence of actions | Dynamic deontic logic |
| `DEFINE` | term ≡ kind ∧ difference | A definition, not a norm |
| `FACT`, `BECAUSE` | A proposition with no operator; no logical content | None |

Rule 3.4.4b, with d the driver and c the cyclist:

```
O( keep(d, c, ≥ 1 m) / passing(d, c) ∧ practical )
¬keep(d, c, ≥ 1 m) ∧ passing(d, c)  →  fine ∧ demerits(2)
```

**What can be checked.**

1. **Conflicts.** Two LAW statements whose conditions can hold together, with O φ against O ¬φ, or P φ against F φ, and no `EXCEPTION TO` between them.
2. **Advice against law.** Oₐ φ where the law says O ¬φ.
3. **A scene.** Given the conditions true in a driving scene, list the duties in force and check the action taken against them (the use in `analysis/vla/`).
4. **Handbooks against each other.** The same action with a different modality in Ontario, California and Texas.

**The limit.** Conditions and actions are still English phrases, and a checker needs named predicates. The verb list and the modifiers (§5) name the actions; conditions would need a closed list too, starting from the TAGS dimensions. Until then a person or a model matches the phrases.

## 10. Machine-readable form

The JSON is unchanged from v1 (`rule-language-v1.md` §10, `analysis/passing-rules/statements.schema.json`). Its field names keep the v1 terms until the next prompt version:

| v2 term | JSON field and values |
|---|---|
| strength LAW, ADVICE | `force`: `"LEGAL"`, `"ADVISORY"` |
| STRENGTH FROM | `force_from` |
| action (verb, thing, modifiers) | Part of `text`; no separate field |

A future version that renames these fields or adds an `action` or `title` field needs a new prompt version (fixed-v2) and a new run.

## 11. Readable view

`tools/render_rules_md.py` writes a Markdown page from a statements file, in the layout of Henry's `Ontario passing rules.md`: terms first, then one table per group (ID, situation, statement, law or advice, source), the modal in bold, vague words in italics with †, the flag notes under each table, a link to the local handbook for every source, and the verbatim passages at the end. The pages are generated and never edited by hand.

| Page | From |
|---|---|
| `analysis/passing-rules/passing-rules.v1.md` | `passing-rules.v1.json` (the 88 Ontario statements), grouped by `inputs/passing-structure.json`, linked into `handbooks/mto/` |
| `extractions/fixed-v1/california/output.md` | That run's `output.json`, grouped by handbook section, linked into `handbooks/ca/` |
| `extractions/fixed-v1/texas/output.md` | That run's `output.json`, grouped by handbook chapter, linked into `handbooks/tx/` |

The commands are in the script's docstring.

## 12. Not covered in v2

As in v1 §9: consequences with no rule broken, escalating penalties, fallback chains, proportional comparisons, duties on someone other than the driver, and task boundaries in the road-test chapter, each with the v1 workaround.
