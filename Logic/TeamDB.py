import copy
import json
from os.path import isfile


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
            print "File already exists."
            return False

        return True

    def load(self, file_name):
        """
        Load the database from the specified file name
        Input: The name of the database to load
        Output: True  -  the database is loaded into the TeamDB object
        """

        del self.db[:]  # Empty existing DB list

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
                else:
                    print "Invalid Attribute: %s" % attr

            return attribute_tuple

        self.db = sorted(self.db, key=compare, reverse=descend)

    def search(self, attributes, compare='exact'):
        """
        Search for teams
        Input: A dictionary the attributes and values, and the optional comparison type('higher', 'exact', 'lower')
        Example 1: arguments = {'attr1': value1}, 'exact'
        or without the comparison operator
        Example 2: arguments = {'attr1': value1, 'attr2': value2, 'attr3': value3}
        Output: A list of all matching teams
        """

        teams = []

        if not (compare == 'higher' or compare == 'exact' or compare == 'lower'):
            print "Compare field is not valid. Use 'higher', 'exact', or 'lower'."
            return teams

        for team in self.db:
            match = True
            for attribute, value in attributes.iteritems():
                if attribute == 'formation':
                    string_value = str(value.upper())
                    stat = str(team['formation']['name'].upper())
                    if compare == 'higher':
                        if not stat >= string_value:
                            match = False
                    elif compare == 'exact':
                        if stat != string_value:
                            match = False
                    elif compare == 'lower':
                        if not stat <= string_value:
                            match = False
                elif attribute == 'manager_league':
                    string_value = str(value.upper())
                    stat = str(team['manager']['league'].upper())
                    if compare == 'higher':
                        if not stat >= string_value:
                            match = False
                    elif compare == 'exact':
                        if stat != string_value:
                            match = False
                    elif compare == 'lower':
                        if not stat <= string_value:
                            match = False
                elif attribute == 'manager_nation':
                    string_value = str(value.upper())
                    stat = str(team['manager']['nation'].upper())
                    if compare == 'higher':
                        if not stat >= string_value:
                            match = False
                    elif compare == 'exact':
                        if stat != string_value:
                            match = False
                    elif compare == 'lower':
                        if not stat <= string_value:
                            match = False
                elif attribute == 'rating':
                    if compare == 'higher':
                        if not team[attribute] >= value:
                            match = False
                    elif compare == 'exact':
                        if not team[attribute] == value:
                            match = False
                    elif compare == 'lower':
                        if not team[attribute] <= value:
                            match = False
                elif attribute == 'total_ic':
                    if compare == 'higher':
                        if not team[attribute] >= value:
                            match = False
                    elif compare == 'exact':
                        if not team[attribute] == value:
                            match = False
                    elif compare == 'lower':
                        if not team[attribute] <= value:
                            match = False
                elif attribute == 'chemistry':
                    if compare == 'higher':
                        if not team[attribute] >= value:
                            match = False
                    elif compare == 'exact':
                        if not team[attribute] == value:
                            match = False
                    elif compare == 'lower':
                        if not team[attribute] <= value:
                            match = False
                elif attribute == 'style':
                    string_value = value.upper()
                    stat = team['formation']['style'].upper()
                    if not stat.startswith(string_value):
                        match = False
                else:
                    print "Invalid Attribute: %s" % attribute
                    match = False
                    break

                if not match:
                    break

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
