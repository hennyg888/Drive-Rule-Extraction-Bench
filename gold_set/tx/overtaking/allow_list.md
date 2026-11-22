# Allow list: reported "errors" that are not errors

Kinds of finding that were rejected or ignored at triage while building the overtaking gold set
(steps a0–a3 and b0–b3). A future finding of one of these kinds can be rejected by pointing here.
Examples give the step and finding id: a0 = `a0_freeform_report.md` (M = major; V, C, G, F, N =
minor), a1 = `a1_format_report.txt`, S2 = `a2_atomic_report.md`, S3 = `a3_aggregate_report.md`; b0 =
`b0_freeform_report.md` (m = minor), b2 S2 = `b2_atomic_report.md`, b3 S3 =
`b3_aggregate_report.md`. Rule ids are as they were at that step. No rule was renumbered: new rules
were added at the end of their groups.

The companion list of confirmed error types is `error_set.md`.

## Writing and grammar

- **Lowercase verb "pass" / "passing".** Only the noun PASS (the defined manoeuvre) is capitalized;
  the verb stays lowercase, as in the extraction prompt's example ("the PASSER MAY pass"). Stage 1
  allows it (`--allow-lowercase pass`).
  - a0 V1 (the verb was lowercased in the 21 statements that had capitalized it).
  - S2-001, S2-003, S2-004 ("about to pass", "changing lanes to pass", "WHEN passing"); S2-009
    ("UNLESS passing"); S2-081 ("another vehicle is passing the DRIVER's vehicle").
  - b2 S2-002, S2-003, S2-004, S2-009, S2-010, S2-011, S2-013, S2-014, S2-037 (the verb in
    conditions and actions); b2 S2-060 (BEING-04's "for the PASSER to pass").
- **A lowercase phrase that looks like a vocab term but means something else.** Only the CAPS term
  is bound by the vocabulary definition.
  - a0 G4, S2-038, S3-009, b2 S2-029: SIGN-02's "WHEN passing a warning sign" means driving past a
    fixed sign, not overtaking.
- **A positive and a negated phrase joined in one MUST action**, written positive first and negated
  last ("MUST either complete the PASS or slow down out of the other DRIVER's BLIND SPOT, and not
  drive or linger in it"), in place of a second modal or separate MUST and MUST NOT rules. The "not"
  then clearly covers only the last phrase.
  - a0 M1 (GEN-06, USER-09, USER-13 reworded to this pattern); S2-006 (GEN-06), S2-054 (USER-06),
    S2-061 (USER-09), S2-068 (USER-13).
  - Where the two phrases have different scopes, the rule is split instead (`error_set.md`, S2-063).
  - b2 S2-006 (GEN-06); b2 S2-047 (USER-09 was not split; 10.129's "Either" was added to group the
    alternatives, see `error_set.md`).
- **A positive instruction written as MUST NOT … UNLESS.** "Be sure to move back only when you can
  see the entire front of the truck" → "MUST NOT move back …, UNLESS the entire front of the TRUCK
  can be seen in the rearview mirror".
  - a0 (checked and found correct: USER-07); S2-055 kept the form when the condition was reworded.
- **Alternatives joined by a lowercase "or" inside one fact of an AND chain.** The grammar has no
  brackets, so this is how A AND (B OR C) is written.
  - a0 G1 (MARK-02, SIDE-01); S2-030 (MARK-02's "either … or"), S2-045 (SIDE-02).
  - b2 S2-022 (MARK-02), b2 S2-033 (SIDE-01, where "both … and" groups the two parts of 7.43), b2
    S2-036 (SIDE-02).
  - A lowercase "and" inside one fact works the same way: b2 S2-038 (USER-01's second exception, one
    place where all three conditions hold).
- **MAY ONLY attached to the action, explained in the note**, where the handbook states the "only"
  (7.42: "you can pass on the right only when conditions permit you to do so safely"). The note says
  that it does not forbid passing on the left, or require using the shoulder.
  - a0 G3 (SIDE-01, SIDE-02); S2-044 (SIDE-02); S3-004 (the misreading point only; the conflict it
    raised was fixed, see `error_set.md`).
  - b2 S2-035 (SIDE-02).
- **A pronoun whose referent is clear from the rule** ("WHEN the line the PASSER would cross … is a
  BROKEN LINE AND it is safe, the PASSER MAY cross it").
  - S2-028 (MARK-01).
- **A "before" clause that governs every step after it** ("MUST NOT move into the passing lane
  before checking …, and confirming …").
  - S2-051 (USER-04).
- **A purpose clause at the end of the action.** PROC-03's "turn on the left turn signal to alert
  DRIVERS behind" says why the signal is given; it does not make the signal depend on drivers being
  behind.
  - b2 S2-012 (the wording was set in the a1 triage).
- **Two situations from one handbook sentence, with the same strength, kept in one rule.**
  - S2-031 (MARK-02, from 6.187: "Do not cross the line if it is not safe or it is a solid yellow
    line").
  - b2 S2-022 (MARK-02).
- **A wording set at triage to keep a vocabulary term in CAPS.** "the DRIVER of the school bus"
  stays; "the school bus driver" would bring back the lowercase "driver" that stage 1 flags.
  - a1 (USER-02); S2-048, b2 S2-040.
- **One passage's wording kept where two passages state the same duty.**
  - b2 S2-056, b3 S3-008: USER-15 and USER-16 keep the wording set in S2-073 from 9.30 ("reduce …
    speed to 20 mph below the speed limit"). 5.70's "not more than 20 mph less than" is not a
    clearer ceiling.

## Vague terms

- **A condition whose timing is set by a sibling rule** needs no vague term. PROC-07's "has
  overtaken the vehicle being passed" uses 7.38's own word; when the PASSER may return is PROC-06's
  rule, where "safely cleared" is the vague term.
  - a0 G2; S2-022.
- **A proximity condition kept with a vague term**, rather than dropped. Without "near", the
  condition would hold for any motorcycle anywhere on the road.
  - a0 (vague terms: USER-13's "near a MOTORCYCLE"); S2-067, b2 S2-053.
- **A term whose meaning other rules fix is not vague.** Whether a stretch of road is a legal
  passing zone is set by the markings, signs and places in the LOC, MARK and SIGN rules, not left to
  the DRIVER's judgement.
  - b2 S2-042 (USER-04's "legal passing zone", in 10.112's words).
- **A vague phrase paraphrased close to the handbook.**
  - b2 S2-059 (BEING-03's "as far to the right as possible" for the handbook's "as you can"; the
    entry was set in a0, vague terms).

## Citations

- **Headings are not cited.** A condition taken from the heading above a cited block rests on that
  heading, so a finding that it is unsupported is rejected. task.md does not list headings as
  citable blocks.
  - a0 C1 (the lists under the headings 7.28, 7.34, 7.47 and 10.111 keep no lead-in).
  - S2-012, S2-014, S2-016, S2-017, S2-018, S2-020, S2-021 (PROC-01 to PROC-07: "two-lane road",
    from 7.34 "How to Pass on a Two-Lane Road"); S2-079, S2-080 (BEING-01, BEING-02: from 7.47 "When
    Another Vehicle is Passing").
  - S2-026, S2-029 (MARK-01's note and MARK-02: from 6.186 "Two-Lane Rural Road with Two-Way
    Traffic"); S2-034 (MARK-03: from 6.196 "Multi-lane Highway (Four or More Lanes)"); S2-043
    (SIGN-04: under 6.242 "Passing Traffic"); S2-059 (USER-09: from 10.128 "Cutting Off a Vehicle to
    Reach Your Exit or Turn").
  - The a2 judge was shown each cited block with only its chapter section, not the nearer heading,
    which is why it raised these.
  - b2 S2-025 (MARK-03's multi-lane condition, from 6.196).
- **Something mentioned only in a note or a vague-term explanation needs no citation.**
  - S2-035, S3-008 (SIGN-01's note on the pennant's fine, 6.266, 6.267); S2-066 (USER-12's
    explanation pointing to the cues in 10.207–10.210).
  - b2 S2-026, b3 S3-005 (SIGN-01's fine); b2 S2-052 (USER-12).
- **A caption that states what the ban rests on stays cited.**
  - a0 C2 (LOC-05 keeps 6.194 and 6.194-c: "Left Turn Lane Only" states the lane's exclusive use).
- **A block that supports one part of the rule stays cited**: its setting, its exception, or the
  rule stated more broadly. The note says which.
  - b2 S2-005 (10.48 on GEN-06 states the rule for all driving; added in a0 C3, noted in S2-008).
  - b2 S2-018 (7.45 on PROC-07, for the paved-shoulder exception; added in b0 m1).
  - b2 S2-064 (10.13 on BEING-09, for the FREEWAY setting; added in S2-087).

## Penalties

- **No penalty in `penalty` when part of what the rule covers has no stated penalty.** SIGN-01
  covers the regulatory "Do Not Pass" sign, which has none, and the "No Passing Zone" pennant, a
  warning sign with the 6.267 fine. The penalty stays empty, and the note gives the pennant's fine.
  - a0 M4; S2-035, S3-008; b2 S2-026, b3 S3-005.
- **The penalty is a few words** (task.md). The fines and jail terms for every offence in a table
  are not copied in.
  - b2 S2-039 (USER-01; the misstated conviction count was fixed, see `error_set.md`).

## Strength

- **A stronger passage elsewhere that covers a different or wider situation** is not "stronger
  wording of the same rule".
  - a0 F1: the street-racing law (9.37) reaches BEING-08 only through the glossary's definition of a
    race (16.125, 16.126). BEING-08 stays INSTRUCTION.
  - b3 S3-001: raised again with 9.43's penalty, which belongs to the racing law.
- **A plain command stays INSTRUCTION** when the other cited blocks only say what a marking means,
  with no "must", "may not" or penalty.
  - S2-032 (MARK-02: 6.187 "Do not cross"; 6.200 and 7.19 describe the no-passing zone).
- **An imperative is a plain command even when it asks the driver to help.** "Help the truck driver
  by keeping to the far side of your lane" is INSTRUCTION. The softer "You'll make it easier … if"
  sentence is a separate ADVICE rule.
  - S2-083 (BEING-05; BEING-06 is the ADVICE rule).
- **Lane choice worded as an imperative is INSTRUCTION.**
  - S3-005, b3 S3-004 (GEN-09, from 10.23: "Use the middle or left lane").

## Vocabulary

- **A CAPS term in a note that the vocabulary does define.**
  - S2-033, b2 S2-023 (NO-PASSING ZONE in MARK-02's note). The atomic-check judge is shown only the
    terms used in the statement.
- **A definition may name the use that makes the thing what it is.** A CENTER LEFT-TURN LANE is a
  lane for left turns, so its definition cannot leave out that use. This differs from a0 V2
  (`error_set.md`), where the line definitions built in what MARK-01 to MARK-03 state; here the
  "only" repeats LOC-05's ban without changing what any rule says.
  - b0 m5 (CENTER LEFT-TURN LANE, from 16.146 and 6.149).

## Conditions and actor

- **A situation that a sibling rule covers.** The atomic check reads one rule at a time.
  - S2-070, b2 S2-055: USER-15 says nothing about one-lane roads, because USER-16 covers them (split
    by lane count in a0 M6.1).
  - S2-060, b2 S2-046: USER-09's condition is the exit-or-turn situation of 10.128; cutting back in
    after passing a truck is USER-07.
  - S3-006: GEN-02 and GEN-03 (the basic rules for every pass, 7.30, 7.31) and PROC-02 and PROC-03
    (the two-lane steps, 7.35) are all stated by the handbook, and they do not conflict.
  - b2 S2-020: MARK-01 (crossing a BROKEN LINE) need not state 6.187's prohibitions, which are
    MARK-02; a link was added instead (`error_set.md`, Notes).
  - b2 S2-034: SIDE-01 covers a traffic lane, because passing on a paved shoulder is SIDE-02 (set in
    S3-004).
- **The actor is DRIVER where the handbook says "traffic" or "someone"**, since the rule set is
  written for drivers.
  - S2-042 (SIGN-03, 6.98 "traffic"); S2-086 (BEING-08, 15.79 "someone"); b2 S2-062 (BEING-08).
- **A reading of the handbook's wording that the rule already reflects.**
  - S2-005: GEN-05's source, "if you must return to your original lane", reads as "if you need to
    return"; the handbook does not mention giving up a pass.
  - S2-058, b2 S2-045: USER-08's "maintain speed", with the PASSER as actor, means the PASSER's own
    speed.
  - S2-062, b2 S2-048: USER-09 names the bus because 10.129 does ("in front of a truck or bus"),
    under a heading about cutting off any vehicle.
  - b2 S2-019: LOC-01 keeps the handbook's "left side of the road", and the note gives the reading
    (S2-023).
  - b2 S2-021: MARK-01's exception names the center line. Where there is no center line, the
    exception does not hold and the permission applies.
  - b2 S2-028: SIGN-01's "for the DRIVER's direction": a no-passing zone applies to one direction
    (6.200: "on your side of the road", cited by NO-PASSING ZONE).

## Notes

- **The note need not mention parts of the cited block that are outside the topic or are rules of
  their own.**
  - S2-011 (10.23's faster-traffic trigger, on GEN-09); S2-056 (10.114's maintain-speed sentence is
    USER-08).
  - S3-003: 10.113's "you may need to increase your speed" on a downgrade stays as context in
    USER-06's note. It is not worded as a permission or as advice.
  - b2 S2-051: USER-11's note leaves out 10.125's blind-spot reason, which goes with USER-17's ban
    (S2-065).
- **Emphasis stays in the note, not in the condition or action.**
  - a0 G5 (USER-05's "especially at night"); S2-052, b2 S2-043.
- **A note that already says what the finding asks for.**
  - S2-069 (USER-14's note names the duty being lifted).
- **A note may give the setting that comes from the block's own heading.**
  - S2-026 (MARK-01's "On a two-lane rural road", from 6.186).

## Organisation

- **The order of rules within a group.** A rule may be added at the end of its group to avoid
  renumbering.
  - a0 (checked and found correct: GEN-06 placed before GEN-07); a0 M6 (SIGN-03, SIGN-04, USER-15,
    USER-16 and BEING-10 added at the ends of their groups); S2-063 (USER-17).

## Scope (overtaking)

- **Lane choice by speed that does not mention passing.**
  - S2-011 (10.23's "if you are traveling faster than other traffic"); S3-001 (the "Slower Traffic
    Keep Right" sign 6.130, 6.197, 10.22).
  - GEN-08 and BEING-09 are in scope because their blocks mention passing (6.148: "The farthest left
    lane is for passing only"; 10.34: "to allow faster traffic to pass").
  - b2 S2-008 (GEN-09, 10.23's faster-traffic trigger again); b3 S3-003 (the "Slower Traffic Keep
    Right" sign again).
- **A cyclist's lane position not tied to passing.**
  - a0 M6.5 (10.184; 14.33 states the purpose of a marking, not a rule).
- **Markings that ban crossing in general, without mentioning passing.**
  - a0 M6.6 (6.209, the left-edge yellow line); S3-002 (6.211 and 6.139, double solid white lines
    between lanes going the same way).
  - In 7.19, "solid lane lines" are center lines, which MARK-02 and MARK-03 cover (S3-002).
  - b3 S3-002 (6.211, 6.139 and 6.209, raised again).
- **Passing a hazard other than a vehicle is in scope.** A finding that such a rule is outside the
  topic is rejected.
  - a0 M6.3 (SIGN-03, the two-arrow sign), a0 M6.4 (SIGN-04, barricade stripes under 6.242 "Passing
    Traffic"); S2-040, S2-043, S3-007; b2 S2-031, b2 S2-032, b3 S3-007.
  - 6.266's separate ban on driving around a barricade was not added (a0 M6.4).
- **A duty while doing something else that only leaves room for others to pass.** The BEING group
  covers a pass that is under way or wanted. A block that mentions passing can be in scope (GEN-08,
  BEING-09), but that alone does not make it so.
  - b0 m2 (8.26: how to leave the vehicle standing on a highway when it cannot be parked off the
    road).

## Tensions the handbook leaves open

- **Two rules that both rest on the handbook and pull different ways**, when the handbook does not
  say which applies. Notes in both rules link them.
  - a0 M5, S3-005: GEN-09 (MUST use the middle or left lane to pass on a multi-lane FREEWAY, 10.23)
    and SIDE-01 (MAY ONLY pass on the right on wide roads, 7.42, 7.43).
  - Raised again in b3 S3-004, which read 10.23 as lane-choice advice; 10.23 is an imperative
    (Strength).

## Re-raising a settled triage

- **A finding that asks to undo an earlier triage decision** is rejected unless new evidence is
  given.
  - S2-035, S3-008 (a0 M4); S2-038, S3-009 (a0 G4); S2-040, S2-043, S3-007 (a0 M6.3, M6.4); S2-044
    (a0 G3).
  - S2-048 (a1); S2-052 (a0 G5); S2-059, S2-060 (a0 M1); S2-067 (a0 vague terms); S2-070 (a0 M6.1);
    S3-005 (a0 M5).
  - b2 S2-005 (a0 C3, S2-008); b2 S2-007, S2-063 (a0 M5, S2-010, S2-087); b2 S2-008 (S2-011); b2
    S2-012 (a1); b2 S2-018 (b0 m1); b2 S2-019 (S2-023).
  - b2 S2-021 (a0 G8, S2-027); b2 S2-022 (S2-030, S2-031); b2 S2-025 (S2-034); b2 S2-026 (a0 M4); b2
    S2-027, S2-028 (S2-036); b2 S2-029 (a0 G4); b2 S2-031, S2-032 (a0 M6.3, M6.4).
  - b2 S2-033 (a0 G1); b2 S2-034 (S3-004); b2 S2-035 (a0 G3); b2 S2-036 (S2-045); b2 S2-040
    (S2-048); b2 S2-043 (a0 G5); b2 S2-045 (S2-058); b2 S2-046 (S2-059, S2-060); b2 S2-048 (S2-062).
  - b2 S2-051 (S2-065); b2 S2-052 (S2-066); b2 S2-053 (S2-067); b2 S2-055 (a0 M6.1, S2-070); b2
    S2-056, S2-058 (S2-073); b2 S2-057 (S2-072); b2 S2-061 (S2-084); b2 S2-062 (S2-086); b2 S2-064
    (S2-087).
  - b3 S3-001 (a0 F1); b3 S3-002 (a0 M6.6, S3-002); b3 S3-003 (S3-001, S2-011); b3 S3-004 (a0 M5,
    S3-005); b3 S3-005 (a0 M4, S2-035, S3-008); b3 S3-007 (a0 M6.3, M6.4, S3-007); b3 S3-008 (a0
    M6.1, S2-071, S2-073, S2-076, S2-077).
  - The b2 judge saw each cited block with its full heading path, so the heading findings of a2
    (Citations) were not repeated. Where it raised a point that was settled with the heading in view
    (b2 S2-032, S2-046, S2-063), it gave no new evidence.
- **New evidence can reopen a decision.**
  - S3-010 reversed S2-072 and S2-078 (and a0 M6.1's empty evidence): SERVICE VEHICLE now cites
    9.29. The new evidence: its definition copies 9.29's list almost word for word; FREEWAY, defined
    the same way from 10.13, cites 10.13; and task.md says to cite the block when the handbook
    supplies the definition.
  - b0 m3 reopened the wording a0 G7 gave PROC-02 ("passing the PASSER"); it is now "passing the
    PASSER's vehicle". The new evidence: the wording went against G7's own principle, that the
    vehicle, not the DRIVER, is passed.
  - b2 S2-044 reopened S2-056: USER-07's note now says that the flash not replacing the mirror check
    is a reading of 10.114 (`error_set.md`, Notes).
