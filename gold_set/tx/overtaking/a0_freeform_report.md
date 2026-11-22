# Freeform error check: `gold_set/tx/overtaking/00_raw_rules.json`

Source: `corpus/tx` · Prompt: `prompts/formal-rules` (system.md, task.md, schema.json) · Topic: overtaking

Quotations from the handbook are given as `id`: "text", and some are trimmed with "…". Image links point to `handbooks/tx/images/`.

**What was checked**

- Every cited block id was resolved against the corpus HTML. They all exist, so there are no dangling citations.
- The structure was checked by script:
  - With the format script (`check_format.py --handbook tx`), checks 1–7 pass: schema, statement matches fields, ids and numbering, force and modal, evidence, vague terms, vocabulary.
  - Check 8 found 12 lowercase vocabulary terms ("driver" ten times, "highway", "truck"). They are left to the format check a1 and not repeated below.
  - A separate script looked for conditions that mix AND and OR, brackets, and modals inside an action.
- Each rule was read against the text of its cited blocks, with the blocks around them.
- The cited diagrams and signs were viewed to confirm what the rules and notes say about them:
  - Diagrams: [7.40](../../../handbooks/tx/images/p045-01.png), [7.54](../../../handbooks/tx/images/p045-02.png), [6.188](../../../handbooks/tx/images/p039-02.png), [6.194](../../../handbooks/tx/images/p039-04.png), [6.198](../../../handbooks/tx/images/p039-05.png), [6.201](../../../handbooks/tx/images/p040-01.png), [5.73](../../../handbooks/tx/images/p029-01.png).
  - Signs: [7.18](../../../handbooks/tx/images/p044-02.png), [6.50-f1](../../../handbooks/tx/images/p032-13.png), [6.120-f1](../../../handbooks/tx/images/p036-03.png), [6.129-f1](../../../handbooks/tx/images/p036-11.png), [6.148-f1](../../../handbooks/tx/images/p037-13.png), [6.149-f1](../../../handbooks/tx/images/p037-14.png), and the uncited [6.98-f1](../../../handbooks/tx/images/p035-01.png).
- The whole corpus was searched for "pass" and "overtak" to find rules that were left out. It was also searched for passing situations described in other words: move over, stopped vehicles, obstructions, barricades, cyclists, blind spots, racing.
- This scope has no triage records of its own yet (`allow_list.md`, `error_set.md`); they are written at the end of round a.

**Result:** 52 rules and 14 vocabulary terms. The JSON fits the schema, and every statement matches its fields word for word. Ids, numbering and force/modal pairs are all valid. The errors found are listed below, grouped by severity.

**Triage:** every finding has been triaged, and its decision is recorded as a Triage line under it. Fixes were applied to `a0_freeform.json`, which started as an exact copy of `00_raw_rules.json`.
- Rules added, each at the end of its group, so no rule was renumbered:
  - PASS-SIGN-03 (two-arrow sign, M6.3) and PASS-SIGN-04 (barricade stripes, M6.4);
  - PASS-USER-15 and PASS-USER-16 (slow down or move over for a stopped service vehicle, M6.1);
  - PASS-BEING-10 (truck signals before returning after a pass, M6.2).
- Vocabulary added: FREEWAY (M5) and SERVICE VEHICLE (M6.1).
- Every statement a fix touched was rebuilt from its fields. Finding text uses the draft's rule ids, which did not change.
- After all fixes there are 57 rules and 16 vocabulary terms.
- Format check on `a0_freeform.json`: checks 1–7 pass. Check 8 reports 10 lowercase vocabulary terms, all from the draft (two of its 12 went away with the GEN-06 and USER-12 rewrites); they are left to a1.

Severity: **Major** means the rule says something the handbook does not, misstates its strength, or breaks the grammar or vocabulary contract. **Minor** covers citation, wording, vague-term or ordering issues.

---

## Major

### M1. A MUST NOT action carries a second modal, "and must …" (PASS-GEN-06, PASS-USER-09, PASS-USER-13)
The grammar allows one MODAL per rule. In these three rules, a lowercase "must" inside a MUST NOT action adds a duty. As written, "MUST NOT (drive or linger …, and must either complete the PASS …)" can be read as forbidding the very way out that the handbook orders.
- GEN-06: "the PASSER MUST NOT drive or linger in the other driver's BLIND SPOT, and must either complete the PASS or slow down out of the BLIND SPOT."
  - `7.53`: "When you are passing, do not drive or linger in the other driver's blind spot. Either pass the other driver or slow down so you are not in another driver's blind spot."
- USER-09: "the DRIVER MUST NOT cut into the open space in front of the TRUCK or bus, and must instead slow down and exit or stay behind it."
  - `10.129`: "Never cut in front of a truck. … Trying to beat a truck to a single-lane construction zone represents a particularly dangerous situation. Either slow down and exit or stay behind the truck."
- USER-13: "the DRIVER MUST NOT attempt to share the lane with the MOTORCYCLE, and must allow the motorcyclist a full lane width."
  - `10.160`: "Allow the motorcyclist a full lane width. … Do not attempt to share the lane with a motorcycle."
- Fix: use MUST, with the positive phrase first and the negated phrase last, so that the lowercase "not" covers only the last phrase.
  - GEN-06: "…the PASSER MUST either complete the PASS or slow down out of the other DRIVER's BLIND SPOT, and not drive or linger in it."
  - USER-09: "…the DRIVER MUST stay behind the TRUCK or bus or slow down and exit, and not cut into the open space in front of it."
  - USER-13: "…the DRIVER MUST allow the MOTORCYCLE a full lane width, and not attempt to share the lane with it."
  - USER-09's condition ("including when trying to reach an exit or turn or a single-lane construction zone") is also not a fact; see G5.
- Triage: fixed as proposed (positive phrase first, negated phrase last). USER-09 reworded with the exit/construction-zone situation as its condition (also settles G5 for USER-09).

### M2. A keep-right instruction is turned into a permission whose exception points elsewhere (PASS-GEN-07)
The handbook states a duty with exceptions: keep right, except when passing on a two- or three-lane street, on a one-way street, or when the right side is blocked. The rule turns one exception into a PERMISSION ("MAY leave the right side of the road"), so the duty itself is not in the set.
- `7.24`: "Always keep to the right side of the road except when:"
- `7.25`: "Passing another vehicle on a two- or three-lane street"
- `7.26`: "Driving on a one-way street"
- `7.27`: "The right side of the road is blocked"

The exception, "UNLESS a condition under which driving on the left side of the road is prohibited applies", is not a fact the model can recognize. It refers to other rules (the note names LOC and MARK), which task.md rules out ("Make each rule stand on its own").
- Fix: restate it as the keep-right duty. For example, "WHEN driving on a road, the DRIVER MUST keep to the right side of the road, UNLESS passing another vehicle on a two- or three-lane street OR driving on a one-way street OR the right side of the road is blocked." The force is INSTRUCTION ("Always keep"), citing `7.24`–`7.27`. The note can say that LOC-01 to LOC-04, MARK-02 and SIGN-01 limit when the left side may be used.
- Triage: fixed as proposed.

### M3. Advice strength given to a plain command (PASS-GEN-01)
`7.29`: "It is not always safe to pass. **Be patient and wait** until the time is right." This is a plain command, which the table maps to INSTRUCTION / MUST. The rule records ADVICE / SHOULD, against "Do not turn … an obligation into advice".
- Fix: force `INSTRUCTION`, modal `MUST`.
- Triage: fixed as proposed.

### M4. A stronger wording elsewhere is not recorded: disobeying a warning sign is a violation with a fine (PASS-SIGN-02, PASS-SIGN-01)
SIGN-02 rests on six warning signs (Table 18) whose descriptions end "do not pass". It records them as INSTRUCTION with no penalty. The handbook says elsewhere that disobeying a warning sign is an offence, and gives the fine:
- `6.56` (Warning Signs): "Not only must warning signs be observed for safety reasons but to disregard them may be a traffic violation."
- `6.266` (Obey Warning Signs and Barricades): "It is a violation to disobey the instructions, signals, warnings, or markings of a warning sign, or to drive around a barricade."
- `6.267`: "The offense is a misdemeanor punishable by a fine of $1 to $200. Fines double in a construction or maintenance work zone when workers are present anywhere in the construction zone."

task.md says to record the stronger wording and say so in the note, and to give a penalty when the handbook states one for the rule. Here the handbook ties the fine to disobeying a warning sign itself, so the penalty is not inferred from a general offence table.
- Fix:
  - SIGN-02: force REQUIREMENT (modal stays MUST NOT); penalty "A fine of $1 to $200, doubled in a work zone with workers present."; add `6.56`, `6.266`, `6.267` to the evidence; the note gives the source.
  - SIGN-01 is already a REQUIREMENT, from 6.120's "you may not pass". Its "No Passing Zone" pennant is a warning sign (`6.50`: "Pennant: Advance warning of no pass zones"; yellow in [6.120-f1](../../../handbooks/tx/images/p036-03.png)), so the same penalty may apply to the pennant. *(Lower confidence: SIGN-01 also covers the regulatory "Do Not Pass" sign, for which no penalty is given.)*
- Triage: fixed as proposed.
  - SIGN-02 is REQUIREMENT / MUST NOT, with the 6.267 fine as its penalty. It cites `6.56`, `6.266` and `6.267`, and its note gives the source.
  - SIGN-01's penalty stays empty, because its "Do Not Pass" sign has no stated penalty. Its note now says the pennant is a warning sign carrying the 6.267 fine.

### M5. Freeway lane rules are applied to every multi-lane road, which conflicts with passing on the right (PASS-GEN-09, PASS-BEING-09)
GEN-09 ("WHEN passing other vehicles on a multi-lane HIGHWAY, the PASSER MUST use the middle or left lane") and BEING-09 rest on 10.23 and 10.34. Both blocks are in the freeway section: heading `10.12` "Highway Driving", `10.13` "Freeways, toll-roads, throughways, turnpikes, and expressways…", then the headings "Before Using a Highway", "Entering the Highway" and "Driving on the Highway". The vocabulary, however, defines HIGHWAY by its legal meaning:
- `16.78`: "highway – the width between the boundary lines of a publicly maintained way any part of which is open to the public for vehicular travel"

With that meaning, the rules cover every public road with more than one lane each way. GEN-09 then contradicts SIDE-01, which the handbook also states for such roads:
- `7.42`/`7.43`: "you can pass on the right only when conditions permit you to do so safely. The road is clear of parked vehicles or other lane obstructions and is wide enough for two or more lanes in each direction."

The condition is broader than the handbook's context, and the two rules conflict without a note saying how they relate.
- Fix: limit both conditions to the freeway setting, e.g. "on a multi-lane freeway or expressway". Either use CONTROLLED-ACCESS HIGHWAY (16.35), or add a FREEWAY term defined from 10.13. Add notes linking GEN-09 and SIDE-01.
- Triage: fixed as proposed. Added FREEWAY term, defined from 10.13, and changed GEN-09 and BEING-09 to refer to it. Added notes linking GEN-09 and SIDE-01.

### M6. Rules left out
None of these are in the file:
1. **Slow down or move over for stopped emergency, tow, utility and TxDOT vehicles.** This is a REQUIREMENT about driving past a stopped vehicle. The draft includes the mail-truck rule in the next block (USER-03, `9.32`), but not these.
   - `9.29`: "If an emergency medical vehicle, law enforcement vehicle, fire truck, tow truck, utility service vehicle, Texas Department of Transportation vehicle (TxDOT, or other highway construction or maintenance vehicle) is stopped on the road with its lights activated (the lights are on or flashing), then the driver is required:"
   - `9.30`: "To reduce his/her speed to 20 mph below the speed limit; or"
   - `9.31`: "Move out of the lane closest to the emergency medical vehicle, law enforcement vehicle, fire truck, tow truck or a TxDOT vehicle if the road has multiple lanes traveling in the same direction."
   - `5.68`–`5.71`: "Unless otherwise directed by a law enforcement officer, drivers who approach a stopped emergency vehicle with its lights activated must: Vacate the lane closest to the emergency vehicle if the highway has two or more lanes traveling in the direction of the emergency vehicle; Slow to a speed not more than 20 mph less than the posted speed limit when the posted speed limit is 25 mph or more; or Slow to a speed less than 5 mph when the posted speed limit is less than 25 mph."
   - Suggested: two REQUIREMENT rules in USER, citing `9.28`–`9.31` and `5.68`–`5.71`.
     - Vacate the nearest lane when there are two or more lanes in that direction.
     - Otherwise, slow to 20 mph below the limit (or to under 5 mph where the limit is under 25 mph), UNLESS directed otherwise by a law enforcement officer.
   - The two passages differ: 9.29 lists more vehicle types, and 5.71 adds the under-25-mph case. The note should say how they were combined.
   - Triage: fixed as proposed, split by the number of lanes:
     - **PASS-USER-15**, two or more lanes in the DRIVER's direction: move out of the lane closest to the vehicle, or slow down. This keeps the handbook's "or", since 9.30/9.31 and 5.69/5.70 give the DRIVER the choice.
     - **PASS-USER-16**, one lane: slow down.
     - Both rules: slow to 20 mph below the limit, or to under 5 mph where the posted limit is under 25 mph, UNLESS a law enforcement officer directs otherwise.
     - The vehicles are named by a new SERVICE VEHICLE term, taken from 9.29's list, with empty evidence. The notes say how the two passages were combined.
2. **A truck driver who has passed should signal before returning to the lane.** This is ADVICE, actor DRIVER of a TRUCK. It appears only in BEING-07's note. That is a rule hidden outside the rule list.
   - `10.115`: "…After passing, the truck driver should signal to let you know he is returning to your lane."
   - Suggested: "WHEN the DRIVER of a TRUCK has passed another vehicle AND is returning to that vehicle's lane, the DRIVER of the TRUCK SHOULD signal." Cite `10.115`, and remove 10.115 from BEING-07 (see C2).
   - Triage: fixed as proposed. Added as **PASS-BEING-10**, with BEING-07's note pointing to it.
3. **A sign permits passing on either side of an island or obstruction.** This is a PERMISSION. Passing a hazard other than a vehicle is in scope.
   - `6.98` ([sign](../../../handbooks/tx/images/p035-01.png), a yellow diamond with two arrows pointing down and outward): "Indicates traffic is permitted to pass on either side of a traffic island or an obstruction."
   - Suggested: "WHEN a sign shows two arrows pointing down to the left and right at a traffic island or obstruction, the DRIVER MAY pass on either side of it." Cite `6.98`, `6.98-f1`.
   - Triage: fixed as proposed. Added as **PASS-SIGN-03**.
4. **Barricade stripes show the side on which to pass.** This is ADVICE ("should bear"). It concerns passing an obstruction, as in item 3. The handbook's heading names it "Passing Traffic".
   - `6.243`: "The diagonal stripes on the barricade or vertical panel guide the driver towards the direction to where the traffic is to pass."
   - `6.245`: "Stripes sloping downward to the right means the driver should bear to the right." `6.248`: "…to the left means the driver should bear to the left."
   - Suggested: one ADVICE rule per direction, or one rule naming both, citing `6.242`–`6.249` with the figures `6.246`, `6.249`. *(6.266 also makes it a violation "to drive around a barricade". That is a separate REQUIREMENT, and is in scope only if driving around a barricade counts as passing it.)*
   - Triage: fixed as proposed, as one rule naming both directions.
     - Added as **PASS-SIGN-04**: "WHEN a barricade or vertical panel has diagonal stripes sloping downward to one side, the DRIVER SHOULD bear to the side to which the stripes slope downward."
     - It cites `6.243`, `6.245`, `6.246`, `6.248`, `6.249`. The headings 6.242, 6.244 and 6.247 are not cited, as under C1.
     - 6.266's ban on driving around a barricade was not added.
5. *(Borderline)* **Cyclists may take the full lane when the lane is too narrow to share.** The text does not mention passing, so this may be out of scope.
   - `10.184`: "The lane is of substandard width, making it unsafe for a car and a bicycle to safely share the lane side-by-side. When this is the case, it is best for the cyclist to take the full lane…"
   - `14.33` (purposes of the shared lane marking): "Encourage safe passing of bicyclists by motorists". This states the purpose of a marking, not a rule.
   - Triage: rejected (out of scope). 10.184 is about a cyclist's lane position when a car and a bicycle cannot share the lane side by side; it does not mention passing, and it does not sit in a passing section. 14.33 states the purpose of a marking, not a rule. The rule belongs to the all-rules scope.

6. *(Borderline)* **No driving left of the left-edge yellow line.** The text bans driving there but does not mention passing.
   - `6.209`: "The solid yellow line on the left edge of the road is a guide for drivers to indicate driving to the left of the yellow line is prohibited. This type of yellow line can be found on interstate highways."
   - Triage: rejected (out of scope). 6.209 bans driving left of the left-edge yellow line in general; it does not mention passing and sits under Pavement Markings, not a passing section. The rule belongs to the all-rules scope.

---

## Minor

### Vocabulary
- **V1. PASS has a definition the handbook doesn't give.** The entry adds "and then returning in front of it", which the glossary does not have. It conflicts with passing on the right on multi-lane roads (SIDE-01) and on a paved shoulder (SIDE-02), where the passer need not return in front.
  - `16.106`: "overtake – to pass the vehicle ahead"
  - PASS is also defined as a verb ("To overtake: …") and written in CAPITALS as a verb ("MUST NOT PASS other vehicles", "MAY ONLY PASS on the right") as well as a noun ("complete the PASS"), while "passing" stays lowercase. The extraction prompt's example capitalizes only the noun PASS, the manoeuvre ("complete the PASS"), and keeps the verb lowercase ("the PASSER MAY pass").
  - Fix: "Moving past the vehicle ahead; overtaking." with evidence `["16.106"]` only. The process steps 7.35/7.38/7.39 do not define the term. Lowercase the verb uses ("pass", "to pass"), and keep PASS for the noun.
  - Triage: fixed as proposed. PASS is now "Moving past the vehicle ahead; overtaking.", with evidence 16.106. The verb is lowercased in the 21 statements that used PASS as a verb; the noun PASS stays capitalized, as in the extraction prompt's example.
- **V2. Line definitions build in their meaning or position.** A definition should define the thing itself.
  - BROKEN LINE: "…which permits passing or changing lanes if safe". This is MARK-01's rule.
  - SOLID YELLOW LINE: "…on the driver's side of the road it marks a NO-PASSING ZONE". This is MARK-02's rule.
  - DOUBLE YELLOW LINE: "…separating opposing traffic on a multi-lane highway". This builds in where the line is used.
  - Fix: "A broken or dashed line painted on the pavement." / "A continuous yellow line painted on the pavement." / "Two parallel solid yellow lines painted on the pavement." Each has empty evidence, since 6.187, 6.197 and 6.200 say what the lines mean, not what they are. The meanings stay in the MARK rules.
  - Triage: fixed, with slightly different wording. BROKEN LINE "A broken or dashed painted line on the road.", SOLID YELLOW LINE "A continuous yellow painted line on the road.", DOUBLE YELLOW LINE "Two parallel continuous yellow painted lines on the road.", each with empty evidence: they are self-made definitions, and the cited blocks say what the lines mean, not what they are. The meanings stay in MARK-01 to MARK-03.
- **V3. CYCLIST includes a legal status**: "…which is a vehicle with the rights and responsibilities of a driver", from 10.176. That is a statement about bicycles, not a definition of a cyclist.
  - Fix: "A person riding a bicycle.", with evidence `["16.14"]` (the glossary's definition of bicycle). Drop 10.176.
  - Triage: fixed. CYCLIST is now "A person riding a bicycle.", a self-made definition with empty evidence; 16.14 (which defines a bicycle, not a cyclist) and 10.176 are dropped.

### Citations
- **C1. List items are cited without the line that introduces them.** task.md says to cite "a list and the line that introduces it".
  - SIDE-02 cites `7.45` without `7.42` ("In Texas, you can pass on the right only when conditions permit you to do so safely."). The lead-in also carries a condition the rule drops: the shoulder pass, like the others, is allowed only when it is safe. See G3.
  - MARK-02 and SIGN-01 cite `7.19` without `7.17` ("Never drive on the left side of the road when:"). The NO-PASSING ZONE entry cites 7.19 for its definition, which needs no lead-in.
  - Fix: add `7.42` to SIDE-02, and `7.17` to MARK-02 and SIGN-01, each just before the list item.
  - Triage: fixed, for every rule and vocabulary entry that cites a list item. Each lead-in is placed just before the first item from its list: 7.42 on SIDE-02; 7.17 on MARK-02, SIGN-01 and NO-PASSING ZONE; 2.293 on USER-01 and USER-02, whose penalty's "automatic suspension" comes from it (not named above). Lists introduced only by a heading (7.28, 7.34, 7.47, 10.111) are unchanged: task.md does not list headings as citable blocks.
- **C2. Cited blocks that do not support the rule.**
  - PROC-01 (keep enough distance to see ahead) cites the passing diagram `7.40`. The [diagram](../../../handbooks/tx/images/p045-01.png) shows the car pulling out, passing and returning; it says nothing about following distance. It is rightly cited on PROC-06.
  - BEING-07 (truck driver keeps to the far side when being passed) cites `10.115`. 10.115's truck-driver sentence is about signalling after passing (M6.2), not about being passed.
  - *(Low confidence)* LOC-05 cites the [Left Turn Lane Only diagram](../../../handbooks/tx/images/p039-04.png) `6.194` and its caption `6.194-c`. They show left turns from the centre lane, which supports the CENTER LEFT-TURN LANE term, not the ban on passing in it.
  - Triage: partly fixed. PROC-01 no longer cites 7.40. BEING-07 no longer cites 10.115, which goes to the new rule if M6.2 is accepted. LOC-05's 6.194/6.194-c rejected: the caption "Left Turn Lane Only" states the lane's exclusive use, on which the ban rests.
- **C3. Supporting blocks not cited.**
  - LOC-05's note says the REQUIREMENT rests on a regulatory sign, but the rule does not cite `6.115` ("Drivers must obey all regulatory signs in the same manner as traffic laws."). GEN-08 cites it for the same reason.
  - GEN-06 (blind spot) does not cite `10.48`, which states the same rule under Highway Safety Tips: "Stay out of another driver's blind spot. … Stay behind or go around the other vehicle. Do not follow to the side."
  - SIGN-02: `6.56`, `6.266`, `6.267` (see M4).
  - Triage: fixed. LOC-05 adds 6.115. GEN-06 adds 10.48, and its note says the rule is stated again there. SIGN-02's sources are added under M4.

### Grammar and wording
- **G1. AND/OR mixed with no grouping, or grouped with brackets the grammar does not have**.
  - MARK-02: "on a two-lane road with two-way traffic AND the center line on the DRIVER's side is a SOLID YELLOW LINE OR crossing it is not safe". The grouping is A AND (B OR C), but it can be read as (A AND B) OR C.
  - SIDE-01: "conditions permit doing so safely AND (the road is clear … OR the road is one-way)". It uses brackets.
  - Fix: write each as an AND chain, with the alternatives as one fact joined by a lowercase "or", since the grammar has no brackets. For example, SIDE-01: "WHEN conditions permit doing so safely AND the road either is clear of parked vehicles or other lane obstructions and is wide enough for two or more lanes in each direction or is one-way, …".
  - Triage: fixed. MARK-02 and SIDE-01 are now AND chains, with the alternatives joined by a lowercase "or" in one fact; SIDE-01's bracket is removed.
- **G2. PROC-07's condition repeats the action**: "WHEN returning to the right lane after passing on a two-lane road, the PASSER MUST turn on the right turn signal, return to the right lane, …".
  - Fix: "WHEN the PASSER has safely cleared the overtaken vehicle on a two-lane road, …".
  - Triage: fixed, with different wording. PROC-07's condition is now "WHEN the PASSER has overtaken the vehicle being passed on a two-lane road", using 7.38's own word "overtaken"; "safely cleared" was not used, as it is a vague term in PROC-06.
- **G3. MAY ONLY on the verb can be misread.**
  - SIDE-01, "the PASSER MAY ONLY PASS on the right", reads as "may pass only on the right, never on the left". The intended meaning is "passing on the right is allowed only in these conditions".
  - SIDE-02 uses plain MAY, although 7.42's "only when" governs its list item too.
  - Fix: name the manoeuvre in the action, and give the reading in the note. SIDE-01: "…the PASSER MAY ONLY pass on the right in these conditions". The note says that MAY ONLY means passing on the right is not allowed otherwise and does not forbid passing on the left. SIDE-02: MAY ONLY, with "conditions permit doing so safely" added (from 7.42).
  - Triage: partly fixed. SIDE-01 keeps "MAY ONLY pass on the right", and its note gives the reading. SIDE-02 is now MAY ONLY, with "conditions permit doing so safely" added to the condition and to its vague terms; the note says the "only" comes from 7.42. MAY ONLY is used because the handbook states the "only".
- **G4. "passing" used for driving past a sign.** SIGN-02's condition, "WHEN passing a warning sign for a reverse curve…", uses the topic's own verb for something that is not overtaking. In a rule set about passing, this is easy to misread.
  - Fix: "WHEN a warning sign shows a reverse curve, sharp turn, gradual curve, reverse sharp turn, sharp curve or winding road ahead, …".
  - Triage: rejected. A lowercase phrase that means driving past a fixed object, not overtaking, is not an error. SIGN-02's condition is unchanged.
- **G5. Phrases in a condition that are not facts.**
  - USER-05: "WHEN passing a TRUCK, especially at night". "especially at night" sets an emphasis, not a condition. `10.112`: "Let the truck driver know you are passing by flashing your headlights, especially at night."
  - BEING-01: "WHEN another vehicle, including a TRUCK, is passing…".
  - USER-09: "WHEN near a TRUCK or bus, including when trying to reach an exit or turn or a single-lane construction zone".
  - Fix: drop the "especially …" and "including …" phrases from the conditions. Where the emphasis matters, keep it in the note.
  - Triage: fixed as proposed.
    - USER-05: the condition is now "WHEN passing a TRUCK", and the note reads: The handbook adds "especially at night".
    - BEING-01: "including a TRUCK" was removed; the note already says the rule is stated again for trucks.
    - USER-09: settled under M1.
- **G6. USER-02's exception "OR the red lights are no longer flashing" cannot hold while its condition holds** ("WHEN a school bus is displaying alternately flashing red lights"). It is harmless, but it shows that the condition should describe the stop, not the lights.
  - Fix: "WHEN the DRIVER has stopped for a school bus displaying alternately flashing red lights, the DRIVER MUST NOT pass the school bus, UNLESS …".
  - Triage: fixed, with 5.78's two exceptions also removed.
    - USER-02's exceptions are now only the three release conditions of 5.75–5.77.
    - The two 5.78 exceptions (a bus on a different road; a loading zone on a CONTROLLED-ACCESS HIGHWAY) say when a DRIVER need not stop. They stay in USER-01, and a DRIVER who need not stop is not in USER-02's condition. The note says so.
    - The evidence is unchanged.
- **G7. Whose vehicle is passed is unclear.**
  - BEING-01, BEING-02 and BEING-04 say "another vehicle is passing the DRIVER". The DRIVER is a person; it is the DRIVER's vehicle that is passed.
  - PROC-02 dropped "you" from 7.35's "no other vehicles are passing you".
  - Fix: "…passing the DRIVER's vehicle" in BEING-01, 02 and 04; "no other vehicles are passing the PASSER" in PROC-02.
  - Triage: fixed as proposed.
- **G8. MARK-01's "at the left of the PASSER's lane" is the prompt example's wording, not the Texas handbook's.** Texas says "on your side of the road" (`6.200`), and 6.187 says simply "You may cross a broken line when passing". The meaning is close on a two-lane road. Using the handbook's wording keeps MARK-01 parallel with MARK-02 ("the center line on the DRIVER's side").
  - Triage: fixed, using 6.187's wording. MARK-01 is now "WHEN the line the PASSER would cross to pass another vehicle is a BROKEN LINE AND it is safe, the PASSER MAY cross it." This covers every broken line, as 6.200 does, not only one at the left of the lane.

### Vague terms not listed
- USER-03: "safely" ("before safely passing the vehicle"). `9.32`: "…change lanes before **safely** passing one of these vehicles".
- BEING-03: "safely" and "as far to the right as possible". `7.50`: "**Safely** move **as far to the right as you can**…".
- USER-09: "near a TRUCK or bus"; USER-13: "near a MOTORCYCLE". No distance is given for either.
- Fix: add a vague-term entry for each: "no criteria given", "no distance given", "does not say how near".
- Triage: fixed. Entries were added for:
  - USER-03: "safely";
  - BEING-03: "safely" and "as far to the right as possible";
  - USER-13: "near a MOTORCYCLE".
  
  USER-09 needs none: its "near a TRUCK or bus" left the condition under M1.

### Force borderline
- **F1. BEING-08 could be a REQUIREMENT.** 15.79 is a plain command ("Do not … speed up to keep someone from passing"), so INSTRUCTION fits that block. However, the street-racing law (`9.37`: "A person may not participate in: A race;") defines a race to include preventing a pass (`16.125`/`16.126`: "race – the use of one or more vehicles in an attempt to: Out gain or outdistance another vehicle or prevent another vehicle from passing;"). This is lower confidence: the stronger wording is reached only through the glossary's definition, and racing covers more than this situation (a stronger passage that covers a different situation is not stronger wording of the same rule).
  - Triage: rejected. The racing law covers a different, wider situation, and it reaches this one only through a glossary definition. It is not stronger wording of the same rule. BEING-08 stays INSTRUCTION.

### Notes
- **N1. USER-12's reason is written into the action**: "SHOULD be very careful, as the other driver may drift in front". A reason belongs in the note.
  - Fix: action "be very careful"; note "Reason given: the other driver may not be aware of the PASSER and may drift in front (10.212)."
  - Triage: fixed as proposed.
- **N2. USER-01's note describes the diagram wrongly.** It says "traffic in both directions stopped for a school bus with flashing lights while children cross". The [diagram](../../../handbooks/tx/images/p029-01.png) shows traffic in both directions stopped and three pedestrians beside the bus, on the sidewalk side, not crossing the road.
  - Fix: "…while pedestrians walk beside the bus."
  - Triage: fixed as proposed.

---

## Checked and found correct
- All cited ids exist. The figures cited for diagrams and signs show what the rules and notes claim:
  - [7.40](../../../handbooks/tx/images/p045-01.png): a car passes another on a two-lane road with a broken centre line, moving left and back.
  - [7.54](../../../handbooks/tx/images/p045-02.png): blind spots to the rear on both sides of a car.
  - [6.198](../../../handbooks/tx/images/p039-05.png): a four-lane road with a double solid yellow centre line.
  - [6.201](../../../handbooks/tx/images/p040-01.png): solid and broken yellow centre lines.
  - [6.120-f1](../../../handbooks/tx/images/p036-03.png): DO NOT PASS with the NO PASSING ZONE pennant.
  - [6.129-f1](../../../handbooks/tx/images/p036-11.png): DO NOT PASS.
  - [7.18](../../../handbooks/tx/images/p044-02.png) and [6.148-f1](../../../handbooks/tx/images/p037-13.png): LEFT LANE FOR PASSING ONLY.
  - [6.149-f1](../../../handbooks/tx/images/p037-14.png): CENTER LANE ONLY, with turn arrows.
- USER-01's note is right that 5.78 names "Table 17" while the penalties are in Table 15 (`5.79`); Table 17 is "Signs by Shape" (`6.45`). The school-bus penalties match `5.81`–`5.84`, and the automatic suspension for a subsequent conviction matches `2.300`.
- SIGN-01's REQUIREMENT matches 6.120's "you may not pass". GEN-08's REQUIREMENT, which rests on a regulatory sign and 6.115, is well founded, and its note gives the sign's softer "should" wording.
- LOC-01 to LOC-04 match the 7.17 list item for item, with the "Never" wording recorded as INSTRUCTION.
- The truck passing rules USER-04 to USER-08 match 10.112–10.114, and their strengths fit the wording. USER-07's MUST NOT … UNLESS form for "move back only when you can see the entire front" is a valid way to write that instruction.
- Rule order within groups (e.g. GEN-06 from 7.53 placed before GEN-07 from 7.24) is not raised: it does not change any rule's meaning.
