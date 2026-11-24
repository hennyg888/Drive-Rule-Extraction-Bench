# Atomic check (stage 2): gold_set\ca\overtaking\a1_format.json

Judge: anthropic/claude-opus-5-5 · run folder: `runs\20261120-195545-check-atomic-overtaking-a2` (requests, responses, findings.jsonl, triage.csv) · 44 rules checked, 0 failed calls · $1.0062

**62 findings** (7 major, 55 minor) in 36 rules.

**Triage:** all 62 findings were triaged. The majors went first, by the reviewer. The minors were then decided against the CA a0 triages, the MTO `allow_list.md` and `error_set.md`, and each finding's confidence: 25 fixed (some partly), 28 rejected, 2 already fixed by a major fix. Fixes were applied to `a2_atomic.json`, which started as an exact copy of `a1_format.json`. Each decision is recorded under its finding as a **Triage** line.
- Two rules were added at the end of the USER group, so no rules were renumbered: PASS-USER-18 (S2-031) and PASS-USER-19 (S2-036).
- Two a0 decisions were reopened on new evidence: LARGE VEHICLE (S2-025) and TURNOUT (S2-054).
- A finding whose fix would duplicate an existing rule is ignored, because the atomic judge sees one rule at a time (S2-041).
- After the fixes there are 46 rules and 15 vocabulary terms (CENTER LEFT TURN LANE added, S2-018).
- Format check (`check_format.py a2_atomic.json --handbook ca --allow-lowercase pass`): no format errors.

## PASS-GEN-01: Judge space before passing near hazards

> WHEN approaching an oncoming vehicle or BICYCLIST OR a hill, curve, INTERSECTION, or road obstruction, the PASSER MUST judge whether there is enough space to pass.

### S2-001. Vague-term explanation cites a one-third-mile distance the rule does not contain

*vague terms / note* · minor · medium confidence

The vague-term explanation for "enough space" reads "no distance given except the one-third mile advice for hills and curves". That distance comes from 10.186: "To safely pass, the hill or curve should be at least one-third of a mile ahead." It is not in this rule, and the `note` is empty, so a reader of the rule alone cannot tell where the figure comes from or how it applies. That sentence is a separate ADVICE rule (SHOULD) and should not be folded into this REQUIREMENT. The explanation should describe only the rule's own words.

- Fix: Change the explanation to "no distance or gap given". Set note to: "10.186 also advises that, to pass safely, the hill or curve should be at least one-third of a mile ahead; that is a separate ADVICE rule."
- **Triage: fixed (partly).** The explanation is now "no distance or gap given". The note only points to GEN-02, instead of restating its advice (MTO `allow_list.md`: the note need not restate a sentence that is a rule of its own).

### S2-002. Lowercase 'or' mixed with the OR keyword makes the condition hard to parse

*grammar* · minor · medium confidence

The `when` field mixes the keyword and plain words: "approaching an oncoming vehicle or BICYCLIST OR a hill, curve, INTERSECTION, or road obstruction". The grammar joins FACTs with the keywords AND or OR. Here one keyword OR sits beside two lowercase "or"s and a comma list, so it is unclear how 'approaching' distributes over the items and which disjunction is the formal one.

- Fix: when: "approaching an oncoming vehicle OR approaching an oncoming BICYCLIST OR approaching a hill OR approaching a curve OR approaching an INTERSECTION OR approaching a road obstruction". Update `statement` to match.
- **Triage: rejected.** Every alternative in the condition is a disjunction, so mixing lowercase "or" inside a fact with the OR keyword changes nothing in meaning (MTO `allow_list.md`: alternatives joined by lowercase "or").

### S2-003. 'approaching' is not listed as vague

*vague terms* · minor · low confidence

The rule is triggered by "approaching" a hazard. Neither the rule nor 10.184 ("whenever you approach:") gives a distance or time at which a driver counts as approaching, so a driving model cannot tell when the judgement is required.

- Fix: Add a vague term: {"term": "approaching", "explanation": "no distance or time given for when the hazard counts as being approached"}.
- **Triage: fixed as proposed.** Added the vague term "approaching", as a0 Q1 did for LOC-01 (MTO S2-029).

## PASS-GEN-02: Hill or curve at least one-third mile ahead

> WHEN planning to pass on a road with a hill or curve ahead, the PASSER SHOULD NOT pass, UNLESS the hill or curve is at least one-third of a mile ahead.

### S2-004. Rule uses PASSER for a driver who is only planning to pass

*vocabulary* · minor · low confidence

The vocabulary defines PASSER as "The driver making a PASS." The condition, however, is "planning to pass on a road with a hill or curve ahead" and the action is "pass". The actor is therefore a driver who has not started a pass, and the rule tells that driver not to begin one. Calling this driver PASSER, the one already making a PASS, is slightly circular and can be misread as applying only once a pass is under way. The handbook frames it as a judgement made on approach: 10.184: "You must judge whether you have enough space to pass whenever you approach:" and 10.186: "A hill, curve… To safely pass, the hill or curve should be at least one-third of a mile ahead."

- Fix: Set actor to "DRIVER" and the when field to "approaching a hill or curve AND considering a PASS". Statement: "WHEN approaching a hill or curve AND considering a PASS, the DRIVER SHOULD NOT begin the PASS, UNLESS the hill or curve is at least one-third of a mile ahead." Add DRIVER and PASS to the vocabulary if they are not already there.
- **Triage: rejected.** PASSER as the actor of rules about deciding whether to pass follows the MTO gold set (CA a0, "Considered and not raised"), and GEN-02's wording was set in a0 G3.

## PASS-GEN-03: Look ahead for conditions before passing

> WHEN about to pass, the PASSER MUST look ahead for road conditions that may cause other vehicles to move into the PASSER's lane.

### S2-005. Lowercase "pass" is used instead of the vocabulary term PASS

*vocabulary* · minor · medium confidence

The condition "about to pass" means the defined manoeuvre that the actor's own definition relies on: PASSER is "The driver making a PASS." The instructions require a word naming a vocabulary term with its defined meaning to be in CAPITALS. Writing it in lowercase leaves unclear whether it means the defined PASS or some looser sense of moving past. The meaning matches 10.187: "Before you pass, look ahead…".

- Fix: Set when to "about to PASS" and statement to "WHEN about to PASS, the PASSER MUST look ahead for road conditions that may cause other vehicles to move into the PASSER's lane."
- **Triage: rejected.** The verb "pass" stays lowercase and only the noun PASS is capitalized (CA a0 V3; MTO `allow_list.md`).

## PASS-GEN-04: Space to return to lane

> WHEN considering a PASS, the PASSER MUST NOT pass, UNLESS there is enough space to return to the PASSER's lane.

### S2-006. "the PASSER's lane" does not say which lane to return to

*clarity* · minor · low confidence

The exception reads "there is enough space to return to the PASSER's lane". During a pass the PASSER is in the passing lane, so "the PASSER's lane" can be read as that lane rather than the lane the pass started from. The handbook's own wording, 10.192: "Unless you have enough space to return to your lane", means the driver's original lane. A driving model reading the rule on its own could misread it.

- Fix: Set unless to "there is enough space to return to the PASSER's original lane". The statement then reads: "WHEN considering a PASS, the PASSER MUST NOT pass, UNLESS there is enough space to return to the PASSER's original lane."
- **Triage: fixed as proposed.** The exception now reads "…to return to the PASSER's original lane" (MTO `error_set.md`: S2-100, "the lane" → "the original lane").

## PASS-GEN-05: Use the left lane to pass

> WHEN driving on a multilane road AND intending to pass, the PASSER MUST use the left lane (the PASSING LANE) to pass.

### S2-007. A lane-choice tip is recorded as an absolute MUST

*strength* · major · medium confidence

The command is introduced as advice. 10.32 says "Here are some tips for choosing a lane:", and 10.33 says "Use the left lane to pass or turn left." The imperative wording alone suggests INSTRUCTION. But the intro sentence frames it as a tip, and 10.46 only describes the lane: it "is used to pass other vehicles". Recording an unconditional MUST makes every pass in any other lane look illegal. The rule's own note admits this conflicts with another rule that allows passing on the right on multilane highways. A driving model reading this rule alone would treat passing in a right lane as forbidden, which the cited blocks do not say.

- Fix: Set force to ADVICE and modal to SHOULD. Statement: "WHEN driving on a multilane road AND intending to pass, the PASSER SHOULD use the PASSING LANE to pass." Change the note to: "Given as a tip for choosing a lane (10.32, 10.33); 10.46 describes the far left lane as the lane used to pass."
- **Triage: fixed as proposed.** GEN-05 is ADVICE / SHOULD again: "WHEN driving on a multilane road AND intending to pass, the PASSER SHOULD use the PASSING LANE to pass." The note is the proposed one, with the a0 N1 link to SIDE-01 kept at the end. This reverses a0 S2.

### S2-008. Lowercase 'left lane' is mixed with the defined term PASSING LANE

*vocabulary* · minor · medium confidence

The action reads "use the left lane (the PASSING LANE)". PASSING LANE is defined as the far left lane closest to the center divider. The lowercase "left lane" could be read as any lane to the left of the driver, which is not the same lane. The parenthetical gives two names for one lane and invites misreading.

- Fix: Change action to "use the PASSING LANE to pass".
- **Triage: no change needed.** Already fixed by S2-007: the action is now "use the PASSING LANE to pass".

### S2-009. The condition repeats what the actor already implies

*clarity* · minor · low confidence

The actor is PASSER, "the driver making a PASS". The condition "AND intending to pass" therefore repeats it, and "to pass" in the action repeats it a third time.

- Fix: Set when to "driving on a multilane road". Statement: "WHEN driving on a multilane road, the PASSER SHOULD use the PASSING LANE to pass."
- **Triage: rejected.** "intending to pass" keeps the rule from reading as a duty to overtake (MTO `error_set.md`: b2 S2-004 moved passing into the condition).

## PASS-MARK-01: Single solid yellow line: no passing

> WHEN there is only one lane of traffic going the DRIVER's direction AND a single solid yellow line is on the DRIVER's side of the road, the DRIVER MUST NOT pass a vehicle in front.

### S2-010. Rule narrows "a solid yellow line" to a "single" solid yellow line

*faithfulness* · major · medium confidence

The rule's condition reads "a single solid yellow line is on the DRIVER's side of the road". The prohibition in the handbook is broader. 10.6: "Do not pass a vehicle in front of you if there is only one lane of traffic going your direction and a solid yellow line on your side of the road." The word "single" comes only from the block's first sentence, which describes how a single solid yellow line marks the centre of a two-way road. The prohibition itself applies to any solid yellow line on the driver's side. That includes the solid half of a solid-and-broken pair, or a double solid line. As written, a driving model could conclude the rule does not apply when the solid line on its side is part of a combined marking. The title has the same narrowing.

- Fix: Set when to: "there is only one lane of traffic going the DRIVER's direction AND a solid yellow line is on the DRIVER's side of the road". Set statement to: "WHEN there is only one lane of traffic going the DRIVER's direction AND a solid yellow line is on the DRIVER's side of the road, the DRIVER MUST NOT pass a vehicle in front." Set title to: "Solid yellow line on your side: no passing". Optionally add a note: "10.6 introduces the single solid yellow centre line, but the prohibition is worded for any solid yellow line on the driver's side."
- **Triage: fixed as proposed**, including the optional note. MARK-01's condition now says "a solid yellow line is on the DRIVER's side of the road", and its title is "Solid yellow line on your side: no passing".

## PASS-MARK-02: Double solid yellow lines: do not cross

> WHEN the road has double solid yellow lines, the DRIVER MUST stay to the right of the double solid yellow lines and not pass over them, UNLESS in a high-occupancy vehicle carpool lane with a designated entrance on the left OR instructed by construction or other signs to drive on the other side of the road because the DRIVER's side is closed or blocked OR turning left across a single set of double yellow lines to enter or exit a driveway or private road or make a U-turn.

### S2-011. Lowercase "pass over" can be misread as the overtaking PASS

*vocabulary* · minor · medium confidence

In an overtaking rule set, the action "stay to the right of the double solid yellow lines and not pass over them" uses "pass" in lowercase to mean "drive across". A reader or model familiar with the overtaking sense of PASS could read it as "not overtake over them". That narrower reading would wrongly allow other crossings. The note already has to explain the word: "'Pass over' here means drive across the lines". The handbook wording is 10.8: "Do not pass over double solid yellow lines." The meaning is drive across, so the rule can say "cross" directly and drop the explanation.

- Fix: Change action to "stay to the right of the double solid yellow lines and not cross them", and update the statement to match. Shorten the note to: "Handbook says 'pass over', meaning drive across the lines; none of the exceptions allows crossing them to overtake. The figure shows a road where the divided section ends (END DIVIDED ROAD sign) and a U-turn is permitted (U-TURN OK sign)."
- **Triage: rejected.** "stay to the right of the double solid yellow lines and not pass over them" is the wording set at a0 M3, and the note explains "pass over".

## PASS-MARK-03: Broken yellow line: passing allowed when safe

> WHEN a broken yellow line is next to the PASSER's driving lane AND it is safe, the PASSER MAY pass.

### S2-012. Note makes an unsupported claim about passing elsewhere

*note* · minor · medium confidence

The note says "the broken line does not restrict passing elsewhere". Block 10.15 says nothing about passing elsewhere: 10.15: "A broken yellow line indicates you may pass if the broken line is next to your driving lane. Only pass when it is safe." The remark is unsupported by the citation. It could also be read as saying passing is unrestricted where there is no broken line, which misleads a checker.

- Fix: Set note to: "Combines the permission with the same block's instruction 'Only pass when it is safe' as a condition; that instruction is worded as a command (INSTRUCTION force)."
- **Triage: rejected.** The note was set at a0 M1 to explain why the modal is MAY, not MAY ONLY. A note may give a reading.

### S2-013. The PASS action is written in lowercase

*vocabulary* · minor · medium confidence

The vocabulary defines PASSER as "The driver making a PASS", so PASS is a defined term. The rule's action "pass" names that same manoeuvre but is written in lowercase, which breaks the instruction to write defined terms in CAPITALS. There is also some circularity: the permission is addressed to a PASSER, who is by definition already making a PASS. DRIVER would be the clearer actor for a rule about whether a pass is allowed.

- Fix: Set action to "PASS" and statement to "WHEN a broken yellow line is next to the PASSER's driving lane AND it is safe, the PASSER MAY PASS." Alternatively, use actor "DRIVER" with statement "WHEN a broken yellow line is next to the DRIVER's driving lane AND it is safe, the DRIVER MAY PASS."
- **Triage: rejected.** Lowercase verb (CA a0 V3) and PASSER actor (MTO gold set).

## PASS-MARK-04: Double solid white lines: no lane change to pass

> WHEN there are double solid white lines next to the DRIVER's lane, the DRIVER MUST NOT cross them to pass.

### S2-014. Lowercase "pass" used while the note relies on the defined term PASS

*vocabulary* · minor · medium confidence

The action reads "cross them to pass" in lowercase. The note justifies the rule with "a PASS is a lane change", using the capitalised term. The inference that makes the rule follow from 10.19 ("Never change lanes over double solid white lines") depends on the defined meaning of PASS, so the statement should use that term. As written, "pass" could be read loosely, for example as passing a slower vehicle within the same lane, which is not a lane change.

- Fix: action: "cross them to make a PASS"; statement: "WHEN there are double solid white lines next to the DRIVER's lane, the DRIVER MUST NOT cross them to make a PASS." Make sure PASS is in the vocabulary as a lane change past a slower vehicle.
- **Triage: fixed (partly).** The casing is unchanged (CA a0 V3). The note no longer relies on PASS being defined as a lane change, which the CA definition does not say: "Inferred: passing here means changing lanes, and 10.19 says …".

### S2-015. Handbook's instruction to wait for a single broken white line is left only in the note

*completeness* · minor · low confidence

10.19 says: "Never change lanes over double solid white lines. Wait until you see a single broken white line." The second sentence tells the driver what to do instead, and the rule leaves it out of the statement. A driving model reading only the statement learns only the prohibition, not that it should wait for a broken line before passing.

- Fix: Add a companion INSTRUCTION rule. Suggested wording: "WHEN there are double solid white lines next to the DRIVER's lane AND the DRIVER wants to make a PASS, the DRIVER MUST wait until there is a single broken white line before changing lanes." Alternatively, mention in the note that this is covered by a separate rule.
- **Triage: rejected.** Low confidence, and the note already records 10.19's "wait until there is a single broken white line".

## PASS-LOC-03: No passing at crossroads and driveways

> WHEN at crossroads or driveways, the PASSER MUST NOT pass.

### S2-016. Missing vague term for the extent of 'at crossroads or driveways'

*vague terms* · minor · medium confidence

The rule keeps the handbook's wording (10.191: "At crossroads and driveways."), but this gives no distance. A driving model cannot tell how far before or after a crossroad or driveway the ban applies. Under the instructions, such open judgements should be listed in `vague_terms`, yet the list is empty.

- Fix: Set vague_terms to [{"term": "at crossroads or driveways", "explanation": "no distance given for how near the crossroad or driveway the ban applies"}].
- **Triage: fixed as proposed.** Added the vague term "at crossroads or driveways" (no distance given), as for "near an intersection" in MTO b0 m3.

### S2-017. Circular actor: PASSER MUST NOT pass

*grammar/vocabulary* · minor · low confidence

PASSER is defined as "The driver making a PASS." A rule saying that the PASSER "MUST NOT pass" is self-contradictory: it addresses someone who is already passing and forbids the act that defines them. The handbook addresses any driver (10.188: "Do not pass:"). In addition, the action "pass" is lowercase although PASS is the defined term.

- Fix: actor: "DRIVER"; action: "PASS"; statement: "WHEN at crossroads or driveways, the DRIVER MUST NOT PASS."
- **Triage: rejected.** PASSER actor (MTO gold set) and lowercase verb (CA a0 V3).

## PASS-LOC-06: No passing in the center left turn lane

> WHEN on a road with a center left turn lane, the DRIVER MUST NOT use the center left turn lane to pass.

### S2-018. Center left turn lane is a key term but not a defined vocabulary term

*vocabulary* · minor · medium confidence

The rule writes "center left turn lane" in lowercase twice and gives it no definition. The handbook defines it in 10.56: "A center left turn lane is located in the middle of a two-way street. It is marked on both sides by two painted lines. The inner line is broken and the outer line is solid." A driving model has to recognise this lane from its markings, so it needs a strict, cited definition.

- Fix: Add a vocabulary entry: {"term": "CENTER LEFT TURN LANE", "definition": "A lane in the middle of a two-way street, marked on each side by two painted lines, the inner broken and the outer solid, used to prepare for and make left turns or U-turns.", "evidence": ["10.56"]}. Then set the statement to: "WHEN on a road with a CENTER LEFT TURN LANE, the DRIVER MUST NOT use the CENTER LEFT TURN LANE to pass."
- **Triage: fixed.** Added CENTER LEFT TURN LANE: "A lane in the middle of a two-way street, marked on each side by two painted lines, the inner broken and the outer solid.", evidence `10.56`. LOC-06 now uses the term. The definition leaves out the proposed usage clause, because a definition gives the thing itself (MTO `error_set.md`: a0 V2, S2-062). MTO has the matching term TWO-WAY LEFT-TURN LANE.

### S2-019. Heading block cited as evidence

*citation* · minor · low confidence

Block 10.55 is only the heading "Center Left Turn Lanes" and states no rule. All of the rule's content comes from 10.56: "…It is not a regular traffic lane or passing lane."

- Fix: Set evidence to ["10.56"].
- **Triage: fixed as proposed.** Evidence is now `10.56`. The prompt lists text blocks, figures and captions as citable, not headings, so the heading 10.55 added at a0 M6 is removed.

## PASS-PROC-01: How to pass on an open highway

> WHEN going to pass on an open highway, the PASSER MUST signal the plan to pass, look over the shoulder to check blind spots, move into the lane used for passing, speed up to pass the vehicle, then signal and return to the original lane.

### S2-020. Lane-change blocks are cited but none of their steps are in the rule

*citation* · minor · medium confidence

The rule cites 10.36–10.42, the general lane-change checklist under "Traffic Lanes". 10.36: "Before you change lanes:". 10.38: "Check your mirrors." 10.39: "Check traffic behind and beside you." 10.42: "Be sure there is enough space for your vehicle in the next lane…". The rule's action draws only on 10.194–10.199: "signal the plan to pass, look over the shoulder to check blind spots, move into the lane used for passing, speed up…, then signal and return". It contains none of the mirror, traffic or space checks. The note says these checks "also apply", but the rule does not state them. The citations therefore point to requirements the rule does not contain, which goes against "Cite only the materials directly relevant to the rule." A checker could wrongly take mirror checks or space checks as part of this rule. The lane-change checks belong to a separate lane-change rule.

- Fix: Set evidence to ["10.194", "10.195", "10.196", "10.197", "10.198", "10.199"]. Shorten the note to: "10.197 says 'the passing lane' without saying which lane on a two-lane road." Leave the lane-change checklist (10.36–10.42) to its own rule. If it is to be part of passing, add its steps to the action explicitly with a note that the rule is inferred from two places.
- **Triage: rejected.** These citations were added on purpose at a0 C5, as MTO b3 S3-003 did for its PROC-01.

## PASS-PROC-02: Never leave the pavement to pass

> WHEN passing, the PASSER MUST NOT drive off the paved or main-traveled part of the road to pass.

### S2-021. Lowercase 'passing'/'to pass' used instead of the defined term PASS

*vocabulary* · minor · medium confidence

The rule set defines PASS, and the actor PASSER is defined as 'The driver making a PASS'. The rule still writes the same act in lowercase twice: 'WHEN passing' and '…road to pass'. Elsewhere in the rule set, lowercase 'pass' could be read more loosely than the defined PASS. The condition 'WHEN passing' also repeats the action's 'to pass', and the actor PASSER already implies it. The meaning is unchanged, but the terms are not used consistently. Handbook 10.204: "Never drive off the paved or main-traveled part of the road to pass."

- Fix: when: "making a PASS"; action: "drive off the paved or main-traveled part of the road to complete the PASS"; statement: "WHEN making a PASS, the PASSER MUST NOT drive off the paved or main-traveled part of the road to complete the PASS."
- **Triage: rejected.** Lowercase verb (CA a0 V3). "WHEN passing" sets when the ban applies.

## PASS-SIDE-01: When passing on the right is allowed

> WHEN an open highway has two or more lanes going in the PASSER's direction OR the DRIVER ahead is turning left and the PASSER can safely pass on the right OR the PASSER is on a one-way street, the PASSER MAY ONLY pass on the right.

### S2-022. Lowercase 'and' inside an OR chain makes the condition ambiguous

*grammar* · minor · medium confidence

The `when` field reads "an open highway has two or more lanes going in the PASSER's direction OR the DRIVER ahead is turning left and the PASSER can safely pass on the right OR the PASSER is on a one-way street". The middle case joins two facts with a lowercase "and", while the grammar only allows the keywords AND/OR between FACTs. Nothing shows that "can safely pass" belongs only to the left-turn case (10.202: "The driver ahead of you is turning left and you can safely pass on the right."). A parser or reader could also take it as one more alternative, or as a requirement for every case.

- Fix: Use the keyword and make the grouping explicit, e.g. when: "an open highway has two or more lanes going in the PASSER's direction OR (the DRIVER ahead is turning left AND the PASSER can safely pass on the right) OR the PASSER is on a one-way street". Alternatively, add a note saying that 'safely' applies only to the left-turn case.
- **Triage: rejected.** This is the grouping fix from a0 M2: one case's parts joined by lowercase "and" inside one fact (MTO `allow_list.md`). The grammar has no brackets.

### S2-023. Cited block's 'never pass on the left' instruction is not accounted for

*note* · minor · medium confidence

Block 10.202 also says: "Never pass on the left if the driver is signaling a left turn." This is a separate INSTRUCTION (MUST NOT) rule. The rule cites the block, but neither the rule nor its note mentions this sentence, so a checker cannot tell whether it was captured elsewhere or missed.

- Fix: Add to the note: "Block 10.202 also states a separate INSTRUCTION: WHEN the DRIVER ahead is signaling a left turn, the PASSER MUST NOT pass on the left; extracted as its own rule." Make sure that rule exists.
- **Triage: rejected.** The sentence is SIDE-02, and the note need not mention other sentences of the cited block that are rules of their own (MTO `allow_list.md`).

## PASS-SIDE-02: No passing on the left of a left-turning vehicle

> WHEN the DRIVER ahead is signaling a left turn, the PASSER MUST NOT pass on the left.

### S2-024. Cites the pass-on-the-right intro, which does not support this prohibition

*citation* · minor · medium confidence

The rule is a prohibition on passing on the left. Block 10.200 reads: "You may pass on the right only when:". That line introduces the conditions for passing on the right, not this prohibition. The prohibition is a standalone sentence in 10.202: "…Never pass on the left if the driver is signaling a left turn." Citing 10.200 links the rule to the pass-on-the-right permission, which it does not draw on.

- Fix: Set evidence to ["10.202"]. Optionally add a note: "Stated in 10.202 after the permission to pass on the right of a left-turning driver; the prohibition is a separate sentence."
- **Triage: rejected.** List lead-ins stay cited with every list item (a0 C2; MTO `allow_list.md`).

## PASS-USER-01: Check a large vehicle's turn signals before passing

> WHEN following a LARGE VEHICLE AND before starting to pass it, the DRIVER MUST look at its turn signals.

### S2-025. LARGE VEHICLE definition adds details the cited block does not give

*vocabulary* · minor · low confidence

The rule depends on LARGE VEHICLE, which is self-defined with no evidence as "A truck, bus or other vehicle much larger than a passenger vehicle". The cited block only says 13.10: "…large vehicles and truck drivers must often swing wide…" and links the problem to vehicle length ("The longer the vehicle, the greater the difference in the length of the turning path"). It does not mention buses and gives no size threshold. The phrase "much larger" is itself vague, so the definition replaces the handbook's open term with another open one. A self-defined entry that adds "bus" and "much larger than a passenger vehicle" may go beyond what the handbook states. This does not change what the rule tells the driver to do.

- Fix: Define the term from the handbook's own wording and mark it as open, e.g. {"term": "LARGE VEHICLE", "definition": "A long vehicle such as a truck, whose rear wheels follow a noticeably shorter path than its front wheels when turning, so that it may swing wide to turn; the handbook gives no size threshold.", "evidence": ["13.10"]}.
- **Triage: fixed (with S2-026 and S2-030).** LARGE VEHICLE is now "A truck or other vehicle much larger than a passenger vehicle; the handbook gives no size threshold." This reopens a0 V5 on new evidence: the CA large-vehicle section (13.8–13.16) never names buses, which have their own section (13.17). The proposed 13.10 turning-path definition was not used, because it defines by a property.

## PASS-USER-02: Pass large vehicles on the left

> WHEN passing a LARGE VEHICLE, the PASSER MUST pass on the left side.

### S2-026. LARGE VEHICLE definition adds content not in the cited blocks

*vocabulary* · minor · medium confidence

The vocabulary entry defines LARGE VEHICLE as "A truck, bus or other vehicle much larger than a passenger vehicle". The cited blocks only speak of "Large vehicles and trucks" (13.12: "Large vehicles and trucks are not as easy to maneuver as passenger vehicles…"). They mention no buses and give no size criterion. "Bus" is therefore not supported by the citations, and "much larger" is a vague threshold presented as if it were a definition. The instructions say not to invent definitions for terms the handbook leaves vague.

- Fix: Change the definition to: "A large vehicle or truck, as the handbook uses the term; the handbook gives no size threshold." Alternatively, keep "large vehicle" in lowercase in the rule and list it in vague_terms with the explanation "no size or vehicle type given".
- **Triage: fixed, see S2-025.** "bus" was removed. "much larger … no size threshold" stays, so the term is visibly left vague.

### S2-027. Action does not say whose left side

*clarity* · minor · low confidence

The action "pass on the left side" does not say whose left side is meant. The handbook says "Always pass a large vehicle on the left side" (13.14), which refers to the large vehicle's left side. The rule's wording is looser than the handbook's.

- Fix: Set action to "pass the LARGE VEHICLE on its left side". The statement becomes: "WHEN passing a LARGE VEHICLE, the PASSER MUST pass the LARGE VEHICLE on its left side."
- **Triage: rejected.** Low confidence, and the referent is clear: the only vehicle in the condition is the LARGE VEHICLE (MTO `allow_list.md`: a pronoun that can only refer to one vehicle).

## PASS-USER-03: Do not linger beside a large vehicle

> WHEN passing a LARGE VEHICLE, the PASSER MUST move ahead of it after passing and not drive next to it longer than needed.

### S2-028. A MUST and a MUST NOT are merged into one MUST action

*grammar* · minor · medium confidence

The action "move ahead of it after passing and not drive next to it longer than needed" puts a prohibition inside a MUST rule. The handbook states it as a "do not" item (13.12: "When driving near large vehicles and trucks, do not:"; 13.14: "Drive next to them longer than you need to"), followed by a separate command ("After you pass the large vehicle or truck, move ahead of it"). The grammar allows one modal per rule. Mixing them hides the MUST NOT and makes the rule harder to check.

- Fix: Split into two rules. (a) when: "driving next to a LARGE VEHICLE", modal: MUST NOT, action: "drive next to it longer than needed", statement: "WHEN driving next to a LARGE VEHICLE, the DRIVER MUST NOT drive next to it longer than needed.", evidence ["13.12","13.14"]. (b) when: "having passed a LARGE VEHICLE", modal: MUST, action: "move ahead of it", statement: "WHEN having passed a LARGE VEHICLE, the PASSER MUST move ahead of it.", evidence ["13.14"].
- **Triage: rejected.** Positive first, negated last in one MUST action is an accepted pattern (a0 M4; MTO `allow_list.md`).

### S2-029. Prohibition on lingering is narrowed from 'driving near' to 'passing'

*scope* · minor · medium confidence

The handbook applies the no-lingering instruction to any driver near a large vehicle: 13.12 "When driving near large vehicles and trucks, do not:" … 13.14 "Drive next to them longer than you need to." The rule limits it to "passing a LARGE VEHICLE" with actor PASSER. A driver who rides alongside a truck without passing it is therefore not covered. In addition, the condition "WHEN passing" sits awkwardly with the action "after passing".

- Fix: Use when: "driving next to a LARGE VEHICLE" and actor: "DRIVER" for the lingering part. Keep the PASSER actor only for the "move ahead of it after passing" part, as in the split above.
- **Triage: rejected.** Out of scope: driving alongside a vehicle without overtaking it is not passing (MTO `allow_list.md`: S3-004).

### S2-030. LARGE VEHICLE definition adds content not in the cited blocks

*vocabulary* · minor · low confidence

The self-made definition reads "A truck, bus or other vehicle much larger than a passenger vehicle". The cited blocks say only "Large vehicles and trucks are not as easy to maneuver as passenger vehicles" (13.12). They do not mention buses, and "much larger" is itself vague. The definition widens the term beyond what the cited text supports.

- Fix: Define it as: "A large vehicle or truck, as referred to by the handbook; no size threshold is given." Alternatively, list "LARGE VEHICLE" as deliberately vague and note it in vague_terms.
- **Triage: fixed, see S2-025.

## PASS-USER-04: Passing a stopped bus, streetcar or trolley

> WHEN a bus, streetcar, or trolley is stopped at a SAFETY ZONE or traffic light, the DRIVER MAY ONLY pass it at no more than 10 mph and without driving through any SAFETY ZONE.

### S2-031. Absolute safety-zone ban weakened into a condition on a permission

*strength* · major · high confidence

The rule folds "without driving through any SAFETY ZONE" into a PERMISSION / MAY ONLY rule about passing. The handbook states this as an unconditional command, not as a limit on a permission: 13.18: "Do not drive through a safety zone under any condition." That is INSTRUCTION force (MUST NOT), and it applies whether or not a bus is stopped or the driver is passing. As written, the ban reads as one of the terms of an allowance, and only while a bus, streetcar or trolley is stopped. The note acknowledges this but does not fix it. Only the 10 mph limit comes from the permission in 13.19: "you may pass at no more than 10 mph."

- Fix: Split into two rules. (1) PASS-USER-04, force PERMISSION, modal MAY ONLY: when "a bus, streetcar, or trolley is stopped at a SAFETY ZONE or traffic light", action "pass it at no more than 10 mph". Statement: "WHEN a bus, streetcar, or trolley is stopped at a SAFETY ZONE or traffic light, the DRIVER MAY ONLY pass it at no more than 10 mph." Evidence: ["13.19", "13.20"]. (2) New rule, force INSTRUCTION, modal MUST NOT: when "approaching or passing a SAFETY ZONE", action "drive through the SAFETY ZONE". Statement: "WHEN approaching or passing a SAFETY ZONE, the DRIVER MUST NOT drive through the SAFETY ZONE." Evidence: ["13.18", "13.21"]. Note: "13.18 says 'under any condition'."
- **Triage: fixed as proposed (split).** USER-04 is now "…the DRIVER MAY ONLY pass it at no more than 10 mph.", with evidence `13.19`, `13.20`. Its note explains the MAY ONLY reading and points to the new rule. New **PASS-USER-18**, "Never drive through a safety zone": INSTRUCTION / MUST NOT, "WHEN approaching or passing a SAFETY ZONE, the DRIVER MUST NOT drive through the SAFETY ZONE.", evidence `13.18`, `13.21`. Its note quotes "under any condition" and carries the marking difference (13.18 vs 13.21) moved from USER-04. This undoes the a0 O3 fold-in.

### S2-032. SAFETY ZONE definition omits how the zone is marked

*vocabulary* · minor · medium confidence

The vocabulary entry defines SAFETY ZONE only by its purpose: "A space set aside for pedestrians waiting…". A driving model cannot recognise a zone from that. The cited blocks say how zones are marked. 13.18: "marked by raised buttons or markers on a road". 13.21: "Safe Zones are marked by dotted white lines." The figure 13.20 shows the dotted outline. Right now the markings appear only in the rule's note.

- Fix: Change the definition to: "A space on the road set aside for pedestrians waiting for buses, streetcars, and trolleys, marked by raised buttons or markers or by dotted white lines." Evidence: ["13.18", "13.21", "13.20"].
- **Triage: rejected.** At a0 V5 the markings were taken out of the definition on purpose, because 13.18 and 13.21 disagree. The difference is recorded in USER-18's note.

## PASS-USER-05: No passing light rail or streetcar on the left

> WHEN overtaking a LIGHT RAIL VEHICLE, whether it is moving or standing, the PASSER MUST NOT pass it on the left side, UNLESS the tracks are so close to the right side that the PASSER's vehicle cannot pass on the right OR the PASSER is on a one-way street OR a traffic officer directs the PASSER to pass on the left.

### S2-033. Note depends on another rule instead of standing alone

*note* · minor · medium confidence

The note says: "Can call for passing on the right on a two-way street that is not one of SIDE-01's cases; SIDE-01's list does not mention this case." It only makes sense to someone who has rule SIDE-01 at hand, and it comments on that rule's coverage rather than on this rule's source. None of the cited blocks (13.22–13.25) mention SIDE-01's list. The instructions ask for each rule to stand on its own and for notes to tell a checker something about this rule.

- Fix: Replace the note with: "Taken from 13.22 (the prohibition) and its list of exceptions 13.23–13.25. In practice the prohibition means passing a light rail vehicle or streetcar on the right on two-way streets, but the handbook states only the prohibition on passing on the left."
- **Triage: rejected.** A note may name another rule (MTO `allow_list.md`). This link was added at a0 N1.

### S2-034. 'passenger vehicle' wording replaced by 'PASSER's vehicle'

*faithfulness* · minor · low confidence

13.23 reads: "the tracks are so close to the right side that the passenger vehicle cannot pass on the right." The rule says "the PASSER's vehicle cannot pass on the right". This drops the handbook's word "passenger". That word could be read as limiting the exception to passenger vehicles, so dropping it silently settles a possible ambiguity.

- Fix: Keep the handbook wording, e.g. unless: "the tracks are so close to the right side that the passenger vehicle cannot pass on the right OR the PASSER is on a one-way street OR a traffic officer directs the PASSER to pass on the left". Alternatively, add a note that the handbook says "passenger vehicle" and that the rule reads it as the PASSER's vehicle.
- **Triage: rejected.** Low confidence, and the wording was set at a0 G4.

## PASS-USER-06: Never pass a motorcycle in the same lane

> WHEN a MOTORCYCLIST is in the same lane as the DRIVER, the DRIVER MUST NOT try to pass the motorcycle in that lane.

### S2-035. Condition names the MOTORCYCLIST but the action names the motorcycle

*vocabulary* · minor · low confidence

The condition reads "a MOTORCYCLIST is in the same lane as the DRIVER", but the action reads "try to pass the motorcycle in that lane". The rule switches from the defined person (MOTORCYCLIST) to an undefined object ("the motorcycle") that the condition never introduced. The handbook speaks of the vehicle throughout, 13.39: "Never try to pass a motorcycle in the same lane as you." The meaning is clear, but the wording is inconsistent.

- Fix: Make both parts refer to the same entity. Set when: "a motorcycle is in the same lane as the DRIVER" and statement: "WHEN a motorcycle is in the same lane as the DRIVER, the DRIVER MUST NOT try to pass the motorcycle in that lane." Alternatively, keep MOTORCYCLIST in both parts by setting action: "try to pass the MOTORCYCLIST in that lane".
- **Triage: rejected.** Low confidence, and two names for the same road user are fine where the referent is clear (MTO `allow_list.md`: b2 S2-012).

## PASS-USER-07: Passing a bicyclist by changing lanes

> WHEN passing a BICYCLIST in the travel lane by changing to another lane, the PASSER MUST pass safely, leave space between the vehicle and the BICYCLIST, then return to the original lane.

### S2-036. Leave-space instruction limited to lane-change passes

*scope* · major · medium confidence

The rule ties "leave space between the vehicle and the BICYCLIST" to the condition "passing a BICYCLIST in the travel lane by changing to another lane". In 13.110, "In this case" governs only the sentence "pass safely, then return to your original lane". The next sentence, "Leave space between your vehicle and the bicyclist.", is a separate, unqualified command. The Right/Wrong figures (13.111 and 13.113) also illustrate leaving room versus not leaving room, not lane changing as such. As written, a driving model could conclude it need not leave space when it passes a cyclist without fully changing lanes. The vague-term explanation "no distance given when changing lanes" repeats this narrowing.

- Fix: Split into two rules. (1) PASS-USER-07: when "passing a BICYCLIST in the travel lane by changing to another lane", action "pass safely, then return to the original lane", evidence ["13.110"], vague term "safely". (2) New rule: "WHEN passing a BICYCLIST, the PASSER MUST leave space between the vehicle and the BICYCLIST.", force INSTRUCTION, evidence ["13.110", "13.111", "13.112", "13.113", "13.114"], vague term "leave space" with explanation "no distance given", and a note on the Right/Wrong figures. Alternatively, keep a single rule and add a note saying the leave-space sentence may apply to all passes of a bicyclist.
- **Triage: fixed as proposed (split).** USER-07 is now "…the PASSER MUST pass safely, then return to the original lane.", with evidence `13.110` and vague term "safely". New **PASS-USER-19**, "Leave space when passing a bicyclist": INSTRUCTION / MUST, "WHEN passing a BICYCLIST, the PASSER MUST leave space between the vehicle and the BICYCLIST.", vague term "leave space" (no distance given), evidence `13.110`–`13.114`. Its note describes the Right/Wrong figures and links USER-08.

## PASS-USER-08: Three feet when passing a bicyclist in the same lane

> WHEN about to pass a BICYCLIST AND the PASSER cannot change lanes, the PASSER MUST allow at least three feet between the vehicle and the BICYCLIST, and not pass until three feet of clearance can be given.

### S2-037. A prohibition is folded into a MUST action

*grammar* · minor · medium confidence

The action "allow at least three feet between the vehicle and the BICYCLIST, and not pass until three feet of clearance can be given" combines a positive duty with a prohibition under a single MUST. 13.115 states the second part as its own conditional command: "If you cannot give three feet of space, do not pass the cyclist until three feet of clearance can be given." Writing it as "MUST … not pass" hides a MUST NOT inside a MUST action. A checker reading the modal field alone would miss the prohibition.

- Fix: Keep the clearance duty here, with action "allow at least three feet between the vehicle and the BICYCLIST". Add a separate rule: "WHEN about to pass a BICYCLIST AND the PASSER cannot change lanes AND three feet of clearance cannot be given, the PASSER MUST NOT pass the BICYCLIST, UNLESS three feet of clearance can be given." Alternatively, put the 'until' into the when field: "WHEN three feet of clearance cannot yet be given, the PASSER MUST NOT pass the BICYCLIST." Cite 13.115.
- **Triage: rejected.** Positive first, negated last in one MUST action is an accepted pattern (MTO `allow_list.md`). A separate MUST NOT rule would repeat it.

### S2-038. PASSER may clash with a passer who cannot change lanes

*vocabulary* · minor · low confidence

The actor is PASSER, defined as "The driver making a PASS." In this rule set PASS appears to be defined, as in the template, as "Changing lanes to move past a slower vehicle". The rule's condition "the PASSER cannot change lanes" then describes a driver who is passing without changing lanes, which that definition does not cover. 13.115 simply speaks of "you", the driver.

- Fix: Use the actor "DRIVER" (defined, or lowercase "driver"). The when field becomes "about to pass a BICYCLIST AND the DRIVER cannot change lanes". Alternatively, confirm that PASS covers moving past a road user within the same lane.
- **Triage: rejected.** The premise is wrong. The CA PASS definition ("Moving past a slower or stopped vehicle or road user…") does not require a lane change.

## PASS-USER-09: Do not squeeze bicyclists into parked cars

> WHEN passing a BICYCLIST, the PASSER MUST give the BICYCLIST enough space so the BICYCLIST is not forced into parked vehicles or open vehicle doors.

### S2-039. Vague-term explanation points to a rule outside this one

*vague terms* · minor · medium confidence

The vague-term explanation for "enough space" reads "no distance given beyond the three-foot rule". This rule does not state a three-foot rule, so the explanation relies on a separate rule. It could also suggest that three feet is enough to meet this rule. The handbook item 13.116, "Give bicyclists enough space so they are not forced into parked vehicles or open vehicle doors", gives no distance of its own.

- Fix: Change the explanation to: "no distance given; how much space depends on the parked vehicles and opening doors".
- **Triage: fixed as proposed.** The explanation is now "no distance given; how much space depends on the parked vehicles and opening doors". This is the same kind of fix as S2-001.

### S2-040. Condition drops the 'cannot change lanes' setting of the introducing passage

*condition* · minor · low confidence

Item 13.116 is part of the list introduced by 13.115: "When you cannot change lanes to pass a bicyclist, allow at least three feet … Remember to:". The rule's condition, "passing a BICYCLIST", is broader than that setting, and no note records the choice. A checker cannot tell whether the list item was meant to apply only when the passer stays in the same lane.

- Fix: Either narrow the condition to: when "passing a BICYCLIST without changing lanes". Or add a note: "13.116 is a 'Remember to' item under 13.115, which concerns passing a bicyclist when a lane change is not possible; applied here to all passes of bicyclists."
- **Triage: rejected.** The lead-in to a list is not a condition of each item (MTO `allow_list.md`: a0 M4).

## PASS-USER-11: One danger at a time: oncoming vehicle and bicyclist

> WHEN on a two-lane road with an oncoming vehicle to the left AND a BICYCLIST ahead to the right, the DRIVER MUST slow down, let the oncoming vehicle pass, then move left to allow at least three feet to pass the BICYCLIST, and not drive between the vehicle and the BICYCLIST.

### S2-041. Steady-flow exception from the same block is missing

*exception* · major · medium confidence

The rule says the DRIVER "MUST slow down, let the oncoming vehicle pass, then move left…" with no exception. The same cited block qualifies this for a different case: 17.13: "If there is a steady flow of oncoming vehicles, use as much of the left lane as you safely can to pass the bicyclist." With a continuous stream of oncoming traffic there is no gap to wait for. Read alone, the rule tells the model to wait for the oncoming traffic to clear, and to keep three feet from the bicyclist, in a situation where the handbook gives a different instruction.

- Fix: Set unless to "there is a steady flow of oncoming vehicles" and update the statement to match. Write a separate rule, also citing 17.13: "WHEN on a two-lane road AND passing a BICYCLIST ahead to the right AND there is a steady flow of oncoming vehicles, the DRIVER MUST use as much of the left lane as the DRIVER safely can to pass the BICYCLIST." List "as much … as the DRIVER safely can" as a vague term in that rule.
- **Triage: ignored.** The proposed separate rule duplicates the existing PASS-USER-12, which already covers the steady-flow case from 17.13. The atomic judge sees one rule at a time, so it could not know that. USER-11 is unchanged.

### S2-042. 17.12 cited although it states no part of this rule

*citation* · minor · medium confidence

17.12 only introduces the topic: "Sometimes dangers will be on both sides of the road at the same time. For example, parked cars to the right and oncoming cars to the left." It has nothing about bicyclists, slowing, or the three-foot gap. The whole rule comes from 17.13.

- Fix: Change evidence to ["17.13"].
- **Triage: fixed as proposed.** Evidence is now `17.13` (MTO `error_set.md`: a cited block that does not support the rule).

### S2-043. "plenty of space" dropped from the action

*faithfulness* · minor · low confidence

17.13 says "move to the left to allow plenty of space (at least three feet) to pass the bicyclist". The rule keeps only "at least three feet". This makes the three feet read as the whole target, while the handbook treats it as a minimum within "plenty of space".

- Fix: Set action to "slow down, let the oncoming vehicle pass, then move left to allow plenty of space (at least three feet) to pass the BICYCLIST, and not drive between the vehicle and the BICYCLIST", update the statement to match, and add the vague term {"term": "plenty of space", "explanation": "only a minimum is given"}.
- **Triage: fixed as proposed.** The action now says "move left to allow plenty of space (at least three feet) to pass the BICYCLIST", with the vague term "plenty of space" (only a minimum is given) (MTO `error_set.md`: part of a handbook sentence left out).

## PASS-USER-12: Steady oncoming flow when passing a bicyclist

> WHEN passing a BICYCLIST on a two-lane road AND there is a steady flow of oncoming vehicles, the PASSER MUST use as much of the left lane as the PASSER safely can.

### S2-044. Note relies on a block that is not cited

*citation* · minor · medium confidence

The note says the rule "Does not relax USER-08: if three feet cannot be given, do not pass the BICYCLIST (13.115)." Block 13.115 is not in `evidence`, and the cited block 17.13 does not say this. 17.13 only says "move to the left to allow plenty of space (at least three feet) to pass the bicyclist" and "If there is a steady flow of oncoming vehicles, use as much of the left lane as you safely can to pass the bicyclist." The cited block therefore does not support the limit the note asserts. 17.13 does support the three-feet context, but the note does not point to it.

- Fix: Point the note at the cited block instead, for example: "In 17.13 this sentence follows the advice to allow at least three feet when passing the bicyclist; the handbook does not say the three-feet space is waived in steady oncoming traffic." If the cross-reference to 13.115 is kept, add "13.115" to `evidence`.
- **Triage: rejected.** Something mentioned only in a note needs no citation (MTO `allow_list.md`).

### S2-045. "left lane" on a two-lane road is ambiguous and not flagged

*vague terms* · minor · low confidence

On a two-lane road, "the left lane" is the oncoming lane. The action "use as much of the left lane as the PASSER safely can" could be read as telling the driver to move into the lane of a steady stream of oncoming traffic. The words come from the handbook (17.13: "use as much of the left lane as you safely can"). However, the only vague-term entry covers the amount ("amount not given"). It does not cover which lane is meant or how far into the oncoming lane the driver may go. A driving model reading only this rule could misread it.

- Fix: Add a note: "On a two-lane road the 'left lane' is the lane used by oncoming traffic; the handbook leaves to judgement how far into it the PASSER may move while oncoming vehicles are present." Alternatively, widen the vague-term explanation to: "how far into the oncoming lane not given; depends on gaps in oncoming traffic".
- **Triage: fixed (explanation option).** The explanation is now "amount not given; on a two-lane road the left lane is the oncoming lane, and how far into it is left to judgement".

## PASS-USER-13: Follow a bicyclist at a safe distance

> WHEN behind a BICYCLIST in a travel lane who is not able to be passed, the DRIVER SHOULD follow at a safe distance.

### S2-046. Condition rests on blocks that are not cited

*citation* · major · high confidence

The only cited block, 13.108, says just: "Drivers should follow at a safe distance. When it is safe, the bicyclist should move to a position that allows vehicles to pass." It does not say "in a travel lane" or that the bicyclist "is not able to be passed". The note admits the condition is inferred from the preceding list (13.101-13.107) of reasons a bicyclist may ride away from the right edge. Those blocks are not cited. As cited, the rule's condition is not supported by its citations.

- Fix: Add the blocks the condition comes from to evidence: the list 13.101-13.107 and the sentence that introduces it. Keep 13.108.
- **Triage: fixed as proposed.** USER-13's evidence is now `13.101`–`13.108` (the lead-in, the list and the original block).

### S2-047. Condition paraphrases the handbook's situation in invented, ambiguous words

*faithfulness* · minor · medium confidence

"behind a BICYCLIST in a travel lane who is not able to be passed" swaps the handbook's situation (a bicyclist riding away from the right edge for one of the listed reasons) for the extractor's own phrase "not able to be passed". The rule then lists that phrase as a vague term. The wording is also grammatically unclear: "who" could refer to the lane or to the bicyclist. It is also unclear whether the driver could not pass because of the bicyclist's lane position or for other reasons. A driving model cannot tell when the condition holds.

- Fix: when: "behind a BICYCLIST who is riding away from the right edge of the travel lane for one of the reasons the handbook lists, so that the DRIVER cannot safely pass". Statement: "WHEN behind a BICYCLIST who is riding away from the right edge of the travel lane for one of the reasons the handbook lists, so that the DRIVER cannot safely pass, the DRIVER SHOULD follow at a safe distance." Replace the vague term with {"term":"cannot safely pass","explanation":"no criteria given"}.
- **Triage: rejected.** USER-13's condition was settled at a0 K2 (note option) and its citations at a2 S2-046. The proposed condition would refer to the list in words ("for one of the reasons the handbook lists").

## PASS-USER-14: Bicyclist may leave the right edge to pass

> WHEN passing a vehicle or another bicycle going in the same direction, the BICYCLIST travelling slower than the flow of traffic MAY ride away from the right curb or edge of the road.

### S2-048. Exception to a requirement is recast as a separate PERMISSION rule

*strength* · major · medium confidence

The handbook states one REQUIREMENT with an exception. 13.101: "Bicyclists traveling slower than the flow of traffic must ride as close as possible to the right curb or edge of the road, unless:". 13.102 then lists "Passing a vehicle or another bicycle in the same direction." No block uses "may" or "you can", so force PERMISSION and modal MAY have no basis in the handbook's wording. The instructions say to keep a rule's exceptions with it as one entry and not to split one rule into pieces. Here the exception has been split off as a free-standing permission, and the note even admits it is "Stated as an exception to the requirement".

- Fix: Fold this into the requirement rule. Use force "REQUIREMENT", modal "MUST", actor "BICYCLIST", when "travelling slower than the flow of traffic", action "ride as close as possible to the right curb or edge of the road", and unless "passing a vehicle or another bicycle going in the same direction". The statement becomes: "WHEN travelling slower than the flow of traffic, the BICYCLIST MUST ride as close as possible to the right curb or edge of the road, UNLESS passing a vehicle or another bicycle going in the same direction." Set vague_terms to [{"term":"as close as possible","explanation":"no distance given"}]. Keep the evidence ["13.101","13.102"]. If a separate requirement rule already exists, drop this one and make sure that rule carries the UNLESS clause.
- **Triage: fixed as proposed.** USER-14 is now the requirement with its passing exception: "WHEN travelling slower than the flow of traffic, the BICYCLIST MUST ride as close as possible to the right curb or edge of the road, UNLESS passing a vehicle or another bicycle going in the same direction." REQUIREMENT / MUST, vague term "as close as possible", evidence `13.101`, `13.102`, title "Bicyclist keeps right unless passing". Only the passing exception is included. The note says the other exceptions in 13.103–13.107 are outside the overtaking topic. No separate requirement rule existed, so nothing was dropped.

### S2-049. "ride away from the right curb" overstates what the exception allows

*faithfulness* · minor · medium confidence

The handbook only lifts the duty to ride "as close as possible to the right curb or edge of the road" (13.101) while passing (13.102). The action "ride away from the right curb or edge of the road" reads as a positive permission to move away from the edge, with no limit on how far. That wording is the extractor's own, not the handbook's.

- Fix: If kept as a separate rule, use the action "not ride as close as possible to the right curb or edge of the road", or better, merge the rule as described in the other finding.
- **Triage: no change needed.** Already fixed by S2-048: USER-14 is now the requirement with its passing exception.

## PASS-USER-15: Emergency flashers ahead: pass carefully

> WHEN a vehicle's emergency flashers are seen ahead, the DRIVER MUST slow down and pass carefully.

### S2-050. Action can be read as an order to pass the flashing vehicle

*ambiguity* · minor · low confidence

The rule's action, "slow down and pass carefully", sits under MUST. A driving model could read this as an obligation to pass the vehicle with flashers. The handbook only says how to pass, not that the driver has to: 19.25: "If you see a vehicle's emergency flashers ahead, slow down. There may be a collision or other road emergency. Pass carefully." The vehicle may be stopped in a place where passing is not possible or not safe, so the driver may need to stop or wait instead. The handbook's "pass carefully" is a manner requirement that applies when the driver goes past.

- Fix: Change action to "slow down and, when going past the vehicle, pass carefully". The statement then reads: "WHEN a vehicle's emergency flashers are seen ahead, the DRIVER MUST slow down and, when going past the vehicle, pass carefully." Alternatively, add to the note: "'Pass carefully' governs how to go past; the handbook does not require passing."
- **Triage: fixed as proposed.** The action is now "slow down and, when going past the vehicle, pass carefully" (MTO `error_set.md`: b2 S2-004, wording that reads as a duty to pass).

## PASS-USER-17: Do not pass the patrol car during a traffic break

> WHEN a law enforcement TRAFFIC BREAK is in progress ahead, the DRIVER SHOULD NOT drive past the patrol vehicle.

### S2-051. TRAFFIC BREAK definition adds a purpose the cited block does not state

*vocabulary* · minor · medium confidence

The vocabulary entry defines TRAFFIC BREAK as a manoeuvre in which an officer weaves across lanes "to slow or stop traffic". The only cited block stops before giving the purpose: 15.147: "During a traffic break, the officer turns on their emergency lights and slowly weaves across lanes. Law enforcement uses traffic breaks to:". The purpose clause is not supported by this citation. It may come from the list items that follow, but those are not cited.

- Fix: Either cite the list items that state the purpose of traffic breaks, or shorten the definition to: "A law enforcement manoeuvre in which an officer turns on their emergency lights and slowly weaves across lanes."
- **Triage: fixed as proposed (shorter definition).** TRAFFIC BREAK is now "A law enforcement manoeuvre in which an officer turns on their emergency lights and slowly weaves across lanes."

### S2-052. Redundant qualifier "law enforcement" before a defined term

*wording* · minor · medium confidence

The condition reads "a law enforcement TRAFFIC BREAK is in progress ahead". By its vocabulary definition, TRAFFIC BREAK is already a law enforcement manoeuvre. The extra qualifier is redundant, and it suggests there could be another kind of TRAFFIC BREAK.

- Fix: when: "a TRAFFIC BREAK is in progress ahead"; statement: "WHEN a TRAFFIC BREAK is in progress ahead, the DRIVER SHOULD NOT drive past the patrol vehicle."
- **Triage: fixed as proposed.** The condition is now "a TRAFFIC BREAK is in progress ahead".

## PASS-BEING-01: Allow the pass; keep lane and speed

> WHEN a vehicle is passing the DRIVER OR signals that it plans to pass, the DRIVER being passed MUST allow the vehicle to pass and maintain lane position and speed.

### S2-053. Actor 'DRIVER being passed' does not fit the 'signals that it plans to pass' case

*actor* · minor · medium confidence

The handbook applies the rule in two cases. 10.206: "If a vehicle is passing you or signals that they plan on passing, allow the vehicle to pass." The second case is before any pass has begun, so the driver is not yet being passed. The actor "DRIVER being passed" therefore fits only the first case. The condition also refers to the actor by a different name, "the DRIVER", which makes the wording inconsistent. A reader could take the actor qualifier to mean the rule only applies once the pass is under way.

- Fix: Set actor to "DRIVER". Set statement to "WHEN another vehicle is passing the DRIVER OR signals that it plans to pass the DRIVER, the DRIVER MUST allow the vehicle to pass and maintain lane position and speed." Set when to "another vehicle is passing the DRIVER OR signals that it plans to pass the DRIVER".
- **Triage: fixed as proposed.** The actor is DRIVER, and the condition is "another vehicle is passing the DRIVER OR signals that it plans to pass the DRIVER" (MTO `error_set.md`: S2-089, whose vehicle is being passed).

## PASS-BEING-02: Use turnouts to let traffic pass

> WHEN driving on a two-lane road with a TURNOUT AND cars are behind the DRIVER AND the DRIVER is slower than the cars behind, the DRIVER MUST merge into the TURNOUT to allow the cars behind to pass.

### S2-054. TURNOUT definition does not say what a turnout is for

*vocabulary* · minor · medium confidence

The vocabulary defines TURNOUT only as "A special area or lane on some two-lane roads." That does not tell a driving model how to recognise a turnout or what it is for. The cited block gives its function: 10.65: "Merge into these areas or lanes to allow cars behind you to pass." As defined, the term could cover any special area, such as a parking area or bus bay.

- Fix: Change the definition to: "A special area or lane at the side of some two-lane roads into which slower vehicles merge to let following vehicles pass." Keep evidence ["10.65"].
- **Triage: fixed.** TURNOUT is back to "A special area or lane on some two-lane roads into which slower vehicles merge to let vehicles behind them pass." This reopens a0 V5 on new evidence: without its use, the definition does not tell a turnout from other roadside areas. MTO allows definitions that describe use (MTO `allow_list.md`: b0 m9, PASSING LANE).

### S2-055. Sign 10.66 may be regulatory but force is not discussed

*strength* · minor · low confidence

The rule takes its slower-traffic condition from sign 10.66: "SLOWER TRAFFIC USE TURNOUTS". It is a white rectangular sign, which is the regulatory style. Under the instructions, a regulatory sign gives force REQUIREMENT. The rule records force INSTRUCTION based only on the plain command in 10.65. The modal MUST is the same either way, but the instructions say to record the stronger wording when two sources word the same rule differently, and to say so in the note.

- Fix: Either set force to REQUIREMENT and add to the note: "Sign 10.66 is a regulatory sign; 10.65 words the same rule as a plain command." Or keep INSTRUCTION and add a note explaining why the sign is not treated as regulatory.
- **Triage: fixed (REQUIREMENT).** 12.85 says the white rectangular sign "Communicates many important rules you must obey", and sign 10.66 is one. BEING-02 is now REQUIREMENT / MUST, 12.85 is cited, and the note records the stronger wording (MTO `error_set.md`: S2-035, the block that gives regulatory signs their force).

### S2-056. "cars are behind the DRIVER" is vague but not listed

*vague terms* · minor · low confidence

The condition "cars are behind the DRIVER" does not say how many cars or how close they must be. The note itself says another rule covers five or more following vehicles. This general rule leaves that judgement open, yet it is not listed in vague_terms. Also, "the DRIVER is slower" describes the driver rather than the vehicle being slower.

- Fix: Change when to: "driving on a two-lane road with a TURNOUT AND cars are behind the DRIVER's vehicle AND the DRIVER's vehicle is slower than the cars behind", and update statement to match. Add the vague term {"term": "cars are behind", "explanation": "no number of cars or following distance given"}.
- **Triage: fixed (partly).** Added the vague term "cars are behind the DRIVER" (no number of cars or following distance given). "the DRIVER is slower" was kept, because the referent is clear.

## PASS-BEING-04: Move right for faster drivers

> WHEN another DRIVER is close behind AND wishes to drive faster, the DRIVER MUST move to the right.

### S2-057. Same term DRIVER names both the following and the acting driver

*clarity* · minor · medium confidence

The statement reads "WHEN another DRIVER is close behind AND wishes to drive faster, the DRIVER MUST move to the right." Both the follower and the actor are called DRIVER, so "close behind" has no explicit reference point: it does not say behind whom. The handbook is clear, 13.144: "When another driver is close behind you and wishes to drive faster, move to the right." The vague-term explanation "does not say how the DRIVER can tell" adds to the confusion, because there DRIVER could mean either driver.

- Fix: when: "another DRIVER is close behind the DRIVER's vehicle AND that other DRIVER wishes to drive faster"; statement: "WHEN another DRIVER is close behind the DRIVER's vehicle AND that other DRIVER wishes to drive faster, the DRIVER MUST move to the right." Change the vague-term explanation for "wishes to drive faster" to: "does not say how the DRIVER ahead can tell what the following driver wants".
- **Triage: fixed as proposed.** The condition is now "another DRIVER is close behind the DRIVER's vehicle AND that other DRIVER wishes to drive faster", and the vague-term explanation names "the DRIVER ahead".

## PASS-BEING-05: Let a tailgater pass

> WHEN a tailgater is behind the DRIVER, the DRIVER MUST create more space in front, maintain course and speed, then, when safe to do so, merge right into another lane and allow the tailgater to pass.

### S2-058. "tailgater" is a key term left undefined and not listed as vague

*vocabulary* · minor · medium confidence

The whole rule is triggered by "a tailgater is behind the DRIVER". The cited block 15.14 says only "A tailgater is behind you" and gives no following distance. The rule neither defines the term in the vocabulary nor lists it in vague_terms. A driving model therefore cannot tell how close a following vehicle must be before the rule applies. The handbook leaves this to the driver's judgement, and the rule does not say so.

- Fix: Add to vague_terms: {"term": "a tailgater is behind the DRIVER", "explanation": "no following distance given for when a vehicle counts as tailgating"}. Alternatively, add a vocabulary entry with empty evidence, for example TAILGATER: "A vehicle following the DRIVER's vehicle too closely." Then write it in capitals in the rule and still note that "too closely" is not quantified.
- **Triage: fixed (vague-term option).** Added the vague term "a tailgater is behind the DRIVER" (no following distance given). No vocabulary entry, because the handbook leaves it to judgement.

### S2-059. Merging right is required even where there is no lane to the right

*condition* · minor · low confidence

The rule says the DRIVER "MUST … merge right into another lane" with no condition that such a lane exists. On a road with one lane in each direction this cannot be done. The handbook's "when safe to do so" (15.14) arguably covers this, but a model reading the rule literally may treat it as an unmet obligation or attempt an unsafe move. The lane-change part depends on there being a lane to move into, and the rule does not make this explicit.

- Fix: Add a note: "The lane change applies only where a lane to the right is available; 'when safe to do so' is read as including this." Alternatively, change the action to: "create more space in front, maintain course and speed, then, when safe to do so and a lane to the right is available, merge right into another lane and allow the tailgater to pass".
- **Triage: rejected.** Low confidence, and "when safe to do so" already covers a road with no lane to the right (MTO `allow_list.md`: a condition already implied).

## PASS-BEING-06: Make room for passing motorcyclists

> WHEN a MOTORCYCLIST is passing AND it is possible, the DRIVER MUST move to one side of the lane to give the MOTORCYCLIST more room to pass.

### S2-060. What the motorcyclist is passing, and which lane, is left unstated

*clarity* · minor · medium confidence

The condition "a MOTORCYCLIST is passing" does not say that the motorcyclist is passing the DRIVER's vehicle. The action "move to one side of the lane" does not say which lane. The handbook is specific on both points. 13.41: "move to one side of your lane to give motorcyclists more room to pass." A model reading only this rule could apply it to any motorcyclist passing anyone, or to some other lane.

- Fix: when: "a MOTORCYCLIST is passing the DRIVER's vehicle AND it is possible"; action: "move to one side of the DRIVER's own lane to give the MOTORCYCLIST more room to pass"; statement: "WHEN a MOTORCYCLIST is passing the DRIVER's vehicle AND it is possible, the DRIVER MUST move to one side of the DRIVER's own lane to give the MOTORCYCLIST more room to pass."
- **Triage: fixed as proposed.** "…is passing the DRIVER's vehicle AND it is possible, … move to one side of the DRIVER's own lane …" (MTO `error_set.md`: S2-089, b2 S2-060).

### S2-061. Note relies on a block that is not cited

*note* · minor · low confidence

The note says "13.38 states that lane sharing with motorcycles (lane splitting) is legal." Block 13.38 is not in the rule's evidence and is not among the blocks shown, so this claim cannot be checked against the rule's citations. It also adds nothing to the rule as stated.

- Fix: Remove the note (set it to ""). Alternatively, if lane sharing is the situation that makes a motorcyclist pass within the driver's lane, cite 13.38 and explain that link in the note.
- **Triage: rejected.** The 13.38 citation was removed on purpose at a0 C3. Something mentioned only in a note needs no citation.

## PASS-BEING-07: Bicyclist moves over to let vehicles pass

> WHEN vehicles are following the BICYCLIST in a travel lane AND it is safe, the BICYCLIST SHOULD move to a position that allows vehicles to pass.

### S2-062. "in a travel lane" is not supported by the cited block

*unsupported condition* · minor · medium confidence

The condition reads "vehicles are following the BICYCLIST in a travel lane". The only cited block says nothing about a travel lane. 13.108: "Drivers should follow at a safe distance. When it is safe, the bicyclist should move to a position that allows vehicles to pass." The phrase may come from surrounding text that is not shown. If so, that text should be cited. If not, it narrows the rule's situation beyond what the block supports.

- Fix: Either cite the block that places the bicyclist in a travel lane, or drop the phrase. Without it: when = "vehicles are following the BICYCLIST AND it is safe"; statement = "WHEN vehicles are following the BICYCLIST AND it is safe, the BICYCLIST SHOULD move to a position that allows vehicles to pass."
- **Triage: fixed as proposed (drop the phrase).** The condition is now "vehicles are following the BICYCLIST AND it is safe".

## No findings (8 rules)

PASS-LOC-01, PASS-LOC-02, PASS-LOC-04, PASS-LOC-05, PASS-USER-10, PASS-USER-16, PASS-COND-01, PASS-BEING-03
