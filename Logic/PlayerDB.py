import copy
import json
import unicodedata
import requests
from Logic.Player import Player
from Logic.HelperFunctions import ascii_text


class PlayerDB:
    """
    The PlayerDB class contains a list of players.
    """

    def __init__(self, db_input=None):
        """
        Initialization function - creates either a blank dict or copies one from input
        Input: Optional player database dictionary
        Output: None  -  the database is created
        """

        if db_input is None:
            db_input = []
        elif type(db_input) != list:
            db_input = [db_input]
        self.db = copy.deepcopy(db_input)

    def download(self):
        """
        Download the database from the EA FIFA website
        Input: None
        Output: The downloaded database which is also already saved in the object
        """

        url_db_start = 'https://www.easports.com/fifa/ultimate-team/api/fut/item?jsonParamObject={"page":"'
        url_db_end = '"}'
        del self.db[:]  # Empty existing DB list

        # Create session
        sess = requests.Session()

        # Get total number of pages of data
        page_data = sess.get("%s1%s" % (url_db_start, url_db_end)).content  # Get first page data
        total_pages = json.loads(page_data)['totalPages']   # Get total number of pages

        # Iterate through all pages
        for page_num in range(1, total_pages+1):
            print "%d of %d pages" % (page_num, total_pages)

            while True:
                try:
                    # Get first page data
                    page_data = json.loads(sess.get("%s%s%s" % (url_db_start, page_num, url_db_end)).content)
                    break
                except Exception:
                    print "JSON Loading Error. Retrying Load."

            # Get the number of players on the page
            total_players = page_data['count']

            # Iterate through players on page
            for player_num in range(total_players):
                # Get player data
                player_data = page_data['items'][player_num]

                # Add player to database
                self.db.append(Player(player_data).__dict__)

        return self.db

    def save(self, db_name):
        """
        Save the database to the specified file name and overwrite the data
        Input: The name of the database to save
        Output: True  -  the database is saved in the file
        """

        # Create filename from database name
        filename = 'JSONs/' + db_name + '.json'

        with open(filename, 'w') as f:
            json.dump(self.db, f)
            f.close()

        return True

    def load(self, db_name):
        """
        Load the database from the specified file name
        Input: The name of the database to load
        Output: True  -  the database is loaded into the PlayerDB object
        """

        del self.db[:]  # Empty existing DB list

        # Create filename from database name
        filename = 'JSONs/' + db_name + '.json'

        with open(filename, 'r') as f:
            self.db = json.load(f)
            f.close()

        return True

    def add(self, new_player_list):
        """
        Add new players to the PlayerDB
        Input: The list of new players to add
        Output: True  -  the new players are added to the database
        """

        # Get a list of all players
        all_players = self.db + new_player_list

        # Find and remove duplicates
        for player in all_players:
            if all_players.count(player) > 1:
                all_players.remove(player)

        # Assign combined list of players to PlayerDB
        self.__init__(all_players)

        return True

    def sort(self, attributes, descend=True):
        """
        Sort the database or list of players
        Input: A list of attributes and the optional order boolean
        Example 1: arguments = ['attr1', 'attr2', 'attr3'], False
        or without the comparison operator
        Example 2: arguments = ['attr1', 'attr2']
        Output: None  -  the database is sorted
        """

        # Comparison function for sort that returns all attributes given
        def compare(current_player):
            attribute_tuple = ()
            for attr in attributes:

                if attr in current_player:
                    attribute_tuple += (current_player[attr],)

                elif attr in ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY']:
                    index = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY'].index(attr)
                    if not current_player['isGK']:
                        attribute_tuple += (current_player['attributes'][index]['value'],)
                    else:
                        attribute_tuple += (0,)

                elif attr in ['DIV', 'HAN', 'KIC', 'REF', 'SPD', 'POS']:
                    index = ['DIV', 'HAN', 'KIC', 'REF', 'SPD', 'POS'].index(attr)
                    if current_player['isGK']:
                        attribute_tuple += (current_player['attributes'][index]['value'],)
                    else:
                        attribute_tuple += (0,)

                elif attr in ['clubId', 'leagueId', 'nationId']:
                    attribute_tuple += (current_player[attr[:-2]]['id'],)

                elif attr == 'custom_name':
                    attribute_tuple += (current_player['lastName'],)

                else:
                    print "Invalid Attribute: %s" % attr

            return attribute_tuple

        self.db = sorted(self.db, key=compare, reverse=descend)

    def special_sort(self, position):
        """
        Sort the database or list of players by beneficial stats for the specified position
        Input: The position to sort for
        Output: None  -  the database is sorted
        """

        # Goalkeepers
        if position in ['GK']:
            attributes = ['rating']
        # Defense
        elif position in ['RB', 'CB', 'LB', 'RWB', 'LWB']:
            attributes = ['rating']
        # Midfield
        elif position in ['CDM', 'CM', 'CAM', 'RM', 'LM', 'RW', 'LW']:
            attributes = ['rating']
        # Offense
        elif position in ['CF', 'RF', 'LF', 'ST']:
            attributes = ['rating']

        # Comparison function for sort that returns all attributes given
        def compare(current_player):
            attribute_tuple = ()
            for attr in attributes:

                if attr in current_player:
                    attribute_tuple += (current_player[attr],)
                else:
                    print "Invalid Attribute: %s" % attr

            return attribute_tuple

        self.db = sorted(self.db, key=compare, reverse=True)

    def search(self, attributes):
        """
        Search for one set of players
        Input: A dictionary of tuples of the attribute values and the optional comparison type
        Comparison: 'higher', 'exact', 'lower', 'not'
        Example 1: arguments = {'attr1': (value1, 'exact')}
        or without the comparison operator
        Example 2: arguments = {'attr1': (value1,), 'attr2': (value2,), 'attr3': (value3,)}
        Output: A list of all matching players
        """

        players = []

        for player in self.db:
            match = True
            for attribute, tup in attributes.iteritems():

                if type(tup) is not tuple:
                    print "Attributes parameter is not valid. Must be a dict with a tuple value."
                    return []

                # Assign attribute value
                value = tup[0]

                # Assign comparison value and set default
                if len(tup) < 2:
                    compare = 'exact'
                # Treat 'not' like 'exact' and flip at the end
                elif tup[1] == 'not':
                    compare = 'exact'
                else:
                    compare = tup[1]

                # Make sure the comparison value is valid
                if compare not in ['higher', 'exact', 'lower']:
                    print "Compare value is not valid. Use 'higher', 'exact', or 'lower'."
                    return []

                if attribute in ['id', 'baseId']:
                    if not player[attribute] == str(value):
                        match = False
                elif attribute in ['nationId', 'leagueId', 'clubId']:
                    if not player[attribute]['id'] == str(value):
                        match = False
                elif attribute in ['name', 'quality', 'color', 'positionFull', 'itemType', 'modelName', 'playerType',
                                   'commonName', 'firstName', 'lastName', 'position', 'playStyle', 'foot',
                                   'atkWorkRate', 'defWorkRate']:
                    string_value = value.upper()
                    stat = player[attribute].upper()
                    if not stat.startswith(string_value):
                        match = False
                # Custom attribute used when user searching for players by any name
                elif attribute == 'name_custom':
                    string_value = value.upper()
                    name = ascii_text(player['name']).upper()
                    common_name = ascii_text(player['commonName']).upper()
                    first_name = ascii_text(player['firstName']).upper()
                    last_name = ascii_text(player['lastName']).upper()
                    if len(string_value) == 1:
                        if not (name.startswith(string_value) or common_name.startswith(string_value) or
                                first_name.startswith(string_value) or last_name.startswith(string_value)):
                            match = False
                    else:
                        if not (string_value in name or string_value in common_name or
                                string_value in first_name or string_value in last_name or
                                string_value in (first_name+' '+last_name)):
                            match = False
                elif attribute in ['isGK', 'isSpecialType']:
                    if not player[attribute] == value:
                        match = False
                elif attribute in ['rating', 'height', 'weight', 'birthdate', 'age', 'acceleration', 'aggression',
                                   'agility', 'balance', 'ballcontrol', 'crossing', 'curve', 'dribbling', 'finishing',
                                   'freekickaccuracy', 'gkdiving', 'gkhandling', 'gkkicking', 'gkpositioning',
                                   'gkreflexes', 'headingaccuracy', 'interceptions', 'jumping', 'longpassing',
                                   'longshots', 'marking', 'penalties', 'positioning', 'potential', 'reactions',
                                   'shortpassing', 'shotpower', 'skillMoves', 'slidingtackle', 'sprintspeed',
                                   'standingtackle', 'stamina', 'strength', 'vision', 'volleys', 'weakFoot']:
                    if compare == 'higher':
                        if not player[attribute] >= value:
                            match = False
                    elif compare == 'exact':
                        if not player[attribute] == value:
                            match = False
                    elif compare == 'lower':
                        if not player[attribute] <= value:
                            match = False
                elif attribute in ['nation', 'league', 'club']:
                    string_value = value.upper()
                    stat = player[attribute]['name'].upper()
                    if string_value not in stat:
                        match = False
                elif attribute in ['headshot', 'headshotImgUrl']:
                    print "Not searching based on " + attribute
                    match = False
                # Attributes for non goalkeepers
                elif attribute in ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY']:
                    if not player['isGK']:
                        index = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY'].index(attribute)
                        player_value = player['attributes'][index]['value']
                        if compare == 'higher':
                            if not player_value >= value:
                                match = False
                        elif compare == 'exact':
                            if not player_value == value:
                                match = False
                        elif compare == 'lower':
                            if not player_value <= value:
                                match = False
                    else:
                        match = False
                # Attributes for goalkeepers
                elif attribute in ['DIV', 'HAN', 'KIC', 'REF', 'SPD', 'POS']:
                    if player['isGK']:
                        index = ['DIV', 'HAN', 'KIC', 'REF', 'SPD', 'POS'].index(attribute)
                        player_value = player['attributes'][index]['value']
                        if compare == 'higher':
                            if not player_value >= value:
                                match = False
                        elif compare == 'exact':
                            if not player_value == value:
                                match = False
                        elif compare == 'lower':
                            if not player_value <= value:
                                match = False
                    else:
                        match = False
                elif attribute in ['specialities', 'traits']:
                    print "Haven't implemented %s yet" % attribute
                    match = False
                else:
                    print "Invalid Attribute: %s" % attribute
                    match = False
                    break

                # Switch matching boolean if comparison is 'not'
                if len(tup) > 1:
                    if tup[1] == 'not':
                        match = not match

                # If still matching, check next attribute
                if not match:
                    break

            # If all attributes match, add to the list
            if match:
                players.append(copy.deepcopy(player))

        return players

    def multi_search(self, attribute_dict_list):
        """
        Search for multiple sets of players
        Input: List of dicts of the attributes, values, and the optional comparison type
        ('higher', 'exact', 'lower', 'not')
        Example: attribute_tuple_list =[{'attr1': (value1, comp1)},
                                        {'attr2': (value2,), 'attr3': (value3, comp3)},
                                        {'attr4': (value4,), 'attr5': (value5,), 'attr6': (value6,)}]
        Output: A list of all matching players without duplicates
        """

        players = []

        for attributes in attribute_dict_list:

            temp_list = self.search(attributes)

            # Combine lists
            players += temp_list

        # Find and remove duplicates
        for player in players:
            if players.count(player) > 1:
                players.remove(player)

        return players

    def print_db(self, num_results=0):
        """
        Print out the name and rating of the first requested number of results
        Input: The number of results to be printed
        Output: None  -  prints the results to the console
        """

        # Ensure num_results is valid and set default/invalid to all results
        if num_results < 1 or num_results > len(self.db):
            num_results = len(self.db)

        # Iterate and print out all of the players
        for player in self.db[:num_results]:
            # Check for common name
            if len(player['commonName']) > 0:
                player_name = unicodedata.normalize('NFKD', player['commonName']).encode('ascii', 'ignore')
            else:
                player_name = unicodedata.normalize('NFKD', player['firstName']).encode('ascii', 'ignore') + ' ' + \
                              unicodedata.normalize('NFKD', player['lastName']).encode('ascii', 'ignore')

            # Print out name and rating
            print "%s%s%d" % (player_name,
                              " " * (35 - len(player_name)),
                              player['rating'])

    def print_compare_info(self, num_results=0):
        """
        Print out summary info for a player to help compare
        Input: A list of dicts of the players to print the info of to compare
        Output: None  -  prints the results to the console
        """

        # Ensure num_results is valid and set default/invalid to all results
        if num_results < 1 or num_results > len(self.db):
            num_results = len(self.db)

        # Iterate through players to print out
        for index, player in enumerate(self.db[:num_results]):

            # Get player's common name
            common_name = unicodedata.normalize('NFKD', player['commonName']).encode('ascii', 'ignore')

            # Get player's name
            player_name = unicodedata.normalize('NFKD', player['firstName']).encode('ascii', 'ignore') + ' ' + \
                          unicodedata.normalize('NFKD', player['lastName']).encode('ascii', 'ignore')

            # If the player has a common name, print it out first
            if len(common_name) > 0:
                title = common_name + " (" + player_name + ")"
            else:
                title = player_name

            # Get player's nation
            nation = unicodedata.normalize('NFKD', player['nation']['name']).encode('ascii', 'ignore')

            # Get player's club
            club = unicodedata.normalize('NFKD', player['club']['name']).encode('ascii', 'ignore')

            # Print out player info
            print "%s%s%s%s%s%s%d%s%s%s%s%s%s%s%s%s%d%s%s%s%d%s%s%s%d%s%s%s%d%s%s%s%d%s%s%s%d" % \
                  (index,
                   " " * (5 - len(str(index))),
                   title,
                   " " * (50 - len(title)),
                   player['color'],
                   " " * (15 - len(player['color'])),
                   player['rating'],
                   " " * 3,
                   player['position'],
                   " " * (6 - len(player['position'])),
                   nation,
                   " " * (20 - len(nation)),
                   club,
                   " " * (33 - len(club)),
                   player['attributes'][0]['name'][-3:],
                   ": ",
                   player['attributes'][0]['value'],
                   " " * 3,
                   player['attributes'][1]['name'][-3:],
                   ": ",
                   player['attributes'][1]['value'],
                   " " * 3,
                   player['attributes'][2]['name'][-3:],
                   ": ",
                   player['attributes'][2]['value'],
                   " " * 3,
                   player['attributes'][3]['name'][-3:],
                   ": ",
                   player['attributes'][3]['value'],
                   " " * 3,
                   player['attributes'][4]['name'][-3:],
                   ": ",
                   player['attributes'][4]['value'],
                   " " * 3,
                   player['attributes'][5]['name'][-3:],
                   ": ",
                   player['attributes'][5]['value'])

    def console_search(self, player_db):
        """
        Find players and create database interactively using the console
        Input: The PlayerDB to search
        Output: True  -  the database is created in the PlayerDB object
        """

        # Player list
        player_list = self.db

        # Words to cause exit
        exit_words = ['stop', 'quit', 'done', 'finished', 'finish', 'end']

        # Input variable
        input_var = ''

        # Loop until user says stop
        while input_var not in exit_words:

            print ''

            # Get player rating
            input_var = raw_input("Player Rating: ")

            # Check for exit word
            if input_var in exit_words:
                continue

            # Check that input is a number
            if not input_var.isdigit():
                print "Incorrect input - Try again"
                continue

            # Check number is between 1 and 99
            rating = int(input_var)
            if (rating < 1) or (rating > 99):
                print "Incorrect input - Try again"
                continue

            results = player_db.search({'rating': (rating, 'exact')})

            # Get player's name or initial
            input_var = raw_input("Name, Partial Name, or Initial: ")

            # Check for exit word
            if input_var in exit_words:
                continue

            # Search for player
            results = PlayerDB(results)
            results = results.search({'name_custom': (input_var, 'exact')})

            # No players found
            if len(results) == 0:
                print "No player found - Try again"
                continue

            # Check if player found
            if len(results) == 1:
                if player_list.count(results[0]) == 0:
                    player_list.append(results[0])
                    print "Player found, added to list."
                else:
                    print "Player already on list. Not adding."
                continue

            print "Players Remaining:"

            # Print player info out for comparison
            results = PlayerDB(results)
            results.print_compare_info()

            # Get player selection
            input_var = raw_input("Pick player or 'n' for none: ")

            # Check for exit word
            if input_var in exit_words:
                continue

            # Check if typed n
            if input_var == 'n':
                print "No player found - Try again"
                continue

            # Check that input is a number
            if not input_var.isdigit():
                print "Incorrect input - Try again"
                continue

            # Check if value entered was in range
            player_index = int(input_var)
            if (player_index < 0) or (player_index >= len(results.db)):
                print "Incorrect player value - Try again"
                continue

            # Return player
            if player_list.count(results.db[player_index]) == 0:
                player_list.append(results.db[player_index])
                print "Player found, added to list."
            else:
                print "Player already on list. Not adding."

        # Find and remove duplicates
        for player in player_list:
            if player_list.count(player) > 1:
                player_list.remove(player)

        # Assign list of players to PlayerDB
        self.__init__(player_list)
