# Atomic check (stage 2): gold_set\mto\overtaking\b1_format.json

Judge: anthropic/claude-opus-5-5 · run folder: `runs\20261117-231220-check-atomic-overtaking-b2` (requests, responses, findings.jsonl, triage.csv) · 54 rules checked, 0 failed calls · $2.9576

Skipped 20 rules already checked: identical to a rule in `gold_set\mto\overtaking\a1_format.json` (ignoring id and number), with the same vocabulary entries. PASS-GEN-01, PASS-GEN-03, PASS-GEN-07, PASS-PROC-04, PASS-PROC-07, PASS-NIGHT-02, PASS-LOC-01, PASS-LOC-04, PASS-LOC-05, PASS-LOC-06, PASS-LOC-07, PASS-SIDE-03, PASS-USER-01, PASS-USER-02, PASS-USER-05, PASS-USER-07, PASS-USER-11, PASS-WX-01, PASS-BEING-07, PASS-TOW-01

**Proposed triage:** each finding has a **Proposed triage** line under its fix, following `allow_list.md`, `error_set.md` and the a0–a3 and b0 triages. All 19 proposed fixes (fix and partly-fixed lines) have been applied to `b2_atomic.json`, which started as an exact copy of `b1_format.json`: 18 rules changed, with every changed statement rebuilt from its fields, and no vocabulary changes. Rule ids are unchanged. Stage 1 on `b2_atomic.json` passes all 8 checks with no format errors (74 rules, 20 vocab terms).

**67 findings** (5 major, 62 minor) in 42 rules.

## PASS-GEN-02: If in doubt, do not pass

> WHEN the DRIVER is in doubt about whether a PASS can be made safely, the DRIVER MUST NOT pass.

### S2-001. Safety condition is inferred from context but not noted

*note* · minor · low confidence

Block 10.15 says only "If in doubt, do not pass." It does not say what the doubt is about. The rule's condition "in doubt about whether a PASS can be made safely" takes that subject from the preceding sentence in the same block: 10.15: "Never overtake and pass another vehicle unless you are sure you can do so without danger to yourself or others." This is a reasonable reading, but the rule records it nowhere, and `note` is empty. A checker cannot tell that the condition is an interpretation and not a quotation.

- Fix: Set note to: "The handbook says only 'If in doubt, do not pass'; the object of the doubt (whether the pass can be made without danger) is taken from the preceding sentence in 10.15."
- **Proposed triage: fix as proposed.** GEN-02 note: "The handbook says only 'If in doubt, do not pass'; the object of the doubt (whether the pass can be made without danger) is taken from the preceding sentence in 10.15." An inference not stated in the note is a confirmed error type (S2-028).

## PASS-GEN-04: Keep right except to pass

> WHEN driving on a road, the DRIVER MUST keep to the right of the road, or in the right-hand lane on a multi-lane road, UNLESS preparing to turn left OR passing another vehicle.

### S2-002. Slow-traffic sign cited for a broader rule it does not state

*citation* · minor · medium confidence

The statement applies to every DRIVER on any road. The regulatory sign it cites is narrower: 18.29-c: "Slow traffic on multi-lane roads must keep right." That sign supports a separate rule for slow traffic on multi-lane roads, worded as a requirement, not this general instruction. Citing 18.29 and 18.29-c as evidence suggests that block 5.13 and the sign word the same rule. That conflicts with the rule's force: the rule is INSTRUCTION, but under the stronger-wording rule a shared rule would have to be REQUIREMENT. The general rule rests only on 5.13: "Keep to the right of the road or in the right-hand lane on multi-lane roads unless you want to turn left or pass another vehicle."

- Fix: Set evidence to ["5.13"]. Change the note to: "The handbook says this is especially important when driving more slowly than other vehicles; the 'Slower traffic keep right' sign (18.29) states that case as a separate requirement." Then make the sign its own rule: {force: REQUIREMENT, modal: MUST, actor: DRIVER, when: "driving more slowly than other traffic on a multi-lane road AND a 'Slower traffic keep right' sign is posted", action: "keep right", unless: "", evidence: ["18.29", "18.29-c"]}.
- **Proposed triage: rejected, no change.** Settled in S3-002: 18.29 and 18.29-c were added to GEN-04 on purpose, with a note, and the force kept INSTRUCTION because the sign covers only slow traffic on multi-lane roads.

## PASS-GEN-05: Freeway left lane for passing only

> WHEN driving on a multi-lane FREEWAY, the DRIVER MUST use the far left lane to pass traffic moving slower than the speed limit, and not stay in that lane after passing, UNLESS the DRIVER is driving a truck on a road that has a TRUCK PASSING LANE.

### S2-003. One rule combines a MUST and a MUST NOT action

*grammar* · minor · medium confidence

The action "use the far left lane to pass traffic moving slower than the speed limit, and not stay in that lane after passing" puts a negative obligation ("not stay") under the modal MUST. The grammar allows one MODAL per rule, and the prohibition is really a MUST NOT. 12.24 states two commands: "Use the far left lane … to pass …, but don't stay there." Folding both into one MUST makes the rule harder for a program to read and check.

- Fix: Split into two rules. PASS-GEN-05: "WHEN driving on a multi-lane FREEWAY AND passing traffic moving slower than the speed limit, the DRIVER MUST use the far left lane, UNLESS the DRIVER is driving a large truck on a road that has a TRUCK PASSING LANE." New rule: "WHEN driving on a multi-lane FREEWAY AND the DRIVER has finished passing in the far left lane, the DRIVER MUST NOT stay in the far left lane." Add a vague term for the second rule: "stay", explained as "no time or distance given for leaving the lane".
- **Proposed triage: not an error, no change.** Positive phrase first and negated phrase last in one MUST action is the accepted pattern (a0 M3).

### S2-004. Wording can be read as an obligation to pass all slower traffic

*ambiguity* · minor · medium confidence

"the DRIVER MUST use the far left lane to pass traffic moving slower than the speed limit" can be read as requiring the driver to pass any vehicle going below the limit. 12.24 is about which lane to use when passing: the left lane is for passing, and drivers should keep right. A driving model could misread the rule as a duty to overtake.

- Fix: Move passing into the condition: when: "driving on a multi-lane FREEWAY AND passing traffic moving slower than the speed limit"; action: "use the far left lane".
- **Proposed triage: fix, condition only.** Passing moves into the condition so the rule cannot be read as a duty to overtake; "only" is still not added (a0 G3). when: "driving on a multi-lane FREEWAY AND passing traffic moving slower than the speed limit"; action: "use the far left lane, and not stay in that lane after passing"; statement: "WHEN driving on a multi-lane FREEWAY AND passing traffic moving slower than the speed limit, the DRIVER MUST use the far left lane, and not stay in that lane after passing, UNLESS the DRIVER is driving a truck on a road that has a TRUCK PASSING LANE." The vague term "not stay in that lane after passing" stays.

### S2-005. Exception says "truck" where the handbook says "large trucks"

*faithfulness* · minor · medium confidence

The exception reads "the DRIVER is driving a truck on a road that has a TRUCK PASSING LANE". 12.24 limits the restriction to "large trucks": "large trucks cannot travel in the far left lane and must use the lane to the right for passing." As written, the exception covers every truck, including small ones the handbook does not restrict.

- Fix: unless: "the DRIVER is driving a large truck on a road that has a TRUCK PASSING LANE"
- **Proposed triage: not an error, no change.** The actor follows 10.26 ("trucks"), as decided in S2-012 (a2); GEN-07's note records 12.24's "large trucks".

## PASS-GEN-06: Staying behind is often safer

> WHEN following another vehicle AND considering changing lanes to go around it, the DRIVER SHOULD consider staying behind it for a few seconds rather than going around it.

### S2-006. "SHOULD consider" makes the action a mental act that cannot be checked

*clarity* · minor · low confidence

The action reads "consider staying behind it for a few seconds rather than going around it". Combined with the modal, this becomes "SHOULD consider…". That is a recommendation to think about something, not a driving behaviour. A driving model cannot act on it, and a checker cannot verify it. The hedge seems meant to carry the handbook's "often", in 10.11: "Remember that spending a few seconds behind another vehicle is often safer than going around it." The rule hides that qualifier inside "consider" instead of stating it. It also does not list it as a judgement left to the driver.

- Fix: Set action to "stay behind it for a few seconds rather than go around it, as this is often safer". The statement then reads: "WHEN following another vehicle AND considering changing lanes to go around it, the DRIVER SHOULD stay behind it for a few seconds rather than go around it, as this is often safer." Add a vague_terms entry: {"term": "often safer", "explanation": "does not say when going around is safer"}. Keep the existing entry for "a few seconds".
- **Proposed triage: not an error, no change.** "Consider" is the hedge of the ADVICE wording (S2-010, a2).

## PASS-PROC-01: Signal left and check before pulling out

> WHEN about to change lanes to pass, the PASSER MUST use the left-turn signal, check the mirrors and BLIND SPOT and check that the way is clear ahead and behind.

### S2-007. A night-only step is applied to every pass

*scope* · major · high confidence

The rule's condition is any pass ("WHEN about to change lanes to pass"), but the action adds "check the mirrors and BLIND SPOT". In the sections shown, that check appears only in the night-passing steps: 10.29: "Be very careful when you pass other vehicles at night. If you have to pass and the way is clear, follow these steps:" and 10.31: "Signal, check your mirrors and blind spot, and pull out to pass." The general passing steps say only 10.17: "Use your left-turn signal … and check that the way is clear ahead and behind before moving into the passing lane." The note admits the night steps were the source. Applying them to every pass is not supported by the citations.

- Fix: Limit this rule to the general steps. Set action to "use the left-turn signal and check that the way is clear ahead and behind before moving into the passing lane". Set statement to "WHEN about to change lanes to pass, the PASSER MUST use the left-turn signal and check that the way is clear ahead and behind before moving into the passing lane." Set evidence to ["10.16", "10.17"] and note to "". Put the mirror and blind-spot check in a separate night rule: "WHEN passing another vehicle at night, the PASSER MUST signal and check the mirrors and BLIND SPOT before pulling out to pass." with evidence ["10.29", "10.31"].
- **Proposed triage: ignored, no change.** Same as a0 M2 and S2-013 (a2). Reviewer decision: the blind spot is checked on every pass.

### S2-008. Night-passing blocks cited for a general rule

*citation* · minor · medium confidence

10.29 ("Be very careful when you pass other vehicles at night…") and 10.31 belong to the night-passing procedure under heading 10.28 "Passing at night". They do not support a rule that applies to every pass. 10.19 ("Change lanes only after signalling.") does directly support signalling before the lane change, but it is not cited.

- Fix: Set evidence to ["10.16", "10.17", "10.19"].
- **Proposed triage: rejected, no change.** 10.29 and 10.31 stay because the mirror and blind-spot check rests on them (a0 M2). 10.19's "Change lanes only after signalling" is PROC-03's evidence.

## PASS-PROC-02: Watch for hidden and entering road users

> WHEN preparing to pass a vehicle, the PASSER MUST watch for bicycles and small vehicles that may be hidden from view in front of the vehicle being passed, vehicles that may be turning left in front of the PASSER, and vehicles or pedestrians entering the road from another road or driveway.

### S2-009. Defined term PASS written in lowercase

*vocabulary* · minor · medium confidence

The rule uses the defined actor PASSER, whose vocabulary definition is "The driver making a PASS", so PASS is a defined vocabulary term. Yet the condition says "preparing to pass a vehicle" and the action says "the vehicle being passed", both in lowercase. The instructions require a word naming a vocabulary term in its defined meaning to be written in CAPITALS. Without that, a reader cannot tell whether lowercase "pass" means the defined manoeuvre (10.14: "Passing is changing lanes to move past a slower vehicle") or something looser.

- Fix: when: "preparing to PASS a vehicle"; action: "watch for bicycles and small vehicles that may be hidden from view in front of the vehicle the PASSER is about to PASS, vehicles that may be turning left in front of the PASSER, and vehicles or pedestrians entering the road from another road or driveway". Update the statement to match.
- **Proposed triage: not an error, no change.** Lowercase verb "pass" is allowed.

## PASS-PROC-03: Change lanes only after signalling

> WHEN making a PASS, the PASSER MUST NOT change lanes, UNLESS the PASSER has signalled.

### S2-010. Unclear whether the rule covers the return lane change and which signal is required

*clarity* · minor · medium confidence

The rule says "WHEN making a PASS, the PASSER MUST NOT change lanes, UNLESS the PASSER has signalled." The cited blocks describe two lane changes, each with its own signal. 10.17 says: "Use your left-turn signal to show that you want to pass … before moving into the passing lane." 10.19 says: "After overtaking, signal that you want to move back into the lane you started from …". The vocabulary defines PASS only as "Changing lanes to move past a slower vehicle", which does not include the return to the original lane. A model could therefore read the rule as covering only the move out, and "has signalled" does not say that the left-turn signal is required for that move. The note is empty, so nothing tells a checker how the two blocks were combined.

- Fix: Make both lane changes explicit. Set when: "making a PASS, including moving back into the original lane after overtaking"; action: "change lanes"; unless: "the PASSER has signalled the lane change, using the left-turn signal when moving into the passing lane". Statement: "WHEN making a PASS, including moving back into the original lane after overtaking, the PASSER MUST NOT change lanes, UNLESS the PASSER has signalled the lane change, using the left-turn signal when moving into the passing lane." Add a note: "Combines 10.17 (left-turn signal before moving into the passing lane) and 10.19 ('Change lanes only after signalling'; signal before moving back)."
- **Proposed triage: not an error, no change.** PROC-01 requires the left-turn signal before moving out and PROC-04 the signal before moving back; PROC-03 cites 10.17 and 10.19, which cover both.

## PASS-PROC-05: Return only when front of passed vehicle visible

> WHEN the PASSER has overtaken the vehicle being passed, the PASSER MUST NOT move back into the original lane, UNLESS the entire front of the passed vehicle can be seen in the inside rear-view mirror.

### S2-011. Note relies on Diagram 2-46, which is not cited

*citation* · minor · medium confidence

The note says "Diagram 2-46 shows the full passing path, pulling out and back in." That diagram is figure 10.21 (caption 10.21-c), but neither block is in `evidence`. The note and the citations disagree: either the diagram supports the rule and should be cited, or it should not be mentioned. The diagram only shows the path. It does not show the mirror test this rule is about, so citing it adds little.

- Fix: Remove the diagram sentence from the note: "Stated in the general passing steps (10.19, 'inside mirror') and repeated in the night passing steps (10.32, 'rear view mirror')." Alternatively, keep the sentence and add "10.21" to evidence.
- **Proposed triage: not an error, no change.** Something mentioned only in a note needs no citation; 10.21 was removed from this rule in S2-017 (a2) with the note sentence kept.

### S2-012. Inconsistent naming of the overtaken vehicle

*clarity* · minor · low confidence

The rule calls the same vehicle "the vehicle being passed" in `when` and "the passed vehicle" in `unless`. The vocabulary defines PASS, but neither phrase uses it, and the mixed wording is needlessly loose for a formal rule.

- Fix: Use one phrase throughout, e.g. unless: "the entire front of the vehicle being passed can be seen in the inside rear-view mirror".
- **Proposed triage: not an error, no change.** Low confidence. Both phrases clearly name the one vehicle in the condition; the wording follows the handbook ("the vehicle you are passing").

## PASS-NIGHT-01: Low beams when following within 60 metres

> WHEN using headlights AND less than 60 metres behind another vehicle, the DRIVER MUST use low-beam headlights, UNLESS the DRIVER is passing that vehicle.

### S2-013. Introductory sentence of the offence table cited as evidence

*citation* · minor · low confidence

The rule cites 22.96: "Here are the demerit points for driving offences." This sentence only introduces the table and states nothing specific to this rule. The penalty is fully supported by 22.134: "Two points" together with 22.135: "Failing to lower headlight beam". The instructions say to cite only materials directly relevant to the rule.

- Fix: Remove "22.96" from evidence: ["4.65", "14.8", "22.134", "22.135"].
- **Proposed triage: not an error, no change.** The block that introduces a list stays cited with its items (a0 C1, S2-088); 22.134 was added in b0 m5.

### S2-014. Note does not mention that the second passage omits the passing exception

*note* · minor · low confidence

The rule draws on two passages. 4.65 says "Use your low beams when you are less than 60 metres behind another vehicle unless you are passing it." 14.8 says "Use your low-beam headlights … when following a vehicle within 60 metres", framed as cutting down glare "at night", and gives no exception for passing. The note does not say the rule is inferred from two places, or that only 4.65 supplies the UNLESS clause. It also does not say that the penalty is linked to this rule by inference from the generic offence "Failing to lower headlight beam".

- Fix: Set note to: "Stated in 4.65 (with the exception for passing, applying to all roads including divided ones) and in 14.8 (as a glare rule at night, without the exception). The penalty is inferred from the offence 'Failing to lower headlight beam' in the table of offences."
- **Proposed triage: fix, shorter note.** The rule is drawn from two places and only 4.65 gives the exception. NIGHT-01 note: "Stated in 4.65 (with the exception for passing, applying to all roads including divided ones) and in 14.8 (at night, without the exception). The two demerit points are listed for failing to lower headlight beam (22.134, 22.135)." The proposed wording that the penalty is "inferred" is left out: the offence names this duty directly.

## PASS-NIGHT-03: Low beams on approach at night

> WHEN passing at night AND approaching the vehicle to be passed from behind, the PASSER MUST switch the headlights to low beams.

### S2-015. Procedure's precondition "the way is clear" is dropped

*condition* · minor · medium confidence

The handbook introduces the night-passing steps with a condition: 10.29: "If you have to pass and the way is clear, follow these steps:". Step 10.30 ("Switch your headlights to low beams as you approach a vehicle from behind.") is the first of those steps. The rule's condition is only "passing at night AND approaching the vehicle to be passed from behind". It leaves out the handbook's precondition that the way is clear, which slightly broadens the situation the rule covers.

- Fix: when: "making a PASS at night AND the way is clear AND approaching the vehicle to be passed from behind"; statement: "WHEN making a PASS at night AND the way is clear AND approaching the vehicle to be passed from behind, the PASSER MUST switch the headlights to low beams." Add a vague_terms entry {"term": "the way is clear", "explanation": "no gap or sight distance given"}.
- **Proposed triage: rejected, no change.** "If you have to pass and the way is clear" is the lead-in to the step list, not a condition of each step (a0 M4, S2-023/S2-026 in a2).

### S2-016. Lowercase "passing" stands in for the defined term PASS

*vocabulary* · minor · low confidence

The actor PASSER is defined as "The driver making a PASS", so PASS is a defined term. The condition, however, says "passing at night" in lowercase. That leaves unclear whether the rule refers to the defined manoeuvre, and it is inconsistent with the vocabulary.

- Fix: Write the condition as "making a PASS at night …" so that it uses the defined term in capitals.
- **Proposed triage: not an error, no change.** Lowercase "passing" is allowed.

## PASS-NIGHT-04: High beams when alongside at night

> WHEN passing at night AND moving alongside the vehicle being passed, the PASSER MUST switch on the high-beam headlights, UNLESS an oncoming vehicle is within 150 metres.

### S2-017. The 'way is clear' condition of the night-passing steps is dropped

*missing condition* · minor · medium confidence

The steps in 10.31 apply only in the situation that 10.29 introduces. 10.29 says: "If you have to pass and the way is clear, follow these steps". The rule's `when` reads only "passing at night AND moving alongside the vehicle being passed", so the handbook's precondition "the way is clear" is missing. The rule's practical effect barely changes, since a driver moving alongside to pass has normally judged the way clear. Still, the rule does not state the scope the handbook gives these steps. If the phrase is added, it is vague and must be listed in `vague_terms`.

- Fix: when: "passing at night AND the way is clear AND moving alongside the vehicle being passed"; statement: "WHEN passing at night AND the way is clear AND moving alongside the vehicle being passed, the PASSER MUST switch on the high-beam headlights, UNLESS an oncoming vehicle is within 150 metres."; vague_terms: [{"term": "the way is clear", "explanation": "no gap or sight distance given"}]
- **Proposed triage: rejected, no change.** Same as S2-015.

## PASS-LOC-03: No passing at hill crests or blind curves

> WHEN there is not enough clear distance ahead to pass in safety AND the view of oncoming traffic is obstructed AND the DRIVER is approaching the crest of a hill or is on a curve, the DRIVER MUST NOT attempt to pass.

### S2-018. Ambiguous scope of the 'vision obstructed' and 'clear distance' conditions is not noted

*note* · minor · medium confidence

10.22 reads: "Don't attempt to pass when approaching the crest of a hill or on a curve where your vision of oncoming traffic is obstructed and there is not enough clear distance ahead to pass in safety." This can be read two ways. In one reading, the 'where…' clause applies only to curves, so passing near a hill crest is barred outright. In the other, it applies to both. The rule silently picks the narrower reading: "there is not enough clear distance ahead to pass in safety AND the view of oncoming traffic is obstructed AND the DRIVER is approaching the crest of a hill or is on a curve". Under that reading, the hill-crest prohibition applies only when both further conditions also hold. The instructions ask that wording which could be read two ways be recorded in `note`, but the note is empty.

- Fix: Set note to: "10.22 is ambiguous: the clause 'where your vision of oncoming traffic is obstructed and there is not enough clear distance ahead' may qualify only 'on a curve', in which case passing when approaching a hill crest is barred without further conditions. This rule applies the clause to both situations."
- **Proposed triage: fix as proposed.** LOC-03 note: "10.22 is ambiguous: the clause 'where your vision of oncoming traffic is obstructed and there is not enough clear distance ahead' may qualify only 'on a curve', in which case passing when approaching a hill crest is barred without further conditions. This rule applies the clause to both situations." Wording that could be read two ways belongs in the note (task.md).

## PASS-LOC-08: No passing by lane change at intersections

> WHEN in or near an intersection, the DRIVER MUST NOT change lanes to pass.

### S2-019. The note hides the cited ban on going around a vehicle in the intersection

*completeness* · minor · medium confidence

The rule uses only the lane-change clause of 29.104: "Do not go over lane markings or change lanes in the intersection." The same cited block goes on: "If your lane is blocked by a vehicle turning left or a vehicle edging into the intersection from the right, slow down or stop instead of pulling out to go around the vehicle." That is a passing rule, and it also bans crossing lane markings in the intersection. The note says "Passing on the right without a lane change is PASS-SIDE-01", which suggests that passing inside an intersection is unaffected so long as no lane change is made. The cited block says otherwise, and the note does not mention this content at all.

- Fix: Change the note to: "Both blocks ban changing lanes in or near an intersection; since a PASS is a lane change, this bans passing there by changing lanes. 29.104 also bans going over lane markings in the intersection and pulling out to go around a vehicle that blocks the lane; that is a separate rule." Make sure a separate rule exists, citing 29.104: "WHEN in an intersection AND the DRIVER's lane is blocked by a vehicle turning left or a vehicle edging into the intersection from the right, the DRIVER MUST slow down or stop, instead of pulling out to go around the vehicle." (force INSTRUCTION).
- **Proposed triage: partly fixed, one sentence added to the note.** The other sentence of 29.104 is its own rule (PASS-SIDE-04), so the note need not restate it (allow list), but a link avoids the misreading. Add to LOC-08's note: "Going around a vehicle that blocks the lane in an intersection is PASS-SIDE-04." No new rule.

### S2-020. PASS in capitals in the note but lowercase "pass" in the rule

*vocabulary* · minor · low confidence

The note treats PASS as a defined term: "since a PASS is a lane change". The action, however, writes "change lanes to pass" in lowercase, and PASS is not among the vocabulary entries this rule uses. Either PASS is a defined term and the rule should use it, or it is not and the note should not capitalise it.

- Fix: If PASS is in the rule set's vocabulary, set action to "change lanes to PASS", update the statement to match, and list PASS among the vocabulary the rule uses. Otherwise, write "pass" in lowercase in the note.
- **Proposed triage: not an error, no change.** The note uses the noun PASS, the rule the lowercase verb "pass", which is allowed.

## PASS-MARK-02: Broken line: passing allowed

> WHEN there is a BROKEN LINE at the left of the DRIVER's lane AND the way is clear AND enough BROKEN LINE remains ahead to complete the PASS safely, the DRIVER MAY pass.

### S2-021. BROKEN LINE definition also covers continuity lines

*vocabulary* · minor · medium confidence

The rule depends on BROKEN LINE, defined as "A dashed painted line on the road." That definition also includes continuity lines, which the same page treats separately and gives a different meaning: 21.8: "Broken lines that are wider and closer together than regular broken lines are called continuity lines. When you see continuity lines on your left side, it generally means the lane you are in is ending or exiting and that you must change lanes…". Under the current definition, a continuity line on the driver's left meets the rule's condition "BROKEN LINE at the left of the DRIVER's lane" and appears to permit a pass. The handbook gives continuity lines a lane-ending meaning, not a passing permission. The cited blocks 21.6 and 21.7 also do not define the term; they only use it.

- Fix: Change the vocabulary entry to: {"term": "BROKEN LINE", "definition": "A regular dashed painted lane line, not including continuity lines (wider, more closely spaced dashes).", "evidence": ["21.6", "21.8"]}. Alternatively, add to the rule's note: "Continuity lines (21.8) are a distinct marking and do not grant this permission."
- **Proposed triage: not an error, no change.** Same as S2-034 (a2): a definition is not narrowed to exclude look-alikes.

### S2-022. Second condition comes from the diagram's parenthetical, but the note is empty

*note* · minor · medium confidence

The condition "enough BROKEN LINE remains ahead to complete the PASS safely" is not part of the main sentence of 21.6 ("A broken line at the left of your lane means you may pass if the way is clear"). It comes from the parenthetical that describes Diagram 3-3: "('A' may pass if there are enough broken lines ahead to complete the pass safely.)". The instructions ask for a note when a rule draws on a diagram or combines sources. The note is empty.

- Fix: Set note to: "The condition about enough broken line ahead comes from the parenthetical in 21.6 describing Diagram 3-3 (21.7), in which vehicle 'A' is beside a broken line with more broken line ahead."
- **Proposed triage: not an error, no change.** The condition is in the cited block itself: the parenthetical is part of 21.6's text.

## PASS-SIGN-03: Keep right where a passing lane is provided

> WHEN on a two-lane section where a PASSING LANE is provided AND a keep-right-except-to-pass sign is posted, the DRIVER MUST keep to the right lane, UNLESS the DRIVER is passing.

### S2-023. Sign is named by an invented label rather than described as it appears

*clarity* · minor · medium confidence

The condition says "a keep-right-except-to-pass sign is posted". The handbook gives this sign no such name, and the sign itself carries no words. 18.40 shows only a black square sign with a white straight arrow and a second arrow branching off to one side, where the lane widens. Its meaning comes from the caption, 18.40-c: "Keep to the right lane except when passing on two-lane sections where climbing or passing lanes are provided." A model that sees the road cannot match the label "keep-right-except-to-pass sign" to this pictogram, so it may not know when the rule applies.

- Fix: Change `when` to: "on a two-lane section where a PASSING LANE is provided AND the regulatory sign showing a straight arrow with a second arrow branching from it (Ontario sign 18.40) is posted". Update `statement` to match. Add to `note`: "The sign has no text; its meaning is given by caption 18.40-c."
- **Proposed triage: not an error, no change.** A sign may be named by its meaning (S2-036, S2-039 in a2).

## PASS-SIGN-04: Merge when passing lane ends

> WHEN in the right-hand lane of a PASSING LANE section AND a sign warns that the lane is ending, the DRIVER MUST merge safely with traffic in the left-hand lane.

### S2-024. The warning sign is not identified in the condition

*clarity* · minor · medium confidence

The condition reads "a sign warns that the lane is ending", which follows the unnamed sign in 10.36: "Another sign warns when the lane is ending…". The rule's MUST, however, comes from the specific sign in 18.70, whose caption is "Right lane ends ahead. If you are in the right-hand lane, you must merge safely…". A driving model reading only the rule cannot tell which sign triggers the obligation, even though the cited figure shows it.

- Fix: Set when to "in the right-hand lane of a passing or climbing lane section AND a 'right lane ends ahead' warning sign is posted". Update the statement to match.
- **Proposed triage: not an error, no change.** Same as S2-044 (a2); 18.70 and 18.70-c are cited and the note names the right-lane-ends sign.

### S2-025. PASSING LANE is used for a road section, but defined as a lane

*vocabulary* · minor · medium confidence

The vocabulary defines PASSING LANE as "A special passing or climbing lane that lets slower vehicles move into the right-hand lane…", which is a single lane. The rule writes "the right-hand lane of a PASSING LANE section", using the term for a stretch of road that has two lanes. This does not match the definition and makes it unclear which lane is meant.

- Fix: Write the condition as "in the right-hand lane where a PASSING LANE is provided", or redefine the term as "PASSING LANE SECTION: a stretch of road with a special passing or climbing lane, where slower vehicles use the right-hand lane so faster ones can pass in the left lane" and use that term.
- **Proposed triage: ignored, no change.** Same as b0 m9 (PASSING LANE definition left as is).

### S2-026. The strength depends on identifying the 10.36 sign with the 18.70 sign

*strength* · minor · low confidence

10.36 is descriptive ("so drivers in the right-hand lane can begin to merge safely"). The REQUIREMENT force comes only from 18.70-c, a general right-lane-ends sign that the passing-lane text never names. The note discloses this inference. The rule is still mostly the 18.70 sign rule, framed narrowly as a passing-lane rule.

- Fix: Keep the REQUIREMENT, but state in the note that the MUST comes from the general right-lane-ends sign (18.70) and that 10.36 alone would support only ADVICE. Alternatively, frame the rule around the 18.70 sign without the passing-lane restriction.
- **Proposed triage: rejected, no change.** Settled in S2-045 (a2); the note already says the MUST comes from the 18.70 sign and that 10.36 is soft wording.

## PASS-SIGN-05: Hazard marker: pass on the marked side

> WHEN a hazard marker sign is posted at a hazard close to the edge of the road, the DRIVER MAY ONLY pass the hazard on the side shown by the sign's downward lines.

### S2-027. Rule is about passing a roadside hazard, not overtaking

*scope* · major · medium confidence

The topic is "overtaking (passing another vehicle, and being passed)". The cited sign is about going past a fixed obstacle: 18.68-c: "Hazard close to the edge of the road. The downward lines show the side on which you may safely pass." Going past a stationary roadside hazard is not overtaking another vehicle. The word "pass" only overlaps in wording, so the rule falls outside the topic and should not be in an overtaking ground-truth set.

- Fix: Remove PASS-SIGN-05 from the overtaking rule set. Extract it under a signs or hazard topic instead.
- **Proposed triage: rejected, no change.** You added this rule in b0 m7, following S3-006: passing a hazard other than a vehicle (animals, PASS-USER-23) is in scope.

### S2-028. MAY ONLY turns 'may safely pass' into a prohibition and drops 'safely'

*strength* · major · medium confidence

The handbook says only that the lines show "the side on which you may safely pass" (18.68-c). This wording grants permission and marks the safe side. It does not say passing on the other side is not permitted. MAY ONLY ("allowed when the condition holds, and not otherwise") reads in a prohibition that the sign's caption does not state. The note's claim that the other side "is not permitted" is likewise unsupported. The rule also drops the handbook's word "safely", which shows this is a safety indication.

- Fix: Set modal to MAY and action to "safely pass the hazard on the side to which the sign's diagonal lines slope downward". Statement: "WHEN a hazard marker sign is posted at a hazard close to the edge of the road, the DRIVER MAY safely pass the hazard on the side to which the sign's diagonal lines slope downward." Change the note to: "Based on the caption of the hazard marker sign; the handbook does not state that passing on the other side is prohibited."
- **Proposed triage: fix, partly as proposed.** The caption gives permission and marks the safe side; it does not forbid the other side. force stays PERMISSION; modal: MAY; action stays "pass the hazard on the side shown by the sign's downward lines"; statement: "WHEN a hazard marker sign is posted at a hazard close to the edge of the road, the DRIVER MAY pass the hazard on the side shown by the sign's downward lines." note: "The caption says the lines show 'the side on which you may safely pass'; it does not say that passing on the other side is prohibited." "Safely" is not added to the action, since it would then need a vague-term entry and adds nothing a driver can act on.

### S2-029. 'side shown by the sign's downward lines' is unclear

*clarity* · minor · medium confidence

The phrase "the side shown by the sign's downward lines" does not tell the driving model how to read the sign. It does not say that the safe side is the one toward which the diagonal stripes slope down. The diagram in 18.68 shows diagonal black and yellow stripes, but the rule does not describe them.

- Fix: Reword the action as "pass the hazard on the side toward which the diagonal stripes on the sign slope downward". Add a note describing the sign shown in 18.68: a vertical rectangle with diagonal black and yellow stripes.
- **Proposed triage: not an error, no change.** The rule uses the caption's own words; a sign may be described in the note or not at all (allow list).

### S2-030. Note refers to another rule

*format* · minor · medium confidence

The note says "as in PASS-LOC-07". The instructions require each rule to stand on its own, so its note should not depend on another rule for its meaning.

- Fix: Remove the reference to PASS-LOC-07 from the note.
- **Proposed triage: not an error, no change.** Links to related rules in notes are wanted (error set: missing link to a related rule). The sentence goes anyway with the new note in S2-028.

## PASS-SIDE-01: When passing on the right is allowed

> WHEN on a multi-lane road OR on a one-way road OR overtaking a STREETCAR OR overtaking a left-turning vehicle, the DRIVER MAY pass on the right, UNLESS doing so requires changing lanes in or near an intersection.

### S2-031. Exception imported from a separate lane-change rule into the permission

*faithfulness* · minor · medium confidence

The handbook grants this permission without any exception. 10.40 says only: "You may pass on the right on multi-lane or one-way roads and when overtaking a streetcar or a left-turning vehicle." The rule's `unless` ("doing so requires changing lanes in or near an intersection") comes from a different section on lane changes. 10.11 says: "Don't change lanes in or near an intersection." That is a general INSTRUCTION, and it applies to every lane change, not just passing on the right. Folding it into this PERMISSION as an UNLESS has three effects. It turns a MUST NOT into a mere withdrawal of permission. It makes this rule an inference drawn from two places. It narrows the overtaking-a-left-turner case, which by nature happens near intersections. The note mentions 10.11 but does not say that the exception is inferred rather than stated in 10.40.

- Fix: Set unless to "". Remove 10.11 from evidence. The statement becomes: "WHEN on a multi-lane road OR on a one-way road OR overtaking a STREETCAR OR overtaking a left-turning vehicle, the DRIVER MAY pass on the right." Drop the "near an intersection" vague term. Leave the lane-change ban to its own rule. If the combination is kept, add to the note: "The exception is inferred from 10.11's general ban on lane changes in or near an intersection; 10.40 states the permission without exception."
- **Proposed triage: rejected, no change.** The exception was set in S3-008 and reworded in b0 M1; the note already says it rests on 10.11's ban on lane changes in or near an intersection.

### S2-032. 10.41 cited although it does not support the permission

*citation* · minor · low confidence

Block 10.41 ("Passing on the right can be more dangerous… If you are driving in the left most lane with a slower vehicle in front of you, wait for the vehicle to move to the right. Do not suddenly change lanes and pass on the right…") mainly states a separate instruction about the leftmost lane. It does not establish when passing on the right is allowed. Only its first sentence is reflected, and only in the note.

- Fix: Cite only 10.40 as evidence, or 10.40 and 10.11 if the exception is kept. Keep the 'more dangerous' remark in the note, attributed to 10.41.
- **Proposed triage: fix, citation only.** 10.41 does not support the permission; the "more dangerous" remark stays in the note without a citation (a0 C2 ruling). SIDE-01 evidence: ["10.11", "10.40"].

## PASS-SIDE-02: Wait for a slower vehicle to move right

> WHEN driving in the leftmost lane with a slower vehicle in front, the DRIVER MUST wait for the slower vehicle to move to the right and not suddenly change lanes to pass on the right.

### S2-033. A prohibition is folded into a MUST action with an embedded 'not'

*grammar* · minor · medium confidence

Block 10.41 gives two plain commands. The first is positive: "wait for the vehicle to move to the right." The second is a prohibition: "Do not suddenly change lanes and pass on the right." The rule puts both under the modal MUST, writing the prohibition as a negated clause inside the action: "MUST wait for the slower vehicle to move to the right and not suddenly change lanes to pass on the right." The grammar provides MUST NOT for prohibitions, so a reader or program filtering by modal will not find this prohibition. The negation inside a MUST action is also awkward to read. The meaning is preserved, so this is a matter of form.

- Fix: Split into two entries, both citing 10.41. (1) PASS-SIDE-02: when "driving in the leftmost lane with a slower vehicle in front", modal MUST, action "wait for the slower vehicle to move to the right"; statement "WHEN driving in the leftmost lane with a slower vehicle in front, the DRIVER MUST wait for the slower vehicle to move to the right." (2) PASS-SIDE-03: the same when, modal MUST NOT, action "suddenly change lanes to pass on the right"; statement "WHEN driving in the leftmost lane with a slower vehicle in front, the DRIVER MUST NOT suddenly change lanes to pass on the right." Keep the note on the reason in rule (2). Alternatively, keep a single entry with modal MUST NOT, action "suddenly change lanes to pass on the right", and record the instruction to wait in the note.
- **Proposed triage: not an error, no change.** Same as a0 M3 / S2-046 (a2): the positive-first, negated-last pattern.

## PASS-SIDE-04: Do not go around a left-turner in an intersection

> WHEN driving through an intersection AND the DRIVER's lane is blocked by a vehicle turning left, the DRIVER MUST slow down or stop and not pull out to go around the vehicle.

### S2-034. Omits the vehicle edging in from the right

*incompleteness* · major · high confidence

The rule covers only a lane blocked by a vehicle turning left. The cited block gives two triggers for the same instruction. 29.104: "If your lane is blocked by a vehicle turning left or a vehicle edging into the intersection from the right, slow down or stop instead of pulling out to go around the vehicle." Because the second case is dropped, a driver whose lane is blocked by a vehicle edging in from the right gets no guidance. The title also narrows the rule to left-turners only.

- Fix: Set when: "driving through an intersection AND the DRIVER's lane is blocked by a vehicle turning left OR by a vehicle edging into the intersection from the right". Set title: "Do not go around a vehicle blocking the lane in an intersection". Update statement: "WHEN driving through an intersection AND the DRIVER's lane is blocked by a vehicle turning left OR by a vehicle edging into the intersection from the right, the DRIVER MUST slow down or stop and not pull out to go around the vehicle."
- **Proposed triage: fix, with the alternatives joined by a lowercase "or" inside one fact (a0 G1), since the condition already has an AND.** when: "driving through an intersection AND the DRIVER's lane is blocked by a vehicle turning left or a vehicle edging into the intersection from the right"; statement: "WHEN driving through an intersection AND the DRIVER's lane is blocked by a vehicle turning left or a vehicle edging into the intersection from the right, the DRIVER MUST slow down or stop and not pull out to go around the vehicle." title: "Do not go around a vehicle blocking the lane in an intersection".

### S2-035. Citation 10.11 supports a different, broader rule

*citation* · minor · medium confidence

10.11 says "Don't change lanes in or near an intersection. Remember that spending a few seconds behind another vehicle is often safer than going around it." That is a general lane-change prohibition plus advice, not the blocked-lane instruction this rule states. The rule's content comes entirely from 29.104. Citing 10.11 without a note mixes a separate rule (with its broader "near" scope and advisory wording) into this one's support.

- Fix: Remove "10.11" from evidence, leaving ["29.104"]. Alternatively, keep it and add a note: "10.11 separately forbids lane changes in or near an intersection and advises that staying behind a vehicle is often safer than going around it."
- **Proposed triage: rejected, no change.** 10.11 was added in S3-008 on purpose: the rule bans pulling out (changing lanes) in an intersection, which 10.11 states.

## PASS-USER-03: Tap horn lightly and early

> WHEN overtaking a CYCLIST AND the DRIVER feels the horn must be used, the DRIVER MUST tap the horn quickly and lightly while still some distance away from the CYCLIST.

### S2-036. Reason given in the handbook is not recorded in the note

*note* · minor · low confidence

The cited block gives the reason for the horn guidance: 6.38: "It may frighten them and cause them to lose control." The instructions list "a reason the handbook gives" as something to record in `note`, but the rule's note is "". The reason helps a driving model see why the horn must be tapped lightly and early, while the driver is still some distance away.

- Fix: Set note to: "The handbook explains that sounding the horn may frighten a cyclist and cause them to lose control. The same block's prohibition on sounding the horn unnecessarily when overtaking a cyclist is a separate rule."
- **Proposed triage: fix, reason only.** USER-03 note: "Reason given: sounding the horn may frighten the cyclist and cause loss of control." The second proposed sentence is left out: the other sentence of 6.38 is its own rule (allow list).

## PASS-USER-04: Pass two-wheelers by changing lanes

> WHEN wanting to pass a motorcycle, bicycle, limited-speed motorcycle or moped, the DRIVER MUST pass by changing lanes, not within the same lane.

### S2-037. Cyclist passage's 'whenever possible' qualifier is dropped in the merged rule

*faithfulness* · minor · medium confidence

The rule cites 6.32 as a softer wording of the same rule and keeps the plain command of 10.24. But 6.32 is not only softer. It is also conditional: 6.32: "Whenever possible, you should change lanes to pass." The same block also expects that a cyclist can sometimes be passed with "a minimum distance of one metre, where practical", which implies passing within the lane when a lane change is not possible. The merged rule says, without exception, that the DRIVER "MUST pass by changing lanes, not within the same lane". The note mentions the softer wording but not the "whenever possible" condition, so a reader of this rule would see an unqualified ban on in-lane passing of cyclists that sits uneasily with the one-metre rule of 6.32.

- Fix: Extend the note: "6.32 words this more softly for cyclists and adds a condition ('Whenever possible, you should change lanes to pass'). The same block requires a one-metre gap when passing a cyclist, which implies in-lane passing may happen when a lane change is not possible. The unconditional command of 10.24 is recorded here." Alternatively, drop 6.32 from the evidence and leave the 6.32 advice to its own ADVICE rule with "whenever possible" listed as a vague term.
- **Proposed triage: rejected, no change.** The merge was decided in b0 m1, and the note already quotes 6.32 in full, including "Whenever possible".

## PASS-USER-06: Wait for a smaller vehicle to move right before passing

> WHEN making a left turn behind a motorcycle, bicycle, limited-speed motorcycle or moped, the DRIVER MUST NOT pass it, UNLESS the smaller vehicle has moved right.

### S2-038. Condition limits the rule to the turn itself, though the wait applies after the turn

*condition* · major · medium confidence

The rule's condition is "making a left turn behind a motorcycle, bicycle, limited-speed motorcycle or moped". In 9.18, however, the pass in question comes after the turn: 9.18: "…do not pull up beside it to make your turn at the same time. Stay behind and turn when the way is clear. Wait for the smaller vehicle to move right before you pass." The rule's own note admits that "the pass referred to is after the turn". As written, the condition stops holding once the turn is complete. A driving model could then pass the smaller vehicle on the new road before it has moved right, which is exactly the situation the handbook covers. The pronoun "it" in "pass it" also leaves the referent to inference across three vehicle types.

- Fix: when: "the DRIVER has turned left behind a motorcycle, bicycle, limited-speed motorcycle or moped (the smaller vehicle) and is still behind it"; action: "pass the smaller vehicle"; statement: "WHEN the DRIVER has turned left behind a motorcycle, bicycle, limited-speed motorcycle or moped (the smaller vehicle) and is still behind it, the DRIVER MUST NOT pass the smaller vehicle, UNLESS the smaller vehicle has moved right."
- **Proposed triage: fix as proposed (reopens S2-053 on new grounds).** S2-053 (a2) explained the timing in the note but kept a condition that stops holding once the turn is done. when: "the DRIVER has turned left behind a motorcycle, bicycle, limited-speed motorcycle or moped (the smaller vehicle) and is still behind it"; action: "pass the smaller vehicle"; statement: "WHEN the DRIVER has turned left behind a motorcycle, bicycle, limited-speed motorcycle or moped (the smaller vehicle) and is still behind it, the DRIVER MUST NOT pass the smaller vehicle, UNLESS the smaller vehicle has moved right." note: "In 9.18 this follows the instruction not to pull up beside the smaller vehicle and to stay behind it through the turn. The no-side-by-side turning instruction is PASS-USER-05." The vague term "moved right" stays. Your call if you prefer to keep the a2 decision.

## PASS-USER-08: Allow more room when passing a large vehicle

> WHEN passing a LARGE VEHICLE, the PASSER MUST allow more room in front of the LARGE VEHICLE than when passing a smaller vehicle, before returning to its lane.

### S2-039. Added placement and comparison not flagged as inference

*note* · minor · medium confidence

6.55 says only "Allow more room when passing a large vehicle." The rule adds "in front of the LARGE VEHICLE than when passing a smaller vehicle, before returning to its lane". This reading follows from the surrounding sentences in 6.55 ("do not cut in front closely … it reduces the space cushion large vehicles require in order to stop safely"), so it is reasonable. But the note does not say that the location of the extra room comes from context and is not stated in the handbook.

- Fix: Change note to: "The handbook says only 'Allow more room when passing a large vehicle'; that the room is in front of the vehicle before returning to the lane is inferred from the preceding sentences of 6.55 about not cutting in front closely and the large vehicle's stopping space cushion."
- **Proposed triage: fix, note only.** b0 m4 added the comparison, so the note should say both parts are inferred. USER-08 note: "The handbook says only 'Allow more room when passing a large vehicle'; that the room is in front of the vehicle before returning to the original lane, and more than for a smaller vehicle, is inferred from 6.55's sentences about not cutting in front closely and the longer stopping distance of large vehicles. The handbook also notes that turbulence from a large vehicle may affect control when passing it."

### S2-040. "its lane" is ambiguous

*clarity* · minor · medium confidence

In "before returning to its lane", "its" could refer to the LARGE VEHICLE or to the PASSER's vehicle. The rule means the lane the PASSER started in, which is also the lane of the vehicle being passed.

- Fix: action: "allow more room in front of the LARGE VEHICLE than when passing a smaller vehicle, before returning to the original lane"; update statement accordingly.
- **Proposed triage: fix as proposed.** action: "allow more room in front of the LARGE VEHICLE than when passing a smaller vehicle, before returning to the original lane"; statement updated to match. Same fix as S2-100 (a2).

### S2-041. Note refers to an uncited, unrelated block

*note* · minor · low confidence

The note says "The handbook also notes that turbulence from a large vehicle may affect control when passing it." That comes from 6.61, which is not cited and has nothing to do with the room-allowance rule. 6.61 is a separate advisory point that belongs to its own rule. Here it only adds noise and leaves part of the note without a citation.

- Fix: Remove the turbulence sentence from the note, or replace the note with the inference note suggested above.
- **Proposed triage: rejected, no change.** Settled in S2-055 (a2): the turbulence remark stays in the note without a citation.

## PASS-USER-09: Anticipate long commercial vehicles

> WHEN preparing to pass a LONG COMMERCIAL VEHICLE on the highway, the DRIVER SHOULD anticipate its extended length and limited speed.

### S2-042. Recognising an LCV by its rear placard is left out

*completeness* · minor · medium confidence

The caption gives two linked pieces of advice for the same situation: 18.129-c: "It is important to be able to recognize an LCV on the highway, based on rear signage, and anticipate both the extended length and limited speed when preparing to pass one…". The rule keeps only the second part: "anticipate its extended length and limited speed". It drops the advice to recognise an LCV from its rear signage. That cue is what lets a camera-based driving model tell it is behind an LCV. The vocabulary entry mentions the placard, but the rule itself does not tell the driver to look for it.

- Fix: Make the action: "recognize it as a LONG COMMERCIAL VEHICLE from its rear signage AND anticipate its extended length and limited speed". The statement then reads: "WHEN preparing to pass a LONG COMMERCIAL VEHICLE on the highway, the DRIVER SHOULD recognize it as a LONG COMMERCIAL VEHICLE from its rear signage and anticipate its extended length and limited speed." Alternatively, keep the action as it is and add a note: "The caption also advises recognizing an LCV by its rear signage."
- **Proposed triage: not an error, no change.** Recognising an LCV is in the LONG COMMERCIAL VEHICLE entry (S2-057, a2).

## PASS-USER-10: Farm machinery: do not pass until safe

> WHEN behind farm machinery or another vehicle displaying a SLOW-MOVING VEHICLE SIGN, the DRIVER MUST NOT pass, UNLESS it is safe to do so.

### S2-043. Background block 6.74 cited although it states no part of the rule

*citation* · minor · low confidence

The rule's statement rests entirely on 6.75: "If you see one of these signs, slow down and be cautious. Stay well back and do not pass until it is safe to do so." Block 6.74 is background explaining why farm machinery is hazardous: "Farm machinery moves quite slowly… Farmers often turn directly into fields rather than roads or lanes, or move from lane to lane." It does not state the passing prohibition, its condition, or its exception. Its only use is the reason given in the note. The instructions ask to "Cite only the materials directly relevant to the rule."

- Fix: Set evidence to ["6.75"]. Keep the reason in the note and attribute it to the handbook text, e.g. "Block 6.74 explains that farm machinery may turn into fields or move between lanes."
- **Proposed triage: rejected, no change.** Settled in S2-059 (a2), which set the evidence to ["6.74", "6.75"].

## PASS-USER-16: Stay 2 metres behind streetcar doors

> WHEN at a STREETCAR stop where passengers are getting off or on, the DRIVER MUST stay at least 2 metres behind the rear doors of the STREETCAR, UNLESS an area has been set aside for STREETCAR passengers at the stop.

### S2-044. Force recorded as REQUIREMENT on the strength of alt text

*strength* · minor · medium confidence

The only handbook text for this rule is a plain command. 10.45 reads: "At streetcar stops, stay at least two metres behind the rear doors…". The instructions classify a plain command such as "stay" as INSTRUCTION. The note justifies REQUIREMENT with the figure's alt text, 10.43: "a vehicle stopped the required two metres behind…". Alt text is a short image description, not handbook wording, and the image itself does not say "required". The modal is MUST under either force, so the rule's meaning does not change, but the recorded force and the note overstate the evidence.

- Fix: Set force to "INSTRUCTION" and keep modal "MUST". Change the note to: "10.45 words this as a plain command; Diagram 2-49 (10.43) shows a vehicle stopped two metres behind the rear doors of a stopped streetcar." Alternatively, keep REQUIREMENT but say in the note that it rests only on the alt-text word "required".
- **Proposed triage: rejected, no change.** Decided in b0 M2; the note quotes the alt text's "the required two metres", so the source of the force is visible.

## PASS-USER-18: Slow down for stopped emergency vehicle or tow truck

> WHEN approaching, in the DRIVER's direction of travel, an EMERGENCY VEHICLE stopped with its red, or red and blue, lights flashing OR a tow truck stopped with its amber lights flashing, the DRIVER MUST reduce speed, assessing the speed of the surrounding traffic and the condition of the roadway, and proceed with caution.

### S2-045. Jail and escalating fines are taken from the penalty for failing to stop, not failing to slow

*penalty* · minor · medium confidence

The rule's penalty reads "higher fines and up to six months in jail for further offences." That part comes from 13.117, which ties those penalties to not stopping: "Proceed with caution, clear the way and bring your vehicle to a stop, where required… If you don’t stop, you can be fined and get three demerit points for a first offence. For additional offences, fines increase and you could also go to jail for up to six months." This rule's action is to slow down and proceed with caution, not to stop. The only penalty in the shown sections that names this offence is 22.129: "Failing to slow and carefully pass a stopped emergency vehicle" (three points). 13.118 extends "the above law, fines and penalties" to a stopped tow truck, but those are still the penalties for failing to stop. Attaching them to the slow-down duty overstates what the handbook says. The note partly admits this mixing but still records the penalty as stated.

- Fix: Set penalty to "Three demerit points." and remove 13.117 and 13.118 as penalty sources. If they are kept, rewrite the note: "22.129 lists three demerit points for failing to slow and carefully pass a stopped emergency vehicle. 13.117 states fines, three demerit points and up to six months in jail for repeat offences, but for failing to stop for an emergency vehicle; 13.118 extends those to a stopped tow truck. It is unclear whether they apply to failing to slow."
- **Proposed triage: rejected, no change.** Penalty sources settled (a0 C5, S2-070).

## PASS-USER-19: Brake early and gradually for a stopped emergency vehicle or tow truck

> WHEN approaching, in the DRIVER's direction of travel, an EMERGENCY VEHICLE stopped with its red, or red and blue, lights flashing OR a tow truck stopped with its amber lights flashing, the DRIVER MUST brake early and gradually.

### S2-046. The direction condition is attached to the driver's approach, not to the stopped vehicle

*ambiguity* · minor · low confidence

The rule says "approaching, in the DRIVER's direction of travel, an EMERGENCY VEHICLE stopped…". This reads as though the driver is simply coming up behind the vehicle. The handbook ties the direction to the stopped vehicle's position: 13.107: "When approaching any emergency vehicle that is stopped … or a tow truck with its amber lights flashing in the same direction of your travel…". In other words, the stopped vehicle is on the side of the road carrying traffic in the driver's direction. 13.109 confirms this reading: "two or more lanes of traffic in the same direction of your travel… move into a lane away from the emergency vehicle". As worded, the rule leaves open whether it applies to a vehicle stopped on the opposite side of a divided road that the driver is nonetheless "approaching".

- Fix: when: "approaching an EMERGENCY VEHICLE that is stopped, with its red, or red and blue, lights flashing, on the side of the road carrying traffic in the DRIVER's direction of travel OR a tow truck that is stopped there with its amber lights flashing". Update the statement to match.
- **Proposed triage: rejected, no change.** The wording was set in S2-072/S2-073 (a2) and matched in USER-20 (b0 m2).

## PASS-USER-20: Move over for stopped emergency vehicle or tow truck

> WHEN the road has two or more lanes in the DRIVER's direction AND the DRIVER is approaching, in the DRIVER's direction of travel, either an EMERGENCY VEHICLE stopped with its red, or red and blue, lights flashing or a tow truck stopped with its amber lights flashing, the DRIVER MUST move into a lane away from the EMERGENCY VEHICLE or tow truck, well in advance, signalling and checking mirrors and BLIND SPOTS, UNLESS it is not safe to do so.

### S2-047. Penalty borrows the 'failing to stop' fines and jail term

*penalty* · minor · medium confidence

The penalty field reads "A fine and three demerit points for a first offence; higher fines and up to six months in jail for further offences." The shown handbook supports only the three demerit points for this offence: 22.130: "Failing to move, where possible, into another lane when passing a stopped emergency vehicle", listed under three points. The fine and the jail term come from 13.117: "Proceed with caution, clear the way and bring your vehicle to a stop, where required… If you don't stop, you can be fined and get three demerit points… you could also go to jail for up to six months." That passage concerns failing to stop or clear the way for an emergency vehicle, not failing to move over. 13.118 extends that same stop law to tow trucks. The rule therefore attaches another offence's fines and jail term to the move-over duty. 22.130 also names only emergency vehicles, yet the penalty is applied to tow trucks too.

- Fix: Set penalty to "Three demerit points (for a stopped emergency vehicle)." Remove 13.117 and 13.118 from evidence. Rewrite the note: "The three demerit points are listed for failing to move, where possible, into another lane when passing a stopped emergency vehicle (22.130); the handbook shown does not state a penalty specific to tow trucks for this duty."
- **Proposed triage: rejected, no change.** Penalty sources settled (a0 C5, S2-075).

### S2-048. Block defining the triggering lights is not cited

*citation* · minor · high confidence

The condition "an EMERGENCY VEHICLE stopped with its red, or red and blue, lights flashing or a tow truck stopped with its amber lights flashing" is taken from 13.107: "When approaching any emergency vehicle that is stopped with its red, or red and blue, lights flashing or a tow truck with its amber lights flashing in the same direction of your travel…". 13.109 itself only refers back to "the emergency vehicle or tow truck". 13.107 is not in the evidence.

- Fix: Add "13.107" to evidence.
- **Proposed triage: fix as proposed.** USER-20 evidence: ["13.107", "13.109", "13.117", "13.118", "22.96", "22.112", "22.130", "13.106"]. The lights in the condition come from 13.107 (error set: supporting block not cited).

### S2-049. Procedural advice folded into the legal requirement

*strength* · minor · low confidence

The action adds "signalling and checking mirrors and BLIND SPOTS" to the requirement. 13.109 states the legal duty as "you are required to move into a lane away from the emergency vehicle or tow truck, if safe to do so". It then gives a separate procedure, introduced as "Similar to the procedures noted above": "use your turn signal… double check your rearview mirrors and shoulder check your blind spots". Merging that procedure into the MUST rule blurs the stated legal duty with how-to steps. It also leaves out other steps from the same procedure, such as matching surrounding speed. The note does not mention any of this.

- Fix: Set action to "move into a lane away from the EMERGENCY VEHICLE or tow truck, well in advance". Either put the signalling and mirror/blind-spot checks in a separate INSTRUCTION rule citing 13.109 and 13.113, or add a note saying they come from the procedural part of 13.109.
- **Proposed triage: not an error, no change.** Same as S2-076 (a2): the checks are a paraphrase of 13.109's steps.

## PASS-USER-21: Slow down to pass roadside workers

> WHEN approaching workers or vehicles on the road that pose a hazard, such as roadside assistance vehicles, disabled vehicles, surveyors, road maintenance workers or utility workers, the DRIVER MUST slow down and pass with caution.

### S2-050. "that pose a hazard" reads as an extra, undefined condition

*faithfulness* · minor · medium confidence

In the rule's `when`, "workers or vehicles on the road that pose a hazard, such as …" makes posing a hazard a separate test that the driver must judge before the rule applies. The handbook instead treats the listed workers and vehicles as hazards in themselves: 13.41: "Other types of workers and vehicles may also be present on the road and pose a hazard, such as roadside assistance and disable vehicles, surveyors, road maintenance or utility workers. Always slow down and pass with caution…". As written, a model could decide that a disabled vehicle or surveyor 'does not pose a hazard' and skip slowing down. The phrase is also a judgement call but is not listed in `vague_terms`.

- Fix: Set when: "approaching workers or vehicles on or beside the road, such as roadside assistance vehicles, disabled vehicles, surveyors, road maintenance workers or utility workers". Update the statement to match: "WHEN approaching workers or vehicles on or beside the road, such as roadside assistance vehicles, disabled vehicles, surveyors, road maintenance workers or utility workers, the DRIVER MUST slow down and pass with caution." Add a note: "The handbook describes these workers and vehicles as hazards; the reason given is to prevent a collision."
- **Proposed triage: rejected, no change.** The wording was set in S2-077/S2-081 (a2) so the handbook's examples are not a closed list.

## PASS-USER-22: Move over a lane for roadside workers

> WHEN passing workers or vehicles on the road that pose a hazard, such as roadside assistance vehicles, disabled vehicles, surveyors, road maintenance workers or utility workers, AND it is safe to do so, the DRIVER MUST move over a lane to increase the space between the vehicle and the hazard.

### S2-051. Title names only roadside workers, but the rule also covers vehicles

*clarity* · minor · medium confidence

The title is "Move over a lane for roadside workers". The rule's condition, following 13.41, also covers vehicles: "roadside assistance and disable vehicles, surveyors, road maintenance or utility workers". A disabled vehicle is not a worker, so the title undersells the rule's scope.

- Fix: Change title to "Move over a lane for workers and hazardous vehicles on the road".
- **Proposed triage: fix.** title: "Move over a lane for roadside workers and vehicles" (error set: title does not match the statement, S2-058).

## PASS-USER-23: Slow down and pass animals carefully

> WHEN an animal is on or near the road, the DRIVER MUST slow down and pass carefully.

### S2-052. "pass carefully" conflicts with the ban on driving around the animal

*ambiguity* · minor · medium confidence

The rule tells the DRIVER to "slow down and pass carefully". A driving model could read "pass" as permission to steer around the animal. The same section forbids exactly that: 13.57: "Don't try to drive around the animal. Animal movements are unpredictable." Read alone, the rule does not make clear that "pass" means continuing past an animal that is beside or near the travel path, not manoeuvring around one in the way. The note does not flag this.

- Fix: Add to note: "'Pass carefully' means continuing past an animal beside or near the path of travel; it does not permit steering around an animal on the road, which 13.57 forbids ('Don't try to drive around the animal')." Optionally cite 13.57 for context.
- **Proposed triage: rejected, no change.** Weighed in S3-006: 13.57 is left out.

### S2-053. Passing an animal may be outside the overtaking scope

*scope* · minor · low confidence

The topic is "overtaking (passing another vehicle, and being passed)". 13.47 is about moving past an animal on or near the road, not about overtaking another vehicle. Under that scope, this is an animal-hazard rule rather than an overtaking rule, and including it may inflate the ground-truth set for the topic.

- Fix: Consider removing this rule from the PASS rule set, or keep it and add to note: "Included because the handbook uses 'pass'; the situation is an animal hazard, not overtaking a vehicle."
- **Proposed triage: rejected, no change.** Passing animals is in scope (S3-006).

## PASS-WX-02: No speeding up to pass in fog

> WHEN driving in fog, the DRIVER MUST NOT speed up to pass a vehicle moving slowly.

### S2-054. Rule can be misread as allowing a pass in fog if the driver does not speed up

*note* · minor · low confidence

The rule says "the DRIVER MUST NOT speed up to pass a vehicle moving slowly". Read alone, a driving model could infer that passing in fog is acceptable as long as the driver does not speed up. The same section says more about passing in fog. 14.19: "Be patient. Avoid passing, changing lanes and crossing traffic." 14.35: "Remain calm and patient. Don't pass other vehicles or speed up suddenly." The rule's statement is faithful to 14.31, but nothing in it warns a reader that passing itself is discouraged or prohibited in fog.

- Fix: Set note to: "Covers only the speeding-up part of 14.31; the second clause of 14.31 (speeding up to get away from a vehicle following too closely) concerns being followed, not passing. Passing in fog is itself addressed separately: 14.19 'Avoid passing' and 14.35 'Don't pass other vehicles'; this rule does not imply that passing without speeding up is acceptable."
- **Proposed triage: fix, link only.** WX-02 note: "Passing in fog at all is PASS-WX-01." (error set: missing link to a related rule). The rest of the proposed note is left out.

## PASS-WX-03: No passing in blowing snow or whiteout

> WHEN driving in blowing snow OR a whiteout, the DRIVER MUST NOT attempt to pass a vehicle moving slowly.

### S2-055. Broader 'avoid passing' advice of 14.68 is cited and noted as if it were the same rule

*citation* · minor · medium confidence

The rule forbids only passing "a vehicle moving slowly", taken from 14.76: "Don't attempt to pass a vehicle moving slowly…". It also cites 14.68, and the note says "14.68 also advises avoiding passing; the stronger 'Don't' of 14.76 is recorded." But 14.68 ("Be patient. Avoid passing, changing lanes and crossing traffic.") covers passing any vehicle, not just slow ones. It is not a weaker wording of the same rule. It is a separate, broader ADVICE rule. Citing it here and treating it as superseded by the narrower 'Don't' misdescribes the source. It also suggests that general advice is covered by this rule, when this rule does not cover it.

- Fix: Remove "14.68" from evidence so it reads ["14.63", "14.76"]. Change note to: "14.68 separately advises avoiding any passing in blowing snow or whiteouts; that broader advice is a separate ADVICE rule (WHEN driving in blowing snow OR a whiteout, the DRIVER SHOULD NOT pass)." If no such rule exists in the set, add it with force ADVICE, modal SHOULD NOT and evidence ["14.63", "14.68"].
- **Proposed triage: rejected, no change.** Settled in S2-083 (a2) and a0.

## PASS-BEING-02: Do not speed up when being passed

> WHEN another DRIVER is trying to pass the DRIVER's vehicle, the DRIVER being passed MUST NOT speed up.

### S2-056. List intro for passing steps cited for a being-passed rule

*citation* · minor · medium confidence

The rule cites 10.16: "Here are the steps for passing a vehicle:". That block only introduces the passing driver's steps. It says nothing about the driver being passed. The rule's support is entirely in 10.20: "…do not speed up when another driver is trying to pass you. It is unlawful and dangerous."

- Fix: Remove 10.16 from evidence. Keep 10.20, plus any test-question blocks that are retained.
- **Proposed triage: not an error, no change.** The list intro stays cited (S2-088, a2).

### S2-057. Wrong-answer test option cited as support for a prohibition

*citation* · minor · low confidence

The rule cites 28.22, 28.23 and 28.42. The answer key (28.42: "5-d") only says the correct answer is 28.26: "Move to the right and allow such vehicle to pass." Option 28.23 ("Speed up so that passing is not necessary") is not the answer, but the question asks what the driver must do. It does not state that speeding up is prohibited. These blocks are at best indirect support. The rule's prohibition and its REQUIREMENT force come from 10.20 alone.

- Fix: Either drop 28.22, 28.23 and 28.42 from evidence, leaving ["10.20"], or keep them and rewrite the note: "Stated as unlawful and dangerous in 10.20. Sample test question 5 (28.22) gives 'move to the right and allow such vehicle to pass' (28.26) as the answer (28.42) and lists 'speed up' (28.23) as a wrong option; this is indirect support only."
- **Proposed triage: rejected, no change.** Settled in S2-088 (a2); the note already says the test lists "speed up" as a wrong answer.

### S2-058. Ambiguous reference to 'the DRIVER's vehicle' with two drivers

*clarity* · minor · low confidence

The condition reads "another DRIVER is trying to pass the DRIVER's vehicle". It mentions two DRIVERs, so "the DRIVER's vehicle" could be misread as the passing driver's own vehicle. The actor "DRIVER being passed" only appears after the condition.

- Fix: when: "another DRIVER is trying to pass the vehicle of the DRIVER being passed"; statement: "WHEN another DRIVER is trying to pass the vehicle of the DRIVER being passed, the DRIVER being passed MUST NOT speed up."
- **Proposed triage: rejected, no change.** Settled in S2-089 (a2): the condition was fixed and the actor kept.

## PASS-BEING-03: Do not block a vehicle from passing

> WHEN another vehicle is passing or trying to pass, the DRIVER MUST NOT drive the vehicle so as to prevent the other vehicle from passing.

### S2-059. Sample-test citations do not state this prohibition

*citation* · minor · medium confidence

The rule cites 28.22, 28.24 and 28.42. These blocks are a multiple-choice question and its answer key. 28.22: "When the driver of another vehicle is about to overtake and pass your vehicle, you must:" and 28.42: "5-d". Together they support a different rule, namely 28.26: "Move to the right and allow such vehicle to pass." 28.24 ("Move to the left to prevent passing.") is only a wrong answer option, so it states no rule. Citing it as evidence is weak support. It is also selective: 28.23 ("Speed up so that passing is not necessary.") is an equally wrong option and is not cited. The prohibition itself rests on 23.19 and 23.22.

- Fix: Change evidence to ["23.19", "23.22"]. Use 28.22, 28.26 and 28.42 for a separate rule about moving right to let the vehicle pass, if that rule is extracted. Change the note to: "Listed among aggressive driving behaviours under 'Sanctions – dangerous behaviours' (23.17–23.22)."
- **Proposed triage: rejected, no change.** Settled in S2-090 (a2), which added the answer key.

### S2-060. Condition does not say the other vehicle is passing the DRIVER

*clarity* · minor · medium confidence

The condition reads "another vehicle is passing or trying to pass" and does not say who is being passed. The rule only makes sense when the DRIVER is the one being passed, or is in a position to block the pass. As worded, "the vehicle" in the action has no clear antecedent, and the condition could be read as any pass anywhere.

- Fix: Set when to: "another vehicle is passing or trying to pass the DRIVER's vehicle". Set action to: "drive so as to prevent the other vehicle from passing". Statement: "WHEN another vehicle is passing or trying to pass the DRIVER's vehicle, the DRIVER MUST NOT drive so as to prevent the other vehicle from passing."
- **Proposed triage: fix as proposed.** Same as S2-089 (a2) for BEING-02. when: "another vehicle is passing or trying to pass the DRIVER's vehicle"; action: "drive so as to prevent the other vehicle from passing"; statement: "WHEN another vehicle is passing or trying to pass the DRIVER's vehicle, the DRIVER MUST NOT drive so as to prevent the other vehicle from passing."

## PASS-BEING-04: Being passed on an undivided road: keep right

> WHEN on an undivided road AND the PASSER has pulled into the opposite lane, the DRIVER being passed MUST pay attention to oncoming traffic and move closer to the right side of the lane.

### S2-061. "opposite lane" does not say which lane is meant

*clarity* · minor · low confidence

The condition reads "the PASSER has pulled into the opposite lane". The handbook uses the same words (10.25: "…where the passing driver has pulled into the opposite lane…"), and in context it means the lane for oncoming traffic. Read on its own, "opposite lane" is less clear than it could be for a driving model, which needs to recognise the situation from sensors. The phrase "pay attention to oncoming traffic" does point to this meaning, so the risk of misreading is small.

- Fix: Change `when` to "on an undivided road AND the PASSER has pulled into the lane for oncoming traffic to pass the DRIVER" and update `statement` to match.
- **Proposed triage: not an error, no change.** Low confidence. The wording is the handbook's, and "pay attention to oncoming traffic" fixes the meaning.

## PASS-BEING-05: Be ready to slow to help the passer in

> WHEN on an undivided road AND the PASSER has pulled into the opposite lane, the DRIVER being passed MUST be prepared to slow down to let the PASSER get in front more quickly to prevent a collision.

### S2-062. The handbook's reason is written into the action

*form* · minor · low confidence

The action reads "be prepared to slow down to let the PASSER get in front more quickly to prevent a collision". The phrase "to prevent a collision" is the handbook's reason for the instruction, not part of what the driver does. 10.25: "Be prepared to slow down to let the passing driver get in front of you more quickly to prevent a collision." The instructions say reasons the handbook gives belong in `note`. Here the note is empty. Keeping the purpose in the action adds nothing a driving model can act on, and it could be read as limiting the instruction to cases where a collision is foreseen.

- Fix: action: "be prepared to slow down to let the PASSER get in front more quickly"; statement: "WHEN on an undivided road AND the PASSER has pulled into the opposite lane, the DRIVER being passed MUST be prepared to slow down to let the PASSER get in front more quickly."; note: "The handbook gives the reason: to prevent a collision. The same block also tells the driver to watch oncoming traffic and keep right; those are separate rules."
- **Proposed triage: fix, note shortened.** action: "be prepared to slow down to let the PASSER get in front more quickly"; statement updated to match; note: "Reason given: to prevent a collision." The second proposed note sentence is left out (allow list).

## PASS-BEING-06: Clear the truck passing lane

> WHEN driving in the TRUCK PASSING LANE AND a truck wants to pass, the DRIVER MUST move into the lane to the right of the TRUCK PASSING LANE as soon as possible.

### S2-063. Handbook's vague wording replaced with a paraphrase

*vague terms* · minor · medium confidence

The instructions say to keep the handbook's own words for vague phrases. The handbook says 10.26: "…move into the right-hand lane as soon as you can." The rule's action instead says "as soon as possible", and the vague_terms entry lists the paraphrase. The note admits the substitution but gives no reason for it, so the paraphrase is unnecessary.

- Fix: action: "move into the lane to the right of the TRUCK PASSING LANE as soon as you can"; update the statement to match; vague_terms term: "as soon as you can" (explanation: "no time or distance given"); note: "".
- **Proposed triage: not an error, no change.** Paraphrasing a vague phrase close to the handbook is fine (a0 G5, S2-093).

### S2-064. Interpretation of 'right-hand lane' not flagged

*note* · minor · low confidence

The handbook says "move into the right-hand lane" (10.26). On a road with three or more lanes each way, this could mean the next lane to the right or the far-right lane. The rule reads it as "the lane to the right of the TRUCK PASSING LANE". That reading is plausible, but the note does not say it is an interpretation.

- Fix: Add to note: "Handbook says 'move into the right-hand lane'; read here as the lane immediately to the right of the TRUCK PASSING LANE, though it could also be read as the far-right lane."
- **Proposed triage: fix, note only.** S2-096 (a2) changed the action without saying it is a reading. BEING-06 note: "Handbook wording is 'as soon as you can'. 'Move into the right-hand lane' (10.26) is read as the lane to the right of the TRUCK PASSING LANE."

## PASS-TOW-02: Towing: do not cut back in too soon

> WHEN returning to the original lane after passing, the DRIVER towing a trailer MUST allow more room than when not towing before moving back and not cut back into the lane too soon.

### S2-065. A MUST NOT prohibition is folded into a MUST action

*grammar* · minor · medium confidence

The action "allow more room than when not towing before moving back and not cut back into the lane too soon" joins a positive duty and a prohibition under one modal, MUST. The handbook states them as two commands, 27.45: "Once you have passed, allow more room before you move back to your lane. Do not cut back into the lane too soon." Writing "MUST … not cut back" hides a prohibition inside a MUST, which the grammar's MUST NOT modal exists to express. It also makes the rule harder for programs to read and compare. The second clause adds little, since it restates the first as a prohibition. Also, "the lane" is less clear than "the original lane".

- Fix: Keep MUST and make the action "allow more room than when not towing before moving back into the original lane, so as not to cut back in too soon". The statement becomes: "WHEN returning to the original lane after passing, the DRIVER towing a trailer MUST allow more room than when not towing before moving back into the original lane, so as not to cut back in too soon." Alternatively, split it into a MUST rule (allow more room) and a MUST NOT rule ("cut back into the original lane too soon").
- **Proposed triage: not an error, no change.** Positive-first, negated-last pattern (S2-101, a2); the condition already names the original lane.

## PASS-TOW-04: Towing: wind from a passing truck or bus

> WHEN a large bus or truck passes AND its wind pushes the trailer to the side, the DRIVER towing a trailer MUST carefully steer the vehicle and trailer back into position and not brake.

### S2-066. A prohibition is hidden inside a MUST action

*grammar* · minor · medium confidence

The action "carefully steer the vehicle and trailer back into position and not brake" puts the handbook's prohibition 27.47: "do not brake" inside a MUST clause as "MUST … not brake". The grammar gives each rule a single MODAL, and MUST NOT exists for prohibitions. Joining the two lets a program that reads the modal field see only an obligation to steer and miss the ban on braking.

- Fix: Split into two rules with the same when and evidence ["27.47"]: (a) modal "MUST NOT", action "brake", statement "WHEN a large bus or truck passes the DRIVER AND its wind pushes the trailer to the side, the DRIVER towing a trailer MUST NOT brake."; (b) modal "MUST", action "carefully steer the vehicle and trailer back into position", statement "WHEN a large bus or truck passes the DRIVER AND its wind pushes the trailer to the side, the DRIVER towing a trailer MUST carefully steer the vehicle and trailer back into position."
- **Proposed triage: not an error, no change.** Same pattern (a0 M3, S2-103).

### S2-067. Condition does not say the bus or truck is passing the driver

*clarity* · minor · medium confidence

The condition "a large bus or truck passes" does not say what is being passed. It could be read as any truck going by, including one in the opposite direction. The handbook says 27.47: "If a large bus or truck passes you, the wall of wind behind it may whip your trailer to the side", under the heading "Being passed".

- Fix: when: "a large bus or truck passes the DRIVER AND its wind pushes the trailer to the side"
- **Proposed triage: fix as proposed.** when: "a large bus or truck passes the DRIVER AND its wind pushes the trailer to the side"; statement updated to match. Same kind of fix as S2-089 (a2).

## No findings (12 rules)

PASS-PROC-06, PASS-LOC-02, PASS-MARK-01, PASS-SIGN-01, PASS-SIGN-02, PASS-USER-12, PASS-USER-13, PASS-USER-14, PASS-USER-15, PASS-USER-17, PASS-BEING-01, PASS-TOW-03
