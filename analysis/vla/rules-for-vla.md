# Using the passing rules with a driving VLA

michael's question (11 Oct): can the rules be a VLA's input context, so that it reasons over them, stays grounded in them and leaves a trace, much like RAG? And is rule language v1 a good rule and wording template for that, one that makes the VLA's decisions better and more reliable?

## Short answer

- **Keep v1 as the text the VLA reads.** Its modals (MUST vs SHOULD), condition clauses, exceptions, flags and per-line sources are the parts a VLA and a checker need. Nothing below changes the rule text.
- **On its own it is not enough.** Rules in the prompt change what a model says more reliably than what it does. DriveBench found that VLMs often answer from general knowledge or textual cues rather than the image. A rule the model cites can still be ignored by its trajectory, and Alpamayo-R1 added an RL stage to make its actions agree with its reasoning.
- **What's missing is a grounding layer beside each rule.** It writes the conditions as predicates from one shared scene vocabulary. It records what the rule acts on (motion, signals or attention). For legal duties it adds a check that runs outside the model. v1 already defines a TAGS field for situations, but `passing-rules.v1.json` doesn't fill it yet.
- **With that layer, one rule ID links the prompt, the checker and the training data,** and every decision traces back to a handbook sentence.

## 1. Three places rules can enter

| Where | What happens | What it buys | What it needs from the format |
|---|---|---|---|
| Context (the RAG part) | The rules active in this scene go into the prompt. The VLA cites rule IDs and the facts it relied on. | Explanations, and a record of which rules the model saw | Stable IDs, tags for choosing rules, short rule cards |
| Checker outside the model | Legal duties are evaluated on the planned trajectory. A violation rejects the plan or triggers a fallback. | Reliability that doesn't depend on the model obeying its prompt | Conditions as predicates, a measurable requirement, a priority order |
| Training | Traces of the form "facts → rules → decision" are generated automatically for SFT. RL rewards rule margins and correct citations. | The model learns to use the rules, not only to quote them | All of the above |

Context alone covers only the first row. The closest published system is DriveReg (Cai et al., "Driving with Regulation"):

- It retrieves regulation text, including the Massachusetts driver's manual, by embedding similarity to a scene summary that the VLM writes.
- Like our LEGAL/ADVISORY split, it separates mandatory rules from safety guidelines.
- An LLM judges a fixed set of candidate actions. There's no check on trajectories and no training step.
- It was evaluated on 76 hypothetical scenario–action pairs and 35 nuScenes samples, and takes 0.67–2 s per decision.

## 2. One loop: perceive, match, decide, check, trace

1. **Perceive.** The VLA, or a perception stack, first writes the scene as facts in the rule vocabulary: `cyclist(c1)`, `lateral_gap(ego, c1) = 1.4 m`, `left_marking = broken`, `weather = fog`.
2. **Match.** A small rule engine picks the rules whose tags and conditions hold, applies EXCEPTION TO and SPECIALIZES, and orders them. This step is deterministic and logged, so a trace can show why each rule was active.
3. **Decide.** The VLA gets the facts and the active rules, and outputs a meta-action and a trajectory with the IDs of the rules it relied on.
4. **Check.** The checker evaluates the legal duties on the trajectory and reports a margin (for 3.4.4b, the lateral gap minus 1 m). SHOULD rules become costs, not vetoes.
5. **Trace.** Each decision logs facts → rule IDs → handbook passages and figures (the m-ids are already in the JSON) → check results.

With this loop, every error has an owner:

- wrong facts point to perception;
- wrong active rules point to matching;
- right rules but a wrong action point to the policy;
- no rule at all points to a gap in the handbook.

**On RAG for this rule set.** All 88 statements come to about 12k characters, roughly 3k tokens, so the whole passing rule set fits in the prompt as a fixed, cacheable prefix. Retrieval then decides which rules are active, not which text fits.

- Key retrieval on scene facts (tags and predicates), not on text similarity. That's what makes step 2 auditable.
- The same keys scale to the full handbook (the census counted 3,444 sentences).
- Keep the part that changes per frame small: the facts and the IDs of the active rules.

## 3. What v1 already gives, and what it lacks

First-pass audit of `passing-rules.v1.json`. The per-statement labels are in `vla-audit.csv`, labelled by hand. Its columns:

- `acts_on`: motion, mixed, signals, attention, or another road user;
- `applies_to`: who the statement binds;
- `conditions_from`: users, road, judgment, ego, intent, weather/light;
- `distance`: the distance the statement gives, if any;
- `checkable`: legal duties only.

- **Statement types.** There are 88 statements: 73 rules and procedures, 13 FACT or DEFINE, and 2 EXCEPTION statements that switch another rule off.
- **Force.** Of the 73, **19 are legal** (8 MUST, 7 MUST NOT, 4 MAY) and **54 are advisory**. For a VLA, most of the passing chapter is a preference, not a constraint.
- **Checkable duties.** The legal ones include **15 duties** (MUST or MUST NOT). Once their facts are grounded, 10 can be checked on a planned trajectory. Two of those apply only to trucks, and 3.4.4b needs a stated default for "where practical". The other 5 can't be checked yet:
  - 3 rest on a judgment term: "with caution", "if safe to do so" and "slow traffic" (3.4.13a, 3.4.13b, 3.6.1d);
  - 2 rest on another driver's intention: "trying to pass" and "to prevent another vehicle from passing" (3.6.1b, 3.6.1c).
- **What they act on.**
  - 62 constrain the vehicle's motion only.
  - 5 mix motion with signals or attention.
  - 3 are about beams or the horn.
  - 2 are attention duties: watching for opening doors (3.4.1a) and anticipating an LCV's length (3.4.6e).
  - 1 is a cyclist's right (3.4.4a). It helps predict the cyclist; it doesn't constrain ego.
- **Who they apply to.** Six apply only when ego is towing a trailer (4) or is a truck (2).
- **Where the facts come from.** This counts statements, and one statement can draw on several sources:
  - other road users: 54;
  - the road (map, markings, signs): 29;
  - a judgment term: 29;
  - ego's own plan or vehicle: 13;
  - another road user's intention: 9;
  - weather or light: 6.
- **Distances.** Only 6 statements give one: 1 m, 2 m, 20 m, 30 m (twice) and 60 m.

**Keep:**
- MUST vs SHOULD as hard constraint vs cost. DriveReg makes the same cut at runtime; v1 fixes it at extraction and records why in FORCE FROM.
- WHEN, WHILE, UNTIL, ONLY IF and UNLESS, which say when a rule switches on and for how long.
- EXCEPTION TO and SPECIALIZES, which already give the rules a defeasible structure.
- Sources on every statement and every step. The handbook end of the trace is already done.
- The flags, which list exactly the places that need grounding.

**Add, beside the text (as a `ground` object in the JSON):**

| Field | Why | For 3.4.4b |
|---|---|---|
| `uid` | IDs follow section numbers. Logs and training data need IDs that survive renumbering. | `ON-PASS-CYCLIST-1M` (shown as 3.4.4b) |
| `tags` | v1 §5 defines TAGS. Filling them gives the retrieval keys. | other road user: cyclist; phase: passing |
| `when` | Conditions as predicates from one shared vocabulary. This formalizes v1's "one phrase per concept", in the spirit of Logical English's predicate library. | `passing(ego, c) AND cyclist(c)` |
| `require` | A measurable form of the duty, for the checkable ones | `lateral_gap(ego, c) >= 1.0 m` for the whole pass |
| `acts_on` | The handbook is written for people. Each duty maps to motion, a vehicle signal, a perception precondition or a prediction. | trajectory, lateral |
| `observe` | Where each fact comes from: camera, map, ego, V2X, or not observable | cyclist: camera; gap: camera or lidar |
| `judgment` | For each J term, either a default with its source, or "the model decides and states the value it used". It is kept out of the rule text, so v1's "thresholds are never invented" still holds. | "where practical": treated as never applying until we define when it does |
| `scope` | Jurisdiction, vehicle and road type, so a model trained elsewhere doesn't bring its own rules (which side to pass on, school buses) | Ontario; motor vehicles |
| `priority` | v1 has force per rule and "the more specific wins", but no order across rules (§9: no priority keyword). A checker needs one, for example avoid collision > legal > advisory > progress, as in Rulebooks and ScenicRules. | legal tier |

None of this reverses the decision in `rule-template-plan.md` to stay off the TR2MTL route. The text remains the representation, and the predicates are its vocabulary. A temporal-logic form is compiled only for the 10 checkable duties, and only for the checker.

## 4. One rule end to end: 3.4.4b

The rule text, unchanged (sources m56 and m57, SEE Diagram 2-11):

```
a driver of a motor vehicle MUST keep at least 1 m between the vehicle and a cyclist
  WHILE passing the cyclist, [?where practical]
  IF VIOLATED a fine AND 2 demerit points
```

The grounding layer:

```yaml
uid: ON-PASS-CYCLIST-1M
tags: {other_road_user: cyclist, phase: passing}
when: passing(ego, c) AND cyclist(c)
require: lateral_gap(ego, c) >= 1.0 m          # for the whole pass
judgment: {"where practical": never}           # our default, not the handbook's
acts_on: trajectory.lateral
observe: {cyclist: camera, passing: ego plan + tracking, lateral_gap: camera or lidar}
check: always(passing(ego, c) -> lateral_gap(ego, c) >= 1.0)
margin: min(lateral_gap during the pass) - 1.0 m
```

What the VLA reads (the v1 text of the active rules, excerpt):

```
[3.4.4b] a driver of a motor vehicle MUST keep at least 1 m between the vehicle and a cyclist WHILE passing the cyclist
[3.4.4c] a driver SHOULD change lanes to pass a cyclist WHEN [?possible]
[3.1.6a] a driver MAY pass WHEN there is a broken line at the left of the driver's lane
         ONLY IF the way is clear AND there are [?enough] broken lines ahead to complete the pass [?safely]
```

What it writes back:

```
facts:   cyclist c1 ahead in ego lane, 18 m, 5 m/s; left marking broken; oncoming lane clear for 250 m
rules:   3.4.4b, 3.4.4c, 3.1.6a
action:  pass c1 in the oncoming lane; planned minimum lateral gap 1.8 m
```

- **Check.** 3.4.4b passes with a margin of +0.8 m. For 3.1.6a the checker can report how much broken line lies ahead, but "enough" is a J term, so the VLA has to state the distance it assumed.
- **Trace.** The action leads to 3.4.4b, then to "Sharing the road › Cyclists ¶3" (m56, m57) and Diagram 2-11.

Two other kinds of rule come out differently:

- **A judgment rule.** 2.1a is "SHOULD start a lane change or a pass ONLY IF the driver has [?enough] space and time to complete it [?safely]". It becomes `oncoming_gap_time >= t_pass(v_ego, v_lead) + t_margin`. Either we set `t_pass` and `t_margin` and cite where they come from, or the VLA chooses them and writes them in its output.
- **A human routine.** 2.2a step 1 is "signal left AND check that the way is clear ahead and behind". It becomes `indicator: left`, which applies only if the stack drives the indicators, plus a precondition `clear(ahead) AND clear(rear_left_lane)` on the lane change. For an AV, "check" is a perception duty, not an action.

## 5. How to tell whether the format helps

Use the same model and the same scenes, and change only what the model gets:

| Setting | What the VLA gets |
|---|---|
| A0 | No rules |
| A1 | Retrieved handbook passages (DriveReg-style) |
| A2 | v1 rule text |
| A3 | v1 plus the grounding layer: the active rules and the grounded facts |
| A4 | A3 plus the checker |
| A5 | A3, fine-tuned on rule-cited traces with rule-margin rewards |

- **A1 vs A2** is the downstream test already planned in `rule-template-plan.md` §6 (original text vs our rules), moved from quiz questions to driving scenes.
- **A2 vs A3** tests grounding.
- **A4 and A5** test reliability.

**Measures:**
- legal-duty violations and their margins;
- closed-loop driving score;
- decision accuracy on rule cases;
- citation precision and recall against the rules the engine found active;
- whether the action agrees with the rules the model cited;
- flip rate on counterfactual pairs;
- latency.

**Test sets:**
- **Counterfactual pairs built from the predicates.** For each rule, make two scenes that differ only in its trigger: fog vs clear, solid vs broken line, school-bus lights on vs off, inside vs outside 30 m of a crossover. The decision should change when, and only when, the trigger changes. This is the test that catches a model answering from priors.
- **Closed loop.** Use Bench2Drive (CARLA; 44 scenarios and 220 evaluation routes; its Overtaking and Give_Way groups). Add the Ontario cases it lacks: school bus, streetcar, crossover, and the 1 m cyclist rule.
- **Conflicts.** Use scenes where two rules disagree. For example, 3.4.13b (MUST move into a lane away from a stopped tow truck) against 3.2.2c (SHOULD drive in the right-hand lane). ScenicRules evaluates driving policies against prioritized rules of this kind.

If A2 scores about the same as A1, the format's value lies with people and traceability rather than with the model. That's worth knowing early.

## 6. Next steps

1. Write the scene vocabulary (draft below) and fill TAGS for the 88 statements.
2. Add the grounding layer to the 15 legal duties, with checks for the 10 checkable ones. Record a default, or "the model decides", for every J term in a register kept next to the vagueness flags.
3. Build the counterfactual pairs and run A0–A3 on single frames with an off-the-shelf VLM before any closed-loop work. It's cheap, and it answers "does the format help" first.

## Appendix: draft scene vocabulary from the 88 statements

- **Road and control.** Pedestrian crossover, crosswalk, bridge, viaduct, tunnel, hill crest, curve, centreline, left marking (solid or broken), two-way left-turn lane, shoulder (side, paved). Passing or climbing lane. Signs: lane ending; "do not pass"; "keep right except to pass"; "slower traffic keep right"; far-left lane closed to trucks. Road type (freeway, multi-lane, one-way, undivided, median). Lanes in ego's direction, speed limit, streetcar passenger area.
- **Road users.** Car, large vehicle, LCV, truck, bus, motorcycle, limited-speed motorcycle, moped, cyclist, streetcar, school bus, emergency vehicle, tow truck, farm machinery, horse-drawn vehicle, snow plow, pilot or pace vehicle, parked vehicle, pedestrian.
- **Their state.** Stopped, slow-moving, lights flashing (upper red alternating, red, red and blue, amber), doors opening, passengers getting on or off, carrying a "do not pass" sign, staggered (snow plows).
- **Relations.** Ahead, behind, alongside, in lane, distance, lateral gap, speed, slower than the limit, approaching from the front or from behind, the passed vehicle's front now behind ego.
- **Intentions (predicted).** Wants to pass, trying to pass, turning left, has moved right, holding up traffic.
- **Environment.** Night, fog, blowing snow or whiteout, view obstructed, clear distance ahead.
- **Ego.** Towing a trailer, is a truck, plan (pass, lane change, turn left, keep lane, stop).
- **Outputs.**
  - Meta-actions: keep lane, pass on the left or right, change lanes, return to lane, slow down, stop, wait, move right within the lane, pull over.
  - Trajectory bounds: lateral and longitudinal gaps, speed not increasing.
  - Vehicle signals: indicator, low or high beams, horn.

## Sources

- Censi et al., *Liability, Ethics, and Culture-Aware Behavior Specification using Rulebooks*, ICRA 2019. [arXiv 1902.09355](https://arxiv.org/abs/1902.09355)
- Cai et al., *Driving with Regulation: Trustworthy and Interpretable Decision-Making for Autonomous Driving with Retrieval-Augmented Reasoning* (DriveReg). [arXiv 2410.04759](https://arxiv.org/abs/2410.04759); [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/41168)
- Xie et al., *Are VLMs Ready for Autonomous Driving? An Empirical Study from the Reliability, Data, and Metric Perspectives* (DriveBench), ICCV 2025. [arXiv 2501.04003](https://arxiv.org/abs/2501.04003)
- NVIDIA, *Alpamayo-R1: Bridging Reasoning and Action Prediction for Generalizable Autonomous Driving in the Long Tail*. [arXiv 2511.00088](https://arxiv.org/abs/2511.00088)
- Chang et al., *ScenicRules: An Autonomous Driving Benchmark with Multi-Objective Specifications and Abstract Scenarios*. [arXiv 2602.16073](https://arxiv.org/abs/2602.16073)
- Bench2Drive. [github.com/Thinklab-SJTU/Bench2Drive](https://github.com/Thinklab-SJTU/Bench2Drive)
- Manas et al., *TR2MTL: LLM based framework for Metric Temporal Logic Formalization of Traffic Rules*, IV 2024. [arXiv 2406.05709](https://arxiv.org/abs/2406.05709)
- Maierhofer et al., *Formalization of Interstate Traffic Rules in Temporal Logic*, IV 2020. [TUM](https://portal.fis.tum.de/en/publications/formalization-of-interstate-traffic-rules-in-temporal-logic/)
- In the Paper folder:
  - Sartor et al., *Mind the Gaps* (ICLP 2024) assumes sensor readings arrive as correct facts and leaves the link to machine learning for future work, which is the gap a VLA fills.
  - Goossens et al., *The Rulebook Flywheel* (IV Workshops 2026) uses rulebooks for automated evaluation and continuous improvement, the loop in §2 and §5.
