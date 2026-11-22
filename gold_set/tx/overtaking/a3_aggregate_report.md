# Aggregate check (stage 3): gold_set/tx/overtaking/a2_atomic.json

Judge: anthropic/claude-opus-5-5 · run folder: `runs\20261121-222855-check-aggregate-overtaking-a3` (request, response, findings.jsonl, triage.csv) · 58 rules, whole corpus · $0.8859

**10 findings** (2 major, 8 minor): 3 coverage, 3 conflict, 4 other.

**Triage:** all 10 findings were triaged, and fixes were applied to `a3_aggregate.json`, which started as an exact copy of `a2_atomic.json`. Each decision is recorded under its finding as a **Triage** line. The decisions follow the rulings from the a0, a1 and a2 triages.
- 2 findings were fixed, one of them in a changed form. 1 rule (PASS-SIDE-01) and 1 vocabulary entry (SERVICE VEHICLE) changed, and the rule's statement was rebuilt from its fields. The other 8 were found not to be errors, or were rejected or ignored.
- Four findings repeated decisions already made:
  - SIGN-03 and SIGN-04 are in scope (a0 M6.3, M6.4; a2 S2-040, S2-043);
  - SIGN-01's penalty stays empty (a0 M4; a2 S2-035);
  - "passing a warning sign" stays (a0 G4; a2 S2-038);
  - GEN-09 and SIDE-01 are linked only by their notes on a FREEWAY (a0 M5).
- One earlier decision was reversed on new evidence: SERVICE VEHICLE now cites 9.29, as FREEWAY cites 10.13 (S3-010; it reverses a2 S2-072 and S2-078).
- Two missing-rule findings were out of scope by the a0 M6.5/M6.6 test: slower traffic keeping right, and double white lines.
- No rule was added, removed or renumbered. After all fixes there are 58 rules and 16 vocabulary terms. Stage 1 on `a3_aggregate.json` passes all 8 checks with no format errors.

## Coverage

### S3-001. Slower-traffic-keep-right rules that make room for passing are missing

*missing rule* · minor · low confidence · rules: PASS-GEN-08, PASS-BEING-09

Several passages tell slower drivers to keep right so that faster traffic can pass: 6.130 (sign "SLOWER TRAFFIC KEEP RIGHT"): "Stay in the right-hand lane if you are driving slower than other vehicles on the road."; 6.197: "If you are driving slower, keep in the right-hand lane."; 10.22: "Use the right lane to drive at the minimum posted speed limit or below the normal flow of traffic." The set covers the 'Left Lane for Passing Only' sign (GEN-08) and being ready to move over (BEING-09), but not this regulatory sign or the instruction. This is on the boundary of the topic (lane use that supports being passed).

- Fix: Add PASS-BEING-11: force REQUIREMENT, modal MUST, actor DRIVER, when "on a road with more than one lane in the DRIVER's direction AND the DRIVER is driving slower than other traffic", action "stay in the right-hand lane", unless "". Evidence: 6.130, 6.130-f1, 6.197, 10.22, 6.115. Note that the sign is regulatory (6.115).
- **Triage: ignored, no change.** 6.130, 6.197 and 10.22 say which lane slower traffic should use, and none of them mentions passing. By the test used in a0 M6.5 and M6.6, they belong to the all-rules scope, as 10.23's faster-traffic case did in a2 (S2-011). GEN-08 is in scope because 6.148 says "The farthest left lane is for passing only", and BEING-09 because 10.34 says "to allow faster traffic to pass".

### S3-002. 'Solid lane lines' as a bar on driving left to pass is not captured

*missing condition* · minor · medium confidence · rules: PASS-MARK-02, PASS-LOC-01

7.19 bans driving on the left when "Pavement markings or signs prohibit driving on the left (a 'No Passing Zone' or solid lane lines)". The set only covers a solid yellow center line on a two-lane road (MARK-02) and a double yellow line on multi-lane highways (MARK-03). The handbook also says 6.211: "Crossing is prohibited where there is a pavement marking of double solid white lines" and 6.139: "Drivers should not change lanes … across the double white lines." No rule says a driver must not cross solid lane lines to pass.

- Fix: Add PASS-MARK-04: force REQUIREMENT, modal MUST NOT, actor PASSER, when "the lane line the PASSER would cross is a solid line or double solid white lines", action "cross it to pass". Evidence: 7.17, 7.19, 6.211, 6.212, 6.139, 6.139-f1.
- **Triage: not an error, no change.** In 7.19, "solid lane lines" are lines that forbid driving on the left side of the road, i.e. center lines. MARK-02 (which cites 7.19) and MARK-03 cover them. The double solid white lines of 6.211 and 6.139 separate lanes going the same way (diagram 6.212 shows a ramp lane), and neither block mentions passing. Like the left-edge line of 6.209 (a0 M6.6), they belong to the all-rules scope.

### S3-003. Downgrade advice to increase speed when passing a truck is only in a note

*missing rule* · minor · low confidence · rules: PASS-USER-06

10.113: "On a downgrade, the truck's momentum causes the truck to go faster so you may need to increase your speed." This is a situational permission or advice for the PASSER. It appears only as context in PASS-USER-06's note, not as a rule.

- Fix: Add PASS-USER-18: force PERMISSION, modal MAY, actor PASSER, when "passing a TRUCK on a downgrade", action "increase speed to complete the PASS", unless "". Evidence: ["10.113"]. Note: on an upgrade the truck often loses speed, so it is easier to pass.
- **Triage: not an error, no change.** "You may need to increase your speed" says what passing a truck on a downgrade may take. It is not worded as a permission or as advice. It stays as context in USER-06's note.

## Conflicts

### S3-004. MAY ONLY on right-side passing forbids the shoulder passing that SIDE-02 allows

*contradiction* · major · high confidence · rules: PASS-SIDE-01, PASS-SIDE-02

PASS-SIDE-01 is worded as MAY ONLY: passing on the right is allowed only when "the road is one-way or is both clear of parked vehicles … and wide enough for two or more lanes in each direction". Passing on a paved shoulder is passing on the right. PASS-SIDE-02 then allows it "WHEN … the vehicle being passed is slowing or stopped …, disabled, or preparing to make a left turn", with no road-width condition. On a two-lane road with a paved shoulder, SIDE-01 forbids the move and SIDE-02 allows it. In the handbook, 7.45 is one of three alternative cases under 7.42 ("you can pass on the right only when conditions permit…"), so the shoulder case is a third permitted case, not a separate rule that overrides the first two. The MAY ONLY statements also read badly. "the PASSER MAY ONLY pass on the right" and "MAY ONLY pass on a paved shoulder" can be read as banning passing on the left, which the notes then have to deny.

- Fix: Merge into one rule. PASS-SIDE-01: modal MAY ONLY, action "pass on the right", when "conditions permit doing so safely AND (the road is clear of parked vehicles and other lane obstructions and wide enough for two or more lanes in each direction OR the road is one-way OR the PASSER uses a paved shoulder and the vehicle being passed is slowing or stopped on the main traveled portion of the HIGHWAY, disabled, or preparing to make a left turn)". Cite 7.42–7.45 and delete PASS-SIDE-02. Alternatively, keep SIDE-02 and add its case to SIDE-01's condition as an OR.
- **Triage: partly fixed: SIDE-01 was narrowed to passing in a traffic lane, instead of merging.**
  - The conflict is real. As written, SIDE-01's MAY ONLY allows passing on the right only on a one-way or wide road. That forbids the shoulder pass on a two-lane road that SIDE-02 allows. SIDE-01's note calls the shoulder "a separate permission", but the rule itself does not.
  - In 7.42–7.45, the cases in 7.43 and 7.44 are passes in a traffic lane ("wide enough for two or more lanes"), and 7.45 is the shoulder case. Limiting SIDE-01's action to a traffic lane means the two rules cover different moves. Both stay MAY ONLY (a0 G3), and no ids change.
  - **PASS-SIDE-01:**
    - title: "When passing on the right in a lane is allowed";
    - action: "pass on the right in a traffic lane" ("traffic lanes" is 7.20's word);
    - statement: "WHEN conditions permit doing so safely AND the road is one-way or is both clear of parked vehicles and other lane obstructions and wide enough for two or more lanes in each direction, the PASSER MAY ONLY pass on the right in a traffic lane.";
    - note: "Passing on a paved shoulder is a separate permission (PASS-SIDE-02), so this rule covers passing on the right in a traffic lane. MAY ONLY means passing on the right in a traffic lane is allowed only in these conditions; it does not forbid passing on the left. On a multi-lane FREEWAY, PASS-GEN-09 tells the PASSER to use the middle or left lane (10.23)."
  - The point that MAY ONLY can be read as banning passing on the left was settled in a0 G3. Both notes give the reading.

### S3-005. Freeway passing: one rule requires the left or middle lane, another allows passing on the right

*contradiction* · major · medium confidence · rules: PASS-GEN-09, PASS-SIDE-01

PASS-GEN-09 says "WHEN passing other vehicles on a multi-lane FREEWAY, the PASSER MUST use the middle or left lane." PASS-SIDE-01 allows passing on the right on any road "wide enough for two or more lanes in each direction", and a multi-lane freeway is such a road. Both notes admit the clash, but the set gives a driving model two incompatible answers for the same situation. 10.23 ("Use the middle or left lane if you are traveling faster than other traffic or passing other vehicles") is lane-choice guidance. 7.42 is a legal permission ("you can pass on the right only when conditions permit").

- Fix: Make the relation explicit. Either add to PASS-GEN-09 the exception "UNLESS the conditions of PASS-SIDE-01 for passing on the right are met", or add to PASS-SIDE-01's note that on a FREEWAY the middle or left lane is the default passing lane (PASS-GEN-09) and passing on the right is a permission, not the norm. Consider whether 10.23 is better recorded as ADVICE-level lane choice; if it stays MUST, it needs the exception.
- **Triage: rejected, no change, based on past triage.** a0 M5 weighed GEN-09 against SIDE-01 and added a note to each linking them. The handbook does not say which applies on a FREEWAY, and the notes say so. 10.23 is a plain command ("Use the middle or left lane"), so INSTRUCTION fits, as in a0 M3.

### S3-006. General passing checks duplicate the two-lane procedure rules

*duplicate* · minor · medium confidence · rules: PASS-GEN-02, PASS-PROC-02, PASS-GEN-03, PASS-PROC-03

PASS-GEN-02 ("make certain the way is clear", 7.30) and PASS-PROC-02 ("to make sure the roadway is clear", 7.35) state the same check. PASS-GEN-03 ("give the proper signal before changing lanes", 7.31) and PASS-PROC-03 ("turn on the left turn signal", 7.35) state the same signal. The PROC rules are the same duties limited to two-lane roads, so the set says each thing twice at different levels of detail and does not mark the overlap.

- Fix: Keep both pairs but note in PASS-PROC-02 and PASS-PROC-03 that they are the two-lane detail of PASS-GEN-02 and PASS-GEN-03. Or merge: cite 7.35 in GEN-02 and GEN-03 and drop the duplicated parts of the PROC rules.
- **Triage: not an error, no change.** The handbook states both: the basic safety rules for every pass (7.30, 7.31) and the steps for a two-lane road (7.35). Each rule stands on its own, and the pairs do not conflict.

## Other

### S3-007. Rules about going around islands and barricades are not about overtaking

*out of scope* · minor · medium confidence · rules: PASS-SIGN-03, PASS-SIGN-04

PASS-SIGN-03 (6.98: "traffic is permitted to pass on either side of a traffic island or an obstruction") and PASS-SIGN-04 (6.243–6.248: "Passing Traffic", "Pass to the Right", "bear to the right") use "pass" to mean driving around a fixed object. They are not about moving past another vehicle. The set's own vocabulary defines PASS as "Moving past the vehicle ahead; overtaking" (16.106). Including them confuses the meaning of passing in the set and adds lane-guidance rules outside the topic.

- Fix: Remove PASS-SIGN-03 and PASS-SIGN-04 from the overtaking set, or move them to a lane-guidance or work-zone topic.
- **Triage: rejected, no change, based on past triage.** Same as a2 S2-040 and S2-043. a0 M6.3 and M6.4 put passing a fixed hazard in scope. Since a2 S2-041, SIGN-03's action names the traffic island or obstruction.

### S3-008. Warning-sign fine recorded as a penalty in one rule and only as a note in the other

*inconsistent penalty* · minor · medium confidence · rules: PASS-SIGN-01, PASS-SIGN-02

PASS-SIGN-02 fills penalty with "A fine of $1 to $200, doubled in a work zone with workers present", based on 6.266 and 6.267. PASS-SIGN-01 says in its note that "the pennant is a warning sign; disobeying it is a violation with a fine of $1 to $200 (6.266, 6.267)", but leaves penalty "" and does not cite 6.266 or 6.267. The same handbook penalty is handled two different ways.

- Fix: In PASS-SIGN-01, set penalty to "For the 'No Passing Zone' pennant (a warning sign): a fine of $1 to $200, doubled in a work zone with workers present" and add 6.266 and 6.267 to evidence.
- **Triage: rejected, no change, based on past triage.** Same as a2 S2-035. In a0 M4, SIGN-01's penalty was left empty because its 'Do Not Pass' sign has no stated penalty, and the pennant's fine went into the note.

### S3-009. 'passing a warning sign' uses PASS in a sense its definition does not fit

*inconsistent terms* · minor · medium confidence · rules: PASS-SIGN-02

PASS-SIGN-02's condition reads "WHEN passing a warning sign for a reverse curve…". In a set where PASS means overtaking a vehicle, "passing a sign" is ambiguous and could be read as an overtaking condition.

- Fix: Change the when to "the DRIVER has driven by a warning sign for a reverse curve, sharp turn, gradual curve, reverse sharp turn, sharp curve chevron, or winding road" or "approaching a curve or winding section marked by a warning sign for …".
- **Triage: rejected, no change, based on past triage.** Same as a0 G4 and a2 S2-038: a lowercase phrase that means driving past a fixed object, not overtaking, is not an error.

### S3-010. SERVICE VEHICLE is taken from the handbook but cites no evidence

*missing citation* · minor · high confidence · rules: PASS-USER-15, PASS-USER-16

The vocabulary entry SERVICE VEHICLE lists exactly the vehicles named in 9.29 ("emergency medical vehicle, law enforcement vehicle, fire truck, tow truck, utility service vehicle, Texas Department of Transportation vehicle…"), but its evidence is []. That marks it as self-defined, even though the list comes from the handbook.

- Fix: Set the evidence of SERVICE VEHICLE to ["9.29"].
- **Triage: fixed as proposed.** SERVICE VEHICLE evidence: ["9.29"]. This reverses a2 S2-072 and S2-078, because there is new evidence those triages did not weigh:
  - The definition copies 9.29's list of vehicles almost word for word.
  - FREEWAY is defined the same way, from the list in 10.13, and it cites 10.13 (a0 M5).
  - task.md says to cite the block when the handbook supplies the definition.

  CYCLIST (a0 V3) is different: its definition does not come from 16.14. The b2 atomic check will re-check PASS-USER-15 and PASS-USER-16, because a vocabulary entry they use has changed.
