# Handbook census: labelling guidelines (v0 grammar)

Purpose: label **every sentence** of the MTO Driver's Handbook so we can decide, from data, which keywords and wordings the rule language needs. You are not writing final rules. You are measuring what the handbook says and whether the draft grammar (v0) can express it.

Each input line looks like:

```
[page:block.sentence] (kind; extra context) sentence text
```

- `kind` is `para`, `item` (bullet), `step` (numbered list item), or `caption`.
- `lead` is the sentence that introduced the list, e.g. "Here are the steps for passing a vehicle:".
- Headings appear as `### …` lines. They are context only. Don't label them.

Output **one JSON object per labelled line** (JSONL), keys exactly as below. Keep it compact.

---

## 1. The draft grammar v0 (what "fits" means)

Statement types:
- `DEFINE <term> IS <genus> THAT <differentia> [ALSO CALLED <alias>]`
- `FACT <statement>`: background, how things are, what a sign or marking indicates without directing anyone.
- `<role> <MODAL> <action> [clauses]`: a RULE.
- `TO <goal>: STEP 1 …; STEP 2 …; DONE WHEN <cond>; IF <event> THEN <fallback>`: a PROCEDURE.

Modals (closed set): `MUST`, `MUST NOT`, `MAY`, `SHOULD`, `SHOULD NOT`.
- MUST / MUST NOT / MAY carry legal force.
- SHOULD / SHOULD NOT are advice.
- **Cautions** ("watch for", "be careful of", "be prepared for", "look out for") are written `SHOULD WATCH FOR <hazard>`.
- **Bare imperatives** ("Move to the right", "Never …", "Don't …", "Always …") default to `SHOULD` / `SHOULD NOT`. They become MUST / MUST NOT only when the text itself signals law: must, must not, required, illegal, unlawful, not permitted, not allowed, prohibited, offence, "the law", "it is against the law".

Clauses, usable on any statement:
- `WHEN <situation or event>`
- `WHILE <ongoing state>`
- `ONLY IF <necessary condition>`
- `UNLESS <exception in the same sentence>`
- `BECAUSE <reason>`
- `IF VIOLATED <penalty>`
- `AND` / `OR` / `NOT`

Links between statements: `EXCEPTION TO <rule>` (an exception stated in a different sentence or passage), `SPECIALIZES <rule or procedure>` (a variant).

Conditions and actions are plain English inside this frame. Quantities stay in words, e.g. `within 30 m of a pedestrian crossover`, `at least 2 m behind the rear doors`.

Wording conventions for v0 rewrites:
- Introduce the role with "a" ("a driver"); refer back with "the" ("the driver", "the vehicle").
- Keywords in CAPITALS; everything else lower case.
- Units: m, km, km/h, s.

---

## 2. Keys to output

```json
{"id":"changing-positions:017.1","t":"RULE","role":"driver","m":"MUST_NOT","b":"legal","caut":false,
 "cl":["WHEN","QUANT"],"act":"pass","ent":["pedestrian crossover"],"dim":["location"],
 "fit":"FULL","need":[],"vg":[],"pass":true,
 "v":"a driver MUST NOT pass a vehicle WHEN the driver is within 30 m of a pedestrian crossover"}
```

| key | values | meaning |
|---|---|---|
| `id` | the id in brackets | — |
| `t` | `RULE` · `STEP` · `DEFINE` · `FACT` · `CONSEQ` · `META` | Content type, see §3 |
| `role` | short lower-case noun phrase | Who must act. Default `"driver"` for "you". Examples: `"driver being passed"`, `"cyclist"`, `"pedestrian"`, `"novice driver"`, `"g1 driver"`, `"truck driver"`, `"vehicle owner"`, `"licence applicant"`, `"snowmobile driver"`, `"school bus driver"`. Use `""` for FACT/DEFINE/META. |
| `m` | `MUST` · `MUST_NOT` · `MAY` · `SHOULD` · `SHOULD_NOT` · `NONE` | Modal after applying the §1 rules. "may not" / "cannot" (as prohibition) → `MUST_NOT`. "can" as permission → `MAY`. Cautions → `SHOULD`. |
| `b` | `legal` · `advice` · `imperative` · `permission` · `none` | What in the text gives the modal. `legal` = explicit legal wording (must, required, illegal, not permitted, law, offence). `advice` = should, recommended, avoid, try to, it's a good idea, it is safer. `imperative` = bare imperative, including Never/Don't/Always/Be careful. `permission` = may, can, allowed, permitted. |
| `caut` | true/false | A caution (watch for / be careful / be prepared / look out / be alert). |
| `cl` | list from: `WHEN` `WHILE` `ONLY_IF` `UNLESS` `EXCEPTION_TO` `BECAUSE` `PURPOSE` `IF_VIOLATED` `IF_THEN` `UNTIL` `BEFORE_AFTER` `QUANT` `DEFAULT` | Constructs present in the sentence. `EXCEPTION_TO` = the sentence makes an exception to a rule stated elsewhere ("This rule does not apply …", "However, buses may …"). `PURPOSE` = "to / so that / in order to" giving the goal of the action. `IF_THEN` = an abnormal event and the response ("If your brakes fail, …"). `UNTIL` = keep doing X until Y. `BEFORE_AFTER` = explicit ordering between actions (before, after, once, as soon as, then). `QUANT` = a number threshold (distance, speed, time, count, weight, age, money). `DEFAULT` = a generalisation (usually, most, generally, normally). |
| `act` | short verb phrase, lemma form | The main action, e.g. `"pass"`, `"change lanes"`, `"signal"`, `"stop"`, `"yield"`, `"keep right"`, `"use low beams"`, `"watch for"`. `""` if none. |
| `ent` | list of short nouns | Key things mentioned in the condition or action, normalised singular: `"streetcar"`, `"school bus"`, `"shoulder"`, `"pedestrian crossover"`. Max 4. |
| `dim` | list from: `location` `road_type` `lane` `time_light` `weather_surface` `other_road_user` `own_vehicle` `traffic_control` `driver_state` `licence` `manoeuvre_phase` `emergency` `other` | Kinds of situation the conditions refer to. |
| `fit` | `FULL` · `PARTIAL` · `NONE` | Can v0 express this sentence **without losing meaning**? Try to write `v` first, then judge honestly. |
| `need` | list of short tags | Any construct you needed that v0 lacks, e.g. `"UNTIL"`, `"BEFORE/AFTER"`, `"AT LEAST/AT MOST"`, `"RIGHT-OF-WAY relation"`, `"list/enumeration"`, `"comparative (slower than)"`, `"duty of another role"`, `"definition by list"`, `"time window"`, `"priority between rules"`. Free text but short; reuse the same tag for the same need. |
| `vg` | list of `[code, "exact span"]` | Vague or ambiguous content (codes in §4). |
| `pass` | true/false | Does the sentence concern **passing / overtaking / being passed** (any vehicle, including bicycles, streetcars, school buses, snow plows, trucks, "going around" a vehicle)? |
| `v` | v0 rewrite, one line | Required for RULE, STEP, DEFINE, CONSEQ. Use `""` for FACT and META. |

---

## 3. Content types (`t`)

- **RULE**: directs what some role must, must not, may, should or should not do, including cautions and advice. A sign's meaning that tells drivers what to do ("This sign means you must stop") is a RULE (WHEN the sign …).
- **STEP**: one step of an ordered procedure. Usually a `step` item or a numbered list, sometimes a sentence inside a step. Label each sentence of a multi-sentence step as STEP, unless it is a standalone rule or caution, which you label RULE.
- **DEFINE**: says what a term means, what something is called, or what something is ("Passing is changing lanes to move past a slower vehicle", "A median is a physical barrier…").
- **FACT**: describes the world without directing behaviour: how roads, signs, vehicles or laws are; statistics; why something is dangerous; what a sign indicates when it is purely informational.
- **CONSEQ**: a penalty or legal consequence ("you can be fined", "six demerit points", "your licence will be suspended").
- **META**: learning objectives ("By the end of this section…"), navigation, "For more information visit…", chapter intros about the book itself, fragments with no content (e.g. a lone label "Stop").

---

## 4. Vague / ambiguous codes (`vg`)

| code | when | examples |
|---|---|---|
| `J` | Judgment term: needs human judgment, no threshold | safe, safely, enough, sure, in doubt, reasonable, proper, plenty of room, as soon as you can, carefully, too fast, well before |
| `M` | Modality unclear: can't tell law vs advice; "never/don't" that might be law; "must" that reads like advice | "Don't pass moving snow plows under any conditions" |
| `S` | Hedged scope: hedged quantifier | many, most, some, usually, often, generally, in some areas |
| `R` | Unclear reference or role | "these areas", "the lane next to it", "they" with several candidates, unclear who must act |
| `D` | Implicit default or presupposition the rule depends on, not stated | "You may drive on the right shoulder only to pass…" presupposes shoulder driving is otherwise not allowed |
| `G` | Goal vs sub-action ambiguity: prohibits the goal in one place and the means in another | "passing left of a centreline" vs "passing" |

Use the exact span from the sentence.

---

## 5. Worked examples

```json
{"id":"ex1","t":"DEFINE","role":"","m":"NONE","b":"none","caut":false,"cl":[],"act":"","ent":["passing","lane change"],"dim":[],"fit":"FULL","need":[],"vg":[],"pass":true,"v":"DEFINE passing IS a lane change THAT moves past a slower vehicle"}
{"id":"ex2","t":"RULE","role":"driver","m":"SHOULD_NOT","b":"imperative","caut":false,"cl":["WHEN"],"act":"pass","ent":["snow plow"],"dim":["other_road_user"],"fit":"FULL","need":[],"vg":[["M","Don't pass moving snow plows under any conditions"]],"pass":true,"v":"a driver SHOULD NOT pass a snow plow WHEN the snow plow is moving"}
{"id":"ex3","t":"RULE","role":"driver","m":"SHOULD","b":"imperative","caut":true,"cl":["WHILE"],"act":"watch for","ent":["parked vehicle","door"],"dim":["other_road_user"],"fit":"FULL","need":[],"vg":[],"pass":true,"v":"a driver SHOULD WATCH FOR doors opening suddenly WHILE the driver passes a parked vehicle"}
{"id":"ex4","t":"STEP","role":"driver","m":"SHOULD","b":"imperative","caut":false,"cl":["WHEN","BEFORE_AFTER"],"act":"return to lane","ent":["inside mirror"],"dim":["manoeuvre_phase"],"fit":"FULL","need":[],"vg":[],"pass":true,"v":"STEP signal right; DONE WHEN the entire front of the passed vehicle is visible in the inside mirror"}
{"id":"ex5","t":"RULE","role":"driver","m":"MAY","b":"permission","caut":false,"cl":["ONLY_IF"],"act":"drive on shoulder","ent":["shoulder","left-turning vehicle"],"dim":["lane","other_road_user"],"fit":"FULL","need":[],"vg":[["D","only to pass a vehicle turning left"]],"pass":true,"v":"a driver MAY drive on the right shoulder ONLY IF the driver is passing a vehicle that is turning left AND the shoulder is paved"}
{"id":"ex6","t":"RULE","role":"driver","m":"MUST","b":"legal","caut":false,"cl":["WHEN","UNTIL","QUANT"],"act":"stop","ent":["school bus"],"dim":["other_road_user"],"fit":"PARTIAL","need":["UNTIL"],"vg":[],"pass":true,"v":"a driver MUST stop at least 20 m behind a school bus WHEN the school bus is stopped AND its upper red lights are flashing (… UNTIL the bus moves or the lights stop flashing)"}
{"id":"ex7","t":"CONSEQ","role":"driver","m":"NONE","b":"none","caut":false,"cl":["IF_VIOLATED","QUANT"],"act":"","ent":["demerit point","fine"],"dim":[],"fit":"FULL","need":[],"vg":[],"pass":true,"v":"IF VIOLATED a fine AND 6 demerit points for a first offence"}
{"id":"ex8","t":"FACT","role":"","m":"NONE","b":"none","caut":false,"cl":["DEFAULT"],"act":"","ent":["truck","left lane"],"dim":["road_type","lane"],"fit":"FULL","need":[],"vg":[["S","many high-speed roads"]],"pass":true,"v":""}
{"id":"ex9","t":"META","role":"","m":"NONE","b":"none","caut":false,"cl":[],"act":"","ent":[],"dim":[],"fit":"FULL","need":[],"vg":[],"pass":false,"v":""}
{"id":"ex10","t":"RULE","role":"driver","m":"SHOULD","b":"imperative","caut":false,"cl":["WHEN"],"act":"yield","ent":["cyclist"],"dim":["other_road_user"],"fit":"PARTIAL","need":["RIGHT-OF-WAY relation"],"vg":[],"pass":false,"v":"a driver SHOULD let a cyclist go through the intersection first WHEN the driver is turning right"}
```

Be consistent rather than clever. When unsure between two labels, pick the closer one and add a `vg` flag only if the *text itself* is ambiguous.
