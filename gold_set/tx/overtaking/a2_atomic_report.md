# Atomic check (stage 2): gold_set/tx/overtaking/a1_format.json

Judge: anthropic/claude-opus-5-5 · run folder: `runs\20261121-210359-check-atomic-overtaking-a2` (requests, responses, findings.jsonl, triage.csv) · 57 rules checked, 0 failed calls · $1.3602

**87 findings** (20 major, 67 minor) in 46 rules.

**Proposed triage:** each finding has a **Proposed triage** line under its fix. The decisions follow the rulings from the a0 and a1 triages. All proposed fixes have been applied to `a2_atomic.json`, which started as an exact copy of `a1_format.json`: 25 rules changed and 1 rule added, with every statement rebuilt from its fields. Stage 1 on `a2_atomic.json` passes all 8 checks with no format errors (58 rules, 16 vocab terms).
- 37 findings are proposed for a fix (some partly or in a changed form), and 50 are proposed as not an error or rejected.
- 14 findings (10 of them major) come from what the judge was shown, not from the rules: S2-012, 014, 016, 017, 018, 020, 021, 026, 029, 034, 043, 059, 079, 080. Each cited block is labelled only with its chapter section (the h2). The judge never saw the nearer heading that sets the rule's condition: 7.34 "How to Pass on a Two-Lane Road", 7.47 "When Another Vehicle is Passing", 6.186, 6.196, 6.242 and 10.128. Headings are not cited (a0 C1), so these are proposed as rejected.
- Most of the other rejections repeat rulings from the a0 and a1 triages:
  - lowercase "pass" as a verb is allowed (V1);
  - the positive-then-negated pattern stands (M1);
  - alternatives may be joined by a lowercase "or" inside one fact (G1);
  - SIDE-02 keeps MAY ONLY (G3);
  - "passing" a sign is not overtaking (G4);
  - "especially at night" stays in USER-05's note (G5);
  - SIGN-03 and SIGN-04 are in scope (M6.3, M6.4);
  - USER-15/16 stay split by lane count, and SERVICE VEHICLE keeps its empty evidence (M6.1);
  - "DRIVER of the school bus" stays (a1).
- One rule is added: PASS-USER-17 "Never cross behind a backing truck", split from USER-11 (S2-063). It goes at the end of its group, so no ids change.

## PASS-GEN-02: Make certain the way is clear

> WHEN about to pass, the PASSER MUST make certain the way is clear.

### S2-001. The defined term PASS is written in lowercase

*vocabulary* · minor · low confidence

The condition reads "about to pass" in lowercase. The PASSER vocabulary entry is defined as "The driver making a PASS.", so PASS is a defined term in this rule set. Using lowercase "pass" for the same manoeuvre breaks the instruction that a phrase naming a vocabulary term with its defined meaning should be written in CAPITALS. The meaning does not change.

- Fix: when: "about to PASS"; statement: "WHEN about to PASS, the PASSER MUST make certain the way is clear."
- **Proposed triage: not an error, no change.** Lowercase "pass" as a verb is allowed: a0 V1 lowercased the verb on purpose and kept PASS in CAPS for the noun.

## PASS-GEN-03: Signal before changing lanes to pass

> WHEN changing lanes to pass, the PASSER MUST give the proper signal before changing lanes.

### S2-002. "proper signal" is not listed as a vague term

*vague terms* · minor · medium confidence

The action reads "give the proper signal before changing lanes". Block 7.31 ("Give the proper signal before changing lanes.") does not say which signal is proper or how long before the lane change it must be given. That is a judgement left to the driver, so the phrase belongs in `vague_terms`, but the list is empty.

- Fix: Set vague_terms to [{"term": "the proper signal", "explanation": "neither which signal nor how far in advance is stated"}].
- **Proposed triage: fix as proposed.** Add `{"term": "the proper signal", "explanation": "does not say which signal or how far in advance"}` to GEN-03's vague_terms.

### S2-003. "pass" is in lowercase although PASS is a defined term

*vocabulary* · minor · low confidence

The condition "changing lanes to pass" uses the word that the PASSER entry relies on ("The driver making a PASS."), but writes it in lowercase. This is inconsistent with the defined term and blurs whether the defined meaning applies here.

- Fix: Set when to "changing lanes to PASS". The statement then reads: "WHEN changing lanes to PASS, the PASSER MUST give the proper signal before changing lanes."
- **Proposed triage: not an error, no change.** Same as S2-001.

## PASS-GEN-04: Tap horn when necessary

> WHEN passing AND it is necessary to avoid surprising or to alert the DRIVER ahead, the PASSER MUST tap the horn.

### S2-004. Lowercase 'passing' in the condition instead of the defined term PASS

*vocabulary* · minor · medium confidence

The rule's actor is PASSER, defined as "The driver making a PASS", so PASS is a vocabulary term. The condition still uses the lowercase word: "WHEN passing AND it is necessary…". The instructions say a word that names a vocabulary term with its defined meaning should be written in CAPITALS. Leaving it lowercase makes it unclear whether the condition means the same manoeuvre as PASS. The condition is also redundant with the actor: a PASSER is by definition making a PASS.

- Fix: when: "making a PASS AND it is necessary to avoid surprising or to alert the DRIVER ahead"; statement: "WHEN making a PASS AND it is necessary to avoid surprising or to alert the DRIVER ahead, the PASSER MUST tap the horn."
- **Proposed triage: not an error, no change.** Same as S2-001.

## PASS-GEN-05: Avoid cutting in too quickly

> WHEN returning to the original lane after a PASS, the PASSER SHOULD NOT cut in too quickly.

### S2-005. Condition narrows "if you must return" to after a completed pass

*faithfulness* · minor · low confidence

7.33 says: "Avoid cutting in too quickly if you must return to your original lane." The words "if you must return" describe a return that may not always happen. That fits a driver who has to abandon a pass and pull back in, at least as well as one who has finished it. The rule's condition "returning to the original lane after a PASS" covers only the completed pass and adds no note on the other reading. A driving model would then not apply the advice when it pulls back in from a pass it could not finish.

- Fix: Set when: "returning to the original lane during or after a PASS". Set statement: "WHEN returning to the original lane during or after a PASS, the PASSER SHOULD NOT cut in too quickly." Add note: "Handbook wording 'if you must return to your original lane' may refer to completing a pass or to abandoning one; the rule covers both."
- **Proposed triage: not an error, no change.** Low confidence. "If you must return" reads as "if you need to return": after passing on a multi-lane road the PASSER may stay in the left lane. 7.33 is in the list of safety rules for when you are passing, and it does not mention giving up a pass.

## PASS-GEN-06: Do not linger in the other driver's blind spot

> WHEN passing another vehicle, the PASSER MUST either complete the PASS or slow down out of the other DRIVER's BLIND SPOT, and not drive or linger in it.

### S2-006. Prohibition folded into a MUST action

*grammar* · minor · medium confidence

The handbook's core command is a prohibition, 7.53: "do not drive or linger in the other driver's blind spot." The rule's action, "either complete the PASS or slow down out of the other DRIVER's BLIND SPOT, and not drive or linger in it", puts a MUST NOT inside a MUST action. This mixes two modals in one statement and makes the prohibition read like an afterthought.

- Fix: Make the prohibition the rule: modal "MUST NOT", action "drive or linger in the other DRIVER's BLIND SPOT". Statement: "WHEN passing another vehicle, the PASSER MUST NOT drive or linger in the other DRIVER's BLIND SPOT." Put the remedy (either complete the PASS or slow down out of the BLIND SPOT) in the note or in a separate MUST rule.
- **Proposed triage: not an error, no change.** Positive phrase first and negated phrase last is the accepted pattern, and GEN-06 was reworded to it in a0 M1.

### S2-007. "linger" not listed as vague

*vague terms* · minor · medium confidence

The statement keeps the handbook's word "linger", which gives no duration: how long a PASSER may stay in the BLIND SPOT before it counts as lingering. Yet vague_terms is empty.

- Fix: Add to vague_terms: {"term": "linger", "explanation": "no time limit given for staying in the blind spot"}.
- **Proposed triage: fix as proposed.** Add `{"term": "linger", "explanation": "no time given for staying in the blind spot"}`.

### S2-008. 10.48 is a broader rule, not only about passing

*citation* · minor · low confidence

10.48 reads "Stay out of another driver's blind spot… Stay behind or go around the other vehicle. Do not follow to the side." It applies to all highway driving, not just to passing. The note calls it the same rule "stated again", which hides that the handbook's scope there is wider.

- Fix: Change the note to: "10.48 (Highway Driving) gives a broader version that applies to all highway driving, not just passing: stay behind or go around the other vehicle, do not follow to the side."
- **Proposed triage: fix, last sentence of the note only.** GEN-06 note, last sentence: "Stated more broadly under Highway Safety Tips (10.48), for all driving, not only passing: stay behind or go around the other vehicle, and do not follow to the side." The diagram and reason sentences stay. 10.48 is under Highway Safety Tips, so the note keeps that name; the judge was shown only the chapter section "Highway Driving".

## PASS-GEN-08: Left lane for passing only

> WHEN on a roadway with more than one lane in the same direction AND a 'Left Lane for Passing Only' sign is posted, the DRIVER MUST NOT travel in the farthest left lane, UNLESS passing.

### S2-009. Exception 'passing' is lowercase rather than a defined term

*vocabulary* · minor · low confidence

The exception reads "UNLESS passing". Passing is the key notion of this rule set, which normally defines it as a term (e.g. PASS, "changing lanes to move past a slower vehicle, then returning to the original lane"). Here it is written in lowercase and is neither linked to a vocabulary entry nor listed as a vague term. A reader cannot tell whether a driver who is preparing to pass, or has just finished passing, counts as "passing". The handbook wording is 6.148: "The farthest left lane is for passing only."

- Fix: If PASS is defined in the vocabulary, set unless to "making a PASS" and the statement to: "WHEN on a roadway with more than one lane in the same direction AND a 'Left Lane for Passing Only' sign is posted, the DRIVER MUST NOT travel in the farthest left lane, UNLESS making a PASS." If PASS is not defined, add a vocabulary entry for it.
- **Proposed triage: not an error, no change.** Same as S2-001. PASS is in the vocabulary, and "UNLESS passing" uses the verb, as 6.148 does ("for passing only").

## PASS-GEN-09: Use middle or left lane on highway to pass

> WHEN passing other vehicles on a multi-lane FREEWAY, the PASSER MUST use the middle or left lane.

### S2-010. FREEWAY scope is not supported by the cited block

*citation* · minor · medium confidence

The rule limits itself to "a multi-lane FREEWAY". The only cited block does not mention freeways or the number of lanes: 10.23: "Use the middle or left lane if you are traveling faster than other traffic or passing other vehicles." The freeway setting comes only from the section heading "Highway Driving" and from 10.13, which is cited only in the vocabulary. As cited, the road-type condition has no support.

- Fix: Add the block that places this list item in the freeway context: 10.13, or the lead-in line of the list if it is a separate block. Add a note that the FREEWAY and multi-lane condition is inferred from the section 'Highway Driving' and 10.13.
- **Proposed triage: fix, citation and note.** This is a real gap, not a missing heading: the headings above 10.23 ("Driving on the Highway", "Choose the Proper Lane") say highway, not freeway. The FREEWAY setting comes from 10.13, the opening paragraph of the section (a0 M5). GEN-09 evidence: ["10.13", "10.23"]. Add to the note: "The FREEWAY setting comes from the Highway Driving section that 10.23 is in, which opens with 10.13."

### S2-011. The 'traveling faster than other traffic' condition is dropped without a note

*completeness* · minor · low confidence

10.23 gives two triggers for using the middle or left lane: "if you are traveling faster than other traffic or passing other vehicles." The rule keeps only the passing trigger and does not say the other was left out. Leaving it out may be reasonable for the overtaking topic, but a checker comparing the rule with 10.23 cannot tell whether that was deliberate.

- Fix: Add to note: "10.23 also tells drivers traveling faster than other traffic to use the middle or left lane; that part is outside the overtaking topic and is not included."
- **Proposed triage: not an error, no change.** Choosing a lane for speed is outside the topic. Leaving out the part of a block that is not about passing does not change the rule.

## PASS-PROC-01: Keep distance to see ahead

> WHEN preparing to pass on a two-lane road, the PASSER MUST keep enough distance from the car in front to see ahead clearly.

### S2-012. "two-lane road" condition not supported by the cited block

*citation* · major · medium confidence

The rule restricts itself to "preparing to pass on a two-lane road", but the only cited block says nothing about road type. 7.35 reads: "Keep enough distance between you and the car in front of you so you can see ahead clearly. …" It is a list item, so the two-lane context may come from an introductory line that is not cited. As written, the rule's key condition has no support in its citations, and a driving model could wrongly decide the step does not apply on multi-lane roads.

- Fix: Add the block that introduces this list and states the two-lane context (if it does) to `evidence`. Otherwise change `when` to "preparing to pass" and `statement` to "WHEN preparing to pass, the PASSER MUST keep enough distance from the car in front to see ahead clearly."
- **Proposed triage: rejected, no change.** The two-lane condition comes from the heading 7.34 "How to Pass on a Two-Lane Road", which introduces the list 7.35–7.39. Headings are not cited, and a0 C1 named this list. The judge was shown only the chapter section "Passing", not the heading (see the note at the top).

### S2-013. Vague phrase "see ahead clearly" not listed in vague_terms

*vague terms* · minor · medium confidence

The action ends "to see ahead clearly", which comes from 7.35: "…so you can see ahead clearly". It is a vague standard that gives no sight distance or criterion, yet only "enough distance" is listed in `vague_terms`.

- Fix: Add to vague_terms: {"term": "see ahead clearly", "explanation": "no sight distance or criterion given"}.
- **Proposed triage: fix as proposed.** Add `{"term": "see ahead clearly", "explanation": "no sight distance given"}`.

## PASS-PROC-02: Check mirrors and blind spot before passing

> WHEN preparing to pass on a two-lane road, the PASSER MUST check the rearview mirror and side mirrors and look over the shoulder into the BLIND SPOT to make sure the roadway is clear and no other vehicles are passing the PASSER.

### S2-014. 'Preparing to pass on a two-lane road' is not supported by the cited block

*citation* · major · medium confidence

The condition "preparing to pass on a two-lane road" restricts the rule to two-lane roads. The only cited block is a bare list item, 7.35: "Keep enough distance … Check the rearview mirror, your side mirrors, and look over your shoulder in your blind spot … Turn on your left turn signal…". It mentions neither passing preparation nor a two-lane road. The scope restriction, and even the link to passing, rests on text that is not cited. If no such limit exists, the rule wrongly leaves out passes on multi-lane roads.

- Fix: Add the block that introduces this list and states it applies when preparing to pass on a two-lane road. If no such block exists, change `when` to "preparing to pass". Add a note saying the condition comes from the list's introduction.
- **Proposed triage: rejected, no change.** Same as S2-012.

### S2-015. Vague 'the roadway is clear' not listed

*vague terms* · minor · medium confidence

The action requires making sure "the roadway is clear", but gives no distance or gap for what counts as clear. `vague_terms` is empty, although the phrase appears in the statement.

- Fix: Set vague_terms to [{"term": "the roadway is clear", "explanation": "no distance or gap given"}].
- **Proposed triage: fix as proposed.** Add `{"term": "the roadway is clear", "explanation": "no gap or sight distance given"}`, the explanation GEN-02 gives for "the way is clear".

## PASS-PROC-03: Left turn signal before passing

> WHEN preparing to pass on a two-lane road, the PASSER MUST turn on the left turn signal to alert DRIVERS behind.

### S2-016. "On a two-lane road" is not supported by the cited block

*citation* · minor · medium confidence

The condition "preparing to pass on a two-lane road" limits the rule to two-lane roads. The only cited block, 7.35, says nothing about the type of road: 7.35: "Keep enough distance … Check the rearview mirror … Turn on your left turn signal to alert any drivers behind you." Block 7.35 is a list item, so the two-lane condition probably comes from an introducing line or heading that is not cited. As cited, the rule's scope is not supported by its evidence.

- Fix: Add to `evidence` the block that introduces this list and states the two-lane road context (the list's lead-in line or heading, e.g. the block just before 7.35). If no such block exists, drop the qualifier: "when": "preparing to pass", "statement": "WHEN preparing to pass, the PASSER MUST turn on the left turn signal to alert DRIVERS behind."
- **Proposed triage: rejected, no change.** Same as S2-012.

## PASS-PROC-04: Check ahead for no-passing zones and oncoming traffic

> WHEN preparing to pass on a two-lane road, the PASSER MUST check well ahead for signs and pavement markings of a NO-PASSING ZONE and check for oncoming traffic in the left lane.

### S2-017. "on a two-lane road" is not supported by the cited block

*citation* · major · medium confidence

The rule's condition is "preparing to pass on a two-lane road". The only cited block, 7.36, says just: "Check well ahead for signs and pavement markings for no passing zones, and always check for oncoming traffic in the left lane." It says nothing about two-lane roads. This qualifier narrows when the rule applies. It may come from a list introduction elsewhere in the handbook, but that block is not cited, so as written the restriction has no support.

- Fix: Add to `evidence` the block that introduces the list containing 7.36, if it mentions two-lane roads. Otherwise remove the qualifier: when = "preparing to pass"; statement = "WHEN preparing to pass, the PASSER MUST check well ahead for signs and pavement markings of a NO-PASSING ZONE and check for oncoming traffic in the left lane."
- **Proposed triage: rejected, no change.** Same as S2-012.

## PASS-PROC-05: Return before oncoming car is within 200 feet

> WHEN passing on a two-lane road, the PASSER MUST be sure there is enough time and space to overtake the car ahead and return to the right lane before an approaching car comes within 200 feet.

### S2-018. "two-lane road" condition is not supported by the cited block

*unsupported condition* · major · medium confidence

The rule's `when` is "passing on a two-lane road". The cited block does not mention two-lane roads. 7.36 says: "…always check for oncoming traffic in the left lane. Be sure you have enough time and space to overtake the car ahead and return to the right lane before an approaching car comes within 200 feet of you." The block states the check for any pass. Limiting it to two-lane roads narrows when the rule applies, and that limit is not supported by the citation.

- Fix: Set when to "passing a vehicle ahead" and statement to "WHEN passing a vehicle ahead, the PASSER MUST be sure there is enough time and space to overtake the car ahead and return to the right lane before an approaching car comes within 200 feet of the PASSER." If the two-lane context comes from another block, cite that block and explain it in the note.
- **Proposed triage: rejected, no change.** Same as S2-012. The "of you" point is S2-019.

### S2-019. Reference point of the 200 feet is dropped

*clarity* · minor · medium confidence

The handbook says "before an approaching car comes within 200 feet of you". The rule says only "comes within 200 feet" and drops "of you". It no longer says the distance is measured from the passer's vehicle.

- Fix: End the action with "…before an approaching car comes within 200 feet of the PASSER's vehicle" and update the statement to match.
- **Proposed triage: fix.** action ends "…before an approaching car comes within 200 feet of the PASSER"; statement updated to match. "The PASSER" stands for the handbook's "you", as in PROC-02 (a0 G7).

## PASS-PROC-06: Pass on the left and clear before returning

> WHEN passing on a two-lane road, the PASSER MUST pass on the left and not return to the right lane until the overtaken vehicle is safely cleared and visible in the rearview mirror.

### S2-020. Rule is narrowed to two-lane roads, which the text does not do

*condition* · major · medium confidence

The rule's condition is "passing on a two-lane road". The cited text sets no such limit. 7.38 says: "Pass on the left and do not return to the right lane until you have safely cleared the overtaken vehicle. Wait until you can see the car you have just passed in your rearview mirror before returning…" The only mention of a two-lane road is the alt text of the illustrative diagram 7.40 ("a car passes another car on a two-lane road"). A diagram that illustrates a general instruction does not limit where the instruction applies. As written, a driving model would not apply the pass-on-the-left and clearance requirement when passing on other roads, which the handbook does not intend.

- Fix: Set when to "passing another vehicle". The statement then reads: "WHEN passing another vehicle, the PASSER MUST pass on the left and not return to the right lane until the overtaken vehicle is safely cleared and visible in the rearview mirror." Change the note to: "Diagram 7.40 illustrates the manoeuvre on a two-lane road: the passing car moves into the left lane and back to the right lane ahead of the overtaken car. The text in 7.38 is not limited to two-lane roads."
- **Proposed triage: rejected, no change.** Same as S2-012. 7.38 is in the same list under 7.34, so the two-lane setting comes from the heading, not only from diagram 7.40.

## PASS-PROC-07: Signal right to return and cancel signal

> WHEN the PASSER has overtaken the vehicle being passed on a two-lane road, the PASSER MUST turn on the right turn signal, return to the right lane, and turn the signal off after the lane change is completed.

### S2-021. "on a two-lane road" is not supported by the cited block

*citation* · major · medium confidence

The condition limits the rule to "on a two-lane road". The only cited block says nothing about road type: 7.39: "Turn on your right turn signal and return to the right lane. Be sure to turn your signal off after you have completed the lane change." The restriction probably comes from the list's introduction or a nearby block, but neither is cited. As written, the rule's scope is unsupported by its evidence, and it may wrongly exclude multi-lane roads.

- Fix: Cite the block that introduces the list of passing steps and states the two-lane context, if it exists. Otherwise drop the phrase: "when": "the PASSER has overtaken the vehicle being passed".
- **Proposed triage: rejected, no change.** Same as S2-012.

### S2-022. The point at which return is allowed is left vague and not flagged

*vague terms* · minor · medium confidence

"has overtaken the vehicle being passed" does not say when the PASSER is far enough ahead to move back into the right lane. Block 7.39 itself gives no such cue. A driving model reading only this rule cannot tell when the step applies. The phrase is not listed in vague_terms, and the note does not mention it.

- Fix: Add the vague term {"term": "has overtaken the vehicle being passed", "explanation": "does not say how far ahead the PASSER must be before returning"}. If a neighbouring list item gives a concrete cue (for example, seeing the passed vehicle in the mirror), cite that block and use its wording instead.
- **Proposed triage: not an error, no change.** The condition was set in a0 G2, using 7.38's own word "overtaken". When the PASSER may return is PROC-06's rule ("safely cleared" is a vague term there, and the mirror check is in its action).

## PASS-LOC-01: No left side on roads with two or more lanes each way

> WHEN there are two or more traffic lanes in each direction, the DRIVER MUST NOT drive on the left side of the road.

### S2-023. "left side of the road" can be misread as the left lane of the driver's own direction

*ambiguity* · minor · medium confidence

The rule says the DRIVER "MUST NOT drive on the left side of the road" when "there are two or more traffic lanes in each direction." On a multi-lane road, a driving model could read "left side of the road" as the left-hand lane(s) of its own direction. That would forbid ordinary left-lane driving and passing. In the handbook, 7.17 ("Never drive on the left side of the road when:") appears in the Passing section. In that context it means the half of the road used by oncoming traffic, i.e. crossing the centre line to pass. The rule copies the handbook's wording faithfully, so its meaning is not wrong. But neither the rule nor the note resolves this reading, which matters because the condition itself mentions multiple lanes in the driver's direction.

- Fix: Keep the action wording and set note to: "Worded 'Never drive on the left side of the road when...' in the Passing section; 'left side of the road' means the half of the road used by oncoming traffic (crossing the centre line), not the left lane of the driver's own direction." Alternatively, change action to "drive on the left side of the road (the half used by oncoming traffic)" and update statement to match.
- **Proposed triage: fix, note only.** The action keeps the handbook's words. LOC-01 note: "Worded 'Never drive on the left side of the road when...'. In the Passing section, the left side of the road is the half used by oncoming traffic, across the center line, not the left lane of the DRIVER's own direction."

## PASS-LOC-03: Not on hills, curves or where vision is limited

> WHEN on a hill, curve, or any other place where vision is limited, the DRIVER MUST NOT drive on the left side of the road.

### S2-024. "hill" and "curve" are not listed as vague terms

*vague terms* · minor · low confidence

The rule's condition reads "on a hill, curve, or any other place where vision is limited". Only "vision is limited" is listed in vague_terms. "hill" and "curve" are also left open. The handbook (7.22: "On a hill, curve, or any other place where vision is limited") gives no grade, crest proximity or curvature. A driving model cannot tell whether any slope or bend triggers the prohibition, or only those that block the view ahead. The phrase "any other place where vision is limited" suggests the hill or curve matters because it limits vision, but the rule does not make this explicit.

- Fix: Add to vague_terms: {"term": "hill", "explanation": "no grade or distance from crest given; presumably one that limits the view ahead"} and {"term": "curve", "explanation": "no sharpness given; presumably one that limits the view ahead"}. Optionally add a note: "The handbook groups hills and curves with other places where vision is limited."
- **Proposed triage: fix, without the optional note.** Add `{"term": "hill", "explanation": "no grade or distance from the crest given"}` and `{"term": "curve", "explanation": "no sharpness given"}`, before "vision is limited".

## PASS-LOC-05: Never pass in the center left-turn lane

> WHEN on a road with a CENTER LEFT-TURN LANE, the DRIVER MUST NOT use the CENTER LEFT-TURN LANE for passing or as a through-traffic lane.

### S2-025. Note gives repetition as a reason for the REQUIREMENT force

*strength* · minor · medium confidence

Both text passages use advisory wording. 6.149 says "…should never be used for passing or moving through traffic" and 6.195 says "The center lane should never be used for passing or as a through-traffic lane." The only basis for REQUIREMENT is the regulatory 'CENTER LANE ONLY' sign (6.149-f1), together with 6.115: "Drivers must obey all regulatory signs in the same manner as traffic laws." The note also says the rule was raised because it is "stated twice". Repeating advisory wording does not make it an obligation, so this reasoning misstates why the stronger force applies. The force itself can stand on the sign.

- Fix: Change note to: "Both text passages (6.149, 6.195) word this as 'should never be used'; recorded as REQUIREMENT because the rule is also shown on the regulatory 'CENTER LANE ONLY' sign (6.149-f1), and 6.115 says drivers must obey regulatory signs as traffic laws."
- **Proposed triage: fix as proposed, with the sign named as before.** LOC-05 note: "Both text passages (6.149, 6.195) word this as 'should never be used'; recorded as REQUIREMENT because it is shown on a regulatory 'Center Lane Only' sign (6.149-f1), and 6.115 says drivers must obey regulatory signs in the same manner as traffic laws."

## PASS-MARK-01: Broken line: passing allowed if safe

> WHEN the line the PASSER would cross to pass another vehicle is a BROKEN LINE AND it is safe, the PASSER MAY cross it.

### S2-026. Note adds 'two-lane rural road', which the cited block does not say

*note accuracy* · minor · high confidence

The note says: "On a two-lane rural road the broken yellow center line may also be crossed when the right half of the road is closed." The cited block says only 6.187: "You may cross a broken line when passing another vehicle or when the right half of the road is closed." Nothing in the cited blocks limits this to a 'rural' or 'two-lane' road, so that qualifier is not supported by the citations.

- Fix: Change the note to: "6.187 also permits crossing a broken line when the right half of the road is closed; that permission is not about passing and is left out of this rule."
- **Proposed triage: rejected, no change.** Same as S2-012. 6.187 is under the heading 6.186 "Two-Lane Rural Road with Two-Way Traffic", so the note gives the block's own setting. The judge was shown only "Pavement Markings".

### S2-027. No exception when a solid yellow line is on the passer's side of a combined line

*missing exception* · minor · medium confidence

The condition "the line the PASSER would cross … is a BROKEN LINE" does not say what to do with a combined solid-and-broken center line. The cited figure 6.201 shows exactly such a line. The handbook says 6.200: "A solid yellow line on your side of the road marks a 'no-passing zone.'" and 6.187: "Do not cross the line if … it is a solid yellow line." A model facing a broken line paired with a solid line could read the rule as permitting a pass even when the solid line is on its own side.

- Fix: Set unless to "a solid yellow line is on the PASSER's side of the center line". Statement: "WHEN the line the PASSER would cross to pass another vehicle is a BROKEN LINE AND it is safe, the PASSER MAY cross it, UNLESS a solid yellow line is on the PASSER's side of the center line."
- **Proposed triage: fix as proposed.** MARK-01 unless: "a SOLID YELLOW LINE is on the PASSER's side of the center line"; statement updated to match. This matches MARK-02 and 6.200.

### S2-028. Ambiguous 'it' in the condition and action

*clarity* · minor · medium confidence

In "AND it is safe, the PASSER MAY cross it", the first "it" is a dummy subject and the second refers to the line. The rule's real point, taken from 6.200 "Broken or dashed lines permit you to pass … if safe", is that passing is allowed. Saying only "cross it" is indirect.

- Fix: Set when to "the line the PASSER would cross to pass another vehicle is a BROKEN LINE AND passing is safe" and action to "cross the BROKEN LINE to pass". Change the vague term entry to "passing is safe".
- **Proposed triage: not an error, no change.** The first "it" is the subject of "it is safe", and "cross it" can only mean the line. The wording was set in a0 G8 from 6.187 ("You may cross a broken line").

## PASS-MARK-02: Do not cross solid yellow line or when unsafe

> WHEN on a two-lane road with two-way traffic AND either the center line on the DRIVER's side is a SOLID YELLOW LINE or crossing it is not safe, the DRIVER MUST NOT cross the center line to pass.

### S2-029. Two-lane, two-way road condition not supported by citations

*unsupported condition* · major · medium confidence

The rule only applies "on a two-lane road with two-way traffic". None of the cited blocks limit the rule this way. 6.187 says only: "Keep to the right of the yellow center line… Do not cross the line if it is not safe or it is a solid yellow line." 6.200 says "A solid yellow line on your side of the road marks a 'no-passing zone.'" 7.17/7.19 forbid driving on the left wherever "Pavement markings or signs prohibit driving on the left". The added condition means the rule would not apply to a solid yellow center line on any other road with one.

- Fix: when: "the center line on the DRIVER's side is a SOLID YELLOW LINE OR crossing the center line is not safe"; statement: "WHEN the center line on the DRIVER's side is a SOLID YELLOW LINE OR crossing the center line is not safe, the DRIVER MUST NOT cross the center line to pass."
- **Proposed triage: rejected, no change.** Same as S2-026: the two-lane, two-way setting comes from heading 6.186, and a0 G1 kept the condition. On roads with two or more lanes each way, LOC-01 and MARK-03 already forbid crossing the center line.

### S2-030. Lowercase 'either…or' instead of grammar keyword OR

*grammar* · minor · high confidence

The condition reads "AND either the center line … is a SOLID YELLOW LINE or crossing it is not safe". The grammar allows only the keywords AND/OR between FACTs. Lowercase "either…or" is not a keyword. The mixed AND/or grouping must be read informally, and "it" refers back loosely.

- Fix: Drop the unsupported road-type fact and write the facts with the keyword OR: "the center line on the DRIVER's side is a SOLID YELLOW LINE OR crossing the center line is not safe". Alternatively, split the rule into two (see the separate finding).
- **Proposed triage: not an error, no change.** Joining alternatives with a lowercase "or" inside one fact is the accepted convention, and a0 G1 rewrote MARK-02 that way.

### S2-031. Two distinct situations merged into one rule

*rule structure* · minor · medium confidence

The rule joins a marking-based prohibition ("SOLID YELLOW LINE", backed by 6.200's "no-passing zone" and 7.19's "Pavement markings or signs prohibit driving on the left") with a general judgement prohibition ("not safe"). These apply in different situations and have different evidence. Merging them blurs which citation supports which part, and prevents giving the marking rule its own force.

- Fix: Split into two rules. (a) "WHEN the center line on the DRIVER's side is a SOLID YELLOW LINE, the DRIVER MUST NOT cross the center line to pass." Evidence: 6.187, 6.200, 6.201, 7.17, 7.19. (b) "WHEN crossing the center line is not safe, the DRIVER MUST NOT cross the center line to pass." Evidence: 6.187, 6.200. Keep "not safe" as a vague term in (b).
- **Proposed triage: not an error, no change.** Both situations come from one sentence of 6.187 ("Do not cross the line if it is not safe or it is a solid yellow line"), with the same strength. a0 G1 set the combined condition.

### S2-032. Force may understate the no-passing-zone marking

*strength* · minor · low confidence

The solid yellow line is described as marking a "no-passing zone" (6.200), and 7.19 says markings "prohibit" driving on the left. Under the instructions, a regulatory marking or prohibition wording points to REQUIREMENT, not INSTRUCTION. The modal MUST NOT is the same either way, so the meaning is unchanged.

- Fix: For the solid-yellow-line part, set force to "REQUIREMENT". Add a note: "6.187 words it as a command ('Do not cross'); 6.200/7.19 describe a no-passing zone that markings prohibit; the stronger wording is recorded."
- **Proposed triage: not an error, no change.** Low confidence. 6.187 is a plain command ("Do not cross"). 6.200 and 7.19 say what the marking means, with no "must", "may not" or penalty, so INSTRUCTION fits. The modal is the same either way.

### S2-033. NO-PASSING ZONE capitalised in note but not defined

*vocabulary* · minor · medium confidence

The note writes "NO-PASSING ZONE" in capitals. No such vocabulary entry is listed for this rule, although 6.200 defines it: "A solid yellow line on your side of the road marks a 'no-passing zone.'"

- Fix: Either write "no-passing zone" in lowercase in the note, or add the vocabulary entry {"term": "NO-PASSING ZONE", "definition": "A stretch of road marked by a solid yellow line on the driver's side, where passing is not allowed.", "evidence": ["6.200"]}.
- **Proposed triage: not an error, no change.** NO-PASSING ZONE is in the vocabulary (6.200, 6.120, 6.50, 7.17, 7.19). The judge was shown only the terms used in the statement, not those in the note.

## PASS-MARK-03: Do not cross double yellow line to pass

> WHEN on a multi-lane HIGHWAY with a DOUBLE YELLOW LINE, the DRIVER MUST NOT cross the DOUBLE YELLOW LINE to pass.

### S2-034. 'multi-lane' condition rests only on the diagram, with no note

*note* · minor · medium confidence

The condition "on a multi-lane HIGHWAY with a DOUBLE YELLOW LINE" is narrower than the cited text. 6.197 says only: "Do not cross the double yellow line to pass." It says nothing about multi-lane roads. The multi-lane context comes only from the figure 6.198, "four-lane highway with a double solid yellow center line and broken white lane lines". The extractor's instructions ask the note to explain a condition that depends on a diagram, but the note is empty. A checker cannot tell why the rule is limited to multi-lane roads.

- Fix: Set note to: "The multi-lane context comes from the accompanying diagram 6.198, which shows a four-lane highway with a double solid yellow centre line and broken white lane lines; the text of 6.197 itself does not mention the number of lanes."
- **Proposed triage: rejected, no change.** Same as S2-012. 6.197 is under the heading 6.196 "Multi-lane Highway (Four or More Lanes)", which sets the multi-lane condition; the diagram only shows it.

## PASS-SIGN-01: No Passing Zone and Do Not Pass signs

> WHEN a 'No Passing Zone' pennant sign or a 'Do Not Pass' sign applies to the DRIVER's direction, the DRIVER MUST NOT pass other vehicles.

### S2-035. Fine and warning-sign claim in note rest on uncited blocks; penalty field left empty

*citation* · major · high confidence

The note says "The pennant is a warning sign; disobeying it is a violation with a fine of $1 to $200 (6.266, 6.267)". Blocks 6.266 and 6.267 are not in `evidence`, and none of the cited blocks mention a fine. Yet `penalty` is "". If the handbook does state a penalty for this rule, it belongs in `penalty` with its blocks cited. As things stand, the penalty claim is not supported by the rule's citations, and the two fields contradict each other.

- Fix: If 6.266/6.267 do state this fine for disobeying these signs, set penalty to "Fine of $1 to $200" and add "6.266" and "6.267" to evidence. Otherwise remove the fine sentence from the note.
- **Proposed triage: rejected, no change.** Settled in a0 M4. SIGN-01's penalty stays empty because its "Do Not Pass" sign has no stated penalty, and the note says the pennant carries the 6.267 fine. Something mentioned only in a note needs no citation.

### S2-036. Pennant marks the start of a zone ahead, but the rule bans passing wherever the sign 'applies'

*accuracy* · minor · medium confidence

6.50 says the pennant gives "Advance warning of no pass zones". The ban applies in the no-passing zone that follows the sign, not at the sign itself. The phrase "a 'No Passing Zone' pennant sign … applies to the DRIVER's direction" does not say where the ban starts or ends, so a driving model cannot tell when it is in force. The words "applies to the DRIVER's direction" are also not found in any cited block.

- Fix: when: "the DRIVER is within a no-passing zone marked by a 'No Passing Zone' pennant sign or a 'Do Not Pass' sign". Add a note that per 6.50 the pennant gives advance warning of the zone.
- **Proposed triage: fix, using the NO-PASSING ZONE term.** when: "in a NO-PASSING ZONE marked for the DRIVER's direction by a 'No Passing Zone' pennant sign or a 'Do Not Pass' sign"; statement updated to match. The vocabulary entry already says that such a zone is marked by these signs, and the note already says that the pennant gives advance warning.

### S2-037. 7.17/7.19 prohibit driving on the left, which is broader than 'pass other vehicles'

*scope* · minor · medium confidence

7.17 says "Never drive on the left side of the road when:" and 7.19 continues "…signs prohibit driving on the left (a “No Passing Zone”…)". This bans any driving on the left side, not just passing. The rule uses these blocks as support but narrows the action to "pass other vehicles". The note does not mention the difference.

- Fix: Add to the note: "7.17/7.19 word this more broadly: never drive on the left side of the road in a No Passing Zone." Alternatively, make it a separate rule with action "drive on the left side of the road".
- **Proposed triage: fix as proposed.** Add to SIGN-01's note: "7.17 and 7.19 word the ban more broadly: never drive on the left side of the road in a No Passing Zone."

## PASS-SIGN-02: Curve and winding road signs: do not pass

> WHEN passing a warning sign for a reverse curve, sharp turn, gradual curve, reverse sharp turn, sharp curve chevron, or winding road, the DRIVER MUST NOT pass other vehicles in the curve or winding section ahead.

### S2-038. Condition uses "passing" for driving by a sign, next to the overtaking sense of "pass"

*clarity* · minor · medium confidence

In this rule set, "pass" means overtaking another vehicle, and the action here uses it that way: "pass other vehicles". The condition, "WHEN passing a warning sign for a reverse curve…", uses the same word to mean driving by a sign. A reader or a model could take the condition to mean overtaking. It could also read the rule as applying only at the moment the vehicle goes by the sign, rather than to the road section the sign warns of. The handbook frames these signs as describing the road ahead, e.g. 6.73: "Road ahead makes a sharp turn… do not pass" and 6.74: "There is a winding road ahead… do not pass."

- Fix: when: "the DRIVER has driven by a warning sign for a reverse curve, sharp turn, gradual curve, reverse sharp turn, sharp curve chevron, or winding road AND is approaching or within the curve or winding road the sign warns of"; action: "pass other vehicles in that curve or winding road". Rewrite the statement to match.
- **Proposed triage: rejected, no change.** This is a0 G4 again, which was rejected: a lowercase phrase that means driving past a fixed object, not overtaking, is not an error.

### S2-039. Extent of the no-passing zone is vague but not listed

*vague terms* · minor · high confidence

The action "pass other vehicles in the curve or winding section ahead" leaves open where the prohibition starts and ends. The signs give no distance or end point: 6.68 says only "The road curves one way… and then the other way… do not pass." Yet `vague_terms` is empty.

- Fix: Add to vague_terms: {"term": "the curve or winding section ahead", "explanation": "no start, end or length of the section given"}.
- **Proposed triage: fix as proposed.** Add `{"term": "the curve or winding section ahead", "explanation": "no start, end or length of the section given"}`.

## PASS-SIGN-03: Two-arrow sign: pass on either side

> WHEN a sign shows two arrows pointing down to the left and right at a traffic island or obstruction, the DRIVER MAY pass on either side of it.

### S2-040. Rule is about going around an obstruction, not overtaking

*scope* · major · medium confidence

The topic is "overtaking (passing another vehicle, and being passed)". Block 6.98 says the sign "Indicates traffic is permitted to pass on either side of a traffic island or an obstruction." Here "pass" means going around a fixed island or obstruction, not moving past another vehicle. Putting this sign in the overtaking rule set, with the action "pass on either side of it", could lead a driving model to read it as permission to overtake on either side, for example on the right. That would be a misleading ground-truth entry.

- Fix: Remove PASS-SIGN-03 from the overtaking rule set; it belongs with signs and lane use. If it is kept, reword the action to make clear it is not overtaking: "keep to either the left or the right side of the traffic island or obstruction", and add a note: "'Pass' here means going around a fixed island or obstruction, not overtaking another vehicle."
- **Proposed triage: rejected, no change.** a0 M6.3 put passing a fixed hazard in scope and added this rule. With S2-041's fix, the action names the traffic island or obstruction, so it cannot be read as passing a vehicle.

### S2-041. Ambiguous pronoun "it" in the action

*clarity* · minor · medium confidence

In "the DRIVER MAY pass on either side of it", "it" could refer to the sign or to the traffic island or obstruction. The rule is meant to stand on its own.

- Fix: Set action to "pass on either side of the traffic island or obstruction", and update the statement to match.
- **Proposed triage: fix as proposed.** action: "pass on either side of the traffic island or obstruction"; statement updated to match.

### S2-042. Actor narrowed from 'traffic' to motor-vehicle DRIVER

*actor* · minor · low confidence

Block 6.98 says "traffic is permitted to pass", but the vocabulary defines DRIVER as "A person driving a motor vehicle". This narrows who the permission applies to. The effect is small for a driving model.

- Fix: Keep DRIVER, but add to the note: "The handbook says 'traffic', which also covers other road users."
- **Proposed triage: not an error, no change.** Low confidence. The rule set is written for drivers, and DRIVER is the road user the sign's permission is about here.

## PASS-SIGN-04: Barricade stripes: bear to the side they slope down

> WHEN a barricade or vertical panel has diagonal stripes sloping downward to one side, the DRIVER SHOULD bear to the side to which the stripes slope downward.

### S2-043. Barricade-stripe rule is outside the overtaking topic

*scope* · major · high confidence

The task limits extraction to "overtaking (passing another vehicle, and being passed) only". This rule tells a driver which way to steer around a construction barricade or vertical panel. It does not concern overtaking or being overtaken. The word "pass" in 6.243 ("…guide the driver towards the direction to where the traffic is to pass") means traffic going around the obstruction, not one vehicle overtaking another. Blocks 6.245 and 6.248 only say which way to "bear" based on the stripe direction. Filed under topic PASS, this rule would put a work-zone guidance rule into the overtaking ground truth.

- Fix: Remove PASS-SIGN-04 from the overtaking rule set. If it is kept anywhere, place it under a construction-zone or traffic-control-device topic, not PASS.
- **Proposed triage: rejected, no change.** a0 M6.4 added this rule because its blocks sit under the heading 6.242 "Passing Traffic". As in S2-012, the judge was shown only the chapter section, so it did not see that heading.

## PASS-SIDE-02: Passing on a paved shoulder

> WHEN conditions permit doing so safely AND the vehicle being passed is slowing or stopped on the main traveled portion of the HIGHWAY, disabled, or preparing to make a left turn, the PASSER MAY ONLY pass on a paved shoulder.

### S2-044. MAY ONLY reads as 'pass only on the shoulder' and claims an exclusivity the cited blocks do not state

*strength* · major · high confidence

The statement "…the PASSER MAY ONLY pass on a paved shoulder" most naturally reads as 'in these situations, passing is allowed only on the shoulder'. That would forbid an ordinary pass in the left lane, which the handbook never says. The note itself admits the rule "does not require using the shoulder", so the wording contradicts its intended meaning. Under the intended reading (shoulder passing is allowed in these cases and in no others), the restriction to the three listed situations is not supported by the cited blocks. 7.45 says only "You may pass on a paved shoulder when…", which is PERMISSION wording. The "only" in 7.42 ("you can pass on the right only when conditions permit you to do so safely") governs the safety condition, not the list of situations. A driving model could misread this rule as a mandate to use the shoulder.

- Fix: Set modal to "MAY" and the statement to: "WHEN passing on the right AND conditions permit doing so safely AND the vehicle being passed is slowing or stopped on the main traveled portion of the HIGHWAY, is disabled, OR is preparing to make a left turn, the PASSER MAY pass on a paved shoulder." Change the note to: "7.42 permits passing on the right only when it is safe; 7.45 lists the paved-shoulder case as a permission." If an exclusive reading is wanted, cite the list's introductory block and rephrase the rule so that the exclusivity attaches to the conditions, not to the shoulder.
- **Proposed triage: rejected, no change.** a0 G3 chose MAY ONLY because the handbook states the "only" (7.42). The note gives the reading: the shoulder is one of the listed cases, and the rule does not require using it.

### S2-045. Lowercase 'or' mixed with AND makes the condition's grouping ambiguous

*grammar* · minor · medium confidence

The condition "conditions permit doing so safely AND the vehicle being passed is slowing or stopped on the main traveled portion of the HIGHWAY, disabled, or preparing to make a left turn" joins its alternatives with lowercase "or" and commas instead of the grammar's OR keyword. It is therefore unclear whether "disabled" and "preparing to make a left turn" sit under the safety conjunct, or whether "on the main traveled portion" applies to all three cases. The rule also leaves implicit that a shoulder pass is a pass on the right, which is what 7.42 governs.

- Fix: Write the alternatives as explicit FACTs, for example: "conditions permit doing so safely AND (the vehicle being passed is slowing or stopped on the main traveled portion of the HIGHWAY OR the vehicle being passed is disabled OR the vehicle being passed is preparing to make a left turn)".
- **Proposed triage: not an error, no change.** Joining alternatives with a lowercase "or" inside one fact is the accepted convention (a0 G1). "On the main traveled portion of the HIGHWAY" belongs to "slowing or stopped", as in 7.45.

## PASS-USER-01: Stop for a school bus with flashing red lights

> WHEN approaching a school bus from either direction AND the bus is displaying alternately flashing red lights, the DRIVER MUST stop, UNLESS the school bus is on a different road OR the DRIVER is on a CONTROLLED-ACCESS HIGHWAY where the bus is stopped in a loading zone and pedestrians are not permitted to cross.

### S2-046. Penalty merges the two serious-injury offences

*penalty* · minor · medium confidence

The penalty reads "causing serious bodily injury is a Class A misdemeanor or state jail felony". This makes the choice between the two look open. The table ties each to a different condition. 5.83: "Person causes serious bodily injury to another when passing a stopped school bus | Class A misdemeanor…". 5.84: "Person causes serious bodily injury… and has previously been convicted of passing a school bus and causing serious bodily injury | State jail felony…". The felony applies only to a repeat injury offence.

- Fix: penalty: "1st conviction $500-$1,250; 2nd and later within 5 years $1,000-$2,000 and possible suspension up to six months; causing serious bodily injury is a Class A misdemeanor (state jail felony if previously convicted of the same); subsequent conviction for passing a school bus causes automatic suspension."
- **Proposed triage: fix.** USER-01 penalty: "1st conviction $500-$1,250; 2nd within 5 years $1,000-$2,000 and possible suspension up to six months; causing serious bodily injury is a Class A misdemeanor, or a state jail felony after a previous conviction for the same; subsequent conviction causes automatic suspension." Only the serious-injury part changes (5.83, 5.84).

## PASS-USER-02: Do not pass a stopped school bus until allowed

> WHEN the DRIVER has stopped for a school bus displaying alternately flashing red lights, the DRIVER MUST NOT pass the school bus, UNLESS the school bus has resumed motion OR the DRIVER of the school bus signals the DRIVER to proceed OR the red lights are no longer flashing.

### S2-047. Penalty summary misstates when the state jail felony applies

*penalty* · minor · high confidence

The penalty says "causing serious bodily injury is a Class A misdemeanor or state jail felony", which reads as if either can apply to any first injury. The table separates them. 5.83: "Person causes serious bodily injury to another when passing a stopped school bus … Class A misdemeanor". 5.84: "…and has previously been convicted of passing a school bus and causing serious bodily injury … State jail felony". The felony applies only to a repeat injury offender.

- Fix: penalty: "1st conviction: fine $500-$1,250; 2nd and later conviction within 5 years: fine $1,000-$2,000 and possible suspension up to six months; causing serious bodily injury: Class A misdemeanor; causing serious bodily injury after a prior such conviction: state jail felony; subsequent conviction for passing a school bus: automatic licence suspension."
- **Proposed triage: fix.** Same as S2-046. USER-02 gets the same penalty text as USER-01.

### S2-048. DRIVER term reused for the school bus driver

*vocabulary* · minor · medium confidence

The exception says "the DRIVER of the school bus signals the DRIVER to proceed". The same capitalised term names both the actor and the bus driver, so the clause is easy to misread. The handbook (5.76) says only "You are signaled by the driver to proceed".

- Fix: unless: "the school bus has resumed motion OR the school bus driver signals the DRIVER to proceed OR the red lights are no longer flashing". Update the statement to match.
- **Proposed triage: rejected, no change.** The wording was set in the a1 triage (PASS-USER-02). "The school bus driver" would bring back the lowercase "driver" that check 8 flags.

### S2-049. Note refers to another rule by an incomplete id

*note* · minor · medium confidence

The note says "5.78's exceptions are in USER-01". This is not a full rule id (PASS-USER-01). It also leans on another rule instead of stating the limit plainly. The exceptions in 5.78 ("not necessary to stop when passing a school bus on a different road or when on a controlled-access highway where the bus is stopped in a loading zone…") could be stated directly.

- Fix: note: "5.78 says a driver need not stop for a school bus on a different road, or on a controlled-access highway where the bus is stopped in a loading zone and pedestrians may not cross; such a driver is outside this rule's condition (see PASS-USER-01). 5.78 refers to the penalties as Table 17, but the table caption (5.79) is Table 15."
- **Proposed triage: fix, full id only.** USER-02 note: "5.78's exceptions are in PASS-USER-01: a DRIVER who need not stop is not in this rule's condition." The rest of the note was set in a0 G6, and the Table 17 remark is in USER-01's note.

## PASS-USER-04: Checks before passing a truck

> WHEN about to pass a TRUCK, the PASSER MUST NOT move into the passing lane before checking front and rear, mirrors and BLIND SPOTS, and confirming the lane is clear and the road is a legal passing zone.

### S2-050. Vague phrase 'the lane is clear' not listed

*vague_terms* · minor · high confidence

The action requires "confirming the lane is clear", which follows 10.112: "…move into the passing lane only if it is clear…". The handbook gives no gap, distance or sight-line criterion for 'clear'. The instructions' own example lists "the way is clear" as a vague term, yet `vague_terms` here is empty.

- Fix: Add to vague_terms: {"term": "the lane is clear", "explanation": "no gap or sight distance given"}.
- **Proposed triage: fix as proposed.** Add `{"term": "the lane is clear", "explanation": "no gap or sight distance given"}`, as in GEN-02.

### S2-051. Negated sequence makes the scope of MUST NOT ambiguous

*clarity* · minor · low confidence

The statement "MUST NOT move into the passing lane before checking front and rear, mirrors and BLIND SPOTS, and confirming the lane is clear and the road is a legal passing zone" can be parsed two ways. It may mean the conditions are prerequisites, or it may read as a list of separate actions under MUST NOT. The handbook's wording in 10.112 is a positive instruction: "first check… then move into the passing lane only if it is clear and you are in a legal passing zone". The sentence also blurs the order of the steps (the checks first, then the move) with the condition on the move (only if the lane is clear and the zone is legal).

- Fix: Rewrite positively: modal "MUST", action "check front and rear, mirrors and BLIND SPOTS before moving into the passing lane, and move into the passing lane only if it is clear and the road is a legal passing zone". Statement: "WHEN about to pass a TRUCK, the PASSER MUST check front and rear, mirrors and BLIND SPOTS before moving into the passing lane, and move into the passing lane only if it is clear and the road is a legal passing zone."
- **Proposed triage: not an error, no change.** Low confidence. "Before" governs both the checks and the confirming, so the rule reads as one prohibition: do not move into the passing lane until they are done.

## PASS-USER-05: Flash headlights when passing a truck

> WHEN passing a TRUCK, the PASSER MUST let the DRIVER of the TRUCK know of the PASS by flashing the headlights.

### S2-052. "especially at night" is left out of the statement

*completeness* · minor · medium confidence

The handbook says 10.112: "Let the truck driver know you are passing by flashing your headlights, especially at night." The rule's statement drops "especially at night" and mentions it only in the note. A driving model that reads only the statement loses the handbook's stress that the signal matters most after dark. The instructions say to keep the handbook's own words in the rule. The phrase does not change who must act or when, so the rule's meaning is intact.

- Fix: Set action to "let the DRIVER of the TRUCK know of the PASS by flashing the headlights, especially at night". Update statement to match: "WHEN passing a TRUCK, the PASSER MUST let the DRIVER of the TRUCK know of the PASS by flashing the headlights, especially at night." Change the note to: "The handbook stresses the signal at night but words it as applying to every pass of a truck."
- **Proposed triage: rejected, no change.** a0 G5 moved "especially at night" from the condition to the note, because it sets an emphasis, not a condition.

## PASS-USER-06: Complete the pass quickly

> WHEN passing a TRUCK or other vehicle, the PASSER MUST complete the PASS as quickly as possible and not stay alongside the other vehicle.

### S2-053. Rule widened from trucks to every vehicle

*scope* · major · medium confidence

The rule's condition is "passing a TRUCK or other vehicle", so it applies to every pass. The cited block sits under the heading "Share the Road with Trucks" and is entirely about passing a truck: 10.113: "…it takes three to five seconds longer to pass a truck than a car… Complete your pass as quickly as possible and don't stay alongside the other vehicle." Here "the other vehicle" means the vehicle being passed, which is the truck. It is not a separate class of vehicles. The cited blocks give no general instruction covering passes of any vehicle.

- Fix: Set when to "passing a TRUCK" and statement to "WHEN passing a TRUCK, the PASSER MUST complete the PASS as quickly as possible and not stay alongside the TRUCK." Change action to "complete the PASS as quickly as possible and not stay alongside the TRUCK".
- **Proposed triage: fix as proposed, with a note on the wording.** when: "passing a TRUCK"; action: "complete the PASS as quickly as possible and not stay alongside the TRUCK"; statement updated to match. Add to the note: "The handbook's 'the other vehicle' is the truck being passed." For passing any vehicle, GEN-06 already says not to linger beside it.

### S2-054. Prohibition folded into a MUST action

*grammar* · minor · low confidence

The action "complete the PASS as quickly as possible and not stay alongside the other vehicle" puts a prohibition ("don't stay alongside") inside a MUST action. The handbook words it as a separate negative command. The grammar has a MUST NOT modal for this, and writing it inside MUST makes the rule harder to parse and check.

- Fix: Either keep a single positive obligation, "complete the PASS as quickly as possible without remaining alongside the TRUCK", or split it into two rules. Rule 1: "WHEN passing a TRUCK, the PASSER MUST complete the PASS as quickly as possible." Rule 2: "WHEN passing a TRUCK, the PASSER MUST NOT stay alongside the TRUCK."
- **Proposed triage: not an error, no change.** Positive phrase first and negated phrase last is the accepted pattern (a0 M1).

## PASS-USER-07: Return in front of a truck only when its front is visible

> WHEN returning in front of a TRUCK after passing it, the PASSER MUST NOT move back into the lane, UNLESS the entire front of the TRUCK can be seen in the rearview mirror.

### S2-055. Condition and action are circular and the target lane is unnamed

*clarity* · minor · medium confidence

The rule reads "WHEN returning in front of a TRUCK after passing it, the PASSER MUST NOT move back into the lane". The condition already assumes the PASSER is returning, so the action restates it. "the lane" also never says which lane is meant. The handbook's point is when the move back is allowed. 10.114: "Be sure to move back only when you can see the entire front of the truck in your rearview mirror."

- Fix: when: "having passed a TRUCK"; action: "move back into the lane in front of the TRUCK"; statement: "WHEN having passed a TRUCK, the PASSER MUST NOT move back into the lane in front of the TRUCK, UNLESS the entire front of the TRUCK can be seen in the rearview mirror."
- **Proposed triage: fix, with "passing a TRUCK" as the condition.** when: "passing a TRUCK"; action: "move back into the lane in front of the TRUCK"; statement: "WHEN passing a TRUCK, the PASSER MUST NOT move back into the lane in front of the TRUCK, UNLESS the entire front of the TRUCK can be seen in the rearview mirror." "Having passed a TRUCK" is USER-08's condition, for after the pass. The MUST NOT … UNLESS form stays.

### S2-056. Note could be read as letting the truck's flash replace the mirror check

*note* · minor · low confidence

The note says the truck driver flashing the lights "signals that it is clear to pull back in". It does not say that the mirror condition still applies. A reader could take the flash as an alternative way to meet the rule. 10.114 gives the flash as information only, then follows it with the plain command "Be sure to move back only when you can see the entire front…".

- Fix: Note: "The same block says that if the truck driver flashes the truck's lights after the pass, it signals that it is clear to pull back in; this does not replace the requirement to see the entire front of the TRUCK in the rearview mirror. The block also says to maintain speed after passing a truck, which is a separate rule."
- **Proposed triage: fix, shorter note.** USER-07 note: "The truck driver flashing the truck's lights after the pass signals that it is clear to pull back in; this does not replace seeing the entire front of the truck in the rearview mirror." The maintain-speed sentence is its own rule, PASS-USER-08.

## PASS-USER-08: Maintain speed after passing a truck

> WHEN having passed a TRUCK, the PASSER MUST maintain speed.

### S2-057. Open-ended duration of 'maintain speed' not flagged as vague

*vague terms* · minor · medium confidence

The handbook says only 10.114: "After you pass a truck, maintain your speed." It gives no duration or distance for keeping that speed. The rule's condition "having passed a TRUCK" carries the same gap: it does not say how long after the pass the duty lasts. Yet `vague_terms` is empty, so a driving model is not told that this is left to the driver's judgement.

- Fix: Set vague_terms to [{"term": "having passed a TRUCK", "explanation": "does not say how long after the pass speed must be maintained"}].
- **Proposed triage: fix as proposed.** Add `{"term": "having passed a TRUCK", "explanation": "does not say how long after the pass speed must be maintained"}`.

### S2-058. 'maintain speed' drops 'your', leaving unclear whose speed is kept

*clarity* · minor · low confidence

The handbook says "maintain your speed", meaning the passing driver keeps their own speed, i.e. does not slow down after moving back in front of the truck. The rule's "maintain speed" does not say whose speed. It could be misread as matching the truck's speed or keeping some posted speed.

- Fix: Set action to "maintain the PASSER's speed" and statement to "WHEN having passed a TRUCK, the PASSER MUST maintain the PASSER's speed."
- **Proposed triage: not an error, no change.** Low confidence. With the PASSER as actor, "maintain speed" means the PASSER's own speed. 10.114 says only "maintain your speed".

## PASS-USER-09: Never cut in front of a truck

> WHEN trying to reach an exit or turn, or a single-lane construction zone, ahead of a TRUCK or bus, the DRIVER MUST slow down and exit or stay behind the TRUCK or bus, and not cut into the open space in front of it.

### S2-059. "Exit or turn" condition is not supported by the cited block

*faithfulness* · major · high confidence

The rule's `when` begins "trying to reach an exit or turn … ahead of a TRUCK or bus". The cited block names only one such situation: 10.129: "Trying to beat a truck to a single-lane construction zone represents a particularly dangerous situation." The word "exit" appears only in the remedy ("Either slow down and exit or stay behind the truck"). It is not a situation the driver is racing toward. "Turn" does not appear at all.

- Fix: Remove "an exit or turn" from the condition. If another handbook block states it, cite that block. Otherwise use: when = "trying to reach a single-lane construction zone ahead of a TRUCK"; action = "slow down and exit or stay behind the TRUCK".
- **Proposed triage: rejected, no change.** Same as S2-012. "An exit or turn" comes from the heading 10.128 "Cutting Off a Vehicle to Reach Your Exit or Turn", which 10.129 sits under; the judge was shown only "Share the Road with Trucks". a0 M1 set the condition.

### S2-060. General ban on cutting in front of a truck is limited to special situations

*scope* · major · high confidence

10.129 opens with an unconditional command: "Never cut in front of a truck." The rule attaches this ban ("not cut into the open space in front of it") only to drivers who are trying to reach an exit, a turn or a construction zone. A driving model reading the rule would conclude that cutting in front of a truck is acceptable in all other situations.

- Fix: Split the rule in two, both citing 10.129. (a) PASS-USER-09: force INSTRUCTION, modal MUST NOT, actor DRIVER, when = "returning to a lane ahead of a TRUCK", action = "cut into the open space in front of the TRUCK", statement "WHEN returning to a lane ahead of a TRUCK, the DRIVER MUST NOT cut into the open space in front of the TRUCK." (b) A new rule: force INSTRUCTION, modal MUST, actor DRIVER, when = "trying to reach a single-lane construction zone ahead of a TRUCK", action = "slow down and exit or stay behind the TRUCK", statement "WHEN trying to reach a single-lane construction zone ahead of a TRUCK, the DRIVER MUST slow down and exit or stay behind the TRUCK."
- **Proposed triage: rejected, no change.** Under the heading 10.128, "Never cut in front of a truck" is about cutting in to reach an exit or turn, and a0 M1 chose this situation as the condition. Cutting back in after passing a truck is PASS-USER-07.

### S2-061. MUST and a prohibition are mixed in one action

*grammar* · minor · medium confidence

The action "slow down and exit or stay behind …, and not cut into the open space in front of it" puts a negative obligation inside a MUST rule. The grammar provides MUST NOT for prohibitions, and this phrasing blurs the modal.

- Fix: Express the prohibition as a separate MUST NOT rule, as in the split above.
- **Proposed triage: not an error, no change.** USER-09 was reworded to this pattern in a0 M1.

### S2-062. Bus is added to the instruction, which names only trucks

*faithfulness* · minor · medium confidence

The commands in 10.129 name only the truck: "Never cut in front of a truck … Either slow down and exit or stay behind the truck." The bus appears only in the explanatory sentence: "Cutting into the open space in front of a truck or bus removes the driver's cushion of safety." The rule applies the full remedy to "a TRUCK or bus" without saying in the note that the bus is inferred from that reason sentence.

- Fix: Limit the instruction to TRUCK. Alternatively, keep "or bus" only in the prohibition and add to the note: "Bus is included from the reason sentence in 10.129."
- **Proposed triage: not an error, no change.** 10.129 names the bus in the sentence that gives the danger ("in front of a truck or bus"), and its heading 10.128 is about cutting off any vehicle. The wording was approved in a0 M1.

## PASS-USER-11: Wait for a backing truck

> WHEN a TRUCK is preparing to back or is backing from the road into a loading area, the DRIVER MUST wait for the TRUCK to complete its maneuver before trying to pass, and never cross behind it.

### S2-063. General no-crossing-behind prohibition narrowed to loading-area backing

*scope/conditions* · major · high confidence

In the handbook, 10.125: "Never cross behind a truck preparing to back up." applies to any truck preparing to back up. Only the next sentences limit the waiting instruction to the loading-area case: "When a truck driver is preparing to back the truck from a road into a loading area… Wait for the truck to complete its maneuver before trying to pass." The rule puts "never cross behind it" under the WHEN condition "backing from the road into a loading area". A driving model would read it as allowing a crossing behind a truck that is backing anywhere else.

- Fix: Split into two rules. (1) PASS-USER-11 "Wait for a truck backing into a loading area": force INSTRUCTION, modal MUST, actor DRIVER, when "a TRUCK is preparing to back or is backing from the road into a loading area", action "wait for the TRUCK to complete its maneuver before trying to pass", statement "WHEN a TRUCK is preparing to back or is backing from the road into a loading area, the DRIVER MUST wait for the TRUCK to complete its maneuver before trying to pass.", evidence ["10.125"]. (2) A new rule "Never cross behind a backing truck": force INSTRUCTION, modal MUST NOT, actor DRIVER, when "a TRUCK is preparing to back up", action "cross behind the TRUCK", statement "WHEN a TRUCK is preparing to back up, the DRIVER MUST NOT cross behind the TRUCK.", evidence ["10.125"].
- **Proposed triage: fix as proposed, by splitting the rule.** The never-cross-behind sentence covers any truck preparing to back up, and the waiting sentence covers the loading-area case.
  - USER-11: title "Wait for a truck backing into a loading area"; action "wait for the TRUCK to complete its maneuver before trying to pass"; statement updated to match.
  - New rule **PASS-USER-17** "Never cross behind a backing truck", at the end of the USER group: INSTRUCTION, MUST NOT, actor DRIVER; when "a TRUCK is preparing to back up"; action "cross behind the TRUCK"; evidence ["10.125"]. Statement: "WHEN a TRUCK is preparing to back up, the DRIVER MUST NOT cross behind the TRUCK."

### S2-064. Prohibition embedded in a MUST action

*grammar* · minor · high confidence

The action "…before trying to pass, and never cross behind it" puts a prohibition inside a MUST rule, so the statement reads "MUST … never cross". The grammar allows one modal per rule, and a prohibition belongs under MUST NOT as its own entry. The instructions also ask for one rule per entry.

- Fix: Remove ", and never cross behind it" from the action and statement. State the prohibition as its own MUST NOT rule, as in the split above.
- **Proposed triage: fix, by the split in S2-063.** The prohibition is now PASS-USER-17, so USER-11's action no longer has one.

### S2-065. Handbook's reason not recorded in note

*note* · minor · medium confidence

The handbook gives a reason for the rule, 10.125: "If you pass too closely behind the truck, a crash may occur because you are in the truck's blind spot." The instructions say to record reasons the handbook gives in `note`, but the rule's note is empty.

- Fix: Set note to: "Reason given: passing too closely behind a backing truck puts you in the truck's blind spot and may cause a crash; the road is temporarily blocked while the truck backs."
- **Proposed triage: fix, with the reason split between the two rules.** USER-11 note: "Reason given: the road is temporarily blocked while the truck backs." PASS-USER-17 note: "Reason given: a driver who passes too closely behind the truck is in the truck's blind spot, and a crash may occur."

## PASS-USER-12: Care when passing a distracted driver

> WHEN passing the vehicle of a DRIVER who seems to be distracted, the PASSER SHOULD be very careful.

### S2-066. Vague-term explanation points to blocks the rule does not cite

*citation* · minor · low confidence

The `vague_terms` explanation for "seems to be distracted" reads "cues listed in 10.207-10.210 but judgement left to driver". Those blocks are not in the rule's evidence, which is only ["10.212"]. The only cited block, 10.212, says "Be very careful when passing a driver who seems to be distracted…" and lists no cues. A checker reading the rule and its citations cannot verify the reference. If those blocks do list cues the model can recognize, they are relevant to the rule's condition and could be cited.

- Fix: Either add the cue blocks (10.207–10.210) to `evidence` if they describe the signs of a distracted driver, or rewrite the explanation without the uncited reference: {"term": "seems to be distracted", "explanation": "no observable signs of distraction given"}.
- **Proposed triage: not an error, no change.** Low confidence. The explanation only says where the cues are listed. Something mentioned only in a note or an explanation needs no citation.

## PASS-USER-13: Do not share a lane with a motorcycle

> WHEN near a MOTORCYCLE in a traffic lane, the DRIVER MUST allow the MOTORCYCLE a full lane width, and not attempt to share the lane with it.

### S2-067. Condition "near a MOTORCYCLE" is not in the handbook

*faithfulness* · minor · medium confidence

The handbook block 10.160 gives the command without any proximity condition: "Allow the motorcyclist a full lane width… Do not attempt to share the lane with a motorcycle." The rule adds "near a MOTORCYCLE" and then lists it as vague ("does not say how near"). This creates an ambiguity the handbook does not contain. The handbook's situation is simply a motorcycle occupying a traffic lane.

- Fix: when: "a MOTORCYCLE is in a traffic lane"; statement: "WHEN a MOTORCYCLE is in a traffic lane, the DRIVER MUST allow the MOTORCYCLE a full lane width, and not attempt to share the lane with it." Remove the vague_terms entry for "near a MOTORCYCLE".
- **Proposed triage: rejected, no change.** a0 kept this condition and added "near a MOTORCYCLE" to USER-13's vague terms (Vague terms not listed). Without "near", the condition would hold for any motorcycle anywhere on the road.

### S2-068. Prohibition is hidden inside a MUST action

*grammar* · minor · low confidence

The action "allow the MOTORCYCLE a full lane width, and not attempt to share the lane with it" puts a prohibition ("Do not attempt to share the lane…") under the modal MUST. The grammar provides MUST NOT for prohibitions. A checker parsing the modal sees only an obligation, so the explicit negative command is not captured as a MUST NOT.

- Fix: Phrase the action positively and record the prohibition in the note, or split the rule into two. Rule A: "WHEN a MOTORCYCLE is in a traffic lane, the DRIVER MUST allow the MOTORCYCLE a full lane width." Rule B: "WHEN a MOTORCYCLE is in a traffic lane, the DRIVER MUST NOT attempt to share the lane with the MOTORCYCLE." Both cite 10.160.
- **Proposed triage: not an error, no change.** USER-13 was reworded to this pattern in a0 M1.

## PASS-USER-14: Cyclist may leave the right edge to overtake

> WHEN overtaking and passing another vehicle proceeding in the same direction, the CYCLIST MAY ride away from the right curb or edge of the road and take the full lane.

### S2-069. Rule omits the setting in which the keep-right duty applies

*completeness* · minor · low confidence

The handbook states this as an exception to a duty that applies only in certain cases. 14.15 says: "A person operating a bicycle who is moving slower than the other traffic on the road shall ride as near as possible to the right curb…unless: … The person is overtaking and passing…". 10.180 says bicyclists must keep right "only when the lane can be shared safely by a car and a bicycle, side-by-side." The rule's `when` ("overtaking and passing another vehicle proceeding in the same direction") drops this setting, and the note mentions only the slower-cyclist condition. The permission stays true without the setting, so the rule's meaning does not change. Still, a reader cannot see what duty is being lifted, or that 10.180 frames it as a condition that "allow[s] a bicyclist to take the full lane."

- Fix: Expand the note to: "Exception to the rule that a CYCLIST moving slower than other traffic must ride as near as possible to the right curb or edge (14.15), a duty that 10.180 says applies only when the lane can be shared safely side-by-side; both passages list overtaking and passing a vehicle going the same direction as a condition allowing the cyclist to take the full lane."
- **Proposed triage: not an error, no change.** Low confidence. The note already names the duty being lifted (a slower cyclist rides near the right edge), and the permission holds whatever the lane width.

## PASS-USER-15: Move over or slow down for a stopped service vehicle

> WHEN the road has two or more lanes in the DRIVER's direction AND the DRIVER is approaching a SERVICE VEHICLE stopped on the road with its lights on or flashing, the DRIVER MUST move out of the lane closest to the SERVICE VEHICLE, or reduce speed to 20 mph below the speed limit or, where the posted speed limit is less than 25 mph, to less than 5 mph, UNLESS a law enforcement officer directs otherwise.

### S2-070. Slow-down duty wrongly limited to multi-lane roads

*condition* · major · high confidence

The rule puts "the road has two or more lanes in the DRIVER's direction" in WHEN, so it says nothing about two-lane or single-lane roads. In the handbook, the lane count only governs the move-over option. The slow-down duty applies on any road. 9.30: "To reduce his/her speed to 20 mph below the speed limit; or" (no lane condition). 9.31: "Move out of the lane … if the road has multiple lanes traveling in the same direction." 5.69 likewise ties only vacating the lane to "if the highway has two or more lanes". As written, a driver on a single-lane road passing a stopped SERVICE VEHICLE gets no instruction to slow down.

- Fix: Move the lane condition into the action. when: "the DRIVER is approaching a SERVICE VEHICLE stopped on the road with its lights on or flashing". action: "reduce speed to 20 mph below the posted speed limit (or, where the posted speed limit is less than 25 mph, to less than 5 mph), or, where the road has two or more lanes in the DRIVER's direction, move out of the lane closest to the SERVICE VEHICLE". Alternatively, split this into two rules: one for slowing down on any road, and one giving the move-over option on multi-lane roads.
- **Proposed triage: rejected, no change.** a0 M6.1 split the duty by the number of lanes. With one lane in the DRIVER's direction, PASS-USER-16 applies, and it requires slowing down. The judge sees only one rule at a time.

### S2-071. Officer exception extended beyond its source

*scope* · minor · medium confidence

The UNLESS clause "a law enforcement officer directs otherwise" comes only from 5.68, which covers "a stopped emergency vehicle". 9.29 lists tow trucks, utility and TxDOT vehicles but states no such exception. The rule applies the exception to every SERVICE VEHICLE. The note says where the exception comes from but does not say it is being extended to the other vehicles.

- Fix: Add to the note: "The officer-direction exception is stated only for emergency vehicles (5.68) and is extended here to all SERVICE VEHICLES by inference."
- **Proposed triage: fix, note only.** Add to USER-15's note, after the 5.71 sentence: "Both are applied here to every SERVICE VEHICLE." The note already says that the officer exception and the under-25-mph case come from the emergency-vehicle passage (a0 M6.1).

### S2-072. SERVICE VEHICLE vocabulary lacks its handbook evidence

*vocabulary* · minor · medium confidence

The SERVICE VEHICLE definition copies the list in 9.29 ("emergency medical vehicle, law enforcement vehicle, fire truck, tow truck, utility service vehicle, Texas Department of Transportation vehicle…"), but its evidence is empty. The instructions require citing the handbook block a term's definition comes from. Separately, the move-over list in 9.31 leaves out utility service vehicles, so the rule's move-over option for them rests only on the slow-down list in 9.29.

- Fix: Set the SERVICE VEHICLE evidence to ["9.29"]. Add to the rule's note: "9.31's move-over list omits utility service vehicles."
- **Proposed triage: partly: keep the empty evidence, add the note.** a0 M6.1 gave SERVICE VEHICLE empty evidence on purpose. The term is self-made, and 9.29 lists the vehicles that a duty covers rather than defining a term (as for CYCLIST, a0 V3). Add to USER-15's note: "9.31's move-over list leaves out utility service vehicles."

### S2-073. Speed-reduction wording differs between sources without a note

*note* · minor · low confidence

5.70 says "Slow to a speed not more than 20 mph less than the posted speed limit when the posted speed limit is 25 mph or more". 9.30 says "reduce his/her speed to 20 mph below the speed limit". The rule follows 9.30 and says "speed limit" rather than "posted speed limit", but does not mention that the two passages are worded differently.

- Fix: Use "posted speed limit" in both places in the action. Add to the note: "5.70 words the slowing duty as 'not more than 20 mph less than the posted speed limit' and limits it to posted limits of 25 mph or more; 9.30 says '20 mph below the speed limit'."
- **Proposed triage: fix, wording only.** USER-15 and USER-16 action: "20 mph below the posted speed limit"; statements updated to match. No note is needed, because the 25 mph threshold is already in the action.

## PASS-USER-16: Slow down for a stopped service vehicle on a one-lane road

> WHEN the road has one lane in the DRIVER's direction AND the DRIVER is approaching a SERVICE VEHICLE stopped on the road with its lights on or flashing, the DRIVER MUST reduce speed to 20 mph below the speed limit or, where the posted speed limit is less than 25 mph, to less than 5 mph, UNLESS a law enforcement officer directs otherwise.

### S2-074. One-lane condition is not supported by the cited blocks

*support* · major · high confidence

The condition "the road has one lane in the DRIVER's direction" appears in none of the cited blocks. 9.29/9.30 and 5.68/5.70/5.71 state an unconditional duty offered as a choice ending in "or" (9.30: "To reduce his/her speed to 20 mph below the speed limit; or"). The alternative that the one-lane condition rests on (moving over) and any lane-count condition are not in the cited evidence. The note refers to 9.31 and 5.69, but the rule does not cite them. As written, the rule's main restriction is not supported by its citations.

- Fix: Cite the blocks that give the move-over alternative and its lane condition (9.31 and 5.69, per the note), and state in the note that the one-lane condition is inferred from them. Alternatively, write the rule as the handbook's choice: action "reduce speed to 20 mph below the posted speed limit, or vacate the lane closest to the SERVICE VEHICLE when the road has two or more lanes in the same direction", citing all the list items.
- **Proposed triage: fix, citation only.** USER-16 evidence: ["9.29", "9.30", "9.31", "5.68", "5.69", "5.70", "5.71"], as in USER-15. The note already says that with one lane, slowing is the only choice.

### S2-075. Note refers to blocks that are not cited

*citation* · minor · high confidence

The note says "9.29–9.31 and 5.68–5.71 state the duty as a choice", but the evidence lists only 9.29, 9.30, 5.68, 5.70 and 5.71. The blocks 9.31 and 5.69, which the rule's reasoning depends on, are missing from the evidence.

- Fix: Change evidence to ["9.29", "9.30", "9.31", "5.68", "5.69", "5.70", "5.71"].
- **Proposed triage: fix as proposed.** Same change as S2-074.

### S2-076. Officer exception extended from emergency vehicles to all service vehicles

*scope* · minor · medium confidence

The exception comes only from 5.68: "Unless otherwise directed by a law enforcement officer, drivers who approach a stopped emergency vehicle…". 9.29, which covers tow trucks, utility vehicles and TxDOT vehicles, states no such exception. The rule applies "UNLESS a law enforcement officer directs otherwise" to every SERVICE VEHICLE.

- Fix: Add to the note that the officer exception is stated only for stopped emergency vehicles (5.68) and is applied to the other service vehicles by extension. Alternatively, split the emergency-vehicle rule from the 9.29 rule.
- **Proposed triage: fix, note only.** Same as S2-071, in USER-16's note.

### S2-077. Under-25-mph rule applied beyond emergency vehicles

*scope* · major · medium confidence

"where the posted speed limit is less than 25 mph, to less than 5 mph" comes from 5.71, which falls under 5.68 ("a stopped emergency vehicle"). 9.29/9.30, which name tow trucks, utility vehicles and TxDOT vehicles, give only "20 mph below the speed limit" with no low-limit case. The rule applies the 5 mph requirement to all SERVICE VEHICLEs. This is not supported for the non-emergency vehicles. The note admits the source split but the statement does not reflect it.

- Fix: Either split the rule into an emergency-vehicle rule (5.68, 5.70, 5.71, with the 25 mph threshold and the 5 mph case) and a service-vehicle rule (9.29, 9.30, 20 mph below the limit only), or add to the note that the under-25-mph case is extended from 5.71.
- **Proposed triage: partly: note only, no split.** a0 M6.1 combined the two passages into one duty. This gets the same note sentence as S2-071 and S2-076.

### S2-078. SERVICE VEHICLE definition lacks its handbook evidence

*vocabulary* · minor · medium confidence

The SERVICE VEHICLE definition copies the vehicle list in 9.29 ("emergency medical vehicle, law enforcement vehicle, fire truck, tow truck, utility service vehicle, Texas Department of Transportation vehicle…"), yet its evidence is empty. The instructions require citing the block when the handbook supplies the definition.

- Fix: Set the SERVICE VEHICLE evidence to ["9.29"].
- **Proposed triage: rejected, no change.** Same as S2-072 (a0 M6.1).

## PASS-BEING-01: Do not speed up when being passed

> WHEN another vehicle is passing the DRIVER's vehicle, the DRIVER MUST NOT increase speed.

### S2-079. Block 7.48 alone does not state the being-passed situation

*citation* · minor · low confidence

The rule's condition "another vehicle is passing the DRIVER's vehicle" is not stated in block 7.48, which says only 7.48: "Do not increase your speed." This is a list item under the section "Passing". Read alone, it could belong to a list about making a pass rather than being passed. The condition is supported only by 10.115: "When a truck passes you… Don't speed up while the truck is passing." For 7.48 the situation must come from an introductory line that is not among the cited blocks, so the general (non-truck) version of the rule is not fully supported by what is cited. I cannot see that introductory block, so I cannot name its id.

- Fix: Add to `evidence` the block that introduces the list containing 7.48 (the line saying the list applies when another vehicle passes you). Also extend the note: "Block 7.48 is a list item; its situation (being passed) comes from the list's introductory line. Restated for trucks in 10.115."
- **Proposed triage: rejected, no change.** Same as S2-012. 7.48 is in the list under the heading 7.47 "When Another Vehicle is Passing", which a0 C1 named.

## PASS-BEING-02: Stay in lane when being passed

> WHEN another vehicle is passing the DRIVER's vehicle, the DRIVER MUST stay in the DRIVER's lane.

### S2-080. The being-passed condition is not supported by the cited block

*citation* · major · medium confidence

The only cited block is 7.49: "Stay in your lane." It is a bare list item. Nothing in it says the instruction applies when "another vehicle is passing the DRIVER's vehicle". That situation must come from an introductory line or heading for the list, such as one about being passed, and that line is not cited. As cited, the rule's `when` condition has no support. A reader checking the evidence cannot tell whether the item belongs to a being-passed list or to a list of steps for the passer.

- Fix: Add to `evidence` the block id of the line that introduces the list containing 7.49, for example the sentence saying these steps apply when another vehicle is passing you. Also add a note: "Condition taken from the list's introductory line; 7.49 itself only says 'Stay in your lane.'"
- **Proposed triage: rejected, no change.** Same as S2-079.

## PASS-BEING-04: Make passing easy for the other driver

> WHEN another vehicle is passing the DRIVER's vehicle, the DRIVER MUST make it as safe and easy as possible for the PASSER to pass.

### S2-081. Passing is written in lowercase although PASS and PASSER are defined terms

*vocabulary* · minor · medium confidence

The rule introduces the PASSER, whose vocabulary entry reads "The driver making a PASS." Yet both the condition ("another vehicle is passing the DRIVER's vehicle") and the action ("for the PASSER to pass") use lowercase "passing" and "pass". The same act is therefore named once through a defined term and once in plain words. A reader cannot tell whether lowercase "passing" means the defined PASS. The condition also names "another vehicle" instead of the PASSER it introduces. The meaning does not change, but the wording is less formal than the instructions require.

- Fix: Set "when" to "a PASSER is making a PASS of the DRIVER's vehicle". Set "action" to "make it as safe and easy as possible for the PASSER to complete the PASS". Set "statement" to "WHEN a PASSER is making a PASS of the DRIVER's vehicle, the DRIVER MUST make it as safe and easy as possible for the PASSER to complete the PASS."
- **Proposed triage: not an error, no change.** Same as S2-001. "Another vehicle is passing the DRIVER's vehicle" is the BEING group's wording (a0 G7), and "for the PASSER to pass" was set in the a1 triage.

## PASS-BEING-05: Keep to far side of lane when a truck passes

> WHEN a TRUCK is passing the DRIVER, the DRIVER MUST keep to the far side of the DRIVER's lane.

### S2-082. "far side" does not say far from what

*clarity* · minor · medium confidence

The action "keep to the far side of the DRIVER's lane" does not say which side is meant. The handbook's context (10.115: "When a truck passes you, help the truck driver by keeping to the far side of your lane") implies the side away from the passing truck. A model reading the rule alone could not be sure which edge of the lane to move toward.

- Fix: Set action to "keep to the side of the DRIVER's lane farther from the passing TRUCK". Set statement to "WHEN a TRUCK is passing the DRIVER, the DRIVER MUST keep to the side of the DRIVER's lane farther from the passing TRUCK."
- **Proposed triage: fix as proposed.** action: "keep to the side of the DRIVER's lane farther from the passing TRUCK"; statement updated to match.

### S2-083. Advisory wording may be recorded as an instruction

*strength* · major · low confidence

10.115 frames the step as help, not a duty: "help the truck driver by keeping to the far side of your lane. You'll make it easier for the truck driver if…". This is closer to a description of good practice (ADVICE, SHOULD) than a plain command such as "stay" or "do". It contrasts with the block's direct prohibition "Don't speed up while the truck is passing." Recording it as INSTRUCTION/MUST may overstate the handbook's strength. This is debatable, because "help" is grammatically an imperative.

- Fix: Consider force "ADVICE" and modal "SHOULD", with statement "WHEN a TRUCK is passing the DRIVER, the DRIVER SHOULD keep to the side of the DRIVER's lane farther from the passing TRUCK." If INSTRUCTION is kept, add a note explaining that the imperative "help … by keeping" was read as an instruction.
- **Proposed triage: not an error, no change.** Low confidence. "Help the truck driver by keeping to the far side of your lane" is a plain command, so INSTRUCTION fits. The softer sentence, "You'll make it easier … if", is BEING-06, which is recorded as ADVICE.

## PASS-BEING-07: Truck driver helps the passer

> WHEN being passed by another vehicle, the DRIVER of a TRUCK SHOULD stay to the far side of the lane.

### S2-084. "far side of the lane" does not say which side

*clarity* · minor · medium confidence

The action "stay to the far side of the lane" does not say what the side is far from. In 10.112 it is clear only from context: "When passing a truck … The truck driver should make it easier for you to pass by staying to the far side of the lane", meaning the side away from the passing vehicle. A driving model reading only this rule cannot tell which side to keep to. The handbook also gives no lateral position, which is a judgement left to the driver, and this is not recorded in vague_terms.

- Fix: Set action to "stay to the side of the lane away from the passing vehicle" and statement to "WHEN being passed by another vehicle, the DRIVER of a TRUCK SHOULD stay to the side of the lane away from the passing vehicle." Add a note: "Handbook wording: 'staying to the far side of the lane', meaning away from the passer." Optionally add a vague_terms entry for the side of the lane, with the explanation "no lateral distance or position given".
- **Proposed triage: fix, action only.** action: "stay to the side of the lane farther from the passing vehicle", matching BEING-05 (S2-082); statement updated to match. No note or vague term is added.

### S2-085. Note cross-reference uses an incomplete rule id

*format* · minor · low confidence

The note says "The truck driver's signal when returning after passing is BEING-10." Rule ids have the form TOPIC-GROUP-NN, so the reference should be PASS-BEING-10. The note also concerns another rule rather than anything a checker needs to know to check this one.

- Fix: Change the note to "The truck driver's signal when returning after passing is rule PASS-BEING-10." or set it to "".
- **Proposed triage: fix, full id.** BEING-07 note: "The truck driver's signal when returning after passing is PASS-BEING-10." The note stays, because a0 M6.2 asked for it.

## PASS-BEING-08: Do not block someone from passing

> WHEN another DRIVER is trying to pass or enter the DRIVER's lane, the DRIVER MUST NOT intentionally slow down, slam on the brakes, or speed up to keep that DRIVER from passing or entering.

### S2-086. "someone" is narrowed to another DRIVER

*actor/scope* · minor · low confidence

15.79 says: "…to keep someone from passing or entering your lane of travel." The handbook's "someone" covers any road user. The rule writes "another DRIVER is trying to pass…", and the vocabulary defines DRIVER as "A person driving a motor vehicle on the road." This leaves out non-motorized road users, such as a cyclist, who may try to pass or enter the lane.

- Fix: when: "another road user is trying to pass the DRIVER or enter the DRIVER's lane of travel"; action: "intentionally slow down, slam on the brakes, or speed up to keep that road user from passing or entering"; statement: "WHEN another road user is trying to pass the DRIVER or enter the DRIVER's lane of travel, the DRIVER MUST NOT intentionally slow down, slam on the brakes, or speed up to keep that road user from passing or entering."
- **Proposed triage: not an error, no change.** Low confidence. 15.79 is a road-rage tip about other drivers, and the a1 triage kept DRIVER here.

## PASS-BEING-09: Be prepared to move over for faster traffic

> WHEN driving on a FREEWAY in any lane except the right lane used for slower traffic, the DRIVER SHOULD be prepared to move to another lane to allow faster traffic to pass.

### S2-087. FREEWAY condition is not supported by the cited block

*citation* · minor · low confidence

The rule limits itself to "driving on a FREEWAY", but the only cited block, 10.34, does not mention freeways: "Vehicles in any lane, except the right lane used for slower traffic, should be prepared to move to another lane…". The block sits under the section "Highway Driving", and the freeway context comes from 10.13: "Freeways, toll-roads, throughways, turnpikes, and expressways are designed for maximum safety…". That block is not cited. As written, the rule's FREEWAY scope is not supported by its citations.

- Fix: Add 10.13, or the list's lead-in block if there is one, to evidence: ["10.13", "10.34"]. Add a note: "Block 10.34 is a list item under 'Highway Driving'; the freeway scope is taken from the section's opening in 10.13."
- **Proposed triage: fix.** Same as S2-010. BEING-09 evidence: ["10.13", "10.34"]; note: "The FREEWAY setting comes from the Highway Driving section that 10.34 is in, which opens with 10.13."

## No findings (11 rules)

PASS-GEN-01, PASS-GEN-07, PASS-LOC-02, PASS-LOC-04, PASS-SIDE-01, PASS-SIDE-03, PASS-USER-03, PASS-USER-10, PASS-BEING-03, PASS-BEING-06, PASS-BEING-10
