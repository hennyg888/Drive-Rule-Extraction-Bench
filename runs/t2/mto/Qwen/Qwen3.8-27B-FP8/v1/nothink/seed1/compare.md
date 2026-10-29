# T2 comparison: runs/t2/mto/Qwen/Qwen3.8-27B-FP8/v1/nothink/seed1/statements.json

Reference 88 · model 95 · paired 78

Paired statements with at least one difference: 55 of 78
## Paired statements

### 1b ↔ p05:1a (wording similarity 1.00)

**No structural differences.**

Claude:

`1b` DEFINE · None · None

> DEFINE passing IS a lane change THAT moves past a slower vehicle ALSO CALLED overtaking

sources m2 · flags V “overtaking”

Model:

`p05:1a` DEFINE · None · None

> DEFINE passing IS a lane change THAT moves past a slower vehicle ALSO CALLED overtaking

sources m1, m2

### 1c ↔ p05:1b (wording similarity 0.46)

**Differences:** extra clause WHEN

Claude:

`1c` FACT · None · None

> FACT vehicles on the same road do not all travel at the same speed, even though every public road has a speed limit

sources m3

Model:

`p05:1b` FACT · None · None

> FACT not all vehicles travel at the same speed, so a driver may want to pass some slow-moving vehicles WHEN the driver is following them

sources m3

### 2.1a ↔ p05:2.1a (wording similarity 0.58)

**Differences:** missing clause ONLY IF; extra clause WHEN; vague not marked: enough; vague extra: enough space and time

Claude:

`2.1a` RULE · ADVISORY · imperative ("be sure")

> a driver SHOULD start a lane change or a pass ONLY IF the driver has [?enough] space and time to complete it [?safely]

sources m4 · flags J “enough”, J “safely”

Model:

`p05:2.1a` RULE · ADVISORY · imperative ("be sure")

> a driver SHOULD be sure the driver has [?enough space and time] to complete the move [?safely] WHEN the driver is about to change lanes or pass another vehicle

sources m4 · flags J “enough space and time”, J “safely”

### 2.1b ↔ p05:2.1b (wording similarity 0.89)

**No structural differences.**

Claude:

`2.1b` RULE · ADVISORY · imperative ("Never")

> a driver SHOULD NOT pass a vehicle UNLESS the driver is [?sure] the pass can be made without danger to the driver or others

sources m5 · flags J “sure”

Model:

`p05:2.1b` RULE · ADVISORY · imperative ("Never")

> a driver SHOULD NOT pass another vehicle UNLESS the driver is [?sure] the driver can do so without danger to the driver or others

sources m5 · flags J “sure”

### 2.1c ↔ p05:2.1c (wording similarity 0.87)

**Differences:** vague not marked: in doubt

Claude:

`2.1c` RULE · ADVISORY · imperative ("do not")

> a driver SHOULD NOT pass WHEN the driver is [?in doubt]

sources m6 · flags J “in doubt”

Model:

`p05:2.1c` RULE · ADVISORY · imperative ("do not pass")

> a driver SHOULD NOT pass another vehicle WHEN the driver is in doubt

sources m6 · flags J “in doubt”

### 2.1d ↔ p02:2.1a (wording similarity 0.85)

**No structural differences.**

Claude:

`2.1d` RULE · ADVISORY · imperative ("Keep to the right")

> a driver SHOULD keep to the right of the road, or to the right-hand lane of a multi-lane road UNLESS the driver is turning left OR passing another vehicle

sources m7

Model:

`p02:2.1a` RULE · ADVISORY · imperative ("Keep to the right")

> a driver SHOULD keep to the right of the road OR keep in the right-hand lane on multi-lane roads UNLESS the driver wants to turn left OR the driver wants to pass another vehicle

sources m7

### 2.2a ↔ p05:2.2a (wording similarity 1.00)

**Differences:** extra clause ONLY IF

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
> 1. use the left-turn signal to show that the driver wants to pass AND check that the way is clear ahead and behind WHEN the driver is about to move into the passing lane
> 2. change lanes ONLY IF the driver has signalled
> 3. signal that the driver wants to move back into the original lane AND change lanes WHEN the driver can see the entire front of the vehicle being passed in the inside mirror

sources m11, m14, m8, m9 · flags V “inside mirror”

### 2.2b ↔ p05:2.2c (wording similarity 0.69)

**Differences:** missing clause WHEN; extra clause WHILE

Claude:

`2.2b` RULE · ADVISORY · caution ("Be careful not to")

> a driver SHOULD NOT cut off the vehicle being passed by moving in front of it suddenly WHEN returning to the original lane

sources m12

Model:

`p05:2.2c` RULE · ADVISORY · caution ("Be careful")

> a driver SHOULD NOT cut off a vehicle by suddenly moving in front of it WHILE passing a vehicle

sources m12

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

### 3.1.3a ↔ p05:3.1.3a (wording similarity 0.72)

**Differences:** vague not marked: enough, safely; vague extra: enough clear distance, safety

Claude:

`3.1.3a` RULE · ADVISORY · imperative ("Don't attempt")

> a driver SHOULD NOT pass WHEN (the driver is approaching the crest of a hill OR the driver is on a curve) AND the view of oncoming traffic is obstructed AND the clear distance ahead is not [?enough] to pass [?safely]

sources m18 · flags J “enough”, J “safely”

Model:

`p05:3.1.3a` RULE · ADVISORY · imperative ("Don't attempt")

> a driver SHOULD NOT attempt to pass WHEN the driver is approaching the crest of a hill OR the driver is on a curve AND the driver's vision of oncoming traffic is obstructed AND there is not [?enough clear distance] ahead to pass in [?safety]

sources m18 · flags J “enough clear distance”, J “safety”

### 3.1.4a ↔ p06:3.1.4a (wording similarity 0.87)

**No structural differences.**

Claude:

`3.1.4a` RULE · ADVISORY · default (prescriptive passive "are not to be used")

> a driver SHOULD NOT use a two-way left-turn lane for passing

sources m19 · flags M “are not to be used”

Model:

`p06:3.1.4a` RULE · ADVISORY · default ("not to be used for")

> a driver SHOULD NOT use a left-turn lane to pass

sources m19 · flags M “not to be used for passing”

### 3.1.5b ↔ p11:3.1.5a (wording similarity 0.62)

**Differences:** force ADVISORY → LEGAL; modal SHOULD NOT → MUST NOT; missing clause BECAUSE

Claude:

`3.1.5b` RULE · ADVISORY · text ("should not")

> a driver SHOULD NOT pass WHEN there is a solid line at the left of the driver's lane BECAUSE a solid line there means it is unsafe to pass

sources m21, m22

Model:

`p11:3.1.5a` RULE · LEGAL · text ("not safe to pass")

> a driver MUST NOT pass a vehicle WHEN a solid line is at the left of the driver's lane

sources m20, m21, m22 · flags M “unsafe to pass”

### 3.1.6a ↔ p11:3.1.6a (wording similarity 0.91)

**Differences:** missing clause ONLY IF; vague not marked: enough, safely

Claude:

`3.1.6a` RULE · LEGAL · text ("may")

> a driver MAY pass WHEN there is a broken line at the left of the driver's lane ONLY IF the way is clear AND there are [?enough] broken lines ahead to complete the pass [?safely]

sources m23, m24 · flags J “enough”, J “safely”

Model:

`p11:3.1.6a` RULE · LEGAL · text ("may pass")

> a driver MAY pass a vehicle WHEN a broken line is at the left of the driver's lane AND the way is clear AND there are enough broken lines ahead to complete the pass safely

sources m23, m24 · flags J “enough broken lines ahead to complete the pass safely”

### 3.1.7a ↔ p10:3.1.7a (wording similarity 0.83)

**No structural differences.**

Claude:

`3.1.7a` RULE · LEGAL · context (Regulatory signs: "These signs give a direction that must be obeyed")

> a driver MUST NOT pass WHEN a "do not pass" sign applies to the road

sources m25, m26

Model:

`p10:3.1.7a` RULE · LEGAL · context (Regulatory signs: "These signs give a direction that must be obeyed")

> a driver MUST NOT pass on the road WHEN a "do not pass" sign is posted for the road

sources m25, m26

### 3.2.1a ↔ p05:3.2.1a (wording similarity 0.81)

**Differences:** type DEFINE → FACT; vague not marked: safely

Claude:

`3.2.1a` DEFINE · None · None

> DEFINE a passing lane or climbing lane IS an added lane THAT lets slower vehicles move into the right-hand lane so faster vehicles can pass [?safely] in the left lane

sources m27, m28 · flags J “safely”

Model:

`p05:3.2.1a` FACT · None · None

> FACT some roads have special passing or climbing lanes that let slower vehicles move into the right-hand lane so that faster ones can pass safely in the left lane

sources m27, m28

### 3.2.1c ↔ p05:3.2.1b (wording similarity 0.42)

**Differences:** type RULE → FACT; force ADVISORY → None; modal SHOULD → -; basis implied → None; missing clause WHEN; vague not marked: safely

Claude:

`3.2.1c` RULE · ADVISORY · implied ("so drivers … can begin to merge safely")

> a driver in the right-hand lane SHOULD merge [?safely] with traffic in the left-hand lane WHEN a sign warns that the lane is ending

sources m29 · flags D “merge”, J “safely”

Model:

`p05:3.2.1b` FACT · None · None

> FACT an advance sign tells drivers they will soon have a chance to pass AND another sign warns when the lane is ending so drivers in the right-hand lane can begin to merge safely with traffic in the left-hand lane

sources m29

### 3.2.1d ↔ p10:3.2.1a (wording similarity 0.67)

**No structural differences.**

Claude:

`3.2.1d` RULE · LEGAL · context (Regulatory signs: "must be obeyed")

> a driver MUST keep to the right-hand lane WHEN a "keep right except to pass" sign is posted UNLESS the driver is passing on a two-lane section where a climbing or passing lane is provided

sources m30, m31

Model:

`p10:3.2.1a` RULE · LEGAL · context (Regulatory signs: "These signs give a direction that must be obeyed")

> a driver MUST keep to the right lane WHEN driving on a two-lane section where climbing or passing lanes are provided UNLESS the driver is passing

sources m30, m31

### 3.2.2a ↔ p07:3.2.2a (wording similarity 0.77)

**Differences:** extra clause WHILE

Claude:

`3.2.2a` RULE · ADVISORY · text ("should")

> a driver on a freeway SHOULD keep to the right AND use the left lanes for passing

sources m32

Model:

`p07:3.2.2a` RULE · ADVISORY · text ("should keep")

> a driver SHOULD keep to the right AND use the left lanes for passing WHILE driving on a freeway

sources m32

### 3.2.2b ↔ p07:3.2.2b (wording similarity 0.65)

**Differences:** modal SHOULD → SHOULD SHOULD NOT; missing clause ONLY IF; extra clause WHILE

Claude:

`3.2.2b` RULE · ADVISORY · imperative ("Use … but don't stay there")

> a driver SHOULD use the far-left lane of a multi-lane freeway ONLY IF the driver is passing traffic that moves slower than the speed limit

sources m33

Model:

`p07:3.2.2b` RULE · ADVISORY · imperative ("Use")

> a driver SHOULD use the far left lane of a multi-lane freeway to pass traffic moving slower than the speed limit AND SHOULD NOT stay in the far left lane WHILE driving on a multi-lane freeway

sources m33

### 3.2.2c ↔ p07:3.2.2e (wording similarity 0.82)

**Differences:** missing clause WHEN; extra clause WHILE; vague not marked: possible

Claude:

`3.2.2c` RULE · ADVISORY · imperative ("Drive in the right-hand lane", "Get into the habit")

> a driver on a freeway SHOULD drive in the right-hand lane WHEN [?possible] BECAUSE this leaves the other lanes clear for passing

sources m33, m34 · flags J “possible”

Model:

`p07:3.2.2e` RULE · ADVISORY · imperative ("Get into the habit")

> a driver SHOULD drive in the right lane WHILE driving on a freeway BECAUSE this leaves the other lanes clear for passing

sources m34

### 3.2.3a ↔ p05:3.2.3b (wording similarity 0.58)

**Differences:** type RULE → FACT; force ADVISORY → None; modal SHOULD → -; basis default → None; missing clause BECAUSE

Claude:

`3.2.3a` RULE · ADVISORY · default (stated as a description: "Most passing is done on the left")

> a driver SHOULD pass on the left BECAUSE passing on the right can be more dangerous

sources m35, m36 · flags D “pass on the left”, S “Most passing”

Model:

`p05:3.2.3b` FACT · None · None

> FACT passing on the right can be more dangerous than passing on the left

sources m36

### 3.2.3b ↔ p05:3.2.3a (wording similarity 0.94)

**No structural differences.**

Claude:

`3.2.3b` RULE · LEGAL · text ("may")

> EXCEPTION TO 3.2.3a: a driver MAY pass on the right WHEN the road is multi-lane OR the road is one-way OR the vehicle being passed is a streetcar OR the vehicle being passed is turning left

sources m35

Model:

`p05:3.2.3a` RULE · LEGAL · text ("may")

> a driver MAY pass on the right WHEN the road is multi-lane OR the road is one-way OR the vehicle being passed is a streetcar OR the vehicle being passed is turning left

sources m35

### 3.2.3d ↔ p05:3.2.3c (wording similarity 0.39)

**Differences:** modal SHOULD NOT → SHOULD SHOULD NOT; missing clause BECAUSE

Claude:

`3.2.3d` RULE · ADVISORY · imperative ("Do not")

> a driver SHOULD NOT change lanes suddenly to pass on the right WHEN the driver is in the leftmost lane behind a slower vehicle BECAUSE the driver in front may move to the right at the same time

sources m37

Model:

`p05:3.2.3c` RULE · ADVISORY · imperative ("wait", "Do not")

> a driver SHOULD wait for the vehicle in front to move to the right AND SHOULD NOT suddenly change lanes and pass on the right WHEN the driver is driving in the far-left lane AND there is a slower vehicle in front of the driver

sources m37

### 3.2.4a ↔ p05:3.2.4a (wording similarity 0.97)

**No structural differences.**

Claude:

`3.2.4a` RULE · LEGAL · text ("may … only")

> a driver MAY drive on the right shoulder ONLY IF the driver is passing a vehicle that is turning left AND the shoulder is paved

sources m38 · flags D “right shoulder”

Model:

`p05:3.2.4a` RULE · LEGAL · text ("may")

> a driver MAY drive on the right shoulder ONLY IF the driver is passing a vehicle turning left AND the shoulder is paved

sources m38

### 3.2.4b ↔ p05:3.2.4b (wording similarity 0.75)

**No structural differences.**

Claude:

`3.2.4b` RULE · LEGAL · text ("may not")

> a driver MUST NOT pass on the left shoulder, whether or not it is paved

sources m38

Model:

`p05:3.2.4b` RULE · LEGAL · text ("may not")

> a driver MUST NOT pass on the left shoulder

sources m38

### 3.3.1a ↔ p05:3.3.1a (wording similarity 0.79)

**Differences:** basis imperative → caution

Claude:

`3.3.1a` RULE · ADVISORY · imperative ("Be very careful")

> a driver SHOULD pass with [?extra care] WHEN it is night

sources m39 · flags J “extra care”

Model:

`p05:3.3.1a` RULE · ADVISORY · caution ("Be very careful")

> a driver SHOULD pass other vehicles with [?extra care] WHEN passing at night

sources m39 · flags J “extra care”

### 3.3.1b ↔ p05:3.3.1b (wording similarity 0.90)

**Differences:** missing clause BECAUSE

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

> TO pass a vehicle at night WHEN the driver has to pass AND the way is clear
> 1. switch the headlights to low beams WHEN the driver is approaching a vehicle from behind
> 2. signal AND check the mirrors and blind spot AND pull out to pass
> 3. switch on the high beams WHILE moving alongside the vehicle being passed
> 4. pull back into the right-hand lane WHEN the driver can see all of the front of the vehicle being passed in the inside mirror
> 5. signal

sources m40, m41, m42, m43, m52 · flags V “inside mirror”

### 3.3.1c ↔ p01:3.4.6a (wording similarity 0.96)

**No structural differences.**

Claude:

`3.3.1c` RULE · ADVISORY · imperative ("Use")

> a driver SHOULD use low beams WHEN the driver is less than 60 m behind another vehicle UNLESS the driver is passing it

sources m44

Model:

`p01:3.4.6a` RULE · ADVISORY · imperative ("Use")

> a driver SHOULD use low beams WHEN the driver is less than 60 m behind another vehicle UNLESS the driver is passing the vehicle

sources m44

### 3.3.2a ↔ p09:3.3.2c (wording similarity 0.85)

**Differences:** basis text → imperative

Claude:

`3.3.2a` RULE · ADVISORY · text ("Avoid") and imperative ("Don't")

> a driver SHOULD NOT pass WHEN driving in fog

sources m45, m47

Model:

`p09:3.3.2c` RULE · ADVISORY · imperative ("Don't")

> a driver SHOULD NOT pass other vehicles WHEN driving in fog

sources m47 · flags X “Don't pass other vehicles”

### 3.3.2b ↔ p09:3.3.2b (wording similarity 0.86)

**No structural differences.**

Claude:

`3.3.2b` RULE · ADVISORY · imperative ("Don't")

> a driver SHOULD NOT speed up to pass a slow-moving vehicle WHEN driving in fog

sources m46

Model:

`p09:3.3.2b` RULE · ADVISORY · imperative ("Don't")

> a driver SHOULD NOT speed up to pass a vehicle moving slowly WHEN driving in fog

sources m46

### 3.3.3a ↔ p09:3.3.3a (wording similarity 0.76)

**No structural differences.**

Claude:

`3.3.3a` RULE · ADVISORY · text ("Avoid")

> a driver SHOULD NOT pass WHEN driving in blowing snow or a whiteout

sources m48

Model:

`p09:3.3.3a` RULE · ADVISORY · text ("Avoid")

> a driver SHOULD NOT pass another vehicle WHEN driving in a whiteout

sources m48

### 3.3.3b ↔ p09:3.3.3b (wording similarity 0.80)

**No structural differences.**

Claude:

`3.3.3b` RULE · ADVISORY · imperative ("Don't")

> a driver SHOULD NOT attempt to pass a slow-moving vehicle WHEN driving in blowing snow or a whiteout

sources m49

Model:

`p09:3.3.3b` RULE · ADVISORY · imperative ("Don't")

> a driver SHOULD NOT attempt to pass a vehicle moving slowly WHEN driving in a whiteout

sources m49

### 3.4.1a ↔ p05:3.4.1a (wording similarity 0.84)

**Differences:** missing clause WHILE; extra clause WHEN

Claude:

`3.4.1a` RULE · ADVISORY · caution ("watch carefully for")

> a driver SHOULD WATCH FOR doors opening suddenly AND doors opened to load or unload WHILE passing parked vehicles

sources m50

Model:

`p05:3.4.1a` RULE · ADVISORY · caution ("watch carefully")

> a driver SHOULD WATCH FOR people suddenly opening doors AND doors opened to load and unload WHEN passing parked vehicles

sources m50

### 3.4.2c ↔ p05:3.4.2a (wording similarity 0.61)

**Differences:** modal SHOULD → SHOULD NOT

Claude:

`3.4.2c` RULE · ADVISORY · imperative ("do so by changing lanes")

> a driver SHOULD change lanes WHEN passing a motorcycle, bicycle, limited-speed motorcycle or moped

sources m51

Model:

`p05:3.4.2a` RULE · ADVISORY · imperative ("Do not take", "do so by changing lanes")

> a driver SHOULD NOT pass a motorcycle, bicycle, limited-speed motorcycle or moped in the same lane WHEN the vehicle pulls to the left or right side of its lane

sources m51

### 3.4.3a ↔ p06:3.4.3a (wording similarity 0.91)

**Differences:** vague not marked: smaller vehicle

Claude:

`3.4.3a` RULE · ADVISORY · imperative ("Wait … before you pass")

> a driver SHOULD NOT pass a [?smaller vehicle] that is turning left ahead UNTIL it has moved to the right

sources m53 · flags R “smaller vehicle”

Model:

`p06:3.4.3a` RULE · ADVISORY · imperative ("Wait")

> a driver SHOULD NOT pass a smaller vehicle that is turning left ahead UNTIL the smaller vehicle has moved to the right

sources m53 · flags R “the smaller vehicle”

### 3.4.3b ↔ p06:3.4.3b (wording similarity 0.68)

**Differences:** vague not marked: smaller vehicle

Claude:

`3.4.3b` RULE · ADVISORY · imperative ("do not pull up beside it")

> a driver SHOULD NOT pull up beside a [?smaller vehicle] that is turning left ahead to make the turn at the same time WHEN the driver is also turning left, behind it

sources c6 · flags R “smaller vehicle”

Model:

`p06:3.4.3b` RULE · ADVISORY · imperative ("do not pull up")

> a driver SHOULD NOT pull up beside a vehicle turning left WHEN the driver is making a left turn behind the vehicle

sources c6 · flags R “one of these vehicles”

### 3.4.3c ↔ p06:3.4.3c (wording similarity 0.70)

**Differences:** missing clause UNTIL; vague not marked: clear, smaller vehicle

Claude:

`3.4.3c` RULE · ADVISORY · imperative ("Stay behind")

> a driver SHOULD stay behind a [?smaller vehicle] that is turning left ahead WHEN the driver is also turning left, behind it UNTIL the way is [?clear]

sources c7 · flags R “smaller vehicle”, J “clear”

Model:

`p06:3.4.3c` RULE · ADVISORY · imperative ("Stay", "turn")

> a driver SHOULD stay behind a vehicle turning left AND turn WHEN the way is clear WHEN the driver is making a left turn behind the vehicle

sources c7 · flags J “clear”

### 3.4.4a ↔ p03:3.4.4b (wording similarity 0.68)

**Differences:** force LEGAL → ADVISORY; modal MAY → SHOULD; basis text → implied; vague not marked: necessary for safety, safely

Claude:

`3.4.4a` RULE · LEGAL · text ("can")

> a cyclist MAY use any part of the lane WHEN this is [?necessary for safety], for example to discourage passing where the lane is too narrow to be shared [?safely]

sources m54, m55 · flags J “necessary for safety”, J “safely”

Model:

`p03:3.4.4b` RULE · ADVISORY · implied ("Discourage passing")

> a cyclist SHOULD position the bicycle in the lane to discourage passing WHEN the lane is too narrow to be shared safely

sources m54, m55 · flags J “too narrow to be shared safely”

### 3.4.4b ↔ p03:3.4.4c (wording similarity 0.78)

**Differences:** extra clause ONLY IF; vague not marked: where practical

Claude:

`3.4.4b` RULE · LEGAL · text ("must maintain")

> a driver of a motor vehicle MUST keep at least 1 m between the vehicle and a cyclist WHILE passing the cyclist, [?where practical] IF VIOLATED a fine AND 2 demerit points

sources m56, m57, m59 · flags J “where practical”

Model:

`p03:3.4.4c` RULE · LEGAL · text ("must maintain")

> a driver MUST maintain a minimum distance of 1 m between the vehicle and the cyclist WHILE passing a cyclist ONLY IF practical IF VIOLATED a fine AND 2 demerit points

sources m56, m57, m59 · flags J “practical”

### 3.4.4c ↔ p03:3.4.4d (wording similarity 1.00)

**Differences:** vague not marked: possible

Claude:

`3.4.4c` RULE · ADVISORY · text ("should")

> a driver SHOULD change lanes to pass a cyclist WHEN [?possible]

sources m58 · flags J “possible”

Model:

`p03:3.4.4d` RULE · ADVISORY · text ("should change lanes")

> a driver SHOULD change lanes to pass a cyclist WHEN possible

sources m58 · flags J “possible”

### 3.4.4d ↔ p03:3.4.4e (wording similarity 0.93)

**Differences:** vague not marked: unnecessarily

Claude:

`3.4.4d` RULE · ADVISORY · imperative ("Do not")

> a driver SHOULD NOT sound the horn [?unnecessarily] WHILE passing a cyclist BECAUSE it may frighten the cyclist and cause a loss of control

sources m60 · flags J “unnecessarily”

Model:

`p03:3.4.4e` RULE · ADVISORY · imperative ("Do not sound")

> a driver SHOULD NOT sound the horn unnecessarily WHILE passing a cyclist BECAUSE it may frighten the cyclist and cause the cyclist to lose control

sources m60 · flags J “unnecessarily”

### 3.4.4e ↔ p03:3.4.4f (wording similarity 0.70)

**Differences:** extra clause WHILE; vague not marked: some distance

Claude:

`3.4.4e` RULE · ADVISORY · imperative ("tap it")

> a driver SHOULD tap the horn quickly and lightly while still [?some distance] away from the cyclist WHEN the driver feels the horn must be used

sources m60 · flags J “some distance”

Model:

`p03:3.4.4f` RULE · ADVISORY · imperative ("tap it quickly")

> a driver SHOULD tap the horn quickly and lightly WHILE passing a cyclist WHEN the driver is still some distance away from the cyclist

sources m60 · flags J “some distance”

### 3.4.5a ↔ p05:3.4.5a (wording similarity 0.95)

**No structural differences.**

Claude:

`3.4.5a` RULE · LEGAL · text ("must")

> a driver MUST pass a streetcar on the right UNLESS the driver is on a one-way road

sources m62

Model:

`p05:3.4.5a` RULE · LEGAL · text ("must")

> a driver MUST pass a streetcar on the right UNLESS the driver is driving on a one-way road

sources m62

### 3.4.5b ↔ p05:3.4.5b (wording similarity 0.37)

**Differences:** extra clause UNLESS

Claude:

`3.4.5b` RULE · ADVISORY · imperative ("stay")

> a driver SHOULD stay at least 2 m behind the rear doors of a streetcar WHEN the streetcar is stopped AND passengers are getting on or off

sources m61, m63 · flags M “stay at least two metres”

Model:

`p05:3.4.5b` RULE · ADVISORY · imperative ("stay")

> a driver SHOULD stay at least 2 m behind the rear doors WHERE passengers are getting off or on WHEN the driver is at a streetcar stop UNLESS an area has been set aside for streetcar passengers at the stop

sources m61, m63 · flags M “stay at least two metres”

### 3.4.5d ↔ p05:3.4.5c (wording similarity 0.76)

**Differences:** extra clause WHEN; vague extra: these areas

Claude:

`3.4.5d` RULE · ADVISORY · imperative ("Always pass", "be prepared")

> a driver SHOULD pass a streetcar passenger area at a [?reasonable speed] AND SHOULD WATCH FOR pedestrians making sudden or unexpected moves

sources m64 · flags J “reasonable speed”, R “these areas”, X “safety islands and zones”

Model:

`p05:3.4.5c` RULE · ADVISORY · imperative ("pass", "be prepared")

> a driver SHOULD pass [?these areas] at a [?reasonable speed] AND SHOULD be prepared for pedestrians to make sudden or unexpected moves WHEN passing a streetcar stop

sources m64 · flags R “these areas”, J “reasonable speed”

### 3.4.6a ↔ p03:3.4.6a (wording similarity 0.76)

**Differences:** missing clause WHEN; extra clause WHILE; vague not marked: closely, safely

Claude:

`3.4.6a` RULE · ADVISORY · imperative ("do not cut in")

> a driver SHOULD NOT cut in [?closely] in front of a large vehicle WHEN returning to the lane after passing it BECAUSE this reduces the space cushion the large vehicle needs to stop [?safely]

sources m65 · flags J “closely”, J “safely”

Model:

`p03:3.4.6a` RULE · ADVISORY · imperative ("do not cut in front")

> a driver SHOULD NOT cut in front closely of a large vehicle WHILE passing a large vehicle BECAUSE it reduces the space cushion large vehicles require in order to stop safely

sources m65 · flags J “closely”

### 3.4.6b ↔ p03:3.4.6b (wording similarity 0.98)

**Differences:** missing clause WHEN; extra clause WHILE; vague not marked: more room

Claude:

`3.4.6b` RULE · ADVISORY · imperative ("Allow")

> a driver SHOULD allow [?more room] WHEN passing a large vehicle

sources m65 · flags J “more room”

Model:

`p03:3.4.6b` RULE · ADVISORY · imperative ("Allow more room")

> a driver SHOULD allow more room WHILE passing a large vehicle

sources m65 · flags J “more room”

### 3.4.6c ↔ p03:3.4.6c (wording similarity 0.85)

**No structural differences.**

Claude:

`3.4.6c` FACT · None · None

> FACT a large vehicle can create heavy air turbulence that may affect the driver's control WHILE passing it

sources m66

Model:

`p03:3.4.6c` FACT · None · None

> FACT a large vehicle can create heavy air turbulence that may affect the driver's ability to control the vehicle WHILE passing a large vehicle

sources m66

### 3.4.6e ↔ p10:3.4.6a (wording similarity 0.44)

**No structural differences.**

Claude:

`3.4.6e` RULE · ADVISORY · text ("It is important to")

> a driver SHOULD anticipate the extended length AND limited speed of an LCV WHEN preparing to pass it

sources m68

Model:

`p10:3.4.6a` RULE · ADVISORY · text ("It is important to")

> a driver SHOULD recognize a long commercial vehicle on the highway based on rear signage AND anticipate the extended length and limited speed WHEN the driver is preparing to pass the long commercial vehicle on the highway

sources m67, m68

### 3.4.7a ↔ p03:3.4.7a (wording similarity 0.80)

**Differences:** modal SHOULD SHOULD NOT → SHOULD; vague not marked: well back

Claude:

`3.4.7a` RULE · ADVISORY · imperative ("Stay … do not pass until")

> a driver SHOULD stay [?well back] of farm machinery AND SHOULD NOT pass it UNTIL it is [?safe] to do so

sources m69 · flags J “well back”, J “safe”

Model:

`p03:3.4.7a` RULE · ADVISORY · imperative ("Stay well back")

> a driver SHOULD stay well back from farm machinery UNTIL it is [?safe] to pass

sources m69 · flags J “well back”, J “safe”

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

### 3.4.8b ↔ p03:3.4.8c (wording similarity 0.68)

**Differences:** vague not marked: as much distance as possible

Claude:

`3.4.8b` RULE · ADVISORY · imperative ("give")

> a driver SHOULD leave [?as much distance as possible] WHILE passing a horse-drawn vehicle BECAUSE passing too closely could startle the horse and make it change direction suddenly

sources m71 · flags J “as much distance as possible”

Model:

`p03:3.4.8c` RULE · ADVISORY · imperative ("give as much distance")

> a driver SHOULD give as much distance between the vehicle and the horse-drawn vehicle as possible WHILE passing a horse-drawn vehicle BECAUSE passing too closely could scare or startle the horse, causing it to change direction suddenly on the roadway

sources m71 · flags J “as much distance ... as possible”

### 3.4.9a ↔ p05:3.4.9a (wording similarity 0.70)

**Differences:** missing clause WHEN

Claude:

`3.4.9a` RULE · ADVISORY · imperative ("Don't")

> a driver SHOULD NOT pass a snow plow WHEN the snow plow is moving

sources m72 · flags M “under any conditions”

Model:

`p05:3.4.9a` RULE · ADVISORY · imperative ("Don't pass")

> a driver SHOULD NOT pass a moving snow plow

sources m72 · flags M “under any conditions”

### 3.4.9b ↔ p09:3.4.9a (wording similarity 0.80)

**Differences:** vague not marked: enough, safely

Claude:

`3.4.9b` RULE · ADVISORY · imperative ("Do not try")

> a driver SHOULD NOT pass between snow plows WHEN several snow plows are staggered across a freeway BECAUSE there is not [?enough] room to pass [?safely] AND the ridge of wet snow can throw the vehicle out of control

sources m73 · flags J “enough”, J “safely”

Model:

`p09:3.4.9a` RULE · ADVISORY · imperative ("Do not try")

> a driver SHOULD NOT pass between several snow plows WHEN the snow plows are staggered across the road on a freeway BECAUSE there is not enough room to pass safely AND the ridge of wet snow can throw the vehicle out of control

sources m73

### 3.4.10a ↔ p10:3.4.10a (wording similarity 0.72)

**Differences:** force ADVISORY → LEGAL; modal SHOULD NOT → MUST NOT; basis imperative → context

Claude:

`3.4.10a` RULE · ADVISORY · imperative ("Do not pass")

> a driver SHOULD NOT pass a pilot vehicle or pace vehicle WHEN it carries the "do not pass" temporary condition sign

sources m74, m75 · flags M “Do not pass the pilot vehicle”

Model:

`p10:3.4.10a` RULE · LEGAL · context (Temporary condition signs: implied legal force for temporary traffic control)

> a driver MUST NOT pass a pilot vehicle or pace vehicle WHEN the vehicle is bearing a "do not pass" sign

sources m74, m75

### 3.4.11a ↔ p03:3.4.11a (wording similarity 0.95)

**No structural differences.**

Claude:

`3.4.11a` RULE · ADVISORY · imperative ("Do not pass")

> a driver SHOULD NOT pass a vehicle WHEN the vehicle is stopped at a crosswalk BECAUSE a stopped vehicle may mean a pedestrian is crossing

sources m76

Model:

`p03:3.4.11a` RULE · ADVISORY · imperative ("Do not pass")

> a driver SHOULD NOT pass a vehicle WHEN the vehicle is stopped at a crosswalk BECAUSE a stopped vehicle may be a clue that a pedestrian is crossing

sources m76

### 3.4.12a ↔ p04:3.4.12e (wording similarity 0.95)

**Differences:** vague not marked: illegally passed

Claude:

`3.4.12a` FACT · None · None

> FACT school bus drivers and other witnesses can report vehicles that have [?illegally passed] a school bus

sources m77 · flags G “illegally passed”

Model:

`p04:3.4.12e` FACT · None · None

> FACT school bus drivers and other witnesses can report vehicles that have illegally passed a school bus IN Ontario

sources m77

### 3.4.12b ↔ p04:3.4.12f (wording similarity 0.81)

**Differences:** basis text → context; vague not marked: heavy

Claude:

`3.4.12b` RULE · LEGAL · text ("You must stop")

> a driver MUST stop WHEN approaching a stopped school bus with its upper alternating red lights flashing, from either direction IF VIOLATED a [?heavy] fine AND 6 demerit points for a first offence

sources c1, c5 · flags J “heavy”, X “stop arm activated”

Model:

`p04:3.4.12f` RULE · LEGAL · context (penalty: "can be fined heavily and get six demerit points")

> a driver MUST stop WHEN the driver approaches a stopped school bus with its upper alternating red lights flashing IF VIOLATED a fine AND 6 demerit points

sources c1, c5

### 3.4.12c ↔ p04:3.4.12b (wording similarity 0.82)

**Differences:** force ADVISORY → LEGAL; modal SHOULD → MUST; basis imperative → text

Claude:

`3.4.12c` RULE · ADVISORY · imperative ("stop at least 20 metres away")

> a driver SHOULD stop at least 20 m from the bus WHEN approaching a stopped school bus with its upper alternating red lights flashing from behind

sources c2 · flags M “stop at least 20 metres away”

Model:

`p04:3.4.12b` RULE · LEGAL · text ("must stop" from c1, "stop" imperative in c2)

> a driver MUST stop at least 20 m from the school bus WHEN the driver is approaching a stopped school bus with its upper alternating red lights flashing AND the driver is coming from behind the bus

sources c1, c2

### 3.4.12d ↔ p04:3.4.12c (wording similarity 0.89)

**Differences:** force ADVISORY → LEGAL; modal SHOULD NOT → MUST NOT; basis imperative → text

Claude:

`3.4.12d` RULE · ADVISORY · imperative ("Do not go until")

> a driver SHOULD NOT go WHEN stopped for a school bus with its upper alternating red lights flashing UNTIL the bus moves OR the lights have stopped flashing

sources c3 · flags M “Do not go”, X “and its stop arm is no longer activated”

Model:

`p04:3.4.12c` RULE · LEGAL · text ("must stop" from c1, "Do not go" imperative in c3)

> a driver MUST NOT move the vehicle WHEN the driver is stopped for a school bus with its upper alternating red lights flashing UNTIL the bus moves OR the lights have stopped flashing

sources c1, c3

### 3.4.12e ↔ p04:3.4.12d (wording similarity 0.86)

**No structural differences.**

Claude:

`3.4.12e` EXCEPTION · None · None

> EXCEPTION TO 3.4.12b WHEN the road has a median strip AND the driver is approaching the bus from the front

sources c4

Model:

`p04:3.4.12d` EXCEPTION · None · None

> EXCEPTION TO p04:3.4.12a WHEN the driver is on a road with a median strip AND the driver is approaching the school bus from the front

sources c4

### 3.4.13a ↔ p12:3.4.13a (wording similarity 0.45)

**Differences:** basis text → context; missing clause WHEN; vague not marked: caution

Claude:

`3.4.13a` RULE · LEGAL · text ("you are required")

> a driver MUST slow down AND proceed with [?caution] WHEN approaching, in the same direction, an emergency vehicle stopped with red or red-and-blue lights flashing OR a tow truck stopped with amber lights flashing IF VIOLATED 3 demerit points

sources m78, m80 · flags J “caution”

Model:

`p12:3.4.13a` RULE · LEGAL · context (listed under "Table of offences")

> a driver MUST slow AND carefully pass a stopped emergency vehicle IF VIOLATED 3 demerit points

sources m80 · flags J “carefully”

### 3.4.13b ↔ p12:3.4.13b (wording similarity 0.62)

**Differences:** basis text → context; extra clause ONLY IF; vague not marked: if safe to do so

Claude:

`3.4.13b` RULE · LEGAL · text ("you are required")

> a driver MUST move into a lane away from the stopped emergency vehicle or tow truck, [?if safe to do so] WHEN the road has 2 or more lanes in the driver's direction IF VIOLATED 3 demerit points

sources m79, m81 · flags J “if safe to do so”, X “where possible”

Model:

`p12:3.4.13b` RULE · LEGAL · context (listed under "Table of offences")

> a driver MUST move into another lane WHEN passing a stopped emergency vehicle ONLY IF moving is possible IF VIOLATED 3 demerit points

sources m81 · flags J “possible”

### 3.5.1a ↔ p14:3.5.1a (wording similarity 0.70)

**Differences:** missing clause BECAUSE

Claude:

`3.5.1a` FACT · None · None

> FACT a vehicle towing a trailer cannot accelerate as quickly AND needs more space BECAUSE it is much longer

sources m82

Model:

`p14:3.5.1a` FACT · None · None

> FACT a driver towing a trailer cannot accelerate as quickly as a driver without a trailer

sources m82

### 3.5.1b ↔ p14:3.5.1c (wording similarity 0.75)

**Differences:** missing clause ONLY IF; extra clause WHEN

Claude:

`3.5.1b` RULE · ADVISORY · imperative ("make sure")

> a driver towing a trailer SHOULD pass ONLY IF the driver has [?enough] time and room to complete the pass

sources m82 · flags J “enough”

Model:

`p14:3.5.1c` RULE · ADVISORY · imperative ("make sure")

> a driver towing a trailer SHOULD make sure the driver has [?enough] time and room to complete the pass WHEN the driver is about to pass a vehicle

sources m82 · flags J “enough”

### 3.5.1c ↔ p14:3.5.1e (wording similarity 0.66)

**Differences:** modal SHOULD SHOULD NOT → SHOULD NOT; vague not marked: more room

Claude:

`3.5.1c` RULE · ADVISORY · imperative ("allow", "Do not cut back")

> a driver towing a trailer SHOULD allow [?more room] before moving back into the lane AND SHOULD NOT cut back in [?too soon] WHEN returning to the lane after passing BECAUSE this can make the trailer sway and become hard to control

sources m82 · flags J “more room”, J “too soon”

Model:

`p14:3.5.1e` RULE · ADVISORY · imperative ("Do not")

> a driver towing a trailer SHOULD NOT cut back into the original lane [?too soon] WHEN the driver has passed a vehicle BECAUSE it can cause the trailer to sway and make it difficult to control

sources m82 · flags J “too soon”

### 3.5.2a ↔ p14:3.5.2a (wording similarity 0.84)

**No structural differences.**

Claude:

`3.5.2a` RULE · ADVISORY · imperative ("signal, pull over and let")

> a driver towing a trailer SHOULD signal, pull over AND let the other vehicles pass WHEN the driver is holding up a line of traffic

sources m83 · flags R “If you are holding up a line of traffic”

Model:

`p14:3.5.2a` RULE · ADVISORY · imperative ("signal", "pull over")

> a driver towing a trailer SHOULD signal AND pull over WHEN the driver is holding up a line of traffic

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

### 3.5.2c ↔ p14:3.5.2e (wording similarity 0.64)

**Differences:** modal SHOULD NOT SHOULD → SHOULD

Claude:

`3.5.2c` RULE · ADVISORY · imperative ("do not brake", "steer")

> a driver towing a trailer SHOULD NOT brake AND SHOULD steer the vehicle and trailer [?carefully] back into position WHEN a passing bus or truck pushes the trailer out of position

sources m83 · flags J “carefully”

Model:

`p14:3.5.2e` RULE · ADVISORY · imperative ("steer")

> a driver towing a trailer SHOULD [?carefully] steer the vehicle and trailer back into position WHEN the trailer is whipped to the side by the wind behind a passing large bus or truck

sources m83 · flags J “carefully”

### 3.6.1a ↔ p05:3.6.1a (wording similarity 0.90)

**Differences:** vague not marked: in safety; vague extra: safety

Claude:

`3.6.1a` RULE · ADVISORY · imperative ("move to the right")

> a driver being passed SHOULD move to the right AND let the faster vehicle pass [?in safety] WHEN faster traffic wants to pass

sources m84, m87, m88 · flags M “move to the right”, J “in safety”

Model:

`p05:3.6.1a` RULE · ADVISORY · imperative ("move")

> a driver being passed SHOULD move to the right AND let faster traffic pass in [?safety] WHEN faster traffic wants to pass the driver

sources m84 · flags J “safety”

### 3.6.1b ↔ p05:3.6.4a (wording similarity 0.86)

**Differences:** missing clause WHILE, BECAUSE; extra clause WHEN

Claude:

`3.6.1b` RULE · LEGAL · text ("It is unlawful")

> a driver being passed MUST NOT speed up WHILE another driver is trying to pass BECAUSE it is dangerous

sources m85

Model:

`p05:3.6.4a` RULE · LEGAL · text ("unlawful")

> a driver being passed MUST NOT speed up WHEN another driver is trying to pass the driver

sources m85

### 3.6.1c ↔ p13:2.1a (wording similarity 0.68)

**Differences:** missing clause IF VIOLATED; vague not marked: sanctions for dangerous driving

Claude:

`3.6.1c` RULE · LEGAL · context (listed under "Sanctions – dangerous behaviours")

> a driver MUST NOT drive to prevent another vehicle from passing IF VIOLATED [?sanctions for dangerous driving]

sources m86 · flags R “sanctions for dangerous driving”

Model:

`p13:2.1a` RULE · LEGAL · context (listed under "Sanctions – dangerous behaviours")

> a driver MUST NOT drive a motor vehicle to prevent another vehicle from passing

sources m86

### 3.6.1d ↔ p10:3.2.2a (wording similarity 0.91)

**Differences:** vague not marked: slow traffic

Claude:

`3.6.1d` RULE · LEGAL · text ("must keep right")

> a driver in [?slow traffic] MUST keep right WHEN on a multi-lane road where a "slower traffic keep right" sign is posted

sources c8, c9 · flags J “slow traffic”

Model:

`p10:3.2.2a` RULE · LEGAL · text ("must keep right")

> a driver of slow traffic MUST keep right WHEN driving on a multi-lane road AND a "slow traffic keep right" sign is posted

sources c8, c9

### 3.6.2a ↔ p05:3.6.2a (wording similarity 0.45)

**Differences:** modal SHOULD SHOULD → SHOULD SHOULD SHOULD

Claude:

`3.6.2a` RULE · ADVISORY · imperative ("pay attention", "move closer")

> a driver being passed SHOULD WATCH FOR oncoming traffic AND SHOULD move closer to the right side of the lane WHEN on an undivided road AND the passing driver has pulled into the opposite lane

sources m89

Model:

`p05:3.6.2a` RULE · ADVISORY · imperative ("pay attention", "move", "Be prepared")

> a driver being passed SHOULD pay attention to oncoming traffic AND SHOULD move closer to the right side of the lane AND SHOULD be prepared to slow down WHEN the driver is being passed on an undivided road AND the passing driver has pulled into the opposite lane

sources m89

### 3.6.3a ↔ p05:3.6.3b (wording similarity 0.80)

**No structural differences.**

Claude:

`3.6.3a` RULE · LEGAL · text ("are not allowed", "cannot")

> a truck driver MUST NOT drive in the far-left lane WHEN on a high-speed road with 3 or more lanes in each direction where trucks are barred from that lane

sources m90, m91 · flags S “many high-speed roads”, X “many freeways”

Model:

`p05:3.6.3b` RULE · LEGAL · text ("not allowed")

> a truck driver MUST NOT drive in the far-left lane WHEN the road is a high-speed road with three or more lanes in each direction

sources m90 · flags S “many”

### 3.6.3b ↔ p07:3.2.2d (wording similarity 0.69)

**No structural differences.**

Claude:

`3.6.3b` RULE · LEGAL · text ("must use")

> a truck driver MUST use the lane next to the far-left lane for passing WHEN on a high-speed road with 3 or more lanes in each direction where trucks are barred from the far-left lane

sources m90, m91

Model:

`p07:3.2.2d` RULE · LEGAL · text ("must use")

> a truck driver MUST use the lane to the right of the far left lane for passing WHEN the freeway has three or more lanes in each direction AND the driver is in a large truck

sources m91 · flags S “many”

### 3.6.3c ↔ p05:3.6.3a (wording similarity 0.71)

**No structural differences.**

Claude:

`3.6.3c` RULE · ADVISORY · imperative ("move into")

> a driver in the truck passing lane SHOULD move into the right-hand lane [?as soon as the driver can] WHEN a truck wants to pass

sources m90 · flags J “as soon as the driver can”

Model:

`p05:3.6.3a` RULE · ADVISORY · imperative ("move")

> a driver SHOULD move into the right-hand lane [?as soon as the driver can] WHEN the driver is in the truck passing lane AND a truck wants to pass the driver

sources m90 · flags J “as soon as the driver can”

## Reference statements with no model partner (10)

`1a` DEFINE · None · None

> DEFINE changing position IS a manoeuvre THAT changes lanes OR passes another vehicle

sources m1

`1d` FACT · None · None

> FACT cyclists, road service vehicles and drivers preparing to turn are [?usually] slower than through traffic

sources m3 · flags S “usually”

`3.1.5a` FACT · None · None

> FACT pavement markings show, among other things, where it is not [?safe] to pass

sources m20 · flags J “safe”

`3.2.1b` FACT · None · None

> FACT an advance sign tells drivers a passing opportunity is coming, AND another sign warns when the added lane is ending

sources m29

`3.2.3c` RULE · ADVISORY · imperative ("wait")

> a driver SHOULD wait WHEN the driver is in the leftmost lane with a slower vehicle in front UNTIL the slower vehicle moves to the right

sources m37

`3.4.2a` FACT · None · None

> FACT motorcycles, bicycles, limited-speed motorcycles and mopeds [?often] move to the left or right side of their lane to avoid dangerous road conditions OR to be seen

sources m51 · flags S “often”

`3.4.2b` RULE · ADVISORY · imperative ("Do not take this as an invitation")

> a driver SHOULD NOT pass a motorcycle, bicycle, limited-speed motorcycle or moped within its lane BECAUSE its position in the lane is not an invitation to pass (3.4.2a)

sources m51, m52

`3.4.5c` EXCEPTION · None · None

> EXCEPTION TO 3.4.5b WHEN the streetcar stop has an area set aside for passengers

sources m63

`3.4.6d` DEFINE · None · None

> DEFINE a long commercial vehicle IS a double-trailer vehicle THAT can be up to 40 m long AND carries an LCV placard on its rear ALSO CALLED LCV

sources m67, m68

`3.6.2b` RULE · ADVISORY · caution ("Be prepared to")

> a driver being passed SHOULD be ready to slow down WHEN on an undivided road AND the passing driver is in the opposite lane BECAUSE slowing down lets the passing driver get back in front sooner and prevents a collision

sources m89

## Model statements with no reference partner (17)

`p03:3.4.4a` RULE · ADVISORY · text ("can use")

> a cyclist MAY use any part of the lane WHEN necessary for safety

sources m54

`p03:3.4.1a` RULE · ADVISORY · imperative ("look behind you")

> a driver SHOULD look behind the vehicle AND check the mirrors and blind spots for a passing cyclist WHEN the vehicle is parked on the side of the roadway AND the driver is about to open a door

sources m96

`p03:3.4.7b` RULE · ADVISORY · imperative ("do not pass")

> a driver SHOULD NOT pass farm machinery UNTIL it is [?safe] to do so

sources m69 · flags J “safe”

`p03:3.4.8a` RULE · ADVISORY · imperative ("Maintain")

> a driver SHOULD maintain a [?safe] following distance from a horse-drawn vehicle

sources m70 · flags J “safe”

`p04:3.1.1a` RULE · LEGAL · text ("must not pass")

> a driver MUST NOT pass any vehicle WHEN the driver is within 30 m of a pedestrian crossover

sources m16

`p04:3.4.12a` RULE · LEGAL · text ("must stop")

> a driver MUST stop WHEN the driver approaches a stopped school bus with its upper alternating red lights flashing

sources c1

`p05:2.2b` RULE · ADVISORY · caution ("Watch for")

> a driver SHOULD WATCH FOR bicycles and small vehicles that may be hidden from view in front of the vehicle being passed AND vehicles that may be turning left in front of the driver AND vehicles or pedestrians entering the road from another road or driveway WHILE passing a vehicle

sources m10

`p05:2.2d` RULE · ADVISORY · imperative ("do not race", "Go back")

> a driver SHOULD NOT race AND SHOULD go back to the original lane WHEN the vehicle being passed speeds up

sources m13

`p07:3.2.2c` RULE · ADVISORY · imperative ("Drive")

> a driver SHOULD drive in the right-hand lane WHEN possible WHILE driving on a freeway

sources m33 · flags J “possible”

`p09:3.3.2a` RULE · ADVISORY · text ("Avoid")

> a driver SHOULD NOT pass another vehicle WHEN driving in fog

sources m45

`p10:3.1.7b` FACT · None · None

> FACT the downward lines on a warning sign show the side on which a driver may safely pass

sources m94

`p14:3.5.1b` FACT · None · None

> FACT a driver towing a trailer needs more space than a driver without a trailer BECAUSE the length of the vehicle is much longer with a trailer attached

sources m82

`p14:3.5.1d` RULE · ADVISORY · imperative ("allow")

> a driver towing a trailer SHOULD allow [?more] room WHEN the driver has passed a vehicle UNTIL the driver moves back to the original lane

sources m82 · flags J “more”

`p14:3.5.2c` FACT · None · None

> FACT the wall of wind behind a large bus or truck that passes a driver towing a trailer may whip the trailer to the side, pushing it out of control

sources m83

`p14:3.5.2d` RULE · ADVISORY · imperative ("do not brake")

> a driver towing a trailer SHOULD NOT brake WHEN the trailer is whipped to the side by the wind behind a passing large bus or truck

sources m83

`p14:3.5.2f` RULE · ADVISORY · text ("may help")

> a driver towing a trailer MAY increase speed slightly WHEN the trailer is whipped to the side by the wind behind a passing large bus or truck

sources m83 · flags M “may help”

`p15:3.6.1a` RULE · LEGAL · text ("must")

> a driver being passed MUST move to the right AND allow the vehicle to pass WHEN the driver of another vehicle is about to overtake and pass the vehicle

sources m87, m88
