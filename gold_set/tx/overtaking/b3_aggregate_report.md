# Aggregate check (stage 3): gold_set/tx/overtaking/b2_atomic.json

Judge: anthropic/claude-opus-5-5 · run folder: `runs\20261122-000000-check-aggregate-overtaking-b3` (request, response, findings.jsonl, triage.csv) · 58 rules, whole corpus · $0.8787

**8 findings** (2 major, 6 minor): 3 coverage, 3 conflict, 2 other.

**Triage:** all 8 findings were triaged, and fixes were applied to `b3_aggregate.json`, which started as an exact copy of `b2_atomic.json`. Each decision is recorded under its finding as a **Triage** line. The decisions follow the rulings from the a0–a3 and b0–b2 triages.
- Rule changed: BEING-10 (S3-006). Its statement was rebuilt from its fields.
- No rule was added, merged or renumbered, and rule ids are those of `b2_atomic.json`.
- The other 7 findings repeat decisions already made and were rejected.
- After all fixes there are 58 rules and 16 vocabulary terms. Stage 1 on `b3_aggregate.json` passes all 8 checks with no format errors.

## Coverage

### S3-001. Blocking another vehicle from passing is also illegal racing; the stronger wording and penalty are missed

*missing citation / strength* · major · medium confidence · rules: PASS-BEING-08

PASS-BEING-08 rests only on the road-rage tip 15.79, and its note says "Given as a tip to avoid road rage." The glossary defines a race to include using a vehicle to try to stop another from passing: 16.125: "race – the use of one or more vehicles in an attempt to: Out gain or outdistance another vehicle or prevent another vehicle from passing". 9.37–9.38 say "A person may not participate in: A race", and 9.43 gives the penalty: "The criminal penalty for a conviction of Speed Racing ranges from a Class B misdemeanor to a second-degree felony." The extractor's instructions say to record the stronger wording and the penalty.

- Fix: Change force to REQUIREMENT (modal stays MUST NOT). Set penalty to "Class B misdemeanor up to second-degree felony (racing)". Add evidence 16.125, 16.126, 9.37, 9.38 and 9.43. Set note to: "Stated as a road-rage tip (15.79); trying to prevent another vehicle from passing is also part of the definition of a race (16.125), which is prohibited (9.37) with the penalty in 9.43."
- **Triage: rejected, no change.** The same finding was rejected in a0 F1: the racing law covers a different, wider situation and reaches BEING-08 only through the glossary's definition of a race (allow list, Strength). The penalty in 9.43 belongs to that law, so it does not change the decision.

### S3-002. No rule bars passing across solid lane lines or double solid white lines

*missing rule* · major · medium confidence · rules: PASS-MARK-02, PASS-MARK-03

7.17/7.19: "Never drive on the left side of the road when: Pavement markings or signs prohibit driving on the left (a 'No Passing Zone' or solid lane lines)". 6.211: "Crossing is prohibited where there is a pavement marking of double solid white lines." 6.139 (DO NOT CROSS DOUBLE WHITE LINE sign): "Drivers should not change lanes or turn across the double white lines." 6.209: "Crossing a solid white line should be avoided if possible." The set covers only solid yellow center lines on two-lane roads (PASS-MARK-02) and double yellow lines on multi-lane highways (PASS-MARK-03). Nothing stops a PASSER from changing lanes across a double white line to pass.

- Fix: Add PASS-MARK-04 "Do not cross double solid white lines": force REQUIREMENT, modal MUST NOT, actor DRIVER, when "the lane line is a pair of solid white lines", action "cross it, including to pass or change lanes", unless "", evidence ["6.211","6.212","6.139","6.139-f1","7.19"]. Add PASS-MARK-05: force ADVICE, modal SHOULD NOT, actor DRIVER, when "the line is a solid white line", action "cross it to pass", unless "crossing cannot be avoided", vague term "cannot be avoided", evidence ["6.209"].
- **Triage: rejected, no change.** The same finding was rejected in a0 M6.6 and S3-002 (a3). Markings that ban crossing in general, without mentioning passing, are out of scope, and in 7.19 the solid lane lines are center lines, which MARK-02 and MARK-03 cover (allow list, Scope).

### S3-003. Slower-traffic-keep-right rules, which make room for passing, are not captured

*missing rule* · minor · low confidence · rules: PASS-GEN-08, PASS-BEING-09

6.130 (regulatory SLOWER TRAFFIC KEEP RIGHT sign): "Stay in the right-hand lane if you are driving slower than other vehicles on the road." 6.197: "If you are driving slower, keep in the right-hand lane." 10.22: "Use the right lane to drive at the minimum posted speed limit or below the normal flow of traffic." These complement PASS-GEN-08 and PASS-BEING-09, which deal with leaving room for faster traffic to pass, but no rule states them. This is at the edge of the topic.

- Fix: Add PASS-BEING-11: force REQUIREMENT, modal MUST, actor DRIVER, when "driving slower than other vehicles AND a 'Slower Traffic Keep Right' sign is posted", action "stay in the right-hand lane", unless "passing", evidence ["6.130","6.130-f1","6.115"]. Add PASS-BEING-12: force INSTRUCTION, modal MUST, actor DRIVER, when "driving slower than other traffic on a multi-lane road", action "keep in the right-hand lane", unless "", evidence ["6.197","10.22"].
- **Triage: rejected, no change.** The same finding was ignored in S3-001 (a3), and the lane-choice part of 10.23 in S2-011 (a2): lane choice by speed that does not mention passing is out of scope (allow list, Scope).

## Conflicts

### S3-004. Freeway passing: one rule requires the left or middle lane while another allows passing on the right

*contradiction* · minor · medium confidence · rules: PASS-GEN-09, PASS-SIDE-01

PASS-GEN-09 says "WHEN passing other vehicles on a multi-lane FREEWAY, the PASSER MUST use the middle or left lane." PASS-SIDE-01 lets the PASSER pass on the right in a traffic lane when "the road is … wide enough for two or more lanes in each direction". Every multi-lane freeway meets that condition. On a freeway, one rule forbids passing on the right and the other allows it. Both notes admit "the handbook does not say which applies", but the clash is left in the ground truth. 10.23 is lane-choice advice: "Use the middle or left lane if you are traveling faster than other traffic or passing other vehicles." It is not a ban on right-side passing, and 7.42–7.43 allow passing on the right.

- Fix: Narrow PASS-GEN-09 so it states lane choice and does not forbid passing on the right. Set when: "traveling faster than other traffic or passing other vehicles on a multi-lane FREEWAY" and action: "use the middle or left lane". Add a note to both rules: "10.23 sets the normal lane for faster traffic; it does not withdraw the right-side passing permission of 7.42–7.43." Then remove the unresolved "does not say which applies" wording from both notes.
- **Triage: rejected, no change.** Settled in a0 M5 and S3-005 (a3). 10.23 is an imperative ("Use the middle or left lane"), so GEN-09 is an INSTRUCTION (allow list, Strength), and the handbook does not say how it relates to 7.42–7.43; the notes of both rules link them (allow list, Tensions the handbook leaves open). The finding gives no new evidence.

### S3-005. Penalty for disobeying a warning sign is recorded for one sign rule but left out of the other

*inconsistent penalty* · minor · high confidence · rules: PASS-SIGN-01, PASS-SIGN-02

PASS-SIGN-02 records "A fine of $1 to $200, doubled in a work zone with workers present" from 6.266–6.267 for disobeying warning signs. PASS-SIGN-01's note says the 'No Passing Zone' pennant "is a warning sign; disobeying it is a violation with a fine of $1 to $200 (6.266, 6.267)". Yet its penalty field is "" and it does not cite 6.266 or 6.267.

- Fix: In PASS-SIGN-01, set penalty to "For the warning pennant: a fine of $1 to $200, doubled in a work zone with workers present." Add 6.266 and 6.267 to its evidence.
- **Triage: rejected, no change.** Settled in a0 M4, S2-035 (a2) and S3-008 (a3): SIGN-01 also covers the 'Do Not Pass' sign, which has no stated penalty, so the penalty stays empty and the note gives the pennant's fine (allow list, Penalties).

### S3-006. The same actor is named two different ways

*inconsistent terms* · minor · high confidence · rules: PASS-BEING-07, PASS-BEING-10

PASS-BEING-07 uses actor "DRIVER of a TRUCK" and PASS-BEING-10 uses "DRIVER of the TRUCK" for the same class of actor. PASS-BEING-10's condition also repeats "the DRIVER of a TRUCK".

- Fix: Use "DRIVER of a TRUCK" in both. Reword PASS-BEING-10's when to "having passed another vehicle AND returning to that vehicle's lane".
- **Triage: fixed as proposed.** BEING-10's actor is now "DRIVER of a TRUCK", as in BEING-07, and its condition no longer repeats the actor. when: "having passed another vehicle AND returning to that vehicle's lane"; statement: "WHEN having passed another vehicle AND returning to that vehicle's lane, the DRIVER of a TRUCK SHOULD signal." Evidence and note are unchanged.

## Other

### S3-007. Rules about steering around islands and barricades are included as overtaking rules

*off-topic* · minor · medium confidence · rules: PASS-SIGN-03, PASS-SIGN-04

PASS-SIGN-03 rests on 6.98: "traffic is permitted to pass on either side of a traffic island or an obstruction". PASS-SIGN-04 rests on 6.243–6.248: "Stripes sloping downward to the right means the driver should bear to the right." In both, 'pass' means going around a fixed object, not overtaking another vehicle. PASS is defined as "Moving past the vehicle ahead; overtaking". These rules fall outside the topic and use the word in a different sense from the vocabulary.

- Fix: Remove PASS-SIGN-03 and PASS-SIGN-04 from the overtaking set; they belong in a signs or lane-guidance set. If they are kept, rewrite the actions with "go around" or "bear" instead of "pass" so that the PASS term is not overloaded.
- **Triage: rejected, no change.** Settled in a0 M6.3 and M6.4, S2-040 and S2-043 (a2), S3-007 (a3), and b2 S2-031 and S2-032: passing a hazard other than a vehicle is in scope (allow list, Scope). SIGN-04's action already says "bear". SIGN-03's "pass on either side of the traffic island or obstruction" is 6.98's wording and names the object (S2-041 (a2); allow list: a lowercase phrase that means something else).

### S3-008. Move-over rules apply conditions from the emergency-vehicle passage to every service vehicle and misstate the 20 mph wording

*overgeneralization* · minor · medium confidence · rules: PASS-USER-15, PASS-USER-16

Both rules apply the officer exception and the under-25-mph limit to every SERVICE VEHICLE. These come from 5.68–5.71, which concern only "a stopped emergency vehicle with its lights activated". 9.29–9.31, which list tow, utility and TxDOT vehicles, have neither condition. The notes admit this ("Both are applied here to every SERVICE VEHICLE"). The rules also say "reduce speed to 20 mph below the posted speed limit", but 5.70 says "Slow to a speed not more than 20 mph less than the posted speed limit when the posted speed limit is 25 mph or more", which reads differently. The 25-mph threshold is dropped. The material is also only at the edge of the topic, being about driving past a stopped vehicle.

- Fix: Split the rules by source vehicle class. One pair for emergency vehicles cites 5.68–5.71, keeps the officer exception, and states the speed limits as worded: not more than 20 mph below when the limit is 25 mph or more, less than 5 mph when the limit is under 25 mph. One pair for the 9.29 vehicles cites 9.29–9.31 only and uses "reduce speed to 20 mph below the speed limit", with no officer exception. Note that 9.31 leaves utility vehicles out of the move-over choice.
- **Triage: rejected, no change.** Settled in a0 M6.1 and S2-071, S2-073, S2-076 and S2-077 (a2): the two passages are combined into one duty, split by lane count, and the notes say that the officer exception and the under-25-mph case are applied to every SERVICE VEHICLE. The 25 mph threshold is in the action ("where the posted speed limit is less than 25 mph"), and the 20 mph wording follows 9.30 (b2 S2-056, S2-058).
