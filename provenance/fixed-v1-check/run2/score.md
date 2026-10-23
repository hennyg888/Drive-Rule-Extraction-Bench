# Score: provenance/fixed-v1-check/run2/output.json against analysis/passing-rules/passing-rules.v1.json

## Summary

- Statements: model 106 (DEFINE 2, EXCEPTION 1, FACT 21, PROCEDURE 2, RULE 80); reference 88 (DEFINE 4, EXCEPTION 2, FACT 9, PROCEDURE 2, RULE 71).
- Paired by shared sources: 86. Reference recall 86/88 (98%); model precision 86/106 (81%).
- On paired statements: type 84/86 (98%), force 81/86 (94%), modal 75/86 (87%), clause keywords 61/86 (71%), same sources 74/86 (86%), links 83/86 (97%).
- Law or advice on paired rules and procedures: 68/72 (94%).
- Inline flags (J, S, R, G) on paired statements: precision 0.75, recall 0.79, F1 0.77; same code on 41 of 42 matched spans.
- Passages the reference cites and the model does not: m50.
- Passages the model cites and the reference does not: m95.

## Validity

- Schema errors: 0
- Duplicate ids: none; links to missing ids: none; unknown source ids: none.
- Quotes that are not the full passage text: 0.
- Statements using "you": none.
- Capitalised words that are not keywords: none.
- Numbers not found in the sources: none.

## Hard cases

| Case | Reference statements | Paired | Clauses, modal and force agree | Not paired |
|---|---|---|---|---|
| condition only in a heading | 15 | 15 | 9 | - |
| condition only in a neighbouring passage | 2 | 2 | 2 | - |
| legal force set only by a heading | 3 | 3 | 0 | - |
| link between different passages | 3 | 3 | 3 | - |
| duty written apart from its penalty | 4 | 4 | 3 | - |
| sources on two pages | 6 | 6 | 4 | - |

Passages that should give no passing rule (m92 to m96) cited by the model: m95.

## Paired statements that disagree

| Reference | Model | Differs in | Reference text | Model text |
|---|---|---|---|---|
| 3.2.3b | m35b | links | EXCEPTION TO 3.2.3a: a driver MAY pass on the right WHEN the road is multi-lane OR the road is one-way OR the vehicle being passed is a streetcar OR the vehicle being passed is turning left | a driver MAY pass on the right WHEN the driver is on a multi-lane road OR the driver is on a one-way road OR the vehicle being passed is a streetcar OR the vehicle being passed is turning left |
| 3.1.6a | m23a | clauses | a driver MAY pass WHEN there is a broken line at the left of the driver's lane ONLY IF the way is clear AND there are [?enough] broken lines ahead to complete the pass [?safely] | a driver MAY pass WHEN there is a broken line at the left of the driver's lane AND the way is clear AND there are [?enough] broken lines ahead to complete the pass [?safely] |
| 3.5.2c | m83e | modal | a driver towing a trailer SHOULD NOT brake AND SHOULD steer the vehicle and trailer [?carefully] back into position WHEN a passing bus or truck pushes the trailer out of position | a driver towing a trailer SHOULD steer the vehicle and trailer back into position [?carefully] WHEN a passing bus or truck pushes the trailer out of position |
| 3.4.4e | m60b | clauses | a driver SHOULD tap the horn quickly and lightly while still [?some distance] away from the cyclist WHEN the driver feels the horn must be used | a driver SHOULD tap the horn quickly and lightly WHEN passing a cyclist AND the driver feels that the horn must be used WHILE the driver is still [?some distance] away from the cyclist |
| 3.4.4a | m55a | clauses | a cyclist MAY use any part of the lane WHEN this is [?necessary for safety], for example to discourage passing where the lane is too narrow to be shared [?safely] | a cyclist MAY use any part of the lane to discourage passing WHEN the lane is [?too narrow to be shared safely] ONLY IF using any part of the lane is [?necessary for safety] |
| 3.4.7a | m69b | modal | a driver SHOULD stay [?well back] of farm machinery AND SHOULD NOT pass it UNTIL it is [?safe] to do so | a driver SHOULD NOT pass farm machinery UNTIL it is [?safe to do so] |
| 3.6.1a | m84a | force, modal | a driver being passed SHOULD move to the right AND let the faster vehicle pass [?in safety] WHEN faster traffic wants to pass | a driver being passed MUST move to the right AND MUST let the passing vehicle pass [?in safety] WHEN faster traffic wants to pass the driver OR another driver is about to pass the driver |
| 3.2.3c | m37a | clauses | a driver SHOULD wait WHEN the driver is in the leftmost lane with a slower vehicle in front UNTIL the slower vehicle moves to the right | a driver in the leftmost lane SHOULD wait for the slower vehicle in front to move to the right WHEN a slower vehicle is in front of the driver |
| 3.2.1d | m31a | force, modal | a driver MUST keep to the right-hand lane WHEN a "keep right except to pass" sign is posted UNLESS the driver is passing on a two-lane section where a climbing or passing lane is provided | a driver SHOULD keep to the right-hand lane WHEN on a two-lane section of road where a passing lane or climbing lane is provided UNLESS the driver is passing |
| 3.4.11a | m76a | clauses | a driver SHOULD NOT pass a vehicle WHEN the vehicle is stopped at a crosswalk BECAUSE a stopped vehicle may mean a pedestrian is crossing | a driver SHOULD NOT pass a vehicle stopped at a crosswalk BECAUSE a stopped vehicle may be a clue that a pedestrian is crossing |
| 3.4.5b | m63a | force, modal, clauses | a driver SHOULD stay at least 2 m behind the rear doors of a streetcar WHEN the streetcar is stopped AND passengers are getting on or off | a driver MUST stay at least 2 m behind the rear doors of a streetcar WHEN the streetcar is stopped at a streetcar stop AND passengers are getting off or on UNLESS an area has been set aside for streetcar passengers at the stop |
| 3.5.1b | m82c | clauses | a driver towing a trailer SHOULD pass ONLY IF the driver has [?enough] time and room to complete the pass | a driver towing a trailer SHOULD make sure there is [?enough] time and room to complete the pass WHEN the driver is about to pass |
| 3.4.8a | m70b | modal, clauses | a driver SHOULD keep a [?safe] following distance behind a horse-drawn vehicle AND SHOULD NOT pass it UNLESS it is [?safe] to do so | a driver SHOULD pass a horse-drawn vehicle ONLY IF it is [?safe to do so] |
| 3.4.3b | c6a | clauses | a driver SHOULD NOT pull up beside a [?smaller vehicle] that is turning left ahead to make the turn at the same time WHEN the driver is also turning left, behind it | a driver turning left behind [?one of these vehicles] SHOULD NOT pull up beside the vehicle to turn at the same time |
| 3.5.1a | m82a | clauses | FACT a vehicle towing a trailer cannot accelerate as quickly AND needs more space BECAUSE it is much longer | FACT a vehicle cannot accelerate as quickly WHEN it is towing a trailer |
| 3.2.2b | m33a | clauses | a driver SHOULD use the far-left lane of a multi-lane freeway ONLY IF the driver is passing traffic that moves slower than the speed limit | a driver on a multi-lane freeway SHOULD use the far-left lane to pass traffic moving slower than the speed limit |
| 3.4.9a | m72a | clauses | a driver SHOULD NOT pass a snow plow WHEN the snow plow is moving | a driver SHOULD NOT pass a moving snow plow under any conditions |
| 3.5.2b | m83b | clauses | FACT fast-moving trucks and buses create a strong air disturbance behind them that can whip a trailer to the side WHEN they pass | FACT fast-moving trucks and buses create a strong air disturbance behind them |
| 3.6.1c | m86a | clauses | a driver MUST NOT drive to prevent another vehicle from passing IF VIOLATED [?sanctions for dangerous driving] | a driver of a motor vehicle MUST NOT drive the motor vehicle to prevent another vehicle from passing |
| 3.5.1c | m82e | modal, clauses | a driver towing a trailer SHOULD allow [?more room] before moving back into the lane AND SHOULD NOT cut back in [?too soon] WHEN returning to the lane after passing BECAUSE this can make the trailer sway and become hard to control | a driver towing a trailer SHOULD NOT cut back into the original lane [?too soon] BECAUSE cutting back [?too soon] can cause the trailer to sway and make the trailer difficult to control |
| 3.4.10a | m75a | clauses | a driver SHOULD NOT pass a pilot vehicle or pace vehicle WHEN it carries the "do not pass" temporary condition sign | a driver SHOULD NOT pass a pilot vehicle or pace vehicle bearing [?this sign] |
| 3.4.6c | m66b | clauses | FACT a large vehicle can create heavy air turbulence that may affect the driver's control WHILE passing it | FACT the air turbulence created by a large vehicle may affect a driver's ability to control the vehicle WHEN the driver is passing the large vehicle |
| 3.1.7a | m26a | force, modal | a driver MUST NOT pass WHEN a "do not pass" sign applies to the road | a driver SHOULD NOT pass WHEN on a road where a "do not pass" sign is posted |
| 3.4.2b | m51c | modal, clauses | a driver SHOULD NOT pass a motorcycle, bicycle, limited-speed motorcycle or moped within its lane BECAUSE its position in the lane is not an invitation to pass (3.4.2a) | a driver SHOULD change lanes to pass a motorcycle, bicycle, limited-speed motorcycle or moped |
| 3.4.13b | m79a | clauses | a driver MUST move into a lane away from the stopped emergency vehicle or tow truck, [?if safe to do so] WHEN the road has 2 or more lanes in the driver's direction IF VIOLATED 3 demerit points | a driver MUST move into a lane away from the emergency vehicle WHEN approaching an emergency vehicle that is stopped in the driver's direction of travel with red or red-and-blue lights flashing AND the road has 2 or more lanes in the driver's direction ONLY IF it is [?safe to do so] IF VIOLATED 3 demerit points |
| 3.4.2c | m51b | modal, clauses | a driver SHOULD change lanes WHEN passing a motorcycle, bicycle, limited-speed motorcycle or moped | a driver SHOULD NOT take a motorcycle, bicycle, limited-speed motorcycle or moped moving to the left or right side of its lane as an invitation to pass in the same lane |
| 2.2b | m12a | links | a driver SHOULD NOT cut off the vehicle being passed by moving in front of it suddenly WHEN returning to the original lane | a driver SHOULD NOT cut off a vehicle by suddenly moving in front of the vehicle WHEN passing |
| 3.2.1a | m28b | type, clauses | DEFINE a passing lane or climbing lane IS an added lane THAT lets slower vehicles move into the right-hand lane so faster vehicles can pass [?safely] in the left lane | FACT a passing or climbing lane lets slower vehicles move into the right-hand lane BECAUSE this lets faster vehicles pass [?safely] in the left lane |
| 3.4.3c | c7a | clauses | a driver SHOULD stay behind a [?smaller vehicle] that is turning left ahead WHEN the driver is also turning left, behind it UNTIL the way is [?clear] | a driver turning left behind [?one of these vehicles] SHOULD stay behind the vehicle UNTIL the way is clear for the turn |
| 2.1a | m4a | clauses | a driver SHOULD start a lane change or a pass ONLY IF the driver has [?enough] space and time to complete it [?safely] | a driver SHOULD make sure there is [?enough] space and time to complete the lane change or pass [?safely] WHEN the driver is about to change lanes OR the driver is about to pass another vehicle |
| 3.2.3a | m35a | clauses | a driver SHOULD pass on the left BECAUSE passing on the right can be more dangerous | a driver SHOULD pass on the left |
| 3.4.5d | m64b | clauses | a driver SHOULD pass a streetcar passenger area at a [?reasonable speed] AND SHOULD WATCH FOR pedestrians making sudden or unexpected moves | a driver SHOULD WATCH FOR pedestrians making sudden or unexpected moves WHEN passing a streetcar stop where an area has been set aside for streetcar passengers |
| 3.4.5c | m64a | type, force, modal, links | EXCEPTION TO 3.4.5b WHEN the streetcar stop has an area set aside for passengers | a driver SHOULD pass at a [?reasonable] speed WHEN passing a streetcar stop where an area has been set aside for streetcar passengers |

## Reference statements with no pair

- 1a (DEFINE, sources m1): DEFINE changing position IS a manoeuvre THAT changes lanes OR passes another vehicle
- 3.4.1a (RULE, sources m50): a driver SHOULD WATCH FOR doors opening suddenly AND doors opened to load or unload WHILE passing parked vehicles

## Model statements with no pair

- m3c (FACT, sources m3): FACT a driver following [?some] slow-moving vehicles may want to pass those vehicles
- m11a (RULE, sources m11, m8): a driver SHOULD change lanes WHEN passing ONLY IF the driver has first signalled
- m90b (FACT, sources m90): FACT the lane next to the far-left lane is the truck passing lane WHEN trucks are not allowed in the far-left lane
- m28a (FACT, sources m27, m28): FACT [?some] roads have special passing or climbing lanes
- m29a (FACT, sources m29): FACT an advance sign tells drivers that they will soon have a chance to pass WHEN a passing or climbing lane is ahead
- m36a (FACT, sources m36): FACT passing on the right can be more dangerous than passing on the left
- m95a (RULE, sources m95): a driver SHOULD wait for the emergency vehicle to pass AND SHOULD WATCH FOR other emergency vehicles that may be responding to the same call WHEN an emergency vehicle is approaching
- m78b (RULE, sources m78): a driver MUST slow down AND MUST proceed [?with caution] WHEN approaching a tow truck that is stopped in the driver's direction of travel with amber lights flashing
- m79b (RULE, sources m78, m79): a driver MUST move into a lane away from the tow truck WHEN approaching a tow truck that is stopped in the driver's direction of travel with amber lights flashing AND the road has 2 or more lanes in the driver's direction ONLY IF it is [?safe to do so]
- m73a (FACT, sources m73): FACT [?several] snow plows may be staggered across a freeway, clearing all lanes at the same time by passing a ridge of snow from plow to plow
- m33b (RULE, sources m33): a driver on a multi-lane freeway SHOULD NOT stay in the far-left lane
- m66a (FACT, sources m66): FACT a large vehicle can create heavy air turbulence, due to factors such as air pressure and airflow
- m69a (RULE, sources m69): a driver SHOULD stay [?well back] WHEN behind farm machinery
- m70a (RULE, sources m70): a driver SHOULD keep a [?safe] following distance WHEN behind a horse-drawn vehicle
- m68a (FACT, sources m67, m68): FACT the LCV placard on the rear of a vehicle indicates a long commercial vehicle
- m82b (FACT, sources m82): FACT a driver towing a trailer needs [?more space] BECAUSE the vehicle is much longer with a trailer attached
- m82d (RULE, sources m82): a driver towing a trailer SHOULD allow [?more room] WHEN the driver has passed AND the driver is about to move back into the original lane
- m83c (FACT, sources m83): FACT the wall of wind behind a large bus or truck that passes a vehicle towing a trailer may whip the trailer to the side, pushing the trailer out of control
- m83d (RULE, sources m83): a driver towing a trailer SHOULD NOT brake WHEN a passing bus or truck pushes the trailer out of position
- m83f (FACT, sources m83): FACT a slight increase in speed may help WHEN a passing bus or truck pushes a trailer out of position
