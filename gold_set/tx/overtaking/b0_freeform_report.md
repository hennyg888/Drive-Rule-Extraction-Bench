# Freeform error check: `gold_set/tx/overtaking/a3_aggregate.json`

Source: `corpus/tx` · Prompt: `prompts/formal-rules` (system.md, task.md, schema.json) · Topic:
overtaking · Error types judged against `error_set.md`; kinds of finding listed in `allow_list.md` and
earlier triage decisions (a0, a1, S2, S3) are not raised again unless new evidence is given.

Handbook quotes are given as `id`: "text". Some are trimmed with "…". Rule ids are as they are in
`a3_aggregate.json`.

**What was checked**

- Scripted structure checks: `check_format.py --handbook tx` runs all 8 checks: schema, each statement
  matches its fields word for word, ids and numbering, force agrees with modal, every cited block id
  (rules and vocabulary) exists in the corpus, every vague term appears in its statement, every CAPS term
  is in the vocabulary and every vocabulary term is used, and no vocabulary term is written in lowercase.
  **All pass.**
- Scripts also listed: rule ids in notes written without their topic (see m4); cited list items whose
  introducing block is not cited; cited table rows whose table caption is not cited; cited blocks that
  are headings.
- Each rule was read against the text of its cited blocks, with the full path of headings above each
  block. The 6.120-f1, 6.129-f1, 6.50-f1, 6.149-f1 sign images and the 6.194 diagram were viewed:
  6.120-f1 shows the DO NOT PASS sign with the NO PASSING ZONE pennant, and 6.194 and 6.149-f1 show left
  turns from the centre lane in both directions.
- The fixes of round a were checked for consistency with each other: the noun PASS in CAPS and the verb
  in lowercase, "the DRIVER's vehicle" (a0 G7, see m3), "farther from" (S2-082, S2-084), "posted speed
  limit" (S2-073), full rule ids in notes (S2-049, S2-085, see m4), SIDE-01 narrowed to a traffic lane
  (S3-004) and SERVICE VEHICLE citing 9.29 (S3-010).
- The whole corpus was searched for "pass", "passing" and "overtak" (109 blocks, 79 of them not cited;
  most are licence exams, inspections, quiz questions or sentences inside cited blocks) to find rules
  that were left out. It was also searched for passing described in other words: go or drive around, cut
  in, move over, shoulder, alongside, slow-moving vehicles, emergency vehicles, cyclists and motorcycles.
  A search for stated penalties (fines, misdemeanors, violations) near passing rules found none that the
  set leaves out.

**Result:** 58 rules and 16 vocabulary terms, with no format errors. There are **no major** and **5
minor** findings below.

**Triage:** all 5 findings were triaged, and fixes were applied to `b0_freeform.json`, which started as
an exact copy of `a3_aggregate.json`. Each decision is recorded under its finding as a **Triage** line.
- No rule was added, merged or renumbered, and the vocabulary is unchanged.
- Rules changed: PROC-06 and PROC-07 (m1), BEING-05, BEING-06 and PROC-02 (m3), and GEN-07's note (m4).
  Every statement a fix touched was rebuilt from its fields.
- After all fixes there are 58 rules and 16 vocabulary terms. All 8 format checks pass on
  `b0_freeform.json`: schema, statements match their fields, ids and numbering are valid, force agrees
  with modal, every cited id exists, every vague term appears in its statement, every CAPS term is in the
  vocabulary, and no vocabulary term is written in lowercase.

Severity: **Major** means the rule says something the handbook does not, or misstates its strength.
**Minor** covers conflicts and duplicates between rules, coverage gaps, citations, vague terms, notes and
vocabulary.

---

## Major

None found.

---

## Minor

### m1. PASS-PROC-06 requires passing on the left where PASS-SIDE-02 allows passing on a paved shoulder

*conflict: a duty forbids what a sibling permission allows* · medium confidence · rules: PASS-PROC-06,
PASS-PROC-07, PASS-SIDE-02

PROC-06: "WHEN passing on a two-lane road, the PASSER MUST pass on the left and not return to the right
lane until the overtaken vehicle is safely cleared and visible in the rearview mirror."

SIDE-02: "WHEN conditions permit doing so safely AND the vehicle being passed is slowing or stopped on
the main traveled portion of the HIGHWAY, disabled, or preparing to make a left turn, the PASSER MAY ONLY
pass on a paved shoulder."

- `7.38`: "Pass on the left and do not return to the right lane until you have safely cleared the
  overtaken vehicle."
- `7.45`: "You may pass on a paved shoulder when the vehicle you are passing is slowing or stopped on the
  main traveled portion of the highway, disabled, or preparing to make a left turn."

On a two-lane road with a paved shoulder, a PASSER behind a vehicle waiting to turn left meets SIDE-02's
condition, but PROC-06 still says the PASSER MUST pass on the left. 7.45 names this case outright, so the
handbook does settle it: the two-lane steps (7.34 "How to Pass on a Two-Lane Road") describe the usual
pass in the left lane, and 7.45 is a listed case where passing on the right is allowed. PROC-07 also
assumes a pass on the left ("turn on the right turn signal, return to the right lane"). This is the error
type of S3-004 (a rule that forbids what a sibling permission allows).

- Fix: PROC-06: unless "passing on a paved shoulder"; statement "…visible in the rearview mirror, UNLESS
  passing on a paved shoulder."; note "Passing on a paved shoulder is allowed only in the cases of
  PASS-SIDE-02 (7.45)." PROC-07: unless "the PASSER passed on a paved shoulder", with the same note. Or,
  if the reviewer prefers to keep the statements, a note only in PROC-06 and PROC-07, as GEN-09 and
  SIDE-01 are linked.
- **Triage: fixed as proposed, with the UNLESS (not the note-only option), and 7.45 cited.** The handbook
  names this case (7.45), so it is an exception to the two-lane steps, not a tension the handbook leaves
  open.
  - PROC-06 now reads: "WHEN passing on a two-lane road, the PASSER MUST pass on the left and not return
    to the right lane until the overtaken vehicle is safely cleared and visible in the rearview mirror,
    UNLESS passing on a paved shoulder." The diagram sentence of its note is kept, followed by "Passing
    on a paved shoulder is allowed only in the cases of PASS-SIDE-02 (7.45)."
  - PROC-07 now reads: "WHEN the PASSER has overtaken the vehicle being passed on a two-lane road, the
    PASSER MUST turn on the right turn signal, return to the right lane, and turn the signal off after
    the lane change is completed, UNLESS the PASSER passed on a paved shoulder." Its note, which was
    empty, is the same sentence.
  - Evidence: PROC-06 `["7.38", "7.40", "7.45"]`, PROC-07 `["7.39", "7.45"]`. 7.45 was added because the
    new exception rests on it (task.md: a rule and its exception list each block).

### m2. No rule for leaving room for others to pass a vehicle stopped on a highway

*coverage: rule stated outside the passing section* · low confidence · rules: no rule (related:
PASS-BEING-04, PASS-BEING-09)

Under the heading 8.24 "Parking, Stopping, or Standing on a Highway Outside an Urban Area":
- `8.25`: "Never park or leave a vehicle to stand idling on the paved part of any highway outside of a
  business or residential district when you can park off the road. If you cannot park off the road:"
- `8.26`: "Leave plenty of room for others to pass"

The allow list puts a rule in scope when its block mentions passing (GEN-08 and BEING-09, from 6.148 and
10.34). 8.26 is a plain command about making room for others to pass the DRIVER's stopped vehicle, close
to BEING-04 ("make it as safe and easy as possible for the PASSER to pass") and BEING-09 ("move to
another lane to allow faster traffic to pass").

- Fix: add PASS-BEING-11 "Leave room to pass a vehicle stopped on a highway": INSTRUCTION / MUST, actor
  DRIVER, when "the DRIVER has parked or left the DRIVER's vehicle standing on the paved part of a
  HIGHWAY outside a business or residential district because it cannot be parked off the road", action
  "leave plenty of room for others to pass", vague term "plenty of room" ("no distance given"), evidence
  `["8.25", "8.26"]`. Or reject it as out of scope, if a parking rule whose only link to passing is this
  list item is judged unlike GEN-08 and BEING-09; it then goes in the allow list's Scope section.
- **Triage: ignored, no change (out of scope).** No rule was added. 8.26 is a parking duty: it says how
  to leave the DRIVER's vehicle standing on a highway when it cannot be parked off the road. The BEING
  group covers a pass that is under way or wanted (BEING-04: "another vehicle is passing"; BEING-09: "to
  allow faster traffic to pass"). A duty while doing something else, which only leaves room for others to
  pass, is outside the topic. A block that mentions passing can be in scope (GEN-08, BEING-09), but that
  alone does not make it so.

### m3. PASS-BEING-05 and PASS-BEING-06 still say a TRUCK is "passing the DRIVER"

*wording: triage convention not applied everywhere* · medium confidence · rules: PASS-BEING-05,
PASS-BEING-06

a0 G7 found that "another vehicle is passing the DRIVER" does not say that it is the DRIVER's vehicle
("The DRIVER is a person; it is the DRIVER's vehicle that is passed"), and BEING-01, BEING-02 and
BEING-04 were changed to "passing the DRIVER's vehicle". BEING-05 and BEING-06, from the same kind of
sentence, were not:
- BEING-05: "WHEN a TRUCK is passing the DRIVER, the DRIVER MUST keep to the side of the DRIVER's lane
  farther from the passing TRUCK."
- BEING-06: "WHEN a TRUCK is passing the DRIVER, the DRIVER SHOULD slightly reduce speed."
- `10.115`: "When a truck passes you, help the truck driver by keeping to the far side of your lane."

PROC-02's "no other vehicles are passing the PASSER" was the wording a0 G7 itself chose, so it is not
raised. The reviewer may still want "the PASSER's vehicle" there, for the same reason.

- Fix: when: "a TRUCK is passing the DRIVER's vehicle" in BEING-05 and BEING-06; statements updated to
  match.
- **Triage: fixed as proposed, and PROC-02 as well.** BEING-05 now reads: "WHEN a TRUCK is passing the
  DRIVER's vehicle, the DRIVER MUST keep to the side of the DRIVER's lane farther from the passing
  TRUCK." BEING-06 now reads: "WHEN a TRUCK is passing the DRIVER's vehicle, the DRIVER SHOULD slightly
  reduce speed." Evidence and notes are unchanged.
  - PROC-02 was offered only for a decision, and the reviewer chose to change it. This reopens the
    wording a0 G7 chose for PROC-02; the new evidence is that it went against G7's own principle (the
    DRIVER's vehicle, not the DRIVER, is passed). PROC-02 now reads: "WHEN preparing to pass on a
    two-lane road, the PASSER MUST check the rearview mirror and side mirrors and look over the shoulder
    into the BLIND SPOT to make sure the roadway is clear and no other vehicles are passing the PASSER's
    vehicle." Evidence and note are unchanged.

### m4. PASS-GEN-07's note names rules without their topic

*note: rule id written without its topic* · high confidence · rules: PASS-GEN-07

GEN-07's note: "Worded 'Always keep to the right side of the road except when…'. LOC-01 to LOC-04,
MARK-02 and SIGN-01 limit when the left side of the road may be used to pass."

Every other note names rules in full (PASS-SIDE-01, PASS-GEN-09, PASS-USER-01, PASS-BEING-10). S2-049 and
S2-085 fixed this error in USER-01 and BEING-07; GEN-07's note was written at a0 M2, and a2 reported no
finding on GEN-07.

- Fix: note: "Worded 'Always keep to the right side of the road except when…'. PASS-LOC-01 to
  PASS-LOC-04, PASS-MARK-02 and PASS-SIGN-01 limit when the left side of the road may be used to pass."
- **Triage: fixed as proposed.** GEN-07's note now reads: "Worded 'Always keep to the right side of the
  road except when…'. PASS-LOC-01 to PASS-LOC-04, PASS-MARK-02 and PASS-SIGN-01 limit when the left side
  of the road may be used to pass." The rule is otherwise unchanged.

### m5. CENTER LEFT-TURN LANE's definition builds in the ban that PASS-LOC-05 states

*vocabulary: definition builds in use* · low confidence · rules: vocabulary CENTER LEFT-TURN LANE (used
in PASS-LOC-05)

Definition: "A center lane shared by traffic in both directions that is used only by vehicles turning
left." Evidence `["16.146", "6.149", "6.194"]`.

The "only" is the restriction that LOC-05 records as a rule ("MUST NOT use the CENTER LEFT-TURN LANE for
passing or as a through-traffic lane"), from:
- `6.149`: "The center lane is only used for vehicles turning left, and should never be used for passing
  or moving through traffic."

The glossary defines the lane by what it is for, without the restriction:
- `16.146`: "shared left-turn lane – the lane on a busy street helping drivers make safe mid-block left
  turns into business areas from a center lane"

a0 V2 took this kind of meaning out of the line definitions, so that it stays in MARK-01 to MARK-03.
Here, with "only" in the definition, LOC-05's ban on through traffic follows from the term itself.

- Fix: definition: "A center lane, shared by traffic in both directions, from which vehicles make left
  turns." Evidence unchanged; LOC-05 keeps the ban.
- **Triage: ignored, no change.** The CENTER LEFT-TURN LANE definition is unchanged. A CENTER LEFT-TURN
  LANE is a lane for left turns, so its definition cannot leave out its use, and the definition follows
  the blocks it cites (16.146, 6.149). a0 V2's line definitions built in what MARK-01 to MARK-03 state;
  here "only" repeats LOC-05's ban without changing what any rule says. LOC-05 still states the ban, with
  its own evidence.

---

## Checked and not raised

These looked like possible findings but are settled by `allow_list.md` or earlier triage, or are not
errors:

- USER-09 keeps 10.129's "Never cut in front of a truck" to the exit-or-turn setting of its heading:
  S2-059, S2-060.
- GEN-02 to GEN-05 cite the list items 7.30–7.33 without 7.29. The list sits under the heading 7.28 with
  no lead-in (a0 C1); 7.29 ("It is not always safe to pass…") does not introduce it.
- Sign-table rows are cited without their table captions (6.45, 6.62, 6.116). The captions only name the
  table. SIGN-02's signs are warning signs by their section heading and Table 18's caption, and
  conditions taken from headings need no citation (allow list, Citations). GEN-08 and LOC-05 cite 6.115,
  which introduces Table 19.
- TRUCK cites the heading 10.109 "Share the Road with Trucks (Large trucks and truck-tractor
  combinations)". It is the only block that says what the handbook means by a truck, and S3-010 says to
  cite the block that supplies a definition. The allow-list entry "Headings are not cited" is about
  conditions taken from a heading.
- FREEWAY's definition repeats the word "freeway". It is 10.13's list, the handbook defines none of these
  roads, and task.md says not to make up definitions for terms the handbook leaves undefined.
- 6.141 (a sign: the shoulder is only for vehicles that must stop in an emergency) against SIDE-02's
  paved-shoulder pass: a sign that limits shoulder use in general, without mentioning passing, the same
  kind as a0 M6.6 and S3-002.
- 5.63 (pull to the right and stop for an approaching emergency vehicle), 15.78 ("Do not cut into another
  driver's lane of traffic") and 10.162 (following distance behind a motorcycle): yielding, lane changes
  and following, none of them about passing.
- 6.268 (a Class B misdemeanor for a warning sign or barricade placed where water is over the road): it
  applies only to flooded roads, so SIGN-02's penalty stays the 6.267 fine.
- No penalty for slowing down or moving over (USER-15, USER-16) is stated anywhere in the corpus, so
  their penalty stays empty.
- 16.125/16.126 (a race includes preventing a pass): a0 F1. 14.10, 14.19, 14.33 (cyclist lane position):
  a0 M6.5.
- The review questions 18.12, 18.20, 18.64 and 18.65 ask about passing but state no rule; the rules they
  ask about are SIGN-01, USER-01/02, LOC-01 to LOC-04 and SIDE-01 to SIDE-03.
- GEN-09's note says SIDE-01 permits passing on the right "on multi-lane roads". Since S3-004, SIDE-01
  covers a traffic lane on a road with two or more lanes in each direction, or a one-way road. The note
  is still accurate for the multi-lane FREEWAY it is about.
