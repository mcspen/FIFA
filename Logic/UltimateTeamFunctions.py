"""
All of the functions containing the logic to create the ultimate teams.
"""

from Window.AppConfig import config_filename
from PlayerDB import PlayerDB
import Team
import time
import copy
import json
from multiprocessing import Pool

req_link_chem = 0.3


def recursive_create_tup(tup):
    """
    Wrapper function to all Team.recursive_create_tup to be called by pool
    """
    return puzzle_piece_create(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10],
                              roster=tup[11], base_ids=tup[12], start_roster_num=tup[13], must_have_players=tup[14])


def calculate_dependency_dict_list(dependent_positions, roster):
    """
    Calculate and create a tuple of the traits of players eligible to use based on dependencies
    Input: List of tuples of the positions of dependent players and chemistry needed and the roster
    Output: A list of dicts of traits of players eligible based on dependencies
    """

    # Only one dependent player to add traits to search for
    if len(dependent_positions) == 1:

        # Need at least one chemistry
        if dependent_positions[0][1] <= 1:
            # Create position dict list of one trait for the player dependency search
            return [{'nation': (roster[dependent_positions[0][0]]['nation']['name'], 'exact')},
                    {'league': (roster[dependent_positions[0][0]]['league']['name'], 'exact')}]

        # Need at least two chemistry
        elif dependent_positions[0][1] == 2:
            # Create position dict list of two traits for the player dependency search
            return [{'nation': (roster[dependent_positions[0][0]]['nation']['name'], 'exact'),
                     'league': (roster[dependent_positions[0][0]]['league']['name'], 'exact')},
                    {'club': (roster[dependent_positions[0][0]]['club']['name'], 'exact')}]

        # Need three chemistry
        else:
            # Create position dict list of all three traits for the player dependency search
            return [{'nation': (roster[dependent_positions[0][0]]['nation']['name'], 'exact'),
                     'club': (roster[dependent_positions[0][0]]['club']['name'], 'exact')}]

    # Multiple dependent players to add traits to search for
    else:

        # Sort players by chemistry needed
        dependent_positions = sorted(dependent_positions, key=lambda d_tup: d_tup[1], reverse=True)

        # Need three chemistry
        if dependent_positions[0][1] > 2:

            match = True
            nation = roster[dependent_positions[0][0]]['nation']['name']
            league = roster[dependent_positions[0][0]]['league']['name']
            club = roster[dependent_positions[0][0]]['club']['name']

            # Iterate through all positions and check that specific number of traits match
            for position in dependent_positions[1:]:
                total_match = 0

                if roster[position[0]]['nation']['name'] == nation:
                    total_match += 1
                if roster[position[0]]['league']['name'] == league:
                    total_match += 1
                    if roster[position[0]]['club']['name'] == club:
                        total_match += 1

                # Check if enough traits matched
                if not (total_match >= position[1]):
                    match = False
                    break

            # All traits did match. Return dependency dict
            if match:
                return [{'nation': (nation, 'exact'), 'club': (club, 'exact')}]

        # Need two chemistry for at least one dependency, and the remaining need one or two chemistry
        elif dependent_positions[0][1] > 1:

            dependency_tuple_list = []
            nations = []
            leagues = []
            clubs = []

            # Get list of unique nations and leagues
            for tup in dependent_positions:

                nations.append(roster[tup[0]]['nation']['name'])
                leagues.append(roster[tup[0]]['league']['name'])
                clubs.append(roster[tup[0]]['club']['name'])

            nations = list(set(nations))
            leagues = list(set(leagues))
            clubs = list(set(clubs))

            # Check for nation and league matching all or club matching all
            if ((len(nations) == 1) and (len(leagues) == 1)) or (len(clubs) == 1):
                # All nations and leagues match
                if (len(nations) == 1) and (len(leagues) == 1):
                    dependency_tuple_list.append({'nation': (nations[0], 'exact'), 'league': (leagues[0], 'exact')})
                # All clubs match
                if len(clubs) == 1:
                    dependency_tuple_list.append({'club': (clubs[0], 'exact')})

                return dependency_tuple_list

            # Search for matching trait combinations
            else:

                # Iterate through nations
                for nation_index, nation_position in enumerate(dependent_positions):
                    # Iterate through clubs
                    for club_index, club_position in enumerate(dependent_positions):

                        # Only accept combinations that include first position in list (that needs 2 chem)
                        if (nation_index != 0) and (club_index != 0):
                            continue

                        match = True

                        # Get current nation, league, and club
                        nation = roster[nation_position[0]]['nation']['name']
                        league = roster[nation_position[0]]['league']['name']
                        club = roster[club_position[0]]['club']['name']

                        # Change league to the club's league if club is first position trait and nation isn't
                        if (club_index == 0) and (nation_index != 0):
                            league = roster[club_position[0]]['league']['name']

                        # Check if club is in the league
                        else:
                            if roster[club_position[0]]['league']['name'] != league:
                                continue

                        # Iterate through all positions and check that specific number of traits match
                        for position in dependent_positions[1:]:
                            total_match = 0

                            if roster[position[0]]['nation']['name'] == nation:
                                total_match += 1
                            if roster[position[0]]['league']['name'] == league:
                                total_match += 1
                                if roster[position[0]]['club']['name'] == club:
                                    total_match += 1

                            # Check if enough traits matched
                            if not (total_match >= position[1]):
                                match = False
                                break

                        # All traits did match. Return dependency tuple
                        if match:
                            dependency_tuple_list.append({'nation': (nation, 'exact'),
                                                          'league': (league, 'exact'),
                                                          'club': (club, 'exact')})

                return dependency_tuple_list

        # Only need one chemistry for each dependency - don't need to look at club because only one chem needed
        else:

            dependency_tuple_list = []
            nations = []
            leagues = []

            # Get list of unique nations and leagues
            for tup in dependent_positions:

                nations.append(roster[tup[0]]['nation']['name'])
                leagues.append(roster[tup[0]]['league']['name'])

            nations = list(set(nations))
            leagues = list(set(leagues))

            # Check for nation or league matching all
            if (len(nations) == 1) or (len(leagues) == 1):
                # All nations match
                if len(nations) == 1:
                    dependency_tuple_list.append({'nation': (nations[0], 'exact')})
                # All leagues match
                if len(leagues) == 1:
                    dependency_tuple_list.append({'league': (leagues[0], 'exact')})

                return dependency_tuple_list

            # Search for matching trait combinations
            else:
                # Iterate through all nations and leagues to get every combination
                for nation in nations:
                    for league in leagues:
                        match = True

                        # Iterate through dependent positions and see if combo doesn't match either trait
                        for tup in dependent_positions:
                            if (roster[tup[0]]['nation']['name'] != nation) and \
                               (roster[tup[0]]['league']['name'] != league):
                                match = False
                                break

                        # All positions matched at least one trait
                        if match:
                            dependency_tuple_list.append({'nation': (nation, 'exact'), 'league': (league, 'exact')})

                # Return the dependency tuple created
                return dependency_tuple_list

    # There were no matches
    return []


def reduce_teams(team_sort_attributes, num_teams, team_list):
    """
    Narrow down the team list to the top teams to save memory.
    """

    def compare(current_team):
        """
        Based on the list of attributes, return a tuple of attributes for the current team.
        Input: The current team.
        Output: A tuple of attributes to compare with.
        """

        attribute_tuple = ()
        for attr in team_sort_attributes:

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
            elif attr in ['total_PAC', 'total_SHO', 'total_PAS', 'total_DRI', 'total_DEF', 'total_PHY']:
                # Calculate total
                total = 0
                index = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY'].index(attr[6:])
                for position in current_team['formation']['positions'].itervalues():
                    player = position['player']
                    if not player['isGK']:
                        total += player['attributes'][index]['value']
                attribute_tuple += (total,)
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

    # Compare teams and narrow down to specified max number of teams
    sorted_list = sorted(team_list, key=compare, reverse=True)
    return sorted_list[:num_teams]


def find_dependent_players(position, custom_symbol, formation, roster,):
    """
    Check previously assigned players for critical dependencies
    """

    dependent_pos = []

    # Get list of previously assigned players
    recheck_list = []
    for link in position['links']:

        # Check if position is already assigned and if it is, add position to recheck list
        if link in roster:
            recheck_list.append(link)

    # Recheck chemistry of previously assigned positions for critical dependencies
    for recheck_position in recheck_list:
        recheck_chemistry = 0.0

        # Iterate through previously assigned player's links
        for link in formation['positions'][recheck_position]['links']:

            # Player currently being assigned. Assume 0 chemistry to see if dependent on player.
            if link == custom_symbol:
                recheck_chemistry += 0.0

            # Player is assigned. Get link chemistry.
            elif link in roster:
                recheck_chemistry += Team.Team.teammate_chemistry(roster[recheck_position], roster[link])

            # Player not assigned yet and isn't currently being assigned. Best possible chemistry is 3
            else:
                recheck_chemistry += 3.0

        recheck_chemistry /= len(formation['positions'][recheck_position]['links'])

        # Check if chemistry meets requirements
        if recheck_chemistry < req_link_chem:
            needed_chem = (req_link_chem - recheck_chemistry) * len(formation['positions'][recheck_position]['links'])
            dependent_pos.append((recheck_position, needed_chem))

    return dependent_pos


def check_current_player_chemistry(player, position, roster):
    potential_chemistry = 0.0

    for link in position['links']:

        # Player is assigned. Get link chemistry.
        if link in roster:
            potential_chemistry += Team.Team.teammate_chemistry(player, roster[link])

        # Player not assigned yet. Best possible chemistry is 3
        else:
            potential_chemistry += 3

    potential_chemistry /= len(position['links'])

    return potential_chemistry


def recursive_create(players, player_db, formation, chemistry_matters, time_limit, budget, players_per_position,
                     teams_per_formation, team_sort_attributes, player_sort_attributes, num_teams,
                     pos_index=0, roster=None, base_ids=None, team_list=None, team_count=0):
    """
    Recursive function to build all possible team combinations with good chemistry.
    Builds team by position.
    Input: PlayerDB of players, one formation, position index, roster, base IDs list, list of teams, and team count.
    Output: The list of teams and the team count.
    """

    print_formation_name_and_team_count = False
    print_all_team_chemistry = False
    positions_less = 5
    positions_greater = -1
    print_positions_less = False
    print_positions_greater = False

    # Set defaults
    if roster is None:
        roster = {}
    if base_ids is None:
        base_ids = []
    if team_list is None:
        team_list = []

    # Check if recursion is finished and team is full
    if pos_index > 10:

        # Set the team using the roster and add to list
        temp_team = Team.Team()
        temp_team.set_team(formation, roster)
        team_list.append(temp_team.__dict__)
        team_count += 1

        # Print out progress information -------------------------------------------------------------------------------
        if print_formation_name_and_team_count:
            print "%s: %d team(s)" % (formation['name'], team_count)
        # TEMPORARY ----------------------------------------------------------------------------------------------------

        # Print out team chemistry -------------------------------------------------------------------------------------
        if print_all_team_chemistry:
            for team in team_list:
                temp = Team.Team(team)
                temp.print_summary()
                temp.print_chemistry_stats()
                print ''
        # TEMPORARY ----------------------------------------------------------------------------------------------------

        # Narrow down team_list to save memory
        if (team_count % num_teams) == 0:
            print "Calculating... %d teams created" % team_count
            team_list = reduce_teams(team_sort_attributes, num_teams, team_list)

        return [team_list, team_count]

    # Check to see if function should return
    if team_count >= teams_per_formation or time.time() > time_limit:
        return [team_list, team_count]

    # Set next position index value
    next_index = pos_index + 1

    # Get position
    custom_symbol = ''
    position = {}
    for sym, pos in formation['positions'].iteritems():
        if pos['index'] == pos_index:
            custom_symbol = sym
            position = dict(pos)
            break

    # Check if position is already filled.
    if custom_symbol in roster:
        # Call recursive function
        results = recursive_create(players, player_db, formation, chemistry_matters, time_limit, budget,
                                   players_per_position, teams_per_formation, team_sort_attributes,
                                   player_sort_attributes, num_teams, next_index, roster, base_ids, team_list,
                                   team_count)
        team_list = results[0]
        team_count = results[1]

        return [team_list, team_count]

    dependent_pos = []
    pos_list = []

    # If chemistry matters
    if chemistry_matters:
        # Check previously assigned players for critical dependencies
        dependent_pos.extend(find_dependent_players(position, custom_symbol, formation, roster))

    # Since chemistry doesn't matter, add in 'orange' similar positions, but not 'red'. Need to keep it reasonable.
    else:
        pos_list += Team.Team.related_positions(position['symbol'], 'orange')

    # Get all eligible positions (related, exact is added individually later) for current position
    pos_list += Team.Team.related_positions(position['symbol'], 'yellow')

    # If no dependent players, simple search
    if len(dependent_pos) < 1:

        # Create position tuple list for the player search
        position_tuple_list = [{'position': (position['symbol'], 'exact')}]
        for x in pos_list:
            position_tuple_list.append({'position': (x, 'exact')})

        # Get all eligible players and create DB
        eligible_players = PlayerDB(players.multi_search(position_tuple_list))

        # If budget is higher than 200 (cheapest player price) add other players
        if budget >= 200:
            eligible_players.add(player_db.multi_search(position_tuple_list))

    # Add required traits for dependent player(s) to search
    else:

        # Get a list of tuples of traits of players eligible based on dependencies
        dependency_tuple_list = calculate_dependency_dict_list(dependent_pos, roster)

        # Get all players that match dependency and create DB
        dependency_match = PlayerDB(players.multi_search(dependency_tuple_list))

        # Create position tuple list for the player position search
        position_tuple_list = [{'position': (position['symbol'], 'exact')}]
        for x in pos_list:
            position_tuple_list.append({'position': (x, 'exact')})

        # Get all eligible players from smaller pool matching dependency and create DB
        eligible_players = PlayerDB(dependency_match.multi_search(position_tuple_list))

        # If budget is higher than 200 (cheapest player price) add other players
        if budget >= 200:
            dependency_match = PlayerDB(player_db.multi_search(dependency_tuple_list))
            eligible_players.add(dependency_match.multi_search(position_tuple_list))

        del position_tuple_list
        del dependency_tuple_list
        del dependency_match

    # Sort eligible players
    eligible_players.sort(player_sort_attributes, descend=False)
    # eligible_players.special_sort(position['symbol'])

    # Set variables for controlling the scope of team creation
    if players_per_position < 1:
        players_per_position = len(eligible_players.db)
    players_checked = 0

    # Iterate through eligible players for current position
    for player in eligible_players.db:

        # Check to see if function should return
        if team_count >= teams_per_formation or time.time() > time_limit:
            break






        # Special Checks
        # Check leagues
        # Get list of leagues
        leagues_list = [player['league']['id']]
        for guy in roster.itervalues():
            leagues_list.append(guy['league']['id'])
        leagues_set = set(leagues_list)

        # Check if more than 7 leagues
        if len(leagues_set) > 7:
            break
        # Check if more than 3 from 1 league
        too_many = False
        for league_id in leagues_set:
            if leagues_list.count(league_id) > 3:
                too_many = True
        if too_many:
            break

        # Check rating if full roster
        if len(roster) >= 10:
            rating_total = player['rating']
            for guy in roster.itervalues():
                rating_total += guy['rating']
            if rating_total / 11.0 < 77.5:
                break
            # Check that there are exactly 7 leagues
            if len(leagues_set) != 7:
                break





        # Check if player is in budget ---------------------------------------------------------------------------------
        if budget >= 200:
            if player['price'] > budget:
                if player not in players.db:
                    continue

        # Check if player is already used
        if player['baseId'] in base_ids:
            continue

        # Check number of players checked
        if players_checked < players_per_position:
            players_checked += 1
        else:
            break

        # DELETE LATER ---------------------------------------------------------------------------------------------
        if print_positions_less:
            if pos_index <= positions_less:
                print "Player" + ' '*(3-len(str(pos_index))) + str(pos_index) + " change!" + \
                      "     Teams created: " + str(team_count) + \
                      "     Player " + str(players_checked)
        # ----------------------------------------------------------------------------------------------------------
        # DELETE LATER ---------------------------------------------------------------------------------------------
        if print_positions_greater:
            if pos_index >= positions_greater:
                print "Player" + ' '*(3-len(str(pos_index))) + str(pos_index) + " change!" + \
                      "     Teams created: " + str(team_count) + \
                      "     Player " + str(players_checked)
        # ----------------------------------------------------------------------------------------------------------

        # Calculate current teammate potential chemistry
        potential_chemistry = 0.0
        if chemistry_matters:
            potential_chemistry = check_current_player_chemistry(player, position, roster)

        # Check if player meets chemistry requirements (must at least be 1 to reach 10 individual chemistry)
        if (potential_chemistry >= req_link_chem) or not chemistry_matters:

            # Create copy of base IDs list and roster for recursive function
            base_ids_copy = copy.deepcopy(base_ids)
            roster_copy = copy.deepcopy(roster)

            # Place current player in position
            roster_copy[custom_symbol] = player
            base_ids_copy.append(player['baseId'])

            # If budget is higher than 200, check if player is new and if so subtract the price.
            if budget >= 200 and player not in players.db:
                remaining_budget = budget - player['price']
                # player_db_copy = PlayerDB(copy.deepcopy(player_db.search({'price': (remaining_budget, 'lower')})))
            else:
                remaining_budget = budget
                # player_db_copy = player_db
            player_db_copy = player_db

            # Call recursive function
            results = recursive_create(players, player_db_copy, formation, chemistry_matters, time_limit,
                                       remaining_budget, players_per_position, teams_per_formation,
                                       team_sort_attributes, player_sort_attributes, num_teams, next_index, roster_copy,
                                       base_ids_copy, team_list, team_count)
            team_list = results[0]
            team_count = results[1]

    return [team_list, team_count]


def find_related_custom_positions(position_list, formation):
    """
    Match positions in list to custom positions in the formation.
    """
    custom_positions = []

    for natural_position in position_list:
        for custom_position, position_info in formation['positions'].iteritems():
            if position_info['symbol'] == natural_position:
                custom_positions.append(custom_position)

    return custom_positions


def check_linked_players_chemistry(linked_positions, formation, roster):
    """
    Check chemistry of affected previously assigned players.
    """

    # Get list of previously assigned players
    recheck_list = []
    for link in linked_positions:

        # Check if position is already assigned and if it is, add position to recheck list.
        if link in roster:
            recheck_list.append(link)

    # Recheck chemistry of previously assigned positions for critical dependencies.
    for recheck_position in recheck_list:
        potential_chemistry = check_current_player_chemistry(roster[recheck_position],
                                                             formation['positions'][recheck_position],
                                                             roster)

        # Check if chemistry meets requirements
        if potential_chemistry < req_link_chem:
            return False

    return True


def recursive_create_2(players, player_db, formation, chemistry_matters, time_limit, budget, players_per_position,
                       teams_per_formation, team_sort_attributes, player_sort_attributes, num_teams,
                       pos_index=0, roster=None, base_ids=None, team_list=None, team_count=0,
                       start_roster_num=0, must_have_players=None):
    """
    Recursive function to build all possible team combinations with good chemistry.
    Builds team based on best players.
    Input: PlayerDB of players, one formation, position index, roster, base IDs list, list of teams, and team count.
    Output: The list of teams and the team count.
    """

    print_formation_name_and_team_count = False
    print_all_team_chemistry = False

    # Set defaults
    if roster is None:
        roster = {}
    if base_ids is None:
        base_ids = []
    if team_list is None:
        team_list = []

    # Check if recursion is finished and team is full
    if len(roster) > 10:
        # Set the team using the roster and add to list
        temp_team = Team.Team()
        temp_team.set_team(formation, roster)
        team_list.append(temp_team.__dict__)
        team_count += 1

        # Print out progress information -------------------------------------------------------------------------------
        if print_formation_name_and_team_count:
            print "%s: %d team(s)" % (formation['name'], team_count)
        # TEMPORARY ----------------------------------------------------------------------------------------------------

        # Print out team chemistry -------------------------------------------------------------------------------------
        if print_all_team_chemistry:
            for team in team_list:
                temp = Team.Team(team)
                temp.print_summary()
                temp.print_chemistry_stats()
                print ''
        # TEMPORARY ----------------------------------------------------------------------------------------------------

        # Narrow down team_list to save memory
        if (team_count % num_teams) == 0:
            print "Calculating... %d teams created" % team_count
            team_list = reduce_teams(team_sort_attributes, num_teams, team_list)

        return [team_list, team_count]

    # Check to see if function should return
    if team_count >= teams_per_formation or time.time() > time_limit:
        return [team_list, team_count]

    # ==================================================================================================================
    # Temp path which switches to recursive function 1 when specified players have been assigned.
    if len(roster) >= start_roster_num:
        # Call recursive function 1
        results = recursive_create(players, player_db, formation, chemistry_matters, time_limit, budget,
                                   players_per_position, teams_per_formation, team_sort_attributes,
                                   player_sort_attributes, num_teams, pos_index, roster, base_ids, team_list,
                                   team_count)
        team_list = results[0]
        team_count = results[1]
        return [team_list, team_count]
    # ==================================================================================================================

    # Sort players by specified attributes
    # players.sort(player_sort_attributes)     ----  If adding this, implement the budget parameter
    must_have_players.sort(player_sort_attributes)

    # Iterate players
    # for player in players.db:
    for player in must_have_players.db:

        # Check to see if function should return
        if team_count >= teams_per_formation or time.time() > time_limit:
            break

        # Check if player is already used
        if player['baseId'] in base_ids:
            continue

        # Create possible position list
        # Add natural position
        pos_list = [player['position']]
        # Add very similar positions
        pos_list.extend(Team.Team.related_positions(player['position'], 'yellow'))
        # If chemistry doesn't matter, add in 'orange' similar positions, but not 'red'. Need to keep it reasonable.
        if not chemistry_matters:
            pos_list.extend(Team.Team.related_positions(player['position'], 'orange'))

        # Match positions in list to custom positions in the formation
        pos_list = find_related_custom_positions(pos_list, formation)

        # Iterate through positions for player
        for custom_symbol in pos_list:

            # Check to see if function should return
            if team_count >= teams_per_formation or time.time() > time_limit:
                break

            # Check if position is already filled.
            if custom_symbol in roster:
                # Skip rest of loop and try next position.
                continue

            # Get position's info
            position = formation['positions'][custom_symbol]

            # Check chemistry values of new player and linked teammates.
            if chemistry_matters:
                # Calculate current teammate potential chemistry in selected position.
                potential_chemistry = check_current_player_chemistry(player, position, roster)
                # If potential chemistry is not high enough, skip to next position or player.
                if potential_chemistry < req_link_chem:
                    continue

                # Check if the chemistry of linked of teammates is high enough.
                roster_copy = copy.deepcopy(roster)
                roster_copy[custom_symbol] = player
                # If potential chemistry of linked players is not high enough, skip to next position or player.
                if not check_linked_players_chemistry(position['links'], formation, roster_copy):
                    continue

            # All checks passed. Add player to roster and move on to next iteration.
            # Create copy of base IDs list and roster for recursive function
            base_ids_copy = copy.deepcopy(base_ids)
            roster_copy = copy.deepcopy(roster)

            # Place current player in position
            roster_copy[custom_symbol] = player
            base_ids_copy.append(player['baseId'])

            # Call recursive function
            results = recursive_create_2(players, player_db, formation, chemistry_matters, time_limit, budget,
                                         players_per_position, teams_per_formation, team_sort_attributes,
                                         player_sort_attributes, num_teams, pos_index, roster_copy, base_ids_copy,
                                         team_list, team_count, start_roster_num, must_have_players)
            team_list = results[0]
            team_count = results[1]

    return [team_list, team_count]


def puzzle_piece_create(players, player_db, formation, chemistry_matters, time_limit, budget, players_per_position,
                        teams_per_formation, team_sort_attributes, player_sort_attributes, num_teams,
                        pos_index=0, roster=None, base_ids=None, team_list=None, team_count=0,
                        start_roster_num=0, must_have_players=None):
    """
    Puzzle piece approach to build the best possible team combinations with good chemistry.
    Builds team through building up small pieces of players and combining them when possible.
    Input: PlayerDB of players, one formation, position index, roster, base IDs list, list of teams, and team count.
    Output: The list of teams and the team count.
    """

    players.sort(player_sort_attributes)

    if chemistry_matters:
        link_chem_avg = 0.3
    else:
        link_chem_avg = 0

    start_time = time.clock()
    puzzle_piece_index = ["rating", "position", "nation", "league", "club", "id", "baseId", "chem_needed"]
    puzzle_piece_bag = []
    partial_piece_bag = []
    complete_piece_bag = []
    complete_team_bag = []

    partial_piece_bag_total = 0
    complete_piece_bag_total = 0
    complete_team_bag_total = 0

    total_players = 60
    partial_piece_bag_max = 20000
    complete_piece_bag_max = 2000
    complete_team_bag_max = 250
    new_piece_bag_max = 20000

    formation_time = time.clock()
    for player_idx, player in enumerate(players.db[:total_players]):
        # Check to see if function should return
        if len(complete_team_bag) >= teams_per_formation or time.time() > time_limit:
            break

        print "Player " + str(player_idx + 1) + " of " + str(total_players)
        print "Formation: " + formation['name']
        iteration_time = time.clock()

        # Iterate through possible positions
        positions_list = [player['position']] + Team.Team.related_positions(player['position'], 'yellow')
        for player_position in positions_list:
            for custom_symbol, formation_position in formation['positions'].iteritems():

                # Check to see if function should return
                if len(complete_team_bag) >= teams_per_formation or time.time() > time_limit:
                    break

                if player_position == formation_position['symbol']:
                    new_piece_bag = []
                    new_complete_piece_bag = []

                    # Create small puzzle pieces for each related position
                    needed_chemistry = link_chem_avg * len(formation_position['links'])

                    puzzle_piece = (player['rating'],
                                    custom_symbol,
                                    player['nation']['id'],
                                    player['league']['id'],
                                    player['club']['id'],
                                    player['id'],
                                    player['baseId'],
                                    needed_chemistry)
                    puzzle_piece_bag.append(puzzle_piece)

                    rating_index = puzzle_piece_index.index('rating')
                    position_index = puzzle_piece_index.index('position')
                    baseId_index = puzzle_piece_index.index('baseId')
                    nation_index = puzzle_piece_index.index('nation')
                    league_index = puzzle_piece_index.index('league')
                    club_index = puzzle_piece_index.index('club')
                    chem_index = puzzle_piece_index.index('chem_needed')

                    # Create new combinations with new piece
                    for old_piece in puzzle_piece_bag:
                        # Check to see if function should return
                        if len(complete_team_bag) >= teams_per_formation or time.time() > time_limit:
                            break

                        # Check if piece touches position-wise and isn't the same player
                        if puzzle_piece[position_index] in formation['positions'][old_piece[position_index]]['links'] \
                                and puzzle_piece[baseId_index] != old_piece[baseId_index]:
                            # Check if any chemistry matches up
                            matches = 0
                            if puzzle_piece[nation_index] == old_piece[nation_index]:
                                matches += 1
                            if puzzle_piece[league_index] == old_piece[league_index]:
                                matches += 1
                                if puzzle_piece[club_index] == old_piece[club_index]:
                                    matches += 1
                            # If there were chemistry matches, create new piece
                            if matches > 0:

                                temp_list = list(old_piece)
                                temp_list[chem_index] -= matches
                                new_piece_1 = tuple(temp_list)

                                temp_list = list(puzzle_piece)
                                temp_list[chem_index] -= matches
                                new_piece_2 = tuple(temp_list)

                                # Create piece description tuple
                                new_piece_rating = float(
                                    new_piece_1[rating_index] + new_piece_2[rating_index]) / 2.0
                                new_piece_positions = [new_piece_1[position_index], new_piece_2[position_index]]
                                new_piece_positions.sort()
                                new_piece_positions = tuple(new_piece_positions)
                                piece_description_tuple = (new_piece_rating, new_piece_positions)

                                if new_piece_1[chem_index] <= 0 and new_piece_2[chem_index] <= 0:
                                    new_complete_piece_bag.append((piece_description_tuple,
                                                                   new_piece_1, new_piece_2))
                                    complete_piece_bag.append((piece_description_tuple, new_piece_1, new_piece_2))
                                    partial_piece_bag.append((piece_description_tuple, new_piece_1, new_piece_2))
                                else:
                                    partial_piece_bag.append((piece_description_tuple, new_piece_1, new_piece_2))
                                new_piece_bag.append((piece_description_tuple, new_piece_1, new_piece_2))

                    # Create larger combinations with new piece and existing partial piece
                    for old_block in partial_piece_bag:
                        # Check to see if function should return
                        if len(complete_team_bag) >= teams_per_formation or time.time() > time_limit:
                            break

                        positions_filled = []
                        base_ids = []
                        for small_piece in old_block[1:]:
                            positions_filled.append(small_piece[position_index])
                            base_ids.append(small_piece[baseId_index])

                        # Check if player is already used or if position is already filled
                        if puzzle_piece[baseId_index] in base_ids or puzzle_piece[
                            position_index] in positions_filled:
                            continue

                        # Check if pieces touches position-wise
                        adjacent_positions = []
                        for position in positions_filled:
                            if position in formation['positions'][puzzle_piece[position_index]]['links']:
                                adjacent_positions.append(position)

                        if not adjacent_positions:
                            continue

                        # Iterate through touching pieces and check for matches
                        total_matches = {}

                        for adjacent_position in adjacent_positions:
                            # Get piece of old block corresponding to position
                            for old_block_piece in old_block[1:]:
                                if old_block_piece[position_index] == adjacent_position:
                                    old_piece = old_block_piece
                                    break

                            # Check if any chemistry matches up
                            matches = 0
                            if puzzle_piece[nation_index] == old_piece[nation_index]:
                                matches += 1
                            if puzzle_piece[league_index] == old_piece[league_index]:
                                matches += 1
                                if puzzle_piece[club_index] == old_piece[club_index]:
                                    matches += 1

                            if matches > 0:
                                total_matches[adjacent_position] = matches

                        # If there were chemistry matches, create new piece
                        if total_matches:
                            new_block = []
                            positions_filled.append(puzzle_piece[position_index])

                            # Add old pieces to new block with updated chemistry
                            for old_block_piece in old_block[1:]:
                                if old_block_piece[position_index] in total_matches:
                                    temp_list = list(old_block_piece)
                                    temp_list[chem_index] -= total_matches[old_block_piece[position_index]]
                                    new_block.append(tuple(temp_list))
                                else:
                                    new_block.append(old_block_piece)

                            # Add new piece to new block with updated chemistry
                            total_matches_total = 0
                            for chem_value in total_matches.itervalues():
                                total_matches_total += chem_value

                            temp_list = list(puzzle_piece)
                            temp_list[chem_index] -= total_matches_total
                            new_block.append(tuple(temp_list))

                            new_block_tuple = tuple(new_block)

                            # Determine which bag to add the piece to. Complete requires 0 chem for all pieces.
                            # Check if a surrounded piece does not have enough chemistry (and thus the piece is useless)
                            independent_piece = True
                            useless_piece = False
                            total_rating = 0.0
                            # Iterate through each piece in the new block
                            for new_block_piece in new_block_tuple:
                                total_rating += new_block_piece[rating_index]

                                # Check the chem of the piece. All must be 0 to be independent.
                                if new_block_piece[chem_index] > 0:
                                    independent_piece = False

                                    # Check if piece is surrounded and still needs chemistry.
                                    piece_surrounded = True
                                    for piece_link in formation['positions'][new_block_piece[position_index]][
                                        'links']:
                                        if piece_link not in positions_filled:
                                            piece_surrounded = False

                                    # Piece is surrounded and still needs chemistry. It is useless.
                                    if piece_surrounded:
                                        useless_piece = True
                                        break

                            if not useless_piece:
                                # Create block description tuple
                                new_block_rating = total_rating / len(new_block_tuple)
                                new_block_positions = positions_filled
                                new_block_positions.sort()
                                new_block_positions = tuple(new_block_positions)
                                block_description_tuple = (new_block_rating, new_block_positions)

                                new_block_tuple = tuple([block_description_tuple] + list(new_block_tuple))

                                if independent_piece:
                                    # Complete, independent team
                                    if len(new_block_tuple) >= 11 + 1:  # +1 is for the description tup
                                        base_ids_list = []
                                        for tup in new_block_tuple[1:]:
                                            base_ids_list.append(tup[baseId_index])
                                        base_ids_list.sort()
                                        base_ids_tup = tuple(base_ids_list)
                                        new_block_tuple = list(new_block_tuple)
                                        new_block_tuple[0] = list(new_block_tuple[0]) + [base_ids_tup]
                                        new_block_tuple = tuple(new_block_tuple)

                                        duplicate = False
                                        for complete_team in complete_team_bag:
                                            if complete_team[0][2] == base_ids_tup:
                                                duplicate = True
                                                break
                                        if not duplicate:
                                            complete_team_bag.append(new_block_tuple)
                                    # Independent piece of a team
                                    else:
                                        new_complete_piece_bag.append(new_block_tuple)
                                        complete_piece_bag.append(new_block_tuple)
                                        partial_piece_bag.append(new_block_tuple)
                                else:
                                    # Piece of a team with dependencies
                                    partial_piece_bag.append(new_block_tuple)
                                new_piece_bag.append(new_block_tuple)

                    # Merge recently created blocks into new blocks based on current puzzle piece
                    for idx, new_combo_piece_1 in enumerate(new_piece_bag):
                        # Check to see if function should return
                        if len(complete_team_bag) >= teams_per_formation or time.time() > time_limit:
                            break

                        for new_combo_piece_2 in new_piece_bag[idx + 1:]:
                            # Check to see if function should return
                            if len(complete_team_bag) >= teams_per_formation or time.time() > time_limit:
                                break

                            positions_filled = list(new_combo_piece_1[0][1]) + list(new_combo_piece_2[0][1])
                            base_ids = []
                            for small_piece in new_combo_piece_1[1:]:
                                base_ids.append(small_piece[baseId_index])
                            for small_piece in new_combo_piece_2[1:]:
                                base_ids.append(small_piece[baseId_index])

                            # Check for duplicate players other than current player
                            if len(base_ids) - 1 != len(set(base_ids)) or \
                                            base_ids.count(puzzle_piece[baseId_index]) != 2:
                                continue
                            else:
                                base_ids = list(set(base_ids))
                            # Check for duplicate positions other than current player
                            if len(positions_filled) - 1 != len(set(positions_filled)) or \
                                            positions_filled.count(puzzle_piece[position_index]) != 2:
                                continue
                            else:
                                positions_filled = list(set(positions_filled))

                            # Check which pieces touches position-wise, not including the current piece
                            adjacent_positions = {}
                            combo_piece_1_positions = list(new_combo_piece_1[0][1])
                            combo_piece_2_positions = list(new_combo_piece_2[0][1])
                            combo_piece_1_positions.remove(puzzle_piece[position_index])
                            combo_piece_2_positions.remove(puzzle_piece[position_index])

                            # Find adjacent pieces across blocks
                            for position_1 in combo_piece_1_positions:
                                for position_2 in combo_piece_2_positions:
                                    if position_2 in formation['positions'][position_1]['links']:
                                        if position_1 in adjacent_positions:
                                            adjacent_positions[position_1].append(position_2)
                                        else:
                                            adjacent_positions[position_1] = [position_2]
                                        if position_2 in adjacent_positions:
                                            adjacent_positions[position_2].append(position_1)
                                        else:
                                            adjacent_positions[position_2] = [position_1]
                            for position_1 in combo_piece_1_positions:
                                if position_1 in formation['positions'][puzzle_piece[position_index]]['links']:
                                    if puzzle_piece[position_index] in adjacent_positions:
                                        adjacent_positions[puzzle_piece[position_index]].append(position_1)
                                    else:
                                        adjacent_positions[puzzle_piece[position_index]] = [position_1]
                            for position_2 in combo_piece_2_positions:
                                if position_2 in formation['positions'][puzzle_piece[position_index]]['links']:
                                    if puzzle_piece[position_index] in adjacent_positions:
                                        adjacent_positions[puzzle_piece[position_index]].append(position_2)
                                    else:
                                        adjacent_positions[puzzle_piece[position_index]] = [position_2]
                            # Remove duplicates
                            for key, adj_position_list in adjacent_positions.iteritems():
                                adjacent_positions[key] = list(set(adj_position_list))

                            if not adjacent_positions:
                                continue

                            # Iterate through touching pieces and check for matches
                            total_matches = {}

                            for current_position, adjacent_position_list in adjacent_positions.iteritems():
                                # Get piece of old block corresponding to current position
                                if current_position == puzzle_piece[position_index]:
                                    current_piece = puzzle_piece
                                elif current_position in new_combo_piece_1[0][1]:
                                    for old_block_piece in new_combo_piece_1[1:]:
                                        if old_block_piece[position_index] == current_position:
                                            current_piece = old_block_piece
                                            break
                                elif current_position in new_combo_piece_2[0][1]:
                                    for old_block_piece in new_combo_piece_2[1:]:
                                        if old_block_piece[position_index] == current_position:
                                            current_piece = old_block_piece
                                            break
                                else:
                                    print "Invalid current position: " + current_position

                                # Iterate through adjacent pieces to see if any chemistry matches up
                                matches = 0
                                for adjacent_position in adjacent_position_list:
                                    if adjacent_position in new_combo_piece_1[0][1]:
                                        for old_block_piece in new_combo_piece_1[1:]:
                                            if old_block_piece[position_index] == adjacent_position:
                                                adjacent_piece = old_block_piece
                                                break
                                    elif adjacent_position in new_combo_piece_2[0][1]:
                                        for old_block_piece in new_combo_piece_2[1:]:
                                            if old_block_piece[position_index] == adjacent_position:
                                                adjacent_piece = old_block_piece
                                                break
                                    else:
                                        print "Invalid adjacent position: " + adjacent_position

                                    # Check if any chemistry matches up
                                    if current_piece[nation_index] == adjacent_piece[nation_index]:
                                        matches += 1
                                    if current_piece[league_index] == adjacent_piece[league_index]:
                                        matches += 1
                                        if current_piece[club_index] == adjacent_piece[club_index]:
                                            matches += 1

                                if matches > 0:
                                    total_matches[current_position] = matches

                            # If there were chemistry matches, create new piece
                            if total_matches:
                                new_block = []

                                # Add current piece to new block
                                temp_list = list(puzzle_piece)
                                temp_list[chem_index] -= total_matches[puzzle_piece[position_index]]
                                new_block.append(tuple(temp_list))

                                # Add old pieces to new block with updated chemistry
                                for old_block_piece in new_combo_piece_1[1:]:
                                    if old_block_piece[position_index] == puzzle_piece[position_index]:
                                        continue
                                    if old_block_piece[position_index] in total_matches:
                                        temp_list = list(old_block_piece)
                                        temp_list[chem_index] -= total_matches[old_block_piece[position_index]]
                                        new_block.append(tuple(temp_list))
                                    else:
                                        new_block.append(old_block_piece)

                                for old_block_piece in new_combo_piece_2[1:]:
                                    if old_block_piece[position_index] == puzzle_piece[position_index]:
                                        continue
                                    if old_block_piece[position_index] in total_matches:
                                        temp_list = list(old_block_piece)
                                        temp_list[chem_index] -= total_matches[old_block_piece[position_index]]
                                        new_block.append(tuple(temp_list))
                                    else:
                                        new_block.append(old_block_piece)

                                new_block_tuple = tuple(new_block)

                                # Determine which bag to add the piece to. Complete requires 0 chem for all pieces.
                                # Check if a surrounded piece does not have enough chemistry
                                # (and thus the piece is useless)
                                independent_piece = True
                                useless_piece = False
                                total_rating = 0.0
                                # Iterate through each piece in the new block
                                for new_block_piece in new_block_tuple:
                                    total_rating += new_block_piece[rating_index]

                                    # Check the chem of the piece. All must be 0 to be independent.
                                    if new_block_piece[chem_index] > 0:
                                        independent_piece = False

                                        # Check if piece is surrounded and still needs chemistry.
                                        piece_surrounded = True
                                        for piece_link in \
                                                formation['positions'][new_block_piece[position_index]]['links']:
                                            if piece_link not in positions_filled:
                                                piece_surrounded = False

                                        # Piece is surrounded and still needs chemistry. It is useless.
                                        if piece_surrounded:
                                            useless_piece = True
                                            break

                                if not useless_piece:
                                    # Create block description tuple
                                    new_block_rating = total_rating / len(new_block_tuple)
                                    new_block_positions = positions_filled
                                    new_block_positions.sort()
                                    new_block_positions = tuple(new_block_positions)
                                    block_description_tuple = (new_block_rating, new_block_positions)

                                    new_block_tuple = tuple([block_description_tuple] + list(new_block_tuple))

                                    if independent_piece:
                                        # Complete, independent team
                                        if len(new_block_tuple) >= 11 + 1:  # +1 is for the description tup
                                            base_ids_list = []
                                            for tup in new_block_tuple[1:]:
                                                base_ids_list.append(tup[baseId_index])
                                            base_ids_list.sort()
                                            base_ids_tup = tuple(base_ids_list)
                                            new_block_tuple = list(new_block_tuple)
                                            new_block_tuple[0] = list(new_block_tuple[0]) + [base_ids_tup]
                                            new_block_tuple = tuple(new_block_tuple)

                                            duplicate = False
                                            for complete_team in complete_team_bag:
                                                if complete_team[0][2] == base_ids_tup:
                                                    duplicate = True
                                                    break
                                            if not duplicate:
                                                complete_team_bag.append(new_block_tuple)
                                        # Independent piece of a team
                                        else:
                                            new_complete_piece_bag.append(new_block_tuple)
                                            complete_piece_bag.append(new_block_tuple)
                                            partial_piece_bag.append(new_block_tuple)
                                    else:
                                        # Piece of a team with dependencies
                                        partial_piece_bag.append(new_block_tuple)
                                    new_piece_bag.append(new_block_tuple)
                        new_piece_bag.sort(key=lambda tup: (len(tup[0][1]), tup[0][0]), reverse=True)
                        new_piece_bag = new_piece_bag[:new_piece_bag_max]
                    print "new_piece_bag total:   " + str(len(new_piece_bag))

                    # Merge complete independent pieces together
                    for complete_piece_1 in new_complete_piece_bag:
                        # Check to see if function should return
                        if len(complete_team_bag) >= teams_per_formation or time.time() > time_limit:
                            break

                        for complete_piece_2 in complete_piece_bag:
                            # Check to see if function should return
                            if len(complete_team_bag) >= teams_per_formation or time.time() > time_limit:
                                break

                            # Check if duplicate players
                            all_player_ids = []
                            for complete_tup in complete_piece_1[1:]:
                                all_player_ids.append(complete_tup[baseId_index])
                            for complete_tup in complete_piece_2[1:]:
                                all_player_ids.append(complete_tup[baseId_index])
                            if len(all_player_ids) != len(set(all_player_ids)):
                                continue

                            # Check if duplicate positions
                            all_positions = list(complete_piece_1[0][1]) + list(complete_piece_2[0][1])
                            if len(all_positions) != len(set(all_positions)):
                                continue

                            # Create new independent block
                            # Currently ignores additional chemistry connections!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            # Currently seems irrelevant since they are maxed out!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            complete_piece_1_list = list(complete_piece_1)
                            complete_piece_2_list = list(complete_piece_2)
                            new_block_tuple = tuple(tuple(complete_piece_1_list[1:] + complete_piece_2_list[1:]))
                            new_block_rating = ((complete_piece_1[0][0] * len(complete_piece_1[0][1])) +
                                                (complete_piece_2[0][0] * len(complete_piece_2[0][1]))) / \
                                               len(all_positions)
                            new_block_positions = all_positions
                            new_block_positions.sort()
                            new_block_positions = tuple(new_block_positions)
                            block_description_tuple = (new_block_rating, new_block_positions)

                            new_block_tuple = tuple([block_description_tuple] + list(new_block_tuple))

                            # Complete, independent team
                            if len(new_block_tuple) >= 11 + 1:  # +1 is for the description tup
                                base_ids_list = all_player_ids
                                base_ids_list.sort()
                                base_ids_tup = tuple(base_ids_list)
                                new_block_tuple = list(new_block_tuple)
                                new_block_tuple[0] = list(new_block_tuple[0]) + [base_ids_tup]
                                new_block_tuple = tuple(new_block_tuple)

                                duplicate = False
                                for complete_team in complete_team_bag:
                                    if complete_team[0][2] == base_ids_tup:
                                        duplicate = True
                                        break
                                if not duplicate:
                                    complete_team_bag.append(new_block_tuple)
                            # Independent piece of a team
                            else:
                                new_complete_piece_bag.append(new_block_tuple)
                                complete_piece_bag.append(new_block_tuple)
                                partial_piece_bag.append(new_block_tuple)

        puzzle_piece_bag.sort(key=lambda tup: tup[0], reverse=True)
        partial_piece_bag.sort(key=lambda tup: (len(tup[0][1]), tup[0][0]), reverse=True)
        complete_piece_bag.sort(key=lambda tup: (len(tup[0][1]), tup[0][0]), reverse=True)
        complete_team_bag.sort(key=lambda tup: (tup[0][0]), reverse=True)

        if partial_piece_bag_total < partial_piece_bag_max:
            partial_piece_bag_total = len(partial_piece_bag)
        else:
            partial_piece_bag_total += (len(partial_piece_bag) - partial_piece_bag_max)

        if complete_piece_bag_total < complete_piece_bag_max:
            complete_piece_bag_total = len(complete_piece_bag)
        else:
            complete_piece_bag_total += (len(complete_piece_bag) - complete_piece_bag_max)

        if complete_team_bag_total < complete_team_bag_max:
            complete_team_bag_total = len(complete_team_bag)
        else:
            complete_team_bag_total += (len(complete_team_bag) - complete_team_bag_max)

        partial_piece_bag = partial_piece_bag[:partial_piece_bag_max]
        complete_piece_bag = complete_piece_bag[:complete_piece_bag_max]
        complete_team_bag = complete_team_bag[:complete_team_bag_max]

        print "puzzle_piece_bag total:   " + str(len(puzzle_piece_bag))
        print "partial_piece_bag total:  " + str(partial_piece_bag_total)
        print "complete_piece_bag total: " + str(complete_piece_bag_total)
        print "complete_team_bag total:  " + str(complete_team_bag_total)
        if len(puzzle_piece_bag) > 0:
            print "Best Piece Rating:        " + str(puzzle_piece_bag[0][0])
        if len(partial_piece_bag) > 0:
            print "Best Partial Rating:      " + str(partial_piece_bag[0][0][0]) + "     Size: " + str(len(partial_piece_bag[0][0][1]))
        if len(complete_piece_bag) > 0:
            print "Best Complete Rating:     " + str(complete_piece_bag[0][0][0]) + "     Size: " + str(len(complete_piece_bag[0][0][1]))
        if len(complete_team_bag) > 0:
            print "Best Team Rating:         " + str(complete_team_bag[0][0][0])

        iteration_time_data = time.clock() - iteration_time
        minutes = str(int(iteration_time_data / 60))
        seconds = str(int(iteration_time_data % 60))
        if minutes == '0' and seconds == '0':
            seconds = '<1'
        print "Iteration time: " + minutes + ' minutes     ' + seconds + ' seconds'
        formation_time_data = time.clock() - formation_time
        minutes = str(int(formation_time_data / 60))
        seconds = str(int(formation_time_data % 60))
        print "Formation time: " + minutes + ' minutes     ' + seconds + ' seconds'
        total_time_data = time.clock() - start_time
        minutes = str(int(total_time_data / 60))
        seconds = str(int(total_time_data % 60))
        print "Total time:     " + minutes + ' minutes     ' + seconds + ' seconds'
        print ""

    if team_list is None:
        team_list = []
    for team in complete_team_bag:
        # Create the roster of player positions and IDs
        roster = {}
        for position in team[1:]:
            roster[position[1]] = players.search({'id': (position[5], 'exact')})[0]

        # Set the team using the roster and add to list
        temp_team = Team.Team()
        temp_team.set_team(formation, roster)
        team_list.append(temp_team.__dict__)
        team_count += 1

        # Narrow down team_list to save memory
        if (team_count % num_teams) == 0:
            print "Calculating... %d teams created" % team_count
            team_list = reduce_teams(team_sort_attributes, num_teams, team_list)

    return [team_list, team_count]


def enough_players(players, formation, chemistry_matters):
    """
    Quickly checks if there are players for each of the positions in the formation.
    Input: PlayerDB of players, a formation, and if chemistry matters.
    Output: Boolean of whether there are enough players.
    """

    # Get what level of similarity matters when searching for players
    if chemistry_matters:
        similarity = 'yellow'
    else:
        similarity = 'orange'

    for position in formation['positions'].itervalues():
        standard_position = position['symbol']

        # Get related positions that could fill that role
        related_positions = Team.Team.related_positions(standard_position, similarity)

        # Create position tuple list for the player search
        position_tuple_list = [{'position': (standard_position, 'exact')}]
        for x in related_positions:
            position_tuple_list.append({'position': (x, 'exact')})

        # Get all eligible players and check if any exist
        if len(players.multi_search(position_tuple_list)) < 1:
            # No players match the position - don't try to create teams for this formation
            return False

    return True


def find_teams_ultimate(players, player_db, formations):
    """
    Finds the best team using my thorough method from the given players and formations.
    Input: PlayerDB of players, FormationDB of formations, and the process type.
    Output: A list of the best teams using my thorough method.
    """

    # Team lists and counts for both process types
    team_list_mp = []  # List of teams created in pool
    team_list_sp = []  # List of teams created in single process
    count_mp = 0  # Count of teams created in pool
    count_sp = 0  # Count of teams created in single process

    # Get configuration values
    with open(config_filename, 'r') as f:
        configs = json.load(f)['ultimate_team_configs']
        f.close()

    # Get mandatory configuration values
    process = configs['process_type']
    team_sort_attributes = configs['team_sort_attributes']
    if len(team_sort_attributes) < 1:
        team_sort_attributes.append('rating')
    player_sort_attributes = configs['player_sort_attributes']
    if len(player_sort_attributes) < 1:
        player_sort_attributes.append('rating')
    chemistry_matters = configs['chemistry_matters']
    roster = configs['roster']

    # Get optional configuration values or set the defaults
    if configs['budget'][0] and configs['budget'][1] >= 200:
        budget = configs['budget'][1]
        budget_players = PlayerDB(player_db.search({'price': (budget, 'lower')}))
        budget_players = PlayerDB(budget_players.search({'price': (1, 'higher')}))  # Skip players with incorrect prices
    else:
        budget = configs['max_values']['budget']  # Sets budget to -1, so no new players are added
        budget_players = PlayerDB()
    if configs['players_per_position'][0]:
        players_per_position = configs['players_per_position'][1]
    else:
        players_per_position = configs['max_values']['players_per_position']
    if configs['teams_per_formation'][0]:
        teams_per_formation = configs['teams_per_formation'][1]
    else:
        teams_per_formation = configs['max_values']['teams_per_formation']
    if configs['num_teams_returned'][0]:
        num_teams = configs['num_teams_returned'][1]
    else:
        num_teams = configs['max_values']['num_teams_returned']
    if configs['time_limit'][0]:
        time_limit = time.time() + configs['time_limit'][1]
    else:
        time_limit = time.time() + configs['max_values']['time_limit']

    # If roster exists, set the base IDs list
    base_ids = []
    if roster:
        for player in roster.itervalues():
            base_ids.append(player['baseId'])

    start_roster_num = 0
    must_have_players = None
    #  Check if players without positions are assigned
    if any(key in roster for key in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']):
        # Set the number of players starting on the roster
        start_roster_num = len(roster)
        # Assign roster players to special list to be assigned
        must_have_players = PlayerDB()
        must_have_players.add(list(roster.values()))
        # Delete roster
        roster.clear()
        base_ids = []

    # Remove links to locked positions
    if 0 in base_ids and len(formations.db) == 1:
        # Get locked positions
        locked_positions = []
        for sym, position in roster.iteritems():
            if position['rating'] == 0:
                locked_positions.append(sym)
        # Remove links to locked positions
        for position in formations.db[0]['positions'].itervalues():
            for locked_position in locked_positions:
                if locked_position in position['links']:
                    position['links'].remove(locked_position)

    if process in ['multi', 'both']:
        # Multiprocess Method --------------------------------------------------------------------------------------
        # Create objects for recursive function
        pool = Pool()  # Create process pool
        input_tuples = []  # List of tuples for the map function

        # Create tuple list for each formation
        for formation in formations.db:
            if enough_players(players, formation, chemistry_matters):
                input_tuples.append((
                    players, budget_players, formation, chemistry_matters, time_limit, budget, players_per_position,
                    teams_per_formation, team_sort_attributes, player_sort_attributes, num_teams, roster, base_ids,
                    start_roster_num, must_have_players))

        # Temporary Timing Information------------------------------------------------------------------------------
        print "Start Multi Process!"
        start_time = time.clock()
        from time import localtime, strftime
        print "Start Time: " + strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())
        # ----------------------------------------------------------------------------------------------------------

        # Run function for each formation
        results_mp = pool.map(recursive_create_tup, input_tuples)

        # Temporary Timing Information------------------------------------------------------------------------------
        end_time = time.clock()
        print "Finished Multi!     Time:" + str(end_time - start_time)
        print ''
        # ----------------------------------------------------------------------------------------------------------

        # Combine results from all formations into one list
        for result_list in results_mp:
            team_list_mp += result_list[0]
            count_mp += result_list[1]
        # ----------------------------------------------------------------------------------------------------------

    if (process == 'single') or (process == 'both'):
        # Single Process Method ------------------------------------------------------------------------------------
        # Temporary Timing Information------------------------------------------------------------------------------
        print "Start Single Process!"
        start_all_time = time.clock()
        from time import localtime, strftime
        print "Start Time: " + strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())
        # ----------------------------------------------------------------------------------------------------------

        # Iterate through the formations
        for formation in formations.db:

            if enough_players(players, formation, chemistry_matters):
                # Temporary Timing Information--------------------------------------------------------------------------
                print "Round Start!"
                start_time = time.clock()
                # ------------------------------------------------------------------------------------------------------

                # Call recursive team building function
                results_sp = recursive_create_2(
                    players, budget_players, formation, chemistry_matters, time_limit, budget, players_per_position,
                    teams_per_formation, team_sort_attributes, player_sort_attributes, num_teams, roster=roster,
                    base_ids=base_ids, start_roster_num=start_roster_num, must_have_players=must_have_players)

                team_list_sp += results_sp[0]
                count_sp += results_sp[1]

                # Temporary Timing Information--------------------------------------------------------------------------
                end_time = time.clock()
                print "Finished!     Time:" + str(end_time - start_time)
                # ------------------------------------------------------------------------------------------------------

        # Temporary Timing Information------------------------------------------------------------------------------
        end_all_time = time.clock()
        print "Finished Single!     Time:" + str(end_all_time - start_all_time)
        print ''
        # ----------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------

    # Check if both process types ran
    if process == 'both':

        # Combine results from both processes
        all_teams_list = team_list_mp + team_list_sp
        count = count_mp + count_sp

        if len(all_teams_list) > 0:
            print "Created %d different teams" % count
            return all_teams_list

        else:
            # No teams
            print "Unable to create a good team"
            return {}

    # Return best teams from multi process
    elif process == 'multi' and len(team_list_mp) > 0:

        print "Created %d different teams using multi process" % count_mp
        return team_list_mp

    # Return best teams from single process
    elif process == 'single' and len(team_list_sp) > 0:

        print "Created %d different teams using single process" % count_sp
        return team_list_sp

    # No teams
    print "Unable to create a good team"
    return []


def find_team_ultimate(players, player_db, formations):
    """
    Calls the find_teams_ultimate function and sorts and returns the results.
    Input: PlayerDB of players and FormationDB of formations.
    Output: The best team using my thorough method.
    """

    # List of teams returned from find_teams_ultimate
    team_list = find_teams_ultimate(players, player_db, formations)

    # Pick the top specified number of teams and ties.
    # Sort teams by rating and total individual chemistry
    team_list = sorted(team_list, key=lambda k: (k['rating'], k['total_ic']), reverse=True)

    # Get number of teams to return (plus tied teams)
    with open(config_filename, 'r') as f:
        configs = json.load(f)['ultimate_team_configs']
        f.close()

    if configs['num_teams_returned'][0]:
        num_teams = configs['num_teams_returned'][1]
    else:
        num_teams = configs['max_values']['num_teams_returned']

    # Iterate through teams until tie is broken if more than specified number of teams
    if len(team_list) > num_teams:

        # Check for ties and include in teams returned
        last_rating = team_list[num_teams-1]['rating']
        last_ic = team_list[num_teams-1]['total_ic']
        teams_to_return = num_teams

        for team in team_list[num_teams:]:
            if team['rating'] == last_rating and team['total_ic'] == last_ic:
                teams_to_return += 1
            else:
                break

        # Return the specified number of teams and ties
        return team_list[:teams_to_return]

    # Less teams than requested, return all
    else:

        return team_list
