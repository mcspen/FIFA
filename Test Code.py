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

    # Puzzle Piece Team Creation
    player_list = PlayerDB()
    player_list.load('my_players_17', 'list')
    player_list.sort(['rating'])
    # player_list.sort(['price', 'rating'], False)
    link_chem_avg = 0.3

    start_time = time.clock()
    for formation_idx, formation in enumerate(formation_db.db):
        puzzle_piece_index = ["rating", "position", "nation", "league", "club", "id", "baseId", "chem_needed"]
        puzzle_piece_bag = []
        partial_piece_bag = []
        complete_piece_bag = []
        complete_team_bag = []

        partial_piece_bag_total = 0
        complete_piece_bag_total = 0
        complete_team_bag_total = 0
        save_counter = 1
        save_interval = 50

        total_players = 60
        partial_piece_bag_max = 20000
        complete_piece_bag_max = 2000
        complete_team_bag_max = 250
        new_piece_bag_max = 20000

        formation_time = time.clock()
        for player_idx, player in enumerate(player_list.db[:total_players]):
            print "Player " + str(player_idx + 1) + " of " + str(total_players)
            print "Formation " + str(formation_idx + 1) + " of " + str(len(formation_db.db)) + ' - ' + formation['name']
            iteration_time = time.clock()

            # Iterate through possible positions
            positions_list = [player['position']] + Team.related_positions(player['position'], 'yellow')
            for player_position in positions_list:

                for custom_symbol, formation_position in formation['positions'].iteritems():
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
                                    new_piece_rating = float(new_piece_1[rating_index] + new_piece_2[rating_index]) / 2.0
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
                            positions_filled = []
                            base_ids = []
                            for small_piece in old_block[1:]:
                                positions_filled.append(small_piece[position_index])
                                base_ids.append(small_piece[baseId_index])

                            # Check if player is already used or if position is already filled
                            if puzzle_piece[baseId_index] in base_ids or puzzle_piece[position_index] in positions_filled:
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
                                        for piece_link in formation['positions'][new_block_piece[position_index]]['links']:
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
                                        if len(new_block_tuple) >= 11+1:  # +1 is for the description tup
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
                            for new_combo_piece_2 in new_piece_bag[idx+1:]:

                                positions_filled = list(new_combo_piece_1[0][1]) + list(new_combo_piece_2[0][1])
                                base_ids = []
                                for small_piece in new_combo_piece_1[1:]:
                                    base_ids.append(small_piece[baseId_index])
                                for small_piece in new_combo_piece_2[1:]:
                                    base_ids.append(small_piece[baseId_index])

                                # Check for duplicate players other than current player
                                if len(base_ids)-1 != len(set(base_ids)) or \
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
                            for complete_piece_2 in complete_piece_bag:

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
                print "Best Partial Rating:      " + str(partial_piece_bag[0][0][0])
            if len(complete_piece_bag) > 0:
                print "Best Complete Rating:     " + str(complete_piece_bag[0][0][0])
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

            if complete_team_bag_total / save_interval == save_counter:
                save_counter += 1
                file_path = 'JSONs/Puzzle/' + str(formation['name']) + ' - ' + str(complete_team_bag_total) + '.json'

                with open(file_path, 'w') as f:
                    json.dump(complete_team_bag, f)
                    f.close()

        file_path = 'JSONs/Puzzle/' + str(formation['name']) + ' - ' + str(complete_team_bag_total) + '.json'

        with open(file_path, 'w') as f:
            json.dump(complete_team_bag, f)
            f.close()

    # Create Team DB from Puzzle Team List
    '''filename = "3-5-2 - 289"
    file_path = 'JSONs/Puzzle/' + filename + '.json'
    with open(file_path, 'r') as f:
        teams_list = json.load(f)
        f.close()

    player_list.load('my_players_17', 'list')
    puzzle_team_list = TeamDB()
    formation = formation_db.db[3]

    for team in teams_list:
        roster = {}
        for position in team[1:]:
            roster[position[1]] = player_list.search({'id': (position[5], 'exact')})[0]
        temp_team = Team()
        temp_team.set_team(formation, roster)
        puzzle_team_list.add_team(temp_team)

    puzzle_team_list.save("Chem Test 4")'''

    # Iterative Team Creation
    """player_list = PlayerDB()
    player_list.load('my_players_17', 'list')
    player_list.sort(['rating'])
    team = Team()
    teams = TeamDB()

    player_counter = 10

    while len(teams.db) < 50:
        player_counter += 5
        teams = TeamDB(team.create_team_ultimate(PlayerDB(player_list.db[:player_counter]), player_db, formation_db))
    teams.save("Iterative Create Test 3")

    print player_counter"""

    # Player DB Profile Function
    #player_db = PlayerDB()
    #player_db.load('my_players_17', 'list')
    #player_db.profile()

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
    """image_file_names = ['award_winner', 'confederation_champions_motm', 'halloween', 'movember', 'tott']
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
