import copy
import json
import sys
from HelperFunctions import ascii_text, format_attr_name, convert_height

from PlayerDB import PlayerDB
import UltimateTeamFunctions


class Team:
    """
    The Team class contains:
        manager: The given or suggested manager traits
        total_ic: The total individual chemistry of the team (non-rounded chemistry value)
        chemistry: The total chemistry of the team (max of 100)
        rating: The rating of the team
        strength: The rating of the team's strengths (traits, high stats, etc.)
        formation: The formation of the team.
    """

    def __init__(self, input_dict=None):
        """
        Initialization function - creates either a blank dict or copies one from input
        Input: Optional team dictionary
        Output: None  -  the team is created
        """

        if input_dict is None:
            self.manager = {}
            self.total_ic = 0
            self.chemistry = 0
            self.rating = 0
            self.strength = 0
            self.formation = {}
        else:
            self.manager = copy.deepcopy(input_dict['manager'])
            self.total_ic = input_dict['total_ic']
            self.chemistry = input_dict['chemistry']
            self.rating = input_dict['rating']
            #self.strength = input_dict['strength']
            self.formation = copy.deepcopy(input_dict['formation'])

            # TEMPORARY UNTIL ALL TEAMS HAVE STRENGTHS------------------------------------------------------------------
            if 'strength' in input_dict:
                self.strength = input_dict['strength']
            else:
                self.strength = 0
            # TEMPORARY UNTIL ALL TEAMS HAVE STRENGTHS------------------------------------------------------------------

    def set_team(self, formation, roster, manager=None, loyalty=True):
        """
        Create a new team from the individual parts
        Input: The input 'formation' is: a dictionary of all the positions and the players
                                         optional manager
                                         optional loyalty
        Output: None  -  the team is created
        """

        # Assign formation and manager from input
        # If manager is not assigned, one will be advised when calculating chemistry
        self.formation = copy.deepcopy(formation)
        if manager is None:
            self.manager = {}
        else:
            self.manager = copy.deepcopy(manager)

        # Assign all players into the formation (and assign chemistry loyalty)
        for position, player in roster.iteritems():
            if position in self.formation['positions']:
                self.formation['positions'][position]['player'] = copy.deepcopy(player)
                self.formation['positions'][position]['chemistry'] = 0
                self.formation['positions'][position]['loyalty'] = loyalty
                self.formation['positions'][position]['strengths'] = []
                self.formation['positions'][position]['strength_rating'] = 0

            else:
                print "Error: Invalid position"

        # Calculate the team rating
        # According to Reddit, Team Rating = Average Rating of all 18 players (7 bench) + a Correctional Factor
        # CF = ((IR1 - AR) + ... + (IR11 - AR) + (IR12 - AR)/2 + ... + (IR18 - AR)/2) / 18
        # CF = Correctional Factor, IR = Individual Player Rating, AR = Average rating of all 18 players
        team_total = 0.0
        for player in roster.itervalues():
            team_total += player['rating']

        self.rating = team_total / len(roster)

        # Calculate the team chemistry
        self.calculate_chemistry()

        # Calculate the team strength
        self.calculate_strength()

    def save(self, team_name):
        """
        Save the team to the specified file name and overwrite the data
        Input: The name of the team
        Output: True  -  the team is saved in the file
        """

        # Create filename from team name
        filename = 'JSONs/' + team_name + '.json'

        with open(filename, 'w') as f:
            json.dump(self.__dict__, f)
            f.close()

        return True

    def load(self, team_name):
        """
        Load the team with the specified team name
        Input: The name of the team to load
        Output: True  -  the team is loaded from the file
        """

        # Delete/clear/reassign existing team items
        if self.manager is not None:
            self.manager.clear()
        self.chemistry = 0
        self.rating = 0
        if len(self.formation) > 0:
            self.formation.clear()

        # Create filename from team name
        filename = 'JSONs/' + team_name + '.json'

        with open(filename, 'r') as f:
            self.__init__(json.load(f))
            f.close()

        return True

    def has_player(self, player_name):
        """
        Checks if the player is on the team
        Input: The player name or part of name
        Output: Boolean value of if player is on team
        """

        has_player = False
        name = player_name.upper()

        # Only starting initial
        if len(name) == 1:
            for position in self.formation['positions'].itervalues():
                player = position['player']

                if (player['commonName'].upper().startswith(name) or
                        player['firstName'].upper().startswith(name) or
                        player['lastName'].upper().startswith(name) or
                        player['name'].upper().startswith(name)):
                    has_player = True
                    break

        # Find part of name anywhere
        else:
            for position in self.formation['positions'].itervalues():
                player = position['player']

                if (name in player['commonName'].upper()) or \
                   (name in player['firstName'].upper()) or \
                   (name in player['lastName'].upper()) or \
                   (name in player['name'].upper()):
                    has_player = True
                    break

        return has_player

    def print_roster(self, symbol='normal'):
        """
        Print out the roster of the team
        Input: Optional - symbol type to be printed
        Output: None  -  Prints the roster to the console
        """

        # Print out the roster info
        print "Roster:"
        print "Rating: %d" % self.rating
        print "Chemistry: %d" % self.chemistry
        print "Formation: %s" % self.formation['name']

        index = 0
        while index < 1 + self.formation['num_defenders'] + self.formation['num_midfielders'] + \
                self.formation['num_attackers']:
            for position, player in self.formation['positions'].iteritems():
                if player['index'] == index:
                    name = ascii_text(player['player']['firstName']) + " " + ascii_text(player['player']['lastName'])
                    if player['player']['commonName'] != '':
                        name = ascii_text(player['player']['commonName'])
                    if symbol == 'normal':
                        symbol_to_print = player['symbol']
                    else:
                        symbol_to_print = position
                    print'%s%s%s%s' % (symbol_to_print, ':', ' ' * (6 - len(symbol_to_print)), name)
                    index += 1

    def print_roster_sections(self):
        """
        Print out the roster of the team by area of the field
        Input: None
        Output: None  -   prints the roster to the console
        """

        # Print out the roster info
        print "Roster:"
        print "Formation: %s" % self.formation['name']

        # Print out goalkeeper info
        goalkeeper = self.formation['positions']['GK']['player']
        name = ascii_text(goalkeeper['firstName']) + " " + ascii_text(goalkeeper['lastName'])
        if goalkeeper['commonName'] != '':
            name = ascii_text(goalkeeper['commonName'])
        print "Goalkeeper: " + name

        # Print out defenders info
        sys.stdout.write("Def:  ")
        index = 1
        while index < 1 + self.formation['num_defenders']:
            for player in self.formation['positions'].itervalues():
                if player['index'] == index:
                    defender = player['player']
                    name = ascii_text(defender['firstName']) + " " + ascii_text(defender['lastName'])
                    if defender['commonName'] != '':
                        name = ascii_text(defender['commonName'])
                    sys.stdout.write('%s   ' % name)
                    index += 1
        sys.stdout.write('\n')

        # Print out midfielders info
        sys.stdout.write("Mid:  ")
        index = 1 + self.formation['num_defenders']
        while index < 1 + self.formation['num_defenders'] + self.formation['num_midfielders']:
            for player in self.formation['positions'].itervalues():
                if player['index'] == index:
                    midfielder = player['player']
                    name = ascii_text(midfielder['firstName']) + " " + ascii_text(midfielder['lastName'])
                    if midfielder['commonName'] != '':
                        name = ascii_text(midfielder['commonName'])
                    sys.stdout.write('%s   ' % name)
                    index += 1
        sys.stdout.write('\n')

        # Print out attackers info
        sys.stdout.write("Off:  ")
        index = 1 + self.formation['num_defenders'] + self.formation['num_midfielders']
        while index < 1 + self.formation['num_defenders'] + self.formation['num_midfielders'] + \
                self.formation['num_attackers']:
            for player in self.formation['positions'].itervalues():
                if player['index'] == index:
                    attacker = player['player']
                    name = ascii_text(attacker['firstName']) + " " + ascii_text(attacker['lastName'])
                    if attacker['commonName'] != '':
                        name = ascii_text(attacker['commonName'])
                    sys.stdout.write('%s   ' % name)
                    index += 1
        sys.stdout.write('\n')

    def print_summary(self):
        """
        Print out the summary info of the team
        Input: None
        Output: None  -  Prints the summary to the console
        """

        # Print out the roster info
        print "Roster:"
        print "Rating: %.2f" % self.rating
        print "Strength: %d" % self.strength
        print "Chemistry: %d" % self.chemistry
        print "Formation: %s" % self.formation['name']

# ====================CHEMISTRY FUNCTIONS========== #

    @staticmethod
    def position_chemistry(natural_position, playing_position):
        """
        Calculate the position chemistry of the player based on natural position and actual position
        Input: The player's normal/natural position and the position the player is playing.
        Output: The position chemistry of the player represented by 0 = red, 1 = orange, 2 = yellow, or 3 = green
        """

        red = 0
        orange = 1
        yellow = 2
        green = 3

        # Players playing in their natural positions are always green
        if playing_position == natural_position:
            return green

        # Goalkeepers only play well in goal
        elif playing_position == 'GK':
            return red

        # Right Back
        elif playing_position == 'RB':
            if natural_position == 'RWB':
                return yellow
            elif (natural_position == 'CB') or (natural_position == 'LB') or (natural_position == 'RM'):
                return orange
            else:
                return red

        # Center Back
        elif playing_position == 'CB':
            if (natural_position == 'RB') or (natural_position == 'LB') or (natural_position == 'CDM'):
                return orange
            else:
                return red

        # Left Back
        elif playing_position == 'LB':
            if natural_position == 'LWB':
                return yellow
            elif (natural_position == 'CB') or (natural_position == 'RB') or (natural_position == 'LM'):
                return orange
            else:
                return red

        # Right Wing Back
        elif playing_position == 'RWB':
            if natural_position == 'RB':
                return yellow
            elif (natural_position == 'LWB') or (natural_position == 'RM') or (natural_position == 'RW'):
                return orange
            else:
                return red

        # Left Wing Back
        elif playing_position == 'LWB':
            if natural_position == 'LB':
                return yellow
            elif (natural_position == 'RWB') or (natural_position == 'LM') or (natural_position == 'LW'):
                return orange
            else:
                return red

        # Center Defensive Mid
        elif playing_position == 'CDM':
            if natural_position == 'CM':
                return yellow
            elif (natural_position == 'CB') or (natural_position == 'CAM'):
                return orange
            else:
                return red

        # Center Mid
        elif playing_position == 'CM':
            if (natural_position == 'CDM') or (natural_position == 'CAM'):
                return yellow
            elif (natural_position == 'RM') or (natural_position == 'LM'):
                return orange
            else:
                return red

        # Center Attacking Mid
        elif playing_position == 'CAM':
            if (natural_position == 'CM') or (natural_position == 'CF'):
                return yellow
            elif natural_position == 'CDM':
                return orange
            else:
                return red

        # Right Mid
        elif playing_position == 'RM':
            if natural_position == 'RW':
                return yellow
            elif (natural_position == 'RB') or (natural_position == 'RWB') or \
                    (natural_position == 'CM') or (natural_position == 'LM') or (natural_position == 'RF'):
                return orange
            else:
                return red

        # Left Mid
        elif playing_position == 'LM':
            if natural_position == 'LW':
                return yellow
            elif (natural_position == 'LB') or (natural_position == 'LWB') or \
                    (natural_position == 'CM') or (natural_position == 'RM') or (natural_position == 'LF'):
                return orange
            else:
                return red

        # Right Winger
        elif playing_position == 'RW':
            if (natural_position == 'RM') or (natural_position == 'RF'):
                return yellow
            elif (natural_position == 'RWB') or (natural_position == 'LW'):
                return orange
            else:
                return red

        # Left Winger
        elif playing_position == 'LW':
            if (natural_position == 'LM') or (natural_position == 'LF'):
                return yellow
            elif (natural_position == 'LWB') or (natural_position == 'RW'):
                return orange
            else:
                return red

        # Center Forward
        elif playing_position == 'CF':
            if (natural_position == 'CAM') or (natural_position == 'ST'):
                return yellow
            elif (natural_position == 'RF') or (natural_position == 'LF'):
                return orange
            else:
                return red

        # Right Forward
        elif playing_position == 'RF':
            if natural_position == 'RW':
                return yellow
            elif (natural_position == 'RM') or (natural_position == 'CF') or \
                    (natural_position == 'LF') or (natural_position == 'ST'):
                return orange
            else:
                return red

        # Left Forward
        elif playing_position == 'LF':
            if natural_position == 'LW':
                return yellow
            elif (natural_position == 'LM') or (natural_position == 'CF') or \
                    (natural_position == 'RF') or (natural_position == 'ST'):
                return orange
            else:
                return red

        # Striker
        elif playing_position == 'ST':
            if natural_position == 'CF':
                return yellow
            elif (natural_position == 'RF') or (natural_position == 'LF'):
                return orange
            else:
                return red

        # If it isn't one of these, there is an error
        else:
            print "Error: Invalid playing_position: %s" % playing_position
            return -1

    @staticmethod
    def related_positions(natural_position, similarity='yellow'):
        """
        Calculate the position chemistry of the player based on natural position and actual position
        Input: The player's normal/natural position and similarity level.
        Output: The positions related to the natural position with the similarity level specified

        green =  The same position
        yellow = Very closely related positions
        orange = Reasonably related positions
        red    = Not related positions at all
        blue   = Custom level representing red positions that are slightly related
        purple = Custom level representing red positions that barely related
        """

        positions_list = []

        # Check for incorrect similarity levels
        if (similarity != 'green') and (similarity != 'yellow') and (similarity != 'orange')\
                and (similarity != 'red') and (similarity != 'blue') and (similarity != 'purple'):
            print "ERROR: 'similarity' must be 'green', 'yellow', 'orange', 'red', 'blue, or 'purple'."
            return []

        # Green similarity is only for the same position
        if similarity == 'green':
            positions_list = [natural_position]

        # Goalkeepers only play well in goal
        elif natural_position == 'GK':
            if similarity in ['yellow', 'orange', 'blue', 'purple']:
                positions_list = []
            elif similarity == 'red':
                positions_list = ['RB', 'CB', 'LB', 'RWB', 'LWB', 'CDM', 'CM', 'CAM',
                                  'RM', 'LM', 'RW', 'LW', 'CF', 'RF', 'LF', 'ST']
            elif similarity == 'blue':
                positions_list = ['RB', 'CB', 'LB', 'RWB', 'LWB']
            elif similarity == 'purple':
                positions_list = ['CDM', 'CM', 'CAM', 'RM', 'LM']

        # Right Back
        elif natural_position == 'RB':
            if similarity == 'yellow':
                positions_list = ['RWB']
            elif similarity == 'orange':
                positions_list = ['CB', 'LB', 'RM']
            elif similarity == 'red':
                positions_list = ['GK', 'LWB', 'CDM', 'CM', 'CAM', 'LM', 'RW', 'LW', 'CF', 'RF', 'LF', 'ST']
            elif similarity == 'blue':
                positions_list = ['LWB', 'CDM', 'CM', 'LM']
            elif similarity == 'purple':
                positions_list = ['CAM', 'RW', 'LW', 'CF', 'RF', 'LF', 'ST']

        # Center Back
        elif natural_position == 'CB':
            if similarity == 'yellow':
                positions_list = []
            elif similarity == 'orange':
                positions_list = ['RB', 'LB', 'CDM']
            elif similarity == 'red':
                positions_list = ['GK', 'RWB', 'LWB', 'CM', 'CAM', 'RM', 'LM', 'RW', 'LW', 'CF', 'RF', 'LF', 'ST']
            elif similarity == 'blue':
                positions_list = ['RWB', 'LWB', 'CM', 'RM', 'LM']
            elif similarity == 'purple':
                positions_list = ['CAM', 'RW', 'LW', 'CF', 'RF', 'LF', 'ST']

        # Left Back
        elif natural_position == 'LB':
            if similarity == 'yellow':
                positions_list = ['LWB']
            elif similarity == 'orange':
                positions_list = ['CB', 'RB', 'LM']
            elif similarity == 'red':
                positions_list = ['GK', 'RWB', 'CDM', 'CM', 'CAM', 'RM', 'RW', 'LW', 'CF', 'RF', 'LF', 'ST']
            elif similarity == 'blue':
                positions_list = ['RWB', 'CDM', 'CM', 'RM']
            elif similarity == 'purple':
                positions_list = ['CAM', 'RW', 'LW', 'CF', 'RF', 'LF', 'ST']

        # Right Wing Back
        elif natural_position == 'RWB':
            if similarity == 'yellow':
                positions_list = ['RB']
            elif similarity == 'orange':
                positions_list = ['LWB', 'RM', 'RW']
            elif similarity == 'red':
                positions_list = ['GK', 'CB', 'LB', 'CDM', 'CM', 'CAM', 'LM', 'LW', 'CF', 'RF', 'LF', 'ST']
            elif similarity == 'blue':
                positions_list = ['CB', 'LB', 'CDM', 'CM', 'LM']
            elif similarity == 'purple':
                positions_list = ['CAM', 'LW', 'CF', 'RF', 'LF', 'ST']

        # Left Wing Back
        elif natural_position == 'LWB':
            if similarity == 'yellow':
                positions_list = ['LB']
            elif similarity == 'orange':
                positions_list = ['RWB', 'LM', 'LW']
            elif similarity == 'red':
                positions_list = ['GK', 'RB', 'CB', 'CDM', 'CM', 'CAM', 'RM', 'RW', 'CF', 'RF', 'LF', 'ST']
            elif similarity == 'red':
                positions_list = ['RB', 'CB', 'CDM', 'CM', 'RM']
            elif similarity == 'red':
                positions_list = ['CAM', 'RW', 'CF', 'RF', 'LF', 'ST']

        # Center Defensive Mid
        elif natural_position == 'CDM':
            if similarity == 'yellow':
                positions_list = ['CM']
            elif similarity == 'orange':
                positions_list = ['CB', 'CAM']
            elif similarity == 'red':
                positions_list = ['GK', 'RB', 'LB', 'RWB', 'LWB', 'RM', 'LM', 'RW', 'LW', 'CF', 'RF', 'LF', 'ST']
            elif similarity == 'blue':
                positions_list = ['RB', 'LB', 'RWB', 'LWB', 'RM', 'LM']
            elif similarity == 'purple':
                positions_list = ['RW', 'LW', 'CF', 'RF', 'LF', 'ST']

        # Center Mid
        elif natural_position == 'CM':
            if similarity == 'yellow':
                positions_list = ['CDM', 'CAM']
            elif similarity == 'orange':
                positions_list = ['RM', 'LM']
            elif similarity == 'red':
                positions_list = ['GK', 'RB', 'CB', 'LB', 'RWB', 'LWB', 'RW', 'LW', 'CF', 'RF', 'LF', 'ST']
            elif similarity == 'blue':
                positions_list = ['CB', 'RW', 'LW', 'CF']
            elif similarity == 'purple':
                positions_list = ['RB', 'LB', 'RWB', 'LWB', 'RF', 'LF', 'ST']

        # Center Attacking Mid
        elif natural_position == 'CAM':
            if similarity == 'yellow':
                positions_list = ['CM', 'CF']
            elif similarity == 'orange':
                positions_list = ['CDM']
            elif similarity == 'red':
                positions_list = ['GK', 'RB', 'CB', 'LB', 'RWB', 'LWB', 'RM', 'LM', 'RW', 'LW', 'RF', 'LF', 'ST']
            elif similarity == 'blue':
                positions_list = ['RM', 'LM', 'RW', 'LW', 'RF', 'LF', 'ST']
            elif similarity == 'purple':
                positions_list = ['RB', 'CB', 'LB', 'RWB', 'LWB']

        # Right Mid
        elif natural_position == 'RM':
            if similarity == 'yellow':
                positions_list = ['RW']
            elif similarity == 'orange':
                positions_list = ['RB', 'RWB', 'CM', 'LM', 'RF']
            elif similarity == 'red':
                positions_list = ['GK', 'CB', 'LB', 'LWB', 'CDM', 'CAM', 'LW', 'CF', 'LF', 'ST']
            elif similarity == 'blue':
                positions_list = ['LWB', 'CDM', 'CAM', 'LW']
            elif similarity == 'purple':
                positions_list = ['CB', 'LB', 'CF', 'LF', 'ST']

        # Left Mid
        elif natural_position == 'LM':
            if similarity == 'yellow':
                positions_list = ['LW']
            elif similarity == 'orange':
                positions_list = ['LB', 'LWB', 'CM', 'RM', 'LF']
            elif similarity == 'red':
                positions_list = ['GK', 'RB', 'CB', 'RWB', 'CDM', 'CAM', 'RW', 'CF', 'RF', 'ST']
            elif similarity == 'blue':
                positions_list = ['RWB', 'CDM', 'CAM', 'RW']
            elif similarity == 'purple':
                positions_list = ['RB', 'CB', 'CF', 'RF', 'ST']

        # Right Winger
        elif natural_position == 'RW':
            if similarity == 'yellow':
                positions_list = ['RM', 'RF']
            elif similarity == 'orange':
                positions_list = ['RWB', 'LW']
            elif similarity == 'red':
                positions_list = ['GK', 'RB', 'CB', 'LB', 'LWB', 'CDM', 'CM', 'CAM', 'LM', 'CF', 'LF', 'ST']
            elif similarity == 'blue':
                positions_list = ['LWB', 'CM', 'CAM', 'LM', 'CF', 'LF', 'ST']
            elif similarity == 'purple':
                positions_list = ['RB', 'CB', 'LB', 'CDM']

        # Left Winger
        elif natural_position == 'LW':
            if similarity == 'yellow':
                positions_list = ['LM', 'LF']
            elif similarity == 'orange':
                positions_list = ['LWB', 'RW']
            elif similarity == 'red':
                positions_list = ['GK', 'RB', 'CB', 'LB', 'RWB', 'CDM', 'CM', 'CAM', 'RM', 'CF', 'RF', 'ST']
            elif similarity == 'blue':
                positions_list = ['RWB', 'CM', 'CAM', 'RM', 'CF', 'RF', 'ST']
            elif similarity == 'purple':
                positions_list = ['RB', 'CB', 'LB', 'CDM']

        # Center Forward
        elif natural_position == 'CF':
            if similarity == 'yellow':
                positions_list = ['CAM', 'ST']
            elif similarity == 'orange':
                positions_list = ['RF', 'LF']
            elif similarity == 'red':
                positions_list = ['GK', 'RB', 'CB', 'LB', 'RWB', 'LWB', 'CDM', 'CM', 'RM', 'LM', 'RW', 'LW']
            elif similarity == 'blue':
                positions_list = ['CM', 'RM', 'LM', 'RW', 'LW']
            elif similarity == 'purple':
                positions_list = ['RB', 'CB', 'LB', 'RWB', 'LWB', 'CDM']

        # Right Forward
        elif natural_position == 'RF':
            if similarity == 'yellow':
                positions_list = ['RW']
            elif similarity == 'orange':
                positions_list = ['RM', 'CF', 'LF', 'ST']
            elif similarity == 'red':
                positions_list = ['GK', 'RB', 'CB', 'LB', 'RWB', 'LWB', 'CDM', 'CM', 'CAM', 'LM', 'LW']
            elif similarity == 'blue':
                positions_list = ['CM', 'CAM', 'LM', 'LW']
            elif similarity == 'purple':
                positions_list = ['RB', 'CB', 'LB', 'RWB', 'LWB', 'CDM']

        # Left Forward
        elif natural_position == 'LF':
            if similarity == 'yellow':
                positions_list = ['LW']
            elif similarity == 'orange':
                positions_list = ['LM', 'CF', 'RF', 'ST']
            elif similarity == 'red':
                positions_list = ['GK', 'RB', 'CB', 'LB', 'RWB', 'LWB', 'CDM', 'CM', 'CAM', 'RM', 'RW']
            elif similarity == 'blue':
                positions_list = ['CM', 'CAM', 'RM', 'RW']
            elif similarity == 'purple':
                positions_list = ['RB', 'CB', 'LB', 'RWB', 'LWB', 'CDM']

        # Striker
        elif natural_position == 'ST':
            if similarity == 'yellow':
                positions_list = ['CF']
            elif similarity == 'orange':
                positions_list = ['RF', 'LF']
            elif similarity == 'red':
                positions_list = ['GK', 'RB', 'CB', 'LB', 'RWB', 'LWB', 'CDM', 'CM', 'CAM', 'RM', 'LM', 'RW', 'LW']
            elif similarity == 'blue':
                positions_list = ['CM', 'CAM', 'RM', 'LM', 'RW', 'LW']
            elif similarity == 'purple':
                positions_list = ['RB', 'CB', 'LB', 'RWB', 'LWB', 'CDM']

        # If it isn't one of these, there is an error
        else:
            print "Error: Invalid playing_position: %s" % natural_position
            return []

        return positions_list

    @staticmethod
    def teammate_chemistry(player, teammate):
        """
        Calculate the link chemistry between a player and one teammate
        Input: The player and the teammate
        Output: The teammate chemistry of the link represented by 0 = red, 1 = orange, 2 = yellow, or 3 = green
        """

        red = 0
        orange = 1
        yellow = 2
        green = 3

        nationality = False
        league = False
        club = False

        if player['nation']['id'] == teammate['nation']['id']:
            nationality = True

        if player['league']['id'] == teammate['league']['id']:
            league = True

        if player['club']['id'] == teammate['club']['id']:
            club = True

        # Edited these functions because database has league wrong for a bunch of players
        if nationality and club:  # if nationality and league and club:
            return green

        elif (nationality and league) or club:  # elif (nationality and league) or (league and club):
            return yellow

        elif nationality or league:  # elif nationality or league or club:
            return orange

        elif (not nationality) and (not league) and (not club):
            return red

        else:
            print "Error: Invalid link relation"
            return -1

    def links_chemistry(self, position):
        """
        Calculate the link chemistry between a player and all linked teammates
        Input: The player
        Output: The link chemistry, L, represented by a float between 0 and 3
        """

        # Calculate the sum of all the link chemistry for the player
        sum_links = 0
        for symbol in position['links']:
            sum_links += self.teammate_chemistry(position['player'], self.formation['positions'][symbol]['player'])

        # Return the link chemistry as a float
        return (sum_links + 0.0) / len(position['links'])

    @staticmethod
    def position_links_chemistry(links_chemistry, position_chemistry):
        """
        Calculate the position and links chemistry (PLC) for a player
        Input: The player's position chemistry and links chemistry
        Output: The position and links chemistry, represent by an integer in the range of 0 and 10
        """

        # Check links chemistry value
        if (links_chemistry < 0) or (links_chemistry > 3):
            print "Error: Invalid links chemistry value: %d" % links_chemistry
            return -1

        # Check position chemistry value
        if (position_chemistry != 0) and (position_chemistry != 1) and\
                (position_chemistry != 2) and (position_chemistry != 3):
            print "Error: Invalid position chemistry value: %d" % position_chemistry
            return -1

        # Red position chemistry
        if position_chemistry == 0:
            if links_chemistry < 0.3:
                return 0
            elif links_chemistry < 1:
                return 1
            elif links_chemistry <= 1.6:
                return 2
            elif links_chemistry <= 3:
                return 2
            else:
                print "Error: Invalid links chemistry value: %d" % links_chemistry
                return -1

        # Orange position chemistry
        elif position_chemistry == 1:
            if links_chemistry < 0.3:
                return 1
            elif links_chemistry < 1:
                return 3
            elif links_chemistry <= 1.6:
                return 5
            elif links_chemistry <= 3:
                return 5
            else:
                print "Error: Invalid links chemistry value: %d" % links_chemistry
                return -1

        # Yellow position chemistry
        elif position_chemistry == 2:
            if links_chemistry < 0.3:
                return 2
            elif links_chemistry < 1:
                return 5
            elif links_chemistry <= 1.6:
                return 8
            elif links_chemistry <= 3:
                return 9
            else:
                print "Error: Invalid links chemistry value: %d" % links_chemistry
                return -1

        # Green position chemistry
        elif position_chemistry == 3:
            if links_chemistry < 0.3:
                return 3
            elif links_chemistry < 1:
                return 6
            elif links_chemistry <= 1.6:
                return 9
            elif links_chemistry <= 3:
                return 10
            else:
                print "Error: Invalid links chemistry value: %d" % links_chemistry
                return -1

        # Error
        else:
            print "Error: Invalid position chemistry value"
            return -1

    def individual_chemistry(self, position):
        """
        Calculate the individual chemistry for the specified position
        Input: The position
        Output: The individual chemistry
        """

        # Calculate the position and links chemistry
        plc = self.position_links_chemistry(self.links_chemistry(position),
                                            self.position_chemistry(position['player']['position'], position['symbol']))

        # Calculate the manager chemistry bonus
        manager_bonus = 0
        if len(self.manager) == 2:
            if (position['player']['nation']['name'] == self.manager['nation']) or \
                    (position['player']['league']['name'] == self.manager['league']):
                manager_bonus = 1

        # Calculate the loyalty bonus
        if position['loyalty']:
            loyalty_bonus = 1
        else:
            loyalty_bonus = 0

        chemistry = plc + manager_bonus + loyalty_bonus

        # Check if chemistry is above 10
        if chemistry > 10:
            chemistry = 10

        return chemistry

    def team_chemistry(self):
        """
        Calculate the team chemistry
        Input: None  -  Just uses self
        Output: The team chemistry
        """

        # Calculate and return the team's chemistry
        team_chemistry = 0
        for position in self.formation['positions'].itervalues():
            team_chemistry += position['chemistry']

        return team_chemistry

    def manager_suggestion(self):
        """
        Calculate the most beneficial manager traits
        Input: None  -  Just uses self
        Output: Suggested manager traits
        """

        not_maxed_chem = []
        existing_manager = self.manager
        self.manager = {}  # Reset manager

        # Recalculate individual chemistry without manager and see if it is maxed
        for symbol, position in self.formation['positions'].iteritems():
            position['chemistry'] = self.individual_chemistry(position)

            # Check if chemistry is maxed
            if position['chemistry'] < 10:
                not_maxed_chem.append(symbol)

        # If individual chemistry isn't maxed out, suggest manager
        if (len(self.manager) < 2) and (len(not_maxed_chem) > 0):

            nations = []
            leagues = []

            for symbol in not_maxed_chem:
                nations.append(self.formation['positions'][symbol]['player']['nation']['name'])
                leagues.append(self.formation['positions'][symbol]['player']['league']['name'])

            nation_league_tuple_list = []

            # Iterate through each nation and then leagues to find most beneficial option
            diff_nations = set(nations)

            for nation in diff_nations:
                # Count number of people from specified nation
                nation_count = nations.count(nation)

                # Count leagues excluding people from above nation
                leagues_not_nation = []
                for x in range(0, len(leagues)):
                    if nations[x] != nation:
                        leagues_not_nation.append(leagues[x])

                # Check if all people were from that nation
                if len(leagues_not_nation) == 0:
                    nation_league_tuple_list.append((nation, "Doesn't Matter", nation_count))

                # Find most popular league
                else:
                    diff_leagues = set(leagues_not_nation)
                    league_count = 0
                    popular_league = ''

                    for league in diff_leagues:
                        if leagues_not_nation.count(league) > league_count:
                            league_count = leagues_not_nation.count(league)
                            popular_league = league

                    nation_league_tuple_list.append((nation, popular_league, nation_count+league_count))

            # Iterate through each league and then nations to find most beneficial option
            diff_leagues = set(leagues)

            for league in diff_leagues:
                # Count number of people from specified league
                league_count = leagues.count(league)

                # Count nations excluding people from above league
                nations_not_league = []
                for x in range(0, len(nations)):
                    if leagues[x] != league:
                        nations_not_league.append(nations[x])

                # Check if all people were from that league
                if len(nations_not_league) == 0:
                    nation_league_tuple_list.append(("Doesn't Matter", league, league_count))

                # Find most popular nation
                else:
                    diff_nations = set(nations_not_league)
                    nation_count = 0
                    popular_nation = ''

                    for nation in diff_nations:
                        if nations_not_league.count(nation) > nation_count:
                            nation_count = nations_not_league.count(nation)
                            popular_nation = nation

                    nation_league_tuple_list.append((popular_nation, league, nation_count+league_count))

            # Narrow tuples list to most beneficial options
            most_benefit = 0
            for tup in nation_league_tuple_list:
                if tup[2] > most_benefit:
                    most_benefit = tup[2]

            nation_league_tuple_list[:] = [tup for tup in nation_league_tuple_list if not tup[2] < most_benefit]

            # Remove the number values from the tuples
            for x in range(0, len(nation_league_tuple_list)):
                nation_league_tuple_list[x] = nation_league_tuple_list[x][:2]

            # Reset values
            self.manager = existing_manager
            for position in self.formation['positions'].itervalues():
                position['chemistry'] = self.individual_chemistry(position)

            return nation_league_tuple_list

        # The individual chemistry is maxed without a manager so it doesn't matter
        else:
            # Reset values
            self.manager = existing_manager
            for position in self.formation['positions'].itervalues():
                position['chemistry'] = self.individual_chemistry(position)

            return [("Doesn't matter", "Doesn't matter")]

    def calculate_chemistry(self):
        """
        Calculate and assign the team chemistry and all individual chemistry
        Input: None  -  Just uses self
        Output: The team chemistry
        """

        maxed_chem = True

        # Calculate and assign the individual chemistry for all of the positions
        for symbol, position in self.formation['positions'].iteritems():
            position['chemistry'] = self.individual_chemistry(position)

            # Check if chemistry is maxed
            if position['chemistry'] < 10:
                maxed_chem = False

        # If chemistry isn't maxed, check for manager suggestions
        if (not maxed_chem) and (len(self.manager) < 2):
            # Get suggestions
            nation_league_tuple_list = self.manager_suggestion()

            # Assign the top manager suggestion
            self.manager['nation'] = nation_league_tuple_list[0][0]
            self.manager['league'] = nation_league_tuple_list[0][1]

            # Recalculate the individual chemistry with the manager suggestion
            for symbol, position in self.formation['positions'].iteritems():
                position['chemistry'] = self.individual_chemistry(position)

        # Chemistry is maxed; set manager to doesn't matter
        else:
            self.manager['nation'] = "Doesn't Matter"
            self.manager['league'] = "Doesn't Matter"

        # Calculate, assign, and return the team's chemistry
        team_chemistry = self.team_chemistry()

        self.total_ic = team_chemistry

        if team_chemistry > 100:
            team_chemistry = 100

        self.chemistry = team_chemistry

        return self.chemistry

    def print_chemistry_stats(self):
        """
        Calculates all of the stats relating to the team and individual chemistry
        Input: None  -  All of the information is in self
        Output: None  -  Prints out the chemistry statistics
        """

        # Colors for printing
        green = '\033[92m'
        yellow = '\033[93m'
        orange = '\033[91m'
        blue = '\033[94m'  # Using blue instead of red
        color_end = '\033[0m'

        print "Player Chemistry:"

        # Iterate through each of the players
        index = 0
        while index < 1 + self.formation['num_defenders'] + self.formation['num_midfielders'] + \
                self.formation['num_attackers']:
            for position, player in self.formation['positions'].iteritems():
                if player['index'] == index:

                    # Get player's common name, if it exists, or the full name
                    name = ascii_text(player['player']['firstName']) + " " + ascii_text(player['player']['lastName'])
                    if player['player']['commonName'] != '':
                        name = ascii_text(player['player']['commonName'])

                    # Color info
                    # Determine individual chemistry color
                    chemistry = 'CHEMISTRY COLOR ERROR'
                    if player['chemistry'] < 4:
                        chemistry = blue + str(player['chemistry']) + color_end
                    elif player['chemistry'] < 7:
                        chemistry = orange + str(player['chemistry']) + color_end
                    elif player['chemistry'] < 10:
                        chemistry = yellow + str(player['chemistry']) + color_end
                    elif player['chemistry'] == 10:
                        chemistry = green + str(player['chemistry']) + color_end

                    # Determine position color
                    position_color = 'POSITION COLOR ERROR'
                    color_num = self.position_chemistry(player['player']['position'], player['symbol'])
                    if color_num == 0:
                        position_color = blue
                    elif color_num == 1:
                        position_color = orange
                    elif color_num == 2:
                        position_color = yellow
                    elif color_num == 3:
                        position_color = green

                    # Determine links and colors
                    links = ''
                    link_size = 0
                    for link in player['links']:
                        color_num = self.teammate_chemistry(player['player'],
                                                            self.formation['positions'][link]['player'])
                        if color_num == 0:
                            links += (blue + link + color_end + ' ')
                        elif color_num == 1:
                            links += (orange + link + color_end + ' ')
                        elif color_num == 2:
                            links += (yellow + link + color_end + ' ')
                        elif color_num == 3:
                            links += (green + link + color_end + ' ')

                        link_size += (len(link) + 1)

                    # Determine manager color
                    if (player['player']['nation']['name'] == self.manager['nation']) \
                            or (player['player']['league']['name'] == self.manager['league']):
                        manager = green + 'Manager' + color_end
                    else:
                        manager = blue + 'Manager' + color_end

                    # Determine loyalty color
                    if player['loyalty']:
                        loyalty = green + 'Loyalty' + color_end
                    else:
                        loyalty = blue + 'Loyalty' + color_end

                    print'%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s' % \
                         (position, ':', ' ' * (6 - len(position)),
                          name, ' ' * (35 - len(name)),
                          'Rating: ', player['player']['rating'], ' ' * (5 - len(str(player['player']['rating']))),
                          'Chemistry: ', chemistry, ' ' * (5 - len(str(player['chemistry']))),
                          'Natural Position: ', position_color, player['player']['position'], color_end,
                          ' ' * (5 - len(player['player']['position'])),
                          'Links: ', links, ' ' * (25 - link_size),
                          manager, ' ' * 3, loyalty)
                    index += 1

        # Print manager info
        print 'Manager - Nation: %s   League: %s' % (self.manager['nation'], self.manager['league'])

        return 0

# ====================STRENGTH FUNCTIONS========== #
    @staticmethod
    def individual_strengths(player, important_attributes=None, bad_traits=None, good_skill=None,
                             good_weak_foot=None, good_height=None, good_stat_value=None):
        """
        Determine the strong attributes and traits of the player
        Input: The player
        Output: A tuple of the strengths rating an a list of the player's strengths
        """

        # Get strength config values
        if important_attributes is None:
            # Get important stats from config file
            with open('configs.json', 'r') as config_file:
                strengths_dict = json.load(config_file)['player_attributes']['important_attributes']
                config_file.close()

            important_attributes = strengths_dict['important_attributes']
            bad_traits = strengths_dict['bad_traits']
            good_skill = strengths_dict['good_skill']
            good_weak_foot = strengths_dict['good_weak_foot']
            good_height = strengths_dict['good_height']
            good_stat_value = strengths_dict['good_stat_value']

        rating = 0
        strengths = []
        good_strength = 1
        great_strength = 2
        amazing_strength = 3

        # Get traits
        traits = copy.deepcopy(player['traits'])

        if traits is not None:
            # Remove bad traits or ones that don't affect ability
            for bad_trait in bad_traits:
                if bad_trait in traits:
                    traits.remove(bad_trait)

            # Add good traits to list
            if len(traits) > 0:
                traits_str = ''
                for trait in traits:
                    traits_str += trait + ', '
                    rating += good_strength
                strengths.append(('Good Traits', traits_str[:-2]))

        # Specialities are just player tendencies and don't affect ability
        """# Get specialities
        specialities = player['specialities']
        if specialities is not None:
            specialities_str = ''
            for speciality in specialities:
                specialities_str += speciality + ', '
            strengths.append(('Specialities', specialities_str[:-2]))"""

        # Check for skill moves
        skill_moves = player['skillMoves']
        if skill_moves >= good_skill:
            stars = skill_moves*'* '
            stars = stars[:-1]
            strengths.append(('Skill Moves', stars))
            rating += great_strength + skill_moves - good_skill

        # Check for weak foot
        weak_foot = player['weakFoot']
        if weak_foot >= good_weak_foot:
            stars = weak_foot*'* '
            stars = stars[:-1]
            strengths.append(('Weak Foot', stars))
            rating += good_strength

        # Check for height
        height = player['height']
        if height >= good_height:
            strengths.append(('Height', convert_height(height, 'string')))
            rating += good_strength

        # Check for any high important stats
        for attribute in important_attributes:
            # Skip already checked stats
            if attribute not in ['traits', 'skillMoves', 'weakFoot', 'height']:
                stat = player[attribute]
                if stat >= good_stat_value:
                    strengths.append((format_attr_name(attribute), stat))
                    rating += good_strength

        # Sort strengths by value
        strengths = sorted(strengths, key=lambda k: k[1], reverse=True)

        return rating, strengths

    def calculate_strength(self):
        """
        Calculate and assign the team strength rating and individual strengths
        Input: None  -  Just uses self
        Output: The team strength
        """

        # Get important stats from config file
        with open('configs.json', 'r') as config_file:
            strengths_dict = json.load(config_file)['player_attributes']['important_attributes']
            config_file.close()

        important_attributes = strengths_dict['important_attributes']
        bad_traits = strengths_dict['bad_traits']
        good_skill = strengths_dict['good_skill']
        good_weak_foot = strengths_dict['good_weak_foot']
        good_height = strengths_dict['good_height']
        good_stat_value = strengths_dict['good_stat_value']

        strength = 0

        for position in self.formation['positions'].itervalues():
            # Get player's strengths
            player_strengths = self.individual_strengths(position['player'], important_attributes, bad_traits,
                                                         good_skill, good_weak_foot, good_height, good_stat_value)

            position['strength_rating'] = player_strengths[0]
            position['strengths'] = player_strengths[1]
            strength += position['strength_rating']

        self.strength = strength

        return self.strength

    def print_team_strengths(self):
        """
        Prints out the key strengths of the players on the team
        Input: None  -  All of the information is in self
        Output: None  -  Prints out the key strengths
        """

        index = 0

        while index < 1 + self.formation['num_defenders'] + self.formation['num_midfielders'] + \
                self.formation['num_attackers']:
            for symbol, position in self.formation['positions'].iteritems():
                if position['index'] == index:

                    player = position['player']
                    strengths = sorted(position['strengths'], key=lambda k: k[1], reverse=True)

                    # Get player's common name, if it exists, or the full name
                    name = ascii_text(player['firstName']) + " " + ascii_text(player['lastName'])
                    if player['commonName'] != '':
                        name = ascii_text(player['commonName'])

                    if len(strengths) > 0:
                        print "%s%s%d%s%d%s%s" % (symbol, ' '*(5-len(symbol)), player['rating'], '-',
                                                  position['strength_rating'], ' '*3, name)
                        for strength in strengths:
                            print "%s%s%s %s" % (' '*15, strength[0], ' '*(17-len(strength[0])), str(strength[1]))

                    index += 1
        return 0

# ====================FIND ATTRIBUTE TEAM FUNCTIONS========== #

    @staticmethod
    def pick_best_team(team_list, attributes=None):
        """
        Calculate the best team from the list of teams based on the list of attributes
        Input: List of teams and list of attributes
        Output: The index of the best team on the list
        """

        # Check if the team list is empty
        if len(team_list) == 0:
            return -1

        # Check if there is only one team
        elif len(team_list) == 1:
            return 0

        else:
            if attributes is None:
                attributes = ['rating']

            # Calculate a score for each team based on given attributes
            scores = []

            # Iterate through the teams
            for idx, team in enumerate(team_list):
                total = 0
                # Iterate through the attributes
                for attr_num, attribute in enumerate(attributes):
                    subtotal = 0
                    # Iterate through the position
                    for position in team['formation']['positions'].itervalues():
                        if attribute == 'skillMoves':
                            subtotal += (position['player']['skillMoves']*20)
                        else:
                            subtotal += position['player'][attribute]
                    # Divide subtotal by attribute number to weigh results
                    total += (subtotal/(attr_num+1))
                # Add total to scores list
                scores.append((idx, total))

            # Sort score tuples by the score value
            scores.sort(key=lambda score: score[1], reverse=True)

            # Check for a top team
            if scores[0][1] != scores[1][1]:
                # No ties, assign top team
                return scores[0][0]

            # There is a tie
            else:
                tied_teams = []
                # Find all tied teams
                for score_tuple in scores:
                    if score_tuple[1] == scores[0][1]:
                        # Add team chemistry to tuple
                        tied_teams.append(score_tuple + (team_list[score_tuple[0]]['chemistry'],))

                # Break tie with team chemistry
                # Sort teams by team chemistry
                tied_teams.sort(key=lambda tup: tup[2], reverse=True)

                # Check for tie
                if tied_teams[0][2] != tied_teams[1][2]:
                    # Tie broken
                    return tied_teams[0][0]

                else:
                    # Find all still tied teams
                    tied_teams_again = []
                    for team_tuple in tied_teams:
                        if team_tuple[2] == tied_teams[0][2]:
                            # Calculate total individual chemistry
                            total_ic = 0
                            for position in team_list[team_tuple[0]]['formation']['positions'].itervalues():
                                total_ic += position['chemistry']

                            # Add total individual chemistry to tuple
                            tied_teams_again.append(team_tuple + (total_ic,))

                    # Break tie with total individual chemistry
                    # Sort teams by total individual chemistry
                    tied_teams_again.sort(key=lambda tup: tup[3], reverse=True)

                    # Check for tie
                    if tied_teams_again[0][3] != tied_teams_again[1][3]:
                        # Tie broken
                        return tied_teams_again[0][0]

                    else:
                        # Find all still tied teams
                        tied_teams_again_again = []
                        for again_tuple in tied_teams_again:
                            if again_tuple[3] == tied_teams_again[0][3]:
                                # Add team rating to tuple
                                tied_teams_again_again.append(again_tuple + (team_list[again_tuple[0]]['rating'],))

                        # Break tie with ratings
                        # Sort teams by team chemistry
                        tied_teams_again_again.sort(key=lambda tup: tup[4], reverse=True)

                        # No more tie breakers, taking top team
                        return tied_teams_again_again[0][0]

    @staticmethod
    def find_team(players, formations, attributes=None):
        """
        Finds the best team (ignoring chemistry) with specific attribute emphasis from the given players and formations
        Input: PlayerDB of players, FormationDB of formations, and a list of attributes to focus on
        Output: None  -  Creates team of players with highest specified attributes and assigns to self
        """

        # Check that there are at least 11 players
        if len(players.db) < 11:
            return {}

        # List of teams created
        team_list = []

        # Check if there are no attributes
        if attributes is None:
            attributes = ['rating']

        for formation in formations.db:
            # Find players and create a list of players with current formation
            player_list = []  # List of players before they are assigned to roster
            base_ids = []  # List of base IDs of players already in formation
            positions_remaining = []  # List of positions remaining to fill

            # Sort the players by the attributes
            players.sort(attributes)

            # Get positions remaining
            for position in formation['positions'].itervalues():
                positions_remaining.append(position['symbol'])

            # Find players for each position
            index = 0
            while (len(positions_remaining) > 0) and (index < len(players.db)):

                # Assign current player, position symbol, and alternative positions
                player = players.db[index]
                symbol = player['position']
                alt_positions = Team.related_positions(symbol)
                assigned = False

                # Check if player is already on the team
                if player['baseId'] not in base_ids:

                    # Fill open position with player
                    if symbol in positions_remaining:
                        player_list.append((symbol, player))
                        base_ids.append(player['baseId'])
                        # Remove position from remaining
                        positions_remaining.remove(symbol)
                        assigned = True

                    # Check alternate positions
                    elif len(alt_positions) > 0:
                        for x in range(0, len(alt_positions)):
                            if alt_positions[x] in positions_remaining:
                                player_list.append((alt_positions[x], player))
                                base_ids.append(player['baseId'])
                                # Remove position from remaining
                                positions_remaining.remove(alt_positions[x])
                                assigned = True
                                break

                    # Assign positions that might switch the CMs - midfield in 4-1-2-1-2 (2)
                    # Verify player is a CAM or CDM and formation is 4-1-2-1-2 (2)
                    if (not assigned) and ((symbol == 'CAM') or (symbol == 'CDM')) \
                            and (formation['name'] == '4-1-2-1-2 (2)'):

                        if symbol == 'CAM':
                            tup_num = -1
                            # Check if CM is in CAM spot and if CDM is remaining
                            for idx, tup in enumerate(player_list):
                                if (tup[0] == 'CAM') and (tup[1]['position'] == 'CM') \
                                        and ('CDM' in positions_remaining):
                                    # Does exist, so must replace
                                    tup_num = idx
                                    break

                            if tup_num != -1:
                                # Replace CM with CAM in CAM spot
                                cm = player_list[tup_num][1]
                                player_list.remove(player_list[tup_num])
                                player_list.append((symbol, player))
                                base_ids.append(player['baseId'])
                                # Fill CDM spot with CM
                                player_list.append(('CDM', cm))
                                # Remove position from remaining
                                positions_remaining.remove('CDM')

                        elif symbol == 'CDM':
                            tup_num = -1
                            # Check if CM is in CDM spot and if CAM is remaining
                            for idx, tup in enumerate(player_list):
                                if (tup[0] == 'CDM') and (tup[1]['position'] == 'CM') \
                                        and ('CAM' in positions_remaining):
                                    # Does exist, so must replace
                                    tup_num = idx
                                    break

                            if tup_num != -1:
                                # Replace CM with CDM in CDM spot
                                cm = player_list[tup_num][1]
                                player_list.remove(player_list[tup_num])
                                player_list.append((symbol, player))
                                base_ids.append(player['baseId'])
                                # Fill CAM spot with CM
                                player_list.append(('CAM', cm))
                                # Remove position from remaining
                                positions_remaining.remove('CAM')

                index += 1

            # Fill out remaining positions
            # Iterate through the levels of position relativity
            for relation in ['orange', 'blue', 'purple', 'red']:
                index = 0
                while (len(positions_remaining) > 0) and (index < len(players.db)):

                    # Assign current player, position symbol, and orange alternative positions
                    player = players.db[index]
                    symbol = player['position']
                    alt_positions = Team.related_positions(symbol, similarity=relation)

                    # Check if player is already on the team
                    if player['baseId'] not in base_ids:

                        # Check alternate positions
                        if len(alt_positions) > 0:
                            for x in range(0, len(alt_positions)):
                                if alt_positions[x] in positions_remaining:
                                    player_list.append((alt_positions[x], player))
                                    base_ids.append(player['baseId'])
                                    # Remove position from remaining
                                    positions_remaining.remove(alt_positions[x])
                                    break
                    index += 1

            # Check if team is not filled because there are not enough players (because of doubles)
            if len(positions_remaining) > 0:
                return {}

            # Assign players to roster
            roster = {}  # Dict of players and positions
            # Iterate through players
            for tup in player_list:
                # Iterate through formation positions
                for custom_symbol, position in formation['positions'].iteritems():
                    # Find position that matches players position on list
                    if (tup[0] == position['symbol']) and (custom_symbol not in roster):
                        roster[custom_symbol] = tup[1]
                        break

            # Set the team using the roster and add to list
            temp_team = Team()
            temp_team.set_team(formation, roster)
            team_list.append(temp_team.__dict__)

        # Compare teams and pick the best one
        team_index = Team.pick_best_team(team_list, attributes)

        # No teams
        if team_index == -1:
            return {}

        # Return the best team
        return team_list[team_index]

# ====================FIND ULTIMATE TEAM FUNCTIONS========== #

    @staticmethod
    def find_team_club(players, formations):
        """
        Finds the best team of players from the same club from the given players and formations.
        Input: PlayerDB of players and FormationDB of formations.
        Output: The best team of players from the same club.
        """

        # List of teams created
        team_list = []

        # Get a list of all player's clubs
        club_list = []
        for player in players.db:
            club_list.append(player['club']['id'])

        # Determine the clubs with at least 11 players
        club_set = set(club_list)
        clubs_with_players = []
        for club in club_set:
            if club_list.count(club) >= 11:
                clubs_with_players.append(club)

        # Create teams for each of the clubs with at least 11 players
        for club in clubs_with_players:
            team_list.append(Team.find_team(PlayerDB(players.search({'clubId': (club, 'exact')})), formations))

        # Remove blank teams
        while team_list.count({}) > 0:
            team_list.remove({})

        # If no teams teams were created, return a blank dict
        if len(team_list) == 0:
            return {}

        # Find the best team based on player ratings and individual chemistry
        team_index = Team.pick_best_team(team_list)

        # No teams
        if team_index == -1:
            return {}

        # Return the best team
        return team_list[team_index]

    @staticmethod
    def find_team_league(players, formations):
        """
        Finds the best team of players from the same league from the given players and formations.
        Input: PlayerDB of players and FormationDB of formations.
        Output: The best team of players from the same league.
        """

        # List of teams created
        team_list = []

        # Get a list of all player's leagues
        league_list = []
        for player in players.db:
            league_list.append(player['league']['id'])

        # Determine the leagues with at least 11 players
        league_set = set(league_list)
        leagues_with_players = []
        for league in league_set:
            if league_list.count(league) >= 11:
                leagues_with_players.append(league)

        # Create teams for each of the leagues with at least 11 players
        for league in leagues_with_players:
            team_list.append(Team.find_team(PlayerDB(players.search({'leagueId': (league, 'exact')})), formations))

        # Remove blank teams
        while team_list.count({}) > 0:
            team_list.remove({})

        # If no teams teams were created, return a blank dict
        if len(team_list) == 0:
            return {}

        # Find the best team based on player ratings and individual chemistry
        team_index = Team.pick_best_team(team_list)

        # No teams
        if team_index == -1:
            return {}

        # Return the best team
        return team_list[team_index]

    @staticmethod
    def find_team_nation(players, formations):
        """
        Finds the best team of players from the same nation from the given players and formations.
        Input: PlayerDB of players and FormationDB of formations.
        Output: The best team of players from the same nation.
        """

        # List of teams created
        team_list = []

        # Get a list of all player's nations
        nation_list = []
        for player in players.db:
            nation_list.append(player['nation']['id'])

        # Determine the nations with at least 11 players
        nation_set = set(nation_list)
        nations_with_players = []
        for nation in nation_set:
            if nation_list.count(nation) >= 11:
                nations_with_players.append(nation)

        # Create teams for each of the leagues with at least 11 players
        for nation in nations_with_players:
            team_list.append(Team.find_team(PlayerDB(players.search({'nationId': (nation, 'exact')})), formations))

        # Remove blank teams
        while team_list.count({}) > 0:
            team_list.remove({})

        # If no teams teams were created, return a blank dict
        if len(team_list) == 0:
            return {}

        # Find the best team based on player ratings and individual chemistry
        team_index = Team.pick_best_team(team_list)

        # No teams
        if team_index == -1:
            return {}

        # Return the best team
        return team_list[team_index]

# ====================CREATE ULTIMATE TEAM FUNCTIONS========== #

    @staticmethod
    def pass_requirements_check(players, formations):
        """
        Checks there are enough players and formations.
        Input: PlayerDB of players and FormationDB of formations.
        Output: Boolean of the check
        """

        # Check if there are at least 11 players
        if len(players.db) < 11:
            print "Not enough players."
            return False

        # Check if there is at least 1 formation
        if len(formations.db) < 1:
            print "Need at least one formation."
            return False

        # Passed both checks
        return True

    def create_team_club(self, players, formations):
        """
        Creates the best team of players from the same club from the given players and formations.
        Input: PlayerDB of players and FormationDB of formations.
        Output: True  -  Creates best team and assigns to self.
        """

        # Check the minimum requirements
        if not Team.pass_requirements_check(players, formations):
            return False

        # Create team dict using the one club method
        team_dict = Team.find_team_club(players, formations)

        # Check if team was not created
        if team_dict == {}:
            return False

        # Assign to self
        self.__init__(team_dict)
        return True

    def create_team_league(self, players, formations):
        """
        Creates the best team of players from the same league from the given players and formations.
        Input: PlayerDB of players and FormationDB of formations.
        Output: True  -  Creates best team and assigns to self.
        """

        # Check the minimum requirements
        if not Team.pass_requirements_check(players, formations):
            return False

        # Create team dict using the one league method
        team_dict = Team.find_team_league(players, formations)

        # Check if team was not created
        if team_dict == {}:
            return False

        # Assign to self
        self.__init__(team_dict)
        return True

    def create_team_nation(self, players, formations):
        """
        Creates the best team of players from the same nation from the given players and formations.
        Input: PlayerDB of players and FormationDB of formations.
        Output: True  -  Creates best team and assigns to self.
        """

        # Check the minimum requirements
        if not Team.pass_requirements_check(players, formations):
            return False

        # Create team dict using the one nation method
        team_dict = Team.find_team_nation(players, formations)

        # Check if team was not created
        if team_dict == {}:
            return False

        # Assign to self
        self.__init__(team_dict)
        return True

    def create_team_ultimate(self, players, formations):
        """
        Creates the best team using my thorough method from the given players and formations.
        Input: PlayerDB of players, FormationDB of formations, the process to use, and the minimum number of teams.
        Output: List of top teams and creates best team and assigns to self.
        """

        # Check the minimum requirements
        if not Team.pass_requirements_check(players, formations):
            return False

        # Create team dict using my thorough method
        team_list = UltimateTeamFunctions.find_team_ultimate(players, formations)

        # Check if team was not created
        if len(team_list) == 0:
            return []

        # Assign top team to self
        self.__init__(team_list[0])
        return team_list
