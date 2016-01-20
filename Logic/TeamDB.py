import copy
import json
from os.path import isfile
from Team import Team
from Player import Player


class TeamDB:
    """
    The TeamDB class contains a list of teams.
    """

    def __init__(self, db_input=None):
        """
        Initialization function - creates either a blank dict or copies one from input
        Input: Optional team database dictionary
        Output: None  -  the database is created
        """

        if db_input is None:
            db_input = []
        elif type(db_input) != list:
            db_input = [db_input]
        self.db = copy.deepcopy(db_input)

    def add_team(self, team):
        """
        Add a new team to the database
        Input: Team
        Output: None  -  the team is added to the database
        """

        self.db.append(copy.deepcopy(team.__dict__))

    def add_teams(self, team_list):
        """
        Add a list of new teams to the database
        Input: List of teams
        Output: None  -  the teams are added to the database
        """

        for team in team_list:
            self.db.append(copy.deepcopy(team.__dict__))

    def save(self, file_name, overwrite=False):
        """
        Save the database to the specified file name and overwrite the data
        Input: The name of the database to save
        Output: True  -  the database is saved in the file
        """

        # Create filename from file name
        file_path = 'JSONs/team_lt_' + file_name + '.json'

        if (not isfile(file_path)) or overwrite:
            with open(file_path, 'w') as f:
                json.dump(self.db, f)
                f.close()

        else:
            index = 1
            while isfile('JSONs/team_lt_' + file_name + ' (' + str(index) + ').json'):
                index += 1
            print "File already exists. Adding ' (%d)' to file name" % index
            self.save(file_name + ' (' + str(index) + ')', overwrite)

        return True

    def load(self, file_name, file_type='list'):
        """
        Load the database from the specified file name
        Input: The name of the database to load
        Output: True  -  the database is loaded into the TeamDB object

        The only file type is list, but kept the argument for symmetry.
        """

        del self.db[:]  # Empty existing DB list

        if file_type != 'list':
            print "Invalid list type."

        # Create filename from database name
        file_path = 'JSONs/team_lt_' + file_name + '.json'

        if isfile(file_path):
            with open(file_path, 'r') as f:
                self.db = json.load(f)
                f.close()

        else:
            print "File does not exist."
            return False

        return True

    def update_player_prices(self, queue=None, console='PS4'):
        """
        Gets updated price information for all the players on all of the teams on the list
        Input: None
        Output: None  -  the player price information is updated
        """

        # Create a list of all the players to avoid duplicating searches
        player_list = []
        price_list = {}
        # Iterate through teams
        for team in self.db:
            # Iterate through positions on team
            for position in team['formation']['positions'].itervalues():
                player = position['player']
                if player_list.count(player) == 0:
                    player_list.append(player)

        # Iterate through list of players and get updated prices
        total_players = len(player_list)
        for idx, player_info in enumerate(player_list):
            player = Player(player_info)
            price_list[player.id] = player.get_price(console)

            # Display number of pages completed
            if queue is not None:
                queue.put((idx+1, total_players))
            print "%d of %d players updated" % (idx+1, total_players)

        # Assign values back to players on teams
        # Iterate through teams
        for team in self.db:
            # Iterate through positions on team
            for position in team['formation']['positions'].itervalues():
                # Assign updated price
                player = position['player']
                player['price'] = price_list[player['id']]

    def sort(self, attributes, descend=True):
        """
        Sort the TeamDB
        Input: A list of attributes and the optional order boolean
        Example 1: arguments = ['attr1', 'attr2', 'attr3'], False
        or without the comparison operator
        Example 2: arguments = ['attr1', 'attr2']
        Output: None  -  the database is sorted
        """

        def compare(current_team):
            """
            Based on the list of attributes, return a tuple of attributes for the current team.
            Input: The current team.
            Output: A tuple of attributes to compare with.
            """

            attribute_tuple = ()
            for attr in attributes:

                if attr in current_team:
                    attribute_tuple += (current_team[attr],)
                elif attr in ['style']:
                    attribute_tuple += (current_team['formation'][attr],)
                elif attr in ['manager_league', 'manager_nation']:
                    attribute_tuple += (current_team['manager'][attr[8:]],)
                elif attr in ['player']:
                    # Get list of player names
                    player_names = []
                    for position in current_team['formation']['positions'].itervalues():
                        player = position['player']
                        player_names.append(player['name'] + player['commonName'] +
                                            player['firstName'] + player['lastName'])
                    attribute_tuple += (player_names,)
                elif attr in ['total_skillMoves']:
                    # Calculate total
                    total = 0
                    for position in current_team['formation']['positions'].itervalues():
                        player = position['player']
                        total += player[attr[6:]]
                    attribute_tuple += (total,)
                else:
                    print "Invalid Attribute: %s" % attr

            return attribute_tuple

        self.db = sorted(self.db, key=compare, reverse=descend)

    def search(self, attributes):
        """
        Search for teams
        Input: A dictionary the attribute values, and the optional comparison type
        Comparison: 'higher', 'exact', 'lower', 'not'
        Example 1: arguments = {'attr1': (value1, 'exact')}
        or without the comparison operator
        Example 2: arguments = {'attr1': (value1,), 'attr2': (value2,), 'attr3': (value3,)}
        Output: A list of all matching teams
        """

        teams = []

        for team in self.db:
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
                    print "Compare value is not valid. Use 'higher', 'exact', 'not', or 'lower'."
                    return []

                if attribute in ['formation']:
                    string_value = str(value.upper())
                    stat = str(team[attribute]['name'].upper())
                    if compare == 'higher':
                        if not stat >= string_value:
                            match = False
                    elif compare == 'exact':
                        if stat != string_value:
                            match = False
                    elif compare == 'lower':
                        if not stat <= string_value:
                            match = False
                elif attribute in ['manager_league', 'manager_nation']:
                    string_value = str(value.upper())
                    stat = str(team[attribute[:7]][attribute[8:]].upper())
                    if compare == 'higher':
                        if not stat >= string_value:
                            match = False
                    elif compare == 'exact':
                        if stat != string_value:
                            match = False
                    elif compare == 'lower':
                        if not stat <= string_value:
                            match = False
                elif attribute in ['rating', 'total_ic', 'chemistry', 'strength']:
                    if compare == 'higher':
                        if not team[attribute] >= value:
                            match = False
                    elif compare == 'exact':
                        if not team[attribute] == value:
                            match = False
                    elif compare == 'lower':
                        if not team[attribute] <= value:
                            match = False
                elif attribute in ['total_skillMoves']:
                    # Calculate total
                    total = 0
                    for position in team['formation']['positions'].itervalues():
                        player = position['player']
                        total += player[attribute[6:]]
                    if compare == 'higher':
                        if not total >= value:
                            match = False
                    elif compare == 'exact':
                        if not total == value:
                            match = False
                    elif compare == 'lower':
                        if not total <= value:
                            match = False
                elif attribute in ['style']:
                    string_value = value.upper()
                    stat = team['formation']['style'].upper()
                    if not stat.startswith(string_value):
                        match = False
                elif attribute in ['player']:
                    if not Team(team).has_player(value):
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
                teams.append(copy.deepcopy(team))

        return teams

    def print_db(self, num_results=None):
        """
        Print out the information of all of the teams in the database
        Input: The number of results to print out
        Output: None  -  prints the results to the console
        """

        # Sort DB by rating
        self.sort({'rating'})

        if num_results is None:
            num_results = len(self.db)

        # Iterate and print out all of the teams
        for team in self.db[:num_results]:
            rating = 'Rating: ' + str(team['rating'])[:5] + '0' * (5 - len(str(team['rating'])[:5]))
            chemistry = 'Chemistry: ' + str(team['chemistry']) + ' (' + str(team['total_ic']) + ')'
            formation = team['formation']['name']
            manager = 'Manager League: ' + team['manager']['league'] + ',' + \
                      ' ' * (25 - len(team['manager']['league'])) + 'Manager Nation: ' + team['manager']['nation']

            print rating + ' ' * (20 - len(rating)) + chemistry + ' ' * (27 - len(chemistry)) + \
                formation + ' ' * (16 - len(formation)) + manager
