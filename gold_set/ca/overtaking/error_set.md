# Error set: confirmed error types

Kinds of error that were confirmed and fixed at triage while building the CA overtaking gold set (steps a0–c0).

Examples give the step and finding id:
- a0 = `a0_freeform_report.md` (M = major; C, V, S, G, K, Q, N, O = minor)
- a2 S2 = `a2_atomic_report.md`, a3 S3 = `a3_aggregate_report.md`
- b0 = `b0_freeform_report.md` (M = major, m = minor)
- b2 S2 = `b2_atomic_report.md`, b3 S3 = `b3_aggregate_report.md`
- c0 = `c0_freeform_report.md` (m = minor)

Rule ids are as they were at that step. No rules were renumbered in this scope.

The companion list of reported errors that were rejected is `allow_list.md`.

## Faithfulness: the rule says something the handbook does not

- **MAY ONLY reading in a prohibition the handbook does not state.**
  - a0 M1: MARK-03 "MAY ONLY pass" next to a broken yellow line forbade passing everywhere else. 10.15's "only" belongs to "when it is safe". Now MAY.
- **A prohibition narrowed by a word from a neighbouring sentence.**
  - a2 S2-010: MARK-01 said "a single solid yellow line". 10.6's prohibition covers any solid yellow line on the driver's side.
- **Words added that the handbook does not use.**
  - a0 V3: PASS's definition had "…and then returning to the original lane", copied from the prompt's example.
  - a2 S2-025: LARGE VEHICLE named buses, which the CA large-vehicle section never does.
  - a2 S2-051: TRAFFIC BREAK's definition stated a purpose its cited block does not give.
- **Part of a handbook phrase left out.**
  - a2 S2-043: USER-11 dropped "plenty of space" before "(at least three feet)".
  - b2 S2-030: USER-16 dropped 13.47's "(hazard lights)", which helps the model recognise the vehicle.
  - b2 S2-052: BEING-08 waited for one emergency vehicle; 13.44 says "emergency vehicle(s)". Now "until every EMERGENCY VEHICLE has passed".
  - b2 S2-053: BEING-08's penalty dropped 13.44's "may" ("Failure to pull over may result in a ticket").
- **A trigger reworded away from the handbook's.**
  - b2 S2-056: BEING-09 said "approaches"; 13.48 says "when you see".
- **Wording that reads as a duty to pass.**
  - a2 S2-050: USER-15's "slow down and pass carefully" became "slow down and, when going past the vehicle, pass carefully".

## Strength (force and modal)

- **A speed restriction written as a plain permission.**
  - a0 S1: USER-04's "MAY pass it at no more than 10 mph" did not forbid passing faster. Now MAY ONLY, with the note explaining that it does not require passing.
- **Two duties under one ADVICE modal, with an "until" reaching both.**
  - a0 S3: USER-17 kept only "SHOULD NOT drive past the patrol vehicle". The speed-up sentence went to the note as outside the topic.
- **A ban folded into a permission as one of its terms.**
  - a2 S2-031: 13.18's "Do not drive through a safety zone under any condition" had been folded into USER-04's MAY ONLY (a0 O3). It was split out as USER-18 (INSTRUCTION / MUST NOT).
- **An exception to a requirement recast as a separate PERMISSION.**
  - a2 S2-048: USER-14 ("BICYCLIST MAY ride away from the right curb … when passing") became the requirement with its exception: "MUST ride as close as possible to the right curb … UNLESS passing…".
- **Strength reversed after review** (both later undone; see `allow_list.md`).
  - a0 S2 → a2 S2-007 (GEN-05); a2 S2-055 → a3 S3-009 (BEING-02).

## Conditions and exceptions

- **AND and OR mixed with no grouping.**
  - a0 M2: SIDE-01's three cases could be read as (A OR B) AND (C OR D). The left-turn case is now one fact joined by a lowercase "and".
- **A condition broader than the handbook's context.**
  - a0 K1: BEING-02 required any driver with cars behind to use a turnout. It now needs "the DRIVER is slower than the cars behind" (sign 10.66).
- **A condition that contradicts the action.**
  - a0 G2: USER-08 "WHEN passing a BICYCLIST … MUST … not pass until …" became "WHEN about to pass a BICYCLIST".
- **A condition phrase that no cited block supports.**
  - a2 S2-062: BEING-07's "in a travel lane" was dropped.
- **Whose vehicle is being passed or followed, not stated.**
  - a2 S2-053 (BEING-01, "…plans to pass the DRIVER"), S2-057 (BEING-04, "close behind the DRIVER's vehicle"), S2-060 (BEING-06, "passing the DRIVER's vehicle … the DRIVER's own lane").
- **A referent that is unclear or wrong.**
  - a0 G4: USER-05's "the vehicle cannot pass" became "the PASSER's vehicle".
  - a2 S2-006: GEN-04's "the PASSER's lane" became "the PASSER's original lane".
- **An exception that carries a duty with no modal.**
  - b0 M1: BEING-08's "UNLESS … in an INTERSECTION, in which case the DRIVER continues through it…" was cut down to the fact. The intersection duty became BEING-09.
- **An exception that lifts more of the action than it should.**
  - b0 M2 → b2 S2-042: BEING-01's motorcycle exception also lifted "allow the vehicle to pass". It was split, so BEING-10 holds only lane position with the exception.
- **A stop with no end point.**
  - b2 S2-055: BEING-09 now stops "until every EMERGENCY VEHICLE has passed" (13.44).
- **A rule that, with another, leaves no legal action.**
  - b3 S3-005: USER-02 (always pass a large vehicle on the left) and SIDE-02 (never pass on the left of a left-turn signal). USER-02 now has "UNLESS the LARGE VEHICLE is signaling a left turn", inferred from 10.202 and stated in the note.

## Grammar and wording

- **A second, lowercase modal inside the action.**
  - a0 M3: MARK-02's "MUST NOT pass over …, and must stay to the right" became "MUST stay to the right of the double solid yellow lines and not pass over them".
- **A lowercase "not" before the positive duties in a MUST action.**
  - a0 M4: USER-03 and USER-11 were reworded positive first, negated last.
- **A condition or action that doesn't read in the grammar.**
  - a0 G1: GEN-03's "WHEN before starting to pass" became "WHEN about to pass".
  - a0 G3: GEN-02's "SHOULD pass only when…" became "SHOULD NOT pass, UNLESS…".
- **A lowercase "and" joining two facts where the keyword AND fits** (no OR in the clause).
  - b2 S2-043: BEING-10's exception now reads "…is a motorcycle AND it is possible to move to one side of the lane".
- **A redundant qualifier before a defined term.**
  - a2 S2-052: "a law enforcement TRAFFIC BREAK" became "a TRAFFIC BREAK".
- **Sign wording in CAPS that trips the vocabulary check.**
  - a3 S3-001: LOC-07 names the sign by its meaning ("a do-not-pass sign"), with "DO NOT PASS" in the note.

## Vocabulary and terminology

- **A CAPS term with no vocabulary entry, or a key term left undefined.**
  - a0 V1: "HOV" was reworded as "high-occupancy vehicle".
  - a2 S2-018: CENTER LEFT TURN LANE was added (10.56), defined by its markings without its use.
  - b2 S2-054, S2-057: EMERGENCY VEHICLE was added (13.44) and capitalized in USER-16, BEING-08 and BEING-09.
- **A vocabulary term written in lowercase where its defined meaning is meant.**
  - a0 V2: "the driver ahead" and "another driver" became DRIVER.
- **The verb and the noun PASS not kept apart.**
  - a0 V3: PASS became a noun only, with verb uses lowercase across 34 rules.
- **A CAPS term used with a meaning its definition doesn't cover.**
  - a0 M5: PROC-01's "drive into the PASSING LANE" (the far left lane of a multilane road) applied to any open highway. Now "move into the lane used for passing".
- **A definition cited to a block that doesn't define the term, or carrying legal status.**
  - a0 V4: BICYCLIST and MOTORCYCLIST ("…same rights and responsibilities…") became "A person riding a bicycle/motorcycle." with empty evidence.
  - a0 C4: PASS cited the how-to-pass steps; evidence is now empty.
- **A definition that lists properties instead of the thing.**
  - a0 V5: LARGE VEHICLE ("…has large blind spots, takes longer to stop…").

## Citations

- **A cited id that does not exist.**
  - a0 C1: `13.111-c` (USER-07).
- **A list item cited without the line that introduces it.** Applied to every rule citing a list item.
  - a0 C2: 10.184, 10.200, 12.130, 12.103, 13.12, 13.35, 13.115.
  - b0 m3: 13.153 on USER-20.
- **A cited block that does not support the rule.**
  - a0 C3: 13.38 on BEING-06 (only the note uses it).
  - a2 S2-042: 17.12 on USER-11.
  - b0 m2: 12.67 (red-and-white signs) on LOC-07.
- **A heading cited as evidence.**
  - a2 S2-019: 10.55 on LOC-06. The heading 12.84 was also left off LOC-07 at a3 S3-001.
- **A supporting block not cited.**
  - a0 C5: 10.36–10.42 on PROC-01; a3 S3-007: 9.33–9.36 on PROC-01.
  - a2 S2-046: 13.101–13.107 on USER-13.
  - b2 S2-041: 13.35 and 13.41 for BEING-10's motorcycle exception.
  - b3 S3-005: 10.202 on USER-02.

## Vague terms

- **A vague word or phrase kept in the statement but not listed.** This is the most common error.
  - a0 Q1: "approaching a hill or curve" (LOC-01), "so close to the right side" (USER-05), "slow down" (USER-11, USER-15), "not able to be passed" (USER-13), "wishes to drive faster" and "move to the right" (BEING-04).
  - a2 S2-003 "approaching" (GEN-01), S2-016 "at crossroads or driveways" (LOC-03), S2-056 "cars are behind the DRIVER" (BEING-02), S2-058 "a tailgater is behind the DRIVER" (BEING-05).
  - b0 m4: "approaching" (USER-10, USER-16, USER-18) and "approaches" (BEING-08).
  - b2 S2-026 "steady flow of oncoming vehicles" (USER-12), S2-051 "a position that allows vehicles to pass" (BEING-07).
- **A vague-term explanation that points outside the rule.**
  - a2 S2-001 (GEN-01's one-third-mile remark), S2-039 (USER-09's "three-foot rule").
  - a2 S2-045: USER-12's explanation now says the left lane on a two-lane road is the oncoming lane.

## Notes

- **An inference or reading not stated in the note.**
  - a0 K2: USER-13's inferred condition.
  - a2 S2-014: MARK-04 relied on PASS being a lane change, which the CA definition does not say.
  - b2 S2-005: GEN-05 reads 10.33's "left lane" as the PASSING LANE.
  - b2 S2-010: LOC-07's direction qualifier.
  - b2 S2-031: USER-16's reading of 13.137's amber-light clause.
- **A missing link to a related rule.**
  - a0 N1 (SIDE-01 with USER-02, USER-05 and GEN-05), a0 N2 (USER-12 with USER-08).
  - b0 m1 (USER-04 with USER-20); a3 S3-008 (SIDE-01 with USER-05).
  - b3 S3-005 (USER-02 with SIDE-02).
- **A note that misstates the handbook or another rule.**
  - a0 N3: BEING-04 said "should" where 13.144 says "drive in the right lane".
  - b2 S2-009: LOC-07 said 12.85 mentions white regulatory signs; the link comes from its heading.
  - b2 S2-019: USER-05 said it "calls for" passing on the right; it only forbids the left.
  - c0 m1: SIDE-01 still said USER-02 means "always pass on the left" after b3 gave USER-02 an exception.
- **The reason for a strength or modal reading left implicit**, so judges keep raising it.
  - b3 S3-004: SIDE-01's note says MAY ONLY limits passing on the right only.
  - b3 S3-011: GEN-05's note says "so recorded as ADVICE although 10.33 is worded as a command".

## Granularity

- **An instruction limited by a condition that belongs only to its neighbour** → split.
  - a2 S2-036: USER-07's "leave space" applied only to lane-change passes. It became USER-19, for every pass of a BICYCLIST.
- **A rule whose exception should lift only part of the action** → split.
  - b2 S2-042: BEING-01 and BEING-10.

## Coverage: rules the set left out

- **A restriction on where to pass, stated outside the passing section.**
  - a0 M6: the center left turn lane "is not a regular traffic lane or passing lane" (10.56). Added as LOC-06.
  - a0 O1: no lane change over double solid white lines (10.19). Added as MARK-04.
- **A rule shown only by a sign.**
  - a3 S3-001: the DO NOT PASS sign in figure 12.89. Added as LOC-07.
- **Being passed by an emergency vehicle.**
  - a3 S3-002: pull over and stop (13.44, 13.48). Added as BEING-08, and BEING-09 at b0 M1.
- **Driving past a stopped school bus.**
  - a3 S3-003: stop for flashing red lights (13.158, 13.159). Added as USER-20.
- **How to return in front of a passed vehicle.**
  - a3 S3-004: do not cut in front of a large vehicle (13.8, 13.13). Added as USER-21.
