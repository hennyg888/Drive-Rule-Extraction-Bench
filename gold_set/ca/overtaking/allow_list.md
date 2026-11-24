# Allow list: reported "errors" that are not errors

Kinds of finding that were rejected or ignored at triage while building the CA overtaking gold set (steps
a0–c0). A future finding of one of these kinds can be rejected by pointing here.

Examples give the step and finding id:
- a0 = `a0_freeform_report.md` (M = major; C, V, S, G, K, Q, N, O = minor)
- a2 S2 = `a2_atomic_report.md`, a3 S3 = `a3_aggregate_report.md`
- b0 = `b0_freeform_report.md` (M = major, m = minor)
- b2 S2 = `b2_atomic_report.md`, b3 S3 = `b3_aggregate_report.md`
- c0 = `c0_freeform_report.md` (m = minor)

Rule ids are as they were at that step. No rules were renumbered in this scope; new rules were always added at the end of their group.

Several rulings follow the MTO overtaking conventions, which the reviewer adopted for CA at a0 (for example V3). They are listed here with CA examples, so this file stands on its own. The companion list of confirmed error types is `error_set.md`.

## Writing and grammar

- **Lowercase verb "pass" / "passing".** Only the noun PASS is capitalized (a0 V3). Stage 1 runs with `--allow-lowercase pass`.
  - a2 S2-005 (GEN-03), S2-013 (MARK-03), S2-017 (LOC-03), S2-021 (PROC-02), and the casing part of S2-014 (MARK-04).
  - b2 S2-008 (LOC-03).
- **A positive and a negated phrase in one MUST action**, written positive first and negated last ("MUST move ahead of it after passing and not drive next to it longer than needed"), in place of separate MUST and MUST NOT rules.
  - a0 M3 (MARK-02, the reviewer's own wording), a0 M4 (USER-03, USER-11).
  - a2 S2-028 (USER-03), S2-037 (USER-08); b2 S2-017 (USER-03), S2-024 (USER-11).
- **The parts of one case joined by a lowercase "and" or "or" inside one fact of an OR chain.** The grammar has no brackets, so this is how A OR (B and C) OR D is written. Where a clause has no OR, the keyword AND is used instead (see `error_set.md`, b2 S2-043).
  - a0 M2 (SIDE-01's left-turn case).
  - a2 S2-002 and b2 S2-001 (GEN-01's "an oncoming vehicle or BICYCLIST OR a hill, …": all disjunctions, so the meaning is the same); a2 S2-022, b2 S2-014 (SIDE-01).
- **"pass over" in MARK-02**, the reviewer's own wording at a0 M3. Its note explains that it means drive across.
  - a2 S2-011.
- **A referent that can only mean one road user**, or two names for the same one ("the MOTORCYCLIST" and "the motorcycle"; "the patrol vehicle" during a TRAFFIC BREAK; "the DRIVER is slower").
  - a2 S2-027 (USER-02 "on the left side"), S2-035 (USER-06), S2-056 (BEING-02, kept); b2 S2-032 (USER-17), S2-046 (BEING-02).
- **A condition that keeps the rule from reading as a duty to pass**, even if it seems to repeat the actor ("AND intending to pass"; "WHEN passing").
  - a2 S2-009 (GEN-05), S2-021 (PROC-02).

## Actor

- **PASSER vs DRIVER for passing prohibitions, and PASSER for a driver only considering a pass.** Ignored by the reviewer at a3 S3-011, including GEN-04's "WHEN considering a PASS, the PASSER MUST NOT pass".
  - a2 S2-004 (GEN-02), S2-017 (LOC-03).
  - b2 S2-002 (GEN-01), S2-003 (GEN-04), S2-007 (LOC-03), S2-011 (LOC-07); b3 S3-008.
- **A finding that assumes PASS means a lane change.** The CA definition ("Moving past a slower or stopped vehicle or road user travelling in the same direction") does not require one.
  - a2 S2-038 (USER-08).

## Strength

- **GEN-05 stays ADVICE.** 10.33 "Use the left lane to pass" is introduced as one of the "tips for choosing a lane" (10.32). The reviewer reversed a0 S2 (INSTRUCTION) at a2 S2-007, and the note has said so explicitly since b3 S3-011.
  - b2 S2-004, b3 S3-011 (strength part).
- **BEING-02 is INSTRUCTION, and BEING-03 holds the legal requirement** with its thresholds (five or more vehicles, passing unsafe). Settled at a3 S3-009, with notes on both rules.
  - b3 S3-007.

## Citations

- **The block that introduces a list stays cited with each list item** (a0 C2), even when it adds nothing by itself.
  - a2 S2-024 (SIDE-02 keeps 10.200); b2 S2-037 (USER-20 keeps 13.153, the school-zone lead-in, added at b0 m3).
- **Something mentioned only in a note needs no citation.**
  - a2 S2-044 (USER-12, 13.115), S2-061 (BEING-06, 13.38).
  - b2 S2-025 (USER-12), S2-036 (USER-19), S2-050 (BEING-06, 13.38).
- **PROC-01 keeps the general lane-change and signal blocks** (10.36–10.42, 9.33–9.36), explained in its note. The reviewer chose this at a0 C5 and a3 S3-007.
  - a2 S2-020, b2 S2-012.
- **A figure that would only help recognition, where the rule is already clear** (the Crossroad warning sign in 12.90 for LOC-03).
  - b0 m5.

## Vocabulary

- **SAFETY ZONE is defined without its markings**, because 13.18 (raised buttons or markers) and 13.21 (dotted white lines) disagree. The difference is recorded in USER-18's note.
  - a0 V5; a2 S2-032, b2 S2-034.
- **TURNOUT's definition describes its use** ("…into which slower vehicles merge to let vehicles behind them pass"). It was restored at a2 S2-054, because without it the term doesn't tell a turnout from other roadside areas.
  - b2 S2-045.
- **"tailgater" is listed as a vague term, not given a vocabulary entry.** The handbook leaves it to judgement.
  - a2 S2-058; b2 S2-048.
- **LIGHT RAIL VEHICLE covers streetcars and trolleys**, and USER-04 uses the term for "streetcar, or trolley" (reviewer, a3 S3-011).
  - b2 S2-018, S2-021.

## Conditions and exceptions

- **Only the passing-related exceptions of a non-passing requirement are included.** USER-14 (a slower bicyclist keeps right) keeps only "UNLESS passing…", and its note names the other exceptions in 13.103–13.107 (reviewer, a2 S2-048).
  - b2 S2-028, b3 S3-010.
- **The lead-in to a list is not a condition of each item.**
  - a2 S2-040 (USER-09 under 13.115's "When you cannot change lanes…"); b2 S2-022.
- **A condition already covered by the rule's own wording** ("when safe to do so" covers a road with no lane to the right).
  - a2 S2-059, b2 S2-049 (BEING-05).
- **USER-13's inferred condition** ("…who is not able to be passed"). The note explains the inference (a0 K2), and 13.101–13.107 are cited (a2 S2-046).
  - a2 S2-047, b2 S2-027.
- **Wording settled at an earlier step:**
  - USER-05 "the PASSER's vehicle" for 13.23's "passenger vehicle" (a0 G4): a2 S2-034, b2 S2-020.
  - USER-15 "when going past the vehicle, pass carefully" (a2 S2-050): b2 S2-029.
  - USER-18's condition (a2 S2-031, b0 m4): b2 S2-033.

## Notes

- **A note may name another rule** (a0 N1), using short ids such as BEING-06.
  - a2 S2-033 (USER-05); b2 S2-015 (USER-02), S2-038 (USER-20), S2-044 (BEING-01).
- **A note may explain how the rule is read**, such as why the modal is MAY, not MAY ONLY.
  - a2 S2-012 (MARK-03).
- **The note need not restate sentences of the cited block that are rules of their own.**
  - a2 S2-023 (SIDE-01 and 10.202's "Never pass on the left…", which is SIDE-02); a2 S2-001 (GEN-01 only points to GEN-02).

## Granularity

- **Splits the reviewer accepted are not merged back.**
  - USER-07 / USER-19 (a2 S2-036): a3 S3-010, b2 S2-035.
  - BEING-01 / BEING-10 (b2 S2-042): b3 S3-006.
- **An atomic-check fix that would add a rule duplicating an existing one.** The atomic judge sees one rule at a time and can't know the other rule exists.
  - a2 S2-041 and b2 S2-023 (USER-11's steady-flow case is USER-12).

## Low confidence or too minor

- **Low-confidence findings where the rule's meaning is already clear**, and note additions that fix no confident error.
  - a2 S2-015 (MARK-04), S2-027 (USER-02); b0 m5 (LOC-03).
  - c0 m2 (USER-02's swing-wide link: note-only but medium confidence, rules correct as they stand), c0 m3 (BEING-09's empty penalty: low confidence, not note-only).

## Scope (overtaking, CA)

Decided by the reviewer. Some CA calls differ from MTO.

- **In scope** (a finding that one of these is out of scope is rejected):
  - pulling over and stopping for an emergency vehicle with siren and red lights (a3 S3-002; BEING-08, BEING-09);
  - not driving past a school bus flashing its red lights (a3 S3-003; USER-20);
  - not cutting in front of a large vehicle after passing it (a3 S3-004; USER-21);
  - the DO NOT PASS sign (a3 S3-001; LOC-07);
  - never driving through a safety zone (a2 S2-031; USER-18).
- **Out of scope: general rules of the road not specific to passing.**
  - 15.12, a vehicle merging in too closely: a3 S3-005.
  - 13.144 and the SLOWER TRAFFIC KEEP RIGHT sign, slower traffic keeps right: a0 N3, a3 S3-006, b3 S3-001.
  - Truck blind spots (No Zones) and driving alongside other vehicles: b3 S3-003.
  - Lingering beside, or moving in front of, a large vehicle without passing it: a2 S2-029, b2 S2-016, S2-039.
  - Lane changes made for reasons other than passing: b2 S2-006 (MARK-04), S2-040 (USER-21).
- **Ignored coverage suggestions:**
  - lane splitting as a separate rule (a0 O2; mentioned in BEING-06's note);
  - the double-double-yellow barrier, 10.13 (a0 O4, b3 S3-002).

## Reviewer decisions that resolve a conflict in the handbook

- **SIDE-01 has a fourth case, "OR the PASSER is overtaking a LIGHT RAIL VEHICLE"**, citing 13.22. It resolves the clash with USER-05, which forbids passing such a vehicle on the left on two-way streets (a3 S3-008). Since b3 S3-004, SIDE-01's note says MAY ONLY limits passing on the right and does not restrict passing on the left.
  - b2 S2-013, b3 S3-009 (rejected); b3 S3-004 (the finding misread MAY ONLY; only the note was added).

## Re-raising a settled triage

- **A finding that asks to undo an earlier triage decision** is rejected unless new evidence is given. Most b2 and b3 rejections are of this kind. Examples:
  - b2 S2-004 and b3 S3-011 (a2 S2-007); b2 S2-013 and b3 S3-009 (a3 S3-008)
  - b2 S2-028 and b3 S3-010 (a2 S2-048); b2 S2-023 (a2 S2-041); b2 S2-027 (a0 K2)
  - b3 S3-006 (b2 S2-042); b3 S3-002 (a0 O4)
- **New evidence can reopen a decision.** These findings did:
  - a2 S2-025: LARGE VEHICLE dropped "bus", reopening a0 V5. The CA large-vehicle section (13.8–13.16) never names buses, which have their own section.
  - a2 S2-054: TURNOUT's use was restored, reopening a0 V5. Without it the definition doesn't tell a turnout from other roadside areas.
  - a2 S2-019: the heading 10.55 cited at a0 M6 was removed, because headings are not citable blocks.
  - a3 S3-009: BEING-02 went back to INSTRUCTION, reversing a2 S2-055, because the REQUIREMENT made BEING-03's legal thresholds redundant.
  - a2 S2-007 (reviewer): GEN-05 went back to ADVICE, reversing a0 S2.
