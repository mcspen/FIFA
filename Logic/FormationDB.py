import copy
import json
from os.path import isfile
import sys


class FormationDB:
    """
    The FormationDB class contains a list of formations.
    """

    def __init__(self, db_input=None):
        """
        Initialization function - creates either a blank dict or copies one from input
        Input: Optional formation database dictionary
        Output: None  -  the database is created
        """

        if db_input is None:
            db_input = []
        elif type(db_input) != list:
            db_input = [db_input]
        self.db = copy.deepcopy(db_input)

    def add_formation(self, formation):
        """
        Add a new formation to the database
        Input: Formation
        Output: None  -  the formation is added to the database
        """

        self.db.append(copy.deepcopy(formation.__dict__))

    def save(self, file_name, file_type):
        """
        Save the database to the specified file name and overwrite the data
        Input: The name of the database to save, and the type of the file ('db' or 'list')
        Output: True  -  the database is saved in the file
        """

        if file_type == 'db':
            # Create filename from file name and file type
            file_name = 'form_db_' + file_name

        elif file_type == 'list':
            # Create filename from file name and file type
            file_name = 'form_lt_' + file_name

        else:
            print "Invalid file type. Must be 'db' or 'list'."
            return False

        file_path = 'JSONs/' + file_name + '.json'

        if not isfile(file_path):
            with open(file_path, 'w') as f:
                json.dump(self.db, f)
                f.close()

        else:
            print "File already exists."
            return False

        return True

    def load(self, file_name, file_type):
        """
        Load the database from the specified file name
        Input: The name of the database to load, and the type of the file ('db' or 'list')
        Output: True  -  the database is loaded into the FormationDB object
        """

        del self.db[:]  # Empty existing DB list

        if file_type == 'db':
            # Create filename from file name and file type
            file_name = 'form_db_' + file_name

        elif file_type == 'list':
            # Create filename from file name and file type
            file_name = 'form_lt_' + file_name

        else:
            print "Invalid file type. Must be 'db' or 'list'."
            return False

        file_path = 'JSONs/' + file_name + '.json'

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
        Sort the formations database or list
        Input: A list of attributes and the optional order boolean
        Example 1: arguments = ['attr1', 'attr2', 'attr3'], False
        or without the comparison operator
        Example 2: arguments = ['attr1', 'attr2']
        Output: None  -  the database is sorted
        """

        def compare(current_formation):
            """
            Based on the list of attributes, return a tuple of attributes for the current formation.
            Input: The current formation.
            Output: A tuple of attributes to compare with.
            """

            attribute_tuple = ()
            for attr in attributes:

                if attr in current_formation:
                    attribute_tuple += (current_formation[attr],)
                else:
                    print "Invalid Attribute: %s" % attr

            return attribute_tuple

        self.db = sorted(self.db, key=compare, reverse=descend)

    def search(self, attributes):
        """
        Search for formations
        Input: A dictionary the attributes and values, and the optional comparison type
        ('higher', 'exact', 'lower', 'not')
        Example 1: arguments = {'attr1': (value1, 'exact')}
        or multiple
        Example 2: arguments = {'attr1': (value1, 'exact'), 'attr2': (value2, 'exact'), 'attr3': (value3, 'exact')}
        Output: A list of all matching formations
        """

        formations = []

        for formation in self.db:
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

                if attribute == 'name':
                    string_value = str(value.upper())
                    stat = str(formation['name'].upper())
                    if compare == 'higher':
                        if not stat >= string_value:
                            match = False
                    elif compare == 'exact':
                        if stat != string_value:
                            match = False
                    elif compare == 'lower':
                        if not stat <= string_value:
                            match = False
                elif attribute == 'style':
                    string_value = value.upper()
                    stat = formation['style'].upper()
                    if not stat.startswith(string_value):
                        match = False
                elif attribute == 'description':
                    string_value = value.upper()
                    stat = formation['description'].upper()
                    if string_value not in stat:
                        match = False
                elif attribute in ['num_links', 'num_defenders', 'num_midfielders', 'num_attackers']:
                    if compare == 'higher':
                        if not formation[attribute] >= value:
                            match = False
                    elif compare == 'exact':
                        if not formation[attribute] == value:
                            match = False
                    elif compare == 'lower':
                        if not formation[attribute] <= value:
                            match = False
                elif attribute == 'custom_position':
                    string_value = str(value.upper())
                    if string_value not in formation['positions']:
                        match = False
                elif attribute == 'position':
                    string_value = str(value.upper())
                    symbol_list = []
                    for position in formation['positions'].itervalues():
                        symbol_list.append(position['symbol'])
                    if string_value not in symbol_list:
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

            if match:
                formations.append(copy.deepcopy(formation))

        return formations

    def print_db(self, formation_name='all'):
        """
        Print out the formations and positions
        Input: Optional formation name
        Output: None  -  prints the results to the console
        """

        # Iterate and print out all of the formations
        for formation in self.db:
            if formation['name'] == formation_name or formation_name == 'all':
                # Print out formation info
                print "===============| %s |===============" % formation['name']
                print "Style: %s" % formation['style']
                print "Description: %s" % formation['description']
                print "Number of Links: %s" % formation['num_links']

                # Print out goalkeeper
                print "\nGoalkeeper: 1"
                position = formation['positions']['GK']
                links = 'Links: '
                for link in position['links']:
                    links += link + ', '
                print "%s%s%s%s%s%s%s" % (position['name'],        " " * (35-len(position['name'])),
                                          position['symbol'],      " " * (5-len(position['symbol'])),
                                          'GK',                    " " * (5-len('GK')),
                                          links)

                # Print out defense
                index = 1
                print "\nDefense: %d" % formation['num_defenders']
                while index < 1 + formation['num_defenders']:
                    for custom_symbol, position in formation['positions'].iteritems():
                        if index == position['index']:
                            links = 'Links: '
                            for link in position['links']:
                                links += link + ', '
                            print "%s%s%s%s%s%s%s" % (position['name'],        " " * (35-len(position['name'])),
                                                      position['symbol'],      " " * (5-len(position['symbol'])),
                                                      custom_symbol,           " " * (5-len(custom_symbol)),
                                                      links)
                            index += 1
                            break

                # Print out midfield
                index = 1 + formation['num_defenders']
                print "\nMidfield: %d" % formation['num_midfielders']
                while index < 1 + formation['num_defenders'] + formation['num_midfielders']:
                    for custom_symbol, position in formation['positions'].iteritems():
                        if index == position['index']:
                            links = 'Links: '
                            for link in position['links']:
                                links += link + ', '
                            print "%s%s%s%s%s%s%s" % (position['name'],        " " * (35-len(position['name'])),
                                                      position['symbol'],      " " * (5-len(position['symbol'])),
                                                      custom_symbol,           " " * (5-len(custom_symbol)),
                                                      links)
                            index += 1
                            break

                # Print out offense
                index = 1 + formation['num_defenders'] + formation['num_midfielders']
                print "\nOffense: %d" % formation['num_attackers']
                while index < 1 + formation['num_defenders'] + formation['num_midfielders'] + \
                        formation['num_attackers']:
                    for custom_symbol, position in formation['positions'].iteritems():
                        if index == position['index']:
                            links = 'Links: '
                            for link in position['links']:
                                links += link + ', '
                            print "%s%s%s%s%s%s%s" % (position['name'],        " " * (35-len(position['name'])),
                                                      position['symbol'],      " " * (5-len(position['symbol'])),
                                                      custom_symbol,           " " * (5-len(custom_symbol)),
                                                      links)
                            index += 1
                            break
                print ''

    def print_db_short(self, formation_name='all'):
        """
        Print out the concise version of the formations
        Input: Optional formation name
        Output: None  -  prints the results to the console
        """

        # Print out column labels
        print "%s%s%s%s%s%s%s" % ("Formation:", " " * (15-len("Formation:")),
                                  "Style:", " " * (15-len("Style:")),
                                  "# Links:", " " * (10-len("# Links:")),
                                  "Description:")

        # Iterate and print out all of the formations
        for formation in self.db:
            if formation['name'] == formation_name or formation_name == 'all':
                # Print out formation info
                print "%s%s%s%s%s%s%s" % (formation['name'], " " * (15-len(formation['name'])),
                                          formation['style'], " " * (15-len(formation['style'])),
                                          formation['num_links'], " " * (10-len(str(formation['num_links']))),
                                          formation['description'])

    def print_positions(self, formation_name='all', symbol='normal'):
        """
        Print out the positions of the specified formation, kind of in the shape of a field to give a general idea
        Input: The formation name to be printed and the type of symbol to print (normal or custom)
        Output: None  -  prints the positions to the console
        """

        for formation in self.db:
            if (formation['name'] == formation_name) or (formation_name == 'all'):

                # Print out the formation name
                print "Formation: %s" % formation['name']

                width = 50

                # Get the width of all the attackers' symbols
                symbol_width = 0
                index = 1 + formation['num_defenders'] + formation['num_midfielders']
                while index < 1 + formation['num_defenders'] + formation['num_midfielders'] + \
                        formation['num_attackers']:
                    for custom_symbol, position in formation['positions'].iteritems():
                        if index == position['index']:
                            if symbol == 'normal':
                                symbol_width += len(position['symbol'])
                            else:
                                symbol_width += len(custom_symbol)
                            index += 1
                            break

                # Calculate spacing between attackers
                space = (width - symbol_width)/(formation['num_attackers']+1)

                # Print out the attackers
                index = 1 + formation['num_defenders'] + formation['num_midfielders']
                sys.stdout.write("Off:  %s" % (' ' * space))
                while index < 1 + formation['num_defenders'] + formation['num_midfielders'] + \
                        formation['num_attackers']:
                    for custom_symbol, position in formation['positions'].iteritems():
                        if index == position['index']:
                            if symbol == 'normal':
                                sys.stdout.write("%s%s" % (position['symbol'], ' ' * space))
                            else:
                                sys.stdout.write("%s%s" % (custom_symbol, ' ' * space))
                            index += 1
                            break

                sys.stdout.write('\n')

                print ''

                # Get the width of all the midfielders' symbols
                symbol_width = 0
                index = 1 + formation['num_defenders']
                while index < 1 + formation['num_defenders'] + formation['num_midfielders']:
                    for custom_symbol, position in formation['positions'].iteritems():
                        if index == position['index']:
                            if symbol == 'normal':
                                symbol_width += len(position['symbol'])
                            else:
                                symbol_width += len(custom_symbol)
                            index += 1
                            break

                # Calculate spacing between midfielders
                space = (width - symbol_width)/(formation['num_midfielders']+1)

                # Print out the midfielders
                index = 1 + formation['num_defenders']
                sys.stdout.write("Mid:  %s" % (' ' * space))
                while index < 1 + formation['num_defenders'] + formation['num_midfielders']:
                    for custom_symbol, position in formation['positions'].iteritems():
                        if index == position['index']:
                            if symbol == 'normal':
                                sys.stdout.write("%s%s" % (position['symbol'], ' ' * space))
                            else:
                                sys.stdout.write("%s%s" % (custom_symbol, ' ' * space))
                            index += 1
                            break

                sys.stdout.write('\n')

                print ''

                # Get the width of all the defenders' symbols
                symbol_width = 0
                index = 1
                while index < 1 + formation['num_defenders']:
                    for custom_symbol, position in formation['positions'].iteritems():
                        if index == position['index']:
                            if symbol == 'normal':
                                symbol_width += len(position['symbol'])
                            else:
                                symbol_width += len(custom_symbol)
                            index += 1
                            break

                # Calculate spacing between defenders
                space = (width - symbol_width)/(formation['num_defenders']+1)

                # Print out the defenders
                index = 1
                sys.stdout.write("Def:  %s" % (' ' * space))
                while index < 1 + formation['num_defenders']:
                    for custom_symbol, position in formation['positions'].iteritems():
                        if index == position['index']:
                            if symbol == 'normal':
                                sys.stdout.write("%s%s" % (position['symbol'], ' ' * space))
                            else:
                                sys.stdout.write("%s%s" % (custom_symbol, ' ' * space))
                            index += 1
                            break

                sys.stdout.write('\n')

                print ''

                # Print out the goalkeeper
                space = (width - 2) / 2
                print "Goal: %s%s%s" % (' ' * space, 'GK', ' ' * space)

                sys.stdout.write('\n')
