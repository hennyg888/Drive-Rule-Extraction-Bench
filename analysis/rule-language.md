# Rule language

The rule language for turning a driver's handbook into formal rules that still read like English. A statement is one line of fixed keywords (in capitals) around plain English. Keywords never change meaning; everything between them is ordinary text with a controlled vocabulary. The modal of each rule names its deontic modality and its strength (law or advice), and every construct has a reading in deontic logic (§9), so the rules can be checked.

The language was shaped by a census of all 3,444 sentences of the Ontario handbook (§13, `census/census-report.md`). The statements written in it are in `passing-rules/{mto,ca,tx}/rules.json`, with a readable page beside each (§11). Earlier versions of this document are in the git history.

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

`EITHER … OR` is for a duty that is a choice between actions: three Texas rules have one ("EITHER pass the other driver OR slow down", p95b, p110b, p118d).

### One rule parsed

Rule 3.4.4b:

`a driver of a motor vehicle MUST keep at least 1 m between the vehicle and a cyclist WHEN [?practical] WHILE passing the cyclist IF VIOLATED a fine AND 2 demerit points`

```
rule
  role         a driver of a motor vehicle
  modal        MUST
  choice
    action
      verb     keep
      distance at least 1 m between the vehicle and a cyclist
  clause       WHEN [?practical]
  clause       WHILE passing the cyclist
  clause       IF VIOLATED a fine AND 2 demerit points
```

| Part | Derivation |
|---|---|
| `a driver of a motor vehicle` | role |
| `MUST` | modal: obligation, strength LAW (§2) |
| `keep` | verb |
| `at least 1 m between the vehicle and a cyclist` | distance ::= comparator (`at least`) quantity (`1 m`) `between` thing `and` thing |
| `[?practical]` | condition › part › phrase, with a J flag |
| `passing the cyclist` | condition › part › phrase |
| `a fine AND 2 demerit points` | penalty, two parts joined by AND |

The statement was first written "… WHILE passing the cyclist, [?where practical] IF VIOLATED …", with the vague phrase after a comma and no keyword, so it had no place in the grammar; it is now a WHEN clause. A parser over the stored statements would list any others like it (3.4.13b has "[?if safe to do so]" inside its action).

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

| Clause | Meaning | Example |
|---|---|---|
| `WHEN <situation or event>` | When the statement applies | `WHEN the driver is within 30 m of a pedestrian crossover` |
| `WHILE <state>` | A state that lasts for the whole action | `WHILE passing the cyclist` |
| `ONLY IF <condition>` | A condition that must hold; mostly after `MAY` | `MAY drive on the right shoulder ONLY IF … the shoulder is paved` |
| `UNLESS <condition>` | An exception inside the same sentence | `MUST pass a streetcar on the right UNLESS the driver is on a one-way road` |
| `UNTIL <event or state>` | When the duty ends | `SHOULD NOT pass a smaller vehicle that is turning left ahead UNTIL it has moved to the right` |
| `BECAUSE <reason or purpose>` | Why; never changes when the rule applies | `BECAUSE passing on the right can be more dangerous` |
| `IF VIOLATED <penalty>` | Fine, demerit points, suspension, impoundment | `IF VIOLATED a fine AND 2 demerit points` |
| `AND` / `OR` / `NOT` | Connectives | |

Rules for clauses:

- A clause applies to the whole statement. Clauses come in the order of the table, each starting a new line when displayed.
- Capital `AND` / `OR` / `NOT` join conditions or actions. Lowercase "and" / "or" stay inside a noun phrase ("a bridge, viaduct or tunnel").
- `AND` binds tighter than `OR`. Use parentheses for any other grouping: `WHEN (the driver is approaching the crest of a hill OR the driver is on a curve) AND the view of oncoming traffic is obstructed`.
- A purpose is written as a reason: "so that the other lanes are clear for passing" becomes `BECAUSE this leaves the other lanes clear for passing`.
- `IF … THEN` is only for a branch inside a `PROCEDURE`. An event in a rule is `WHEN`: "If a bus pushes your trailer, do not brake" becomes `… SHOULD NOT brake … WHEN a passing bus or truck pushes the trailer out of position`.
- Order without a keyword: inside a procedure, step order carries "before" and "after". In a rule, "before X" is `WHEN about to X` and "after X" is `WHEN the driver has X-ed`.
- `UNTIL` is for a duty that ends: stop until, wait until, do not pass until. Use `UNLESS` for an exception that is not about time.

Section §9 gives each clause its logical reading.

## 4. Links between statements

| Link | Meaning |
|---|---|
| `EXCEPTION TO <id>` | Changes another statement where both apply; the more specific statement wins |
| `SPECIALIZES <id>` | A variant of another statement for a narrower situation (passing at night specializes passing) |
| `ALSO CALLED <term>` | A synonym, inside `DEFINE` |

**An exception defeats only the statement it names.** `EXCEPTION TO 3.2.3a: a driver MAY pass on the right WHEN the road is multi-lane …` lifts the advice to pass on the left; it does not lift 3.1.1a (no passing within 30 m of a pedestrian crossover), which still applies on a multi-lane road.

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
| `STRENGTH FROM` | Rules and procedures only: why the modal is law or advice (§2) |
| `TAGS` | Situation dimensions: location, road type, lane, light and weather, other road user, own vehicle, traffic control, manoeuvre phase |
| `SEE` | A diagram or sign image that goes with the statement |
| `FLAGS` | Vague or ambiguous content (§8) |

## 7. Wording

- **Roles.** Introduce with "a", refer back with "the": "a driver … the driver". Never "you". Use the most specific role the source supports: driver, driver being passed, driver towing a trailer, truck driver, cyclist.
- **One phrase per concept.** pass (not overtake), lane change, the vehicle being passed, the passing lane, the original lane, the right-hand lane, the far-left lane, the inside mirror, oncoming traffic. Where the handbook itself drifts (inside mirror / rear view mirror), the statement keeps the one phrase and gets a `V` flag.
- **Quantities.** Digits and short units: m, km, km/h, s. Fixed comparison phrases, not keywords: "at least", "at most", "more than", "less than", "within 30 m of", "between … and …". Penalties as "3 demerit points", "a fine".
- **Lists.** A sentence that introduces a list ("Bring the following:") passes its role, modal and clauses to each item; each item becomes its own statement with the same source. A definition by list is `DEFINE <term> IS <kind> THAT includes <a>, <b> or <c>`.
- **Right of way.** "yield the right-of-way to <road user>" is a verb phrase in the vocabulary, not a keyword.
- **Two statements in one sentence.** Split them, both with the same source.
- **Vague words stay as written**, wrapped in `[?…]` and flagged. Thresholds are never invented.

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

Each handbook's `rules.json` holds one object per statement, and `passing-rules/statements.schema.json` is the schema a model's output must meet:

```json
{
  "id": "3.4.4b", "section": "3.4.4", "type": "RULE", "strength": "LAW",
  "strength_from": "text (\"must maintain\")",
  "text": "a driver of a motor vehicle MUST keep at least 1 m between the vehicle and a cyclist WHEN [?practical] WHILE passing the cyclist IF VIOLATED a fine AND 2 demerit points",
  "sources": [{"id": "m56", "quote": "When passing a cyclist, drivers of motor vehicles must …", "where": "Sharing the road › Cyclists · ¶3"}],
  "flags": [{"code": "J", "span": "practical", "note": "Leaves open when the 1 m minimum can be set aside."}],
  "note": null, "links": []
}
```

`strength` is `"LAW"`, `"ADVICE"` or `null` (DEFINE, FACT and `EXCEPTION … WHEN`); `strength_from` is STRENGTH FROM. Procedures add `"steps": [{"n": "1", "text": "…", "sources": ["m9"]}]`, and statements with a figure add `"see": [{"figure": "Diagram 2-11", "source": "m59"}]`. Source ids are passage ids: m1–m96 and c1–c9 (census sentences) for Ontario, p1… for California and Texas. The action (verb, thing, modifiers) is part of `text`; there is no separate field for it yet.

## 11. Readable view

`tools/render_rules_md.py` writes a Markdown page from a statements file, in the layout of Henry's `Ontario passing rules.md`: terms first, then one table per group (ID, situation, statement, law or advice, source), the modal in bold, vague words in italics with †, the flag notes under each table, a link to the local handbook for every source, and the verbatim passages at the end. The pages are generated and never edited by hand.

| Page | From |
|---|---|
| `analysis/passing-rules/mto/passing-rules.md` | `mto/rules.json` (the 88 reviewed Ontario statements), grouped by `mto/inputs/passing-structure.json`, linked into `handbooks/mto/` |
| `analysis/passing-rules/ca/passing-rules.md` | `ca/rules.json`, grouped by handbook section, linked into `handbooks/ca/` |
| `analysis/passing-rules/tx/passing-rules.md` | `tx/rules.json`, grouped by handbook chapter, linked into `handbooks/tx/` |

The commands are in the script's docstring.

## 12. Not covered

These came up in the census and are left out because they are rare or sit outside driving behaviour (mostly licensing and penalties). Each has a workaround that keeps to the keywords.

- **Consequences with no rule broken.** Demerit-point totals ("nine points within two years"), failing a re-examination, a bounced cheque. Write them as `FACT <trigger> leads to <consequence>` for now.
- **Escalating penalties** (first, second, third occurrence within five years). Write each tier after `IF VIOLATED`; "within 5 years" is vocabulary.
- **Fallback chains** ("stop at the stop line; if there is none, at the crosswalk; if there is none, …"). Write one rule per case with `WHEN … AND there is no …`. There is no priority keyword.
- **Proportional comparisons** ("the sharper the turn, the slower you should go"). Write a `SHOULD` rule and flag the comparison `J`.
- **Duties on things or on someone other than the driver** ("courses must last 40 hours", "the owner may be charged"). The role is the responsible party: a driving school, the vehicle owner.
- **Task boundaries in the road-test chapter** ("This driving task begins when … ends when …"). These are `FACT`s about the test, not rules.

## 13. What the census added, kept and left out

The census labelled every handbook sentence against the first draft of the language (the template plan of 10 October, in the git history) and recorded what the draft could not write.

- **Added: UNTIL.** 58 instructions say a duty lasts until something happens (stop until the bus moves, wait until the fog lifts), and the first draft could not write 37 of them. Writing them as WHILE NOT turns the handbook's wording inside out, and several are safety rules.
- **Added: STRENGTH FROM (metadata).** 239 sentences, about 12% of the instructions, have unclear legal strength, mostly bare imperatives with a law behind them. Recording whether the strength came from the wording, the imperative default or the section context lets them be raised later without guessing now.
- **Added: SEE (metadata).** The handbook has 245 images and diagrams; a diagram goes with a rule but never changes when it applies, so SEE names the figure instead of being a clause.
- **Kept: All clauses and modals of the first draft.** Every one is in use: WHEN in 1,070 instructions, WHILE in 153, ONLY IF in 96, UNLESS in 46, exceptions across passages in 74, penalties in 201 sentences.
- **Kept: Imperatives default to SHOULD.** They are the most common kind of instruction (1,185, 59%); section context or an offence table can still make one law, with the reason recorded.
- **Kept: SHOULD WATCH FOR.** All 153 cautions fit it without a separate keyword.
- **Not added: BEFORE / AFTER.** 209 instructions mention order, and 174 of them were written at full fit with step order, WHEN about to …, or ONLY IF the driver has first …; only 10 asked for a keyword.
- **Not added: IF … THEN in rules.** 45 rules are worded "if … then" in the handbook, and 37 were written with WHEN at full fit, so IF … THEN stays a procedure branch.
- **Not added: SO THAT (purpose).** 257 instructions give a purpose; 248 were written at full fit with BECAUSE this … or a plain "to …", so purpose shares BECAUSE.
- **Not added: Quantities, lists, right of way.** 203 instructions carry a number and fixed phrases cover them ("at least", "within 30 m of"); 65 partial fits came from list leads ("Bring the following:"), handled as one statement per item; 44 needed "yield the right-of-way to", which is a verb phrase.
