"""
Helper functions that don't belong to any class
"""

__author__ = 'mspencer'

import unicodedata
from PIL import Image
import urllib2
import cStringIO
import os


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


def formation_info_labels():
    """
    Gets the labels of the formations info to be displayed
    Input: None
    Output: A list of the labels of the formations info
    """

    # Formation's base info
    labels = ['Name', 'Style', 'Links', 'Dfnds', 'Mids', 'Atkrs', 'Positions', 'Description']

    return labels


def team_info_labels(attributes):
    """
    Gets the labels of the players info to be displayed
    Input: The list of attributes
    Output: A list of the labels of the players info
    """

    # Player's base info
    labels = ['Rating', 'Str.', 'Chem.', 'Formation', 'Style', 'Mgr League', 'Mgr Nation']

    # Remove attributes already displayed
    for attr in ['rating', 'strength', 'chemistry', 'formation', 'style', 'manager_league', 'manager_nation']:
        while attributes.count(attr) > 0:
            attributes.remove(attr)

    # Add attributes from list
    for attribute in attributes:
        labels.append(attribute[:3].capitalize()+'.')

    return labels


def player_info(player, attributes):
    """
    Gets the name and attributes of the given player and specified attributes
    Input: The player and list of attributes
    Output: A list of the player's info
    """

    player_info = []

    # Get player's common name
    common_name = ascii_text(player['commonName'])

    # Get player's name
    player_name = ascii_text(player['firstName']) + ' ' + ascii_text(player['lastName'])

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
    nation = ascii_text(player['nation']['name'])
    player_info.append(nation[:20])

    # Player's league
    league = ascii_text(player['league']['name'])
    player_info.append(league[:20])

    # Get player's club
    club = ascii_text(player['club']['name'])
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
        elif attribute in ['specialities', 'traits']:
            if player[attribute] is not None:
                player_info.append(', '.join(player[attribute])[:-1])
            else:
                player_info.append('')
        else:
            player_info.append(str(player[attribute]))

    return player_info


def formation_info(formation):
    """
    Gets the basic attributes of the given formation and specified attributes
    Input: The formation
    Output: A list of the formation's info
    """

    formation_info = []

    # Formation's name
    formation_info.append(formation['name'])

    # Formation's style
    formation_info.append(formation['style'])

    # Formation's number of links
    formation_info.append(str(formation['num_links']))

    # Formation's number of defenders
    formation_info.append(str(formation['num_defenders']))

    # Formation's number of midfielders
    formation_info.append(str(formation['num_midfielders']))

    # Formation's number of attackers
    formation_info.append(str(formation['num_attackers']))

    # Formation's positions
    position_list = list(formation['positions'].keys())
    position_string = ', '.join(position_list[:4]) + '...'
    formation_info.append(position_string)

    # Formation's description
    formation_info.append(formation['description'][:35] + '...')

    return formation_info


def team_info(team, attributes):
    """
    Gets the basic attributes of the given team and specified attributes
    Input: The team and list of attributes
    Output: A list of the team's info
    """

    team_info = []

    # Team's rating
    team_info.append(str(team['rating'])[:7])

    # Team's strength
    team_info.append(str(team['strength']))

    # Team's chemistry
    team_info.append(str(team['chemistry']))

    # Team's formation
    team_info.append(team['formation']['name'])

    # Team's formation style
    team_info.append(team['formation']['style'])

    # Team's manager's league
    team_info.append(ascii_text(team['manager']['league'])[:20])

    # Team's manager's nation
    team_info.append(ascii_text(team['manager']['nation'])[:20])

    # Remove attributes already displayed
    for attr in ['rating', 'strength', 'chemistry', 'formation', 'style', 'manager_league', 'manager_nation']:
        while attributes.count(attr) > 0:
            attributes.remove(attr)

    # Add attributes from list
    for attribute in attributes:
        if attribute in []:
            team_info.append(str(team[attribute]))
        else:
            team_info.append(str(team[attribute]))

    return team_info


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
                       "name", "quality", "color", "rating", "formation", "style", "description", "chemistry",
                       "player"]:
        return attribute.capitalize()
    elif attribute in ["num_links", "num_defenders", "num_attackers", "num_midfielders"]:
        return "Number of " + attribute[4:].capitalize()
    elif attribute in ["position_all"]:
        return attribute[:-4].capitalize()
    elif attribute in ["manager_league", "manager_nation"]:
        return attribute[:7].capitalize() + " " + attribute[8:].capitalize()
    elif attribute in ["total_ic"]:
        return "Total Individual Chemistry"
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
    """
    Returns the JSON file prefix for the specified file type.
    """
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


def save_image(image_url, image_file_name):
    """
    Saves the image from the specified url and returns the file name.
    """

    try:
        image_file_name = 'Images/temp/' + image_file_name + '.png'

        if not os.path.isfile(image_file_name):
            image_file = cStringIO.StringIO(urllib2.urlopen(image_url).read())
            image_info = Image.open(image_file)
            image_info.save(image_file_name)
            image_file.close()

    # In case of no internet connection
    except Exception:
        image_file_name = 'Images/no_internet.png'

    return image_file_name


def save_small_image(image_url, image_file_name, ratio=0.75):
    """
    Saves a smaller image from the specified url and returns the file name.
    """

    try:
        image_file_name = 'Images/temp/' + image_file_name + '.png'

        if not os.path.isfile(image_file_name):
            image_file = cStringIO.StringIO(urllib2.urlopen(image_url).read())
            image_info = Image.open(image_file)
            image_info = image_info.resize((int(image_info.size[0]*ratio),
                                            int(image_info.size[1]*ratio)),
                                           Image.ANTIALIAS)
            image_info.save(image_file_name)
            image_file.close()

    # In case of no internet connection
    except Exception:
        image_file_name = 'Images/no_internet_small.png'

    return image_file_name


def delete_image(image_file_name):
    """
    Deletes the image with the specified file name.
    Returns true if it was deleted and false if it was unsuccessful.
    """

    try:
        os.remove(image_file_name)
        return True

    except Exception as err:
        print "Error: " + err.args[1]
        return False


def delete_all_temp_images():
    """
    Deletes all of the files in the temp image folder
    """

    file_names = os.listdir("Images/temp/")
    for file_name in file_names:
        delete_image("Images/temp/" + file_name)
