# Freeform error check: `gold_set/tx/overtaking/b3_aggregate.json`

Source: `corpus/tx` · Prompt: `prompts/formal-rules` (system.md, task.md, schema.json) · Topic:
overtaking · Error types judged against `error_set.md`. Kinds of finding listed in `allow_list.md`, and
decisions from the a0–a3 and b0–b3 triages, are not raised again unless new evidence is given. Both lists
include the round-b decisions.

Handbook quotes are given as `id`: "text". Some are trimmed with "…". Rule ids are as they are in
`b3_aggregate.json`.

**What was checked**

- Scripted structure checks: each statement matches its fields, ids and numbering are valid, force agrees
  with modal, every CAPS term is in the vocabulary and every vocabulary term is used, every vague term
  appears in its statement, and every cited block id exists. **All pass** (58 rules, 16 vocabulary
  terms). Stage 1 (`check_format.py --handbook tx`) also passes.
- List-intro check: every cited list item has its introducing block cited, except 7.45 on PROC-06 and
  PROC-07 (m1). Lists that follow a heading have no lead-in (a0 C1); 7.29, between the heading 7.28 and
  its list, does not introduce the list.
- Every cross-reference between rules in the notes (9 notes, naming 14 rules) was resolved. All point to
  an existing rule with the intended content.
- The 16 rules changed in round b were read again against their cited blocks, with the full path of
  headings above each block: GEN-01, GEN-07, PROC-02, PROC-06, PROC-07, MARK-01, MARK-02, SIGN-02,
  USER-01, USER-02, USER-07, USER-09, USER-13, BEING-05, BEING-06 and BEING-10. Each was read against the
  rules it overlaps or links to: PROC-06/PROC-07/SIDE-01/SIDE-02, MARK-01/MARK-02/SIGN-01,
  SIGN-01/SIGN-02, USER-01/USER-02, USER-07/USER-08/USER-09, BEING-05/BEING-06/BEING-07/BEING-10, and
  GEN-07 with LOC-01 to LOC-04.
- Conventions set at triage were checked across the whole set: the noun PASS in CAPS and the verb in
  lowercase; "the DRIVER's vehicle" or "the PASSER's vehicle" as what is passed (a0 G7, b0 m3; see m3);
  full rule ids in notes (b0 m4); "DRIVER of a TRUCK" as the truck driver's actor (b3 S3-006); the same
  penalty in USER-01 and USER-02 (b2 S2-039, S2-041); and the "Reason given:" form in notes (see m2).
- The whole corpus was searched again for "pass", "passing" and "overtak" in blocks that are not cited.
  Round b added no rule, and none of these blocks is new: licence exams, inspections, review questions
  (18.12, 18.20, 18.64, 18.65), headings, trains, following distance (9.3, 16.63), parallel parking
  (8.45), 8.26 (b0 m2), 14.33 (a0 M6.5), 15.57 (check for passing vehicles before getting out when
  stopped by police) and 16.126 (a0 F1).

**Result: no major problems remain.** No rule says something the handbook does not, misstates its
strength, or breaks the grammar or vocabulary contract, and no two rules give conflicting instructions
for the same situation without a note saying how they relate. There are **3 minor findings** below.

**Triage:** all 3 minor findings were triaged. m2 was fixed in `c0_freeform.json`, which started as an
exact copy of `b3_aggregate.json`: only GEN-06's note changed. m1 and m3 were judged too minor and
ignored. Stage 1 on `c0_freeform.json` passes all 8 checks with no format errors (58 rules, 16 vocabulary
terms). `gold_set.json` is a copy of `c0_freeform.json`, frozen.

Severity: **Major** means the rule says something the handbook does not, misstates its strength, breaks
the grammar or vocabulary contract, or conflicts with another rule without saying so. **Minor** covers
citations, wording, links between rules, coverage on the boundary of the topic, and notes.

---

## Minor

### m1. PASS-PROC-06 and PASS-PROC-07 cite the list item 7.45 without its lead-in 7.42

*citation: list item without its lead-in* · high confidence · rules: PASS-PROC-06, PASS-PROC-07

b0 m1 cited 7.45 in both rules for the paved-shoulder exception. 7.45 is the third item of the list that
7.42 introduces:

- `7.42`: "In Texas, you can pass on the right only when conditions permit you to do so safely."
- `7.45`: "You may pass on a paved shoulder when the vehicle you are passing is slowing or stopped on the
  main traveled portion of the highway, disabled, or preparing to make a left turn."

a0 C1 applied "a list item cited without the line that introduces it" to every rule and vocabulary entry
citing a list item, and SIDE-02 cites 7.42 with 7.45. The two exceptions name only 7.45's cases; 7.42's
safety condition is left to SIDE-02, which both notes link ("Passing on a paved shoulder is allowed only
in the cases of PASS-SIDE-02 (7.45).").

- Fix: add 7.42 to the evidence of PROC-06 and PROC-07. The statements are unchanged.

- **Triage: ignored, too minor.** No change. Both exceptions rest on 7.45's cases, and both notes point to
  PASS-SIDE-02, which cites 7.42 with 7.45.

### m2. PASS-GEN-06's note does not use the "Reason given" form and addresses the reader

*note: wording* · high confidence · rules: PASS-GEN-06

GEN-06's note says: "Reason: the other driver likely cannot see you in or near the blind spot." Every
other note that gives the handbook's reason starts "Reason given:" (GEN-01, USER-09, USER-11, USER-12,
USER-13, USER-17), and b2 S2-050 changed USER-09's "Reason:" to that form. The "you" comes from 7.53 but
is not quoted:

- `7.53`: "… It is likely the other driver cannot see you if you are in or near their blind spot."

- Fix: replace that sentence with "Reason given: the other driver likely cannot see a vehicle in or near
  the blind spot."

- **Triage: fixed as proposed.** GEN-06's note now reads: "Diagram shows blind spots to the rear on both
  sides of a car. Reason given: the other driver likely cannot see a vehicle in or near the blind spot.
  Stated more broadly under Highway Safety Tips (10.48), for all driving, not only passing: stay behind or
  go around the other vehicle, and do not follow to the side." The rule is otherwise unchanged.

### m3. PASS-BEING-03 and PASS-BEING-07 say the actor is "being passed"

*wording: what is passed* · low confidence · rules: PASS-BEING-03, PASS-BEING-07

a0 G7 and b0 m3 settled that the DRIVER's vehicle, not the DRIVER, is passed. BEING-01, BEING-02 and
BEING-04 say "another vehicle is passing the DRIVER's vehicle", BEING-05 and BEING-06 say "a TRUCK is
passing the DRIVER's vehicle", and PROC-02 says "passing the PASSER's vehicle". Two conditions still use
the passive, with the actor as the one passed:

- BEING-03: "WHEN being passed on the left AND the lanes are not marked, the DRIVER MUST safely move as
  far to the right as possible."
- BEING-07: "WHEN being passed by another vehicle, the DRIVER of a TRUCK SHOULD stay to the side of the
  lane farther from the passing vehicle."
- `7.50`: "Safely move as far to the right as you can when being passed on the left and the lanes are not
  marked."

- Fix: BEING-03 when: "another vehicle is passing the DRIVER's vehicle on the left AND the lanes are not
  marked"; BEING-07 when: "another vehicle is passing the TRUCK".

- **Triage: ignored, too minor.** No change. "being passed" is the handbook's own wording (7.50), and the
  passive is not misread as passing a person. Neither b0 nor b2 raised it.

## Still open from earlier rounds

None. Every finding of rounds a and b has a Triage line, and no decision was left for later.
