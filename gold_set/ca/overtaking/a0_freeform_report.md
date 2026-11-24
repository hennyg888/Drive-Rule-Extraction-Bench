# Freeform error check: `gold_set/ca/overtaking/00_raw_rules.json`

Source: `corpus/ca` · Prompt: `prompts/formal-rules` (system.md, task.md, schema.json) · Topic: overtaking

Quotations from the handbook are given as `id`: "text", and some are trimmed with "…". Image links point to `handbooks/ca/images/`.

**What was checked**

- Every cited block id was resolved against the corpus HTML. One id does not exist (C1).
- The stage-1 script was run for an early view: `check_format.py 00_raw_rules.json --handbook ca --allow-lowercase pass`. It reports 5 errors (C1, V1, V2). Schema, statement-vs-fields, ids and numbering, force/modal and vague-term presence all pass.
- Each rule was read against the text of its cited blocks and the blocks around them (list lead-ins, headings, neighbouring sentences).
- The cited figures were viewed: [10.9](../../../handbooks/ca/images/Double_Solid_Yellow_Lines.png), [10.70](../../../handbooks/ca/images/Bicycle_Lane.png), [13.20](../../../handbooks/ca/images/Bus-Safety-Zone-1.png). The alt text of 10.66, 13.111 and 13.113 is clear enough on its own.
- The whole corpus was searched for "pass", "overtak", "turnout", "tailgat", "left lane", "right lane", "faster", "lane split" and similar, to find rules that were left out.
- The MTO overtaking triage records (`gold_set/mto/overtaking/allow_list.md`, `error_set.md`) were applied. Findings of a kind the allow list rejects are not raised. Findings that match a confirmed MTO error type cite it as "MTO precedent".

**Result:** 42 rules in 8 groups (GEN 5, MARK 3, LOC 5, PROC 2, SIDE 2, USER 17, COND 1, BEING 7) and 14 vocabulary terms. The JSON fits the schema and every statement matches its fields word for word. Strength is mostly right, and coverage of the handbook's Passing section (10.183–10.206) is complete. The errors found are listed below, grouped by severity: 6 major, 27 minor.

**Triage:** all findings have been triaged. Fixes were applied to `a0_freeform.json`, which started as an exact copy of `00_raw_rules.json`. Each decision is recorded under its finding as a **Triage** line. The majors were fixed first, then the minors, then V3 (verb/noun casing of PASS).
- Every statement was rebuilt from its fields after the fixes.
- Two rules were added at the end of their groups, so no rules were renumbered: PASS-LOC-06 (M6) and PASS-MARK-04 (O1).
- After all fixes there are 44 rules and 14 vocabulary terms.
- Format check (`check_format.py a0_freeform.json --handbook ca --allow-lowercase pass`): no format errors.
- The major and minor fixes first kept the draft's capitalized verb PASS. V3 then lowercased every verb use across the set, so the quotes in earlier Triage lines may show "PASS" where the file now has "pass".

Severity: **Major** means the rule says something the handbook does not, misstates its strength, breaks the grammar or vocabulary contract, or a clear rule is missing. **Minor** covers citation, wording, vague-term, note and organisation issues.

---

## Major

### M1. MAY ONLY turns a permission into a prohibition the handbook does not state (PASS-MARK-03)
"WHEN a broken yellow line is next to the PASSER's driving lane AND it is safe, the PASSER MAY ONLY PASS." MAY ONLY means "allowed when the condition holds, and not otherwise", so the rule says passing is allowed *only* where a broken yellow line is next to the lane. That forbids passing on a multilane road with broken white lines, on a one-way street, or on the right where SIDE-01 allows it. In the handbook the "only" belongs to the safety condition, not to the broken line.
- `10.15`: "A broken yellow line indicates you **may** pass if the broken line is next to your driving lane. **Only pass when it is safe.**"
- MTO precedent: `error_set.md`, "MAY ONLY reading in a prohibition the handbook does not state" (b2 S2-028).
- Fix: modal `MAY`. Keep "AND it is safe" in the condition, and update the note: "Combines the permission with 'Only pass when it is safe'; the broken line does not restrict passing elsewhere."
- Confidence: high.
- **Triage: fixed as proposed.** MARK-03 is now PERMISSION / MAY: "WHEN a broken yellow line is next to the PASSER's driving lane AND it is safe, the PASSER MAY PASS." The note is replaced with the proposed text.

### M2. AND and OR mixed with no grouping (PASS-SIDE-01)
"WHEN an open highway has two or more lanes going in the PASSER's direction OR the driver ahead is turning left AND the PASSER can safely PASS on the right OR the PASSER is on a one-way street, …". With no brackets this can be read as (A OR B) AND (C OR D), which would require "can safely pass on the right" on an open highway, or would allow passing on the right on a one-way street only when the driver ahead is turning left. The handbook has three separate cases, and "safely" belongs only to the left-turn case:
- `10.200`: "You may pass on the right only when:"
- `10.201`: "An open highway has two or more lanes going in your direction."
- `10.202`: "The driver ahead of you is turning left and you can safely pass on the right. …"
- `10.203`: "You are on a one-way street."
- MTO precedent: `error_set.md`, "A condition whose scope is unclear", a0 G1. The convention is to join the parts of one case with a lowercase word inside a single fact.
- Fix: "WHEN an open highway has two or more lanes going in the PASSER's direction OR the DRIVER ahead is turning left and the PASSER can safely pass on the right OR the PASSER is on a one-way street, the PASSER MAY ONLY PASS on the right." (This also fixes V2.)
- Confidence: high.
- **Triage: fixed as proposed**, except that "safely PASS" keeps the capitalized verb. The rest of the draft writes the verb as PASS, and casing is left to V3. The condition is now "an open highway has two or more lanes going in the PASSER's direction OR the DRIVER ahead is turning left and the PASSER can safely PASS on the right OR the PASSER is on a one-way street". This also fixes V2 for SIDE-01.

### M3. A second, lowercase modal inside the action (PASS-MARK-02)
"…the DRIVER MUST NOT pass over the double solid yellow lines, **and must stay to the right of them**, UNLESS …". The grammar allows one MODAL per rule. The lowercase "must" adds an unlisted second duty, and the scope of "MUST NOT" over "and must stay" reads as a double negative. The handbook's exceptions are attached to the "Stay to the right" sentence:
- `10.8`: "Do not pass over double solid yellow lines. Stay to the right of these lines unless you are:"
- Fix: drop the second clause. The rule becomes "WHEN the road has double solid yellow lines, the DRIVER MUST NOT pass over them, UNLESS …", with the three exceptions unchanged, which already covers staying to their right. Alternatively, split it into a MUST NOT rule and a MUST rule ("MUST stay to the right of them, UNLESS …").
- Note: stage 1 has no check for a lowercase modal in `action`, so this passes the format check.
- Confidence: high.
- **Triage: fixed differently, by rewording into the positive-first, negated-last pattern.** MARK-02 is now INSTRUCTION / MUST: "WHEN the road has double solid yellow lines, the DRIVER MUST stay to the right of the double solid yellow lines and not pass over them, UNLESS …". The three exceptions are unchanged. This matches 10.8, where the exceptions attach to "Stay to the right".

### M4. A lowercase "not" before the positive duties in a MUST action (PASS-USER-03, PASS-USER-11)
- USER-03: "the PASSER MUST not drive next to it longer than needed, and move ahead of it after passing". This can be read as "MUST NOT (drive next to it … and move ahead of it)", which forbids moving ahead, the very thing 13.14 tells you to do.
  - `13.12`: "…When driving near large vehicles and trucks, do not:"
  - `13.14`: "Drive next to them longer than you need to. … After you pass the large vehicle or truck, move ahead of it. …"
- USER-11: "the DRIVER MUST not drive between the vehicle and the BICYCLIST, but slow down, let the oncoming vehicle pass, then move left …". The "but" helps, but the action still starts with the ban and chains three duties after it.
  - `17.13`: "Instead of driving between the vehicle and the bicyclist, take one danger at a time. Slow down and let the oncoming vehicle pass. When the vehicle has passed, move to the left …"
- MTO precedent: a0 M3 (confirmed). The allowed pattern is positive first, negated last (`allow_list.md`).
- Fix:
  - USER-03: "…MUST move ahead of it after passing and not drive next to it longer than needed."
  - USER-11: "…MUST slow down, let the oncoming vehicle pass, then move left to allow at least three feet to pass the BICYCLIST, and not drive between the vehicle and the BICYCLIST."
- Confidence: high for USER-03, medium for USER-11.
- **Triage: fixed as proposed**, keeping the capitalized "PASS the BICYCLIST" in USER-11 as in the draft (see V3).
  - USER-03: "WHEN passing a LARGE VEHICLE, the PASSER MUST move ahead of it after passing and not drive next to it longer than needed."
  - USER-11: "…the DRIVER MUST slow down, let the oncoming vehicle pass, then move left to allow at least three feet to PASS the BICYCLIST, and not drive between the vehicle and the BICYCLIST."

### M5. PASSING LANE (far left lane of a multilane road) is used for the lane a passer pulls into on any open highway (PASS-PROC-01)
The vocabulary defines PASSING LANE from 10.46: "On a multilane road, the far left lane closest to the center divider, used to pass other vehicles." PROC-01 writes "WHEN going to PASS on an open highway, the PASSER MUST … drive into the PASSING LANE …". On a two-lane open highway, the lane a passer pulls into is the oncoming lane. That is not a PASSING LANE as defined, so either the rule applies only to multilane roads (which 10.194 does not say), or the CAPS term is used with a different meaning.
- `10.194`: "When you are going to pass on an open highway:" · `10.197`: "Drive into the passing lane."
- This differs from the allowed MTO case (a0 V3), where the phrase stayed lowercase and so was not bound by the definition. Here it is in CAPS.
- MTO precedent: a1, where "move into the passing lane" was reworded to "change lanes to pass".
- Fix: in PROC-01, replace "drive into the PASSING LANE" with "move into the lane used for passing", and add a note that 10.197 says "the passing lane" without saying which lane on a two-lane road. GEN-05's "the left lane (the PASSING LANE)" on a multilane road fits the definition and can stay.
- Confidence: medium-high.
- **Triage: fixed as proposed.** PROC-01's action now reads "…look over the shoulder to check blind spots, move into the lane used for passing, speed up to PASS the vehicle, …". Its note is now "10.197 says 'the passing lane' without saying which lane on a two-lane road." GEN-05 and the PASSING LANE vocabulary entry are unchanged.

### M6. Missing rule: the center left turn lane is not a passing lane (10.56)
- `10.56`: "…Use the center left turn lane to prepare for and make a left turn or U-turn. **It is not a regular traffic lane or passing lane.** You may only drive for 200 feet in the center left turn lane. …"

This restricts where a pass may be made and can be recognised from the markings ("marked on both sides by two painted lines. The inner line is broken and the outer line is solid"). The MTO gold set has the same rule as PASS-LOC-05 ("MUST NOT use the TWO-WAY LEFT-TURN LANE for passing").
- Fix: add `PASS-LOC-06`: INSTRUCTION / MUST NOT, actor DRIVER, "WHEN on a road with a center left turn lane, the DRIVER MUST NOT use the center left turn lane to PASS.", evidence `10.55`, `10.56`. Add a note: "Inferred from 'It is not a regular traffic lane or passing lane' together with the instruction to use it only for left turns and U-turns."
- Confidence: high.
- **Triage: fixed as proposed.** Added **PASS-LOC-06**, "No passing in the center left turn lane": INSTRUCTION / MUST NOT, actor DRIVER, "WHEN on a road with a center left turn lane, the DRIVER MUST NOT use the center left turn lane to PASS." It has no vague terms, the proposed note, and evidence `10.55`, `10.56`. It is placed after LOC-05, so no rules were renumbered.

---

## Minor

### Citations

**C1. Cited id does not exist (PASS-USER-07).** `13.111-c` is cited, but figure 13.111 has no caption. Its "Right" label is the paragraph `13.112`, which is already cited. Stage 1 fails on this.
- Fix: remove `13.111-c`.
- **Triage: fixed as proposed.** USER-07's evidence is now `13.110`, `13.111`, `13.112`, `13.113`, `13.114`.

**C2. List items cited without the line that introduces the list.** MTO precedent: a0 C1, which was applied to every rule.

| Rule | Item | Add |
|---|---|---|
| GEN-02 | 10.186 | `10.184` "You must judge whether you have enough space to pass whenever you approach:" |
| SIDE-02 | 10.202 | `10.200` "You may pass on the right only when:" |
| LOC-04 | 12.131 | `12.130` "Other things to keep in mind:" |
| LOC-05 | 12.108 | `12.103` "How to use a roundabout:" |
| USER-02, USER-03 | 13.14 | `13.12` "…When driving near large vehicles and trucks, do not:" |
| USER-06, BEING-06 | 13.39, 13.41 | `13.35` "…To safely share the road with motorcyclists:" |
| USER-10 | 13.121 | `13.115` "…Remember to:" |

USER-03 depends on 13.12 more than the others: its ban ("do not … drive next to them longer than you need to") comes from that lead-in, so without it the cited text does not state the rule.
- **Triage: fixed as proposed.** Each lead-in in the table was added to its rules, before the item, in handbook order.

**C3. A block cited only for the note (PASS-BEING-06).** `13.38` (lane splitting is legal) supports only the note, not "move to one side of your lane". Per the allow list, something mentioned only in a note needs no citation.
- Fix: evidence `["13.35", "13.41"]`. Keep the note. See also O2.
- **Triage: fixed as proposed.** BEING-06's evidence is now `13.35`, `13.41`, and the note is unchanged.

**C4. PASS is cited to the how-to-pass steps, which do not define it.** The PASS vocabulary entry cites `10.194`–`10.199`, a procedure that does not say what a pass is. MTO precedent: a0 V4 and S2-031, where a self-made definition gets empty evidence. See V3 for the wording.
- **Triage: fixed as proposed.** PASS now has empty evidence. Its definition is unchanged until V3 is decided.

**C5. The general lane-change checks are not cited on PROC-01 (optional).** `10.36`–`10.42` (signal, check mirrors, check traffic behind and beside, look over your shoulder, enough space in the next lane) apply to every lane change, and so to the move into and out of the lane used for passing. MTO precedent: b3 S3-003 added the same kind of blocks to PROC-01. This can go in the evidence and a note, without changing the action.
- **Triage: fixed, citation added.** `10.36`–`10.42` (the lead-in and its six items) were added to PROC-01's evidence. Its note now ends: "The general lane-change checks (10.36-10.42) also apply to the moves out of and back into the original lane." The action is unchanged.

### Vocabulary and terminology

**V1. HOV is in CAPS but has no vocabulary entry (PASS-MARK-02).** Stage 1 flags it.
- Fix: write the action as "high-occupancy vehicle carpool lane", or add a vocabulary entry citing `10.48`, or add acronyms to the stage-1 allowlist. The first is simplest.
- **Triage: fixed as proposed (first option).** MARK-02's first exception now reads "in a high-occupancy vehicle carpool lane with a designated entrance on the left".

**V2. The vocab term DRIVER is written in lowercase (PASS-SIDE-01, PASS-SIDE-02, PASS-BEING-04).** The phrases are "the driver ahead" and "another driver". Stage 1 flags these. MTO precedent: a1 ("another driver" → DRIVER).
- Fix: "the DRIVER ahead", "another DRIVER".
- **Triage: fixed as proposed.** SIDE-01 was already fixed with M2. SIDE-02 now has "the DRIVER ahead" and BEING-04 "another DRIVER".

**V3. PASS is used inconsistently as noun and verb, and differs from the MTO convention.** The entry defines PASS as a verb ("To move past…"), and rules write "MUST NOT PASS" and "PASS a vehicle". Yet many rules use lowercase "passing", "after passing" or "overtaking" for the same act: PROC-02 ("WHEN passing"), USER-03, USER-05 ("overtaking"), USER-08, USER-09, USER-10, USER-12, BEING-03 ("passing is unsafe") and BEING-06. In the MTO gold set, only the noun PASS is in CAPS and the verb stays lowercase ("the PASSER MAY pass"), as in the prompt's own example. The definition also ends "…and then returning to the original lane", the phrase MTO a0 V1 removed as copied from the prompt's example (task.md still contains it).
- Fix: adopt the MTO convention, so the definition becomes a noun, "Moving past a slower or stopped vehicle or road user travelling in the same direction." with empty evidence (C4), and verbs become lowercase. This is a mechanical change across most rules, so it can wait for the a1 fixes. At minimum, make "passing"/"PASS" consistent within each rule.
- **Triage: fixed as proposed, following the MTO convention.**
  - PASS is now a noun: "Moving past a slower or stopped vehicle or road user travelling in the same direction." It has empty evidence (C4), and the "then returning to the original lane" wording is gone.
  - Every verb use of PASS in `when`, `action` and `unless` was lowercased in 34 rules, and their statements were rebuilt. This includes the verbs written in CAPS by the M2, M4, M6, O1, S1, G2 and G4 fixes.
  - The noun stays in CAPS in GEN-04 ("WHEN considering a PASS, the PASSER MUST NOT pass, …"), in MARK-04's note ("a PASS is a lane change") and in PASSER's definition ("The driver making a PASS").
  - Lowercase "passing", "overtaking" and "let the oncoming vehicle pass" were already lowercase and are unchanged.
  - The format check passes with `--allow-lowercase pass`, as in the MTO scope.

**V4. Definitions cite blocks that do not define the term, and add legal status.** BICYCLIST ("…who has the same rights and responsibilities as other drivers", `13.71`) and MOTORCYCLIST (`13.35`) cite statements about rights, not definitions. MTO precedent: a0 V4 (CYCLIST cited licensing facts) and "define the thing itself".
- Fix: "A person riding a bicycle." and "A person riding a motorcycle.", both with empty evidence.
- **Triage: fixed as proposed.**

**V5. Other definitions that go beyond the thing itself.**
- LARGE VEHICLE: "A truck or other large vehicle that has large blind spots, takes longer to stop, and swings wide when turning" lists properties, and the handbook never gives a size. The prompt says not to make up definitions for terms the handbook leaves vague. Fix: "A truck, bus or other vehicle much larger than a passenger vehicle; the handbook gives no size threshold."
- SAFETY ZONE: the definition says it is "marked by raised buttons or markers on the road" (`13.18`), but it also cites `13.21`: "Safe Zones are marked by dotted white lines." The two blocks disagree. Fix: "A space set aside for pedestrians waiting for buses, streetcars, and trolleys.", citing `13.18`, with the marking difference noted in USER-04.
- LIGHT RAIL VEHICLE: the definition includes streetcars, but USER-05 says "LIGHT RAIL VEHICLE or streetcar", which repeats it. Fix: drop "or streetcar" from USER-05, or drop streetcar from the definition.
- TURNOUT: "into which slower vehicles merge to let vehicles behind them pass" describes how it is used, not what it is. Low priority.
- **Triage: fixed as proposed.**
  - LARGE VEHICLE: "A truck, bus or other vehicle much larger than a passenger vehicle; the handbook gives no size threshold." Evidence stays empty.
  - SAFETY ZONE: "A space set aside for pedestrians waiting for buses, streetcars, and trolleys.", evidence `13.18`. USER-04's note now records the marking difference between 13.18 and 13.21.
  - LIGHT RAIL VEHICLE: the first option was used. USER-05's condition is now "overtaking a LIGHT RAIL VEHICLE, whether it is moving or standing", and the definition is unchanged.
  - TURNOUT: "A special area or lane on some two-lane roads.", evidence `10.65` unchanged.

### Strength (force and modal)

**S1. A speed restriction written as a plain MAY (PASS-USER-04).** "the DRIVER MAY PASS it at no more than 10 mph". As a MAY rule, nothing forbids passing faster; the note has to say that the speed is part of the permission.
- `13.19`: "When a bus, streetcar, or trolley is stopped at a safety zone or traffic light, you may pass at no more than 10 mph."
- Fix: `MAY ONLY`, with the speed in the action, as in the MTO LOC-07 pattern (allowed: "MAY ONLY attached to the action, explained in the note").
- Confidence: medium.
- **Triage: fixed as proposed, together with O3.** USER-04 is now PERMISSION / MAY ONLY: "WHEN a bus, streetcar, or trolley is stopped at a SAFETY ZONE or traffic light, the DRIVER MAY ONLY PASS it at no more than 10 mph and without driving through any SAFETY ZONE." Evidence `13.18`, `13.19`, `13.20`, `13.21`. The note explains the MAY ONLY reading (it does not require passing). It also quotes 13.18's ban, which applies beyond passing, and the marking difference from V5.

**S2. A plain command "use" recorded as ADVICE (PASS-GEN-05).** `10.33` is "Use the left lane to pass or turn left." The table maps "use" to INSTRUCTION, but the lead-in `10.32` calls these "tips for choosing a lane", and the note records that. Either reading is defensible.
- Confidence: low. Left to triage.
- **Triage: fixed, as INSTRUCTION.** The finding gave no single fix, so the table's reading was applied. GEN-05 is now INSTRUCTION / MUST: "…the PASSER MUST use the left lane (the PASSING LANE) to PASS." The note says it is worded as a plain command though given as a tip (10.32), and links SIDE-01 (N1).

**S3. Two duties under one ADVICE modal, with an "until" that reaches both (PASS-USER-17).** "SHOULD NOT drive past the patrol vehicle, or speed up until the officer turns off the emergency lights…". In the handbook these are two sentences, and only the second has the "until":
- `15.154`: "Not drive past the patrol vehicle. Do not speed up until the officer turns off their emergency lights and traffic conditions allow you to return to your normal speed."

Speeding up is not overtaking.
- Fix: keep only "SHOULD NOT drive past the patrol vehicle" in this rule, and move the speed-up sentence into the note (it is outside the topic).
- **Triage: fixed as proposed.** USER-17 is now "WHEN a law enforcement TRAFFIC BREAK is in progress ahead, the DRIVER SHOULD NOT drive past the patrol vehicle." Its vague term "traffic conditions allow" was removed, since that phrase is no longer in the statement. The note quotes the speed-up sentence as outside the topic.

### Grammar and wording

**G1. "WHEN before starting to PASS" (PASS-GEN-03)** does not read as a condition. Fix: "WHEN about to PASS".
- **Triage: fixed as proposed.**

**G2. The condition contradicts the action (PASS-USER-08).** "WHEN passing a BICYCLIST AND the PASSER cannot change lanes, the PASSER MUST … not PASS until three feet of clearance can be given". If the driver is already passing, "do not pass until" cannot apply. MTO precedent: a0 G2 (a condition that repeats the action).
- Fix: "WHEN about to pass a BICYCLIST AND the PASSER cannot change lanes, …".
- **Triage: fixed as proposed**, as "about to PASS a BICYCLIST" (capitalized verb, see the note at the top).

**G3. "SHOULD PASS only when…" reads as advice to pass (PASS-GEN-02).** Fix: "the PASSER SHOULD NOT PASS, UNLESS the hill or curve is at least one-third of a mile ahead."
- **Triage: fixed as proposed.** GEN-02 is now ADVICE / SHOULD NOT, with the exception in `unless`.

**G4. Unclear referent (PASS-USER-05).** "UNLESS the tracks are so close to the right side that the vehicle cannot PASS on the right". Here "the vehicle" could be the light rail vehicle. `13.23` says "the passenger vehicle". MTO precedent: S2-061.
- Fix: "the PASSER's vehicle cannot pass on the right".
- **Triage: fixed as proposed**, as "the PASSER's vehicle cannot PASS on the right".

### Conditions

**K1. Turnout rule broader than its context, and it overlaps BEING-03 (PASS-BEING-02).** "WHEN driving on a two-lane road with a TURNOUT AND cars are behind the DRIVER, the DRIVER MUST merge into the TURNOUT". As written, any car behind triggers the duty, even for a driver at the limit. The sign on the same figure, `10.66`, reads "SLOWER TRAFFIC USE TURNOUTS". BEING-03 then adds a narrower duty that BEING-02 already covers.
- `10.65`: "Some two-lane roads have special turnout areas or lanes. Merge into these areas or lanes to allow cars behind you to pass."
- `10.67`: "You must use a turnout area or lane … when you are driving slowly …, where passing is unsafe, and there are five or more vehicles following you."
- Fix: add "AND the DRIVER is slower than the cars behind" (citing the sign), and add notes linking BEING-02 and BEING-03 (BEING-03 is the legal requirement, BEING-02 the general instruction). MTO precedent: S2-009 (a condition broader than the handbook's context).
- Confidence: medium.
- **Triage: fixed as proposed.** BEING-02's condition now ends "AND the DRIVER is slower than the cars behind". "slower than the cars behind" was added as a vague term (no speed difference given). BEING-02's note cites the sign for the condition and links BEING-03, and BEING-03's note links back.

**K2. An inferred condition with no note (PASS-USER-13).** "WHEN behind a BICYCLIST in a travel lane **who is not able to be passed**". 13.108 does not say the cyclist cannot be passed; it follows the list of reasons a cyclist may leave the right edge. Fix: either reword to "behind a BICYCLIST riding away from the right edge for one of the reasons in 13.102–13.107", or say in the note that the condition is inferred.
- **Triage: fixed with the note option.** A condition naming block ids would not read as a rule. The condition is unchanged. The note now says "not able to be passed" is inferred from 13.108's place after the list (13.101-13.107) and from its next sentence. The phrase is also listed as a vague term (Q1).

### Vague terms

**Q1. Vague phrases in statements that are not listed.** MTO precedent: this is the most common error type (`error_set.md`).

| Rule | Unlisted phrase | Why vague |
|---|---|---|
| LOC-01 | "approaching a hill or curve" | no distance (MTO S2-029) |
| USER-05 | "so close to the right side" | no distance |
| USER-11 | "slow down" (its `vague_terms` is empty) | no speed |
| USER-13 | "not able to be passed" | no criteria (see K2) |
| USER-15 | "slow down" | no speed (MTO S2-078) |
| BEING-04 | "move to the right", "wishes to drive faster" | how far; how the DRIVER knows (MTO S2-087) |

- **Triage: fixed as proposed.** Each phrase was added to its rule's `vague_terms`, in statement order, with the explanation in the table (BEING-04: "does not say how the DRIVER can tell", "does not say how far or into which lane").

### Notes and links between rules

**N1. Rules that restrict SIDE-01 have no link to it.** SIDE-01 allows passing on the right only in three cases. Three other rules interact with it:
- USER-02 ("Always pass a large vehicle on the left side") overrides SIDE-01 on a multilane highway.
- USER-05 (a streetcar must not be passed on the left) in effect requires passing a streetcar on the right on ordinary two-way city streets, which are not one of SIDE-01's three cases.
- GEN-05 (use the left lane to pass) sits beside SIDE-01's multilane permission.

MTO precedent: S3-008 and b3 S3-004. Fix: add a one-line note to each pair saying how they relate. The rules themselves are faithful.
- **Triage: fixed as proposed.** SIDE-01 has a new note naming USER-02, USER-05 and GEN-05. USER-02's note adds that it restricts SIDE-01. USER-05's note says it can call for passing on the right where SIDE-01's list is silent. GEN-05's note (rewritten in S2) points to SIDE-01.

**N2. USER-12 can be read as allowing less than three feet (PASS-USER-12).** "use as much of the left lane as the PASSER safely can" with steady oncoming traffic does not say what to do if that still gives less than three feet. 13.115 says "do not pass the cyclist until three feet of clearance can be given" (USER-08). Fix: add a note pointing to USER-08.
- **Triage: fixed as proposed.** USER-12's note: "Does not relax USER-08: if three feet cannot be given, do not pass the BICYCLIST (13.115)."

**N3. The note misstates the handbook's strength (PASS-BEING-04).** The note says "drivers choosing to drive slower than other traffic **should** use the right lane", but `13.144` says "If you choose to drive slower than other traffic, **drive** in the right lane." Fix: quote the handbook's wording. (That sentence is general lane-use advice and stays out of scope, per the MTO allow list.)
- **Triage: fixed as proposed.** BEING-04's note: "Same block: 'If you choose to drive slower than other traffic, drive in the right lane.'"

### Coverage: possible omissions

**O1. Lane changes over double solid white lines (10.19).** "Never change lanes over double solid white lines. Wait until you see a single broken white line." A pass is a lane change, and MTO b0 m6 added a lane-change restriction on these grounds (LOC-08). Suggest a MARK rule: "WHEN there are double solid white lines next to the DRIVER's lane, the DRIVER MUST NOT cross them to PASS", citing `10.18` and `10.19` (and possibly `10.54` for HOV lanes). Confidence: medium.
- **Triage: fixed, rule added as proposed.** Added **PASS-MARK-04**, "Double solid white lines: no lane change to pass": INSTRUCTION / MUST NOT, actor DRIVER, "WHEN there are double solid white lines next to the DRIVER's lane, the DRIVER MUST NOT cross them to PASS." It has no vague terms and evidence `10.18`, `10.19`; `10.54` was left out. The note says the rule is inferred because a PASS is a lane change. It is placed after MARK-03, so no rules were renumbered.

**O2. Lane splitting (13.38).** "It is legal to share lanes with motorcycles, this is known as lane splitting." This is the handbook's only statement that a motorcyclist may pass between lanes, which matters both for MOTORCYCLIST passing and for drivers being passed (BEING-06). Suggest a PERMISSION rule, actor MOTORCYCLIST, or at least a BEING-group link. Confidence: medium.
- **Triage: ignored.** No rule added. BEING-06's note still mentions lane splitting.

**O3. Do not drive through a safety zone when passing a stopped bus (13.18).** "Do not drive through a safety zone under any condition." USER-04 mentions this only in its note, yet it is the main constraint on how to pass a stopped bus or streetcar. Suggest a USER rule (INSTRUCTION / MUST NOT), evidence `13.18`, or folding it into USER-04's action. Confidence: medium.
- **Triage: fixed by folding into USER-04, not as a separate rule.** USER-04's action is now "PASS it at no more than 10 mph and without driving through any SAFETY ZONE", and `13.18` is cited (see S1).

**O4. Double double yellow lines as a barrier (10.13).** "Do not drive on or over this barrier, make a left turn, or make a U-turn across it, except at designated openings." This is stronger than 10.8, and MARK-02 does not cover it. Confidence: low-medium.
- **Triage: ignored.**

---

## Considered and not raised

- `13.44`–`13.45`: pull to the right edge and stop until an emergency vehicle with siren has passed. This is a "being passed" situation, but the MTO gold set does not include the equivalent rule, so it is left as a scope question for triage.
- `13.152`–`13.159`: stopping for school buses. This is the stopping topic (MTO allow list).
- `12.144`: two vehicles on a steep narrow road where "neither vehicle can pass". Here "pass" means getting by an oncoming vehicle, not overtaking.
- `13.146`–`13.149`: towing vehicles and trucks with three or more axles must use the right lane. This is general lane use and not stated in terms of passing (compare the MTO allow list, "General lane-use advice").
- `13.13`, `13.36`, `13.120`, `15.12`: lane-change and merging cautions that are not about a pass.
- PASSER as the actor of rules about deciding whether to pass (GEN-01, GEN-04). This follows the MTO gold set.
- Group choice and order, such as COND for fog and GEN-04 under GEN rather than LOC. Per the allow list, these are not errors.

## Observations for the pipeline

- Stage 1 (`check_format.py`) did not catch M2 (mixed AND/OR in one condition) or M3/M4 (a lowercase "must" or "MUST not" inside `action`). Both are mechanical and could become format checks.
- The prompt's example PASS definition in task.md still ends ", then returning to the original lane", the wording MTO a0 V1 removed. The CA draft picked it up again (V3). Consider updating the example, which changes the prompt hash.
