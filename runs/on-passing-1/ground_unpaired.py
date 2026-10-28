"""Hand grounding of the on-passing-1 flags and provisions on statements with no pair in the reviewed set.
Run once from the repo root after runs/on-passing-1/ground_paired.py; kept as the record of the hand grounding.
Each flag either takes the grounding of a named reviewed flag ("same") or gets its own."""
import sys
sys.path.insert(0, 'tools')
import db as dbtool  # noqa: E402

db = dbtool.connect()
q = lambda s, *a: db.execute(s, a).fetchall()  # noqa: E731
R = 'on-passing-1:'
S = 'mto:sent:'

# Provisions not yet in the database, copied word for word from the local copies, history notes left out.
NEW_UNITS = [
    ('on-hta:1(1)median-strip', 'on-hta', 's. 1 (1), "median strip"', 'Definitions', None, None,
     '“median strip” means the portion of a highway so constructed as to separate traffic travelling in one direction from '
     'traffic travelling in the opposite direction by a physical barrier or a raised or depressed paved or unpaved separation '
     'area that is not intended to allow crossing vehicular movement;'),
    ('on-hta:142.1(1)', 'on-hta', 's. 142.1 (1)', 'Requirement to yield to bus from bus bay', None, None,
     '142.1 (1) Every driver of a vehicle in the lane of traffic adjacent to a bus bay shall yield the right of way to the '
     'driver of a bus who has indicated his or her intention, as prescribed, to re-enter that lane from the bus bay.'),
    ('on-hta:159(1)', 'on-hta', 's. 159 (1)', 'Stop on approach of vehicle with flashing lights or bell or siren sounding',
     None, '2027-01-01',
     '159 (1) The driver of a vehicle, upon the approach of an emergency vehicle mentioned in clause (a) of the definition of '
     'that term, with its bell or siren sounding or with its lamp producing intermittent flashes of red light or red and blue '
     'light, or upon the approach of a public utility emergency vehicle with its bell or siren sounding or its lamp producing '
     'intermittent flashes of red light, shall immediately bring such vehicle to a standstill, (a) as near as is practicable '
     'to the right-hand curb or edge of the roadway and parallel therewith and clear of any intersection; or (b) when on a '
     'roadway having more than two lanes for traffic and designated for the use of one-way traffic, as near as is practicable '
     'to the nearest curb or edge of the roadway and parallel therewith and clear of any intersection.'),
    ('on-hta:159(1)@2027', 'on-hta', 's. 159 (1), in force January 1, 2027',
     'Stop on approach of vehicle with flashing lights or bell or siren sounding', '2027-01-01', None,
     '159 (1) The driver of a vehicle, upon the approach of a vehicle mentioned in clause (a) of the definition of “emergency '
     'vehicle”, with its bell or siren sounding or with its lamp producing intermittent flashes of red light or red and blue '
     'light, or upon the approach of a public utility emergency vehicle with its bell or siren sounding or its lamp producing '
     'intermittent flashes of red light, shall immediately bring such vehicle to a standstill, (a) as near as is practicable '
     'to the right-hand curb or edge of the roadway and parallel therewith and clear of any intersection; or (b) when on a '
     'roadway having more than two lanes for traffic and designated for the use of one-way traffic, as near as is practicable '
     'to the nearest curb or edge of the roadway and parallel therewith and clear of any intersection.'),
    ('on-hta:175(6)', 'on-hta', 's. 175 (6)', 'School bus driver, signals', None, None,
     '(6) Subject to subsection (9), every school bus driver, (a) who is about to stop on a highway for the purpose of '
     'receiving or discharging children or receiving or discharging adults who have developmental disabilities, shall actuate '
     'the overhead signal-lights on the bus; (b) as soon as the bus is stopped for a purpose set out in clause (a), shall '
     'actuate the school bus stop arm; and (c) while the bus is stopped for a purpose set out in clause (a) on a highway, shall '
     'continue to operate the overhead signal-lights and stop arm until the passengers have been received or discharged and '
     'until all passengers having to cross the highway have completed the crossing.'),
    ('on-hta:175(13)', 'on-hta', 's. 175 (13)', 'Designating school bus loading zones', None, None,
     '(13) A council of a municipality may by by-law designate school bus loading zones, in accordance with the regulations, '
     'on highways under its jurisdiction and, where it does so, subsection (6) does not apply to a driver about to stop or '
     'stopping in a zone so designated.'),
    ('on-hta:207(1)', 'on-hta', 's. 207 (1)', 'Vehicle owner may be convicted', None, None,
     '207 (1) Subject to subsection (2), the owner of a vehicle may be charged with and convicted of an offence under this Act '
     'or the regulations or any municipal by-law regulating traffic for which the driver of the vehicle is subject to be '
     'charged unless, at the time of the offence, the vehicle was in the possession of some person other than the owner '
     'without the owner’s consent and on conviction the owner is liable to the penalty prescribed for the offence.'),
    ('on-hta:207(7)', 'on-hta', 's. 207 (7)', 'Limitation', None, None,
     '(7) An owner of a motor vehicle convicted of an offence under subsection 175 (19), (19.1), (20) or (20.1) is not liable '
     'to imprisonment, a probation order under subsection 72 (1) of the Provincial Offences Act or a driver’s licence '
     'suspension as a result of that conviction or as a result of default in payment of a fine resulting from that conviction.'),
    ('on-hta:214(1)', 'on-hta', 's. 214 (1)', 'General penalty', None, None,
     '214 (1) Every person who contravenes this Act or any regulation is guilty of an offence and on conviction, where a '
     'penalty for the contravention is not otherwise provided for herein, is liable to a fine of not less than $60 and not '
     'more than $1,000.'),
    ('on-reg-339-94:item-35', 'on-reg-339-94', 'Table, item 35', 'Failing to stop on right for emergency vehicle', None, None,
     '35 | Clause 159 (1) (a) of the Highway Traffic Act | 3 | Failing to stop on right for emergency vehicle'),
    ('on-reg-339-94:item-36', 'on-reg-339-94', 'Table, item 36', 'Failing to stop – nearest curb – for emergency vehicle',
     None, None, '36 | Clause 159 (1) (b) of the Highway Traffic Act | 3 | Failing to stop – nearest curb – for emergency vehicle'),
    ('on-reg-339-94:item-36.1', 'on-reg-339-94', 'Table, item 36.1',
     'Failing to stop – nearest edge of roadway – for emergency vehicle', None, None,
     '36.1 | Clause 159 (1) (b) of the Highway Traffic Act | 3 | Failing to stop – nearest edge of roadway – for emergency vehicle'),
]

KEEP_RIGHT = dict(status='LAW_STATES',
                  definition='Only a vehicle travelling at less than the normal speed of traffic must keep to the right-hand lane, '
                             'or as close as practicable to the right edge, where practicable (147 (1)).',
                  effect='None; the statement is already about slower drivers. The Act makes it a duty.',
                  links=[('on-hta:147(1)', 'law')])
SAME_PASSAGES = lambda *sents, note=None: dict(status='HANDBOOK', definition=None, note=note,  # noqa: E731
                                               effect='None; the passages give the same advice.',
                                               links=[(S + s, 'handbook') for s in sents])
OVERHEAD = dict(status='LAW_DEFINES', definition='The Act\'s term is "overhead red signal-lights" (175 (11), (12)).',
                effect='None; the handbook wordings name the same lights.', links=[('on-hta:175(11)', 'law'), ('on-hta:175(12)', 'law')])
PASS_WORD = dict(status='LAW_REPEATS', definition=None, effect='None; read it as passing.',
                 note='The Act uses "pass" (148 (8)), "overtake" (148 (2)) and "overtake and pass" (150 (1)) and defines none of them.',
                 links=[('on-hta:148(2)', 'law'), ('on-hta:148(8)', 'law'), ('on-hta:150(1)', 'law')])
DESCRIBES = lambda what: dict(status='OPEN', note=f'A description, not a duty; no source says {what}.')  # noqa: E731
WAIT = ('Wait until the bus moves, or until every signal that was on has stopped: the red lights have stopped flashing and '
        'the stop arm is no longer actuated.')
WAIT_LINKS = [(S + 'sharing-road-other-road-users:081.1', 'handbook'), (S + 'stopping:023.4', 'handbook'),
              (S + 'stopping:028.3', 'handbook'), ('on-hta:175(11)', 'law'), ('on-hta:175(11.1)', 'law')]
STANDSTILL = [('on-hta:159(1)', 'law'), ('on-hta:159(1)@2027', 'law')]

SPEC = {
    ('p6b', 'X', 'especially important if you are driving more slowly than other vehicles'): KEEP_RIGHT,
    ('p23a', 'J', 'heavy'): 'mto:3.4.12b|J|heavy',
    ('p23a', 'V', 'overhead red lights'): OVERHEAD,
    ('p23a', 'X', 'You must stop whenever you approach a stopped school bus with its upper alternating red lights flashing'): dict(
        status='LAW_STATES', definition='A stopped bus with its stop arm actuated is a reason to stop on its own (175 (11.1), (12.1)).',
        effect='None; the statement names both signals, as the Act does. p28 and p34 name only the red lights.',
        links=[(S + 'stopping:023.1', 'handbook'), (S + 'stopping:029.1', 'handbook'),
               ('on-hta:175(11.1)', 'law'), ('on-hta:175(12.1)', 'law')]),
    ('p24a', 'X', 'only vehicles coming from behind the bus must stop'): dict(
        status='LAW_STATES', definition='Meeting the bus from the front, the duty does not apply on a highway with a median strip '
                                        '(175 (11), (11.1)); from the rear it always applies (175 (12), (12.1)).',
        effect='None; both passages give the Act\'s exception.',
        links=[(S + 'sharing-road-other-road-users:079.1', 'handbook'), (S + 'stopping:026.1', 'handbook'),
               ('on-hta:175(11)', 'law'), ('on-hta:175(11.1)', 'law')]),
    ('p26a', 'M', 'Do not proceed on your route'): 'mto:3.4.12d|M|Do not go',
    ('p26a', 'X', 'until the bus moves, the overhead red lights have stopped flashing and its stop arm is no longer activated'): dict(
        status='LAW_STATES', definition=WAIT,
        effect='The statement waits for the bus to move and every signal to stop; the Act lets the driver go at either point.',
        links=WAIT_LINKS),
    ('p26a', 'V', 'overhead red lights'): OVERHEAD,
    ('p33a', 'V', 'stop sign arm'): dict(
        status='LAW_DEFINES', definition='The Act says "stop arm" (175 (6), (11.1), (12.1)).',
        effect='None; both handbook wordings name the same arm.',
        links=[('on-hta:175(6)', 'law'), ('on-hta:175(11.1)', 'law'), ('on-hta:175(12.1)', 'law')]),
    ('p33b', 'M', 'Remain stopped'): 'mto:3.4.12d|M|Do not go',
    ('p33b', 'X', 'until the arm folds away and all lights stop flashing'): dict(
        status='LAW_STATES', definition=WAIT,
        effect='The statement leaves out the bus moving; the Act also lets the driver go once the bus moves.', links=WAIT_LINKS),
    ('p41b', 'V', 'overtake'): 'mto:1b|V|overtaking',
    ('p42a', 'S', 'often'): DESCRIBES('when waiting is not safer'),
    ('p42a', 'V', 'going around it'): PASS_WORD,
    ('p43d', 'S', 'some'): DESCRIBES('which slow-moving vehicles'),
    ('p54a', 'J', 'in safety'): 'mto:3.6.1a|J|in safety',
    ('p54a', 'X', 'move to the right and let it pass in safety'): 'mto:3.6.1a|M|move to the right',
    ('p62a', 'S', 'some'): DESCRIBES('which roads'),
    ('p74b', 'J', 'possible'): 'mto:3.2.2c|J|possible',
    ('p74c', 'S', 'many'): 'mto:3.6.3a|S|many high-speed roads',
    ('p74c', 'X', 'must use the lane to the right for passing'): dict(
        status='LAW_STATES', definition='The regulation bars a commercial motor vehicle over 6.5 m from the left lane of the highway '
                                        'portions in its Schedules (Reg. 608, 1 (1)); that trucks pass in the next lane is the handbook\'s reading.',
        effect='None; both passages give the same reading.',
        links=[(S + 'changing-positions:024.2', 'handbook'), ('on-reg-608:1(1)', 'law')]),
    ('p75a', 'J', 'with caution'): dict(
        status='OPEN', note='No provision covers these workers and vehicles today. From January 1, 2027, 159 (2) also covers a stopped '
                            '"work-related vehicle" with amber flashing lamps and uses the same word, "caution"; which vehicles count is '
                            'left to a regulation (159 (12)) that was not pulled.',
        links=[('on-hta:159(2)@2027', 'law')]),
    ('p75b', 'J', 'safe to do so'): dict(
        status='OPEN', note='From January 1, 2027, 159 (3) asks a driver to move over for a stopped "work-related vehicle" "if the '
                            'movement can be made safely"; which vehicles count is left to a regulation that was not pulled.',
        links=[('on-hta:159(3)@2027', 'law')]),
    ('p76a', 'J', 'safe to do so'): dict(
        status='OPEN', note='The Act requires a standstill clear of any intersection (159 (1)) and gives no test for when clearing it is safe.',
        links=[('on-hta:159(1)', 'law')]),
    ('p77a', 'X', 'Check to make sure the way is clear and signal before merging back into traffic.'): SAME_PASSAGES(
        'dealing-particular-situations:084.1', 'dealing-particular-situations:091.2'),
    ('p77b', 'X', 'watch for other emergency vehicles that may be responding to the same call'): SAME_PASSAGES(
        'dealing-particular-situations:084.2', 'dealing-particular-situations:091.1'),
    ('p83b', 'J', 'too fast'): dict(status='OPEN', note='No speed is given.'),
    ('p83b', 'J', 'well in advance'): dict(
        status='OPEN', note='No distance is given; the Act asks only that the move be made safely (159 (3)).',
        links=[('on-hta:159(3)', 'law')]),
    ('p83b', 'J', 'safe to do so'): 'mto:3.4.13b|J|if safe to do so',
    ('p84a', 'J', 'excessively'): dict(
        status='OPEN', note='No measure; the Act asks only for slowing down and proceeding with caution (159 (2)).',
        links=[('on-hta:159(2)', 'law')]),
    ('p86a', 'J', 'with caution'): dict(
        status='LAW_STATES', definition='Bring the vehicle to a standstill at once, as near as practicable to the right-hand curb or '
                                        'edge, parallel to it and clear of any intersection (159 (1)).',
        effect='Replace "proceed with caution, clear the way and stop" with the standstill; the Act does not say caution here.',
        links=STANDSTILL),
    ('p86a', 'R', 'where required'): dict(
        status='LAW_DEFINES', definition='Always, when an ambulance, fire, police or ministry vehicle, or a public utility emergency '
                                         'vehicle, approaches with its bell or siren sounding or its lamp flashing red (or red and blue): '
                                         'near the right-hand curb, or the nearest curb on a one-way road with more than two lanes, '
                                         'clear of any intersection (159 (1)).',
        effect='Replace "where required" with the Act\'s conditions.', links=STANDSTILL),
    ('p87a', 'R', 'above law'): dict(
        status='LAW_DEFINES', definition='For a stopped tow truck with amber flashing lamps the duties are to slow down and proceed with '
                                         'caution (159 (2)) and to move over (159 (3)); the duty to stop for an approaching vehicle '
                                         '(159 (1)) does not cover tow trucks.',
        effect='Read "the above law" as the slow-down and move-over duties (p81, p83), not p86.',
        links=[('on-hta:159(1)', 'law'), ('on-hta:159(2)', 'law'), ('on-hta:159(3)', 'law')]),
    ('p95b', 'S', 'some'): DESCRIBES('which snow plows'),
    ('p95c', 'S', 'several'): dict(
        status='LAW_DEFINES', definition='Two or more plows travelling in echelon (148.1 (1)).', effect='Could say two or more.',
        links=[('on-hta:148.1(1)', 'law')]),
    ('p100a', 'X', 'Stop for school bus when signals are flashing.'): dict(
        status='LAW_STATES', definition='The duty to stop applies on every highway whether or not the sign is posted (175 (11) to (12.1)); '
                                        'the sign is a reminder.',
        effect='Drop "the sign is posted" from the condition.',
        links=[(S + 'stopping:023.1', 'handbook'), ('on-hta:175(11)', 'law'), ('on-hta:175(11.1)', 'law'),
               ('on-hta:175(12)', 'law'), ('on-hta:175(12.1)', 'law')]),
    ('p102b', 'V', 'centre median divider'): dict(
        status='LAW_DEFINES', definition='The Act says "median strip": a part of the highway built to separate traffic travelling in '
                                         'opposite directions by a physical barrier or a raised or depressed separation area not meant '
                                         'to be crossed (s. 1 (1)).',
        effect='None; "centre median divider" and "median strip" name the same thing.',
        links=[('on-hta:1(1)median-strip', 'law'), ('on-hta:175(11)', 'law')]),
    ('p108a', 'V', 'red alternating lights'): OVERHEAD,
    ('p124d', 'J', 'more room'): 'mto:3.5.1c|J|more room',
    ('p125e', 'J', 'slight'): dict(status='OPEN', note='No amount is given, and no source gives one.'),
    ('p131a', 'J', 'enough'): dict(
        status='HANDBOOK', definition='Enough to see the rear wheels of the vehicle in front, or to pull around it without backing up '
                                      '(Level Two road test).',
        effect='Could replace "enough space" with the rear-wheels test.',
        links=[(S + 'level-two-road-test:107.5', 'handbook'), (S + 'level-two-road-test:114.4', 'handbook')]),
    ('p131a', 'X', 'When stopped behind another vehicle at the intersection, leave enough space to pull out and pass without having to back up.'):
        SAME_PASSAGES('level-two-road-test:016.1', 'level-two-road-test:036.1',
                      note='p137 and p138 give the rear-wheels test for any stop behind a vehicle.'),
    ('p132a', 'J', 'possible'): dict(
        status='OPEN', note='The candidate\'s own judgment. 142 (1) asks a driver to first see that a turn can be made in safety, with no measure.',
        links=[('on-hta:142(1)', 'law')]),
    ('p132a', 'V', 'overtake'): 'mto:1b|V|overtaking',
    ('p134a', 'V', 'go around'): PASS_WORD,
    ('p135a', 'V', 'overtaking'): 'mto:1b|V|overtaking',
    ('p137a', 'J', 'enough'): dict(
        status='HANDBOOK', definition='The statement gives the test: the rear wheels of the vehicle in front can be seen, or there is '
                                      'room to pull around it without backing up.',
        effect='Could drop "enough".',
        links=[(S + 'level-two-road-test:107.5', 'handbook'), (S + 'level-two-road-test:114.4', 'handbook')]),
    ('p137a', 'V', 'pull around it'): PASS_WORD,
    ('p137a', 'X', 'leave enough space to see its rear wheels or to pull around it without having to back up'): SAME_PASSAGES(
        'level-two-road-test:107.5', 'level-two-road-test:114.4', note='p131 and p133 give a similar rule at intersections.'),
}

# Provisions and law lines. Each entry: rows of (unit, relation, note), and lines of (text, note, units).
SB_PEN = [('on-hta:175(17)', 'PENALTY', '$400 to $2,000 for a first offence; $1,000 to $4,000, up to six months in jail, or both, after that.'),
          ('on-reg-339-94:item-14', 'PENALTY', '6 demerit points for 175 (11) and (12).')]
SB_DUTIES = ['on-hta:175(11)', 'on-hta:175(11.1)', 'on-hta:175(12)', 'on-hta:175(12.1)']
SB_STOP = ('a driver MUST stop before reaching a stopped school bus WHEN (the bus has its overhead red lights flashing OR its stop arm '
           'actuated) AND (the driver is approaching it from the rear OR meeting it from the front on a highway without a median strip) '
           'IF VIOLATED a fine of $400 to $2,000 for a first offence AND 6 demerit points',
           'The demerit table lists 6 points for 175 (11) and (12), the red-light duties; it names no points for the stop-arm duties.',
           SB_DUTIES + ['on-hta:175(17)', 'on-reg-339-94:item-14'])
sb_rows = lambda rel, note, arm_rel=None, arm_note=None: (  # noqa: E731
    [(u, arm_rel if arm_rel and u in ('on-hta:175(11.1)', 'on-hta:175(12.1)') else rel,
      arm_note if arm_note and u in ('on-hta:175(11.1)', 'on-hta:175(12.1)') else note) for u in SB_DUTIES] + SB_PEN)
front_rear = lambda front, rear: ([(u, 'BROADER', front) for u in SB_DUTIES[:2]] +  # noqa: E731
                                  [(u, 'SAME', rear) for u in SB_DUTIES[2:]] + SB_PEN)
LONGER_WAIT = 'BROADER'
STANDSTILL_PEN = [('on-hta:159(6)', 'PENALTY', '$400 to $2,000 for a first offence; $1,000 to $4,000, up to six months in jail, or both, after that.'),
                  ('on-reg-339-94:item-35', 'PENALTY', '3 demerit points.')]
L159A = ('a driver MUST immediately stop as near as practicable to the right-hand curb or edge of the roadway, parallel to it and clear '
         'of any intersection, WHEN an ambulance, fire, police or ministry vehicle approaches with its bell or siren sounding or its lamp '
         'flashing red or red and blue OR a public utility emergency vehicle approaches with its bell or siren sounding or its lamp '
         'flashing red IF VIOLATED a fine of $400 to $2,000 for a first offence AND 3 demerit points',
         'On a one-way roadway with more than two lanes, the nearest curb or edge instead (159 (1) (b)).',
         ['on-hta:159(1)', 'on-hta:159(1)@2027', 'on-hta:159(6)', 'on-reg-339-94:item-35'])
standstill_rows = lambda note: [('on-hta:159(1)', 'DIFFERENT', note),  # noqa: E731
                                ('on-hta:159(1)@2027', 'DIFFERENT', 'The same duty from January 1, 2027.')] + STANDSTILL_PEN
WORK_2027 = 'From January 1, 2027 the Act also covers a stopped work-related vehicle with amber flashing lamps.'
MOVE_OVER_ROWS = [('on-hta:159(2)@2027', 'NARROWER', WORK_2027), ('on-hta:159(3)@2027', 'NARROWER', WORK_2027),
                  ('on-hta:159(6)', 'PENALTY', '$400 to $2,000 for a first offence.'),
                  ('on-reg-339-94:item-36.2', 'PENALTY', '3 demerit points.'), ('on-reg-339-94:item-36.3', 'PENALTY', '3 demerit points.')]


def ref_lines(sid):
    return [(r['text'], r['note'], [u[0] for u in q('SELECT unit_id FROM statement_law_ref WHERE statement_id = ? AND position = ?',
                                                     sid, r['position'])])
            for r in q('SELECT * FROM statement_law WHERE statement_id = ? ORDER BY position', sid)]


def from_ref(sid):
    """Copy a reviewed statement's provisions and law lines, each note saying where it came from."""
    tag = lambda n: ((n or '') + f' (From {sid}.)').strip()  # noqa: E731
    return ([(r['unit_id'], r['relation'], tag(r['note'])) for r in q('SELECT * FROM statement_basis WHERE statement_id = ?', sid)],
            [(t, tag(n), u) for t, n, u in ref_lines(sid)])


BASIS = {
    'p6b': ([('on-hta:147(1)', 'SAME', 'The Act makes it a duty, where practicable; the handbook words it as advice.'),
             ('on-hta:147(3)', 'PENALTY', '$150 to $1,000.')],
            [(ref_lines('mto:3.2.2c')[0][0], 'Law where practicable, for a vehicle slower than the normal speed of traffic.',
              ['on-hta:147(1)', 'on-hta:147(3)'])]),
    'p23a': (front_rear('Meeting the bus from the front: the Act excludes a highway with a median strip (p24a).',
                        'Approaching from the rear.'), [SB_STOP]),
    'p24a': ([('on-hta:175(11)', 'SAME', 'The Act leaves a highway with a median strip out of the duty to stop when meeting the bus.'),
              ('on-hta:175(11.1)', 'SAME', 'The Act leaves a highway with a median strip out of the duty to stop when meeting the bus.')],
             [('a driver MUST stop before reaching a stopped school bus WHEN meeting it from the front AND (the bus has its overhead red '
               'lights flashing OR its stop arm actuated) UNLESS the highway has a median strip', None, ['on-hta:175(11)', 'on-hta:175(11.1)'])]),
    'p26a': (sb_rows(LONGER_WAIT, 'The Act makes it a duty and lets the driver go when the bus moves or the signal that was on stops; '
                                  'the statement waits for both.'),
             ref_lines('mto:3.4.12d')),
    'p32a': (front_rear('Any highway, except that meeting the bus from the front the Act excludes a highway with a median strip (p24a).',
                        'Any highway, from the rear.'), [SB_STOP]),
    'p33a': ([('on-hta:175(6)', 'SAME', 'The Act has the bus driver turn on the overhead signal-lights when about to stop and the stop arm '
                                        'as soon as the bus is stopped.')],
             [('a school bus driver MUST turn on the overhead signal-lights before stopping AND actuate the stop arm once stopped AND keep '
               'both on until the passengers are on or off and have crossed the highway WHEN stopping on a highway to pick up or drop off '
               'children or adults who have developmental disabilities',
               'Not at or within 60 m of a traffic control signal (175 (9)), which was not pulled.', ['on-hta:175(6)'])]),
    'p33b': (sb_rows(LONGER_WAIT, 'The Act makes it a duty and also lets the driver go once the bus moves; the statement waits for the '
                                  'arm to fold and every light to stop.'),
             ref_lines('mto:3.4.12d')),
    'p34b': ([('on-hta:207(1)', 'SAME', 'The owner may be charged with and convicted of the offence and is liable to its fine, unless the '
                                        'vehicle was taken without consent. 207 (2), which was not pulled, keeps this for 175 (11) to (12.1) '
                                        'and leaves out the 20 m rule of 175 (12.2).'),
              ('on-hta:207(7)', 'SAME', 'An owner convicted under 175 (19) to (20.1), the subsections a charge names for an owner, is not '
                                        'liable to jail or a licence suspension. The demerit table lists only 175 (11) and (12).')],
             [('the owner of a vehicle MAY be convicted of failing to stop for a school bus AND is then liable to the fine but not to jail '
               'or a licence suspension UNLESS the vehicle was in the possession of another person without the owner\'s consent',
               None, ['on-hta:207(1)', 'on-hta:207(7)'])]),
    'p54a': from_ref('mto:3.6.1a'),
    'p74b': from_ref('mto:3.2.2c'),
    'p74c': from_ref('mto:3.6.3b'),
    'p76a': (standstill_rows('The Act requires a standstill near the right-hand curb, clear of any intersection; abandoning the turn '
                             'and going straight is the handbook\'s way to get clear.'), [L159A]),
    'p78a': (standstill_rows('The Act requires a standstill near the right-hand curb, clear of any intersection; waiting there for the '
                             'vehicle to pass is the handbook\'s advice.'), [L159A]),
    'p81b': ([('on-hta:159(2)', 'SAME', 'The Act asks the driver to slow down having due regard for traffic, the highway and the weather; '
                                        'it does not name assessing the speed of traffic.'),
              ('on-hta:159(2)@2027', 'NARROWER', WORK_2027),
              ('on-hta:159(6)', 'PENALTY', '$400 to $2,000 for a first offence.'),
              ('on-reg-339-94:item-36.2', 'PENALTY', '3 demerit points.')],
             [('a driver MUST slow down AND proceed with [?caution], having due regard for traffic on and the conditions of the highway '
               'and the weather, so as not to collide with the stopped vehicle or endanger anyone outside it, WHEN approaching, on the same '
               'side of the road, an emergency vehicle stopped with red or red-and-blue lights flashing OR a tow truck stopped with amber '
               'lights flashing IF VIOLATED a fine of $400 to $2,000 for a first offence AND 3 demerit points', WORK_2027,
               ['on-hta:159(2)', 'on-hta:159(2)@2027', 'on-hta:159(6)', 'on-reg-339-94:item-36.2'])]),
    'p83b': ([('on-hta:159(2)', 'DIFFERENT', 'The steps carry out the duties to slow down (159 (2)) and move over (159 (3)); the Act names no steps.'),
              ('on-hta:159(3)', 'DIFFERENT', 'The steps carry out the duties to slow down (159 (2)) and move over (159 (3)); the Act names no steps.')]
             + MOVE_OVER_ROWS,
             ref_lines('mto:3.4.13a') + ref_lines('mto:3.4.13b')),
    'p86a': (standstill_rows('The Act requires an immediate standstill near the right-hand curb, clear of any intersection, for an '
                             'ambulance, fire, police or ministry vehicle or a public utility emergency vehicle; it does not say "proceed '
                             'with caution" or "where required".')
             + [('on-reg-339-94:item-36', 'PENALTY', '3 demerit points (159 (1) (b), nearest curb).'),
                ('on-reg-339-94:item-36.1', 'PENALTY', '3 demerit points (159 (1) (b), nearest edge).')],
             [L159A]),
    'p87a': ([('on-hta:159(2)', 'SAME', 'Covers a stopped tow truck with amber flashing lamps.'),
              ('on-hta:159(3)', 'SAME', 'Covers a stopped tow truck with amber flashing lamps.')] + MOVE_OVER_ROWS,
             ref_lines('mto:3.4.13a') + ref_lines('mto:3.4.13b')),
    'p100a': (sb_rows('NARROWER', 'The Act\'s duty does not depend on a sign.'), [SB_STOP]),
    'p102b': (sb_rows('SAME', 'The Act\'s duty, on a highway without a median strip.', 'NARROWER',
                      'The Act also makes the stop arm alone a reason to stop.'), [SB_STOP]),
    'p106a': ([('on-hta:142.1(1)', 'BROADER', 'The Act asks only a driver in the lane next to a bus bay, once the bus has signalled as '
                                              'prescribed; "bus" and "bus bay" are defined in O. Reg. 393/02, which was not pulled.'),
               ('on-hta:214(1)', 'PENALTY', '$60 to $1,000; the demerit table lists no points.')],
              [('a driver in the lane next to a bus bay MUST yield the right of way to a bus WHEN the bus driver has indicated, as '
                'prescribed, the intention to re-enter that lane from the bus bay IF VIOLATED a fine of $60 to $1,000', None,
                ['on-hta:142.1(1)', 'on-hta:214(1)'])]),
    'p108a': ([('on-hta:175(13)', 'SAME', 'A council may designate school bus loading zones by by-law; the bus driver\'s duty to use the '
                                          'signals (175 (6)) does not apply in them.')],
              [('a school bus driver MAY stop in a school bus loading zone designated by municipal by-law without turning on the overhead '
                'signal-lights or the stop arm', 'The by-law takes effect only once the signs are up (175 (14)), which was not pulled.',
                ['on-hta:175(13)'])]),
}


def main():
    for u in NEW_UNITS:
        db.execute('INSERT OR REPLACE INTO unit (id, source_id, kind, locator, heading, valid_from, valid_to, text) '
                   'VALUES (?, ?, \'provision\', ?, ?, ?, ?, ?)', u)
    done = 0
    for (local, code, span), spec in SPEC.items():
        oid = f'{R}{local}|{code}|{span}'
        if not q('SELECT 1 FROM occurrence WHERE id = ?', oid):
            sys.exit(f'no flag {oid}')
        db.execute('DELETE FROM grounding_link WHERE occurrence_id = ?', (oid,))
        db.execute('DELETE FROM grounding WHERE occurrence_id = ?', (oid,))
        if isinstance(spec, str):
            g = q('SELECT * FROM grounding WHERE occurrence_id = ?', spec)[0]
            note = ((g['note'] or '') + f' (Same as {spec.split("|")[0]}.)').strip()
            db.execute('INSERT INTO grounding VALUES (?, ?, ?, ?, ?)', (oid, g['status'], g['definition'], g['effect'], note))
            db.executemany('INSERT INTO grounding_link VALUES (?, ?, ?)',
                           [(oid, l['unit_id'], l['role']) for l in q('SELECT * FROM grounding_link WHERE occurrence_id = ?', spec)])
        else:
            db.execute('INSERT INTO grounding VALUES (?, ?, ?, ?, ?)',
                       (oid, spec['status'], spec.get('definition'), spec.get('effect'), spec.get('note')))
            db.executemany('INSERT INTO grounding_link VALUES (?, ?, ?)', [(oid, u, role) for u, role in spec.get('links', [])])
        done += 1

    for local, (rows, lines) in BASIS.items():
        sid = R + local
        for t in ('statement_law_ref', 'statement_law', 'statement_basis'):
            db.execute(f'DELETE FROM {t} WHERE statement_id = ?', (sid,))
        db.executemany('INSERT INTO statement_basis VALUES (?, ?, ?, ?)', [(sid, u, rel, note) for u, rel, note in rows])
        for pos, (text, note, units) in enumerate(lines):
            db.execute('INSERT INTO statement_law VALUES (?, ?, ?, ?)', (sid, pos, text, note))
            db.executemany('INSERT INTO statement_law_ref VALUES (?, ?, ?)', [(sid, pos, u) for u in units])
    dbtool.derive(db)
    db.commit()
    print(f'{len(NEW_UNITS)} provisions added; {done} flags grounded; provisions and law lines for {len(BASIS)} statements')


main()
