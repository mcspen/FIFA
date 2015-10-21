import json
import multiprocessing
import time

import FifaApp
from Logic.FormationDB import FormationDB
from Logic.Player import Player
from Logic.PlayerDB import PlayerDB
from Logic.TeamDB import TeamDB
from Logic.Team import Team
from Logic.HelperFunctions import delete_all_temp_images

if __name__ == '__main__':
    multiprocessing.freeze_support()

    # Load defaults
    """with open('configs.json', 'r') as f:
        configs = json.load(f)
        f.close()
    default_dbs = configs['default_databases']

    # Set defaults
    player_db = PlayerDB()
    player_list = PlayerDB()
    formation_db = FormationDB()
    formation_list = FormationDB()
    team_list = TeamDB()

    temp_time = time.time()
    player_db.load(default_dbs['player_db'], 'db')
    player_list.load(default_dbs['player_list'], 'list')
    formation_db.load(default_dbs['formation_db'], 'db')
    formation_list.load(default_dbs['formation_list'], 'list')
    team_list.load(default_dbs['team_list'])
    print "Time to load DBs: %f" % (time.time()-temp_time)

    db_dict = {
        'player_db': (default_dbs['player_db'], player_db),
        'player_list': (default_dbs['player_list'], player_list),
        'formation_db': (default_dbs['formation_db'], formation_db),
        'formation_list': (default_dbs['formation_list'], formation_list),
        'team_list': (default_dbs['team_list'], team_list)
    }

    FifaApp.start_app(db_dict)
    # delete_all_temp_images()"""

    teams = TeamDB()
    teams.load('2015-10-14')

    for index, team in enumerate(teams.db):
        temp = Team(team)
        temp.calculate_strength()
        teams.db[index] = temp.__dict__
    teams.sort(['strength', 'rating', 'total_ic'])
    for team in teams.db:
        temp = Team(team)
        temp.print_summary()
        print
        temp.print_chemistry_stats()
        print
        temp.print_team_strengths()
        print('\n')
    # """

    # -------------------------PLAYER DB EXAMPLES---------------------------
    # Initialize DB
    # player_db = PlayerDB()

    # Download Database from Website
    # temp_time = time.time()
    # player_db.download()
    # print "Time to create DB: %f" % (time.time()-temp_time)

    # Save Database to File
    # temp_time = time.time()
    # player_db.save('FIFA 16 - 5', 'db')
    # print "Time to save DB: %f" % (time.time()-temp_time)

    # Load Player Database from File
    # temp_time = time.time()
    # player_db.load('FIFA 16 - Current', 'db')
    # print "Time to load DB: %f" % (time.time()-temp_time)

    """teams = TeamDB()
    teams.load('2015-10-08', 'db')
    for index, team in enumerate(teams.db):
        print '============ TEAM %d ==============' % index
        Team(team).print_team_strengths()
        print"""

    """team = Team()
    team.load('Germany2014WorldCupFinal')
    team.print_team_strengths()"""

    """my_players = PlayerDB()
    my_players.load('my_players_16', 'list')"""

    """# Load Formation Database from file
    formation_db = FormationDB()
    formation_db.load('All Formations', 'db')"""

    """ultimate_team = Team()
    teams = TeamDB(ultimate_team.create_team_ultimate(my_players, formation_db, 'multi', 250))
    teams.save('2015-10-14')"""

    """silver_players = PlayerDB(my_players.search({'quality': ('silver', 'exact')}))

    ultimate_team = Team()
    teams = TeamDB(ultimate_team.create_team_ultimate(silver_players, formation_db, 'multi'))
    teams.save('silver_teams')"""

    """gold_players = PlayerDB(my_players.search({'quality': ('gold', 'exact')}))

    ultimate_team = Team()
    teams = TeamDB(ultimate_team.create_team_ultimate(gold_players, formation_list, 'multi'))
    teams.save('2015-10-13')"""

    """americans = PlayerDB(player_db.search({'nation': ('United States',)}))"""

    """ultimate_team = Team(Team.find_team_club(americans, formation_db))
    ultimate_team = Team(Team.find_team_league(americans, formation_db))
    ultimate_team = Team(Team.find_team_nation(americans, formation_db))
    ultimate_team.create_team_ultimate(americans, formation_db, 'both')"""

    """attr = 'skillMoves'
    fast_players = my_players.search({attr: 4}, 'higher')
    fast_players = PlayerDB(fast_players)
    fast_players.sort([attr])
    fast_players.print_compare_info()"""

    """my_players.console_search(player_db)
    my_players.sort(['rating'])
    my_players.save('my_players_16', 'list')"""

    """my_team = Team()
    my_formations = FormationDB(formation_db.search({'num_defenders': 4}, 'lower'))
    # team_list = my_team.create_team_ultimate(my_players, my_formations, 'multi', 50)
    team_list = my_team.create_team_ultimate(my_players, formation_db, 'single', 50)
    # team_list = my_team.create_team_ultimate(player_db, formation_db, 'single', 50)"""

    """my_teams = TeamDB()

    my_teams.__init__(team_list)
    my_teams.save('2015-09-23')"""

    """my_teams.load('2015-09-11')
    my_teams.print_db(20)

    for team in my_teams.db:
        temp = Team()
        temp.__init__(team)
        print '\n'
        temp.print_summary()
        temp.print_chemistry_stats()"""

    """traits = []
    for player in player_db.db:
        if player['traits'] is not None:
            traits += player['traits']
    traits = list(set(traits))
    print traits"""

    """team = TeamDB()
    team.load('2015-10-07')
    team.print_db()
    for t in team.db:
        Team(t).print_chemistry_stats()"""

    """from os import listdir
    files = listdir('Teams/2015-09-02/')
    team_list = []
    for filename in files:
        temp_team = Team()
        temp_team.load('2015-09-02/' + filename[:-5])
        team_list.append(temp_team)

    my_teams.add_teams(team_list)

    my_teams.save('2015-09-02')"""
