# Freeform error check: `gold_set/mto/overtaking/00_raw_rules.json`

Source: `corpus/mto` · Prompt: `prompts/formal-rules` (system.md, task.md, schema.json) · Topic: overtaking

Quotations from the handbook are given as `id`: "text", and some are trimmed with "…". Image links point to `handbooks/mto/images/`.

**What was checked**

- Every cited block id was resolved against the corpus HTML. They all exist, so there are no dangling citations.
- I scripted checks of the structure: the statement matches its fields, the id matches topic-group-number, numbers run in sequence, force agrees with modal, every CAPS term is in the vocabulary, and every vague term appears in its statement.
- Each rule was read against the text of its cited blocks.
- The cited diagrams were viewed to confirm what the notes say about them:
  - Diagrams: [2-11](../../../handbooks/mto/images/diagram2-11.jpg), [2-46](../../../handbooks/mto/images/2-36.jpg), [2-47](../../../handbooks/mto/images/2-36.5.jpg), [2-48](../../../handbooks/mto/images/2-48a.jpg), [2-57](../../../handbooks/mto/images/diagram2-56.jpg), [2-16](../../../handbooks/mto/images/2-16a.jpg), [3-2](../../../handbooks/mto/images/3-2.jpg).
  - Signs: [18.28](../../../handbooks/mto/images/3-1-22.jpg), [18.36](../../../handbooks/mto/images/3-1-29.jpg), [18.103](../../../handbooks/mto/images/3-1-83.jpg).
- The whole corpus was searched for "pass" and "overtak" to find rules that were left out.

**Result:** 68 rules and 19 vocabulary terms. The JSON fits the schema, and every statement matches its fields word for word. Ids, numbering and force/modal pairs are all valid. The errors found are listed below, grouped by severity.

**Triage:** the major findings were triaged, and fixes were applied to `a0_freeform.json`, which started as an exact copy of `00_raw_rules.json`. Each decision is recorded under its finding as a **Triage** line. All minor findings have now been triaged as well.
- Finding text uses the original rule ids. For open findings, the current id in `a0_freeform.json` is given as "(now …)" where it changed.
- The fixes renumbered the USER group. Old USER-06 is now USER-06 and 07, and old 07–18 are now 08–19. The new brake rule is USER-20, and old 19–21 are now 21–23. GEN-07 and BEING-07 were added at the end of their groups, and the cross-references in notes were updated.
- After all fixes there are 72 rules and 20 vocabulary terms. The scripted checks pass with no warnings: statements match their fields, ids and numbering are valid, force agrees with modal, every CAPS term is in the vocabulary, every vague term appears in its statement, and no condition mixes AND and OR.

Severity: **Major** means the rule says something the handbook does not, misstates its strength, or breaks the grammar or vocabulary contract. **Minor** covers citation, wording, vague-term or ordering issues.

---

## Major

### M1. BLIND SPOT is used but not in the vocabulary (PASS-PROC-01, PASS-USER-19)
`BLIND SPOT` (PROC-01) and `BLIND SPOTS` (USER-19) are written in CAPITALS, but neither has a `vocabulary` entry. task.md requires one for every CAPS term. In PROC-01 the definition was put in the `note` instead ("BLIND SPOT is the area on each side of the vehicle that cannot be seen in the mirrors (4.24)"), and 4.24 is cited as rule evidence.
- `4.24`: "Check and adjust your mirrors and find your blind spots, the area on each side of your vehicle where you cannot see."
- Fix: add `{"term": "BLIND SPOT", "definition": "The area on each side of the vehicle that the driver cannot see.", "evidence": ["4.24"]}`. Remove the definition and the 4.24 citation from PROC-01.
- **Triage: fixed as proposed.** Added the BLIND SPOT vocabulary entry above, with evidence `4.24`. PROC-01's note now reads only "Blind-spot check drawn from the night-passing steps in 10.31.", and its evidence is `["10.17", "10.31"]`.

### M2. A night-only step is applied to every pass (PASS-PROC-01)
The general passing steps say only to signal left and check that the way is clear. The mirror and blind-spot check comes only in the *Passing at night* steps. The rule applies the night step to all passes, and its note admits the source ("drawn from the night-passing steps in 10.31").
- `10.16`: "Here are the steps for passing a vehicle:"
- `10.17`: "Use your left-turn signal to show that you want to pass and check that the way is clear ahead and behind before moving into the passing lane."
- `10.31` (under *Passing at night*): "Signal, check your mirrors and blind spot, and pull out to pass."
- Fix: PROC-01 keeps only the signal and the clear-way check, citing 10.16 and 10.17. Add a NIGHT rule: "WHEN passing at night, the PASSER MUST signal, check the mirrors and BLIND SPOT, and pull out to pass", citing 10.29 and 10.31.
- **Triage: ignored.** Reviewer decision: the blind spot should be checked on every pass. PROC-01 is unchanged on this point.

### M3. Lowercase "not" inside a MUST action mixes a ban with a duty (PROC-07, TOW-04, GEN-05, TOW-02)
- PROC-07: "the PASSER MUST not race it and go back to the original lane". It can be read as "MUST NOT (race and go back)", which forbids the very return that 10.20 orders.
  - `10.20`: "If the vehicle you are passing speeds up, do not race. Go back to your original lane."
- TOW-04: "MUST not brake, and carefully steer…".
  - `27.47`: "When you experience this, do not brake. Carefully steer your vehicle and trailer back into position."
- GEN-05: "MUST use the far left lane only to pass…, and not stay in that lane after passing".
- TOW-02: "MUST allow more room before moving back and not cut back into the lane too soon".

The grammar allows one MODAL per rule, and prohibitions must use `MUST NOT`.
- Fix: split each into a MUST NOT rule and a MUST rule. For example, PROC-07a is "MUST NOT race it" and PROC-07b is "MUST go back to the original lane". TOW-04 becomes "MUST NOT brake" plus "MUST carefully steer the vehicle and trailer back into position".
- **Triage: partly fixed, by rewording instead of splitting.** Only PROC-07 and TOW-04 were changed. They now follow the GEN-05/TOW-02 pattern: the positive phrase comes first and the negated phrase last, so the "not" clearly covers only the last phrase.
  - PROC-07: "WHEN the vehicle being passed speeds up, the PASSER MUST go back to the original lane and not race it."
  - TOW-04: "…the DRIVER towing a trailer MUST carefully steer the vehicle and trailer back into position and not brake."
  - GEN-05 and TOW-02 already follow this pattern and are unchanged.

### M4. A lead-in to a list is turned into a restriction (PASS-NIGHT-02)
`10.29` reads: "Be very careful when you pass other vehicles at night. If you have to pass and the way is clear, follow these steps:". The second sentence only sets up the step list (10.30–10.32). The rule turns it into a restriction: "pass only if the DRIVER has to and the way is clear". The handbook does not say you may pass at night only when you have to. The condition "WHEN at night", with passing tucked into the action, also hides the real trigger.
- Fix: "WHEN passing at night, the DRIVER SHOULD be very careful." Drop "pass only if…" and the "has to" vague term.
- **Triage: fixed as proposed.** NIGHT-02 now reads "WHEN passing at night, the DRIVER SHOULD be very careful." The only vague term left is "very careful"; "has to" and "the way is clear" were removed.

### M5. Advice strength given to a plain command (PASS-USER-04)
`6.38`: "If you feel that you must use your horn, **tap it** quickly and lightly while you are still some distance away from the cyclist." This is a plain command, which the table maps to INSTRUCTION / MUST. The rule records ADVICE / SHOULD, against "Do not turn … an obligation into advice".
- Fix: force `INSTRUCTION`, modal `MUST`.
- **Triage: fixed as proposed.** USER-04 is now INSTRUCTION / MUST, and its statement was rebuilt.

### M6. A requirement and advised wording share one modal (PASS-USER-18)
The action "reduce speed and proceed with caution, braking early and gradually" is tagged REQUIREMENT / MUST. The rule's own note says "braking early is advised wording". Block 13.107 has three separate sentences:
- `13.107`: "…you are **required** to reduce the speed of your vehicle and proceed with caution. When reducing your speed, you are **required** to assess the speed of the surrounding traffic and the condition of the roadway (such as fog, rain, snow). To ensure safety, **brake early and gradually**…"

The braking sentence is separate, and the note itself treats it as weaker. Either it is a separate INSTRUCTION rule, or the note is wrong. As written, the note contradicts the force. The second requirement, assessing traffic speed and road condition, is pushed into the note and not made a rule.
- Fix: split the braking into its own rule, and correct the note.
- **Triage: fixed as proposed.**
  - Old USER-18, now **PASS-USER-19**, keeps "reduce speed and proceed with caution" as REQUIREMENT, with its penalty. Its note now states the duty to assess the speed of surrounding traffic and the road condition, and points to the new rule.
  - New **PASS-USER-20**, "Brake early and gradually for a stopped emergency vehicle or tow truck": INSTRUCTION / MUST, same condition, action "brake early and gradually", vague term "early and gradually", evidence `13.107`, no penalty.

### M7. The exception covers more than the handbook allows (PASS-USER-06)
`9.18`: "If you are making a left turn behind one of these vehicles, do not pull up beside it to make your turn at the same time. Stay behind and turn when the way is clear. Wait for the smaller vehicle to move right before you pass." The rule puts both bans under one exception: "MUST NOT pull up beside it to turn at the same time or pass it, UNLESS the smaller vehicle has moved right". That suggests pulling up beside it to turn at the same time is fine once the smaller vehicle moves right, which the handbook never says.
- Fix: two rules. (a) MUST NOT pull up beside it to turn at the same time, with no exception. (b) MUST NOT pass it, UNLESS the smaller vehicle has moved right.
- **Triage: fixed as proposed.** The rule is split in two, and both parts cite `9.18`.
  - **PASS-USER-06**, "Do not pull beside a smaller vehicle to turn left with it": MUST NOT pull up beside it to make the left turn at the same time, with no exception. It keeps the note "stay behind and turn when the way is clear".
  - **PASS-USER-07**, "Wait for a smaller vehicle to move right before passing": MUST NOT pass it, UNLESS the smaller vehicle has moved right.

### M8. A stronger wording elsewhere is not recorded (PASS-PROC-06)
PROC-06 is ADVICE / SHOULD NOT and cites only 10.19:
- `10.19`: "…**Be careful not to** cut off a vehicle by suddenly moving in front of it."

It ignores stronger passages on the same behaviour:
- `10.10`: "**Never** make sudden lane changes by cutting in front of another vehicle, including bicycles." This is an INSTRUCTION.
- `12.23`: "Be careful not to cut off any vehicle, large or small, when making a lane change or joining the flow of traffic. It is dangerous and **illegal** for a slower moving vehicle to cut in front of a faster moving vehicle." This is a REQUIREMENT.
- `23.23` lists "intentionally cutting off another vehicle" as aggressive driving.

task.md says: "When two passages word the same rule differently, record the stronger wording and say so in `note`."
- Fix: force `INSTRUCTION`, modal `MUST NOT`. Cite 10.10 and 10.19, and note the softer wording of 10.19.
- **Triage: fixed as proposed.** PROC-06 is now INSTRUCTION / MUST NOT, with evidence `["10.10", "10.19"]`. The note records that 10.19 is softer and that the 'Never' of 10.10 was used. It points to the large-vehicle rule, now PASS-USER-08.

### M9. Rules left out
None of these are in the file:
1. **Trucks may not use the far left lane.** This is a REQUIREMENT for truck drivers. It appears only inside the TRUCK PASSING LANE definition, not as a rule.
   - `10.26`: "On many high-speed roads with three or more lanes in each direction, trucks are not allowed to drive in the far left-hand lane. This means that the lane next to it is the truck passing lane."
   - `12.24`: "On many freeways with three or more lanes in each direction, large trucks cannot travel in the far left lane and must use the lane to the right for passing."
   - **Triage: added** as **PASS-GEN-07**, "Trucks keep out of the far left lane": "WHEN on a road that has a TRUCK PASSING LANE, the DRIVER of a truck MUST use the TRUCK PASSING LANE for passing and not drive in the far left lane." It is a REQUIREMENT citing `10.26` and `12.24`, written positive phrase first, negated phrase last, as in M3.
2. **Cyclists may use any part of the lane to discourage passing where the lane is too narrow to share safely.** This is a PERMISSION about being passed, with actor CYCLIST.
   - `6.24`: "Bicycles and mopeds travelling at a lower speed than other traffic are expected to ride about one metre from the curb or parked cars… However, they can use any part of the lane if necessary for safety, such as to:"
   - `6.27`: "Discourage passing where the lane is too narrow to be shared safely"
   - **Triage: added** as **PASS-BEING-07**, "Cyclists may take the lane to discourage unsafe passing": "WHEN travelling slower than other traffic AND the lane is too narrow to be shared safely, the CYCLIST or rider of a moped MAY use any part of the lane to discourage passing." It is a PERMISSION citing `6.24` and `6.27`, with vague term "too narrow to be shared safely". Its note gives the usual one-metre riding position.
3. **Check the blind spot when you might be overtaken.** Both are INSTRUCTIONs about being passed.
   - `29.44`: "If it is possible for another vehicle to overtake you while you are turning, check your blind spot before starting to turn."
   - `29.171`: "If there is a chance of traffic or pedestrians overtaking you on the right, check your right blind spot just before pulling over."
   - **Triage: rejected.** These are not overtaking rules; they are cautions about other vehicles that may overtake.
4. **Right lane ends: merge safely.** This is the regulatory wording of the end-of-passing-lane rule. PASS-SIGN-05 records only the descriptive, weaker version from 10.36, as ADVICE / SHOULD. Either cite 18.70 and raise the rule to REQUIREMENT / MUST, or justify the weaker form in the note.
   - `10.36`: "Another sign warns when the lane is ending so drivers in the right-hand lane can begin to merge safely with traffic in the left-hand lane."
   - `18.70-c` ([sign image](../../../handbooks/mto/images/3-1-55a.jpg)): "Right lane ends ahead. If you are in the right-hand lane, you **must** merge safely with traffic in the lane to the left."
   - **Triage: fixed.** SIGN-05 is raised to REQUIREMENT / MUST, with action "merge safely with traffic in the left-hand lane" and evidence `["10.36", "18.70", "18.70-c"]`. The note records the softer 10.36 wording and the "must" of 18.70.
5. **Drive in the right-hand lane when possible.** This is only partly covered by GEN-05.
   - `12.24`: "Drive in the right-hand lane when possible… Get into the habit of driving in the right lane, leaving the other lanes clear for passing."
   - **Triage: rejected.** This is general lane advice, not directly about overtaking.
6. *(Borderline)* **School bus.** 8.32 calls failing to stop "illegally passed". If passing a stopped school bus counts as within scope, a REQUIREMENT with a penalty is missing (six demerit points, `22.105`: "Failing to stop for a school bus").
   - `8.32`: "It is illegal to fail to stop for a stopped school bus that has its red lights flashing… school bus drivers and other witnesses can report vehicles that have illegally passed a school bus."
   - **Triage: rejected.**

---

## Minor

### Vocabulary
- **V1. PASS has a definition the handbook doesn't give.** The entry adds ", then returning to the original lane", which was copied from the prompt's example and is not in the cited block. It also conflicts with passing on the right, passing on the shoulder, and passing on a multi-lane road, where the driver may not return.
  - `10.14`: "Passing is changing lanes to move past a slower vehicle."
  - **Triage: fixed.** PASS is now defined only as moving past a slower vehicle, using the handbook's wording: "Changing lanes to move past a slower vehicle." The evidence stays `10.14`.
- **V2. SOLID LINE and BROKEN LINE are defined with their position built in** ("…at the left of the driver's lane"). The rules then repeat it: "a SOLID LINE at the left of the DRIVER's lane". The phrase is redundant, and the term can't be used for a line in any other position. The cited blocks state what each line means, not what it is.
  - `21.4`: "A solid line at the left of your lane means it is unsafe to pass." ([Diagram 3-2](../../../handbooks/mto/images/3-2.jpg))
  - `21.6`: "A broken line at the left of your lane means you may pass if the way is clear." ([Diagram 3-3](../../../handbooks/mto/images/3-3a.jpg))
  - **Triage: fixed.** The position was removed, so each term defines only the line. SOLID LINE is now "A continuous painted line on the road." and BROKEN LINE is "A dashed painted line on the road." The position stays in the rule conditions (MARK-01, MARK-02), and the evidence is unchanged.
- **V3. PASSING LANE clashes with lowercase "the passing lane".** PROC-01 says "move into the passing lane", meaning the lane a passer pulls into. The vocabulary defines PASSING LANE as the special passing or climbing lane from 10.35. SIGN-05 also says "PASSING LANE section", so it's unclear whether the term names a lane or a stretch of road.
  - `10.35`: "Some roads have special passing or climbing lanes. These lanes let slower vehicles move into the right-hand lane so that faster ones can pass safely in the left lane."
  - **Triage: not an error, no change.** A lowercase phrase may mean something different from the uppercase vocabulary term. Only the CAPS term is bound by the vocabulary definition.
- **V4. CYCLIST** is defined from 2.71, which states licensing facts and the Highway Traffic Act status of bicycles. It does not define a cyclist. The HTA clause is not part of a definition.
  - `2.71`: "You do not need a licence to ride a bicycle in Ontario; however bicycles are defined as vehicles in the Highway Traffic Act and bicyclists have rights and responsibilities similar to other vehicle operators…"
  - **Triage: fixed.** CYCLIST is now a self-made definition, "A person riding a bicycle.", with empty evidence. The wrong citation of 2.71 was removed.

### Citations
- **C1. List items are cited without the line that introduces them.** task.md says to cite "a list and the line that introduces it".
  - PROC-01 to PROC-07 cite 10.17–10.20 without `10.16` ("Here are the steps for passing a vehicle:").
  - NIGHT-03 and NIGHT-04 cite 10.30 and 10.31 without `10.29` ("…If you have to pass and the way is clear, follow these steps:").
  - **Triage: fixed, for every rule that cites a list item, not only those named above.** Each one now also cites the block that introduces its list, placed just before the first item from that list. New ids are used.
    - `10.16` (passing steps): PROC-01 to PROC-07, BEING-02.
    - `10.29` (night passing steps): PROC-01, PROC-04, PROC-05, NIGHT-03, NIGHT-04.
    - `6.6` (crosswalk list, "Watch for all crosswalks – A crosswalk can be the portion of a roadway that:"): LOC-04.
    - `14.13` (fog tips, "…If you are caught driving in fog, follow these safe-driving tips:"): WX-01, WX-02.
    - `14.63` (whiteout tips, "…If you get caught driving in blowing snow or a whiteout, follow these safe driving tips:"): WX-03.
    - `22.96` (table of offences, "Here are the demerit points for driving offences."): NIGHT-01, USER-19, USER-21.
    - `28.22` (test question, "When the driver of another vehicle is about to overtake and pass your vehicle, you must:"): BEING-02, BEING-03.
    - `23.19` (aggressive-driving list, "Other types of aggressive driving include:"): BEING-03.
    - Already complete, so unchanged: CROSSWALK (6.6), BEING-01 (28.22), BEING-07 (6.24).
- **C2. Captions are irrelevant or missing.**
  - LOC-01 cites caption 18.36-c, which says nothing about passing. The figure 18.36 alone ([sign image](../../../handbooks/mto/images/3-1-29.jpg)), with its "No Passing Here to Crossing" sign, supports the rule.
    - `18.36-c`: "This is a pedestrian crossover. Be prepared to stop and yield right-of-way to pedestrians."
  - Several notes name a diagram by its caption without citing the caption:
    - PROC-05: 10.21-c, [Diagram 2-46](../../../handbooks/mto/images/2-36.jpg)
    - SIGN-04: 10.34-c, [Diagram 2-48](../../../handbooks/mto/images/2-48a.jpg)
    - USER-07: 6.56-c, [Diagram 2-16](../../../handbooks/mto/images/2-16a.jpg)
    - USER-16: 10.43-c, [Diagram 2-49](../../../handbooks/mto/images/2-39.jpg)
    - USER-19: 13.106-c, [Diagram 2-57](../../../handbooks/mto/images/diagram2-56.jpg)
  - **Triage: LOC-01 fixed; the uncited note captions are not an error.**
    - LOC-01 no longer cites `18.36-c`. Its evidence is now `8.37`, `10.22`, `18.36`.
    - The uncited captions are ignored. Something mentioned only in a note, and not in the rule itself, does not need a citation.
- **C3. The 4.65 citation in NIGHT-04 does not support switching to high beams.** 4.65 only excuses a passer from the low-beam rule. The high-beam step is stated only in 10.31.
  - `4.65`: "Use your low beams when you are less than 60 metres behind another vehicle unless you are passing it."
  - `10.31`: "As you move alongside the vehicle you are passing, switch on your high beams. This will let you see more of the road ahead."
  - **Triage: fixed.** NIGHT-04 no longer cites `4.65`; its evidence is now `10.29`, `10.31`. The note drops "Consistent with the exception for passing in 4.65" and reads only "Reason given: lets the PASSER see more of the road ahead."
- **C4. USER-18 (now USER-19) cites 13.106, which is [Diagram 2-57](../../../handbooks/mto/images/diagram2-56.jpg).** The diagram shows a car moving over a lane away from a stopped ambulance. That manoeuvre belongs to old USER-19 (now USER-21), not to slowing down. USER-18 itself rests on 13.107: "…you are required to reduce the speed of your vehicle and proceed with caution."
  - **Triage: fixed.** USER-19 no longer cites `13.106`. The diagram stays cited on USER-21, the move-over rule it shows.
- **C5. The penalties for USER-18 and USER-19 (now USER-19 and USER-21) rest on 13.116–13.118.** The tie is plausible because 13.118 extends the penalties to a *stopped* tow truck. But the note should say where each part comes from: the fine and jail term from 13.117 and 13.118, and the three demerit points from 22.129 and 22.130.
  - `13.116` (heading): "Failing to respond to an emergency vehicle"
  - `13.117`: "…If you don't stop, you can be fined and get three demerit points for a first offence. For additional offences, fines increase and you could also go to jail for up to six months."
  - `13.118`: "Please note the above law, fines and penalties are also applicable to a tow truck with its lamp producing intermittent flashes of amber light that is stopped on a highway."
  - `22.129` / `22.130` (under "Three points"): "Failing to slow and carefully pass a stopped emergency vehicle" / "Failing to move, where possible, into another lane when passing a stopped emergency vehicle"
  - **Triage: fixed.**
    - Citations: after C4, each rule now cites exactly its penalty sources and no unrelated blocks. USER-19 cites `13.107`, `13.117`, `13.118`, `22.96`, `22.129`. USER-21 cites `13.109`, `13.117`, `13.118`, `22.96`, `22.130`, plus the diagram `13.106`.
    - Notes: each note now ends by saying where each part of the penalty comes from. The three demerit points come from the table entry: 22.129 for USER-19, 22.130 for USER-21. The higher fines and jail term for further offences come from 13.117 (under "Failing to respond to an emergency vehicle"), which 13.118 extends to a stopped tow truck.
- **C6. Possible missing penalty.** `22.138` (under "Two points") lists "Failing to obey signs". That could apply to SIGN-01 ([sign 18.28](../../../handbooks/mto/images/3-1-22.jpg)), SIGN-02 ([sign 18.103](../../../handbooks/mto/images/3-1-83.jpg)) and SIGN-03 ([sign 18.40](../../../handbooks/mto/images/3-1-33.jpg)), which rest on regulatory signs. Low confidence, because the handbook does not link the table entry to these signs.
  - **Triage: ignored.** No change.

### Grammar and wording
- **G1. AND/OR mixed with no grouping.**
  - LOC-03: "approaching the crest of a hill OR on a curve, AND the view … is obstructed AND …". The precedence depends on a comma.
    - `10.22`: "Don't attempt to pass when approaching the crest of a hill or on a curve where your vision of oncoming traffic is obstructed and there is not enough clear distance ahead to pass in safety."
  - USER-19 (now USER-21): "…EMERGENCY VEHICLE … OR a tow truck … AND the road has two or more lanes…". This reads as if the two-lane condition applies only to the tow truck.
    - `13.109`: "When the roadway has two or more lanes of traffic in the same direction of your travel, you are required to move into a lane away from the emergency vehicle or tow truck, if safe to do so…"
  - **Triage: fixed, using the grouping the reviewer gave.** The grammar has no brackets, so each condition is now a chain of facts joined by AND. The two alternatives become a single fact joined by a lowercase "or", which cannot be read as splitting the AND chain.
    - LOC-03 is (not enough distance AND vision obstructed) AND (hill OR curve): "WHEN there is not enough clear distance ahead to pass in safety AND the view of oncoming traffic is obstructed AND the DRIVER is approaching the crest of a hill or is on a curve, the DRIVER MUST NOT attempt to pass."
    - USER-21 (old USER-19) is (two or more lanes) AND (emergency vehicle OR tow truck): "WHEN the road has two or more lanes in the DRIVER's direction AND the DRIVER is approaching either an EMERGENCY VEHICLE stopped with its red, or red and blue, lights flashing or a tow truck stopped with its amber lights flashing, the DRIVER MUST move into a lane away from…, UNLESS it is not safe to do so."
- **G2. PROC-05's condition repeats the action:** "WHEN returning to the original lane…, the PASSER MUST NOT move back into the original lane, UNLESS…". The condition should be "after overtaking the vehicle being passed".
  - `10.19`: "After overtaking, signal that you want to move back into the lane you started from, and when you can see the entire front of the vehicle you are passing in your inside mirror, make the lane change."
  - **Triage: fixed as proposed.** PROC-05 now reads "WHEN the PASSER has overtaken the vehicle being passed, the PASSER MUST NOT move back into the original lane, UNLESS the entire front of the passed vehicle can be seen in the inside rear-view mirror." The condition matches PROC-04's wording.
- **G3. GEN-05 adds "only"** ("use the far left lane only to pass"). "Only" is an interpretation and should either be dropped or explained in the note.
  - `12.24`: "Use the far left lane of a multi-lane freeway to pass traffic moving slower than the speed limit, but don't stay there."
  - **Triage: fixed.** "Only" was removed: "…the DRIVER MUST use the far left lane to pass traffic moving slower than the speed limit, and not stay in that lane after passing."
- **G4. GEN-04 leaves out half of 5.13**: the part about keeping to the right on roads that aren't multi-lane.
  - `5.13`: "Keep to the right of the road or in the right-hand lane on multi-lane roads unless you want to turn left or pass another vehicle."
  - **Triage: fixed.** The rule now includes keeping to the right of the road: "WHEN driving on a road, the DRIVER MUST keep to the right of the road, or in the right-hand lane on a multi-lane road, UNLESS turning left OR passing another vehicle."
- **G5. BEING-06 replaces the handbook's wording.** It uses "as soon as possible" and lists the substitute as the vague term. task.md says to keep the handbook's own words.
  - `10.26`: "If you are in this lane and a truck wants to pass, move into the right-hand lane **as soon as you can**."
  - **Triage: not an error, no change.**
- **G6. LOC-07** "the DRIVER MAY ONLY drive on the right shoulder" can be misread as "must drive only on the shoulder". The meaning intended is "the shoulder may be used only in this situation". The note admits the ambiguity, but a clearer action would be better, such as "use the right shoulder to pass".
  - `10.38`: "You may drive on the right shoulder only to pass a vehicle turning left and only if the shoulder is paved."
  - **Triage: fixed, by rephrasing.** The modal stays MAY ONLY, and the action now names the purpose: "WHEN passing a vehicle that is turning left AND the right shoulder is paved, the DRIVER MAY ONLY use the right shoulder to pass that vehicle." The note now spells out the reading: "MAY ONLY here means driving on the right shoulder is allowed in this situation and in no other; it does not require the DRIVER to use the shoulder."

### Vague terms not listed
- USER-19 (now USER-21): "it is not safe to do so" (the exception). `13.109`: "…move into a lane away from the emergency vehicle or tow truck, **if safe to do so**…"
- SIDE-02: "suddenly". `10.41`: "Do not **suddenly** change lanes and pass on the right…"
- GEN-03: "safely". `10.1`: "Before beginning, be sure you have enough space and time to complete the move **safely**."
- USER-02: "it is possible to change lanes". `6.32`: "**Whenever possible**, you should change lanes to pass."
- **Triage: fixed. A vague-term entry was added for each of these:**
  - USER-21: "it is not safe to do so", "does not say what makes moving over unsafe".
  - SIDE-02: "suddenly", "no timing or distance given".
  - GEN-03: "safely", "no criteria given".
  - USER-02: "it is possible to change lanes", "does not say when a lane change is possible".

### Force borderline
- LOC-05 reads as a prohibition ("not allowed"), so REQUIREMENT fits better than INSTRUCTION. The modal does not change.
  - `9.36`: "These left-turn lanes are **not to be used** for passing."
  - **Triage: fixed as proposed.** LOC-05's force is now REQUIREMENT; the modal stays MUST NOT.

### Grouping and ordering
- **O1. Rules are not in handbook order within groups**, which task.md asks for.
  - GEN order: 10.15, 10.15, 10.1, 5.13, 12.20/24, 10.11.
  - USER jumps 6.x → 10.24 → 9.18 → 6.55 → 18.129 → 6.75 → … → 10.15 → 14.89 → 10.23 → ….
  - LOC places 6.8 and 9.36 after the 10.22 rules.
  - **Triage: not an error, no change.** Order within a group doesn't matter much.
- **O2. SIGN-04 and SIGN-05 are passing-lane rules, not sign rules.** They rest on 10.35 and 10.36, quoted under V3 and M9.4. A `LANE` group, or GEN, would fit better.
  - **Triage: not an error, no change.** These rules are fine under SIGN.

### Notes
- **N1. USER-01's note repeats the vocabulary definition** ("Applies to drivers of motor vehicles", which DRIVER already defines as "A person driving a motor vehicle on the road."). Per the earlier goldset decision, vocabulary definitions should not be repeated in notes.
  - **Triage: fixed.** USER-01's note now reads only "Diagram 2-11 shows the 1 metre gap."

---

## Checked and found correct
- All cited ids exist. The figures cited for diagrams show what the notes claim:
  - [Diagram 2-11](../../../handbooks/mto/images/diagram2-11.jpg) shows the 1.0 m gap.
  - [Diagram 2-47](../../../handbooks/mto/images/2-36.5.jpg) shows a lane change to pass a cyclist in a sharrow lane.
  - [Diagram 2-16](../../../handbooks/mto/images/2-16a.jpg) shows 90 m vs 60 m at 80 km/h.
  - [18.36](../../../handbooks/mto/images/3-1-29.jpg) shows the "No Passing Here to Crossing" sign.
  - [18.103](../../../handbooks/mto/images/3-1-83.jpg) reads "WHEN FLASHING".
  - [Diagram 2-57](../../../handbooks/mto/images/diagram2-56.jpg) shows a car moving over away from an ambulance.
- The weather rules sit in the right sections: 14.19, 14.31 and 14.35 are under Fog, and 14.68 and 14.76 are under Whiteouts. The stronger-wording notes in WX-01 and WX-03 are correct.
- NIGHT-01's penalty (two points, 22.135) and USER-01's penalty (fine plus two points, 6.32) match the handbook.
