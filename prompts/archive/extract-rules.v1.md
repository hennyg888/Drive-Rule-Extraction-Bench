# Task: turn driver's handbook passages into rule language v1

You rewrite passages from a driver's handbook as statements in **rule language v1**, a controlled English with fixed keywords. Each statement says exactly one thing. It makes explicit what the handbook leaves implicit: who must act, whether it is law or advice, when it applies, and which words are vague. Every statement keeps the handbook sentences it came from.

You receive one batch of passages from one handbook. Each passage has an id (such as `m17`), the page it is on, its heading path (`Stopping at railway crossings · item 2` means the second list item under the heading "Stopping at railway crossings"; `A › B` means heading B under heading A), its kind (`para` or `text`, `item` for a bullet, `step` for a numbered step, `figure`, `table`), and its text. A figure gives its caption and alt text instead of sentences.

You return one JSON object, `{"statements": [...]}`, and nothing else.

Part A is the rule language. Part B is the method: follow its steps in order. Part C is the topic. Part D is the output format. Part E has worked examples. Part F is the check to run before you answer.

---

# Part A. Rule language v1

{{RULE_LANGUAGE}}

---

# Part B. Method

Work through the batch passage by passage, in order, and run steps 1 to 9 for each one. Then run steps 10 and 11 across all your statements. The illustrations below come from other parts of a handbook on purpose; apply the same reasoning to your topic.

## Step 1. Read the passage with its context

A passage often depends on text outside it. Before writing anything, collect:

1. **The heading path.** Headings often hold the condition. "Use your low-beam headlights." under `Fog › Tips for driving safely in fog › DO:` applies only in fog. "Slow down, listen and look both ways" under `Stopping at railway crossings` applies only at a railway crossing. Every condition a heading gives must end up written in the statement. Some headings only name a subject and give no condition: a rule that holds at all times, filed under a heading like "Heavy traffic or bad weather", does not become a fog-or-traffic rule. Ask whether the sentence would still be true without the heading. If it would not, the heading's condition goes in. When you are unsure, put it in and say so in the note.
2. **Lead sentences.** A sentence ending in a colon ("When you come to a railway crossing, remember:", "Here are the steps for …:", "follow these directions:") passes its condition, role and goal to every item under it, unless an item plainly starts an instruction of its own.
3. **Neighbouring passages.** Words like "they", "these vehicles", "this lane", "this area", "do so", "it" and "this rule" point to something said just before. Replace each with the noun it refers to. If you cannot tell what it refers to, keep the words and flag them R (step 8).
4. **Section-level force.** Some sections make everything under them law: "These signs give a direction that must be obeyed" (regulatory signs), a table of offences, a list of sanctions, "It is against the law to …" before a list. Remember these for step 6.

## Step 2. Decide whether the passage is in scope

Part C says what the topic covers. If the passage says nothing in scope, write no statement for it and move on. Writing nothing is correct for such passages; never invent a rule to produce output. If only part of a passage is in scope, write statements only for that part.

## Step 3. Find the propositions: split and join

A statement holds one proposition: one role, one modal, one set of conditions. Two actions with the same role and conditions may share a statement: `a driver SHOULD slow down AND SHOULD look both ways WHEN …`.

**Split** when:

- one sentence holds two rules, or a rule and a fact: "Fog is a thin layer of cloud … Fog can reduce visibility" gives a DEFINE and a FACT;
- one sentence gives duties to two roles: "You must use your seatbelt … All passengers must be buckled up" gives a rule for the driver and a rule for the passenger;
- a list lead introduces several items that are each an instruction ("Do not pass:" followed by places): each item becomes its own statement, citing the lead and the item.

**Do not split** a list whose items are alternative conditions for one instruction. A lead that ends in "only when:", "only if:", "unless:", "except when:", "when:" or "if:" holds the instruction, and its items are the cases. Write ONE statement, with the items joined by OR inside the clause, citing the lead and every item: "You may turn only when: · the light is green · an arrow shows" is `a driver MAY turn ONLY IF the light is green OR an arrow shows`. One statement per item would contradict itself, because each would say the instruction holds only in that one case.

**Join** when:

- a duty and its penalty are in different sentences or passages: one RULE with `IF VIOLATED`, citing both;
- a sentence makes sense only with its neighbour ("This means you may not stop your vehicle in this area", "Failure to do so …", "However, they can …"): one statement citing both;
- the same rule appears in two passages: one statement citing both. If the two wordings differ, add an X flag that says how. If the two passages give it **different force** (a caption says "must", the paragraph gives advice), keep two statements, each with its own force, and put an X flag on both.

**Ordered steps** make one PROCEDURE, not a rule per step. A list is a procedure when its items are the actions of one manoeuvre in the order they are done: "Here are the steps for …", "follow these steps", or a list under a lead like "When you are going to X:". Whether the list is numbered or bulleted does not decide it, since some handbooks number every list. A numbered list of places, conditions, exceptions or separate rules is not a procedure. A sentence inside a step that holds on its own, whatever the order ("Do not stop where you will block an entrance or other traffic"), also becomes its own RULE, linked to the procedure.

## Step 4. Choose the statement type

Take the first that fits:

1. It says what a term means or what something is called: **DEFINE**. ("Fog is a thin layer of cloud resting on the ground.")
2. It is an ordered sequence of actions toward a goal: **PROCEDURE**.
3. It changes a rule written in a **different** passage:
   - if it grants or imposes something of its own (a later paragraph says certain vehicles "may" do what an earlier one forbids), it is a RULE whose text starts `EXCEPTION TO <id>:`, with `<id>` in `links`;
   - if it only switches the other rule off ("This rule does not apply …" in a later paragraph), it is type **EXCEPTION**, text `EXCEPTION TO <id> WHEN <condition>`, force `null`, with `<id>` in `links`.
   - An exception that changes two rules gets one exception statement per rule, each with its own id.
   An exception inside the same passage as its rule is an `UNLESS` clause, not a separate statement.
4. It tells some role what it must, must not, may, should or should not do, including cautions ("watch for") and advice: **RULE**.
5. Anything else is a **FACT**: how roads, signs, vehicles or laws are; what tends to happen; why something is dangerous; what a sign shows when it directs no one.

"May" or "can" as a possibility ("you may want to …", "… may help", "fog can reduce visibility") is not a permission. Write a FACT, or put it in the note; never a MAY rule.

## Step 5. Name the role

- "You" is `a driver`. Use the most specific role the text supports: `a driver being passed`, `a driver towing a trailer`, `a truck driver`, `a driver of a motor vehicle`, `a driver in the right-hand lane`, `a novice driver`, `a cyclist`, `a passenger`.
- Introduce the role with "a" once, then refer to it with "the": `a driver SHOULD stop at least 5 m from the nearest rail or gate WHEN the driver comes to a railway crossing AND a train is coming`.
- Never write "you" or "your" in a statement. "Your vehicle" becomes "the vehicle"; "your lane" becomes "the driver's lane".
- A rule for someone other than the driver keeps that role. Say in the note why it matters to the topic.
- If you cannot tell who a rule is for, keep your best reading and flag it: `[?a driver] MAY …`, with an R flag on `a driver`.

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
| `text` | Words in the sentence decide it: must, must not, shall, shall not, required, is not permitted, not allowed, illegal, unlawful, prohibited, offence, violation, by law, may, can (permission), may not, cannot (prohibition), should, avoid, it is important to | `text ("must use")`, `text ("may not")`, `text ("Avoid")` |
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
- Read what the word does, not only which word it is:
  - "must" meaning "have to" sets no duty: "If you must drive in fog, …" is the condition `WHEN the driver has to drive in fog`;
  - "may not be able to see" and "you may want to" are possibilities, not a ban or a permission;
  - a legal word on a judgment or mental act ("You must judge whether you have enough space") keeps MUST, with an M flag.
- When the modal comes from a lead sentence ("You should: · not drive past …"), quote the lead's words in `force_from`: `text ("You should: … not drive past")`.
- Never raise force by guessing. "Never … under any conditions" with no legal word stays SHOULD NOT with an M flag. A precise distance in a bare imperative ("stop at least five metres from the nearest rail") stays SHOULD with an M flag.
- `implied` and `default` rules are SHOULD or SHOULD NOT and carry a D flag (or M when the force is the doubt).

## Step 7. Write the action and the conditions

**Action.** A verb phrase in the base form: `stop at least 5 m from the nearest rail or gate`, `use low-beam headlights`, `change lanes`, `move to the right`, `keep right`. Use the topic's one-phrase vocabulary (Part C). A caution is `SHOULD WATCH FOR <hazard>`, with basis `caution`. "Be careful" that names a hazard, in the same or the next sentence, is also `SHOULD WATCH FOR <hazard>`. "Be careful" with no named hazard is `SHOULD <action> with [?extra care]`, flagged J.

**Alternative actions.** The grammar joins actions only with AND. When the handbook offers a choice of actions ("vacate the lane or slow down", "either pass or slow down"), write the choice inside one verb phrase with lowercase "either … or": `a driver SHOULD either pass the other vehicle or slow down WHEN …`.

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

**Numbers.** Write digits and the handbook's own unit, never a converted one: metric handbooks use `m`, `km`, `km/h`, `s`, `cm`; US handbooks use `ft`, `mi`, `mph`, `s`. "Five metres" is `5 m`, "three feet" is `3 ft`, "one-third of a mile" is `1/3 mi`. Keep the comparison words ("at least", "within", "more than", "at most"). Never write a number that is not in the source passages or their headings. If a threshold is missing ("a safe distance"), keep the vague words and flag them; never invent a value.

**Spelling.** Keep the handbook's own spelling (centre or center, signalling or signaling, manoeuvre or maneuver).

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
- A figure (a diagram of the manoeuvre, a sign image) goes into the sources of the statement it illustrates. A figure that illustrates nothing in scope gives no statement. You see only a figure's caption and alt text. If they don't say what the figure shows ("a regulatory sign"), don't guess its content.
- A test or study question can support a statement but never be its only source; questions without their answers say nothing for certain. Say in the note that the source is a test question.
- `note` is one or two sentences when you made a reading decision a reviewer should see: why a sentence gave no MAY rule, why two passages were joined, why a condition came from a heading, a rule for another role, a possibility kept out of the rule. Otherwise `null`.

## Step 10. Link statements

- `EXCEPTION TO <id>` and `SPECIALIZES <id>` put `<id>` in `links` as well as in the text.
- A PROCEDURE for a narrower situation (the same manoeuvre at night, or while towing) `SPECIALIZES` the general one: `TO <narrower goal> SPECIALIZES <id> WHEN <condition>`.
- A RULE taken from a step of a procedure lists the procedure's id in `links`.
- Every id in `links` must be the id of a statement in your answer.

## Step 11. Number and order

Give each statement an id from the outline in Part C: section number, then a letter in order of appearance (`3.4.4a`, `3.4.4b`). A statement that covers several sections of one group (a list of places where passing is restricted) takes the group's number (`3.1a`). Ids must be unique. List statements in the order of their ids.

---

# Part C. Topic

{{TOPIC}}

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

{{EXAMPLES}}

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
