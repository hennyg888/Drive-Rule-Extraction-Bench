# T2 comparison: runs/t2/mto/Qwen/Qwen3.8-27B-FP8/v1/think/seed1/statements.json

Reference 88 · model 102 · paired 85

Paired statements with at least one difference: 48 of 85
## Paired statements

### 1a ↔ p05:1a (wording similarity 0.72)

**Differences:** type DEFINE → FACT

Claude:

`1a` DEFINE · None · None

> DEFINE changing position IS a manoeuvre THAT changes lanes OR passes another vehicle

sources m1

Model:

`p05:1a` FACT · None · None

> FACT changing position on the road involves changing lanes or passing another vehicle

sources m1

### 1b ↔ p05:1b (wording similarity 0.75)

**No structural differences.**

Claude:

`1b` DEFINE · None · None

> DEFINE passing IS a lane change THAT moves past a slower vehicle ALSO CALLED overtaking

sources m2 · flags V “overtaking”

Model:

`p05:1b` DEFINE · None · None

> DEFINE passing IS changing lanes THAT moves past a slower vehicle

sources m2

### 1c ↔ p05:1c (wording similarity 0.47)

**No structural differences.**

Claude:

`1c` FACT · None · None

> FACT vehicles on the same road do not all travel at the same speed, even though every public road has a speed limit

sources m3

Model:

`p05:1c` FACT · None · None

> FACT not all vehicles travel at the same speed

sources m3

### 1d ↔ p05:1d (wording similarity 0.97)

**No structural differences.**

Claude:

`1d` FACT · None · None

> FACT cyclists, road service vehicles and drivers preparing to turn are [?usually] slower than through traffic

sources m3 · flags S “usually”

Model:

`p05:1d` FACT · None · None

> FACT cyclists, road service vehicles and drivers ahead preparing to turn are [?usually] slower than through traffic

sources m3 · flags S “usually”

### 2.1a ↔ p05:2.1a (wording similarity 0.55)

**Differences:** missing clause ONLY IF; extra clause WHEN; vague extra: sure

Claude:

`2.1a` RULE · ADVISORY · imperative ("be sure")

> a driver SHOULD start a lane change or a pass ONLY IF the driver has [?enough] space and time to complete it [?safely]

sources m4 · flags J “enough”, J “safely”

Model:

`p05:2.1a` RULE · ADVISORY · imperative ("be sure")

> a driver SHOULD be [?sure] the driver has [?enough] space and time to complete a lane change or pass a vehicle [?safely] WHEN the driver is about to change lanes or pass a vehicle

sources m1, m4 · flags J “sure”, J “enough”, J “safely”

### 2.1b ↔ p05:2.1b (wording similarity 0.88)

**Differences:** vague extra: danger

Claude:

`2.1b` RULE · ADVISORY · imperative ("Never")

> a driver SHOULD NOT pass a vehicle UNLESS the driver is [?sure] the pass can be made without danger to the driver or others

sources m5 · flags J “sure”

Model:

`p05:2.1b` RULE · ADVISORY · imperative ("Never")

> a driver SHOULD NOT pass a vehicle UNLESS the driver is [?sure] the driver can pass without [?danger] to the driver or other road users

sources m5 · flags M “Never”, J “sure”, J “danger”

### 2.1c ↔ p05:2.1c (wording similarity 1.00)

**No structural differences.**

Claude:

`2.1c` RULE · ADVISORY · imperative ("do not")

> a driver SHOULD NOT pass WHEN the driver is [?in doubt]

sources m6 · flags J “in doubt”

Model:

`p05:2.1c` RULE · ADVISORY · imperative ("do not")

> a driver SHOULD NOT pass WHEN the driver is [?in doubt]

sources m6 · flags J “in doubt”

### 2.1d ↔ p02:2.1a (wording similarity 0.92)

**No structural differences.**

Claude:

`2.1d` RULE · ADVISORY · imperative ("Keep to the right")

> a driver SHOULD keep to the right of the road, or to the right-hand lane of a multi-lane road UNLESS the driver is turning left OR passing another vehicle

sources m7

Model:

`p02:2.1a` RULE · ADVISORY · imperative ("Keep")

> a driver SHOULD keep to the right of the road or in the right-hand lane on multi-lane roads UNLESS the driver wants to turn left OR pass another vehicle

sources m7

### 2.2a ↔ p05:2.2a (wording similarity 1.00)

**Differences:** extra clause ONLY IF; vague extra: clear

Claude:

`2.2a` PROCEDURE · ADVISORY · imperative steps

> TO pass a vehicle
> 1. signal left AND check that the way is clear ahead and behind
> 2. move into the passing lane
> 3. WATCH FOR bicycles and small vehicles hidden in front of the vehicle being passed, vehicles turning left ahead, and vehicles or pedestrians entering from a road or driveway
> 4. signal right to return to the original lane
> 5. move back into the original lane WHEN the entire front of the vehicle being passed is visible in the inside mirror
> IF. IF the vehicle being passed speeds up THEN do not race AND go back to the original lane

sources m10, m11, m13, m14, m8, m9 · flags V “inside mirror”

Model:

`p05:2.2a` PROCEDURE · ADVISORY · imperative steps

> TO pass a vehicle
> 1. use the left-turn signal to show the driver wants to pass AND check that the way is [?clear] ahead and behind WHEN the driver is about to move into the passing lane
> 2. WATCH FOR bicycles and small vehicles that may be hidden from view in front of the vehicle being passed AND vehicles that may be turning left in front of the driver AND vehicles or pedestrians entering the road from another road or driveway
> 3. change lanes into the passing lane ONLY IF the driver has signalled
> 4. signal that the driver wants to move back into the original lane WHEN the driver has passed the vehicle being passed
> 5. change lanes into the original lane WHEN the driver can see the entire front of the vehicle being passed in the inside mirror
> IF. IF the vehicle being passed speeds up THEN do not race AND go back into the original lane

sources m10, m11, m13, m14, m52, m8, m9 · flags J “clear”, V “rear view mirror”

### 2.2b ↔ p05:2.2b (wording similarity 0.69)

**Differences:** missing clause WHEN; extra clause WHILE; vague extra: suddenly

Claude:

`2.2b` RULE · ADVISORY · caution ("Be careful not to")

> a driver SHOULD NOT cut off the vehicle being passed by moving in front of it suddenly WHEN returning to the original lane

sources m12

Model:

`p05:2.2b` RULE · ADVISORY · caution ("Be careful not to")

> a driver SHOULD NOT cut off a vehicle by [?suddenly] moving in front of it WHILE passing

sources m12 · flags J “suddenly”

### 3.1.1a ↔ p05:3.1.1a (wording similarity 1.00)

**No structural differences.**

Claude:

`3.1.1a` RULE · LEGAL · text ("is not permitted", "must not")

> a driver MUST NOT pass a vehicle WHEN the driver is within 30 m of a pedestrian crossover

sources m15, m16 · flags X “within 30 m”

Model:

`p05:3.1.1a` RULE · LEGAL · text ("not permitted")

> a driver MUST NOT pass a vehicle WHEN the driver is within 30 m of a pedestrian crossover

sources m15

### 3.1.2a ↔ p05:3.1.2a (wording similarity 0.92)

**Differences:** vague not marked: 30 m from, on the left of a centreline

Claude:

`3.1.2a` RULE · LEGAL · text ("is not permitted")

> a driver MUST NOT pass [?on the left of a centreline] WHEN the driver is [?30 m from] a bridge, viaduct or tunnel

sources m17 · flags R “30 m from”, G “on the left of a centreline”

Model:

`p05:3.1.2a` RULE · LEGAL · text ("not permitted")

> a driver MUST NOT pass left of a centreline WHEN the driver is within 30 m of a bridge, viaduct or tunnel

sources m17

### 3.1.3a ↔ p05:3.1.3a (wording similarity 0.79)

**Differences:** vague not marked: enough, safely; vague extra: enough clear, in safety

Claude:

`3.1.3a` RULE · ADVISORY · imperative ("Don't attempt")

> a driver SHOULD NOT pass WHEN (the driver is approaching the crest of a hill OR the driver is on a curve) AND the view of oncoming traffic is obstructed AND the clear distance ahead is not [?enough] to pass [?safely]

sources m18 · flags J “enough”, J “safely”

Model:

`p05:3.1.3a` RULE · ADVISORY · imperative ("Don't")

> a driver SHOULD NOT attempt to pass WHEN (the driver is approaching the crest of a hill OR the driver is on a curve) AND the driver's view of oncoming traffic is obstructed AND there is not [?enough clear] distance ahead to pass [?in safety]

sources m18 · flags J “enough clear”, J “in safety”

### 3.1.4a ↔ p06:3.1.4a (wording similarity 0.73)

**No structural differences.**

Claude:

`3.1.4a` RULE · ADVISORY · default (prescriptive passive "are not to be used")

> a driver SHOULD NOT use a two-way left-turn lane for passing

sources m19 · flags M “are not to be used”

Model:

`p06:3.1.4a` RULE · ADVISORY · default ("are not to be used for passing")

> a driver SHOULD NOT pass in a left-turn lane

sources m19 · flags D “are not to be used for passing”

### 3.1.5a ↔ p11:1a (wording similarity 0.78)

**No structural differences.**

Claude:

`3.1.5a` FACT · None · None

> FACT pavement markings show, among other things, where it is not [?safe] to pass

sources m20 · flags J “safe”

Model:

`p11:1a` FACT · None · None

> FACT pavement markings tell a driver when it is not [?safe] to pass

sources m20 · flags J “safe”

### 3.1.5b ↔ p11:3.1.5a (wording similarity 0.89)

**Differences:** vague extra: safe

Claude:

`3.1.5b` RULE · ADVISORY · text ("should not")

> a driver SHOULD NOT pass WHEN there is a solid line at the left of the driver's lane BECAUSE a solid line there means it is unsafe to pass

sources m21, m22

Model:

`p11:3.1.5a` RULE · ADVISORY · text ("should not pass")

> a driver SHOULD NOT pass WHEN there is a solid line at the left of the driver's lane BECAUSE it is not [?safe] to pass

sources m21, m22 · flags J “safe”

### 3.1.6a ↔ p11:3.1.6a (wording similarity 0.98)

**Differences:** missing clause ONLY IF; vague extra: clear

Claude:

`3.1.6a` RULE · LEGAL · text ("may")

> a driver MAY pass WHEN there is a broken line at the left of the driver's lane ONLY IF the way is clear AND there are [?enough] broken lines ahead to complete the pass [?safely]

sources m23, m24 · flags J “enough”, J “safely”

Model:

`p11:3.1.6a` RULE · LEGAL · text ("may pass")

> a driver MAY pass WHEN there is a broken line at the left of the driver's lane AND the way is [?clear] AND there are [?enough] broken lines ahead to complete the pass [?safely]

sources m23, m24 · flags J “clear”, J “enough”, J “safely”

### 3.1.7a ↔ p10:3.1.7a (wording similarity 0.85)

**No structural differences.**

Claude:

`3.1.7a` RULE · LEGAL · context (Regulatory signs: "These signs give a direction that must be obeyed")

> a driver MUST NOT pass WHEN a "do not pass" sign applies to the road

sources m25, m26

Model:

`p10:3.1.7a` RULE · LEGAL · context (Regulatory signs: these signs give a direction that must be obeyed)

> a driver MUST NOT pass on a road WHEN a "do not pass" sign is posted for the road

sources m25, m26

### 3.2.1a ↔ p05:3.2.1a (wording similarity 0.83)

**Differences:** type DEFINE → FACT; vague extra: some

Claude:

`3.2.1a` DEFINE · None · None

> DEFINE a passing lane or climbing lane IS an added lane THAT lets slower vehicles move into the right-hand lane so faster vehicles can pass [?safely] in the left lane

sources m27, m28 · flags J “safely”

Model:

`p05:3.2.1a` FACT · None · None

> FACT [?some] roads have special passing or climbing lanes that let slower vehicles move into the right-hand lane so that faster vehicles can pass [?safely] in the left lane

sources m27, m28 · flags S “some”, J “safely”

### 3.2.1b ↔ p05:3.2.1b (wording similarity 0.43)

**No structural differences.**

Claude:

`3.2.1b` FACT · None · None

> FACT an advance sign tells drivers a passing opportunity is coming, AND another sign warns when the added lane is ending

sources m29

Model:

`p05:3.2.1b` FACT · None · None

> FACT an advance sign tells a driver that the driver will soon have a chance to pass a vehicle

sources m29

### 3.2.1c ↔ p05:3.2.1c (wording similarity 0.53)

**Differences:** type RULE → FACT; force ADVISORY → None; modal SHOULD → -; basis implied → None; missing clause WHEN; extra clause BECAUSE

Claude:

`3.2.1c` RULE · ADVISORY · implied ("so drivers … can begin to merge safely")

> a driver in the right-hand lane SHOULD merge [?safely] with traffic in the left-hand lane WHEN a sign warns that the lane is ending

sources m29 · flags D “merge”, J “safely”

Model:

`p05:3.2.1c` FACT · None · None

> FACT a sign warns a driver that the passing or climbing lane is ending BECAUSE the sign lets drivers in the right-hand lane begin to merge [?safely] with traffic in the left-hand lane

sources m29 · flags J “safely”

### 3.2.1d ↔ p10:2.1b (wording similarity 0.98)

**No structural differences.**

Claude:

`3.2.1d` RULE · LEGAL · context (Regulatory signs: "must be obeyed")

> a driver MUST keep to the right-hand lane WHEN a "keep right except to pass" sign is posted UNLESS the driver is passing on a two-lane section where a climbing or passing lane is provided

sources m30, m31

Model:

`p10:2.1b` RULE · LEGAL · context (Regulatory signs: these signs give a direction that must be obeyed)

> a driver MUST keep to the right-hand lane WHEN a "keep right except to pass" sign is posted UNLESS the driver is passing on a two-lane section where a climbing lane or a passing lane is provided

sources m30, m31

### 3.2.2a ↔ p07:3.2.2a (wording similarity 0.77)

**Differences:** extra clause WHEN, BECAUSE

Claude:

`3.2.2a` RULE · ADVISORY · text ("should")

> a driver on a freeway SHOULD keep to the right AND use the left lanes for passing

sources m32

Model:

`p07:3.2.2a` RULE · ADVISORY · text ("should")

> a driver SHOULD keep to the right WHEN on a freeway BECAUSE the left lanes are for passing

sources m32 · flags X “keep to the right, using the left lanes for passing”

### 3.2.2b ↔ p07:3.2.2b (wording similarity 0.57)

**Differences:** modal SHOULD → SHOULD SHOULD NOT; missing clause ONLY IF; extra clause WHEN

Claude:

`3.2.2b` RULE · ADVISORY · imperative ("Use … but don't stay there")

> a driver SHOULD use the far-left lane of a multi-lane freeway ONLY IF the driver is passing traffic that moves slower than the speed limit

sources m33

Model:

`p07:3.2.2b` RULE · ADVISORY · imperative ("Use", "don't stay")

> a driver SHOULD use the far-left lane to pass traffic moving slower than the speed limit AND SHOULD NOT stay in the far-left lane WHEN on a multi-lane freeway

sources m33

### 3.2.2c ↔ p07:3.2.2d (wording similarity 0.86)

**No structural differences.**

Claude:

`3.2.2c` RULE · ADVISORY · imperative ("Drive in the right-hand lane", "Get into the habit")

> a driver on a freeway SHOULD drive in the right-hand lane WHEN [?possible] BECAUSE this leaves the other lanes clear for passing

sources m33, m34 · flags J “possible”

Model:

`p07:3.2.2d` RULE · ADVISORY · imperative ("Drive", "Get into the habit")

> a driver SHOULD drive in the right-hand lane WHEN on a freeway AND it is [?possible] BECAUSE this leaves the other lanes clear for passing

sources m33, m34 · flags J “possible”, X “Drive in the right-hand lane when possible / driving in the right lane, leaving the other lanes clear for passing”

### 3.2.3a ↔ p05:3.2.3c (wording similarity 0.58)

**Differences:** type RULE → FACT; force ADVISORY → None; modal SHOULD → -; basis default → None; missing clause BECAUSE

Claude:

`3.2.3a` RULE · ADVISORY · default (stated as a description: "Most passing is done on the left")

> a driver SHOULD pass on the left BECAUSE passing on the right can be more dangerous

sources m35, m36 · flags D “pass on the left”, S “Most passing”

Model:

`p05:3.2.3c` FACT · None · None

> FACT passing on the right can be more dangerous than passing on the left

sources m36

### 3.2.3b ↔ p05:3.2.3b (wording similarity 0.77)

**No structural differences.**

Claude:

`3.2.3b` RULE · LEGAL · text ("may")

> EXCEPTION TO 3.2.3a: a driver MAY pass on the right WHEN the road is multi-lane OR the road is one-way OR the vehicle being passed is a streetcar OR the vehicle being passed is turning left

sources m35

Model:

`p05:3.2.3b` RULE · LEGAL · text ("may")

> a driver MAY pass on the right WHEN the road is multi-lane OR the road is one-way OR the driver is passing a streetcar OR the driver is passing a left-turning vehicle

sources m35

### 3.2.3c ↔ p05:3.2.3d (wording similarity 0.86)

**No structural differences.**

Claude:

`3.2.3c` RULE · ADVISORY · imperative ("wait")

> a driver SHOULD wait WHEN the driver is in the leftmost lane with a slower vehicle in front UNTIL the slower vehicle moves to the right

sources m37

Model:

`p05:3.2.3d` RULE · ADVISORY · imperative ("wait")

> a driver SHOULD wait WHEN the driver is driving in the far-left lane AND a slower vehicle is in front of the driver UNTIL the slower vehicle moves to the right

sources m37

### 3.2.3d ↔ p05:3.2.3e (wording similarity 0.37)

**Differences:** vague extra: suddenly

Claude:

`3.2.3d` RULE · ADVISORY · imperative ("Do not")

> a driver SHOULD NOT change lanes suddenly to pass on the right WHEN the driver is in the leftmost lane behind a slower vehicle BECAUSE the driver in front may move to the right at the same time

sources m37

Model:

`p05:3.2.3e` RULE · ADVISORY · imperative ("Do not")

> a driver SHOULD NOT [?suddenly] change lanes and pass on the right WHEN the driver is driving in the far-left lane AND a slower vehicle is in front of the driver BECAUSE the slower vehicle may realize the driver wants to pass and move to the right at the same time

sources m37 · flags J “suddenly”

### 3.2.4a ↔ p05:3.2.4a (wording similarity 0.97)

**No structural differences.**

Claude:

`3.2.4a` RULE · LEGAL · text ("may … only")

> a driver MAY drive on the right shoulder ONLY IF the driver is passing a vehicle that is turning left AND the shoulder is paved

sources m38 · flags D “right shoulder”

Model:

`p05:3.2.4a` RULE · LEGAL · text ("may drive")

> a driver MAY drive on the right shoulder ONLY IF the driver is passing a vehicle turning left AND the shoulder is paved

sources m38 · flags D “only to pass”

### 3.2.4b ↔ p05:3.2.4b (wording similarity 0.83)

**No structural differences.**

Claude:

`3.2.4b` RULE · LEGAL · text ("may not")

> a driver MUST NOT pass on the left shoulder, whether or not it is paved

sources m38

Model:

`p05:3.2.4b` RULE · LEGAL · text ("may not")

> a driver MUST NOT pass on the left shoulder, paved or not

sources m38

### 3.3.1a ↔ p05:3.3.1a (wording similarity 0.75)

**Differences:** basis imperative → caution; missing clause WHEN; extra clause WHILE

Claude:

`3.3.1a` RULE · ADVISORY · imperative ("Be very careful")

> a driver SHOULD pass with [?extra care] WHEN it is night

sources m39 · flags J “extra care”

Model:

`p05:3.3.1a` RULE · ADVISORY · caution ("Be very careful")

> a driver SHOULD drive with [?extra care] WHILE passing a vehicle at night

sources m39 · flags J “extra care”

### 3.3.1b ↔ p05:3.3.1b (wording similarity 0.98)

**Differences:** vague extra: clear

Claude:

`3.3.1b` PROCEDURE · ADVISORY · imperative steps

> TO pass a vehicle at night SPECIALIZES 2.2a WHEN the driver has to pass AND the way is clear
> 1. switch to low beams WHILE approaching the vehicle from behind
> 2. signal, check the mirrors and blind spot, AND pull out to pass
> 3. switch on high beams WHILE alongside the vehicle being passed BECAUSE this shows more of the road ahead
> 4. move back into the original lane AND signal WHEN the entire front of the vehicle being passed is visible in the inside mirror

sources m40, m41, m42, m43 · flags V “rear view mirror”

Model:

`p05:3.3.1b` PROCEDURE · ADVISORY · imperative steps

> TO pass a vehicle at night SPECIALIZES p05:2.2a WHEN the driver has to pass AND the way is [?clear]
> 1. switch the headlights to low beams WHEN the driver is approaching a vehicle from behind
> 2. signal AND check the mirrors and blind spot AND pull out to pass
> 3. switch on the high beams WHILE the driver moves alongside the vehicle being passed BECAUSE this lets the driver see more of the road ahead
> 4. signal AND pull back into the right-hand lane WHEN the driver can see all of the front of the vehicle being passed in the inside mirror

sources m40, m41, m42, m43 · flags J “clear”, V “rear view mirror”

### 3.3.1c ↔ p01:3.3a (wording similarity 0.84)

**No structural differences.**

Claude:

`3.3.1c` RULE · ADVISORY · imperative ("Use")

> a driver SHOULD use low beams WHEN the driver is less than 60 m behind another vehicle UNLESS the driver is passing it

sources m44

Model:

`p01:3.3a` RULE · ADVISORY · imperative ("Use")

> a driver SHOULD use low beams WHEN at night or in poor conditions AND the driver is less than 60 m behind another vehicle UNLESS the driver is passing the vehicle

sources m44 · flags M “less than 60 metres”

### 3.3.2a ↔ p09:3.3.2a (wording similarity 0.90)

**No structural differences.**

Claude:

`3.3.2a` RULE · ADVISORY · text ("Avoid") and imperative ("Don't")

> a driver SHOULD NOT pass WHEN driving in fog

sources m45, m47

Model:

`p09:3.3.2a` RULE · ADVISORY · text ("Avoid passing")

> a driver SHOULD NOT pass a vehicle WHEN driving in fog

sources m45, m47 · flags X “Avoid passing / Don't pass other vehicles”

### 3.3.2b ↔ p09:3.3.2b (wording similarity 0.82)

**No structural differences.**

Claude:

`3.3.2b` RULE · ADVISORY · imperative ("Don't")

> a driver SHOULD NOT speed up to pass a slow-moving vehicle WHEN driving in fog

sources m46

Model:

`p09:3.3.2b` RULE · ADVISORY · imperative ("Don't")

> a driver SHOULD NOT speed up to pass a vehicle that is moving slowly WHEN driving in fog

sources m46

### 3.3.3a ↔ p09:3.3.3a (wording similarity 0.80)

**No structural differences.**

Claude:

`3.3.3a` RULE · ADVISORY · text ("Avoid")

> a driver SHOULD NOT pass WHEN driving in blowing snow or a whiteout

sources m48

Model:

`p09:3.3.3a` RULE · ADVISORY · text ("Avoid passing")

> a driver SHOULD NOT pass a vehicle WHEN driving in a whiteout

sources m48

### 3.3.3b ↔ p09:3.3.3b (wording similarity 0.76)

**No structural differences.**

Claude:

`3.3.3b` RULE · ADVISORY · imperative ("Don't")

> a driver SHOULD NOT attempt to pass a slow-moving vehicle WHEN driving in blowing snow or a whiteout

sources m49

Model:

`p09:3.3.3b` RULE · ADVISORY · imperative ("Don't")

> a driver SHOULD NOT attempt to pass a vehicle that is moving slowly WHEN driving in a whiteout

sources m49

### 3.4.1a ↔ p05:3.4.1a (wording similarity 0.86)

**No structural differences.**

Claude:

`3.4.1a` RULE · ADVISORY · caution ("watch carefully for")

> a driver SHOULD WATCH FOR doors opening suddenly AND doors opened to load or unload WHILE passing parked vehicles

sources m50

Model:

`p05:3.4.1a` RULE · ADVISORY · caution ("watch")

> a driver SHOULD WATCH FOR people suddenly opening doors OR doors opened to load and unload WHILE passing parked vehicles

sources m50 · flags J “carefully”

### 3.4.2a ↔ p05:3.4.2a (wording similarity 0.91)

**No structural differences.**

Claude:

`3.4.2a` FACT · None · None

> FACT motorcycles, bicycles, limited-speed motorcycles and mopeds [?often] move to the left or right side of their lane to avoid dangerous road conditions OR to be seen

sources m51 · flags S “often”

Model:

`p05:3.4.2a` FACT · None · None

> FACT motorcycles, bicycles, limited-speed motorcycles and mopeds [?often] need to pull to the left or right side of their lane to avoid dangerous road conditions or to be seen by other drivers

sources m51 · flags S “often”

### 3.4.2b ↔ p05:3.4.2b (wording similarity 0.57)

**Differences:** missing clause BECAUSE; extra clause WHEN

Claude:

`3.4.2b` RULE · ADVISORY · imperative ("Do not take this as an invitation")

> a driver SHOULD NOT pass a motorcycle, bicycle, limited-speed motorcycle or moped within its lane BECAUSE its position in the lane is not an invitation to pass (3.4.2a)

sources m51, m52

Model:

`p05:3.4.2b` RULE · ADVISORY · imperative ("Do not take")

> a driver SHOULD NOT pass a motorcycle, a bicycle, a limited-speed motorcycle or a moped in the same lane WHEN the vehicle pulls to the left or right side of its lane

sources m51

### 3.4.2c ↔ p05:3.4.2c (wording similarity 0.76)

**No structural differences.**

Claude:

`3.4.2c` RULE · ADVISORY · imperative ("do so by changing lanes")

> a driver SHOULD change lanes WHEN passing a motorcycle, bicycle, limited-speed motorcycle or moped

sources m51

Model:

`p05:3.4.2c` RULE · ADVISORY · imperative ("do so")

> a driver SHOULD change lanes to pass a motorcycle, a bicycle, a limited-speed motorcycle or a moped WHEN the driver wants to pass the vehicle

sources m51

### 3.4.3a ↔ p06:3.4.3a (wording similarity 0.84)

**Differences:** vague not marked: smaller vehicle

Claude:

`3.4.3a` RULE · ADVISORY · imperative ("Wait … before you pass")

> a driver SHOULD NOT pass a [?smaller vehicle] that is turning left ahead UNTIL it has moved to the right

sources m53 · flags R “smaller vehicle”

Model:

`p06:3.4.3a` RULE · ADVISORY · imperative ("Wait")

> a driver SHOULD NOT pass a smaller vehicle that is turning left UNTIL the smaller vehicle has moved right

sources m53

### 3.4.4a ↔ p03:3.4.4a (wording similarity 0.61)

**Differences:** vague not marked: safely

Claude:

`3.4.4a` RULE · LEGAL · text ("can")

> a cyclist MAY use any part of the lane WHEN this is [?necessary for safety], for example to discourage passing where the lane is too narrow to be shared [?safely]

sources m54, m55 · flags J “necessary for safety”, J “safely”

Model:

`p03:3.4.4a` RULE · LEGAL · text ("can use")

> a cyclist MAY use any part of the lane WHEN it is [?necessary for safety]

sources m54, m55 · flags J “necessary for safety”

### 3.4.4b ↔ p03:3.4.4b (wording similarity 0.89)

**No structural differences.**

Claude:

`3.4.4b` RULE · LEGAL · text ("must maintain")

> a driver of a motor vehicle MUST keep at least 1 m between the vehicle and a cyclist WHILE passing the cyclist, [?where practical] IF VIOLATED a fine AND 2 demerit points

sources m56, m57, m59 · flags J “where practical”

Model:

`p03:3.4.4b` RULE · LEGAL · text ("must maintain")

> a driver of a motor vehicle MUST maintain a minimum distance of 1 m between the vehicle and the cyclist WHILE passing the cyclist [?where practical] IF VIOLATED a fine AND 2 demerit points

sources m56, m57, m59 · flags J “where practical”

### 3.4.4c ↔ p03:3.4.4c (wording similarity 0.93)

**Differences:** vague not marked: possible; vague extra: whenever possible

Claude:

`3.4.4c` RULE · ADVISORY · text ("should")

> a driver SHOULD change lanes to pass a cyclist WHEN [?possible]

sources m58 · flags J “possible”

Model:

`p03:3.4.4c` RULE · ADVISORY · text ("should")

> a driver SHOULD change lanes to pass a cyclist WHEN [?whenever possible]

sources m58 · flags J “whenever possible”

### 3.4.4d ↔ p03:3.4.4d (wording similarity 0.90)

**No structural differences.**

Claude:

`3.4.4d` RULE · ADVISORY · imperative ("Do not")

> a driver SHOULD NOT sound the horn [?unnecessarily] WHILE passing a cyclist BECAUSE it may frighten the cyclist and cause a loss of control

sources m60 · flags J “unnecessarily”

Model:

`p03:3.4.4d` RULE · ADVISORY · imperative ("Do not sound")

> a driver SHOULD NOT sound the horn [?unnecessarily] WHILE overtaking a cyclist BECAUSE it may frighten the cyclist and cause the cyclist to lose control

sources m60 · flags J “unnecessarily”

### 3.4.4e ↔ p03:3.4.4e (wording similarity 0.63)

**Differences:** extra clause WHILE

Claude:

`3.4.4e` RULE · ADVISORY · imperative ("tap it")

> a driver SHOULD tap the horn quickly and lightly while still [?some distance] away from the cyclist WHEN the driver feels the horn must be used

sources m60 · flags J “some distance”

Model:

`p03:3.4.4e` RULE · ADVISORY · imperative ("tap")

> a driver SHOULD tap the horn quickly and lightly WHEN the driver uses the horn WHILE overtaking a cyclist AND the driver is still [?some distance] away from the cyclist

sources m60 · flags J “some distance”

### 3.4.5a ↔ p05:3.4.5a (wording similarity 0.88)

**No structural differences.**

Claude:

`3.4.5a` RULE · LEGAL · text ("must")

> a driver MUST pass a streetcar on the right UNLESS the driver is on a one-way road

sources m62

Model:

`p05:3.4.5a` RULE · LEGAL · text ("must")

> a driver MUST pass a streetcar on the right UNLESS the road is one-way

sources m62

### 3.4.5b ↔ p05:3.4.5b (wording similarity 0.44)

**Differences:** extra clause UNLESS

Claude:

`3.4.5b` RULE · ADVISORY · imperative ("stay")

> a driver SHOULD stay at least 2 m behind the rear doors of a streetcar WHEN the streetcar is stopped AND passengers are getting on or off

sources m61, m63 · flags M “stay at least two metres”

Model:

`p05:3.4.5b` RULE · ADVISORY · imperative ("stay")

> a driver SHOULD stay at least 2 m behind the rear doors of a stopped streetcar WHEN the driver is at a streetcar stop AND passengers are getting off or on UNLESS the streetcar stop has an area set aside for streetcar passengers

sources m61, m63 · flags M “stay at least two metres”

### 3.4.5d ↔ p05:3.4.5c (wording similarity 0.79)

**Differences:** modal SHOULD SHOULD → SHOULD; extra clause WHEN; vague not marked: reasonable speed; vague extra: reasonable, these areas

Claude:

`3.4.5d` RULE · ADVISORY · imperative ("Always pass", "be prepared")

> a driver SHOULD pass a streetcar passenger area at a [?reasonable speed] AND SHOULD WATCH FOR pedestrians making sudden or unexpected moves

sources m64 · flags J “reasonable speed”, R “these areas”, X “safety islands and zones”

Model:

`p05:3.4.5c` RULE · ADVISORY · imperative ("Always")

> a driver SHOULD pass [?these areas] at [?reasonable] speed AND WATCH FOR pedestrians making sudden or unexpected moves WHEN passing a streetcar stop

sources m64 · flags R “these areas”, J “reasonable”

### 3.4.6a ↔ p03:3.4.6a (wording similarity 0.78)

**Differences:** missing clause WHEN; extra clause WHILE

Claude:

`3.4.6a` RULE · ADVISORY · imperative ("do not cut in")

> a driver SHOULD NOT cut in [?closely] in front of a large vehicle WHEN returning to the lane after passing it BECAUSE this reduces the space cushion the large vehicle needs to stop [?safely]

sources m65 · flags J “closely”, J “safely”

Model:

`p03:3.4.6a` RULE · ADVISORY · imperative ("do not cut")

> a driver SHOULD NOT cut in front [?closely] of a large vehicle WHILE passing the vehicle BECAUSE it reduces the space cushion large vehicles require to stop [?safely]

sources m65 · flags J “closely”, J “safely”

### 3.4.6b ↔ p03:3.4.6b (wording similarity 1.00)

**No structural differences.**

Claude:

`3.4.6b` RULE · ADVISORY · imperative ("Allow")

> a driver SHOULD allow [?more room] WHEN passing a large vehicle

sources m65 · flags J “more room”

Model:

`p03:3.4.6b` RULE · ADVISORY · imperative ("Allow")

> a driver SHOULD allow [?more room] WHEN passing a large vehicle

sources m65 · flags J “more room”

### 3.4.6c ↔ p03:3.4.6c (wording similarity 0.84)

**No structural differences.**

Claude:

`3.4.6c` FACT · None · None

> FACT a large vehicle can create heavy air turbulence that may affect the driver's control WHILE passing it

sources m66

Model:

`p03:3.4.6c` FACT · None · None

> FACT a large vehicle can create heavy air turbulence that may affect the driver's ability to control the vehicle WHILE passing the large vehicle

sources m66

### 3.4.6d ↔ p10:3.4.6a (wording similarity 0.79)

**No structural differences.**

Claude:

`3.4.6d` DEFINE · None · None

> DEFINE a long commercial vehicle IS a double-trailer vehicle THAT can be up to 40 m long AND carries an LCV placard on its rear ALSO CALLED LCV

sources m67, m68

Model:

`p10:3.4.6a` DEFINE · None · None

> DEFINE a long commercial vehicle IS a double trailer THAT can be up to 40 m in length ALSO CALLED an LCV

sources m67, m68

### 3.4.6e ↔ p10:3.4.6b (wording similarity 0.47)

**No structural differences.**

Claude:

`3.4.6e` RULE · ADVISORY · text ("It is important to")

> a driver SHOULD anticipate the extended length AND limited speed of an LCV WHEN preparing to pass it

sources m68

Model:

`p10:3.4.6b` RULE · ADVISORY · text ("It is important to")

> a driver SHOULD recognize a long commercial vehicle (LCV) based on rear signage AND anticipate the LCV's extended length AND the LCV's limited speed WHEN the driver is about to pass the LCV on a highway

sources m67, m68

### 3.4.7a ↔ p03:3.4.7b (wording similarity 0.64)

**Differences:** modal SHOULD SHOULD NOT → SHOULD NOT; vague not marked: well back

Claude:

`3.4.7a` RULE · ADVISORY · imperative ("Stay … do not pass until")

> a driver SHOULD stay [?well back] of farm machinery AND SHOULD NOT pass it UNTIL it is [?safe] to do so

sources m69 · flags J “well back”, J “safe”

Model:

`p03:3.4.7b` RULE · ADVISORY · imperative ("do not pass")

> a driver SHOULD NOT pass farm machinery UNTIL it is [?safe] to do so

sources m69 · flags J “safe”

### 3.4.8a ↔ p03:3.4.8b (wording similarity 0.69)

**Differences:** modal SHOULD SHOULD NOT → SHOULD; missing clause UNLESS; extra clause ONLY IF

Claude:

`3.4.8a` RULE · ADVISORY · imperative ("Maintain", "only pass when")

> a driver SHOULD keep a [?safe] following distance behind a horse-drawn vehicle AND SHOULD NOT pass it UNLESS it is [?safe] to do so

sources m70 · flags J “safe”

Model:

`p03:3.4.8b` RULE · ADVISORY · imperative ("pass")

> a driver SHOULD pass a horse-drawn vehicle ONLY IF it is [?safe] to do so

sources m70 · flags J “safe”

### 3.4.8b ↔ p03:3.4.8c (wording similarity 0.61)

**Differences:** vague extra: too closely

Claude:

`3.4.8b` RULE · ADVISORY · imperative ("give")

> a driver SHOULD leave [?as much distance as possible] WHILE passing a horse-drawn vehicle BECAUSE passing too closely could startle the horse and make it change direction suddenly

sources m71 · flags J “as much distance as possible”

Model:

`p03:3.4.8c` RULE · ADVISORY · imperative ("give")

> a driver SHOULD give [?as much distance as possible] between the vehicle and the horse-drawn vehicle WHILE passing it BECAUSE passing [?too closely] could scare or startle the horse, causing it to change direction suddenly on the roadway

sources m71 · flags J “as much distance as possible”, J “too closely”

### 3.4.9a ↔ p05:3.4.9a (wording similarity 0.64)

**Differences:** missing clause WHEN

Claude:

`3.4.9a` RULE · ADVISORY · imperative ("Don't")

> a driver SHOULD NOT pass a snow plow WHEN the snow plow is moving

sources m72 · flags M “under any conditions”

Model:

`p05:3.4.9a` RULE · ADVISORY · imperative ("Don't")

> a driver SHOULD NOT pass a moving snow plow under any conditions

sources m72 · flags M “under any conditions”

### 3.4.9b ↔ p09:3.4.9b (wording similarity 0.75)

**No structural differences.**

Claude:

`3.4.9b` RULE · ADVISORY · imperative ("Do not try")

> a driver SHOULD NOT pass between snow plows WHEN several snow plows are staggered across a freeway BECAUSE there is not [?enough] room to pass [?safely] AND the ridge of wet snow can throw the vehicle out of control

sources m73 · flags J “enough”, J “safely”

Model:

`p09:3.4.9b` RULE · ADVISORY · imperative ("Do not try")

> a driver SHOULD NOT try to pass between snow plows WHEN the driver is on a freeway AND several snow plows are staggered across the road BECAUSE there is not [?enough] room to pass [?safely] AND the ridge of wet snow can throw the vehicle out of control

sources m73 · flags J “enough”, J “safely”

### 3.4.10a ↔ p10:3.4.10a (wording similarity 0.66)

**No structural differences.**

Claude:

`3.4.10a` RULE · ADVISORY · imperative ("Do not pass")

> a driver SHOULD NOT pass a pilot vehicle or pace vehicle WHEN it carries the "do not pass" temporary condition sign

sources m74, m75 · flags M “Do not pass the pilot vehicle”

Model:

`p10:3.4.10a` RULE · ADVISORY · imperative ("Do not pass")

> a driver SHOULD NOT pass a pilot vehicle or a pace vehicle WHEN a "do not pass" sign is posted on the pilot vehicle or the pace vehicle

sources m74, m75

### 3.4.11a ↔ p03:3.1.1a (wording similarity 0.95)

**No structural differences.**

Claude:

`3.4.11a` RULE · ADVISORY · imperative ("Do not pass")

> a driver SHOULD NOT pass a vehicle WHEN the vehicle is stopped at a crosswalk BECAUSE a stopped vehicle may mean a pedestrian is crossing

sources m76

Model:

`p03:3.1.1a` RULE · ADVISORY · imperative ("Do not pass")

> a driver SHOULD NOT pass a vehicle WHEN the vehicle is stopped at a crosswalk BECAUSE a stopped vehicle may be a clue that a pedestrian is crossing

sources m76

### 3.4.12a ↔ p04:3.4.12f (wording similarity 0.94)

**Differences:** vague not marked: illegally passed

Claude:

`3.4.12a` FACT · None · None

> FACT school bus drivers and other witnesses can report vehicles that have [?illegally passed] a school bus

sources m77 · flags G “illegally passed”

Model:

`p04:3.4.12f` FACT · None · None

> FACT in Ontario, school bus drivers and other witnesses can report vehicles that have illegally passed a school bus

sources m77

### 3.4.12b ↔ p04:3.4.12a (wording similarity 0.62)

**Differences:** vague not marked: heavy

Claude:

`3.4.12b` RULE · LEGAL · text ("You must stop")

> a driver MUST stop WHEN approaching a stopped school bus with its upper alternating red lights flashing, from either direction IF VIOLATED a [?heavy] fine AND 6 demerit points for a first offence

sources c1, c5 · flags J “heavy”, X “stop arm activated”

Model:

`p04:3.4.12a` RULE · LEGAL · text ("must stop")

> a driver MUST stop WHEN the driver approaches a stopped school bus with its upper alternating red lights flashing AND the driver is behind the school bus OR the driver is approaching the school bus from the front IF VIOLATED a fine AND 6 demerit points for a first offence

sources c1, c5 · flags J “heavily”

### 3.4.12c ↔ p04:3.4.12b (wording similarity 0.74)

**Differences:** force ADVISORY → LEGAL; modal SHOULD → MUST; basis imperative → context

Claude:

`3.4.12c` RULE · ADVISORY · imperative ("stop at least 20 metres away")

> a driver SHOULD stop at least 20 m from the bus WHEN approaching a stopped school bus with its upper alternating red lights flashing from behind

sources c2 · flags M “stop at least 20 metres away”

Model:

`p04:3.4.12b` RULE · LEGAL · context (c1: "must stop")

> a driver MUST stop at least 20 m from the school bus WHEN the school bus is stopped with its upper alternating red lights flashing AND the driver is coming from behind the school bus

sources c1, c2

### 3.4.12d ↔ p04:3.4.12c (wording similarity 0.85)

**Differences:** force ADVISORY → LEGAL; modal SHOULD NOT → MUST NOT; basis imperative → context

Claude:

`3.4.12d` RULE · ADVISORY · imperative ("Do not go until")

> a driver SHOULD NOT go WHEN stopped for a school bus with its upper alternating red lights flashing UNTIL the bus moves OR the lights have stopped flashing

sources c3 · flags M “Do not go”, X “and its stop arm is no longer activated”

Model:

`p04:3.4.12c` RULE · LEGAL · context (c1: "must stop")

> a driver MUST NOT proceed WHEN the driver approaches a stopped school bus with its upper alternating red lights flashing UNTIL the school bus moves OR the lights have stopped flashing

sources c1, c3

### 3.4.12e ↔ p04:3.4.12e (wording similarity 0.86)

**No structural differences.**

Claude:

`3.4.12e` EXCEPTION · None · None

> EXCEPTION TO 3.4.12b WHEN the road has a median strip AND the driver is approaching the bus from the front

sources c4

Model:

`p04:3.4.12e` EXCEPTION · None · None

> EXCEPTION TO p04:3.4.12c WHEN the driver is on a road with a median strip AND the driver is approaching the school bus from the front

sources c4

### 3.4.13a ↔ p12:3.4.13a (wording similarity 0.45)

**Differences:** basis text → context; missing clause WHEN; vague not marked: caution; vague extra: carefully

Claude:

`3.4.13a` RULE · LEGAL · text ("you are required")

> a driver MUST slow down AND proceed with [?caution] WHEN approaching, in the same direction, an emergency vehicle stopped with red or red-and-blue lights flashing OR a tow truck stopped with amber lights flashing IF VIOLATED 3 demerit points

sources m78, m80 · flags J “caution”

Model:

`p12:3.4.13a` RULE · LEGAL · context (listed under "Table of offences")

> a driver MUST slow AND [?carefully] pass a stopped emergency vehicle IF VIOLATED 3 demerit points

sources m80 · flags J “carefully”

### 3.4.13b ↔ p12:3.4.13b (wording similarity 0.64)

**Differences:** basis text → context; vague not marked: if safe to do so; vague extra: possible

Claude:

`3.4.13b` RULE · LEGAL · text ("you are required")

> a driver MUST move into a lane away from the stopped emergency vehicle or tow truck, [?if safe to do so] WHEN the road has 2 or more lanes in the driver's direction IF VIOLATED 3 demerit points

sources m79, m81 · flags J “if safe to do so”, X “where possible”

Model:

`p12:3.4.13b` RULE · LEGAL · context (listed under "Table of offences")

> a driver MUST move into another lane WHEN the driver is passing a stopped emergency vehicle AND it is [?possible] to move into another lane IF VIOLATED 3 demerit points

sources m81 · flags J “possible”

### 3.5.1a ↔ p14:3.5.1a (wording similarity 0.66)

**Differences:** missing clause BECAUSE

Claude:

`3.5.1a` FACT · None · None

> FACT a vehicle towing a trailer cannot accelerate as quickly AND needs more space BECAUSE it is much longer

sources m82

Model:

`p14:3.5.1a` FACT · None · None

> FACT a driver towing a trailer cannot accelerate as quickly

sources m82

### 3.5.1b ↔ p14:3.5.1c (wording similarity 0.75)

**Differences:** missing clause ONLY IF; extra clause WHEN; vague not marked: enough; vague extra: enough time and room

Claude:

`3.5.1b` RULE · ADVISORY · imperative ("make sure")

> a driver towing a trailer SHOULD pass ONLY IF the driver has [?enough] time and room to complete the pass

sources m82 · flags J “enough”

Model:

`p14:3.5.1c` RULE · ADVISORY · imperative ("make sure")

> a driver towing a trailer SHOULD make sure the driver has [?enough time and room] to complete the pass WHEN the driver is about to pass a vehicle

sources m82 · flags J “enough time and room”

### 3.5.1c ↔ p14:3.5.1b (wording similarity 0.38)

**Differences:** type RULE → FACT; force ADVISORY → None; modal SHOULD SHOULD NOT → -; basis imperative → None; missing clause WHEN; vague not marked: more room, too soon; vague extra: more space

Claude:

`3.5.1c` RULE · ADVISORY · imperative ("allow", "Do not cut back")

> a driver towing a trailer SHOULD allow [?more room] before moving back into the lane AND SHOULD NOT cut back in [?too soon] WHEN returning to the lane after passing BECAUSE this can make the trailer sway and become hard to control

sources m82 · flags J “more room”, J “too soon”

Model:

`p14:3.5.1b` FACT · None · None

> FACT a driver towing a trailer needs [?more space] BECAUSE the length of the vehicle is much longer with a trailer attached

sources m82 · flags J “more space”

### 3.5.2a ↔ p14:3.5.2a (wording similarity 0.69)

**Differences:** type RULE → PROCEDURE; modal SHOULD → -

Claude:

`3.5.2a` RULE · ADVISORY · imperative ("signal, pull over and let")

> a driver towing a trailer SHOULD signal, pull over AND let the other vehicles pass WHEN the driver is holding up a line of traffic

sources m83 · flags R “If you are holding up a line of traffic”

Model:

`p14:3.5.2a` PROCEDURE · ADVISORY · imperative steps

> TO let the other vehicles pass WHEN the driver towing a trailer is holding up a line of traffic
> 1. signal
> 2. pull over
> 3. let the other vehicles pass

sources m83

### 3.5.2b ↔ p14:3.5.2b (wording similarity 0.75)

**Differences:** missing clause WHEN

Claude:

`3.5.2b` FACT · None · None

> FACT fast-moving trucks and buses create a strong air disturbance behind them that can whip a trailer to the side WHEN they pass

sources m83

Model:

`p14:3.5.2b` FACT · None · None

> FACT fast-moving trucks and buses create a strong air disturbance behind them

sources m83

### 3.5.2c ↔ p14:3.5.2e (wording similarity 0.44)

**Differences:** type RULE → FACT; force ADVISORY → None; modal SHOULD NOT SHOULD → -; basis imperative → None; vague not marked: carefully; vague extra: slight

Claude:

`3.5.2c` RULE · ADVISORY · imperative ("do not brake", "steer")

> a driver towing a trailer SHOULD NOT brake AND SHOULD steer the vehicle and trailer [?carefully] back into position WHEN a passing bus or truck pushes the trailer out of position

sources m83 · flags J “carefully”

Model:

`p14:3.5.2e` FACT · None · None

> FACT a [?slight] increase in speed may help WHEN a large bus or truck passes the driver towing a trailer AND the wall of wind behind the large bus or truck whips the trailer to the side

sources m83 · flags J “slight”

### 3.6.1a ↔ p05:3.6.1a (wording similarity 0.84)

**No structural differences.**

Claude:

`3.6.1a` RULE · ADVISORY · imperative ("move to the right")

> a driver being passed SHOULD move to the right AND let the faster vehicle pass [?in safety] WHEN faster traffic wants to pass

sources m84, m87, m88 · flags M “move to the right”, J “in safety”

Model:

`p05:3.6.1a` RULE · ADVISORY · imperative ("move")

> a driver SHOULD move to the right AND let faster traffic pass [?in safety] WHEN faster traffic wants to pass the driver

sources m84 · flags J “in safety”

### 3.6.1b ↔ p05:3.6.1b (wording similarity 0.87)

**Differences:** missing clause WHILE; extra clause WHEN

Claude:

`3.6.1b` RULE · LEGAL · text ("It is unlawful")

> a driver being passed MUST NOT speed up WHILE another driver is trying to pass BECAUSE it is dangerous

sources m85

Model:

`p05:3.6.1b` RULE · LEGAL · text ("unlawful")

> a driver MUST NOT speed up WHEN another driver is trying to pass the driver BECAUSE it is dangerous

sources m85

### 3.6.1c ↔ p13:3.6.1a (wording similarity 0.63)

**Differences:** missing clause IF VIOLATED; vague not marked: sanctions for dangerous driving

Claude:

`3.6.1c` RULE · LEGAL · context (listed under "Sanctions – dangerous behaviours")

> a driver MUST NOT drive to prevent another vehicle from passing IF VIOLATED [?sanctions for dangerous driving]

sources m86 · flags R “sanctions for dangerous driving”

Model:

`p13:3.6.1a` RULE · LEGAL · context (listed under "Sanctions – dangerous behaviours")

> a driver being passed MUST NOT drive a motor vehicle to prevent another vehicle from passing

sources m86

### 3.6.1d ↔ p10:2.1a (wording similarity 0.58)

**Differences:** vague not marked: slow traffic

Claude:

`3.6.1d` RULE · LEGAL · text ("must keep right")

> a driver in [?slow traffic] MUST keep right WHEN on a multi-lane road where a "slower traffic keep right" sign is posted

sources c8, c9 · flags J “slow traffic”

Model:

`p10:2.1a` RULE · LEGAL · text ("must keep right")

> a driver MUST keep to the right-hand lane WHEN the driver is in slow traffic on a multi-lane road AND a "keep right" sign is posted for the road

sources c8, c9

### 3.6.2a ↔ p05:3.6.2a (wording similarity 0.25)

**Differences:** modal SHOULD SHOULD → SHOULD

Claude:

`3.6.2a` RULE · ADVISORY · imperative ("pay attention", "move closer")

> a driver being passed SHOULD WATCH FOR oncoming traffic AND SHOULD move closer to the right side of the lane WHEN on an undivided road AND the passing driver has pulled into the opposite lane

sources m89

Model:

`p05:3.6.2a` RULE · ADVISORY · imperative ("pay attention", "move")

> a driver being passed SHOULD pay attention to oncoming traffic AND move closer to the right side of the lane WHEN the driver being passed is being passed on an undivided road AND the passing driver has pulled into the opposite lane

sources m89

### 3.6.2b ↔ p05:3.6.2b (wording similarity 0.44)

**No structural differences.**

Claude:

`3.6.2b` RULE · ADVISORY · caution ("Be prepared to")

> a driver being passed SHOULD be ready to slow down WHEN on an undivided road AND the passing driver is in the opposite lane BECAUSE slowing down lets the passing driver get back in front sooner and prevents a collision

sources m89

Model:

`p05:3.6.2b` RULE · ADVISORY · caution ("Be prepared")

> a driver being passed SHOULD be prepared to slow down WHEN the driver being passed is being passed on an undivided road AND the passing driver has pulled into the opposite lane BECAUSE slowing down lets the passing driver get in front of the driver being passed more quickly to prevent a collision

sources m89

### 3.6.3a ↔ p05:3.6.3a (wording similarity 0.80)

**Differences:** vague extra: many

Claude:

`3.6.3a` RULE · LEGAL · text ("are not allowed", "cannot")

> a truck driver MUST NOT drive in the far-left lane WHEN on a high-speed road with 3 or more lanes in each direction where trucks are barred from that lane

sources m90, m91 · flags S “many high-speed roads”, X “many freeways”

Model:

`p05:3.6.3a` RULE · LEGAL · text ("not allowed")

> a truck driver MUST NOT drive in the far-left lane WHEN the road is one of [?many] high-speed roads with 3 or more lanes in each direction

sources m90 · flags S “many”

### 3.6.3b ↔ p07:3.2.2c (wording similarity 0.59)

**Differences:** modal MUST → MUST NOT MUST

Claude:

`3.6.3b` RULE · LEGAL · text ("must use")

> a truck driver MUST use the lane next to the far-left lane for passing WHEN on a high-speed road with 3 or more lanes in each direction where trucks are barred from the far-left lane

sources m90, m91

Model:

`p07:3.2.2c` RULE · LEGAL · text ("cannot travel", "must use")

> a driver of a large truck MUST NOT travel in the far-left lane AND MUST use the lane to the right for passing WHEN on a freeway with three or more lanes in each direction

sources m91 · flags S “many”

### 3.6.3c ↔ p05:3.6.3c (wording similarity 0.71)

**Differences:** vague not marked: as soon as the driver can

Claude:

`3.6.3c` RULE · ADVISORY · imperative ("move into")

> a driver in the truck passing lane SHOULD move into the right-hand lane [?as soon as the driver can] WHEN a truck wants to pass

sources m90 · flags J “as soon as the driver can”

Model:

`p05:3.6.3c` RULE · ADVISORY · imperative ("move")

> a driver SHOULD move into the right-hand lane as soon as the driver can WHEN the driver is in the truck passing lane AND a truck wants to pass the driver

sources m90 · flags J “as soon as the driver can”

## Reference statements with no model partner (3)

`3.4.3b` RULE · ADVISORY · imperative ("do not pull up beside it")

> a driver SHOULD NOT pull up beside a [?smaller vehicle] that is turning left ahead to make the turn at the same time WHEN the driver is also turning left, behind it

sources c6 · flags R “smaller vehicle”

`3.4.3c` RULE · ADVISORY · imperative ("Stay behind")

> a driver SHOULD stay behind a [?smaller vehicle] that is turning left ahead WHEN the driver is also turning left, behind it UNTIL the way is [?clear]

sources c7 · flags R “smaller vehicle”, J “clear”

`3.4.5c` EXCEPTION · None · None

> EXCEPTION TO 3.4.5b WHEN the streetcar stop has an area set aside for passengers

sources m63

## Model statements with no reference partner (17)

`p03:3.4.4f` RULE · ADVISORY · imperative ("look", "check")

> a driver SHOULD look behind AND check the mirrors and blind spots for a passing cyclist WHEN the driver is parked on the side of the roadway AND the driver is about to open a door

sources m96

`p03:3.4.7a` RULE · ADVISORY · imperative ("Stay")

> a driver SHOULD stay [?well back] from farm machinery

sources m69 · flags J “well back”

`p03:3.4.8a` RULE · ADVISORY · imperative ("Maintain")

> a driver SHOULD maintain a [?safe] following distance from a horse-drawn vehicle

sources m70 · flags J “safe”

`p04:3.1.1a` RULE · LEGAL · text ("must not pass")

> a driver MUST NOT pass a vehicle WHEN the driver is within 30 m of a pedestrian crossover

sources m16

`p04:3.4.12d` EXCEPTION · None · None

> EXCEPTION TO p04:3.4.12a WHEN the driver is on a road with a median strip AND the driver is approaching the school bus from the front

sources c4

`p05:1e` FACT · None · None

> FACT a driver may want to pass [?some] slow-moving vehicles when following them

sources m3 · flags S “some”

`p05:2.3a` RULE · ADVISORY · imperative ("make")

> a driver SHOULD change lanes into the original lane WHEN the driver is passing a vehicle AND the driver can see the entire front of the vehicle being passed in the inside mirror

sources m11 · flags V “rear view mirror”

`p05:3.2.3a` FACT · None · None

> FACT [?most] passing is done on the left

sources m35 · flags S “most”

`p05:3.6.3b` FACT · None · None

> FACT on [?many] high-speed roads with 3 or more lanes in each direction, the lane next to the far-left lane is the truck passing lane

sources m90 · flags S “many”

`p08:3.4.13a` RULE · LEGAL · text ("required to")

> a driver MUST reduce the speed of the vehicle AND proceed with [?caution] WHEN the driver is approaching an emergency vehicle that is stopped with its red or red and blue lights flashing OR a tow truck with its amber lights flashing in the same direction of the driver's travel

sources m78 · flags J “caution”

`p08:3.4.13b` RULE · LEGAL · text ("required to")

> a driver MUST move into a lane away from the emergency vehicle or tow truck WHEN the driver is approaching an emergency vehicle that is stopped with its red or red and blue lights flashing OR a tow truck with its amber lights flashing in the same direction of the driver's travel AND the roadway has two or more lanes of traffic in the same direction of the driver's travel ONLY IF it is [?safe] to do so

sources m78, m79 · flags J “safe”

`p09:3.4.9a` FACT · None · None

> FACT several snow plows may be staggered across the road on freeways, clearing all lanes at the same time by passing a ridge of snow from plow to plow

sources m73

`p10:3.1.7b` FACT · None · None

> FACT the downward lines on a warning sign show the side on which a driver may [?safely] pass

sources m94 · flags J “safely”

`p14:3.5.1d` RULE · ADVISORY · imperative ("allow", "Do not")

> a driver towing a trailer SHOULD allow [?more room] AND SHOULD NOT move back into the original lane [?too soon] WHEN the driver has passed a vehicle AND the driver is about to move back to the original lane BECAUSE a move back into the original lane [?too soon] can cause the trailer to sway and make it difficult to control

sources m82 · flags J “more room”, J “too soon”, J “too soon”

`p14:3.5.2c` FACT · None · None

> FACT the wall of wind behind a large bus or truck may whip the trailer of a driver towing a trailer to the side, pushing it out of control WHEN a large bus or truck passes the driver towing a trailer

sources m83

`p14:3.5.2d` RULE · ADVISORY · imperative ("do not brake", "Carefully steer")

> a driver towing a trailer SHOULD NOT brake AND SHOULD [?carefully] steer the vehicle and the trailer back into position WHEN a large bus or truck passes the driver AND the wall of wind behind the large bus or truck whips the trailer to the side

sources m83 · flags J “carefully”

`p15:3.6.1a` RULE · ADVISORY · imperative ("Move to the right")

> a driver being passed SHOULD move to the right AND allow the other vehicle to pass WHEN the driver of another vehicle is about to pass the driver's vehicle

sources m87, m88 · flags M “you must”
