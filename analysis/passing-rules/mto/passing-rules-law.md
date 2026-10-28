# Ontario passing rules, with the law added

Generated from the rules database (`db/`) by `python3 tools/db.py export --write`. Do not edit by hand.

Each statement is shown as extracted from the handbook, with its flags and their notes unchanged: it is the reference the extraction is scored against. What the law adds comes under it:

- under each flag, how far a formal source settles it, and the provisions or handbook sentences that do;
- **Law**: what the law says on the statement's subject, in the rule language, with the provisions it cites. A word the law leaves as open as the handbook keeps its `[?…]` mark;
- **Compared with the law**: each provision behind the statement and how the statement compares with it.

Every provision is quoted word for word under [Provisions](#provisions), with a link to its line in the local copy of the law (`statutes/`, checked by `tools/db.py check`) and to the official page on e-Laws.

## Summary

88 statements. Law lines are added under 31 of them (33 lines); for 14, the handbook words as advice what the law makes a duty.

| Flags | | |
|---|---|---|
| `LAW_DEFINES` | 8 | the law gives the definition or the number |
| `LAW_STATES` | 18 | the law states the duty itself, which settles its strength, scope or reference |
| `LAW_REPEATS` | 20 | the law uses the same open word, so the vagueness is in the law too |
| `HANDBOOK` | 8 | another part of the handbook settles it |
| `OPEN` | 18 | no formal source settles it |

| Compared with the law | |
|---|---|
| `SAME` | the provision states the same duty |
| `BROADER` | the statement applies in more cases than the provision (it drops a condition) |
| `NARROWER` | the statement applies in fewer cases than the provision |
| `DIFFERENT` | the statement and the provision disagree |
| `PENALTY` | the provision sets the penalty |

## Statements

### 1a

> DEFINE changing position IS a manoeuvre THAT changes lanes OR passes another vehicle

DEFINE. Handbook: Changing positions page · Chapter 2.

### 1b

> DEFINE passing IS a lane change THAT moves past a slower vehicle ALSO CALLED overtaking

DEFINE. Handbook: Changing positions page · Chapter 2 › Passing.

**Flags**

- V "overtaking": The handbook uses "pass", "overtake" and "overtake and pass" for the same manoeuvre.
  - `LAW_REPEATS`: None; keep ALSO CALLED overtaking. The Act uses "pass" (148 (8)), "overtake" (148 (2), 148.1 (1)) and "overtake and pass" (150 (1)) and defines none of them. ([HTA 148 (2)](#on-hta-148-2), [HTA 148 (8)](#on-hta-148-8), [HTA 150 (1)](#on-hta-150-1))

### 1c

> FACT vehicles on the same road do not all travel at the same speed, even though every public road has a speed limit

FACT. Handbook: Changing positions page · Chapter 2 › Passing.

### 1d

> FACT cyclists, road service vehicles and drivers preparing to turn are [?usually] slower than through traffic

FACT. Handbook: Changing positions page · Chapter 2 › Passing.

_"You may want to pass some slow-moving vehicles" is motivation, not a permission, so no MAY rule is written for it._

**Flags**

- S "usually": Hedged generalisation.
  - `OPEN`: A description of traffic, not a duty.

### 2.1a

> a driver SHOULD start a lane change or a pass ONLY IF the driver has [?enough] space and time to complete it [?safely]

RULE, ADVICE. Handbook: Changing positions page · Chapter 2.

**Flags**

- J "enough": No measure of space or time.
  - `LAW_REPEATS`: For a lane change: at least a two- to three-second gap behind the vehicle ahead in the new lane, and not beside another vehicle or in its blind spot (handbook, Level Two road test). Could replace "enough space" for lane changes; no measure for a pass on a two-lane road. The Act asks the driver to "first see that the movement can be made in safety" (142 (1)) and to "first ascertain that it can be done safely" (154 (1) (a)), with no measure. ([HTA 142 (1)](#on-hta-142-1), [HTA 154 (1) (a)](#on-hta-154-1-a), handbook level-two-road-test:142.1, handbook level-two-road-test:142.2)
- J "safely": Judgment term.
  - `LAW_REPEATS`: The Act uses the same word: 154 (1) (a) "safely", 142 (1) "in safety". ([HTA 142 (1)](#on-hta-142-1), [HTA 154 (1) (a)](#on-hta-154-1-a))

**Law**

- `a driver MUST start a lane change or a pass ONLY IF the driver has first made sure there is [?enough] space and time to complete it [?safely] IF VIOLATED 3 demerit points`
  - [HTA 142 (1)](#on-hta-142-1), [HTA 154 (1) (a)](#on-hta-154-1-a), [O. Reg. 339/94 Table, item 13](#on-reg-339-94-item-13). The Act puts the same judgment on the driver and gives no measure. For a lane change the handbook's road test gives one: at least a 2 to 3 s gap behind the vehicle ahead in the new lane, not beside another vehicle or in its blind spot.

**Compared with the law**

- `SAME` [HTA 142 (1)](#on-hta-142-1): The Act also requires the driver to see first that the move can be made in safety, and to signal when another vehicle may be affected.
- `SAME` [HTA 154 (1) (a)](#on-hta-154-1-a): The Act makes it a duty for any move from one lane to another; the handbook words it as advice.
- `PENALTY` [O. Reg. 339/94 Table, item 13](#on-reg-339-94-item-13): 3 demerit points for a conviction under s. 154.

### 2.1b

> a driver SHOULD NOT pass a vehicle UNLESS the driver is [?sure] the pass can be made without danger to the driver or others

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing.

**Flags**

- J "sure": Subjective certainty; no observable test.
  - `LAW_REPEATS`: Strength: the Act makes it a duty for any pass that moves from one lane to another. The Act puts the same judgment on the driver: "first ascertains that it can be done safely" (154 (1) (a)), "first see that the movement can be made in safety" (142 (1)). ([HTA 142 (1)](#on-hta-142-1), [HTA 154 (1) (a)](#on-hta-154-1-a))

**Law**

- `a driver MUST NOT pass a vehicle UNLESS the driver has first made [?sure] the pass can be made without danger to the driver or others IF VIOLATED 3 demerit points`
  - [HTA 154 (1) (a)](#on-hta-154-1-a), [O. Reg. 339/94 Table, item 13](#on-reg-339-94-item-13). For a pass that moves from one lane to another, which is every pass but one within the lane.

**Compared with the law**

- `SAME` [HTA 154 (1) (a)](#on-hta-154-1-a): For a pass that moves from one lane to another. The Act makes it a duty; the handbook words it as advice.
- `PENALTY` [O. Reg. 339/94 Table, item 13](#on-reg-339-94-item-13): 3 demerit points for a conviction under s. 154.

### 2.1c

> a driver SHOULD NOT pass WHEN the driver is [?in doubt]

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing.

**Flags**

- J "in doubt": Subjective state; the catch-all behind 2.1b.
  - `OPEN`: The driver’s own state. A driver in doubt has not ascertained that the move is safe, which 154 (1) (a) requires, but no source names the state.

### 2.1d

> a driver SHOULD keep to the right of the road, or to the right-hand lane of a multi-lane road UNLESS the driver is turning left OR passing another vehicle

RULE, ADVICE. Handbook: Driving along › Keep right · ¶1.

### 2.2a

> TO pass a vehicle

PROCEDURE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing.

_Steps 1 and 2 restate the lane-change steps on the same page; the order of the steps carries "only after signalling"._

**Flags**

- V "inside mirror": Called "rear view mirror" in the night procedure (3.3.1b).
  - `HANDBOOK`: The inside rear-view mirror. None; both procedures already say inside mirror. The handbook says "inside mirror" in the passing steps and "rear view mirror" in the night steps. (handbook changing-positions:018.2, handbook changing-positions:029.1)

### 2.2b

> a driver SHOULD NOT cut off the vehicle being passed by moving in front of it suddenly WHEN returning to the original lane

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing.

### 3.1.1a

> a driver MUST NOT pass a vehicle WHEN the driver is within 30 m of a pedestrian crossover

RULE, LAW. Handbook: Changing positions page · Chapter 2 › Passing; Stopping › Stopping for pedestrian crossovers · ¶2.

**Flags**

- X "within 30 m": Stated on two pages (Changing positions, Stopping) in different words; the meanings agree.
  - `LAW_STATES`: Within 30 m of the crossover, do not let the front of your vehicle pass beyond the front of another vehicle approaching it. Use the Act’s wording; both handbook pages agree with it. ([HTA 140 (3)](#on-hta-140-3))

**Law**

- `a driver approaching from the rear MUST NOT let the front of the driver's vehicle pass beyond the front of another vehicle WHEN the other vehicle is approaching a pedestrian crossover AND is within 30 m of it IF VIOLATED 4 demerit points`
  - [HTA 140 (3)](#on-hta-140-3), [O. Reg. 339/94 Table, item 21](#on-reg-339-94-item-21). Measured front to front, as the Act states it.

**Compared with the law**

- `SAME` [HTA 140 (3)](#on-hta-140-3): The Act states the test: do not let the front of your vehicle pass beyond the front of the other vehicle that is approaching the crossover.
- `PENALTY` [O. Reg. 339/94 Table, item 21](#on-reg-339-94-item-21): 4 demerit points.

### 3.1.2a

> a driver MUST NOT pass [?on the left of a centreline] WHEN the driver is [?30 m from] a bridge, viaduct or tunnel

RULE, LAW. Handbook: Changing positions page · Chapter 2 › Passing.

**Flags**

- R "30 m from": "30 metres from" is read as "within 30 m of"; the text does not say whether it covers both approaches.
  - `LAW_DEFINES`: Within 30 m of the bridge, viaduct or tunnel, where the driver’s view is obstructed within that distance. Read "30 m from" as "within 30 m of", and add WHEN the view is obstructed. ([HTA 149 (1)](#on-hta-149-1))
- G "on the left of a centreline": Prohibits the means (crossing the centreline), not passing; passing near a bridge on a multi-lane road is not covered.
  - `LAW_STATES`: Driving left of the centre of a roadway with one or more lanes in each direction. None; the Act also bans the means, not the pass, so a pass on a road with more lanes one way than the other is not covered (149 (2) (a)). ([HTA 149 (1)](#on-hta-149-1), [HTA 149 (2)](#on-hta-149-2))

**Law**

- `a driver MUST NOT drive left of the centre of the road WHEN the road has one or more lanes in each direction AND the driver is within 30 m of a bridge, viaduct or tunnel AND the driver's view is obstructed within that distance UNLESS the road has more lanes in one direction than in the other OR the road is one-way IF VIOLATED 3 demerit points`
  - [HTA 149 (1)](#on-hta-149-1), [HTA 149 (2)](#on-hta-149-2), [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12). The Act bans the means, driving left of centre, so it covers passing there but not a pass that stays right of centre. Road service vehicles taking precautions are also exempt (149 (2) (b)).

**Compared with the law**

- `BROADER` [HTA 149 (1)](#on-hta-149-1): The Act bans driving left of centre within 30 m of a bridge, viaduct or tunnel only where the driver’s view is obstructed within that distance; the statement leaves that condition out.
- `BROADER` [HTA 149 (2)](#on-hta-149-2): The statement leaves out the exceptions: more lanes in one direction than the other, road service vehicles, one-way traffic.
- `PENALTY` [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12): 3 demerit points (improper passing).

### 3.1.3a

> a driver SHOULD NOT pass WHEN (the driver is approaching the crest of a hill OR the driver is on a curve) AND the view of oncoming traffic is obstructed AND the clear distance ahead is not [?enough] to pass [?safely]

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing.

**Flags**

- J "enough": No distance given.
  - `LAW_REPEATS`: Strength: 149 (1) (a) makes it a prohibition. The Act gives no distance either: 148 (8) asks that the road ahead be "safely free from approaching traffic". An engineering measure (passing sight distance, OTM Book 11) was not obtained. ([HTA 148 (8)](#on-hta-148-8), [HTA 149 (1)](#on-hta-149-1))
- J "safely": Judgment term.
  - `LAW_REPEATS`: The Act gives no distance either: 148 (8) asks that the road ahead be "safely free from approaching traffic". An engineering measure (passing sight distance, OTM Book 11) was not obtained. ([HTA 148 (8)](#on-hta-148-8))

**Law**

- `a driver MUST NOT drive left of the centre of the road WHEN the road has one or more lanes in each direction AND (the driver is approaching the crest of a hill OR the driver is on a curve) AND the driver's view is obstructed so that a vehicle coming the other way would be a [?potential hazard] UNLESS the road has more lanes in one direction than in the other OR the road is one-way IF VIOLATED 3 demerit points`
  - [HTA 149 (1)](#on-hta-149-1), [HTA 149 (2)](#on-hta-149-2), [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12). The Act's test, "a potential hazard", is as open as the handbook's "not enough to pass safely". The engineering measure, passing sight distance in OTM Book 11, was not obtained.

**Compared with the law**

- `SAME` [HTA 149 (1)](#on-hta-149-1): The Act bans driving left of centre approaching a crest or on a curve where the view is obstructed; the handbook words it as advice.
- `BROADER` [HTA 149 (2)](#on-hta-149-2): The Act does not apply where the road has more lanes in one direction than in the other, or is one-way; the statement has no exception.
- `PENALTY` [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12): 3 demerit points (improper passing).

### 3.1.4a

> a driver SHOULD NOT use a two-way left-turn lane for passing

RULE, ADVICE. Handbook: Changing directions › Left-turn lanes · ¶3.

**Flags**

- M "are not to be used": Not an imperative and no legal marker; the default puts it at SHOULD NOT, but the wording reads like a prohibition.
  - `LAW_STATES`: Where the lane carries the Figure 7 Lane Designation sign, it is for left turns only, and drivers must obey the sign. Without it, on a three-lane highway, the centre lane may be used to pass when the road is clearly visible and the lane is clear. Strength LAW WHEN the lane carries the two-way left-turn sign; otherwise the handbook is stricter than the Act. ([HTA 154 (1) (b)](#on-hta-154-1-b), [HTA 182 (2)](#on-hta-182-2), [Reg. 615 34 (3)](#on-reg-615-34-3), [Reg. 615 34 (4) (a), (b)](#on-reg-615-34-4))

**Law**

- `a driver MUST NOT use a two-way left-turn lane for passing WHEN the lane is marked with the two-way left-turn lane sign`
  - [HTA 182 (2)](#on-hta-182-2), [Reg. 615 34 (3)](#on-reg-615-34-3), [Reg. 615 34 (4) (a), (b)](#on-reg-615-34-4). The sign makes the lane for left turns only.

**Compared with the law**

- `DIFFERENT` [HTA 154 (1) (b)](#on-hta-154-1-b): On a three-lane highway, the Act lets a driver pass in the centre lane when the road is clearly visible and the lane is clear; the statement bars it.
- `BROADER` [HTA 182 (2)](#on-hta-182-2): Drivers must obey the sign.
- `BROADER` [Reg. 615 34 (3)](#on-reg-615-34-3): Law where the lane carries the Figure 7 sign, which goes directly over a two-way left-turn lane (34 (4) (b)): the lane is for left turns only.
- `BROADER` [Reg. 615 34 (4) (a), (b)](#on-reg-615-34-4): The Figure 7 sign goes directly over a two-way left-turn lane.

### 3.1.5a

> FACT pavement markings show, among other things, where it is not [?safe] to pass

FACT. Handbook: Pavement markings › Intro · ¶1.

**Flags**

- J "safe": Judgment term inside a description.
  - `OPEN`: Describes what markings are for; no duty to ground.

### 3.1.5b

> a driver SHOULD NOT pass WHEN there is a solid line at the left of the driver's lane BECAUSE a solid line there means it is unsafe to pass

RULE, ADVICE. Handbook: Pavement markings › Intro · ¶3; Pavement markings › Intro · Diagram 3-2.

### 3.1.6a

> a driver MAY pass WHEN there is a broken line at the left of the driver's lane ONLY IF the way is clear AND there are [?enough] broken lines ahead to complete the pass [?safely]

RULE, LAW. Handbook: Pavement markings › Intro · ¶4; Pavement markings › Intro · Diagram 3-3.

**Flags**

- J "enough": No distance given.
  - `LAW_REPEATS`: The Act gives no distance either: 148 (8) asks that the road ahead be "safely free from approaching traffic". An engineering measure (passing sight distance, OTM Book 11) was not obtained. ([HTA 148 (8)](#on-hta-148-8))
- J "safely": Judgment term.
  - `LAW_REPEATS`: The Act gives no distance either: 148 (8) asks that the road ahead be "safely free from approaching traffic". An engineering measure (passing sight distance, OTM Book 11) was not obtained. ([HTA 148 (8)](#on-hta-148-8))

**Law**

- `a driver MAY pass WHEN there is a broken line at the left of the driver's lane ONLY IF the road in front of and to the left of the vehicle being passed is [?safely] free of approaching traffic AND the road to the left of the driver is [?safely] free of overtaking traffic AND there are [?enough] broken lines ahead to complete the pass IF VIOLATED 3 demerit points`
  - [HTA 148 (8)](#on-hta-148-8), [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12). "The way is clear" becomes the Act's two conditions; "safely" is the Act's own word.

**Compared with the law**

- `NARROWER` [HTA 148 (8)](#on-hta-148-8): The Act asks that the road ahead be safely free of approaching traffic on any road; the statement covers only a broken line.
- `PENALTY` [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12): 3 demerit points (improper passing).

### 3.1.7a

> a driver MUST NOT pass WHEN a "do not pass" sign applies to the road

RULE, LAW. Handbook: Signs › Regulatory signs · ¶19; Signs › Regulatory signs · image.

_The sign's own caption is a plain imperative; the legal force comes from the section introduction._

**Law**

- `a driver MUST NOT pass WHEN a "do not pass" sign applies to the road`
  - [HTA 182 (2)](#on-hta-182-2), [Reg. 615 35](#on-reg-615-35)

**Compared with the law**

- `SAME` [HTA 182 (2)](#on-hta-182-2): Drivers must obey the instructions on a sign erected under the regulations.
- `SAME` [Reg. 615 35](#on-reg-615-35): The Do Not Pass sign the regulations prescribe.

### 3.2.1a

> DEFINE a passing lane or climbing lane IS an added lane THAT lets slower vehicles move into the right-hand lane so faster vehicles can pass [?safely] in the left lane

DEFINE. Handbook: Changing positions page · Chapter 2 › Passing and climbing lanes.

**Flags**

- J "safely": Judgment term inside a definition.
  - `OPEN`: Inside a definition, about the lane’s purpose; no duty to ground.

### 3.2.1b

> FACT an advance sign tells drivers a passing opportunity is coming, AND another sign warns when the added lane is ending

FACT. Handbook: Changing positions page · Chapter 2 › Passing and climbing lanes.

### 3.2.1c

> a driver in the right-hand lane SHOULD merge [?safely] with traffic in the left-hand lane WHEN a sign warns that the lane is ending

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing and climbing lanes.

**Flags**

- D "merge": The rule is implied by a purpose clause about the sign; the text states no instruction.
  - `LAW_STATES`: Do not move from the ending lane into the next lane unless you first ascertain it can be done safely. The instruction the flag misses is 154 (1) (a); the statement can cite it. ([HTA 154 (1) (a)](#on-hta-154-1-a))
- J "safely": Judgment term.
  - `LAW_REPEATS`: The Act uses the same word (154 (1) (a)). ([HTA 154 (1) (a)](#on-hta-154-1-a))

**Law**

- `a driver MUST NOT move from one lane to another UNLESS the driver has first made sure the move can be made [?safely] IF VIOLATED 3 demerit points`
  - [HTA 154 (1) (a)](#on-hta-154-1-a), [O. Reg. 339/94 Table, item 13](#on-reg-339-94-item-13). The duty the merge falls under.

**Compared with the law**

- `NARROWER` [HTA 154 (1) (a)](#on-hta-154-1-a): The Act covers any move from one lane to another; the statement only a lane that is ending. The handbook words it as advice.
- `PENALTY` [O. Reg. 339/94 Table, item 13](#on-reg-339-94-item-13): 3 demerit points for a conviction under s. 154.

### 3.2.1d

> a driver MUST keep to the right-hand lane WHEN a "keep right except to pass" sign is posted UNLESS the driver is passing on a two-lane section where a climbing or passing lane is provided

RULE, LAW. Handbook: Signs › Regulatory signs · ¶31; Signs › Regulatory signs · image.

### 3.2.2a

> a driver on a freeway SHOULD keep to the right AND use the left lanes for passing

RULE, ADVICE. Handbook: Freeway driving › Driving along a freeway · ¶1.

### 3.2.2b

> a driver SHOULD use the far-left lane of a multi-lane freeway ONLY IF the driver is passing traffic that moves slower than the speed limit

RULE, ADVICE. Handbook: Freeway driving › Driving along a freeway · ¶5.

_"Use the far left lane … to pass …, but don't stay there" is read as: that lane is for passing only._

### 3.2.2c

> a driver on a freeway SHOULD drive in the right-hand lane WHEN [?possible] BECAUSE this leaves the other lanes clear for passing

RULE, ADVICE. Handbook: Freeway driving › Driving along a freeway · ¶5.

**Flags**

- J "possible": No test for when it is possible.
  - `LAW_REPEATS`: The Act says "where practicable", and only for vehicles slower than the normal speed of traffic (147 (1)). ([HTA 147 (1)](#on-hta-147-1))

**Law**

- `a driver travelling at less than the normal speed of traffic at that time and place MUST drive in the right-hand lane then available for traffic OR as close as [?practicable] to the right-hand curb or edge of the roadway WHEN [?practicable] IF VIOLATED a fine of $150 to $1,000`
  - [HTA 147 (1)](#on-hta-147-1), [HTA 147 (3)](#on-hta-147-3). Law only for a vehicle slower than the normal speed of traffic; the handbook asks every driver on a freeway.

**Compared with the law**

- `BROADER` [HTA 147 (1)](#on-hta-147-1): The Act asks only a vehicle slower than the normal speed of traffic to keep to the right-hand lane, where practicable; the statement asks every driver.
- `PENALTY` [HTA 147 (3)](#on-hta-147-3): $150 to $1,000.

### 3.2.3a

> a driver SHOULD pass on the left BECAUSE passing on the right can be more dangerous

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing on the right.

**Flags**

- D "pass on the left": The default is described, not instructed; it is needed so that 3.2.3b reads as an exception.
  - `LAW_STATES`: Pass on the left, except in the cases of 150 (1) (a) to (c). The default exists in the Act: passing on the right is lawful only in those cases. ([HTA 150 (1)](#on-hta-150-1))
- S "Most passing": Hedged generalisation in the source.
  - `LAW_STATES`: The hedge "most" is exact: the exceptions are 150 (1) (a) to (c). ([HTA 150 (1)](#on-hta-150-1))

**Law**

- `a driver MUST pass on the left BECAUSE passing on the right can be more dangerous`
  - [HTA 150 (1)](#on-hta-150-1). Passing on the right is lawful only in the cases of 3.2.3b.

**Compared with the law**

- `SAME` [HTA 150 (1)](#on-hta-150-1): Passing on the right is lawful only in the cases of 150 (1) (a) to (c), so passing on the left is the rule.

### 3.2.3b

> EXCEPTION TO 3.2.3a: a driver MAY pass on the right WHEN the road is multi-lane OR the road is one-way OR the vehicle being passed is a streetcar OR the vehicle being passed is turning left

RULE, LAW. Handbook: Changing positions page · Chapter 2 › Passing on the right.

**Law**

- `EXCEPTION TO 3.2.3a: a driver MAY pass on the right ONLY IF the pass can be made [?in safety] AND (the vehicle being passed is making or about to make a left turn OR its driver has signalled a left turn OR the road has unobstructed pavement wide enough for 2 or more lines of vehicles in each direction OR the road is one-way OR the vehicle being passed is a streetcar) IF VIOLATED 3 demerit points`
  - [HTA 150 (1)](#on-hta-150-1), [HTA 166 (2)](#on-hta-166-2), [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12). "Multi-lane" is the Act's pavement wide enough for two or more lines of vehicles in each direction; a streetcar must be passed on the right (3.4.5a).

**Compared with the law**

- `BROADER` [HTA 150 (1)](#on-hta-150-1): The Act adds "only where the movement can be made in safety"; its multi-lane case is pavement wide enough for two or more lines of vehicles in each direction. Streetcars are in 166 (2).
- `SAME` [HTA 166 (2)](#on-hta-166-2): The streetcar case: the Act bans passing a streetcar on the left, except on a one-way road.
- `PENALTY` [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12): 3 demerit points (improper passing).

### 3.2.3c

> a driver SHOULD wait WHEN the driver is in the leftmost lane with a slower vehicle in front UNTIL the slower vehicle moves to the right

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing on the right.

### 3.2.3d

> a driver SHOULD NOT change lanes suddenly to pass on the right WHEN the driver is in the leftmost lane behind a slower vehicle BECAUSE the driver in front may move to the right at the same time

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing on the right.

### 3.2.4a

> a driver MAY drive on the right shoulder ONLY IF the driver is passing a vehicle that is turning left AND the shoulder is paved

RULE, LAW. Handbook: Changing positions page · Chapter 2 › Passing on the shoulder.

**Flags**

- D "right shoulder": Presupposes that driving on the shoulder is otherwise not allowed; that default is not stated here.
  - `LAW_STATES`: Passing by driving off the roadway is banned (150 (2)), except on a paved right shoulder to pass a vehicle turning left (150 (3) (a)). The unstated prohibition is 150 (2); the statement is its exception. ([HTA 150 (2)](#on-hta-150-2), [HTA 150 (3) (a)](#on-hta-150-3-a))

**Law**

- `a driver MUST NOT pass a vehicle by driving off the roadway IF VIOLATED 3 demerit points`
  - [HTA 150 (2)](#on-hta-150-2), [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12). The prohibition the permission presupposes.
- `a driver MAY pass on the right shoulder ONLY IF the shoulder is paved AND (the vehicle being passed is making or about to make a left turn OR its driver has signalled a left turn) AND the pass can be made [?in safety]`
  - [HTA 150 (1)](#on-hta-150-1), [HTA 150 (3) (a)](#on-hta-150-3-a). The exception to the line above.

**Compared with the law**

- `BROADER` [HTA 150 (1)](#on-hta-150-1): The Act also requires a pass on the right to be made in safety; the statement leaves the condition out.
- `NARROWER` [HTA 150 (2)](#on-hta-150-2): The general rule the permission is an exception to: no passing by driving off the roadway.
- `NARROWER` [HTA 150 (3) (a)](#on-hta-150-3-a): The Act also allows it when the vehicle passed is about to turn left or has signalled a left turn.
- `PENALTY` [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12): 3 demerit points (improper passing).

### 3.2.4b

> a driver MUST NOT pass on the left shoulder, whether or not it is paved

RULE, LAW. Handbook: Changing positions page · Chapter 2 › Passing on the shoulder.

**Law**

- `a driver MUST NOT pass on the left shoulder, whether or not it is paved IF VIOLATED 3 demerit points`
  - [HTA 150 (2)](#on-hta-150-2), [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12)

**Compared with the law**

- `NARROWER` [HTA 150 (2)](#on-hta-150-2): The Act bans passing by driving off the roadway on either side.
- `PENALTY` [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12): 3 demerit points (improper passing).

### 3.3.1a

> a driver SHOULD pass with [?extra care] WHEN it is night

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing at night.

**Flags**

- J "extra care": A caution with no named hazard, so WATCH FOR does not fit.
  - `OPEN`: No source sets a night standard for passing.

### 3.3.1b

> TO pass a vehicle at night SPECIALIZES 2.2a WHEN the driver has to pass AND the way is clear

PROCEDURE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing at night.

**Flags**

- V "rear view mirror": The handbook calls the mirror "rear view mirror" here and "inside mirror" in 2.2a; both rules say inside mirror.
  - `HANDBOOK`: The inside rear-view mirror. None; both procedures already say inside mirror. (handbook changing-positions:018.2, handbook changing-positions:029.1)

### 3.3.1c

> a driver SHOULD use low beams WHEN the driver is less than 60 m behind another vehicle UNLESS the driver is passing it

RULE, ADVICE. Handbook: Getting ready to drive › Turn on headlights at night and in poor conditions · ¶1.

### 3.3.2a

> a driver SHOULD NOT pass WHEN driving in fog

RULE, ADVICE. Handbook: Night and bad weather › Fog › DO · item 5; Night and bad weather › Fog › REMEMBER · item 3.

_The fog advice says "Avoid passing" in one list and "Don't pass" in another; both map to SHOULD NOT._

### 3.3.2b

> a driver SHOULD NOT speed up to pass a slow-moving vehicle WHEN driving in fog

RULE, ADVICE. Handbook: Night and bad weather › Fog › Don’t · item 3.

### 3.3.3a

> a driver SHOULD NOT pass WHEN driving in blowing snow or a whiteout

RULE, ADVICE. Handbook: Night and bad weather › Whiteouts › DO · item 4.

### 3.3.3b

> a driver SHOULD NOT attempt to pass a slow-moving vehicle WHEN driving in blowing snow or a whiteout

RULE, ADVICE. Handbook: Night and bad weather › Whiteouts › DON'T · item 2.

### 3.4.1a

> a driver SHOULD WATCH FOR doors opening suddenly AND doors opened to load or unload WHILE passing parked vehicles

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing.

### 3.4.2a

> FACT motorcycles, bicycles, limited-speed motorcycles and mopeds [?often] move to the left or right side of their lane to avoid dangerous road conditions OR to be seen

FACT. Handbook: Changing positions page · Chapter 2 › Passing.

**Flags**

- S "often": Hedged generalisation.
  - `OPEN`: A description of riders, not a duty.

### 3.4.2b

> a driver SHOULD NOT pass a motorcycle, bicycle, limited-speed motorcycle or moped within its lane BECAUSE its position in the lane is not an invitation to pass (3.4.2a)

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing.

### 3.4.2c

> a driver SHOULD change lanes WHEN passing a motorcycle, bicycle, limited-speed motorcycle or moped

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing.

### 3.4.3a

> a driver SHOULD NOT pass a [?smaller vehicle] that is turning left ahead UNTIL it has moved to the right

RULE, ADVICE. Handbook: Changing directions › Left turns · ¶5.

**Flags**

- R "smaller vehicle": The motorcycles, bicycles and mopeds turning left, named two sentences earlier.
  - `HANDBOOK`: Motorcycles, bicycles, limited-speed motorcycles and mopeds. Name the vehicles instead of "smaller vehicle". (handbook changing-directions:017.1)

### 3.4.3b

> a driver SHOULD NOT pull up beside a [?smaller vehicle] that is turning left ahead to make the turn at the same time WHEN the driver is also turning left, behind it

RULE, ADVICE. Handbook: Changing directions › Left turns · ¶5.

_Pulling up beside a turning two-wheeler is the start of a pass._

**Flags**

- R "smaller vehicle": The source says "one of these vehicles": those named in the sentence before.
  - `HANDBOOK`: Motorcycles, bicycles, limited-speed motorcycles and mopeds. Name the vehicles instead of "smaller vehicle". (handbook changing-directions:017.1)

### 3.4.3c

> a driver SHOULD stay behind a [?smaller vehicle] that is turning left ahead WHEN the driver is also turning left, behind it UNTIL the way is [?clear]

RULE, ADVICE. Handbook: Changing directions › Left turns · ¶5.

_"… and turn when the way is clear" is written as the end of the wait (UNTIL)._

**Flags**

- R "smaller vehicle": Same vehicles as 3.4.3b; the source only says "Stay behind".
  - `HANDBOOK`: Motorcycles, bicycles, limited-speed motorcycles and mopeds. Name the vehicles instead of "smaller vehicle". (handbook changing-directions:017.1)
- J "clear": No test for when the way is clear.
  - `LAW_REPEATS`: The Act asks the driver to "first see that the movement can be made in safety" before turning left (142 (1)), with no test. ([HTA 142 (1)](#on-hta-142-1))

### 3.4.4a

> a cyclist MAY use any part of the lane WHEN this is [?necessary for safety], for example to discourage passing where the lane is too narrow to be shared [?safely]

RULE, LAW. Handbook: Sharing the road › Cyclists · ¶1; Sharing the road › Cyclists · item 3.

_A rule for the cyclist, not the passing driver._

**Flags**

- J "necessary for safety": Judgment of the cyclist.
  - `LAW_REPEATS`: The permission is the "where practicable" of 147 (1); the Act gives no test. ([HTA 147 (1)](#on-hta-147-1))
- J "safely": Judgment term.
  - `LAW_REPEATS`: Same "where practicable" of 147 (1). ([HTA 147 (1)](#on-hta-147-1))

**Law**

- `a cyclist MAY use any part of the lane WHEN this is [?necessary for safety], for example to discourage passing where the lane is too narrow to be shared [?safely]`
  - [HTA 147 (1)](#on-hta-147-1). The "where practicable" of 147 (1): a slower vehicle keeps right only where practicable.

**Compared with the law**

- `SAME` [HTA 147 (1)](#on-hta-147-1): The permission is the "where practicable" of 147 (1), seen from the cyclist’s side: a slower vehicle keeps right only where practicable.

### 3.4.4b

> a driver of a motor vehicle MUST keep at least 1 m between the vehicle and a cyclist WHEN [?practical] WHILE passing the cyclist IF VIOLATED a fine AND 2 demerit points

RULE, LAW. Handbook: Sharing the road › Cyclists · ¶3; Sharing the road › Cyclists · Diagram 2-11.

**Flags**

- J "practical": Leaves open when the 1 m minimum can be set aside.
  - `LAW_REPEATS`: The 1 m is measured from the extreme right side of the motor vehicle to the extreme left side of the bicycle, including all projections and attachments. Add how the 1 m is measured. The Act says "as nearly as may be practicable" and gives no test for when the 1 m may be reduced. ([HTA 148 (6.1)](#on-hta-148-6-1), [HTA 148 (6.2)](#on-hta-148-6-2))

**Law**

- `a driver of a motor vehicle MUST keep at least 1 m between the right side of the vehicle and the left side of the bicycle, including all projections and attachments, WHEN [?practicable] WHILE passing a cyclist UNTIL the vehicle is [?safely] past the bicycle IF VIOLATED a fine of $60 to $1,000 AND 2 demerit points`
  - [HTA 148 (6.1)](#on-hta-148-6-1), [HTA 148 (6.2)](#on-hta-148-6-2), [HTA 214 (1)](#on-hta-214-1), [O. Reg. 339/94 Table, item 44](#on-reg-339-94-item-44)

**Compared with the law**

- `SAME` [HTA 148 (6.1)](#on-hta-148-6-1)
- `SAME` [HTA 148 (6.2)](#on-hta-148-6-2): How the 1 m is measured.
- `PENALTY` [HTA 214 (1)](#on-hta-214-1): No fine is set in s. 148, so the general penalty applies: $60 to $1,000.
- `PENALTY` [O. Reg. 339/94 Table, item 44](#on-reg-339-94-item-44): 2 demerit points.

### 3.4.4c

> a driver SHOULD change lanes to pass a cyclist WHEN [?possible]

RULE, ADVICE. Handbook: Sharing the road › Cyclists · ¶3.

**Flags**

- J "possible": No test for when it is possible.
  - `OPEN`: The Act sets only the 1 m minimum (148 (6.1)); changing lanes is advice.

### 3.4.4d

> a driver SHOULD NOT sound the horn [?unnecessarily] WHILE passing a cyclist BECAUSE it may frighten the cyclist and cause a loss of control

RULE, ADVICE. Handbook: Sharing the road › Cyclists · ¶6.

**Flags**

- J "unnecessarily": Who judges necessity is not stated.
  - `LAW_REPEATS`: The Act says "so as to make an unreasonable noise" (75 (4)) and gives no test. ([HTA 75 (4)](#on-hta-75-4))

### 3.4.4e

> a driver SHOULD tap the horn quickly and lightly while still [?some distance] away from the cyclist WHEN the driver feels the horn must be used

RULE, ADVICE. Handbook: Sharing the road › Cyclists · ¶6.

**Flags**

- J "some distance": No distance given.
  - `OPEN`: The Act asks for the horn "whenever it is reasonably necessary to notify pedestrians or others of its approach" (75 (5)) and gives no distance.

### 3.4.5a

> a driver MUST pass a streetcar on the right UNLESS the driver is on a one-way road

RULE, LAW. Handbook: Changing positions page · Chapter 2 › Passing streetcars.

**Law**

- `a driver MUST pass a streetcar on the right UNLESS the streetcar is on a one-way road IF VIOLATED 3 demerit points`
  - [HTA 166 (2)](#on-hta-166-2), [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12). Fire department vehicles going to a fire are exempt.

**Compared with the law**

- `SAME` [HTA 166 (2)](#on-hta-166-2): The Act also exempts a fire department vehicle going to a fire.
- `PENALTY` [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12): 3 demerit points (improper passing).

### 3.4.5b

> a driver SHOULD stay at least 2 m behind the rear doors of a streetcar WHEN the streetcar is stopped AND passengers are getting on or off

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing streetcars.

**Flags**

- M "stay at least two metres": The diagram's alt text calls it "the required two metres", which suggests a legal requirement.
  - `LAW_STATES`: Do not pass or come nearer than 2 m, measured back from the nearest passenger door, until the passengers are on or safely at the side of the street. Strength LAW; measure from the nearest passenger door; the duty ends when the passengers are on or at the side of the street. ([HTA 166 (1)](#on-hta-166-1))

**Law**

- `a driver MUST NOT pass a streetcar OR come nearer than 2 m to it, measured back from the nearest door passengers use, WHEN the streetcar is stopped to take on or let off passengers UNTIL the passengers have got on OR have got safely to the side of the street IF VIOLATED 3 demerit points`
  - [HTA 166 (1)](#on-hta-166-1), [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12). Not where a safety zone is designated by by-law (3.4.5c).

**Compared with the law**

- `BROADER` [HTA 166 (1)](#on-hta-166-1): The Act makes it a duty; it measures 2 m back from the nearest passenger door, lasts until the passengers are on or safely at the side of the street, and does not apply at a safety zone designated by by-law (3.4.5c).
- `PENALTY` [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12): 3 demerit points (improper passing).

### 3.4.5c

> EXCEPTION TO 3.4.5b WHEN the streetcar stop has an area set aside for passengers

EXCEPTION. Handbook: Changing positions page · Chapter 2 › Passing streetcars.

### 3.4.5d

> a driver SHOULD pass a streetcar passenger area at a [?reasonable speed] AND SHOULD WATCH FOR pedestrians making sudden or unexpected moves

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing streetcars.

**Flags**

- J "reasonable speed": No speed given.
  - `OPEN`: The Act lifts the 2 m rule at a designated safety zone (166 (1)) and sets no speed there.
- R "these areas": The source says "these areas"; read as the passenger areas in 3.4.5c.
  - `HANDBOOK`: Streetcar stops with an area set aside for passengers. None; the statement already names the area. (handbook changing-positions:040.2)
- X "safety islands and zones": Repeated on the pedestrians page, with an added caution about sudden moves.
  - `HANDBOOK`: None; the statement already joins both passages. (handbook sharing-road-other-road-users:018.2, handbook sharing-road-other-road-users:018.3)

### 3.4.6a

> a driver SHOULD NOT cut in [?closely] in front of a large vehicle WHEN returning to the lane after passing it BECAUSE this reduces the space cushion the large vehicle needs to stop [?safely]

RULE, ADVICE. Handbook: Sharing the road › Large commercial vehicles · ¶3.

_The source also calls it discourteous._

**Flags**

- J "closely": No gap given.
  - `HANDBOOK`: Move back only when the entire front of the passed vehicle is visible in the inside mirror. Could cite 2.2a step 5 instead of "closely". (handbook changing-positions:018.2)
- J "safely": Judgment term.
  - `OPEN`: Inside the reason; no duty to ground.

### 3.4.6b

> a driver SHOULD allow [?more room] WHEN passing a large vehicle

RULE, ADVICE. Handbook: Sharing the road › Large commercial vehicles · ¶3.

**Flags**

- J "more room": Comparative with no baseline.
  - `OPEN`

### 3.4.6c

> FACT a large vehicle can create heavy air turbulence that may affect the driver's control WHILE passing it

FACT. Handbook: Sharing the road › Large commercial vehicles · ¶8.

### 3.4.6d

> DEFINE a long commercial vehicle IS a double-trailer vehicle THAT can be up to 40 m long AND carries an LCV placard on its rear ALSO CALLED LCV

DEFINE. Handbook: Signs › Other signs › Long commercial vehicle (LCV) · ¶3; Signs › Other signs › Long commercial vehicle (LCV) · image.

### 3.4.6e

> a driver SHOULD anticipate the extended length AND limited speed of an LCV WHEN preparing to pass it

RULE, ADVICE. Handbook: Signs › Other signs › Long commercial vehicle (LCV) · ¶3.

### 3.4.7a

> a driver SHOULD stay [?well back] of farm machinery AND SHOULD NOT pass it UNTIL it is [?safe] to do so

RULE, ADVICE. Handbook: Sharing the road › Farm machinery · ¶2.

**Flags**

- J "well back": No distance given.
  - `OPEN`
- J "safe": Judgment term.
  - `LAW_REPEATS`: The Act gives no distance either: 148 (8) asks that the road ahead be "safely free from approaching traffic". An engineering measure (passing sight distance, OTM Book 11) was not obtained. ([HTA 148 (8)](#on-hta-148-8))

### 3.4.8a

> a driver SHOULD keep a [?safe] following distance behind a horse-drawn vehicle AND SHOULD NOT pass it UNLESS it is [?safe] to do so

RULE, ADVICE. Handbook: Sharing the road › Horse-drawn vehicles · ¶2.

**Flags**

- J "safe": Judgment term (twice).
  - `LAW_REPEATS`: Following distance: at least two seconds behind the vehicle in front (handbook, Driving along). Could use two seconds for the following distance; passing stays open. The Act says "more closely than is reasonable and prudent" (158 (1)) and "safely free from approaching traffic" (148 (8)). ([HTA 148 (8)](#on-hta-148-8), [HTA 158 (1)](#on-hta-158-1), handbook driving-along:023.2)

### 3.4.8b

> a driver SHOULD leave [?as much distance as possible] WHILE passing a horse-drawn vehicle BECAUSE passing too closely could startle the horse and make it change direction suddenly

RULE, ADVICE. Handbook: Sharing the road › Horse-drawn vehicles · ¶2.

**Flags**

- J "as much distance as possible": No distance given.
  - `OPEN`: The 1 m rule of 148 (6.1) is for bicycles only.

### 3.4.9a

> a driver SHOULD NOT pass a snow plow WHEN the snow plow is moving

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing.

**Flags**

- M "under any conditions": Absolute wording ("under any conditions") without a legal marker; the default gives SHOULD NOT.
  - `LAW_STATES`: Law only for plows in echelon on highways posted 80 km/h or more with two or more lanes in the driver’s direction (148.1 (1)). Keep 3.4.9a as advice; 3.4.9b holds the case the Act makes law. ([HTA 148.1 (1)](#on-hta-148-1-1))

### 3.4.9b

> a driver SHOULD NOT pass between snow plows WHEN several snow plows are staggered across a freeway BECAUSE there is not [?enough] room to pass [?safely] AND the ridge of wet snow can throw the vehicle out of control

RULE, ADVICE. Handbook: Night and bad weather › Snow plows · ¶2.

**Flags**

- J "enough": Judgment term.
  - `LAW_DEFINES`: The lane used to overtake is entirely clear of any part of the plows, including attachments and blades. Strength LAW on highways posted 80 km/h or more with two or more lanes in the driver’s direction, with the Act’s test in place of "enough room". ([HTA 148.1 (1)](#on-hta-148-1-1))
- J "safely": Judgment term.
  - `LAW_DEFINES`: Same test as "enough". ([HTA 148.1 (1)](#on-hta-148-1-1))

**Law**

- `a driver MUST NOT overtake a snow plow that is travelling in echelon with other plows UNLESS the lane the driver uses to overtake is entirely clear of every part of the plow, including attachments and the blade, WHEN the speed limit is 80 km/h or more AND the road has 2 or more marked lanes in the driver's direction`
  - [HTA 148.1 (1)](#on-hta-148-1-1)

**Compared with the law**

- `BROADER` [HTA 148.1 (1)](#on-hta-148-1-1): The Act bans it only on highways posted 80 km/h or more with two or more lanes in the driver’s direction, and only unless the overtaking lane is entirely clear of the plows, including their blades. The handbook words it as advice.

### 3.4.10a

> a driver SHOULD NOT pass a pilot vehicle or pace vehicle WHEN it carries the "do not pass" temporary condition sign

RULE, ADVICE. Handbook: Signs › Temporary condition signs · ¶12; Signs › Temporary condition signs · image.

**Flags**

- M "Do not pass the pilot vehicle": The section presents these signs as warnings, so no legal force; the wording is a direct prohibition.
  - `OPEN`: Reg. 615 s. 35 prescribes the Do Not Pass sign and s. 182 (2) of the Act makes drivers obey signs "erected, installed or displayed" under the regulations; whether a sign carried on a pilot vehicle is one was not settled.

### 3.4.11a

> a driver SHOULD NOT pass a vehicle WHEN the vehicle is stopped at a crosswalk BECAUSE a stopped vehicle may mean a pedestrian is crossing

RULE, ADVICE. Handbook: Sharing the road › Pedestrians · item 2.

### 3.4.12a

> FACT school bus drivers and other witnesses can report vehicles that have [?illegally passed] a school bus

FACT. Handbook: Stopping › Stopping for school buses · ¶6.

_The law behind it is 3.4.12b, from the same section of the Stopping page._

**Flags**

- G "illegally passed": Implies a prohibition on passing; the law behind it is the duty to stop in 3.4.12b.
  - `LAW_STATES`: Read "illegally passed" as "failed to stop for". The Act’s duty is to stop for the bus (175 (11) to (12.1)), not a ban on passing. ([HTA 175 (11)](#on-hta-175-11), [HTA 175 (12)](#on-hta-175-12))

### 3.4.12b

> a driver MUST stop WHEN approaching a stopped school bus with its upper alternating red lights flashing, from either direction IF VIOLATED a [?heavy] fine AND 6 demerit points for a first offence

RULE, LAW. Handbook: Stopping › Stopping for school buses · ¶2; Stopping › Stopping for school buses · ¶6.

_This duty to stop is what makes passing a stopped school bus illegal (3.4.12a)._

**Flags**

- J "heavy": The handbook says "fined heavily" and gives no amount.
  - `LAW_DEFINES`: $400 to $2,000 for a first offence (175 (17)), and 6 demerit points (O. Reg. 339/94, item 14). Replace "a heavy fine" with the amounts. ([HTA 175 (17)](#on-hta-175-17), [O. Reg. 339/94 Table, item 14](#on-reg-339-94-item-14))
- X "stop arm activated": Repeated on Sharing the road (which also counts the stop arm), the Signs page and the six-point offence table.
  - `LAW_STATES`: A stopped bus with its stop arm actuated is a reason to stop on its own. Add OR its stop arm is actuated. ([HTA 175 (11.1)](#on-hta-175-11-1), [HTA 175 (12.1)](#on-hta-175-12-1))

**Law**

- `a driver MUST stop before reaching a stopped school bus WHEN the bus has its overhead red lights flashing OR its stop arm actuated, from either direction IF VIOLATED a fine of $400 to $2,000 for a first offence AND 6 demerit points`
  - [HTA 175 (11)](#on-hta-175-11), [HTA 175 (11.1)](#on-hta-175-11-1), [HTA 175 (12)](#on-hta-175-12), [HTA 175 (12.1)](#on-hta-175-12-1), [HTA 175 (17)](#on-hta-175-17), [O. Reg. 339/94 Table, item 14](#on-reg-339-94-item-14). The demerit table lists 6 points for 175 (11) and (12), the red-light duties; it names no points for the stop-arm duties.

**Compared with the law**

- `BROADER` [HTA 175 (11)](#on-hta-175-11): Meeting the bus from the front: the Act excludes a highway with a median strip (3.4.12e).
- `NARROWER` [HTA 175 (11.1)](#on-hta-175-11-1): The Act also makes the stop arm alone a reason to stop.
- `SAME` [HTA 175 (12)](#on-hta-175-12): Approaching from the rear.
- `NARROWER` [HTA 175 (12.1)](#on-hta-175-12-1): The Act also makes the stop arm alone a reason to stop.
- `PENALTY` [HTA 175 (17)](#on-hta-175-17): $400 to $2,000 for a first offence; $1,000 to $4,000, up to six months in jail, or both, after that.
- `PENALTY` [O. Reg. 339/94 Table, item 14](#on-reg-339-94-item-14): 6 demerit points.

### 3.4.12c

> a driver SHOULD stop at least 20 m from the bus WHEN approaching a stopped school bus with its upper alternating red lights flashing from behind

RULE, ADVICE. Handbook: Stopping › Stopping for school buses · ¶2.

**Flags**

- M "stop at least 20 metres away": A bare imperative right after "You must stop"; it reads as part of the law in 3.4.12b, but the handbook does not say so.
  - `LAW_STATES`: At least 20 m before reaching the bus, from the rear, when its red lights flash or its stop arm is actuated. Strength LAW. ([HTA 175 (12.2)](#on-hta-175-12-2))

**Law**

- `a driver MUST stop at least 20 m before reaching the bus WHEN approaching from the rear a stopped school bus with its overhead red lights flashing OR its stop arm actuated IF VIOLATED a fine of $400 to $2,000 for a first offence`
  - [HTA 175 (12.2)](#on-hta-175-12-2), [HTA 175 (17)](#on-hta-175-17)

**Compared with the law**

- `NARROWER` [HTA 175 (12.2)](#on-hta-175-12-2): The Act makes it a duty, and also when only the stop arm is actuated. The handbook words it as advice.
- `PENALTY` [HTA 175 (17)](#on-hta-175-17): $400 to $2,000 for a first offence.

### 3.4.12d

> a driver SHOULD NOT go WHEN stopped for a school bus with its upper alternating red lights flashing UNTIL the bus moves OR the lights have stopped flashing

RULE, ADVICE. Handbook: Stopping › Stopping for school buses · ¶2.

**Flags**

- M "Do not go": A bare imperative that ends the duty in 3.4.12b; it reads as part of that law, but the handbook does not say so.
  - `LAW_STATES`: Strength LAW. ([HTA 175 (11)](#on-hta-175-11), [HTA 175 (11.1)](#on-hta-175-11-1), [HTA 175 (12)](#on-hta-175-12), [HTA 175 (12.1)](#on-hta-175-12-1))
- X "and its stop arm is no longer activated": Elsewhere the stop ends only when every condition holds (bus moves, lights stop, arm folds away); here either one ends it.
  - `LAW_STATES`: Wait until the bus moves, or until every signal that was on has stopped: the red lights have stopped flashing and the stop arm is no longer actuated. The statement ends the wait when either one stops; with both signals on, the Act ends it only when both have. Each signal is its own duty, each lasting until the bus moves or that signal stops. ([HTA 175 (11)](#on-hta-175-11), [HTA 175 (11.1)](#on-hta-175-11-1), handbook sharing-road-other-road-users:080.1, handbook stopping:025.3)

**Law**

- `a driver MUST NOT proceed WHEN stopped for a school bus UNTIL the bus moves OR (the overhead red lights have stopped flashing AND the stop arm is no longer actuated) IF VIOLATED a fine of $400 to $2,000 for a first offence AND 6 demerit points`
  - [HTA 175 (11)](#on-hta-175-11), [HTA 175 (11.1)](#on-hta-175-11-1), [HTA 175 (12)](#on-hta-175-12), [HTA 175 (12.1)](#on-hta-175-12-1), [HTA 175 (17)](#on-hta-175-17), [O. Reg. 339/94 Table, item 14](#on-reg-339-94-item-14). Each signal is its own duty; a signal that was not on does not have to stop.

**Compared with the law**

- `SAME` [HTA 175 (11)](#on-hta-175-11): The Act makes it a duty; the handbook words it as advice.
- `NARROWER` [HTA 175 (11.1)](#on-hta-175-11-1): When the stop arm is actuated the driver also waits until the bus moves or the arm is no longer actuated.
- `SAME` [HTA 175 (12)](#on-hta-175-12): The Act makes it a duty; the handbook words it as advice.
- `NARROWER` [HTA 175 (12.1)](#on-hta-175-12-1): When the stop arm is actuated the driver also waits until the bus moves or the arm is no longer actuated.
- `PENALTY` [HTA 175 (17)](#on-hta-175-17): $400 to $2,000 for a first offence.
- `PENALTY` [O. Reg. 339/94 Table, item 14](#on-reg-339-94-item-14): 6 demerit points for 175 (11) and (12).

### 3.4.12e

> EXCEPTION TO 3.4.12b WHEN the road has a median strip AND the driver is approaching the bus from the front

EXCEPTION. Handbook: Stopping › Stopping for school buses · ¶3.

### 3.4.13a

> a driver MUST slow down AND proceed with [?caution] WHEN approaching, in the same direction, an emergency vehicle stopped with red or red-and-blue lights flashing OR a tow truck stopped with amber lights flashing IF VIOLATED 3 demerit points

RULE, LAW. Handbook: Particular situations › Reacting to a stopped emergency vehicle or tow truck · ¶1; Keeping your licence › Table of offences › Three points · item 17.

_The offence table words it as "Failing to slow and carefully pass a stopped emergency vehicle"._

**Flags**

- J "caution": Judgment term.
  - `LAW_REPEATS`: The goal the Act states: not collide with the stopped vehicle or endanger anyone outside it, having regard to traffic, road conditions and weather. Could add the goal after "caution". The Act uses the same word and gives no speed. ([HTA 159 (2)](#on-hta-159-2), [HTA 159 (2), in force January 1, 2027](#on-hta-159-2-2027))

**Law**

- `a driver MUST slow down AND proceed with [?caution], so as not to collide with the stopped vehicle or endanger anyone outside it, WHEN approaching, on the same side of the road, an emergency vehicle stopped with red or red-and-blue lights flashing OR a tow truck stopped with amber lights flashing IF VIOLATED a fine of $400 to $2,000 for a first offence AND 3 demerit points`
  - [HTA 159 (2)](#on-hta-159-2), [HTA 159 (2), in force January 1, 2027](#on-hta-159-2-2027), [HTA 159 (6)](#on-hta-159-6), [O. Reg. 339/94 Table, item 36.2](#on-reg-339-94-item-36-2). From January 1, 2027 the Act also covers a stopped work-related vehicle with amber flashing lamps.

**Compared with the law**

- `SAME` [HTA 159 (2)](#on-hta-159-2): The version in force until December 31, 2026.
- `NARROWER` [HTA 159 (2), in force January 1, 2027](#on-hta-159-2-2027): From January 1, 2027 the Act also covers a stopped work-related vehicle with amber flashing lamps.
- `PENALTY` [HTA 159 (6)](#on-hta-159-6): $400 to $2,000 for a first offence.
- `PENALTY` [O. Reg. 339/94 Table, item 36.2](#on-reg-339-94-item-36-2): 3 demerit points.

### 3.4.13b

> a driver MUST move into a lane away from the stopped emergency vehicle or tow truck, [?if safe to do so] WHEN the road has 2 or more lanes in the driver's direction IF VIOLATED 3 demerit points

RULE, LAW. Handbook: Particular situations › Reacting to a stopped emergency vehicle or tow truck · ¶3; Keeping your licence › Table of offences › Three points · item 18.

**Flags**

- J "if safe to do so": Judgment term.
  - `LAW_REPEATS`: The Act says "if the movement can be made safely". ([HTA 159 (3)](#on-hta-159-3), [HTA 159 (3), in force January 1, 2027](#on-hta-159-3-2027))
- X "where possible": The offence table qualifies the same duty with "where possible" instead of "if safe to do so".
  - `LAW_STATES`: Keep "if safe to do so"; the handbook’s offence table says "where possible", the regulation’s says "if safe to do so". ([HTA 159 (3)](#on-hta-159-3), [O. Reg. 339/94 Table, item 36.3](#on-reg-339-94-item-36-3), handbook keeping-your-drivers-licence:129.1)

**Law**

- `a driver in the same lane as the stopped vehicle or the lane next to it MUST move into another lane [?if safe to do so] WHEN an emergency vehicle with red or red-and-blue lights flashing OR a tow truck with amber lights flashing is stopped AND the road has 2 or more lanes in the driver's direction IF VIOLATED a fine of $400 to $2,000 for a first offence AND 3 demerit points`
  - [HTA 159 (3)](#on-hta-159-3), [HTA 159 (3), in force January 1, 2027](#on-hta-159-3-2027), [HTA 159 (6)](#on-hta-159-6), [O. Reg. 339/94 Table, item 36.3](#on-reg-339-94-item-36-3). The Act says "if the movement can be made safely". From January 1, 2027 it also covers a stopped work-related vehicle with amber flashing lamps.

**Compared with the law**

- `BROADER` [HTA 159 (3)](#on-hta-159-3): The Act asks only a driver in the lane of the stopped vehicle or the lane next to it to move over. The version in force until December 31, 2026.
- `NARROWER` [HTA 159 (3), in force January 1, 2027](#on-hta-159-3-2027): From January 1, 2027 the Act also covers a stopped work-related vehicle with amber flashing lamps.
- `PENALTY` [HTA 159 (6)](#on-hta-159-6): $400 to $2,000 for a first offence.
- `PENALTY` [O. Reg. 339/94 Table, item 36.3](#on-reg-339-94-item-36-3): 3 demerit points.

### 3.5.1a

> FACT a vehicle towing a trailer cannot accelerate as quickly AND needs more space BECAUSE it is much longer

FACT. Handbook: Towing › Passing · ¶1.

### 3.5.1b

> a driver towing a trailer SHOULD pass ONLY IF the driver has [?enough] time and room to complete the pass

RULE, ADVICE. Handbook: Towing › Passing · ¶1.

**Flags**

- J "enough": Judgment term.
  - `LAW_REPEATS`: The Act gives no distance either: 148 (8) asks that the road ahead be "safely free from approaching traffic". An engineering measure (passing sight distance, OTM Book 11) was not obtained. ([HTA 148 (8)](#on-hta-148-8))

### 3.5.1c

> a driver towing a trailer SHOULD allow [?more room] before moving back into the lane AND SHOULD NOT cut back in [?too soon] WHEN returning to the lane after passing BECAUSE this can make the trailer sway and become hard to control

RULE, ADVICE. Handbook: Towing › Passing · ¶1.

**Flags**

- J "more room": Comparative with no baseline.
  - `OPEN`
- J "too soon": No gap given.
  - `OPEN`: The inside-mirror test of 2.2a may not work when a trailer blocks the inside mirror.

### 3.5.2a

> a driver towing a trailer SHOULD signal, pull over AND let the other vehicles pass WHEN the driver is holding up a line of traffic

RULE, ADVICE. Handbook: Towing › Being passed · ¶1.

**Flags**

- R "If you are holding up a line of traffic": Worded for any driver, but placed in the towing section; scoped here to towing.
  - `LAW_STATES`: Scope: every driver being overtaken, not only drivers towing. The Act puts the duty to turn out to the right and let the faster vehicle pass on every driver (148 (2)). ([HTA 148 (2)](#on-hta-148-2))

**Law**

- `a driver being overtaken MUST turn out to the right AND let the overtaking vehicle pass WHEN a vehicle travelling at a greater speed overtakes the driver IF VIOLATED a fine of $150 to $1,000 AND 2 demerit points`
  - [HTA 148 (2)](#on-hta-148-2), [HTA 148 (2.1)](#on-hta-148-2-1), [O. Reg. 339/94 Table, item 22](#on-reg-339-94-item-22). Every driver who is overtaken, towing or not (3.6.1a).

**Compared with the law**

- `NARROWER` [HTA 148 (2)](#on-hta-148-2): The Act puts this duty on every driver who is overtaken by a faster vehicle, not only drivers towing. The handbook words it as advice.
- `PENALTY` [HTA 148 (2.1)](#on-hta-148-2-1): $150 to $1,000.
- `PENALTY` [O. Reg. 339/94 Table, item 22](#on-reg-339-94-item-22): 2 demerit points (failing to share road).

### 3.5.2b

> FACT fast-moving trucks and buses create a strong air disturbance behind them that can whip a trailer to the side WHEN they pass

FACT. Handbook: Towing › Being passed · ¶1.

### 3.5.2c

> a driver towing a trailer SHOULD NOT brake AND SHOULD steer the vehicle and trailer [?carefully] back into position WHEN a passing bus or truck pushes the trailer out of position

RULE, ADVICE. Handbook: Towing › Being passed · ¶1.

_"A slight increase in speed may help" is a possibility, not a permission, so it stays as a note._

**Flags**

- J "carefully": Judgment term.
  - `OPEN`

### 3.6.1a

> a driver being passed SHOULD move to the right AND let the faster vehicle pass [?in safety] WHEN faster traffic wants to pass

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing; Sample test questions › Intro · ¶6; Sample test questions › Intro · item 4.

_Two of its sources come from the sample test page (question 5); keep them out of the rule set if that page is used for evaluation._

**Flags**

- M "move to the right": A sample test question says "you must" move right, and the offence table lists "Failing to share the road"; the text itself only advises.
  - `LAW_STATES`: Turn out to the right and allow the overtaking vehicle to pass. Strength LAW. ([HTA 148 (2)](#on-hta-148-2))
- J "in safety": Judgment term.
  - `LAW_STATES`: The Act’s duty has no such qualifier; drop it or keep it as advice. ([HTA 148 (2)](#on-hta-148-2))

**Law**

- `a driver being overtaken MUST turn out to the right AND let the overtaking vehicle pass WHEN a vehicle travelling at a greater speed overtakes the driver IF VIOLATED a fine of $150 to $1,000 AND 2 demerit points`
  - [HTA 148 (2)](#on-hta-148-2), [HTA 148 (2.1)](#on-hta-148-2-1), [O. Reg. 339/94 Table, item 22](#on-reg-339-94-item-22). The Act has no "in safety" qualifier.

**Compared with the law**

- `SAME` [HTA 148 (2)](#on-hta-148-2): The Act makes it a duty; the handbook words it as advice.
- `PENALTY` [HTA 148 (2.1)](#on-hta-148-2-1): $150 to $1,000.
- `PENALTY` [O. Reg. 339/94 Table, item 22](#on-reg-339-94-item-22): 2 demerit points (failing to share road).

### 3.6.1b

> a driver being passed MUST NOT speed up WHILE another driver is trying to pass BECAUSE it is dangerous

RULE, LAW. Handbook: Changing positions page · Chapter 2 › Passing.

### 3.6.1c

> a driver MUST NOT drive to prevent another vehicle from passing IF VIOLATED [?sanctions for dangerous driving]

RULE, LAW. Handbook: Losing your licence › Sanctions – dangerous behaviours · item 3.

**Flags**

- R "sanctions for dangerous driving": The passage lists the behaviour but does not state its sanction.
  - `LAW_DEFINES`: A stunt under s. 172 of the Act (O. Reg. 455/07, s. 3): $2,000 to $10,000, up to six months in jail, or both (172 (2)); licence suspended for at least one year on a first conviction (172 (3)); at the roadside, a 30-day licence suspension and a 14-day vehicle impoundment (172 (9), (10)); 6 demerit points (O. Reg. 339/94, item 3). Replace the placeholder with the sanction. ([HTA 172 (1)](#on-hta-172-1), [HTA 172 (10)](#on-hta-172-10), [HTA 172 (2)](#on-hta-172-2), [HTA 172 (3)](#on-hta-172-3), [HTA 172 (9)](#on-hta-172-9), [O. Reg. 339/94 Table, item 3](#on-reg-339-94-item-3), [O. Reg. 455/07 3](#on-reg-455-07-3), [O. Reg. 455/07 3, para. 8, subpara. i](#on-reg-455-07-3-8-i))

**Law**

- `a driver MUST NOT drive in a manner that indicates an intention to prevent another vehicle from passing IF VIOLATED a fine of $2,000 to $10,000 OR up to 6 months in jail OR both AND a licence suspension of at least 1 year for a first conviction AND 6 demerit points AND, at the roadside, a 30-day licence suspension AND a 14-day vehicle impoundment`
  - [HTA 172 (1)](#on-hta-172-1), [HTA 172 (10)](#on-hta-172-10), [HTA 172 (2)](#on-hta-172-2), [HTA 172 (3)](#on-hta-172-3), [HTA 172 (9)](#on-hta-172-9), [O. Reg. 339/94 Table, item 3](#on-reg-339-94-item-3), [O. Reg. 455/07 3](#on-reg-455-07-3), [O. Reg. 455/07 3, para. 8, subpara. i](#on-reg-455-07-3-8-i). A stunt under s. 172 of the Act.

**Compared with the law**

- `SAME` [HTA 172 (1)](#on-hta-172-1)
- `SAME` [O. Reg. 455/07 3](#on-reg-455-07-3): Makes the driving behaviours it lists stunts for s. 172 of the Act.
- `SAME` [O. Reg. 455/07 3, para. 8, subpara. i](#on-reg-455-07-3-8-i): Driving to prevent another vehicle from passing is one of the driving behaviours the regulation lists for s. 172 of the Act.
- `PENALTY` [HTA 172 (10)](#on-hta-172-10): At the roadside: vehicle impounded for 14 days.
- `PENALTY` [HTA 172 (2)](#on-hta-172-2): $2,000 to $10,000, up to six months in jail, or both.
- `PENALTY` [HTA 172 (3)](#on-hta-172-3): Licence suspended for at least one year on a first conviction, three on a second, indefinitely after that.
- `PENALTY` [HTA 172 (9)](#on-hta-172-9): At the roadside: licence suspended for 30 days.
- `PENALTY` [O. Reg. 339/94 Table, item 3](#on-reg-339-94-item-3): 6 demerit points.

### 3.6.1d

> a driver in [?slow traffic] MUST keep right WHEN on a multi-lane road where a "slower traffic keep right" sign is posted

RULE, LAW. Handbook: Signs › Regulatory signs · ¶20; Signs › Regulatory signs · image.

_The caption of a regulatory sign. It is the legal side of keeping right so faster traffic can pass (2.1d, 3.6.1a)._

**Flags**

- J "slow traffic": No speed given; slow compared with the traffic around it.
  - `LAW_DEFINES`: Travelling at less than the normal speed of traffic at that time and place. Replace "slow traffic" with this. ([HTA 147 (1)](#on-hta-147-1))

**Law**

- `a driver travelling at less than the normal speed of traffic at that time and place MUST keep right WHEN on a multi-lane road where a "slower traffic keep right" sign is posted`
  - [HTA 147 (1)](#on-hta-147-1), [HTA 154 (1) (c)](#on-hta-154-1-c). 147 (1) asks this on any road, signed or not, where practicable.

**Compared with the law**

- `NARROWER` [HTA 147 (1)](#on-hta-147-1): The Act asks a slower vehicle to keep right, where practicable, on any road, signed or not.
- `SAME` [HTA 154 (1) (c)](#on-hta-154-1-c): Where a lane is designated by official signs, drivers must obey the signs.
- `PENALTY` [HTA 147 (3)](#on-hta-147-3): $150 to $1,000.
- `PENALTY` [O. Reg. 339/94 Table, item 13](#on-reg-339-94-item-13): 3 demerit points (s. 154).

### 3.6.2a

> a driver being passed SHOULD WATCH FOR oncoming traffic AND SHOULD move closer to the right side of the lane WHEN on an undivided road AND the passing driver has pulled into the opposite lane

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing.

### 3.6.2b

> a driver being passed SHOULD be ready to slow down WHEN on an undivided road AND the passing driver is in the opposite lane BECAUSE slowing down lets the passing driver get back in front sooner and prevents a collision

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing.

### 3.6.3a

> a truck driver MUST NOT drive in the far-left lane WHEN on a high-speed road with 3 or more lanes in each direction where trucks are barred from that lane

RULE, LAW. Handbook: Changing positions page · Chapter 2 › Passing; Freeway driving › Driving along a freeway · ¶5.

_A rule for truck drivers. The passing rule for other drivers (3.6.3c) depends on it._

**Flags**

- S "many high-speed roads": The source says "many" such roads without saying which.
  - `LAW_DEFINES`: The portions of highways described in the Schedules to Reg. 608. Replace "a high-speed road with 3 or more lanes" with the scheduled portions, and "truck" with a commercial motor vehicle over 6.5 m long. ([Reg. 608 1 (1)](#on-reg-608-1-1))
- X "many freeways": The Freeway page says "many freeways"; Changing positions says "many high-speed roads".
  - `LAW_DEFINES`: The portions of highways described in the Schedules to Reg. 608. Both handbook wordings give way to the Schedules. ([Reg. 608 1 (1)](#on-reg-608-1-1))

**Law**

- `a driver of a commercial motor vehicle more than 6.5 m long, alone or with a towed vehicle, MUST NOT drive in the left lane WHEN on a highway portion described in the Schedules to Reg. 608 AND the left lane is not a high occupancy vehicle lane`
  - [Reg. 608 1 (1)](#on-reg-608-1-1). Subject to s. 1 (2), which was not pulled.
- `a driver of a commercial motor vehicle more than 6.5 m long, alone or with a towed vehicle, MUST NOT drive in the lane next to the high occupancy vehicle lane WHEN on a highway portion described in the Schedules to Reg. 608 AND the left lane is a high occupancy vehicle lane`
  - [Reg. 608 1 (1)](#on-reg-608-1-1)

**Compared with the law**

- `DIFFERENT` [Reg. 608 1 (1)](#on-reg-608-1-1): The regulation covers a commercial motor vehicle, or a combination, over 6.5 m long, not any truck; only on the highway portions in its Schedules, not any high-speed road with three or more lanes; and where the left lane is an HOV lane, the lane next to it.

### 3.6.3b

> a truck driver MUST use the lane next to the far-left lane for passing WHEN on a high-speed road with 3 or more lanes in each direction where trucks are barred from the far-left lane

RULE, LAW. Handbook: Freeway driving › Driving along a freeway · ¶5; Changing positions page · Chapter 2 › Passing.

**Law**

- `a driver of a commercial motor vehicle more than 6.5 m long, alone or with a towed vehicle, MUST NOT drive in the left lane WHEN on a highway portion described in the Schedules to Reg. 608 AND the left lane is not a high occupancy vehicle lane`
  - [Reg. 608 1 (1)](#on-reg-608-1-1). The regulation only bars the left lane; that trucks pass in the next lane is the handbook's reading of it.

**Compared with the law**

- `DIFFERENT` [Reg. 608 1 (1)](#on-reg-608-1-1): The regulation bars the left lane; using the next lane to pass is the handbook’s reading of it.

### 3.6.3c

> a driver in the truck passing lane SHOULD move into the right-hand lane [?as soon as the driver can] WHEN a truck wants to pass

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing.

**Flags**

- J "as soon as the driver can": No time given (the handbook says "as soon as you can").
  - `OPEN`: The Act makes moving right for a faster vehicle a duty (148 (2)) but gives no time.

**Law**

- `a driver in the truck passing lane MUST move into the right-hand lane [?as soon as the driver can] WHEN a truck travelling at a greater speed overtakes the driver IF VIOLATED a fine of $150 to $1,000 AND 2 demerit points`
  - [HTA 148 (2)](#on-hta-148-2), [HTA 148 (2.1)](#on-hta-148-2-1), [O. Reg. 339/94 Table, item 22](#on-reg-339-94-item-22). The Act gives no time.

**Compared with the law**

- `SAME` [HTA 148 (2)](#on-hta-148-2): The Act makes moving right for a faster vehicle a duty; the handbook words it as advice.
- `PENALTY` [HTA 148 (2.1)](#on-hta-148-2-1): $150 to $1,000.
- `PENALTY` [O. Reg. 339/94 Table, item 22](#on-reg-339-94-item-22): 2 demerit points (failing to share road).

## Provisions

<a id="on-hta-140-3"></a>**R.S.O. 1990, c. H.8, s. 140 (3), Passing moving vehicles within 30 metres of pedestrian crossover** · [hta.txt, line 8717](../../../statutes/on/hta/hta.txt#L8717) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (3) When a vehicle is approaching a pedestrian crossover and is within 30 metres of it, the driver of any other vehicle approaching from the rear shall not allow the front extremity of his or her vehicle to pass beyond the front extremity of the other vehicle.

<a id="on-hta-142-1"></a>**R.S.O. 1990, c. H.8, s. 142 (1), Signal for left or right turn** · [hta.txt, line 8762](../../../statutes/on/hta/hta.txt#L8762) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> 142 (1) The driver or operator of a vehicle upon a highway before turning to the left or right at any intersection or into a private road or driveway or from one lane for traffic to another lane for traffic or to leave the roadway shall first see that the movement can be made in safety, and if the operation of any other vehicle may be affected by the movement shall give a signal plainly visible to the driver or operator of the other vehicle of the intention to make the movement.

<a id="on-hta-147-1"></a>**R.S.O. 1990, c. H.8, s. 147 (1), Slow vehicles to travel on right side** · [hta.txt, line 9002](../../../statutes/on/hta/hta.txt#L9002) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> 147 (1) Any vehicle travelling upon a roadway at less than the normal speed of traffic at that time and place shall, where practicable, be driven in the right-hand lane then available for traffic or as close as practicable to the right hand curb or edge of the roadway.

<a id="on-hta-147-3"></a>**R.S.O. 1990, c. H.8, s. 147 (3), Offence** · [hta.txt, line 9010](../../../statutes/on/hta/hta.txt#L9010) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (3) Every person who, while driving a motor vehicle, contravenes this section is guilty of an offence and on conviction is liable to a fine of not less than $150 and not more than $1,000.

<a id="on-hta-148-2"></a>**R.S.O. 1990, c. H.8, s. 148 (2), Vehicles or equestrians overtaken** · [hta.txt, line 9018](../../../statutes/on/hta/hta.txt#L9018) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (2) Every person in charge of a vehicle or on horseback on a highway who is overtaken by a vehicle or equestrian travelling at a greater speed shall turn out to the right and allow the overtaking vehicle or equestrian to pass.

<a id="on-hta-148-2-1"></a>**R.S.O. 1990, c. H.8, s. 148 (2.1), Offence** · [hta.txt, line 9020](../../../statutes/on/hta/hta.txt#L9020) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (2.1) Every person who, while driving a motor vehicle, contravenes subsection (2) is guilty of an offence and on conviction is liable to a fine of not less than $150 and not more than $1,000.

<a id="on-hta-148-6-1"></a>**R.S.O. 1990, c. H.8, s. 148 (6.1), Bicycles overtaken** · [hta.txt, line 9030](../../../statutes/on/hta/hta.txt#L9030) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (6.1) Every person in charge of a motor vehicle on a highway who is overtaking a person travelling on a bicycle shall, as nearly as may be practicable, leave a distance of not less than one metre between the bicycle and the motor vehicle and shall maintain that distance until safely past the bicycle.

<a id="on-hta-148-6-2"></a>**R.S.O. 1990, c. H.8, s. 148 (6.2), Bicycles overtaken** · [hta.txt, line 9032](../../../statutes/on/hta/hta.txt#L9032) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (6.2) The one metre distance required by subsection (6.1) refers to the distance between the extreme right side of the motor vehicle and the extreme left side of the bicycle, including all projections and attachments.

<a id="on-hta-148-8"></a>**R.S.O. 1990, c. H.8, s. 148 (8), Passing vehicle going in same direction** · [hta.txt, line 9036](../../../statutes/on/hta/hta.txt#L9036) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (8) No person in charge of a vehicle shall pass or attempt to pass another vehicle going in the same direction on a highway unless the roadway, (a) in front of and to the left of the vehicle to be passed is safely free from approaching traffic; and (b) to the left of the vehicle passing or attempting to pass is safely free from overtaking traffic.

<a id="on-hta-148-1-1"></a>**R.S.O. 1990, c. H.8, s. 148.1 (1), No overtaking a snow plow** · [hta.txt, line 9043](../../../statutes/on/hta/hta.txt#L9043) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> 148.1 (1) On a highway on which the speed limit is 80 kilometres per hour or more and which is divided into clearly marked lanes for traffic, no person shall, while travelling in a direction that has two or more such lanes, overtake a snow plow that is travelling in echelon with another plow or plows unless the lane of travel that is used by the overtaking vehicle to overtake the snow plow is entirely clear of any part of the snow plow, including any part of an attachment or the plow blade.

<a id="on-hta-149-1"></a>**R.S.O. 1990, c. H.8, s. 149 (1), Driving to left of centre prohibited under certain conditions** · [hta.txt, line 9052](../../../statutes/on/hta/hta.txt#L9052) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> 149 (1) No vehicle shall be driven or operated to the left of the centre of a roadway designed for one or more lanes of traffic in each direction, (a) when approaching the crest of a grade or upon a curve in the roadway or within 30 metres of a bridge, viaduct or tunnel where the driver’s view is obstructed within that distance so as to create a potential hazard in the event another vehicle might approach from the opposite direction; or (b) when approaching within 30 metres of a level railway crossing.

<a id="on-hta-149-2"></a>**R.S.O. 1990, c. H.8, s. 149 (2), Exception** · [hta.txt, line 9056](../../../statutes/on/hta/hta.txt#L9056) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (2) Subsection (1) does not apply, (a) on a highway divided into clearly marked lanes where there are more such lanes for traffic in one direction than in the other direction; (b) to a road service vehicle where precautions are taken to eliminate the hazard; or (c) on a highway while it is designated for the use of one-way traffic.

<a id="on-hta-150-1"></a>**R.S.O. 1990, c. H.8, s. 150 (1), Passing to right of vehicle** · [hta.txt, line 9063](../../../statutes/on/hta/hta.txt#L9063) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> 150 (1) The driver of a motor vehicle may overtake and pass to the right of another vehicle only where the movement can be made in safety and, (a) the vehicle overtaken is making or about to make a left turn or its driver has signalled his or her intention to make a left turn; (b) is made on a highway with unobstructed pavement of sufficient width for two or more lines of vehicles in each direction; or (c) is made on a highway designated for the use of one-way traffic only.

<a id="on-hta-150-2"></a>**R.S.O. 1990, c. H.8, s. 150 (2), Driving off roadway prohibited** · [hta.txt, line 9068](../../../statutes/on/hta/hta.txt#L9068) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (2) No driver of a motor vehicle shall overtake and pass another vehicle by driving off the roadway.

<a id="on-hta-150-3-a"></a>**R.S.O. 1990, c. H.8, s. 150 (3) (a), Non-application of subs. (2)** · [hta.txt, line 9070](../../../statutes/on/hta/hta.txt#L9070) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (3) Subsection (2) does not apply to, (a) a motor vehicle overtaking and passing to the right of another vehicle where the shoulder to the right of the roadway is paved and the vehicle overtaken is making or about to make a left turn or its driver has signalled his or her intention to make a left turn;

<a id="on-hta-154-1-a"></a>**R.S.O. 1990, c. H.8, s. 154 (1) (a), Where highway divided into lanes** · [hta.txt, line 9117](../../../statutes/on/hta/hta.txt#L9117) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (a) a vehicle shall not be driven from one lane to another lane or to the shoulder or from the shoulder to a lane unless the driver first ascertains that it can be done safely;

<a id="on-hta-154-1-b"></a>**R.S.O. 1990, c. H.8, s. 154 (1) (b), Where highway divided into lanes** · [hta.txt, line 9118](../../../statutes/on/hta/hta.txt#L9118) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (b) in the case of a highway that is divided into three lanes, a vehicle shall not be driven in the centre lane except when overtaking and passing another vehicle where the roadway is clearly visible and the centre lane is clear of traffic within a reasonable safe distance, or in preparation for a left turn, or where the centre lane is at the time designated for the use of traffic moving in the direction in which the vehicle is proceeding and official signs are erected to indicate the designation;

<a id="on-hta-154-1-c"></a>**R.S.O. 1990, c. H.8, s. 154 (1) (c), Where highway divided into lanes** · [hta.txt, line 9119](../../../statutes/on/hta/hta.txt#L9119) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (c) any lane may be designated for slowly moving traffic, traffic moving in a particular direction or classes or types of vehicles and, despite section 141, where a lane is so designated and official signs indicating the designation are erected, every driver shall obey the instructions on the official signs.

<a id="on-hta-158-1"></a>**R.S.O. 1990, c. H.8, s. 158 (1), Headway of motor vehicles, generally** · [hta.txt, line 9194](../../../statutes/on/hta/hta.txt#L9194) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> 158 (1) The driver of a motor vehicle or street car shall not follow another vehicle or street car more closely than is reasonable and prudent having due regard for the speed of the vehicle and the traffic on and the conditions of the highway.

<a id="on-hta-159-2"></a>**R.S.O. 1990, c. H.8, s. 159 (2), Slow down on approaching stopped emergency vehicle or tow truck** (until 2027-01-01) · [hta.txt, line 9203](../../../statutes/on/hta/hta.txt#L9203) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (2) Upon approaching an emergency vehicle with its lamp producing intermittent flashes of red light or red and blue light or a tow truck with its lamp producing intermittent flashes of amber light that is stopped on a highway, the driver of a vehicle travelling on the same side of the highway shall slow down and proceed with caution, having due regard for traffic on and the conditions of the highway and the weather, to ensure that the driver does not collide with the emergency vehicle or tow truck or endanger any person outside of the emergency vehicle or tow truck.

<a id="on-hta-159-2-2027"></a>**R.S.O. 1990, c. H.8, s. 159 (2), in force January 1, 2027, Slow down on approaching specified stopped vehicles** (in force from 2027-01-01) · [hta.txt, line 9237](../../../statutes/on/hta/hta.txt#L9237) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (2) If any of the following vehicles is stopped on a highway, the driver of a vehicle travelling on the same side of the highway shall, upon approaching the stopped vehicle, slow down and proceed with caution, having due regard for traffic on and the conditions of the highway and the weather, to ensure that the driver does not collide with the stopped vehicle or endanger any person outside of the stopped vehicle: 1. An emergency vehicle with its lamp producing intermittent flashes of red light or red and blue light. 2. A tow truck with its lamp producing intermittent flashes of amber light. 3. A work-related vehicle with its lamp producing intermittent flashes of amber light.

<a id="on-hta-159-3"></a>**R.S.O. 1990, c. H.8, s. 159 (3), Slow down on approaching stopped emergency vehicle or tow truck** (until 2027-01-01) · [hta.txt, line 9205](../../../statutes/on/hta/hta.txt#L9205) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (3) Upon approaching an emergency vehicle with its lamp producing intermittent flashes of red light or red and blue light or a tow truck with its lamp producing intermittent flashes of amber light that is stopped on a highway with two or more lanes of traffic on the same side of the highway as the side on which the emergency vehicle or tow truck is stopped, the driver of a vehicle travelling in the same lane that the emergency vehicle or tow truck is stopped in or in a lane that is adjacent to the emergency vehicle or tow truck, in addition to slowing down and proceeding with caution as required by subsection (2), shall move into another lane if the movement can be made safely.

<a id="on-hta-159-3-2027"></a>**R.S.O. 1990, c. H.8, s. 159 (3), in force January 1, 2027, Same** (in force from 2027-01-01) · [hta.txt, line 9242](../../../statutes/on/hta/hta.txt#L9242) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (3) If any of the vehicles listed in subsection (2) is stopped on a highway with two or more lanes of traffic on the same side of the highway as the side on which the vehicle is stopped, the driver of a vehicle travelling in the same lane as the stopped vehicle or in a lane that is adjacent to the stopped vehicle, in addition to slowing down and proceeding with caution as required by subsection (2), shall, upon approaching the stopped vehicle, move into another lane if the movement can be made safely.

<a id="on-hta-159-6"></a>**R.S.O. 1990, c. H.8, s. 159 (6), Offence** · [hta.txt, line 9211](../../../statutes/on/hta/hta.txt#L9211) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (6) Every person who contravenes subsection (1), (2), (3) or (4) is guilty of an offence and on conviction is liable, (a) for a first offence, to a fine of not less than $400 and not more than $2,000; and (b) for each subsequent offence, to a fine of not less than $1,000 and not more than $4,000 or to imprisonment for a term of not more than six months, or to both.

<a id="on-hta-166-1"></a>**R.S.O. 1990, c. H.8, s. 166 (1), Standing street car, etc.** · [hta.txt, line 9308](../../../statutes/on/hta/hta.txt#L9308) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> 166 (1) Where a person in charge of a vehicle or on horseback or leading a horse on a highway overtakes a street car or a car of an electric railway, operated in or near the centre of the roadway, which is stationary for the purpose of taking on or discharging passengers, he or she shall not pass the car or approach nearer than 2 metres measured back from the nearest door of the car that the person is approaching and through which passengers may get on or off until the passengers have got on or got safely to the side of the street, as the case may be, but this subsection does not apply where a safety zone has been set aside and designated by a by-law passed under section 9, 10 or 11 of the Municipal Act, 2001 or under section 7 or 8 of the City of Toronto Act, 2006.

<a id="on-hta-166-2"></a>**R.S.O. 1990, c. H.8, s. 166 (2), Prohibition as to passing street cars on left-hand side** · [hta.txt, line 9310](../../../statutes/on/hta/hta.txt#L9310) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (2) No person in charge of a vehicle or on horseback or leading a horse, overtaking a street car or the car of an electric railway, operated in or near the centre of the roadway, which is stationary or in motion, shall pass on the left side of the car, having reference to the direction in which the car is travelling, but this subsection does not apply to a fire department vehicle while proceeding to a fire or answering a fire alarm call or where the street car or car of an electric railway is being operated on a highway designated for the use of one-way traffic.

<a id="on-hta-172-1"></a>**R.S.O. 1990, c. H.8, s. 172 (1), Racing, stunts, etc., prohibited** · [hta.txt, line 9385](../../../statutes/on/hta/hta.txt#L9385) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> 172 (1) No person shall drive a motor vehicle on a highway in a race or contest, on a bet or wager or while performing a stunt.

<a id="on-hta-172-10"></a>**R.S.O. 1990, c. H.8, s. 172 (10), Administrative 14-day vehicle impoundment** · [hta.txt, line 9416](../../../statutes/on/hta/hta.txt#L9416) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (10) Upon a motor vehicle being detained under clause (8) (b), the motor vehicle shall, at the cost of and risk to its owner, (a) be removed to an impound facility as directed by a police officer; and (b) be impounded for 14 days from the day it was detained under clause (8) (b).

<a id="on-hta-172-2"></a>**R.S.O. 1990, c. H.8, s. 172 (2), Fine or imprisonment** · [hta.txt, line 9387](../../../statutes/on/hta/hta.txt#L9387) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (2) Every person who contravenes subsection (1) is guilty of an offence and on conviction is liable to a fine of not less than $2,000 and not more than $10,000 or to imprisonment for a term of not more than six months, or to both.

<a id="on-hta-172-3"></a>**R.S.O. 1990, c. H.8, s. 172 (3), Suspension** · [hta.txt, line 9389](../../../statutes/on/hta/hta.txt#L9389) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (3) In addition to the penalty imposed under subsection (2), the driver’s licence of a person convicted of a contravention of subsection (1) is suspended, (a) on a first conviction under this section, for a minimum of one year; (b) on a second conviction under this section, for a minimum of three years; and (c) on a third or subsequent conviction under this section, indefinitely.

<a id="on-hta-172-9"></a>**R.S.O. 1990, c. H.8, s. 172 (9), Administrative 30-day licence suspension** · [hta.txt, line 9414](../../../statutes/on/hta/hta.txt#L9414) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (9) Upon a request being made under clause (8) (a), the person to whom the request is made shall forthwith surrender their driver’s licence to the police officer and, whether or not the person is unable or fails to surrender the licence to the police officer, the driver’s licence is suspended for a period of 30 days from the day the request is made.

<a id="on-hta-175-11"></a>**R.S.O. 1990, c. H.8, s. 175 (11), Duty of drivers when school bus stopped** · [hta.txt, line 9561](../../../statutes/on/hta/hta.txt#L9561) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (11) Every driver or street car operator, when meeting on a highway, other than a highway with a median strip, a stopped school bus that has its overhead red signal-lights flashing, shall stop before reaching the bus and shall not proceed until the bus moves or the overhead red signal-lights have stopped flashing.

<a id="on-hta-175-11-1"></a>**R.S.O. 1990, c. H.8, s. 175 (11.1), Duty of drivers when school bus stopped** · [hta.txt, line 9563](../../../statutes/on/hta/hta.txt#L9563) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (11.1) Every driver or street car operator, when meeting on a highway, other than a highway with a median strip, a stopped school bus that has its stop arm actuated, shall stop before reaching the bus and shall not proceed until the bus moves or the stop arm is no longer actuated.

<a id="on-hta-175-12"></a>**R.S.O. 1990, c. H.8, s. 175 (12), Duty of drivers when school bus stopped** · [hta.txt, line 9565](../../../statutes/on/hta/hta.txt#L9565) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (12) Every driver or street car operator on a highway, when approaching from the rear a stopped school bus that has its overhead red signal-lights flashing, shall stop and shall not proceed until the bus moves or the overhead red signal-lights have stopped flashing.

<a id="on-hta-175-12-1"></a>**R.S.O. 1990, c. H.8, s. 175 (12.1), Duty of drivers when school bus stopped** · [hta.txt, line 9567](../../../statutes/on/hta/hta.txt#L9567) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (12.1) Every driver or street car operator on a highway, when approaching from the rear a stopped school bus that has its stop arm actuated, shall stop and shall not proceed until the bus moves or the stop arm is no longer actuated.

<a id="on-hta-175-12-2"></a>**R.S.O. 1990, c. H.8, s. 175 (12.2), Duty of drivers when school bus stopped** · [hta.txt, line 9569](../../../statutes/on/hta/hta.txt#L9569) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (12.2) Every driver or street car operator on a highway, when approaching from the rear a stopped school bus that has its overhead red signal-lights flashing, or that has its stop arm actuated, shall stop at least 20 metres before reaching the bus.

<a id="on-hta-175-17"></a>**R.S.O. 1990, c. H.8, s. 175 (17), Penalty** · [hta.txt, line 9589](../../../statutes/on/hta/hta.txt#L9589) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (17) Every person who contravenes subsection (11), (11.1), (12), (12.1) or (12.2) is guilty of an offence and on conviction is liable, (a) for a first offence, to a fine of not less than $400 and not more than $2,000; and (b) for each subsequent offence, to a fine of not less than $1,000 and not more than $4,000 or to imprisonment for a term of not more than six months, or to both.

<a id="on-hta-182-2"></a>**R.S.O. 1990, c. H.8, s. 182 (2), Signs to be obeyed** · [hta.txt, line 9703](../../../statutes/on/hta/hta.txt#L9703) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (2) Every driver or operator of a vehicle or street car shall obey the instructions or directions indicated on any sign so erected, installed or displayed.

<a id="on-hta-214-1"></a>**R.S.O. 1990, c. H.8, s. 214 (1), General penalty** · [hta.txt, line 10875](../../../statutes/on/hta/hta.txt#L10875) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> 214 (1) Every person who contravenes this Act or any regulation is guilty of an offence and on conviction, where a penalty for the contravention is not otherwise provided for herein, is liable to a fine of not less than $60 and not more than $1,000.

<a id="on-hta-75-4"></a>**R.S.O. 1990, c. H.8, s. 75 (4), Unnecessary noise** · [hta.txt, line 6452](../../../statutes/on/hta/hta.txt#L6452) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (4) A person having the control or charge of a motor vehicle shall not sound any bell, horn or other signalling device so as to make an unreasonable noise, and a driver of any motor vehicle shall not permit any unreasonable amount of smoke to escape from the motor vehicle, nor shall the driver at any time cause the motor vehicle to make any unnecessary noise, but this subsection does not apply to a motor vehicle of a municipal fire department while proceeding to a fire or answering a fire alarm call.

<a id="on-reg-339-94-item-12"></a>**O. Reg. 339/94, Table, item 12, Improper passing** · [940339.txt, line 328](../../../statutes/on/reg-339-94/940339.txt#L328) · [e-Laws](https://www.ontario.ca/laws/regulation/940339)

> 12 | Subsection 148 (8), sections 149, 150 and 166 of the Highway Traffic Act | 3 | Improper passing

<a id="on-reg-339-94-item-13"></a>**O. Reg. 339/94, Table, item 13, Improper driving where highway divided into lanes** · [940339.txt, line 336](../../../statutes/on/reg-339-94/940339.txt#L336) · [e-Laws](https://www.ontario.ca/laws/regulation/940339)

> 13 | Section 154 of the Highway Traffic Act | 3 | Improper driving where highway divided into lanes

<a id="on-reg-339-94-item-14"></a>**O. Reg. 339/94, Table, item 14, Failing to stop for school bus** · [940339.txt, line 344](../../../statutes/on/reg-339-94/940339.txt#L344) · [e-Laws](https://www.ontario.ca/laws/regulation/940339)

> 14 | Subsections 175 (11) and (12) of the Highway Traffic Act | 6 | Failing to stop for school bus

<a id="on-reg-339-94-item-21"></a>**O. Reg. 339/94, Table, item 21, Pedestrian crossover** · [940339.txt, line 400](../../../statutes/on/reg-339-94/940339.txt#L400) · [e-Laws](https://www.ontario.ca/laws/regulation/940339)

> 21 | Subsections 140 (1) and (3) of the Highway Traffic Act | 4 | Pedestrian crossover

<a id="on-reg-339-94-item-22"></a>**O. Reg. 339/94, Table, item 22, Failing to share road** · [940339.txt, line 408](../../../statutes/on/reg-339-94/940339.txt#L408) · [e-Laws](https://www.ontario.ca/laws/regulation/940339)

> 22 | Subsections 148 (1), (2), (4), (5), (6) and (7) of the Highway Traffic Act | 2 | Failing to share road

<a id="on-reg-339-94-item-3"></a>**O. Reg. 339/94, Table, item 3, Racing** · [940339.txt, line 232](../../../statutes/on/reg-339-94/940339.txt#L232) · [e-Laws](https://www.ontario.ca/laws/regulation/940339)

> 3 | Section 172 of the Highway Traffic Act | 6 | Racing

<a id="on-reg-339-94-item-36-2"></a>**O. Reg. 339/94, Table, item 36.2, Failing to slow down and proceed with caution for emergency vehicle or tow truck** · [940339.txt, line 568](../../../statutes/on/reg-339-94/940339.txt#L568) · [e-Laws](https://www.ontario.ca/laws/regulation/940339)

> 36.2 | Subsection 159 (2) of the Highway Traffic Act | 3 | Failing to slow down and proceed with caution for emergency vehicle or tow truck

<a id="on-reg-339-94-item-36-3"></a>**O. Reg. 339/94, Table, item 36.3, Failing to move into another lane for emergency vehicle or tow truck – if safe to do so** · [940339.txt, line 576](../../../statutes/on/reg-339-94/940339.txt#L576) · [e-Laws](https://www.ontario.ca/laws/regulation/940339)

> 36.3 | Subsection 159 (3) of the Highway Traffic Act | 3 | Failing to move into another lane for emergency vehicle or tow truck – if safe to do so

<a id="on-reg-339-94-item-44"></a>**O. Reg. 339/94, Table, item 44, Failing to leave one metre while passing bicycle** · [940339.txt, line 648](../../../statutes/on/reg-339-94/940339.txt#L648) · [e-Laws](https://www.ontario.ca/laws/regulation/940339)

> 44 | Subsection 148 (6.1) of the Highway Traffic Act | 2 | Failing to leave one metre while passing bicycle

<a id="on-reg-455-07-3"></a>**O. Reg. 455/07, s. 3, Definition, “stunt”** · [070455.txt, line 145](../../../statutes/on/reg-455-07/070455.txt#L145) · [e-Laws](https://www.ontario.ca/laws/regulation/070455)

> 3. For the purposes of section 172 of the Act, “stunt” includes any activity where one or more persons engage in any of the following driving behaviours:

<a id="on-reg-455-07-3-8-i"></a>**O. Reg. 455/07, s. 3, para. 8, subpara. i** · [070455.txt, line 155](../../../statutes/on/reg-455-07/070455.txt#L155) · [e-Laws](https://www.ontario.ca/laws/regulation/070455)

> 8. Driving a motor vehicle without due care and attention, without reasonable consideration for other persons using the highway or in a manner that may endanger any person by, i. driving a motor vehicle in a manner that indicates an intention to prevent another vehicle from passing,

<a id="on-reg-608-1-1"></a>**R.R.O. 1990, Reg. 608, s. 1 (1)** · [900608.txt, line 133](../../../statutes/on/reg-608/900608.txt#L133) · [e-Laws](https://www.ontario.ca/laws/regulation/900608)

> 1. (1) Subject to subsection (2), no person shall operate a commercial motor vehicle or any combination of a commercial motor vehicle and a towed vehicle that exceeds 6.5 metres in length in the left lane or, where the left lane has been designated as a high occupancy vehicle lane, in the lane adjacent to the high occupancy vehicle lane of those portions of a highway described in the Schedules.

<a id="on-reg-615-34-3"></a>**R.R.O. 1990, Reg. 615, s. 34 (3)** · [900615.txt, line 796](../../../statutes/on/reg-615/900615.txt#L796) · [e-Laws](https://www.ontario.ca/laws/regulation/900615)

> (3) A Lane Designation sign in Figure 7 signifies that the lane marked with the sign shall be used by a vehicle for the purpose only of making a left turn.

<a id="on-reg-615-34-4"></a>**R.R.O. 1990, Reg. 615, s. 34 (4) (a), (b)** · [900615.txt, line 797](../../../statutes/on/reg-615/900615.txt#L797) · [e-Laws](https://www.ontario.ca/laws/regulation/900615)

> (4) A Lane Designation sign, (a) may, in the case of Figures 1 to 6 and Figure 8, be erected over the lane or be ground mounted; (b) shall, in the case of Figure 7, be erected directly over a two-way left turn lane;

<a id="on-reg-615-35"></a>**R.R.O. 1990, Reg. 615, s. 35, Do Not Pass Sign** · [900615.txt, line 815](../../../statutes/on/reg-615/900615.txt#L815) · [e-Laws](https://www.ontario.ca/laws/regulation/900615)

> 35. A Do Not Pass sign erected on or after the 28th day of March, 1986 shall, (a) be not less than 60 centimetres in height and not less than 60 centimetres in width; and (b) bear the markings and have the dimensions illustrated in the following Figure:
