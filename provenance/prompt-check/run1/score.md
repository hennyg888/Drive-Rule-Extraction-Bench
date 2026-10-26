# Score: provenance/prompt-check/run1/output.json against analysis/passing-rules/mto/rules.json

## Summary

- Statements: model 104 (DEFINE 4, EXCEPTION 1, FACT 20, PROCEDURE 2, RULE 77); reference 88 (DEFINE 4, EXCEPTION 2, FACT 9, PROCEDURE 2, RULE 71).
- Paired by shared sources: 85. Reference recall 85/88 (97%); model precision 85/104 (82%).
- On paired statements: type 84/85 (99%), strength 83/85 (98%), modal 77/85 (91%), clause keywords 64/85 (75%), same sources 71/85 (84%), links 83/85 (98%).
- Law or advice on paired rules and procedures: 70/72 (97%).
- Inline flags (J, S, R, G) on paired statements: precision 0.78, recall 0.79, F1 0.79; same code on 41 of 42 matched spans.
- Passages the reference cites and the model does not: m50.
- Passages the model cites and the reference does not: none.

## Validity

- Schema errors: 0
- Duplicate ids: none; links to missing ids: none; unknown source ids: none.
- Quotes that are not the full passage text: 0.
- Statements using "you": none.
- Capitalised words that are not keywords: none.
- Numbers not found in the sources: none.

## Hard cases

| Case | Reference statements | Paired | Clauses, modal and strength agree | Not paired |
|---|---|---|---|---|
| condition only in a heading | 15 | 15 | 13 | - |
| condition only in a neighbouring passage | 2 | 2 | 2 | - |
| legal strength set only by a heading | 3 | 3 | 2 | - |
| link between different passages | 3 | 3 | 3 | - |
| duty written apart from its penalty | 4 | 4 | 3 | - |
| sources on two pages | 6 | 6 | 6 | - |

Passages that should give no passing rule (m92 to m96) cited by the model: none.

## Paired statements that disagree

| Reference | Model | Differs in | Reference text | Model text |
|---|---|---|---|---|
| 3.4.4b | m56a | clauses | a driver of a motor vehicle MUST keep at least 1 m between the vehicle and a cyclist WHEN [?practical] WHILE passing the cyclist IF VIOLATED a fine AND 2 demerit points | a driver of a motor vehicle MUST keep a distance of at least 1 m between the vehicle and the cyclist, [?where practical], WHILE passing a cyclist IF VIOLATED a fine AND 2 demerit points |
| 3.5.2c | m83e | modal | a driver towing a trailer SHOULD NOT brake AND SHOULD steer the vehicle and trailer [?carefully] back into position WHEN a passing bus or truck pushes the trailer out of position | a driver towing a trailer SHOULD steer the vehicle and trailer back into position [?carefully] WHEN a passing large bus or truck pushes the trailer out of position |
| 3.2.3b | m35b | links | EXCEPTION TO 3.2.3a: a driver MAY pass on the right WHEN the road is multi-lane OR the road is one-way OR the vehicle being passed is a streetcar OR the vehicle being passed is turning left | a driver MAY pass on the right WHEN the driver is on a multi-lane road OR the driver is on a one-way road OR the driver is passing a streetcar OR the driver is passing a vehicle that is turning left |
| 3.4.4a | m55a | clauses | a cyclist MAY use any part of the lane WHEN this is [?necessary for safety], for example to discourage passing where the lane is too narrow to be shared [?safely] | a cyclist MAY use any part of the lane to discourage passing WHEN the lane is [?too narrow to be shared safely] ONLY IF it is [?necessary for safety] |
| 3.1.5b | m21b | clauses | a driver SHOULD NOT pass WHEN there is a solid line at the left of the driver's lane BECAUSE a solid line there means it is unsafe to pass | a driver SHOULD NOT pass WHEN there is a solid line at the left of the driver's lane |
| 3.2.3c | m37a | clauses | a driver SHOULD wait WHEN the driver is in the leftmost lane with a slower vehicle in front UNTIL the slower vehicle moves to the right | a driver in the leftmost lane SHOULD wait for the vehicle in front to move to the right WHEN the vehicle in front is slower |
| 3.4.4e | m60b | clauses | a driver SHOULD tap the horn quickly and lightly while still [?some distance] away from the cyclist WHEN the driver feels the horn must be used | a driver SHOULD tap the horn quickly and lightly WHEN about to pass a cyclist AND the driver [?feels that the driver must use the horn] WHILE the driver is still [?some distance] away from the cyclist |
| 3.5.1b | m82c | clauses | a driver towing a trailer SHOULD pass ONLY IF the driver has [?enough] time and room to complete the pass | a driver towing a trailer SHOULD make sure the driver has [?enough] time and room to complete the pass WHEN about to pass |
| 3.4.11a | m76a | clauses | a driver SHOULD NOT pass a vehicle WHEN the vehicle is stopped at a crosswalk BECAUSE a stopped vehicle may mean a pedestrian is crossing | a driver SHOULD NOT pass a vehicle that is stopped at a crosswalk BECAUSE a stopped vehicle may be a clue that a pedestrian is crossing |
| 3.4.4d | m60a | clauses | a driver SHOULD NOT sound the horn [?unnecessarily] WHILE passing a cyclist BECAUSE it may frighten the cyclist and cause a loss of control | a driver SHOULD NOT sound the horn [?unnecessarily] WHEN passing a cyclist BECAUSE the horn may frighten the cyclist and cause the cyclist to lose control |
| 3.4.5b | m63a | strength, modal, clauses | a driver SHOULD stay at least 2 m behind the rear doors of a streetcar WHEN the streetcar is stopped AND passengers are getting on or off | a driver MUST stay at least 2 m behind the rear doors of a streetcar WHEN the streetcar is stopped at a streetcar stop AND passengers are getting off or on UNLESS an area has been set aside for streetcar passengers at the stop |
| 2.2b | m12a | links | a driver SHOULD NOT cut off the vehicle being passed by moving in front of it suddenly WHEN returning to the original lane | a driver SHOULD NOT cut off a vehicle by suddenly moving in front of the vehicle WHEN passing |
| 3.6.1c | m86a | clauses | a driver MUST NOT drive to prevent another vehicle from passing IF VIOLATED [?sanctions for dangerous driving] | a driver of a motor vehicle MUST NOT drive to prevent another vehicle from passing |
| 3.4.9a | m72a | clauses | a driver SHOULD NOT pass a snow plow WHEN the snow plow is moving | a driver SHOULD NOT pass a moving snow plow under any conditions |
| 3.5.1c | m82e | modal | a driver towing a trailer SHOULD allow [?more room] before moving back into the lane AND SHOULD NOT cut back in [?too soon] WHEN returning to the lane after passing BECAUSE this can make the trailer sway and become hard to control | a driver towing a trailer SHOULD NOT cut back into the original lane [?too soon] WHEN the driver has passed BECAUSE cutting back into the lane [?too soon] can cause the trailer to sway and become difficult to control |
| 3.4.6c | m66b | clauses | FACT a large vehicle can create heavy air turbulence that may affect the driver's control WHILE passing it | FACT the air turbulence created by a large vehicle may affect a driver's ability to control the vehicle WHEN the driver is passing the large vehicle |
| 3.4.10a | m75a | clauses | a driver SHOULD NOT pass a pilot vehicle or pace vehicle WHEN it carries the "do not pass" temporary condition sign | a driver SHOULD NOT pass a pilot vehicle or pace vehicle that bears [?this sign] |
| 3.4.8a | m70a | modal, clauses | a driver SHOULD keep a [?safe] following distance behind a horse-drawn vehicle AND SHOULD NOT pass it UNLESS it is [?safe] to do so | a driver SHOULD pass a horse-drawn vehicle ONLY IF it is [?safe] to pass |
| 3.2.2b | m33a | modal, clauses | a driver SHOULD use the far-left lane of a multi-lane freeway ONLY IF the driver is passing traffic that moves slower than the speed limit | a driver on a multi-lane freeway SHOULD use the far-left lane to pass traffic moving slower than the speed limit AND SHOULD NOT stay in the far-left lane |
| 3.5.2b | m83b | clauses | FACT fast-moving trucks and buses create a strong air disturbance behind them that can whip a trailer to the side WHEN they pass | FACT a strong air disturbance forms behind fast-moving trucks and buses |
| 3.2.2c | m34a | clauses | a driver on a freeway SHOULD drive in the right-hand lane WHEN [?possible] BECAUSE this leaves the other lanes clear for passing | a driver on a freeway SHOULD drive in the right-hand lane BECAUSE this leaves the other lanes clear for passing |
| 3.4.2c | m51b | modal | a driver SHOULD change lanes WHEN passing a motorcycle, bicycle, limited-speed motorcycle or moped | a driver SHOULD NOT pass a motorcycle, bicycle, limited-speed motorcycle or moped within the same lane WHEN the motorcycle, bicycle, limited-speed motorcycle or moped pulls to the left or right side of its lane |
| 3.4.2b | m51c | modal, clauses | a driver SHOULD NOT pass a motorcycle, bicycle, limited-speed motorcycle or moped within its lane BECAUSE its position in the lane is not an invitation to pass (3.4.2a) | a driver SHOULD change lanes WHEN about to pass a motorcycle, bicycle, limited-speed motorcycle or moped |
| 3.4.3a | m53a | clauses | a driver SHOULD NOT pass a [?smaller vehicle] that is turning left ahead UNTIL it has moved to the right | a driver SHOULD NOT pass [?the smaller vehicle] WHEN the driver is making a left turn behind [?the smaller vehicle] UNTIL [?the smaller vehicle] has moved to the right |
| 2.1a | m4a | clauses | a driver SHOULD start a lane change or a pass ONLY IF the driver has [?enough] space and time to complete it [?safely] | a driver SHOULD make sure the driver has [?enough] space and time to complete the pass [?safely] WHEN about to pass another vehicle |
| 3.2.3a | m36a | type, strength, modal, clauses | a driver SHOULD pass on the left BECAUSE passing on the right can be more dangerous | FACT passing on the right can be more dangerous than passing on the left |

## Reference statements with no pair

- 1a (DEFINE, sources m1): DEFINE changing position IS a manoeuvre THAT changes lanes OR passes another vehicle
- 3.4.1a (RULE, sources m50): a driver SHOULD WATCH FOR doors opening suddenly AND doors opened to load or unload WHILE passing parked vehicles
- 3.4.5c (EXCEPTION, sources m63): EXCEPTION TO 3.4.5b WHEN the streetcar stop has an area set aside for passengers

## Model statements with no pair

- m3c (FACT, sources m3): FACT a driver following [?some] slow-moving vehicles may want to pass the slow-moving vehicles
- m90b (DEFINE, sources m90): DEFINE the truck passing lane IS the lane THAT is next to the far-left lane on a high-speed road with 3 or more lanes in each direction where trucks are not allowed in the far-left lane
- m28a (FACT, sources m27, m28): FACT [?some] roads have special passing or climbing lanes
- m35a (FACT, sources m35): FACT [?most] passing is done on the left
- m78b (RULE, sources m78): a driver MUST slow down AND MUST proceed [?with caution] WHEN approaching a tow truck that is stopped in the driver's direction of travel with its amber lights flashing
- m79b (RULE, sources m78, m79): a driver MUST move into a lane away from the tow truck [?if safe to do so] WHEN the road has 2 or more lanes of traffic in the driver's direction of travel AND the driver is approaching a tow truck that is stopped with its amber lights flashing
- m7a (RULE, sources m7): a driver SHOULD keep to the right of the road UNLESS the driver wants to turn left OR the driver wants to pass another vehicle
- m73a (FACT, sources m73): FACT on freeways, [?several] snow plows may be staggered across the road, clearing all lanes at the same time by passing a ridge of snow from plow to plow
- m33b (RULE, sources m33): a driver on a freeway SHOULD drive in the right-hand lane WHEN it is [?possible]
- m91a (RULE, sources m91): a truck driver MUST NOT drive a large truck in the far-left lane WHEN the driver is on one of the [?many] freeways with 3 or more lanes in each direction that have this restriction
- m66a (FACT, sources m66): FACT a large vehicle can create heavy air turbulence BECAUSE of various factors such as air pressure and airflow
- m21a (FACT, sources m21, m22): FACT a solid line at the left of a driver's lane means it is [?unsafe] to pass
- m68a (FACT, sources m67, m68): FACT a "long" placard on the rear of a vehicle indicates a long commercial vehicle
- m88a (RULE, sources m87, m88): a driver being passed MUST move to the right AND MUST allow the passing vehicle to pass WHEN another driver is about to pass the driver
- m82a (FACT, sources m82): FACT a driver towing a trailer cannot accelerate as quickly as without a trailer
- m82d (RULE, sources m82): a driver towing a trailer SHOULD allow [?more room] WHEN the driver has passed AND the driver is about to move back into the original lane
- m83c (FACT, sources m83): FACT the wall of wind behind a large bus or truck that passes a driver towing a trailer may whip the trailer to the side, pushing the trailer out of control
- m83d (RULE, sources m83): a driver towing a trailer SHOULD NOT brake WHEN a passing large bus or truck pushes the trailer out of position
- m83f (FACT, sources m83): FACT a slight increase in speed may help a driver towing a trailer WHEN a passing large bus or truck pushes the trailer out of position
