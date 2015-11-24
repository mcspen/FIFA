"""
All of the functions containing the logic to create the ultimate teams.
"""

from PlayerDB import PlayerDB
import Team
import time
import copy
import json
from multiprocessing import Pool


def recursive_create_tup(tup):
    """
    Wrapper function to all Team.recursive_create_tup to be called by pool
    """
    return recursive_create(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])


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
            return [{'nation': (roster[dependent_positions[0][0]]['nation']['name'], 'exact'),
                    'league': (roster[dependent_positions[0][0]]['league']['name'], 'exact')}]

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
                            league = roster[club_position[0]]['club']['name']

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


def recursive_create(players, formation, time_limit, players_per_position, teams_per_formation, sort_attributes,
                     num_teams, pos_index=0, roster=None, base_ids=None, team_list=None, team_count=0):
    """
    Recursive function to build all possible team combinations with good chemistry
    Input: PlayerDB of players, one formation, position index, roster, base IDs list, list of teams, and team count.
    Output: The list of teams and the team count
    """

    print_formation_name_and_team_count = False
    print_all_team_chemistry = False
    positions_less = 5
    positions_greater = 9
    print_positions_less = False
    print_positions_greater = True

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

        # Print out progress information
        if print_formation_name_and_team_count:
            print "%s: %d team(s)" % (formation['name'], team_count)

        # Print out team chemistry ---------------------------------------------------------------------------------
        if print_all_team_chemistry:
            for team in team_list:
                temp = Team.Team(team)
                temp.print_summary()
                temp.print_chemistry_stats()
                print ''
        # TEMPORARY ------------------------------------------------------------------------------------------------

        # Narrow down team_list to save memory
        if (team_count % num_teams) == 0:
            print "Calculating... %d teams created" % team_count

            def compare(current_team):
                """
                Comparison function for sorting the teams based on attributes list in config file.
                """
                attribute_tuple = ()
                for attribute in sort_attributes:

                    if attribute in current_team:
                        attribute_tuple += (current_team[attribute],)
                    else:
                        print "Invalid Attribute: %s" % attribute

                return attribute_tuple

            # Compare teams and narrow down to specified max number of teams
            sorted_list = sorted(team_list, key=compare, reverse=True)
            return [sorted_list[:num_teams], team_count]

        # Check to see if function should return
        if team_count >= teams_per_formation or time.time() > time_limit:
            return [team_list, team_count]

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

    # Check previously assigned players for critical dependencies
    # Get list of previously assigned players
    recheck_list = []
    for link in position['links']:

        # Check if position is already assigned and if it is add position to recheck list
        if link in roster:
            recheck_list.append(link)

    # Recheck chemistry of previously assigned positions for critical dependencies
    dependent_pos = []
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
        if recheck_chemistry < 1:
            needed_chem = (1.0 - recheck_chemistry) * len(formation['positions'][recheck_position]['links'])
            dependent_pos.append((recheck_position, needed_chem))

    # Get all eligible positions (exact and related) for current position
    pos_list = Team.Team.related_positions(position['symbol'])

    # If no dependent players, simple search
    if len(dependent_pos) < 1:

        # Create position tuple list for the player search
        position_tuple_list = [{'position': (position['symbol'], 'exact')}]
        for x in pos_list:
            position_tuple_list.append({'position': (x, 'exact')})

        # Get all eligible players and create DB
        eligible_players = PlayerDB(players.multi_search(position_tuple_list))

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

        del position_tuple_list
        del dependency_tuple_list
        del dependency_match

    # Sort eligible players by rating
    # eligible_players.sort(['rating'])
    eligible_players.special_sort(position['symbol'])

    # Set variables for controlling the scope of team creation
    if players_per_position < 1:
        players_per_position = len(eligible_players.db)
    players_checked = 0

    # Iterate through eligible players for current position
    for player in eligible_players.db:

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
        for link in position['links']:

            # Player is assigned. Get link chemistry.
            if link in roster:
                potential_chemistry += Team.Team.teammate_chemistry(player, roster[link])

            # Player not assigned yet. Best possible chemistry is 3
            else:
                potential_chemistry += 3

        potential_chemistry /= len(position['links'])

        # Check if player meets chemistry requirements (must at least be 1 to reach 10 individual chemistry)
        if potential_chemistry >= 1:

            # Create copy of base IDs list and roster for recursive function
            base_ids_copy = copy.deepcopy(base_ids)
            roster_copy = copy.deepcopy(roster)

            # Place current player in position
            roster_copy[custom_symbol] = player
            base_ids_copy.append(player['baseId'])

            # Call recursive function
            results = recursive_create(players, formation, time_limit, players_per_position, teams_per_formation,
                                       sort_attributes, num_teams, next_index, roster_copy, base_ids_copy, team_list,
                                       team_count)
            team_list = results[0]
            team_count = results[1]

            # Check to see if function should return
            if team_count >= teams_per_formation or time.time() > time_limit:
                return [team_list, team_count]

    return [team_list, team_count]


def find_teams_ultimate(players, formations):
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
    with open('ultimate_team_configs.json', 'r') as f:
        configs = json.load(f)
        f.close()

    process = configs['process_type']
    sort_attributes = configs['sort_attributes']

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

    if process in ['multi', 'both']:
        # Multiprocess Method --------------------------------------------------------------------------------------
        # Create objects for recursive function
        pool = Pool()  # Create process pool
        input_tuples = []  # List of tuples for the map function

        # Create tuple list for each formation
        for formation in formations.db:
            input_tuples.append((players, formation, time_limit, players_per_position,
                                 teams_per_formation, sort_attributes, num_teams))

        # Temporary Timing Information------------------------------------------------------------------------------
        print "Start Multi Process!"
        start_time = time.clock()
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
        # ----------------------------------------------------------------------------------------------------------

        # Iterate through the formations
        for formation in formations.db:

            # Temporary Timing Information--------------------------------------------------------------------------
            print "Round Start!"
            start_time = time.clock()
            # ------------------------------------------------------------------------------------------------------

            # Call recursive team building function
            results_sp = recursive_create(players, formation, time_limit, players_per_position,
                                          teams_per_formation, sort_attributes, num_teams)

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


def find_team_ultimate(players, formations):
    """
    Calls the find_teams_ultimate function and sorts and returns the results.
    Input: PlayerDB of players, FormationDB of formations, process type, and the minimum number of teams to return.
    Output: The best team using my thorough method.
    """

    # List of teams returned from find_teams_ultimate
    team_list = find_teams_ultimate(players, formations)

    # Pick the top specified number of teams and ties.
    # Sort teams by rating and total individual chemistry
    team_list = sorted(team_list, key=lambda k: (k['rating'], k['total_ic']), reverse=True)

    # Get number of teams to return (plus tied teams)
    with open('ultimate_team_configs.json', 'r') as f:
        configs = json.load(f)
        f.close()
    num_teams = configs['num_teams_returned']

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
