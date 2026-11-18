# Aggregate check (stage 3): gold_set\mto\overtaking\b2_atomic.json

Judge: anthropic/claude-opus-5-5 · run folder: `runs\20261117-232954-check-aggregate-overtaking-b3` (request, response, findings.jsonl, triage.csv) · 74 rules, whole corpus · $0.9583

**8 findings** (3 major, 5 minor): 3 coverage, 5 conflict, 0 other.

**Triage:** all 8 findings were triaged, and the proposed decisions were accepted as written. Fixes were applied to `b3_aggregate.json`, which started as an exact copy of `b2_atomic.json`. Each decision is recorded under its finding as a **Triage** line.
- Rules changed: PROC-01, GEN-05, SIDE-01, NIGHT-01 and USER-04. Changed statements were rebuilt from their fields.
- Rule added: PASS-USER-24 (S3-005), at the end of the USER group. No rules were renumbered, and rule ids are those of `b2_atomic.json`.
- After all fixes there are 75 rules and 20 vocabulary terms. Stage 1 on `b3_aggregate.json` passes all 8 checks with no format errors.

## Coverage

### S3-001. Checking the blind spot for vehicles that may overtake you is not covered

*missing rule* · major · medium confidence · rules: no rule

The set has no rule telling the driver who may be overtaken to check for overtaking traffic. 29.44: "If it is possible for another vehicle to overtake you while you are turning, check your blind spot before starting to turn." 29.171: "If there is a chance of traffic or pedestrians overtaking you on the right, check your right blind spot just before pulling over." Both are plain commands about being passed. They sit in the road-test chapter, so this is on the boundary of the topic.

- Fix: Add PASS-BEING-08: force INSTRUCTION, modal MUST, actor DRIVER, when "about to turn OR about to pull over to the right AND another vehicle or a pedestrian may be overtaking the DRIVER", action "check the BLIND SPOT on the side of the possible overtaking before starting the manoeuvre", unless "", vague_terms [{"term":"may be overtaking","explanation":"no criteria given"}], evidence ["29.44","29.171"].
- **Triage: rejected, no change.** The same finding was ignored in a0 M9.3 and in S3-001 (a3). These are general cautions about turning or pulling over while another vehicle might overtake, and the BEING group covers only a pass that is actually happening or wanted (allow list, Scope).

### S3-002. Ban on moving up beside a turning large vehicle is not covered

*missing rule* · minor · low confidence · rules: no rule

6.57: "If a large vehicle in front of you is making a right turn, do not move up into the space that opens up in the right lane … Stay well back until the truck has completely cleared the lane." 6.58 gives the same instruction for left turns on two-lane off-ramps. Moving up beside a turning truck amounts to overtaking it, so this is on the boundary of the topic.

- Fix: If it is treated as in scope, add PASS-USER-24: force INSTRUCTION, modal MUST NOT, actor DRIVER, when "a LARGE VEHICLE in front is making a turn and swings wide", action "move up into the space that opens beside it", evidence ["6.57","6.58"], note "Stay well back until the truck has cleared the turn."
- **Triage: rejected, no change.** The same finding was ignored in S3-004 (a3): moving alongside a turning large vehicle is not overtaking it (allow list, Scope).

### S3-003. Other passages that support the passing-procedure rules are not cited

*missing citation* · minor · medium confidence · rules: PASS-PROC-01, PASS-PROC-06

PASS-PROC-01 takes its mirror and blind-spot checks for daytime passing from the night-passing steps (10.31) alone. The general duties are stated in 10.7 ("Check your blind spot by looking over your shoulder in the direction of the lane change") and 16.40 ("Always check your blind spot … before you change lanes"). PASS-PROC-06 (do not cut off the passed vehicle) does not cite 23.23, which lists "intentionally cutting off another vehicle" among sanctioned aggressive behaviours, or 12.23: "It is dangerous and illegal … to cut in front of a faster moving vehicle".

- Fix: Add 10.7 and 16.40 to the evidence of PASS-PROC-01 and update its note. Add 23.23 and 12.23 to the evidence of PASS-PROC-06, and note that the handbook treats cutting off as illegal or sanctioned behaviour.
- **Triage: partly fixed: PROC-01 only.**
  - **PROC-01: fix.** 10.7 and 16.40 are general (not night-only) sources for the mirror and blind-spot check, which supports the a0 M2 reviewer decision with handbook text (error set: supporting block not cited). 10.6 ("Check your mirrors for a space in traffic") supports the mirror check too. Each is a list item, so its list intro is cited with it: 10.5 ("Here are the steps for making a lane change:") and 16.31 ("10 ways you can help make Ontario's roads the safest in North America"). PROC-01 evidence: `["10.5", "10.6", "10.7", "10.16", "10.17", "10.29", "10.31", "16.31", "16.40"]`. Note: "A PASS is a lane change, and the lane-change steps (10.6, 10.7) and 16.40 ('Always check your blind spot: look in your mirror and over your shoulder before you change lanes') give the mirror and blind-spot checks for every lane change; the night-passing steps (10.31) repeat them."
  - **PROC-06: rejected, no change.** Settled in a0 M8 and S3-003 (a3): 12.23's "illegal" covers a slower vehicle cutting in front of a faster one, and 23.23 lists aggressive driving, not a passing rule (allow list, Strength).

## Conflicts

### S3-004. On a multi-lane freeway one rule requires passing in the far left lane while another allows passing on the right

*contradiction* · major · medium confidence · rules: PASS-GEN-05, PASS-SIDE-01

PASS-GEN-05 says: "WHEN driving on a multi-lane FREEWAY AND passing traffic moving slower than the speed limit, the DRIVER MUST use the far left lane". PASS-SIDE-01 says: "WHEN on a multi-lane road … the DRIVER MAY pass on the right". A multi-lane freeway is a multi-lane road, so a driver passing a slow vehicle there is both required to use the far left lane and allowed to pass on the right. The handbook supports both passages: 12.24: "Use the far left lane of a multi-lane freeway to pass traffic moving slower than the speed limit, but don't stay there" and 10.40: "You may pass on the right on multi-lane or one-way roads". Neither rule says which one takes precedence. GEN-05 also turns a lane-use instruction into an absolute obligation, which leaves no room for the passing-on-right permission.

- Fix: Reword PASS-GEN-05 so that its main point is that the far left lane is for passing and the driver must not stay in it. Set action to "use the far left lane only for passing traffic moving slower than the speed limit, and not stay there". Add a note: "10.40 still permits passing on the right on multi-lane roads (PASS-SIDE-01); 12.24 tells drivers to use the far left lane to pass and not to stay there." Add a matching cross-reference note to PASS-SIDE-01.
- **Triage: partly fixed: cross-reference notes only, no "only".** The handbook states both passages (12.24, 10.40) and does not say how they relate, so the set should link them (error set: a permission that overlaps restrictions elsewhere without saying so, S3-008). The proposed "use the far left lane only for passing" adds the "only" that a0 G3 removed, so it is left out (allow list: re-raising a settled triage). GEN-05's wording from b2 S2-004 stays.
  - Add to GEN-05's note: "10.40 also permits passing on the right on multi-lane roads (PASS-SIDE-01); the handbook does not say how the two passages relate."
  - Add to SIDE-01's note: "On a multi-lane FREEWAY, 12.24 tells the DRIVER to use the far left lane to pass traffic moving slower than the speed limit (PASS-GEN-05)."

### S3-005. Absolute duty to change lanes when passing cyclists contradicts the softer 'whenever possible' wording and the same-lane one-metre rule

*inconsistent strength* · major · medium confidence · rules: PASS-USER-04, PASS-USER-01

PASS-USER-04 says the DRIVER "MUST pass by changing lanes, not within the same lane" when passing a bicycle, and gives no exception. For cyclists specifically, the handbook words this as conditional advice. 6.32: "Whenever possible, you should change lanes to pass." The same block (6.32) also sets the rule for passing within the lane: "maintain a minimum distance of one metre, where practical". PASS-USER-01 restates that rule, and it only makes sense if same-lane passing of a cyclist is sometimes allowed. Recording 10.24's command as unconditional for bicycles drops the 'whenever possible' condition and makes PASS-USER-01 nearly empty.

- Fix: Narrow PASS-USER-04 to what 10.24 addresses: a rider who has pulled to one side of the lane is not an invitation to pass in the same lane. Set when to "a motorcycle, bicycle, limited-speed motorcycle or moped has pulled to the left or right side of its lane AND the DRIVER wants to pass it". Add a separate ADVICE rule: "WHEN passing a CYCLIST, the DRIVER SHOULD change lanes to pass, UNLESS changing lanes is not possible." with evidence ["6.32"]. Cross-reference both rules to PASS-USER-01.
- **Triage: fix as proposed (reverses b0 m1; your call).** b2 S2-037 rejected the same objection because the note quoted 6.32. This finding brings new evidence: the fix that b0 m1 lacked. 10.24's command is about riders who have moved to one side of their lane, so USER-04's unconditional condition is broader than the handbook's context (error set, S2-009). Once USER-04 is narrowed, it no longer overlaps the 6.32 advice, so the merge reason from b0 m1 (duplicate rules at different strengths) goes away.
  - **USER-04**: when: "a motorcycle, bicycle, limited-speed motorcycle or moped has pulled to the left or right side of its lane AND the DRIVER wants to pass it"; action unchanged. Statement: "WHEN a motorcycle, bicycle, limited-speed motorcycle or moped has pulled to the left or right side of its lane AND the DRIVER wants to pass it, the DRIVER MUST pass by changing lanes, not within the same lane." Evidence: `["10.24", "10.27"]` (6.32 removed). Note: "These riders often move to one side of their lane for road conditions or visibility; the handbook says this is not an invitation to pass in the same lane. Passing cyclists in general is PASS-USER-24; the one-metre gap is PASS-USER-01."
  - **New PASS-USER-24**, "Change lanes to pass cyclists", at the end of the USER group so nothing is renumbered (rule order within a group is not an error). It is old USER-02 restored: "WHEN passing a CYCLIST AND it is possible to change lanes, the DRIVER SHOULD change lanes to pass." ADVICE / SHOULD, evidence `["6.32", "10.27"]`, vague term "it is possible to change lanes" (does not say when a lane change is possible). Note: "Diagram 2-47 shows a car moving into the next lane to pass a cyclist in a sharrow lane. When a rider has pulled to one side of the lane, PASS-USER-04 applies; the one-metre gap is PASS-USER-01."

### S3-006. Vocabulary term PASS (a lane change) is used for manoeuvres that are not lane changes

*inconsistent terms* · minor · medium confidence · rules: PASS-LOC-07, PASS-LOC-08, PASS-SIDE-01, PASS-SIGN-05, PASS-USER-15, PASS-USER-17, PASS-USER-21, PASS-USER-23

The vocabulary defines PASS as "Changing lanes to move past a slower vehicle", and the note to PASS-LOC-08 relies on that: "since a PASS is a lane change". Several rules, though, use pass or passing to mean moving past something without a lane change, or past things that are not slower vehicles: driving on the paved right shoulder (LOC-07); passing on the right in the driver's own lane (SIDE-01 note: "Passing on the right while staying in the DRIVER's lane … is not a lane change"); passing a roadside hazard (SIGN-05); parked vehicles (USER-15); streetcar passenger areas (USER-17); workers (USER-21); animals (USER-23). As a result the scope of rules that use the term PASS, such as GEN-01, GEN-03 and PROC-03, is unclear.

- Fix: Keep PASS for the defined manoeuvre. Write the other rules in lower-case plain language, for example "drive past", and add a note to the vocabulary entry: "Rules that say 'pass' in lower case include moving past vehicles or hazards without a lane change." Alternatively, widen the definition and drop the inference in the PASS-LOC-08 note.
- **Triage: rejected, no change.** The same finding was ignored in S3-010 (a3). A definition is not stretched to cover every use (allow list, Vocabulary), and lowercase "pass" is allowed (allow list, Writing and grammar). The LOC-08 note's reading holds for the defined manoeuvre.

### S3-007. The passing exception to the 60-metre low-beam rule overlaps the duty to use low beams while approaching to pass

*overlapping conditions* · minor · medium confidence · rules: PASS-NIGHT-01, PASS-NIGHT-03

PASS-NIGHT-01 waives low beams within 60 metres of a vehicle ahead "UNLESS the DRIVER is passing that vehicle". PASS-NIGHT-03 requires low beams while "approaching the vehicle to be passed from behind". A driver closing in on a vehicle in order to pass it may count as "passing" under NIGHT-01, which would exempt the driver from the low-beam duty that NIGHT-03 imposes. 10.30 and 10.31 show that the exception should apply only once the driver is alongside.

- Fix: Change the unless of PASS-NIGHT-01 to "the DRIVER has pulled out and is alongside the vehicle being passed". Add a note that cross-references PASS-NIGHT-03 and PASS-NIGHT-04.
- **Triage: fix, worded to match NIGHT-04, with the reading recorded.** One rule could exempt what another requires in the same situation (error set: conflicts between rules).
  - unless: "the DRIVER has pulled out and is moving alongside the vehicle being passed". Statement: "WHEN using headlights AND less than 60 metres behind another vehicle, the DRIVER MUST use low-beam headlights, UNLESS the DRIVER has pulled out and is moving alongside the vehicle being passed."
  - Evidence: add 10.29, 10.30 and 10.31, since the narrower reading rests on the night-passing steps (10.29 is their list intro): `["4.65", "10.29", "10.30", "10.31", "14.8", "22.96", "22.134", "22.135"]`.
  - Add to the note: "4.65 says 'unless you are passing it'; read, from the night-passing steps (10.30, 10.31), as starting once the DRIVER is alongside. While approaching to pass, low beams are required (PASS-NIGHT-03); high beams come on alongside (PASS-NIGHT-04)."

### S3-008. The intersection lane-change ban is spread over three rules, with a misattributed citation

*duplicate* · minor · medium confidence · rules: PASS-LOC-08, PASS-SIDE-01, PASS-SIDE-04

PASS-LOC-08 bans changing lanes to pass in or near an intersection. PASS-SIDE-01 repeats the same ban as its unless clause, "doing so requires changing lanes in or near an intersection", even though 10.40, its source, states no such exception. PASS-SIDE-04 cites 10.11, but its content ("slow down or stop instead of pulling out to go around") comes only from 29.104.

- Fix: Remove the unless clause and the 10.11 citation from PASS-SIDE-01, and keep a note pointing to PASS-LOC-08. Remove 10.11 from the evidence of PASS-SIDE-04.
- **Triage: partly fixed: SIDE-01 only.**
  - **SIDE-01: fix.** Since b0 m6 added LOC-08, SIDE-01's exception repeats it (error set: overlapping rules → merge). Removing it keeps the substance in LOC-08, and it also settles b2 S2-031's point that 10.40 states the permission without an exception. unless: ""; statement: "WHEN on a multi-lane road OR on a one-way road OR overtaking a STREETCAR OR overtaking a left-turning vehicle, the DRIVER MAY pass on the right."; evidence: `["10.40"]`; vague term "near an intersection" removed. Note (with the S3-004 sentence): "The handbook adds that most passing is done on the left and that passing on the right can be more dangerous. PASS-SIDE-02 and PASS-LOC-07 restrict this permission. Changing lanes to pass in or near an intersection is banned by PASS-LOC-08; going around a vehicle that blocks the lane in an intersection is PASS-SIDE-04. On a multi-lane FREEWAY, 12.24 tells the DRIVER to use the far left lane to pass traffic moving slower than the speed limit (PASS-GEN-05)."
  - **SIDE-04: rejected, no change.** 10.11 was added in S3-008 (a3) on purpose, and b2 S2-035 kept it: pulling out to go around the vehicle is a lane change in the intersection, which 10.11 bans.
