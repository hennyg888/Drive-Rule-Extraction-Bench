# Atomic check (stage 2): gold_set\ca\overtaking\b1_format.json

Judge: anthropic/claude-opus-5-5 · run folder: `runs\20261121-182609-check-atomic-overtaking-b2` (requests, responses, findings.jsonl, triage.csv) · 38 rules checked, 0 failed calls · $0.9239

Skipped 13 rules already checked: identical to a rule in `gold_set\ca\overtaking\a1_format.json` (ignoring id and number), with the same vocabulary entries. PASS-GEN-02, PASS-GEN-03, PASS-MARK-02, PASS-MARK-03, PASS-LOC-01, PASS-LOC-02, PASS-LOC-04, PASS-LOC-05, PASS-PROC-02, PASS-SIDE-02, PASS-USER-06, PASS-USER-08, PASS-COND-01

**57 findings** (10 major, 47 minor) in 32 rules.

**Triage:** all 57 findings were triaged. The reviewer accepted the triages Claude Code proposed: 17 fixed, 40 rejected. Each decision is recorded under its finding as a **Triage** line, weighed against the CA triages (a0, a2, a3, b0). Fixes were applied to `b2_atomic.json`, which started as an exact copy of `b1_format.json`.
- BEING-01 was split (S2-042): BEING-01 keeps "allow the vehicle to pass and maintain speed", and the new PASS-BEING-10 holds "maintain lane position" with the motorcycle exception, citing 13.35 and 13.41 (S2-041). BEING-06's note now points to BEING-10. PASS-BEING-10 was added at the end of the BEING group, so no rules were renumbered.
- New vocabulary term EMERGENCY VEHICLE (S2-054, S2-057), written in CAPS in USER-16, BEING-08 and BEING-09.
- After the fixes there are 52 rules and 16 vocabulary terms.
- Format check (`check_format.py b2_atomic.json --handbook ca --allow-lowercase pass`): no format errors.

## PASS-GEN-01: Judge space before passing near hazards

> WHEN approaching an oncoming vehicle or BICYCLIST OR a hill, curve, INTERSECTION, or road obstruction, the PASSER MUST judge whether there is enough space to pass.

### S2-001. Lowercase 'or' mixed with keyword 'OR' in the condition

*grammar* · minor · medium confidence

The condition "approaching an oncoming vehicle or BICYCLIST OR a hill, curve, INTERSECTION, or road obstruction" uses the keyword OR once and lowercase 'or' twice, all with the same disjunctive meaning. The grammar joins FACTs with the keyword OR. Mixing the two forms makes the structure ambiguous: it is unclear which disjunctions are formal and whether 'approaching' governs every item. The handbook (10.184–10.186) lists all six hazards as equal alternatives after "whenever you approach".

- Fix: when: "approaching an oncoming vehicle OR approaching an oncoming BICYCLIST OR approaching a hill OR approaching a curve OR approaching an INTERSECTION OR approaching a road obstruction"; update statement to match.
- **Triage: rejected.** Settled at a2 S2-002: every alternative is a disjunction, so the mixed or/OR doesn't change the meaning.

### S2-002. Actor PASSER implies a pass already under way, but the judgement precedes the pass

*actor* · minor · low confidence

PASSER is defined as "The driver making a PASS", but 10.184 says "You must judge whether you have enough space to pass whenever you approach…". This is a judgement made before deciding to pass, by any driver considering a pass. Read literally, the rule applies only once a pass is in progress, which is too late for the judgement.

- Fix: actor: "DRIVER"; when: "the DRIVER intends to PASS AND is approaching …" (with the hazards as above). Alternatively, add a note that PASSER here includes a driver considering a pass.
- **Triage: rejected.** PASSER vs DRIVER was ignored at a3 S3-011, and PASSER as the actor was settled at a2 S2-004.

## PASS-GEN-04: Space to return to lane

> WHEN considering a PASS, the PASSER MUST NOT pass, UNLESS there is enough space to return to the PASSER's original lane.

### S2-003. Actor PASSER (a driver already making a PASS) clashes with the condition "considering a PASS"

*vocabulary* · minor · low confidence

The vocabulary defines PASSER as "The driver making a PASS". The rule applies to a driver who is only "considering a PASS" and has not yet started one. So the actor is, by definition, already passing, while the rule forbids starting the pass. The handbook simply says to the driver, 10.188: "Do not pass:" … 10.192: "Unless you have enough space to return to your lane." Using PASSER here is slightly circular and could be read as applying only after a pass has begun.

- Fix: Set actor to "DRIVER" and when to "about to PASS another vehicle". Change unless to "there is enough space to return to the DRIVER's lane". The statement becomes: "WHEN about to PASS another vehicle, the DRIVER MUST NOT pass, UNLESS there is enough space to return to the DRIVER's lane." Add DRIVER to the vocabulary if it is not already defined.
- **Triage: rejected.** GEN-04's use of PASSER was ignored at a3 S3-011.

## PASS-GEN-05: Use the left lane to pass

> WHEN driving on a multilane road AND intending to pass, the PASSER SHOULD use the PASSING LANE to pass.

### S2-004. Plain command "Use the left lane" recorded as ADVICE

*strength* · major · medium confidence

10.33 reads "Use the left lane to pass or turn left." That is a plain command. The extractor's table maps a plain command, and "use" by name, to INSTRUCTION with MUST or MUST NOT. The rule instead records force "ADVICE" with modal "SHOULD". The intro in 10.32, "Here are some tips for choosing a lane:", hints at softer intent. Even so, the instructions say to keep the handbook's wording strength, and the wording is imperative. At minimum the choice needs a note explaining it.

- Fix: Set force "INSTRUCTION" and modal "MUST", giving the statement "WHEN driving on a multilane road AND intending to pass, the PASSER MUST use the PASSING LANE to pass." If ADVICE is kept on purpose, add a note: "Worded as an imperative ('Use the left lane') but introduced as a tip in 10.32; recorded as ADVICE because of the 'tips' framing."
- **Triage: rejected.** Re-raises a2 S2-007, where the reviewer set GEN-05 to ADVICE. The note already gives the 'tips' framing (10.32, 10.33), so no new evidence.

### S2-005. "Left lane" in 10.33 narrowed to the far-left PASSING LANE

*faithfulness* · minor · low confidence

10.33 says "the left lane". 10.46 defines the passing lane as the "far left lane … closest to the center divider". The rule merges the two by requiring the PASSING LANE. On a road with three or more lanes, "the left lane" could mean any lane to the left of the driver's lane, not only the far-left one. The note acknowledges that two blocks are combined but does not flag this possible difference in meaning.

- Fix: Add to the note: "10.33 says 'the left lane'; it is read here as the far left PASSING LANE defined in 10.46."
- **Triage: fixed as proposed.** Cheap and accurate: add to GEN-05's note "10.33 says 'the left lane'; it is read here as the far left PASSING LANE defined in 10.46."

## PASS-MARK-04: Double solid white lines: no lane change to pass

> WHEN there are double solid white lines next to the DRIVER's lane, the DRIVER MUST NOT cross them to pass.

### S2-006. Rule narrows a general lane-change ban to passing only

*faithfulness* · minor · medium confidence

Block 10.19 forbids every lane change across these lines: "Never change lanes over double solid white lines. Wait until you see a single broken white line." The rule's action, "cross them to pass", covers only crossing to pass. Read alone, it could suggest that crossing for other reasons, such as entering or leaving a carpool (HOV) lane or a ramp, is allowed. The limit to passing comes from the topic scope, not from the handbook, and neither the rule nor its note says so.

- Fix: Set action to "change lanes over them, including to pass", so the statement reads: "WHEN there are double solid white lines next to the DRIVER's lane, the DRIVER MUST NOT change lanes over them, including to pass." Add to note: "10.19 forbids any lane change over double solid white lines (lane barrier to an HOV lane, or near freeway ramps), not only passing."
- **Triage: rejected.** The rule set covers passing only (same scope reasoning as a2 S2-029), and MARK-04's note already quotes 10.19's general ban.

## PASS-LOC-03: No passing at crossroads and driveways

> WHEN at crossroads or driveways, the PASSER MUST NOT pass.

### S2-007. Circular actor: PASSER is told not to pass

*vocabulary* · minor · medium confidence

The vocabulary defines PASSER as "The driver making a PASS." The rule says "the PASSER MUST NOT pass", so the actor is defined by the very action it forbids. Read literally, it only binds a driver who is already passing. The handbook's prohibition (10.188: "Do not pass:" with 10.191: "At crossroads and driveways.") is addressed to any driver.

- Fix: Set actor to "DRIVER" and statement to "WHEN at crossroads or driveways, the DRIVER MUST NOT PASS."
- **Triage: rejected.** PASSER vs DRIVER was ignored at a3 S3-011.

### S2-008. Action 'pass' not written as the vocabulary term PASS

*vocabulary* · minor · low confidence

The PASSER definition relies on a defined term PASS, but the action is written in lowercase: "pass". The rule therefore does not tie the forbidden action to the defined manoeuvre.

- Fix: Set action to "PASS" and update the statement to match.
- **Triage: rejected.** The verb "pass" stays lowercase (a0 V3).

## PASS-LOC-07: No passing where DO NOT PASS sign posted

> WHEN a do-not-pass sign is posted for the PASSER's direction of travel, the PASSER MUST NOT pass.

### S2-009. Note misstates what block 12.85 says

*note* · minor · medium confidence

The note says "12.85 says white regulatory signs state rules you must obey." The cited block reads only 12.85: "Communicates many important rules you must obey." It does not mention white regulatory signs, or any sign type. The link to regulatory signs may come from a heading or context that is not shown. A checker reading the note would expect wording that the block does not contain.

- Fix: Change the note to: "Rule shown only by the DO NOT PASS sign among the White Regulatory Signs in figure 12.89. 12.85 states that this sign category 'communicates many important rules you must obey' (the category is identified by the surrounding heading, which is not in the cited block)."
- **Triage: fixed as proposed.** Partly. Reword LOC-07's note so it says where the link comes from: "Rule shown only by the DO NOT PASS sign among the White Regulatory Signs in figure 12.89; 12.85, under the heading White Rectangular Sign, says these signs communicate 'many important rules you must obey'."

### S2-010. 'for the PASSER's direction of travel' is not supported by the citations

*unsupported condition* · minor · medium confidence

The condition "a do-not-pass sign is posted for the PASSER's direction of travel" adds a direction qualifier. Neither cited block states it: figure 12.89 shows only the sign reading "DO NOT PASS", and 12.85 is a general statement. The qualifier is sensible, but the cited blocks do not support it.

- Fix: Set when to "a DO NOT PASS sign is posted" and the statement to "WHEN a DO NOT PASS sign is posted, the DRIVER MUST NOT pass." If you keep the qualifier, add a note saying it is inferred and not stated in the cited blocks.
- **Triage: fixed as proposed.** Note option, as for an inferred condition at a0 K2: add "The direction qualifier is inferred; the sign applies to the traffic it faces." The condition is unchanged.

### S2-011. Actor PASSER makes the rule circular

*actor* · minor · low confidence

PASSER is defined as "The driver making a PASS." The rule then says "the PASSER MUST NOT pass", meaning a driver who is passing must not pass. The prohibition is meant for any driver who comes upon the sign, before any pass begins.

- Fix: Use actor "DRIVER": "WHEN a DO NOT PASS sign is posted, the DRIVER MUST NOT pass."
- **Triage: rejected.** PASSER vs DRIVER was ignored at a3 S3-011.

## PASS-PROC-01: How to pass on an open highway

> WHEN going to pass on an open highway, the PASSER MUST signal the plan to pass, look over the shoulder to check blind spots, move into the lane used for passing, speed up to pass the vehicle, then signal and return to the original lane.

### S2-012. Cites lane-change and signalling blocks whose content is not in the rule

*citation* · minor · medium confidence

The rule's action follows only the passing list: 10.194: "When you are going to pass on an open highway:" with steps 10.195–10.199. It also cites 9.33, 9.35, 9.36 and 10.36–10.42, which the action does not draw on. 10.38: "Check your mirrors.", 10.39: "Check traffic behind and beside you.", 10.41: "…Do not let the vehicle drift into another lane." and 10.42: "Be sure there is enough space… It is not necessary to slow down…" all appear nowhere in the action. 9.36: "At least five seconds before you change lanes on a freeway" covers freeways, not an open highway. 9.33 is also worded as advice ("You should signal:"), so it cannot support a MUST. These blocks belong to separate lane-change and signalling rules. Citing them suggests this INSTRUCTION rule includes their content and their mixed strengths, when it does not.

- Fix: Set evidence to ["10.194", "10.195", "10.196", "10.197", "10.198", "10.199"]. Change the note to: "10.197 says 'the passing lane' without saying which lane on a two-lane road." Leave the general lane-change checks and the freeway five-second signal to their own rules.
- **Triage: rejected.** Re-raises a0 C5, a2 S2-020 and a3 S3-007: the reviewer chose to cite these blocks and explain them in the note.

## PASS-SIDE-01: When passing on the right is allowed

> WHEN an open highway has two or more lanes going in the PASSER's direction OR the DRIVER ahead is turning left and the PASSER can safely pass on the right OR the PASSER is on a one-way street OR the PASSER is overtaking a LIGHT RAIL VEHICLE, the PASSER MAY ONLY pass on the right.

### S2-013. Light rail vehicle case added to the 'only when' list without support

*faithfulness* · major · high confidence

The rule adds a fourth permitted case, "OR the PASSER is overtaking a LIGHT RAIL VEHICLE", to the exhaustive list introduced by 10.200: "You may pass on the right only when:". The handbook's list (10.201–10.203) has only three cases: an open highway with two or more lanes, a driver ahead turning left, and a one-way street. 13.22 does not grant permission to pass on the right. It says: "Do not overtake and pass a light rail vehicle or streetcar on the left side, whether it is moving or standing, unless:". That is a prohibition on passing on the left, with exceptions that are not shown here. Under MAY ONLY, the added case widens where passing on the right is allowed (for example, on a two-way single-lane street next to a streetcar). Neither 10.200 nor 13.22 states this. The note admits the case is inferred from 13.22.

- Fix: Remove the fourth case and the citation 13.22. Set when: "an open highway has two or more lanes going in the PASSER's direction OR the DRIVER ahead is turning left AND the PASSER can safely pass on the right OR the PASSER is on a one-way street". Set statement: "WHEN an open highway has two or more lanes going in the PASSER's direction OR the DRIVER ahead is turning left AND the PASSER can safely pass on the right OR the PASSER is on a one-way street, the PASSER MAY ONLY pass on the right." Set evidence: ["10.200","10.201","10.202","10.203"]. Leave the light rail vehicle prohibition to its own rule (USER-05), and change the note accordingly.
- **Triage: rejected.** Re-raises a3 S3-008: the fourth case was the reviewer's chosen fix for the SIDE-01/USER-05 conflict, and the note says it is inferred from 13.22.

### S2-014. Lowercase 'and' inside an OR chain leaves grouping unclear

*grammar* · minor · medium confidence

The condition joins facts with the keyword OR but writes "the DRIVER ahead is turning left and the PASSER can safely pass on the right" with a lowercase 'and'. The grammar requires the AND keyword between facts. The grouping (the turning-left case requires safety, and the other cases do not) is implied but not marked. This makes the condition harder to parse formally.

- Fix: Use the keyword AND and make the grouping explicit, e.g. "... OR (the DRIVER ahead is turning left AND the PASSER can safely pass on the right) OR ...". Alternatively, add a note that AND binds tighter than OR.
- **Triage: rejected.** The lowercase "and" grouping inside one fact was set at a0 M2 (rejected again at a2 S2-022).

## PASS-USER-02: Pass large vehicles on the left

> WHEN passing a LARGE VEHICLE, the PASSER MUST pass on the left side.

### S2-015. Note claims an override of another rule that the cited blocks do not support

*note* · minor · low confidence

The note says the rule "Restricts SIDE-01: a LARGE VEHICLE is passed on the left even where SIDE-01 allows passing on the right." The cited blocks say nothing about passing on the right or about how the two rules interact. 13.14 only says: "Always pass a large vehicle on the left side." The claim that this rule overrides the passing-on-the-right permissions is the extractor's own reading, not supported by these citations. The note also depends on another rule's id instead of standing on its own.

- Fix: Change the note to: "Worded 'Always pass a large vehicle on the left side.' within a list about driving near large vehicles and trucks (13.12). The handbook does not say how this interacts with situations where passing on the right is otherwise allowed."
- **Triage: rejected.** A note may name another rule (a0 N1; a2 S2-033).

## PASS-USER-03: Do not linger beside a large vehicle

> WHEN passing a LARGE VEHICLE, the PASSER MUST move ahead of it after passing and not drive next to it longer than needed.

### S2-016. The no-lingering prohibition is narrowed to passing only

*scope* · major · medium confidence

The handbook states the prohibition for anyone driving near a large vehicle. 13.12: "When driving near large vehicles and trucks, do not:" and 13.14: "Drive next to them longer than you need to." The rule makes it apply only "WHEN passing a LARGE VEHICLE" to the "PASSER". A driver who is travelling alongside a truck without passing it (for example, in an adjacent lane at the same speed) is told not to linger by the handbook, but this rule does not cover that case. Only the "After you pass … move ahead of it" part is specific to passing.

- Fix: Split into two rules. (1) when: "driving near a LARGE VEHICLE", actor: "DRIVER", modal: "MUST NOT", action: "drive next to the LARGE VEHICLE longer than needed"; statement: "WHEN driving near a LARGE VEHICLE, the DRIVER MUST NOT drive next to the LARGE VEHICLE longer than needed." Keep the vague term "longer than needed". (2) when: "the PASSER has passed a LARGE VEHICLE", actor: "PASSER", modal: "MUST", action: "move ahead of the LARGE VEHICLE"; statement: "WHEN the PASSER has passed a LARGE VEHICLE, the PASSER MUST move ahead of the LARGE VEHICLE." Both rules cite 13.12 and 13.14.
- **Triage: rejected.** Out of scope, as at a2 S2-029: driving alongside a large vehicle without passing it is not passing.

### S2-017. A prohibition is hidden inside a MUST action

*grammar* · minor · medium confidence

The action "move ahead of it after passing and not drive next to it longer than needed" joins a positive obligation and a prohibition under the single modal MUST. The handbook words the second part as a "do not" item (13.12/13.14), which calls for MUST NOT. Putting a negated clause under MUST bundles two separately checkable rules into one and blurs the modal.

- Fix: Express the prohibition with modal MUST NOT in its own rule, as in the split given in the other finding.
- **Triage: rejected.** Positive first, negated last in one MUST action is the accepted pattern (a0 M4; a2 S2-028).

## PASS-USER-04: Passing a stopped bus, streetcar or trolley

> WHEN a bus or LIGHT RAIL VEHICLE is stopped at a SAFETY ZONE or traffic light, the DRIVER MAY ONLY pass it at no more than 10 mph.

### S2-018. LIGHT RAIL VEHICLE is self-defined more broadly than the handbook's "streetcar, or trolley"

*vocabulary* · minor · medium confidence

The handbook names only "a bus, streetcar, or trolley" (13.19: "When a bus, streetcar, or trolley is stopped at a safety zone or traffic light, you may pass at no more than 10 mph."). The rule replaces this with the self-defined LIGHT RAIL VEHICLE: "A rail vehicle, such as a light rail train, streetcar or trolley, operating on tracks on public roads." That definition adds "light rail train", which the cited blocks do not mention. It also requires the vehicle to run "on tracks", which may leave out a trolley that is a trolleybus. The handbook's own words are clear, so the coined term is unnecessary and slightly shifts which vehicles the 10 mph limit covers.

- Fix: Use the handbook's words and drop the coined term. Set when: "a bus, streetcar, or trolley is stopped at a SAFETY ZONE or traffic light". Set statement: "WHEN a bus, streetcar, or trolley is stopped at a SAFETY ZONE or traffic light, the DRIVER MAY ONLY pass it at no more than 10 mph."
- **Triage: rejected.** Re-raises a3 S3-011, where the reviewer chose LIGHT RAIL VEHICLE for streetcar and trolley.

## PASS-USER-05: No passing light rail or streetcar on the left

> WHEN overtaking a LIGHT RAIL VEHICLE, whether it is moving or standing, the PASSER MUST NOT pass it on the left side, UNLESS the tracks are so close to the right side that the PASSER's vehicle cannot pass on the right OR the PASSER is on a one-way street OR a traffic officer directs the PASSER to pass on the left.

### S2-019. Note points to another rule and misdescribes this one

*note* · minor · medium confidence

The note says "SIDE-01's fourth case allows the pass on the right that this rule calls for." Rules and notes should stand on their own, and this note depends on another rule the reader cannot see. It also misstates this rule: the rule does not call for a pass on the right. It only forbids a pass on the left, as 13.22 says: "Do not overtake and pass a light rail vehicle or streetcar on the left side…".

- Fix: Replace the note with: "Handbook covers both light rail vehicles and streetcars (13.22); the prohibition applies whether the vehicle is moving or standing. The three exceptions are the list items 13.23–13.25."
- **Triage: fixed as proposed.** Partly. Naming another rule is allowed (a2 S2-033), but "calls for" overstates USER-05, which only forbids the left side. Reword: "SIDE-01's fourth case allows passing a LIGHT RAIL VEHICLE on the right, the side this rule leaves open."

### S2-020. 'passenger vehicle' reworded as 'PASSER's vehicle'

*faithfulness* · minor · low confidence

13.23 reads: "When the tracks are so close to the right side that the passenger vehicle cannot pass on the right." The rule says "the PASSER's vehicle cannot pass on the right". The handbook's own wording is "passenger vehicle", which may refer to a class of vehicle. Generalising it to any vehicle the PASSER drives is a small departure from the source.

- Fix: Use the handbook wording in the unless field: "the tracks are so close to the right side that the passenger vehicle cannot pass on the right OR the PASSER is on a one-way street OR a traffic officer directs the PASSER to pass on the left". Update the statement to match.
- **Triage: rejected.** Settled at a0 G4 and a2 S2-034.

### S2-021. LIGHT RAIL VEHICLE definition adds 'trolley'

*vocabulary* · minor · low confidence

The self-defined LIGHT RAIL VEHICLE entry lists "a light rail train, streetcar or trolley". The cited block 13.22 names only "a light rail vehicle or streetcar". The word "trolley" is not supported by the blocks shown and widens the term.

- Fix: Define LIGHT RAIL VEHICLE as: "A light rail vehicle or streetcar operating on tracks on public roads."
- **Triage: rejected.** "trolley" was added to the definition at a3 S3-011 so that USER-04 still covers trolleys.

## PASS-USER-09: Do not squeeze bicyclists into parked cars

> WHEN passing a BICYCLIST, the PASSER MUST give the BICYCLIST enough space so the BICYCLIST is not forced into parked vehicles or open vehicle doors.

### S2-022. Passing condition is inferred from the intro but no note says so

*note* · minor · low confidence

The list item 13.116 does not mention passing: "Give bicyclists enough space so they are not forced into parked vehicles or open vehicle doors." The rule's condition "passing a BICYCLIST" comes from the introducing paragraph 13.115: "When you cannot change lanes to pass a bicyclist, allow at least three feet… Remember to:". That paragraph opens with a narrower situation (passing without changing lanes). It is unclear whether the list applies to every pass or only to that one. The rule silently picks the broader reading and gives the checker no explanation.

- Fix: Set note to: "Instruction from list item 13.116, read with its introduction 13.115. 13.115 opens with passing a bicyclist when you cannot change lanes; the item is taken to apply to any pass of a bicyclist. The 3-feet minimum in 13.115 is a separate rule."
- **Triage: rejected.** The lead-in to a list is not a condition of each item (a2 S2-040).

## PASS-USER-11: One danger at a time: oncoming vehicle and bicyclist

> WHEN on a two-lane road with an oncoming vehicle to the left AND a BICYCLIST ahead to the right, the DRIVER MUST slow down, let the oncoming vehicle pass, then move left to allow plenty of space (at least three feet) to pass the BICYCLIST, and not drive between the vehicle and the BICYCLIST.

### S2-023. Steady-flow alternative from the same block is omitted

*completeness* · major · high confidence

The rule requires, without exception, that the driver "slow down, let the oncoming vehicle pass, then move left…". The same cited block gives a different action when there is no gap in oncoming traffic. 17.13: "If there is a steady flow of oncoming vehicles, use as much of the left lane as you safely can to pass the bicyclist." As written, the rule tells the driver to wait for the oncoming vehicle to pass and then move left in every case, which is not workable under a steady oncoming flow. It also contradicts the handbook's guidance for that situation.

- Fix: Set unless to "there is a steady flow of oncoming vehicles" and rewrite the statement accordingly. Then add a separate rule: "WHEN on a two-lane road with a BICYCLIST ahead to the right AND there is a steady flow of oncoming vehicles, the DRIVER MUST use as much of the left lane as the DRIVER safely can to pass the BICYCLIST." Cite 17.13 and list "as much of the left lane as the DRIVER safely can" as a vague term.
- **Triage: rejected.** Re-raises a2 S2-041 (ignored): the proposed steady-flow rule duplicates USER-12, which the atomic judge can't see.

### S2-024. Prohibition folded into a MUST action

*grammar* · minor · medium confidence

The action combines a positive duty with a prohibition: "…to pass the BICYCLIST, and not drive between the vehicle and the BICYCLIST". The grammar allows one modal per rule, and here a MUST NOT is hidden inside a MUST rule. This makes the rule harder to parse and check. It is also partly redundant: once the oncoming vehicle has been let pass first, the driver no longer drives between the two.

- Fix: Drop ", and not drive between the vehicle and the BICYCLIST" from the action. If the prohibition is wanted, state it as its own rule: "WHEN on a two-lane road with an oncoming vehicle to the left AND a BICYCLIST ahead to the right, the DRIVER MUST NOT drive between the oncoming vehicle and the BICYCLIST." Cite 17.13.
- **Triage: rejected.** Positive first, negated last in one MUST action is the accepted pattern (a0 M4).

## PASS-USER-12: Steady oncoming flow when passing a bicyclist

> WHEN passing a BICYCLIST on a two-lane road AND there is a steady flow of oncoming vehicles, the PASSER MUST use as much of the left lane as the PASSER safely can.

### S2-025. Note relies on a block the rule does not cite

*citation* · minor · medium confidence

The note says: "Does not relax USER-08: if three feet cannot be given, do not pass the BICYCLIST (13.115)." Block 13.115 is not in `evidence`, so this claim is not supported by the rule's citations. The cited block 17.13 only says "…move to the left to allow plenty of space (at least three feet) to pass the bicyclist. If there is a steady flow of oncoming vehicles, use as much of the left lane as you safely can…". It does not say that the pass must be abandoned when three feet cannot be given. A checker reading only this rule cannot verify how the two rules interact.

- Fix: Either add "13.115" to `evidence`, or reword the note to rest on the cited block, for example: "Same block (17.13) sets a minimum of at least three feet when passing a bicyclist; this rule does not relax that minimum. See PASS-USER-08."
- **Triage: rejected.** Something mentioned only in a note needs no citation (a2 S2-044).

### S2-026. "steady flow of oncoming vehicles" is vague but not listed

*vague terms* · minor · medium confidence

The condition "there is a steady flow of oncoming vehicles" leaves open what traffic density or gap length counts as a "steady flow". The handbook gives no measure for it, so the driving model cannot tell when the rule applies. It is not listed in `vague_terms`.

- Fix: Add to `vague_terms`: {"term": "steady flow of oncoming vehicles", "explanation": "no traffic density or gap length given"}.
- **Triage: fixed as proposed.** An unlisted vague phrase, fixed the same way as at a2 (S2-003, S2-016): add {"term": "steady flow of oncoming vehicles", "explanation": "no traffic density or gap length given"} to USER-12.

## PASS-USER-13: Follow a bicyclist at a safe distance

> WHEN behind a BICYCLIST in a travel lane who is not able to be passed, the DRIVER SHOULD follow at a safe distance.

### S2-027. Condition 'not able to be passed' does not match the handbook's situation

*condition* · major · medium confidence

The rule's condition is "behind a BICYCLIST in a travel lane who is not able to be passed". The cited text gives a narrower situation. 13.108 ("Drivers should follow at a safe distance. When it is safe, the bicyclist should move to a position that allows vehicles to pass.") follows the list in 13.101–13.107 of reasons a bicyclist may ride away from the right curb or edge (13.101: "…must ride as close as possible to the right curb or edge of the road, unless:"). So the handbook's situation is a bicyclist who is lawfully riding away from the right edge in a position that blocks passing. The rule's wording is broader: it would cover a cyclist who cannot be passed for any reason, such as oncoming traffic or a no-passing zone. It also adds "in a travel lane", which no cited block states. A driving model reading only this rule would apply it more widely than the handbook does. The note admits the condition is inferred but does not tie it to the actual context.

- Fix: when: "behind a BICYCLIST who is riding away from the right curb or edge of the road for one of the permitted reasons (passing, preparing a left turn, avoiding a hazard, a lane too narrow to share, approaching a right turn, or on a multi-lane one-way road) AND whose position does not allow the DRIVER to pass"; statement: "WHEN behind a BICYCLIST who is riding away from the right curb or edge of the road for one of the permitted reasons AND whose position does not allow the DRIVER to pass, the DRIVER SHOULD follow at a safe distance." Remove the vague term "not able to be passed" or replace it to match the new wording. Update the note to say the condition comes from the context of 13.101–13.107.
- **Triage: rejected.** Re-raises a0 K2 and a2 S2-046/S2-047. The proposed condition would spell out the list in the rule's words.

## PASS-USER-14: Bicyclist keeps right unless passing

> WHEN travelling slower than the flow of traffic, the BICYCLIST MUST ride as close as possible to the right curb or edge of the road, UNLESS passing a vehicle or another bicycle going in the same direction.

### S2-028. Other listed exceptions are dropped, so the obligation is stated too broadly

*completeness* · major · medium confidence

The rule cites 13.101: "Bicyclists traveling slower than the flow of traffic must ride as close as possible to the right curb or edge of the road, unless:". This colon introduces a list of exceptions, and the rule includes only one item, 13.102: "Passing a vehicle or another bicycle in the same direction." The rule's own note says 13.103–13.107 give further exceptions in the same list: preparing to turn left, avoiding a hazard, a lane too narrow to share, approaching a right turn, and a one-way road with two or more lanes. The statement "the BICYCLIST MUST ride as close as possible to the right curb … UNLESS passing …" therefore tells a driving model that keeping right is required in all those other situations too, which the handbook does not say. Putting the exceptions only in the note does not fix the rule's meaning. The instructions say to "Include each rule's conditions and exceptions with it as one entry." The topic limit does not justify cutting exceptions from a rule the extractor chose to include. I have not seen blocks 13.103–13.107 myself; this finding relies on the rule's own note.

- Fix: Add all the exceptions from the list to `unless` and cite them, e.g. unless: "passing a vehicle or another bicycle going in the same direction OR preparing to turn left OR avoiding a hazard OR the lane is too narrow to share OR approaching a place where a right turn is allowed OR riding on a one-way road with two or more lanes". Add 13.103–13.107 to evidence and rewrite `statement` to match. Alternatively, keep only the passing exception but change `note` to say plainly that the rule as stated is incomplete. Adding the exceptions is preferred.
- **Triage: rejected.** Re-raises a2 S2-048, where the reviewer ruled that only the passing-related exceptions are included. The note names the others.

## PASS-USER-15: Emergency flashers ahead: pass carefully

> WHEN a vehicle's emergency flashers are seen ahead, the DRIVER MUST slow down and, when going past the vehicle, pass carefully.

### S2-029. 'Going past the vehicle' narrows the handbook's 'Pass carefully'

*faithfulness* · minor · low confidence

Block 19.25 says: "If you see a vehicle’s emergency flashers ahead, slow down. There may be a collision or other road emergency. Pass carefully." The handbook does not say what is being passed. Read in context, it is the collision or emergency scene, which may include other vehicles, people or debris, not only the vehicle with flashers. The rule's action, "when going past the vehicle, pass carefully", limits the care to passing that one vehicle. It also places a second condition inside the action.

- Fix: Set action to "slow down and pass the scene carefully" and statement to "WHEN a vehicle's emergency flashers are seen ahead, the DRIVER MUST slow down and pass the scene carefully." Change the vague term to {"term": "carefully", "explanation": "no specific action given"}. Add to the note: "The handbook does not say what is passed; read as the collision or emergency scene."
- **Triage: rejected.** Low confidence, and the wording was set at a2 S2-050.

## PASS-USER-16: Move over and slow down for stopped emergency and work vehicles

> WHEN approaching a stationary emergency vehicle with flashing emergency signal lights OR a stationary tow truck displaying flashing amber warning lights OR a stopped road work vehicle displaying emergency flashing or amber warning lights, the DRIVER MUST move over and slow down.

### S2-030. Parenthetical '(hazard lights)' from 13.47 dropped

*completeness* · minor · medium confidence

13.47 says: "stationary emergency vehicle with flashing emergency signal lights (hazard lights)". The rule keeps only "flashing emergency signal lights" and drops the handbook's gloss "(hazard lights)". That gloss tells the driving model what visual cue to look for, so leaving it out makes the condition harder to recognise.

- Fix: when: "approaching a stationary emergency vehicle with flashing emergency signal lights (hazard lights) OR a stationary tow truck displaying flashing amber warning lights OR a stopped road work vehicle displaying emergency flashing or amber warning lights" (update statement to match).
- **Triage: fixed as proposed.** Part of a handbook phrase left out, as at a2 S2-043. The gloss helps a driving model recognise the vehicle. Restore "(hazard lights)" in USER-16's condition.

### S2-031. Reading of 13.137's amber-light clause not noted

*note* · minor · low confidence

13.137 reads "Stationary emergency vehicles or tow trucks displaying flashing amber warning lights". It can be read as amber lights applying to both kinds of vehicle. The rule instead pairs emergency vehicles with "flashing emergency signal lights", taken from 13.47, and gives amber only to tow trucks. That is a fair reading, but it combines two blocks and settles an ambiguous sentence without saying so.

- Fix: Add to note: "13.137 could be read as amber lights qualifying both emergency vehicles and tow trucks; the emergency-vehicle light condition is taken from 13.47."
- **Triage: fixed as proposed.** An inference that isn't noted. Add the proposed note to USER-16: "13.137 could be read as amber lights qualifying both emergency vehicles and tow trucks; the emergency-vehicle light condition is taken from 13.47."

## PASS-USER-17: Do not pass the patrol car during a traffic break

> WHEN a TRAFFIC BREAK is in progress ahead, the DRIVER SHOULD NOT drive past the patrol vehicle.

### S2-032. "the patrol vehicle" is not tied to the TRAFFIC BREAK

*clarity* · minor · low confidence

The action "drive past the patrol vehicle" uses the definite article, but neither the rule nor the TRAFFIC BREAK vocabulary entry names a patrol vehicle. The definition speaks only of "an officer". 15.147 says: "During a traffic break, the officer turns on their emergency lights and slowly weaves across lanes." Read alone, the rule does not make clear that the vehicle meant is the one whose officer is carrying out the traffic break, rather than any patrol vehicle nearby.

- Fix: Set action to "drive past the patrol vehicle carrying out the TRAFFIC BREAK". The statement then reads: "WHEN a TRAFFIC BREAK is in progress ahead, the DRIVER SHOULD NOT drive past the patrol vehicle carrying out the TRAFFIC BREAK."
- **Triage: rejected.** Low confidence, and the referent is clear: the patrol vehicle is the one making the TRAFFIC BREAK (a2 S2-027).

## PASS-USER-18: Never drive through a safety zone

> WHEN approaching or passing a SAFETY ZONE, the DRIVER MUST NOT drive through the SAFETY ZONE.

### S2-033. Unconditional prohibition is given an invented, vague trigger

*condition* · minor · medium confidence

13.18 says: "Do not drive through a safety zone under any condition." The rule limits this to "WHEN approaching or passing a SAFETY ZONE". The cited blocks never mention approaching or passing. This adds a vague term ("approaching") that the handbook does not use. The lowercase "passing" in an overtaking rule set could also be read as overtaking, which is a different meaning. Driving through a safety zone already implies being at one, so the condition only adds ambiguity.

- Fix: Set when: "a SAFETY ZONE is in or beside the DRIVER's path". Set statement: "WHEN a SAFETY ZONE is in or beside the DRIVER's path, the DRIVER MUST NOT drive through the SAFETY ZONE." Set vague_terms to []. Keep 'under any condition' in the note.
- **Triage: rejected.** USER-18's condition is the one accepted at a2 S2-031, and its vague term came from b0 m4.

### S2-034. SAFETY ZONE definition omits how the zone is marked

*vocabulary* · minor · medium confidence

The vocabulary defines SAFETY ZONE only by its purpose: "A space set aside for pedestrians waiting for buses, streetcars, and trolleys." The driving model needs visible cues to recognize one. The cited blocks give them: 13.18 says "marked by raised buttons or markers on a road", and 13.21 says "Safe Zones are marked by dotted white lines." These cues appear only in the rule's note, not in the definition the rule relies on.

- Fix: Change the definition to: "A space on the road set aside for pedestrians waiting for buses, streetcars, and trolleys, marked by raised buttons or markers or by dotted white lines." Set its evidence to ["13.18", "13.21"].
- **Triage: rejected.** Re-raises a0 V5 and a2 S2-032: markings were kept out of the definition, and the difference is in USER-18's note.

## PASS-USER-19: Leave space when passing a bicyclist

> WHEN passing a BICYCLIST, the PASSER MUST leave space between the vehicle and the BICYCLIST.

### S2-035. Condition drops "in the travel lane"

*condition* · minor · medium confidence

The handbook limits the passage to a bicyclist in the travel lane: 13.110: "To safely pass a bicyclist that is in the travel lane, you may need to change to another lane… Leave space between your vehicle and the bicyclist." The rule's condition reads only "passing a BICYCLIST", so it also covers bicyclists in a bike lane or on the shoulder, which the cited block does not address. The instruction to leave space is general good sense, so the practical effect is small. Still, the rule's scope is wider than its source.

- Fix: Set when to "passing a BICYCLIST that is in the travel lane" and statement to "WHEN passing a BICYCLIST that is in the travel lane, the PASSER MUST leave space between the vehicle and the BICYCLIST."
- **Triage: rejected.** Settled at a2 S2-036: USER-19 was split out to apply to every pass of a BICYCLIST.

### S2-036. Note asserts a three-foot minimum not supported by the cited blocks

*note* · minor · low confidence

The note says "USER-08 gives the three-foot minimum when the PASSER cannot change lanes." None of the cited blocks (13.110–13.114) mentions three feet or any other distance. A checker reading only this rule cannot verify that claim from its citations.

- Fix: Drop the cross-reference, or reword it as: "A separate rule (PASS-USER-08) covers a minimum distance; it is not stated in these blocks."
- **Triage: rejected.** A note may name another rule (a2 S2-033) and carry uncited information (a2 S2-044).

## PASS-USER-20: Do not drive past a school bus with flashing red lights

> WHEN a school bus ahead or approaching is flashing its red lights, the DRIVER MUST stop and remain stopped, not driving past the bus, until the children are safely across and the lights stop flashing, UNLESS the school bus is on the other side of a divided or multilane highway with two or more lanes in each direction.

### S2-037. Irrelevant school-zone speed-limit block cited

*citation* · minor · high confidence

The evidence includes 13.153, which is about school-zone speed limits: 13.153: "The speed limit is 25 mph within 500 feet of a school while children are outside or crossing the street… When near schools, look for:". It says nothing about stopping for or driving past a school bus with flashing red lights, so it does not support this rule.

- Fix: Remove "13.153" from evidence: ["13.151", "13.152", "13.158", "13.159"].
- **Triage: rejected.** 13.153 is the list's lead-in, cited at b0 m3 under the a0 C2 convention. It supports the rule only as the lead-in.

### S2-038. Note makes a claim about another rule that the citations do not support

*note* · minor · medium confidence

The note says: "Applies even where USER-04 would allow passing a stopped bus at no more than 10 mph." None of the cited blocks (13.151, 13.152, 13.158, 13.159) mention passing a stopped bus at 10 mph. The note therefore describes an interaction with another rule that this rule's citations do not support. It also implies a conflict a checker cannot verify from this rule's evidence.

- Fix: Drop the sentence about USER-04, or cite the block that states the 10 mph rule and explain how the two rules relate. Suggested note: "Worded in the handbook as a stop requirement; it applies from either direction (13.158)."
- **Triage: rejected.** This link was added at b0 m1 (a0 N1). A note may name another rule.

## PASS-USER-21: Do not cut in front of a large vehicle after passing

> WHEN returning to the lane in front of a LARGE VEHICLE after passing it, the PASSER MUST NOT move in front of it and then suddenly slow down or stop, or change lanes directly in front of it to reach an exit or turn.

### S2-039. Rule is narrowed to the moment after passing, though the handbook applies it whenever driving near a large vehicle

*scope/condition* · major · medium confidence

The rule only applies "WHEN returning to the lane in front of a LARGE VEHICLE after passing it" and its actor is "PASSER". Neither cited block mentions passing. 13.8 says generally: "Do not move in front of a large vehicle and suddenly slow down or stop." 13.12–13.13 say: "When driving near large vehicles and trucks, do not: … Change lanes directly in front of them to reach an exit or turn." Moving in front of a large vehicle by merging, changing lanes or turning is not covered by this rule. A driving model would read the prohibition as limited to completing a pass.

- Fix: Widen the condition and the actor to match the handbook, and note the link to passing. For example, when: "moving into the lane in front of a LARGE VEHICLE, including when returning to the lane after passing it"; actor: "DRIVER". Add to note: "The handbook states this for any driver near a large vehicle; it applies to passing among other cases."
- **Triage: rejected.** Out of scope, as at a2 S2-029. USER-21 was added at a3 S3-004 as a passing rule.

### S2-040. Two separate instructions are merged, and the second one does not fit the condition

*rule structure* · minor · medium confidence

The action joins two different prohibitions from different blocks with "or". The first is "move in front of it and then suddenly slow down or stop" (13.8). The second is "change lanes directly in front of it to reach an exit or turn" (13.13, under the 'When driving near large vehicles' list in 13.12). Under the condition "returning to the lane in front of a LARGE VEHICLE after passing it", the second prohibition reads oddly: the driver is already changing lanes in front of the vehicle. These are separate situations and should be separate rules.

- Fix: Split into two rules. Rule A: "WHEN moving into the lane in front of a LARGE VEHICLE, including after passing it, the DRIVER MUST NOT suddenly slow down or stop in front of it." Evidence: ["13.8"]. Vague term: "suddenly". Rule B: "WHEN driving near a LARGE VEHICLE AND intending to reach an exit or turn, the DRIVER MUST NOT change lanes directly in front of the LARGE VEHICLE." Evidence: ["13.12", "13.13"]. Vague term: "directly in front".
- **Triage: rejected.** USER-21 was accepted as proposed at a3 S3-004, and a split would make a non-passing rule (lane changes to reach an exit), which is out of scope.

## PASS-BEING-01: Allow the pass; keep lane and speed

> WHEN another vehicle is passing the DRIVER OR signals that it plans to pass the DRIVER, the DRIVER MUST allow the vehicle to pass and maintain lane position and speed, UNLESS the passing vehicle is a motorcycle and it is possible to move to one side of the lane.

### S2-041. Motorcycle exception is not supported by the cited block

*citation* · major · high confidence

The unless clause "the passing vehicle is a motorcycle and it is possible to move to one side of the lane" has no support in the only cited block. 10.206 says only: "If a vehicle is passing you or signals that they plan on passing, allow the vehicle to pass. Maintain your lane position and your speed." The note says the exception comes from 13.41, but 13.41 is not in `evidence`. As cited, the exception is unsupported, and it changes when the rule applies.

- Fix: Remove the exception: unless: ""; statement: "WHEN another vehicle is passing the DRIVER OR signals that it plans to pass the DRIVER, the DRIVER MUST allow the vehicle to pass and maintain lane position and speed."; vague_terms: []. Keep the motorcycle case as its own rule citing 13.41. Alternatively, add 13.41 to evidence if it really states this exception.
- **Triage: fixed as proposed.** New: the motorcycle exception added at b0 M2 rests on 13.41, which BEING-01 doesn't cite. Fix with the finding's alternative: cite `13.35` and `13.41` (the lead-in with its item, a0 C2), on whichever rule carries the exception after S2-042.

### S2-042. Exception wrongly lifts the duty to allow the pass

*logic* · major · medium confidence

The UNLESS clause covers the whole action, "allow the vehicle to pass and maintain lane position and speed". When a motorcycle passes, the rule therefore no longer tells the driver to allow the pass at all. The motorcycle guidance the note describes (moving to one side of the lane) would at most replace the "maintain lane position" part, not the duty to let the vehicle pass. A driving model could read the rule as freeing it to resist a motorcycle's pass.

- Fix: Drop the exception from this rule. Write the motorcycle case as a separate rule, cited to 13.41, that keeps the duty to allow the pass, e.g. "WHEN a motorcycle is passing the DRIVER, the DRIVER MUST allow the motorcycle to pass and stay in the lane…", following what 13.41 actually says.
- **Triage: fixed as proposed.** New, and valid: the UNLESS lifts the whole action, so a passing motorcycle no longer has to be allowed to pass. Keep the b0 M2 intent but narrow its reach by splitting. BEING-01 becomes "…the DRIVER MUST allow the vehicle to pass and maintain speed." (evidence `10.206`, no exception). New PASS-BEING-10, "Keep lane position when being passed": "WHEN another vehicle is passing the DRIVER OR signals that it plans to pass the DRIVER, the DRIVER MUST maintain lane position, UNLESS the passing vehicle is a motorcycle AND it is possible to move to one side of the lane." Evidence `10.206`, `13.35`, `13.41` (S2-041), vague term "it is possible". Move BEING-01's current note there.

### S2-043. Lowercase 'and' used as a connective in the exception

*grammar* · minor · high confidence

The grammar requires EXCEPTION := FACT { ("AND" | "OR") FACT }. The unless clause joins two facts with lowercase "and" ("is a motorcycle and it is possible…") instead of the AND keyword.

- Fix: If the exception is kept, write "the passing vehicle is a motorcycle AND it is possible to move to one side of the lane".
- **Triage: fixed as proposed.** With no OR in the exception, the keyword AND is the right connective. Write "…is a motorcycle AND it is possible to move to one side of the lane" (in BEING-10 after S2-042).

### S2-044. Note cites rules by incomplete ids

*note* · minor · medium confidence

The note refers to "BEING-06" and "BEING-05" rather than the full ids PASS-BEING-06 and PASS-BEING-05. It also leans on a block (13.41) that is not cited, so a checker cannot verify it from this rule.

- Fix: Use full ids, e.g. "For a passing motorcycle, see PASS-BEING-06 (13.41). PASS-BEING-05 covers a tailgater." Or remove the cross-references once the exception is dropped.
- **Triage: rejected.** Short ids such as BEING-06 are used in notes throughout the set. The uncited-13.41 point is fixed by S2-041.

## PASS-BEING-02: Use turnouts to let traffic pass

> WHEN driving on a two-lane road with a TURNOUT AND cars are behind the DRIVER AND the DRIVER is slower than the cars behind, the DRIVER MUST merge into the TURNOUT to allow the cars behind to pass.

### S2-045. TURNOUT definition embeds the rule's own condition and action

*vocabulary* · minor · low confidence

The vocabulary entry defines TURNOUT as "A special area or lane on some two-lane roads into which slower vehicles merge to let vehicles behind them pass." This builds the rule itself (slower vehicles merge so others can pass) into the definition. The rule then repeats it: "the DRIVER MUST merge into the TURNOUT to allow the cars behind to pass". The definition should say what a turnout is, not what drivers do with it. As written, the term is partly circular. 10.65 only says: "Some two-lane roads have special turnout areas or lanes."

- Fix: Change the TURNOUT definition to: "A special area or lane at the side of some two-lane roads, provided so that vehicles can move out of the travel lane and let following vehicles pass." (evidence ["10.65"]).
- **Triage: rejected.** TURNOUT's definition was restored at a2 S2-054.

### S2-046. Awkward condition wording "the DRIVER is slower"

*clarity* · minor · low confidence

The condition "the DRIVER is slower than the cars behind" compares a person's speed with cars. The sign 10.66 refers to "SLOWER TRAFFIC", that is, the slower vehicle. The meaning is recoverable, but the wording is imprecise for a formal rule.

- Fix: Set when to: "driving on a two-lane road with a TURNOUT AND vehicles are following the DRIVER's vehicle AND the DRIVER's vehicle is travelling slower than the following vehicles". Update statement and the vague_terms to match.
- **Triage: rejected.** Kept at a2 S2-056: the referent is clear.

## PASS-BEING-03: Turnout required with five or more following

> WHEN driving slowly on a two-lane road where passing is unsafe AND five or more vehicles are following the DRIVER, the DRIVER MUST use a TURNOUT to let the other vehicles pass.

### S2-047. Turnout sign cited for the five-vehicle legal requirement

*citation* · minor · low confidence

The rule's specific content (the five-or-more-vehicles condition, the two-lane road, and 'passing is unsafe') comes entirely from 10.67: "You must use a turnout area or lane … there are five or more vehicles following you." The figure 10.66 is the sign "SLOWER TRAFFIC USE TURNOUTS". It states no vehicle count and no unsafe-passing condition. It supports the general instruction that slower traffic should use turnouts (BEING-02, from 10.65) more than this conditional legal rule. Citing it here adds little and blurs which block grounds the rule.

- Fix: Set evidence to ["10.67"]. If the sign is kept, add to the note: "Sign 10.66 'SLOWER TRAFFIC USE TURNOUTS' shows turnouts in use generally; the five-vehicle condition comes from 10.67 only."
- **Triage: rejected.** Low confidence, and the sign shows the turnouts the rule is about.

## PASS-BEING-05: Let a tailgater pass

> WHEN a tailgater is behind the DRIVER, the DRIVER MUST create more space in front, maintain course and speed, then, when safe to do so, merge right into another lane and allow the tailgater to pass.

### S2-048. Key term 'tailgater' is undefined

*vocabulary* · minor · medium confidence

The rule depends on recognising 'a tailgater', and uses the word as both the trigger and the vehicle to be let past. It is lowercase and has no vocabulary entry. The vague_terms entry for the whole condition only says no following distance is given; it does not say who the tailgater is. 15.14 reads: "A tailgater is behind you." The handbook does not define the word, so it should stay vague rather than get an invented distance. Its meaning, a vehicle following too closely behind, should still be explicit so the rule reads the same way every time.

- Fix: Add a self-defined vocabulary entry {"term": "TAILGATER", "definition": "A vehicle following the DRIVER's vehicle too closely from behind.", "evidence": []}. Write 'a TAILGATER is behind the DRIVER' and 'allow the TAILGATER to pass' in when, action and statement. Keep a vague_terms entry explaining that 'too closely' has no distance given.
- **Triage: rejected.** a2 S2-058 chose a vague term over a vocabulary entry for "tailgater".

### S2-049. Lane change assumes another lane exists

*clarity* · minor · low confidence

The action says the DRIVER MUST 'merge right into another lane'. This is unconditional on the presence of a lane to the right. The phrase 'when safe to do so' covers safety, not whether a lane exists. 15.14 says "merge right to change into another lane", which implies a multi-lane road. A model reading only this rule on a single-lane road would be told to do something impossible. The rule does not say that only the first two steps apply there.

- Fix: Add a note: "The merge-right step presupposes another lane to the right; the handbook (15.14) does not say what to do on a road with no such lane beyond creating space and maintaining course and speed."
- **Triage: rejected.** Rejected at a2 S2-059: "when safe to do so" covers it.

## PASS-BEING-06: Make room for passing motorcyclists

> WHEN a MOTORCYCLIST is passing the DRIVER's vehicle AND it is possible, the DRIVER MUST move to one side of the DRIVER's own lane to give the MOTORCYCLIST more room to pass.

### S2-050. Note relies on an uncited block (13.38) for a lane-splitting claim

*note/citation* · minor · medium confidence

The note says "13.38 states that lane sharing with motorcycles (lane splitting) is legal." Block 13.38 is not in the rule's evidence and was not shown for review, so this claim is not supported by the rule's citations. The cited blocks, 13.35 ("To safely share the road with motorcyclists:") and 13.41 ("When possible, move to one side of your lane to give motorcyclists more room to pass."), say nothing about lane splitting being legal. The note also calls the rule "An exception to BEING-01's 'maintain lane position'", which depends on another rule a checker cannot see here. A checker reading this rule alone cannot verify either statement.

- Fix: Either add 13.38 to `evidence`, if it directly explains the situation (a motorcyclist passing within or between lanes), or reduce the note to what the cited blocks support: "Stated as a plain command in a list introduced by 13.35 about sharing the road with motorcyclists; the handbook does not say which side to move to."
- **Triage: rejected.** Settled at a0 C3 and a2 S2-061 (13.38 is mentioned only in the note). Naming BEING-01 is allowed.

## PASS-BEING-07: Bicyclist moves over to let vehicles pass

> WHEN vehicles are following the BICYCLIST AND it is safe, the BICYCLIST SHOULD move to a position that allows vehicles to pass.

### S2-051. Vague position not listed as a vague term

*vague terms* · minor · medium confidence

The action "move to a position that allows vehicles to pass" does not say where the bicyclist should move: how far right, onto a shoulder, or for how long. 13.108 is no more specific: "…the bicyclist should move to a position that allows vehicles to pass." Only "it is safe" is listed in vague_terms, so a driving model is not told that this phrase is also left to judgement.

- Fix: Add to vague_terms: {"term": "a position that allows vehicles to pass", "explanation": "position and distance not specified"}.
- **Triage: fixed as proposed.** An unlisted vague phrase. Add {"term": "a position that allows vehicles to pass", "explanation": "position and distance not specified"} to BEING-07.

## PASS-BEING-08: Pull over and stop for an emergency vehicle

> WHEN an emergency vehicle using a siren and red lights approaches, the DRIVER MUST drive to the right edge of the road and stop until the emergency vehicle has passed, UNLESS the DRIVER is in an INTERSECTION.

### S2-052. Rule waits for only one emergency vehicle

*faithfulness* · minor · medium confidence

The handbook says to stop until all emergency vehicles have passed: 13.44: "stop until the emergency vehicle(s) have passed." The rule says "stop until the emergency vehicle has passed". A driving model could read this as permission to pull out after the first vehicle passes while others are still coming.

- Fix: action: "drive to the right edge of the road and stop until all approaching emergency vehicles have passed" (update statement accordingly).
- **Triage: fixed as proposed.** Faithful to 13.44's "emergency vehicle(s)". BEING-08's action becomes "…and stop until every EMERGENCY VEHICLE has passed", and BEING-09 uses the same wording (S2-055).

### S2-053. Penalty drops the handbook's 'may'

*penalty* · minor · medium confidence

The penalty field reads "A ticket for failure to pull over." The handbook makes the ticket possible, not certain: 13.44: "Failure to pull over may result in a ticket."

- Fix: penalty: "Failure to pull over may result in a ticket."
- **Triage: fixed as proposed.** Faithful to 13.44. Penalty: "Failure to pull over may result in a ticket."

### S2-054. 'emergency vehicle' is a key term left undefined

*vocabulary* · minor · medium confidence

The whole rule depends on which vehicles count, and the handbook lists them: 13.44: "any law enforcement vehicle, fire engine, ambulance, or other emergency vehicle using a siren and red lights". The rule writes "emergency vehicle" in lowercase with no vocabulary entry, so the covered vehicle types are not given.

- Fix: Add vocabulary entry EMERGENCY VEHICLE: "A law enforcement vehicle, fire engine, ambulance, or other emergency vehicle." with evidence ["13.44"]. Then write "WHEN an EMERGENCY VEHICLE using a siren and red lights approaches, …".
- **Triage: fixed as proposed.** 13.44 lists the vehicles, and MTO's gold set also defines EMERGENCY VEHICLE. Add EMERGENCY VEHICLE: "A law enforcement vehicle, fire engine, ambulance, or other emergency vehicle.", evidence `13.44`. Write it in CAPS in BEING-08, BEING-09 and USER-16 ("a stationary EMERGENCY VEHICLE…"), or stage 1 will flag the lowercase uses.

## PASS-BEING-09: Emergency vehicle while in an intersection

> WHEN the DRIVER is in an INTERSECTION AND an emergency vehicle using a siren and red lights approaches, the DRIVER MUST continue through the INTERSECTION, then drive to the right as soon as it is safe and stop.

### S2-055. Stop has no end point: 'until the emergency vehicle(s) have passed' is dropped

*omission* · major · medium confidence

The action ends with "…drive to the right as soon as it is safe and stop" and never says how long to stay stopped. The cited block 13.44 gives the end point: "Drive to the right edge of the road and stop until the emergency vehicle(s) have passed." Without it, a driving model does not know when it may move off again.

- Fix: action: "continue through the INTERSECTION, then drive to the right as soon as it is safe and stop until the emergency vehicle has passed"; update the statement to match.
- **Triage: fixed as proposed.** New, and valid: 13.44 gives the end point and BEING-09 drops it. Action: "…drive to the right as soon as it is safe and stop until every EMERGENCY VEHICLE has passed" (with S2-052/S2-054 wording).

### S2-056. Trigger 'approaches' replaces the handbook's 'when you see'

*faithfulness* · minor · medium confidence

Block 13.48 triggers the rule "when you see an emergency vehicle". The rule's condition says the vehicle "approaches", which is a different condition, and the rule then has to list "approaches" as a vague term.

- Fix: when: "the DRIVER is in an INTERSECTION AND the DRIVER sees an emergency vehicle using a siren and red lights"; update the statement and remove the vague-term entry for "approaches".
- **Triage: fixed as proposed.** Faithful to 13.48's "when you see". BEING-09's condition becomes "the DRIVER is in an INTERSECTION AND the DRIVER sees an EMERGENCY VEHICLE using a siren and red lights", and its vague term "approaches" (added at b0 m4) is dropped, since the word is gone.

### S2-057. 'emergency vehicle' is a key term left undefined

*vocabulary* · minor · medium confidence

Block 13.44 names which vehicles count: "any law enforcement vehicle, fire engine, ambulance, or other emergency vehicle using a siren and red lights". The rule writes "emergency vehicle" in lowercase and leaves it undefined, so the model does not know that police vehicles, fire engines and ambulances are covered.

- Fix: Add a vocabulary entry: EMERGENCY VEHICLE: "A law enforcement vehicle, fire engine, ambulance, or other emergency vehicle", with evidence ["13.44"]. Write the term in capitals in the rule.
- **Triage: fixed as proposed.** Same as S2-054.

## No findings (6 rules)

PASS-MARK-01, PASS-LOC-06, PASS-USER-01, PASS-USER-07, PASS-USER-10, PASS-BEING-04
