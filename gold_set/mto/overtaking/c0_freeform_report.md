# Freeform error check: `gold_set/mto/overtaking/b3_aggregate.json`

Source: `corpus/mto` · Prompt: `prompts/formal-rules` (system.md, task.md, schema.json) · Topic: overtaking ·
Error types judged against `error_set.md`. Kinds of finding listed in `allow_list.md`, and decisions from
the a0–a3 and b0–b3 triages, are not raised again unless new evidence is given.

Handbook quotes are given as `id`: "text". Some are trimmed with "…".

**What was checked**

- Scripted structure checks: each statement matches its fields, ids and numbering are valid, force agrees
  with modal, every CAPS term is in the vocabulary and every vocabulary term is used, every vague term
  appears in its statement, and every cited block id exists. **All pass** (75 rules, 20 vocabulary terms).
  Stage 1 (`check_format.py`) also passes.
- List-intro check: every cited list item has its introducing block cited, except the WX sub-headings
  left open in b0 m5 (see "Still open").
- Every cross-reference between rules in the notes (23 of them) was resolved. All point to an existing
  rule with the intended content, including after the b0 renumbering and the b3 USER-24 addition.
- The rules changed in rounds b0–b3 were read again against their cited blocks, and each rule was read
  against the rules it now overlaps or links to: GEN-05/SIDE-01, LOC-07/LOC-08/SIDE-01/SIDE-04,
  NIGHT-01/03/04, USER-01/04/24, USER-05/06, USER-16/17/SIDE-03, BEING-01/03/07.

**Result: no major problems remain.** No rule says something the handbook does not, misstates its
strength, or breaks the grammar or vocabulary contract, and no two rules give conflicting instructions
for the same situation without a note saying how they relate. There are **4 minor findings** below and a
short list of items still open from earlier rounds.

**Triage:** all 4 minor findings were judged too minor and ignored. `b3_aggregate.json` is unchanged.

Severity: **Major** means the rule says something the handbook does not, misstates its strength, breaks
the grammar or vocabulary contract, or conflicts with another rule without saying so. **Minor** covers
links between rules, coverage on the boundary of the topic, and notes.

---

## Minor

### m1. PASS-SIDE-03 does not link to the streetcar-stop rules that limit it

*note: missing link to a related rule* · medium confidence · rules: PASS-SIDE-03, PASS-USER-16, PASS-USER-17

SIDE-03: "WHEN passing a STREETCAR, the DRIVER MUST pass on the right, UNLESS driving on a one-way road."
Its note is empty. At a stop, USER-16 requires the DRIVER to stay at least 2 metres behind the rear
doors, so passing on the right is not allowed there while passengers get on or off. Where there is a
passenger area, USER-17 governs how to pass it.

- `10.44`: "You must pass streetcars on the right unless you are driving on a one-way road."
- `10.45`: "At streetcar stops, stay at least two metres behind the rear doors where passengers are getting
  off or on. This rule does not apply at stops where an area has been set aside for streetcar passengers."

A reader of SIDE-03 alone could take passing a stopped streetcar on the right to be required or allowed
while passengers are getting off. This is the error type "missing link to a related rule, where one rule's
scope depends on another" (S2-048, S2-068, S3-008).

- Fix: SIDE-03 note: "At a STREETCAR stop where passengers are getting off or on, the DRIVER must stay at
  least 2 metres behind the rear doors (PASS-USER-16), except where an area is set aside for passengers
  (PASS-USER-17)."

- **Triage: ignored, too minor.** No change.

### m2. For a cyclist at the side of the lane, PASS-USER-04 (MUST) and PASS-USER-24 (SHOULD) overlap

*overlap at different strengths, resolved by notes* · low confidence · rules: PASS-USER-04, PASS-USER-24

Since b3 S3-005, USER-04 covers a rider who has pulled to one side of the lane (MUST change lanes), and
USER-24 covers passing any CYCLIST (SHOULD change lanes when possible). For a cyclist at the side of the
lane both apply, at different strengths. This is the shape of S3-009 (a3), which was fixed by merging.
Here the overlap is deliberate: the narrower, stronger rule wins, and both notes say so ("When a rider
has pulled to one side of the lane, PASS-USER-04 applies").

- Fix: none needed. Optionally add this case to `allow_list.md` (overlap where the narrower rule is
  stronger and both notes give the precedence), so later checks do not raise it again.

- **Triage: ignored, too minor.** No change.

### m3. PROC-01's new note implies the other lane-change steps also apply to every pass

*note / coverage on the topic boundary* · low confidence · rules: PASS-PROC-01

PROC-01's note (b3 S3-003) now says: "A PASS is a lane change, and the lane-change steps (10.6, 10.7) and
16.40 … give the mirror and blind-spot checks for every lane change." By the same reasoning, the other
lane-change steps apply to a pass too, but the set has no rule for them:

- `10.7`: "… Be especially careful to check for bicycles and other small vehicles."
- `10.8`: "Check again to make sure the way is clear and that no one is coming too fast from behind or
  from two lanes over on a multi-lane road."
- `10.9`: "Steer gradually into the new lane. Do not slow down, maintain the same speed or gently increase
  it."

These are general lane-change rules, not passing rules, so they belong to a lane-change topic. The issue is
only that the note's wording invites the question.

- Fix: either leave as is and record that general lane-change steps are out of scope, or narrow the
  note: "The general lane-change steps (10.6, 10.7) and 16.40 … give the same mirror and blind-spot checks
  for every lane change; the night-passing steps (10.31) repeat them for passing." Drop the clause "A PASS
  is a lane change, and".

- **Triage: ignored, too minor.** No change.

### m4. Going around a blocking obstacle in a work zone is not covered

*coverage: passing a hazard other than a vehicle* · low confidence · rules: no rule (related: PASS-USER-21, PASS-USER-22, PASS-SIGN-05)

- `13.43`: "If your lane is blocked and no one is directing traffic, yield to the driver coming from the
  opposite direction. When the way is clear, move slowly and carefully around the obstacle."

S3-006 (a3) and b0 m7 brought passing hazards other than vehicles into scope (animals, USER-23; hazard
marker, SIGN-05), and USER-21/22 cover passing roadside workers. Going around a lane-blocking obstacle
into the opposing lane is the same kind of manoeuvre, and it carries a yield duty. It is closer to
right-of-way than to overtaking, so this is a boundary case.

- Fix: either add a USER rule: "WHEN the DRIVER's lane is blocked by an obstacle in a work zone AND no one
  is directing traffic, the DRIVER MUST yield to traffic from the opposite direction and move slowly and
  carefully around the obstacle only when the way is clear." (INSTRUCTION, evidence `["13.43"]`, vague
  terms "slowly and carefully", "the way is clear"). Or reject it as right-of-way, not passing.

- **Triage: ignored, too minor.** No change.

---

## Still open from earlier rounds

These were left undecided, and nothing has changed them since:

- **b0 m5:** the WX sub-headings ("DO:", "Don't:", "REMEMBER:": 14.14, 14.28, 14.32, 14.64, 14.74) are not
  cited with the items under them. a0 C1 accepted the outer lead-ins (14.13, 14.63) as enough. This is
  the only thing the list-intro check still flags.
- **b0 m6:** the optional construction-zone rule (13.40: "do not change lanes" in a construction zone,
  which bans passing there by lane change) was not added.

## Suggested housekeeping

The b-round decisions are not yet in `allow_list.md` and `error_set.md`, and the judges re-raised several
of them (for example S2-031, S2-037, S2-044 in b2; S3-005, S3-008 in b3). Adding them would save triage
time on the next round. Confirmed error types:
- a permission's exception that duplicates another rule (b3 S3-008);
- a rule's condition broader than the handbook's context (b3 S3-005; USER-04 narrowed to 10.24's
  situation);
- MAY ONLY reading in a prohibition the handbook does not state (b2 S2-028);
- a condition that stops holding before the handbook's situation ends (b2 S2-038).

Rejected kinds:
- PASSING LANE's definition (b0 m9);
- REQUIREMENT force resting on a figure's alt text (b2 S2-044, decided in b0 M2).
