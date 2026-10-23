# Rule language v1

The rule language for turning the MTO Driver's Handbook into formal rules that still read like English. v1 replaces the draft v0 in `rule-template-plan.md`; every change was checked against a census of all 3,444 handbook sentences (`census/census-report.md`). The passing rules written in v1 are in `passing-rules/passing-rules.v1.json` and on the side-by-side page.

A statement is one line of fixed keywords (in capitals) around plain English. Keywords never change meaning; everything between them is ordinary text with a controlled vocabulary.

---

## 1. Statement types

| Type | Pattern | Use for |
|---|---|---|
| `DEFINE` | `DEFINE <term> IS <kind> THAT <difference> [ALSO CALLED <alias>]` | A term and what it means |
| `FACT` | `FACT <sentence>` | Background with no instruction: how things work, what a sign shows, what tends to happen |
| `RULE` | `<role> <MODAL> <action> [clauses]` | Obligations, prohibitions, permissions, advice, cautions |
| `PROCEDURE` | `TO <goal> [SPECIALIZES <id>] [WHEN …]` then `STEP n <action> [clauses]` lines, optional `DONE WHEN <state>`, optional `IF <event> THEN <action>` | Ordered steps |

An exception written in a different passage from the rule it changes is its own statement:

- `EXCEPTION TO <id>: <role> <MODAL> <action> [clauses]`, when the exception is a rule of its own (a driver MAY pass on the right when …);
- `EXCEPTION TO <id> WHEN <condition>`, when it only switches the other rule off.

```
DEFINE passing IS a lane change THAT moves past a slower vehicle ALSO CALLED overtaking
FACT a large vehicle can create heavy air turbulence that may affect the driver's control WHILE passing it
a driver MUST NOT pass a vehicle WHEN the driver is within 30 m of a pedestrian crossover
TO pass a vehicle
  STEP 1 signal left AND check that the way is clear ahead and behind
  STEP 2 move into the passing lane
  …
  IF the vehicle being passed speeds up THEN do not race AND go back to the original lane
EXCEPTION TO 3.2.3a: a driver MAY pass on the right WHEN the road is multi-lane OR the road is one-way OR …
```

### Grammar

Capitals are keywords; lowercase names on the right that are not defined here (role, verb-phrase, hazard, phrase, reason, penalty, term, kind, difference, alias, sentence, goal, state, event, id, n) are plain English written by the wording rules in §6; `AND`, `OR` and `NOT` can also join phrases inside them (`IF VIOLATED a fine AND 2 demerit points`). `{ }` repeats, `[ ]` is optional, `|` means or.

```
statement ::= rule | define | fact | procedure | exception
rule      ::= role modal action { AND [ modal ] action } { clause }
modal     ::= MUST | MUST NOT | MAY | SHOULD | SHOULD NOT
action    ::= verb-phrase | WATCH FOR hazard
clause    ::= WHEN condition | WHILE condition | ONLY IF condition
            | UNLESS condition | UNTIL condition
            | BECAUSE reason | IF VIOLATED penalty
condition ::= all-of { OR all-of }
all-of    ::= part { AND part }
part      ::= [ NOT ] ( phrase | "(" condition ")" )
define    ::= DEFINE term IS kind THAT difference [ ALSO CALLED alias ]
fact      ::= FACT sentence { clause }
procedure ::= TO goal [ SPECIALIZES id ] [ WHEN condition ]
              step { step } [ DONE WHEN state ] { IF event THEN action { AND action } }
step      ::= STEP n action { AND action } { clause }
exception ::= EXCEPTION TO id ( ":" rule | WHEN condition )
```

## 2. Modals and legal force

| Modal | Meaning | Force |
|---|---|---|
| `MUST` | Obligation | Law |
| `MUST NOT` | Prohibition | Law |
| `MAY` | Permission | Law |
| `SHOULD` | Advice | Advice |
| `SHOULD NOT` | Advice against | Advice |

A caution is a rule: `<role> SHOULD WATCH FOR <hazard> [clauses]`. When the handbook says "be careful" without naming a hazard, write `SHOULD <action> with [?extra care]` and flag it.

**Choosing the modal.** Take the first line that applies:

1. **Legal wording** gives `MUST` / `MUST NOT`: must, must not, required, is not permitted, not allowed, illegal, unlawful, prohibited, offence, by law.
2. **Permission wording** gives `MAY`: may, can, allowed, permitted, but only when it grants permission. "May" as possibility ("may want to", "may help", "may be") is not a permission; write a `FACT` or a note.
3. **Section context** can give law to the statements under it, when the section says so. Example: the Regulatory signs section opens with "These signs give a direction that must be obeyed", so a sign's plain caption becomes `MUST` / `MUST NOT`. A behaviour listed in an offence or sanctions table counts the same way.
4. **Advice wording** gives `SHOULD` / `SHOULD NOT`: should, it is important to, try to, avoid.
5. **Bare imperatives** (do, don't, never, always, be sure) give `SHOULD` / `SHOULD NOT`.
6. **Cautions** (watch for, look out for, be prepared, be alert) give `SHOULD WATCH FOR` when a hazard is named.

When the wording and the default disagree in spirit (an absolute "under any conditions" with no legal marker, a test question that says "must"), keep the default and add an `M` flag. Never raise force by guessing.

Every rule records why it got its force in `FORCE FROM`: wording, imperative default, caution default, section context, or implied.

## 3. Clauses

| Clause | Meaning | Example |
|---|---|---|
| `WHEN <situation or event>` | When the statement applies | `WHEN the driver is within 30 m of a pedestrian crossover` |
| `WHILE <state>` | A state that lasts for the whole action | `WHILE passing the cyclist` |
| `ONLY IF <condition>` | A condition that must hold; mostly after `MAY` | `MAY drive on the right shoulder ONLY IF … the shoulder is paved` |
| `UNLESS <condition>` | An exception inside the same sentence | `MUST pass a streetcar on the right UNLESS the driver is on a one-way road` |
| `UNTIL <event or state>` | When the duty ends (new in v1) | `SHOULD NOT pass a smaller vehicle that is turning left ahead UNTIL it has moved to the right` |
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

## 4. Links between statements

| Link | Meaning |
|---|---|
| `EXCEPTION TO <id>` | Changes another statement; the more specific statement wins |
| `SPECIALIZES <id>` | A variant of another statement for a narrower situation (passing at night specializes passing) |
| `ALSO CALLED <alias>` | A synonym, inside `DEFINE` |

## 5. Metadata

Every statement carries:

| Field | Content |
|---|---|
| `ID` | Section number plus a letter, following the topic's structure (`3.4.4b`) |
| `SOURCE` | The verbatim handbook sentence(s) and where they are (page › section › paragraph) |
| `FORCE FROM` | Rules only: why the modal is law or advice (see §2) |
| `TAGS` | Situation dimensions: location, road type, lane, light and weather, other road user, own vehicle, traffic control, manoeuvre phase |
| `SEE` | A diagram or sign image that goes with the statement |
| `FLAGS` | Vague or ambiguous content (see §7) |

## 6. Wording

- **Roles.** Introduce with "a", refer back with "the": "a driver … the driver". Never "you". Use the most specific role the source supports: driver, driver being passed, driver towing a trailer, truck driver, cyclist.
- **One phrase per concept.** pass (not overtake), lane change, the vehicle being passed, the passing lane, the original lane, the right-hand lane, the far-left lane, the inside mirror, oncoming traffic. Where the handbook itself drifts (inside mirror / rear view mirror), the statement keeps the one phrase and gets a `V` flag.
- **Quantities.** Digits and short units: m, km, km/h, s. Fixed comparison phrases, not keywords: "at least", "at most", "more than", "less than", "within 30 m of", "between … and …". Penalties as "3 demerit points", "a fine".
- **Lists.** A sentence that introduces a list ("Bring the following:") passes its role, modal and clauses to each item; each item becomes its own statement with the same source. A definition by list is `DEFINE <term> IS <kind> THAT includes <a>, <b> or <c>`.
- **Right of way.** "yield the right-of-way to <road user>" is a verb phrase in the vocabulary, not a keyword.
- **Two statements in one sentence.** Split them, both with the same source.
- **Vague words stay as written**, wrapped in `[?…]` and flagged. Thresholds are never invented.

## 7. Flags

| Code | Meaning | Where it shows |
|---|---|---|
| `J` | Judgment term: safe, enough, sure, reasonable, as soon as you can | Inline `[?…]` |
| `S` | Hedged scope: usually, often, many, most | Inline |
| `R` | Unclear reference or role: "these areas", "the smaller vehicle" | Inline |
| `G` | Goal and means differ: the rule bans crossing the centreline, not passing as such | Inline |
| `M` | Unclear legal force | On the statement |
| `D` | Implicit default: a permission that presupposes an unstated prohibition | On the statement |
| `V` | Wording drift across passages: inside mirror / rear-view mirror | On the statement |
| `X` | Stated again elsewhere, possibly differently | On the statement |

## 8. What the census added, kept and left out

- **Added: UNTIL.** 58 instructions say a duty lasts until something happens (stop until the bus moves, wait until the fog lifts), and v0 could not write 37 of them. Writing them as WHILE NOT turns the handbook's wording inside out, and several are safety rules.
- **Added: FORCE FROM (metadata).** 239 sentences, about 12% of the instructions, have unclear legal force, mostly bare imperatives with a law behind them. Recording whether the force came from the wording, the imperative default or the section context lets them be raised later without guessing now.
- **Added: SEE (metadata).** The handbook has 245 images and diagrams; a diagram goes with a rule but never changes when it applies, so SEE names the figure instead of being a clause.
- **Kept: All v0 clauses and modals.** Every v0 clause is in use: WHEN in 1,070 instructions, WHILE in 153, ONLY IF in 96, UNLESS in 46, exceptions across passages in 74, penalties in 201 sentences.
- **Kept: Imperatives default to SHOULD.** They are the most common kind of instruction (1,185, 59%); section context or an offence table can still make one law, with the reason recorded.
- **Kept: SHOULD WATCH FOR.** All 153 cautions fit it without a separate keyword.
- **Not added: BEFORE / AFTER.** 209 instructions mention order, and 174 of them were written at full fit with step order, WHEN about to …, or ONLY IF the driver has first …; only 10 asked for a keyword.
- **Not added: IF … THEN in rules.** 45 rules are worded "if … then" in the handbook, and 37 were written with WHEN at full fit, so IF … THEN stays a procedure branch.
- **Not added: SO THAT (purpose).** 257 instructions give a purpose; 248 were written at full fit with BECAUSE this … or a plain "to …", so purpose shares BECAUSE.
- **Not added: Quantities, lists, right of way.** 203 instructions carry a number and fixed phrases cover them ("at least", "within 30 m of"); 65 partial fits came from list leads ("Bring the following:"), handled as one statement per item; 44 needed "yield the right-of-way to", which is a verb phrase.

## 9. Not covered in v1

These came up in the census and are left out of v1 because they are rare or sit outside driving behaviour (mostly licensing and penalties). Each has a workaround that keeps to the v1 keywords.

- **Consequences with no rule broken.** Demerit-point totals ("nine points within two years"), failing a re-examination, a bounced cheque. Write them as `FACT <trigger> leads to <consequence>` for now.
- **Escalating penalties** (first, second, third occurrence within five years). Write each tier after `IF VIOLATED`; "within 5 years" is vocabulary.
- **Fallback chains** ("stop at the stop line; if there is none, at the crosswalk; if there is none, …"). Write one rule per case with `WHEN … AND there is no …`. There is no priority keyword.
- **Proportional comparisons** ("the sharper the turn, the slower you should go"). Write a `SHOULD` rule and flag the comparison `J`.
- **Duties on things or on someone other than the driver** ("courses must last 40 hours", "the owner may be charged"). The role is the responsible party: a driving school, the vehicle owner.
- **Task boundaries in the road-test chapter** ("This driving task begins when … ends when …"). These are `FACT`s about the test, not rules.

## 10. Machine-readable form

`passing-rules.v1.json` holds one object per statement:

```json
{
  "id": "3.4.4b", "section": "3.4.4", "type": "RULE", "force": "LEGAL",
  "force_from": "text (\"must maintain\")",
  "text": "a driver of a motor vehicle MUST keep at least 1 m between the vehicle and a cyclist WHILE passing the cyclist, [?where practical] IF VIOLATED a fine AND 2 demerit points",
  "sources": [{"id": "m56", "quote": "When passing a cyclist, drivers of motor vehicles must …", "where": "Sharing the road › Cyclists · ¶3"}],
  "flags": [{"code": "J", "span": "where practical", "note": "Leaves open when the 1 m minimum can be set aside."}],
  "note": null, "links": []
}
```

Procedures add `"steps": [{"n": "1", "text": "…", "sources": ["m9"]}]`, and statements with a figure add `"see": [{"figure": "Diagram 2-11", "source": "m59"}]`. Source ids are the passage ids from the Passing Topic Comparison page (m1–m96). c1–c9 are the sentences added from the census; they also carry their `census_id`. A figure source also carries its `image`.
