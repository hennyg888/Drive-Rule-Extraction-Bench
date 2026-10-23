# Passing (overtaking): content structure of the MTO Driver's Handbook

Step 1 of the rule-extraction project. Source: `mto_drivers_handbook/changing-positions.html` (ontario.ca, updated March 31, 2026). I also skimmed `changing-directions.html`, `stopping.html` and `freeway-driving.html` to see whether the pattern holds elsewhere.

No formal rules yet. This file only covers how the handbook organises what it says.

---

## 1. The hypothesis, tested

Your hypothesis: **definition → general concept + normal procedure → restrictions/cautions → special conditions (each with its own condition, cautions, procedure, can/can't)**.

**Verdict: the overall order holds, and the handbook says so itself.** The page's Summary lists exactly two learning goals:

> - The safety considerations and the sequence of steps to follow when changing lanes or passing
> - How to deal with specific situations when passing (for example, at night, streetcars)

So the editors do think in terms of a "general" part and a "specific situations" part. Three refinements are needed, though:

1. **Passing is a sub-type of lane change, not a standalone topic.** The definition is literally "Passing is changing lanes to move past a slower vehicle." Passing inherits the lane-change steps (mirror, blind spot, signal) and adds its own. The structure is a hierarchy, not a flat list.
2. **The "restrictions and cautions" block is not one kind of thing.** It mixes at least five different kinds of statement, and some of them are about the driver being passed, not the one passing (see §3).
3. **Special-condition sections don't share one shape.** "Passing at night" is a modified procedure; "Passing on the shoulder" is a pure can/can't rule; "Passing and climbing lanes" mostly describes road infrastructure. Each special section fills only some of the slots (see §4).

---

## 2. Proposed structure (draft v0)

### Page level (holds for all four pages I checked)

```
Chapter (e.g. "Changing positions")
├── Chapter intro: scope + overarching principle
│     "Before beginning, be sure you have enough space and time to complete the move safely."
├── Manoeuvre section(s)        ← may nest: Changing lanes ⊃ Passing
│   ├── [general part]
│   └── [special-situation sections]
└── Summary: learning objectives ("By the end of this section, you should know…")
```

### Manoeuvre level (the template to fill per manoeuvre)

| Slot | What it holds | Typical wording |
|---|---|---|
| **A. Definition** | What the manoeuvre is; its parent manoeuvre | "X is …" |
| **B. Purpose / context** | Why or when you'd do it, typical examples | "You may want to …", "For example …" |
| **C. Governing principle** | The overarching safety gate | "Never … unless you are sure …", "If in doubt, …" |
| **D. Absolute prohibitions** | Unconditional "never" | "Don't … under any conditions" |
| **E. Normal procedure** | Ordered steps | "Here are the steps for …" (bulleted list) |
| **F. Constraints & cautions** | Split by **actor** and **context dimension** (§3) | "not permitted", "watch for", "do not" |
| **G. Special situations** | Each is a sub-unit that reuses A–F *selectively* (§4) | H2 subsections |
| **H. Illustration** | Diagram reference | "Diagram 2-46" |

### Language strength (worth tagging now, it'll matter later)

The handbook uses a fairly consistent ladder of strength:

| Level | Markers in the passing text |
|---|---|
| Legal obligation / prohibition | "must", "is not permitted", "It is unlawful" |
| Strong directive | "Never", "Don't", "Do not" |
| Permission | "You may", "only if" |
| Advice / caution | "Be careful", "watch for", "Be prepared to", "Avoid" |
| Default / heuristic | "If in doubt, do not pass", "Most passing is done on the left" |

---

## 3. The general part of Passing, slotted

**A. Definition**
- "Passing is changing lanes to move past a slower vehicle." *(parent: Changing lanes)*

**B. Purpose / context**
- Not all vehicles travel at the same speed. Cyclists, road service vehicles and drivers preparing to turn are usually slower. "You may want to pass some slow-moving vehicles when you are following them."

**C. Governing principle**
- "Never overtake and pass another vehicle unless you are sure you can do so without danger to yourself or others."
- "If in doubt, do not pass."

**D. Absolute prohibition**
- "Don't pass moving snow plows under any conditions."

**E. Normal procedure** (4 steps; the inherited lane-change steps are in brackets)
0. *[inherited from Changing lanes: check mirrors, check blind spot, signal, check again, steer gradually, keep speed]*
1. Left-turn signal; check the way is clear ahead and behind; move into the passing lane.
2. Watch for hidden bicycles or small vehicles ahead of the target, vehicles turning left in front, and vehicles or pedestrians entering from roads or driveways.
3. Change lanes only after signalling. After overtaking, signal; return when **the entire front of the passed vehicle is visible in the inside mirror**. Don't cut off.
4. If the passed vehicle speeds up, don't race; go back to your original lane.
   - ⚠ Same bullet, different actor: "do not speed up when another driver is trying to pass you. It is unlawful." This is a rule for the driver being passed, sitting inside the passer's procedure.

**F. Constraints & cautions.** Your quoted paragraph splits into these kinds:

| # | Kind | Actor | Context dimension | Text (condensed) | Strength |
|---|---|---|---|---|---|
| F1 | Location prohibition | passer | location (quantified) | No passing within **30 m of a pedestrian crossover** | legal |
| F2 | Location prohibition | passer | location + manoeuvre type | No passing **left of centreline** within **30 m of a bridge, viaduct or tunnel** | legal |
| F3 | Visibility prohibition | passer | geometry + condition | Don't pass approaching a **hill crest or curve** *when* oncoming view is obstructed *and* clear distance is insufficient | directive (conditional) |
| F4 | Hazard caution | passer | target = parked vehicle | Watch for opening doors / loading | advice |
| F5 | Target-specific constraint | passer | target = motorcycle, bicycle, LSM, moped | Their lateral position isn't an invitation to pass **in the same lane**; pass by **changing lanes** | directive |
| F6 | Yield duty | **passed** | — | When faster traffic wants to pass, move right | directive |
| F7 | Yield duty + caution | **passed** | road = undivided, passer in opposite lane | Watch oncoming traffic, move right within lane, be ready to slow down | advice |
| F8 | Road-type rule | **passed** (by a truck) | road = high-speed, ≥3 lanes each way | Trucks are barred from far-left lane, so the next lane is the truck passing lane; move right when a truck wants to pass | directive (+ background fact) |

Observations:
- **F1–F5 are "when can't I pass / what to watch for".** F1–F3 are about *where*, F4–F5 about *whom*.
- **F6–F8 are "how to be passed".** That's arguably its own sub-topic and could be split out.
- F3 has **compound conditions** (hill/curve AND obstructed view AND insufficient distance). Easy to over-simplify into "never pass on hills".
- F8 embeds a **background fact** (trucks barred from the far-left lane) that's needed to understand the rule but isn't itself about passing.

---

## 4. Special situations, slotted

✓ = slot present, – = absent

| Section | Trigger condition | Modified procedure | Can / can't | Cautions | Mostly… |
|---|---|---|---|---|---|
| **Passing at night** | night | ✓ 3 steps (low beams approaching → high beams alongside → return when front visible in mirror, signal) | – | "Be very careful" | **procedure variant** |
| **Passing and climbing lanes** | road has a passing or climbing lane | – | implicit: slower vehicles go right, faster pass left | merge when lane ends | **infrastructure + signage description** |
| **Passing on the shoulder** | target turning left | – | ✓ MAY use right shoulder **only if** target is turning left **and** shoulder is paved; MAY NOT use left shoulder (paved or not) | – | **pure permission rule** |
| **Passing on the right** | — | – | ✓ default is left; MAY pass right on multi-lane or one-way roads, or when overtaking a streetcar or left-turning vehicle | ✓ more dangerous; don't suddenly switch, wait for the slower vehicle to move right | **exception to a default** |
| **Passing streetcars** | target = streetcar | – | ✓ MUST pass on right unless one-way road; MUST stop ≥ 2 m behind rear doors at stops; exception: stops with a passenger area set aside | ✓ reasonable speed; expect sudden pedestrian moves | **obligation + exception** |

Observations:
- Special situations are keyed on **different dimensions**: time/visibility (night), road infrastructure (climbing lane, shoulder), side of passing (right), target type (streetcar). So "special condition" isn't one axis.
- **Overlaps and cross-references:** streetcars appear in both "Passing on the right" and "Passing streetcars"; left-turning vehicles appear in both "shoulder" and "right". The same fact gets restated from different angles.
- **Implicit defaults are left unstated.** "Passing on the shoulder" only makes sense against the unwritten default that you don't drive on the shoulder. "Passing on the right" states its default ("most passing is done on the left").
- Night repeats the inherited steps (signal, mirror, blind spot) and only *changes* the headlight behaviour. It's effectively "base procedure + delta".

---

## 5. Passing rules elsewhere in the handbook

Passing content isn't confined to this page. Examples from a quick skim of three sibling pages:

| Page | Passing-related content |
|---|---|
| Stopping → Pedestrian crossovers | "You must not pass any vehicle within 30 metres of a pedestrian crossover." (same as F1, restated) |
| Changing directions → Left turns | Behind a motorcycle/bicycle turning left: don't pull up beside it; "Wait for the smaller vehicle to move right before you pass." |
| Changing directions → Two-way left-turn lane | "These left-turn lanes are not to be used for passing." |
| Freeway driving → Driving along | Keep right, left lanes for passing, don't stay in the far-left lane; trucks use the lane right of far-left for passing (same as F8) |
| Stopping → School buses | Failing to stop for a school bus with red lights flashing (i.e., illegally passing it) |

The handbook is organised by **driving task / chapter**, not by rule topic. A complete "passing" rule set needs a cross-page index.

---

## 6. Does the pattern hold on other pages?

| Page | Intro principle | General → special | Explicit "special situations" heading | Dominant unit |
|---|---|---|---|---|
| Changing positions | ✓ | ✓ | implicit (H2 per situation) | procedure (steps) |
| Changing directions | ✓ (check around you) | ✓ (Turning a corner → right/left → on red → roundabout) | ✓ "Dealing with particular situations at a roundabout" | procedure; roundabout split into **phases** (approach / enter / exit) |
| Stopping | ✓ (stop smoothly; where to stop) | ✓ (general stop position → railway, school crossing, school bus, crossover) | implicit | **obligations with conditions** (checklists rather than steps) |
| Freeway driving | ✓ (definition + who may use) | ✓ by **phase** (enter / along / leave) + HOV | – | phases + **eligibility rules** (HOV: who may use) |

So the **page-level skeleton (intro → general → special → summary) is consistent.** The **unit inside** varies by topic. At least four unit types show up:
1. **Procedure**: ordered steps (lane change, passing, turns)
2. **Phased procedure**: steps grouped by phase (roundabout, freeway)
3. **Conditional obligation / prohibition**: if X then must / must-not (stopping, shoulder, streetcar)
4. **Eligibility rule**: who or what may use a facility (HOV lane, climbing lane)

---

## 7. Open questions for the next step

1. **Actor split:** should "being passed" (F6–F8 plus the "don't speed up" clause) become its own unit, separate from "passing"?
2. **Inheritance:** do we model Passing as `Changing lanes` + extra steps, or flatten the inherited steps in?
3. **Special-situation axes:** tag each special case by its trigger dimension (time, infrastructure, target type, side)?
4. **Scope of "passing":** only this page, or also the cross-page items in §5?
5. **Background facts** (e.g. "trucks are barred from the far-left lane"): keep as a separate "context fact" slot, or drop?
