# Score: extractions/ca/output.json against analysis/passing-rules/ca/passing-rules.v1.json

## Summary

- Statements: model 83 (DEFINE 3, EXCEPTION 1, FACT 9, PROCEDURE 4, RULE 66); reference 68 (DEFINE 4, EXCEPTION 1, FACT 4, PROCEDURE 1, RULE 58).
- Paired by shared sources: 66. Reference recall 66/68 (97%); model precision 66/83 (80%).
- On paired statements: type 62/66 (94%), strength 66/66 (100%), modal 59/66 (89%), clause keywords 47/66 (71%), same sources 57/66 (86%), links 66/66 (100%).
- Law or advice on paired rules and procedures: 57/57 (100%).
- Inline flags (J, S, R, G) on paired statements: precision 0.71, recall 0.71, F1 0.71; same code on 24 of 24 matched spans.
- Passages the reference cites and the model does not: none.
- Passages the model cites and the reference does not: p104, p63, p7, p91.

## Validity

- Schema errors: 0
- Duplicate ids: none; links to missing ids: none; unknown source ids: none.
- Quotes that are not the full passage text: 0.
- Statements using "you": none.
- Capitalised words that are not keywords: none.
- Numbers not found in the sources: none.

## Paired statements that disagree

| Reference | Model | Differs in | Reference text | Model text |
|---|---|---|---|---|
| 3.4.4b | p65a | clauses | a cyclist traveling slower than the flow of traffic MUST ride as close as [?possible] to the right curb or edge of the road UNLESS the cyclist is passing a vehicle or another bicycle in the same direction OR the cyclist is preparing to make a left turn OR the cyclist is avoiding a hazard or road condition OR the lane is too narrow for a bicycle and a vehicle to travel side by side in it [?safely] OR the cyclist is approaching a right turn OR the cyclist is on a one-way road with 2 or more lanes | a cyclist MUST ride as close as [?possible] to the right curb or edge of the road WHEN the cyclist is traveling slower than the flow of traffic UNLESS the cyclist is passing a vehicle or another bicycle going in the same direction OR the cyclist is preparing to make a left turn OR the cyclist is avoiding a hazard or road condition OR the lane is too narrow for a bicycle and a vehicle to travel [?safely] side by side in the lane OR the cyclist is approaching a right turn OR the cyclist is on a one-way road with 2 or more lanes |
| 3.4.4l | p84a | clauses | a driver SHOULD approach or pass a cyclist with [?extra care] WHEN on a two-lane road | a driver SHOULD approach or pass a cyclist on a two-lane road with [?extra care] |
| 3.4.4j | p79a | clauses | a driver SHOULD give a cyclist [?enough] space WHILE passing the cyclist BECAUSE this keeps the cyclist from being forced into parked vehicles or open vehicle doors | a driver SHOULD give a cyclist [?enough] space WHEN passing the cyclist BECAUSE this keeps the cyclist from being forced into parked vehicles or open vehicle doors |
| 3.4.11a | p46a | clauses | a driver SHOULD NOT pass a vehicle WHEN the vehicle is stopped at a crosswalk BECAUSE the driver may not be able to see a pedestrian crossing the street | a driver SHOULD NOT pass a vehicle stopped at a crosswalk BECAUSE the driver may not be able to see a pedestrian crossing the street |
| 3.1.5c | p2b | modal | a driver SHOULD NOT [?pass over] double solid yellow lines AND SHOULD stay to the right of them UNLESS the driver is in a high-occupancy vehicle (HOV) carpool lane that has a designated entrance on the left OR construction or other signs instruct the driver to drive on the other side of the road because the driver's side is closed or blocked OR the driver is turning left across a single set of double yellow lines to enter or exit a driveway or private road or to make a U-turn | a driver SHOULD keep to the right of double solid yellow lines UNLESS the driver is in a high-occupancy vehicle (HOV) carpool lane that has a designated entrance on the left OR construction or other signs instruct the driver to drive on the other side of the road because the driver's side is closed or blocked OR the driver is turning left across a single set of double yellow lines to enter or exit a driveway or private road or to make a U-turn |
| 3.4.13b | p87a | clauses | a driver MUST [?move over] AND slow down WHEN approaching a stopped road work vehicle displaying emergency flashing or amber warning lights | a driver MUST move over AND slow down for a stopped road work vehicle displaying emergency flashing or amber warning lights |
| 3.4.4h | p78a | clauses | a driver SHOULD allow at least 3 ft between the vehicle and the cyclist WHEN the driver cannot change lanes to pass a cyclist WHILE passing the cyclist BECAUSE this helps avoid putting the cyclist in danger | a driver SHOULD allow at least 3 ft between the driver's vehicle and the cyclist WHEN the driver is passing a cyclist AND the driver cannot change lanes BECAUSE this helps the driver avoid putting the cyclist in danger |
| 3.1.6a | p6a | clauses | a driver MAY pass WHEN a broken yellow line is next to the driver's lane ONLY IF it is [?safe] | a driver MAY pass WHEN a broken yellow line is next to the driver's lane |
| 3.4.14d | p52a | clauses | a driver MAY pass a bus, streetcar or trolley at no more than 10 mph WHEN the bus, streetcar or trolley is stopped at a safety zone or traffic light | a driver MAY pass a bus, streetcar or trolley WHEN the bus, streetcar or trolley is stopped at a safety zone or at a traffic light ONLY IF the driver's speed is at most 10 mph |
| 3.1.9a | p44a | clauses | a driver SHOULD NOT pass WHEN the driver is in a roundabout | a driver SHOULD NOT pass WHILE in a roundabout |
| 3.4.15c | p62a | clauses | a driver being passed by motorcyclists SHOULD move to one side of the lane to give the motorcyclists [?more room] to pass WHEN [?possible] | a driver SHOULD move to one side of the driver's lane WHEN it is [?possible] BECAUSE this gives motorcyclists [?more room] to pass |
| 3.4.4n | p103b | modal | a driver SHOULD slow down AND let the oncoming vehicle go by WHEN the driver is on a two-lane road with an oncoming vehicle to the left AND a cyclist ahead to the right | a driver SHOULD NOT drive between the oncoming vehicle and the cyclist AND SHOULD take one danger at a time WHEN the driver is on a two-lane road AND an oncoming vehicle is to the left AND a cyclist is ahead to the right |
| 2.1a | p9a | clauses | a driver SHOULD use the left lane to pass or to turn left WHEN choosing among traffic lanes | a driver SHOULD use the left lane to pass |
| 3.4.6d | p50c | clauses | a driver SHOULD move ahead of a large vehicle or truck WHEN the driver has passed it | a driver SHOULD move ahead of a large vehicle or truck WHEN the driver has passed the large vehicle or truck BECAUSE driving alongside a large vehicle makes it hard for the large vehicle's driver to avoid dangers in the road |
| 3.4.13a | p86a | clauses | a driver MUST [?move over] AND slow down WHEN approaching a stationary emergency vehicle or tow truck displaying flashing amber warning lights | a driver MUST move over AND slow down for a stationary emergency vehicle or tow truck displaying flashing amber warning lights |
| 3.4.10b | p101a | clauses | a driver SHOULD NOT pass the patrol vehicle WHILE a law enforcement traffic break is under way | a driver SHOULD NOT pass the patrol vehicle WHEN law enforcement is conducting a traffic break |
| 3.2.5c | p14a | clauses | a driver MUST use a turnout area or lane to let other vehicles pass WHEN the driver is driving [?slowly] on a two-lane road where passing is [?unsafe] AND 5 or more vehicles are following the driver | a driver MUST use a turnout area or lane WHEN the driver is driving [?slowly] on a two-lane road AND passing is [?unsafe] AND 5 or more vehicles are following the driver BECAUSE this lets the other vehicles pass |
| 3.4.4m | p103a | modal | a driver SHOULD NOT drive between the oncoming vehicle and the cyclist AND SHOULD take one danger at a time WHEN the driver is on a two-lane road with an oncoming vehicle to the left AND a cyclist ahead to the right | a driver SHOULD give [?more space] to the most dangerous situation WHEN dangers are on both sides of the road AND one danger is [?greater] than the other |
| 3.1.3a | p19b | modal, clauses | a driver SHOULD pass WHEN approaching a hill or curve ONLY IF the hill or curve is at least 1/3 mi ahead BECAUSE this distance is needed to pass [?safely] | a driver SHOULD NOT pass WHEN approaching a hill or a curve UNLESS the hill or curve is at least 1/3 mi ahead BECAUSE that distance is needed to pass [?safely] |
| 3.2.5b | p12b | clauses | a driver SHOULD merge into a turnout area or lane to allow the vehicles behind to pass WHEN on a two-lane road that has turnout areas or lanes | a driver on a two-lane road with a turnout area or lane SHOULD merge into the turnout area or lane BECAUSE this lets vehicles behind the driver pass |
| 3.4.4o | p103c | type, modal | a driver SHOULD move to the left to allow [?plenty of space], at least 3 ft, to pass the cyclist WHEN the driver is on a two-lane road with an oncoming vehicle to the left AND a cyclist ahead to the right AND the oncoming vehicle has gone by | TO pass a cyclist WHEN the driver is on a two-lane road AND an oncoming vehicle is to the left AND the cyclist is ahead to the right |
| 3.2.3a | p33a | clauses | a driver MAY pass on the right ONLY IF an open highway has 2 or more lanes going in the driver's direction OR (the driver ahead is turning left AND the driver can pass on the right [?safely]) OR the driver is on a one-way street | a driver MAY pass on the right WHEN the driver is on an open highway with 2 or more lanes going in the driver's direction |
| 3.6.1e | p94a | type, modal | a driver SHOULD keep the course and speed WHEN a tailgater is behind the driver | TO deal with a tailgater WHEN a tailgater is behind the driver |
| 3.4.10a | p99a | type | DEFINE a traffic break IS a law enforcement maneuver THAT has an officer turn on the emergency lights and slowly weave across lanes | FACT during a traffic break, the officer turns on the emergency lights and slowly weaves across lanes |
| 3.4.4f | p73b | type, modal, clauses | a driver SHOULD pass the cyclist [?safely] AND SHOULD then return to the original lane WHEN the driver has changed lanes to pass a cyclist in the travel lane | TO pass a cyclist who is in the travel lane by changing lanes |

## Reference statements with no pair

- 3.4.4p (RULE, sources p103): a driver SHOULD use as much of the left lane as the driver [?safely] can to pass the cyclist WHEN the driver is on a two-lane road with a cyclist ahead to the right AND there is a steady flow of oncoming vehicles
- 3.6.1f (RULE, sources p95): a driver SHOULD merge right into another lane AND allow the tailgater to pass WHEN a tailgater is behind the driver AND it is [?safe] to do so

## Model statements with no pair

- p2a (RULE, sources p2): a driver SHOULD NOT [?pass over] double solid yellow lines
- p6b (RULE, sources p6): a driver SHOULD NOT pass WHEN a broken yellow line is next to the driver's lane UNLESS passing is [?safe]
- p7a (FACT, sources p7): FACT double solid white lines indicate a lane barrier between a regular use lane and a preferential use lane, such as a carpool (HOV) lane
- p7b (FACT, sources p7): FACT double solid white lines can also be found in or [?near] freeway on and off ramps
- p7c (RULE, sources p7): a driver SHOULD NOT [?change lanes] WHEN double solid white lines separate the driver's lane from the next lane UNTIL the driver sees a single broken white line
- p13a (RULE, sources p13): a driver of a slower vehicle SHOULD use a turnout WHEN a "slower traffic use turnouts" sign applies
- p34a (RULE, sources p32, p34): a driver MAY pass on the right WHEN the driver in front is turning left AND the driver can pass on the right [?safely]
- p35a (RULE, sources p32, p35): a driver MAY pass on the right WHEN the driver is on a one-way road
- p37a (RULE, sources p37): a driver being passed SHOULD allow the other vehicle to pass WHEN another vehicle is passing the driver OR another vehicle signals that it plans to pass the driver
- p54a (FACT, sources p53, p54): FACT safety zones are marked by dotted white lines
- p63a (RULE, sources p63): a driver SHOULD drive to the right edge of the road AND stop WHEN a law enforcement vehicle, fire engine, ambulance or other emergency vehicle is using a siren and red lights UNTIL the emergency vehicle has passed IF VIOLATED a possible ticket
- p64a (RULE, sources p64): a driver SHOULD move over AND slow down WHEN approaching a stationary emergency vehicle with flashing emergency signal lights (hazard lights)
- p90a (RULE, sources p89, p90): a driver MUST stop for a school bus
- p92b (RULE, sources p92): a driver SHOULD remain stopped WHILE the red lights of a school bus are flashing
- p102a (FACT, sources p102): FACT dangers are [?sometimes] on both sides of the road at the same time, such as parked cars to the right and oncoming cars to the left
- p104a (RULE, sources p104): a driver SHOULD slow down WHEN the driver sees a vehicle's emergency flashers ahead BECAUSE there may be a collision or other road emergency
- p104b (RULE, sources p104): a driver SHOULD pass [?carefully] WHEN the driver sees a vehicle's emergency flashers ahead
