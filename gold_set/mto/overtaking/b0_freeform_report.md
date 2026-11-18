# Freeform error check: `gold_set/mto/overtaking/a3_aggregate.json`

Source: `corpus/mto` · Prompt: `prompts/formal-rules` (system.md, task.md, schema.json) · Topic: overtaking ·
Error types judged against `error_set.md`; kinds of finding listed in `allow_list.md` and earlier triage
decisions (a0, S2, S3) are not raised again unless new evidence is given.

Handbook quotes are given as `id`: "text". Some are trimmed with "…".

**What was checked**

- Scripted structure checks: each statement matches its fields word for word, ids match TOPIC-GROUP-NN,
  numbers run in order within each group, force agrees with modal, every CAPS term is in the vocabulary
  and every vocabulary term is used, every vague term appears in its statement, and every cited block id
  (rules and vocabulary) exists in the corpus. **All pass.**
- A script listed every cited list item whose introducing block is not cited (see m5).
- Each rule was read against the text of its cited blocks. The 18.36 sign image was viewed: it shows
  the "NO PASSING HERE TO CROSSING" tab, so the note on PASS-LOC-01 is correct.
- The whole corpus was searched for "pass", "passing" and "overtak" to find rules that were left out.

**Result:** 73 rules and 20 vocabulary terms, with no format errors. There are **2 major** and **9 minor**
findings below.

**Triage:** all 11 findings were triaged, and fixes were applied to `b0_freeform.json`, which started as an
exact copy of `a3_aggregate.json`. Each decision is recorded under its finding as a **Triage** line.
- Rules added: PASS-LOC-08 (m6) and PASS-SIGN-05 (m7), each at the end of its group.
- Rule merged: PASS-USER-02 was merged into old PASS-USER-05 (m1), so old USER-03 to USER-24 are now
  **USER-02 to USER-23** (each drops by one). The notes that name USER rules were updated to the new ids:
  PROC-06 (old USER-08 → USER-07), old USER-07 (old USER-06 → USER-05), old USER-18 (old USER-17 → USER-16)
  and old USER-19 (old USER-20 → USER-19). Finding text uses
  the original ids, and Triage lines give the new id as "(now …)".
- After all fixes there are 74 rules and 20 vocabulary terms. The scripted checks pass on
  `b0_freeform.json`: statements match their fields, ids and numbering are valid, force agrees with modal,
  every CAPS term is in the vocabulary, every vague term appears in its statement, and every cited id
  exists. The list-intro check flags only the WX sub-headings left open in m5.

Severity: **Major** means the rule says something the handbook does not, or misstates its strength.
**Minor** covers conflicts and duplicates between rules, coverage gaps, citations, vague terms, notes and
vocabulary.

---

## Major

### M1. PASS-SIDE-01's intersection exception bans more than the handbook does, and contradicts PASS-LOC-07

*exception stretched / conflict* · medium confidence · rules: PASS-SIDE-01, PASS-LOC-07, PASS-SIDE-04

SIDE-01: "WHEN on a multi-lane road OR on a one-way road OR overtaking a STREETCAR OR overtaking a
left-turning vehicle, the DRIVER MAY pass on the right, UNLESS in or near an intersection."

The exception rests on 10.11, which bans *lane changes* near an intersection, not passing:
- `10.11.3`: "Don't change lanes in or near an intersection."
- `29.104`: "Do not go over lane markings or change lanes in the intersection. If your lane is blocked by
  a vehicle turning left …, slow down or stop instead of pulling out to go around the vehicle."

But the handbook allows passing on the right in two ways that need no lane change:
- `10.40.2`: "You may pass on the right on multi-lane or one-way roads and when overtaking a streetcar or
  a left-turning vehicle." A driver who stays in the right lane while a vehicle in the left lane waits
  to turn left is passing on the right without changing lanes.
- `10.38.1`: "You may drive on the right shoulder only to pass a vehicle turning left and only if the
  shoulder is paved." Driving onto the shoulder is not a lane change either.

A vehicle turning left is nearly always at or near an intersection. So the exception:
1. removes almost all of SIDE-01's own "overtaking a left-turning vehicle" case, and
2. forbids the shoulder pass that PASS-LOC-07 allows ("WHEN passing a vehicle that is turning left AND
   the right shoulder is paved, the DRIVER MAY ONLY use the right shoulder…"). SIDE-01's note says
   LOC-07 *restricts* this permission, but SIDE-01 now forbids the very case LOC-07 allows.

The exception was added in S3-008 as proposed. This finding gives new evidence that S3-008 did not weigh:
the conflict with LOC-07 and with SIDE-01's own left-turner case. The case S3-008 was worried about
(pulling out around a left-turner in an intersection) is fully covered by PASS-SIDE-04.

- Fix: change `unless` to "doing so requires changing lanes in or near an intersection". Statement: "…,
  the DRIVER MAY pass on the right, UNLESS doing so requires changing lanes in or near an intersection."
  Add to the note: "10.11 bans lane changes in or near an intersection. Passing on the right while
  staying in the DRIVER's lane, or on a paved right shoulder past a left-turner (PASS-LOC-07), is not a
  lane change. Going around a left-turner that blocks the lane is PASS-SIDE-04." Add "near an
  intersection" to `vague_terms` (see m3).
- **Triage: fixed as proposed.** SIDE-01 now reads: "WHEN on a multi-lane road OR on a one-way road OR
  overtaking a STREETCAR OR overtaking a left-turning vehicle, the DRIVER MAY pass on the right, UNLESS
  doing so requires changing lanes in or near an intersection." The proposed sentences were added to its
  note, followed by "PASS-LOC-08 also applies." (from m6). The vague term "near an intersection" was added
  (m3). Evidence is unchanged.

### M2. PASS-USER-17 is recorded as INSTRUCTION, but the handbook calls the 2-metre distance "required"

*strength* · medium confidence · rules: PASS-USER-17 (also the note of PASS-USER-18)

USER-17: "WHEN at a STREETCAR stop where passengers are getting off or on, the DRIVER MUST stay at least 2
metres behind the rear doors of the STREETCAR, UNLESS …" Force: INSTRUCTION.

- `10.43` (Diagram 2-49, cited by USER-17): the image is described as "a vehicle stopped the
  **required** two metres behind the rear doors of a stopped streetcar".
- `10.45.2`: "This **rule** does not apply at stops where an area has been set aside for streetcar
  passengers."
- The set's own note on USER-18 already calls it "the **requirement** to stop two metres behind the
  streetcar's rear doors (PASS-USER-17)".

task.md lists "required" under REQUIREMENT and says: "When two passages word the same rule differently,
record the stronger wording and say so in `note`." This is the same error type as a0 M8 and S2-085. The
set also contradicts itself: one rule's note calls USER-17 a requirement while USER-17 is recorded below
REQUIREMENT.

- Fix: set USER-17's force to REQUIREMENT (the modal stays MUST). Note: "10.45 words this as a plain
  command; Diagram 2-49 shows a vehicle stopped 'the required two metres' behind the rear doors. The
  stronger wording is recorded." This replaces the current note, which only describes the diagram.
- **Triage: fixed as proposed (now PASS-USER-16).** Force is now REQUIREMENT, and the modal stays MUST.
  The note was replaced with the proposed text. The note of old USER-18 (now USER-17), which calls it "the
  requirement", now agrees with the force.

---

## Minor

### m1. PASS-USER-02 and PASS-USER-05 give the same duty at different strengths

*duplicate rules at different strengths* · medium confidence · rules: PASS-USER-02, PASS-USER-05

- USER-02 (ADVICE): "WHEN passing a CYCLIST AND it is possible to change lanes, the DRIVER SHOULD change
  lanes to pass." (`6.32.4`: "Whenever possible, you should change lanes to pass.")
- USER-05 (INSTRUCTION): "WHEN wanting to pass a motorcycle, bicycle, limited-speed motorcycle or moped,
  the DRIVER MUST pass by changing lanes, not within the same lane." (`10.24.3`: "If you do want to pass
  these vehicles, do so by changing lanes.")

For a cyclist, the two rules state the same duty, one as SHOULD and one as MUST. USER-02's note even
points to USER-05 ("10.24 states passing these riders by changing lanes as an instruction; that is
PASS-USER-05"), but the set keeps both. This is the error type of S3-009 (SIGN-03 vs SIGN-04, merged):
task.md says to record the stronger wording and note the softer one.

- Fix: merge USER-02 into USER-05. USER-05 keeps INSTRUCTION / MUST. Add `6.32` to its evidence. Add to
  its note: "6.32 words this more softly for cyclists ('Whenever possible, you should change lanes to
  pass'); the plain command of 10.24 is recorded." Move USER-02's Diagram 2-47 remark into USER-05's
  note if wanted (10.27 is already cited there). Renumber USER-03 onward (each drops by one), and update the
  notes that name USER rules: PROC-06 (USER-08), USER-07 (USER-06), USER-18 (USER-17) and USER-19
  (USER-20).
- **Triage: fixed as proposed (merged rule is now PASS-USER-04).** USER-02 was removed. Old USER-05 keeps
  INSTRUCTION / MUST and its statement. Its evidence is now `["10.24", "10.27", "6.32"]`. Two sentences
  were added to its note: the proposed 6.32 sentence, and "Diagram 2-47 shows a car moving into the next
  lane to pass a cyclist in a sharrow lane." (moved from USER-02). The USER group was renumbered and the
  note cross-references were updated, as listed at the top.

### m2. PASS-USER-21 does not say the stopped vehicle is in the DRIVER's direction of travel

*condition broader than the handbook* · low–medium confidence · rules: PASS-USER-21

USER-21's condition: "the road has two or more lanes in the DRIVER's direction AND the DRIVER is
approaching either an EMERGENCY VEHICLE stopped … or a tow truck stopped …". The direction qualifier
covers only the *lanes*. Nothing says the stopped vehicle is on the DRIVER's side of the road, so the rule
also fires for an ambulance stopped on the far side of a divided highway.

- `13.109.1`: "When the roadway has two or more lanes of traffic in the same direction of your travel,
  you are required to move into a lane away from the emergency vehicle or tow truck, if safe to do so,
  **in addition to reducing the speed** of your vehicle and proceeding with caution." This ties the
  duty to the 13.107 situation.
- `13.107.1`: "When approaching any emergency vehicle that is stopped … or a tow truck with its amber
  lights flashing **in the same direction of your travel** …".

S2-072 and S2-073 put "in the DRIVER's direction of travel" at the front of USER-19's and USER-20's
conditions. USER-21 was not changed to match.

- Fix: when: "the road has two or more lanes in the DRIVER's direction AND the DRIVER is approaching, in
  the DRIVER's direction of travel, either an EMERGENCY VEHICLE stopped with its red, or red and blue,
  lights flashing or a tow truck stopped with its amber lights flashing". Update the statement to match.
- **Triage: fixed as proposed (now PASS-USER-20).** The condition and statement are as proposed. Evidence
  is unchanged, apart from the m5 addition.

### m3. Vague words kept in statements but not listed

*vague terms* · medium confidence · rules: PASS-SIDE-01, PASS-SIDE-02, PASS-SIDE-04, PASS-USER-07, PASS-USER-24, PASS-GEN-04

The most common error type in `error_set.md`. Each phrase below is in the statement, leaves a judgement
open, and has no `vague_terms` entry. The precedent is in brackets.

- **SIDE-01** "near an intersection": no distance given. [similar to "approaching the crest of a hill",
  S2-029]
- **SIDE-02** "slower vehicle" (twice): no speed difference given. [S2-042] "move to the right": whether
  it changes lanes or shifts within the lane, and how far, is not said. [S2-087]
- **SIDE-04** "slow down": no amount or target speed given. Its `vague_terms` list is empty. [S2-078]
- **USER-07** "moved right": how far right is not said. [S2-087]
- **USER-24** "near the road": no distance given. Only "slow down" and "carefully" are listed.
- **GEN-04** "preparing to turn left": does not say how far before the turn this starts. (Low confidence.
  The wording came from S2-005, which fixed possibility wording but did not list it as vague.)

- Fix: add an entry for each, for example `{"term": "near an intersection", "explanation": "no distance
  given"}` and `{"term": "slower vehicle", "explanation": "no speed difference given"}`.
- **Triage: fixed, all entries added as proposed.** Statements are unchanged.
  - SIDE-01: "near an intersection" (no distance given).
  - SIDE-02: "slower vehicle" (no speed difference given); "move to the right" (does not say whether to
    change lanes or shift within the lane, or how far).
  - SIDE-04: "slow down" (no amount or target speed given).
  - USER-07 (now USER-06): "moved right" (does not say how far right).
  - USER-24 (now USER-23): "near the road" (no distance given).
  - GEN-04: "preparing to turn left" (does not say how far before the turn this starts).

### m4. PASS-USER-09's "more room" has no comparison

*unclear referent* · low–medium confidence · rules: PASS-USER-09

USER-09: "WHEN passing a LARGE VEHICLE, the PASSER MUST allow more room in front of the LARGE VEHICLE
before returning to its lane." More than what? S2-054 added *where* the room goes but not the comparison.
S2-099 found the same defect in TOW-02 ("more room had no comparison"), which now says "than when not
towing".

- `6.55.1`: "Large commercial vehicles require a much longer distance to stop than smaller vehicles."
- `6.55.4`: "Allow more room when passing a large vehicle."

- Fix: action: "allow more room in front of the LARGE VEHICLE than when passing a smaller vehicle,
  before returning to its lane". Update the statement to match.
- **Triage: fixed as proposed (now PASS-USER-08).** It now reads: "WHEN passing a LARGE VEHICLE, the PASSER
  MUST allow more room in front of the LARGE VEHICLE than when passing a smaller vehicle, before returning
  to its lane." The vague term "more room" is kept.

### m5. The penalty tables' point headings are not cited

*citation (list intro / penalty source)* · medium confidence · rules: PASS-NIGHT-01, PASS-USER-19, PASS-USER-21

In the demerit table (page 22), each offence is a list item under a heading that gives the number of
points. The rules cite the offence and the table's lead-in (22.96), but not the heading that holds the
number they put in `penalty`:

- NIGHT-01 ("Two demerit points …") cites `22.135` "Failing to lower headlight beam", but not
  `22.134` "Two points".
- USER-19 ("… three demerit points …") cites `22.129`, and USER-21 cites `22.130`, but neither cites
  `22.112` "Three points".

This falls under two confirmed types: "A list item cited without the line that introduces it" (a0 C1,
applied to every rule) and "Penalty parts not traced to their sources" (a0 C5).

- Fix: add `22.134` to NIGHT-01's evidence, and `22.112` to USER-19's and USER-21's.
- Low confidence, same check: the WX rules cite each section's outer lead-in (`14.13`, `14.63`, added in
  a0 C1), but not the sub-headings directly over the cited items: `14.14` "DO:" (14.19), `14.28` "Don't:"
  (14.31), `14.32` "REMEMBER:" (14.35), `14.64` "DO:" (14.68) and `14.74` "DON'T:" (14.76). a0 C1 seems to
  have accepted the outer lead-in as enough, so this is listed only for a decision.
- **Triage: fixed as proposed.** The point headings were added right after 22.96:
  - NIGHT-01: `["4.65", "14.8", "22.96", "22.134", "22.135"]`.
  - USER-19 (now USER-18): `["13.107", "13.117", "13.118", "22.96", "22.112", "22.129"]`.
  - USER-21 (now USER-20): `["13.109", "13.117", "13.118", "22.96", "22.112", "22.130", "13.106"]`.
  - The WX sub-headings (the low-confidence part) were not added. They were offered only for a decision,
    outside the proposed fix, and stay open.

### m6. No rule against passing by changing lanes in or near an intersection (or in a construction zone)

*coverage: restriction stated outside the passing section* · low–medium confidence · rules: no rule (related: PASS-SIDE-01, PASS-SIDE-04)

PASS is defined as "Changing lanes to move past a slower vehicle". So a ban on changing lanes at a place
is a ban on passing there. The handbook states two such bans:

- `10.11.3` (in the lane-change section, just before Passing): "Don't change lanes in or near an
  intersection." `29.104.1`: "Do not go over lane markings or change lanes in the intersection."
- `13.40.3`: "In the construction zone, drive carefully and adjust your driving to suit the conditions,
  do not change lanes, be ready for sudden stops…"

The set uses 10.11 only as an exception to passing *on the right* (SIDE-01) and for the blocked-lane case
(SIDE-04). Passing on the left by changing lanes in or near an intersection, the usual case, has no LOC
rule. The construction-zone ban is not covered at all. This is the same kind of gap as S3-008's added rule
(SIDE-04, "a restriction on passing stated outside the passing chapter").

- Fix: add PASS-LOC-08, "No passing by lane change at intersections": "WHEN in or near an intersection,
  the DRIVER MUST NOT change lanes to pass." INSTRUCTION, evidence `["10.11", "29.104"]`, vague term
  "near an intersection" (no distance given). If M1 is fixed as proposed, add to SIDE-01's note that
  PASS-LOC-08 also applies. Optionally add PASS-LOC-09: "WHEN driving in a construction zone, the DRIVER
  MUST NOT change lanes to pass." INSTRUCTION, evidence `["13.40"]`. This one is closer to the scope
  boundary, since 13.40 is about construction zones in general.
- **Triage: fixed as proposed, with PASS-LOC-08 only.**
  - New PASS-LOC-08, "No passing by lane change at intersections": "WHEN in or near an intersection, the
    DRIVER MUST NOT change lanes to pass." INSTRUCTION, evidence `["10.11", "29.104"]`, vague term "near an
    intersection" (no distance given).
  - The rule draws on two places, so a note was added (task.md asks for one): "Both blocks ban changing
    lanes in or near an intersection; since a PASS is a lane change, this bans passing there by changing
    lanes. Passing on the right without a lane change is PASS-SIDE-01."
  - "PASS-LOC-08 also applies." was added to SIDE-01's note.
  - The optional construction-zone rule (LOC-09) was **not** added and stays open.

### m7. Hazard-marker sign: which side to pass a roadside hazard on is not covered

*coverage: passing a hazard other than a vehicle* · low confidence · rules: no rule (related: PASS-USER-22, PASS-USER-24)

- `18.68-c`: "Hazard close to the edge of the road. The downward lines show the side on which you may
  safely pass."

S3-006 brought passing a non-vehicle hazard into scope (animals, PASS-USER-24), and PASS-USER-22/23 cover
passing roadside workers. This warning sign says which side of a hazard to pass, and it is a cue the
driving model can see. No rule covers it.

- Fix: add a SIGN rule: "WHEN a hazard marker sign is posted at a hazard close to the edge of the road,
  the DRIVER MAY ONLY pass the hazard on the side shown by the sign's downward lines." PERMISSION / MAY
  ONLY, evidence `["18.68", "18.68-c"]`. The note should say that MAY ONLY here means the other side is not
  permitted, as in LOC-07. Or reject it as out of scope, if passing fixed objects is judged unlike passing
  animals.
- **Triage: fixed by adding the rule, as PASS-SIGN-05.**
  - "Hazard marker: pass on the marked side": "WHEN a hazard marker sign is posted at a hazard close to the
    edge of the road, the DRIVER MAY ONLY pass the hazard on the side shown by the sign's downward lines."
  - PERMISSION / MAY ONLY, evidence `["18.68", "18.68-c"]`, no vague terms.
  - Note: "MAY ONLY here means passing the hazard on the other side is not permitted, as in PASS-LOC-07; it
    does not require the DRIVER to pass."

### m8. PASS-PROC-01's note gives only part of what it takes from the night steps

*note: inference not fully stated* · low confidence · rules: PASS-PROC-01

The note says: "Blind-spot check drawn from the night-passing steps in 10.31." But the *mirror* check is
taken from 10.31 too. The general steps never mention mirrors:
- `10.17`: "Use your left-turn signal … and check that the way is clear ahead and behind before moving
  into the passing lane."
- `10.31.1`: "Signal, check your mirrors and blind spot, and pull out to pass."

The reviewer decision to apply the 10.31 checks to every pass (a0 M2) is not questioned here. Only the
note is incomplete (error type of S2-018).

- Fix: note: "Mirror and blind-spot checks drawn from the night-passing steps in 10.31."
- **Triage: fixed as proposed.** PROC-01's note now reads: "Mirror and blind-spot checks drawn from the
  night-passing steps in 10.31."

### m9. PASSING LANE's definition describes its use, and leaves unclear which lane it names

*vocabulary* · low confidence · rules: vocabulary PASSING LANE (used in PASS-SIGN-03, PASS-SIGN-04)

Definition: "A special passing or climbing lane that lets slower vehicles move into the right-hand lane so
faster ones can pass in the left lane." This has two problems:
- It defines the lane by its use (what it lets vehicles do), which `error_set.md` treats as an error
  ("A definition that builds in position, equipment or usage", a0 V2, S2-062).
- It does not say which lane is the PASSING LANE: the added lane, or the left lane where the passing
  happens. That matters for SIGN-04 ("the right-hand lane of a PASSING LANE section") and SIGN-03 ("a
  two-lane section where a PASSING LANE is provided").

- `10.35`: "Some roads have special passing or climbing lanes. These lanes let slower vehicles move into
  the right-hand lane so that faster ones can pass safely in the left lane."
- `18.40-c`: "Keep to the right lane except when passing on two-lane sections where climbing or passing
  lanes are provided."

- Fix: definition: "An extra lane added in the same direction on a section of a two-lane road, so that
  the section has two lanes in that direction." Keep evidence `10.35` and add `10.34` (Diagram 2-48). The
  usage stays in SIGN-03, where it already is.
- **Triage: ignored, no change.** The PASSING LANE definition is unchanged.

---

## Checked and not raised

These looked like possible findings but are already settled by `allow_list.md` or earlier triage:

- 13.57 ("Don't try to drive around the animal") against PASS-USER-24's "pass carefully": weighed and
  left out in S3-006.
- 12.23's "illegal" cutting in, for PROC-06: S3-003 / a0 M8.
- Stopped school bus (8.32), blind-spot checks when you may be overtaken (29.44, 29.171), and moving up
  beside a turning large vehicle (6.57, 6.58): out of scope (a0 M9.3, M9.6, S3-001, S3-004, S3-005).
- 6.47.4 (check for a passing cyclist before opening a door): a general caution about something else
  while you might be passed, the same kind as 29.44/29.171.
- Penalty sources for USER-19/21 (13.117, 13.118): settled in a0 C5 / S2-070 / S2-075. m5 adds only the
  missing points headings and does not reopen the sources.
- PROC-01 and PROC-03 both require signalling before the lane change. This is overlap at the same strength,
  and the handbook states both (10.17, 10.19). task.md prefers a repeated rule to a missing one.
