# Extracting rules from a driver's handbook

## 1. Your task

You will read a batch of passages from a driver's handbook. You will rewrite everything they say about one topic as short, structured statements in a controlled language called **rule language v1**. You return one JSON object and nothing else.

The most important requirement is **completeness**. Everything the passages say about the topic must end up in a statement. A rule you leave out is a rule the driving model will never know.

The second most important requirement is **faithfulness**. Each statement must mean exactly what the handbook means: no stronger, no weaker, nothing added, nothing dropped.

## 2. Why we do this

The statements will be used by a driving model: a vision-language-action (VLA) model that looks at the road, decides what to do, and explains why. In every situation it will:

1. **retrieve** the statements that might apply to what it sees;
2. **check the conditions** of each statement against the scene ("is it foggy?", "is the traffic light red?");
3. **decide** what to do, treating law and advice differently;
4. **be checked**: a separate checker tests the chosen action against the legal duties;
5. **cite** the statement and the handbook sentence behind its decision.

The handbook is written for people, who read it from start to finish and fill gaps with common sense. The driving model reads one statement at a time, with no surrounding text. So every statement must have these properties:

| Property | What it means | Why the driving model needs it |
|---|---|---|
| Complete coverage | Every piece of topic content is in some statement | It cannot follow a rule it never received |
| Self-contained | All conditions are written in the statement, including conditions the handbook gives only in a heading, a lead sentence or a neighbouring sentence | It sees the statement alone, so it must know exactly when the statement applies |
| One proposition | One statement says one thing | It retrieves, checks and cites statements one at a time |
| Faithful | Same meaning as the handbook; same strength; no new numbers | A wrong statement is followed as if it were right |
| Force made explicit | Law or advice is stated, with the reason | Law must be obeyed and can be checked; advice is weighed |
| Vague words visible | Words like "safe" or "enough" are kept and marked | It must know where its own judgment is needed |
| Traceable | Each statement quotes the exact handbook sentences it came from | A person or checker can trace every decision back to the handbook |
| Consistent wording | The same thing always has the same name | Conditions are matched to what the model sees by their wording |

Keep these properties in mind. When you are unsure how to write something, choose the version that serves them best.

## 3. The rule language

A statement is one line. It is plain English with a few fixed **keywords** written in CAPITALS. The keywords never change meaning; everything between them is ordinary lower-case English.

### 3.1 The five statement types

| Type | Use it when the handbook… | Pattern | Example |
|---|---|---|---|
| `DEFINE` | says what a term means | `DEFINE <term> IS <kind> THAT <difference> [ALSO CALLED <other name>]` | `DEFINE fog IS a thin layer of cloud THAT rests on the ground` |
| `FACT` | describes how things are, without telling anyone what to do | `FACT <sentence> [clauses]` | `FACT fog can reduce visibility for drivers` |
| `RULE` | tells someone what they must, must not, may, should or should not do | `<role> <MODAL> <action> [clauses]` | `a driver SHOULD use low-beam headlights WHEN driving in fog` |
| `PROCEDURE` | gives actions to be done in order to reach a goal | `TO <goal> [WHEN <condition>]`, then numbered steps | `TO make a roadside stop WHEN …`, step 1, step 2 … |
| `EXCEPTION` | in a separate passage, switches off a rule written elsewhere | `EXCEPTION TO <id> WHEN <condition>` | `EXCEPTION TO s4 WHEN the driver is turning left` |

An exception that gives a permission or duty of its own is written as a RULE that starts `EXCEPTION TO <id>:`. An exception in the same passage as its rule is not a separate statement; it is an `UNLESS` clause of that rule.

### 3.2 How a RULE is built

A RULE has four parts, always in this order: **role, modal, action, clauses**.

```
a driver   SHOULD NOT   cross the track   WHEN the driver comes to a railway crossing AND a train is coming
  role       modal         action                         clause
```

**Role.** Who must act. Write "a driver" the first time and "the driver" after that. Use the most specific role the handbook supports ("a passenger", "a cyclist", "a driver towing a trailer"). Never write "you" or "your".

**Modal.** Exactly one of five:

| Modal | Meaning | Force |
|---|---|---|
| `MUST` | a legal duty | law |
| `MUST NOT` | a legal prohibition | law |
| `MAY` | a legal permission | law |
| `SHOULD` | advice to do | advice |
| `SHOULD NOT` | advice not to do | advice |

A warning to look out for something is written `SHOULD WATCH FOR <hazard>`. Two actions with the same role and conditions may share one statement: `a driver SHOULD slow down AND SHOULD look both ways WHEN …`.

**Action.** A verb phrase in the base form: `stop at least 5 m from the nearest rail or gate`, `use low-beam headlights`, `change lanes`.

**Clauses.** Clauses say when and why the rule applies. Use only these, in this order, each at most once:

| Clause | Meaning | Example |
|---|---|---|
| `WHEN` | the situation or event in which the rule applies | `WHEN there is a fog warning` |
| `WHILE` | a state that lasts for the whole action | `WHILE the gate is down` |
| `ONLY IF` | a condition that must hold (mostly after MAY) | `MAY park ONLY IF the sign allows it` |
| `UNLESS` | an exception written in the same passage | `UNLESS the driver is turning left` |
| `UNTIL` | when the duty ends | `UNTIL the fog clears` |
| `BECAUSE` | the reason or purpose; it never changes when the rule applies | `BECAUSE high beams reflect off the fog` |
| `IF VIOLATED` | the penalty | `IF VIOLATED a fine AND 2 demerit points` |

Join conditions with capital `AND`, `OR` and `NOT`. `AND` binds tighter than `OR`; use parentheses for any other grouping: `WHEN (the road is wet OR the road is icy) AND it is dark`. Lower-case "and" and "or" stay inside a noun phrase ("a gate or barrier"). Write every condition as a short clause with a subject: `WHEN the driver comes to a railway crossing`, not `WHEN railway crossing`.

### 3.3 Grammar

Capitals are keywords. `{ }` means repeat, `[ ]` means optional, `|` means or. Everything in lower case is plain English.

{{GRAMMAR}}

### 3.4 Law or advice

The force of a statement comes from **the handbook's own words**, never from what you believe the law to be.

- It is **law** (MUST, MUST NOT, MAY) when the handbook's words make it a legal duty, a legal prohibition or a legal permission, or when it is in a part of the handbook that says its contents are law (for example, a section that says its signs must be obeyed, or a table of offences). A stated penalty for not doing something also makes doing it law.
- It is **advice** (SHOULD, SHOULD NOT) when the handbook advises, gives a plain command ("do", "don't", "never", "always"), or warns ("watch for", "be careful").
- Read what each word does in its sentence. Words like "may", "can" and "must" are not always modals: "a slight increase in speed may help" states a possibility, and "if you must drive in fog" describes a situation. Neither is a permission or a duty.
- Force belongs to the sentence that has it. A legal word in one sentence makes another sentence law only when it clearly refers to that same action ("Never do X. It is illegal.").
- When you are unsure, keep the weaker force and add an M flag. Never raise force by guessing.

Record the reason in `force_from` as a basis and the deciding words in quotes. The bases are:

| Basis | The force comes from |
|---|---|
| `text` | words in the sentence (must, not permitted, illegal, may, should, avoid…) |
| `imperative` | a plain command with no deciding word |
| `caution` | a warning (watch for, be careful, be prepared) |
| `context` | a heading, section introduction, offence table or penalty |
| `implied` | no instruction is written; it follows from a stated purpose or description |
| `default` | a description that sets an expectation ("most … is done …") |
| `imperative steps` | a PROCEDURE whose steps are commands |

Example: `imperative ("Never")`, `text ("is not permitted")`, `context (Regulatory signs: "These signs give a direction that must be obeyed")`.

### 3.5 Vague words and flags

Keep the handbook's vague words exactly as written. Never replace them with a number. Mark them so the driving model knows its own judgment is needed there.

| Code | Name | Meaning | Where it goes |
|---|---|---|---|
| J | judgment | needs human judgment, no measure given ("safe", "enough", "sure", "reasonable", "as soon as you can") | inline `[?…]` and a flag |
| S | hedged scope | "usually", "often", "most", "many", "some" | inline `[?…]` and a flag |
| R | unclear reference | you cannot tell what or who the words refer to | inline `[?…]` and a flag |
| G | goal and means | the rule restricts one means of doing something, not the thing itself | inline `[?…]` and a flag |
| M | unclear force | you cannot tell whether it is law or advice | flag only |
| D | implicit default | the statement depends on something the handbook does not say | flag only |
| V | wording drift | the handbook names the same thing in different ways | flag only |
| X | stated elsewhere | the same content appears in another passage, possibly differently | flag only |

An inline mark looks like `WHEN it is [?safe] to do so`, and its flag is `{"code": "J", "span": "safe", "note": "No measure of safety is given."}`. The `span` is exactly the text inside the brackets. If you had to rewrite the vague words out of the statement, keep the flag with the handbook's words as its span. Every flag has a short `note` that says what a reader cannot decide.

### 3.6 Wording

- **Numbers**: digits, with the handbook's own unit (`5 m`, `3 ft`, `20 mph`, `1/3 mi`). Never convert units. Never write a number that is not in the passages.
- **One name per thing**: use the handbook's most common name for each thing and keep it in every statement. If the handbook uses two names, choose one and add a V flag.
- **Spelling**: keep the handbook's spelling.
- **Signs**: name a sign by its wording in quotes: `a "do not enter" sign`.

## 4. What you return

One JSON object with two fields, in this order:

```
{"passages": [ ... one entry per input passage ... ],
 "statements": [ ... your statements ... ]}
```

### 4.1 `passages`: your reading notes, written first

Write one entry for **every** passage in the batch, in the order given. This is your plan, and it is how we check that nothing was missed.

| Field | Content |
|---|---|
| `id` | the passage id, such as `"m17"` |
| `about_topic` | `true` if the passage says anything about the topic, or gives a condition, force or definition that a topic statement needs; otherwise `false` |
| `says` | one short line. If `about_topic` is true, list what it says that will become statements ("rule: never cross the track until sure the train has passed; rule: stop at least 5 m away"). If false, say why ("about turning left, not about the topic") |

### 4.2 `statements`

| Field | Content |
|---|---|
| `id` | `"s1"`, `"s2"`, … in the order you write them |
| `type` | `"DEFINE"`, `"FACT"`, `"RULE"`, `"PROCEDURE"` or `"EXCEPTION"` |
| `force` | `"LEGAL"` (MUST, MUST NOT, MAY), `"ADVISORY"` (SHOULD, SHOULD NOT), or `null` for DEFINE, FACT and EXCEPTION |
| `force_from` | basis and quoted words (3.4); `null` when force is `null` |
| `text` | the statement, on one line. For a PROCEDURE, only the `TO …` line |
| `steps` | PROCEDURE only: `{"n": "1", "text": "…", "sources": ["m9"]}` for each step, in order. A branch is `{"n": "IF", "text": "IF … THEN …"}`. Leave `steps` out for other types |
| `sources` | `{"id": "m17", "quote": "…"}` for every passage the statement uses. The quote is copied character for character: the shortest complete sentence or sentences that support the statement |
| `flags` | `{"code": "J", "span": "…", "note": "…"}` for each flag (3.5), or `[]` |
| `links` | ids of statements this one refers to (`EXCEPTION TO`, `SPECIALIZES`, a rule taken from a procedure step), or `[]` |
| `note` | one or two sentences when you made a reading decision a reviewer should see, otherwise `null` |

## 5. How to extract

Follow these steps in order.

**Step 1. Read the whole batch.** Notice the headings, the sentences that end with a colon and introduce a list, and the section introductions. They often carry the conditions and the force for the sentences under them.

**Step 2. Write `passages`.** Go through the passages in order. Read each one sentence by sentence and write what it says about the topic. Decide by meaning, not by keywords. A sentence belongs to the topic when it tells a driver something about the topic, even if it never uses the topic's usual words. A sentence does not belong when it only uses one of those words in a different sense.

**Step 3. Write `statements`.** Follow your `passages` notes, passage by passage. For each thing a passage says:

1. **Type**: what is the sentence doing (defining, describing, telling someone what to do, listing steps, switching off another rule)?
2. **Role**: who must act?
3. **Force**: law or advice, from the handbook's words (3.4).
4. **Action**: what must be done or not done?
5. **Conditions**: when does it apply? Collect the conditions from the sentence, its heading path, the lead sentence above it, and the sentences around it. Then test the statement: *if a driver saw only this statement, would they know exactly when it applies?* If not, a condition is missing.
6. **Vague words**: mark and flag them (3.5).
7. **Sources**: cite every passage you used, including the heading, lead sentence or neighbour that gave a condition or the force, and the figure that shows the rule. Copy the quotes exactly.
8. **Links and note**.

While you write, keep each statement to one proposition:

- **Split** a sentence that says two things (two rules, a rule and a fact, duties for two different roles).
- **Join** sentences that only make sense together: a duty and its penalty, a pronoun ("they", "this", "do so") and what it refers to, a sentence and the exception written right after it. Cite all of them.
- **Lists**: a lead sentence and its items. Ask whether each item says something true on its own. If yes, write one statement per item, each carrying the lead's role, force and conditions. If the items are only alternative cases of one instruction (the lead says "only when:" or "unless:"), write one statement and join the items with OR.
- **Ordered actions toward one goal** make one PROCEDURE. A step that is also true on its own, whatever the order, can also be its own RULE, linked to the procedure.
- **The same content twice**: write it once, cite both passages, and add an X flag if the two passages say it differently.

**Step 4. Check completeness.** Go back through `passages`. Every passage marked `about_topic: true` must be cited by at least one statement, and everything listed in its `says` must appear in a statement. Add any statement you missed.

## 6. Topic

{{TOPIC}}

## 7. Worked examples

These examples come from other parts of a handbook, each with its own small topic. They show the principles above at work. Their statement ids (`ex1a`) are only labels; yours are `s1`, `s2`, ….

{{EXAMPLES}}

## 8. Final check

Before you answer, check:

1. `passages` has one entry for every passage in the batch, in order.
2. Every passage marked `about_topic: true` is cited by a statement, and nothing listed in its `says` is missing.
3. Every statement stands alone: all its conditions are written in it.
4. Every RULE is role, modal, action, clauses, with clauses in the order WHEN, WHILE, ONLY IF, UNLESS, UNTIL, BECAUSE, IF VIOLATED.
5. Every force comes from the handbook's words, and `force` matches the modal.
6. Every vague word is kept and marked, and every `[?…]` has a flag with the same span.
7. Every number is in the passages, in the handbook's unit.
8. Every quote is copied exactly.
9. No "you" or "your" in any statement.

Return only the JSON object.
