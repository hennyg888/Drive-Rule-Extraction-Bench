# Allow list: reported "errors" that are not errors

Kinds of finding that were rejected or ignored at triage while building the overtaking gold set
(steps a0–a3 and b0–b3). A future finding of one of these kinds can be rejected by pointing here.
Examples give the step and finding id: a0 = `a0_freeform_report.md` (M = major, others minor), a1 =
`a1_format_report.txt`, S2 = `a2_atomic_report.md`, S3 = `a3_aggregate_report.md`; b0 =
`b0_freeform_report.md` (M = major, m = minor), b2 S2 = `b2_atomic_report.md`, b3 S3 =
`b3_aggregate_report.md`. Rule ids are as they were at that step (the USER group was renumbered in a0
and b0).

The companion list of confirmed error types is `error_set.md`.

## Writing and grammar

- **Lowercase verb "pass" / "passing".** Only the noun PASS (the defined manoeuvre) is capitalized;
  the verb stays lowercase, as in the extraction prompt's example ("the PASSER MAY pass"). Stage 1
  allows it (`--allow-lowercase pass`).
  - S2-001, S2-003, S2-025, S2-032, S2-098 ("considering whether to overtake and pass", "MUST NOT
    pass"); S2-022 ("WHEN passing at night").
  - b2 S2-009 ("preparing to pass a vehicle"), b2 S2-016 ("passing at night"), b2 S2-020 (the noun PASS
    in a note and the verb "pass" in the rule).
- **A lowercase phrase that looks like a vocab term but means something else.** Only the CAPS term is
  bound by the vocabulary definition.
  - a0 V3: "the passing lane" (the lane a passer pulls into) vs PASSING LANE (the special passing or
    climbing lane).
  - S2-065: "passing a STREETCAR stop safety island" (driving past a fixed area, not overtaking).
  - Stage 1 cannot tell these apart, so where it flags one, the phrase is reworded rather than
    capitalized (a1: "move into the passing lane" → "change lanes to pass").
- **A positive and a negated phrase joined in one MUST action**, written positive first and negated
  last ("MUST go back to the original lane and not race it"), in place of separate MUST and MUST NOT
  rules. The "not" then clearly covers only the last phrase.
  - a0 M3 (PROC-07, TOW-04 reworded to this pattern; GEN-05, TOW-02 already in it); S2-011 (GEN-07),
    S2-020 (PROC-07), S2-101 (TOW-02), S2-103 (TOW-04). New rules are written this way too (S3-008,
    PASS-SIDE-04).
  - b2 S2-003 (GEN-05), b2 S2-033 (SIDE-02), b2 S2-065 (TOW-02), b2 S2-066 (TOW-04).
- **A positive instruction written as MUST NOT … UNLESS.** "When you can see the entire front …,
  make the lane change" → "MUST NOT move back …, UNLESS the entire front … can be seen".
  - a0 G2, S2-019 (PROC-05).
- **Alternatives joined by a lowercase "or" inside one fact of an AND chain.** The grammar has no
  brackets, so this is how (A OR B) AND C is written.
  - a0 G1 (LOC-03, USER-21); S2-079 (USER-22, "road maintenance or utility workers"). New conditions
    are written this way too (b2 S2-034, SIDE-04).
- **MAY ONLY attached to the action, explained in the note** ("the DRIVER MAY ONLY use the right
  shoulder to pass that vehicle", with a note saying it does not require using the shoulder). This
  holds only where the handbook does state the restriction ("only"); see `error_set.md`, b2 S2-028.
  - a0 G6, S2-030 (LOC-07).
- **A pronoun that can only refer to the one vehicle named in the condition** ("MUST NOT pass it,
  UNLESS the smaller vehicle has moved right").
  - S2-052 (USER-07).
- **Two names for the same vehicle where the referent is clear** ("the vehicle being passed" and "the
  passed vehicle").
  - b2 S2-012 (PROC-05).
- **Rule titles** are not part of the grammar and may use lowercase for defined terms.

## Vague terms

- **A vague phrase paraphrased close to the handbook** ("as soon as possible" for "as soon as you
  can"), with the handbook's wording in the note.
  - a0 G5, S2-093 (BEING-06), b2 S2-063 (BEING-06).
- **The hedge of ADVICE wording** ("SHOULD consider staying behind") is not a vague condition.
  - S2-010 (GEN-06), b2 S2-006 (GEN-06).

## Citations

- **Something mentioned only in a rule's note needs no citation**, such as a diagram named by its
  caption. Cite only what the rule itself rests on.
  - a0 C2 (captions of Diagrams 2-46, 2-48, 2-16, 2-49, 2-57); S2-047 (USER-01, Diagram 2-11).
  - b2 S2-011 (PROC-05, Diagram 2-46), b2 S2-041 (USER-08, the turbulence remark from 6.61).
- **The block that introduces a list stays cited with each list item**, even though it does not
  support the rule by itself.
  - S2-088 (BEING-02 keeps 10.16, "Here are the steps for passing a vehicle:").
  - b2 S2-013 (NIGHT-01 keeps 22.96, the offence table's lead-in), b2 S2-056 (BEING-02 keeps 10.16).
- **A diagram stays on the rule it shows**, not on a neighbouring rule about the same situation.
  - S2-074 (13.106, the move-over diagram, stays on USER-21 and is not added to USER-20; see a0 C4).
- **Night-step blocks cited on a rule that applies to every pass**, where the rule rests on them by the
  reviewer decision below.
  - b2 S2-008 (PROC-01 keeps 10.29 and 10.31). b3 S3-003 then added the general lane-change sources.

## Penalties

- **No penalty inferred from the general offence table** unless the handbook links the entry to the
  rule ("Failing to obey signs" for sign rules).
  - a0 C6.
- **Penalty sources already settled are not reopened.** For the emergency-vehicle rules, the fine
  and jail term come from 13.117, which 13.118 extends to a stopped tow truck, and the demerit points
  from the table (22.129, 22.130). The note says where each part comes from.
  - a0 C5; S2-070 (USER-19), S2-075 (USER-21); b2 S2-045 (USER-18), b2 S2-047 (USER-20).

## Strength

- **A stronger passage elsewhere that covers a different or narrower situation** is not "stronger
  wording of the same rule".
  - S3-003: 12.23's "illegal" covers a slower vehicle cutting in front of a faster one, not a passer
    moving back in (PROC-06 stays INSTRUCTION, as decided in a0 M8). Raised again in b3 S3-003.
  - S2-083: WX-03's stronger-wording note (14.68 advice vs 14.76 "Don't") was checked and found
    correct in a0. Raised again in b2 S2-055.
- **A figure's alt text counts as handbook wording for strength.** USER-16's REQUIREMENT rests on
  Diagram 2-49's alt text, "the required two metres", and the note quotes it.
  - b2 S2-044 (decided in b0 M2).
- **Strength taken from a sign the note identifies with the passage's unnamed sign**, when the note
  states the inference.
  - b2 S2-026 (SIGN-04, from 18.70; settled in S2-045).

## Vocabulary

- **A definition is not narrowed to exclude look-alikes or stretched to cover every use.** It defines
  the thing itself.
  - S2-034: BROKEN LINE need not exclude continuity lines. Raised again in b2 S2-021.
  - S3-010: PASS ("Changing lanes to move past a slower vehicle") need not be widened for shoulder
    passing or in-lane cases. Raised again in b3 S3-006.
  - b0 m9, b2 S2-025: PASSING LANE's definition (it describes the lane's use, and "PASSING LANE
    section" uses the term as a modifier) is left as is.
- **Details already carried by a vocabulary entry need not be repeated in a rule.**
  - S2-057 (recognising an LCV by its rear placard is in the LONG COMMERCIAL VEHICLE entry); b2 S2-042.

## Conditions and actor

- **The lead-in to a step list is not a condition of each step.** "If you have to pass and the way
  is clear, follow these steps:" only introduces the night-passing steps.
  - a0 M4; S2-023 (NIGHT-03), S2-026 (NIGHT-04); b2 S2-015 (NIGHT-03), b2 S2-017 (NIGHT-04).
- **A condition already implied by the rule's existing condition** need not be spelled out.
  - S2-014 (PROC-01's "about to change lanes to pass" already places the checks before the lane
    change); S2-097 (BEING-07's "too narrow to be shared safely" already carries "if necessary for
    safety"); S2-060 (farm machinery is covered whether or not "displaying" applies to it).
- **A rule whose scope is completed by sibling rules.** PROC-03 ("MUST NOT change lanes, UNLESS the
  PASSER has signalled") need not name each lane change: PROC-01 requires the left-turn signal before
  moving out and PROC-04 the signal before moving back.
  - b2 S2-010.
- **The handbook's own wording in a condition, when the rest of the rule fixes its meaning** ("the
  PASSER has pulled into the opposite lane", with "pay attention to oncoming traffic").
  - b2 S2-061 (BEING-04).
- **The actor follows the main passage's wording** when another passage words it slightly
  differently and the note records the difference.
  - S2-012 (GEN-07 "truck" from 10.26; 12.24's "large trucks" is in the note); S2-027 (LOC-01's
    DRIVER, not DRIVER or CYCLIST); b2 S2-005 (GEN-05's exception, "truck").
- **A paraphrase of a list of checks that covers the same checks.**
  - S2-076 (USER-21's "signalling and checking mirrors and BLIND SPOTS" covers the shoulder check);
    b2 S2-049 (USER-20).

## Notes

- **The note need not mention other sentences of the cited block that are rules of their own.**
  - S2-002 ("If in doubt, do not pass" is GEN-02); S2-021 ("It is unlawful" belongs to BEING-02);
    S2-051 (the pass-after-moving-right sentence is USER-07); S2-080 (the move-over sentence is
    USER-23).
  - b2 S2-019 (29.104's second sentence is SIDE-04; a one-line link was added instead); the second
    proposed sentences of b2 S2-036 and b2 S2-062 were left out for the same reason.
- **A note may name another rule.** Links between related rules are wanted (`error_set.md`: missing
  link to a related rule), so "notes must stand alone" does not forbid them.
  - b2 S2-030 (SIGN-05's pointer to LOC-07).
- **A condition taken from the cited block's own text needs no note**, even when that text is a
  parenthetical about a diagram.
  - b2 S2-022 (MARK-02's "enough BROKEN LINE remains ahead" is part of 21.6).
- **A sign may be named by its meaning**, with its appearance in the note or not at all.
  - S2-036 (SIGN-01 "do-not-pass sign"), S2-038 (SIGN-02), S2-039 (SIGN-03), S2-044 (SIGN-05).
  - b2 S2-023 (SIGN-03), b2 S2-024 (SIGN-04), b2 S2-029 (SIGN-05, the caption's own "downward lines").
- **A note that already says what the finding asks for.**
  - S2-064 (USER-17's note already describes Diagram 2-49).

## Organisation

- **The order of rules within a group.** A rule may be added at the end of its group to avoid
  renumbering.
  - a0 O1; b3 S3-005 (USER-24 added at the end of the USER group).
- **Loose group choice** (passing-lane rules under SIGN).
  - a0 O2, S2-043.

## Scope (overtaking)

- **General cautions about doing something else while another vehicle might overtake you.** These
  are about turning or pulling over, not about a pass. The BEING group covers only a pass that is
  actually happening or wanted.
  - a0 M9.3, S3-001 (29.44, check the blind spot before turning; 29.171, check the right blind spot
    before pulling over). Raised again in b3 S3-001.
- **General lane-use advice** not directly about overtaking.
  - a0 M9.5 (12.24, "Drive in the right-hand lane when possible").
- **Stopping rules phrased with "pass".**
  - a0 M9.6, S3-005 (stopped school bus, 8.32: "illegally passed a school bus").
- **Moving alongside a vehicle without overtaking it.**
  - S3-004 (6.57/6.58, not moving up beside a large vehicle that is turning wide). Raised again in
    b3 S3-002.
- **Passing a hazard other than a vehicle is in scope.** A finding that such a rule is outside the
  topic is rejected.
  - b2 S2-053 (USER-23, animals; added in S3-006), b2 S2-027 (SIGN-05, the hazard marker; added in b0
    m7).
  - b2 S2-052: 13.57 ("Don't try to drive around the animal") stays out of USER-23, as weighed in
    S3-006.

## Reviewer decisions that override the handbook's placement

- **The blind spot is checked on every pass**, not only at night, although the handbook lists it only
  in the night-passing steps (10.31).
  - a0 M2, S2-013 (PROC-01); b2 S2-007. Since b3 S3-003, PROC-01 also cites the general lane-change
    checks (10.6, 10.7, 16.40), so the decision now rests on handbook text too.

## Re-raising a settled triage

- **A finding that asks to undo an earlier triage decision** is rejected unless new evidence is given.
  - S2-007 asks to add back the "only" that a0 G3 removed from GEN-05. Raised again in b3 S3-004
    (rejected; notes were added instead).
  - S2-022 asks to reword NIGHT-02, whose wording was set in a0 M4.
  - b2 S2-002: 18.29 on GEN-04 (settled in S3-002). b2 S2-043: 6.74 on USER-10 (settled in S2-059).
    b2 S2-035 and b3 S3-008: 10.11 on SIDE-04 (settled in S3-008).
  - b2 S2-046: the direction-of-travel wording (settled in S2-072/S2-073). b2 S2-050: "that pose a
    hazard" (settled in S2-077/S2-081). b2 S2-057, S2-058, S2-059: BEING-02/03 citations and condition
    (settled in S2-088 to S2-090).
- **New evidence can reopen a decision.** These are examples of findings that did reopen one:
  - b2 S2-037 (rejected) and b3 S3-005 (accepted) raised the same objection to the USER-04 merge from
    b0 m1. S3-005 was accepted because it brought what S2-037 lacked: a fix that narrows USER-04 to
    10.24's situation, so it no longer duplicates the 6.32 advice.
  - b2 S2-038 reopened S2-053: the condition stopped holding after the turn, a point S2-053 had not
    weighed.
