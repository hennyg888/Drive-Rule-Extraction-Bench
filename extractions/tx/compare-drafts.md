# Score: extractions/tx/output.json against analysis/passing-rules/tx/passing-rules.v1.json

## Summary

- Statements: model 104 (DEFINE 3, EXCEPTION 2, FACT 15, PROCEDURE 2, RULE 82); reference 65 (DEFINE 3, EXCEPTION 1, FACT 9, PROCEDURE 2, RULE 50).
- Paired by shared sources: 63. Reference recall 63/65 (97%); model precision 63/104 (61%).
- On paired statements: type 63/63 (100%), strength 62/63 (98%), modal 59/63 (94%), clause keywords 45/63 (71%), same sources 49/63 (78%), links 59/63 (94%).
- Law or advice on paired rules and procedures: 49/50 (98%).
- Inline flags (J, S, R, G) on paired statements: precision 0.74, recall 0.66, F1 0.70; same code on 29 of 29 matched spans.
- Passages the reference cites and the model does not: none.
- Passages the model cites and the reference does not: p117, p43, p44, p57, p58, p97.

## Validity

- Schema errors: 0
- Duplicate ids: none; links to missing ids: none; unknown source ids: none.
- Quotes that are not the full passage text: 0.
- Statements using "you": none.
- Capitalised words that are not keywords: none.
- Numbers not found in the sources: {'p102a': ['20']}.

## Paired statements that disagree

| Reference | Model | Differs in | Reference text | Model text |
|---|---|---|---|---|
| 3.4.17a | p124a | clauses | a driver SHOULD WATCH FOR the other driver drifting in front of the vehicle WHILE passing a driver who [?seems] to be distracted BECAUSE the distracted driver may not be aware of the passing vehicle | a driver SHOULD WATCH FOR the other driver drifting in front of the passing vehicle WHEN passing a driver who [?seems] to be distracted BECAUSE the other driver may not be aware of the passing driver |
| 3.4.12c | p14b | links | EXCEPTION TO 3.4.12a WHEN the school bus is on a different road OR (the driver is on a controlled-access highway AND the bus is stopped in a loading zone AND pedestrians are not permitted to cross) | EXCEPTION TO p10d WHEN the school bus is on a different road OR (the driver is on a controlled-access highway AND the school bus is stopped in a loading zone AND pedestrians are not permitted to cross) |
| 2.2a | p80a | clauses | TO pass a vehicle WHEN on a two-lane road | TO pass on a two-lane road |
| 3.4.6h | p114a | clauses | a driver being passed by a truck SHOULD keep to the far side of the lane BECAUSE this helps the truck driver | a driver being passed SHOULD keep to the far side of the driver's lane WHEN a truck is passing the driver BECAUSE this helps the truck driver |
| 2.1d | p77a | links | a driver SHOULD give the [?proper] signal WHEN about to change lanes to pass | a driver SHOULD give the [?proper] signal WHEN the driver is passing AND the driver is about to change lanes |
| 3.1.6a | p49b | clauses | a driver MAY cross a broken yellow center line WHEN on a two-lane road with two-way traffic AND (the driver is passing another vehicle OR the right half of the road is closed) ONLY IF it is [?safe] | a driver MAY cross the centreline WHEN driving on a two-lane rural road with two-way traffic AND the centreline is a broken line AND (the driver is passing another vehicle OR the right half of the road is closed) |
| 3.4.6m | p118d | clauses | a driver SHOULD either slow down and exit or stay behind the truck WHEN the driver and a truck are approaching a single-lane construction zone BECAUSE trying to beat a truck to a single-lane construction zone is particularly dangerous | a driver SHOULD either slow down and exit or stay behind the truck WHEN the driver is trying to reach an exit ahead of a truck OR the driver is trying to beat a truck to a single-lane construction zone |
| 2.1f | p79a | links | a driver SHOULD NOT cut in [?too quickly] WHEN returning to the original lane after passing | a driver SHOULD NOT cut in [?too quickly] WHEN the driver is passing AND the driver has to return to the original lane |
| 3.6.1e | p94a | clauses | a driver being passed SHOULD make it as [?safe and easy as possible] for the other driver to pass WHILE another vehicle is passing | a driver being passed SHOULD make the pass [?as safe and easy as possible] for the passing driver |
| 3.6.1g | p109a | clauses | a driver in any lane other than the right-hand lane SHOULD be prepared to move to another lane to allow faster traffic to pass WHEN driving on a highway | a driver in any lane except the right-hand lane used for [?slower traffic] SHOULD be prepared to move to another lane WHEN driving on a highway BECAUSE this allows faster traffic to pass |
| 3.4.6b | p111b | clauses | a truck driver being passed SHOULD stay to the far side of the lane BECAUSE this makes it easier for the other driver to pass | a truck driver SHOULD stay to the far side of the lane WHEN another vehicle is passing the truck BECAUSE this makes the pass easier for the passing driver |
| 3.6.1d | p92a | clauses | a driver being passed SHOULD stay in the driver's lane WHILE another vehicle is passing | a driver being passed SHOULD stay in the driver's own lane |
| 2.1b | p75b | modal, clauses | a driver SHOULD be patient AND wait WHEN the driver is about to pass UNTIL the time is [?right] BECAUSE it is not always [?safe] to pass | a driver SHOULD be patient AND SHOULD NOT pass UNTIL the time is [?right] |
| 3.4.6i | p114b | clauses | a driver being passed by a truck SHOULD [?slightly] reduce speed BECAUSE this makes it easier for the truck driver | a driver being passed SHOULD slow down [?slightly] WHEN a truck is passing the driver BECAUSE this makes the pass easier for the truck driver |
| 3.1.6b | p55b | clauses | a driver MAY pass or change lanes WHEN there are [?broken or dashed lines] ONLY IF it is [?safe] | a driver MAY pass or change lanes across a broken line ONLY IF it is [?safe] to do so |
| 3.4.4a | p125a | clauses | a cyclist moving slower than the other traffic MUST ride as near as [?possible] to the right curb or edge of the road UNLESS the cyclist is passing another vehicle proceeding in the same direction OR the cyclist is preparing for a left turn at an intersection or onto a private road or driveway OR there are [?unsafe conditions] in the road, such as fixed or moving objects, parked or moving vehicles, pedestrians, animals, potholes or debris, OR the cyclist is in an outside lane that is less than 14 ft wide and has no designated bicycle lane adjacent to it OR the lane is too narrow for a bicycle and a motor vehicle to travel [?safely] side by side | a cyclist MUST ride as near as [?possible] to the right curb or edge of the road WHEN the cyclist is moving slower than the other traffic on the road UNLESS the cyclist is passing another vehicle going in the same direction OR the cyclist is preparing for a left turn at an intersection or onto a private road or driveway OR there are [?unsafe] conditions in the road such as fixed or moving objects, parked or moving vehicles, pedestrians, animals, potholes or debris OR the cyclist is in an outside lane that is less than 14 ft wide and has no designated bicycle lane adjacent to that lane OR the cyclist is in an outside lane that is too narrow for a bicycle and a motor vehicle to travel [?safely] side by side |
| 3.4.13b | p102a | clauses | a driver MUST reduce speed to 20 mph below the speed limit or move out of the lane closest to the stopped vehicle, if the road has multiple lanes traveling in the same direction, WHEN an emergency medical vehicle, law enforcement vehicle, fire truck, tow truck, utility service vehicle, or TxDOT or other highway construction or maintenance vehicle is stopped on the road with its lights activated | a driver MUST move out of the lane closest to the stopped vehicle WHEN an emergency medical vehicle, law enforcement vehicle, fire truck, tow truck, utility service vehicle, Texas Department of Transportation (TxDOT) vehicle or other highway construction or maintenance vehicle is stopped on the road with its lights on or flashing AND the road has multiple lanes traveling in the same direction UNLESS the driver slows down to 20 mph below the speed limit |
| 2.1c | p76a | clauses | a driver SHOULD pass ONLY IF the way is [?clear] | a driver SHOULD make certain that the way is clear WHEN the driver is passing |
| 3.4.6l | p118a | clauses | a driver SHOULD NOT cut in front of a truck BECAUSE cutting into the open space in front of a truck or bus removes the truck or bus driver's cushion of safety | a driver SHOULD NOT cut in front of a truck |
| 2.3a | p95a | modal, clauses | a driver SHOULD NOT drive or linger in the other driver's blind spot AND SHOULD pass the other driver or slow down WHILE passing BECAUSE the other driver [?likely] cannot see the vehicle in or near the blind spot | a driver SHOULD NOT drive or linger in the other driver's blind spot WHEN the driver is passing |
| 2.1e | p78a | clauses, links | a driver SHOULD tap the horn WHEN passing AND this is [?necessary] to avoid surprising the driver ahead | a driver SHOULD tap the horn [?when necessary] WHEN the driver is passing BECAUSE this avoids surprising the driver in front |
| 3.1.3a | p31a | modal | a driver MUST keep right AND MUST NOT pass WHEN a warning sign for a reverse curve, sharp turn, gradual curve, reverse turn or sharp curve ahead is posted IF VIOLATED a misdemeanor punishable by a fine of $1 to $200 | a driver MUST NOT pass WHEN a warning sign shows that the road ahead makes a sharp turn to the right and then a sharp turn to the left IF VIOLATED a misdemeanor punishable by a fine of $1 to $200, doubled in a construction or maintenance work zone when workers are present anywhere in the zone |
| 3.1a | p66a | strength, modal | a driver SHOULD NOT drive [?on the left side of the road] WHEN pavement markings or signs prohibit driving on the left, such as a "no passing zone" or solid lane lines, OR there are 2 or more traffic lanes in each direction OR the driver is within 100 ft of or crossing an intersection or railroad crossing OR the driver is on a hill, curve or any other place where [?vision is limited] OR the driver is within 100 ft of a bridge, viaduct or tunnel | a driver MUST NOT [?drive on the left side of the road] WHEN pavement markings or signs prohibit driving on the left, such as a no-passing zone or solid lane lines |

## Reference statements with no pair

- 2.2b (RULE, sources p81): a driver SHOULD pass WHEN on a two-lane road ONLY IF the driver has [?enough] time and space to pass the vehicle ahead and return to the original lane before an approaching vehicle comes within 200 ft
- 3.4.6f (RULE, sources p112): a driver SHOULD complete the pass [?as quickly as possible] AND SHOULD NOT stay alongside the truck WHILE passing a truck

## Model statements with no pair

- p6a (RULE, sources p5, p6): a driver MUST vacate the lane closest to the emergency vehicle WHEN the driver is approaching a stopped emergency vehicle with its lights activated AND the highway has 2 or more lanes traveling in the direction of the emergency vehicle UNLESS a law enforcement officer directs otherwise
- p8a (RULE, sources p5, p8): a driver MUST slow down to a speed less than 5 mph WHEN the driver is approaching a stopped emergency vehicle with its lights activated AND the posted speed limit is less than 25 mph UNLESS a law enforcement officer directs otherwise
- p10a (RULE, sources p10): a driver MUST yield the right-of-way to a school bus
- p10b (RULE, sources p10): a driver SHOULD drive [?with care] WHEN the driver is [?near] a school bus
- p14a (EXCEPTION, sources p14): EXCEPTION TO p10c WHEN the school bus is on a different road OR (the driver is on a controlled-access highway AND the school bus is stopped in a loading zone AND pedestrians are not permitted to cross)
- p23a (RULE, sources p21, p22, p23, p62, p63): a driver MUST NOT pass WHEN a warning sign shows that the road curves one way (right) and then the other way (left) IF VIOLATED a misdemeanor punishable by a fine of $1 to $200, doubled in a construction or maintenance work zone when workers are present anywhere in the zone
- p25a (RULE, sources p21, p24, p25, p62, p63): a driver MUST NOT pass WHEN a warning sign shows that the road ahead makes a sharp turn in the direction of the arrow IF VIOLATED a misdemeanor punishable by a fine of $1 to $200, doubled in a construction or maintenance work zone when workers are present anywhere in the zone
- p29a (RULE, sources p21, p28, p29, p62, p63): a driver MUST NOT pass WHEN a warning sign shows that the road ahead makes a gradual curve in the direction of the arrow IF VIOLATED a misdemeanor punishable by a fine of $1 to $200, doubled in a construction or maintenance work zone when workers are present anywhere in the zone
- p35a (RULE, sources p21, p34, p35, p62, p63): a driver MUST NOT pass WHEN a warning sign shows that the road ahead curves sharply IF VIOLATED a misdemeanor punishable by a fine of $1 to $200, doubled in a construction or maintenance work zone when workers are present anywhere in the zone
- p44a (RULE, sources p36, p43, p44): a driver MUST NOT change lanes or turn [?across double white lines] WHEN a "do not cross double white line" sign applies
- p49a (RULE, sources p49, p50): a driver SHOULD keep to the right of the yellow centreline WHEN driving on a two-lane rural road with two-way traffic
- p57a (RULE, sources p57): a driver SHOULD NOT [?cross a solid white line] WHEN avoiding the crossing is [?possible]
- p57b (RULE, sources p57): a driver MUST NOT [?drive to the left of the solid yellow line on the left edge of the road]
- p58a (RULE, sources p58): a driver MUST NOT [?cross a pavement marking of double solid white lines]
- p67a (RULE, sources p64, p67): a driver SHOULD NOT [?drive on the left side of the road] WHEN there are 2 or more traffic lanes in each direction
- p68a (RULE, sources p142, p64, p68): a driver SHOULD NOT [?drive on the left side of the road] WHEN the driver is within 100 ft of an intersection or railway crossing OR the driver is crossing an intersection or railway crossing
- p69a (RULE, sources p64, p69): a driver SHOULD NOT [?drive on the left side of the road] WHEN the driver is on a hill OR the driver is on a curve OR the driver is at any other place where the view of oncoming traffic is obstructed
- p70a (RULE, sources p142, p64, p70): a driver SHOULD NOT [?drive on the left side of the road] WHEN the driver is within 100 ft of a bridge, viaduct or tunnel
- p75a (FACT, sources p75): FACT passing is not always [?safe]
- p91a (RULE, sources p91): a driver being passed SHOULD NOT speed up
- p95b (RULE, sources p95, p96): a driver SHOULD either pass the other driver or slow down WHEN the driver is passing AND the driver is in another driver's blind spot BECAUSE this keeps the driver out of the other driver's blind spot
- p95c (FACT, sources p95): FACT the other driver [?likely] cannot see a driver who is in or [?near] the other driver's blind spot
- p97a (RULE, sources p97): a driver SHOULD leave [?plenty of room] for others to pass WHEN the driver is parking, stopping or standing on a highway outside an urban area
- p101a (RULE, sources p100, p101): a driver MUST slow down to 20 mph below the speed limit WHEN an emergency medical vehicle, law enforcement vehicle, fire truck, tow truck, utility service vehicle, Texas Department of Transportation (TxDOT) vehicle or other highway construction or maintenance vehicle is stopped on the road with its lights on or flashing UNLESS the road has multiple lanes traveling in the same direction AND the driver moves out of the lane closest to the stopped vehicle
- p103b (RULE, sources p103): a driver SHOULD WATCH FOR vehicles stopped on the road
- p103d (RULE, sources p103): a driver MUST change lanes [?if possible] WHEN about to pass a mail, delivery or trash-collection vehicle that is stopped on the road
- p107a (RULE, sources p107): a driver SHOULD use the right-hand lane WHEN driving on a highway AND (the driver is driving at the minimum posted speed limit OR the driver is driving below the normal flow of traffic)
- p110a (RULE, sources p110): a driver SHOULD stay out of another driver's blind spot WHEN driving on a highway BECAUSE traveling where the driver in front cannot see the vehicle can be dangerous
- p110b (RULE, sources p110): a driver SHOULD either stay behind another vehicle or pass the other vehicle WHEN driving on a highway BECAUSE this keeps the driver out of the other driver's blind spot
- p110c (RULE, sources p110): a driver SHOULD NOT follow another vehicle to the side WHEN driving on a highway
- p116b (FACT, sources p116): FACT trucks make wide right turns and [?sometimes] leave an open space to the right just before the turn
- p117a (RULE, sources p117): a driver SHOULD NOT cross behind a truck WHEN the truck is preparing to back up
- p117b (RULE, sources p117): a driver SHOULD NOT pass a truck WHEN the truck driver is backing the truck from a road into a loading area UNTIL the truck has completed its maneuver BECAUSE the road is temporarily blocked
- p117c (FACT, sources p117): FACT a crash may occur WHEN a driver passes [?too closely] behind a truck that is backing BECAUSE the driver is in the truck's blind spot
- p118b (FACT, sources p118): FACT cutting into the open space in front of a truck or bus removes the truck or bus driver's cushion of safety
- p118c (FACT, sources p118): FACT trying to beat a truck to a single-lane construction zone is a particularly dangerous situation
- p119a (RULE, sources p119): a cyclist MUST ride as far to the right in the lane as [?possible] ONLY IF the lane can be shared [?safely] by a car and a bicycle side by side
- p120a (RULE, sources p119, p120): EXCEPTION TO p119a: a cyclist MAY take the full lane WHEN the cyclist is passing another vehicle going in the same direction
- p121a (RULE, sources p119, p121): EXCEPTION TO p119a: a cyclist MAY take the full lane WHEN the cyclist is preparing for a left turn at an intersection or onto a private road or driveway
- p122a (RULE, sources p119, p122): EXCEPTION TO p119a: a cyclist MAY take the full lane WHEN there are [?unsafe] conditions in the road, such as fixed or moving objects, parked or moving vehicles, pedestrians, animals, potholes or debris
- p123a (RULE, sources p119, p123): EXCEPTION TO p119a: a cyclist MAY take the full lane WHEN the lane is of substandard width, making it [?unsafe] for a car and a bicycle to share the lane side by side
