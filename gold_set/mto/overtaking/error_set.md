# Error set: confirmed error types

Kinds of error that were confirmed and fixed at triage while building the overtaking gold set (steps
a0–a3 and b0–b3). Examples give the step and finding id: a0 = `a0_freeform_report.md` (M = major, others
minor), a1 = `a1_format_report.txt`, S2 = `a2_atomic_report.md`, S3 = `a3_aggregate_report.md`; b0 =
`b0_freeform_report.md` (M = major, m = minor), b2 S2 = `b2_atomic_report.md`, b3 S3 =
`b3_aggregate_report.md`. Rule ids are as they were at that step (the USER group was renumbered in a0
and b0).

The companion list of reported errors that were rejected is `allow_list.md`.

## Faithfulness: the rule says something the handbook does not

- **A list's lead-in turned into a restriction.**
  - a0 M4: "If you have to pass and the way is clear, follow these steps:" became "pass only if the
    DRIVER has to". NIGHT-02 is now "WHEN passing at night, the DRIVER SHOULD be very careful."
- **An exception stretched over more than the handbook allows.**
  - a0 M7: one UNLESS covered two bans, so pulling up beside a turning cyclist seemed fine once it
    moved right. Split into USER-06 (no exception) and USER-07.
  - b0 M1: SIDE-01's "UNLESS in or near an intersection" rested on 10.11's ban on *lane changes*, but
    banned every pass on the right, including staying in one's lane and the paved-shoulder pass that
    LOC-07 allows. Reworded to "UNLESS doing so requires changing lanes in or near an intersection"
    (later removed, see b3 S3-008 under Granularity).
- **MAY ONLY reading in a prohibition the handbook does not state.**
  - b2 S2-028: 18.68-c says the lines show "the side on which you may safely pass"; it does not forbid
    the other side. SIGN-05 went from MAY ONLY to MAY, and the note says so.
- **The handbook's example list made exhaustive.**
  - S2-077, S2-081: "such as roadside assistance and disabled vehicles, surveyors…" became a closed
    list. Now "workers or vehicles on the road that pose a hazard, such as …".
- **Words added that the handbook does not use.**
  - a0 G3 ("use the far left lane only to pass": "only" removed).
  - a0 V1 (PASS's definition had ", then returning to the original lane", copied from the prompt's
    example).
- **Part of a handbook sentence left out.**
  - a0 G4: GEN-04 dropped "keep to the right of the road" from 5.13 and kept only the multi-lane
    part.
  - b2 S2-034: SIDE-04 dropped the second trigger of 29.104, "a vehicle edging into the intersection
    from the right". Added, joined by a lowercase "or", and the rule retitled.
- **Possibility wording dropped or narrowed.**
  - S2-015: "bicycles that may be hidden" became "hidden".
  - S2-005: "unless you want to turn left" became "UNLESS turning left", which reads as the turn
    itself. Now "preparing to turn left".

## Conditions and exceptions

- **A missing exception stated in the cited block or elsewhere.**
  - S2-006: GEN-05 told every freeway driver to pass in the far left lane, which trucks may not use.
    Now UNLESS driving a truck on a road with a TRUCK PASSING LANE, pointing to GEN-07.
  - S3-007: NIGHT-04's high beams while passing ignored the 150 m oncoming low-beam rule. Now UNLESS
    an oncoming vehicle is within 150 metres (4.65, 14.8).
  - S3-008: SIDE-01's permission to pass on the right had no exception. Now UNLESS in or near an
    intersection (10.11). (Reworded in b0 M1, then removed in b3 S3-008 once LOC-08 held the ban.)
- **A condition broader than the handbook's context.**
  - S2-009: GEN-06 fired on all following. It is lane-change advice, so the condition now includes
    "considering changing lanes to go around it".
  - S2-041: SIGN-04 applied to the whole road, not the stretch with the extra lane.
  - b0 m2: USER-21's move-over duty did not say the stopped vehicle is in the DRIVER's direction of
    travel (13.107, 13.109). Matched to USER-19/20.
  - b3 S3-005: USER-04's "MUST pass by changing lanes" applied to every two-wheeler, but 10.24 is about
    a rider who has pulled to one side of the lane. Narrowed to that situation.
- **A condition that stops holding before the handbook's situation ends.**
  - b2 S2-038: USER-06's "WHEN making a left turn behind …" stopped holding once the turn was done,
    though 9.18's "wait for the smaller vehicle to move right before you pass" applies after it. Now
    "WHEN the DRIVER has turned left behind … and is still behind it".
- **A condition that lets the action read as a duty to do something the handbook does not require.**
  - b2 S2-004: GEN-05's "MUST use the far left lane to pass traffic moving slower …" could be read as a
    duty to overtake. Passing moved into the condition ("AND passing traffic moving slower than the
    speed limit").
- **A condition that repeats the action.**
  - a0 G2: "WHEN returning to the original lane …, MUST NOT move back into the original lane" became
    "WHEN the PASSER has overtaken the vehicle being passed".
- **A condition whose scope is unclear.**
  - a0 G1: AND and OR mixed with no grouping (LOC-03, USER-21).
  - S2-072, S2-073: "in the DRIVER's direction of travel" placed after the second alternative, so it
    seemed to limit only the tow truck. Moved to the front.
  - S2-089: "another DRIVER is trying to pass" did not say whose vehicle. Now "…to pass the DRIVER's
    vehicle".
  - b2 S2-060: BEING-03's "another vehicle is passing or trying to pass" (same fix: "… the DRIVER's
    vehicle").
  - b2 S2-067: TOW-04's "a large bus or truck passes" did not say it passes the DRIVER (27.47 is under
    "Being passed").

## Strength (force and modal)

- **A plain command recorded as ADVICE.**
  - a0 M5: USER-04's "tap it quickly and lightly" was raised to INSTRUCTION / MUST.
- **A plain command recorded as REQUIREMENT.**
  - S2-037: SIGN-02's "Do not pass the pilot vehicle" is a temporary-condition sign caption, so it
    is now INSTRUCTION.
- **The stronger of two wordings not recorded.** The task says to record the stronger one and say so
  in the note.
  - a0 M8: PROC-06 went from "Be careful not to" (ADVICE) to the "Never" of 10.10 (INSTRUCTION).
  - a0 M9.4: SIGN-05 went from 10.36's descriptive wording to the "must" of 18.70 (REQUIREMENT).
  - S2-085: BEING-01 went to REQUIREMENT from the test's "you must".
  - b0 M2: USER-17 went to REQUIREMENT from Diagram 2-49's "the required two metres" (10.43); 10.45
    also calls it a "rule", and another rule's note already called it "the requirement".
- **A prohibition worded as "not to be used" recorded below REQUIREMENT.**
  - a0 force borderline: LOC-05 (9.36).
- **A requirement and advised wording sharing one modal.**
  - a0 M6: 13.107's required slowing and its "brake early and gradually" were split into USER-19
    (REQUIREMENT) and USER-20 (INSTRUCTION).
- **The same situation given different strengths in two rules.**
  - S3-009: SIGN-03 (MUST, signed) and SIGN-04 (SHOULD) covered the same keep-right duty. They were
    merged into SIGN-03.
  - b0 m1: USER-02 (SHOULD change lanes to pass a cyclist, 6.32) and USER-05 (MUST, 10.24) were merged
    into USER-05. In b3 S3-005 the overlap was removed differently: USER-04 (the merged rule) was
    narrowed to 10.24's situation and the 6.32 advice restored as USER-24.

## Granularity

- **Two bans or duties under one modal or exception** → split.
  - a0 M6, a0 M7.
- **A required duty pushed into the note instead of the rule.**
  - S2-069: USER-19's "you are required to assess the speed of the surrounding traffic and the
    condition of the roadway" now sits in the action.
- **Overlapping rules** → merge.
  - S3-009.
  - b3 S3-008: SIDE-01's exception ("doing so requires changing lanes in or near an intersection")
    repeated LOC-08. The exception and its 10.11 citation were removed, and the note points to LOC-08.

## Grammar and wording

- **A lowercase "not" inside a MUST action whose scope is ambiguous.**
  - a0 M3: "MUST not race it and go back" could be read as forbidding the return. Reworded to the
    positive-first, negated-last pattern.
  - S2-046: "wait … rather than suddenly changing lanes" left open whether an unhurried lane change is
    also forbidden. Now "wait … and not suddenly change lanes".
- **MAY ONLY that can be misread as an obligation.**
  - a0 G6: LOC-07 was rephrased so the action names the purpose, and the note gives the reading.
- **A referent that is unclear or missing.**
  - S2-061: "between the vehicle and the HORSE-DRAWN VEHICLE" became "the PASSER's vehicle".
  - S2-100: "the lane" became "the original lane".
  - S2-081: "the hazard" had no antecedent.
  - S2-054: "allow more room" did not say where; now "in front of the LARGE VEHICLE before returning
    to its lane".
  - S2-099: "more room" had no comparison; now "than when not towing".
  - b0 m4: USER-09's "more room" had no comparison (as in S2-099); now "than when passing a smaller
    vehicle".
  - b2 S2-040: USER-08's "its lane" could mean either vehicle's; now "the original lane".
- **A title that does not match the statement.**
  - S2-058: USER-11 is now "Farm machinery: do not pass until safe".
  - b2 S2-051: USER-22 named only workers; now "Move over a lane for roadside workers and vehicles".
  - b2 S2-034: SIDE-04 retitled when its second trigger was added.

## Vocabulary and terminology

- **A CAPS term with no vocabulary entry.**
  - a0 M1: BLIND SPOT; its definition had been put in a note.
- **A vocabulary term written in lowercase where its defined meaning is intended.**
  - a1: "enough broken line remains" → BROKEN LINE; "another driver" → DRIVER.
- **A lowercase phrase that looks like a vocab term and trips stage 1, with a different meaning** →
  reword it.
  - a1: PROC-01's "move into the passing lane" became "change lanes to pass".
- **A definition that builds in position, equipment or usage.** Define the thing itself.
  - a0 V2: SOLID LINE and BROKEN LINE had "at the left of the driver's lane".
  - S2-062: SNOW PLOW had "equipped with flashing blue lights".
- **A definition cited to a block that does not define the term** → self-made definition with empty
  evidence.
  - a0 V4: CYCLIST, which had cited 2.71's licensing facts.
  - S2-031: SOLID LINE, where 21.4 says what the line means, not what it is.
- **A vocabulary definition repeated in a rule's note.**
  - a0 N1: USER-01's note repeated DRIVER's definition.

## Citations

- **A list item cited without the line that introduces it.** Applied to every rule citing a list
  item.
  - a0 C1: 10.16, 10.29, 6.6, 14.13, 14.63, 22.96, 28.22, 23.19.
  - b0 m5: in the demerit table, the point heading carries the number used in `penalty` ("Two points"
    22.134 for NIGHT-01; "Three points" 22.112 for USER-19 and USER-21).
- **A cited block that does not support the rule.**
  - a0 C2: 18.36-c, the pedestrian-crossover caption.
  - a0 C3: 4.65 cited for switching to high beams.
  - S2-017: 10.21, a diagram that does not show the mirror condition.
  - S2-040: 10.36, about the signs, on the keep-right rule.
  - S2-055: 6.61, turbulence.
  - S2-059: 18.126-c.
  - S2-095: 12.24 on BEING-06.
  - b2 S2-032: 10.41 on SIDE-01 (it states the leftmost-lane instruction, not the permission).
  - The remark can stay in the note without a citation.
- **A diagram cited on the wrong rule.**
  - a0 C4: the move-over diagram 13.106 had been on the slow-down rule.
- **A supporting block not cited.**
  - S2-016: 10.17 on PROC-03.
  - S2-035: 18.9, which gives regulatory signs their force.
  - S2-050: Diagram 2-47 (10.27) on USER-05.
  - S3-002: 18.29, the "Slow traffic … must keep right" sign, on GEN-04.
  - S3-007: 4.65 and 14.8 for the new exception.
  - b2 S2-048: 13.107, the source of the lights in USER-20's condition.
  - b3 S3-003: 10.6, 10.7 and 16.40 (with intros 10.5 and 16.31), the general mirror and blind-spot
    checks for every lane change, on PROC-01.
  - b3 S3-007: 10.29–10.31 for NIGHT-01's narrowed exception.
- **A sample-test answer option cited without the answer key.** Add 28.42.
  - S2-086, S2-088, S2-090 (BEING-01, 02, 03).
- **Penalty parts not traced to their sources.**
  - a0 C5: the note now says which block gives the fine, jail term and demerit points.

## Vague terms

- **A vague word or phrase kept in the statement but not listed.** This is the most common error.
  Examples:
  - "safely" (GEN-02, GEN-03), "suddenly" (SIDE-02).
  - "approaching the crest of a hill" (S2-029), "slower vehicle" (S2-042).
  - "quickly and lightly" (S2-049), "limited speed" and "anticipate" (S2-056).
  - "watch carefully" (S2-063), "slow down" (S2-078), "moving slowly" (S2-082, S2-084).
  - "move to the right" and "wants to pass" (S2-087), "holding up a line of traffic" (S2-102).
  - "carefully" (S2-104).
  - b0 m3: "near an intersection" (SIDE-01), "slower vehicle" and "move to the right" (SIDE-02), "slow
    down" (SIDE-04), "moved right" (USER-07), "near the road" (USER-24), "preparing to turn left"
    (GEN-04).
- **A vague-term entry narrower than the vague phrase**, or with the wrong explanation.
  - S2-033: widened to "enough BROKEN LINE remains ahead to complete the PASS safely".
  - S2-071: "no speed given" was attached to "proceed with caution"; "reduce speed" was added.

## Notes

- **An inference or reading not stated in the note.**
  - S2-028: "not permitted 30 metres from" read as "within 30 metres of".
  - S2-045: SIGN-05's unnamed sign taken to be the 18.70 sign.
  - S2-018: a rule merged from the general and night passing steps.
  - b0 m8: PROC-01's note named only the blind-spot check as taken from 10.31; the mirror check was too.
  - b2 S2-001: GEN-02's object of the doubt is taken from the preceding sentence of 10.15.
  - b2 S2-014: NIGHT-01 is drawn from 4.65 and 14.8, and only 4.65 gives the passing exception.
  - b2 S2-018: 10.22 can be read two ways (does the "where…" clause qualify the hill crest too?).
  - b2 S2-039: USER-08's location of the extra room and its comparison are inferred from 6.55.
  - b2 S2-064: BEING-06's "right-hand lane" read as the lane to the right of the TRUCK PASSING LANE.
  - b3 S3-007: NIGHT-01's "unless you are passing it" read, from 10.30/10.31, as starting once alongside.
- **The handbook's reason missing from the note, or written into the action.**
  - b2 S2-036: USER-03's reason (the horn may frighten the cyclist) added to the note.
  - b2 S2-062: BEING-05's "to prevent a collision" moved from the action to the note.
- **A missing link to a related rule**, where one rule's scope depends on another.
  - S2-006: GEN-05 → GEN-07.
  - S2-048: USER-02 → USER-05.
  - S2-053: USER-07 → USER-06, and the pass is after the turn.
  - S2-068: USER-18 replaces USER-17 at stops with a passenger area.
  - S3-008: SIDE-01 is restricted by SIDE-02 and LOC-07.
  - b2 S2-019: LOC-08 → SIDE-04 (going around a blocking vehicle in an intersection).
  - b2 S2-054: WX-02 → WX-01 (passing in fog at all is banned).
  - b3 S3-004: GEN-05 ↔ SIDE-01 (far left lane on a freeway vs passing on the right).

## Coverage: rules the set left out

- **A rule hidden inside a vocabulary definition.**
  - a0 M9.1: trucks may not use the far left lane, which was only in TRUCK PASSING LANE. Added as
    GEN-07.
- **A rule about being passed.**
  - a0 M9.2: cyclists may take the lane to discourage unsafe passing. Added as BEING-07.
- **Passing a hazard other than a vehicle.**
  - S3-006: "If you see an animal on or near the road, slow down and pass carefully" (13.47). Added
    as USER-24.
  - b0 m7: the hazard-marker sign, "The downward lines show the side on which you may safely pass"
    (18.68-c). Added as SIGN-05 (MAY after b2 S2-028).
- **A restriction on passing stated outside the passing chapter.**
  - S3-008: do not go around a left-turner in an intersection (29.104, 10.11). Added as SIDE-04.
  - b0 m6: no lane change to pass in or near an intersection (10.11, 29.104); a PASS is a lane change.
    Added as LOC-08.

## Conflicts between rules

- **One rule requires what another rule or the handbook forbids in the same situation.**
  - S3-007: high beams while passing vs the 150 m low-beam rule.
  - S2-006: GEN-05 vs GEN-07, for trucks.
- **One rule's exception exempts the DRIVER from what another rule requires.**
  - b3 S3-007: NIGHT-01's "UNLESS … passing that vehicle" could exempt a driver closing in to pass from
    NIGHT-03's low-beam duty. Now "UNLESS the DRIVER has pulled out and is moving alongside the vehicle
    being passed".
- **A permission that overlaps restrictions elsewhere without saying so.**
  - S3-008: SIDE-01 vs SIDE-02, LOC-07 and the intersection rule.
  - b0 M1: SIDE-01's intersection exception forbade the shoulder pass LOC-07 allows.
  - b3 S3-004: GEN-05 (MUST use the far left lane on a freeway) vs SIDE-01 (MAY pass on the right on
    multi-lane roads). Both rest on the handbook, so notes in both now say how they relate.
- **Duplicate rules at different strengths.**
  - S3-009: SIGN-03 vs SIGN-04.
  - b0 m1: USER-02 vs USER-05 (see Strength for how this was finally resolved).
