# Atomic check (stage 2): gold_set/tx/overtaking/b1_format.json

Judge: anthropic/claude-opus-5-5 · run folder: `runs\20261121-234532-check-atomic-overtaking-b2` (requests, responses, findings.jsonl, triage.csv) · 58 rules checked, 0 failed calls · $1.2678

All 58 rules were checked, without `--previous`: in round a the judge saw each cited block with only its top-level heading, so the rules that b0 left unchanged had not yet been checked with their full heading path.

**Proposed triage:** each finding has a **Proposed triage** line under its fix, following `allow_list.md`, `error_set.md` and the a0–a3 and b0 triages. All 14 proposed fixes (fix and partly-fixed lines) have been applied to `b2_atomic.json`, which started as an exact copy of `b1_format.json`: 11 rules changed, with every changed statement rebuilt from its fields, and no vocabulary changes. Rule ids are unchanged. Stage 1 on `b2_atomic.json` passes all 8 checks with no format errors (58 rules, 16 vocab terms).

**64 findings** (7 major, 57 minor) in 41 rules.

## PASS-GEN-01: Wait until it is safe to pass

> WHEN it is not safe to pass, the DRIVER MUST be patient and wait until the time is right before passing.

### S2-001. Note overstates the handbook's stated reason

*note* · minor · low confidence

The note reads "improper passing often results in deadly head-on crashes". The handbook says 7.29: "Crashes resulting from improper passing often result in head on crashes and can be deadly." In the handbook, "often" applies to head-on crashes, and "deadly" is only "can be". The note's wording says such crashes are often deadly, which is stronger than the source.

- Fix: note: "Reason given: crashes from improper passing often result in head-on crashes and can be deadly."
- **Proposed triage: fix as proposed.** GEN-01 note: "Reason given: crashes from improper passing often result in head-on crashes and can be deadly." A note that misstates its source is a confirmed error type (a0 N2, S2-008 (a2)).

## PASS-GEN-02: Make certain the way is clear

> WHEN about to pass, the PASSER MUST make certain the way is clear.

### S2-002. Lowercase "pass" in the condition instead of the defined term PASS

*vocabulary* · minor · medium confidence

The PASSER is defined as "The driver making a PASS", so PASS is a defined term. The condition "about to pass" writes it in lowercase. A lowercase look-alike of a vocabulary term leaves unclear whether the defined meaning applies. The meaning here is clearly that defined manoeuvre (7.30 sits under "Basic Safety Rules When You Are Passing").

- Fix: Set when: "about to PASS". Set statement: "WHEN about to PASS, the PASSER MUST make certain the way is clear."
- **Proposed triage: not an error, no change.** Lowercase verb "pass" is allowed (a0 V1, S2-001 (a2)).

## PASS-GEN-03: Signal before changing lanes to pass

> WHEN changing lanes to pass, the PASSER MUST give the proper signal before changing lanes.

### S2-003. Lowercase "pass" used where the defined term PASS is meant

*vocabulary* · minor · medium confidence

The `when` field reads "changing lanes to pass". The actor PASSER is defined as "The driver making a PASS", so PASS is a defined vocabulary term. Here "pass" carries that defined meaning but is written in lowercase. This is inconsistent with the instruction that a word naming a vocabulary term with its defined meaning be written in CAPITALS. It also leaves unclear whether the condition is meant to match the defined manoeuvre.

- Fix: Set when: "changing lanes to PASS". Set statement: "WHEN changing lanes to PASS, the PASSER MUST give the proper signal before changing lanes."
- **Proposed triage: not an error, no change.** Same as S2-002.

## PASS-GEN-04: Tap horn when necessary

> WHEN passing AND it is necessary to avoid surprising or to alert the DRIVER ahead, the PASSER MUST tap the horn.

### S2-004. Lowercase "passing" stands in for the defined term PASS

*vocabulary* · minor · medium confidence

The condition reads "WHEN passing AND …". The actor PASSER is defined as "The driver making a PASS", so the rule set treats PASS as a defined term. Writing the same act in lowercase ("passing") leaves it unclear whether the condition means the defined PASS or some looser sense of passing. That breaks the rule that a phrase naming a vocabulary term should be in CAPITALS. The meaning is unchanged, since the actor is already the PASSER.

- Fix: when: "making a PASS AND it is necessary to avoid surprising or to alert the DRIVER ahead"; statement: "WHEN making a PASS AND it is necessary to avoid surprising or to alert the DRIVER ahead, the PASSER MUST tap the horn."
- **Proposed triage: not an error, no change.** Same as S2-002.

## PASS-GEN-06: Do not linger in the other driver's blind spot

> WHEN passing another vehicle, the PASSER MUST either complete the PASS or slow down out of the other DRIVER's BLIND SPOT, and not drive or linger in it.

### S2-005. Broader highway tip 10.48 cited as support for a passing-only rule

*citation* · minor · medium confidence

The rule is limited to "WHEN passing another vehicle" and is fully supported by 7.53: "When you are passing, do not drive or linger in the other driver’s blind spot. Either pass the other driver or slow down…". Block 10.48 states a different, broader rule from a different section (Highway Safety Tips): "Stay out of another driver’s blind spot… Stay behind or go around the other vehicle. Do not follow to the side." It applies to all highway driving, not only passing. The note admits this. Citing 10.48 makes the evidence broader than the rule and mixes two rules. The instructions say to cite only the materials directly relevant to the rule.

- Fix: Remove "10.48" from evidence: ["7.53", "7.54", "7.54-c"]. Drop the 10.48 sentence from the note, or reword it as: "A broader general rule to stay out of blind spots appears in 10.48; it is a separate rule." Extract 10.48 as its own rule if it is in scope.
- **Proposed triage: rejected, no change.** Settled in a0 C3, which added 10.48 as a supporting block, and S2-008 (a2), which made the note say that 10.48 states the rule more broadly, for all driving.

### S2-006. Prohibition folded into a MUST action

*grammar* · minor · low confidence

The handbook's main command in 7.53 is a prohibition: "do not drive or linger in the other driver’s blind spot". The rule instead uses MUST and puts the prohibition inside the action as "…, and not drive or linger in it". Mixing a positive obligation and a negation in one MUST action is awkward. A reader could also take "it" to refer to the PASS rather than the BLIND SPOT.

- Fix: Set modal to "MUST NOT" and action to "drive or linger in the other DRIVER's BLIND SPOT, and so must either complete the PASS or slow down until out of that BLIND SPOT". Alternatively, keep MUST and use the action "either complete the PASS or slow down so as not to be in the other DRIVER's BLIND SPOT". Rebuild the statement to match whichever option is chosen.
- **Proposed triage: not an error, no change.** Positive phrase first and negated phrase last in one MUST action is the accepted pattern (a0 M1, S2-006 (a2)).

## PASS-GEN-09: Use middle or left lane on highway to pass

> WHEN passing other vehicles on a multi-lane FREEWAY, the PASSER MUST use the middle or left lane.

### S2-007. Setting narrowed to FREEWAY when the source section covers highways generally

*scope* · minor · low confidence

The rule applies only "on a multi-lane FREEWAY". The vocabulary defines FREEWAY as "a freeway, toll-road, throughway, turnpike or expressway". Block 10.23 sits under "Highway Driving > Driving on the Highway > Choose the Proper Lane", and the opening block of that section also defines the wider term: 10.13: "In Texas, a highway is defined as the width between the boundary lines of a publicly maintained way…". Block 10.23 itself names no road type: "Use the middle or left lane if you are … passing other vehicles." Limiting the rule to FREEWAY may narrow it compared with the handbook's "highway" heading. The added word "multi-lane" is implied by "middle or left lane", but it is not stated.

- Fix: Either keep FREEWAY and say in the note that the road type is inferred from the section heading, or word the condition after the subsection: "when": "passing other vehicles on a highway with more than one lane in the PASSER's direction", and add a note saying the setting comes from the "Driving on the Highway" subsection heading.
- **Proposed triage: rejected, no change.** Settled in a0 M5 and S2-010 (a2): the FREEWAY setting comes from 10.13, which is cited, and the note says so. "Multi-lane" follows from "middle or left lane".

### S2-008. Second condition in 10.23 (traveling faster than other traffic) left out without a note

*completeness* · minor · medium confidence

10.23: "Use the middle or left lane if you are traveling faster than other traffic or passing other vehicles." The rule keeps only the passing condition. The faster-traffic condition is closely tied to overtaking, but it is neither included nor mentioned in the note, so a checker cannot tell whether it was dropped on purpose.

- Fix: Add to the note: "10.23 also tells drivers traveling faster than other traffic to use the middle or left lane; that case is left out here because it concerns lane choice rather than passing." Alternatively, add it to the condition with OR.
- **Proposed triage: rejected, no change.** Settled in S2-011 (a2): lane choice by speed is outside the topic (allow list, Scope).

### S2-009. "passing" written in lowercase although PASS is a defined term

*vocabulary* · minor · low confidence

The condition reads "passing other vehicles" in lowercase. PASSER is defined as "The driver making a PASS", so PASS is a vocabulary term. The lowercase verb leaves it unclear whether the defined meaning of PASS is intended.

- Fix: "when": "making a PASS of other vehicles on a multi-lane FREEWAY", with the statement updated to match.
- **Proposed triage: not an error, no change.** Same as S2-002.

## PASS-PROC-01: Keep distance to see ahead

> WHEN preparing to pass on a two-lane road, the PASSER MUST keep enough distance from the car in front to see ahead clearly.

### S2-010. Lowercase "pass" where the defined term PASS is meant

*vocabulary* · minor · medium confidence

The vocabulary defines PASSER as "The driver making a PASS", so PASS is a defined term. The rule's condition, "preparing to pass on a two-lane road", uses the same concept in lowercase. A lowercase word that matches a defined term invites the reader to wonder whether a different meaning is intended. The block's heading "How to Pass on a Two-Lane Road" refers to the same manoeuvre.

- Fix: when: "preparing to PASS on a two-lane road"; statement: "WHEN preparing to PASS on a two-lane road, the PASSER MUST keep enough distance from the car in front to see ahead clearly."
- **Proposed triage: not an error, no change.** Same as S2-002.

## PASS-PROC-02: Check mirrors and blind spot before passing

> WHEN preparing to pass on a two-lane road, the PASSER MUST check the rearview mirror and side mirrors and look over the shoulder into the BLIND SPOT to make sure the roadway is clear and no other vehicles are passing the PASSER's vehicle.

### S2-011. "pass" is written in lowercase although PASS is a vocabulary term

*vocabulary* · minor · medium confidence

The condition reads "preparing to pass on a two-lane road". The rule's own actor, PASSER, is defined as "The driver making a PASS", so PASS is a vocabulary term in this rule set. Here the word names that same manoeuvre, yet it is written in lowercase. This mixes defined and undefined forms of the same term within one rule.

- Fix: when: "preparing to PASS on a two-lane road"; statement: "WHEN preparing to PASS on a two-lane road, the PASSER MUST check the rearview mirror and side mirrors and look over the shoulder into the BLIND SPOT to make sure the roadway is clear and no other vehicles are passing the PASSER's vehicle."
- **Proposed triage: not an error, no change.** Same as S2-002.

## PASS-PROC-03: Left turn signal before passing

> WHEN preparing to pass on a two-lane road, the PASSER MUST turn on the left turn signal to alert DRIVERS behind.

### S2-012. Purpose clause in the action could be read as a condition

*form* · minor · low confidence

The action "turn on the left turn signal to alert DRIVERS behind" includes the reason for the signal. 7.35 gives it as a reason: "Turn on your left turn signal to alert any drivers behind you." The instructions say reasons belong in `note`. Kept in the action, a model could read it as signalling only when drivers are seen behind, while the handbook's command to signal applies to every pass on a two-lane road.

- Fix: action: "turn on the left turn signal"; statement: "WHEN preparing to pass on a two-lane road, the PASSER MUST turn on the left turn signal."; note: "Handbook gives the reason: to alert any drivers behind. In 7.35 the signal follows the mirror and blind-spot checks."
- **Proposed triage: rejected, no change.** The purpose stays in the action, in the wording set in the a1 triage; it says why the signal is given and does not make the signal depend on drivers being behind.

## PASS-PROC-04: Check ahead for no-passing zones and oncoming traffic

> WHEN preparing to pass on a two-lane road, the PASSER MUST check well ahead for signs and pavement markings of a NO-PASSING ZONE and check for oncoming traffic in the left lane.

### S2-013. Lowercase "pass" used where the vocabulary term PASS is meant

*vocabulary* · minor · low confidence

The condition reads "preparing to pass on a two-lane road". The actor PASSER is defined as "The driver making a PASS", so the rule set treats PASS as a defined term. Here the same act is written in lowercase, which leaves it unclear whether "pass" carries the defined meaning. The instructions say a word naming a vocabulary term with its defined meaning should be in CAPITALS.

- Fix: when: "preparing to PASS on a two-lane road"; statement: "WHEN preparing to PASS on a two-lane road, the PASSER MUST check well ahead for signs and pavement markings of a NO-PASSING ZONE and check for oncoming traffic in the left lane." Also make sure PASS is listed in the vocabulary.
- **Proposed triage: not an error, no change.** Same as S2-002.

## PASS-PROC-05: Return before oncoming car is within 200 feet

> WHEN passing on a two-lane road, the PASSER MUST be sure there is enough time and space to overtake the car ahead and return to the right lane before an approaching car comes within 200 feet of the PASSER.

### S2-014. Lowercase "passing" used where the vocabulary term PASS is meant

*vocabulary* · minor · medium confidence

The PASSER vocabulary entry is defined as "The driver making a PASS.", so PASS is a defined term in this rule set. The condition "passing on a two-lane road" names that same manoeuvre in lowercase. The instructions require a phrase that names a vocabulary term with its defined meaning to be written in CAPITALS. The condition is also redundant with the actor PASSER, who is by definition making a PASS.

- Fix: Set when to "making a PASS on a two-lane road". The statement then reads: "WHEN making a PASS on a two-lane road, the PASSER MUST be sure there is enough time and space to overtake the car ahead and return to the right lane before an approaching car comes within 200 feet of the PASSER."
- **Proposed triage: not an error, no change.** Same as S2-002. "WHEN passing" with the PASSER as actor is the set's wording throughout.

## PASS-PROC-06: Pass on the left and clear before returning

> WHEN passing on a two-lane road, the PASSER MUST pass on the left and not return to the right lane until the overtaken vehicle is safely cleared and visible in the rearview mirror, UNLESS passing on a paved shoulder.

### S2-015. Paved-shoulder exception drops the conditions that limit it

*exception* · major · high confidence

The rule's exception is "UNLESS passing on a paved shoulder", with no conditions. Read alone, it releases the PASSER from passing on the left whenever they choose to use a paved shoulder. The cited block permits this only in specific cases. 7.45: "You may pass on a paved shoulder when the vehicle you are passing is slowing or stopped on the main traveled portion of the highway, disabled, or preparing to make a left turn." The note points to PASS-SIDE-02, but a driving model reading only this rule's statement would not see those limits.

- Fix: Set unless to "passing on a paved shoulder when the vehicle being passed is slowing or stopped on the main traveled portion of the highway, is disabled, or is preparing to make a left turn" and update the statement to match. Alternatively, drop the exception and the 7.45 citation and leave shoulder passing to PASS-SIDE-02.
- **Proposed triage: fix, partly as proposed.** The exception now names 7.45's cases, so the rule can be read on its own; the note still points to PASS-SIDE-02. PROC-06 unless: "passing on a paved shoulder when the vehicle being passed is slowing or stopped on the main traveled portion of the HIGHWAY, disabled, or preparing to make a left turn"; statement updated to match. The alternative, dropping the exception, is not taken: it would bring back the conflict fixed in b0 m1.

### S2-016. Vague-term explanation does not say what is left open

*vague_terms* · minor · medium confidence

The vague term "safely cleared" is explained as "defined only by the rearview-mirror check". That explanation suggests the mirror check defines the term, which would make it not vague. In fact 7.38 gives no gap or distance for 'safely', so the margin is left to the driver's judgement.

- Fix: Set the explanation to: "no gap or distance given; the only concrete check is seeing the passed vehicle in the rearview mirror".
- **Proposed triage: fix as proposed.** PROC-06 vague term "safely cleared": explanation "no gap or distance given; the only concrete check is seeing the passed vehicle in the rearview mirror". The explanation should say what the words leave open (task.md).

## PASS-PROC-07: Signal right to return and cancel signal

> WHEN the PASSER has overtaken the vehicle being passed on a two-lane road, the PASSER MUST turn on the right turn signal, return to the right lane, and turn the signal off after the lane change is completed, UNLESS the PASSER passed on a paved shoulder.

### S2-017. Paved-shoulder exception is not stated in the cited passing procedure

*unsupported content* · major · high confidence

The rule adds "UNLESS the PASSER passed on a paved shoulder". The procedure step 7.39 states no exception: 7.39: "Turn on your right turn signal and return to the right lane. Be sure to turn your signal off after you have completed the lane change." Block 7.45 belongs to a different section ("Passing on the Right") and only says when passing on a paved shoulder is allowed: 7.45: "You may pass on a paved shoulder when the vehicle you are passing is slowing or stopped…". It says nothing about signalling or returning to the lane. The exception is the extractor's own inference and is not supported by its citations. It also makes the rule's situation unclear: 7.39 describes the left-side pass on a two-lane road, and that should be stated in the condition, not handled by a carved-out exception.

- Fix: Set unless to "" and state the situation in the condition. when: "the PASSER is passing on the left on a two-lane road AND has overtaken the vehicle being passed". statement: "WHEN the PASSER is passing on the left on a two-lane road AND has overtaken the vehicle being passed, the PASSER MUST turn on the right turn signal, return to the right lane, and turn the signal off after the lane change is completed."
- **Proposed triage: fix, as in S2-015, not as proposed.** The exception stays, with 7.45 cited (b0 m1), and now names 7.45's cases. PROC-07 unless: "the PASSER passed on a paved shoulder a vehicle that was slowing or stopped on the main traveled portion of the HIGHWAY, disabled, or preparing to make a left turn"; statement updated to match.

### S2-018. Irrelevant citation 7.45 and a note that depends on another rule

*citation* · minor · high confidence

7.45 is the permission to pass on a paved shoulder. It does not support any part of this signalling and return step. The note "Passing on a paved shoulder is allowed only in the cases of PASS-SIDE-02 (7.45)" exists only to justify the unsupported exception. It also points to another rule, although each rule should stand on its own.

- Fix: Set evidence to ["7.39"]. Set note to "", or to "Step in the handbook's procedure for passing on a two-lane road."
- **Proposed triage: rejected, no change.** Decided in b0 m1: 7.45 supports the exception, and a link to a related rule is wanted where one rule's scope depends on another (error set, Notes).

## PASS-LOC-01: No left side on roads with two or more lanes each way

> WHEN there are two or more traffic lanes in each direction, the DRIVER MUST NOT drive on the left side of the road.

### S2-019. "left side of the road" is ambiguous in the statement and clarified only in the note

*clarity* · minor · medium confidence

The statement says "the DRIVER MUST NOT drive on the left side of the road" when there are "two or more traffic lanes in each direction". Read alone, a driving model could take this to forbid using the left lane(s) of its own direction on a multilane road. Only the note says the phrase means the opposing half of the road, across the center line. The cited blocks give the wording but not that meaning: 7.17: "Never drive on the left side of the road when:" and 7.20: "There are two or more traffic lanes in each direction". The note's reading is plausible from the section heading ("Keep to the Right"), but it is not stated in the cited blocks. A key term that the action depends on should be explicit in the rule itself.

- Fix: Make the meaning explicit in the action, for example: action "drive on the left side of the road (the half of the road used by oncoming traffic)". Alternatively, define a vocabulary term such as LEFT SIDE OF THE ROAD: "the half of the roadway used by traffic coming in the opposite direction", with empty evidence, and use it in the rule. In the note, say that this interpretation is inferred from the section context and is not stated in 7.17 or 7.20.
- **Proposed triage: rejected, no change.** Settled in S2-023 (a2): the action keeps the handbook's words, and the note gives the reading.

## PASS-MARK-01: Broken line: passing allowed if safe

> WHEN the line the PASSER would cross to pass another vehicle is a BROKEN LINE AND it is safe, the PASSER MAY cross it, UNLESS a SOLID YELLOW LINE is on the PASSER's side of the center line.

### S2-020. The solid-line and unsafe prohibitions are weakened to an exception of a permission

*strength* · minor · medium confidence

6.187 gives a plain command: "Do not cross the line if it is not safe or it is a solid yellow line." 6.200 adds that "A solid yellow line on your side of the road marks a 'no-passing zone.'" The rule puts the solid-line case only in `unless` of a MAY rule ("UNLESS a SOLID YELLOW LINE is on the PASSER's side of the center line"). It puts the unsafe case only in `when` ("AND it is safe"). A MAY rule with an UNLESS only says the permission does not apply. It does not tell the model that crossing is forbidden. The INSTRUCTION-strength prohibition in the cited text is therefore not recorded as a MUST NOT anywhere in this rule, and the note does not mention it.

- Fix: Keep this rule as the permission and add separate INSTRUCTION rules citing 6.187, 6.200 and 6.201. First rule: "WHEN a SOLID YELLOW LINE is on the PASSER's side of the center line, the PASSER MUST NOT cross the center line to pass." Second rule: "WHEN it is not safe, the PASSER MUST NOT cross a BROKEN LINE to pass." Alternatively, add this note: "6.187 also states the solid-line and unsafe cases as prohibitions ('Do not cross the line…'); see the separate MUST NOT rules."
- **Proposed triage: fix, link only.** MARK-02 already states 6.187's prohibitions as a MUST NOT rule, so no new rule is needed (a situation that a sibling rule covers, allow list). Add to MARK-01's note: "6.187's 'Do not cross the line if it is not safe or it is a solid yellow line' is PASS-MARK-02." (error set: missing link to a related rule).

### S2-021. The exception refers to a center line that the condition never establishes

*clarity* · minor · low confidence

Under the BROKEN LINE vocabulary entry, `when` covers any "broken or dashed painted line", which includes lane lines between same-direction lanes. 6.200 does say broken lines "permit you to pass or change lanes". However, `unless` speaks of "the PASSER's side of the center line", which only makes sense on a two-way road with a yellow center line (6.187, 6.201). The rule is therefore unclear about which situations the exception applies to.

- Fix: Make the exception work for any line, for example: unless "the line being crossed has a SOLID YELLOW LINE on the PASSER's side of it". Alternatively, limit the rule to the two-way case, with when: "the center line of a two-way road is a BROKEN LINE AND it is safe".
- **Proposed triage: rejected, no change.** Set in a0 G8 (MARK-01 covers every broken line, as 6.200 does) and S2-027 (a2) (the exception matches MARK-02 and 6.200). Where there is no center line, the exception does not hold and the permission applies.

## PASS-MARK-02: Do not cross solid yellow line or when unsafe

> WHEN on a two-lane road with two-way traffic AND either the center line on the DRIVER's side is a SOLID YELLOW LINE or crossing it is not safe, the DRIVER MUST NOT cross the center line to pass.

### S2-022. Mixed AND/OR condition uses non-grammar word "either" and has unclear precedence

*grammar* · minor · medium confidence

The condition reads "on a two-lane road with two-way traffic AND either the center line on the DRIVER's side is a SOLID YELLOW LINE or crossing it is not safe". The grammar only allows FACT joined by AND / OR. It has no keyword "either" and no grouping, and lowercase "or" is not the OR keyword. A strict parser cannot tell whether the road-type condition applies to both alternatives. The rule also merges two different prohibitions from 6.187 ("Do not cross the line if it is not safe or it is a solid yellow line") into a single entry.

- Fix: Split into two rules. (1) when: "on a two-lane road with two-way traffic AND the center line on the DRIVER's side is a SOLID YELLOW LINE", action: "cross the center line to pass", evidence ["6.187","6.200","6.201","7.17","7.19"]. (2) when: "on a two-lane road with two-way traffic AND crossing the center line is not safe", action: "cross the center line to pass", evidence ["6.187"], with vague term "not safe". Alternatively keep one rule written as "... AND the center line on the DRIVER's side is a SOLID YELLOW LINE OR on a two-lane road with two-way traffic AND crossing the center line is not safe ...", stating the precedence in the note.
- **Proposed triage: rejected, no change.** Settled in S2-030 and S2-031 (a2): a lowercase "or" inside one fact is the accepted convention (a0 G1), and both situations come from one sentence of 6.187 with the same strength.

### S2-023. NO-PASSING ZONE written in capitals but not defined

*vocabulary* · minor · medium confidence

The note writes "marks a NO-PASSING ZONE (6.200)" in capitals, which signals a defined term. NO-PASSING ZONE is not among the vocabulary entries the rule uses. 6.200 supplies a definition: "A solid yellow line on your side of the road marks a 'no-passing zone.'"

- Fix: Either add the vocabulary entry {"term":"NO-PASSING ZONE","definition":"A stretch of road where a SOLID YELLOW LINE is on the driver's side of the center line, in which passing is not allowed.","evidence":["6.200"]}, or write "no-passing zone" in lowercase in the note.
- **Proposed triage: not an error, no change.** Same as S2-033 (a2): NO-PASSING ZONE is in the vocabulary; the judge is shown only the terms used in the statement.

### S2-024. Cited 7.19 covers solid lane lines and signs, not only solid yellow center lines

*citation* · minor · low confidence

7.17/7.19 say "Never drive on the left side of the road when: Pavement markings or signs prohibit driving on the left (a 'No Passing Zone' or solid lane lines)". This is broader than the rule's SOLID YELLOW LINE condition, since it includes signs and solid lane lines of any colour. The note does not mention that the rule rests partly on these blocks, nor how their wording differs.

- Fix: Add to the note: "7.17/7.19 restate the prohibition more broadly ('Never drive on the left side of the road when pavement markings or signs prohibit driving on the left'); signs and other solid lines are left to a separate rule." Alternatively, drop 7.17 and 7.19 from the evidence if they are covered by another rule.
- **Proposed triage: fix, note only.** Same as S2-037 (a2) for SIGN-01. Add to MARK-02's note: "7.17 and 7.19 word the ban more broadly: never drive on the left side of the road where pavement markings prohibit it." The citations stay: in 7.19 the solid lane lines are center lines (S3-002).

## PASS-MARK-03: Do not cross double yellow line to pass

> WHEN on a multi-lane HIGHWAY with a DOUBLE YELLOW LINE, the DRIVER MUST NOT cross the DOUBLE YELLOW LINE to pass.

### S2-025. "multi-lane" is left undefined though the section defines it as four or more lanes

*precision* · minor · medium confidence

The condition reads "on a multi-lane HIGHWAY with a DOUBLE YELLOW LINE". The cited blocks sit under the section heading "Multi-lane Highway (Four or More Lanes)", so the handbook does say what multi-lane means here. The diagram in 6.198 also shows four lanes divided by a double solid yellow centre line. Left as the lowercase "multi-lane", the phrase could be read as any road with two or more lanes. A driving model needs the handbook's lane count to know when the rule applies.

- Fix: Set when: "on a HIGHWAY with four or more lanes divided by a DOUBLE YELLOW LINE". Set statement: "WHEN on a HIGHWAY with four or more lanes divided by a DOUBLE YELLOW LINE, the DRIVER MUST NOT cross the DOUBLE YELLOW LINE to pass." Add note: "Section heading for 6.197 is 'Multi-lane Highway (Four or More Lanes)'; the diagram 6.198 shows a four-lane road with a double solid yellow centre line."
- **Proposed triage: rejected, no change.** Settled in S2-034 (a2): the multi-lane condition comes from the heading 6.196.

## PASS-SIGN-01: No Passing Zone and Do Not Pass signs

> WHEN in a NO-PASSING ZONE marked for the DRIVER's direction by a 'No Passing Zone' pennant sign or a 'Do Not Pass' sign, the DRIVER MUST NOT pass other vehicles.

### S2-026. Note states a fine from uncited blocks, while the penalty field is empty

*citation* · minor · medium confidence

The note says "disobeying it is a violation with a fine of $1 to $200 (6.266, 6.267)". Blocks 6.266 and 6.267 are not in the rule's evidence, and none of the cited blocks mentions a violation or a fine. So this claim is not supported by the citations. It also conflicts with the empty `penalty` field: if the handbook states a penalty for this rule, it belongs in `penalty` with its source cited; if not, it should not be in the note.

- Fix: If 6.266/6.267 state a penalty specifically for disobeying these signs, add them to `evidence` and set `penalty` to "A fine of $1 to $200.". Otherwise remove the sentence "The pennant is a warning sign; disobeying it is a violation with a fine of $1 to $200 (6.266, 6.267)." from the note.
- **Proposed triage: rejected, no change.** Settled in a0 M4, S2-035 (a2) and S3-008 (allow list, Penalties).

### S2-027. Pennant is treated as marking the zone, but the handbook calls it an advance warning

*faithfulness* · minor · low confidence

The condition reads "in a NO-PASSING ZONE marked … by a 'No Passing Zone' pennant sign". Block 6.50 says the pennant is an "Advance warning of no pass zones", so it is posted ahead of the zone rather than marking its extent. The rule does not make clear where the ban starts. The note mentions the advance-warning role, but the statement itself does not.

- Fix: Set when to: "in a NO-PASSING ZONE indicated for the DRIVER's direction by a 'Do Not Pass' sign or announced ahead by a 'No Passing Zone' pennant sign". Add to the note: "The pennant warns in advance that a no-passing zone is ahead."
- **Proposed triage: rejected, no change.** Settled in S2-036 (a2), which set the condition; the advance-warning role is in the note and the NO-PASSING ZONE entry cites 6.50.

### S2-028. 'for the DRIVER's direction' is not supported by the cited sign blocks

*citation* · minor · low confidence

The qualifier "marked for the DRIVER's direction" does not appear in any cited block. Blocks 6.120, 6.129 and 6.50 describe the signs without reference to direction of travel. The only similar wording shown is 6.200 ("A solid yellow line on your side of the road"), which concerns pavement lines, not signs, and is not cited.

- Fix: Drop the qualifier so when reads: "in a NO-PASSING ZONE marked by a 'No Passing Zone' pennant sign or a 'Do Not Pass' sign". Alternatively, keep it and explain in the note that it is inferred from sign placement.
- **Proposed triage: rejected, no change.** The wording was set in S2-036 (a2). A no-passing zone applies to one direction (6.200: "on your side of the road", cited by the NO-PASSING ZONE entry).

## PASS-SIGN-02: Curve and winding road signs: do not pass

> WHEN passing a warning sign for a reverse curve, sharp turn, gradual curve, reverse sharp turn, sharp curve chevron, or winding road, the DRIVER MUST NOT pass other vehicles in the curve or winding section ahead.

### S2-029. "passing a warning sign" reuses the overtaking verb in another sense

*clarity* · minor · medium confidence

In a rule set about overtaking, the condition "WHEN passing a warning sign for a reverse curve…" uses "passing" to mean driving past a sign. The action "pass other vehicles" then uses "pass" to mean overtaking. A reader or a program matching on "pass" could read the condition as overtaking a sign, or could merge the two senses. The handbook rows only say the sign warns of the road ahead, e.g. 6.73: "Road ahead makes a sharp turn… do not pass."

- Fix: when: "the DRIVER has driven past a warning sign for a reverse curve, sharp turn, gradual curve, reverse sharp turn, sharp curve chevron, or winding road"; statement: "WHEN the DRIVER has driven past a warning sign for a reverse curve, sharp turn, gradual curve, reverse sharp turn, sharp curve chevron, or winding road, the DRIVER MUST NOT pass other vehicles in the curve or winding section ahead."
- **Proposed triage: rejected, no change.** Settled in a0 G4, S2-038 (a2) and S3-009 (allow list, Writing and grammar).

### S2-030. Note does not say the sign rows word the rule as a plain command

*note* · minor · medium confidence

Every sign row words the rule as a plain command: "do not pass" (6.68, 6.73, 6.74, 6.78, 6.95, 6.110). Under the instructions that wording is an INSTRUCTION. The rule records REQUIREMENT, which rests on 6.266: "It is a violation to disobey the instructions… of a warning sign". The instructions say that when passages word the same rule differently, the stronger wording should be recorded and the note should say so. The note cites 6.266 but does not explain that this is why the force is REQUIREMENT rather than INSTRUCTION. 6.56 is also hedged ("may be a traffic violation").

- Fix: Add to note: "The sign descriptions word this as a plain command ('do not pass', INSTRUCTION); 6.266 makes disobeying a warning sign a violation, so the stronger REQUIREMENT is recorded."
- **Proposed triage: fix, note only.** task.md asks the note to say when the stronger wording is recorded, as LOC-05's and GEN-08's notes do. SIGN-02 note: "The sign descriptions word this as a plain command ('do not pass'); disobeying a warning sign is a violation (6.56, 6.266), punishable by the fine in 6.267, so the stronger wording is recorded. Each sign description also says to slow down and keep right; those are not passing rules."

## PASS-SIGN-03: Two-arrow sign: pass on either side

> WHEN a sign shows two arrows pointing down to the left and right at a traffic island or obstruction, the DRIVER MAY pass on either side of the traffic island or obstruction.

### S2-031. Rule is about going around an island or obstruction, not overtaking, and 'pass' is ambiguous

*scope* · minor · medium confidence

The topic is overtaking: passing another vehicle, and being passed. Block 6.98 says the sign "Indicates traffic is permitted to pass on either side of a traffic island or an obstruction." Here "pass" means going around a fixed object. It does not mean overtaking a vehicle. The rule still files this under topic PASS and uses the lowercase verb "pass" in "the DRIVER MAY pass on either side of the traffic island or obstruction". A model reading the PASS rule set could take this as permission to overtake another vehicle on either side near an island. The rule is arguably outside the requested topic. If it is kept, its wording should make clear that it concerns which side of the object to drive on.

- Fix: Drop the rule as out of scope for overtaking. If it is kept, set action to "drive around the traffic island or obstruction on either side" and update the statement to match. Add to note: "'Pass' in 6.98 means going around a fixed island or obstruction, not overtaking another vehicle."
- **Proposed triage: rejected, no change.** Settled in a0 M6.3 and S2-040 (a2): passing a hazard other than a vehicle is in scope (allow list, Scope), and since S2-041 (a2) the action names the traffic island or obstruction.

## PASS-SIGN-04: Barricade stripes: bear to the side they slope down

> WHEN a barricade or vertical panel has diagonal stripes sloping downward to one side, the DRIVER SHOULD bear to the side to which the stripes slope downward.

### S2-032. Rule is about following channelizing devices, not overtaking

*scope* · major · medium confidence

The topic is "overtaking (passing another vehicle, and being passed)". The cited blocks are about steering around construction barricades and vertical panels, not about overtaking another vehicle. 6.243 says: "The diagonal stripes on the barricade or vertical panel guide the driver towards the direction to where the traffic is to pass." Here "pass" means going past the obstruction on a given side; the section headings "Pass to the Right" and "Pass to the Left" use it the same way. The rule seems to have been included only because the word "pass" appears. Keeping it in an overtaking ground-truth set would wrongly count work-zone lane guidance as an overtaking rule.

- Fix: Remove PASS-SIGN-04 from the overtaking rule set. If it is kept anywhere, move it to a rule set on signs and work-zone devices.
- **Proposed triage: rejected, no change.** Settled in a0 M6.4 and S2-043 (a2) (allow list, Scope). The judge now sees the heading "Passing Traffic" and gives no new evidence.

## PASS-SIDE-01: When passing on the right in a lane is allowed

> WHEN conditions permit doing so safely AND the road is one-way or is both clear of parked vehicles and other lane obstructions and wide enough for two or more lanes in each direction, the PASSER MAY ONLY pass on the right in a traffic lane.

### S2-033. Nested lowercase 'or'/'and' make the condition's grouping ambiguous

*grammar* · minor · medium confidence

The CONDITION grammar joins FACTs with the keywords AND/OR. This rule mixes one keyword AND with lowercase 'or', 'both … and' and a second 'and': "the road is one-way or is both clear of parked vehicles and other lane obstructions and wide enough for two or more lanes in each direction". A parser cannot recover the intended grouping, and a reader could take the 'and' before 'wide enough' as a top-level conjunction. The handbook lists two separate alternatives: 7.43 "The road is clear of parked vehicles or other lane obstructions and is wide enough for two or more lanes in each direction" and 7.44 "You are on a one-way road."

- Fix: Make the alternatives separate FACTs, or split the rule in two. For example: when = "conditions permit doing so safely AND (the road is a one-way road OR the road is clear of parked vehicles and other lane obstructions and is wide enough for two or more lanes in each direction)". Alternatively write two MAY rules, one per list item, each with "conditions permit doing so safely AND …", and use the matching statement for each.
- **Proposed triage: rejected, no change.** Settled in a0 G1, which wrote SIDE-01 this way: alternatives inside one fact are joined by a lowercase "or", and "both … and" groups the two parts of 7.43.

### S2-034. 'in a traffic lane' restriction is not supported by the cited blocks

*faithfulness* · minor · low confidence

The cited blocks say only "you can pass on the right" (7.42) under the listed conditions. They do not mention traffic lanes or exclude shoulders. The action "pass on the right in a traffic lane" adds a qualifier that the cited text does not contain. The note justifies it by a separate shoulder rule, but that rule's source is not cited here.

- Fix: Use action "pass on the right" to match 7.42. Alternatively, keep the qualifier and cite the block that separates shoulder passing from lane passing, explaining this in the note.
- **Proposed triage: rejected, no change.** Set in S3-004: SIDE-01 covers a traffic lane because passing on a paved shoulder is PASS-SIDE-02, and the note says so.

## PASS-SIDE-02: Passing on a paved shoulder

> WHEN conditions permit doing so safely AND the vehicle being passed is slowing or stopped on the main traveled portion of the HIGHWAY, disabled, or preparing to make a left turn, the PASSER MAY ONLY pass on a paved shoulder.

### S2-035. MAY ONLY makes the paved shoulder the only place the passer may pass

*strength/modal* · major · high confidence

The statement reads: "...the PASSER MAY ONLY pass on a paved shoulder." Taken literally, it says that whenever the vehicle ahead is slowing, stopped, disabled or turning left, the passer may pass only on the shoulder. That rules out passing in another lane. The handbook says nothing like this. 7.45: "You may pass on a paved shoulder when the vehicle you are passing is slowing or stopped…". This is a plain permission. The "only" belongs to passing on the right in general (7.42: "you can pass on the right only when conditions permit you to do so safely"), not to the shoulder. The note's reading ("it does not require using the shoulder") contradicts what the statement says. A driving model reading only the statement would misunderstand it.

- Fix: Use modal "MAY" (force PERMISSION). Statement: "WHEN conditions permit doing so safely AND the vehicle being passed is slowing or stopped on the main traveled portion of the HIGHWAY OR is disabled OR is preparing to make a left turn, the PASSER MAY pass on a paved shoulder." To capture the restriction, add a note saying that 7.42 limits passing on the right to situations where conditions permit it safely. Do not phrase the action as "MAY ONLY pass on a paved shoulder".
- **Proposed triage: rejected, no change.** Settled in a0 G3 and S2-044 (a2) (allow list, Writing and grammar): MAY ONLY follows 7.42's "only", and the note gives the reading.

### S2-036. The OR alternatives are written in lowercase prose, not grammar keywords

*grammar* · minor · medium confidence

The condition "…is slowing or stopped on the main traveled portion of the HIGHWAY, disabled, or preparing to make a left turn" joins its alternatives with commas and a lowercase "or". It sits inside an AND-joined CONDITION. The grammar requires FACTs joined by AND/OR keywords. As written, it is unclear how the alternatives group with "conditions permit doing so safely".

- Fix: when: "conditions permit doing so safely AND (the vehicle being passed is slowing or stopped on the main traveled portion of the HIGHWAY OR the vehicle being passed is disabled OR the vehicle being passed is preparing to make a left turn)". If parentheses are not allowed, state in the note that the safety condition applies to all three cases.
- **Proposed triage: rejected, no change.** Settled in S2-045 (a2): a lowercase "or" inside one fact (a0 G1).

## PASS-SIDE-03: Do not pass on the right off the pavement

> WHEN passing on the right, the PASSER MUST NOT drive off the paved portion of the HIGHWAY.

### S2-037. "passing" is written in lowercase although PASS is the defined term

*vocabulary* · minor · low confidence

The condition "passing on the right" names the act that the actor PASSER is defined by ("The driver making a PASS"). It is written in lowercase rather than with the defined term PASS. This makes it unclear whether it means a PASS as defined in the rule set. The handbook block 7.46 ("Do not pass on the right by driving off the paved portion of the highway") refers to the same overtaking manoeuvre.

- Fix: when: "making a PASS on the right"; statement: "WHEN making a PASS on the right, the PASSER MUST NOT drive off the paved portion of the HIGHWAY."
- **Proposed triage: not an error, no change.** Same as S2-002.

## PASS-USER-01: Stop for a school bus with flashing red lights

> WHEN approaching a school bus from either direction AND the bus is displaying alternately flashing red lights, the DRIVER MUST stop, UNLESS the school bus is on a different road OR the DRIVER is on a CONTROLLED-ACCESS HIGHWAY where the bus is stopped in a loading zone and pedestrians are not permitted to cross.

### S2-038. Compound exception mixes keyword OR with lowercase 'where … and'

*grammar* · minor · medium confidence

The unless field reads "the school bus is on a different road OR the DRIVER is on a CONTROLLED-ACCESS HIGHWAY where the bus is stopped in a loading zone and pedestrians are not permitted to cross". In the grammar, facts are joined only by the keywords AND or OR. Here the second fact is a single fact with a 'where' clause and a lowercase 'and' inside it, so the AND/OR structure is not explicit. A parser, or a careless reader, cannot tell that all three conditions in the highway exception must hold together. The handbook, 5.78: "…when on a controlled-access highway where the bus is stopped in a loading zone and pedestrians aren't permitted to cross", requires all three.

- Fix: unless: "the school bus is on a different road OR (the DRIVER is on a CONTROLLED-ACCESS HIGHWAY AND the school bus is stopped in a loading zone AND pedestrians are not permitted to cross)". Alternatively keep the wording and add a note that the three highway conditions must all hold.
- **Proposed triage: not an error, no change.** The second alternative is one fact (a place where all three hold), written with a lowercase "and" inside it, the same convention as the lowercase "or" inside one fact (a0 G1). The grammar has no brackets.

### S2-039. Penalty summary drops part of Table 15

*penalty* · minor · medium confidence

The penalty field says "2nd within 5 years $1,000-$2,000". Block 5.82 applies this to the "2nd conviction and every conviction after (within 5 years)". The field also gives no fine or jail terms for the injury offences. 5.83 says "fine of up to $4,000 and/or up to one year in jail", and 5.84 says "180 days to 2 years confinement and a possible fine of up to $10,000". The field is meant to be only a few words, but saying '2nd' alone understates the scope of the penalty.

- Fix: penalty: "1st conviction $500-$1,250; 2nd and later convictions within 5 years $1,000-$2,000 and possible suspension up to six months; causing serious bodily injury is a Class A misdemeanor (up to $4,000 and/or one year in jail), or a state jail felony after a previous such conviction; subsequent conviction causes automatic suspension."
- **Proposed triage: fix, partly as proposed.** The penalty understates 5.82 ("2nd conviction and every conviction after"): a penalty misstated (S2-046 (a2)). USER-01 penalty: "2nd within 5 years" becomes "2nd and later convictions within 5 years"; the rest is unchanged. The fines and jail terms for the injury offences are not added: the field is a few words (task.md).

## PASS-USER-02: Do not pass a stopped school bus until allowed

> WHEN the DRIVER has stopped for a school bus displaying alternately flashing red lights, the DRIVER MUST NOT pass the school bus, UNLESS the school bus has resumed motion OR the DRIVER of the school bus signals the DRIVER to proceed OR the red lights are no longer flashing.

### S2-040. DRIVER names both the actor and the bus driver

*vocabulary* · minor · medium confidence

The exception reads "the DRIVER of the school bus signals the DRIVER to proceed". The capitalised term DRIVER is used here for two different people: the bus driver and the rule's actor. A reader has to work out which DRIVER is which. The handbook says only 5.76: "You are signaled by the driver to proceed".

- Fix: Set unless to: "the school bus has resumed motion OR the school bus driver signals the DRIVER to proceed OR the red lights are no longer flashing". Update the statement to match.
- **Proposed triage: rejected, no change.** Settled in S2-048 (a2) and the a1 triage.

### S2-041. Penalty summary drops 'and every conviction after'

*penalty* · minor · medium confidence

The penalty says "2nd within 5 years $1,000-$2,000 and possible suspension". The table row is 5.82: "2nd conviction and every conviction after (within 5 years)", so the summary leaves out third and later convictions. Also, 5.78 refers to "Table 17" while the caption 5.79 reads "Table 15". This mismatch is not mentioned in the note.

- Fix: Change the penalty to: "1st conviction $500-$1,250; 2nd and later conviction within 5 years $1,000-$2,000 and possible suspension up to six months; causing serious bodily injury is a Class A misdemeanor (up to $4,000 and/or one year in jail), or a state jail felony after a previous such conviction; a subsequent conviction brings automatic suspension." Add to the note: "5.78 refers to Table 17, but the penalty table is captioned Table 15."
- **Proposed triage: fix, penalty only.** Same penalty change as S2-039. The Table 17 remark stays in USER-01's note (S2-049 (a2)).

## PASS-USER-04: Checks before passing a truck

> WHEN about to pass a TRUCK, the PASSER MUST NOT move into the passing lane before checking front and rear, mirrors and BLIND SPOTS, and confirming the lane is clear and the road is a legal passing zone.

### S2-042. "legal passing zone" is an undefined key term

*vocabulary* · minor · medium confidence

The action requires "confirming … the road is a legal passing zone". The phrase is written in lowercase and is not in the vocabulary. A driving model cannot tell from it which signs or markings make a stretch of road a legal passing zone. The cited block 10.112 also leaves it undefined: "…only if it is clear and you are in a legal passing zone." Because the handbook does not define the term here, it should either link to a vocabulary term defined elsewhere or be listed as a vague term.

- Fix: Add to vague_terms: {"term": "a legal passing zone", "explanation": "the cited block does not say which signs or markings make a zone legal for passing"}. Alternatively, if the rule set defines a NO-PASSING ZONE or a similar term, use that defined term in CAPITALS instead.
- **Proposed triage: not an error, no change.** Whether a stretch of road is a legal passing zone is set by the markings, signs and places in the LOC, MARK and SIGN rules, not left to the driver's judgement, so it is not a vague term. The rule keeps 10.112's words.

## PASS-USER-05: Flash headlights when passing a truck

> WHEN passing a TRUCK, the PASSER MUST let the DRIVER of the TRUCK know of the PASS by flashing the headlights.

### S2-043. "Especially at night" is left out of the statement

*completeness* · minor · low confidence

In 10.112 the handbook says: "Let the truck driver know you are passing by flashing your headlights, especially at night." The rule's statement drops "especially at night" and records it only in the note. A driving model reading only the statement gets no sign that the handbook stresses signalling after dark. The phrase is also a vague emphasis: it does not say how strongly the rule applies in daylight compared with night. That vagueness is not recorded in vague_terms.

- Fix: Set action to "let the DRIVER of the TRUCK know of the PASS by flashing the headlights, especially at night". Set statement to "WHEN passing a TRUCK, the PASSER MUST let the DRIVER of the TRUCK know of the PASS by flashing the headlights, especially at night." Add the vague term {"term": "especially at night", "explanation": "emphasis only; does not say how the duty differs by day"}. Set note to "".
- **Proposed triage: rejected, no change.** Settled in a0 G5 and S2-052 (a2): emphasis stays in the note.

## PASS-USER-07: Return in front of a truck only when its front is visible

> WHEN passing a TRUCK, the PASSER MUST NOT move back into the lane in front of the TRUCK, UNLESS the entire front of the TRUCK can be seen in the rearview mirror.

### S2-044. Note claims more than the handbook says about flashed lights

*note* · minor · low confidence

The note says the truck driver's flash "does not replace seeing the entire front of the TRUCK in the rearview mirror." Block 10.114 only places the two sentences side by side: "If the driver flashes the truck's lights after you pass, it's a signal that it is clear for you to pull back in front of the truck. Be sure to move back only when you can see the entire front of the truck in your rearview mirror." It never says how the flash relates to the mirror check. The note presents the extractor's reading as if the handbook stated it, so a checker cannot tell it is an inference.

- Fix: Change the note to: "The same block says that if the truck driver flashes the truck's lights after the pass, it is a signal that it is clear to pull back in front of the truck. Reading the two sentences together, the mirror check is taken to still apply when the lights are flashed. The block also says to maintain speed after passing a truck; that is a separate rule."
- **Proposed triage: fix, note only (reopens S2-056 (a2) on new grounds).** S2-056 (a2) made the note say the flash does not replace the mirror check, but not that this is a reading of 10.114: an inference not stated in the note (error set). USER-07 note: "If the truck driver flashes the truck's lights after the pass, it is a signal that it is clear to pull back in. The same block says to move back only when the entire front of the truck can be seen in the rearview mirror, so the flash is read as not replacing that check." The maintain-speed sentence is USER-08 and is not repeated (allow list, Notes).

## PASS-USER-08: Maintain speed after passing a truck

> WHEN having passed a TRUCK, the PASSER MUST maintain speed.

### S2-045. "maintain speed" drops the handbook's "your" and leaves unclear which speed is meant

*clarity* · minor · low confidence

The handbook says 10.114: "After you pass a truck, maintain your speed." This means the passer should keep the speed used for the pass and not slow down once back in front of the truck. The rule's action "maintain speed" drops "your", so it does not say whose speed or which speed is to be kept. Nothing in the rule warns against slowing down in front of the truck, which is the point of the instruction. The vague-terms list also does not record that the handbook gives no duration or distance for keeping the speed; it only flags the condition phrase.

- Fix: Set action to "maintain the speed used to complete the PASS and not slow down in front of the TRUCK" and make the statement: "WHEN having passed a TRUCK, the PASSER MUST maintain the speed used to complete the PASS and not slow down in front of the TRUCK." Alternatively keep the handbook wording "maintain their speed". Add a note: "Handbook says only 'maintain your speed'; it gives no duration or distance."
- **Proposed triage: rejected, no change.** Settled in S2-058 (a2).

## PASS-USER-09: Never cut in front of a truck

> WHEN trying to reach an exit or turn, or a single-lane construction zone, ahead of a TRUCK or bus, the DRIVER MUST slow down and exit or stay behind the TRUCK or bus, and not cut into the open space in front of it.

### S2-046. General prohibition narrowed to exit, turn and construction-zone situations

*scope* · major · medium confidence

The block opens with an unconditional prohibition, 10.129: "Never cut in front of a truck." The rule only applies it "WHEN trying to reach an exit or turn, or a single-lane construction zone, ahead of a TRUCK or bus". A driving model would read the rule as allowing a cut-in in front of a truck in any other situation, such as completing a pass on an open highway. The exit/turn context comes from the section heading, and the construction zone is given as "a particularly dangerous" example. Neither limits the opening command.

- Fix: Split into two rules. (1) when: "in front of a TRUCK", action: "cut into the open space in front of the TRUCK", modal MUST NOT. Statement: "WHEN in front of a TRUCK, the DRIVER MUST NOT cut into the open space in front of the TRUCK." (2) when: "trying to reach an exit or turn, or a single-lane construction zone, ahead of a TRUCK", action: "slow down and exit, or stay behind the TRUCK", modal MUST. Statement: "WHEN trying to reach an exit or turn, or a single-lane construction zone, ahead of a TRUCK, the DRIVER MUST slow down and exit, or stay behind the TRUCK."
- **Proposed triage: rejected, no change.** Settled in S2-059 and S2-060 (a2): under the heading 10.128, 10.129's "Never cut in front of a truck" is about cutting in to reach an exit or turn, and cutting back in after passing a truck is USER-07. The judge now sees the heading and gives no new evidence.

### S2-047. Positive and negative obligations combined under one MUST

*grammar* · minor · high confidence

The action "slow down and exit or stay behind the TRUCK or bus, and not cut into the open space in front of it" puts a prohibition inside a MUST action. The grammar expects a single MODAL per rule, and the instructions say to keep separate rules apart. The "and/or" grouping is also ambiguous: it can be read as "(slow down and exit) or (stay behind)", or as "slow down and (exit or stay behind)".

- Fix: Make the prohibition its own MUST NOT rule, as in the split above. Write the remaining action as "either slow down and exit, or stay behind the TRUCK".
- **Proposed triage: fix, wording only.** The MUST with a negated last phrase is the accepted pattern (a0 M1, S2-061 (a2)), so the rule is not split. The grouping point is new: 10.129's "Either" is added. USER-09 action: "either slow down and exit, or stay behind the TRUCK or bus, and not cut into the open space in front of it"; statement updated to match.

### S2-048. Bus added to the required alternative action

*faithfulness* · minor · medium confidence

The block mentions bus only in its explanation, 10.129: "Cutting into the open space in front of a truck or bus removes…". Its command and its alternative are about trucks only: "Never cut in front of a truck… stay behind the truck." The rule extends "stay behind the TRUCK or bus" and the construction-zone situation to buses. The instruction itself does not say this.

- Fix: Remove "or bus" from the when and action fields. If bus coverage is kept, add a note saying it is inferred from the explanatory sentence only.
- **Proposed triage: rejected, no change.** Settled in S2-062 (a2).

### S2-049. Vague terms not listed

*vague terms* · minor · medium confidence

"the open space in front of it" gives no distance, and "cut into" does not say how close a lane change counts as cutting in. Yet vague_terms is empty.

- Fix: Add to vague_terms: {"term": "open space in front of", "explanation": "no distance given"} and {"term": "cut into", "explanation": "no gap or distance defining a cut-in"}.
- **Proposed triage: fix, one term.** Vague words not listed (error set). Add `{"term": "the open space in front of it", "explanation": "no distance given"}`. "cut into" is not added: it names the act, and the open space is what leaves the distance open.

### S2-050. Note's 'driver's cushion of safety' is ambiguous

*note* · minor · medium confidence

The note says "cutting in removes the driver's cushion of safety". In this rule set, DRIVER is the actor, the one doing the cutting in. In the handbook the cushion belongs to the truck or bus driver.

- Fix: Note: "Reason given: cutting into the open space in front of a truck or bus removes the truck or bus driver's cushion of safety; beating a truck to a single-lane construction zone is described as particularly dangerous."
- **Proposed triage: fix, reason only.** USER-09 note: "Reason given: cutting into the open space in front of a truck or bus removes the truck or bus driver's cushion of safety." The construction-zone sentence is left out: it is already in the condition.

## PASS-USER-11: Wait for a truck backing into a loading area

> WHEN a TRUCK is preparing to back or is backing from the road into a loading area, the DRIVER MUST wait for the TRUCK to complete its maneuver before trying to pass.

### S2-051. Note omits the handbook's blind-spot reason

*note* · minor · medium confidence

The note gives only one reason: "the road is temporarily blocked while the truck backs." The cited block gives a second reason, tied to passing: 10.125: "If you pass too closely behind the truck, a crash may occur because you are in the truck's blind spot." The instructions say to record reasons the handbook gives in `note`, so a checker reading this note gets an incomplete picture.

- Fix: Set note to: "Reasons given: the road is temporarily blocked while the truck backs, and passing too closely behind the truck puts the driver in the truck's blind spot, where a crash may occur. The same block's 'Never cross behind a truck preparing to back up' is a separate rule."
- **Proposed triage: rejected, no change.** Settled in S2-065 (a2): the blind-spot reason goes with the ban on crossing behind the truck, PASS-USER-17, whose note gives it.

## PASS-USER-12: Care when passing a distracted driver

> WHEN passing the vehicle of a DRIVER who seems to be distracted, the PASSER SHOULD be very careful.

### S2-052. Vague-term explanation points to blocks the rule does not cite

*citation* · minor · medium confidence

The explanation for "seems to be distracted" reads "cues listed in 10.207-10.210 but judgement left to driver". Blocks 10.207–10.210 are not in the rule's evidence, so the claim that they list cues cannot be checked from the citations. The only cited block, 10.212, says just "Be very careful when passing a driver who seems to be distracted" and lists no cues. The explanation either leans on uncited material or adds something the citations do not support.

- Fix: Change the explanation to describe only what the term leaves open, for example: {"term": "seems to be distracted", "explanation": "no signs of distraction given; left to the driver's judgement"}. If blocks 10.207–10.210 do list the cues a driver should look for, cite them in evidence and say so in note.
- **Proposed triage: rejected, no change.** Settled in S2-066 (a2) (allow list, Citations).

## PASS-USER-13: Do not share a lane with a motorcycle

> WHEN near a MOTORCYCLE in a traffic lane, the DRIVER MUST allow the MOTORCYCLE a full lane width, and not attempt to share the lane with it.

### S2-053. Condition "near a MOTORCYCLE" is not in the handbook and is then flagged as vague

*condition* · minor · medium confidence

The rule's condition is "near a MOTORCYCLE in a traffic lane", and it lists "near a MOTORCYCLE" as a vague term ("does not say how near"). The cited block contains no nearness condition. 10.160 says: "Allow the motorcyclist a full lane width… the motorcycle is entitled to a full lane… Do not attempt to share the lane with a motorcycle." The duty applies whenever a motorcycle occupies a lane. The extractor has added its own vague qualifier that the handbook does not use, which makes the scope look fuzzier than the source.

- Fix: when: "a MOTORCYCLE is in a traffic lane"; statement: "WHEN a MOTORCYCLE is in a traffic lane, the DRIVER MUST allow the MOTORCYCLE a full lane width, and not attempt to share the lane with it."; vague_terms: []
- **Proposed triage: rejected, no change.** Settled in a0 (vague terms) and S2-067 (a2) (allow list, Vague terms).

### S2-054. Handbook's reason not recorded in note

*note* · minor · medium confidence

10.160 gives a reason for the rule: "the motorcycle is entitled to a full lane and may need the room to maneuver safely", even though "it may seem as though there is enough room". The instructions say to record a reason the handbook gives in `note`. The note only explains why the rule is relevant to the topic.

- Fix: note: "Included because it rules out passing a motorcycle within its lane. The handbook explains that even if there seems to be room, the motorcycle is entitled to a full lane and may need the room to maneuver safely."
- **Proposed triage: fix as proposed, in the set's "Reason given" form.** The handbook's reason missing from the note (error set, S2-065 (a2)). USER-13 note: "Included because it rules out passing a motorcycle within its lane. Reason given: even if there seems to be room, the motorcycle is entitled to a full lane and may need the room to maneuver safely."

## PASS-USER-15: Move over or slow down for a stopped service vehicle

> WHEN the road has two or more lanes in the DRIVER's direction AND the DRIVER is approaching a SERVICE VEHICLE stopped on the road with its lights on or flashing, the DRIVER MUST move out of the lane closest to the SERVICE VEHICLE, or reduce speed to 20 mph below the posted speed limit or, where the posted speed limit is less than 25 mph, to less than 5 mph, UNLESS a law enforcement officer directs otherwise.

### S2-055. The whole duty is limited to multi-lane roads, so the slow-down duty is lost on single-lane roads

*condition* · major · high confidence

The rule puts "the road has two or more lanes in the DRIVER's direction" in `when`, so it applies only on multi-lane roads. In the handbook, the lane count is a condition only of the move-over option. 5.69 says: "Vacate the lane closest … if the highway has two or more lanes traveling in the direction of the emergency vehicle". 9.31 likewise says "Move out of the lane … if the road has multiple lanes traveling in the same direction." The slow-down duty has no lane condition. 9.29/9.30 say: "the driver is required: To reduce his/her speed to 20 mph below the speed limit". 5.70/5.71 give the slow-down limits without one either. As written, a driver on a road with one lane in each direction is told nothing, when the handbook requires them to slow down.

- Fix: Remove the lane condition from `when` and attach it to the move-over option. when: "the DRIVER is approaching a SERVICE VEHICLE stopped on the road with its lights on or flashing"; action: "reduce speed to not more than the posted speed limit minus 20 mph or, where the posted speed limit is less than 25 mph, to less than 5 mph, or, where the road has two or more lanes in the DRIVER's direction, move out of the lane closest to the SERVICE VEHICLE". Alternatively, split into two rules: (a) on a road with only one lane in the DRIVER's direction, the DRIVER MUST slow down as above; (b) on a road with two or more lanes in the DRIVER's direction, the DRIVER MUST either move out of the closest lane or slow down as above.
- **Proposed triage: rejected, no change.** Settled in a0 M6.1 and S2-070 (a2): with one lane in the DRIVER's direction, PASS-USER-16 requires slowing down (allow list, Conditions and actor).

### S2-056. Speed limit wording reads as a target rather than a maximum

*accuracy* · minor · medium confidence

The rule says "reduce speed to 20 mph below the posted speed limit". 5.70 sets a ceiling: "Slow to a speed not more than 20 mph less than the posted speed limit". In other words, the speed must be at most the posted limit minus 20 mph. "To 20 mph below" can be read as an exact target speed rather than a maximum.

- Fix: Reword to "reduce speed to not more than 20 mph below the posted speed limit".
- **Proposed triage: rejected, no change.** The wording was set in S2-073 (a2) from 9.30 ("reduce his/her speed to 20 mph below the speed limit"). 5.70's "not more than 20 mph less than" is not a clearer ceiling, so 9.30's wording is kept.

### S2-057. Move-over option is extended to utility service vehicles, which 9.31 leaves out

*scope* · minor · low confidence

Because the rule uses SERVICE VEHICLE, the move-over option covers utility service vehicles and other construction or maintenance vehicles. 9.31 lists only "the emergency medical vehicle, law enforcement vehicle, fire truck, tow truck or a TxDOT vehicle". The note admits this but the statement still generalizes. The effect is small, since slowing down remains an option, but the statement says more than its citations support.

- Fix: In the note, state that the move-over option for utility service vehicles is not supported by 9.31. Alternatively, restrict the move-over option in the action to the vehicles 9.31 lists.
- **Proposed triage: rejected, no change.** Settled in S2-072 (a2): the note says 9.31's move-over list leaves out utility service vehicles.

## PASS-USER-16: Slow down for a stopped service vehicle on a one-lane road

> WHEN the road has one lane in the DRIVER's direction AND the DRIVER is approaching a SERVICE VEHICLE stopped on the road with its lights on or flashing, the DRIVER MUST reduce speed to 20 mph below the posted speed limit or, where the posted speed limit is less than 25 mph, to less than 5 mph, UNLESS a law enforcement officer directs otherwise.

### S2-058. The two speed cases are joined by an ambiguous 'or' and the 25 mph threshold is missing

*clarity* · minor · medium confidence

The action reads "reduce speed to 20 mph below the posted speed limit or, where the posted speed limit is less than 25 mph, to less than 5 mph". The handbook gives the 20 mph reduction only for limits of 25 mph or more (5.70: "…when the posted speed limit is 25 mph or more; or"). The 5 mph ceiling applies when the limit is below 25 mph (5.71). Because the rule leaves out the ≥25 mph condition and joins the cases with "or", it can be read as a free choice between the two targets. The handbook's "or" joins conditional alternatives, not options for the driver. The phrase "reduce speed to 20 mph below" also suggests one exact target. 5.70 says "not more than 20 mph less than the posted speed limit", which a driving model needs to read as a ceiling.

- Fix: Set action to: "reduce speed to no more than 20 mph below the posted speed limit where the posted speed limit is 25 mph or more, and to less than 5 mph where the posted speed limit is less than 25 mph". Update the statement to match.
- **Proposed triage: rejected, no change.** Settled in S2-073 (a2): the 25 mph threshold is in the action ("where the posted speed limit is less than 25 mph"), and the wording follows 9.30.

## PASS-BEING-03: Move right on unmarked roads when being passed

> WHEN being passed on the left AND the lanes are not marked, the DRIVER MUST safely move as far to the right as possible.

### S2-059. Handbook wording "as you can" changed to "as possible"

*wording* · minor · low confidence

The extractor's instructions say to "Keep the handbook's own words in the rule" where a judgement is left to the driver. The rule's action says "safely move as far to the right as possible", but the cited block says 7.50: "Safely move as far to the right as you can…". The meaning is close, but the vague phrase is reworded, and the vague_terms entry quotes the reworded phrase rather than the handbook's.

- Fix: action: "safely move as far to the right as the DRIVER can"; statement: "WHEN being passed on the left AND the lanes are not marked, the DRIVER MUST safely move as far to the right as the DRIVER can."; vague_terms: [{"term": "safely", "explanation": "no criteria given"}, {"term": "as far to the right as the DRIVER can", "explanation": "no distance given"}]
- **Proposed triage: not an error, no change.** Low confidence. Paraphrasing a vague phrase close to the handbook is fine; the entry was set in a0 (vague terms).

## PASS-BEING-04: Make passing easy for the other driver

> WHEN another vehicle is passing the DRIVER's vehicle, the DRIVER MUST make it as safe and easy as possible for the PASSER to pass.

### S2-060. Lowercase "passing" in the condition instead of the defined term PASS

*vocabulary* · minor · medium confidence

The rule names the other driver as the PASSER, which the vocabulary defines as "The driver making a PASS." Yet the condition uses lowercase "another vehicle is passing the DRIVER's vehicle", and the action ends with lowercase "to pass". The instructions say a word naming a vocabulary term with its defined meaning should be in CAPITALS. Mixing a defined PASSER with an undefined lowercase "passing" makes it unclear whether the condition is the same manoeuvre as PASS. The source, 7.51: "Make it as safe and easy as possible for the other driver to pass you.", uses the same notion throughout.

- Fix: when: "a PASSER is making a PASS of the DRIVER's vehicle"; action: "make it as safe and easy as possible for the PASSER to complete the PASS"; statement: "WHEN a PASSER is making a PASS of the DRIVER's vehicle, the DRIVER MUST make it as safe and easy as possible for the PASSER to complete the PASS."
- **Proposed triage: not an error, no change.** Same as S2-081 (a2): the BEING group's wording (a0 G7), with "for the PASSER to pass" set in the a1 triage.

## PASS-BEING-07: Truck driver helps the passer

> WHEN being passed by another vehicle, the DRIVER of a TRUCK SHOULD stay to the side of the lane farther from the passing vehicle.

### S2-061. Interpretation of "far side" is not noted

*note* · minor · low confidence

The handbook says only 10.112: "The truck driver should make it easier for you to pass by staying to the far side of the lane." The rule turns "far side" into "the side of the lane farther from the passing vehicle". This is the natural reading, but it is an interpretation rather than the handbook's wording. The note does not mention it or the purpose the handbook gives (to make the pass easier). It refers only to another rule.

- Fix: Set note to: "Handbook says 'staying to the far side of the lane'; read as the side away from the passing vehicle. The stated purpose is to make it easier for the other driver to pass. The truck driver's signal when returning after passing is PASS-BEING-10."
- **Proposed triage: rejected, no change.** Settled in S2-084 (a2), which changed the action and added no note.

## PASS-BEING-08: Do not block someone from passing

> WHEN another DRIVER is trying to pass or enter the DRIVER's lane, the DRIVER MUST NOT intentionally slow down, slam on the brakes, or speed up to keep that DRIVER from passing or entering.

### S2-062. "someone" is narrowed to "another DRIVER"

*actor/condition scope* · minor · medium confidence

The handbook protects anyone trying to pass or merge. 15.79 says: "Do not … speed up to keep someone from passing or entering your lane of travel." The rule's condition reads "another DRIVER is trying to pass or enter the DRIVER's lane". The vocabulary defines DRIVER as "A person driving a motor vehicle on the road", so a cyclist or other road user trying to pass is no longer covered. The rule also uses DRIVER for both parties ("another DRIVER … the DRIVER's lane … that DRIVER"), which makes it harder to read.

- Fix: Set when: "another road user is trying to pass the DRIVER or enter the DRIVER's lane of travel". Set action: "intentionally slow down, slam on the brakes, or speed up to keep that road user from passing or entering the lane". Set statement: "WHEN another road user is trying to pass the DRIVER or enter the DRIVER's lane of travel, the DRIVER MUST NOT intentionally slow down, slam on the brakes, or speed up to keep that road user from passing or entering the lane."
- **Proposed triage: rejected, no change.** Settled in S2-086 (a2) and the a1 triage.

## PASS-BEING-09: Be prepared to move over for faster traffic

> WHEN driving on a FREEWAY in any lane except the right lane used for slower traffic, the DRIVER SHOULD be prepared to move to another lane to allow faster traffic to pass.

### S2-063. Rule is limited to FREEWAY although its section speaks of highways in general

*scope* · major · medium confidence

The rule restricts the advice to "driving on a FREEWAY". Block 10.34 itself names no road type: "Vehicles in any lane, except the right lane used for slower traffic, should be prepared to move to another lane to allow faster traffic to pass." Its section is "Highway Driving > Driving on the Highway". Block 10.13 lists freeways and similar roads, but it also defines a much broader term: "In Texas, a highway is defined as the width between the boundary lines of a publicly maintained way, any part of which is open to the public for vehicular travel." The FREEWAY condition is therefore an inference that may be too narrow. A driving model would not apply the advice on other multi-lane highways, which the section heading appears to cover.

- Fix: Set when to "driving on a multi-lane highway in any lane except the right lane used for slower traffic". If the FREEWAY reading is kept, change the note to say the road type is inferred from the section context and that the section's heading and 10.13's definition refer to highways generally.
- **Proposed triage: rejected, no change.** Settled in a0 M5 and S2-087 (a2): the FREEWAY setting comes from 10.13, which is cited, and the note says so. The judge now sees the heading and gives no new evidence.

### S2-064. 10.13 cited only for context, not for the rule's content

*citation* · minor · low confidence

Block 10.13 states no part of this rule. It introduces freeways and defines "highway". It is cited only to justify the inferred FREEWAY setting, and the vocabulary entry for FREEWAY already cites it. If the condition is broadened, this citation no longer supports anything in the rule.

- Fix: If the condition is changed to a general highway setting, set evidence to ["10.34"]. Keep 10.13 only if the FREEWAY condition is retained, with the note explaining that the setting is inferred.
- **Proposed triage: rejected, no change.** 10.13 was added in S2-087 (a2) because the FREEWAY setting rests on it (error set: supporting block not cited).

## No findings (17 rules)

PASS-GEN-05, PASS-GEN-07, PASS-GEN-08, PASS-LOC-02, PASS-LOC-03, PASS-LOC-04, PASS-LOC-05, PASS-USER-03, PASS-USER-06, PASS-USER-10, PASS-USER-14, PASS-USER-17, PASS-BEING-01, PASS-BEING-02, PASS-BEING-05, PASS-BEING-06, PASS-BEING-10
