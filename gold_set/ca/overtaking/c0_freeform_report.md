# Final freeform check: `gold_set/ca/overtaking/b3_aggregate.json`

Source: `corpus/ca` · Prompt: `prompts/formal-rules` (system.md, task.md, schema.json) · Topic: overtaking · Round c, stage 0 (final check, §A4)

Quotations from the handbook are given as `id`: "text", and some are trimmed with "…".

**What was checked**

- The format check (`check_format.py b3_aggregate.json --handbook ca --allow-lowercase pass`) passes with no errors.
- Scripted checks beyond stage 1:
  - every rule id named in a note exists;
  - no condition or exception mixes the AND and OR keywords;
  - no lowercase modal appears in an action (the one match, GEN-03's "may cause", is the handbook's possibility wording);
  - "emergency vehicle" is capitalized in every statement since EMERGENCY VEHICLE was added.
- The rules changed since the b0 check were read against their cited blocks: BEING-01 and BEING-10 (split at b2 S2-042), BEING-08 and BEING-09, USER-16, USER-12, BEING-07 and the EMERGENCY VEHICLE entry (b2), and USER-02, SIDE-01, SIDE-02 and GEN-05 (b3).
- Their interactions with neighbouring rules were checked: BEING-01/05/06/10, BEING-08/09, USER-01/02 with SIDE-01/02, and USER-04/05 with SIDE-01.
- The whole set was checked earlier in this round (b0, then b2 and b3 on the changed rules). Findings were weighed only against the CA triage decisions in the a0, a2, a3, b0, b2 and b3 reports. Nothing settled there is raised again.

**Result:** 52 rules and 16 vocabulary terms. **No major problems. 3 minor findings.**

Per §A4, the set was frozen as `gold_set.json` after the minor triage below.

**Triage and freeze:** all 3 minor findings were triaged under the reviewer's rule: apply a fix only when it changes just a note and the error is confident, otherwise ignore it as too minor. m1 was fixed, and m2 and m3 were ignored. The fix was applied to `c0_freeform.json` (a copy of `b3_aggregate.json` with the one note edit). That file was copied unchanged to **`gold_set.json`**, the frozen CA overtaking gold set.

| Frozen gold set | |
|---|---|
| File | `gold_set/ca/overtaking/gold_set.json` (identical to `c0_freeform.json`) |
| SHA-256 | `c8392a54b9d7eed67793281e5c0b1a41934b193fbb65c3a2c0f1e26ad922b91a` |
| Date | 2026-11-21 |
| Contents | 52 rules, 16 vocabulary terms; format check passes |
| Extraction prompt | `formal-rules`, sha256 `3e330fa2b145…` (draft by Opus 5.5, medium effort, $0.67) |
| Atomic judge prompt | sha256 `591c44868d53…` (a2, b2) |
| Aggregate judge prompt | sha256 `e96627bec01a…` (a3, b3) |
| Judge model | `anthropic/claude-opus-5-5`, medium effort; git commit `484bdd3` in all four judge runs |

| Step | Check | Findings (major / minor) | Cost |
|---|---|---|---|
| a0 | freeform | 33 (6 / 27) | — |
| a1 | format | 0 errors | — |
| a2 | atomic, 44 rules | 62 (7 / 55) | $1.01 |
| a3 | aggregate | 11 (5 / 6) | $0.55 |
| b0 | freeform | 7 (2 / 5) | — |
| b1 | format | 0 errors | — |
| b2 | atomic, 38 rules (`--previous a1_format.json`) | 57 (10 / 47) | $0.92 |
| b3 | aggregate | 11 (4 / 7) | $0.58 |
| c0 | final freeform | 3 (0 / 3) | — |

Severity: **Major** means the rule says something the handbook does not, misstates its strength, breaks the grammar, or conflicts with another rule. **Minor** covers citation, wording, vague-term and note issues.

---

## Major

None.

---

## Minor

**m1. SIDE-01's note no longer matches USER-02.** SIDE-01's note says "USER-02 restricts this for a LARGE VEHICLE (always pass on the left)". Since b3 S3-005, USER-02 has an exception: "…MUST pass on the left side, UNLESS the LARGE VEHICLE is signaling a left turn." A reader of SIDE-01 alone would miss that, for a large vehicle signalling a left turn, SIDE-01's second case (pass on the right if safe) applies again.
- Fix: change "(always pass on the left)" to "(pass it on the left, unless it is signaling a left turn)".
- Confidence: high.
- **Triage: fixed as proposed.** A note-only fix and a confident error (high confidence). SIDE-01's note now says "USER-02 restricts this for a LARGE VEHICLE (pass it on the left, unless it is signaling a left turn)."

**m2. Passing a large vehicle on the right when it signals a left turn: the swing-wide warning isn't linked.** With USER-02's new exception, passing on the right of a large vehicle signalling left is allowed where SIDE-01's second case holds ("the DRIVER ahead is turning left and the PASSER can safely pass on the right"). The handbook warns that such a vehicle may move the other way first:
- `13.10`: "…look at its turn signals before you start to pass. It may appear to be turning one direction but instead is swinging wide in the opposite direction in order to turn."

USER-01 carries this warning in its note, but USER-02's exception doesn't point to it. The rules stay correct, since SIDE-01's "safely" covers the risk, but the link would help a checker.
- Fix: add to USER-02's note: "13.10 warns that a LARGE VEHICLE may swing wide in the opposite direction to its turn (USER-01), which matters when passing it on the right."
- Confidence: medium.
- **Triage: ignored as too minor.** The fix is a note only, but the finding is medium confidence and itself says the rules are correct as they stand (SIDE-01's "safely" covers the risk), so it is not a confident error.

**m3. BEING-09's note gives the 13.44 ticket as the basis for its strength, but `penalty` is empty.** BEING-08 records "Failure to pull over may result in a ticket." BEING-09 (the intersection case) rests on the same duty, and its note says so, but its `penalty` is "". The prompt says to record a penalty "only when the handbook states one for this rule". 13.48 itself states none, so leaving it empty is defensible.
- Fix: either set BEING-09's penalty to "Failure to pull over may result in a ticket." (from 13.44), or leave it empty and add "13.48 states no penalty of its own." to the note.
- Confidence: low.
- **Triage: ignored as too minor.** Low confidence, and one of its fixes changes `penalty` rather than a note. Leaving the penalty empty is defensible, because 13.48 states none.

---

## Considered and not raised

- **BEING-01 and BEING-10:** BEING-01 keeps "allow the vehicle to pass and maintain speed" with no exception. BEING-10 carries lane position, with the motorcycle exception, and cites 13.41. Their notes link each other and BEING-05/06. The b2 S2-042 problem (the exception lifting the duty to allow the pass) is resolved. The split itself was confirmed at b3 S3-006.
- **BEING-08 and BEING-09:** the exception is now a fact only. The intersection duty has its own rule with an end point ("until every EMERGENCY VEHICLE has passed") and the handbook's trigger ("sees", from 13.48). The b0 M1 and b2 S2-055 problems are resolved.
- **USER-02 vs SIDE-02:** the b3 S3-005 deadlock for a large vehicle turning left is resolved by USER-02's exception, and both notes link the rules (see m1 for SIDE-01's).
- **EMERGENCY VEHICLE:** it is defined from 13.44 and used consistently in USER-16, BEING-08 and BEING-09. Notes that write "emergency vehicles" in lowercase are fine, because notes aren't bound by the grammar.
- **Settled decisions, not re-raised:**
  - SIDE-01's fourth case and MAY ONLY reading (a3 S3-008, b3 S3-004/S3-009)
  - USER-14's passing-only exceptions (a2 S2-048)
  - GEN-05's ADVICE strength (a2 S2-007, b3 S3-011)
  - PASSER vs DRIVER (a3 S3-011)
  - the lowercase verb "pass" (a0 V3)
  - general rules of the road out of scope (a3 S3-005/S3-006, b3 S3-001/S3-003)
  - the double-double-yellow barrier (a0 O4, b3 S3-002)
