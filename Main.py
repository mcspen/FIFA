import json
import multiprocessing
import time

import FifaApp
from Logic.FormationDB import FormationDB
from Logic.Player import Player
from Logic.PlayerDB import PlayerDB
from Logic.TeamDB import TeamDB
from Logic.Team import Team

if __name__ == '__main__':
    multiprocessing.freeze_support()

    # Load defaults
    with open('configs.json', 'r') as f:
        configs = json.load(f)
        f.close()

    default_dbs = configs['default_databases']

    # Set defaults
    player_db = PlayerDB()
    formation_db = FormationDB()
    player_list = PlayerDB()
    formation_list = FormationDB()
    team_list = TeamDB()

    temp_time = time.time()
    player_db.load(default_dbs['all_players'])
    player_list.load(default_dbs['my_players'])
    formation_db.load(default_dbs['all_formations'])
    formation_list.load(default_dbs['my_formations'])
    team_list.load(default_dbs['teams'])
    print "Time to load DBs: %f" % (time.time()-temp_time)

    db_dict = {
        'all_players': (default_dbs['all_players'], player_db),
        'my_players': (default_dbs['my_players'], player_list),
        'all_formations': (default_dbs['all_formations'], formation_db),
        'my_formations': (default_dbs['my_formations'], formation_list),
        'teams': (default_dbs['teams'], team_list)
    }

    FifaApp.start_app(db_dict)

    # -------------------------PLAYERDB EXAMPLES---------------------------
    # Initialize DB
    player_db = PlayerDB()

    # Download Database from Website
    # temp_time = time.time()
    # player_db.download()
    # print "Time to create DB: %f" % (time.time()-temp_time)

    # Save Database to File
    # temp_time = time.time()
    # player_db.save('player_db_16_3')
    # print "Time to save DB: %f" % (time.time()-temp_time)

    # Load Database from File
    temp_time = time.time()
    player_db.load('player_db_16_3')
    print "Time to load DB: %f" % (time.time()-temp_time)

    # Sort Database by Rating and Sprint Speed
    """temp_time = time.time()
    player_db.sort(['rating', 'sprintspeed'])
    print "Time to sort DB: %f" % (time.time()-temp_time)

    # Search Example: Find all normal players (not Legends) that are age 43 or over
    results = PlayerDB(player_db.search({'age': 43, 'isSpecialType': False}, 'higher'))
    results.sort(['age'])
    print ''
    for player in results.db:
        print "%s %s %d %s" % (player['firstName'], player['lastName'], player['age'], player['color'])

    # Search Ex: Find all normal players (not legends) that are age 43 or over and 18 or younger and those that are 31
    attribute_list = [({'age': 43, 'isSpecialType': False}, 'higher'),
                      ({'age': 17, 'isSpecialType': False}, 'lower'),
                      ({'age': 37, 'isSpecialType': False},)]
    young_and_old = PlayerDB(player_db.multi_search(attribute_list))
    young_and_old.sort(['age'])
    print ''
    for player in young_and_old.db:
        print "%d %s" % (player['age'], player['color'])

    '''player_db.sort(['age'])
    for player in player_db.db:
        print "%s %s %d %s" % (player['firstName'], player['lastName'], player['age'], player['color'])'''

    messi = PlayerDB(player_db.search({'lastName': 'Messi'}))
    messi.sort(['rating'])
    messi.print_db()

    player_db.print_db(10)

    attribute_list = [({'lastName': 'Messi'},), ({'rating': 95}, 'higher'), ({'club': 'FC Barcelona'}, 'exact')]
    messiAllStarsBarca = PlayerDB(player_db.multi_search(attribute_list))
    print ''
    print len(messiAllStarsBarca.db)
    messiAllStarsBarca.sort({'rating', 'firstName'})

    for player in messiAllStarsBarca.db:
        if len(player['commonName']) > 0:
            player_name = player['commonName']
        else:
            player_name = unicodedata.normalize('NFKD', player['firstName']).encode('ascii', 'ignore') + ' ' + \
                unicodedata.normalize('NFKD', player['lastName']).encode('ascii', 'ignore')
        print "%s%s%d%s%s" % (player_name, " " * (35-len(player_name)), player['rating'], "     ", player['color'])"""

    # -------------------------FORMATION DB EXAMPLES---------------------------

    formation_db = FormationDB()
    formation_db.load('formation_db')

    '''formation_db.print_db()

    print '\nNormal'
    formation_db.print_db_short()

    print '\nSorted by num_midfielders'
    formation_db.sort(['num_midfielders', 'name'])
    formation_db.print_db_short()

    print '\nSearch for 5 midfielders'
    five_mids = FormationDB(formation_db.search({'num_midfielders': 5}, 'higher'))
    five_mids.print_db_short()

    formation_db.print_positions()

    # -------------------------TEAM EXAMPLES---------------------------
    test_team = Team()
    test_team.set_team(formation_db.search({'name': '4-4-2'})[0], {
        'GK': player_db.search({'position': 'GK', 'rating': 85}, 'lower')[0],
        'LB': player_db.search({'position': 'LB', 'rating': 85}, 'lower')[0],
        'LCB': player_db.search({'position': 'CB', 'rating': 85}, 'lower')[0],
        'RCB': player_db.search({'position': 'CB', 'rating': 85}, 'lower')[0],
        'RB': player_db.search({'position': 'RB', 'rating': 85}, 'lower')[0],
        'LM': player_db.search({'position': 'LM', 'rating': 85}, 'lower')[0],
        'LCM': player_db.search({'position': 'CM', 'rating': 85}, 'lower')[0],
        'RCM': player_db.search({'position': 'CM', 'rating': 85}, 'lower')[0],
        'RM': player_db.search({'position': 'RM', 'rating': 85}, 'lower')[0],
        'LST': player_db.search({'position': 'ST', 'rating': 85}, 'lower')[0],
        'RST': player_db.search({'position': 'ST', 'rating': 85}, 'lower')[0]},
        {'nation': 'Moon', 'league': 'Rocket League'}, loyalty=False)

    test_team_copy = Team(test_team.__dict__)

    test_team_copy.print_roster()
    print ''
    test_team_copy.print_roster_sections()
    print ''
    test_team_copy.print_summary()
    print ''
    test_team_copy.print_chemistry_stats()

    test_team_copy.manager = {'nation': 'Error', 'league': 'Error Again'}
    print test_team_copy.manager
    test_team_copy.load('TestTeam')
    print test_team_copy.manager

    # -------------------------CREATE ATTRIBUTE TEAM EXAMPLES---------------------------

    italians = PlayerDB(player_db.search({'nation': 'Italy'}))
    three_def = FormationDB(formation_db.search({'num_defenders': 3}))

    italian_speedy_job = Team()
    italian_speedy_job.__init__(Team.create_team_attributes_old(italians, three_def, ['sprintspeed', 'acceleration']))
    italian_speedy_job.print_chemistry_stats()

    for position, player in italian_speedy_job.formation['positions'].iteritems():
        print "%s:%sRating: %d   Sprint Speed: %d   Acceleration: %d" % (position, ' ' * (7 - len(position)),
                                                                         player['player']['rating'],
                                                                         player['player']['sprintspeed'],
                                                                         player['player']['acceleration'])

    print ''

    italians.sort(['sprintspeed', 'acceleration'])
    index = 1
    for player in italians.db:
        print "%s:%sRating: %d   Sprint Speed: %d   Acceleration: %d" % (player['position'],
                                                                         ' ' * (7 - len(player['position'])),
                                                                         player['rating'], player['sprintspeed'],
                                                                         player['acceleration'])
        index += 1
        if index == 20:
            break

    # -------------------------CREATE ATTRIBUTE TEAM EXAMPLES---------------------------

    print italian_speedy_job.related_positions('CM')

    italian_speedy_job2 = Team()
    italian_speedy_job2.create_team(italians, formation_db, ['sprintspeed', 'acceleration'])

    print 'Italian Speedy Job 1:'
    italian_speedy_job.print_chemistry_stats()
    italian_speedy_job.print_summary()
    print ''
    print 'Italian Speedy Job 2:'
    italian_speedy_job2.print_chemistry_stats()
    italian_speedy_job2.print_summary()

    fastest_team = Team()
    fastest_team.create_team(player_db, formation_db, ['sprintspeed', 'acceleration'])
    fastest_team.print_chemistry_stats()
    fastest_team.print_summary()
    fastest_team.print_roster_sections()

    # -------------------------EDGE CASE TEAM EXAMPLE---------------------------

    edge_case_formation = FormationDB(formation_db.search({'name': '4-1-2-1-2 (2)'}))
    player_list = [
        player_db.search({'position': 'GK', 'rating': 85}, 'lower')[0],
        player_db.search({'position': 'LB', 'rating': 85}, 'lower')[0],
        player_db.search({'position': 'CB', 'rating': 85}, 'lower')[0],
        player_db.search({'position': 'CB', 'rating': 80}, 'lower')[0],
        player_db.search({'position': 'RB', 'rating': 85}, 'lower')[0],
        player_db.search({'position': 'ST', 'rating': 85}, 'lower')[0],
        player_db.search({'position': 'ST', 'rating': 80}, 'lower')[0],

        player_db.search({'position': 'CM', 'rating': 75}, 'lower')[0],
        player_db.search({'position': 'CM', 'rating': 74}, 'lower')[0],
        player_db.search({'position': 'CM', 'rating': 73}, 'lower')[0],
        player_db.search({'position': 'CDM', 'rating': 72}, 'lower')[0]
    ]

    players = PlayerDB(player_list)
    players.print_db()

    edge_case = Team()
    edge_case.create_team(players, edge_case_formation, ['rating'])

    edge_case.print_roster()
    print ''
    edge_case.print_roster_sections()
    print ''
    edge_case.print_summary()
    print ''
    edge_case.print_chemistry_stats()
    '''

    # -------------------------CONSOLE SEARCH EXAMPLE---------------------------

    """personal_db_name = 'my_players'

    # Load personal player database
    personal_db = PlayerDB()
    personal_db.load(personal_db_name)

    # Search for new players using console search
    player_search = PlayerDB()
    player_search.console_search(player_db)

    # Add new players to personal player database
    personal_db.add(player_search.db)

    # Save personal player database
    personal_db.save(personal_db_name)"""

    # -------------------------ULTIMATE TEAM EXAMPLE---------------------------

    americans = PlayerDB(player_db.search({'nation': ('United States',)}))

    """player_db.sort({'firstName'}, False)
    #test1 = player_db.search({'nation': 'Germany', 'club': '1. FC Heidenheim', 'position': 'ST'})
    #test2 = player_db.search({'nation': 'Germany', 'club': '1. FC Heidenheim', 'position': 'CM'})
    #formation_db_2 = FormationDB(formation_db.db[1])
    chumps = PlayerDB(player_db.db[:1000])# + test1 + test2)

    ultimate_team = Team(Team.find_team_club(americans, formation_db))
    ultimate_team = Team(Team.find_team_league(americans, formation_db))
    ultimate_team = Team(Team.find_team_nation(americans, formation_db))
    ultimate_team.create_team_ultimate(americans, formation_db, 'both')"""

    """traits = []
    for player in player_db.db:
        if player['traits'] is not None:
            traits += player['traits']
    traits = list(set(traits))
    print traits"""

    my_players = PlayerDB()
    my_players.load('my_players_db_16')

    """attr = 'skillMoves'
    fast_players = my_players.search({attr: 4}, 'higher')
    fast_players = PlayerDB(fast_players)
    fast_players.sort([attr])
    fast_players.print_compare_info()"""

    """my_players.console_search(player_db)
    my_players.sort(['rating'])
    my_players.save('my_players_db_16')"""

    """my_team = Team()
    my_formations = FormationDB(formation_db.search({'num_defenders': 4}, 'lower'))
    # team_list = my_team.create_team_ultimate(my_players, my_formations, 'multi', 50)
    team_list = my_team.create_team_ultimate(my_players, formation_db, 'single', 50)
    # team_list = my_team.create_team_ultimate(player_db, formation_db, 'single', 50)"""

    my_teams = TeamDB()

    # my_teams.__init__(team_list)
    # my_teams.save('team_db_2015-09-23')

    """my_teams.load('team_db_2015-09-11')
    my_teams.print_db(20)

    for team in my_teams.db:
        temp = Team()
        temp.__init__(team)
        print '\n'
        temp.print_summary()
        temp.print_chemistry_stats()"""

    """from os import listdir
    files = listdir('Teams/2015-09-02/')
    team_list = []
    for filename in files:
        temp_team = Team()
        temp_team.load('2015-09-02/' + filename[:-5])
        team_list.append(temp_team)

    my_teams.add_teams(team_list)

    my_teams.save('team_db_2015-09-02')"""

    test = 1
