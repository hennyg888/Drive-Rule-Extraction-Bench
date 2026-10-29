# Task: turn driver's handbook passages into rule language v1

You rewrite passages from a driver's handbook as statements in **rule language v1**, a controlled English with fixed keywords. Each statement says exactly one thing. It makes explicit what the handbook leaves implicit: who must act, whether it is law or advice, when it applies, and which words are vague. Every statement keeps the handbook sentences it came from.

You receive one batch of passages from one handbook. Each passage has an id (such as `m17`), the page it is on, its heading path (`Stopping at railway crossings · item 2` means the second list item under the heading "Stopping at railway crossings"; `A › B` means heading B under heading A), its kind (`para` or `text`, `item` for a bullet, `step` for a numbered step, `figure`, `table`), and its text. A figure gives its caption and alt text instead of sentences.

You return one JSON object, `{"statements": [...]}`, and nothing else.

Part A is the rule language. Part B is the method: follow its steps in order. Part C is the topic. Part D is the output format. Part E has worked examples. Part F is the check to run before you answer.

---

# Part A. Rule language v1

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

## 9. Not covered in v1

These came up in the census and are left out of v1 because they are rare or sit outside driving behaviour (mostly licensing and penalties). Each has a workaround that keeps to the v1 keywords.

- **Consequences with no rule broken.** Demerit-point totals ("nine points within two years"), failing a re-examination, a bounced cheque. Write them as `FACT <trigger> leads to <consequence>` for now.
- **Escalating penalties** (first, second, third occurrence within five years). Write each tier after `IF VIOLATED`; "within 5 years" is vocabulary.
- **Fallback chains** ("stop at the stop line; if there is none, at the crosswalk; if there is none, …"). Write one rule per case with `WHEN … AND there is no …`. There is no priority keyword.
- **Proportional comparisons** ("the sharper the turn, the slower you should go"). Write a `SHOULD` rule and flag the comparison `J`.
- **Duties on things or on someone other than the driver** ("courses must last 40 hours", "the owner may be charged"). The role is the responsible party: a driving school, the vehicle owner.
- **Task boundaries in the road-test chapter** ("This driving task begins when … ends when …"). These are `FACT`s about the test, not rules.

---

# Part B. Method

Work through the batch passage by passage, in order, and run steps 1 to 9 for each one. Then run steps 10 and 11 across all your statements. The illustrations below come from other parts of a handbook on purpose; apply the same reasoning to your topic.

## Step 1. Read the passage with its context

A passage often depends on text outside it. Before writing anything, collect:

1. **The heading path.** Headings often hold the condition. "Use your low-beam headlights." under `Fog › Tips for driving safely in fog › DO:` applies only in fog. "Slow down, listen and look both ways" under `Stopping at railway crossings` applies only at a railway crossing. Every condition a heading gives must end up written in the statement.
2. **Lead sentences.** A sentence ending in a colon ("When you come to a railway crossing, remember:", "Here are the steps for …:", "follow these directions:") passes its condition, role and goal to every item under it.
3. **Neighbouring passages.** Words like "they", "these vehicles", "this lane", "this area", "do so", "it" and "this rule" point to something said just before. Replace each with the noun it refers to. If you cannot tell what it refers to, keep the words and flag them R (step 8).
4. **Section-level force.** Some sections make everything under them law: "These signs give a direction that must be obeyed" (regulatory signs), a table of offences, a list of sanctions, "It is against the law to …" before a list. Remember these for step 6.

## Step 2. Decide whether the passage is in scope

Part C says what the topic covers. If the passage says nothing in scope, write no statement for it and move on. Writing nothing is correct for such passages; never invent a rule to produce output. If only part of a passage is in scope, write statements only for that part.

## Step 3. Find the propositions: split and join

A statement holds one proposition: one role, one modal, one set of conditions. Two actions with the same role and conditions may share a statement: `a driver SHOULD slow down AND SHOULD look both ways WHEN …`.

**Split** when:

- one sentence holds two rules, or a rule and a fact: "Fog is a thin layer of cloud … Fog can reduce visibility" gives a DEFINE and a FACT;
- one sentence gives duties to two roles: "You must use your seatbelt … All passengers must be buckled up" gives a rule for the driver and a rule for the passenger;
- a list lead introduces several items: each item becomes its own statement, citing the lead and the item.

**Join** when:

- a duty and its penalty are in different sentences or passages: one RULE with `IF VIOLATED`, citing both;
- a sentence makes sense only with its neighbour ("This means you may not stop your vehicle in this area", "Failure to do so …", "However, they can …"): one statement citing both;
- the same rule appears in two passages: one statement citing both. If the two wordings differ, add an X flag that says how.

**Ordered steps** (a numbered list, or "Here are the steps for …", "follow these steps") make one PROCEDURE, not a rule per step. A sentence inside a step that holds on its own, whatever the order ("Do not stop where you will block an entrance or other traffic"), also becomes its own RULE, linked to the procedure.

## Step 4. Choose the statement type

Take the first that fits:

1. It says what a term means or what something is called: **DEFINE**. ("Fog is a thin layer of cloud resting on the ground.")
2. It is an ordered sequence of actions toward a goal: **PROCEDURE**.
3. It changes a rule written in a **different** passage:
   - if it grants or imposes something of its own (a later paragraph says certain vehicles "may" do what an earlier one forbids), it is a RULE whose text starts `EXCEPTION TO <id>:`, with `<id>` in `links`;
   - if it only switches the other rule off ("This rule does not apply …" in a later paragraph), it is type **EXCEPTION**, text `EXCEPTION TO <id> WHEN <condition>`, force `null`, with `<id>` in `links`.
   An exception inside the same passage as its rule is an `UNLESS` clause, not a separate statement.
4. It tells some role what it must, must not, may, should or should not do, including cautions ("watch for") and advice: **RULE**.
5. Anything else is a **FACT**: how roads, signs, vehicles or laws are; what tends to happen; why something is dangerous; what a sign shows when it directs no one.

"May" or "can" as a possibility ("you may want to …", "… may help", "fog can reduce visibility") is not a permission. Write a FACT, or put it in the note; never a MAY rule.

## Step 5. Name the role

- "You" is `a driver`. Use the most specific role the text supports: `a driver being passed`, `a driver towing a trailer`, `a truck driver`, `a driver of a motor vehicle`, `a driver in the right-hand lane`, `a novice driver`, `a cyclist`, `a passenger`.
- Introduce the role with "a" once, then refer to it with "the": `a driver SHOULD stop at least 5 m from the nearest rail or gate WHEN the driver comes to a railway crossing AND a train is coming`.
- Never write "you" or "your" in a statement. "Your vehicle" becomes "the vehicle"; "your lane" becomes "the driver's lane".
- A rule for someone other than the driver keeps that role. Say in the note why it matters to the topic.

## Step 6. Choose the modal and record FORCE FROM

Apply the ladder in Part A §2 and take the first line that applies. Then fill `force` and `force_from`:

| Statement | `force` |
|---|---|
| RULE with MUST, MUST NOT or MAY | `"LEGAL"` |
| RULE with SHOULD or SHOULD NOT | `"ADVISORY"` |
| PROCEDURE | the force of its steps, usually `"ADVISORY"` |
| DEFINE, FACT, EXCEPTION (switch-off) | `null` |

`force_from` is one short string, `basis ("trigger words copied from the source")`. Use these bases:

| Basis | When | Examples |
|---|---|---|
| `text` | Words in the sentence decide it: must, must not, required, is not permitted, not allowed, illegal, unlawful, prohibited, offence, by law, may, can (permission), may not, cannot (prohibition), should, avoid, it is important to | `text ("must use")`, `text ("may not")`, `text ("Avoid")` |
| `imperative` | A bare command with no deciding word: Do, Don't, Never, Always, Use, Stay, Make sure, Be sure, Wait | `imperative ("Never")` |
| `caution` | Watch for, look out for, be careful, be prepared, be alert | `caution ("Be prepared to")` |
| `context` | A heading, section introduction, offence table or penalty makes it law | `context (Regulatory signs: "These signs give a direction that must be obeyed")`, `context (listed under "Table of offences")`, `context (penalty: "can be fined")` |
| `implied` | No instruction is given; one follows from a purpose or description ("… so that drivers can …") | `implied ("so that drivers … can …")` |
| `default` | Descriptive or passive wording that sets an expectation ("most … is done …", "… are not to be used for …") | `default (stated as a description: "…")` |
| `imperative steps` | A PROCEDURE whose steps are commands | `imperative steps` |

Rules for force:

- Legal wording in the **next** sentence counts: "Never drive around a lowered gate. It is illegal and dangerous." is MUST NOT, `text ("It is illegal")`.
- A penalty for failing to do something makes doing it law, even when no sentence states the duty.
- "May not" and "cannot" (as a prohibition) are MUST NOT. "Can" granting permission is MAY.
- Never raise force by guessing. "Never … under any conditions" with no legal word stays SHOULD NOT with an M flag. A precise distance in a bare imperative ("stop at least five metres from the nearest rail") stays SHOULD with an M flag.
- `implied` and `default` rules are SHOULD or SHOULD NOT and carry a D flag (or M when the force is the doubt).

## Step 7. Write the action and the conditions

**Action.** A verb phrase in the base form: `stop at least 5 m from the nearest rail or gate`, `use low-beam headlights`, `change lanes`, `move to the right`, `keep right`. Use the topic's one-phrase vocabulary (Part C). A caution is `SHOULD WATCH FOR <hazard>`. "Be careful" with no named hazard is `SHOULD <action> with [?extra care]`, flagged J.

**Conditions.** Collect every condition that decides when the statement applies, from three places: the sentence itself, the heading path and lead sentence (step 1), and neighbouring sentences. A condition you found in a heading must appear in the statement text. Then choose its clause:

| The handbook says | Clause |
|---|---|
| when, if, whenever, where, at, on (a road type), in (fog, the dark), as you approach | `WHEN` |
| while, during, as you go through (a state that lasts through the action) | `WHILE` |
| only if, only when, only to, provided that | `ONLY IF` |
| unless, except, except when, this does not apply if (in the same passage) | `UNLESS` |
| until, wait until, do not … until, before you (when the duty ends with it) | `UNTIL` |
| because, so that, to (giving the purpose), as, since; also a reason in the next sentence | `BECAUSE` |
| fine, demerit points, suspension, impoundment, licence loss | `IF VIOLATED` |

- Clauses come in this order: WHEN, WHILE, ONLY IF, UNLESS, UNTIL, BECAUSE, IF VIOLATED. Each clause appears at most once; join conditions inside it.
- Join conditions with capital `AND` / `OR` / `NOT`. `AND` binds tighter than `OR`; use parentheses for any other grouping. Lowercase "and" and "or" stay inside a noun phrase ("a gate or barrier", "a seatbelt, child car seat or booster seat").
- Write each condition as a clause with a subject: `WHEN the driver comes to a railway crossing`, `WHEN driving in fog`, `WHEN there is a fog warning`, `WHILE the gate or barrier is down`.
- "Before X" in a rule is `WHEN the driver is about to X`; "after X" is `WHEN the driver has X-ed`.
- A purpose is a reason: "so that drivers will not think you are turning" is `BECAUSE other drivers might otherwise think the driver is turning`.
- `IF … THEN` exists only as a branch inside a PROCEDURE. An event in a rule is `WHEN`.
- Inside a PROCEDURE, step order carries "before" and "after": step 4 `turn off the signal AND turn on the hazard lights` comes after step 3 `stop parallel to the curb`.

**Numbers.** Write digits and the handbook's own unit, never a converted one: metric handbooks use `m`, `km`, `km/h`, `s`, `cm`; US handbooks use `ft`, `mi`, `mph`. "Five metres" is `5 m`, "three feet" is `3 ft`. Keep the comparison words ("at least", "within", "more than", "at most"). Never write a number that is not in the source passages or their headings. If a threshold is missing ("a safe distance"), keep the vague words and flag them; never invent a value.

**Examples and asides.** An example the handbook gives ("for example, in heavy traffic") may stay as plain words after the condition. Advice that is only a possibility goes in the note.

## Step 8. Mark vague words and add flags

Keep the handbook's vague words, exactly as written, and mark them. Never replace them with a threshold.

| Code | Mark | Look for | Span is |
|---|---|---|---|
| J judgment | inline `[?…]` | safe, safely, enough, sure, in doubt, clear (when nothing says how clear), reasonable, proper, properly, carefully, caution, closely, well back, plenty of room, more room, too soon, as soon as you can, where practical, where possible, if possible, unnecessarily, about (a number) | the words inside the brackets |
| S hedged scope | inline `[?…]` | usually, often, most, many, some, generally, in some areas | the words inside the brackets |
| R unclear reference | inline `[?…]` | "these areas", "this lane", "they" with several candidates, a distance without a direction, a role you could not resolve | the words inside the brackets |
| G goal and means | inline `[?…]` | the rule restricts one means of doing something (crossing a line) rather than the thing itself | the words inside the brackets |
| M unclear force | statement only | an absolute with no legal word ("under any conditions"), a fixed distance in a bare imperative, a "must" in a test question | the source words that cause the doubt |
| D implicit default | statement only | a permission that presupposes an unstated ban ("You may … only to …"); a rule implied by a purpose or description | the source or statement words it rests on |
| V wording drift | statement only | the handbook names one thing two ways in different passages | the other wording |
| X stated elsewhere | statement only | the same rule appears elsewhere, possibly differently | the differing words |

- For J, S, R and G, wrap the span in the statement text as `[?span]` **and** add a flag with the same span. Every `[?…]` needs a flag, and every J, S, R or G flag whose words are in the statement needs its `[?…]` mark.
- When you rewrote the vague words out of the statement (a hedged "most …" that became a plain rule), keep the flag, with the handbook's words as its span and no mark.
- For M, D, V and X, add only the flag; the statement text has no mark.
- Each flag's `note` is one short sentence saying what a checker could not decide: "No measure of space or time.", "Subjective certainty; no observable test.", "Approximate distance with no stated tolerance."
- Flag what is vague in the handbook's text, not what you find hard.

## Step 9. Cite sources and write a note

- `sources` lists every passage the statement uses: the sentence itself, the lead sentence or section introduction that gave a condition or force, the neighbour that resolved a pronoun, the penalty sentence, and any figure that shows the rule.
- `quote` is copied **character for character** from the passage: the shortest complete sentence or sentences that support the statement. Keep the handbook's spelling, punctuation and curly quotes. For a figure, quote its alt text or caption as given.
- A figure (a diagram of the manoeuvre, a sign image) goes into the sources of the statement it illustrates. A figure that illustrates nothing in scope gives no statement.
- `note` is one or two sentences when you made a reading decision a reviewer should see: why a sentence gave no MAY rule, why two passages were joined, why a condition came from a heading, a rule for another role, a possibility kept out of the rule. Otherwise `null`.

## Step 10. Link statements

- `EXCEPTION TO <id>` and `SPECIALIZES <id>` put `<id>` in `links` as well as in the text.
- A PROCEDURE for a narrower situation (the same manoeuvre at night, or while towing) `SPECIALIZES` the general one: `TO <narrower goal> SPECIALIZES <id> WHEN <condition>`.
- A RULE taken from a step of a procedure lists the procedure's id in `links`.
- Every id in `links` must be the id of a statement in your answer.

## Step 11. Number and order

Give each statement an id from the outline in Part C: section number, then a letter in order of appearance (`3.4.4a`, `3.4.4b`). Ids must be unique. List statements in the order of their ids.

---

# Part C. Topic

## Topic: passing

**In scope.** Write statements for every passage that says something about:

- passing (overtaking) another vehicle or road user, on either side, including going around a vehicle that is stopped or slow (a school bus, a streetcar, a stopped emergency vehicle, a snow plow, farm machinery, a cyclist);
- places, road markings, signs, light and weather where passing is restricted or allowed (no-passing zones, solid or broken lines, "do not pass" signs, hills, curves, bridges, intersections, crossings, fog, night);
- lanes and parts of the road that exist for passing, or that decide which side to pass on: passing lanes, climbing lanes, turnouts, "keep right except to pass", the left lane of a freeway, passing on the right, the shoulder;
- being passed: what the driver being passed must or should do;
- penalties and offences for any of the above;
- definitions and background facts that a passing rule above needs in order to be understood.

**Out of scope.** Write nothing for a passage where "pass" or "passing" means something else:

- going by or through without overtaking anyone ("wait for the emergency vehicle to pass", "slow down and pass carefully" around an animal or a work zone, "once you have passed the exit");
- passing a test, passing a law, passengers;
- a lane change or turn that is not a pass, unless the handbook ties it to passing.

If a passage mixes both, write statements only for the in-scope part.

**Outline and IDs.** Number each statement by the section of this outline it belongs to, then a letter in the order the statements appear: `3.4.4a`, `3.4.4b`. If no section fits, add one at the end of the closest group (for example `3.4.14`); never renumber the sections below.

| ID | Section |
|---|---|
| 1 | Topic introduction: what passing is, why vehicles pass, background facts |
| 2.1 | General principles: when to pass at all, keeping right |
| 2.2 | The passing procedure |
| 3.1 | Where passing is restricted |
| 3.1.1 | Pedestrian crossovers and crosswalks |
| 3.1.2 | Bridges, viaducts and tunnels |
| 3.1.3 | Hills and curves |
| 3.1.4 | Turn lanes |
| 3.1.5 | Solid lines |
| 3.1.6 | Broken lines |
| 3.1.7 | Signs |
| 3.2 | Lanes and sides |
| 3.2.1 | Passing and climbing lanes |
| 3.2.2 | Freeway lanes |
| 3.2.3 | Passing on the right |
| 3.2.4 | The shoulder |
| 3.3 | Light and weather |
| 3.3.1 | Night |
| 3.3.2 | Fog |
| 3.3.3 | Snow and whiteouts |
| 3.4 | Particular road users and vehicles |
| 3.4.1 | Parked vehicles |
| 3.4.2 | Motorcycles and other two-wheelers |
| 3.4.3 | Smaller vehicles turning left |
| 3.4.4 | Cyclists |
| 3.4.5 | Streetcars |
| 3.4.6 | Large vehicles |
| 3.4.7 | Farm machinery |
| 3.4.8 | Horse-drawn vehicles |
| 3.4.9 | Snow plows |
| 3.4.10 | Pilot and pace vehicles |
| 3.4.11 | Vehicles stopped at a crosswalk |
| 3.4.12 | School buses |
| 3.4.13 | Emergency vehicles and tow trucks |
| 3.5 | Towing |
| 3.5.1 | Passing while towing |
| 3.5.2 | Being passed while towing |
| 3.6 | Being passed |
| 3.6.1 | Letting faster traffic pass |
| 3.6.2 | Being passed on an undivided road |
| 3.6.3 | Truck passing lanes |

**One phrase per concept.** Use these phrases, whatever the handbook says:

| Write | For |
|---|---|
| pass | overtake, overtake and pass, go around (a slower or stopped vehicle) |
| the vehicle being passed | the vehicle you are passing, the passed vehicle |
| a driver being passed | you, when someone is passing you |
| the passing lane | the lane you pass in |
| the original lane | the lane you started from |
| the right-hand lane, the far-left lane | right lane, left-most lane |
| the inside mirror | rear-view mirror, inside mirror (add a V flag when the handbook uses more than one) |
| oncoming traffic | traffic coming toward you |
| change lanes | move into another lane |
| a "do not pass" sign | a sign that forbids passing, named by its wording |

---

# Part D. Output format

Return exactly one JSON object and nothing else: no prose, no markdown fence.

```
{"statements": [ <statement>, ... ]}
```

Each statement has these fields, in this order:

| Field | Type | Content |
|---|---|---|
| `id` | string | From the outline: `"3.1.2a"` |
| `type` | string | `"DEFINE"`, `"FACT"`, `"RULE"`, `"PROCEDURE"` or `"EXCEPTION"` |
| `force` | string or null | `"LEGAL"`, `"ADVISORY"` or `null` (step 6) |
| `force_from` | string or null | `basis ("trigger words")`; `null` when force is `null` |
| `text` | string | The statement in v1, on one line. A PROCEDURE's text is only its `TO <goal> [SPECIALIZES <id>] [WHEN …]` line |
| `steps` | array | PROCEDURE only: `{"n": "1", "text": "…", "sources": ["m9"]}` per step, in order. Step text has no `STEP n` prefix. An `IF … THEN` branch has `"n": "IF"`; a `DONE WHEN` line has `"n": "DONE"`. Omit `steps` for other types |
| `sources` | array | `{"id": "m17", "quote": "…"}` per passage used (step 9) |
| `flags` | array | `{"code": "J", "span": "…", "note": "…"}` (step 8); `[]` if none |
| `links` | array | Ids of linked statements (step 10); `[]` if none |
| `note` | string or null | Step 9 |

---

# Part E. Worked examples

These examples come from other parts of a handbook, each with its own small topic, so the topic differs from yours. Their ids (`ex1a`) are only labels; your ids come from the outline in Part C.

## Example 1: A definition and a fact in one passage

Topic: driving in fog

What it shows: Split a passage into one statement per proposition. 'Can' that describes what something does is not a permission, so it gives a FACT, not a MAY rule.

Input:

```
[e1] page: Driving at night and in bad weather | heading: Fog · ¶1 | para
Fog is a thin layer of cloud resting on the ground. Fog can reduce visibility for drivers, resulting in difficult driving conditions.
```

Answer:

```json
{
 "statements": [
  {
   "id": "ex1a",
   "type": "DEFINE",
   "force": null,
   "force_from": null,
   "text": "DEFINE fog IS a thin layer of cloud THAT rests on the ground",
   "sources": [
    {
     "id": "e1",
     "quote": "Fog is a thin layer of cloud resting on the ground."
    }
   ],
   "flags": [],
   "links": [],
   "note": null
  },
  {
   "id": "ex1b",
   "type": "FACT",
   "force": null,
   "force_from": null,
   "text": "FACT fog can reduce visibility for drivers, resulting in difficult driving conditions",
   "sources": [
    {
     "id": "e1",
     "quote": "Fog can reduce visibility for drivers, resulting in difficult driving conditions."
    }
   ],
   "flags": [],
   "links": [],
   "note": "\"Can\" describes what fog does, not something a driver is allowed to do, so this is a FACT and not a MAY rule."
  }
 ]
}
```

## Example 2: A condition held in the heading and a list lead

Topic: driving in fog

What it shows: The list item never mentions fog. The heading and the lead sentence do, so the condition goes into the statement and both passages are cited. The lead sentence also holds rules of its own.

Input:

```
[e2] page: Driving at night and in bad weather | heading: Fog › Tips for driving safely in fog · ¶1 | para
Before you drive - and during your trip - check weather forecasts. If there is a fog warning, delay your trip until it clears. If you are caught driving in fog, follow these safe-driving tips:

[e3] page: Driving at night and in bad weather | heading: Fog › Tips for driving safely in fog › DO: · item 3 | item
Use your low-beam headlights. High beams reflect off the moisture droplets in the fog, making it harder to see.
```

Answer:

```json
{
 "statements": [
  {
   "id": "ex2a",
   "type": "RULE",
   "force": "ADVISORY",
   "force_from": "imperative (\"check\")",
   "text": "a driver SHOULD check weather forecasts WHEN the driver is about to drive OR the driver is on a trip",
   "sources": [
    {
     "id": "e2",
     "quote": "Before you drive - and during your trip - check weather forecasts."
    }
   ],
   "flags": [],
   "links": [],
   "note": null
  },
  {
   "id": "ex2b",
   "type": "RULE",
   "force": "ADVISORY",
   "force_from": "imperative (\"delay\")",
   "text": "a driver SHOULD delay the trip WHEN there is a fog warning UNTIL the fog clears",
   "sources": [
    {
     "id": "e2",
     "quote": "If there is a fog warning, delay your trip until it clears."
    }
   ],
   "flags": [],
   "links": [],
   "note": null
  },
  {
   "id": "ex2c",
   "type": "RULE",
   "force": "ADVISORY",
   "force_from": "imperative (\"Use\")",
   "text": "a driver SHOULD use low-beam headlights WHEN driving in fog BECAUSE high beams reflect off the moisture droplets in the fog, making it harder to see",
   "sources": [
    {
     "id": "e2",
     "quote": "If you are caught driving in fog, follow these safe-driving tips:"
    },
    {
     "id": "e3",
     "quote": "Use your low-beam headlights. High beams reflect off the moisture droplets in the fog, making it harder to see."
    }
   ],
   "flags": [],
   "links": [],
   "note": "The item does not mention fog; the condition comes from the heading and the lead sentence, so it is written as WHEN driving in fog."
  }
 ]
}
```

## Example 3: Legal force from the section, and a sign caption

Topic: regulatory signs that tell drivers where they may not go or stop

What it shows: A sign caption is a bare imperative, which gives SHOULD by default. The section introduction says these signs must be obeyed, so the force is legal, and force_from names the section. The sentence about sign shapes is out of this topic and gives nothing.

Input:

```
[e4] page: Signs | heading: Regulatory signs · ¶1 | para
These signs give a direction that must be obeyed. They are usually rectangular or square with a white or black background and black, white or coloured letters. A sign with a green circle means you may or must do the activity shown inside the ring. A red circle with a line through it means the activity shown is not allowed.

[e5] page: Signs | heading: Regulatory signs › Here are some common regulatory signs: · ¶4 | para
Do not enter this road.

[e6] page: Signs | heading: Regulatory signs › Here are some common regulatory signs: · image | figure
Figure: Alt text: “a regulatory sign”

[e7] page: Signs | heading: Regulatory signs › Here are some common regulatory signs: · ¶5 | para
Do not stop in the area between the signs. This means you may not stop your vehicle in this area, even for a moment. (Used in pairs or groups.)
```

Answer:

```json
{
 "statements": [
  {
   "id": "ex3a",
   "type": "FACT",
   "force": null,
   "force_from": null,
   "text": "FACT a red circle with a line through it on a regulatory sign means the activity shown is not allowed",
   "sources": [
    {
     "id": "e4",
     "quote": "A red circle with a line through it means the activity shown is not allowed."
    }
   ],
   "flags": [],
   "links": [],
   "note": null
  },
  {
   "id": "ex3b",
   "type": "RULE",
   "force": "LEGAL",
   "force_from": "context (Regulatory signs: \"These signs give a direction that must be obeyed\")",
   "text": "a driver MUST NOT enter a road WHEN a \"do not enter\" sign is posted for the road",
   "sources": [
    {
     "id": "e4",
     "quote": "These signs give a direction that must be obeyed."
    },
    {
     "id": "e5",
     "quote": "Do not enter this road."
    },
    {
     "id": "e6",
     "quote": "a regulatory sign"
    }
   ],
   "flags": [],
   "links": [],
   "note": "The caption alone is a bare imperative; the legal force comes from the section introduction."
  },
  {
   "id": "ex3c",
   "type": "RULE",
   "force": "LEGAL",
   "force_from": "text (\"may not\")",
   "text": "a driver MUST NOT stop the vehicle, even for a moment, WHEN the vehicle is in the area between \"do not stop\" signs",
   "sources": [
    {
     "id": "e4",
     "quote": "These signs give a direction that must be obeyed."
    },
    {
     "id": "e7",
     "quote": "Do not stop in the area between the signs. This means you may not stop your vehicle in this area, even for a moment."
    }
   ],
   "flags": [],
   "links": [],
   "note": null
  }
 ]
}
```

## Example 4: Imperatives, a legal marker in the next sentence, UNTIL, and vague words

Topic: railway crossings

What it shows: "Never" alone gives SHOULD NOT; "It is illegal" in the next sentence makes it MUST NOT. A fixed distance in a bare imperative stays SHOULD with an M flag. "Until you are sure" is UNTIL with a J flag. Numbers become digits with the handbook's unit.

Input:

```
[e8] page: Stopping | heading: Stopping at railway crossings · ¶2 | para
When you come to a railway crossing, remember:

[e9] page: Stopping | heading: Stopping at railway crossings · item 2 | item
If a train is coming, stop at least five metres from the nearest rail or gate. Do not cross the track until you are sure the train or trains have passed.

[e10] page: Stopping | heading: Stopping at railway crossings · item 5 | item
Never drive around, under or through a railway gate or barrier while it is down, being lowered or being raised. It is illegal and dangerous.
```

Answer:

```json
{
 "statements": [
  {
   "id": "ex4a",
   "type": "RULE",
   "force": "ADVISORY",
   "force_from": "imperative (\"stop\")",
   "text": "a driver SHOULD stop at least 5 m from the nearest rail or gate WHEN the driver comes to a railway crossing AND a train is coming",
   "sources": [
    {
     "id": "e8",
     "quote": "When you come to a railway crossing, remember:"
    },
    {
     "id": "e9",
     "quote": "If a train is coming, stop at least five metres from the nearest rail or gate."
    }
   ],
   "flags": [
    {
     "code": "M",
     "span": "stop at least five metres",
     "note": "A fixed distance reads like a legal duty, but the sentence has no legal wording, so it stays SHOULD."
    }
   ],
   "links": [],
   "note": null
  },
  {
   "id": "ex4b",
   "type": "RULE",
   "force": "ADVISORY",
   "force_from": "imperative (\"Do not cross\")",
   "text": "a driver SHOULD NOT cross the track WHEN the driver comes to a railway crossing AND a train is coming UNTIL the driver is [?sure] the train or trains have passed",
   "sources": [
    {
     "id": "e8",
     "quote": "When you come to a railway crossing, remember:"
    },
    {
     "id": "e9",
     "quote": "Do not cross the track until you are sure the train or trains have passed."
    }
   ],
   "flags": [
    {
     "code": "J",
     "span": "sure",
     "note": "Subjective certainty; no observable test."
    }
   ],
   "links": [],
   "note": null
  },
  {
   "id": "ex4c",
   "type": "RULE",
   "force": "LEGAL",
   "force_from": "text (\"It is illegal\")",
   "text": "a driver MUST NOT drive around, under or through a railway gate or barrier WHILE the gate or barrier is down, being lowered or being raised BECAUSE it is dangerous",
   "sources": [
    {
     "id": "e10",
     "quote": "Never drive around, under or through a railway gate or barrier while it is down, being lowered or being raised. It is illegal and dangerous."
    }
   ],
   "flags": [],
   "links": [],
   "note": "\"Never\" alone would give SHOULD NOT; the next sentence, \"It is illegal\", gives legal force."
  }
 ]
}
```

## Example 5: An exception in the same passage is UNLESS

Topic: intersections

What it shows: "This does not apply if …" sits in the same passage as its rule, so it becomes an UNLESS clause. Clauses follow the fixed order WHEN, WHILE, ONLY IF, UNLESS, UNTIL, BECAUSE, IF VIOLATED.

Input:

```
[e11] page: Driving through intersections | heading: Controlled intersections · ¶3 | para
When you approach an intersection on a main road, and the intersection is blocked with traffic, stop before entering the intersection and wait until the traffic ahead moves on. This does not apply if you are turning left or right.
```

Answer:

```json
{
 "statements": [
  {
   "id": "ex5a",
   "type": "RULE",
   "force": "ADVISORY",
   "force_from": "imperative (\"stop\", \"wait\")",
   "text": "a driver SHOULD stop before entering the intersection AND wait WHEN the driver approaches an intersection on a main road AND the intersection is blocked with traffic UNLESS the driver is turning left OR the driver is turning right UNTIL the traffic ahead moves on",
   "sources": [
    {
     "id": "e11",
     "quote": "When you approach an intersection on a main road, and the intersection is blocked with traffic, stop before entering the intersection and wait until the traffic ahead moves on. This does not apply if you are turning left or right."
    }
   ],
   "flags": [],
   "links": [],
   "note": "The exception is in the same passage, so it is an UNLESS clause. In a different passage it would be its own statement: EXCEPTION TO ex5a WHEN the driver is turning left OR the driver is turning right."
  }
 ]
}
```

## Example 6: A procedure, with a step that holds on its own

Topic: making a roadside stop

What it shows: Numbered steps make one PROCEDURE. The lead sentence gives its goal and condition. Each step cites its own passage. A conditional detour inside a step becomes an IF … THEN branch. A prohibition that holds whatever the step order is also written as its own RULE, linked to the procedure.

Input:

```
[e12] page: Parking along roadways | heading: Roadside stop · ¶1 | para
When you need to stop by the side of the road for a short time to check something outside your vehicle, or to look for directions on a map, for example, follow these directions:

[e13] page: Parking along roadways | heading: Roadside stop · item 1 | step
Before slowing down, check your mirrors and blind spot to see when the way is clear.

[e14] page: Parking along roadways | heading: Roadside stop · item 2 | step
Turn on your signal before slowing down unless there are vehicles waiting to enter the road from side roads or driveways between you and the point where you intend to stop. Wait until you have passed these entrances so that drivers will not think you are turning before the stopping point.

[e15] page: Parking along roadways | heading: Roadside stop · item 3 | step
Steer to the side of the road, steadily reducing speed, and stop parallel to the curb or edge of the road. You should not be more than about 30 centimetres away from it. Do not stop where you will block an entrance or other traffic.

[e16] page: Parking along roadways | heading: Roadside stop · item 4 | step
Turn off your signal and turn on your hazard lights.
```

Answer:

```json
{
 "statements": [
  {
   "id": "ex6a",
   "type": "PROCEDURE",
   "force": "ADVISORY",
   "force_from": "imperative steps",
   "text": "TO make a roadside stop WHEN the driver needs to stop by the side of the road for a short time",
   "steps": [
    {
     "n": "1",
     "text": "check the mirrors and blind spot to see when the way is clear WHEN the driver is about to slow down",
     "sources": [
      "e13"
     ]
    },
    {
     "n": "2",
     "text": "turn on the signal WHEN the driver is about to slow down UNLESS vehicles are waiting to enter the road from side roads or driveways between the driver and the stopping point",
     "sources": [
      "e14"
     ]
    },
    {
     "n": "3",
     "text": "steer to the side of the road, steadily reducing speed, AND stop parallel to the curb or edge of the road, at most [?about] 30 cm from it",
     "sources": [
      "e15"
     ]
    },
    {
     "n": "4",
     "text": "turn off the signal AND turn on the hazard lights",
     "sources": [
      "e16"
     ]
    },
    {
     "n": "IF",
     "text": "IF vehicles are waiting to enter the road between the driver and the stopping point THEN turn on the signal only after passing these entrances",
     "sources": [
      "e14"
     ]
    }
   ],
   "sources": [
    {
     "id": "e12",
     "quote": "When you need to stop by the side of the road for a short time to check something outside your vehicle, or to look for directions on a map, for example, follow these directions:"
    }
   ],
   "flags": [
    {
     "code": "J",
     "span": "about",
     "note": "Approximate distance with no stated tolerance."
    }
   ],
   "links": [],
   "note": "The IF branch exists so that waiting drivers do not think the driver is turning before the stopping point."
  },
  {
   "id": "ex6b",
   "type": "RULE",
   "force": "ADVISORY",
   "force_from": "imperative (\"Do not stop\")",
   "text": "a driver SHOULD NOT stop where the vehicle will block an entrance or other traffic WHEN making a roadside stop",
   "sources": [
    {
     "id": "e15",
     "quote": "Do not stop where you will block an entrance or other traffic."
    }
   ],
   "flags": [],
   "links": [
    "ex6a"
   ],
   "note": "This prohibition holds whatever the step order, so it is its own RULE as well as part of step 3's situation."
  }
 ]
}
```

## Example 7: A duty and its penalty in different passages, and choosing the role

Topic: seatbelts

What it shows: A duty and its penalty make one statement with IF VIOLATED, citing both passages. "You" can cover more than one role; use the role each sentence supports. A penalty with no separate duty sentence still makes a legal rule, with force from the penalty.

Input:

```
[e17] page: Getting ready to drive | heading: Fasten your seatbelt · ¶3 | para
You must use your seatbelt every time you travel in any vehicle equipped with seatbelts. All passengers must be buckled up in their own seatbelt, child car seat or booster seat.

[e18] page: Getting ready to drive | heading: Fasten your seatbelt · ¶4 (first two sentences) | para
Drivers who do not buckle up can be fined and will be given two demerit points. Drivers may also be fined and receive demerit points if they fail to ensure that all passengers under 16 years of age are properly buckled in a seatbelt, child car seat or booster seat.
```

Answer:

```json
{
 "statements": [
  {
   "id": "ex7a",
   "type": "RULE",
   "force": "LEGAL",
   "force_from": "text (\"must use\")",
   "text": "a driver MUST use a seatbelt WHILE travelling in a vehicle equipped with seatbelts IF VIOLATED a fine AND 2 demerit points",
   "sources": [
    {
     "id": "e17",
     "quote": "You must use your seatbelt every time you travel in any vehicle equipped with seatbelts."
    },
    {
     "id": "e18",
     "quote": "Drivers who do not buckle up can be fined and will be given two demerit points."
    }
   ],
   "flags": [],
   "links": [],
   "note": "The duty and its penalty are in different paragraphs, so they make one statement. \"You\" also covers passengers, but the penalty names drivers; the passenger duty is ex7b."
  },
  {
   "id": "ex7b",
   "type": "RULE",
   "force": "LEGAL",
   "force_from": "text (\"must be buckled up\")",
   "text": "a passenger MUST be buckled up in the passenger's own seatbelt, child car seat or booster seat",
   "sources": [
    {
     "id": "e17",
     "quote": "All passengers must be buckled up in their own seatbelt, child car seat or booster seat."
    }
   ],
   "flags": [],
   "links": [],
   "note": null
  },
  {
   "id": "ex7c",
   "type": "RULE",
   "force": "LEGAL",
   "force_from": "context (penalty: \"may also be fined and receive demerit points\")",
   "text": "a driver MUST ensure that every passenger under 16 years of age is [?properly] buckled in a seatbelt, child car seat or booster seat IF VIOLATED a fine AND demerit points",
   "sources": [
    {
     "id": "e18",
     "quote": "Drivers may also be fined and receive demerit points if they fail to ensure that all passengers under 16 years of age are properly buckled in a seatbelt, child car seat or booster seat."
    }
   ],
   "flags": [
    {
     "code": "J",
     "span": "properly",
     "note": "The handbook does not say what proper buckling requires."
    }
   ],
   "links": [],
   "note": "Only the penalty is stated; a penalty for failing to do something makes doing it a legal duty. The number of demerit points is not given, so none is written."
  }
 ]
}
```

## Example 8: "Pass" that does not mean overtaking

Topic: passing

What it shows: Here "pass" means that oncoming bicycles go by; nobody overtakes anyone. The sentence is a left-turn rule, which is outside the passing topic, so a passing extraction writes no statement for it. Writing nothing is the right answer for such passages.

Input:

```
[e19] page: Sharing the road with other road users | heading: Sharing the road with cyclists · item 6 | item
When turning left, you must stop and wait for oncoming bicycles to pass before turning.
```

Answer:

```json
{
 "statements": []
}
```

---

# Part F. Check before you answer

Go through every statement and fix anything that fails:

1. The text uses only these capitalised keywords: DEFINE, IS, THAT, ALSO CALLED, FACT, MUST, MUST NOT, MAY, SHOULD, SHOULD NOT, WATCH FOR, WHEN, WHILE, ONLY IF, UNLESS, UNTIL, BECAUSE, IF VIOLATED, AND, OR, NOT, TO, SPECIALIZES, IF, THEN, DONE WHEN, EXCEPTION TO. Everything else is lower case, apart from names, abbreviations and quoted sign wording.
2. A RULE has a role, then a modal, then an action. No "you" or "your" anywhere.
3. `force` matches the modal (MUST, MUST NOT, MAY are LEGAL; SHOULD, SHOULD NOT are ADVISORY), and `force_from` gives a basis from the table in step 6.
4. Every condition held in a heading or lead sentence is written in the statement.
5. Clauses are in the order WHEN, WHILE, ONLY IF, UNLESS, UNTIL, BECAUSE, IF VIOLATED, each at most once.
6. Every number appears in the cited passages or their headings, in the handbook's unit.
7. Every `[?…]` has a flag with the same span, and no vague word from a J, S, R or G flag is left in the text unmarked.
8. Every quote is copied exactly from the passage it cites, and every cited id is a passage in the batch.
9. Every id in `links` exists in your answer, and ids are unique.
10. No statement comes from an out-of-scope passage, and no in-scope sentence is left without a statement.
