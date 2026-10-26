# Score: extractions/mto/output.json against analysis/passing-rules/mto/rules.json

## Summary

- Statements: model 102 (DEFINE 3, EXCEPTION 1, FACT 16, PROCEDURE 2, RULE 80); reference 88 (DEFINE 4, EXCEPTION 2, FACT 9, PROCEDURE 2, RULE 71).
- Paired by shared sources: 86. Reference recall 86/88 (98%); model precision 86/102 (84%).
- On paired statements: type 84/86 (98%), strength 83/86 (97%), modal 78/86 (91%), clause keywords 59/86 (69%), same sources 72/86 (84%), links 83/86 (97%).
- Law or advice on paired rules and procedures: 69/71 (97%).
- Inline flags (J, S, R, G) on paired statements: precision 0.76, recall 0.84, F1 0.80; same code on 41 of 42 matched spans.
- Passages the reference cites and the model does not: c7.
- Passages the model cites and the reference does not: m95, m96.

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
| condition only in a heading | 15 | 15 | 10 | - |
| condition only in a neighbouring passage | 2 | 2 | 2 | - |
| legal strength set only by a heading | 3 | 3 | 2 | - |
| link between different passages | 3 | 3 | 3 | - |
| duty written apart from its penalty | 4 | 4 | 3 | - |
| sources on two pages | 6 | 6 | 5 | - |

Passages that should give no passing rule (m92 to m96) cited by the model: m95, m96.

## Paired statements that disagree

| Reference | Model | Differs in | Reference text | Model text |
|---|---|---|---|---|
| 3.5.2c | m83d | modal | a driver towing a trailer SHOULD NOT brake AND SHOULD steer the vehicle and trailer [?carefully] back into position WHEN a passing bus or truck pushes the trailer out of position | a driver towing a trailer SHOULD steer the vehicle and trailer back into position [?carefully] WHEN a passing bus or truck pushes the trailer out of position |
| 3.4.4b | m56a | clauses | a driver of a motor vehicle MUST keep at least 1 m between the vehicle and a cyclist WHEN [?practical] WHILE passing the cyclist IF VIOLATED a fine AND 2 demerit points | a driver of a motor vehicle MUST keep a distance of at least 1 m between the motor vehicle and the cyclist [?where practical] WHILE passing a cyclist IF VIOLATED a fine AND 2 demerit points |
| 3.4.4e | m60b | clauses | a driver SHOULD tap the horn quickly and lightly while still [?some distance] away from the cyclist WHEN the driver feels the horn must be used | a driver SHOULD tap the horn quickly and lightly WHEN the driver is passing a cyclist AND the driver feels that the horn must be used WHILE the driver is still [?some distance] away from the cyclist |
| 3.4.7a | m69a | clauses | a driver SHOULD stay [?well back] of farm machinery AND SHOULD NOT pass it UNTIL it is [?safe] to do so | a driver SHOULD stay [?well back] AND SHOULD NOT pass WHEN behind farm machinery UNTIL [?it is safe to do so] |
| 3.4.9b | m73b | clauses | a driver SHOULD NOT pass between snow plows WHEN several snow plows are staggered across a freeway BECAUSE there is not [?enough] room to pass [?safely] AND the ridge of wet snow can throw the vehicle out of control | a driver on a freeway SHOULD NOT try to pass between snow plows that are staggered across the road BECAUSE there is not [?enough] room to pass [?safely] AND the ridge of wet snow can throw the vehicle out of control |
| 3.2.3b | m35b | links | EXCEPTION TO 3.2.3a: a driver MAY pass on the right WHEN the road is multi-lane OR the road is one-way OR the vehicle being passed is a streetcar OR the vehicle being passed is turning left | a driver MAY pass on the right WHEN the driver is on a multi-lane road OR the driver is on a one-way road OR the driver is passing a streetcar OR the driver is passing a vehicle that is turning left |
| 3.4.4a | m55a | clauses | a cyclist MAY use any part of the lane WHEN this is [?necessary for safety], for example to discourage passing where the lane is too narrow to be shared [?safely] | a cyclist MAY use any part of the lane to discourage passing WHEN the lane is [?too narrow to be shared safely] ONLY IF using any part of the lane is [?necessary for safety] |
| 3.5.1a | m82a | clauses | FACT a vehicle towing a trailer cannot accelerate as quickly AND needs more space BECAUSE it is much longer | FACT a driver towing a trailer cannot accelerate as quickly, and needs more space because the vehicle is much longer with a trailer attached |
| 3.4.1a | m50a | clauses | a driver SHOULD WATCH FOR doors opening suddenly AND doors opened to load or unload WHILE passing parked vehicles | a driver SHOULD WATCH FOR people suddenly opening doors or doors opened to load and unload WHEN the driver is passing parked vehicles |
| 3.4.11a | m76a | clauses | a driver SHOULD NOT pass a vehicle WHEN the vehicle is stopped at a crosswalk BECAUSE a stopped vehicle may mean a pedestrian is crossing | a driver SHOULD NOT pass a vehicle stopped at a crosswalk BECAUSE the stopped vehicle may be a clue that a pedestrian is crossing |
| 3.6.1b | m85a | clauses | a driver being passed MUST NOT speed up WHILE another driver is trying to pass BECAUSE it is dangerous | a driver being passed MUST NOT speed up WHEN another driver is trying to pass the driver BECAUSE speeding up is dangerous |
| 3.6.1a | m84a | strength, modal | a driver being passed SHOULD move to the right AND let the faster vehicle pass [?in safety] WHEN faster traffic wants to pass | a driver being passed MUST move to the right AND let the passing vehicle pass [?in safety] WHEN faster traffic wants to pass the driver OR another driver is about to pass the driver |
| 3.2.3c | m37a | clauses | a driver SHOULD wait WHEN the driver is in the leftmost lane with a slower vehicle in front UNTIL the slower vehicle moves to the right | a driver in the leftmost lane SHOULD wait for the slower vehicle in front to move to the right WHEN a slower vehicle is in front of the driver |
| 3.5.1b | m82b | clauses | a driver towing a trailer SHOULD pass ONLY IF the driver has [?enough] time and room to complete the pass | a driver towing a trailer SHOULD make [?sure] that the driver has [?enough] time and room to complete the pass WHEN the driver is about to pass |
| 3.4.8b | m71a | clauses | a driver SHOULD leave [?as much distance as possible] WHILE passing a horse-drawn vehicle BECAUSE passing too closely could startle the horse and make it change direction suddenly | a driver SHOULD leave [?as much distance as possible] between the driver's vehicle and the horse-drawn vehicle WHEN the driver is passing a horse-drawn vehicle BECAUSE passing [?too closely] could scare or startle the horse and cause the horse to change direction suddenly on the roadway |
| 3.4.5b | m63a | strength, modal, clauses | a driver SHOULD stay at least 2 m behind the rear doors of a streetcar WHEN the streetcar is stopped AND passengers are getting on or off | a driver MUST stay at least 2 m behind the rear doors of a streetcar where passengers are getting off or on WHEN the streetcar is stopped at a streetcar stop UNLESS an area has been set aside for streetcar passengers at the stop |
| 3.4.8a | m70a | modal, clauses | a driver SHOULD keep a [?safe] following distance behind a horse-drawn vehicle AND SHOULD NOT pass it UNLESS it is [?safe] to do so | a driver SHOULD pass a horse-drawn vehicle ONLY IF [?it is safe to do so] |
| 3.2.2b | m33a | clauses | a driver SHOULD use the far-left lane of a multi-lane freeway ONLY IF the driver is passing traffic that moves slower than the speed limit | a driver on a multi-lane freeway SHOULD use the far-left lane to pass traffic moving slower than the speed limit |
| 3.4.9a | m72a | clauses | a driver SHOULD NOT pass a snow plow WHEN the snow plow is moving | a driver SHOULD NOT pass a moving snow plow under any conditions |
| 3.6.1c | m86a | clauses | a driver MUST NOT drive to prevent another vehicle from passing IF VIOLATED [?sanctions for dangerous driving] | a driver of a motor vehicle MUST NOT drive the motor vehicle to prevent another vehicle from passing |
| 3.4.6c | m66a | clauses | FACT a large vehicle can create heavy air turbulence that may affect the driver's control WHILE passing it | FACT a large vehicle can create heavy air turbulence, due to factors such as air pressure and airflow, that may affect the ability of a driver to control the driver's vehicle WHEN the driver is passing the large vehicle |
| 3.5.1c | m82d | modal | a driver towing a trailer SHOULD allow [?more room] before moving back into the lane AND SHOULD NOT cut back in [?too soon] WHEN returning to the lane after passing BECAUSE this can make the trailer sway and become hard to control | a driver towing a trailer SHOULD NOT cut back into the original lane [?too soon] WHEN the driver has passed a vehicle BECAUSE cutting back in that way can cause the trailer to sway and make the trailer difficult to control |
| 3.2.1b | m29a | clauses | FACT an advance sign tells drivers a passing opportunity is coming, AND another sign warns when the added lane is ending | FACT an advance sign tells drivers that a chance to pass is coming soon WHEN a passing lane or climbing lane is ahead |
| 3.2.2c | m34a | clauses | a driver on a freeway SHOULD drive in the right-hand lane WHEN [?possible] BECAUSE this leaves the other lanes clear for passing | a driver on a freeway SHOULD drive in the right-hand lane BECAUSE this leaves the other lanes clear for passing |
| 3.4.2b | m51c | modal, clauses | a driver SHOULD NOT pass a motorcycle, bicycle, limited-speed motorcycle or moped within its lane BECAUSE its position in the lane is not an invitation to pass (3.4.2a) | a driver SHOULD pass a motorcycle, bicycle, limited-speed motorcycle or moped by changing lanes WHEN the driver wants to pass the motorcycle, bicycle, limited-speed motorcycle or moped |
| 3.4.2c | m51b | modal | a driver SHOULD change lanes WHEN passing a motorcycle, bicycle, limited-speed motorcycle or moped | a driver SHOULD NOT pass a motorcycle, bicycle, limited-speed motorcycle or moped in the same lane WHEN the motorcycle, bicycle, limited-speed motorcycle or moped has moved to the left or right side of its lane |
| 3.4.4c | m58a | clauses | a driver SHOULD change lanes to pass a cyclist WHEN [?possible] | a driver SHOULD change lanes to pass a cyclist [?whenever possible] |
| 3.4.3a | m53a | clauses | a driver SHOULD NOT pass a [?smaller vehicle] that is turning left ahead UNTIL it has moved to the right | a driver SHOULD NOT pass [?the smaller vehicle] WHEN the driver is making a left turn behind the smaller vehicle UNTIL the smaller vehicle has moved to the right |
| 2.2b | m12a | links | a driver SHOULD NOT cut off the vehicle being passed by moving in front of it suddenly WHEN returning to the original lane | a driver SHOULD NOT cut off a vehicle by suddenly moving in front of the vehicle WHEN the driver is passing |
| 3.2.3a | m35a | clauses | a driver SHOULD pass on the left BECAUSE passing on the right can be more dangerous | a driver SHOULD pass on the left |
| 2.1a | m4a | clauses | a driver SHOULD start a lane change or a pass ONLY IF the driver has [?enough] space and time to complete it [?safely] | a driver SHOULD be [?sure] that the driver has [?enough] space and time to complete the move [?safely] WHEN the driver is about to change lanes OR the driver is about to pass another vehicle |
| 3.4.5d | m64b | clauses | a driver SHOULD pass a streetcar passenger area at a [?reasonable speed] AND SHOULD WATCH FOR pedestrians making sudden or unexpected moves | a driver SHOULD WATCH FOR pedestrians making sudden or unexpected moves WHEN the driver is passing an area set aside for streetcar passengers |
| 1a | m1a | type | DEFINE changing position IS a manoeuvre THAT changes lanes OR passes another vehicle | FACT changing position on the road involves changing lanes or passing another vehicle |
| 3.4.5c | m64a | type, strength, modal, clauses, links | EXCEPTION TO 3.4.5b WHEN the streetcar stop has an area set aside for passengers | a driver SHOULD pass an area set aside for streetcar passengers at a [?reasonable] speed |

## Reference statements with no pair

- 3.4.3b (RULE, sources c6): a driver SHOULD NOT pull up beside a [?smaller vehicle] that is turning left ahead to make the turn at the same time WHEN the driver is also turning left, behind it
- 3.4.3c (RULE, sources c7): a driver SHOULD stay behind a [?smaller vehicle] that is turning left ahead WHEN the driver is also turning left, behind it UNTIL the way is [?clear]

## Model statements with no pair

- m3c (FACT, sources m3): FACT a driver may want to pass [?some] slow-moving vehicles WHEN the driver is following the slow-moving vehicles
- m90b (FACT, sources m90): FACT the lane next to the far-left lane is the truck passing lane WHEN trucks are not allowed in the far-left lane of a high-speed road with 3 or more lanes in each direction
- m28a (FACT, sources m28): FACT [?some] roads have passing lanes or climbing lanes
- m95a (RULE, sources m95): a driver SHOULD wait for the emergency vehicle to pass AND WATCH FOR other emergency vehicles that may be responding to the same call WHEN an emergency vehicle is approaching
- m78b (RULE, sources m78): a driver MUST slow down AND proceed [?with caution] WHEN the driver is approaching a tow truck that is stopped with amber lights flashing AND the tow truck is in the driver's direction of travel
- m79b (RULE, sources m78, m79): a driver MUST move into a lane away from the tow truck WHEN the driver is approaching a tow truck that is stopped with amber lights flashing AND the tow truck is in the driver's direction of travel AND the road has 2 or more lanes in the driver's direction of travel AND [?it is safe to do so]
- m7a (RULE, sources m7): a driver SHOULD keep to the right of the road UNLESS the driver wants to turn left OR the driver wants to pass another vehicle
- m73a (FACT, sources m73): FACT [?several] snow plows may be staggered across a freeway, clearing all lanes at the same time by passing a ridge of snow from plow to plow
- m33b (RULE, sources m33): a driver on a multi-lane freeway SHOULD NOT stay in the far-left lane
- m33c (RULE, sources m33): a driver on a multi-lane freeway SHOULD drive in the right-hand lane [?when possible]
- m91a (RULE, sources m91): a truck driver MUST NOT drive a large truck in the far-left lane WHEN the driver is on one of [?many] freeways with 3 or more lanes in each direction
- m96a (RULE, sources m96): a driver parked on the side of the road SHOULD look behind AND check the mirrors AND check the blind spot for a passing cyclist WHEN about to open a door
- m68b (FACT, sources m67, m68): FACT a rear placard showing a double trailer and the word "long" indicates a long commercial vehicle
- m82c (RULE, sources m82): a driver towing a trailer SHOULD allow [?more room] before moving back into the original lane WHEN the driver has passed a vehicle
- m83c (RULE, sources m83): a driver towing a trailer SHOULD NOT brake WHEN a passing bus or truck pushes the trailer out of position
- m83e (FACT, sources m83): FACT a slight increase in speed may help WHEN a passing bus or truck pushes a trailer out of position
