import json
import multiprocessing
import time

import FifaApp
from Window.AppConfig import config_filename
from Logic.FormationDB import FormationDB
from Logic.Player import Player
from Logic.PlayerDB import PlayerDB
from Logic.TeamDB import TeamDB
from Logic.Team import Team
from Logic.HelperFunctions import delete_all_temp_images
from Logic import UltimateTeamFunctions

if __name__ == '__main__':
    multiprocessing.freeze_support()

    # Load defaults
    with open(config_filename, 'r') as f:
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

    # -------------------------SELENIUM EXAMPLE---------------------------
    # new_player_list = PlayerDB()
    # new_player_list.get_players_from_account(player_db, "firefox", "test@yahoo.com", "test")

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

    # Player DB Profile Function
    player_db = PlayerDB()
    player_db.load('my_players_17', 'list')
    player_db.profile()

    # Profile Distribution of Levels and Probability of getting an 85+ Player
    """player_db = PlayerDB()
    player_db.load('FIFA 17 - Current', 'db')
    rating_dict = {}
    for player in player_db.db:
        if player['rating'] in rating_dict:
            rating_dict[player['rating']] = rating_dict[player['rating']] + 1
        else:
            rating_dict[player['rating']] = 1

    for key, value in rating_dict.iteritems():
        print "Rating: " + str(key) + "     # Players: " + str(value)

    total_gold = 0
    total_good = 0
    for key, value in rating_dict.iteritems():
        if key > 84:
            total_good += value
        if key > 74:
            total_gold += value

    print "Odds of getting 85+ player:"
    print str(total_good) + "/" + str(total_gold)
    print str(float(total_good)/float(total_gold)*100)[:4] + "%"

    rating_dict = {}
    for player in player_db.db:
        if player['rating'] >= 75 and 'rare' in player['color']:
            if player['rating'] in rating_dict:
                rating_dict[player['rating']] = rating_dict[player['rating']] + 1
            else:
                rating_dict[player['rating']] = 1

    for key, value in rating_dict.iteritems():
        print "Rating: " + str(key) + "     # Players: " + str(value)

    total_gold = 0
    total_good = 0
    for key, value in rating_dict.iteritems():
        if key > 84:
            total_good += value
        total_gold += value

    print "Odds of getting 84+ player out of rare_gold players:"
    print str(total_good) + "/" + str(total_gold)
    print str(float(total_good) / float(total_gold) * 100)[:4] + "%"
    """

    # Get average short passing for all leagues
    """leagues = {}
    for player in player_db.db:
        if player["league"]["name"] not in leagues:
            leagues[player["league"]["name"]] = {"total_short_passing": player["shortpassing"],
                                                 "total_players": 1,
                                                 "avg_short_passing": 0}
        else:
            leagues[player["league"]["name"]]["total_short_passing"] += player["shortpassing"]
            leagues[player["league"]["name"]]["total_players"] += 1

    # Calculate averages
    for league in leagues.itervalues():
        league["avg_short_passing"] = float(league["total_short_passing"]) / float(league["total_players"])

    # Create list of tuples of leagues and average short passing and sort
    leagues_tup = []
    for league in leagues.iteritems():
        leagues_tup.append((league[0], league[1]['avg_short_passing']))
    leagues_tup.sort(key=lambda leagues_tup: leagues_tup[1], reverse=True)

    # Print results
    from Logic import HelperFunctions
    for tup in leagues_tup:
        print HelperFunctions.ascii_text(tup[0]) + ": " + str(tup[1])"""

    # Get all characters used in names
    """characters = []
    for player in player_db.db:
        for char in player['firstName']:
            if char not in characters:
                characters.append(char)
        for char in player['lastName']:
            if char not in characters:
                characters.append(char)

    print characters"""

    # Add price to old DBs
    """player_db.load('FIFA 15', 'db')
    for player in player_db.db:
        player[u'price'] = 0
    player_db.save('FIFA 15', 'db', True)

    player_db.load('FIFA 16 - Original', 'db')
    for player in player_db.db:
        player[u'price'] = 0
    player_db.save('FIFA 16 - Original', 'db', True)"""

    # Save all of a player's images
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

    # Resize player background images
    """image_file_names = ['blue_purple', 'fut_champions_bronze', 'fut_champions_gold', 'fut_champions_silver', 'motm',
                        'motm_2', 'ones_to_watch', 'pink', 'pink_2', 'purple', 'squad_building_challenge', 'teal',
                        'tots_bronze', 'tots_gold', 'tots_silver', 'totw_bronze', 'totw_gold', 'totw_silver', 'toty']
    import Image
    for image_file_name in image_file_names:
        ratio = 0.85
        image_file = 'Images/Card Originals/FIFA 17/' + image_file_name + '.png'
        image_info = Image.open(image_file)
        image_info = image_info.resize((int(image_info.size[0]*ratio),
                                        int(image_info.size[1]*ratio)),
                                       Image.ANTIALIAS)
        new_image_file_name = 'Images/Cards/' + image_file_name + '.png'
        image_info.save(new_image_file_name)"""

    # Creating Ultimate teams with some players specified
    """players = PlayerDB()
    #players.load('my_players_16', 'list')
    players.load('FIFA 16 - Current', 'db')
    formations = FormationDB()
    formations.load('4-4-2', 'list')
    formation = formations.db[0]
    chemistry_matters = True
    time_limit = time.time() + 600
    players_per_position = 20
    teams_per_formation = 100
    team_sort_attributes = ['rating']
    player_sort_attributes = ['rating']
    num_teams = 100

    player0 = players.search({'name_custom': ('Courtois',)})[0]
    player1 = players.search({'name_custom': ('Reus',)})[0]
    player2 = players.search({'name_custom': ('Thiago Silva',)})[0]
    player3 = players.search({'name_custom': ('Maxwell',)})[0]
    player4 = players.search({'name_custom': ('Kompany',)})[0]
    player5 = players.search({'name_custom': ('Zabaleta',)})[0]
    player6 = players.search({'name_custom': ('Gotze',)})[0]
    player7 = players.search({'name_custom': ('Luiz Gustavo',)})[0]
    player8 = players.search({'name_custom': ('Kruse',)})[0]
    player9 = players.search({'name_custom': ('Huntelaar',)})[0]

    roster = {'GK': player0, 'LM': player1, 'LCB': player2, 'LB': player3, 'RCB': player4, 'RB': player5,
              'RCM': player6, 'LCM': player7, 'LST': player8, 'RST': player9}

    base_ids = [player0['baseId'], player1['baseId'], player2['baseId'], player3['baseId'], player4['baseId'],
                player5['baseId'], player6['baseId'], player7['baseId'], player8['baseId'], player9['baseId']]

    test = UltimateTeamFunctions.recursive_create(
            players, formation, chemistry_matters, time_limit, players_per_position, teams_per_formation,
            team_sort_attributes, player_sort_attributes, num_teams, roster=roster, base_ids=base_ids)

    if len(test[0]) > 0:
        teams = TeamDB(test[0])
        teams.save('test test test test test', True)
        print 'Got some teams!'
    # """

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

    # Create teams of American players
    """americans = PlayerDB(player_db.search({'nation': ('United States',)}))

    ultimate_team = Team(Team.find_team_club(americans, formation_db))
    ultimate_team = Team(Team.find_team_league(americans, formation_db))
    ultimate_team = Team(Team.find_team_nation(americans, formation_db))
    ultimate_team.create_team_ultimate(americans, formation_db, 'both')"""

    # Add players to player list using console search
    """player_list.console_search(player_db)
    player_list.sort(['rating'])
    player_list.save('my_players_16_console_search_test', 'list')"""

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

    # Go through all players and get all traits or specialities
    """item = 'traits'  # 'specialities'
    traits = []
    for player in player_db.db:
        if player[item] is not None:
            traits += player[item]
    traits = list(set(traits))
    traits.sort()
    for trait in traits:
        print str(trait)"""
