"""Hand grounding of the on-passing-1 flags and provisions on statements paired with the reviewed set.
Run once from the repo root after tools/carry_grounding.py; kept as the record of the hand grounding.
Each flag either takes the grounding of a named reviewed flag ("same") or gets its own."""
import sys
sys.path.insert(0, 'tools')
import db as dbtool  # noqa: E402

db = dbtool.connect()
q = lambda s, *a: db.execute(s, a).fetchall()  # noqa: E731
R = 'on-passing-1:'
KEEP_RIGHT = dict(status='LAW_STATES',
                  definition='Only a vehicle travelling at less than the normal speed of traffic must keep to the right-hand lane, '
                             'or as close as practicable to the right edge, where practicable (147 (1)).',
                  effect='The advice to every driver stays advice; the "must" for slow traffic is the Act\'s duty.',
                  links=[('on-hta:147(1)', 'law')])
SAME_PASSAGES = lambda *sents: dict(status='HANDBOOK', definition=None,  # noqa: E731
                                    effect='None; the passages give the same advice.',
                                    links=[(s, 'handbook') for s in sents])
WORD = lambda word, sent: dict(status='HANDBOOK', definition=f'The {word}; the handbook uses both words for the same lane.',  # noqa: E731
                               effect=f'None; the statement says {word}.', links=[(sent, 'handbook')])
OVERHEAD = dict(status='LAW_DEFINES', definition='The Act\'s term is "overhead red signal-lights" (175 (11), (12)).',
                effect='None; both handbook wordings name the same lights.', links=[('on-hta:175(11)', 'law'), ('on-hta:175(12)', 'law')])
SPEED_UP = ('No provision names speeding up while being passed. 148 (2) requires the driver being overtaken to turn out to the '
            'right; O. Reg. 455/07, s. 3, para. 8 i makes driving to prevent another vehicle from passing a stunt. Whether '
            'speeding up is such driving was not settled.')
RIGHT_HAND = 'mto:sent:driving-along:010.1'

SPEC = {
    ('p4a', 'M', 'These rules apply to all roads'): dict(
        status='LAW_STATES', definition='Use the lower beam when following another vehicle within 60 m, except when overtaking and '
                                        'passing, whenever lighted lamps are required (168 (b)).',
        effect='Strength LAW, WHEN lighted lamps are required.', links=[('on-hta:168', 'law')]),
    ('p6a', 'X', 'Keep to the right of the road or in the right-hand lane on multi-lane roads'): KEEP_RIGHT,
    ('p10a', 'J', 'too narrow to be shared safely'): 'mto:3.4.4a|J|safely',
    ('p11a', 'J', 'where practical'): 'mto:3.4.4b|J|practical',
    ('p11b', 'X', 'you should change lanes to pass'): dict(
        status='OPEN', note='The Act sets only the 1 m minimum (148 (6.1)); changing lanes is advice in both passages.'),
    ('p12a', 'V', 'overtaking'): 'mto:1b|V|overtaking',
    ('p14a', 'V', 'Large commercial vehicles'): dict(
        status='HANDBOOK', definition='The same vehicles: the passage says "large commercial vehicles" and "large vehicle".',
        effect='None; the statement says large vehicle.', links=[('mto:sent:sharing-road-other-road-users:051.2', 'handbook'),
                                                                ('mto:sent:sharing-road-other-road-users:051.3', 'handbook')]),
    ('p16a', 'J', 'safe to do so'): 'mto:3.4.7a|J|safe',
    ('p17a', 'J', 'safe to do so'): 'mto:3.4.7a|J|safe',
    ('p17b', 'J', 'too closely'): 'mto:3.4.8b|J|as much distance as possible',
    ('p25a', 'M', 'stop at least 20 meters away'): 'mto:3.4.12c|M|stop at least 20 metres away',
    ('p25a', 'X', 'If you are coming from behind the bus, stop at least 20 metres away.'): dict(
        status='LAW_STATES', definition='At least 20 m before reaching the bus, from the rear, when its red lights flash or its stop arm is actuated.',
        effect='None; both passages give 20 m, as the Act does.', links=[('on-hta:175(12.2)', 'law')]),
    ('p25a', 'V', 'overhead red lights'): OVERHEAD,
    ('p28a', 'X', 'the bus moves or the lights have stopped flashing'): 'mto:3.4.12d|X|and its stop arm is no longer activated',
    ('p35a', 'X', 'Passing within 30 metres of a pedestrian crossover is not permitted.'): 'mto:3.1.1a|X|within 30 m',
    ('p39a', 'R', 'These left-turn lanes'): dict(
        status='HANDBOOK', definition='Two-way left-turn lanes: the centre lanes the paragraph describes, used to turn left by traffic from both directions.',
        effect='None; the statement names them.', links=[('mto:sent:changing-directions:031.1', 'handbook')]),
    ('p40a', 'V', 'overtaking and passing'): 'mto:1b|V|overtaking',
    ('p44a', 'V', 'overtake and pass'): 'mto:1b|V|overtaking',
    ('p44b', 'X', "Don't pass moving snow plows under any conditions."): 'mto:3.4.9a|M|under any conditions',
    ('p45a', 'V', 'After overtaking'): 'mto:1b|V|overtaking',
    ('p49a', 'R', 'It is unlawful and dangerous'): dict(status='OPEN', note=SPEED_UP),
    ('p49a', 'X', 'do not speed up when another driver is trying to pass you'): dict(status='OPEN', note=SPEED_UP),
    ('p51b', 'J', 'in safety'): 'mto:3.1.3a|J|safely',
    ('p52a', 'J', 'carefully'): 'mto:3.5.2c|J|carefully',
    ('p53c', 'X', 'If you do want to pass these vehicles, do so by changing lanes.'): dict(
        status='OPEN', note='The Act sets only the 1 m minimum for bicycles (148 (6.1)); changing lanes is advice in both passages.'),
    ('p55a', 'S', 'many'): 'mto:3.6.3a|S|many high-speed roads',
    ('p55a', 'X', 'large trucks cannot travel in the far left lane'): 'mto:3.6.3a|X|many freeways',
    ('p55a', 'V', 'far left-hand lane'): dict(
        status='LAW_DEFINES', definition='The regulation says "the left lane" of the scheduled highway portions (Reg. 608, 1 (1)).',
        effect='None; both handbook wordings name that lane.', links=[('on-reg-608:1(1)', 'law')]),
    ('p57b', 'V', 'right lane'): WORD('right-hand lane', RIGHT_HAND),
    ('p57b', 'X', 'When you can see all of the front of the vehicle you are passing in your rear view mirror'): dict(
        status='HANDBOOK', definition='Return to the lane when the whole front of the passed vehicle shows in the inside (rear view) mirror.',
        effect='None; both procedures give the same cue.', links=[('mto:sent:changing-positions:017.2', 'handbook'),
                                                                 ('mto:sent:changing-positions:029.1', 'handbook')]),
    ('p63b', 'V', 'left-hand lane'): dict(
        status='HANDBOOK', definition='The left lane of the two-lane section; the handbook says "left lane" and "left-hand lane".',
        effect='None; the statement says left lane.', links=[('mto:sent:changing-positions:031.2', 'handbook'),
                                                             ('mto:sent:changing-positions:032.2', 'handbook')]),
    ('p65a', 'S', 'Most'): 'mto:3.2.3a|S|Most passing',
    ('p65b', 'D', 'You may pass on the right'): 'mto:3.2.3a|D|pass on the left',
    ('p65b', 'V', 'overtaking'): 'mto:1b|V|overtaking',
    ('p66b', 'V', 'left most lane'): dict(
        status='HANDBOOK', definition='The far-left lane.', effect='None; the statement says leftmost lane.',
        links=[('mto:sent:freeway-driving:022.1', 'handbook')]),
    ('p69a', 'M', 'stay at least two metres behind the rear doors'): 'mto:3.4.5b|M|stay at least two metres',
    ('p69b', 'J', 'reasonable'): 'mto:3.4.5d|J|reasonable speed',
    ('p73a', 'X', 'Traffic should keep to the right, using the left lanes for passing.'): KEEP_RIGHT,
    ('p74d', 'V', 'right lane'): WORD('right-hand lane', RIGHT_HAND),
    ('p81a', 'J', 'with caution'): 'mto:3.4.13a|J|caution',
    ('p81a', 'X', 'Failing to slow and carefully pass a stopped emergency vehicle'): dict(
        status='LAW_STATES', definition='The duty of 159 (2) covers an emergency vehicle or a tow truck; the regulation names the offence '
                                        '"failing to slow down and proceed with caution for emergency vehicle or tow truck".',
        effect='None; the statement follows the Act.', links=[('mto:sent:keeping-your-drivers-licence:105.1', 'handbook'),
                                                             ('on-hta:159(2)', 'law'), ('on-reg-339-94:item-36.2', 'law')]),
    ('p83a', 'J', 'safe to do so'): 'mto:3.4.13b|J|if safe to do so',
    ('p89a', 'X', "Don't pass other vehicles or speed up suddenly."): SAME_PASSAGES('mto:sent:driving-night-and-bad-weather:014.2',
                                                                                 'mto:sent:driving-night-and-bad-weather:028.2'),
    ('p93a', 'X', 'Avoid passing'): SAME_PASSAGES('mto:sent:driving-night-and-bad-weather:052.2',
                                                  'mto:sent:driving-night-and-bad-weather:059.1'),
    ('p95d', 'X', 'Do not try to pass between them.'): 'mto:3.4.9a|M|under any conditions',
    ('p98a', 'X', 'Slow traffic on multi-lane roads must keep right.'): KEEP_RIGHT,
    ('p104a', 'V', 'right lane'): WORD('right-hand lane', RIGHT_HAND),
    ('p110a', 'M', 'Do not pass the pilot vehicle or pace vehicle bearing this sign.'): 'mto:3.4.10a|M|Do not pass the pilot vehicle',
    ('p115a', 'J', 'unsafe'): dict(status='OPEN', note='Inside the reason; no duty to ground.'),
    ('p123a', 'X', 'driving a motor vehicle to prevent another vehicle from passing'): dict(
        status='LAW_STATES', definition='Driving in a manner that indicates an intention to prevent another vehicle from passing is a stunt '
                                        '(O. Reg. 455/07, s. 3, para. 8 i).',
        effect='None; the statement follows the regulation. Speeding up while being passed (p49a) is not named there.',
        links=[('on-hta:172(1)', 'law'), ('on-reg-455-07:3.8.i', 'law')]),
    ('p130a', 'M', 'you must'): 'mto:3.6.1a|M|move to the right',
    ('p130a', 'X', 'Move to the right and allow such vehicle to pass.'): 'mto:3.6.1a|M|move to the right',
    ('p130a', 'V', 'overtake and pass'): 'mto:1b|V|overtaking',
}

# Provisions for the paired statements whose wording differs from their pair: (new, reviewed, {unit: new note}),
# None to carry the reviewed note, or a new relation and note as a tuple.
BASIS = {
    'p74d': ('mto:3.2.2c', {}),
    'p130a': ('mto:3.6.1a', {'on-hta:148(2)': ('SAME', 'The Act makes it a duty, as the sample test question does.')}),
    'p55b': ('mto:3.6.3b', {}),
    'p65a': ('mto:3.2.3a', {}),
    'p11a': ('mto:3.4.4b', {}),
    'p69a': ('mto:3.4.5b', {'on-hta:166(1)': ('BROADER', 'The Act measures 2 m back from the nearest passenger door, lasts until the '
                                                         'passengers are on or safely at the side of the street, and does not apply at a '
                                                         'safety zone designated by by-law (p69b).')}),
    'p123a': ('mto:3.6.1c', {}),
    'p40a': ('mto:2.1a', {}),
    'p25a': ('mto:3.4.12c', {'on-hta:175(12.2)': ('SAME', 'The Act makes it a duty when the red lights flash or the stop arm is actuated.')}),
}
LAW_NOTE = {'p69a': 'Not where a safety zone is designated by by-law (p69b).'}


def main():
    # The one provision not yet in the database, copied word for word from statutes/on/hta/hta.txt.
    db.execute('INSERT OR REPLACE INTO unit (id, source_id, kind, locator, heading, text) VALUES (?, ?, ?, ?, ?, ?)',
               ('on-hta:168', 'on-hta', 'provision', 's. 168', 'Use of passing beam',
                '168 When on a highway at any time when lighted lamps are required to be displayed on vehicles, the driver of a motor '
                'vehicle equipped with multiple beam headlamps shall use the lower or passing beam when,\n(a) approaching an oncoming '
                'vehicle within 150 metres; or\n(b) following another vehicle within 60 metres, except when in the act of overtaking '
                'and passing.'))
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

    # p4a: the provision behind it, and the law line.
    sid = R + 'p4a'
    for t in ('statement_law_ref', 'statement_law', 'statement_basis'):
        db.execute(f'DELETE FROM {t} WHERE statement_id = ?', (sid,))
    db.execute('INSERT INTO statement_basis VALUES (?, ?, ?, ?)',
               (sid, 'on-hta:168', 'SAME', 'The Act makes it a duty whenever lighted lamps are required; the handbook words it as advice.'))
    db.execute('INSERT INTO statement_law VALUES (?, ?, ?, ?)',
               (sid, 0, 'a driver of a motor vehicle with multiple beam headlamps MUST use the lower or passing beam WHEN lighted lamps are '
                        'required AND the driver is following another vehicle within 60 m UNLESS the driver is overtaking and passing the vehicle',
                'The Act also requires the lower beam within 150 m of an oncoming vehicle.'))
    db.execute('INSERT INTO statement_law_ref VALUES (?, ?, ?)', (sid, 0, 'on-hta:168'))

    for local, (ref, changed) in BASIS.items():
        sid = R + local
        for t in ('statement_law_ref', 'statement_law', 'statement_basis'):
            db.execute(f'DELETE FROM {t} WHERE statement_id = ?', (sid,))
        for r in q('SELECT * FROM statement_basis WHERE statement_id = ?', ref):
            rel, note = changed.get(r['unit_id'], (r['relation'], r['note']))
            db.execute('INSERT INTO statement_basis VALUES (?, ?, ?, ?)', (sid, r['unit_id'], rel, ((note or '') + f' (From {ref}.)').strip()))
        for r in q('SELECT * FROM statement_law WHERE statement_id = ? ORDER BY position', ref):
            note = LAW_NOTE.get(local, r['note'])
            db.execute('INSERT INTO statement_law VALUES (?, ?, ?, ?)', (sid, r['position'], r['text'], ((note or '') + f' (From {ref}.)').strip()))
            db.executemany('INSERT INTO statement_law_ref VALUES (?, ?, ?)',
                           [(sid, r['position'], u[0]) for u in q('SELECT unit_id FROM statement_law_ref WHERE statement_id = ? AND position = ?',
                                                                  ref, r['position'])])
    dbtool.derive(db)
    db.commit()
    print(f'{done} flags grounded; provisions for p4a and {len(BASIS)} statements')


main()
