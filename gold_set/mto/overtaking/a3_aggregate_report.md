# Aggregate check (stage 3): gold_set\mto\overtaking\a2_atomic.json

Judge: anthropic/claude-opus-5-5 · run folder: `runs\20261117-220631-check-aggregate-overtaking-a3` (request, response, findings.jsonl, triage.csv) · 72 rules, whole corpus · $0.9545

**10 findings** (3 major, 7 minor): 6 coverage, 3 conflict, 1 other.

**Triage:** all 10 findings were triaged, and fixes were applied to `a3_aggregate.json`, which started as an exact copy of `a2_atomic.json`. Each decision is recorded under its finding as a **Triage** line.
- Rules added: PASS-USER-24 (S3-006) and PASS-SIDE-04 (S3-008), each at the end of its group.
- Rules merged: old PASS-SIGN-04 was merged into PASS-SIGN-03 (S3-009), so old PASS-SIGN-05 is now **PASS-SIGN-04**. No note cross-references the SIGN rules, so no notes needed updating. Finding text uses the original ids.
- After all fixes there are 73 rules and 20 vocabulary terms. Stage 1 on `a3_aggregate.json` passes all 8 checks with no format errors.

## Coverage

### S3-001. Blind-spot checks for being overtaken while turning or pulling over are missing

*missing rule* · major · medium confidence · rules: no rule

The handbook gives checks for a driver who may be overtaken. 29.44: "If it is possible for another vehicle to overtake you while you are turning, check your blind spot before starting to turn." 29.171: "If there is a chance of traffic or pedestrians overtaking you on the right, check your right blind spot just before pulling over." These fall under 'being passed', and no BEING rule covers them.

- Fix: Add PASS-BEING-08: WHEN about to turn AND another vehicle could overtake the DRIVER during the turn, the DRIVER MUST check the BLIND SPOT before starting to turn (INSTRUCTION; evidence 29.44). Add PASS-BEING-09: WHEN about to pull over to the roadside AND traffic or pedestrians could overtake on the right, the DRIVER MUST check the right BLIND SPOT just before pulling over (INSTRUCTION; evidence 29.171).
- **Triage: ignored, no change.** These are general cautions about doing something else (turning, pulling over) while another vehicle might pass, not rules about overtaking or being passed. Same decision as a0 M9.3. The existing BEING rules all cover a pass that is actually happening or wanted.

### S3-002. Regulatory 'Slower traffic keep right' sign not used

*missing citation* · minor · medium confidence · rules: PASS-GEN-04, PASS-BEING-01

18.29-c: "Slow traffic on multi-lane roads must keep right." This is a regulatory sign that requires slower traffic to keep right so faster vehicles can pass. PASS-GEN-04 rests only on 5.13 ("This is especially important if you are driving more slowly"). No rule cites the sign or covers its recognisable visual cue.

- Fix: Add a rule PASS-SIGN-06: WHEN on a multi-lane road posted with a 'Slower Traffic Keep Right' sign AND driving slower than other traffic, the DRIVER MUST keep to the right lane (REQUIREMENT; evidence 18.9, 18.29, 18.29-c). Alternatively, add 18.29 and 18.29-c to PASS-GEN-04 with a note.
- **Triage: fixed by adding the citation (the alternative), with no new rule.** PASS-GEN-04's evidence is now `["5.13", "18.29", "18.29-c"]`. A sentence was added to its note: "The regulatory 'Slower traffic keep right' sign (18.29) states the slow-traffic case as a requirement: 'Slow traffic on multi-lane roads must keep right.'" The force stays INSTRUCTION, because the sign covers only slow traffic on multi-lane roads, while GEN-04 applies to every driver on any road. BEING-01 is unchanged.

### S3-003. Stronger 'illegal' wording for cutting in front not used

*strength / missing citation* · minor · medium confidence · rules: PASS-PROC-06, PASS-USER-08

PASS-PROC-06 is recorded as INSTRUCTION from 10.10 and 10.19. Other passages word cutting off more strongly. 12.23: "Be careful not to cut off any vehicle… It is dangerous and illegal for a slower moving vehicle to cut in front of a faster moving vehicle." 23.23 lists "intentionally cutting off another vehicle" among sanctioned aggressive driving. Neither is cited.

- Fix: Add 12.23 and 23.23 to PASS-PROC-06 evidence. Note the 'illegal' wording, and either raise the force to REQUIREMENT or explain why it is kept as INSTRUCTION.
- **Triage: rejected, no change, based on past triage.** a0 M8 already weighed 12.23 and 23.23 against 10.10. It chose INSTRUCTION / MUST NOT from the "Never" of 10.10, and the fix was accepted as proposed. The "illegal" sentence of 12.23 covers a slower vehicle cutting in front of a faster one, which is not the case of a PASSER moving back in front of the vehicle it passed. 23.23 lists aggressive driving and is not a passing rule.

### S3-004. Not moving up beside a large vehicle turning wide is not covered

*missing rule* · minor · low confidence · rules: no rule

6.57: "If a large vehicle in front of you is making a right turn, do not move up into the space that opens up in the right lane… Stay well back until the truck has completely cleared the lane." 6.58 gives the same for double left-turn lanes. This is moving alongside a turning large vehicle, close to the PASS-USER-06 case for small vehicles. It is a boundary case for the overtaking topic.

- Fix: Add PASS-USER-24: WHEN a LARGE VEHICLE in front is making a right turn (or a left turn from double left-turn lanes) and swings wide, the DRIVER MUST NOT move up into the space that opens beside it and MUST stay well back until it has cleared the lane (INSTRUCTION; evidence 6.57, 6.58).
- **Triage: ignored, no change.** 6.57 and 6.58 are about not moving into the space beside a turning large vehicle. The handbook does not present this as passing.

### S3-005. Passing a stopped school bus (stated as illegal, with penalty) not addressed

*missing rule* · minor · low confidence · rules: no rule

8.32: "school bus drivers and other witnesses can report vehicles that have illegally passed a school bus… fined heavily and get six demerit points for a first offence." 6.89: "Do not proceed on your route until the bus moves…" The handbook frames failing to stop as illegally passing the bus, but the set has no rule or cross-reference for it. This is a boundary case: it is mainly a stopping rule.

- Fix: Either add a rule: WHEN approaching a stopped school bus with its overhead red lights flashing or stop arm out (from behind, or from the front on a road without a median), the DRIVER MUST NOT pass it (REQUIREMENT; penalty: heavy fine and six demerit points; evidence 8.26, 8.29, 8.32, 6.89). Or add a scope note explaining why it is left to the stopping topic.
- **Triage: rejected, no change, based on past triage.** The same school-bus finding was rejected in a0 M9.6. It is a stopping rule, left to that topic.

### S3-006. Passing animals on or near the road not covered

*missing rule* · minor · low confidence · rules: PASS-USER-22

13.47: "If you see an animal on or near the road, slow down and pass carefully as they may suddenly bolt onto the road." 13.57: "Don't try to drive around the animal." This is passing a road hazard, comparable to the roadside-worker rule PASS-USER-22. It is a boundary case for passing another vehicle.

- Fix: Add PASS-USER-25: WHEN an animal is on or near the road, the DRIVER MUST slow down and pass carefully (INSTRUCTION; evidence 13.47). Optionally cross-reference 13.57.
- **Triage: added as proposed, as PASS-USER-24, not USER-25.** Numbering continues from USER-23, since the USER-24 proposed in S3-004 was ignored.
  - Rule: "Slow down and pass animals carefully": "WHEN an animal is on or near the road, the DRIVER MUST slow down and pass carefully." INSTRUCTION / MUST, evidence `["13.47"]`.
  - Vague terms: "slow down" (no amount or target speed given) and "carefully" (no criteria given).
  - Note: "Reason given: animals may suddenly bolt onto the road."
  - The optional cross-reference to 13.57 ("Don't try to drive around the animal") was left out. That sentence is collision-avoidance advice for an animal directly ahead, and it reads against "pass carefully".

## Conflicts

### S3-007. High-beam instruction while passing ignores the 150 m oncoming-vehicle dip rule

*missing exception* · major · medium confidence · rules: PASS-NIGHT-04, PASS-NIGHT-01

PASS-NIGHT-04 says the PASSER "MUST switch on the high-beam headlights" when alongside the passed vehicle, with no exception. The handbook requires low beams near oncoming traffic: 4.65: "remember to switch to low beams within 150 metres of an oncoming vehicle… These rules apply to all roads"; 14.8: "Use your low-beam headlights within 150 metres of an oncoming vehicle". The night-passing steps also assume a clear road: 10.29: "If you have to pass and the way is clear". As written, the rule requires high beams even when an oncoming vehicle is within 150 m. That breaks a lighting requirement which carries a penalty (22.135). PASS-NIGHT-01 carries only the following-distance exception.

- Fix: Change PASS-NIGHT-04 unless to "an oncoming vehicle is within 150 metres". Add 4.65 and 14.8 to its evidence. Add a note that the 150 m oncoming low-beam rule still applies while passing.
- **Triage: fixed as proposed.**
  - NIGHT-04 now reads: "WHEN passing at night AND moving alongside the vehicle being passed, the PASSER MUST switch on the high-beam headlights, UNLESS an oncoming vehicle is within 150 metres."
  - Evidence: `["4.65", "10.29", "10.31", "14.8"]`. a0 C3 removed 4.65, because it did not support switching to high beams; it comes back here because it supports the new exception.
  - A sentence was added to the note: "The rule to use low beams within 150 metres of an oncoming vehicle (4.65, 14.8) still applies while passing."

### S3-008. Unconditional permission to pass on the right overlaps restrictions stated elsewhere

*overlapping conditions* · major · medium confidence · rules: PASS-SIDE-01, PASS-SIDE-02, PASS-LOC-07

PASS-SIDE-01 says "WHEN on a multi-lane road OR … overtaking a left-turning vehicle, the DRIVER MAY pass on the right" with no exception. PASS-SIDE-02 forbids suddenly changing lanes to pass on the right when in the leftmost lane behind a slower vehicle (10.41). The handbook also forbids going around a left-turner in an intersection. 29.104: "If your lane is blocked by a vehicle turning left… slow down or stop instead of pulling out to go around the vehicle." 10.11: "Don't change lanes in or near an intersection." A reader of SIDE-01 alone would take passing a left-turner on the right inside an intersection to be allowed. The set never says how SIDE-01 relates to SIDE-02 or to LOC-07, the paved-shoulder-only case.

- Fix: Add to PASS-SIDE-01 unless: "in or near an intersection". Add a note that PASS-SIDE-02 and PASS-LOC-07 restrict it. Add a rule: WHEN driving through an intersection AND the DRIVER's lane is blocked by a vehicle turning left, the DRIVER MUST slow down or stop and MUST NOT pull out to go around the vehicle (INSTRUCTION; evidence 29.104, 10.11).
- **Triage: fixed as proposed.** The new rule's wording follows the a0 M3 pattern, since a rule has only one MODAL.
  - **PASS-SIDE-01:** unless "in or near an intersection". Statement: "WHEN on a multi-lane road OR on a one-way road OR overtaking a STREETCAR OR overtaking a left-turning vehicle, the DRIVER MAY pass on the right, UNLESS in or near an intersection." `10.11` ("Don't change lanes in or near an intersection") was added to its evidence, which is now `["10.11", "10.40", "10.41"]`, because the new exception rests on it. A sentence was added to the note: "PASS-SIDE-02 and PASS-LOC-07 restrict this permission."
  - **New PASS-SIDE-04**, "Do not go around a left-turner in an intersection": "WHEN driving through an intersection AND the DRIVER's lane is blocked by a vehicle turning left, the DRIVER MUST slow down or stop and not pull out to go around the vehicle." INSTRUCTION, evidence `["10.11", "29.104"]`. The proposed "MUST … and MUST NOT …" has two modals, so it is written with the positive phrase first and the negated phrase last.

### S3-009. Same keep-right-in-passing-lane situation given different strengths

*inconsistent strength* · minor · medium confidence · rules: PASS-SIGN-03, PASS-SIGN-04

PASS-SIGN-03 says the DRIVER MUST keep right where passing/climbing lanes are provided (regulatory sign 18.40). PASS-SIGN-04 says the DRIVER of a slower vehicle SHOULD move into the right-hand lane on such a section (10.35). For a slower driver at a signed passing lane, the two rules state the same duty at different strengths, and neither refers to the other.

- Fix: Add a note to PASS-SIGN-04 that where the 18.40 sign is posted, PASS-SIGN-03 (MUST) applies. Alternatively, merge the two, citing 10.34, 10.35, 18.40 and 18.40-c with REQUIREMENT force where signed.
- **Triage: fixed by merging (the alternative).** PASS-SIGN-04 was merged into PASS-SIGN-03, and old PASS-SIGN-05 was renumbered PASS-SIGN-04.
  - The merged **PASS-SIGN-03** is titled "Keep right where a passing lane is provided". It keeps the signed condition and the REQUIREMENT / MUST force: "WHEN on a two-lane section where a PASSING LANE is provided AND a keep-right-except-to-pass sign is posted, the DRIVER MUST keep to the right lane, UNLESS the DRIVER is passing." Evidence: `["10.34", "10.35", "18.40", "18.40-c"]`.
  - Its note now reads: "10.35 describes the same lane use more softly, as the purpose of passing lanes (slower vehicles move into the right-hand lane so faster ones can pass in the left lane); the 'must' of the regulatory sign (18.40) is recorded. Diagram 2-48 shows a truck in the right lane being passed."
  - Old SIGN-04's vague term "slower vehicle" was dropped with it. Its unsigned ADVICE case (10.35 alone) no longer has a rule of its own.

## Other

### S3-010. Vocabulary PASS defined as a lane change but used for shoulder passing and in-lane cases

*vocabulary misfit* · minor · low confidence · rules: PASS-LOC-07, PASS-USER-23, PASS-BEING-07

PASS is defined as "Changing lanes to move past a slower vehicle" (10.14). PASS-LOC-07 lets the driver pass on the paved right shoulder, which is not a lane change. PASS-BEING-07 speaks of discouraging passing within a shared lane, which the handbook (10.24) calls passing "in the same lane". The defined term does not fit these uses.

- Fix: Add a note to PASS that the handbook also uses 'pass' for moving past on the shoulder or within a lane (10.24, 10.38). Alternatively, use lowercase 'pass' in those rules and keep PASS for the lane-change manoeuvre.
- **Triage: ignored, no change.**
