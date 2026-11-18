# Atomic check (stage 2): gold_set\mto\overtaking\1_format_corrected.json

Judge: openrouter/claude-opus-5.5 · run folder: `runs\20261115-210151-check-atomic-1_format_corrected` (requests, responses, findings.jsonl, triage.csv) · 3 rules checked, 0 failed calls · $0.1818

**7 findings** (2 major, 5 minor) in 3 rules.

## PASS-PROC-01: Signal left and check before pulling out

> WHEN about to move into the passing lane, the PASSER MUST use the left-turn signal, check the mirrors and BLIND SPOT and check that the way is clear ahead and behind.

- **S2-001** [major, medium confidence] *overgeneralization* (action, statement, evidence, note): The duty to "check the mirrors and BLIND SPOT" is stated only in the night-passing steps (10.31, under 'Passing at night'). The rule applies it to every pass, while the general passing step (10.17) asks only for a signal and a check that the way is clear ahead and behind. The daytime obligation is not supported by the cited blocks. Evidence: 10.17, 10.28, 10.29, 10.31.
  - Fix: action: "use the left-turn signal and check that the way is clear ahead and behind"; statement: "WHEN about to move into the passing lane, the PASSER MUST use the left-turn signal and check that the way is clear ahead and behind."; evidence: ["10.17"]; note: "" (put the mirror and blind-spot check in a separate night-passing rule citing 10.29 and 10.31, with the condition 'passing at night')
- **S2-002** [minor, high confidence] *citation* (evidence): Block 4.24 only defines blind spots during vehicle setup and states no passing rule. It already backs the BLIND SPOT vocabulary entry, so it should not be cited as rule evidence. Evidence: 4.24.
  - Fix: evidence: ["10.17", "10.31"] (or ["10.17"] if the blind-spot check is moved to a night rule)
- **S2-003** [minor, low confidence] *citation* (evidence): Block 10.19, "Change lanes only after signalling", directly supports signalling before moving into the passing lane but is not cited. Evidence: 10.19.
  - Fix: evidence: ["10.17", "10.19"]

## PASS-PROC-07: Do not race a vehicle that speeds up

> WHEN the vehicle being passed speeds up, the PASSER MUST not race it and go back to the original lane.

- **S2-004** [major, high confidence] *grammar/modal* (modal, action, statement): The statement "the PASSER MUST not race it and go back to the original lane" puts a lowercase negation inside the action and joins a prohibition (do not race) with an obligation (go back) under one modal. It can be read as "MUST NOT (race it and go back)", which would forbid returning to the original lane, the opposite of block 10.20. The modal also does not match the rule's prohibitive part: the grammar requires MUST NOT. Evidence: 10.20.
  - Fix: Split into two rules. Rule A: modal "MUST NOT"; action "race it"; statement "WHEN the vehicle being passed speeds up, the PASSER MUST NOT race it." Rule B (new id, e.g. PASS-PROC-08): modal "MUST"; action "go back to the original lane"; statement "WHEN the vehicle being passed speeds up, the PASSER MUST go back to the original lane." Both keep force INSTRUCTION and evidence ["10.20"].

## PASS-USER-19: Move over for stopped emergency vehicle or tow truck

> WHEN approaching an EMERGENCY VEHICLE stopped with its red, or red and blue, lights flashing OR a tow truck stopped with its amber lights flashing AND the road has two or more lanes in the DRIVER's direction, the DRIVER MUST move into a lane away from the EMERGENCY VEHICLE or tow truck, well in advance, signalling and checking mirrors and BLIND SPOTS, UNLESS it is not safe to do so.

- **S2-005** [minor, medium confidence] *penalty* (penalty, note): The jail and escalating-fine penalty comes from 13.117, which covers failing to stop or clear the way for an emergency vehicle with flashing lights and sirens. The only penalty the shown sections tie directly to moving over is three demerit points (22.130, 'Failing to move, where possible, into another lane'). Whether 13.118's 'above law' carries 13.117's penalties over to the move-over duty is a reading the note does not mention. Evidence: 13.117, 13.118, 22.130.
  - Fix: note: "Diagram 2-57 shows a car moving over a lane away from a stopped ambulance. The three demerit points are listed for failing to move into another lane (22.130). The escalating fines and jail term are stated in 13.117 for failing to respond to an emergency vehicle and are applied here by reading 13.117-13.118 as covering the move-over duty."
- **S2-006** [minor, medium confidence] *vague terms* (vague_terms): The exception 'it is not safe to do so' leaves the driver to judge when moving over is unsafe, but it is not listed in vague_terms. Evidence: 13.109.
  - Fix: vague_terms: [{"term": "well in advance", "explanation": "no distance given"}, {"term": "it is not safe to do so", "explanation": "does not say what makes the lane change unsafe"}]
- **S2-007** [minor, low confidence] *citation* (evidence): The note relies on the caption 'Diagram 2-57' (13.106-c) to name the diagram, but the caption is not cited. The evidence list is also not in handbook order: the figure 13.106 comes before 13.109. Evidence: 13.106, 13.106-c.
  - Fix: evidence: ["13.106", "13.106-c", "13.109", "13.117", "13.118", "22.130"]
