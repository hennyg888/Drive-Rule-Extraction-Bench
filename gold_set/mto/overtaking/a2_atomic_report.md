# Atomic check (stage 2): gold_set\mto\overtaking\a1_format.json

Judge: anthropic/claude-opus-5-5 · run folder: `runs\20261117-213614-check-atomic-overtaking-a2` (requests, responses, findings.jsonl, triage.csv) · 72 rules checked, 0 failed calls · $3.8094

**104 findings** (5 major, 99 minor) in 58 rules.

**Proposed triage:** each finding has a **Proposed triage** line under its fix. The decisions follow the rulings from the a0 and a1 triages. All proposed fixes have been applied to `a2_atomic.json`, which started as an exact copy of `a1_format.json`: 41 rules and 2 vocabulary entries (SOLID LINE, SNOW PLOW) changed, with every statement rebuilt from its fields. Stage 1 on `a2_atomic.json` passes all 8 checks with no format errors (72 rules, 20 vocab terms).
- 60 findings are proposed for a fix (some partly or in a changed form), and 44 are proposed as not an error, rejected or ignored.
- Most of the rejections repeat rulings from the a0 triage: lowercase "pass" is allowed; the blind spot is checked on every pass (M2); the positive-then-negated pattern stands in for MUST NOT splits (M3); a note-only mention needs no citation (C2); penalty sources were settled in C5; group choice is not an error (O2); and paraphrasing a vague phrase close to the handbook is fine (G5).
- No rule is split or added, so no ids change.

## PASS-GEN-01: Pass only without danger

> WHEN considering whether to overtake and pass another vehicle, the DRIVER MUST NOT begin the PASS, UNLESS the DRIVER is sure the PASS can be made without danger to the DRIVER or others.

### S2-001. Lowercase "pass" in the condition instead of the defined term PASS

*vocabulary* · minor · medium confidence

The `when` field reads "considering whether to overtake and pass another vehicle". This lowercase phrase names the same manoeuvre as the vocabulary term PASS (10.14: "Passing is changing lanes to move past a slower vehicle"). The `action` field then writes "begin the PASS" in capitals. Using both forms for one concept invites a reader to treat them as different things.

- Fix: when: "considering a PASS of another vehicle"; statement: "WHEN considering a PASS of another vehicle, the DRIVER MUST NOT begin the PASS, UNLESS the DRIVER is sure the PASS can be made without danger to the DRIVER or others."
- **Proposed triage: not an error, no change.** Lowercase "pass" as a verb is allowed (the stage 1 allowlist, `pass`); the CAPS term is used where the rule names the manoeuvre as a noun.

### S2-002. "If in doubt, do not pass" from the same block is not mentioned

*note* · minor · medium confidence

Block 10.15 also says "If in doubt, do not pass." This restates the same rule from the opposite side: the driver must be sure, so doubt forbids the pass. The rule cites 10.15 but leaves `note` empty, so a checker cannot tell whether this sentence was folded into the rule or left out.

- Fix: note: "Block 10.15 also says 'If in doubt, do not pass', which restates this rule; it is folded in here. The snow-plow prohibition in the same block is a separate rule."
- **Proposed triage: not an error, no change.** "If in doubt, do not pass" is its own rule, PASS-GEN-02.

## PASS-GEN-02: If in doubt, do not pass

> WHEN the DRIVER is in doubt about whether a PASS can be made safely, the DRIVER MUST NOT pass.

### S2-003. Action "pass" is not written as the vocabulary term PASS

*vocabulary* · minor · medium confidence

The condition uses the defined term "a PASS", but the action is written in lowercase: "MUST NOT pass". Both mean the manoeuvre defined at 10.14: "Passing is changing lanes to move past a slower vehicle." Writing the same concept in capitals in one place and lowercase in another makes it unclear whether the action means the defined PASS.

- Fix: Set action to "make a PASS". The statement then reads: "WHEN the DRIVER is in doubt about whether a PASS can be made safely, the DRIVER MUST NOT make a PASS."
- **Proposed triage: not an error, no change.** Same as S2-001: lowercase "pass" as a verb is allowed.

### S2-004. Vague word "safely" is not listed in vague_terms

*vague terms* · minor · medium confidence

The condition reads "whether a PASS can be made safely". "Safely" is a judgement left to the driver: no gap, distance or criterion is given. The source wording is also vague (10.15: "…without danger to yourself or others"). Only "in doubt" is listed in vague_terms.

- Fix: Add to vague_terms: {"term": "safely", "explanation": "no criterion for a safe pass given"}.
- **Proposed triage: fix as proposed.** Add `{"term": "safely", "explanation": "no criterion for a safe pass given"}` to GEN-02's vague_terms, as was done for GEN-03 in a0.

## PASS-GEN-04: Keep right except to pass

> WHEN driving on a road, the DRIVER MUST keep to the right of the road, or in the right-hand lane on a multi-lane road, UNLESS turning left OR passing another vehicle.

### S2-005. Left-turn exception narrowed to the turn itself

*faithfulness* · minor · medium confidence

The handbook's exception covers intending to turn left. 5.13 says: "…unless you want to turn left or pass another vehicle." The rule writes the exception as "turning left". A driving model could read that as covering only the moment of the turn. On a multi-lane road, though, the driver has to leave the right-hand lane before the turn to get into position, and the handbook's "want to turn left" allows this.

- Fix: Set unless to "preparing to turn left OR passing another vehicle", and the statement to: "WHEN driving on a road, the DRIVER MUST keep to the right of the road, or in the right-hand lane on a multi-lane road, UNLESS preparing to turn left OR passing another vehicle."
- **Proposed triage: fix as proposed.** unless: "preparing to turn left OR passing another vehicle"; statement: "WHEN driving on a road, the DRIVER MUST keep to the right of the road, or in the right-hand lane on a multi-lane road, UNLESS preparing to turn left OR passing another vehicle."

## PASS-GEN-05: Freeway left lane for passing only

> WHEN driving on a multi-lane FREEWAY, the DRIVER MUST use the far left lane to pass traffic moving slower than the speed limit, and not stay in that lane after passing.

### S2-006. Large-truck exception from 12.24 is missing

*missing exception* · major · high confidence

The rule applies to every DRIVER on a multi-lane FREEWAY and tells them to "use the far left lane to pass". The block it cites carves out large trucks. 12.24: "On many freeways with three or more lanes in each direction, large trucks cannot travel in the far left lane and must use the lane to the right for passing." As written, the rule tells a truck driver to do what the same block forbids.

- Fix: Set unless to "the DRIVER is driving a large truck on a FREEWAY with three or more lanes in each direction where large trucks are not allowed in the far left lane". Statement: "WHEN driving on a multi-lane FREEWAY, the DRIVER MUST use the far left lane to pass traffic moving slower than the speed limit, and not stay in that lane after passing, UNLESS the DRIVER is driving a large truck on a FREEWAY with three or more lanes in each direction where large trucks are not allowed in the far left lane." Alternatively, extract the truck restriction as its own REQUIREMENT rule and reference it in the note.
- **Proposed triage: fix, with an exception that points to GEN-07 instead of the proposed wording.** The truck restriction is already its own rule (PASS-GEN-07, added in a0 M9.1), so GEN-05 only needs an exception that matches it. unless: "the DRIVER is driving a truck on a road that has a TRUCK PASSING LANE"; statement: "WHEN driving on a multi-lane FREEWAY, the DRIVER MUST use the far left lane to pass traffic moving slower than the speed limit, and not stay in that lane after passing, UNLESS the DRIVER is driving a truck on a road that has a TRUCK PASSING LANE." Add to the note: "Trucks barred from the far left lane are covered by PASS-GEN-07."

### S2-007. Rule can be read as requiring all freeway passing in the far left lane

*ambiguity* · minor · medium confidence

The wording "MUST use the far left lane to pass" can be read as saying passing is allowed only in the far left lane, or even that the driver must pass slower traffic. The cited text is broader. 12.20 says traffic uses "the left lanes for passing" (plural). 12.24 says to leave "the other lanes clear for passing". The handbook's point is that the far left lane is for passing and should not be used for cruising. It does not make the far left lane the only place to pass.

- Fix: Reword the action as: "use the far left lane only to pass traffic moving slower than the speed limit, and not stay in that lane after passing". Add a note: "12.20 and 12.24 treat the other left lanes as passing lanes too; this rule restricts use of the far left lane and does not require passing there."
- **Proposed triage: rejected, no change.** Adding "only" undoes a0 G3, where "only" was removed as an interpretation.

### S2-008. "not stay in that lane" is not listed as a vague term

*vague terms* · minor · low confidence

12.24 says "don't stay there", and the rule renders this as "not stay in that lane after passing". Nothing says how soon after the pass the driver must leave the far left lane. vague_terms is empty, although the handbook leaves this timing to the driver's judgement.

- Fix: Add to vague_terms: {"term": "not stay in that lane after passing", "explanation": "no time or distance given for returning to the right after the pass"}.
- **Proposed triage: fix as proposed.** Add `{"term": "not stay in that lane after passing", "explanation": "no time or distance given for returning to the right after the pass"}`.

## PASS-GEN-06: Staying behind is often safer

> WHEN following another vehicle, the DRIVER SHOULD consider staying behind it for a few seconds rather than going around it.

### S2-009. Condition is broader than the handbook's lane-change context

*condition* · minor · medium confidence

The rule fires "WHEN following another vehicle", so it covers all following. The sentence comes from the lane-change passage: 10.11: "Avoid unnecessary lane changes or weaving from lane to lane… Remember that spending a few seconds behind another vehicle is often safer than going around it." The advice is about the moment a driver is weighing a lane change to go around the vehicle ahead, not about following in general.

- Fix: when: "following another vehicle AND considering changing lanes to go around it"; statement: "WHEN following another vehicle AND considering changing lanes to go around it, the DRIVER SHOULD consider staying behind it for a few seconds rather than going around it."
- **Proposed triage: fix as proposed.** when: "following another vehicle AND considering changing lanes to go around it"; statement: "WHEN following another vehicle AND considering changing lanes to go around it, the DRIVER SHOULD consider staying behind it for a few seconds rather than going around it."

### S2-010. Vague words 'consider' and 'often' are not flagged

*vague_terms* · minor · medium confidence

The handbook's qualifier is lost. 10.11 says staying behind "is often safer", which leaves the choice to the driver's judgement. The rule replaces this with the hedge "consider", which is vague because it does not say when staying behind is preferred. Only "a few seconds" is listed in vague_terms, and the note does not say when going around is acceptable.

- Fix: Add to vague_terms: {"term": "consider staying behind it", "explanation": "handbook says only that staying behind is 'often' safer; does not say when going around is acceptable"}.
- **Proposed triage: not an error, no change.** "Consider" is the hedge of the ADVICE wording, not a vague condition, and "often" is not in the statement.

## PASS-GEN-07: Trucks keep out of the far left lane

> WHEN on a road that has a TRUCK PASSING LANE, the DRIVER of a truck MUST use the TRUCK PASSING LANE for passing and not drive in the far left lane.

### S2-011. A prohibition is folded into a MUST action

*grammar* · minor · medium confidence

The action "use the TRUCK PASSING LANE for passing and not drive in the far left lane" puts a prohibition inside a MUST modal. The handbook states two separate duties. 10.26 gives a prohibition: "trucks are not allowed to drive in the far left-hand lane". 12.24 gives a positive duty: "large trucks cannot travel in the far left lane and must use the lane to the right for passing". Writing "MUST … not drive" hides the prohibition from anyone reading the modal field, and the grammar provides MUST NOT for exactly this case. A program that reads the modal would see only an obligation.

- Fix: Split into two rules. PASS-GEN-07: modal "MUST NOT", action "drive in the far left lane", statement "WHEN on a road that has a TRUCK PASSING LANE, the DRIVER of a large truck MUST NOT drive in the far left lane.", evidence ["10.26", "12.24"]. PASS-GEN-08: modal "MUST", when "on a road that has a TRUCK PASSING LANE AND passing", action "use the TRUCK PASSING LANE", statement "WHEN on a road that has a TRUCK PASSING LANE AND passing, the DRIVER of a large truck MUST use the TRUCK PASSING LANE.", evidence ["12.24"].
- **Proposed triage: not an error, no change.** Positive phrase first and negated phrase last is the accepted pattern (a0 M3), and GEN-07 was written that way on purpose.

### S2-012. Actor broadened from large trucks to any truck

*actor* · minor · low confidence

The rule's actor is "DRIVER of a truck". 12.24 names "large trucks", and 10.26 just says "trucks". The more specific wording in 12.24 suggests the restriction targets large trucks, so "a truck" may also be read as covering light trucks or pickups.

- Fix: Set actor to "DRIVER of a large truck" and add to the note: "10.26 says 'trucks'; 12.24 says 'large trucks'."
- **Proposed triage: not an error, no change.** The actor follows 10.26 ("trucks"), and the note already records that 12.24 says "large trucks".

## PASS-PROC-01: Signal left and check before pulling out

> WHEN about to change lanes to pass, the PASSER MUST use the left-turn signal, check the mirrors and BLIND SPOT and check that the way is clear ahead and behind.

### S2-013. A night-only step is applied to every pass

*scope* · major · high confidence

The rule requires the PASSER to "check the mirrors and BLIND SPOT" whenever "about to change lanes to pass". The general passing steps say only 10.17: "Use your left-turn signal … and check that the way is clear ahead and behind before moving into the passing lane." The mirror and blind-spot check comes from 10.31: "Signal, check your mirrors and blind spot, and pull out to pass." That step belongs to the night-passing list, which 10.29 introduces as "Be very careful when you pass other vehicles at night. If you have to pass and the way is clear, follow these steps". Merging the two lists makes a night-only instruction apply to every pass. The cited sections do not support that, and the note admits the mirror and blind-spot check was "drawn from the night-passing steps".

- Fix: Split the rule in two. PASS-PROC-01: when "about to change lanes to pass", action "use the left-turn signal and check that the way is clear ahead and behind before moving into the passing lane", evidence ["10.16","10.17"], note "". Statement: "WHEN about to change lanes to pass, the PASSER MUST use the left-turn signal and check that the way is clear ahead and behind before moving into the passing lane." Then add a separate night rule: when "passing at night AND about to pull out to pass", action "signal and check the mirrors and BLIND SPOT", evidence ["10.29","10.31"]. Statement: "WHEN passing at night AND about to pull out to pass, the PASSER MUST signal and check the mirrors and BLIND SPOT."
- **Proposed triage: ignored, no change.** Same as a0 M2. Reviewer decision: the blind spot should be checked on every pass.

### S2-014. Rule does not say the check comes before moving into the passing lane

*completeness* · minor · low confidence

10.17 says the checks are done "before moving into the passing lane", and 10.19 adds "Change lanes only after signalling." The rule's "when", "about to change lanes to pass", hints at the timing, but the action never says that the lane change must wait until the signal and checks are done. 10.19, which states the ordering outright, is not cited.

- Fix: End the action with "before moving into the passing lane". Either cite 10.19 for the signal-first ordering, or leave that to a separate rule.
- **Proposed triage: not an error, no change.** The condition "about to change lanes to pass" already places the checks before the lane change, and PASS-PROC-03 covers signalling before changing lanes.

## PASS-PROC-02: Watch for hidden and entering road users

> WHEN preparing to pass a vehicle, the PASSER MUST watch for bicycles and small vehicles hidden in front of the vehicle to be passed, vehicles turning left ahead, and vehicles or pedestrians entering the road from another road or driveway.

### S2-015. The handbook's "may be" possibility wording is dropped

*faithfulness* · minor · medium confidence

The handbook asks the driver to watch for road users who might be there. 10.18 says: "Watch for bicycles and small vehicles that **may be** hidden from view in front of the vehicle you are about to pass. Also watch for vehicles that **may be** turning left in front of you…". The rule instead says "bicycles and small vehicles hidden in front of the vehicle to be passed, vehicles turning left ahead". This reads as watching for road users already known to be hidden or turning. The point of the step is to anticipate unseen or possible hazards. The rule also changes "in front of you" to "ahead". These changes do not alter what the driver does, but the wording is less precise.

- Fix: Set action to: "watch for bicycles and small vehicles that may be hidden from view in front of the vehicle being passed, vehicles that may be turning left in front of the PASSER, and vehicles or pedestrians entering the road from another road or driveway". Update the statement to match.
- **Proposed triage: fix as proposed.** action: "watch for bicycles and small vehicles that may be hidden from view in front of the vehicle being passed, vehicles that may be turning left in front of the PASSER, and vehicles or pedestrians entering the road from another road or driveway"; statement updated to match.

## PASS-PROC-03: Change lanes only after signalling

> WHEN making a PASS, the PASSER MUST NOT change lanes, UNLESS the PASSER has signalled.

### S2-016. Overlapping signal-before-moving-out step in 10.17 not cited

*citation* · minor · medium confidence

The rule covers every lane change made during a PASS, including the move out into the passing lane. The handbook also states this signalling requirement for that lane change in the step just before: 10.17: "Use your left-turn signal to show that you want to pass and check that the way is clear ahead and behind before moving into the passing lane." 10.19 adds the return lane change: "After overtaking, signal that you want to move back into the lane you started from…". The rule cites only 10.16 and 10.19, so the second passage stating the same obligation is left out, and nothing explains the overlap. The instructions say a rule drawing on several blocks lists each of them.

- Fix: Add "10.17" to evidence: ["10.16", "10.17", "10.19"]. Set note to: "10.19 states the general requirement 'Change lanes only after signalling'; 10.17 (left-turn signal before moving into the passing lane) and 10.19 (signal before moving back) apply it to the two lane changes of a pass."
- **Proposed triage: fix, citation only.** PROC-03 evidence: ["10.16", "10.17", "10.19"]. No note is needed.

## PASS-PROC-05: Return only when front of passed vehicle visible

> WHEN the PASSER has overtaken the vehicle being passed, the PASSER MUST NOT move back into the original lane, UNLESS the entire front of the passed vehicle can be seen in the inside rear-view mirror.

### S2-017. Diagram 2-46 cited but does not show the mirror condition

*citation* · minor · medium confidence

The rule cites figure "10.21" and its note says "Diagram 2-46 shows the full passing path, pulling out and back in." The image shows only the path of a pass. It does not show the condition the rule states, "the entire front of the passed vehicle can be seen in the inside rear-view mirror". The rule's subject is when to move back, and the text blocks support that: 10.19 "…when you can see the entire front of the vehicle you are passing in your inside mirror, make the lane change" and 10.32 "When you can see all of the front of the vehicle you are passing in your rear view mirror, you are far enough ahead to pull back…". The note also names the caption, but 10.21-c is not cited.

- Fix: Remove "10.21" from evidence and drop the diagram sentence from the note. If the diagram is kept, cite both "10.21" and "10.21-c", and say in the note that it shows only the passing path, not the mirror check.
- **Proposed triage: fix: remove the citation, keep the note.** The diagram does not show the mirror condition, so 10.21 is removed from the evidence, as 18.36-c was removed from LOC-01 in a0 C2. The note's diagram sentence can stay, since something mentioned only in a note needs no citation. Evidence: ["10.16", "10.19", "10.29", "10.32"].

### S2-018. Note omits that the rule merges the general and night passing steps

*note* · minor · medium confidence

The rule draws on two passages that word the condition differently. 10.19 is a general step: "…in your inside mirror, make the lane change." 10.32 is a night step under 10.29 "Be very careful when you pass other vehicles at night": "…in your rear view mirror, you are far enough ahead to pull back into the right lane." The instructions ask the note to record a rule inferred from two places. The note mentions only the diagram.

- Fix: Set note to: "Stated in the general passing steps (10.19, 'inside mirror', worded as a command) and repeated in the night passing steps (10.32, 'rear view mirror', worded as a description of when one is far enough ahead). The positive command 'when you can see … make the lane change' is rendered as a prohibition on returning earlier."
- **Proposed triage: fix, shorter note.** note: "Stated in the general passing steps (10.19, 'inside mirror') and repeated in the night passing steps (10.32, 'rear view mirror'). Diagram 2-46 shows the full passing path, pulling out and back in."

### S2-019. Positive instruction recast as a prohibition without saying so

*strength* · minor · low confidence

The handbook words the step positively. 10.19: "when you can see the entire front of the vehicle you are passing in your inside mirror, make the lane change." The rule turns this into "MUST NOT move back into the original lane, UNLESS …". This is a reasonable reading, since returning earlier would cut in, and it fits 10.19's "Be careful not to cut off a vehicle". However, it is an inference, it is not flagged, and 10.32 is only descriptive ("you are far enough ahead").

- Fix: Keep the MUST NOT … UNLESS form but explain the inference in the note, as in the note fix above. Alternatively, rephrase as: when "the PASSER has overtaken the vehicle being passed AND the entire front of the passed vehicle can be seen in the inside rear-view mirror", modal MUST, action "move back into the original lane after signalling".
- **Proposed triage: not an error, no change.** The MUST NOT … UNLESS form was accepted in a0 G2.

## PASS-PROC-07: Do not race a vehicle that speeds up

> WHEN the vehicle being passed speeds up, the PASSER MUST go back to the original lane and not race it.

### S2-020. Prohibition hidden inside a MUST action

*grammar* · minor · medium confidence

The action "go back to the original lane and not race it" puts a prohibition ("not race") inside a MUST rule. The grammar gives MUST NOT for prohibitions. A checker parsing the modal sees only an obligation, and "it" is a loose reference. Source 10.20: "If the vehicle you are passing speeds up, do not race. Go back to your original lane."

- Fix: Reword the action so the obligation leads and the prohibition is explicit, e.g. action: "go back to the original lane instead of racing the vehicle being passed"; statement: "WHEN the vehicle being passed speeds up, the PASSER MUST go back to the original lane instead of racing the vehicle being passed." Alternatively, split it into a MUST NOT rule ("race the vehicle being passed") and a MUST rule ("go back to the original lane").
- **Proposed triage: not an error, no change.** PROC-07 was reworded to this pattern in a0 M3.

### S2-021. Note omits the ambiguous "It is unlawful" sentence

*note* · minor · medium confidence

Block 10.20 ends: "And do not speed up when another driver is trying to pass you. It is unlawful and dangerous." "It is unlawful" most naturally refers to speeding up when being passed, but it could be read as also covering racing. Under that reading the force would be REQUIREMENT, not INSTRUCTION. The note is empty, so a checker gets no warning about this reading or about the separate being-passed rule in the same block.

- Fix: Set note to: "Block 10.20 also says not to speed up when being passed (a separate rule) and adds 'It is unlawful and dangerous', which most naturally refers to that sentence. The racing instruction is therefore kept as INSTRUCTION."
- **Proposed triage: not an error, no change.** "It is unlawful" belongs to the being-passed sentence, which is its own rule (PASS-BEING-02, REQUIREMENT).

## PASS-NIGHT-02: Be very careful passing at night

> WHEN passing at night, the DRIVER SHOULD be very careful.

### S2-022. Passing is written in lowercase and the actor is the generic DRIVER

*vocabulary* · minor · low confidence

The rule says "WHEN passing at night, the DRIVER SHOULD be very careful." The handbook passage is about overtaking: 10.29 "Be very careful when you pass other vehicles at night." In this rule set, a pass is the defined term PASS, and the driver making it is PASSER (the instructions' own example defines both). Writing "passing" in lowercase and using the generic DRIVER leaves the situation less formal than the defined terms allow. It also drops "other vehicles", the object of the pass. The meaning does not change.

- Fix: Set actor to "PASSER", when to "making a PASS of another vehicle at night" and statement to "WHEN making a PASS of another vehicle at night, the PASSER SHOULD be very careful." Make sure PASS and PASSER are in the vocabulary.
- **Proposed triage: not an error, no change.** NIGHT-02's wording was set in a0 M4, and lowercase "passing" is allowed.

## PASS-NIGHT-03: Low beams on approach at night

> WHEN passing at night AND approaching the vehicle to be passed from behind, the PASSER MUST switch the headlights to low beams.

### S2-023. Handbook's 'way is clear' condition omitted

*condition* · minor · medium confidence

The handbook introduces the night-passing steps with a condition: 10.29: "If you have to pass and the way is clear, follow these steps:". The rule's `when` is only "passing at night AND approaching the vehicle to be passed from behind". It drops "the way is clear", so the procedure reads as applying before that check has been made. The action itself is unchanged.

- Fix: when: "passing at night AND the way is clear AND approaching the vehicle to be passed from behind"; statement: "WHEN passing at night AND the way is clear AND approaching the vehicle to be passed from behind, the PASSER MUST switch the headlights to low beams."; add vague_terms entry {"term": "the way is clear", "explanation": "no gap or sight distance given"}.
- **Proposed triage: rejected, no change.** In a0 M4, "If you have to pass and the way is clear" was treated as the lead-in to the step list, not a condition of each step.

### S2-024. Timing of the switch left vague but not listed

*vague_terms* · minor · medium confidence

10.30 says to switch to low beams "as you approach a vehicle from behind" and gives no distance or point at which to switch. The rule keeps this as "approaching the vehicle to be passed from behind" but `vague_terms` is empty, so the open judgement is not flagged for the driving model.

- Fix: Add to vague_terms: {"term": "approaching the vehicle to be passed from behind", "explanation": "no distance given for when to switch to low beams"}.
- **Proposed triage: fix as proposed.** Add `{"term": "approaching the vehicle to be passed from behind", "explanation": "no distance given for when to switch to low beams"}`.

## PASS-NIGHT-04: High beams when alongside at night

> WHEN passing at night AND moving alongside the vehicle being passed, the PASSER MUST switch on the high-beam headlights.

### S2-025. Defined term PASS written in lowercase

*vocabulary* · minor · medium confidence

The rule's actor is PASSER, defined as "The driver making a PASS", so PASS is a defined term. The condition still writes "passing at night" in lowercase. A reader cannot tell whether this means the defined PASS manoeuvre or passing in some looser sense.

- Fix: when: "making a PASS at night AND moving alongside the vehicle being passed"; statement: "WHEN making a PASS at night AND moving alongside the vehicle being passed, the PASSER MUST switch on the high-beam headlights."
- **Proposed triage: not an error, no change.** Lowercase "passing" is allowed.

### S2-026. Night step list's 'way is clear' condition dropped

*condition* · minor · low confidence

The handbook makes the whole night-passing procedure conditional: 10.29: "If you have to pass and the way is clear, follow these steps:". The rule leaves out "the way is clear". That condition is largely implied by a pass already being under way, so the effect is small. Still, the steps, including switching to high beams in 10.31, are only given for a pass where the way is clear.

- Fix: Add the condition: when: "passing at night AND the way is clear AND moving alongside the vehicle being passed". Add a vague_terms entry {"term": "the way is clear", "explanation": "no gap or sight distance given"}. Alternatively, add to the note: "Step of the night-passing procedure that 10.29 introduces with 'If you have to pass and the way is clear'."
- **Proposed triage: rejected, no change.** Same as S2-023.

## PASS-LOC-01: No passing near a pedestrian crossover

> WHEN within 30 metres of a PEDESTRIAN CROSSOVER, the DRIVER MUST NOT pass any vehicle.

### S2-027. Actor DRIVER may be narrower than the crossover passing ban

*actor* · minor · low confidence

The vocabulary defines DRIVER as "A person driving a motor vehicle on the road." The paragraph containing the passing ban treats cyclists as drivers: 8.37: "Drivers including cyclists must yield the right-of-way to pedestrians in the crossover… You must not pass any vehicle within 30 metres of a pedestrian crossover." 10.22 states the ban without naming any vehicle type: "Passing within 30 metres of a pedestrian crossover is not permitted." The sign at 18.36 ("NO PASSING HERE TO CROSSING") is also addressed to all traffic. With the actor limited to motor-vehicle drivers, the rule may be narrower than the handbook. This reading is uncertain, because the "You" in 8.37 could mean only the motor-vehicle driver reading the handbook.

- Fix: Either keep DRIVER and add a note: "8.37 groups cyclists with drivers ('Drivers including cyclists must yield…') just before the passing ban, and 10.22 names no vehicle type, so the ban may also apply to cyclists." Or set actor to "DRIVER or CYCLIST" if a CYCLIST term is defined, and update statement to: "WHEN within 30 metres of a PEDESTRIAN CROSSOVER, the DRIVER or CYCLIST MUST NOT pass any vehicle."
- **Proposed triage: not an error, no change.** Low confidence. The handbook's "You" addresses the reader as a driver, and DRIVER matches.

## PASS-LOC-02: No passing left of centreline near bridges and tunnels

> WHEN within 30 metres of a bridge, viaduct or tunnel, the DRIVER MUST NOT pass to the left of the centreline.

### S2-028. "30 metres from" silently read as "within 30 metres"

*note* · minor · medium confidence

The handbook says 10.22: "Passing left of a centreline is not permitted 30 metres from a bridge, viaduct or tunnel." It does not say "within". The rule writes "within 30 metres of a bridge, viaduct or tunnel". This is the most plausible reading, and it matches the crossover sentence just before it ("within 30 metres of a pedestrian crossover"). Still, it is an interpretation of wording that could be read two ways, and the `note` is empty. The instructions ask for exactly this kind of wording to be flagged in `note`.

- Fix: Set note to: "The handbook says 'not permitted 30 metres from a bridge, viaduct or tunnel'; read as 'within 30 metres of', by analogy with the crossover rule in the same block."
- **Proposed triage: fix as proposed.** LOC-02 note: "The handbook says 'not permitted 30 metres from a bridge, viaduct or tunnel'; read as 'within 30 metres of', by analogy with the crossover rule in the same block."

## PASS-LOC-03: No passing at hill crests or blind curves

> WHEN there is not enough clear distance ahead to pass in safety AND the view of oncoming traffic is obstructed AND the DRIVER is approaching the crest of a hill or is on a curve, the DRIVER MUST NOT attempt to pass.

### S2-029. Vague terms list leaves out 'approaching' and 'in safety'

*vague terms* · minor · medium confidence

The statement keeps several handbook judgement words, but `vague_terms` lists only "not enough clear distance ahead". The statement says "the DRIVER is approaching the crest of a hill", and "approaching" gives no distance from the crest. It also says "to pass in safety", which gives no safety margin or criterion. Both come from 10.22: "Don't attempt to pass when approaching the crest of a hill or on a curve … there is not enough clear distance ahead to pass in safety." Neither is defined in the vocabulary, so the driving model is not told that these are left to the driver's judgement.

- Fix: Set vague_terms to: [{"term": "not enough clear distance ahead", "explanation": "distance not given"}, {"term": "to pass in safety", "explanation": "no safety margin or criterion given"}, {"term": "approaching the crest of a hill", "explanation": "no distance from the crest given"}]
- **Proposed triage: fix as proposed.** vague_terms: "not enough clear distance ahead" (distance not given), "to pass in safety" (no safety margin or criterion given), "approaching the crest of a hill" (no distance from the crest given).

## PASS-LOC-07: Right shoulder only for passing a left-turner

> WHEN passing a vehicle that is turning left AND the right shoulder is paved, the DRIVER MAY ONLY use the right shoulder to pass that vehicle.

### S2-030. MAY ONLY action wording can be read as forcing left-turners to be passed only via the shoulder

*clarity* · minor · medium confidence

Block 10.38 says: "You may drive on the right shoulder only to pass a vehicle turning left and only if the shoulder is paved." The word "only" limits when shoulder driving is allowed. The rule's statement, "the DRIVER MAY ONLY use the right shoulder to pass that vehicle", attaches ONLY to the means of passing instead. Read alone, it says that when passing a left-turner on a paved-shoulder road, the shoulder is the only way the driver may pass. That is not what the handbook says. The note gives the intended reading, but the statement itself is ambiguous. Because the condition already includes "passing a vehicle that is turning left", the action "to pass that vehicle" also repeats it.

- Fix: Make the restricted activity the action and keep the purpose and paving in the condition. Set when: "the DRIVER is passing a vehicle that is turning left AND the right shoulder is paved"; action: "drive on the right shoulder"; statement: "WHEN the DRIVER is passing a vehicle that is turning left AND the right shoulder is paved, the DRIVER MAY ONLY drive on the right shoulder." Keep the note: "Driving on the right shoulder is allowed only in this situation; the rule does not require using the shoulder."
- **Proposed triage: not an error, no change.** The wording and the note were settled in a0 G6.

## PASS-MARK-01: Solid line: unsafe to pass

> WHEN there is a SOLID LINE at the left of the DRIVER's lane, the DRIVER SHOULD NOT pass.

### S2-031. SOLID LINE definition is not a longitudinal lane line and is not defined in its cited blocks

*vocabulary* · minor · medium confidence

SOLID LINE is defined as "A continuous painted line on the road." That also covers lines painted across the road, such as stop lines (21.10: "A stop line is a single white line painted across the road…") and crosswalk lines. The rule only means a lane line running alongside the lane. The cited blocks also do not define the term: 21.4 says only what a solid line means for passing ("A solid line at the left of your lane means it is unsafe to pass"), and the figure 21.5 just shows one. The evidence suggests a handbook definition that does not exist.

- Fix: Change the vocabulary entry to: {"term": "SOLID LINE", "definition": "A continuous (unbroken) painted line running along the road that marks the edge of a traffic lane.", "evidence": []}. Alternatively keep ["21.4", "21.5"] as illustration and say in the rule's note that the handbook does not define the term.
- **Proposed triage: partly: keep the definition, empty the evidence.** The definition was set in a0 V2 (define the line only). 21.4 and 21.5 say what the line means, not what it is, so by the CYCLIST ruling (a0 V4) the self-made definition takes empty evidence. SOLID LINE evidence: [].

### S2-032. "pass" is a key term left undefined and in lowercase

*vocabulary* · minor · low confidence

The action is "pass" in lowercase. No PASS term appears among the vocabulary this rule uses, so the rule does not say what manoeuvre is discouraged. The extractor's own example treats PASS as a defined key term ("Changing lanes to move past a slower vehicle, then returning to the original lane"). Without it, a reader cannot tell whether moving past a vehicle without crossing the line is covered.

- Fix: Use the defined term: action "PASS", statement "WHEN there is a SOLID LINE at the left of the DRIVER's lane, the DRIVER SHOULD NOT PASS." Make sure the vocabulary includes {"term": "PASS", "definition": "Changing lanes to move past a slower vehicle, then returning to the original lane."} with its handbook evidence.
- **Proposed triage: not an error, no change.** Lowercase "pass" as a verb is allowed, and PASS is in the vocabulary.

## PASS-MARK-02: Broken line: passing allowed

> WHEN there is a BROKEN LINE at the left of the DRIVER's lane AND the way is clear AND enough BROKEN LINE remains ahead to complete the PASS safely, the DRIVER MAY pass.

### S2-033. Vague word "safely" is not listed in vague_terms

*vague terms* · minor · medium confidence

The condition ends "to complete the PASS safely", taken from 21.6: "('A' may pass if there are enough broken lines ahead to complete the pass safely.)" The handbook does not say what counts as a safe completion: no clearance or gap is given. The instructions require each vague word in the statement to be listed. The listed term "enough BROKEN LINE remains ahead" does not include "safely".

- Fix: Add to vague_terms: {"term": "safely", "explanation": "no margin or gap for a safe completion given"}. Or widen the existing entry to {"term": "enough BROKEN LINE remains ahead to complete the PASS safely", "explanation": "length of line and safety margin not given"}.
- **Proposed triage: fix, by widening the existing entry.** Replace "enough BROKEN LINE remains ahead" with `{"term": "enough BROKEN LINE remains ahead to complete the PASS safely", "explanation": "length of line and safety margin not given"}`.

### S2-034. BROKEN LINE definition also covers continuity lines

*vocabulary* · minor · low confidence

BROKEN LINE is defined as "A dashed painted line on the road." That definition also covers continuity lines, which 21.8 calls "Broken lines that are wider and closer together than regular broken lines". On the left, continuity lines mean "the lane you are in is ending or exiting", not that passing is allowed. Read with this definition, the rule could treat continuity lines on the left as permission to pass. Block 21.6 is about regular broken lines.

- Fix: Change the BROKEN LINE definition to: "A regular dashed painted line on the road separating lanes, not including continuity lines (wider, closer-spaced broken lines)." Keep evidence ["21.6", "21.7"], or add "21.8" for the exclusion.
- **Proposed triage: not an error, no change.** Vocabulary definitions define only the thing itself (a0 V2). Continuity lines are a separate marking and no rule refers to them.

## PASS-SIGN-01: Do-not-pass sign

> WHEN on a road posted with a do-not-pass sign, the DRIVER MUST NOT pass.

### S2-035. Rule omits the block that gives the sign its meaning and force

*citation* · minor · medium confidence

The rule is REQUIREMENT / MUST NOT because the sign is regulatory. The caption 18.28-c, "Do not pass on this road", gives the instruction, but the sign's binding force and the meaning of its symbol come from 18.9: "These signs give a direction that must be obeyed… A red circle with a line through it means the activity shown is not allowed." The rule does not cite 18.9, so its force and the note's reading of the symbol are not fully supported by its own citations.

- Fix: Change evidence to ["18.9", "18.28", "18.28-c"].
- **Proposed triage: fix as proposed.** SIGN-01 evidence: ["18.9", "18.28", "18.28-c"]. 18.9 gives regulatory signs their force and explains the red-circle symbol that the note relies on.

### S2-036. The sign is named only by an informal lowercase label in the condition

*clarity* · minor · low confidence

The condition reads "on a road posted with a do-not-pass sign". "do-not-pass sign" is not a defined term, and the handbook does not use that label. The only description of what the sign looks like is in the note. A driving model needs to recognize the sign itself, so its appearance should be in the condition.

- Fix: Set when to "on a road posted with a regulatory sign showing two cars inside a red circle with a red diagonal line through it (do-not-pass sign)". Update statement to "WHEN on a road posted with a regulatory sign showing two cars inside a red circle with a red diagonal line through it (do-not-pass sign), the DRIVER MUST NOT pass."
- **Proposed triage: not an error, no change.** The rule names the sign by its meaning, and the note describes what it looks like.

## PASS-SIGN-02: Do not pass a flashing pilot vehicle

> WHEN following a pilot vehicle or pace vehicle bearing a do-not-pass 'When Flashing' sign AND the sign is flashing, the DRIVER MUST NOT pass that vehicle.

### S2-037. Force should be INSTRUCTION, not REQUIREMENT

*strength* · minor · medium confidence

The handbook words this rule as a plain command, 18.103-c: "Do not pass the pilot vehicle or pace vehicle bearing this sign." The extractor's table maps a plain "do"/"don't" to INSTRUCTION. The handbook lists the sign under "Temporary condition signs" (18.90–18.91), which it describes as signs that "warn of unusual temporary conditions". It does not present it as a regulatory sign, and no "must", "illegal" or penalty wording appears. The modal MUST NOT is correct either way, so only the force label is affected.

- Fix: Set "force": "INSTRUCTION" and keep "modal": "MUST NOT". Optionally add to the note: "Worded as a plain command ('Do not pass') in a temporary-condition sign caption."
- **Proposed triage: fix as proposed.** SIGN-02 force: INSTRUCTION, modal stays MUST NOT. Add to the note: "Worded as a plain command ('Do not pass') in a temporary-condition sign caption." Same mapping as a0 M5.

### S2-038. The sign is not described in terms the driving model can recognize

*clarity* · minor · low confidence

The condition refers to "a do-not-pass 'When Flashing' sign". The image in 18.103 shows an orange rectangular sign with a no-passing symbol (two cars inside a red circle with a slash) and the words "WHEN FLASHING". Neither the rule nor its note describes this appearance. A model reading only the rule would not know which sign to look for on the vehicle ahead.

- Fix: Change the note to: "The sign (18.103) is an orange rectangular sign with a no-passing symbol (two cars in a red circle with a slash) and the words 'WHEN FLASHING', carried on a pilot or pace vehicle; the caption says do not pass the vehicle bearing it. The flashing condition comes from the sign's text."
- **Proposed triage: not an error, no change.** Same as S2-036. The note already gives the sign's text.

## PASS-SIGN-03: Keep right where passing lanes provided

> WHEN on a two-lane section where a PASSING LANE is provided AND a keep-right-except-to-pass sign is posted, the DRIVER MUST keep to the right lane, UNLESS the DRIVER is passing.

### S2-039. The sign is named by wording that does not appear on it

*clarity* · minor · medium confidence

The condition reads "a keep-right-except-to-pass sign is posted". The sign cited in 18.40 has no words on it. It is a black square with a white straight arrow and a second arrow that branches off to the right, and only the caption 18.40-c gives its meaning: "Keep to the right lane except when passing on two-lane sections where climbing or passing lanes are provided." A model reading "keep-right-except-to-pass sign" could look for a text sign with those words and miss the pictogram. The note is empty, so nothing tells a checker that the rule rests on a sign and its caption alone.

- Fix: Set when to: "on a two-lane section where a PASSING LANE is provided AND the regulatory sign showing a straight arrow with a second arrow branching to the right is posted". Update the statement to match. Add a note: "Rests on the regulatory sign in 18.40 (a black square with a straight arrow and an arrow branching right) and its caption 18.40-c."
- **Proposed triage: not an error, no change.** Same as S2-036.

## PASS-SIGN-04: Slower vehicles use right of a passing lane

> WHEN on a road with a PASSING LANE, the DRIVER of a slower vehicle SHOULD move into the right-hand lane so faster vehicles can pass in the left lane.

### S2-040. Block 10.36 is cited but does not support this rule

*citation* · minor · high confidence

The rule tells slower drivers to keep right in a passing lane section. 10.36 says something else: "An advance sign tells drivers they will soon have a chance to pass. Another sign warns when the lane is ending so drivers in the right-hand lane can begin to merge…". That is about signs and merging at the lane's end, which belongs to separate rules. Only 10.35 (the text) and 10.34 (Diagram 2-48) support this rule.

- Fix: Set evidence to ["10.35", "10.34"], or add "10.34-c" if the caption is wanted. Remove the sign remark from the note.
- **Proposed triage: fix as proposed.** SIGN-04 evidence: ["10.35", "10.34"]. note: "Described as the purpose of the lanes. Diagram 2-48 shows a truck in the right lane being passed."

### S2-041. Condition covers the whole road rather than the stretch with the extra lane

*condition* · major · medium confidence

"WHEN on a road with a PASSING LANE" applies to any point on a road that has such a lane somewhere. 10.35 describes behaviour only where the special lane exists, and 10.36 says the lane ends and right-lane drivers then merge. Read literally, the rule tells a slow driver to move right even where there is no extra lane, for example after the lane has ended.

- Fix: when: "driving on a section of road where a PASSING LANE provides two lanes in the DRIVER's direction"; statement: "WHEN driving on a section of road where a PASSING LANE provides two lanes in the DRIVER's direction, the DRIVER of a slower vehicle SHOULD move into the right-hand lane so faster vehicles can pass in the left lane."
- **Proposed triage: fix.** when: "on a section of road where a PASSING LANE is provided"; statement: "WHEN on a section of road where a PASSING LANE is provided, the DRIVER of a slower vehicle SHOULD move into the right-hand lane so faster vehicles can pass in the left lane."

### S2-042. "slower vehicle" is relative but not listed as vague

*vague terms* · minor · medium confidence

The actor "DRIVER of a slower vehicle" and the phrase "faster vehicles" set no speed threshold. The driver must judge whether they count as slower, and the handbook gives no measure. vague_terms is empty.

- Fix: Add to vague_terms: {"term": "slower vehicle", "explanation": "no speed or speed difference given; relative to other traffic"}.
- **Proposed triage: fix as proposed.** Add `{"term": "slower vehicle", "explanation": "no speed or speed difference given; relative to other traffic"}`.

### S2-043. Group code SIGN does not fit the rule's content

*numbering* · minor · low confidence

The rule concerns lane use in passing and climbing lanes, not a sign. It is filed under group "SIGN" (PASS-SIGN-04), which misleads anyone grouping or reading the rules.

- Fix: Move the rule to a lane-related group, for example PASS-LANE-01, and renumber.
- **Proposed triage: not an error, no change.** Passing-lane rules under SIGN are fine (a0 O2).

## PASS-SIGN-05: Merge when passing lane ends

> WHEN in the right-hand lane of a PASSING LANE section AND a sign warns that the lane is ending, the DRIVER MUST merge safely with traffic in the left-hand lane.

### S2-044. Lane-ending sign is described only vaguely

*clarity* · minor · medium confidence

The condition "a sign warns that the lane is ending" does not say which sign the driving model should recognize. The rule's "must" comes from one specific sign: 18.70-c: "Right lane ends ahead. If you are in the right-hand lane, you must merge safely…", shown in figure 18.70 (a yellow diamond with the right lane line bending into the left). A model reading only this rule cannot tie it to that sign. This also matters because the obligation rests on that sign alone.

- Fix: when: "in the right-hand lane of a PASSING LANE section AND a right-lane-ends warning sign (yellow diamond showing the right lane merging into the left) is posted"; update statement accordingly: "WHEN in the right-hand lane of a PASSING LANE section AND a right-lane-ends warning sign (yellow diamond showing the right lane merging into the left) is posted, the DRIVER MUST merge safely with traffic in the left-hand lane."
- **Proposed triage: not an error, no change.** Same as S2-036. 18.70 and 18.70-c are cited, and the note names the right-lane-ends sign.

### S2-045. Note does not state the inference that links the two passages

*note* · minor · medium confidence

10.36 says only "Another sign warns when the lane is ending so drivers in the right-hand lane can begin to merge safely…". It does not name the sign or use mandatory wording. The REQUIREMENT force depends on assuming that this unnamed sign is the right-lane-ends sign of 18.70, which is a general warning sign not specific to passing lanes. The note records the stronger wording but does not say that this identification is an inference.

- Fix: note: "Inferred from two places: 10.36 says an unnamed sign warns that the passing lane is ending so right-lane drivers 'can begin to merge safely' (soft wording); this is taken to be the right-lane-ends sign of 18.70, whose caption says 'you must merge safely with traffic in the lane to the left'. The stronger wording is recorded."
- **Proposed triage: fix as proposed.** SIGN-05 note: "Inferred from two places: 10.36 says an unnamed sign warns that the passing lane is ending so right-lane drivers 'can begin to merge safely' (soft wording); this is taken to be the right-lane-ends sign of 18.70, whose caption says 'you must merge safely with traffic in the lane to the left'. The stronger wording is recorded."

## PASS-SIDE-02: Wait for a slower vehicle to move right

> WHEN driving in the leftmost lane with a slower vehicle in front, the DRIVER MUST wait for the slower vehicle to move to the right rather than suddenly changing lanes to pass on the right.

### S2-046. Two separate commands merged with an ambiguous "rather than"

*structure* · minor · low confidence

10.41 gives two separate plain commands: "wait for the vehicle to move to the right" and "Do not suddenly change lanes and pass on the right". The rule joins them into one action: "wait for the slower vehicle to move to the right rather than suddenly changing lanes to pass on the right". This makes the prohibition a subordinate clause, which leaves two readings open. Is an unhurried lane change to pass on the right also forbidden, because the driver must wait? Or is only the sudden one forbidden? Two rules would keep each command checkable on its own and match the handbook's wording more closely.

- Fix: Split into two rules, both citing 10.41. (a) PASS-SIDE-02: when "driving in the leftmost lane with a slower vehicle in front", modal MUST, action "wait for the slower vehicle to move to the right"; statement "WHEN driving in the leftmost lane with a slower vehicle in front, the DRIVER MUST wait for the slower vehicle to move to the right." with vague_terms []. (b) PASS-SIDE-03: when "driving in the leftmost lane with a slower vehicle in front", modal MUST NOT, action "suddenly change lanes and pass on the right"; statement "WHEN driving in the leftmost lane with a slower vehicle in front, the DRIVER MUST NOT suddenly change lanes and pass on the right." with vague_terms [{"term":"suddenly","explanation":"no timing or distance given"}]. Keep the note on rule (b): "Reason given: the driver in front may move right at the same time."
- **Proposed triage: fix by rewording instead of splitting, as in a0 M3.** action: "wait for the slower vehicle to move to the right and not suddenly change lanes to pass on the right"; statement: "WHEN driving in the leftmost lane with a slower vehicle in front, the DRIVER MUST wait for the slower vehicle to move to the right and not suddenly change lanes to pass on the right." The vague term "suddenly" stays.

## PASS-USER-01: Cyclists: one metre

> WHEN passing a CYCLIST, the DRIVER MUST keep at least 1 metre between the vehicle and the CYCLIST, where practical.

### S2-047. Diagram caption named in the note is not cited

*citation* · minor · low confidence

The rule's note says "Diagram 2-11 shows the 1 metre gap." Block 6.32 also points to the diagram by its caption: 6.32: "…between their vehicle and the cyclist. (See Diagram 2-11.)" The caption is what links the text to the image: 6.31-c: "Diagram 2-11". The rule cites the figure 6.31 but not its caption 6.31-c. The instructions say to cite a caption when its words are directly relevant, and to cite both the figure and the caption when both are.

- Fix: Change evidence to ["6.32", "6.31", "6.31-c"].
- **Proposed triage: not an error, no change.** Something mentioned only in a note needs no citation (a0 C2).

## PASS-USER-02: Change lanes to pass cyclists

> WHEN passing a CYCLIST AND it is possible to change lanes, the DRIVER SHOULD change lanes to pass.

### S2-048. Block 10.24 gives the same rule as a plain command but is neither cited nor noted

*strength* · major · medium confidence

The rule cites only 6.32 ("Whenever possible, you should change lanes to pass.") and the diagram 10.27. However, 10.24 states the same rule for bicycles as a plain command: "Motorcycles, bicycles, limited-speed motorcycles and mopeds often need to pull to the left or right side of their lane… Do not take this as an invitation to pass in the same lane. If you do want to pass these vehicles, do so by changing lanes." Under the instructions this is INSTRUCTION wording (MUST / MUST NOT), and it has no "whenever possible" qualifier. The instructions say: "When two passages word the same rule differently, record the stronger wording and say so in `note`." The rule keeps ADVICE / SHOULD, does not cite 10.24, and does not mention it in the note. A driving model reading only this rule would treat lane-changing to pass a cyclist as optional advice, while the handbook's page on passing commands it. It also forbids passing a cyclist within the same lane.

- Fix: Add "10.24" to evidence. Then do one of two things. Option 1: raise the strength to force "INSTRUCTION", modal "MUST", when "passing a CYCLIST", action "change lanes to pass", statement "WHEN passing a CYCLIST, the DRIVER MUST change lanes to pass." Add the note: "10.24 commands passing bicycles only by changing lanes ('do so by changing lanes'; 'Do not take this as an invitation to pass in the same lane'); 6.32 words it as advice 'whenever possible'; the stronger wording is recorded. Diagram 2-47 shows a car moving into the next lane to pass a cyclist in a sharrow lane." Option 2: if the 'whenever possible' advice is kept as a separate rule, at least add a note that 10.24 states it as an instruction and that a separate INSTRUCTION rule covers it.
- **Proposed triage: fix with a note only, without raising the strength.** The INSTRUCTION wording of 10.24 is already its own rule, PASS-USER-05 ("MUST pass by changing lanes, not within the same lane"). USER-02 records the separate "whenever possible" advice of 6.32. Add to USER-02's note: "10.24 states passing these riders by changing lanes as an instruction; that is PASS-USER-05."

## PASS-USER-04: Tap horn lightly and early

> WHEN overtaking a CYCLIST AND the DRIVER feels the horn must be used, the DRIVER MUST tap the horn quickly and lightly while still some distance away from the CYCLIST.

### S2-049. Vague phrases in the rule are not listed in vague_terms

*vague terms* · minor · medium confidence

The only vague term listed is "some distance". The statement also keeps two other handbook judgement words: "quickly and lightly", which gives no duration or force for the horn tap, and "the DRIVER feels the horn must be used", which leaves to the driver when the horn is needed. The source is 6.38: "If you feel that you must use your horn, tap it quickly and lightly while you are still some distance away…". The instructions say every vague word or phrase kept in the statement should be listed.

- Fix: Set vague_terms to: [{"term": "some distance", "explanation": "no distance given"}, {"term": "quickly and lightly", "explanation": "no duration or loudness given"}, {"term": "the DRIVER feels the horn must be used", "explanation": "left to the driver's judgement; no criteria given"}].
- **Proposed triage: fix as proposed.** vague_terms: "some distance" (no distance given), "quickly and lightly" (no duration or loudness given), "the DRIVER feels the horn must be used" (left to the driver's judgement; no criteria given).

## PASS-USER-05: Pass two-wheelers by changing lanes

> WHEN wanting to pass a motorcycle, bicycle, limited-speed motorcycle or moped, the DRIVER MUST pass by changing lanes, not within the same lane.

### S2-050. Diagram 2-47 showing a lane-change pass of a cyclist is not cited

*citation* · minor · medium confidence

The rule cites only 10.24 ("…If you do want to pass these vehicles, do so by changing lanes."). Figure 10.27 (Diagram 2-47), placed right after this passage, shows a car moving fully into the adjacent lane to pass a cyclist riding in the same direction, then returning to its lane. That is exactly the behaviour this rule describes, so the figure supports the rule and should be cited with it. The caption "Diagram 2-47" carries no rule content, so it does not need to be cited.

- Fix: Change evidence to ["10.24", "10.27"] and add to the note: "Diagram 2-47 (10.27) shows a car passing a cyclist by moving fully into the adjacent lane."
- **Proposed triage: fix, citation only.** USER-05 evidence: ["10.24", "10.27"]. No note change.

## PASS-USER-06: Do not pull beside a smaller vehicle to turn left with it

> WHEN making a left turn behind a motorcycle, bicycle, limited-speed motorcycle or moped, the DRIVER MUST NOT pull up beside it to make the left turn at the same time.

### S2-051. Note omits the passing instruction in the same block

*note* · minor · low confidence

Block 9.18 ends with "Wait for the smaller vehicle to move right before you pass." This is the sentence in the block most directly about overtaking. The rule's note mentions only "stay behind and turn when the way is clear" and does not mention this sentence. It also does not say whether the sentence is covered by a separate rule. A checker cannot tell whether that instruction was captured or dropped.

- Fix: Change note to: "The handbook says stay behind and turn when the way is clear. The same block also instructs waiting for the smaller vehicle to move right before passing it; that is a separate INSTRUCTION rule." If no such rule exists, add one: "WHEN behind a motorcycle, bicycle, limited-speed motorcycle or moped that is making a left turn at an intersection, the DRIVER MUST wait for it to move right before passing it." Cite 9.18.
- **Proposed triage: not an error, no change.** The pass-after-moving-right sentence is its own rule, PASS-USER-07 (split from this rule in a0 M7).

## PASS-USER-07: Wait for a smaller vehicle to move right before passing

> WHEN making a left turn behind a motorcycle, bicycle, limited-speed motorcycle or moped, the DRIVER MUST NOT pass it, UNLESS the smaller vehicle has moved right.

### S2-052. Action uses the unclear pronoun "it" and names the vehicle inconsistently

*clarity* · minor · medium confidence

The action "pass it" relies on the pronoun "it" to refer back to the list in the condition. The exception then calls the same vehicle "the smaller vehicle", a phrase the condition never introduces. The instructions require each rule to stand on its own. Source 9.18: "Wait for the smaller vehicle to move right before you pass."

- Fix: when: "making a left turn behind a motorcycle, bicycle, limited-speed motorcycle or moped"; action: "pass that motorcycle, bicycle, limited-speed motorcycle or moped"; unless: "that vehicle has moved to the right". Statement: "WHEN making a left turn behind a motorcycle, bicycle, limited-speed motorcycle or moped, the DRIVER MUST NOT pass that motorcycle, bicycle, limited-speed motorcycle or moped, UNLESS that vehicle has moved to the right."
- **Proposed triage: not an error, no change.** "It" refers back to the one vehicle in the condition, and the wording follows the handbook's "the smaller vehicle". The wording was approved in a0 M7.

### S2-053. Note does not explain the timing or the related no-side-by-side instruction

*note* · minor · medium confidence

In 9.18 the wait-to-pass sentence follows "do not pull up beside it to make your turn at the same time. Stay behind and turn when the way is clear." The pass the rule refers to therefore happens after the turn, once the smaller vehicle has moved right. This is not a pass during the turn. The rule's "when" ("making a left turn") does not show that sequence, and the note is empty. A checker cannot tell that this rule is meant to be separate from the related instruction not to turn alongside the vehicle.

- Fix: Add the note: "In 9.18 this follows the instruction not to pull up beside the smaller vehicle and to stay behind it through the turn; the pass referred to is after the turn, once the smaller vehicle has moved to the right. The no-side-by-side turning instruction is a separate rule."
- **Proposed triage: fix as proposed.** USER-07 note: "In 9.18 this follows the instruction not to pull up beside the smaller vehicle and to stay behind it through the turn; the pass referred to is after the turn, once the smaller vehicle has moved to the right. The no-side-by-side turning instruction is PASS-USER-06."

## PASS-USER-09: Allow more room when passing a large vehicle

> WHEN passing a LARGE VEHICLE, the PASSER MUST allow more room.

### S2-054. Rule does not say where the extra room goes

*ambiguity* · minor · medium confidence

The action "allow more room" is a bare comparative: it does not say room for what, or more than what. In 6.55 the sentence ends a passage about cutting back in ahead of the truck: 6.55: "When passing a large vehicle, do not cut in front closely… it reduces the space cushion large vehicles require in order to stop safely. Allow more room when passing a large vehicle." In context, the extra room is the gap left in front of the large vehicle when returning to its lane, compared with passing a smaller vehicle. Read alone, the rule could mean lateral clearance or a following gap. A driving model would not know what to do. The vague-term entry "no distance given" does not cover this missing reference.

- Fix: Set action to "allow more room in front of the LARGE VEHICLE before returning to its lane than when passing a smaller vehicle". The statement becomes "WHEN passing a LARGE VEHICLE, the PASSER MUST allow more room in front of the LARGE VEHICLE before returning to its lane than when passing a smaller vehicle." Keep "more room" as a vague term. Add to the note: "Context of 6.55 (stopping distance, not cutting in closely) indicates the room is in front of the large vehicle."
- **Proposed triage: fix.** action: "allow more room in front of the LARGE VEHICLE before returning to its lane"; statement: "WHEN passing a LARGE VEHICLE, the PASSER MUST allow more room in front of the LARGE VEHICLE before returning to its lane." The vague term "more room" stays. The "than when passing a smaller vehicle" part is left out, since the handbook does not state it.

### S2-055. Block 6.61 (turbulence) cited but does not support the rule

*citation* · minor · medium confidence

The rule's evidence includes 6.61: "a large vehicle can create heavy air turbulence. This may affect your ability to control your vehicle when passing a large one." This block gives a separate hazard. It does not instruct the driver to allow more room, and the rule's support comes entirely from 6.55. The extractor's instructions say to cite only material directly relevant to the rule. Mentioning turbulence in the note does not make 6.61 evidence for this rule.

- Fix: Set evidence to ["6.55"]. Either drop the turbulence remark from the note, or keep it as context while citing only 6.55.
- **Proposed triage: fix: remove the citation, keep the note.** USER-09 evidence: ["6.55"]. The turbulence remark can stay in the note without a citation (a0 C2 ruling).

## PASS-USER-10: Anticipate long commercial vehicles

> WHEN preparing to pass a LONG COMMERCIAL VEHICLE on the highway, the DRIVER SHOULD anticipate its extended length and limited speed.

### S2-056. Vague words "limited speed" and "anticipate" not listed

*vague terms* · minor · medium confidence

The action "anticipate its extended length and limited speed" leaves the driver's judgement open, but `vague_terms` is empty. 18.129-c says only "anticipate both the extended length and limited speed". It gives no speed for an LCV and does not say what anticipating requires, such as extra passing distance or time. "Extended length" is bounded by the vocabulary (up to 40 metres), but "limited speed" and "anticipate" are not. Without these entries, a driving model cannot tell that the rule leaves this to the driver.

- Fix: Set vague_terms to [{"term": "limited speed", "explanation": "no speed or speed limit for LCVs given"}, {"term": "anticipate", "explanation": "does not say what the driver should do differently, e.g. how much extra distance or time to allow"}].
- **Proposed triage: fix as proposed.** vague_terms: "limited speed" (no speed or speed limit for LCVs given), "anticipate" (does not say what the driver should do differently).

### S2-057. Recognition of LCVs by rear signage omitted without a note

*completeness* · minor · low confidence

18.129-c says "It is important to be able to recognize an LCV on the highway, based on rear signage, and anticipate…". The rule keeps only the anticipation part. It neither mentions the advice to recognize the LCV by its rear placard nor notes that this part is covered elsewhere, for example by the vocabulary definition. A checker cannot tell whether that part was dropped on purpose.

- Fix: Set note to: "18.129-c also advises recognizing an LCV on the highway by its rear placard; this identification is captured in the LONG COMMERCIAL VEHICLE vocabulary entry. The handbook words this as 'it is important', recorded as ADVICE."
- **Proposed triage: not an error, no change.** Recognising an LCV is covered by the LONG COMMERCIAL VEHICLE vocabulary entry.

## PASS-USER-11: Farm machinery: stay back until safe

> WHEN behind farm machinery or another vehicle displaying a SLOW-MOVING VEHICLE SIGN, the DRIVER MUST NOT pass, UNLESS it is safe to do so.

### S2-058. "Stay well back" dropped from the action although the title claims it

*completeness* · minor · medium confidence

The source sentence is one instruction: 6.75: "Stay well back and do not pass until it is safe to do so." The rule's action is only "pass", yet its title is "Farm machinery: stay back until safe". The note mentions staying well back, but a model reading only the statement would not be told to keep its distance while waiting to pass. The title also does not match the statement.

- Fix: Either put both parts in the rule: action "stay well back and not pass" with modal MUST, statement "WHEN behind farm machinery or another vehicle displaying a SLOW-MOVING VEHICLE SIGN, the DRIVER MUST stay well back and not pass, UNLESS it is safe to do so.", and add the vague term {"term": "well back", "explanation": "no distance given"}. Or keep the action as is and retitle the rule "Farm machinery: do not pass until safe".
- **Proposed triage: fix, by retitling.** title: "Farm machinery: do not pass until safe". The statement is unchanged, and the note already mentions staying well back.

### S2-059. Cited caption 18.126-c does not support the no-passing rule

*citation* · minor · medium confidence

18.126-c describes the sign and says "Watch for these slow moving vehicles and reduce your speed as necessary." It says nothing about passing. The rule rests on 6.75 alone. 6.74 only gives background, which the note uses: "Farmers often turn directly into fields … or move from lane to lane." Citing 18.126-c as evidence for this prohibition is imprecise.

- Fix: Set evidence to ["6.75", "6.74"], or to ["6.75"] only. The sign's definition already cites 18.126-c through the vocabulary.
- **Proposed triage: fix as proposed.** USER-11 evidence: ["6.74", "6.75"]. 18.126-c stays cited on the SLOW-MOVING VEHICLE SIGN vocabulary entry.

### S2-060. Condition is ambiguous about whether farm machinery must display the sign

*clarity* · minor · low confidence

In "behind farm machinery or another vehicle displaying a SLOW-MOVING VEHICLE SIGN", it is unclear whether "displaying" also applies to the farm machinery. The handbook ties the instruction to seeing the sign. 6.75: "If you see one of these signs, slow down … do not pass until it is safe". 18.126-c extends the sign to "vehicles not capable of sustaining speeds over 40 km/h".

- Fix: when: "behind a vehicle displaying a SLOW-MOVING VEHICLE SIGN, such as farm machinery". Change the statement to match.
- **Proposed triage: not an error, no change.** Low confidence. 6.74 and 6.75 cover farm machinery whether or not "displaying" also applies to it.

## PASS-USER-13: Horse-drawn vehicles: give maximum distance

> WHEN passing a HORSE-DRAWN VEHICLE, the PASSER MUST leave as much distance as possible between the vehicle and the HORSE-DRAWN VEHICLE.

### S2-061. "the vehicle" could refer to either vehicle

*clarity* · minor · medium confidence

The action reads "leave as much distance as possible between the vehicle and the HORSE-DRAWN VEHICLE". The phrase "the vehicle" does not name its owner, and it could be read as the horse-drawn vehicle itself. The handbook is clearer. 6.78: "When passing, give as much distance between you and them as possible." Naming the PASSER's own vehicle removes the ambiguity.

- Fix: action: "leave as much distance as possible between the PASSER's vehicle and the HORSE-DRAWN VEHICLE"; statement: "WHEN passing a HORSE-DRAWN VEHICLE, the PASSER MUST leave as much distance as possible between the PASSER's vehicle and the HORSE-DRAWN VEHICLE."
- **Proposed triage: fix as proposed.** action: "leave as much distance as possible between the PASSER's vehicle and the HORSE-DRAWN VEHICLE"; statement updated to match.

## PASS-USER-14: Never pass moving snow plows

> WHEN behind a moving SNOW PLOW, the DRIVER MUST NOT pass it under any conditions.

### S2-062. SNOW PLOW definition makes the blue lights part of what counts as a snow plow

*vocabulary* · minor · low confidence

The rule depends on the term SNOW PLOW, defined as "A snow-removal vehicle on a public road, equipped with flashing blue lights." In the handbook, the lights describe how snow plows are normally equipped; they are not a condition for being one. 14.88: "Snow-removal vehicles on public roadways are equipped with flashing blue lights…" 10.15 bans passing moving snow plows "under any conditions" and says nothing about lights. Because the lights are written into the definition, a model could conclude that a plow whose lights are off, or not yet visible, is not a SNOW PLOW and may be passed. That narrows an absolute prohibition.

- Fix: Change the SNOW PLOW definition to: "A snow-removal vehicle operating on a public road (such vehicles are normally equipped with flashing blue lights visible from 150 metres)." Keep the evidence ["14.88", "14.89"].
- **Proposed triage: fix as proposed.** SNOW PLOW definition: "A snow-removal vehicle operating on a public road." Evidence stays ["14.88", "14.89"]. The blue lights are equipment, not part of what a snow plow is, as in the a0 V2 ruling.

## PASS-USER-16: Watch for opening doors when passing parked vehicles

> WHEN passing parked vehicles, the DRIVER MUST watch carefully for people suddenly opening doors or for doors opened to load and unload.

### S2-063. 'watch carefully' not listed as a vague term

*vague terms* · minor · low confidence

The action "watch carefully for people suddenly opening doors…" leaves the driver's response to judgement. 10.23 says only "watch carefully". It gives no lateral clearance to keep from parked vehicles and no speed reduction. Under the instructions, words that leave a judgement to the driver should be listed in `vague_terms`, but the list is empty.

- Fix: Set vague_terms to [{"term": "watch carefully", "explanation": "no clearance from parked vehicles or speed reduction given; the response to a door opening is left to the driver"}].
- **Proposed triage: fix as proposed.** Add `{"term": "watch carefully", "explanation": "no clearance from parked vehicles or speed reduction given"}`.

## PASS-USER-17: Stay 2 metres behind streetcar doors

> WHEN at a STREETCAR stop where passengers are getting off or on, the DRIVER MUST stay at least 2 metres behind the rear doors of the STREETCAR, UNLESS an area has been set aside for STREETCAR passengers at the stop.

### S2-064. "Stay … behind" does not say the driver must stop and wait

*clarity* · minor · low confidence

The action "stay at least 2 metres behind the rear doors of the STREETCAR" does not say plainly that the driver must stop behind the streetcar and must not pass it while passengers are getting off or on. A driving model reading only the rule could take it as a following-distance instruction. The cited figure shows the meaning: 10.43 alt text reads "a vehicle stopped the required two metres behind the rear doors of a stopped streetcar". The handbook text in 10.45 ("stay at least two metres behind the rear doors…") is ambiguous in the same way, so this is a clarity issue only.

- Fix: Add to the note: "Diagram 2-49 (10.43) shows vehicles stopped at least 2 metres behind the rear doors of a stopped streetcar; 'stay behind' means stop there and do not pass while passengers are getting off or on." The action can stay as it is.
- **Proposed triage: not an error, no change.** The note already says "Diagram 2-49 shows vehicles stopped 2 metres behind the rear doors."

## PASS-USER-18: Pass streetcar passenger areas carefully

> WHEN passing a STREETCAR stop safety island or area set aside for passengers, the DRIVER MUST pass at a reasonable speed and be prepared for pedestrians to make sudden or unexpected moves.

### S2-065. Lowercase 'passing' means driving past an island, not overtaking

*vocabulary* · minor · medium confidence

The topic is overtaking, where 'pass' normally means moving past another vehicle. In this rule, "passing a STREETCAR stop safety island or area set aside for passengers" and "pass at a reasonable speed" mean driving alongside a fixed passenger zone. The source is 10.45: "Always pass these areas at a reasonable speed…". In a rule set that defines PASS as overtaking, the lowercase 'passing' looks like that term but means something else. Readers may misread it, and the rule's link to overtaking is unclear.

- Fix: Reword with 'driving past' and tie the rule to passing a stopped streetcar. when: "driving past a STREETCAR stopped at a STREETCAR stop that has a safety island or area set aside for STREETCAR passengers"; action: "drive past the safety island or area at a reasonable speed and be prepared for pedestrians to make sudden or unexpected moves".
- **Proposed triage: not an error, no change.** A lowercase phrase may mean something different from the CAPS term (a0 V3).

### S2-066. Condition wording is loose about which passenger areas

*clarity* · minor · medium confidence

The phrase "STREETCAR stop safety island or area set aside for passengers" can be read as any area set aside for passengers, such as a bus platform. The handbook limits it to streetcar stops. 10.45 says: "stops where an area has been set aside for streetcar passengers". 6.18 says: "Some streetcar stops have a special safety island or zone for passengers getting on and off."

- Fix: when: "driving past a safety island or zone set aside for STREETCAR passengers at a STREETCAR stop".
- **Proposed triage: fix as proposed.** when: "passing a safety island or area set aside for STREETCAR passengers at a STREETCAR stop"; statement updated to match.

### S2-067. Vague phrase 'sudden or unexpected moves' not listed

*vague terms* · minor · low confidence

The action "be prepared for pedestrians to make sudden or unexpected moves" does not say what being prepared involves, such as covering the brake or slowing further. It also does not say which moves are meant. Only "reasonable speed" is listed in vague_terms.

- Fix: Add to vague_terms: {"term": "be prepared for pedestrians to make sudden or unexpected moves", "explanation": "no specific action or margin given"}.
- **Proposed triage: fix as proposed.** Add `{"term": "be prepared for pedestrians to make sudden or unexpected moves", "explanation": "no specific action or margin given"}`.

### S2-068. Note omits link to the two-metre rule exception

*note* · minor · medium confidence

In 10.45 this advice applies where the two-metre stopping rule does not: "This rule does not apply at stops where an area has been set aside for streetcar passengers. Always pass these areas…". The note says only "Stated on two pages." A checker would not see that this rule replaces the requirement to stay two metres behind the rear doors.

- Fix: note: "Stated on two pages (10.45, 6.18), both as plain commands. At stops with a safety island or passenger area, the requirement to stop two metres behind the streetcar's rear doors does not apply; this rule applies instead."
- **Proposed triage: fix as proposed.** USER-18 note: "Stated on two pages (10.45, 6.18), both as plain commands. At stops with a safety island or passenger area, the requirement to stop two metres behind the streetcar's rear doors (PASS-USER-17) does not apply; this rule applies instead."

## PASS-USER-19: Slow down for stopped emergency vehicle or tow truck

> WHEN approaching an EMERGENCY VEHICLE stopped with its red, or red and blue, lights flashing OR a tow truck stopped with its amber lights flashing, in the DRIVER's direction of travel, the DRIVER MUST reduce speed and proceed with caution.

### S2-069. Required assessment of traffic speed and road conditions left out of the rule

*incompleteness* · major · medium confidence

13.107 makes a second requirement part of the same manoeuvre: "When reducing your speed, you are required to assess the speed of the surrounding traffic and the condition of the roadway (such as fog, rain, snow)." The rule's action is only "reduce speed and proceed with caution". This requirement appears only in the note, and no separate rule is named for it (the note names only PASS-USER-20, for early braking). A driving model reading the statement would not see this obligation.

- Fix: Set action to "reduce speed, assessing the speed of the surrounding traffic and the condition of the roadway, and proceed with caution". Update the statement to match. Alternatively, write a separate REQUIREMENT rule citing 13.107 and say so in the note.
- **Proposed triage: fix, by putting the duty in the action.** a0 M6 moved this requirement into the note, but it is a separate "you are required" sentence of 13.107. action: "reduce speed, assessing the speed of the surrounding traffic and the condition of the roadway, and proceed with caution"; statement updated to match. Drop the first sentence of the note.

### S2-070. Penalty for 'not stopping' applied to a slow-down rule

*penalty* · minor · medium confidence

The penalty text says "higher fines and up to six months in jail for further offences". This comes from 13.117, which covers failing to respond to an emergency vehicle: "…bring your vehicle to a stop, where required… If you don’t stop, you can be fined and get three demerit points… you could also go to jail for up to six months." That passage is about not stopping or clearing the way for an emergency vehicle, not about failing to slow for one that is already stopped. It is not clear that "the above law" in 13.118 means the slow-down duty. Only 22.129 ("Failing to slow and carefully pass a stopped emergency vehicle", three points) directly supports a penalty for this rule.

- Fix: Set penalty to "Three demerit points." and keep 22.96 and 22.129. Remove 13.117 from the evidence, or keep it and say in the note that the fines and jail term are stated for failing to stop for an emergency vehicle, and that applying them to this rule is an inference.
- **Proposed triage: rejected, no change.** The penalty sources were settled in a0 C5: 13.117 extended by 13.118 for the fines and jail term, and 22.129 for the demerit points. The note already says where each part comes from.

### S2-071. Vague 'reduce speed' not listed; explanation attached to the wrong phrase

*vague terms* · minor · medium confidence

The handbook gives no amount for the speed reduction, so "reduce speed" is vague. It is not listed in vague_terms. The explanation "no speed given" is attached to "proceed with caution", although that phrase leaves the meaning of caution open rather than a speed.

- Fix: Set vague_terms to [{"term":"reduce speed","explanation":"amount or target speed not given"},{"term":"proceed with caution","explanation":"what caution requires is not stated"}].
- **Proposed triage: fix as proposed.** vague_terms: "reduce speed" (amount or target speed not given), "proceed with caution" (what caution requires is not stated).

### S2-072. Scope of 'in the DRIVER's direction of travel' is ambiguous

*clarity* · minor · low confidence

In the when clause, "in the DRIVER's direction of travel" is placed after the tow-truck alternative. It is unclear whether it limits only the tow truck or also the EMERGENCY VEHICLE. 13.107 means the approach is in the same direction of travel for both: "When approaching any emergency vehicle … or a tow truck … in the same direction of your travel".

- Fix: Rewrite the when clause as "approaching, in the DRIVER's direction of travel, an EMERGENCY VEHICLE stopped with its red, or red and blue, lights flashing OR a tow truck stopped with its amber lights flashing" and update the statement.
- **Proposed triage: fix as proposed.** when: "approaching, in the DRIVER's direction of travel, an EMERGENCY VEHICLE stopped with its red, or red and blue, lights flashing OR a tow truck stopped with its amber lights flashing"; statement updated to match.

## PASS-USER-20: Brake early and gradually for a stopped emergency vehicle or tow truck

> WHEN approaching an EMERGENCY VEHICLE stopped with its red, or red and blue, lights flashing OR a tow truck stopped with its amber lights flashing, in the DRIVER's direction of travel, the DRIVER MUST brake early and gradually.

### S2-073. Direction-of-travel qualifier reads as applying only to the tow truck

*ambiguity* · minor · medium confidence

The condition "approaching an EMERGENCY VEHICLE stopped with its red, or red and blue, lights flashing OR a tow truck stopped with its amber lights flashing, in the DRIVER's direction of travel" places "in the DRIVER's direction of travel" after the second disjunct only. It can be read as limiting only the tow truck case. The handbook's situation applies to both vehicles: 13.107: "any emergency vehicle that is stopped … or a tow truck with its amber lights flashing in the same direction of your travel". The heading 13.105 also covers both: "Reacting to a stopped emergency vehicle or tow truck".

- Fix: when: "approaching, in the DRIVER's direction of travel, an EMERGENCY VEHICLE stopped with its red, or red and blue, lights flashing OR a tow truck stopped with its amber lights flashing"; update the statement to match.
- **Proposed triage: fix as proposed.** Same change to USER-20's condition as S2-072, so the two rules match.

### S2-074. Diagram of the situation and the repeated braking advice not cited

*citation* · minor · low confidence

Diagram 2-57 (13.106) shows traffic approaching the stopped emergency vehicle that this rule addresses. The same advice to brake early also appears in 13.113: "Before changing direction or speed, … signal and brake early." The rule cites only 13.107.

- Fix: Add "13.106" to evidence. Optionally add "13.113" and mention it in the note as a restatement in the tips list.
- **Proposed triage: rejected, no change.** In a0 C4, 13.106 was moved to USER-21, the move-over rule it shows. 13.113 is a general tip, not this rule.

## PASS-USER-21: Move over for stopped emergency vehicle or tow truck

> WHEN the road has two or more lanes in the DRIVER's direction AND the DRIVER is approaching either an EMERGENCY VEHICLE stopped with its red, or red and blue, lights flashing or a tow truck stopped with its amber lights flashing, the DRIVER MUST move into a lane away from the EMERGENCY VEHICLE or tow truck, well in advance, signalling and checking mirrors and BLIND SPOTS, UNLESS it is not safe to do so.

### S2-075. Penalty mixes in the fine and jail term for failing to stop for an emergency vehicle

*penalty* · minor · medium confidence

The penalty reads "A fine and three demerit points for a first offence; higher fines and up to six months in jail for further offences." Only the three demerit points are tied to this rule, by 22.130: "Failing to move, where possible, into another lane when passing a stopped emergency vehicle". That table entry gives demerit points only, with no fine, and it covers emergency vehicles, not tow trucks. The fine and the escalating fines and jail come from 13.117, which is about a different duty: "Proceed with caution, clear the way and bring your vehicle to a stop, where required. It's the law. If you don't stop, you can be fined and get three demerit points…". 13.118 extends "the above law" to a stopped tow truck, but the passage's penalty is still for not stopping or clearing the way, not for failing to move over. Reading it as the move-over penalty is an inference, and the rule presents it as stated fact.

- Fix: Set penalty to "Three demerit points (for a stopped emergency vehicle)." Remove 13.117 and 13.118 from evidence, or keep them and say in the note that applying their fines and jail term to the move-over duty is an inference. Note: "22.130 lists three demerit points for failing to move over for a stopped emergency vehicle; no move-over penalty is stated for tow trucks in the sections shown."
- **Proposed triage: rejected, no change.** Same as S2-070 (a0 C5).

### S2-076. Lane-change steps paraphrased loosely

*fidelity* · minor · low confidence

The action says "signalling and checking mirrors and BLIND SPOTS". 13.109 lists more specific steps: "look in front and on both sides of your vehicle, and check your rearview mirrors… use your turn signal prior to making the lane change, and double check your rearview mirrors and shoulder check your blind spots". The rule drops the shoulder check and the look in front and to both sides, and it does not say the signal comes before the lane change.

- Fix: action: "move into a lane away from the EMERGENCY VEHICLE or tow truck, well in advance, after looking in front and on both sides, checking the rearview mirrors, signalling, and shoulder checking the BLIND SPOTS".
- **Proposed triage: not an error, no change.** Low confidence. "Checking mirrors and BLIND SPOTS" covers the mirror check and the shoulder check.

## PASS-USER-22: Slow down to pass roadside workers

> WHEN approaching roadside assistance, disabled vehicles, surveyors, road maintenance or utility workers on the road, the DRIVER MUST slow down and pass with caution.

### S2-077. Handbook's example list is made exhaustive

*scope* · minor · medium confidence

The handbook gives the worker and vehicle types only as examples. 13.41 says: "Other types of workers and vehicles may also be present on the road and pose a hazard, such as roadside assistance and disable vehicles, surveyors, road maintenance or utility workers. Always slow down and pass with caution…". The rule's condition "approaching roadside assistance, disabled vehicles, surveyors, road maintenance or utility workers on the road" lists only these. A driving model would not apply the rule to other workers or vehicles on the road that pose a hazard, though the handbook's instruction covers them.

- Fix: when: "approaching workers or vehicles on the road that pose a hazard, such as roadside assistance vehicles, disabled vehicles, surveyors, road maintenance workers OR utility workers"; update the statement to match.
- **Proposed triage: fix as proposed.** when: "approaching workers or vehicles on the road that pose a hazard, such as roadside assistance vehicles, disabled vehicles, surveyors, road maintenance workers or utility workers"; statement updated to match. Use the same wording in USER-23 (see S2-081).

### S2-078. "slow down" not listed as vague

*vague terms* · minor · medium confidence

The action "slow down" gives no amount or target speed. 13.41 only says "Always slow down". Only "with caution" is listed in vague_terms, so the model is not told that how much to slow down is left to the driver.

- Fix: Add to vague_terms: {"term": "slow down", "explanation": "no amount or target speed given"}.
- **Proposed triage: fix as proposed.** Add `{"term": "slow down", "explanation": "no amount or target speed given"}`.

### S2-079. Condition alternatives not joined with the OR keyword

*grammar* · minor · medium confidence

The grammar requires CONDITION := FACT { ("AND" | "OR") FACT }. The rule writes the alternatives as a comma list with a lowercase "or": "roadside assistance, disabled vehicles, surveyors, road maintenance or utility workers". It also says "roadside assistance" where it means the roadside assistance vehicles or workers present, which is unclear.

- Fix: when: "approaching a roadside assistance vehicle OR a disabled vehicle OR surveyors OR road maintenance workers OR utility workers on the road". If the first finding is adopted, combine both changes.
- **Proposed triage: not an error, no change.** Alternatives joined by a lowercase "or" inside one fact is the accepted convention (a0 G1).

### S2-080. Move-over advice in the same block not mentioned in a note

*note* · minor · low confidence

13.41 continues: "If safe to do so, move over a lane to increase the space between your vehicle and the hazard." This is a separate rule in the cited block, and the block also gives a reason: "to prevent a collision". The rule's note is empty, so a checker is not told about either.

- Fix: note: "Reason given: to prevent a collision. The same block also says to move over a lane if safe to do so; that is a separate rule."
- **Proposed triage: not an error, no change.** The move-over sentence is its own rule, PASS-USER-23.

## PASS-USER-23: Move over a lane for roadside workers

> WHEN passing roadside assistance, disabled vehicles, surveyors, road maintenance or utility workers on the road AND it is safe to do so, the DRIVER MUST move over a lane to increase the space between the vehicle and the hazard.

### S2-081. "the hazard" has no referent in the rule

*clarity* · minor · medium confidence

The action says "increase the space between the vehicle and the hazard", but the rule's condition never calls anything a hazard. It lists "roadside assistance, disabled vehicles, surveyors, road maintenance or utility workers". In 13.41 the referent comes from the preceding sentence: "Other types of workers and vehicles may also be present on the road and pose a hazard…". Read alone, as the instructions require ("name the situation instead of writing 'in this case'"), the rule leaves "the hazard" undefined. It is clear enough from context, but it should be made explicit.

- Fix: Change the action to: "move over a lane to increase the space between the vehicle and those workers or vehicles". Update the statement to match: "WHEN passing roadside assistance, disabled vehicles, surveyors, road maintenance or utility workers on the road AND it is safe to do so, the DRIVER MUST move over a lane to increase the space between the vehicle and those workers or vehicles."
- **Proposed triage: fix, using the S2-077 wording.** USER-23 when: "passing workers or vehicles on the road that pose a hazard, such as roadside assistance vehicles, disabled vehicles, surveyors, road maintenance workers or utility workers, AND it is safe to do so". "The hazard" in the action then has a referent, so the action is unchanged.

## PASS-WX-02: No speeding up to pass in fog

> WHEN driving in fog, the DRIVER MUST NOT speed up to pass a vehicle moving slowly.

### S2-082. "moving slowly" not listed as a vague term

*vague terms* · minor · low confidence

The statement keeps the handbook's phrase "a vehicle moving slowly" (14.31: "Don't speed up to pass a vehicle moving slowly…"). The handbook gives no speed or relative-speed threshold for "slowly", so this is a judgement left to the driver. Yet `vague_terms` is empty.

- Fix: Set vague_terms to [{"term": "moving slowly", "explanation": "no speed or speed difference given"}].
- **Proposed triage: fix as proposed.** Add `{"term": "moving slowly", "explanation": "no speed or speed difference given"}`.

## PASS-WX-03: No passing in blowing snow or whiteout

> WHEN driving in blowing snow OR a whiteout, the DRIVER MUST NOT attempt to pass a vehicle moving slowly.

### S2-083. General 'avoid passing' advice is folded into a narrower slow-vehicle prohibition

*scope/citation* · minor · medium confidence

The note treats 14.68 as a weaker wording of the same rule: "14.68 also advises avoiding passing; the stronger 'Don't' of 14.76 is recorded." The two blocks do not cover the same situation. 14.68: "Be patient. Avoid passing, changing lanes and crossing traffic" advises against passing any vehicle. 14.76: "Don't attempt to pass a vehicle moving slowly" forbids only passing a slow-moving vehicle. Merging them under the narrower action "attempt to pass a vehicle moving slowly" drops the broader ADVICE not to pass at all in these conditions. Citing 14.68 as support for this rule also misrepresents what that block says.

- Fix: Remove 14.68 from this rule's evidence, so evidence is ["14.63", "14.76"]. Change the note to: "From the DON'T list for blowing snow and whiteout (14.76). 14.68 separately advises avoiding passing in general; that is a separate ADVICE rule." Make sure a separate rule exists, for example: "WHEN driving in blowing snow OR a whiteout, the DRIVER SHOULD NOT pass." (force ADVICE, evidence ["14.63", "14.68"]).
- **Proposed triage: rejected, no change.** The stronger-wording note in WX-03 was checked and found correct in a0.

### S2-084. Vague phrase 'moving slowly' not listed in vague_terms

*vague terms* · minor · medium confidence

The statement keeps the handbook's words "a vehicle moving slowly" (14.76). The handbook gives no speed, and no speed relative to traffic or to the limit, that counts as slow. The rule's vague_terms list is still empty.

- Fix: Set vague_terms to [{"term": "moving slowly", "explanation": "no speed or speed difference given"}].
- **Proposed triage: fix as proposed.** Same as S2-082, for WX-03.

## PASS-BEING-01: Move right and let faster traffic pass

> WHEN faster traffic wants to pass, the DRIVER being passed MUST move to the right and let it pass in safety.

### S2-085. Force should be REQUIREMENT given the cited 'must' wording

*strength* · minor · medium confidence

The rule cites a block that words this rule as an obligation. 28.22 says "When the driver of another vehicle is about to overtake and pass your vehicle, you must:", and 28.26 answers "Move to the right and allow such vehicle to pass." The force table maps "must" to REQUIREMENT. The instructions also say: "When two passages word the same rule differently, record the stronger wording and say so in `note`." The rule nonetheless records force INSTRUCTION, which matches only the plain command in 10.25. The note quotes the 'must' wording but does not act on it. The modal MUST stays the same either way.

- Fix: Set "force": "REQUIREMENT". Change the note to: "10.25 words this as a plain command; the sample test question (28.22, answer 28.26 per key 28.42) words it as 'you must … move to the right and allow such vehicle to pass'; the stronger wording is recorded."
- **Proposed triage: fix as proposed.** BEING-01 force: REQUIREMENT, modal stays MUST. note: "10.25 words this as a plain command; the sample test question (28.22, answer 28.26 per key 28.42) words it as 'you must … move to the right and allow such vehicle to pass'; the stronger wording is recorded."

### S2-086. Answer key not cited, so 28.26 is not shown to be the correct answer

*citation* · minor · medium confidence

The rule relies on 28.26 being the correct answer to question 5. 28.26 is only one of four options, and the stem 28.22 alone does not show which option is correct. Only 28.42 establishes it: "Answer Key: … 5-d …". Without 28.42, the test citations do not support the rule.

- Fix: Change evidence to ["10.25", "28.22", "28.26", "28.42"].
- **Proposed triage: fix as proposed.** BEING-01 evidence: ["10.25", "28.22", "28.26", "28.42"].

### S2-087. Vague phrases not listed in vague_terms

*vague terms* · minor · medium confidence

The statement keeps the handbook's words "move to the right", "faster traffic wants to pass" and "in safety", but vague_terms is empty. "move to the right" does not say whether this means moving to a right lane or toward the right side of the current lane, nor how far. "wants to pass" leaves open how the driver recognises the intent, for example a signal or a vehicle closing from behind. "in safety" gives no criterion. A driving model needs these judgement points flagged.

- Fix: Set vague_terms to [{"term": "move to the right", "explanation": "does not say whether to change lanes or shift within the lane, or how far"}, {"term": "wants to pass", "explanation": "does not say how the intent to pass is recognised"}, {"term": "in safety", "explanation": "no criterion for a safe pass given"}].
- **Proposed triage: fix as proposed.** vague_terms: "move to the right" (does not say whether to change lanes or shift within the lane, or how far), "wants to pass" (does not say how the intent to pass is recognised), "in safety" (no criterion for a safe pass given).

## PASS-BEING-02: Do not speed up when being passed

> WHEN another DRIVER is trying to pass, the DRIVER being passed MUST NOT speed up.

### S2-088. Cites the list intro and a wrong test answer instead of the supporting text

*citation* · minor · medium confidence

The rule rests on 10.20: "…do not speed up when another driver is trying to pass you. It is unlawful and dangerous." Three of the other citations do not support it directly:
- 10.16 ("Here are the steps for passing a vehicle:") only introduces the passer's steps and says nothing about the driver being passed.
- 28.23 ("Speed up so that passing is not necessary.") is a wrong answer option. It is wrong only because of the answer key 28.42 ("5-d"), which is not cited.
- 28.22 is a test question whose correct answer, 28.26 ("Move to the right and allow such vehicle to pass"), is a different action, not "do not speed up".
As cited, the test blocks support the rule only indirectly.

- Fix: Set evidence to ["10.20"]. If the test material is kept as corroboration, cite ["10.20", "28.22", "28.23", "28.42"]. Reword the note to: "Stated as unlawful and dangerous in 10.20; sample test question 5 (28.22) marks 'speed up' (28.23) as a wrong answer per the answer key (28.42)."
- **Proposed triage: partly: keep 10.16 and the test blocks, add the answer key.** 10.20 is a step of the list that 10.16 introduces, so 10.16 stays (a0 C1 ruling). BEING-02 evidence: ["10.16", "10.20", "28.22", "28.23", "28.42"]. note: "Stated as unlawful and dangerous in 10.20; sample test question 5 (28.22) marks 'speed up' (28.23) as a wrong answer per the answer key (28.42)."

### S2-089. Condition does not say whose vehicle is being passed

*clarity* · minor · medium confidence

The condition "another DRIVER is trying to pass" does not say what is being passed, while the actor is named "DRIVER being passed". The handbook is specific, 10.20: "…when another driver is trying to pass you." A reader could take the condition to cover any pass happening nearby, such as one driver passing a third vehicle. It also makes the actor's label depend on the condition.

- Fix: when: "another DRIVER is trying to pass the DRIVER's vehicle"; actor: "DRIVER"; statement: "WHEN another DRIVER is trying to pass the DRIVER's vehicle, the DRIVER MUST NOT speed up."
- **Proposed triage: fix, condition only.** when: "another DRIVER is trying to pass the DRIVER's vehicle"; statement: "WHEN another DRIVER is trying to pass the DRIVER's vehicle, the DRIVER being passed MUST NOT speed up." The actor "DRIVER being passed" stays, to match the rest of the BEING group.

## PASS-BEING-03: Do not block a vehicle from passing

> WHEN another vehicle is passing or trying to pass, the DRIVER MUST NOT drive the vehicle so as to prevent the other vehicle from passing.

### S2-090. Wrong test option cited without the answer key

*citation* · minor · medium confidence

The rule cites 28.24: "Move to the left to prevent passing." Read alone, this block is one of the answer options to 28.22: "When the driver of another vehicle is about to overtake and pass your vehicle, you must:". Taken by itself it seems to support the opposite of the rule. The rule's note says the test marks this option as wrong, but only the answer key shows that: 28.42: "Answer Key: … 5-d …", where the correct option is 28.26, "Move to the right and allow such vehicle to pass." Without 28.42 the citation does not support the note. The rule's main support, 23.19 and 23.22, is enough on its own.

- Fix: Either add 28.42 to the evidence so the note's claim can be checked, giving ["23.19", "23.22", "28.22", "28.24", "28.42"], or drop the sample-test citations, giving ["23.19", "23.22"]. If you drop them, rewrite the note as: "Listed among aggressive driving behaviours under 'Sanctions – dangerous behaviours'."
- **Proposed triage: fix, adding the answer key.** BEING-03 evidence: ["23.19", "23.22", "28.22", "28.24", "28.42"]. The note is unchanged.

## PASS-BEING-04: Being passed on an undivided road: keep right

> WHEN on an undivided road AND the PASSER has pulled into the opposite lane, the DRIVER being passed MUST pay attention to oncoming traffic and move closer to the right side of the lane.

### S2-091. Vague 'move closer to the right side of the lane' not listed in vague_terms

*vague terms* · minor · medium confidence

The action "move closer to the right side of the lane" keeps the handbook's wording, which is correct, but leaves open how far to move toward the right edge. 10.25 gives no distance or lane position: "…pay attention to oncoming traffic and move closer to the right side of the lane." The instructions require each vague phrase kept in the statement to be listed in `vague_terms`, but the list is empty.

- Fix: Set vague_terms to [{"term": "move closer to the right side of the lane", "explanation": "no distance or lateral position given"}].
- **Proposed triage: fix as proposed.** Add `{"term": "move closer to the right side of the lane", "explanation": "no distance or lateral position given"}`.

## PASS-BEING-05: Be ready to slow to help the passer in

> WHEN on an undivided road AND the PASSER has pulled into the opposite lane, the DRIVER being passed MUST be prepared to slow down to let the PASSER get in front more quickly to prevent a collision.

### S2-092. Vague trigger for slowing is not listed in vague_terms

*vague terms* · minor · medium confidence

The action, "be prepared to slow down to let the PASSER get in front more quickly to prevent a collision", does not say when the driver actually has to slow down, or by how much. The handbook leaves this to the driver's judgement. 10.25: "Be prepared to slow down to let the passing driver get in front of you more quickly to prevent a collision." The rule nonetheless has an empty vague_terms list, so a driving model is not told that the moment to act is left open.

- Fix: Add to vague_terms: {"term": "be prepared to slow down", "explanation": "does not say when slowing is needed or by how much"}.
- **Proposed triage: fix as proposed.** Add `{"term": "be prepared to slow down", "explanation": "does not say when slowing is needed or by how much"}`.

## PASS-BEING-06: Clear the truck passing lane

> WHEN driving in the TRUCK PASSING LANE AND a truck wants to pass, the DRIVER MUST move into the right-hand lane as soon as possible.

### S2-093. Handbook phrase 'as soon as you can' replaced by 'as soon as possible'

*vague terms* · minor · medium confidence

The instructions say to keep the handbook's own words for vague phrases. 10.26 says "move into the right-hand lane as soon as you can", but the rule says "as soon as possible" and only mentions the original wording in the note. The meaning is close, but the vague term should be quoted as the handbook words it.

- Fix: action: "move into the right-hand lane as soon as the DRIVER can"; statement: "WHEN driving in the TRUCK PASSING LANE AND a truck wants to pass, the DRIVER MUST move into the right-hand lane as soon as the DRIVER can."; vague_terms: [{"term": "as soon as the DRIVER can", "explanation": "no time or distance given"}]; note: "".
- **Proposed triage: not an error, no change.** Paraphrasing a vague phrase close to the handbook is fine (a0 G5).

### S2-094. 'a truck wants to pass' is vague but not listed

*vague terms* · minor · medium confidence

The condition "a truck wants to pass" does not say how the driver can tell (signal, closing speed, following closely). A driving model cannot detect intent directly. The phrase comes from 10.26, so it should stay, but it should be listed in vague_terms.

- Fix: Add to vague_terms: {"term": "a truck wants to pass", "explanation": "does not say how the truck's intent to pass is recognized"}.
- **Proposed triage: fix as proposed.** Add `{"term": "a truck wants to pass", "explanation": "does not say how the truck's intent to pass is recognized"}`.

### S2-095. 12.24 does not state the move-over instruction

*citation* · minor · low confidence

The instruction to move right when a truck wants to pass is stated only in 10.26. 12.24 says "large trucks cannot travel in the far left lane and must use the lane to the right for passing" and gives the general advice "Drive in the right-hand lane when possible". That passage supports the TRUCK PASSING LANE concept, which the vocabulary entry already covers, but not this rule's action. It also uses weaker, general wording.

- Fix: Set evidence to ["10.26"]. If 12.24 is kept, add a note: "12.24 confirms that trucks use the lane right of the far left lane for passing on freeways with three or more lanes each way; the move-over instruction itself is in 10.26."
- **Proposed triage: fix as proposed.** BEING-06 evidence: ["10.26"]. 12.24 stays cited on PASS-GEN-07 and the TRUCK PASSING LANE vocabulary entry.

### S2-096. 'right-hand lane' could be read as the rightmost lane

*ambiguity* · minor · low confidence

In 10.26 "the right-hand lane" means the lane to the right of the truck passing lane, but a driving model could read it as the rightmost lane of the road. On a road with four or more lanes each way, these are different lanes.

- Fix: action: "move into the lane to the right of the TRUCK PASSING LANE as soon as the DRIVER can"; add a note: "Handbook says 'the right-hand lane'; read as the lane to the right of the truck passing lane."
- **Proposed triage: fix, action only.** action: "move into the lane to the right of the TRUCK PASSING LANE as soon as possible"; statement updated to match. The vague term "as soon as possible" and the note stay.

## PASS-BEING-07: Cyclists may take the lane to discourage unsafe passing

> WHEN travelling slower than other traffic AND the lane is too narrow to be shared safely, the CYCLIST or rider of a moped MAY use any part of the lane to discourage passing.

### S2-097. The handbook's 'if necessary for safety' qualifier is dropped

*fidelity* · minor · medium confidence

Block 6.24 grants the permission only as a safety measure: "However, they can use any part of the lane if necessary for safety, such as to:". Block 6.27 then lists the case: "Discourage passing where the lane is too narrow to be shared safely". The rule's action, "use any part of the lane to discourage passing", leaves out the safety purpose. The 'too narrow to be shared safely' condition already implies it, so the practical meaning barely changes, but the handbook's framing is lost.

- Fix: Set action: "use any part of the lane, where necessary for safety, to discourage passing". The statement becomes: "WHEN travelling slower than other traffic AND the lane is too narrow to be shared safely, the CYCLIST or rider of a moped MAY use any part of the lane, where necessary for safety, to discourage passing." Add "where necessary for safety" to vague_terms with the explanation "does not say who judges necessity or how".
- **Proposed triage: not an error, no change.** The condition "too narrow to be shared safely" already carries the safety purpose.

## PASS-TOW-01: Towing: enough time and room to pass

> WHEN about to pass another vehicle, the DRIVER towing a trailer MUST make sure there is enough time and room to complete the PASS.

### S2-098. Lowercase 'pass' in the condition names the defined term PASS

*vocabulary* · minor · medium confidence

The rule's `when` field reads "about to pass another vehicle" with "pass" in lowercase. Its `action` field then writes "complete the PASS" in capitals. Both refer to the same manoeuvre, the vocabulary term PASS ("Changing lanes to move past a slower vehicle", 10.14). The instructions require a word that names a vocabulary term with its defined meaning to be written in CAPITALS. Mixing the two forms in one rule invites reading the condition as something other than the defined manoeuvre. The source is 27.45: "Before you pass, make sure you have enough time and room to complete the pass."

- Fix: Set `when` to "about to PASS another vehicle". Set `statement` to "WHEN about to PASS another vehicle, the DRIVER towing a trailer MUST make sure there is enough time and room to complete the PASS."
- **Proposed triage: not an error, no change.** Same as S2-001.

## PASS-TOW-02: Towing: do not cut back in too soon

> WHEN returning to the lane after passing, the DRIVER towing a trailer MUST allow more room before moving back and not cut back into the lane too soon.

### S2-099. "More room" has no stated comparison

*clarity* · minor · medium confidence

The action says "allow more room before moving back" but never says more than what. Read alone, the rule gives a driving model no baseline. The handbook ties the extra room to the trailer's length. 27.45: "You also need more space because the length of your vehicle is much longer with a trailer attached… Once you have passed, allow more room before you move back to your lane." The implied comparison is with driving without a trailer.

- Fix: action: "allow more room than when not towing before moving back to the original lane, and not cut back into the lane too soon"; vague_terms entry: {"term": "more room than when not towing", "explanation": "no distance given"}
- **Proposed triage: fix, without a new vague term.** action: "allow more room than when not towing before moving back and not cut back into the lane too soon"; statement updated to match. The existing vague term "more room" stays.

### S2-100. "The lane" is unclear; the handbook means the driver's own lane

*clarity* · minor · medium confidence

The when and action say "returning to the lane" and "cut back into the lane" without saying which lane. The handbook says "move back to your lane" (27.45), meaning the lane the driver left to pass.

- Fix: when: "returning to the original lane after passing"; statement: "WHEN returning to the original lane after passing, the DRIVER towing a trailer MUST allow more room than when not towing before moving back and not cut back into the lane too soon."
- **Proposed triage: fix as proposed.** when: "returning to the original lane after passing"; statement updated to match (combined with S2-099).

### S2-101. A prohibition is folded into a MUST action

*form* · minor · low confidence

The action "allow more room … and not cut back into the lane too soon" puts the handbook's "Do not cut back…" (a MUST NOT) inside a MUST rule as a negated verb. It is close to the same instruction, so keeping one entry is defensible. Still, the grammar's modal no longer shows the prohibition, which a program reading the modal field could miss.

- Fix: Keep the action as "allow more room before moving back, so as not to cut back into the lane too soon". Alternatively, add a note that "Do not cut back into the lane too soon" is restated as part of the same MUST instruction.
- **Proposed triage: not an error, no change.** Same as S2-011 (a0 M3 pattern).

## PASS-TOW-03: Towing: let a line of traffic pass

> WHEN holding up a line of traffic, the DRIVER towing a trailer MUST signal, pull over and let the other vehicles pass.

### S2-102. Vague condition "holding up a line of traffic" not listed in vague_terms

*vague terms* · minor · medium confidence

The rule's `when` field, "holding up a line of traffic", leaves a judgement to the driver. 27.47 says: "If you are holding up a line of traffic, signal, pull over and let the other vehicles pass." It does not say how many vehicles make a "line", or how long or how much they must be delayed before the driver counts as "holding up" traffic. The instructions require every vague phrase kept in the statement to be listed in `vague_terms`, but the rule's list is empty. A driving model therefore gets no warning that this trigger is a judgement call.

- Fix: Set vague_terms to [{"term": "holding up a line of traffic", "explanation": "no number of following vehicles or amount of delay given"}].
- **Proposed triage: fix as proposed.** Add `{"term": "holding up a line of traffic", "explanation": "no number of following vehicles or amount of delay given"}`.

## PASS-TOW-04: Towing: wind from a passing truck or bus

> WHEN a large bus or truck passes AND its wind pushes the trailer to the side, the DRIVER towing a trailer MUST carefully steer the vehicle and trailer back into position and not brake.

### S2-103. Prohibition 'not brake' is folded into a MUST action

*grammar* · minor · medium confidence

The action "carefully steer the vehicle and trailer back into position and not brake" puts a prohibition inside a MUST rule. The handbook gives two separate commands, 27.47: "do not brake. Carefully steer your vehicle and trailer back into position." The grammar has a MUST NOT modal for prohibitions. Hiding "not brake" at the end of a MUST action makes the prohibition easy to miss and hard to compare with other rules. The handbook also puts the prohibition first.

- Fix: Split the rule into two. (1) PASS-TOW-04: modal "MUST NOT", action "brake", statement "WHEN a large bus or truck passes AND its wind pushes the trailer to the side, the DRIVER towing a trailer MUST NOT brake." (2) PASS-TOW-05: modal "MUST", action "carefully steer the vehicle and trailer back into position", statement "WHEN a large bus or truck passes AND its wind pushes the trailer to the side, the DRIVER towing a trailer MUST carefully steer the vehicle and trailer back into position." Cite 27.47 for both.
- **Proposed triage: not an error, no change.** TOW-04 was reworded to this pattern in a0 M3.

### S2-104. Vague word 'carefully' not listed

*vague terms* · minor · medium confidence

The statement keeps the handbook's word "carefully" (27.47: "Carefully steer your vehicle and trailer back into position"), but `vague_terms` is empty. The word leaves open how gently or gradually to steer, which is a judgement left to the driver.

- Fix: Set vague_terms to [{"term": "carefully", "explanation": "does not say how gently or gradually to steer"}].
- **Proposed triage: fix as proposed.** Add `{"term": "carefully", "explanation": "does not say how gently or gradually to steer"}`.

## No findings (14 rules)

PASS-GEN-03, PASS-PROC-04, PASS-PROC-06, PASS-NIGHT-01, PASS-LOC-04, PASS-LOC-05, PASS-LOC-06, PASS-SIDE-01, PASS-SIDE-03, PASS-USER-03, PASS-USER-08, PASS-USER-12, PASS-USER-15, PASS-WX-01
