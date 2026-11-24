# Freeform error check: `gold_set/ca/overtaking/a3_aggregate.json`

Source: `corpus/ca` · Prompt: `prompts/formal-rules` (system.md, task.md, schema.json) · Topic: overtaking · Round b, stage 0

Quotations from the handbook are given as `id`: "text", and some are trimmed with "…".

**What was checked**

- The format check (`check_format.py a3_aggregate.json --handbook ca --allow-lowercase pass`) passes with no errors. Also checked: no condition mixes AND and OR outside the accepted lowercase pattern, and no lowercase modal appears in an action.
- Each of the 50 rules was read against its cited blocks and their neighbours. Extra attention went to the rules added or changed in round a: LOC-07, BEING-08, USER-18 to USER-21, SIDE-01, USER-04, BEING-02 and USER-07.
- The two sign figures were viewed: 12.89 (regulatory signs; it has the DO NOT PASS sign cited by LOC-07) and 12.90 (warning signs; no passing sign, but a "Crossroad" sign).
- Findings were weighed only against the CA triage decisions in `a0_freeform_report.md`, `a2_atomic_report.md` and `a3_aggregate_report.md`. Nothing settled there is raised again. That includes:
  - the lowercase verb "pass" (a0 V3);
  - positive-first, negated-last MUST actions (a0 M4);
  - PASSER as an actor, and PASSER vs DRIVER (a3 S3-011);
  - the USER-13 condition (a0 K2, a2 S2-046);
  - the cited lane-change checks on PROC-01 (a0 C5);
  - scope: general rules of the road stay out (a3 S3-005, S3-006), while the emergency vehicle and the school bus are in (a3 S3-002, S3-003).
- I also checked whether conventions decided in round a are applied everywhere: list lead-ins cited (a0 C2), "approaching" listed as vague (a0 Q1, a2 S2-003), and notes linking related rules (a0 N1).

**Result:** 50 rules and 15 vocabulary terms. **2 major and 5 minor findings.** Both majors involve rules added or changed in round a, or a pair of rules that read against each other. No major errors remain in the rules that came through round a unchanged.

**Triage:** all 7 findings were triaged. The majors were fixed as the reviewer decided, and the minors against earlier CA triages. Fixes were applied to `b0_freeform.json`, which started as an exact copy of `a3_aggregate.json`. Each decision is recorded under its finding as a **Triage** line.
- One rule was added at the end of the BEING group, so no rules were renumbered: PASS-BEING-09 (M1).
- After the fixes there are 51 rules and 15 vocabulary terms.
- Format check (`check_format.py b0_freeform.json --handbook ca --allow-lowercase pass`): no format errors.

Severity: **Major** means the rule says something the handbook does not, misstates its strength, breaks the grammar, or conflicts with another rule. **Minor** covers citation, wording, vague-term and note issues.

---

## Major

### M1. An exception carries a duty with no modal (PASS-BEING-08)
"…the DRIVER MUST drive to the right edge of the road and stop until the emergency vehicle has passed, UNLESS the DRIVER is in an INTERSECTION, **in which case the DRIVER continues through it and then drives to the right as soon as it is safe and stops**."

The grammar makes an EXCEPTION a set of FACTs. Here the exception holds a second set of duties (continue through, drive right, stop) that falls under no modal. This is the same kind of problem as a0 M3 (a second duty smuggled into a rule). A program reading the rule gets only "does not apply in an intersection", so what to do in the intersection is lost.
- `13.48`: "If you are in an intersection when you see an emergency vehicle, continue through the intersection. Drive to the right as soon as it is safe and stop."
- Fix: cut the exception down to the fact, "UNLESS the DRIVER is in an INTERSECTION", and drop "as soon as it is safe" from BEING-08's vague terms. Add **PASS-BEING-09**, "Emergency vehicle while in an intersection": REQUIREMENT / MUST, actor DRIVER, "WHEN the DRIVER is in an INTERSECTION AND an emergency vehicle using a siren and red lights approaches, the DRIVER MUST continue through the INTERSECTION, then drive to the right as soon as it is safe and stop." Vague term "as soon as it is safe" (no criteria given). Evidence `13.44`, `13.48`. Note: "REQUIREMENT because 13.44 makes giving the right-of-way to an emergency vehicle a duty with a ticket for failing to pull over; 13.48 gives what to do in an intersection." Add a note to BEING-08 pointing to BEING-09.
- Confidence: high.
- **Triage: fixed as proposed.** BEING-08's exception is now "UNLESS the DRIVER is in an INTERSECTION", and its note points to BEING-09. "as soon as it is safe" left its vague terms, and "approaches" was added (m4). New **PASS-BEING-09**, "Emergency vehicle while in an intersection": REQUIREMENT / MUST, "WHEN the DRIVER is in an INTERSECTION AND an emergency vehicle using a siren and red lights approaches, the DRIVER MUST continue through the INTERSECTION, then drive to the right as soon as it is safe and stop.", vague terms "approaches" and "as soon as it is safe", evidence `13.44`, `13.48`, and the proposed note.

### M2. "Maintain your lane position" conflicts with "move to one side of your lane" (PASS-BEING-01, PASS-BEING-06)
- BEING-01: "WHEN another vehicle is passing the DRIVER OR signals that it plans to pass the DRIVER, the DRIVER MUST allow the vehicle to pass and **maintain lane position** and speed."
- BEING-06: "WHEN a MOTORCYCLIST is passing the DRIVER's vehicle AND it is possible, the DRIVER MUST **move to one side of the DRIVER's own lane** to give the MOTORCYCLIST more room to pass."

When a motorcycle passes, the first rule requires holding lane position and the second requires changing it. Both rest on the handbook:
- `10.206`: "If a vehicle is passing you or signals that they plan on passing, allow the vehicle to pass. Maintain your lane position and your speed."
- `13.41`: "When possible, move to one side of your lane to give motorcyclists more room to pass."

Neither rule mentions the other. BEING-05 also sits beside BEING-01: a tailgater who signals to pass falls under both "maintain lane position" (BEING-01) and "merge right into another lane" (BEING-05). There the order is clear ("Maintain your course and speed. Then, when safe…", 15.14), but no note links the two rules.
- Fix: add to BEING-01 "UNLESS the passing vehicle is a motorcycle and it is possible to move to one side of the lane", with the note: "For a passing motorcycle, BEING-06 applies (13.41). BEING-05 covers a tailgater: keep course and speed, then merge right when safe." Add to BEING-06's note: "An exception to BEING-01's 'maintain lane position'." If you'd rather not change BEING-01's statement, link the two rules with notes only, as a0 N1 did for SIDE-01. That records the conflict but does not resolve it.
- Confidence: medium.
- **Triage: fixed as proposed, by adding UNLESS.** BEING-01 now ends "…, UNLESS the passing vehicle is a motorcycle and it is possible to move to one side of the lane." It has the vague term "it is possible" (as in BEING-06) and the proposed note, which links BEING-06 and BEING-05. BEING-06's note adds "An exception to BEING-01's 'maintain lane position'."

---

## Minor

**m1. USER-04 and USER-20 overlap for a school bus stopped at a traffic light.** USER-04 lets the DRIVER pass "a bus … stopped at a SAFETY ZONE or traffic light" at no more than 10 mph. USER-20 requires stopping for a school bus flashing its red lights. A school bus is a bus, so a school bus stopped at a light with its red lights flashing falls under both rules. The handbook places 13.19 under "Buses, Streetcars, Trolleys" and 13.158 under "Around Children", so the conflict is between the two rules, not in the handbook.
- Fix: add to USER-04's note: "Does not apply to a school bus flashing its red lights; USER-20 requires stopping." Add the matching link to USER-20.
- Confidence: medium.
- **Triage: fixed as proposed.** USER-04's note adds "Does not apply to a school bus flashing its red lights; USER-20 requires stopping.", and USER-20's note links back (as for related rules at a0 N1).

**m2. LOC-07 cites a sentence about red-and-white signs.** `12.67` ("Follow the sign's instruction. For example, DO NOT ENTER means…") sits under the heading "Red and White Regulatory Sign" (12.65). The DO NOT PASS sign in 12.89 is one of the "White Regulatory Signs", which `12.85` covers. LOC-07's force rests on 12.85 and the figure.
- Fix: evidence `["12.85", "12.89"]`.
- Confidence: medium.
- **Triage: fixed as proposed.** LOC-07's evidence is now `12.85`, `12.89` (a cited block that does not support the rule is removed, as at a2 S2-042).

**m3. USER-20 cites list items without the line that introduces them.** `13.158` and `13.159` are items in the list introduced by `13.153` ("…When near schools, look for:"). The a0 C2 convention cites the lead-in with every list item.
- Fix: add `13.153` to USER-20's evidence, before 13.158.
- Confidence: high.
- **Triage: fixed as proposed.** USER-20's evidence is now `13.151`, `13.152`, `13.153`, `13.158`, `13.159` (a0 C2: cite the list lead-in).

**m4. "approaching" is listed as vague in two rules but not in four others.** a0 Q1 (LOC-01) and a2 S2-003 (GEN-01) listed "approaching" as vague because no distance is given. The same word is unlisted in:
- USER-10 ("approaching or passing a BICYCLIST")
- USER-16 ("approaching a stationary emergency vehicle")
- USER-18 ("approaching or passing a SAFETY ZONE")
- BEING-08 ("an emergency vehicle … approaches")

Fix: add `{"term": "approaching", "explanation": "no distance given"}` to USER-10, USER-16 and USER-18, and `{"term": "approaches", "explanation": "no distance given"}` to BEING-08.
- Confidence: medium.
- **Triage: fixed as proposed.** "approaching" (no distance given) was added to USER-10, USER-16 and USER-18, and "approaches" to BEING-08 (and to the new BEING-09), as at a0 Q1 and a2 S2-003.

**m5. The Crossroad warning sign is not cited on LOC-03 (optional).** Figure `12.90` shows the "Crossroad" warning sign, which helps the driving model recognise where LOC-03 ("WHEN at crossroads or driveways, the PASSER MUST NOT pass") applies. The prompt says to cite a figure when its image supports the rule.
- Fix: add `12.90` to LOC-03's evidence, with the note "Figure 12.90 includes the Crossroad warning sign."
- Confidence: low.
- **Triage: ignored.** Low confidence and optional, and LOC-03's meaning is already clear without the figure. a2 rejected low-confidence findings of this kind (S2-015, S2-027).

---

## Considered and not raised

- **New rules from a3 checked and found sound:** LOC-07, USER-18, USER-20 (apart from m1 and m3) and USER-21. Each matches its handbook wording, strength and penalty.
- **SIDE-01's fourth case**, "overtaking a LIGHT RAIL VEHICLE": with MAY ONLY it only widens when passing on the right is allowed. USER-05 still covers the exceptions where the left side is allowed (tracks too close, one-way street, officer's direction). No conflict.
- **The SLOWER TRAFFIC KEEP RIGHT and KEEP RIGHT signs in 12.89:** general lane use, out of scope by a3 S3-006.
- **BEING-02 vs BEING-03:** settled at a3 S3-009 with notes on both rules.
- **USER-09, USER-19 and USER-07 overlap:** settled at a2 S2-036 and a3 S3-010.
