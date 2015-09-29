'''formation_name = '5-3-2'
num_def = 5
num_mid = 3
num_off = 2
p1 = {                                        'symbol': 'GK',  'custom_symbol': 'GK'}

p2 =  {'name': 'Left Wing Back',              'symbol': 'LWB', 'custom_symbol': 'LWB'}
p3 =  {'name': 'Left Center Back',            'symbol': 'CB',  'custom_symbol': 'LCB'}
p4 =  {'name': 'Center Back',                 'symbol': 'CB',  'custom_symbol': 'CB'}
p5 =  {'name': 'Right Center Back',           'symbol': 'CB',  'custom_symbol': 'RCB'}
p6 =  {'name': 'Right Wing Back',             'symbol': 'RWB', 'custom_symbol': 'RWB'}

p7 =  {'name': 'Left Center Midfielder',      'symbol': 'CM',  'custom_symbol': 'LCM'}
p8 =  {'name': 'Center Midfielder',           'symbol': 'CM',  'custom_symbol': 'CM'}
p9 =  {'name': 'Right Center Midfielder',     'symbol': 'CM',  'custom_symbol': 'RCM'}

p10 = {'name': 'Left Striker',                'symbol': 'ST',  'custom_symbol': 'LST'}
p11 = {'name': 'Right Striker',               'symbol': 'ST',  'custom_symbol': 'RST'}

p2['connections'] =  [p3['custom_symbol'], p7['custom_symbol']]
p3['connections'] =  [p1['custom_symbol'], p2['custom_symbol'], p4['custom_symbol'], p7['custom_symbol']]
p4['connections'] =  [p1['custom_symbol'], p3['custom_symbol'], p5['custom_symbol'], p8['custom_symbol']]
p5['connections'] =  [p1['custom_symbol'], p4['custom_symbol'], p6['custom_symbol'], p9['custom_symbol']]
p6['connections'] =  [p5['custom_symbol'], p9['custom_symbol']]

p7['connections'] =  [p2['custom_symbol'], p3['custom_symbol'], p8['custom_symbol'], p10['custom_symbol']]
p8['connections'] =  [p4['custom_symbol'], p7['custom_symbol'], p9['custom_symbol'], p10['custom_symbol'], p11['custom_symbol']]
p9['connections'] =  [p5['custom_symbol'], p6['custom_symbol'], p8['custom_symbol'], p11['custom_symbol']]

p10['connections'] = [p7['custom_symbol'], p8['custom_symbol'], p11['custom_symbol']]
p11['connections'] = [p8['custom_symbol'], p9['custom_symbol'], p10['custom_symbol']]

defense_positions = []
midfield_positions = []
offense_positions = []

defense_positions.append(Position({'name': p2['name'], 'symbol': p2['symbol'], 'custom_symbol': p2['custom_symbol'], 'player': {}, 'connections': p2['connections']}).__dict__)
defense_positions.append(Position({'name': p3['name'], 'symbol': p3['symbol'], 'custom_symbol': p3['custom_symbol'], 'player': {}, 'connections': p3['connections']}).__dict__)
defense_positions.append(Position({'name': p4['name'], 'symbol': p4['symbol'], 'custom_symbol': p4['custom_symbol'], 'player': {}, 'connections': p4['connections']}).__dict__)
defense_positions.append(Position({'name': p5['name'], 'symbol': p5['symbol'], 'custom_symbol': p5['custom_symbol'], 'player': {}, 'connections': p5['connections']}).__dict__)
defense_positions.append(Position({'name': p6['name'], 'symbol': p6['symbol'], 'custom_symbol': p6['custom_symbol'], 'player': {}, 'connections': p6['connections']}).__dict__)

midfield_positions.append(Position({'name': p7['name'], 'symbol': p7['symbol'], 'custom_symbol': p7['custom_symbol'], 'player': {}, 'connections': p7['connections']}).__dict__)
midfield_positions.append(Position({'name': p8['name'], 'symbol': p8['symbol'], 'custom_symbol': p8['custom_symbol'], 'player': {}, 'connections': p8['connections']}).__dict__)
midfield_positions.append(Position({'name': p9['name'], 'symbol': p9['symbol'], 'custom_symbol': p9['custom_symbol'], 'player': {}, 'connections': p9['connections']}).__dict__)

offense_positions.append(Position({'name': p10['name'], 'symbol': p10['symbol'], 'custom_symbol': p10['custom_symbol'], 'player': {}, 'connections': p10['connections']}).__dict__)
offense_positions.append(Position({'name': p11['name'], 'symbol': p11['symbol'], 'custom_symbol': p11['custom_symbol'], 'player': {}, 'connections': p11['connections']}).__dict__)'''

'''formation = Formation()
formation.create_formation(formation_name,
                          'temp_style',
                          'temp_description',
                          num_def, defense_positions, num_mid, midfield_positions, num_off, offense_positions)'''

'''formation_db = FormationDB()
formation_db.load('formation_db.json')

for formation in formation_db.db:
    formation['num_defenders'] = formation['defense']['num_defenders']
    formation['num_midfielders'] = formation['midfield']['num_midfielders']
    formation['num_attackers'] = formation['offense']['num_attackers']

    # Delete old positions dict
    del formation['positions']

    # Create new positions dict
    formation['positions'] = {'GK': {'index': 0}}
    # Goalkeeper dict
    formation['positions']['GK']['symbol'] = formation['goalkeeper']['goalkeeper'][0]['symbol']
    formation['positions']['GK']['name'] = formation['goalkeeper']['goalkeeper'][0]['name']
    formation['positions']['GK']['links'] = formation['goalkeeper']['goalkeeper'][0]['connections']

    # Defense dicts
    index = 1
    for defender in formation['defense']['defenders']:
        formation['positions'][defender['custom_symbol']] = {'index': index}
        formation['positions'][defender['custom_symbol']]['symbol'] = defender['symbol']
        formation['positions'][defender['custom_symbol']]['name'] = defender['name']
        formation['positions'][defender['custom_symbol']]['links'] = defender['connections']
        index += 1

    # Midfield dicts
    index = 1 + formation['num_defenders']
    for midfielder in formation['midfield']['midfielders']:
        formation['positions'][midfielder['custom_symbol']] = {'index': index}
        formation['positions'][midfielder['custom_symbol']]['symbol'] = midfielder['symbol']
        formation['positions'][midfielder['custom_symbol']]['name'] = midfielder['name']
        formation['positions'][midfielder['custom_symbol']]['links'] = midfielder['connections']
        index += 1

    # Midfield dicts
    index = 1 + formation['num_defenders'] + formation['num_midfielders']
    for attacker in formation['offense']['attackers']:
        formation['positions'][attacker['custom_symbol']] = {'index': index}
        formation['positions'][attacker['custom_symbol']]['symbol'] = attacker['symbol']
        formation['positions'][attacker['custom_symbol']]['name'] = attacker['name']
        formation['positions'][attacker['custom_symbol']]['links'] = attacker['connections']
        index += 1

    # Delete old parts
    del formation['goalkeeper']
    del formation['defense']
    del formation['midfield']
    del formation['offense']

    if formation['name'] == '4-3-1-2':
        formation['positions']['CAM']['index'] = 7
        formation['positions']['RCM']['index'] = 8

formation_db.print_positions(symbol='custom')
formation_db.print_db_short()
formation_db.print_db()

formation_db.save('formation_db.json')'''

'''exists = False
for form in formation_db.db:
    if str(form['name']) == formation_name:
        exists = True

if exists:
    print "%s exists already" % formation_name
else:
    formation_db.add_formation(formation)
    formation_db.save('formation_db.json')'''

test = 1
