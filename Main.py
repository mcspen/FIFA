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

    player_db.load(default_dbs['player_db'], 'db')
    player_list.load(default_dbs['player_list'], 'list')
    formation_db.load(default_dbs['formation_db'], 'db')
    formation_list.load(default_dbs['formation_list'], 'list')
    team_list.load(default_dbs['team_list'])

    db_dict = {
        'player_db': (default_dbs['player_db'], player_db),
        'player_list': (default_dbs['player_list'], player_list),
        'formation_db': (default_dbs['formation_db'], formation_db),
        'formation_list': (default_dbs['formation_list'], formation_list),
        'team_list': (default_dbs['team_list'], team_list)
    }

    FifaApp.start_app(db_dict)
    # delete_all_temp_images()"""

    """from Logic.HelperFunctions import save_image
    players = PlayerDB()
    players.load('FIFA 16 - Current', 'db')
    player = players.db[2153]
    save_image(player['headshotImgUrl'], 'headshotImgUrl')
    save_image(player['headshot']['largeImgUrl'], 'player_largeImgUrl')
    save_image(player['headshot']['medImgUrl'], 'player_medImgUrl')
    save_image(player['headshot']['smallImgUrl'], 'player_smallImgUrl')
    save_image(player['league']['imgUrl'], 'league_imgUrl')
    save_image(player['nation']['imgUrl'], 'nation_imgUrl')
    save_image(player['nation']['imageUrls']['small'], 'nation_small_imgUrl')
    save_image(player['nation']['imageUrls']['medium'], 'nation_medium_imgUrl')
    save_image(player['nation']['imageUrls']['large'], 'nation_large_imgUrl')
    save_image(player['club']['imgUrl'], 'club_imgUrl')
    save_image(player['club']['imageUrls']['dark']['small'], 'club_dark_small_imgUrl')
    save_image(player['club']['imageUrls']['dark']['medium'], 'club_dark_medium_imgUrl')
    save_image(player['club']['imageUrls']['dark']['large'], 'club_dark_large_imgUrl')
    save_image(player['club']['imageUrls']['normal']['small'], 'club_normal_small_imgUrl')
    save_image(player['club']['imageUrls']['normal']['small'], 'club_normal_medium_imgUrl')
    save_image(player['club']['imageUrls']['normal']['large'], 'club_normal_large_imgUrl')"""

    # Print out strengths for first 100 teams
    """teams = TeamDB()
    teams.load('2015-11-30_shorter')

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

    # Create teams of American players
    """americans = PlayerDB(player_db.search({'nation': ('United States',)}))

    ultimate_team = Team(Team.find_team_club(americans, formation_db))
    ultimate_team = Team(Team.find_team_league(americans, formation_db))
    ultimate_team = Team(Team.find_team_nation(americans, formation_db))
    ultimate_team.create_team_ultimate(americans, formation_db, 'both')"""

    # Add players to player list using console search
    """my_players.console_search(player_db)
    my_players.sort(['rating'])
    my_players.save('my_players_16', 'list')"""

    # Create team based on individual stats
    """my_players = PlayerDB()
    my_players.load('my_players_16', 'list')
    formation_db = FormationDB()
    formation_db.load('All Formations', 'db')
    team = Team()
    #team.__init__(team.find_team(my_players, formation_db))#, ['skillMoves']))
    team.__init__(team.find_team(my_players, formation_db, ['skillMoves']))
    #team.__init__(team.find_team(my_players, formation_db, ['volleys']))
    #team.__init__(team.find_team(my_players, formation_db, ['sprintspeed']))
    team.print_summary()
    print
    team.print_chemistry_stats()
    print
    team.print_team_strengths()"""

    # Go through all players and get all traits
    """traits = []
    for player in player_db.db:
        if player['traits'] is not None:
            traits += player['traits']
    traits = list(set(traits))
    print traits"""
