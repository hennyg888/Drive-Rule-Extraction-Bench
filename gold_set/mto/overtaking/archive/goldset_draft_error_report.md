# Claude Opus 5.5 medium Goldset Draft Error Report

first extraction output: `extraction_outputs\anthropic\claude-opus-5.5\mto_2026_11_14.json`

corresponding run: `runs\20261114-214852-openrouter_claude-opus-5.5-mto-draft-gold`

All errors below were found in a manual Claude Code pass, before the check pipeline (`goldset_check_pipeline_plan.md`) existed. They were fixed in `gold_set\mto\overtaking\exp_errors_corrected.json`.

## Stage 1: format errors (script-detectable)

### 1. BLIND SPOT(S) used as a capitalized term but not defined in the vocabulary

*Detected by:* `error_check_pipelines\goldset\check_format.py` on `0_raw_rules.json` (report: `gold_set\mto\overtaking\0_raw_rules_format_report.txt`). This fix alone, with no stage 2 fixes, is applied in `gold_set\mto\overtaking\1_format_corrected.json`.

*Stage:* The missing vocab entry is mechanical (a caps term with no vocab entry), so a script can detect it. Writing the definition and removing the duplicate from the note were semantic fixes.

**Error:** `BLIND SPOT` and its plural `BLIND SPOTS` are written in caps in rule text, which marks them as defined terms. But the `vocabulary` section had no entry for them. The only definition was written inline in a rule's `note`.

**Where it appeared:**

| Rule | Field(s) | Text |
|---|---|---|
| `PASS-PROC-01` (Signal left and check before pulling out) | `action`, `statement` | "check the mirrors and BLIND SPOT" |
| `PASS-PROC-01` | `note` | "...BLIND SPOT is the area on each side of the vehicle that cannot be seen in the mirrors (4.24)." (inline definition instead of a vocab entry) |
| `PASS-USER-19` (Move over for stopped emergency vehicle or tow truck) | `action`, `statement` | "signalling and checking mirrors and BLIND SPOTS" |

**Affected sections:** `vocabulary` (missing entry); rules `PASS-PROC-01` and `PASS-USER-19`.

**Handbook source:** The MTO handbook does define the term, under "Find your blind spots" in `corpus\mto\getting-ready-drive.html`:
- `4.24.1`: "Check and adjust your mirrors and find your blind spots, the area on each side of your vehicle where you cannot see."
- `4.25.2`: "Blind spots in most vehicles are to the back left and back right of the vehicle."
- `4.25.8`: "Because your side mirrors show only narrow angles of view, turning your head to do shoulder checks is the only way to make sure there is nothing in your blind spots."

**Fix:**
1. Added a vocab entry, placed after `DRIVER`:
   ```json
   {
    "term": "BLIND SPOT",
    "definition": "The area on each side of a vehicle, in most vehicles to the back left and back right, where the driver cannot see, even with the mirrors; checking it means turning the head to look over the shoulder.",
    "evidence": ["4.24", "4.25"]
   }
   ```
2. Removed the inline definition from the `PASS-PROC-01` note. The term is now defined in the vocabulary, so the note doesn't repeat it. Note changed from "Blind-spot check drawn from the night-passing steps in 10.31; BLIND SPOT is the area on each side of the vehicle that cannot be seen in the mirrors (4.24)." to "Blind-spot check drawn from the night-passing steps in 10.31."
3. Rule text for `PASS-PROC-01` and `PASS-USER-19` is unchanged. `BLIND SPOTS` is the plural of the new term.

## Stage 2: atomic (semantic) errors

These pass every mechanical check. Each needs judgement about what the rule means.

### 2. Lowercase "not" after MUST made the negation ambiguous

**Error:** The action began with a lowercase "not" and was followed by a positive action, so "MUST not X and Y" could be read as forbidding both.

**Fix:** Reworded so the negation applies only to its own clause. Each rule stays as one rule with modal `MUST` (fields `action` and `statement`):

| Rule | Before | After |
|---|---|---|
| `PASS-PROC-07` (evidence 10.20) | "the PASSER MUST not race it and go back to the original lane" | "the PASSER MUST go back to the original lane instead of racing it" |
| `PASS-TOW-04` (evidence 27.47) | "MUST not brake, and carefully steer the vehicle and trailer back into position" | "MUST carefully steer the vehicle and trailer back into position without braking" |

`PASS-TOW-02`, `PASS-GEN-05` and `PASS-USER-05` also mix MUST and "not" in one action, but they read clearly, so they were left as is.

### 3. "passing lane" (lowercase) conflicted with the vocab term PASSING LANE

**Error:** In `PASS-PROC-01` (`when`, `statement`), "the passing lane" meant the lane the PASSER moves into. The vocab term PASSING LANE means a special passing/climbing lane, so the same words carried two meanings.

**Fix:** "about to move into the passing lane" → "about to move into the left lane to make the PASS".

### 4. Vocab terms written in lowercase

**Error / fix:** Two vocab terms were written in lowercase in rule text, so they didn't read as defined terms. Both were uppercased:

| Rule | Field(s) | Before → After |
|---|---|---|
| `PASS-BEING-02` | `when`, `statement` | "another driver is trying to pass" → "another DRIVER is trying to pass" |
| `PASS-MARK-02` | `when`, `statement`, `vague_terms[].term` | "enough broken line remains ahead" → "enough BROKEN LINE remains ahead" |

The verb "pass" stays lowercase throughout (about 45 uses). That matches the prompt's example, where only the noun PASS is in caps.

### 5. TOW TRUCK used as a key term but not defined or capitalized

**Error:** "tow truck" appeared in the same conditions and actions as the defined term EMERGENCY VEHICLE, but was neither capitalized nor in the vocabulary.

**Where:** `PASS-USER-18` (`when`, `statement`) and `PASS-USER-19` (`when`, `action`, `statement`).

**Fix:**
1. Uppercased to `TOW TRUCK` in those fields. Titles are left in lowercase, like "emergency vehicle".
2. Added a vocab entry after `EMERGENCY VEHICLE`. The handbook never defines the term (27.52 only mentions "a tow truck designed to tow vehicles"), so it is self-defined with empty evidence:
   ```json
   {"term": "TOW TRUCK", "definition": "A truck designed to tow disabled or damaged vehicles.", "evidence": []}
   ```


