# Aggregate check (stage 3): gold_set\ca\overtaking\a2_atomic.json

Judge: anthropic/claude-opus-5-5 · run folder: `runs\20261120-202537-check-aggregate-overtaking-a3` (request, response, findings.jsonl, triage.csv) · 46 rules, whole corpus · $0.5503

**11 findings** (5 major, 6 minor): 7 coverage, 3 conflict, 1 other.

**Triage:** all 11 findings were triaged by the reviewer. Fixes were applied to `a3_aggregate.json`, which started as an exact copy of `a2_atomic.json`. Each decision is recorded under its finding as a **Triage** line.
- Four rules were added at the end of their groups, so no rules were renumbered: PASS-LOC-07 (S3-001), PASS-BEING-08 (S3-002), PASS-USER-20 (S3-003) and PASS-USER-21 (S3-004).
- Two scope calls differ from MTO for CA: being passed by an emergency vehicle and the stopped school bus are in scope.
- After the fixes there are 50 rules and 15 vocabulary terms. The new rules have not had an atomic check; the next round's atomic check covers them.
- Format check (`check_format.py a3_aggregate.json --handbook ca --allow-lowercase pass`): no format errors.

## Coverage

### S3-001. DO NOT PASS regulatory sign is not covered

*missing rule* · major · high confidence · rules: no rule

Figure 12.89 shows a DO NOT PASS sign among the 'White Regulatory Signs'. 12.85 says white rectangular signs communicate "many important rules you must obey", and 12.67 says "Follow the sign's instruction." No rule forbids passing where this sign is posted. Every MARK and LOC rule is based on markings or places, not on this sign.

- Fix: Add PASS-LOC-07 "No passing where DO NOT PASS sign posted": force REQUIREMENT, modal MUST NOT, actor PASSER, when "a DO NOT PASS sign is posted for the PASSER's direction of travel", action "pass", unless "", statement "WHEN a DO NOT PASS sign is posted for the PASSER's direction of travel, the PASSER MUST NOT pass.", note "Rule shown only by the sign in figure 12.89; 12.85 says white regulatory signs state rules you must obey.", evidence ["12.89","12.84","12.85","12.67"].
- **Triage: fixed as proposed, with two changes.** Added **PASS-LOC-07**, "No passing where DO NOT PASS sign posted": REQUIREMENT / MUST NOT, actor PASSER, "WHEN a do-not-pass sign is posted for the PASSER's direction of travel, the PASSER MUST NOT pass.", evidence `12.67`, `12.85`, `12.89`. The changes: the sign is named by its meaning in lowercase, and its wording DO NOT PASS goes in the note, because in CAPS "DO" fails the vocabulary check (MTO `allow_list.md`: a sign may be named by its meaning, SIGN-01). The heading `12.84` is not cited, because headings are not citable blocks (a2 S2-019). Figure 12.89 was viewed and does show the DO NOT PASS sign among the white regulatory signs.

### S3-002. Being passed by an emergency vehicle is not covered

*missing rule* · major · high confidence · rules: no rule

13.44 says: "Give the right-of-way to any law enforcement vehicle, fire engine, ambulance, or other emergency vehicle using a siren and red lights. Failure to pull over may result in a ticket. Drive to the right edge of the road and stop until the emergency vehicle(s) have passed." 13.48 adds: "If you are in an intersection … continue through the intersection. Drive to the right as soon as it is safe and stop." Figure 13.45 shows a car pulling over to let a fire truck pass. This is a being-passed rule and it states a penalty. The BEING group omits it.

- Fix: Add PASS-BEING-08: force REQUIREMENT, modal MUST, actor DRIVER, when "an emergency vehicle using a siren and red lights approaches", action "drive to the right edge of the road and stop until the emergency vehicle has passed", unless "the DRIVER is in an INTERSECTION, in which case the DRIVER continues through it and then drives to the right as soon as it is safe and stops", penalty "A ticket for failure to pull over.", evidence ["13.44","13.45","13.46","13.48"].
- **Triage: fixed as proposed.** Added **PASS-BEING-08**, "Pull over and stop for an emergency vehicle": REQUIREMENT / MUST, with the proposed condition, action and exception, penalty "A ticket for failure to pull over.", evidence `13.44`, `13.45`, `13.46`, `13.48`. Added the vague term "as soon as it is safe" (no criteria given) and a note on figure 13.45. This settles the scope question left open at a0 ("Considered and not raised"): being passed by an emergency vehicle is in scope for CA.

### S3-003. Passing a school bus with flashing red lights is not covered

*missing rule* · major · medium confidence · rules: no rule

13.158 says: "When the bus flashes red lights … you must stop from either direction until the children are safely across the street and the lights stop flashing… If you fail to stop, you may be fined up to $1,000 and your driving privilege could be suspended for one year." 13.159 gives the exception: "If the school bus is on the other side of a divided or multilane highway … you do not need to stop." Figure 13.151 has the caption "All vehicles must stop for school buses." This in effect forbids driving past a stopped school bus, and it carries a stated penalty. The set covers buses only at safety zones (USER-04). This case is on the boundary of the topic, because it is worded as a stop requirement rather than a passing rule.

- Fix: Add PASS-USER-20: force REQUIREMENT, modal MUST, actor DRIVER, when "a school bus ahead or approaching is flashing its red lights", action "stop and remain stopped, not driving past the bus, until the children are safely across and the lights stop flashing", unless "the school bus is on the other side of a divided or multilane highway with two or more lanes in each direction", penalty "Fine up to $1,000 and possible one-year suspension.", evidence ["13.151","13.152","13.158","13.159"]. Optionally add an ADVICE rule for the flashing yellow lights in 13.157.
- **Triage: fixed as proposed.** Added **PASS-USER-20**, "Do not drive past a school bus with flashing red lights": REQUIREMENT / MUST, with the proposed condition, action, exception and penalty, evidence `13.151`, `13.152`, `13.158`, `13.159`. Added the vague term "safely across" and a note that the handbook words it as a stop requirement that applies from either direction. The optional ADVICE rule for flashing yellow lights (13.157) was not added. For CA this puts the stopped school bus in scope, unlike the MTO allow list.

### S3-004. Ban on cutting in front of a large vehicle when returning after a pass is not used

*missing rule* · major · medium confidence · rules: PASS-USER-03, PASS-PROC-01

USER-03 tells the PASSER to "move ahead of it after passing" a LARGE VEHICLE. The handbook also says, in 13.8: "Do not move in front of a large vehicle and suddenly slow down or stop. The large vehicle will not be able to stop fast enough…" and, in 13.13: "do not: Change lanes directly in front of them to reach an exit or turn." These limits on how a PASSER returns to the lane ahead of a truck are not captured.

- Fix: Add PASS-USER-21: force INSTRUCTION, modal MUST NOT, actor PASSER, when "returning to the lane in front of a LARGE VEHICLE after passing it", action "move in front of it and then suddenly slow down or stop, or change lanes directly in front of it to reach an exit or turn", evidence ["13.8","13.12","13.13"]. Note the reason the handbook gives: large vehicles take longer to stop.
- **Triage: fixed as proposed.** Added **PASS-USER-21**, "Do not cut in front of a large vehicle after passing": INSTRUCTION / MUST NOT, actor PASSER, with the proposed condition and action, evidence `13.8`, `13.12`, `13.13`. The note gives 13.8's reason. Added the vague terms "suddenly" and "directly in front".

### S3-005. Response to a passer cutting in too closely is not covered

*missing rule* · minor · medium confidence · rules: no rule

15.12 says: "If a vehicle merges in front of you too closely, take your foot off the accelerator. This creates space between you and the vehicle ahead." This is how to react when a vehicle that is passing returns in front of you. The BEING group has no rule for it.

- Fix: Add PASS-BEING-09: force INSTRUCTION, modal MUST, actor DRIVER, when "a vehicle merges in front of the DRIVER too closely", action "take the foot off the accelerator to create space", vague_terms [{"term":"too closely","explanation":"no distance given"}], evidence ["15.12"].
- **Triage: ignored.** This is a general rule of the road, not specific to passing.

### S3-006. Slower-traffic keep-right rule in the same block is left out

*missing rule* · minor · low confidence · rules: PASS-BEING-04

13.144 also says: "If you choose to drive slower than other traffic, drive in the right lane", and "you should not block normal and reasonable traffic flow by driving too slowly." BEING-04 mentions the first sentence only in its note, and no rule states it. Both sentences govern letting faster traffic pass. This case is on the boundary of the topic.

- Fix: Add PASS-BEING-10: force INSTRUCTION, modal MUST, actor DRIVER, when "driving slower than other traffic on a road with more than one lane in the DRIVER's direction", action "drive in the right lane", evidence ["13.144"].
- **Triage: ignored.** This is a general rule of the road, not specific to passing (as at a0 N3).

### S3-007. Freeway five-second signal timing not used for the passing lane change

*missing citation* · minor · low confidence · rules: PASS-PROC-01

PROC-01 cites the general lane-change checklist (10.36–10.42), but not 9.35–9.36: "You should signal: … Before every lane change. At least five seconds before you change lanes on a freeway." This gives a quantified signal time for moving into the passing lane on a freeway.

- Fix: Add 9.33, 9.35 and 9.36 to PROC-01's evidence. Either add a note on the five-second freeway timing, or add a separate ADVICE rule: "WHEN about to change lanes to pass on a freeway, the PASSER SHOULD signal at least five seconds before changing lanes."
- **Triage: fixed, as a note only.** `9.33`, `9.35` and `9.36` were added to PROC-01's evidence, and its note now ends: "On a freeway, 9.36 says to signal at least five seconds before changing lanes." No separate rule was added.

## Conflicts

### S3-008. MAY ONLY pass-on-right list forbids what the light-rail rule requires

*contradiction* · major · medium confidence · rules: PASS-SIDE-01, PASS-USER-05

SIDE-01 says the PASSER "MAY ONLY pass on the right" in three cases: an open highway with two or more lanes, a left-turning driver ahead, or a one-way street. USER-05 forbids passing a LIGHT RAIL VEHICLE on the left on a two-way street unless the tracks are too close to the right. On such a street the only way to pass is on the right, which SIDE-01 forbids. Read together, the two rules leave no legal way to pass, yet 13.22 clearly contemplates passing on the right. The notes on both rules acknowledge the clash but do not resolve which rule applies.

- Fix: Add to SIDE-01's unless: "UNLESS overtaking a LIGHT RAIL VEHICLE where USER-05 requires passing on the right". Alternatively, add a fourth OR condition to SIDE-01's when: "OR the PASSER is overtaking a LIGHT RAIL VEHICLE and 13.22 does not allow passing it on the left", and cite 13.22. Update both notes to match.
- **Triage: fixed with the fourth OR condition.** SIDE-01's condition now ends "… OR the PASSER is on a one-way street OR the PASSER is overtaking a LIGHT RAIL VEHICLE", and `13.22` is cited. The proposed "and 13.22 does not allow passing it on the left" was left out, so the condition doesn't name a block id. USER-05 still forbids the left side, so together the two rules allow passing a LIGHT RAIL VEHICLE on the right. Both notes were updated to say how the rules fit together.

### S3-009. General turnout rule is labelled REQUIREMENT and makes the five-vehicle legal threshold redundant

*overlapping conditions / wrong force* · minor · medium confidence · rules: PASS-BEING-02, PASS-BEING-03

BEING-02 is labelled REQUIREMENT and applies whenever "cars are behind the DRIVER". It reaches that strength through the sign 10.66 and the general statement in 12.85. However, 10.65 is a plain command ("Merge into these areas…"), which is INSTRUCTION. The only stated legal requirement is in 10.67, with its conditions of five or more vehicles and passing being unsafe, which is BEING-03. As labelled, BEING-02 makes BEING-03's conditions irrelevant, so a reader cannot tell which threshold is the legal one. BEING-02 also cites 10.66, which BEING-03 cites too.

- Fix: Change BEING-02's force to INSTRUCTION; the modal MUST stays. Remove 12.85 from its evidence. Revise the note to say that the legal requirement, with its thresholds, is BEING-03.
- **Triage: fixed as proposed.** BEING-02 is INSTRUCTION / MUST again, `12.85` was removed from its evidence, and the note says the legal requirement with its thresholds is BEING-03. This reverses a2 S2-055.

### S3-010. Overlapping bicyclist-spacing rules

*duplicate* · minor · medium confidence · rules: PASS-USER-07, PASS-USER-09, PASS-USER-19

USER-19 ("leave space between the vehicle and the BICYCLIST") comes from the last sentence of 13.110, the same block as USER-07. USER-09 ("give the BICYCLIST enough space…") repeats the same obligation with an added purpose. Three rules split one instruction at different levels of detail.

- Fix: Merge USER-19 into USER-09. The merged action reads "leave enough space between the vehicle and the BICYCLIST so the BICYCLIST is not forced into parked vehicles or open vehicle doors". The merged evidence is ["13.110","13.111","13.112","13.113","13.114","13.115","13.116"]. Update the cross-references in USER-07 and USER-08.
- **Triage: ignored.** Already triaged: the leave-space duty was split into USER-19 at a2 S2-036.

## Other

### S3-011. Inconsistent actor and naming for the same roles

*inconsistent terms* · minor · medium confidence · rules: PASS-MARK-01, PASS-LOC-04, PASS-LOC-05, PASS-LOC-06, PASS-LOC-01, PASS-LOC-02, PASS-USER-04, PASS-USER-05

Rules that forbid passing in a given place use DRIVER in some cases (MARK-01, LOC-04, LOC-05, LOC-06) and PASSER in others (LOC-01, LOC-02). Streetcars appear in two ways: USER-05 counts them as a LIGHT RAIL VEHICLE (the vocabulary says "such as a light rail train or streetcar"), while USER-04 names "a bus, streetcar, or trolley" without the term. GEN-04 also uses PASSER ("the driver making a PASS") for someone who is only "considering a PASS".

- Fix: Use PASSER consistently in all prohibitions on passing, or redefine PASSER as "a driver making or intending to make a PASS". In USER-04, either write "bus, LIGHT RAIL VEHICLE, or trolley" or narrow the LIGHT RAIL VEHICLE definition.
- **Triage: fixed (partly).** USER-04's condition is now "a bus or LIGHT RAIL VEHICLE is stopped at a SAFETY ZONE or traffic light". The LIGHT RAIL VEHICLE definition now names trolleys among its examples ("such as a light rail train, streetcar or trolley"), so USER-04 still covers them. The PASSER vs DRIVER inconsistency and GEN-04's use of PASSER are ignored.
