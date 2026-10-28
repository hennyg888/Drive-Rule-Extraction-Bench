# SYSTEM

You turn passages from a driver's handbook into formal statements written in the Rule Language. The statements must keep the handbook's meaning exactly, make explicit what the handbook leaves implicit (conditions held in headings, legal strength, exceptions written elsewhere), and mark every vague word instead of resolving it. Each statement cites the passages it came from.

Follow this document exactly. It contains: 1 the task, 2 the input, 3 the output, 4 the language, 5 the vocabulary, 6 what to write and what to skip, 7 worked examples, 8 a final checklist.

# 1. Task

You receive a handbook name, a topic with its scope, and a list of passages. Write every statement of the topic that the passages support:

- definitions (DEFINE), background facts (FACT), rules (RULE), step-by-step procedures (PROCEDURE) and exceptions (EXCEPTION);
- for each rule, its strength (law or advice) and the wording or context that gives that strength;
- every condition under which a statement applies, including conditions that appear only in a heading, a list lead, a neighbouring passage, or a figure;
- a flag for every vague, hedged, unclear or inconsistent piece of wording.

Return only the JSON object described in section 3. Do not add commentary before or after it.

# 2. Input

Each passage is one JSON object on its own line:

| Field | Meaning |
|---|---|
| `id` | The passage id. Cite passages only by this id. |
| `page` | The handbook page or chapter it is on. |
| `sec` | The heading path above it, outermost first (`›` or `>` separates levels). It may end with a position such as `· ¶3` (third paragraph) or `· item 2` (second list item). It may be empty. |
| `kind` | `text` or `figure`. |
| `text` | For `text`, the passage itself, verbatim. For `figure`, the image's alt text. |
| `cap` | Figures only: the caption, often with a diagram number. |
| `image` | Figures only, optional: the image file. When the image itself is attached, use what it shows (for example the words on a sign). |

Passages arrive in handbook order, page by page. Read each one with its headings and its neighbours: a heading can hold the condition of every passage under it ("Fog", "At night", "Red light"), and a passage ending in a colon is a list lead whose role, modal and conditions pass to each item after it.

# 3. Output

Return one JSON object: `{"statements": [ … ]}`, statements in order of their first source passage. Each statement has these fields:

| Field | Content |
|---|---|
| `id` | The id of the statement's first source passage plus a lowercase letter, in the order you write them: `m17a`, `m17b`. Ids never repeat. |
| `type` | `DEFINE`, `FACT`, `RULE`, `PROCEDURE` or `EXCEPTION`. An exception that is a rule of its own (`EXCEPTION TO <id>: <rule>`) has type `RULE`. An exception that only switches another statement off (`EXCEPTION TO <id> WHEN <condition>`) has type `EXCEPTION`. |
| `strength` | `LAW` for a statement whose modals are MUST, MUST NOT or MAY; `ADVICE` for SHOULD and SHOULD NOT; `null` for DEFINE, FACT and the `EXCEPTION … WHEN` form. A PROCEDURE takes the strength of its steps (usually `ADVICE`). |
| `strength_from` | Why the strength is what it is (section 4.2), or `null` when `strength` is `null`. |
| `text` | The statement on one line, in the Rule Language (section 4). For a PROCEDURE, only the header: `TO <goal> [SPECIALIZES <id>] [WHEN <condition>]`. |
| `steps` | PROCEDURE only: `[{"n": "1", "text": "<action> [clauses]", "sources": ["<passage id>"]}, …]`. Number steps `"1"`, `"2"`, …; a branch has `"n": "IF"` and text `IF <event> THEN <action>`; a finishing condition has `"n": "DONE"` and text `DONE WHEN <state>`. Step text has no `STEP n` prefix and no role. |
| `sources` | `[{"id": "<passage id>", "quote": "<the passage's full text, verbatim>"}]`. First the passage that states the statement, then passages that add a condition, a penalty, a reason or a list lead, then figures. For a PROCEDURE, the passage that introduces the procedure or states its goal, and its figures; each step lists its own sources. |
| `flags` | `[{"code": "<J S R G M D V X>", "span": "<words>", "note": "<one sentence>"}]`, or `[]` (section 4.6). |
| `links` | The ids named by `EXCEPTION TO` or `SPECIALIZES` in this statement, or `[]`. Only ids of statements you wrote in this output. |
| `note` | `null`, or one or two sentences when the statement rests on a reading choice a reviewer should see: a condition taken from a heading, a "may" read as possibility, a list lead applied to an item, a sentence that is motivation rather than permission. |
| `see` | Optional. `[{"figure": "<label>", "source": "<figure passage id>"}]` for each figure that goes with the statement. The label is the diagram number when the caption has one (`Diagram 2-46`); otherwise a short name such as `the "do not pass" sign`. |

# 4. Rule Language

A statement is one line of fixed keywords (in capitals) around plain English. Keywords never change meaning; everything between them is ordinary text in the controlled vocabulary of section 5.

## 4.1 Statement types and grammar

| Type | Pattern | Use for |
|---|---|---|
| `DEFINE` | `DEFINE <term> IS <kind> THAT <difference> [ALSO CALLED <alias>]` | A term and what it means |
| `FACT` | `FACT <sentence> [clauses]` | Background with no instruction: how things work, what a sign shows, what tends to happen |
| `RULE` | `<role> <MODAL> <action> [clauses]` | Obligations, prohibitions, permissions, advice, cautions |
| `PROCEDURE` | `TO <goal> [SPECIALIZES <id>] [WHEN …]`, then steps, optional `DONE WHEN <state>`, optional `IF <event> THEN <action>` | Ordered steps |
| `EXCEPTION` | `EXCEPTION TO <id> WHEN <condition>` | An exception, written in a different passage, that only switches another statement off |

An exception written in a different passage from the rule it changes is its own statement:

- `EXCEPTION TO <id>: <role> <MODAL> <action> [clauses]` (type `RULE`) when the exception is a rule of its own, such as a permission;
- `EXCEPTION TO <id> WHEN <condition>` (type `EXCEPTION`) when it only switches the other rule off.

An exception inside the same sentence as its rule is not a separate statement; write it with `UNLESS`.

Grammar. Capitals are keywords. Lowercase names on the right (role, verb-phrase, hazard, phrase, reason, penalty, term, kind, difference, alias, sentence, goal, state, event, id, n) are plain English written by the wording rules in 4.5. `AND`, `OR` and `NOT` can also join phrases inside them (`IF VIOLATED a fine AND 2 demerit points`). `{ }` repeats, `[ ]` is optional, `|` means or.

```
statement ::= rule | define | fact | procedure | exception
rule      ::= role modal choice { AND [ modal ] choice } { clause }
choice    ::= action | EITHER action OR action { OR action }
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
step      ::= action { AND action } { clause }
exception ::= EXCEPTION TO id ( ":" rule | WHEN condition )
```

## 4.2 Modals and strength

The modal gives the statement's deontic modality (obligation, prohibition or permission) and its strength (law or advice).

| Modal | Meaning | Strength |
|---|---|---|
| `MUST` | Obligation | `LAW` |
| `MUST NOT` | Prohibition | `LAW` |
| `MAY` | Permission | `LAW` |
| `SHOULD` | Advice | `ADVICE` |
| `SHOULD NOT` | Advice against | `ADVICE` |

A caution is a rule: `<role> SHOULD WATCH FOR <hazard> [clauses]`. When the handbook says "be careful" without naming a hazard, write `SHOULD <action> with [?extra care]` and flag it `J`.

Choosing the modal. Take the first line that applies:

1. Legal wording gives `MUST` / `MUST NOT`: must, must not, required, is not permitted, not allowed, may not, cannot (as a prohibition), illegal, unlawful, prohibited, offence, by law.
2. Permission wording gives `MAY`: may, can, allowed, permitted, but only when it grants permission. "May" or "can" as possibility ("may want to", "may help", "may be", "can create") is not a permission; write a `FACT`, or nothing, and explain in `note`.
3. Section context can give law to the statements under it, when the section says so. Example: a section of regulatory signs that opens "These signs give a direction that must be obeyed" makes each sign's plain caption `MUST` / `MUST NOT`. A behaviour listed in an offence table, a demerit-point table or a sanctions list counts the same way.
4. Advice wording gives `SHOULD` / `SHOULD NOT`: should, it is important to, try to, avoid, make sure, be sure.
5. Bare imperatives (do, don't, never, always, be sure) give `SHOULD` / `SHOULD NOT`.
6. Cautions (watch for, look out for, be prepared, be alert, be careful) give `SHOULD WATCH FOR` when a hazard is named, otherwise `SHOULD` / `SHOULD NOT` with the action.

When the wording and the result disagree in spirit (an absolute "under any conditions" with no legal marker; an imperative that sits right after a "must" about the same duty; a test question that says "must"), keep the result of the list and add an `M` flag. Never raise strength by guessing.

`strength_from` records the line that decided, in one of these forms, quoting the deciding words from the source:

| Form | When |
|---|---|
| `text ("<words>")` | Lines 1, 2 or 4: the sentence's own legal, permission or advice wording, e.g. `text ("is not permitted")`, `text ("may … only")`, `text ("should")`, `text ("Avoid")` |
| `imperative ("<words>")` | Line 5, e.g. `imperative ("Never")`, `imperative ("Keep to the right")` |
| `imperative steps` | A procedure written as imperative steps |
| `caution ("<words>")` | Line 6, e.g. `caution ("watch carefully for")`, `caution ("Be careful not to")` |
| `context (<section or table>: "<words>")` | Line 3, e.g. `context (Regulatory signs: "must be obeyed")`, `context (listed under "Sanctions – dangerous behaviours")` |
| `default (<why>)` | No modal or imperative: a description or a prescriptive passive, e.g. `default (prescriptive passive "are not to be used")`, `default (stated as a description: "Most passing is done on the left")` |
| `implied ("<words>")` | The duty is only implied by a description of what drivers do, e.g. `implied ("so drivers can begin to merge")` |

Two deciding phrases can be joined: `text ("Avoid") and imperative ("Don't")`.

## 4.3 Clauses

| Clause | Meaning | Example |
|---|---|---|
| `WHEN <situation or event>` | When the statement applies | `WHEN the driver is within 30 m of a pedestrian crossover` |
| `WHILE <state>` | A state that lasts for the whole action | `WHILE passing the cyclist` |
| `ONLY IF <condition>` | A condition that must hold; mostly after `MAY` | `MAY drive on the right shoulder ONLY IF … the shoulder is paved` |
| `UNLESS <condition>` | An exception inside the same sentence | `MUST pass a streetcar on the right UNLESS the driver is on a one-way road` |
| `UNTIL <event or state>` | When the duty ends | `SHOULD NOT pass a vehicle that is turning left ahead UNTIL it has moved to the right` |
| `BECAUSE <reason or purpose>` | Why; never changes when the rule applies | `BECAUSE passing on the right can be more dangerous` |
| `IF VIOLATED <penalty>` | Fine, demerit points, suspension, impoundment | `IF VIOLATED a fine AND 2 demerit points` |
| `AND` / `OR` / `NOT` | Connectives | |

- A clause applies to the whole statement. Clauses come in the order of this table.
- Capital `AND` / `OR` / `NOT` join conditions or actions. Lowercase "and" / "or" stay inside a noun phrase ("a bridge, viaduct or tunnel").
- A duty that is a choice between actions is `EITHER <action> OR <action>`: `a driver SHOULD EITHER stay behind the vehicle OR pass it WHEN …`.
- Each part of a condition is a full phrase with its own subject: `WHEN the road is multi-lane OR the road is one-way`, not `WHEN the road is multi-lane OR one-way`.
- `AND` binds tighter than `OR`. Use parentheses for any other grouping: `WHEN (the driver is approaching the crest of a hill OR the driver is on a curve) AND the view of oncoming traffic is obstructed`.
- A purpose is written as a reason: "so that the other lanes are clear for passing" becomes `BECAUSE this leaves the other lanes clear for passing`.
- `IF … THEN` is only for a branch inside a PROCEDURE. An event in a rule is `WHEN`: "If a bus pushes your trailer, do not brake" becomes `… SHOULD NOT brake … WHEN a passing bus or truck pushes the trailer out of position`.
- Order without a keyword: inside a procedure, step order carries "before" and "after". In a rule, "before X" is `WHEN about to X` and "after X" is `WHEN the driver has X-ed` or `ONLY IF the driver has first X-ed`.
- `UNTIL` is for a duty that ends: stop until, wait until, do not pass until. Use `UNLESS` for an exception that is not about time.
- A penalty stated in another passage (a later sentence, an offence table) joins the rule it punishes as `IF VIOLATED`, and that passage becomes a source.

## 4.4 Links

| Link | Meaning |
|---|---|
| `EXCEPTION TO <id>` | Changes another statement; the more specific statement wins |
| `SPECIALIZES <id>` | A variant of another statement for a narrower situation (a procedure for passing at night specializes the passing procedure) |
| `ALSO CALLED <alias>` | A synonym, inside `DEFINE` |

Every id named by `EXCEPTION TO` or `SPECIALIZES` also goes in `links`. Only link to statements in this output.

## 4.5 Wording

- Roles. Introduce with "a", refer back with "the": "a driver … the driver". Never "you" or "your". Use the most specific role the source supports (section 5.1).
- One phrase per concept. Use the vocabulary of section 5. Where the handbook itself drifts between words for one thing (inside mirror / rear view mirror), every statement keeps the one phrase and the statement where the handbook used the other word gets a `V` flag.
- Quantities. Digits and short units: m, km, km/h, s, kg. Number words become digits ("two metres" is `2 m`). Fixed comparison phrases, not keywords: "at least", "at most", "more than", "less than", "within 30 m of", "between … and …", "up to". Never write a number that is not in the sources.
- Lists. A sentence that introduces a list ("Bring the following:") passes its role, modal and clauses to each item; each item becomes its own statement with the item and the lead as sources. A definition by list is `DEFINE <term> IS <kind> THAT includes <a>, <b> or <c>`.
- Right of way. "yield the right-of-way to <road user>" is a verb phrase, not a keyword.
- Two statements in one sentence. Split them; both cite the same source.
- One statement from several passages. Join passages when together they state one statement: a duty and its penalty, a rule and its reason, a sign's caption and its image, a list lead and its item, the same rule stated on two pages (add an `X` flag when their wording differs).
- Vague words stay as written, wrapped in `[?…]` and flagged. Thresholds are never invented, and vague words are never replaced by a sharper reading.
- Pronouns. Replace "it", "they", "do so" with what they refer to when the passage makes that clear; when it does not, keep the words in `[?…]` and flag `R`.

## 4.6 Flags

| Code | Meaning | Where it shows |
|---|---|---|
| `J` | Judgment term: safe, safely, enough, sure, reasonable, possible, as soon as you can, carefully, with caution | Inline `[?…]` |
| `S` | Hedged scope: usually, often, many, most, some, generally | Inline `[?…]` |
| `R` | Unclear reference or role: "these areas", "the smaller vehicle", a heading-only scope you had to assume | Inline `[?…]` |
| `G` | Goal and means differ: the rule bans crossing the centreline, not passing as such | Inline `[?…]` |
| `M` | Unclear legal strength (see 4.2) | On the statement |
| `D` | Implicit default: a permission that presupposes an unstated prohibition, or the reverse | On the statement |
| `V` | Wording drift across passages for the same thing | On the statement |
| `X` | Stated again elsewhere in the passages, possibly differently | On the statement |

- For `J`, `S`, `R` and `G`, the span is the exact text inside the `[?…]` in `text` (or in a step). When the vague words were in the source but are not carried into the statement (a reference you resolved, a hedge you dropped from a rule), the span quotes the source words instead and nothing is marked inline.
- For `M`, `D`, `V` and `X`, the span quotes the words that raise the issue, from the source or the statement.
- Each flag gets a one-sentence `note` saying what is unclear. One flag per distinct span; a span that occurs twice in one statement is flagged once.
- Flag what a careful reader could not act on without a judgment call. Do not flag a precise phrase from the vocabulary (section 5) such as "the way is clear".

## 4.7 Not covered, and the workaround

- Consequences with no rule broken (demerit-point totals, failing a re-examination): `FACT <trigger> leads to <consequence>`.
- Escalating penalties (first, second, third offence): write each tier after `IF VIOLATED`.
- Fallback chains ("stop at the stop line; if there is none, at the crosswalk; …"): one rule per case with `WHEN … AND there is no …`.
- Proportional comparisons ("the sharper the turn, the slower you should go"): a `SHOULD` rule with the comparison flagged `J`.
- Duties on things or on someone other than the driver ("courses must last 40 hours", "the owner may be charged"): the role is the responsible party, such as a driving school or the vehicle owner.
- Task boundaries in a road-test chapter ("This driving task begins when … ends when …"): `FACT`s about the test, not rules.

# 5. Vocabulary

Write these words for these concepts. When a passage uses a listed variant, write the listed phrase instead and, if the handbook uses different words for the same thing across passages, add a `V` flag to the statement where it drifted. When a passage's word means something different from the listed phrase, keep the passage's word. When a concept is not listed, use the handbook's own most frequent wording and keep it the same in every statement you write. Never invent a term the handbook does not use.

## 5.1 Roles (the subject of a rule)

| Write | For | Not |
|---|---|---|
| a driver | anyone driving a vehicle; the default role | you, your, motorist, operator |
| a driver being passed | the driver of a vehicle that another vehicle is passing | the slower driver |
| a driver towing a trailer | a driver pulling a trailer, camper or boat | |
| a truck driver; a bus driver | the driver of a truck or bus, when only they are meant | |
| a driver of a motor vehicle | when the source limits the duty to motor vehicles, as opposed to cyclists | |
| a cyclist; a motorcyclist; a pedestrian | other road users who carry their own duty | |
| a novice driver; a G1 driver; a G2 driver; a licence applicant; a road test candidate; a vehicle owner; a snowmobile driver; an off-road vehicle driver | licensing, ownership and other chapters | |

- Narrow the role with a place or state when the source does: "a driver on a freeway", "a driver in the right-hand lane".
- Refer back with "the": "the driver", "the cyclist". Other people in the same statement: "another driver", "the passing driver", "the driver in front", "other road users".

## 5.2 Actions

| Write | Not |
|---|---|
| pass (a vehicle); a pass | overtake, overtake and pass, get around |
| change lanes; a lane change | switch lanes |
| move into the passing lane | pull out (except inside a procedure step that keeps the handbook's verb) |
| move back into the original lane; return to the original lane | pull back in |
| cut in, cut off | (keep these when the point is moving in too closely) |
| keep to the right; keep to the right-hand lane | stay right |
| turn left; turn right; make a U-turn | |
| merge with traffic in <lane> | |
| stop; come to a complete stop | halt |
| slow down; speed up | accelerate (keep "accelerate" only when the point is how fast a vehicle can gain speed) |
| yield the right-of-way to <road user> | give way |
| signal left; signal right; signal | use your left-turn signal |
| check the mirrors; check the blind spot; check over the shoulder | |
| switch to low beams; use low beams; switch on high beams | dim your lights |
| sound the horn | honk, beep |
| WATCH FOR <hazard> | look out for, be on the lookout for |

## 5.3 Road users and vehicles

vehicle (any); motor vehicle (when the source distinguishes it); the vehicle being passed; the vehicle in front; a slower vehicle; faster traffic; oncoming traffic (not approaching or opposing traffic); cyclist (the person) and bicycle (the vehicle); motorcycle; limited-speed motorcycle; moped; pedestrian; streetcar; school bus; bus; emergency vehicle; tow truck; large vehicle (large trucks and buses); truck; long commercial vehicle (LCV); farm machinery; horse-drawn vehicle; snow plow; pilot vehicle; pace vehicle; trailer.

## 5.4 Roads, lanes and places

| Write | Meaning or variants |
|---|---|
| the passing lane | the lane a driver moves into to pass |
| the original lane | the lane a driver left to pass and returns to |
| the right-hand lane; the left lane; the far-left lane | the far-left lane is the leftmost lane of a road with 3 or more lanes in one direction |
| a multi-lane road; a two-lane road; a one-way road; an undivided road; a freeway; a high-speed road | freeway, not expressway |
| a passing lane or climbing lane | an added lane for slower traffic |
| a two-way left-turn lane | centre lane for left turns in both directions |
| the centreline; a solid line; a broken line | pavement markings; say where: "a solid line at the left of the driver's lane" |
| the shoulder; the right shoulder; the left shoulder; a paved shoulder | |
| a median strip | a physical divider between directions |
| an intersection; a pedestrian crossover; a crosswalk; a railway crossing | |
| a bridge, viaduct or tunnel; the crest of a hill; a curve | |

## 5.5 Conditions and states

| Write | For |
|---|---|
| WHEN it is night | at night, after dark |
| WHEN driving in fog; WHEN driving in rain; WHEN driving in blowing snow or a whiteout | weather conditions |
| the way is clear | no road user is in the path or about to enter it; a precise phrase, not flagged |
| the view of oncoming traffic is obstructed | "your vision is restricted", "you cannot see" |
| WHEN about to <verb> | "before you <verb>" |
| WHEN the driver has <past participle> | "after you have <verb>" |
| WHEN approaching …; WHILE alongside …; WHEN behind … | position relative to another vehicle |

## 5.6 Signs, lights and equipment

- A sign is named by its legend in double quotes, in lowercase: a "do not pass" sign, a "keep right except to pass" sign. Sign types: regulatory sign, warning sign, temporary condition sign.
- Lights on other vehicles as the handbook words them: upper alternating red lights flashing; red or red-and-blue lights flashing; amber lights flashing.
- the inside mirror (not rear view mirror or rear-view mirror); the outside mirrors; the blind spot; the turn signal; low beams; high beams; the horn; the brakes.

## 5.7 Quantities and penalties

- Distances, speeds and times: `30 m`, `1 m`, `150 m`, `60 km/h`, `2 s`; counts in digits: `2 or more lanes`, `3 demerit points`.
- Penalties after `IF VIOLATED`: `a fine`, `a fine of $<n> to $<n>`, `<n> demerit points`, `a licence suspension`, `vehicle impoundment`, `jail`, joined with `AND`; add `for a first offence` and similar tiers when stated. Keep the handbook's adjectives and flag the vague ones (`a [?heavy] fine`).

## 5.8 Words that are always flagged

- `J`: safe, safely, in safety, safe to do so, if safe to do so, enough, sure, in doubt, possible, where practical, where possible, as soon as the driver can, reasonable, carefully, with caution, extra care, well back, more room, too soon, too closely, closely, some distance, unnecessarily, necessary for safety, as much distance as possible, properly, if necessary, slow traffic.
- `S`: usually, often, generally, typically, many, most, some, several, certain, sometimes.
- `R`: these, this, it, they, such, and "the smaller vehicle" or "the area" when the passage does not say which.

# 6. What to write and what to skip

- Cover every passage in scope. Each in-scope passage ends up as a source, a step source or a figure of at least one statement. A passage may support several statements, and several passages may support one.
- Write nothing for passages outside the topic scope, and nothing for passages with no content of their own: navigation ("See Diagram 2-11"), summaries of what a section covers, questions that only introduce an answer, links to other documents.
- Background that explains why a rule exists or what drivers will meet is a `FACT`. Motivation such as "you may want to pass slow vehicles" is not a permission; at most a `FACT`, with a note.
- A sample test question and its answer can be the sources of a rule; flag `M` when only the question supplies "must".
- Keep the handbook's meaning: do not add conditions it does not state, do not merge different duties, do not drop a condition because it is in a heading.
- A statement whose condition comes only from a heading, a list lead or a neighbouring passage says so in `note`.
- A rule for someone other than the driver (a cyclist's permission, a truck driver's duty) is still written when it is in the topic; its role says whose it is.

# 7. Worked examples

These examples use short passage ids (u1, v1, r1, w1) and parts of the Ontario Driver's Handbook outside any topic you will be given. Follow their form, not their content.

## Example A

Topic: U-turns. Scope: turning a vehicle around to travel in the opposite direction.

```
{"id": "u1", "page": "Changing directions", "sec": "Turning around › U-turn · ¶1", "kind": "text", "text": "Before you make a U-turn, check to make sure there is no sign saying not to."}
{"id": "u2", "page": "Changing directions", "sec": "Turning around › U-turn · ¶2", "kind": "text", "text": "It is illegal to make a U-turn on a curve in the road, on or near a railway crossing or hilltop, or near a bridge or tunnel that blocks your view."}
{"id": "u3", "page": "Changing directions", "sec": "Turning around › U-turn · ¶2", "kind": "text", "text": "Never make a U-turn unless you can see at least 150 metres in both directions."}
{"id": "u4", "page": "Changing directions", "sec": "Turning around › U-turn · ¶3", "kind": "text", "text": "To make a U-turn, signal for a right turn, check your mirror and over your shoulder and pull over to the right side of the road."}
{"id": "u5", "page": "Changing directions", "sec": "Turning around › U-turn · ¶3", "kind": "text", "text": "Stop."}
{"id": "u6", "page": "Changing directions", "sec": "Turning around › U-turn · ¶3", "kind": "text", "text": "Signal a left turn and when traffic is clear in both directions, move forward and turn quickly and sharply into the opposite lane."}
{"id": "u7", "page": "Changing directions", "sec": "Turning around › U-turn · ¶3", "kind": "text", "text": "Check for traffic as you turn."}
{"id": "u8", "page": "Signs", "sec": "Regulatory signs › Here are some common regulatory signs: · image", "kind": "figure", "text": "a regulatory sign", "cap": "Alt text: “a regulatory sign”"}
{"id": "u9", "page": "Signs", "sec": "Regulatory signs › Here are some common regulatory signs: · ¶4", "kind": "text", "text": "Do not turn to go in the opposite direction. (U-turn)"}
{"id": "u10", "page": "Changing directions", "sec": "Summary · item 6", "kind": "text", "text": "Methods of turning your vehicle around to travel back in the opposite direction (U-turns, three-point turns)"}
```

```
{"statements": [
{"id": "u1a", "type": "RULE", "strength": "ADVICE", "strength_from": "imperative (\"check to make sure\")", "text": "a driver SHOULD check that no sign prohibits a U-turn WHEN about to make a U-turn", "sources": [{"id": "u1", "quote": "Before you make a U-turn, check to make sure there is no sign saying not to."}], "flags": [], "links": [], "note": null},
{"id": "u2a", "type": "RULE", "strength": "LAW", "strength_from": "text (\"It is illegal\")", "text": "a driver MUST NOT make a U-turn WHEN the driver is on a curve OR the driver is on or [?near] a railway crossing or hilltop OR the driver is [?near] a bridge or tunnel that blocks the driver's view", "sources": [{"id": "u2", "quote": "It is illegal to make a U-turn on a curve in the road, on or near a railway crossing or hilltop, or near a bridge or tunnel that blocks your view."}], "flags": [{"code": "J", "span": "near", "note": "No distance is given."}], "links": [], "note": null},
{"id": "u3a", "type": "RULE", "strength": "ADVICE", "strength_from": "imperative (\"Never\")", "text": "a driver SHOULD NOT make a U-turn UNLESS the driver can see at least 150 m in both directions", "sources": [{"id": "u3", "quote": "Never make a U-turn unless you can see at least 150 metres in both directions."}], "flags": [], "links": [], "note": null},
{"id": "u4a", "type": "PROCEDURE", "strength": "ADVICE", "strength_from": "imperative steps", "text": "TO make a U-turn", "steps": [{"n": "1", "text": "signal right AND check the mirror and over the shoulder AND pull over to the right side of the road", "sources": ["u4"]}, {"n": "2", "text": "stop", "sources": ["u5"]}, {"n": "3", "text": "signal left", "sources": ["u6"]}, {"n": "4", "text": "move forward AND turn quickly and sharply into the opposite lane WHEN the way is clear in both directions", "sources": ["u6"]}, {"n": "5", "text": "check for traffic WHILE turning", "sources": ["u7"]}], "sources": [{"id": "u4", "quote": "To make a U-turn, signal for a right turn, check your mirror and over your shoulder and pull over to the right side of the road."}], "flags": [], "links": [], "note": null},
{"id": "u9a", "type": "RULE", "strength": "LAW", "strength_from": "context (Regulatory signs: \"must be obeyed\")", "text": "a driver MUST NOT make a U-turn WHEN a \"no U-turn\" sign applies", "sources": [{"id": "u9", "quote": "Do not turn to go in the opposite direction. (U-turn)"}, {"id": "u8", "quote": "a regulatory sign"}], "see": [{"figure": "the \"no U-turn\" sign", "source": "u8"}], "flags": [], "links": [], "note": "The caption is a plain imperative; the legal force comes from the regulatory signs section."}
]}
```

u10 gets no statement: it only summarises the section.

## Example B

Topic: Traffic lights. Scope: what drivers must or should do at traffic lights, and what the lights mean.

```
{"id": "v1", "page": "Traffic lights", "sec": "Red light · ¶1", "kind": "text", "text": "A red light means you must stop."}
{"id": "v2", "page": "Traffic lights", "sec": "Red light · ¶1", "kind": "text", "text": "Bring your vehicle to a complete stop at the stop line if it is marked on the pavement."}
{"id": "v3", "page": "Traffic lights", "sec": "Red light · ¶1", "kind": "text", "text": "If there is no stop line, stop at the crosswalk, marked or not."}
{"id": "v4", "page": "Traffic lights", "sec": "Red light · ¶3", "kind": "text", "text": "Unless a sign tells you not to, you may turn right on a red light only after coming to a complete stop and waiting until the way is clear."}
{"id": "v5", "page": "Traffic lights", "sec": "Fully protected left turn · ¶1", "kind": "text", "text": "When a left-turn green arrow appears for traffic in the left-turn lane, traffic going straight ahead or turning right will usually see a red light."}
```

```
{"statements": [
{"id": "v1a", "type": "RULE", "strength": "LAW", "strength_from": "text (\"must\")", "text": "a driver MUST stop WHEN facing a red light", "sources": [{"id": "v1", "quote": "A red light means you must stop."}], "flags": [], "links": [], "note": null},
{"id": "v2a", "type": "RULE", "strength": "ADVICE", "strength_from": "imperative (\"Bring your vehicle to a complete stop\")", "text": "a driver SHOULD come to a complete stop at the stop line WHEN facing a red light AND a stop line is marked on the pavement", "sources": [{"id": "v2", "quote": "Bring your vehicle to a complete stop at the stop line if it is marked on the pavement."}], "flags": [{"code": "M", "span": "Bring your vehicle to a complete stop", "note": "Follows \"you must stop\" (v1); the handbook does not say whether the stopping place is law too."}], "links": [], "note": "\"Facing a red light\" comes from the heading."},
{"id": "v3a", "type": "RULE", "strength": "ADVICE", "strength_from": "imperative (\"stop\")", "text": "a driver SHOULD stop at the crosswalk, marked or not, WHEN facing a red light AND there is no stop line", "sources": [{"id": "v3", "quote": "If there is no stop line, stop at the crosswalk, marked or not."}], "flags": [{"code": "M", "span": "stop at the crosswalk", "note": "Follows \"you must stop\" (v1); the handbook does not say whether the stopping place is law too."}], "links": [], "note": "The next case of the fallback chain begun in v2a."},
{"id": "v4a", "type": "RULE", "strength": "LAW", "strength_from": "text (\"may … only after\")", "text": "a driver MAY turn right WHEN facing a red light ONLY IF the driver has first come to a complete stop AND the way is clear UNLESS a sign prohibits the turn", "sources": [{"id": "v4", "quote": "Unless a sign tells you not to, you may turn right on a red light only after coming to a complete stop and waiting until the way is clear."}], "flags": [], "links": [], "note": null},
{"id": "v5a", "type": "FACT", "strength": null, "strength_from": null, "text": "FACT traffic going straight ahead or turning right [?usually] faces a red light WHEN a left-turn green arrow is shown for the left-turn lane", "sources": [{"id": "v5", "quote": "When a left-turn green arrow appears for traffic in the left-turn lane, traffic going straight ahead or turning right will usually see a red light."}], "flags": [{"code": "S", "span": "usually", "note": "Hedged; the handbook does not say when it differs."}], "links": [], "note": null}
]}
```

## Example C

Topic: Railway crossings. Scope: what drivers must or should do at railway crossings.

```
{"id": "r1", "page": "Stopping", "sec": "Stopping at railway crossings · ¶3", "kind": "text", "text": "When you come to a railway crossing, remember:"}
{"id": "r2", "page": "Stopping", "sec": "Stopping at railway crossings · item 3", "kind": "text", "text": "If a train is coming, stop at least five metres from the nearest rail or gate."}
{"id": "r3", "page": "Stopping", "sec": "Stopping at railway crossings · item 5", "kind": "text", "text": "If there are signal lights, wait until they stop flashing and, if the crossing has a gate or barrier, wait until it rises before you cross the tracks."}
{"id": "r4", "page": "Stopping", "sec": "Stopping at railway crossings · item 6", "kind": "text", "text": "Never drive around, under or through a railway gate or barrier while it is down, being lowered or being raised."}
{"id": "r5", "page": "Keeping your licence", "sec": "Table of offences › Three points · item 9", "kind": "text", "text": "Driving through, around or under a railway crossing barrier"}
```

```
{"statements": [
{"id": "r2a", "type": "RULE", "strength": "ADVICE", "strength_from": "imperative (\"stop\")", "text": "a driver SHOULD stop at least 5 m from the nearest rail or gate WHEN at a railway crossing AND a train is coming", "sources": [{"id": "r2", "quote": "If a train is coming, stop at least five metres from the nearest rail or gate."}, {"id": "r1", "quote": "When you come to a railway crossing, remember:"}], "flags": [], "links": [], "note": "\"At a railway crossing\" comes from the list lead (r1)."},
{"id": "r3a", "type": "RULE", "strength": "ADVICE", "strength_from": "imperative (\"wait until\")", "text": "a driver SHOULD NOT cross the tracks WHEN the railway crossing has signal lights that are flashing UNTIL the lights stop flashing", "sources": [{"id": "r3", "quote": "If there are signal lights, wait until they stop flashing and, if the crossing has a gate or barrier, wait until it rises before you cross the tracks."}, {"id": "r1", "quote": "When you come to a railway crossing, remember:"}], "flags": [], "links": [], "note": null},
{"id": "r3b", "type": "RULE", "strength": "ADVICE", "strength_from": "imperative (\"wait until\")", "text": "a driver SHOULD NOT cross the tracks WHEN the railway crossing has a gate or barrier UNTIL the gate or barrier rises", "sources": [{"id": "r3", "quote": "If there are signal lights, wait until they stop flashing and, if the crossing has a gate or barrier, wait until it rises before you cross the tracks."}, {"id": "r1", "quote": "When you come to a railway crossing, remember:"}], "flags": [], "links": [], "note": null},
{"id": "r4a", "type": "RULE", "strength": "LAW", "strength_from": "context (Table of offences › Three points: \"Driving through, around or under a railway crossing barrier\")", "text": "a driver MUST NOT drive around, under or through a railway crossing gate or barrier WHILE it is down, being lowered or being raised IF VIOLATED 3 demerit points", "sources": [{"id": "r4", "quote": "Never drive around, under or through a railway gate or barrier while it is down, being lowered or being raised."}, {"id": "r5", "quote": "Driving through, around or under a railway crossing barrier"}], "flags": [], "links": [], "note": "The Stopping page words this as advice (\"Never\"); the offence table makes it law and gives the penalty."}
]}
```

r1 has no statement of its own; it is the list lead for r2 to r4.

## Example D

Topic: HOV lanes. Scope: who may use high-occupancy vehicle lanes, and the rules for using them.

```
{"id": "w1", "page": "Freeway driving", "sec": "High Occupancy Vehicle (HOV) Lane · ¶1", "kind": "text", "text": "A High-Occupancy Vehicle (HOV) lane is a specially designed lane that is designated for use by certain types of vehicles with a specified number of occupants."}
{"id": "w2", "page": "Freeway driving", "sec": "High Occupancy Vehicle (HOV) Lane · ¶2", "kind": "text", "text": "HOV lanes are open 24 hours a day, seven days a week."}
{"id": "w3", "page": "Freeway driving", "sec": "High Occupancy Vehicle (HOV) Lane · ¶4", "kind": "text", "text": "HOV lanes on provincial highways are reserved for:"}
{"id": "w4", "page": "Freeway driving", "sec": "High Occupancy Vehicle (HOV) Lane · item 1", "kind": "text", "text": "vehicles carrying at least two people"}
{"id": "w5", "page": "Freeway driving", "sec": "High Occupancy Vehicle (HOV) Lane · ¶5", "kind": "text", "text": "Large trucks are not permitted on the HOV lanes, regardless of the number of occupants."}
{"id": "w6", "page": "Freeway driving", "sec": "High Occupancy Vehicle (HOV) Lane · item 4", "kind": "text", "text": "Buses can use an HOV lane at any time, regardless of the number of occupants."}
{"id": "w7", "page": "Freeway driving", "sec": "High Occupancy Vehicle (HOV) Lane · item 8", "kind": "text", "text": "Single-occupant taxis and airport limousines are permitted in the HOV lane."}
```

```
{"statements": [
{"id": "w1a", "type": "DEFINE", "strength": null, "strength_from": null, "text": "DEFINE a high-occupancy vehicle lane IS a specially designed lane THAT is designated for certain types of vehicles with a specified number of occupants ALSO CALLED HOV lane", "sources": [{"id": "w1", "quote": "A High-Occupancy Vehicle (HOV) lane is a specially designed lane that is designated for use by certain types of vehicles with a specified number of occupants."}], "flags": [], "links": [], "note": null},
{"id": "w2a", "type": "FACT", "strength": null, "strength_from": null, "text": "FACT HOV lanes are open 24 hours a day, 7 days a week", "sources": [{"id": "w2", "quote": "HOV lanes are open 24 hours a day, seven days a week."}], "flags": [], "links": [], "note": null},
{"id": "w4a", "type": "RULE", "strength": "LAW", "strength_from": "text (\"reserved for\")", "text": "a driver MAY use an HOV lane on a provincial highway ONLY IF the vehicle carries at least 2 people", "sources": [{"id": "w4", "quote": "vehicles carrying at least two people"}, {"id": "w3", "quote": "HOV lanes on provincial highways are reserved for:"}], "flags": [{"code": "D", "span": "reserved for", "note": "Implies that vehicles not on the list may not use the lane; the passage does not say so directly."}], "links": [], "note": "The list lead (w3) gives the permission; the item gives its condition."},
{"id": "w5a", "type": "RULE", "strength": "LAW", "strength_from": "text (\"are not permitted\")", "text": "a truck driver MUST NOT drive a large truck in an HOV lane, whatever the number of occupants", "sources": [{"id": "w5", "quote": "Large trucks are not permitted on the HOV lanes, regardless of the number of occupants."}], "flags": [], "links": [], "note": null},
{"id": "w6a", "type": "EXCEPTION", "strength": null, "strength_from": null, "text": "EXCEPTION TO w4a WHEN the vehicle is a bus", "sources": [{"id": "w6", "quote": "Buses can use an HOV lane at any time, regardless of the number of occupants."}], "flags": [], "links": ["w4a"], "note": null},
{"id": "w7a", "type": "RULE", "strength": "LAW", "strength_from": "text (\"are permitted\")", "text": "EXCEPTION TO w4a: a driver of a taxi or airport limousine MAY use an HOV lane WHEN the driver is the only occupant", "sources": [{"id": "w7", "quote": "Single-occupant taxis and airport limousines are permitted in the HOV lane."}], "flags": [], "links": ["w4a"], "note": null}
]}
```

# 8. Checklist before you answer

1. Every in-scope passage is cited by at least one statement; out-of-scope passages are cited by none.
2. Every rule has exactly the modals the decision list in 4.2 gives, its `strength` matches its modals, and `strength_from` quotes the deciding words.
3. Every condition from a heading, list lead, neighbouring passage or figure is in the statement, and `note` says where it came from.
4. Every penalty for a rule is attached with `IF VIOLATED`, with its passage as a source.
5. Every vague word is kept, wrapped in `[?…]` where it appears, and has a flag with the same span.
6. No number appears that is not in a source; number words became digits.
7. Roles start with "a" and refer back with "the"; no "you"; one phrase per concept from section 5.
8. Keywords are in capitals and only from section 4; ordinary words are lowercase.
9. Every id in `links` is the id of a statement in this output, and every statement id is its first source id plus a letter.
10. The output is one JSON object with a `statements` array and nothing else.

# USER

Handbook: Ontario MTO Driver's Handbook (ontario.ca, offline copy checked 2026-10-06)

Topic: passing

Topic scope: Passing (overtaking): a driver moving past another vehicle going the same way, whether that vehicle is travelling, stopped in traffic or parked, and everything that decides whether, where, when and how a driver may do so, including lane use for passing, duties that make passing a stopped vehicle illegal (such as having to stop for it), and what a driver who is being passed should do. "Pass" used only to mean going by a person, an animal, a work zone or another hazard is not this topic.

Passages, one JSON object per line, in handbook order:

{"id": "p1", "page": "Getting Your Driver’s Licence", "sec": "Could You Pass? · ¶1", "kind": "text", "text": "The rest of this handbook gives you information you need to pass your tests and to keep your driving privileges once you get your licence. The written test may ask you about:"}
{"id": "p2", "page": "Getting Your Driver’s Licence", "sec": "Could You Pass? · item 10", "kind": "text", "text": "Passing other vehicles"}
{"id": "p3", "page": "Getting Your Driver’s Licence", "sec": "Could You Pass? · item 16", "kind": "text", "text": "Passing vehicles, including bicycles, and driving in passing lanes"}
{"id": "p4", "page": "Getting ready to drive", "sec": "Turn on headlights at night and in poor conditions · ¶2", "kind": "text", "text": "Headlights enable you to see the roadway in front of your vehicle when visibility is poor, as well as making your vehicle visible to others. Your vehicle’s headlights must shine a white light that can be seen at least 150 metres in front and is strong enough to light up objects 110 metres away. You must also have red rear lights that can be seen 150 metres away and a white light lighting the rear licence plate when headlights are on. Headlights are equipped with the option to use a high beam to enhance vision further down the roadway and the use of a low beam when you are near other vehicles to minimize the glare of your headlights onto others. When you use high-beam headlights, remember to switch to low beams within 150 metres of an oncoming vehicle. Use your low beams when you are less than 60 metres behind another vehicle unless you are passing it. These rules apply to all roads, including divided ones."}
{"id": "p5", "page": "Driving along", "sec": "Intro · ¶2", "kind": "text", "text": "Keep a cushion of space around your vehicle and be prepared for the unexpected. Anticipate other drivers movements and make allowances for every possible error. Look well ahead and watch for people in parked vehicles, they may be about to pull out in front of you or to open a door. Watch for smaller vehicles, bicycles and pedestrians."}
{"id": "p6", "page": "Driving along", "sec": "Keep right · ¶1", "kind": "text", "text": "Keep to the right of the road or in the right-hand lane on multi-lane roads unless you want to turn left or pass another vehicle. This is especially important if you are driving more slowly than other vehicles."}
{"id": "p7", "page": "Sharing the road with other road users", "sec": "Sharing the road with pedestrians · ¶4", "kind": "text", "text": "Watch for all crosswalks – A crosswalk can be the portion of a roadway that:"}
{"id": "p8", "page": "Sharing the road with other road users", "sec": "Sharing the road with pedestrians · item 2", "kind": "text", "text": "has signs, lines or other markings on the roadway for pedestrian crossing Do not pass a vehicle stopped at a crosswalk. A stopped vehicle may be a clue that a pedestrian is crossing."}
{"id": "p9", "page": "Sharing the road with other road users", "sec": "Sharing the road with cyclists · ¶1", "kind": "text", "text": "Bicycles and mopeds travelling at a lower speed than other traffic are expected to ride about one metre from the curb or parked cars, or as close as practical to the right-hand edge of the road when there is no curb. However, they can use any part of the lane if necessary for safety, such as to:"}
{"id": "p10", "page": "Sharing the road with other road users", "sec": "Sharing the road with cyclists · item 3", "kind": "text", "text": "Discourage passing where the lane is too narrow to be shared safely"}
{"id": "p11", "page": "Sharing the road with other road users", "sec": "Sharing the road with cyclists · ¶3", "kind": "text", "text": "When passing a cyclist, drivers of motor vehicles must maintain a minimum distance of one metre, where practical between their vehicle and the cyclist. (See Diagram 2-11.) Failure to do so may result in a fine and an additional two demerit points on the driver’s record. Whenever possible, you should change lanes to pass."}
{"id": "p12", "page": "Sharing the road with other road users", "sec": "Sharing the road with cyclists · ¶6", "kind": "text", "text": "Do not sound your horn unnecessarily when you are overtaking a cyclist. It may frighten them and cause them to lose control. If you feel that you must use your horn, tap it quickly and lightly while you are still some distance away from the cyclist."}
{"id": "p13", "page": "Sharing the road with other road users", "sec": "Sharing the road with cyclists · ¶12", "kind": "text", "text": "Children riding bicycles on the street may lack the necessary training and skills for safe cycling. They may not be aware of all the dangers or the rules of the road. Watch for children on oversized bicycles, as they may not have the ability to control it. When parked on the side of the roadway, look behind you and check your mirrors and blind spots for a passing cyclist before opening a door."}
{"id": "p14", "page": "Sharing the road with other road users", "sec": "Sharing the road with large commercial vehicles · ¶3", "kind": "text", "text": "2. Stopping Distance - Large commercial vehicles require a much longer distance to stop than smaller vehicles. When passing a large vehicle, do not cut in front closely. Not only is this discourteous, it is dangerous; it reduces the space cushion large vehicles require in order to stop safely. Allow more room when passing a large vehicle."}
{"id": "p15", "page": "Sharing the road with other road users", "sec": "Sharing the road with large commercial vehicles · ¶8", "kind": "text", "text": "6. Turbulence - Due to various factors such as air pressure and airflow, a large vehicle can create heavy air turbulence. This may affect your ability to control your vehicle when passing a large one."}
{"id": "p16", "page": "Sharing the road with other road users", "sec": "Sharing the road with farm machinery · ¶2", "kind": "text", "text": "Farm machinery on the road must display an orange and red slow-moving sign on the rear of the vehicle. The sign warns other drivers that the vehicle is travelling at 40 km/h or less. If you see one of these signs, slow down and be cautious. Stay well back and do not pass until it is safe to do so."}
{"id": "p17", "page": "Sharing the road with other road users", "sec": "Sharing the road with horse-drawn vehicles · ¶2", "kind": "text", "text": "Horse-drawn vehicles on the road must display an orange and red slow-moving sign on the rear of the buggy. In addition, many buggies have highly reflective tape affixed to the side and rear of the vehicle. The sign warns other drivers that this vehicle is travelling at 40 km/h or less, and the reflective tape illuminates as headlights hit the buggy. If you see a horse-drawn vehicle, slow down and be very cautious. Maintain a safe following distance and only pass when it is safe to do so. When approaching a horse-drawn vehicle travelling in the opposite direction, move to the far right of your lane. When passing, give as much distance between you and them as possible. Passing too closely could scare or startle the horse, causing it to change direction suddenly on the roadway."}
{"id": "p18", "page": "Sharing the road with other road users", "sec": "Sharing the road with school buses · ¶1", "kind": "text", "text": "When you see a school bus with its overhead amber lights flashing:"}
{"id": "p19", "page": "Sharing the road with other road users", "sec": "Sharing the road with school buses · item 1", "kind": "text", "text": "These signals indicate that the bus is coming to a stop to pick up or drop off passengers"}
{"id": "p20", "page": "Sharing the road with other road users", "sec": "Sharing the road with school buses · item 2", "kind": "text", "text": "Slow down and prepare to stop whether you are behind or approaching the bus"}
{"id": "p21", "page": "Sharing the road with other road users", "sec": "Sharing the road with school buses · item 3", "kind": "text", "text": "If you are on a road with a median strip, only vehicles approach from the rear of the bus should prepare to stop"}
{"id": "p22", "page": "Sharing the road with other road users", "sec": "Sharing the road with school buses · ¶3", "kind": "text", "text": "When you see a school bus with its overhead red lights flashing or its stop arm activated:"}
{"id": "p23", "page": "Sharing the road with other road users", "sec": "Sharing the road with school buses · item 4", "kind": "text", "text": "You must stop whether you are behind or approaching the bus"}
{"id": "p24", "page": "Sharing the road with other road users", "sec": "Sharing the road with school buses · item 5", "kind": "text", "text": "If you are on a roadway with a median strip, only vehicles approaching from the rear of the bus must stop"}
{"id": "p25", "page": "Sharing the road with other road users", "sec": "Sharing the road with school buses · item 6", "kind": "text", "text": "If you are approaching from the rear of the vehicle, stop at least 20 meters away"}
{"id": "p26", "page": "Sharing the road with other road users", "sec": "Sharing the road with school buses · item 7", "kind": "text", "text": "Do not proceed on your route until the bus moves, the overhead red lights have stopped flashing and its stop arm is no longer activated"}
{"id": "p27", "page": "Sharing the road with other road users", "sec": "Sharing the road with school buses · item 8", "kind": "text", "text": "It is dangerous and illegal to fail to stop for a stopped school bus that has its overhead red lights flashing or its stop arm activated"}
{"id": "p28", "page": "Stopping", "sec": "Stopping for school buses · ¶2", "kind": "text", "text": "You must stop whenever you approach a stopped school bus with its upper alternating red lights flashing, regardless of whether you are behind the bus or approaching it from the front. When approaching the bus from the front, stop at a safe distance for children to get off the bus and cross the road in front of you. If you are coming from behind the bus, stop at least 20 metres away. Do not go until the bus moves or the lights have stopped flashing."}
{"id": "p29", "page": "Stopping", "sec": "Stopping for school buses · image", "kind": "figure", "text": "the required stopping distance on a two-way road for vehicles coming up behind a school bus with lights flashing", "cap": "Diagram 2-27 | Alt text: “the required stopping distance on a two-way road for vehicles coming up behind a school bus with lights flashing”", "image": "images/2-27a.jpg"}
{"id": "p30", "page": "Stopping", "sec": "Stopping for school buses · image", "kind": "figure", "text": "the required stopping distance on a roadway with a median strip for vehicles coming up behind a school bus with lights flashing", "cap": "Diagram 2-28 | Alt text: “the required stopping distance on a roadway with a median strip for vehicles coming up behind a school bus with lights flashing”", "image": "images/2-28a.jpg"}
{"id": "p31", "page": "Stopping", "sec": "Stopping for school buses · ¶3", "kind": "text", "text": "If you are on a road with a median strip, only vehicles coming from behind the bus must stop. (A median is a physical barrier such as a raised, lowered, earth or paved strip constructed to separate traffic travelling in different directions. Vehicles cannot cross over a median strip.)"}
{"id": "p32", "page": "Stopping", "sec": "Stopping for school buses · ¶4", "kind": "text", "text": "You must obey the school bus law on any road, no matter how many lanes or what the speed limit. Be prepared to stop for a school bus at any time, not just within school hours."}
{"id": "p33", "page": "Stopping", "sec": "Stopping for school buses · ¶5", "kind": "text", "text": "As well as the upper alternating red flashing lights, school buses use a stop sign arm on the driver’s side of the bus. This arm, a standard stop sign with alternating flashing red lights at top and bottom, swings out after the upper alternating red lights begin to flash. Remain stopped until the arm folds away and all lights stop flashing."}
{"id": "p34", "page": "Stopping", "sec": "Stopping for school buses · ¶6", "kind": "text", "text": "Note: It is illegal to fail to stop for a stopped school bus that has its red lights flashing. If you don't stop, you can be fined heavily and get six demerit points for a first offence. In Ontario, school bus drivers and other witnesses can report vehicles that have illegally passed a school bus. If you are the vehicle’s registered owner, these fines, but not demerit points or jail time, may be applied to you."}
{"id": "p35", "page": "Stopping", "sec": "Stopping for pedestrian crossovers · ¶2", "kind": "text", "text": "Pedestrians may push a button to make the overhead yellow lights flash to warn drivers that they will be crossing. Pedestrians should point or make an indication to drivers that they want to cross before entering the roadway (try making eye contact when possible). Drivers including cyclists must yield the right-of-way to pedestrians in the crossover. Only when pedestrians and school crossing guards have crossed and are safely on the sidewalk can drivers and cyclists proceed. You must not pass any vehicle within 30 metres of a pedestrian crossover."}
{"id": "p36", "page": "Stopping", "sec": "Summary · ¶1", "kind": "text", "text": "By the end of this section, you should know:"}
{"id": "p37", "page": "Stopping", "sec": "Summary · item 3", "kind": "text", "text": "How and when to stop for school crossings and school buses"}
{"id": "p38", "page": "Changing directions", "sec": "Left turns · ¶5", "kind": "text", "text": "Motorcycles, bicycles, limited-speed motorcycles and mopeds turn left at intersections in the same way as larger vehicles. If you are making a left turn behind one of these vehicles, do not pull up beside it to make your turn at the same time. Stay behind and turn when the way is clear. Wait for the smaller vehicle to move right before you pass."}
{"id": "p39", "page": "Changing directions", "sec": "Left-turn lanes · ¶3", "kind": "text", "text": "Remember that vehicles from the opposite direction also use this lane to turn left. As they wait in front of you, it may be hard for you to see oncoming traffic. Only go when you are sure the way is clear. These left-turn lanes are not to be used for passing."}
{"id": "p40", "page": "Changing positions", "sec": "Intro · ¶1", "kind": "text", "text": "Changing your position on the road involves changing lanes or overtaking and passing another vehicle. Before beginning, be sure you have enough space and time to complete the move safely."}
{"id": "p41", "page": "Changing positions", "sec": "Changing lanes · ¶1", "kind": "text", "text": "Changing lanes is a movement from one lane to another on roads with two or more lanes in the same direction. You may have to change lanes to overtake another vehicle, to avoid a parked vehicle or when the vehicle ahead slows to turn at an intersection."}
{"id": "p42", "page": "Changing positions", "sec": "Changing lanes · ¶5", "kind": "text", "text": "Avoid unnecessary lane changes or weaving from lane to lane. You are more likely to cause a collision, especially in heavy traffic or bad weather. Don't change lanes in or near an intersection. Remember that spending a few seconds behind another vehicle is often safer than going around it."}
{"id": "p43", "page": "Changing positions", "sec": "Passing · ¶1", "kind": "text", "text": "Passing is changing lanes to move past a slower vehicle. While all public roads have speed limits, not all vehicles travel at the same speed. For example, cyclists, road service vehicles and drivers ahead that are preparing to turn are usually slower than the through traffic. You may want to pass some slow-moving vehicles when you are following them."}
{"id": "p44", "page": "Changing positions", "sec": "Passing · ¶2", "kind": "text", "text": "Never overtake and pass another vehicle unless you are sure you can do so without danger to yourself or others. Don't pass moving snow plows under any conditions. If in doubt, do not pass."}
{"id": "p45", "page": "Changing positions", "sec": "Passing · ¶3", "kind": "text", "text": "Here are the steps for passing a vehicle:"}
{"id": "p46", "page": "Changing positions", "sec": "Passing · item 1", "kind": "text", "text": "Use your left-turn signal to show that you want to pass and check that the way is clear ahead and behind before moving into the passing lane."}
{"id": "p47", "page": "Changing positions", "sec": "Passing · item 2", "kind": "text", "text": "Watch for bicycles and small vehicles that may be hidden from view in front of the vehicle you are about to pass. Also watch for vehicles that may be turning left in front of you and vehicles or pedestrians entering the road from another road or driveway."}
{"id": "p48", "page": "Changing positions", "sec": "Passing · item 3", "kind": "text", "text": "Change lanes only after signalling. After overtaking, signal that you want to move back into the lane you started from, and when you can see the entire front of the vehicle you are passing in your inside mirror, make the lane change. Be careful not to cut off a vehicle by suddenly moving in front of it."}
{"id": "p49", "page": "Changing positions", "sec": "Passing · item 4", "kind": "text", "text": "If the vehicle you are passing speeds up, do not race. Go back to your original lane. And do not speed up when another driver is trying to pass you. It is unlawful and dangerous."}
{"id": "p50", "page": "Changing positions", "sec": "Passing · image", "kind": "figure", "text": "how to pass another vehicle", "cap": "Diagram 2-46 | Alt text: “how to pass another vehicle”", "image": "images/2-36.jpg"}
{"id": "p51", "page": "Changing positions", "sec": "Passing · ¶4", "kind": "text", "text": "Passing within 30 metres of a pedestrian crossover is not permitted. Passing left of a centreline is not permitted 30 metres from a bridge, viaduct or tunnel. Don't attempt to pass when approaching the crest of a hill or on a curve where your vision of oncoming traffic is obstructed and there is not enough clear distance ahead to pass in safety."}
{"id": "p52", "page": "Changing positions", "sec": "Passing · ¶5", "kind": "text", "text": "When passing parked vehicles, watch carefully for people suddenly opening doors or for doors opened to load and unload."}
{"id": "p53", "page": "Changing positions", "sec": "Passing · ¶6", "kind": "text", "text": "Motorcycles, bicycles, limited-speed motorcycles and mopeds often need to pull to the left or right side of their lane to avoid dangerous road conditions or to be seen by other drivers. Do not take this as an invitation to pass in the same lane. If you do want to pass these vehicles, do so by changing lanes."}
{"id": "p54", "page": "Changing positions", "sec": "Passing · ¶7", "kind": "text", "text": "When faster traffic wants to pass you, move to the right and let it pass in safety. When being passed on an undivided road where the passing driver has pulled into the opposite lane, pay attention to oncoming traffic and move closer to the right side of the lane. Be prepared to slow down to let the passing driver get in front of you more quickly to prevent a collision."}
{"id": "p55", "page": "Changing positions", "sec": "Passing · ¶8", "kind": "text", "text": "On many high-speed roads with three or more lanes in each direction, trucks are not allowed to drive in the far left-hand lane. This means that the lane next to it is the truck passing lane. If you are in this lane and a truck wants to pass, move into the right-hand lane as soon as you can."}
{"id": "p56", "page": "Changing positions", "sec": "Passing · image", "kind": "figure", "text": "how to pass another vehicle", "cap": "Diagram 2-47 | Alt text: “how to pass another vehicle”", "image": "images/2-36.5.jpg"}
{"id": "p57", "page": "Changing positions", "sec": "Passing at night · ¶1", "kind": "text", "text": "Be very careful when you pass other vehicles at night. If you have to pass and the way is clear, follow these steps:"}
{"id": "p58", "page": "Changing positions", "sec": "Passing at night · item 1", "kind": "text", "text": "Switch your headlights to low beams as you approach a vehicle from behind."}
{"id": "p59", "page": "Changing positions", "sec": "Passing at night · item 2", "kind": "text", "text": "Signal, check your mirrors and blind spot, and pull out to pass. As you move alongside the vehicle you are passing, switch on your high beams. This will let you see more of the road ahead."}
{"id": "p60", "page": "Changing positions", "sec": "Passing at night · item 3", "kind": "text", "text": "When you can see all of the front of the vehicle you are passing in your rear view mirror, you are far enough ahead to pull back into the right lane. Remember to signal."}
{"id": "p61", "page": "Changing positions", "sec": "Passing and climbing lanes · image", "kind": "figure", "text": "a passing or climbing lane", "cap": "Diagram 2-48 | Alt text: “a passing or climbing lane”", "image": "images/2-48a.jpg"}
{"id": "p62", "page": "Changing positions", "sec": "Passing and climbing lanes · ¶1", "kind": "text", "text": "Some roads have special passing or climbing lanes. These lanes let slower vehicles move into the right-hand lane so that faster ones can pass safely in the left lane."}
{"id": "p63", "page": "Changing positions", "sec": "Passing and climbing lanes · ¶2", "kind": "text", "text": "An advance sign tells drivers they will soon have a chance to pass. Another sign warns when the lane is ending so drivers in the right-hand lane can begin to merge safely with traffic in the left-hand lane."}
{"id": "p64", "page": "Changing positions", "sec": "Passing on the shoulder · ¶1", "kind": "text", "text": "You may drive on the right shoulder only to pass a vehicle turning left and only if the shoulder is paved. You may not pass on the left shoulder, paved or not."}
{"id": "p65", "page": "Changing positions", "sec": "Passing on the right · ¶1", "kind": "text", "text": "Most passing is done on the left. You may pass on the right on multi-lane or one-way roads and when overtaking a streetcar or a left-turning vehicle."}
{"id": "p66", "page": "Changing positions", "sec": "Passing on the right · ¶2", "kind": "text", "text": "Passing on the right can be more dangerous than passing on the left. If you are driving in the left most lane with a slower vehicle in front of you, wait for the vehicle to move to the right. Do not suddenly change lanes and pass on the right; the driver in front may realize you want to pass and move to the right at the same time you do."}
{"id": "p67", "page": "Changing positions", "sec": "Passing streetcars · image", "kind": "figure", "text": "a vehicle stopped the required two metres behind the rear doors of a stopped streetcar", "cap": "Diagram 2-49 | Alt text: “a vehicle stopped the required two metres behind the rear doors of a stopped streetcar”", "image": "images/2-39.jpg"}
{"id": "p68", "page": "Changing positions", "sec": "Passing streetcars · ¶1", "kind": "text", "text": "You must pass streetcars on the right unless you are driving on a one-way road."}
{"id": "p69", "page": "Changing positions", "sec": "Passing streetcars · ¶2", "kind": "text", "text": "At streetcar stops, stay at least two metres behind the rear doors where passengers are getting off or on. This rule does not apply at stops where an area has been set aside for streetcar passengers. Always pass these areas at a reasonable speed and be prepared for pedestrians to make sudden or unexpected moves."}
{"id": "p70", "page": "Changing positions", "sec": "Summary · ¶1", "kind": "text", "text": "By the end of this section, you should know:"}
{"id": "p71", "page": "Changing positions", "sec": "Summary · item 1", "kind": "text", "text": "The safety considerations and the sequence of steps to follow when changing lanes or passing"}
{"id": "p72", "page": "Changing positions", "sec": "Summary · item 2", "kind": "text", "text": "How to deal with specific situations when passing (for example, at night, streetcars)"}
{"id": "p73", "page": "Freeway driving", "sec": "Driving along a freeway · ¶1", "kind": "text", "text": "Once on the freeway, a safe driver travels at a steady speed, looking forward and anticipating what’s going to happen on the road ahead. Traffic should keep to the right, using the left lanes for passing."}
{"id": "p74", "page": "Freeway driving", "sec": "Driving along a freeway · ¶5", "kind": "text", "text": "Use the far left lane of a multi-lane freeway to pass traffic moving slower than the speed limit, but don't stay there. Drive in the right-hand lane when possible. On many freeways with three or more lanes in each direction, large trucks cannot travel in the far left lane and must use the lane to the right for passing. Get into the habit of driving in the right lane, leaving the other lanes clear for passing."}
{"id": "p75", "page": "Dealing with particular situations", "sec": "Workers on the road · ¶3", "kind": "text", "text": "Other types of workers and vehicles may also be present on the road and pose a hazard, such as roadside assistance and disable vehicles, surveyors, road maintenance or utility workers. Always slow down and pass with caution to prevent a collision. If safe to do so, move over a lane to increase the space between your vehicle and the hazard."}
{"id": "p76", "page": "Dealing with particular situations", "sec": "Reacting to an approaching emergency vehicle · ¶4", "kind": "text", "text": "If you are in an intersection and preparing to make a turn when an emergency vehicle is approaching, you should abandon the turn and clear the intersection by proceeding straight when safe to do so, then pull to the right and stop. This will clear the intersection and minimize the possibility of a collision with the emergency vehicle should it be passing you on the side you intended to turn towards."}
{"id": "p77", "page": "Dealing with particular situations", "sec": "Reacting to an approaching emergency vehicle · ¶5", "kind": "text", "text": "When the emergency vehicle has passed, check to make sure the way is clear and signal before merging back into traffic. Remain vigilant for additional emergency vehicles, and remember it is illegal to follow within 150 metres of a fire vehicle responding to an alarm."}
{"id": "p78", "page": "Dealing with particular situations", "sec": "Reacting to an approaching emergency vehicle · item 3", "kind": "text", "text": "Wait for the emergency vehicle to pass and watch for other emergency vehicles that may be responding to the same call. Check to make sure the way is clear and signal before merging back into traffic."}
{"id": "p79", "page": "Dealing with particular situations", "sec": "Reacting to an approaching emergency vehicle · image", "kind": "figure", "text": "vehicles pulling over to the right to allow emergency vehicle to pass", "cap": "Diagram 2-56 | Alt text: “vehicles pulling over to the right to allow emergency vehicle to pass”", "image": "images/2-46.jpg"}
{"id": "p80", "page": "Dealing with particular situations", "sec": "Reacting to a stopped emergency vehicle or tow truck · image", "kind": "figure", "text": "approaching an emergency vehicle", "cap": "Diagram 2-57 | Alt text: “approaching an emergency vehicle”", "image": "images/diagram2-56.jpg"}
{"id": "p81", "page": "Dealing with particular situations", "sec": "Reacting to a stopped emergency vehicle or tow truck · ¶1", "kind": "text", "text": "When approaching any emergency vehicle that is stopped with its red, or red and blue, lights flashing or a tow truck with its amber lights flashing in the same direction of your travel, you are required to reduce the speed of your vehicle and proceed with caution. When reducing your speed, you are required to assess the speed of the surrounding traffic and the condition of the roadway (such as fog, rain, snow). To ensure safety, brake early and gradually to allow surrounding traffic to better adjust to a reduced speed and to ensure you have full control of your vehicle when braking."}
{"id": "p82", "page": "Dealing with particular situations", "sec": "Reacting to a stopped emergency vehicle or tow truck · ¶2", "kind": "text", "text": "If your vehicle has a manual transmission, it is recommended that you use your brakes, versus shifting down to a lower gear, in order to activate your rear brake lights and indicate to other drivers that you are slowing down."}
{"id": "p83", "page": "Dealing with particular situations", "sec": "Reacting to a stopped emergency vehicle or tow truck · ¶3", "kind": "text", "text": "When the roadway has two or more lanes of traffic in the same direction of your travel, you are required to move into a lane away from the emergency vehicle or tow truck, if safe to do so, in addition to reducing the speed of your vehicle and proceeding with caution. Similar to the procedures noted above, when slowing down and moving over, look in front and on both sides of your vehicle, and check your rearview mirrors, to determine the speed of the traffic around you and condition of the roadway. Proceed to decrease your speed similar to surrounding traffic speed, use your turn signal prior to making the lane change, and double check your rearview mirrors and shoulder check your blind spots to ensure no other vehicles are moving into or approaching that lane too fast. When safe to do so, change lanes well in advance of an emergency vehicle or a stopped tow truck with its flashing amber lights. Once in the lane, brake gradually and continue to reduce the speed of your vehicle when safe to do so. Be aware of any vehicles approaching fast to the rear of your vehicle."}
{"id": "p84", "page": "Dealing with particular situations", "sec": "Reacting to a stopped emergency vehicle or tow truck · item 2", "kind": "text", "text": "Remain calm, and do not make sudden lane changes or brake excessively."}
{"id": "p85", "page": "Dealing with particular situations", "sec": "Reacting to a stopped emergency vehicle or tow truck · item 3", "kind": "text", "text": "Before changing direction or speed, consider road conditions, check surrounding traffic, use your mirrors, look to blind spots, and signal and brake early."}
{"id": "p86", "page": "Dealing with particular situations", "sec": "Reacting to a stopped emergency vehicle or tow truck › Failing to respond to an emergency vehicle · ¶1", "kind": "text", "text": "Take emergency flashing lights and sirens seriously. Proceed with caution, clear the way and bring your vehicle to a stop, where required. It's the law. If you don’t stop, you can be fined and get three demerit points for a first offence. For additional offences, fines increase and you could also go to jail for up to six months."}
{"id": "p87", "page": "Dealing with particular situations", "sec": "Reacting to a stopped emergency vehicle or tow truck › Failing to respond to an emergency vehicle · ¶2", "kind": "text", "text": "Please note the above law, fines and penalties are also applicable to a tow truck with its lamp producing intermittent flashes of amber light that is stopped on a highway."}
{"id": "p88", "page": "Driving at night and in bad weather", "sec": "Fog › Tips for driving safely in fog · ¶1", "kind": "text", "text": "Before you drive - and during your trip - check weather forecasts. If there is a fog warning, delay your trip until it clears. If you are caught driving in fog, follow these safe-driving tips:"}
{"id": "p89", "page": "Driving at night and in bad weather", "sec": "Fog › Tips for driving safely in fog › DO: · item 5", "kind": "text", "text": "Be patient. Avoid passing, changing lanes and crossing traffic."}
{"id": "p90", "page": "Driving at night and in bad weather", "sec": "Fog › Tips for driving safely in fog › Don’t: · item 3", "kind": "text", "text": "Don't speed up to pass a vehicle moving slowly or to get away from a vehicle that is following too closely."}
{"id": "p91", "page": "Driving at night and in bad weather", "sec": "Fog › Tips for driving safely in fog › REMEMBER: · item 3", "kind": "text", "text": "Remain calm and patient. Don't pass other vehicles or speed up suddenly."}
{"id": "p92", "page": "Driving at night and in bad weather", "sec": "Whiteouts › Tips for driving in blowing snow and whiteout conditions · ¶1", "kind": "text", "text": "Before you drive - and during your trip - check weather forecasts and road reports. If there is a weather warning, or reports of poor visibility and driving conditions, delay your trip until conditions improve, if possible. If you get caught driving in blowing snow or a whiteout, follow these safe driving tips:"}
{"id": "p93", "page": "Driving at night and in bad weather", "sec": "Whiteouts › Tips for driving in blowing snow and whiteout conditions › DO: · item 4", "kind": "text", "text": "Be patient. Avoid passing, changing lanes and crossing traffic."}
{"id": "p94", "page": "Driving at night and in bad weather", "sec": "Whiteouts › Tips for driving in blowing snow and whiteout conditions › DON'T: · item 2", "kind": "text", "text": "Don't attempt to pass a vehicle moving slowly or speed up to get away from a vehicle that is following too closely."}
{"id": "p95", "page": "Driving at night and in bad weather", "sec": "Snow plows · ¶2", "kind": "text", "text": "Flashing blue lights warn you of wide and slow-moving vehicles: some snow plows have a wing that extends as far as three metres to the right of the vehicle. On freeways, several snow plows may be staggered across the road, clearing all lanes at the same time by passing a ridge of snow from plow to plow. Do not try to pass between them. This is extremely dangerous because there is not enough room to pass safely, and the ridge of wet snow can throw your vehicle out of control."}
{"id": "p96", "page": "Signs", "sec": "Regulatory signs › Here are some common regulatory signs: · ¶18", "kind": "text", "text": "Do not pass on this road."}
{"id": "p97", "page": "Signs", "sec": "Regulatory signs › Here are some common regulatory signs: · image", "kind": "figure", "text": "a regulatory sign", "cap": "Alt text: “a regulatory sign”", "image": "images/3-1-22.jpg"}
{"id": "p98", "page": "Signs", "sec": "Regulatory signs › Here are some common regulatory signs: · ¶19", "kind": "text", "text": "Slow traffic on multi-lane roads must keep right."}
{"id": "p99", "page": "Signs", "sec": "Regulatory signs › Here are some common regulatory signs: · image", "kind": "figure", "text": "a regulatory sign", "cap": "Alt text: “a regulatory sign”", "image": "images/3-1-23.jpg"}
{"id": "p100", "page": "Signs", "sec": "Regulatory signs › Here are some common regulatory signs: · ¶22", "kind": "text", "text": "Stop for school bus when signals are flashing."}
{"id": "p101", "page": "Signs", "sec": "Regulatory signs › Here are some common regulatory signs: · image", "kind": "figure", "text": "a regulatory sign", "cap": "Alt text: “a regulatory sign”", "image": "images/3-1-25b.jpg"}
{"id": "p102", "page": "Signs", "sec": "Regulatory signs › Here are some common regulatory signs: · ¶23", "kind": "text", "text": "This sign is installed on multi-lane highways with no centre median divider. It informs drivers approaching from both directions that they must stop for a school bus when its signal lights are flashing."}
{"id": "p103", "page": "Signs", "sec": "Regulatory signs › Here are some common regulatory signs: · image", "kind": "figure", "text": "a regulatory sign", "cap": "Alt text: “a regulatory sign”", "image": "images/3-1-26.jpg"}
{"id": "p104", "page": "Signs", "sec": "Regulatory signs › Here are some common regulatory signs: · ¶30", "kind": "text", "text": "Keep to the right lane except when passing on two-lane sections where climbing or passing lanes are provided."}
{"id": "p105", "page": "Signs", "sec": "Regulatory signs › Here are some common regulatory signs: · image", "kind": "figure", "text": "a regulatory sign", "cap": "Alt text: “a regulatory sign”", "image": "images/3-1-33.jpg"}
{"id": "p106", "page": "Signs", "sec": "Regulatory signs › Here are some common regulatory signs: · ¶31", "kind": "text", "text": "This sign on the back of transit buses serves as a reminder to motorists of the law requiring vehicles approaching a bus stopped at a dedicated Bus Stop to yield to the bus, once the bus has signalled its intent to return to the lane."}
{"id": "p107", "page": "Signs", "sec": "Regulatory signs › Here are some common regulatory signs: · image", "kind": "figure", "text": "a regulatory sign", "cap": "Alt text: “a regulatory sign”", "image": "images/3-1-33a.jpg"}
{"id": "p108", "page": "Signs", "sec": "Regulatory signs › Here are some common regulatory signs: · ¶33", "kind": "text", "text": "Marks a zone within which school buses load or unload passengers without using the red alternating lights and stop arm."}
{"id": "p109", "page": "Signs", "sec": "Regulatory signs › Here are some common regulatory signs: · image", "kind": "figure", "text": "a regulatory sign", "cap": "Alt text: “a regulatory sign”", "image": "images/3-1-33c.jpg"}
{"id": "p110", "page": "Signs", "sec": "Temporary condition signs › Here are some common temporary condition signs: · ¶11", "kind": "text", "text": "Do not pass the pilot vehicle or pace vehicle bearing this sign."}
{"id": "p111", "page": "Signs", "sec": "Temporary condition signs › Here are some common temporary condition signs: · image", "kind": "figure", "text": "a temporary condition sign", "cap": "Alt text: “a temporary condition sign”", "image": "images/3-1-83.jpg"}
{"id": "p112", "page": "Signs", "sec": "Other signs › Long commercial vehicle (LCV) · ¶1", "kind": "text", "text": "This placard indicates a long commercial vehicle, which is a double trailer and can be up to 40 metres in length. It is important to be able to recognize an LCV on the highway, based on rear signage, and anticipate both the extended length and limited speed when preparing to pass one on the highway."}
{"id": "p113", "page": "Signs", "sec": "Other signs › Long commercial vehicle (LCV) · image", "kind": "figure", "text": "Title: Long commercial vehicle (LCV) - Description: Long commercial vehicle (LCV)", "cap": "Alt text: “Title: Long commercial vehicle (LCV) - Description: Long commercial vehicle (LCV)”", "image": "images/3-1-101-2a.jpg"}
{"id": "p114", "page": "Pavement markings", "sec": "Intro · ¶1", "kind": "text", "text": "Pavement markings combine with road signs and traffic lights to give you important information about the direction of traffic and where you may and may not travel. Pavement markings divide traffic lanes, show turning lanes, mark pedestrian crossings, indicate obstacles and tell you when it is not safe to pass."}
{"id": "p115", "page": "Pavement markings", "sec": "Intro · ¶3", "kind": "text", "text": "A solid line at the left of your lane means it is unsafe to pass. ('A' should not pass.)"}
{"id": "p116", "page": "Pavement markings", "sec": "Intro · image", "kind": "figure", "text": "vehicles travelling beside a solid yellow line", "cap": "Diagram 3-2 | Alt text: “vehicles travelling beside a solid yellow line”", "image": "images/3-2.jpg"}
{"id": "p117", "page": "Pavement markings", "sec": "Intro · ¶4", "kind": "text", "text": "A broken line at the left of your lane means you may pass if the way is clear. ('A' may pass if there are enough broken lines ahead to complete the pass safely.)"}
{"id": "p118", "page": "Pavement markings", "sec": "Intro · image", "kind": "figure", "text": "vehicles travelling beside broken yellow lines", "cap": "Diagram 3-3 | Alt text: “vehicles travelling beside broken yellow lines”", "image": "images/3-3a.jpg"}
{"id": "p119", "page": "Keeping Your Driver’s Licence", "sec": "Table of offences › Six points · item 5", "kind": "text", "text": "Failing to stop for a school bus"}
{"id": "p120", "page": "Keeping Your Driver’s Licence", "sec": "Table of offences › Three points · item 17", "kind": "text", "text": "Failing to slow and carefully pass a stopped emergency vehicle"}
{"id": "p121", "page": "Keeping Your Driver’s Licence", "sec": "Table of offences › Three points · item 18", "kind": "text", "text": "Failing to move, where possible, into another lane when passing a stopped emergency vehicle"}
{"id": "p122", "page": "Other ways to lose your licence", "sec": "Sanctions – dangerous behaviours · ¶2", "kind": "text", "text": "Other types of aggressive driving include:"}
{"id": "p123", "page": "Other ways to lose your licence", "sec": "Sanctions – dangerous behaviours · item 3", "kind": "text", "text": "driving a motor vehicle to prevent another vehicle from passing"}
{"id": "p124", "page": "Towing", "sec": "Passing · ¶1", "kind": "text", "text": "You cannot accelerate as quickly when you are towing a trailer. You also need more space because the length of your vehicle is much longer with a trailer attached. Before you pass, make sure you have enough time and room to complete the pass. Once you have passed, allow more room before you move back to your lane. Do not cut back into the lane too soon. This can cause your trailer to sway and make it difficult to control."}
{"id": "p125", "page": "Towing", "sec": "Being passed · ¶1", "kind": "text", "text": "If you are holding up a line of traffic, signal, pull over and let the other vehicles pass. Fast-moving trucks and buses create a strong air disturbance behind them. If a large bus or truck passes you, the wall of wind behind it may whip your trailer to the side, pushing it out of control. When you experience this, do not brake. Carefully steer your vehicle and trailer back into position. A slight increase in speed may help."}
{"id": "p126", "page": "Test yourself - Sample knowledge test questions", "sec": "Intro · ¶6", "kind": "text", "text": "5. When the driver of another vehicle is about to overtake and pass your vehicle, you must:"}
{"id": "p127", "page": "Test yourself - Sample knowledge test questions", "sec": "Intro · item 17", "kind": "text", "text": "Speed up so that passing is not necessary."}
{"id": "p128", "page": "Test yourself - Sample knowledge test questions", "sec": "Intro · item 18", "kind": "text", "text": "Move to the left to prevent passing."}
{"id": "p129", "page": "Test yourself - Sample knowledge test questions", "sec": "Intro · item 19", "kind": "text", "text": "Signal to the other driver not to pass."}
{"id": "p130", "page": "Test yourself - Sample knowledge test questions", "sec": "Intro · item 20", "kind": "text", "text": "Move to the right and allow such vehicle to pass."}
{"id": "p131", "page": "The Level Two Road Test", "sec": "Left and right turns › If stopped › Space · ¶1", "kind": "text", "text": "When stopped behind another vehicle at an intersection, leave enough space to pull out and pass without having to back up. Leaving this space protects you in three ways: it lets you pull around the vehicle in front if it stalls; it helps prevent you from being pushed into the vehicle ahead if you are hit from behind; and it reduces the risk of collision if the vehicle ahead rolls backward or backs up."}
{"id": "p132", "page": "The Level Two Road Test", "sec": "Left and right turns › Making the turn › Traffic check · ¶1", "kind": "text", "text": "If you are stopped, waiting for a green light or for the way to be clear, keep checking traffic all around you. Just before entering the intersection, look left, ahead and right to check that the way is clear. If there is any doubt about the right-of-way, try to make eye contact with nearby drivers or pedestrians. If it is possible for another vehicle to overtake you while you are turning, check your blind spot before starting to turn. You have not properly checked traffic if another vehicle or pedestrian has the right-of-way and must take action to avoid your vehicle."}
{"id": "p133", "page": "The Level Two Road Test", "sec": "Stop intersection › The stop › Space · ¶1", "kind": "text", "text": "When stopped behind another vehicle at the intersection, leave enough space to pull out and pass without having to back up. Leaving this space protects you in three ways: it lets you pull around the vehicle in front if it stalls; it helps prevent you from being pushed into the ahead if you are hit from behind; and it reduces the risk of collision if the vehicle ahead rolls backward or backs up."}
{"id": "p134", "page": "The Level Two Road Test", "sec": "Through intersection › Driving through › Lane · ¶1", "kind": "text", "text": "Do not go over lane markings or change lanes in the intersection. If your lane is blocked by a vehicle turning left or a vehicle edging into the intersection from the right, slow down or stop instead of pulling out to go around the vehicle."}
{"id": "p135", "page": "The Level Two Road Test", "sec": "Roadside stop › The approach › Traffic check · ¶1", "kind": "text", "text": "Before slowing down, check your mirrors and scan to see if it is legal (look for signs) to make the roadside stop. Then scan the road for traffic approaching from the front and rear of your of your vehicle. A 150-metre gap in both directions provides enough space to perform the move safely. If there is a chance of traffic or pedestrians overtaking you on the right, check your right blind spot just before pulling over."}
{"id": "p136", "page": "The Level Two Road Test", "sec": "Business section · image", "kind": "figure", "text": "a vehicle stopped the required distance behind a stopped streetcar", "cap": "Diagram 6-8-1 | Alt text: “a vehicle stopped the required distance behind a stopped streetcar”", "image": "images/6-8-1.jpg"}
{"id": "p137", "page": "The Level Two Road Test", "sec": "Business section › Space · ¶1", "kind": "text", "text": "Keep at least a two- to three-second distance behind the vehicle in front of you. Increase the distance if another vehicle follows too closely behind you. On a multi-lane road, try to keep a space on both sides of your vehicle, and try not to drive in the blind spots of other vehicles. In slow traffic, avoid driving behind large vehicles that block your view of traffic ahead of you. When you stop behind another vehicle, leave enough space to see its rear wheels or to pull around it without having to back up."}
{"id": "p138", "page": "The Level Two Road Test", "sec": "Residential section › Space · ¶1", "kind": "text", "text": "Keep at least a two- to three-second distance behind the vehicle in front of you. Increase the distance if another vehicle follows too closely behind you. In slow traffic, avoid driving behind large vehicles that block your view of traffic ahead. When you stop behind another vehicle, leave enough space to see its rear wheels or to pull around it without having to back up."}

Write the statements for this topic as one JSON object, following the system instructions.
