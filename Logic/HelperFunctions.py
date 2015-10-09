"""
Helper functions that don't belong to any class
"""

__author__ = 'mspencer'

import unicodedata


def ascii_text(input_text):
    return unicodedata.normalize('NFKD', input_text).encode('ascii', 'ignore')


def player_info_labels(attributes):
    """
    Gets the labels of the players info to be displayed
    Input: The list of attributes
    Output: A list of the labels of the players info
    """

    # Player's base info
    labels = ['Name', 'Rat.', 'Pos.', 'Color', 'Nation', 'League', 'Club']

    # Remove attributes already displayed
    for attr in ['club', 'color', 'commonName', 'firstName', 'lastName', 'league', 'name',
                 'name_custom', 'nation', 'position', 'positionFull', 'rating']:
        while attributes.count(attr) > 0:
            attributes.remove(attr)

    # Add attributes from list
    for attribute in attributes:
        if attribute in ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY", "DIV", "HAN", "KIC", "REF", "SPD", "POS"]:
            labels.append(attribute)
        else:
            labels.append(attribute[:3].capitalize()+'.')

    return labels


def player_info(player, attributes):
    """
    Gets the name and attributes of the given player and specified attributes
    Input: The player and list of attributes
    Output: A list of the players info
    """

    player_info = []

    # Get player's common name
    common_name = unicodedata.normalize('NFKD', player['commonName']).encode('ascii', 'ignore')

    # Get player's name
    player_name = unicodedata.normalize('NFKD', player['firstName']).encode('ascii', 'ignore') + ' ' + \
                  unicodedata.normalize('NFKD', player['lastName']).encode('ascii', 'ignore')

    # If the player has a common name, use it
    if len(common_name) > 0:
        player_info.append(common_name)
    else:
        player_info.append(player_name)

    # Player's rating
    player_info.append(str(player['rating']))

    # Player's position
    player_info.append(player['position'])

    # Player's card color
    player_info.append(player['color'])

    # Player's nation
    nation = unicodedata.normalize('NFKD', player['nation']['name']).encode('ascii', 'ignore')
    player_info.append(nation[:20])

    # Player's league
    league = unicodedata.normalize('NFKD', player['league']['name']).encode('ascii', 'ignore')
    player_info.append(league[:20])

    # Get player's club
    club = unicodedata.normalize('NFKD', player['club']['name']).encode('ascii', 'ignore')
    player_info.append(club[:20])

    # Remove attributes already displayed
    for attr in ['club', 'color', 'commonName', 'firstName', 'lastName', 'name',
                 'name_custom', 'nation', 'position', 'positionFull', 'rating']:
        while attributes.count(attr) > 0:
            attributes.remove(attr)

    # Add attributes from list
    for attribute in attributes:
        # Attributes for non-goalkeepers
        if attribute in ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY']:
            if not player['isGK']:
                index = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY'].index(attribute)
                player_value = player['attributes'][index]['value']
            else:
                player_value = 0
            player_info.append(str(player_value))
        # Attributes for goalkeepers
        elif attribute in ['DIV', 'HAN', 'KIC', 'REF', 'SPD', 'POS']:
            if player['isGK']:
                index = ['DIV', 'HAN', 'KIC', 'REF', 'SPD', 'POS'].index(attribute)
                player_value = player['attributes'][index]['value']
            else:
                player_value = 0
            player_info.append(str(player_value))
        elif attribute in ['clubId', 'leagueId', 'nationId']:
            player_info.append(str(player[attribute[:-2]]['id']))
        else:
            player_info.append(str(player[attribute]))

    return player_info


def format_attr_name(attribute):
    if attribute in ["commonName", "firstName", "lastName", "birthdate", "weakFoot", "playerType", "positionFull",
                     "itemType", "modelName"]:
        return attribute[:-4].capitalize() + " " + attribute[-4:].capitalize()
    elif attribute in ["playStyle", "skillMoves", "longshots", "shotpower", "sprintspeed"]:
        return attribute[:-5].capitalize() + " " + attribute[-5:].capitalize()
    elif attribute in ["slidingtackle", "standingtackle"]:
        return attribute[:-6].capitalize() + " " + attribute[-6:].capitalize()
    elif attribute in ["ballcontrol", "longpassing", "shortpassing"]:
        return attribute[:-7].capitalize() + " " + attribute[-7:].capitalize()
    elif attribute in ["gkdiving", "gkhandling", "gkkicking", "gkpositioning", "gkreflexes"]:
        return attribute[:2].upper() + " " + attribute[2:].capitalize()
    elif attribute == "headshotImgUrl":
        return "Headshot IMG URL"
    elif attribute == "name_custom":
        return "Name - Any Part"
    elif attribute == "freekickaccuracy":
        return "FK Accuracy"
    elif attribute == "headingaccuracy":
        return "Head Accuracy"
    elif attribute == "isGK":
        return "GK?"
    elif attribute == "isSpecialType":
        return "Special Type?"
    elif attribute in ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY", "DIV", "HAN", "KIC", "REF", "SPD", "POS",
                       "ERASE LIST"]:
        return attribute
    elif attribute in ["id"]:
        return attribute.upper()
    elif attribute in ["atkWorkRate", "defWorkRate"]:
        return attribute[:3].upper() + " " + attribute[3:7] + " " + attribute[-4:]
    elif attribute in ["clubId", "leagueId", "nationId", "baseId"]:
        return attribute[:-2].capitalize() + " " + attribute[-2:].upper()
    elif attribute in ["club", "league", "nation", "headshot", "position", "height", "weight", "age", "acceleration",
                       "aggression", "agility", "agility", "balance", "foot", "crossing", "curve", "dribbling",
                       "finishing", "interceptions", "jumping", "marking", "penalties", "positioning", "potential",
                       "reactions", "stamina", "strength", "vision", "volleys", "traits", "specialities", "attributes",
                       "name", "quality", "color", "rating"]:
        return attribute.capitalize()
    else:
        return "ERROR"


def convert_height(cm_height, return_type='int_tuple'):
    """
    Convert height from cm to ft and inches
    Returns a tuple of the height: (feet, inches)
    """

    total_inches = cm_height/2.54
    feet = int(total_inches/12)
    inches = total_inches % 12

    if return_type == 'int_tuple':
        return feet, inches
    elif return_type == 'string':
        return '%d\' %.1f"' % (feet, inches)


def convert_weight(kg_weight):
    """
    Convert weight from kilograms to pounds
    Returns the weight in pounds
    """

    return kg_weight*2.20462


def format_birthday(birthdate):
    """
    Converts the birthdate to the Month, Day, Year format
    Returns the birthdate as a string
    """

    return '%s/%s/%s' % (birthdate[5:7], birthdate[-2:], birthdate[:4])


def get_file_prefix(file_type):
    if file_type in ['default_player_db', 'current_player_db']:
        file_prefix = 'play_db_'
    elif file_type in ['default_player_list', 'current_player_list']:
        file_prefix = 'play_lt_'
    elif file_type in ['default_formation_db', 'current_formation_db']:
        file_prefix = 'form_db_'
    elif file_type in ['default_formation_list', 'current_formation_list']:
        file_prefix = 'form_lt_'
    elif file_type in ['default_team_list', 'current_team_list']:
        file_prefix = 'team_lt_'
    else:
        file_prefix = ''
        print "File type is invalid."

    return file_prefix
