# Aggregate check (stage 3): gold_set\ca\overtaking\b2_atomic.json

Judge: anthropic/claude-opus-5-5 · run folder: `runs\20261121-184446-check-aggregate-overtaking-b3` (request, response, findings.jsonl, triage.csv) · 52 rules, whole corpus · $0.5773

**11 findings** (4 major, 7 minor): 3 coverage, 5 conflict, 3 other.

**Triage:** all 11 findings were triaged. The reviewer accepted the triages Claude Code proposed: 1 fixed, 2 fixed partly (note only), 8 rejected. Each decision is recorded under its finding as a **Triage** line, weighed against the CA triages (a0, a2, a3, b0, b2). Fixes were applied to `b3_aggregate.json`, which started as an exact copy of `b2_atomic.json`.
- USER-02 now has "UNLESS the LARGE VEHICLE is signaling a left turn" and cites 10.202 (S3-005). The other changes are note edits on SIDE-01, SIDE-02 and GEN-05.
- No rules or vocabulary terms were added: 52 rules and 16 vocabulary terms.
- Format check (`check_format.py b3_aggregate.json --handbook ca --allow-lowercase pass`): no format errors.

## Coverage

### S3-001. SLOWER TRAFFIC KEEP RIGHT regulatory sign not used

*missing citation / sign* · minor · medium confidence · rules: PASS-BEING-04

Figure 12.89 shows the White Regulatory Sign "SLOWER TRAFFIC KEEP RIGHT", and 12.85 says such signs communicate "rules you must obey". This sign is about letting faster traffic pass. The set uses the DO NOT PASS sign from the same figure (LOC-07) but ignores this one. BEING-04 cites only 13.144. The slower-traffic-keep-right instruction in 13.144 ("If you choose to drive slower than other traffic, drive in the right lane") is relegated to a note.

- Fix: Add a rule PASS-BEING-11 with force REQUIREMENT, modal MUST, actor DRIVER. when: "a SLOWER TRAFFIC KEEP RIGHT sign is posted AND the DRIVER is driving slower than other traffic"; action: "drive in the right lane". Evidence: ["12.85","12.89","13.144"]. Note: the rule rests partly on the sign image.
- **Triage: rejected.** SLOWER TRAFFIC KEEP RIGHT is a general rule of the road, not specific to passing. The same content in 13.144 was ignored at a3 S3-006 and kept only in BEING-04's note (a0 N3).

### S3-002. Double-yellow barrier (two sets of double lines) not covered

*missing rule* · minor · medium confidence · rules: PASS-MARK-02

10.13: "Two sets of solid double yellow lines spaced two or more feet apart are considered a barrier. Do not drive on or over this barrier … except at designated openings." This is stricter than MARK-02: the left-turn and HOV exceptions in MARK-02 do not apply to it. No rule captures it, although it governs whether a driver may cross to pass.

- Fix: Add a rule PASS-MARK-05 with force INSTRUCTION, modal MUST NOT, actor DRIVER. when: "there are two sets of solid double yellow lines spaced two or more feet apart"; action: "drive on or over them"; unless: "at a designated opening". Evidence: ["10.13"].
- **Triage: rejected.** Re-raises a0 O4, where 10.13's barrier was ignored. No new evidence.

### S3-003. Truck No-Zone guidance relevant to passing is not captured

*missing rule (boundary)* · minor · low confidence · rules: PASS-USER-03

13.4: "Large vehicle and truck drivers … have large blind spots, also called No Zones … If you cannot see the truck's side mirrors, the truck driver cannot see you." 15.18: "Do not stay in another driver's blind spot." 15.19: "Avoid driving directly alongside other vehicles." These bear directly on how long to stay beside a vehicle while passing it. USER-03 cites only 13.14, and only for large vehicles. This is a boundary case for the topic.

- Fix: Add 13.4, 13.5 and 15.18 to USER-03's evidence and note. Optionally, add an ADVICE rule. when: "passing another vehicle"; modal SHOULD NOT; action: "stay in the other driver's blind spot or alongside the vehicle longer than needed". Evidence: ["15.18","15.19","13.4"].
- **Triage: rejected.** Low confidence. Blind spots and driving alongside other vehicles are general rules of the road (a3 S3-005, S3-006). USER-03's reason is already in its note, and something mentioned only in a note needs no citation (a2 S2-044).

## Conflicts

### S3-004. SIDE-01's MAY ONLY wording forbids left passing in cases where USER-05 allows it

*contradiction* · major · high confidence · rules: PASS-SIDE-01, PASS-USER-05

SIDE-01 puts the allowed cases in the WHEN clause and "pass on the right" as the action: "WHEN … the PASSER is on a one-way street OR the PASSER is overtaking a LIGHT RAIL VEHICLE, the PASSER MAY ONLY pass on the right." Under the defined meaning of MAY ONLY, this reads as "in these situations, passing is allowed only on the right". On a one-way street, that forbids passing on the left. USER-05 explicitly allows passing a LIGHT RAIL VEHICLE on the left when "the PASSER is on a one-way street" (13.24). The handbook means the reverse of SIDE-01's wording. 10.200: "You may pass on the right only when: …" means passing on the right is restricted to these cases, not that left passing is forbidden in them.

- Fix: Rewrite the statement so that passing on the right is the restricted action and the cases are the only conditions that allow it. For example: when: "overtaking a vehicle"; modal MAY ONLY; action: "pass on the right"; unless: "". Put the three cases from 10.201–10.203 into the condition: "WHEN an open highway has two or more lanes going in the PASSER's direction OR the DRIVER ahead is turning left and the PASSER can safely pass on the right OR the PASSER is on a one-way street, the PASSER MAY pass on the right". Add a note that passing on the right is not permitted in any other case. Alternatively, keep MAY ONLY but state explicitly that the restriction is on right-side passing.
- **Triage: fixed partly (note only), as proposed.** The finding misreads MAY ONLY. The prompt defines it as 'allowed when the condition holds, and not otherwise', so SIDE-01 limits passing on the right to its four cases and says nothing about passing on the left. That matches 10.200 and leaves USER-05's one-way-street exception intact. Three judges have now tripped on this reading (b2 S2-013, b3 S3-004, b3 S3-009), so add to SIDE-01's note: "MAY ONLY limits passing on the right to these cases; it does not restrict passing on the left." The statement is unchanged.

### S3-005. Large vehicle signaling a left turn: one rule requires a left pass, another forbids it

*contradiction* · major · medium confidence · rules: PASS-USER-02, PASS-SIDE-02, PASS-SIDE-01

USER-02 says "WHEN passing a LARGE VEHICLE, the PASSER MUST pass on the left side", with no exception, and its note says it overrides SIDE-01. SIDE-02 says "WHEN the DRIVER ahead is signaling a left turn, the PASSER MUST NOT pass on the left." For a truck signaling a left turn, the two rules leave no legal way to pass. The handbook's own warning that a truck may swing wide (13.10) makes this situation realistic. Neither rule says which one prevails.

- Fix: Add an exception to USER-02, unless: "the LARGE VEHICLE is signaling a left turn (see SIDE-02)". Or add a note to both rules stating that, for a large vehicle turning left, the PASSER should not pass on the left and should pass on the right only where SIDE-01 allows it. Otherwise the PASSER should wait.
- **Triage: fixed as proposed.** New and real: for a LARGE VEHICLE signalling a left turn, USER-02 (always pass on the left) and SIDE-02 (never pass on the left of a driver signalling a left turn) leave no legal pass. Use the exception option. USER-02 gets "UNLESS the LARGE VEHICLE is signaling a left turn", adds `10.202` to its evidence, and its note adds: "When the LARGE VEHICLE signals a left turn, SIDE-02 applies: do not pass on the left; pass on the right only where SIDE-01 allows. The exception is inferred from 10.202, which the handbook states for any driver ahead." SIDE-02's note adds: "Applies to a LARGE VEHICLE too; USER-02 makes an exception for this case."

### S3-006. One handbook sentence on being passed is split into two rules

*split rule / duplicate* · minor · medium confidence · rules: PASS-BEING-01, PASS-BEING-10

10.206 says: "allow the vehicle to pass. Maintain your lane position and your speed." BEING-01 says to "allow the vehicle to pass and maintain speed", and BEING-10 says to "maintain lane position". Both have the same condition and cite the same block. The instructions say not to split one rule into pieces. BEING-01 on its own reads as though lane position is not required.

- Fix: Merge them into BEING-01, with action: "allow the vehicle to pass and maintain lane position and speed". Add unless: "the passing vehicle is a motorcycle AND it is possible to move to one side of the lane (see BEING-06)". Use evidence ["10.206","13.41"]. Delete BEING-10 and update the cross-references in BEING-01, BEING-05 and BEING-06.
- **Triage: rejected.** Re-raises b2 S2-042: the split was accepted so the motorcycle exception lifts only lane position, not the duty to allow the pass. BEING-01's note points to BEING-10.

### S3-007. General turnout rule makes the legal turnout thresholds meaningless

*overlapping conditions* · minor · low confidence · rules: PASS-BEING-02, PASS-BEING-03

BEING-02 says a DRIVER MUST merge into a TURNOUT whenever "cars are behind the DRIVER AND the DRIVER is slower". BEING-03 says a DRIVER MUST use a TURNOUT only when driving slowly, passing is unsafe, and "five or more vehicles are following" (10.67: "You must use a turnout … when … there are five or more vehicles following you"). Because both are MUST, BEING-02 covers every case of BEING-03, so BEING-03's thresholds add nothing. Since 10.67 states the legal requirement precisely, BEING-02's 10.65 imperative is better read as advice or as a description of what turnouts are for.

- Fix: Choose one of two fixes. Downgrade BEING-02 to ADVICE/SHOULD, with a note that the legal duty is BEING-03. Or keep it as MUST and add a note that the legal requirement applies at the 10.67 thresholds, and explain how the two relate.
- **Triage: rejected.** Settled at a3 S3-009, where BEING-02 went back to INSTRUCTION and both notes say how the two rules relate (the finding's second option).

### S3-008. Same passing prohibitions use different actors (DRIVER vs PASSER)

*inconsistent terms* · minor · medium confidence · rules: PASS-MARK-01, PASS-LOC-04, PASS-LOC-05, PASS-USER-06, PASS-LOC-01, PASS-LOC-02

Passing prohibitions are assigned to "PASSER" in some rules, such as LOC-01, LOC-02 and LOC-03. Equivalent prohibitions use "DRIVER" in others: MARK-01 "the DRIVER MUST NOT pass a vehicle in front", LOC-04, LOC-05 and USER-06. Nothing in the handbook supports the distinction, and checking programs comparing actors would treat these rules as having different scopes.

- Fix: Use PASSER consistently for every rule whose action is to pass or not pass. Keep DRIVER for being-passed and general-driving rules.
- **Triage: rejected.** The PASSER vs DRIVER inconsistency was ignored at a3 S3-011.

## Other

### S3-009. Light-rail case added to the handbook's closed list of right-pass permissions without support

*unsupported rule content* · major · medium confidence · rules: PASS-SIDE-01, PASS-USER-05

10.200 gives an exhaustive list ("You may pass on the right only when": 10.201–10.203). SIDE-01 adds a fourth case, "OR the PASSER is overtaking a LIGHT RAIL VEHICLE", taken from 13.22. However, 13.22 only forbids passing such a vehicle on the left ("Do not overtake and pass a light rail vehicle or streetcar on the left side…"). It grants no permission to pass on the right, for example on a two-lane road with a single lane each way. The added case creates a permission the handbook does not state.

- Fix: Remove the light-rail disjunct from SIDE-01 and remove 13.22 from its evidence. Leave USER-05 as the only rule on light rail. In USER-05's note, delete the claim that SIDE-01 permits the right side.
- **Triage: rejected.** Re-raises a3 S3-008 (the reviewer's fourth case) and b2 S2-013 (rejected). No new evidence. The S3-004 note makes the reading clearer.

### S3-010. Bicyclist keep-right rule drops most of the handbook's exceptions

*missing exception* · major · high confidence · rules: PASS-USER-14

USER-14 requires a slower BICYCLIST to ride as close as possible to the right edge, "UNLESS passing a vehicle or another bicycle". 13.101 lists six exceptions: 13.103 left turn, 13.104 avoiding a hazard, 13.105 lane too narrow to share, 13.106 approaching a right turn, 13.107 one-way road with two or more lanes. The note dismisses these as "outside the overtaking topic". Leaving them out does not narrow the rule. It makes the rule require a bicyclist to stay right while turning left or avoiding a hazard, which the handbook does not require. Conditions and exceptions must stay with the rule.

- Fix: Extend unless to: "passing a vehicle or another bicycle going in the same direction OR preparing to make a left turn OR avoiding a hazard or road condition OR the lane is too narrow for a bicycle and a vehicle to safely travel side-by-side OR approaching a right turn OR on a one-way road with two or more lanes". Cite 13.101–13.107 and remove the note's claim.
- **Triage: rejected.** Re-raises a2 S2-048 (only passing-related exceptions) and b2 S2-028 (rejected). No new evidence.

### S3-011. Plain command 'Use the left lane to pass' recorded as advice, unlike similar commands

*inconsistent strength* · minor · low confidence · rules: PASS-GEN-05, PASS-PROC-01, PASS-USER-11

10.33, "Use the left lane to pass or turn left", is a plain command, which the instructions class as INSTRUCTION (MUST). GEN-05 records it as ADVICE/SHOULD. Other plain commands in the set are recorded as MUST, for example PROC-01 from 10.195–10.199 and USER-11 from 17.13's worked example. The framing "tips" in 10.32 is the only basis for the downgrade, and the rule's note does not give it as the reason.

- Fix: Either change GEN-05 to force INSTRUCTION and modal MUST, or keep ADVICE and add a note that the downgrade rests on the "tips" framing in 10.32.
- **Triage: fixed partly (note only), as proposed.** Re-raises a2 S2-007 and b2 S2-004, so the strength stays ADVICE. But this is the third time the judge has said the note doesn't give the reason for ADVICE, so make it explicit: GEN-05's note "Given as a tip for choosing a lane (10.32, 10.33);" becomes "Given as a tip for choosing a lane (10.32, 10.33), so recorded as ADVICE although 10.33 is worded as a command;".
