# Ontario passing rules, with the law added

Generated from the rules database (`db/`) by `python3 tools/db.py export --write`. Do not edit by hand.

Each statement is shown as extracted from the handbook, with its flags and their notes unchanged: it is the reference the extraction is scored against. What the law adds comes under it:

- under each flag, what the rest of the handbook and the law say about it, with the sentences and provisions, and whether that resolves it;
- **Law**: what the law says on the statement's subject, in the rule language, with the provisions it cites. A word the law leaves as open as the handbook keeps its `[?…]` mark;
- **Compared with the law**: each provision behind the statement and how the statement compares with it.

Every provision is quoted word for word under [Provisions](#provisions), with a link to its line in the local copy of the law (`statutes/`, checked by `tools/db.py check`) and to the official page on e-Laws.

## Summary

88 statements. Law lines are added under 31 of them (33 lines); for 14, the handbook words as advice what the law makes a duty.

| Flags | | |
|---|---|---|
| `RESOLVED` | 33 | the rest of the handbook or the law settles it for every case the statement covers |
| `PARTIAL` | 18 | settled only for some cases, or narrowed but not settled |
| `OPEN` | 21 | nothing settles it |

| What each source says about a flag | Handbook | Law | |
|---|---|---|---|
| `DEFINES` | 19 | 11 | gives a definition, number, measure or test |
| `STATES` | 25 | 18 | settles it without a measure: the duty, the referent, the default, or the same rule in agreeing words |
| `REPEATS` | 22 | 29 | uses the same open words |
| `SILENT` | 6 | 14 | says nothing on it |

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
  - Handbook, `STATES`: The handbook uses the words for one act: “Changing your position on the road involves changing lanes or overtaking and passing another vehicle”, “Never overtake and pass another vehicle”, “If in doubt, do not pass”, “After overtaking, ... the vehicle you are passing”, and “pass on the right ... when overtaking a streetcar”. (handbook changing-positions:001.1, handbook changing-positions:013.1, handbook changing-positions:013.3, handbook changing-positions:017.2, handbook changing-positions:034.2)
  - Law, `REPEATS`: The Act uses “overtake” (148 (2)), “pass” (148 (8)) and “overtake and pass” (150 (1)) for this act and defines none of them; 148 (2) has the overtaken driver “allow the overtaking vehicle or equestrian to pass”. ([HTA 148 (2)](#on-hta-148-2), [HTA 148 (8)](#on-hta-148-8), [HTA 150 (1)](#on-hta-150-1))
  - **RESOLVED**: Passing = overtaking = overtaking and passing. None; keep ALSO CALLED overtaking. The handbook also uses both words for moves without a lane change (passing a cyclist with a one-metre gap; pedestrians overtaking on the right), so its definition of passing as a lane change is narrower than its use of either word.

### 1c

> FACT vehicles on the same road do not all travel at the same speed, even though every public road has a speed limit

FACT. Handbook: Changing positions page · Chapter 2 › Passing.

### 1d

> FACT cyclists, road service vehicles and drivers preparing to turn are [?usually] slower than through traffic

FACT. Handbook: Changing positions page · Chapter 2 › Passing.

_"You may want to pass some slow-moving vehicles" is motivation, not a permission, so no MAY rule is written for it._

**Flags**

- S "usually": Hedged generalisation.
  - Handbook, `REPEATS`: It speaks of "Bicycles and mopeds travelling at a lower speed than other traffic", notes that cyclists may be "travelling at or faster than the normal speed of traffic", and tells turning drivers to "Slow down before you enter the turn", but never says when these road users are not slower. (handbook changing-directions:003.1, handbook sharing-road-other-road-users:022.1, handbook sharing-road-other-road-users:028.1)
  - Law, `SILENT`
  - **OPEN**: A description of traffic, not a duty; cyclists at or above the normal speed of traffic are one stated case where "usually" fails.

### 2.1a

> a driver SHOULD start a lane change or a pass ONLY IF the driver has [?enough] space and time to complete it [?safely]

RULE, ADVICE. Handbook: Changing positions page · Chapter 2.

**Flags**

- J "enough": No measure of space or time.
  - Handbook, `DEFINES`: For lane changes only: the road test says to signal 'when there is enough space for you to change lanes' and measures the space as 'at least a two- to three-second distance behind the vehicle in front of you', without moving 'in beside another vehicle or into the blind spot of another vehicle'; there is no measure of time, of traffic coming from behind, or for a pass on a two-lane road. (handbook level-two-road-test:076.1, handbook level-two-road-test:077.1, handbook level-two-road-test:077.2)
  - Law, `REPEATS`: The Act asks the driver to 'first see that the movement can be made in safety' (142 (1)), to first ascertain 'that it can be done safely' (154 (1) (a)) and, for a pass, that the roadway be 'safely free' of approaching and overtaking traffic (148 (8)), with no measure. ([HTA 142 (1)](#on-hta-142-1), [HTA 148 (8)](#on-hta-148-8), [HTA 154 (1) (a)](#on-hta-154-1-a))
  - **PARTIAL**: For a lane change, including a pass on a multi-lane road: at least a two- to three-second gap behind the vehicle ahead in the new lane, without moving in beside another vehicle or into its blind spot. Could replace 'enough space' for lane changes; no measure for a pass on a two-lane road. The mirror test for moving back after a pass (changing-positions:029.1) marks when the pass is complete, not the room it needs.
- J "safely": Judgment term.
  - Handbook, `DEFINES`: For lane changes only, the road test's lane-change task spells out the safe move: 'at least a two- to three-second distance behind the vehicle in front of you', not moving 'in beside another vehicle or into the blind spot of another vehicle', and 'Adjust your speed to match the speed of traffic in the new lane'; nothing like it is given for a pass on a two-lane road. (handbook level-two-road-test:077.1, handbook level-two-road-test:077.2, handbook level-two-road-test:078.1)
  - Law, `REPEATS`: The Act uses the same words with no measure: 'in safety' (142 (1)), 'safely' (154 (1) (a)) and 'safely free' (148 (8)). ([HTA 142 (1)](#on-hta-142-1), [HTA 148 (8)](#on-hta-148-8), [HTA 154 (1) (a)](#on-hta-154-1-a))
  - **PARTIAL**: For a lane change: at least a two- to three-second gap behind the vehicle ahead in the new lane, not beside another vehicle or in its blind spot, at the speed of traffic in the new lane. Could replace 'safely' with these checks for lane changes; a pass on a two-lane road stays open.

**Law**

- `a driver MUST start a lane change or a pass ONLY IF the driver has first made sure there is [?enough] space and time to complete it [?safely] IF VIOLATED 3 demerit points`
  - [HTA 142 (1)](#on-hta-142-1), [HTA 154 (1) (a)](#on-hta-154-1-a), [O. Reg. 339/94 Table, item 13](#on-reg-339-94-item-13)

**Compared with the law**

- `SAME` [HTA 142 (1)](#on-hta-142-1): The Act also requires the driver to see first that the move can be made in safety, and to signal when another vehicle may be affected.
- `SAME` [HTA 154 (1) (a)](#on-hta-154-1-a): The Act makes it a duty for any move from one lane to another; the handbook words it as advice.
- `PENALTY` [O. Reg. 339/94 Table, item 13](#on-reg-339-94-item-13): 3 demerit points for a conviction under s. 154.

### 2.1b

> a driver SHOULD NOT pass a vehicle UNLESS the driver is [?sure] the pass can be made without danger to the driver or others

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing.

**Flags**

- J "sure": Subjective certainty; no observable test.
  - Handbook, `REPEATS`: The neighbours stay open: 'If in doubt, do not pass', and the passing steps ask the driver to 'check that the way is clear ahead and behind' and to watch for bicycles and small vehicles 'that may be hidden from view', without a test of certainty. (handbook changing-positions:013.3, handbook changing-positions:015.1, handbook changing-positions:016.1)
  - Law, `REPEATS`: The Act puts the same judgment on the driver: first ascertain 'that it can be done safely' (154 (1) (a)), 'first see that the movement can be made in safety' (142 (1)), and a roadway 'safely free from approaching traffic' (148 (8)). ([HTA 142 (1)](#on-hta-142-1), [HTA 148 (8)](#on-hta-148-8), [HTA 154 (1) (a)](#on-hta-154-1-a))
  - **OPEN**: Strength: 148 (8) makes it a duty for every pass, and 154 (1) (a) for any pass that moves from one lane to another.

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
  - Handbook, `REPEATS`: The handbook uses doubt the same open way elsewhere ('If you're in doubt, let the other driver go first') and frames a pass as needing the driver to be 'sure you can do so without danger to yourself or others', with no test of doubt. (handbook changing-positions:013.1, handbook driving-efficiently:033.1)
  - Law, `REPEATS`: 154 (1) (a) allows a lane-to-lane move only if the driver first ascertains 'that it can be done safely' and 148 (8) requires a roadway 'safely free from approaching traffic', so a driver in doubt has not met them, but the Act neither names nor tests the state. ([HTA 148 (8)](#on-hta-148-8), [HTA 154 (1) (a)](#on-hta-154-1-a))
  - **OPEN**

### 2.1d

> a driver SHOULD keep to the right of the road, or to the right-hand lane of a multi-lane road UNLESS the driver is turning left OR passing another vehicle

RULE, ADVICE. Handbook: Driving along › Keep right · ¶1.

### 2.2a

> TO pass a vehicle

PROCEDURE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing.

_Steps 1 and 2 restate the lane-change steps on the same page; the order of the steps carries "only after signalling"._

**Flags**

- V "inside mirror": Called "rear view mirror" in the night procedure (3.3.1b).
  - Handbook, `STATES`: The night passing steps give the same cue with “rear view mirror” (“When you can see all of the front of the vehicle you are passing in your rear view mirror”), the road test names “your rearview and side mirrors” as different mirrors, and the set-up section calls it “the interior mirror”. (handbook changing-positions:029.1, handbook getting-ready-drive:020.3, handbook level-two-road-test:009.2)
  - Law, `SILENT`: No provision names the inside or rear view mirror in passing.
  - **RESOLVED**: Inside mirror = rear view mirror = interior mirror, the one that shows the rear window. None; both procedures say inside mirror.

### 2.2b

> a driver SHOULD NOT cut off the vehicle being passed by moving in front of it suddenly WHEN returning to the original lane

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing.

### 3.1.1a

> a driver MUST NOT pass a vehicle WHEN the driver is within 30 m of a pedestrian crossover

RULE, LAW. Handbook: Changing positions page · Chapter 2 › Passing; Stopping › Stopping for pedestrian crossovers · ¶2.

**Flags**

- X "within 30 m": Stated on two pages (Changing positions, Stopping) in different words; the meanings agree.
  - Handbook, `STATES`: Both pages give the same ban: “Passing within 30 metres of a pedestrian crossover is not permitted” and “You must not pass any vehicle within 30 metres of a pedestrian crossover”. (handbook changing-positions:020.1, handbook stopping:033.5)
  - Law, `STATES`: When a vehicle “is approaching a pedestrian crossover and is within 30 metres of it”, a driver approaching from the rear “shall not allow the front extremity of his or her vehicle to pass beyond the front extremity of the other vehicle” (140 (3)), with 4 demerit points (O. Reg. 339/94, item 21). ([HTA 140 (3)](#on-hta-140-3), [O. Reg. 339/94 Table, item 21](#on-reg-339-94-item-21))
  - **RESOLVED**: Within 30 m of a pedestrian crossover, do not let the front of your vehicle pass beyond the front of another vehicle that is approaching the crossover. None; both pages agree with each other and with 140 (3).

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
  - Handbook, `SILENT`
  - Law, `DEFINES`: s. 149 (1) (a) bars driving to the left of the centre of a roadway with one or more lanes in each direction "within 30 metres of a bridge, viaduct or tunnel where the driver's view is obstructed within that distance so as to create a potential hazard" if another vehicle might approach from the opposite direction; s. 149 (2) excepts highways with more lanes in one direction than the other, road service vehicles taking precautions, and one-way highways, and O. Reg. 339/94 item 12 gives 3 demerit points. ([HTA 149 (1)](#on-hta-149-1), [HTA 149 (2)](#on-hta-149-2), [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12))
  - **RESOLVED**: Within 30 m of the bridge, viaduct or tunnel, on either side of it, and only where the driver's view is obstructed within that distance. Read "30 m from" as "within 30 m of"; add WHEN the driver's view is obstructed within that distance, and the s. 149 (2) exceptions. "Within 30 metres of" is a distance from the structure, not tied to a direction of approach, so it covers both sides.
- G "on the left of a centreline": Prohibits the means (crossing the centreline), not passing; passing near a bridge on a multi-lane road is not covered.
  - Handbook, `SILENT`
  - Law, `STATES`: Section 149 (1) (a) also bans the means, not the pass: no vehicle may be driven "to the left of the centre of a roadway designed for one or more lanes of traffic in each direction" within 30 metres of a bridge, viaduct or tunnel where the view is obstructed, and 149 (2) (a) lifts it where there are more lanes in one direction than the other. ([HTA 149 (1)](#on-hta-149-1), [HTA 149 (2)](#on-hta-149-2))
  - **RESOLVED**: Driving left of the centre of a roadway with one or more lanes in each direction, within 30 m of a bridge, viaduct or tunnel where the view is obstructed (149 (1) (a)); a pass that stays right of the centre is not covered, in the Act either. None; the gap is in the Act too, and a road with more lanes in one direction than the other is excepted (149 (2) (a)). The handbook mentions bridges and tunnels elsewhere only for U-turns and three-point turns, not for passing.

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
  - Handbook, `REPEATS`: Elsewhere the handbook stays open: where 'you cannot see far ahead on the road because of a curve or a hill, move right', and a pass is made only 'if there are enough broken lines ahead to complete the pass safely'; no clear distance is given. (handbook level-two-road-test:112.3, handbook pavement-markings:006.2)
  - Law, `REPEATS`: 149 (1) (a) forbids driving left of centre 'when approaching the crest of a grade or upon a curve in the roadway' where the view is obstructed 'so as to create a potential hazard', and 148 (8) asks for a roadway 'safely free from approaching traffic', with no clear distance. ([HTA 148 (8)](#on-hta-148-8), [HTA 149 (1)](#on-hta-149-1))
  - **OPEN**: Strength: 149 (1) (a) makes it a prohibition on roads with one or more lanes each way (3 demerit points, item 12). Whether the 30 metres of 149 (1) (a) also limits the crest and curve cases is unclear from its wording and is not counted. An engineering passing sight distance (OTM Book 11) was not obtained.
- J "safely": Judgment term.
  - Handbook, `REPEATS`: Elsewhere the handbook stays open: where 'you cannot see far ahead on the road because of a curve or a hill, move right', and a pass is made only 'if there are enough broken lines ahead to complete the pass safely'; no clear distance is given. (handbook level-two-road-test:112.3, handbook pavement-markings:006.2)
  - Law, `REPEATS`: 149 (1) (a) forbids driving left of centre 'when approaching the crest of a grade or upon a curve in the roadway' where the view is obstructed 'so as to create a potential hazard', and 148 (8) asks for a roadway 'safely free from approaching traffic', with no clear distance. ([HTA 148 (8)](#on-hta-148-8), [HTA 149 (1)](#on-hta-149-1))
  - **OPEN**: Whether the 30 metres of 149 (1) (a) also limits the crest and curve cases is unclear from its wording and is not counted. An engineering passing sight distance (OTM Book 11) was not obtained.

**Law**

- `a driver MUST NOT drive left of the centre of the road WHEN the road has one or more lanes in each direction AND (the driver is approaching the crest of a hill OR the driver is on a curve) AND the driver's view is obstructed so that a vehicle coming the other way would be a [?potential hazard] UNLESS the road has more lanes in one direction than in the other OR the road is one-way IF VIOLATED 3 demerit points`
  - [HTA 149 (1)](#on-hta-149-1), [HTA 149 (2)](#on-hta-149-2), [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12). The Act's test, "a potential hazard", is as open as the handbook's "not enough to pass safely".

**Compared with the law**

- `SAME` [HTA 149 (1)](#on-hta-149-1): The Act bans driving left of centre approaching a crest or on a curve where the view is obstructed; the handbook words it as advice.
- `BROADER` [HTA 149 (2)](#on-hta-149-2): The Act does not apply where the road has more lanes in one direction than in the other, or is one-way; the statement has no exception.
- `PENALTY` [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12): 3 demerit points (improper passing).

### 3.1.4a

> a driver SHOULD NOT use a two-way left-turn lane for passing

RULE, ADVICE. Handbook: Changing directions › Left-turn lanes · ¶3.

**Flags**

- M "are not to be used": Not an imperative and no legal marker; the default puts it at SHOULD NOT, but the wording reads like a prohibition.
  - Handbook, `STATES`: The regulatory-sign list says the two-way left-turn sign "means the lane is only for two-way left turns", and regulatory signs "give a direction that must be obeyed"; for an unsigned lane the handbook gives no legal marker. (handbook signs:012.1, handbook signs:065.1)
  - Law, `STATES`: Under O. Reg. 615 s. 34 (3) and (4) (b) the Figure 7 Lane Designation sign, erected directly over a two-way left turn lane, means the lane "shall be used by a vehicle for the purpose only of making a left turn", and s. 182 (2) and s. 154 (1) (c) make drivers obey it; without such a sign, s. 154 (1) (b) lets a driver on a three-lane highway use the centre lane to overtake where the roadway is clearly visible and the lane is clear. ([HTA 154 (1) (b)](#on-hta-154-1-b), [HTA 154 (1) (c)](#on-hta-154-1-c), [HTA 182 (2)](#on-hta-182-2), [Reg. 615 34 (3)](#on-reg-615-34-3), [Reg. 615 34 (4) (a), (b)](#on-reg-615-34-4))
  - **PARTIAL**: A legal duty where the lane carries the two-way left-turn Lane Designation sign (Figure 7): the lane is for left turns only, so passing in it is unlawful. Strength LAW WHEN the lane carries the two-way left-turn sign; otherwise keep ADVICE (on a three-lane highway without the sign the Act allows passing in the centre lane). The handbook says the sign may be "above the road or on the ground", while s. 34 (4) (b) requires the Figure 7 sign to be erected directly over the lane.

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
  - Handbook, `DEFINES`: The next sentences say which marking tells it: 'A solid line at the left of your lane means it is unsafe to pass', while 'A broken line at the left of your lane means you may pass if the way is clear'. (handbook pavement-markings:004.1, handbook pavement-markings:006.1)
  - Law, `SILENT`: The Act and regulations given do not give pavement lines a meaning.
  - **RESOLVED**: The markings tell it by a solid line at the left of the driver's lane: passing is not safe there; a broken line allows a pass if the way is clear. Could name the marking: a solid line at the left of the lane.

### 3.1.5b

> a driver SHOULD NOT pass WHEN there is a solid line at the left of the driver's lane BECAUSE a solid line there means it is unsafe to pass

RULE, ADVICE. Handbook: Pavement markings › Intro · ¶3; Pavement markings › Intro · Diagram 3-2.

### 3.1.6a

> a driver MAY pass WHEN there is a broken line at the left of the driver's lane ONLY IF the way is clear AND there are [?enough] broken lines ahead to complete the pass [?safely]

RULE, LAW. Handbook: Pavement markings › Intro · ¶4; Pavement markings › Intro · Diagram 3-3.

**Flags**

- J "enough": No distance given.
  - Handbook, `REPEATS`: Elsewhere the handbook stays open: 'be sure you have enough space and time to complete the move safely' and 'check that the way is clear ahead and behind'; no length of broken line or passing distance is given. (handbook changing-positions:001.2, handbook changing-positions:015.1)
  - Law, `REPEATS`: 148 (8) asks that the roadway ahead and to the left be 'safely free from approaching traffic', with no distance; the Act and regulations given do not mention broken lines. ([HTA 148 (8)](#on-hta-148-8))
  - **OPEN**: The mirror test (changing-positions:029.1) marks where a pass ends but not how far ahead the broken line must run. An engineering passing sight distance (OTM Book 11) was not obtained.
- J "safely": Judgment term.
  - Handbook, `REPEATS`: Elsewhere the handbook stays open: 'be sure you have enough space and time to complete the move safely' and 'check that the way is clear ahead and behind'; no length of broken line or passing distance is given. (handbook changing-positions:001.2, handbook changing-positions:015.1)
  - Law, `REPEATS`: 148 (8) asks that the roadway ahead and to the left be 'safely free from approaching traffic', with no distance; the Act and regulations given do not mention broken lines. ([HTA 148 (8)](#on-hta-148-8))
  - **OPEN**: The mirror test (changing-positions:029.1) marks where a pass ends but not how far ahead the broken line must run. An engineering passing sight distance (OTM Book 11) was not obtained.

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
  - Handbook, `SILENT`: No other sentence says what makes a pass in the left lane of a passing or climbing lane safe.
  - Law, `SILENT`: The Act and regulations given do not define passing or climbing lanes.
  - **OPEN**: Inside a definition, about the lane's purpose; it sets no duty. The sign 'Keep to the right lane except when passing on two-lane sections where climbing or passing lanes are provided' (signs:071.1) restates the use, and 149 (2) (a) lifts the crest and curve ban where one direction has more lanes, but neither defines 'safely'.

### 3.2.1b

> FACT an advance sign tells drivers a passing opportunity is coming, AND another sign warns when the added lane is ending

FACT. Handbook: Changing positions page · Chapter 2 › Passing and climbing lanes.

### 3.2.1c

> a driver in the right-hand lane SHOULD merge [?safely] with traffic in the left-hand lane WHEN a sign warns that the lane is ending

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing and climbing lanes.

**Flags**

- D "merge": The rule is implied by a purpose clause about the sign; the text states no instruction.
  - Handbook, `STATES`: The warning-sign list says of the "Right lane ends ahead" sign: "If you are in the right-hand lane, you must merge safely with traffic in the lane to the left"; continuity lines likewise mean "you must change lanes if you want to continue". (handbook pavement-markings:008.2, handbook signs:124.1, handbook signs:124.2)
  - Law, `STATES`: s. 154 (1) (a) governs the merge: a vehicle "shall not be driven from one lane to another lane ... unless the driver first ascertains that it can be done safely"; no provision orders the merge itself. ([HTA 154 (1) (a)](#on-hta-154-1-a))
  - **RESOLVED**: When the right-hand lane ends, a driver in it must merge with traffic in the lane to the left, moving over only after first ascertaining that it can be done safely. State the instruction outright (signs:124.2) and cite s. 154 (1) (a) for the safety condition, which is LAW. "safely" stays a judgment term; s. 154 (1) (a) gives no measure.
- J "safely": Judgment term.
  - Handbook, `DEFINES`: The merge is a lane change, for which the road test measures the space: 'at least a two- to three-second distance behind the vehicle in front of you', without moving 'in beside another vehicle or into the blind spot of another vehicle'; traffic coming from behind in the left lane is not measured. (handbook level-two-road-test:077.1, handbook level-two-road-test:077.2)
  - Law, `REPEATS`: 154 (1) (a) allows a move from one lane to another only if the driver first ascertains 'that it can be done safely', with no measure. ([HTA 154 (1) (a)](#on-hta-154-1-a))
  - **PARTIAL**: Merge with at least a two- to three-second gap behind the vehicle ahead in the left lane, without moving in beside another vehicle or into its blind spot. Could add the gap and side checks; the gap to traffic behind stays open.

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
  - Handbook, `DEFINES`: For some cases: 'Keep to the right of the road or in the right-hand lane on multi-lane roads unless you want to turn left or pass another vehicle', 'Traffic should keep to the right, using the left lanes for passing', and freeway drivers 'should move over, if it is safe to do so, leaving room for merging vehicles'; other reasons the right lane cannot be used are not named. (handbook driving-along:010.1, handbook freeway-driving:015.4, handbook freeway-driving:018.2)
  - Law, `DEFINES`: For slower vehicles only: 147 (1) requires the right-hand lane 'where practicable', and 147 (2) lifts this 'while overtaking and passing another vehicle' or 'while preparing for a left turn'; nothing applies to traffic at the normal speed and 'practicable' is not tested. ([HTA 147 (1)](#on-hta-147-1), [HTA 147 (2)](#on-hta-147-2))
  - **PARTIAL**: Drive in the right-hand lane except while passing, preparing to turn left, or moving over to leave room for merging traffic; other cases where the right lane cannot be used stay open. Could replace 'when possible' with the named exceptions.

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
  - Handbook, `STATES`: Its passing steps say "Use your left-turn signal to show that you want to pass", the freeway section says "Use the far left lane of a multi-lane freeway to pass", and a driver in the left-most lane behind a slower vehicle is told to "wait for the vehicle to move to the right" rather than pass on the right. (handbook changing-positions:015.1, handbook changing-positions:035.2, handbook freeway-driving:022.1)
  - Law, `STATES`: s. 148 (5) requires a person overtaking another vehicle to "turn out to the left so far as may be necessary to avoid a collision", and s. 150 (1) allows passing on the right "only where" one of its three cases applies and it can be done safely; streetcars, which s. 1 (1) excludes from "vehicle", must be passed on the right except on a one-way highway (s. 166 (2)). ([HTA 1 (1), "vehicle"](#on-hta-1-1-vehicle), [HTA 148 (5)](#on-hta-148-5), [HTA 150 (1)](#on-hta-150-1), [HTA 166 (2)](#on-hta-166-2))
  - **RESOLVED**: Pass on the left (s. 148 (5)), except in the cases of s. 150 (1) (a) to (c); pass streetcars on the right unless on a one-way highway (s. 166 (2)). The default is a legal duty in the Act, so 3.2.3a could be LAW, with 3.2.3b as its exception.
- S "Most passing": Hedged generalisation in the source.
  - Handbook, `DEFINES`: The next sentence lists the exceptions exactly: "You may pass on the right on multi-lane or one-way roads and when overtaking a streetcar or a left-turning vehicle"; the right shoulder may be used "only to pass a vehicle turning left", and streetcars must be passed on the right "unless you are driving on a one-way road". (handbook changing-positions:033.1, handbook changing-positions:034.2, handbook changing-positions:037.1)
  - Law, `DEFINES`: s. 148 (5) requires an overtaking driver to "turn out to the left", and s. 150 (1) allows passing to the right "only where the movement can be made in safety" and the overtaken vehicle is turning or signalling left, the highway has unobstructed pavement for two or more lines of vehicles in each direction, or the highway is one-way; s. 166 (2) requires passing a streetcar on its right except on a one-way highway (a streetcar is not a "vehicle" under s. 1 (1), so s. 150 does not reach it). ([HTA 1 (1), "vehicle"](#on-hta-1-1-vehicle), [HTA 148 (5)](#on-hta-148-5), [HTA 150 (1)](#on-hta-150-1), [HTA 166 (2)](#on-hta-166-2))
  - **RESOLVED**: Pass on the left, except: a vehicle turning or signalling left, a highway with room for two or more lines of vehicles each way, or a one-way highway (s. 150 (1) (a) to (c)), and then only where it can be done safely; a streetcar is passed on the right unless on a one-way highway (s. 166 (2)). "Most" is exact: the exceptions are s. 150 (1) (a) to (c) and the streetcar rule. The left default is a legal duty (s. 148 (5)), so the statement's strength could be LAW.

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
  - Handbook, `STATES`: It adds "You may not pass on the left shoulder, paved or not", while elsewhere it tells drivers to "Drive off the road onto the shoulder if you must stop for some reason" and not to "drive on or block the shoulder on freeways", so the unstated default concerns passing on the shoulder, not every use of it. (handbook changing-positions:033.2, handbook dealing-particular-situations:092.1, handbook parking-along-roadways:003.2)
  - Law, `STATES`: s. 150 (2) says "No driver of a motor vehicle shall overtake and pass another vehicle by driving off the roadway", and the roadway "does not include the shoulder" (s. 1 (1)); s. 150 (3) (a) excepts passing on the right where the right shoulder is paved and the overtaken vehicle is turning or signalling left, and s. 154 (1) (a) lets a vehicle move to or from the shoulder only after the driver ascertains it can be done safely. ([HTA 1 (1), "roadway"](#on-hta-1-1-roadway), [HTA 150 (2)](#on-hta-150-2), [HTA 150 (3) (a)](#on-hta-150-3-a), [HTA 154 (1) (a)](#on-hta-154-1-a))
  - **RESOLVED**: Passing by driving off the roadway, onto either shoulder, is prohibited; the only exception is passing on a paved right shoulder a vehicle that is turning or has signalled a left turn. The unstated prohibition is s. 150 (2) and the statement is its exception (s. 150 (3) (a)); read ONLY IF as limiting passing on the shoulder, not stopping on it, and add "or has signalled a left turn".

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
  - Handbook, `DEFINES`: For some steps: the sentences after it say "Switch your headlights to low beams as you approach a vehicle from behind", "As you move alongside the vehicle you are passing, switch on your high beams", and move back "when you can see all of the front of the vehicle you are passing in your rear view mirror", with low beams "when you are less than 60 metres behind another vehicle unless you are passing it"; the hazard is that "you cannot see as far ahead, even with headlights", and nothing else is measured. (handbook changing-positions:026.2, handbook changing-positions:027.1, handbook changing-positions:028.2, handbook changing-positions:029.1, handbook driving-night-and-bad-weather:001.1, handbook getting-ready-drive:057.6)
  - Law, `DEFINES`: For headlight use only: section 168 requires the low beam when approaching an oncoming vehicle within 150 metres and when following another vehicle within 60 metres, "except when in the act of overtaking and passing". ([HTA 168](#on-hta-168))
  - **PARTIAL**: Use low beams while within 60 metres behind the vehicle (and within 150 metres of oncoming traffic), switch to high beams once alongside, and move back only when the whole front of the passed vehicle shows in the rear-view mirror; nothing measures the rest of "very careful". Could replace "be very careful" with the listed night steps, keeping the caution as advice. The earlier pass found no night standard; the steps right after the sentence supply one in part, and 168 matches the beam steps.

### 3.3.1b

> TO pass a vehicle at night SPECIALIZES 2.2a WHEN the driver has to pass AND the way is clear

PROCEDURE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing at night.

**Flags**

- V "rear view mirror": The handbook calls the mirror "rear view mirror" here and "inside mirror" in 2.2a; both rules say inside mirror.
  - Handbook, `STATES`: The day passing steps give the same cue with “when you can see the entire front of the vehicle you are passing in your inside mirror”, the road test names “your rearview and side mirrors” as different mirrors, and the set-up section calls it “the interior mirror”. (handbook changing-positions:017.2, handbook getting-ready-drive:020.3, handbook level-two-road-test:009.2)
  - Law, `SILENT`: No provision names the inside or rear view mirror in passing.
  - **RESOLVED**: Rear view mirror = inside (interior) mirror, the one that shows the rear window, not the side mirrors. None; both procedures say inside mirror.

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
  - Handbook, `REPEATS`: Elsewhere it says bicycles and mopeds "can use any part of the lane if necessary for safety, such as to" avoid "puddles, ice, sand, debris, rutted or grooved pavement, potholes and sewer grates", and that riders "may make sudden moves because of uneven road surfaces or poor weather conditions"; these are open examples, not a frequency. (handbook sharing-road-other-road-users:022.2, handbook sharing-road-other-road-users:023.1, handbook sharing-road-other-road-users:046.2)
  - Law, `SILENT`
  - **OPEN**: A description of riders, not a duty; the examples would let "often" read "when necessary for safety", but they stay open-ended ("such as").

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
  - Handbook, `STATES`: The paragraph opens "Motorcycles, bicycles, limited-speed motorcycles and mopeds turn left at intersections in the same way as larger vehicles" and then speaks of "one of these vehicles". (handbook changing-directions:014.1, handbook changing-directions:014.2)
  - Law, `SILENT`
  - **RESOLVED**: Motorcycles, bicycles, limited-speed motorcycles and mopeds. Name the vehicles instead of "smaller vehicle".

### 3.4.3b

> a driver SHOULD NOT pull up beside a [?smaller vehicle] that is turning left ahead to make the turn at the same time WHEN the driver is also turning left, behind it

RULE, ADVICE. Handbook: Changing directions › Left turns · ¶5.

_Pulling up beside a turning two-wheeler is the start of a pass._

**Flags**

- R "smaller vehicle": The source says "one of these vehicles": those named in the sentence before.
  - Handbook, `STATES`: The sentence before it names the vehicles: "Motorcycles, bicycles, limited-speed motorcycles and mopeds turn left at intersections in the same way as larger vehicles". (handbook changing-directions:014.1)
  - Law, `SILENT`
  - **RESOLVED**: Motorcycles, bicycles, limited-speed motorcycles and mopeds. Name the vehicles instead of "smaller vehicle".

### 3.4.3c

> a driver SHOULD stay behind a [?smaller vehicle] that is turning left ahead WHEN the driver is also turning left, behind it UNTIL the way is [?clear]

RULE, ADVICE. Handbook: Changing directions › Left turns · ¶5.

_"… and turn when the way is clear" is written as the end of the wait (UNTIL)._

**Flags**

- R "smaller vehicle": Same vehicles as 3.4.3b; the source only says "Stay behind".
  - Handbook, `STATES`: The paragraph opens "Motorcycles, bicycles, limited-speed motorcycles and mopeds turn left at intersections in the same way as larger vehicles" and then speaks of "one of these vehicles". (handbook changing-directions:014.1, handbook changing-directions:014.2)
  - Law, `SILENT`
  - **RESOLVED**: Motorcycles, bicycles, limited-speed motorcycles and mopeds. Name the vehicles instead of "smaller vehicle".
- J "clear": No test for when the way is clear.
  - Handbook, `DEFINES`: For a check after the fact: the road test says "You have not properly checked traffic if another vehicle or pedestrian has the right-of-way and must take action to avoid your vehicle", and the left-turn rules say to turn "after yielding the right-of-way to pedestrians and oncoming traffic" and not to "pull up beside it to make your turn at the same time"; no gap or time for starting is given. (handbook changing-directions:013.1, handbook changing-directions:014.2, handbook level-two-road-test:020.5)
  - Law, `REPEATS`: Section 142(1) requires the driver to "first see that the movement can be made in safety", and 141(5) forbids turning left across an approaching vehicle's path unless the driver "has afforded a reasonable opportunity to the driver or operator of the approaching vehicle to avoid a collision"; neither sets a gap. ([HTA 141 (5)](#on-hta-141-5), [HTA 142 (1)](#on-hta-142-1))
  - **PARTIAL**: The way is not clear if any road user with the right-of-way (the smaller vehicle ahead, oncoming traffic or pedestrians) would have to take action to avoid your vehicle. Could replace "clear" with the road test's check. The road test check says when a turn was wrong, after the fact; it gives no gap or time for deciding to start.

### 3.4.4a

> a cyclist MAY use any part of the lane WHEN this is [?necessary for safety], for example to discourage passing where the lane is too narrow to be shared [?safely]

RULE, LAW. Handbook: Sharing the road › Cyclists · ¶1; Sharing the road › Cyclists · item 3.

_A rule for the cyclist, not the passing driver._

**Flags**

- J "necessary for safety": Judgment of the cyclist.
  - Handbook, `DEFINES`: For some cases: the list names 'Avoid obstacles such as puddles, ice, sand, debris, rutted or grooved pavement, potholes and sewer grates' and 'Cross railway or streetcar tracks at a 90° angle', and the passing chapter adds 'to avoid dangerous road conditions or to be seen by other drivers'; the list is open ('such as'). (handbook changing-positions:022.1, handbook sharing-road-other-road-users:023.1, handbook sharing-road-other-road-users:024.1)
  - Law, `REPEATS`: 147 (1) keeps a slower vehicle to the right only 'where practicable', with no test. ([HTA 147 (1)](#on-hta-147-1))
  - **PARTIAL**: Necessary for safety covers at least: avoiding obstacles such as puddles, ice, sand, debris, rutted or grooved pavement, potholes and sewer grates; crossing railway or streetcar tracks at a right angle; being seen by other drivers; and discouraging passing where the lane is too narrow to share (itself unmeasured). Other cases stay open. Could list the named cases. Cyclists at or above the normal speed of traffic, or turning left, need not keep right at all (sharing-road-other-road-users:028.1; 147 (1) applies only to slower vehicles and 147 (2) (b) exempts preparing for a left turn).
- J "safely": Judgment term.
  - Handbook, `REPEATS`: The handbook gives no lane width: it says only that drivers passing a cyclist 'must maintain a minimum distance of one metre, where practical' and that two-wheelers riding to one side are not 'an invitation to pass in the same lane' but should be passed 'by changing lanes', which bears on when a lane is too narrow to share without measuring it. (handbook changing-positions:022.2, handbook changing-positions:022.3, handbook sharing-road-other-road-users:030.1)
  - Law, `REPEATS`: The Act gives no lane width either: 147 (1) keeps a slower vehicle to the right 'where practicable' and 'as close as practicable' to the edge, and 148 (6.1) asks a passing motorist to leave one metre 'as nearly as may be practicable'. ([HTA 147 (1)](#on-hta-147-1), [HTA 148 (6.1)](#on-hta-148-6-1))
  - **OPEN**: Reading 'too narrow' as a lane in which a motor vehicle cannot pass the cyclist while leaving one metre would combine 148 (6.1) with the width of the vehicle; no source says so, so it is not counted.

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
  - Handbook, `REPEATS`: The only neighbouring guidance is equally open, 'Whenever possible, you should change lanes to pass'; the handbook never says when one metre is not practical. (handbook sharing-road-other-road-users:030.4)
  - Law, `REPEATS`: 148 (6.1) asks for the one metre 'as nearly as may be practicable' with no test of when less is allowed; 148 (6.2) only says how the metre is measured ('the extreme right side of the motor vehicle and the extreme left side of the bicycle, including all projections and attachments'), and demerit item 44 gives 2 points. ([HTA 148 (6.1)](#on-hta-148-6-1), [HTA 148 (6.2)](#on-hta-148-6-2), [O. Reg. 339/94 Table, item 44](#on-reg-339-94-item-44))
  - **OPEN**: 148 (6.2) could be added to say how the 1 m is measured, but it does not settle 'where practical'; the Act does not define 'practicable'.

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
  - Handbook, `REPEATS`: Elsewhere the handbook drops the qualifier ('Do not take this as an invitation to pass in the same lane'; 'If you do want to pass these vehicles, do so by changing lanes'), but no sentence says when a lane change to pass a cyclist is possible. (handbook changing-positions:022.2, handbook changing-positions:022.3)
  - Law, `REPEATS`: 148 (6) asks the overtaking vehicle to 'turn out to the left so far as may be necessary to avoid a collision' and 148 (6.1) sets the one-metre minimum; neither requires or tests a lane change. ([HTA 148 (6)](#on-hta-148-6), [HTA 148 (6.1)](#on-hta-148-6-1))
  - **OPEN**: On a two-lane road a lane change to pass means using the opposing lane, so the passing limits (solid line at the left, 30 m of a crossover, 148 (8)) would bear on 'possible', but none is tied to this rule. The unqualified wording of changing-positions:022.3 differs from 'whenever possible'.

### 3.4.4d

> a driver SHOULD NOT sound the horn [?unnecessarily] WHILE passing a cyclist BECAUSE it may frighten the cyclist and cause a loss of control

RULE, ADVICE. Handbook: Sharing the road › Cyclists · ¶6.

**Flags**

- J "unnecessarily": Who judges necessity is not stated.
  - Handbook, `REPEATS`: Elsewhere the handbook leaves the need to the driver's own judgment: "If you need to get another person's attention, use your horn", "Avoid honking your horn at other drivers, unless absolutely necessary", and the next sentence "If you feel that you must use your horn, tap it quickly and lightly"; none says when the horn is necessary. (handbook dealing-particular-situations:008.1, handbook safe-and-responsible-driving:010.3, handbook sharing-road-other-road-users:036.3)
  - Law, `REPEATS`: Section 75(4) bars sounding a horn "so as to make an unreasonable noise" and 75(5) requires it to be sounded "whenever it is reasonably necessary to notify pedestrians or others of its approach"; both leave necessity to a reasonableness judgment with no test. ([HTA 75 (4)](#on-hta-75-4), [HTA 75 (5)](#on-hta-75-5))
  - **OPEN**: On who judges: the next handbook sentence leaves it to the driver ("If you feel that you must use your horn"), while the Act's "unreasonable noise" and "reasonably necessary" are objective standards; the word itself still has no test.

### 3.4.4e

> a driver SHOULD tap the horn quickly and lightly while still [?some distance] away from the cyclist WHEN the driver feels the horn must be used

RULE, ADVICE. Handbook: Sharing the road › Cyclists · ¶6.

**Flags**

- J "some distance": No distance given.
  - Handbook, `SILENT`: No other sentence of the handbook gives a distance, or any other measure, for when to sound the horn while coming up on a cyclist.
  - Law, `REPEATS`: Section 75(5) requires the horn to be sounded "whenever it is reasonably necessary to notify pedestrians or others of its approach", which implies sounding it before reaching the cyclist but sets no distance. ([HTA 75 (5)](#on-hta-75-5))
  - **OPEN**: The one metre of 148(6.1) and the handbook's "minimum distance of one metre" is side clearance while passing, not a horn distance, so it is not counted; the only handbook guide is the purpose in the same passage (the horn "may frighten them").

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
  - Handbook, `STATES`: The diagrams call it "the required two metres behind the rear doors of a stopped streetcar" and "the required distance behind a stopped streetcar", and the knowledge-test topics include "What drivers must do when they meet streetcars and school buses". (handbook changing-positions:036, handbook level-two-road-test:102, handbook getting-your-drivers-licence:164.1)
  - Law, `STATES`: s. 166 (1) bars a person overtaking a streetcar stopped to take on or discharge passengers from passing it or approaching "nearer than 2 metres measured back from the nearest door of the car ... through which passengers may get on or off until the passengers have got on or got safely to the side of the street", except where a safety zone has been set aside and designated by by-law; O. Reg. 339/94 item 12 gives 3 demerit points. ([HTA 166 (1)](#on-hta-166-1), [O. Reg. 339/94 Table, item 12](#on-reg-339-94-item-12))
  - **RESOLVED**: A legal duty: behind a streetcar stopped to take on or let off passengers, do not pass or come nearer than 2 m to its nearest passenger door until the passengers are on board or safely at the side of the street; it does not apply where a by-law has designated a safety zone. Strength LAW; measure from the nearest passenger door rather than "the rear doors"; add UNTIL the passengers are on board or safely at the side; the exception is a by-law safety zone.

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
  - Handbook, `REPEATS`: The other statement of this rule says the same: "Pass these safety islands and zones at a reasonable speed" and "Always be ready, in case pedestrians make sudden or unexpected moves"; no speed is given. (handbook sharing-road-other-road-users:017.2, handbook sharing-road-other-road-users:017.3)
  - Law, `SILENT`: Section 166(1) lifts the two-metre rule where a safety zone has been designated and says nothing about the speed for passing it.
  - **OPEN**: The posted speed limit caps the speed but is not a measure of "reasonable", so it is not counted.
- R "these areas": The source says "these areas"; read as the passenger areas in 3.4.5c.
  - Handbook, `STATES`: The sentence before refers to "stops where an area has been set aside for streetcar passengers", and the pedestrian section says "Some streetcar stops have a special safety island or zone for passengers getting on and off". (handbook changing-positions:038.2, handbook sharing-road-other-road-users:017.1)
  - Law, `STATES`: s. 166 (1) calls the same place a "safety zone ... set aside and designated by a by-law" under the municipal Acts, where the 2-metre rule does not apply. ([HTA 166 (1)](#on-hta-166-1))
  - **RESOLVED**: Streetcar stops with a passenger area set aside: a safety island or zone, in law a safety zone designated by by-law. None; the statement already names the area (it could say "streetcar safety zone").
- X "safety islands and zones": Repeated on the pedestrians page, with an added caution about sudden moves.
  - Handbook, `STATES`: The pedestrians page gives the same advice, “Pass these safety islands and zones at a reasonable speed” and “Always be ready, in case pedestrians make sudden or unexpected moves”, for “a special safety island or zone for passengers”, which the streetcar page calls “an area has been set aside for streetcar passengers”. (handbook changing-positions:038.2, handbook sharing-road-other-road-users:017.1, handbook sharing-road-other-road-users:017.2, handbook sharing-road-other-road-users:017.3)
  - Law, `SILENT`: No provision sets a speed for passing a streetcar safety island or zone.
  - **RESOLVED**: Pass streetcar safety islands and zones at a reasonable speed and be ready for sudden moves by pedestrians. None; the statement already joins both passages. 166 (1) names the place "a safety zone" set aside by by-law and lifts the 2 m stop rule there, but sets no speed for passing it.

### 3.4.6a

> a driver SHOULD NOT cut in [?closely] in front of a large vehicle WHEN returning to the lane after passing it BECAUSE this reduces the space cushion the large vehicle needs to stop [?safely]

RULE, ADVICE. Handbook: Sharing the road › Large commercial vehicles · ¶3.

_The source also calls it discourteous._

**Flags**

- J "closely": No gap given.
  - Handbook, `DEFINES`: For only a minimum: the general passing steps say to move back "when you can see the entire front of the vehicle you are passing in your inside mirror", at which point "you are far enough ahead to pull back", but for large vehicles the same paragraph adds that they "require a much longer distance to stop" and asks drivers to "allow more room", without saying how much more than that test. (handbook changing-positions:017.2, handbook changing-positions:029.1, handbook sharing-road-other-road-users:051.2, handbook sharing-road-other-road-users:051.5)
  - Law, `REPEATS`: The Act lets a driver move from one lane to another only once the driver "first ascertains that it can be done safely" (154(1)(a)) or "first see[s] that the movement can be made in safety" (142(1)), and gives no distance or time. ([HTA 142 (1)](#on-hta-142-1), [HTA 154 (1) (a)](#on-hta-154-1-a))
  - **PARTIAL**: At the least, do not move back in front of the large vehicle until its entire front is visible in the inside (rear-view) mirror; the extra room a large vehicle needs beyond that is not measured. Could cite the mirror test of the passing steps as the minimum in place of "closely", leaving the large-vehicle margin as advice. The earlier pass treated the mirror test as resolving this; it is a general test for any vehicle, and the handbook's own "allow more room" and the longer stopping distance of large vehicles make it a floor only. The two-second rule is the follower's own gap and is not counted.
- J "safely": Judgment term.
  - Handbook, `REPEATS`: The neighbours stay open: large commercial vehicles 'require a much longer distance to stop than smaller vehicles', and the stopping-distance figure compares a tractor-trailer with a much smaller vehicle without a number. (handbook sharing-road-other-road-users:052, handbook sharing-road-other-road-users:051.2)
  - Law, `SILENT`: The Act says nothing about the room a large vehicle needs to stop.
  - **OPEN**: The handbook's mirror test for moving back after a pass ('when you can see the entire front of the vehicle you are passing in your inside mirror', changing-positions:017.2, 029.1) bears on the separate 'closely' flag, not on the stopping cushion, and for large vehicles the handbook asks for more room than that. The move back into the lane falls under 154 (1) (a), whose 'can be done safely' is equally open.

### 3.4.6b

> a driver SHOULD allow [?more room] WHEN passing a large vehicle

RULE, ADVICE. Handbook: Sharing the road › Large commercial vehicles · ¶3.

**Flags**

- J "more room": Comparative with no baseline.
  - Handbook, `DEFINES`: For only the baseline: after any pass "when you can see all of the front of the vehicle you are passing in your rear view mirror, you are far enough ahead to pull back", and large vehicles "require a much longer distance to stop" and need a "space cushion", but the handbook never says how much more room than that baseline to allow. (handbook changing-positions:017.2, handbook changing-positions:029.1, handbook sharing-road-other-road-users:051.2, handbook sharing-road-other-road-users:051.4)
  - Law, `REPEATS`: The Act lets a driver move from one lane to another only once the driver "first ascertains that it can be done safely" (154(1)(a)) or "first see[s] that the movement can be made in safety" (142(1)), and gives no distance or time. ([HTA 142 (1)](#on-hta-142-1), [HTA 154 (1) (a)](#on-hta-154-1-a))
  - **PARTIAL**: More than the general minimum: stay out of the lane in front of the large vehicle at least until its whole front shows in the inside mirror, and then longer; the size of the extra margin is not given. Could state the mirror test as the minimum and keep "more room" as advice for the extra margin. Read in its paragraph (under "Stopping Distance"), "more room" is the gap left ahead of the large vehicle when moving back; the turbulence item ("may affect your ability to control your vehicle when passing a large one", 057.3) could also suggest side room, which no source measures.

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
  - Handbook, `DEFINES`: For only a minimum: "A safe following distance is at least two seconds behind the vehicle in front of you" (counted against a fixed marker; reaching it sooner means "you are following too closely"), the road test asks for "at least a two- to three-second distance", and the handbook calls this "a minimum following distance" that needs "extra space in certain situations"; it gives no measure for "well back" beyond that. (handbook driving-along:018.2, handbook driving-along:024.2, handbook driving-along:025.1, handbook driving-along:025.3, handbook level-two-road-test:065.1)
  - Law, `REPEATS`: Section 158(1) bars following "more closely than is reasonable and prudent having due regard for the speed of the vehicle and the traffic on and the conditions of the highway", with no distance. ([HTA 158 (1)](#on-hta-158-1))
  - **PARTIAL**: At least the two-second following distance (two to three seconds on the road test) behind the farm machinery; how much farther "well back" asks for is not said. Could replace "well back" with "at least two seconds behind", noting that more is advised. Farm machinery is not among the situations listed for extra space (bad weather, motorcycles, large trucks, heavy loads), though the handbook notes it is often oversized and its driver may not see vehicles coming up behind (068.3); "well back" suggests more than the minimum.
- J "safe": Judgment term.
  - Handbook, `DEFINES`: For some cases only: 'A solid line at the left of your lane means it is unsafe to pass'; nothing says when passing a slow vehicle is safe. (handbook pavement-markings:004.1)
  - Law, `REPEATS`: 148 (8) allows a pass only where the roadway ahead and to the left is 'safely free from approaching traffic' and to the left 'safely free from overtaking traffic', with no distance. ([HTA 148 (8)](#on-hta-148-8))
  - **PARTIAL**: Not safe at least where there is a solid line at the left of the driver's lane; on other roads it stays the driver's judgment. Could add the solid-line case; the judgment stays open elsewhere. Where passing is not permitted at all (within 30 m of a pedestrian crossover, left of centre within 30 m of a bridge, viaduct or tunnel: changing-positions:020.1, 020.2; 140 (3), 149 (1)) the result is the same. An engineering passing sight distance (OTM Book 11) was not obtained.

### 3.4.8a

> a driver SHOULD keep a [?safe] following distance behind a horse-drawn vehicle AND SHOULD NOT pass it UNLESS it is [?safe] to do so

RULE, ADVICE. Handbook: Sharing the road › Horse-drawn vehicles · ¶2.

**Flags**

- J "safe": Judgment term (twice).
  - Handbook, `DEFINES`: For the following distance: 'A safe following distance is at least two seconds behind the vehicle in front of you', a minimum that 'applies only to ideal driving conditions'; for the pass, only some cases: 'A solid line at the left of your lane means it is unsafe to pass'. (handbook driving-along:018.2, handbook driving-along:025.2, handbook pavement-markings:004.1)
  - Law, `REPEATS`: 158 (1) forbids following 'more closely than is reasonable and prudent' and 148 (8) asks for a roadway 'safely free from approaching traffic', neither with a measure. ([HTA 148 (8)](#on-hta-148-8), [HTA 158 (1)](#on-hta-158-1))
  - **PARTIAL**: Following distance: at least two seconds behind the horse-drawn vehicle in ideal conditions, more in bad weather; passing is not safe at least where a solid line is at the left of the lane. Could use two seconds for the following distance; passing stays open beyond the solid-line case. (Pass part same as on-passing-1:p17a.)

### 3.4.8b

> a driver SHOULD leave [?as much distance as possible] WHILE passing a horse-drawn vehicle BECAUSE passing too closely could startle the horse and make it change direction suddenly

RULE, ADVICE. Handbook: Sharing the road › Horse-drawn vehicles · ¶2.

**Flags**

- J "as much distance as possible": No distance given.
  - Handbook, `SILENT`: No other sentence gives a passing distance for horse-drawn vehicles; the one-metre rule is for cyclists.
  - Law, `REPEATS`: 148 (5) asks the overtaking driver to 'turn out to the left so far as may be necessary to avoid a collision', equally open; the one-metre rule of 148 (6.1) is for bicycles only. ([HTA 148 (5)](#on-hta-148-5))
  - **OPEN**: A horse-drawn vehicle is a 'vehicle' under s. 1 (1) of the Act (vehicles drawn by muscular power), so 148 (5) applies.

### 3.4.9a

> a driver SHOULD NOT pass a snow plow WHEN the snow plow is moving

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing.

**Flags**

- M "under any conditions": Absolute wording ("under any conditions") without a legal marker; the default gives SHOULD NOT.
  - Handbook, `REPEATS`: The snow-plow section warns "Do not try to pass between them" because it is "extremely dangerous", with no legal marker. (handbook driving-night-and-bad-weather:069.3, handbook driving-night-and-bad-weather:069.4)
  - Law, `STATES`: s. 148.1 (1) bans, only on a highway with a speed limit of 80 km/h or more that is divided into clearly marked lanes and only while travelling in a direction with two or more lanes, overtaking a snow plow "travelling in echelon with another plow or plows" unless the overtaking lane is entirely clear of any part of the plow, its attachments or blade. ([HTA 148.1 (1)](#on-hta-148-1-1))
  - **PARTIAL**: A legal duty only for snow plows in echelon on highways posted 80 km/h or more with two or more marked lanes in the driver's direction, unless the overtaking lane is entirely clear of the plow and its blade. Keep ADVICE for the general ban; the echelon case on such highways is LAW under s. 148.1 (1). s. 148.1 (2) sets a fine of $150 to $1,000; the handbook's "under any conditions" is much broader than the Act.

### 3.4.9b

> a driver SHOULD NOT pass between snow plows WHEN several snow plows are staggered across a freeway BECAUSE there is not [?enough] room to pass [?safely] AND the ridge of wet snow can throw the vehicle out of control

RULE, ADVICE. Handbook: Night and bad weather › Snow plows · ¶2.

**Flags**

- J "enough": Judgment term.
  - Handbook, `STATES`: Elsewhere the handbook says 'Don't pass moving snow plows under any conditions' and that a plow wing 'extends as far as three metres to the right of the vehicle', so no room between plows is treated as enough; it gives no clearance figure. (handbook changing-positions:013.2, handbook driving-night-and-bad-weather:069.1)
  - Law, `DEFINES`: 148.1 (1) forbids overtaking a plow 'travelling in echelon with another plow or plows' on a highway posted 80 km/h or more with two or more marked lanes in the driver's direction 'unless the lane of travel that is used by the overtaking vehicle to overtake the snow plow is entirely clear of any part of the snow plow, including any part of an attachment or the plow blade'. ([HTA 148.1 (1)](#on-hta-148-1-1))
  - **RESOLVED**: Room is enough only if the lane used to overtake is entirely clear of any part of the plows, including attachments and blades; with plows staggered across all lanes no lane is, and the handbook says not to pass moving plows at all. Strength LAW on highways posted 80 km/h or more with two or more lanes in the driver's direction, with the Act's test in place of 'enough room'. The handbook (never pass a moving plow) is stricter than the Act (allowed when the lane is entirely clear); a freeway posted below 80 km/h would fall outside 148.1 but inside the handbook's ban.
- J "safely": Judgment term.
  - Handbook, `STATES`: Elsewhere the handbook says 'Don't pass moving snow plows under any conditions' and that a plow wing 'extends as far as three metres to the right of the vehicle', so no room between plows is treated as enough; it gives no clearance figure. (handbook changing-positions:013.2, handbook driving-night-and-bad-weather:069.1)
  - Law, `DEFINES`: 148.1 (1) forbids overtaking a plow 'travelling in echelon with another plow or plows' on a highway posted 80 km/h or more with two or more marked lanes in the driver's direction 'unless the lane of travel that is used by the overtaking vehicle to overtake the snow plow is entirely clear of any part of the snow plow, including any part of an attachment or the plow blade'. ([HTA 148.1 (1)](#on-hta-148-1-1))
  - **RESOLVED**: Room is enough only if the lane used to overtake is entirely clear of any part of the plows, including attachments and blades; with plows staggered across all lanes no lane is, and the handbook says not to pass moving plows at all. Strength LAW on highways posted 80 km/h or more with two or more lanes in the driver's direction, with the Act's test in place of 'enough room'. The handbook (never pass a moving plow) is stricter than the Act (allowed when the lane is entirely clear); a freeway posted below 80 km/h would fall outside 148.1 but inside the handbook's ban.

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
  - Handbook, `REPEATS`: The section presents these as warnings ("These signs warn of unusual temporary conditions"), the offence table lists "Failing to obey signs" without saying which signs, and the construction-zone advice says "obey all warning signs"; none says this instruction is law. (handbook dealing-particular-situations:036.1, handbook keeping-your-drivers-licence:113.1, handbook signs:164.1)
  - Law, `SILENT`
  - **OPEN**: s. 182 (2) makes drivers obey signs "so erected, installed or displayed" under the regulations, and O. Reg. 339/94 item 31 limits the demerit offence to signs prescribed under s. 182 (1); O. Reg. 615 s. 35 prescribes only the roadside Do Not Pass sign, and no provision in these sources prescribes a sign carried on a pilot or pace vehicle.

### 3.4.11a

> a driver SHOULD NOT pass a vehicle WHEN the vehicle is stopped at a crosswalk BECAUSE a stopped vehicle may mean a pedestrian is crossing

RULE, ADVICE. Handbook: Sharing the road › Pedestrians · item 2.

### 3.4.12a

> FACT school bus drivers and other witnesses can report vehicles that have [?illegally passed] a school bus

FACT. Handbook: Stopping › Stopping for school buses · ¶6.

_The law behind it is 3.4.12b, from the same section of the Stopping page._

**Flags**

- G "illegally passed": Implies a prohibition on passing; the law behind it is the duty to stop in 3.4.12b.
  - Handbook, `STATES`: The handbook names the illegal act as not stopping: "It is illegal to fail to stop for a stopped school bus that has its red lights flashing", "It is dangerous and illegal to fail to stop for a stopped school bus that has its overhead red lights flashing or its stop arm activated", and its offence table lists "Failing to stop for a school bus". (handbook keeping-your-drivers-licence:084.1, handbook sharing-road-other-road-users:082.1, handbook stopping:029.1)
  - Law, `STATES`: Section 175 (11) and (12) require a driver meeting or coming up behind a stopped school bus with its overhead red lights flashing to stop and "not proceed until the bus moves or the overhead red signal-lights have stopped flashing"; (11.1) and (12.1) say the same for the stop arm. There is no separate ban on passing. ([HTA 175 (11)](#on-hta-175-11), [HTA 175 (11.1)](#on-hta-175-11-1), [HTA 175 (12)](#on-hta-175-12), [HTA 175 (12.1)](#on-hta-175-12-1))
  - **RESOLVED**: Failed to stop for a stopped school bus with its overhead red lights flashing or its stop arm out, or went on before the bus moved or the signals stopped (175 (11) to (12.1)). Read "illegally passed" as "failed to stop for".

### 3.4.12b

> a driver MUST stop WHEN approaching a stopped school bus with its upper alternating red lights flashing, from either direction IF VIOLATED a [?heavy] fine AND 6 demerit points for a first offence

RULE, LAW. Handbook: Stopping › Stopping for school buses · ¶2; Stopping › Stopping for school buses · ¶6.

_This duty to stop is what makes passing a stopped school bus illegal (3.4.12a)._

**Flags**

- J "heavy": The handbook says "fined heavily" and gives no amount.
  - Handbook, `SILENT`: No handbook sentence gives the amount of the fine for failing to stop for a school bus.
  - Law, `DEFINES`: Section 175(17) sets the fine for contravening 175(11) or (12) at not less than $400 and not more than $2,000 for a first offence, and $1,000 to $4,000 or up to six months' imprisonment, or both, for each subsequent offence; O. Reg. 339/94, item 14, gives 6 demerit points. ([HTA 175 (17)](#on-hta-175-17), [O. Reg. 339/94 Table, item 14](#on-reg-339-94-item-14))
  - **RESOLVED**: A fine of $400 to $2,000 for a first offence (175(17)(a)); $1,000 to $4,000, or up to six months in jail, or both, for a subsequent offence (175(17)(b)); plus 6 demerit points (O. Reg. 339/94, item 14). Replace "a heavy fine" with "a fine of $400 to $2,000" for a first offence. The handbook's offence table lists "Failing to stop for a school bus" under six points (keeping-your-drivers-licence:084.1), matching item 14.
- X "stop arm activated": Repeated on Sharing the road (which also counts the stop arm), the Signs page and the six-point offence table.
  - Handbook, `STATES`: The Sharing-the-road list makes the stop arm a trigger of its own (“When you see a school bus with its overhead red lights flashing or its stop arm activated”; “You must stop whether you are behind or approaching the bus”; “It is dangerous and illegal to fail to stop for a stopped school bus that has its overhead red lights flashing or its stop arm activated”). (handbook sharing-road-other-road-users:077.1, handbook sharing-road-other-road-users:078.1, handbook sharing-road-other-road-users:082.1)
  - Law, `STATES`: A stopped bus “that has its stop arm actuated” brings its own duty to stop, meeting it (175 (11.1)) or from the rear (175 (12.1)), beside the red-light duties (175 (11), (12)), all punishable under 175 (17); O. Reg. 339/94 item 14 lists only “Subsections 175 (11) and (12)” for the 6 demerit points. ([HTA 175 (11)](#on-hta-175-11), [HTA 175 (11.1)](#on-hta-175-11-1), [HTA 175 (12)](#on-hta-175-12), [HTA 175 (12.1)](#on-hta-175-12-1), [HTA 175 (17)](#on-hta-175-17), [O. Reg. 339/94 Table, item 14](#on-reg-339-94-item-14))
  - **RESOLVED**: Stop for a stopped school bus with its overhead red signal-lights flashing or with its stop arm actuated, either one alone. Add OR its stop arm is actuated. By O. Reg. 339/94 item 14 the six demerit points attach to the red-light duties; the stop-arm duties carry the 175 (17) fine.

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
  - Handbook, `STATES`: The figures call 20 metres "the required stopping distance" for vehicles coming up behind a school bus with lights flashing, the same section says "You must obey the school bus law on any road", and the knowledge-test topics include "What drivers must do when they meet streetcars and school buses". (handbook stopping:024, handbook stopping:025, handbook getting-your-drivers-licence:164.1, handbook stopping:027.1)
  - Law, `STATES`: s. 175 (12.2) requires every driver approaching from the rear a stopped school bus that has its overhead red signal-lights flashing or its stop arm actuated to "stop at least 20 metres before reaching the bus", and s. 175 (17) makes contravening it an offence ($400 to $2,000 for a first offence). ([HTA 175 (12.2)](#on-hta-175-12-2), [HTA 175 (17)](#on-hta-175-17))
  - **RESOLVED**: A legal duty: when approaching from the rear a stopped school bus with its overhead red lights flashing or its stop arm actuated, stop at least 20 m before reaching the bus. Strength LAW; the condition covers red lights OR stop arm, and the 20 m is measured before reaching the bus. O. Reg. 339/94 item 14 gives 6 demerit points only for s. 175 (11) and (12), not (12.2), so the 20 m distance carries the s. 175 (17) fine but no listed demerit points.

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
  - Handbook, `STATES`: It calls failing to stop "dangerous and illegal" and "illegal", says witnesses "can report vehicles that have illegally passed a school bus", and "You must obey the school bus law on any road", so going past the stopped bus is treated as law. (handbook sharing-road-other-road-users:082.1, handbook stopping:027.1, handbook stopping:029.1, handbook stopping:029.3)
  - Law, `STATES`: s. 175 (11) and (12) require the driver who meets, or approaches from the rear, a stopped school bus with its overhead red signal-lights flashing to stop and "not proceed until the bus moves or the overhead red signal-lights have stopped flashing"; s. 175 (11.1) and (12.1) say the same for the stop arm, and s. 175 (17) makes each an offence. ([HTA 175 (11)](#on-hta-175-11), [HTA 175 (11.1)](#on-hta-175-11-1), [HTA 175 (12)](#on-hta-175-12), [HTA 175 (12.1)](#on-hta-175-12-1), [HTA 175 (17)](#on-hta-175-17))
  - **RESOLVED**: A legal duty: after stopping for the bus, do not proceed until the bus moves or the overhead red lights have stopped flashing. Strength LAW; the wording matches s. 175 (11) and (12). When the stop arm is also out, s. 175 (11.1) and (12.1) add: until the bus moves or the arm is no longer actuated. Meeting drivers on a highway with a median strip are excluded.
- X "and its stop arm is no longer activated": Elsewhere the stop ends only when every condition holds (bus moves, lights stop, arm folds away); here either one ends it.
  - Handbook, `STATES`: The other passages give different end points: “Do not proceed on your route until the bus moves, the overhead red lights have stopped flashing and its stop arm is no longer activated” and “Remain stopped until the arm folds away and all lights stop flashing”. (handbook sharing-road-other-road-users:081.1, handbook stopping:028.3)
  - Law, `STATES`: Each signal has its own end point: the red-light duty lasts “until the bus moves or the overhead red signal-lights have stopped flashing” (175 (11), (12)) and the stop-arm duty “until the bus moves or the stop arm is no longer actuated” (175 (11.1), (12.1)). ([HTA 175 (11)](#on-hta-175-11), [HTA 175 (11.1)](#on-hta-175-11-1), [HTA 175 (12)](#on-hta-175-12), [HTA 175 (12.1)](#on-hta-175-12-1))
  - **RESOLVED**: A driver stopped for a school bus may go once the bus moves, or once every signal that was on has stopped: the overhead red signal-lights have stopped flashing and the stop arm is no longer actuated. For the red lights alone the statement matches 175 (11) and (12); when the stop arm is also out, the driver must also wait until it is no longer actuated, unless the bus moves. Each signal is its own duty, each lasting until the bus moves or that signal stops.

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
  - Handbook, `REPEATS`: The next sentences say what to do while slowing, "assess the speed of the surrounding traffic and the condition of the roadway" and "brake early and gradually", and the offence table says "carefully pass"; no measure of caution or speed is given. (handbook dealing-particular-situations:095.2, handbook dealing-particular-situations:095.3, handbook keeping-your-drivers-licence:105.1)
  - Law, `REPEATS`: Section 159(2) uses the same words, "slow down and proceed with caution", adding only the factors ("having due regard for traffic on and the conditions of the highway and the weather") and the goal ("to ensure that the driver does not collide with the emergency vehicle or tow truck or endanger any person outside"); the 2027 version keeps them and the demerit item repeats "proceed with caution". ([HTA 159 (2)](#on-hta-159-2), [HTA 159 (2), in force January 1, 2027](#on-hta-159-2-2027), [O. Reg. 339/94 Table, item 36.2](#on-reg-339-94-item-36-2))
  - **OPEN**: The Act's goal (no collision, no danger to anyone outside the stopped vehicle) could be added after "caution" to say what it is for, but it is not a measure, so the earlier definition is moved here.

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
  - Handbook, `DEFINES`: In part: the move-over steps ask the driver to 'double check your rearview mirrors and shoulder check your blind spots to ensure no other vehicles are moving into or approaching that lane too fast', and the lane-change task measures the space as 'at least a two- to three-second distance behind the vehicle in front of you', without moving 'in beside another vehicle or into the blind spot of another vehicle'; traffic coming from behind is left at 'too fast'. (handbook dealing-particular-situations:097.3, handbook level-two-road-test:077.1, handbook level-two-road-test:077.2)
  - Law, `REPEATS`: 159 (3) (and its version in force January 1, 2027) requires the move into another lane 'if the movement can be made safely', and demerit item 36.3 reads 'if safe to do so', with no measure. ([HTA 159 (3)](#on-hta-159-3), [HTA 159 (3), in force January 1, 2027](#on-hta-159-3-2027), [O. Reg. 339/94 Table, item 36.3](#on-reg-339-94-item-36-3))
  - **PARTIAL**: Safe to move over at least requires a two- to three-second gap behind the vehicle ahead in the new lane and not moving in beside another vehicle or into its blind spot; the gap to traffic approaching from behind stays a judgment. Could add the gap and side checks; the Act's test stays 'can be made safely'. The handbook's demerit list says 'where possible' (keeping-your-drivers-licence:106.1, a source here), which differs from 'if safe to do so' in 097.1 and in item 36.3.
- X "where possible": The offence table qualifies the same duty with "where possible" instead of "if safe to do so".
  - Handbook, `STATES`: The narrative gives the condition as “if safe to do so” (“you are required to move into a lane away from the emergency vehicle or tow truck, if safe to do so”; “When safe to do so, change lanes well in advance”), where the offence table says where possible. (handbook dealing-particular-situations:097.1, handbook dealing-particular-situations:097.4)
  - Law, `STATES`: On a highway with two or more lanes on that side, a driver in the stopped vehicle's lane or the lane next to it “shall move into another lane if the movement can be made safely” (159 (3)), and O. Reg. 339/94 names the offence “Failing to move into another lane for emergency vehicle or tow truck – if safe to do so” (item 36.3). ([HTA 159 (3)](#on-hta-159-3), [HTA 159 (3), in force January 1, 2027](#on-hta-159-3-2027), [O. Reg. 339/94 Table, item 36.3](#on-reg-339-94-item-36-3))
  - **RESOLVED**: Move into another lane if the movement can be made safely; "where possible" in the offence table is a looser wording of the same condition. Keep "if safe to do so"; the duty falls on a driver in the stopped vehicle's lane or the lane next to it, as 159 (3) says. From January 1, 2027, 159 (3) also covers stopped work-related vehicles.

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
  - Handbook, `REPEATS`: Outside the towing paragraph the handbook only repeats 'be sure you have enough space and time to complete the move safely'; the towing paragraph itself asks for more space with no figure. (handbook changing-positions:001.2)
  - Law, `REPEATS`: 148 (8) asks that the roadway be 'safely free' of approaching and overtaking traffic, with no distance and nothing for trailers. ([HTA 148 (8)](#on-hta-148-8))
  - **OPEN**: The road test's two- to three-second lane-change gap and the mirror test are for ordinary vehicles; the towing section says a trailer needs more, so they do not settle it.

### 3.5.1c

> a driver towing a trailer SHOULD allow [?more room] before moving back into the lane AND SHOULD NOT cut back in [?too soon] WHEN returning to the lane after passing BECAUSE this can make the trailer sway and become hard to control

RULE, ADVICE. Handbook: Towing › Passing · ¶1.

**Flags**

- J "more room": Comparative with no baseline.
  - Handbook, `DEFINES`: For only the baseline: with a trailer "you also need more space because the length of your vehicle is much longer with a trailer attached", and after an ordinary pass "when you can see all of the front of the vehicle you are passing in your rear view mirror, you are far enough ahead to pull back"; how much more room a trailer needs beyond that is not said. (handbook changing-positions:017.2, handbook changing-positions:029.1, handbook towing:032.2)
  - Law, `REPEATS`: The Act lets a driver move from one lane to another only once the driver "first ascertains that it can be done safely" (154(1)(a)) or "first see[s] that the movement can be made in safety" (142(1)), and gives no distance or time. ([HTA 142 (1)](#on-hta-142-1), [HTA 154 (1) (a)](#on-hta-154-1-a))
  - **PARTIAL**: More than the ordinary point for moving back (the whole front of the passed vehicle showing in the mirror), because of the trailer's extra length; no amount is given. Could state the mirror test as the minimum and keep "more room" for the trailer margin. A trailer may block the inside mirror; the handbook requires "additional mirrors that provide a clear view of the road to the rear" when the load blocks the view (towing:017.1), so the mirror test can still be applied.
- J "too soon": No gap given.
  - Handbook, `DEFINES`: For only a minimum: the ordinary point for moving back is "when you can see all of the front of the vehicle you are passing in your rear view mirror, you are far enough ahead to pull back", and the sentences before ask a driver towing to "allow more room before you move back to your lane" because "the length of your vehicle is much longer with a trailer attached"; no later point is given. (handbook changing-positions:029.1, handbook towing:032.2, handbook towing:032.4)
  - Law, `REPEATS`: The Act lets a driver move from one lane to another only once the driver "first ascertains that it can be done safely" (154(1)(a)) or "first see[s] that the movement can be made in safety" (142(1)), and gives no distance or time. ([HTA 142 (1)](#on-hta-142-1), [HTA 154 (1) (a)](#on-hta-154-1-a))
  - **PARTIAL**: Moving back before the whole front of the passed vehicle shows in the mirror is too soon in every case; with a trailer the driver should wait longer, by an amount no source gives. Could cite the mirror test as the earliest point and keep "too soon" for the trailer margin. The earlier note that a trailer may block the inside mirror is met by towing:017.1, which requires additional mirrors in that case.

### 3.5.2a

> a driver towing a trailer SHOULD signal, pull over AND let the other vehicles pass WHEN the driver is holding up a line of traffic

RULE, ADVICE. Handbook: Towing › Being passed · ¶1.

**Flags**

- R "If you are holding up a line of traffic": Worded for any driver, but placed in the towing section; scoped here to towing.
  - Handbook, `STATES`: The sentence sits in the towing section under the heading Towing › Being passed, and its neighbours speak of the trailer ("the wall of wind behind it may whip your trailer to the side"), so the handbook addresses it to drivers towing; the general rule for every driver is "When faster traffic wants to pass you, move to the right and let it pass in safety". (handbook changing-positions:023.1, handbook towing:033.2, handbook towing:033.3)
  - Law, `STATES`: s. 148 (2) puts the duty to "turn out to the right and allow the overtaking vehicle ... to pass" on every person in charge of a vehicle who is overtaken, and s. 147 (1) requires any vehicle travelling below the normal speed of traffic to be driven, where practicable, in the right-hand lane or as close as practicable to the right-hand curb or edge. ([HTA 147 (1)](#on-hta-147-1), [HTA 148 (2)](#on-hta-148-2), [HTA 148 (2.1)](#on-hta-148-2-1))
  - **RESOLVED**: The handbook's sentence is addressed to drivers towing a trailer; the underlying duty to keep right and let faster vehicles pass binds every driver (s. 148 (2), s. 147 (1)). Scope: the duty to turn out to the right and let the overtaking vehicle pass applies to every driver being overtaken, not only drivers towing; "signal, pull over" remains towing advice. The Act requires turning out to the right, not pulling over onto the shoulder or stopping.

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
  - Handbook, `REPEATS`: Elsewhere the handbook describes steering only in equally open terms, "All steering should be smooth and precise" and, in a skid, "Continue to steer in the direction you wish to go. Be careful not to oversteer", and the neighbouring sentence adds only "do not brake". (handbook driving-along:003.1, handbook driving-night-and-bad-weather:039.3, handbook driving-night-and-bad-weather:039.4, handbook towing:033.4)
  - Law, `SILENT`: No provision speaks to how to steer a trailer pushed aside by wind.
  - **OPEN**

### 3.6.1a

> a driver being passed SHOULD move to the right AND let the faster vehicle pass [?in safety] WHEN faster traffic wants to pass

RULE, ADVICE. Handbook: Changing positions page · Chapter 2 › Passing; Sample test questions › Intro · ¶6; Sample test questions › Intro · item 4.

_Two of its sources come from the sample test page (question 5); keep them out of the rule set if that page is used for evaluation._

**Flags**

- M "move to the right": A sample test question says "you must" move right, and the offence table lists "Failing to share the road"; the text itself only advises.
  - Handbook, `REPEATS`: Besides the sample question, the handbook offers only the offence-table line "Failing to share the road" (two points), which does not say what it covers, and the nearby warning that speeding up when another driver is trying to pass "is unlawful". (handbook changing-positions:018.3, handbook changing-positions:018.4, handbook keeping-your-drivers-licence:114.1)
  - Law, `STATES`: s. 148 (2) requires every person on a highway who is overtaken by a vehicle travelling at a greater speed to "turn out to the right and allow the overtaking vehicle ... to pass"; s. 148 (2.1) fines a motor-vehicle driver $150 to $1,000, and O. Reg. 339/94 item 22 ("Failing to share road") gives 2 demerit points. ([HTA 148 (2)](#on-hta-148-2), [HTA 148 (2.1)](#on-hta-148-2-1), [O. Reg. 339/94 Table, item 22](#on-reg-339-94-item-22))
  - **RESOLVED**: A legal duty: when overtaken by a faster vehicle, turn out to the right and allow it to pass. Strength LAW. s. 148 (2) has no "in safety" condition; s. 148 (3) exempts road service vehicles and road-building machines at work.
- J "in safety": Judgment term.
  - Handbook, `STATES`: The handbook spells out what the driver being passed does: 'do not speed up when another driver is trying to pass you. It is unlawful and dangerous', on an undivided road 'move closer to the right side of the lane', and 'Be prepared to slow down to let the passing driver get in front of you more quickly'. (handbook changing-positions:018.3, handbook changing-positions:018.4, handbook changing-positions:023.2, handbook changing-positions:023.3)
  - Law, `STATES`: 148 (2) requires a driver who is overtaken to 'turn out to the right and allow the overtaking vehicle or equestrian to pass' with no safety qualifier (fine under 148 (2.1)), and the stunt regulation lists driving 'in a manner that indicates an intention to prevent another vehicle from passing'. ([HTA 148 (2)](#on-hta-148-2), [HTA 148 (2.1)](#on-hta-148-2-1), [O. Reg. 455/07 3, para. 8, subpara. i](#on-reg-455-07-3-8-i))
  - **RESOLVED**: Letting the faster vehicle pass in safety means moving to the right (closer to the right side of the lane on an undivided road), not speeding up, and being ready to slow down so it can get in front sooner. Could replace 'in safety' with these actions; strength LAW under 148 (2). The Act's duty has no 'in safety' qualifier.

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
  - Handbook, `REPEATS`: The behaviour is listed after "Other types of aggressive driving include" in the dangerous-behaviours sanctions section, with no penalty of its own; the chapter opens by naming "stunt" driving among its strictest laws and saying court sanctions "can quickly escalate and include fines in the tens of thousands of dollars ... lifetime bans and even jail time", and the offence table gives "Racing" six points, without linking either to this behaviour. (handbook keeping-your-drivers-licence:081.1, handbook other-ways-lose-your-licence:001.1, handbook other-ways-lose-your-licence:001.2, handbook other-ways-lose-your-licence:016.1)
  - Law, `DEFINES`: O. Reg. 455/07, s. 3, para. 8 i makes "driving a motor vehicle in a manner that indicates an intention to prevent another vehicle from passing" a stunt under s. 172 (1); on conviction the fine is $2,000 to $10,000, up to six months in jail, or both (s. 172 (2)), the licence is suspended for at least one year on a first conviction, three years on a second and indefinitely on a third (s. 172 (3)), at the roadside the licence is suspended for 30 days and the vehicle impounded for 14 days (s. 172 (9), (10)), and O. Reg. 339/94 item 3 gives 6 demerit points. ([HTA 172 (1)](#on-hta-172-1), [HTA 172 (10)](#on-hta-172-10), [HTA 172 (2)](#on-hta-172-2), [HTA 172 (3)](#on-hta-172-3), [HTA 172 (9)](#on-hta-172-9), [O. Reg. 339/94 Table, item 3](#on-reg-339-94-item-3), [O. Reg. 455/07 3](#on-reg-455-07-3), [O. Reg. 455/07 3, para. 8, subpara. i](#on-reg-455-07-3-8-i))
  - **RESOLVED**: A stunt under s. 172 (O. Reg. 455/07, s. 3, para. 8 i): fine of $2,000 to $10,000, up to six months in jail, or both; licence suspension of at least one year on a first conviction (three years on a second, indefinite on a third); roadside 30-day licence suspension and 14-day vehicle impoundment; 6 demerit points. Replace the placeholder with the s. 172 sanctions; the regulation's test is driving "in a manner that indicates an intention" to prevent passing.

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
  - Handbook, `DEFINES`: Elsewhere the handbook ties keeping right to speed relative to other traffic, "Keep to the right of the road or in the right-hand lane on multi-lane roads" being "especially important if you are driving more slowly than other vehicles", and uses the Act's "normal speed of traffic at that time and place" for cyclists. (handbook driving-along:010.1, handbook driving-along:010.2, handbook sharing-road-other-road-users:028.1)
  - Law, `DEFINES`: Section 147(1) applies to "any vehicle travelling upon a roadway at less than the normal speed of traffic at that time and place" and requires it, "where practicable", to be driven in the right-hand lane then available or as close as practicable to the right curb or edge. ([HTA 147 (1)](#on-hta-147-1))
  - **RESOLVED**: A vehicle travelling at less than the normal speed of traffic at that time and place (147(1)). Replace "slow traffic" with this, and add the Act's "where practicable". 147(3) makes it an offence (fine $150 to $1,000). The sign itself is a regulatory sign that must be obeyed (182(2)).

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
  - Handbook, `REPEATS`: Both places say only "many": "On many high-speed roads with three or more lanes in each direction, trucks are not allowed to drive in the far left-hand lane" and "On many freeways with three or more lanes in each direction, large trucks cannot travel in the far left lane". (handbook changing-positions:024.1, handbook freeway-driving:022.3)
  - Law, `DEFINES`: O. Reg. 608 s. 1 (1) bars a commercial motor vehicle, alone or with a towed vehicle, over 6.5 metres long from the left lane (or, where the left lane is an HOV lane, the lane next to it) "of those portions of a highway described in the Schedules", which list each stretch by end points (parts of Highways 400, 401, 403, 404, 407, 409, 410, 417, 427, the QEW, and 7 and 8 in Kitchener); s. 1 (2) exempts buses, ambulances, fire apparatus, vehicles in maintenance or construction, tow trucks called to the lane, and emergencies. ([Reg. 608 1 (1)](#on-reg-608-1-1), [Reg. 608 1 (2)](#on-reg-608-1-2))
  - **RESOLVED**: The portions of highways described in the Schedules to O. Reg. 608. Replace "one of many high-speed roads with 3 or more lanes" with the scheduled portions, "truck" with a commercial motor vehicle (alone or towing) over 6.5 m long, and add the s. 1 (2) exceptions; where the left lane is an HOV lane, the barred lane is the one next to it. The regulation does not turn on the number of lanes or on "high-speed"; the handbook's "three or more lanes in each direction" is descriptive.
- X "many freeways": The Freeway page says "many freeways"; Changing positions says "many high-speed roads".
  - Handbook, `STATES`: The Changing-positions page says many high-speed roads where the Freeway page says many freeways: “On many high-speed roads with three or more lanes in each direction, trucks are not allowed to drive in the far left-hand lane”; neither names the roads. (handbook changing-positions:024.1, handbook changing-positions:024.2)
  - Law, `DEFINES`: O. Reg. 608, s. 1 (1) bars “a commercial motor vehicle or any combination of a commercial motor vehicle and a towed vehicle that exceeds 6.5 metres in length” from “the left lane” (or the lane next to a left-hand high occupancy vehicle lane) “of those portions of a highway described in the Schedules”, and s. 1 (2) exempts a bus, ambulance or fire apparatus, a vehicle engaged in maintenance or construction, a tow truck called to a vehicle in or near the left lane, and an emergency. ([Reg. 608 1 (1)](#on-reg-608-1-1), [Reg. 608 1 (2)](#on-reg-608-1-2))
  - **RESOLVED**: Trucks / large trucks = commercial motor vehicles, or combinations with a towed vehicle, over 6.5 m long, other than the exempt vehicles; the roads = the portions of Highways 400, 401, 403, 404, 407, 407 East, 409, 410, 417, 427, the QEW, the QEW/403 and Highways 7, 8 and 7/8 in Kitchener listed in the Schedules to O. Reg. 608. Replace the [?many] high-speed roads (or freeways) with 3 or more lanes each way by the highway portions in the Schedules, and truck by a commercial motor vehicle or combination over 6.5 m; the regulation does not itself require three lanes. Where the left lane is an HOV lane, the barred lane is the one next to it.

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
  - Handbook, `DEFINES`: For the gap ahead only: the road test says to signal "when there is enough space for you to change lanes", to "keep at least a two- to three-second distance behind the vehicle in front of you" and not to "move in beside another vehicle or into the blind spot of another vehicle", while the gap behind is left at "no one is coming too fast from behind". (handbook changing-positions:007.1, handbook level-two-road-test:076.1, handbook level-two-road-test:077.1, handbook level-two-road-test:077.2)
  - Law, `REPEATS`: Section 148(2) makes turning out to the right for a faster overtaking vehicle a duty but sets no time, and 154(1)(a) allows the lane change only once the driver "first ascertains that it can be done safely". ([HTA 148 (2)](#on-hta-148-2), [HTA 154 (1) (a)](#on-hta-154-1-a))
  - **PARTIAL**: At the first gap in the right-hand lane that lets the driver keep at least two to three seconds behind the vehicle ahead without moving in beside another vehicle or into its blind spot. Could replace "as soon as you can" with "at the first gap that meets the lane-change test". The gap behind ("no one is coming too fast from behind") and how long the driver may wait for a gap are not measured.

**Law**

- `a driver in the truck passing lane MUST move into the right-hand lane [?as soon as the driver can] WHEN a truck travelling at a greater speed overtakes the driver IF VIOLATED a fine of $150 to $1,000 AND 2 demerit points`
  - [HTA 148 (2)](#on-hta-148-2), [HTA 148 (2.1)](#on-hta-148-2-1), [O. Reg. 339/94 Table, item 22](#on-reg-339-94-item-22). The Act gives no time.

**Compared with the law**

- `SAME` [HTA 148 (2)](#on-hta-148-2): The Act makes moving right for a faster vehicle a duty; the handbook words it as advice.
- `PENALTY` [HTA 148 (2.1)](#on-hta-148-2-1): $150 to $1,000.
- `PENALTY` [O. Reg. 339/94 Table, item 22](#on-reg-339-94-item-22): 2 demerit points (failing to share road).

## Provisions

<a id="on-hta-1-1-roadway"></a>**R.S.O. 1990, c. H.8, s. 1 (1), "roadway", Definitions** · [hta.txt, line 2681](../../../statutes/on/hta/hta.txt#L2681) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> “roadway” means the part of the highway that is improved, designed or ordinarily used for vehicular traffic, but does not include the shoulder, and, where a highway includes two or more separate roadways, the term “roadway” refers to any one roadway separately and not to all of the roadways collectively;

<a id="on-hta-1-1-vehicle"></a>**R.S.O. 1990, c. H.8, s. 1 (1), "vehicle", Definitions** · [hta.txt, line 2693](../../../statutes/on/hta/hta.txt#L2693) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> “vehicle” includes a motor vehicle, trailer, traction engine, farm tractor, road-building machine, bicycle and any vehicle drawn, propelled or driven by any kind of power, including muscular power, but does not include a motorized snow vehicle or a street car;

<a id="on-hta-140-3"></a>**R.S.O. 1990, c. H.8, s. 140 (3), Passing moving vehicles within 30 metres of pedestrian crossover** · [hta.txt, line 8717](../../../statutes/on/hta/hta.txt#L8717) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (3) When a vehicle is approaching a pedestrian crossover and is within 30 metres of it, the driver of any other vehicle approaching from the rear shall not allow the front extremity of his or her vehicle to pass beyond the front extremity of the other vehicle.

<a id="on-hta-141-5"></a>**R.S.O. 1990, c. H.8, s. 141 (5), Left turn, across path of approaching vehicle** · [hta.txt, line 8751](../../../statutes/on/hta/hta.txt#L8751) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (5) No driver or operator of a vehicle in an intersection shall turn left across the path of a vehicle approaching from the opposite direction unless he or she has afforded a reasonable opportunity to the driver or operator of the approaching vehicle to avoid a collision.

<a id="on-hta-142-1"></a>**R.S.O. 1990, c. H.8, s. 142 (1), Signal for left or right turn** · [hta.txt, line 8762](../../../statutes/on/hta/hta.txt#L8762) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> 142 (1) The driver or operator of a vehicle upon a highway before turning to the left or right at any intersection or into a private road or driveway or from one lane for traffic to another lane for traffic or to leave the roadway shall first see that the movement can be made in safety, and if the operation of any other vehicle may be affected by the movement shall give a signal plainly visible to the driver or operator of the other vehicle of the intention to make the movement.

<a id="on-hta-147-1"></a>**R.S.O. 1990, c. H.8, s. 147 (1), Slow vehicles to travel on right side** · [hta.txt, line 9002](../../../statutes/on/hta/hta.txt#L9002) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> 147 (1) Any vehicle travelling upon a roadway at less than the normal speed of traffic at that time and place shall, where practicable, be driven in the right-hand lane then available for traffic or as close as practicable to the right hand curb or edge of the roadway.

<a id="on-hta-147-2"></a>**R.S.O. 1990, c. H.8, s. 147 (2), Exception** · [hta.txt, line 9004](../../../statutes/on/hta/hta.txt#L9004) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (2) Subsection (1) does not apply to a driver of a, (a) vehicle while overtaking and passing another vehicle proceeding in the same direction; (b) vehicle while preparing for a left turn at an intersection or into a private road or driveway; (c) road service vehicle; or (d) bicycle in a lane designated under subsection 153 (2) for travel in the opposite direction of traffic.

<a id="on-hta-147-3"></a>**R.S.O. 1990, c. H.8, s. 147 (3), Offence** · [hta.txt, line 9010](../../../statutes/on/hta/hta.txt#L9010) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (3) Every person who, while driving a motor vehicle, contravenes this section is guilty of an offence and on conviction is liable to a fine of not less than $150 and not more than $1,000.

<a id="on-hta-148-2"></a>**R.S.O. 1990, c. H.8, s. 148 (2), Vehicles or equestrians overtaken** · [hta.txt, line 9018](../../../statutes/on/hta/hta.txt#L9018) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (2) Every person in charge of a vehicle or on horseback on a highway who is overtaken by a vehicle or equestrian travelling at a greater speed shall turn out to the right and allow the overtaking vehicle or equestrian to pass.

<a id="on-hta-148-2-1"></a>**R.S.O. 1990, c. H.8, s. 148 (2.1), Offence** · [hta.txt, line 9020](../../../statutes/on/hta/hta.txt#L9020) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (2.1) Every person who, while driving a motor vehicle, contravenes subsection (2) is guilty of an offence and on conviction is liable to a fine of not less than $150 and not more than $1,000.

<a id="on-hta-148-5"></a>**R.S.O. 1990, c. H.8, s. 148 (5), Vehicles or equestrians overtaking others** · [hta.txt, line 9026](../../../statutes/on/hta/hta.txt#L9026) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (5) Every person in charge of a vehicle or on horseback on a highway who is overtaking another vehicle or equestrian shall turn out to the left so far as may be necessary to avoid a collision with the vehicle or equestrian overtaken, and the person overtaken is not required to leave more than one-half of the roadway free.

<a id="on-hta-148-6"></a>**R.S.O. 1990, c. H.8, s. 148 (6), Bicycles overtaken** · [hta.txt, line 9028](../../../statutes/on/hta/hta.txt#L9028) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (6) Every person on a bicycle or motor assisted bicycle who is overtaken by a vehicle or equestrian travelling at a greater speed shall turn out to the right and allow the vehicle or equestrian to pass and the vehicle or equestrian overtaking shall turn out to the left so far as may be necessary to avoid a collision.

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

<a id="on-hta-168"></a>**R.S.O. 1990, c. H.8, s. 168, Use of passing beam** · [hta.txt, line 9334](../../../statutes/on/hta/hta.txt#L9334) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> 168 When on a highway at any time when lighted lamps are required to be displayed on vehicles, the driver of a motor vehicle equipped with multiple beam headlamps shall use the lower or passing beam when,
(a) approaching an oncoming vehicle within 150 metres; or
(b) following another vehicle within 60 metres, except when in the act of overtaking and passing.

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

<a id="on-hta-75-5"></a>**R.S.O. 1990, c. H.8, s. 75 (5), Alarm bell to be sounded** · [hta.txt, line 6454](../../../statutes/on/hta/hta.txt#L6454) · [e-Laws](https://www.ontario.ca/laws/statute/90h08)

> (5) Every motor vehicle, motor assisted bicycle and bicycle shall be equipped with an alarm bell, gong or horn, which shall be kept in good working order and sounded whenever it is reasonably necessary to notify pedestrians or others of its approach.

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

<a id="on-reg-608-1-2"></a>**R.R.O. 1990, Reg. 608, s. 1 (2)** · [900608.txt, line 134](../../../statutes/on/reg-608/900608.txt#L134) · [e-Laws](https://www.ontario.ca/laws/regulation/900608)

> (2) Subsection (1) does not apply to a person operating a commercial motor vehicle if, (a) the vehicle is a bus, an ambulance or a fire apparatus; (b) the vehicle is engaged in maintenance or construction; (c) the vehicle is a tow truck that has been requested to provide towing services or roadside assistance services to a vehicle in or near the left lane, and operating the tow truck in the lane is necessary to access the location of the vehicle; or (d) an emergency requires the use of the lane by the vehicle.

<a id="on-reg-615-34-3"></a>**R.R.O. 1990, Reg. 615, s. 34 (3)** · [900615.txt, line 796](../../../statutes/on/reg-615/900615.txt#L796) · [e-Laws](https://www.ontario.ca/laws/regulation/900615)

> (3) A Lane Designation sign in Figure 7 signifies that the lane marked with the sign shall be used by a vehicle for the purpose only of making a left turn.

<a id="on-reg-615-34-4"></a>**R.R.O. 1990, Reg. 615, s. 34 (4) (a), (b)** · [900615.txt, line 797](../../../statutes/on/reg-615/900615.txt#L797) · [e-Laws](https://www.ontario.ca/laws/regulation/900615)

> (4) A Lane Designation sign, (a) may, in the case of Figures 1 to 6 and Figure 8, be erected over the lane or be ground mounted; (b) shall, in the case of Figure 7, be erected directly over a two-way left turn lane;

<a id="on-reg-615-35"></a>**R.R.O. 1990, Reg. 615, s. 35, Do Not Pass Sign** · [900615.txt, line 815](../../../statutes/on/reg-615/900615.txt#L815) · [e-Laws](https://www.ontario.ca/laws/regulation/900615)

> 35. A Do Not Pass sign erected on or after the 28th day of March, 1986 shall, (a) be not less than 60 centimetres in height and not less than 60 centimetres in width; and (b) bear the markings and have the dimensions illustrated in the following Figure:
