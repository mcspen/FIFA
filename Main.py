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
    with open('configs.json', 'r') as f:
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

    # Calculate strengths and then print out for first 100 teams
    """teams = TeamDB()
    teams.load('2015-11-30_shorter')

    '''for index, team in enumerate(teams.db):
        temp = Team(team)
        temp.calculate_strength()
        teams.db[index] = temp.__dict__'''
    #teams.sort(['strength', 'rating', 'total_ic'])
    teams.sort(['rating', 'strength', 'total_ic'])
    for team in teams.db[:100]:
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

    # Print strengths of a list of teams
    """teams = TeamDB()
    teams.load('2015-11-19')
    for index, team in enumerate(teams.db):
        print '============ TEAM %d ==============' % index
        Team(team).print_team_strengths()
        print"""

    # Print Germany Team Strengths
    """team = Team()
    team.load('Germany2014WorldCupFinal')
    team.print_team_strengths()"""

    # Create ultimate teams and save
    """my_players = PlayerDB()
    #my_players.load('my_players_16', 'list')
    my_players.load('courtois', 'list')

    formation_db = FormationDB()
    formation_db.load('All Formations', 'db')

    ultimate_team = Team()
    teams = TeamDB(ultimate_team.create_team_ultimate(my_players, formation_db))
    teams.save('2015-11-20_2')
    #teams.save('Courtois Teams')"""

    # Create ultimate teams of silver players
    """silver_players = PlayerDB(my_players.search({'quality': ('silver', 'exact')}))

    ultimate_team = Team()
    teams = TeamDB(ultimate_team.create_team_ultimate(silver_players, formation_db, 'multi'))
    teams.save('silver_teams')"""

    # Create ultimate teams of gold players
    """my_players = PlayerDB()
    my_players.load('my_players_16', 'list')
    gold_players = PlayerDB(my_players.search({'quality': ('gold', 'exact')}))

    formation_db = FormationDB()
    formation_db.load('All Formations', 'db')

    ultimate_team = Team()
    teams = TeamDB(ultimate_team.create_team_ultimate(gold_players, formation_db))
    teams.save('2015-11-19')"""

    # Create teams of American players
    """americans = PlayerDB(player_db.search({'nation': ('United States',)}))

    ultimate_team = Team(Team.find_team_club(americans, formation_db))
    ultimate_team = Team(Team.find_team_league(americans, formation_db))
    ultimate_team = Team(Team.find_team_nation(americans, formation_db))
    ultimate_team.create_team_ultimate(americans, formation_db, 'both')"""

    # Search players by attribute and create new list and print comparison info
    """attr = 'skillMoves'
    attr_players = my_players.search({attr: 4}, 'higher')
    attr_players = PlayerDB(attr_players)
    attr_players.sort([attr])
    attr_players.print_compare_info()"""

    # Add players to player list using console search
    """my_players.console_search(player_db)
    my_players.sort(['rating'])
    my_players.save('my_players_16', 'list')"""

    # Create ultimate teams
    """my_team = Team()
    my_formations = FormationDB(formation_db.search({'num_defenders': 4}, 'lower'))
    # team_list = my_team.create_team_ultimate(my_players, my_formations, 'multi', 50)
    team_list = my_team.create_team_ultimate(my_players, formation_db, 'single', 50)
    # team_list = my_team.create_team_ultimate(player_db, formation_db, 'single', 50)"""

    # Save ultimate teams
    """my_teams = TeamDB()

    my_teams.__init__(team_list)
    my_teams.save('2015-09-23')"""

    # Create team based on individual stats
    """my_players = PlayerDB()
    my_players.load('my_players_16', 'list')
    formation_db = FormationDB()
    formation_db.load('All Formations', 'db')
    team = Team()
    #team.__init__(team.find_team(my_players, formation_db))#, ['skillMoves']))
    #team.__init__(team.find_team(my_players, formation_db, ['skillMoves']))
    team.__init__(team.find_team(my_players, formation_db, ['volleys']))
    team.print_summary()
    print
    team.print_chemistry_stats()
    print
    team.print_team_strengths()"""

    # Load teams and print out different info for first 20 teams
    """my_teams.load('2015-09-11')
    my_teams.print_db(20)

    for team in my_teams.db:
        temp = Team()
        temp.__init__(team)
        print '\n'
        temp.print_summary()
        temp.print_chemistry_stats()"""

    # Go through all players and get all traits
    """traits = []
    for player in player_db.db:
        if player['traits'] is not None:
            traits += player['traits']
    traits = list(set(traits))
    print traits"""

    # Load team and print chemistry stats for all of them
    """team = TeamDB()
    team.load('2015-10-07')
    team.print_db()
    for t in team.db:
        Team(t).print_chemistry_stats()"""

    # Create and save team list from all individual team files in a folder
    """from os import listdir
    files = listdir('Teams/2015-09-02/')
    team_list = []
    for filename in files:
        temp_team = Team()
        temp_team.load('2015-09-02/' + filename[:-5])
        team_list.append(temp_team)

    my_teams.add_teams(team_list)

    my_teams.save('2015-09-02')"""
