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

Choose the type by what the sentence does, not by how it is phrased. A sentence that says what someone may, must or must not do is a RULE, even when it is written as a description: "Large trucks are not permitted on the HOV lanes" is a rule for truck drivers (`a truck driver MUST NOT …`), and "Snowmobiles may use this road" is a permission (`a snowmobile driver MAY …`). A FACT tells no one what to do.

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

**Topic: passing (overtaking).**

**What passing is.** Passing is driving past another vehicle or road user (a car, truck, bus, streetcar, motorcycle, cyclist, farm vehicle or horse-drawn vehicle) that is ahead of you, either moving in the same direction or stopped in or beside your path, and continuing ahead of it. Being passed is another vehicle doing this to you while you drive.

**What the topic covers.**

- Whether, where, when and how a driver may pass, and the steps for doing it.
- What a driver must or should do instead of passing: stay behind, slow down, stop or wait.
- How to behave while being passed.
- The lanes, road markings and signs that allow or restrict passing, or that exist so that others can pass.
- Penalties for passing offences.
- The definitions and facts these rules depend on.

**What is not passing.** Going by people, animals or objects, and letting a vehicle go by when it is not overtaking you while you drive, are not passing. A sentence that uses the word "pass" in one of these senses is not about the topic.

## 7. Worked examples

These examples come from other parts of a handbook, each with its own small topic. They show the principles above at work. Their statement ids (`ex1a`) are only labels; yours are `s1`, `s2`, ….

## Example 1: A definition and a fact in one passage

Topic: driving in fog

What it shows: One passage, two propositions: a definition and a fact, so two statements. "Can" here describes what fog does; it is not a permission.

Input:

```
[e1] page: Driving at night and in bad weather | heading: Fog · ¶1 | para
Fog is a thin layer of cloud resting on the ground. Fog can reduce visibility for drivers, resulting in difficult driving conditions.
```

Answer:

```json
{
 "passages": [
  {
   "id": "e1",
   "about_topic": true,
   "says": "definition: what fog is; fact: fog reduces visibility"
  }
 ],
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

What it shows: Self-contained: the list item never says "fog", but its heading and lead sentence do, so the condition is written into the statement and both passages are cited. The lead sentence also says things of its own, so it gets its own statements.

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
 "passages": [
  {
   "id": "e2",
   "about_topic": true,
   "says": "rule: check forecasts before and during a trip; rule: delay the trip when there is a fog warning; lead: the tips below apply when driving in fog"
  },
  {
   "id": "e3",
   "about_topic": true,
   "says": "rule: use low-beam headlights when driving in fog (condition from the heading and lead), with its reason"
  }
 ],
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

What it shows: Force comes from the handbook's words, including its section introductions: the captions are plain commands, but the section says these signs must be obeyed, so they are law. The sentence about sign shapes says nothing about the topic and gives no statement.

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
 "passages": [
  {
   "id": "e4",
   "about_topic": true,
   "says": "force: regulatory signs must be obeyed (makes the captions below law); fact: a red circle with a line means not allowed; sign shapes are not about the topic"
  },
  {
   "id": "e5",
   "about_topic": true,
   "says": "rule: do not enter the road where this sign is posted"
  },
  {
   "id": "e6",
   "about_topic": true,
   "says": "figure: the sign that e5 describes"
  },
  {
   "id": "e7",
   "about_topic": true,
   "says": "rule: do not stop between these signs, even for a moment"
  }
 ],
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

What it shows: Faithful force: "Never" alone is advice; "It is illegal" about the same action makes it law. A precise distance in a plain command stays advice, with an M flag. Vague words ("sure") are kept and flagged. Numbers become digits with the handbook's unit.

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
 "passages": [
  {
   "id": "e8",
   "about_topic": true,
   "says": "lead: the items below apply at a railway crossing"
  },
  {
   "id": "e9",
   "about_topic": true,
   "says": "rule: stop at least 5 m from the nearest rail or gate when a train is coming; rule: do not cross until sure the train has passed"
  },
  {
   "id": "e10",
   "about_topic": true,
   "says": "rule: never drive around a lowered or moving gate; it is illegal, so law"
  }
 ],
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

What it shows: An exception in the same passage as its rule becomes an UNLESS clause. Clauses keep their fixed order.

Input:

```
[e11] page: Driving through intersections | heading: Controlled intersections · ¶3 | para
When you approach an intersection on a main road, and the intersection is blocked with traffic, stop before entering the intersection and wait until the traffic ahead moves on. This does not apply if you are turning left or right.
```

Answer:

```json
{
 "passages": [
  {
   "id": "e11",
   "about_topic": true,
   "says": "rule: stop before a blocked intersection and wait until traffic moves, unless turning"
  }
 ],
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

What it shows: Ordered actions toward one goal make one PROCEDURE; each step cites its own passage. A prohibition inside a step that is true whatever the order is also its own RULE, linked to the procedure.

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
 "passages": [
  {
   "id": "e12",
   "about_topic": true,
   "says": "procedure: goal and situation of a roadside stop"
  },
  {
   "id": "e13",
   "about_topic": true,
   "says": "procedure step 1: check mirrors and blind spot before slowing"
  },
  {
   "id": "e14",
   "about_topic": true,
   "says": "procedure step 2: signal before slowing, unless vehicles are waiting to enter; then signal only after passing them"
  },
  {
   "id": "e15",
   "about_topic": true,
   "says": "procedure step 3: steer to the side and stop near the curb; rule: do not stop where you block an entrance or traffic"
  },
  {
   "id": "e16",
   "about_topic": true,
   "says": "procedure step 4: signal off, hazard lights on"
  }
 ],
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

What it shows: Join what belongs together: a duty and its penalty in different paragraphs make one statement. Choose the role each sentence supports. A penalty for not doing something makes doing it law.

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
 "passages": [
  {
   "id": "e17",
   "about_topic": true,
   "says": "rule: a driver must use a seatbelt; rule: passengers must be buckled up"
  },
  {
   "id": "e18",
   "about_topic": true,
   "says": "penalty for the driver's seatbelt rule; rule (law from its penalty): ensure passengers under 16 are buckled"
  }
 ],
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

What it shows: Decide by meaning, not by keywords: "pass" here means the bicycles go by; nobody overtakes. The passage says nothing about passing, so it gives no statement, and the reading note says why.

Input:

```
[e19] page: Sharing the road with other road users | heading: Sharing the road with cyclists · item 6 | item
When turning left, you must stop and wait for oncoming bicycles to pass before turning.
```

Answer:

```json
{
 "passages": [
  {
   "id": "e19",
   "about_topic": false,
   "says": "about waiting for oncoming bicycles before a left turn; \"pass\" means they go by, nobody overtakes"
  }
 ],
 "statements": []
}
```

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
