# -*- coding: utf-8 -*-

from PIL import Image
import urllib2
import cStringIO
import os


def ascii_text(input_text):
    # Convert input text into a list to be manipulated
    input_list = list(input_text)

    # Iterate through each character and change to an ASCII reasonable equivalent.
    for idx, char in enumerate(input_list):
        # u'À' - u'\xc0'
        # u'Á' - u'\xc1'
        # u'Â' - u'\xc2'
        # u'Ä' - u'\xc4'
        # u'Å' - u'\xc5'
        if char in [u'\xc0', u'\xc1', u'\xc2', u'\xc4', u'\xc5']:
            input_list[idx] = "A"

        # u'à' - u'\xe0'
        # u'á' - u'\xe1'
        # u'â' - u'\xe2'
        # u'ã' - u'\xe3'
        # u'ä' - u'\xe4'
        # u'å' - u'\xe5'
        # u'ă' - u'\u0103'
        # u'ą' - u'\u0105'
        elif char in [u'\xe0', u'\xe1', u'\xe2', u'\xe3', u'\xe4', u'\xe5', u'\u0103', u'\u0105']:
            input_list[idx] = "a"

        # u'æ' - u'\xe6'
        elif char in [u'\xe6']:
            input_list[idx] = "ae"

        # u'ß' - u'\xdf'
        elif char in [u'\xdf']:
            input_list[idx] = "B"

        # u'Ć' - u'\u0106'
        # u'Č' - u'\u010c'
        # u'Ç' - u'\xc7'
        elif char in [u'\u0106', u'\u010c', u'\xc7']:
            input_list[idx] = "C"

        # u'ć' - u'\u0107'
        # u'č' - u'\u010d'
        # u'ç' - u'\xe7'
        elif char in [u'\u0107', u'\u010d', u'\xe7']:
            input_list[idx] = "c"

        # u'Đ' - u'\u0110'
        # u'Ď' - u'\u010e'
        elif char in [u'\u0110', u'\u010e']:
            input_list[idx] = "D"

        # u'đ' - u'\u0111'
        elif char in [u'\u0111']:
            input_list[idx] = "d"

        # u'É' - u'\xc9'
        elif char in [u'\xc9']:
            input_list[idx] = "E"

        # u'ę' - u'\u0119'
        # u'ě' - u'\u011b'
        # u'è' - u'\xe8'
        # u'é' - u'\xe9'
        # u'ê' - u'\xea'
        # u'ë' - u'\xeb'
        elif char in [u'\u0119', u'\u011b', u'\xe8', u'\xe9', u'\xea', u'\xeb']:
            input_list[idx] = "e"

        # u'ğ' - u'\u011f'
        elif char in [u'\u011f']:
            input_list[idx] = "g"

        # u'İ' - u'\u0130'
        # u'Í' - u'\xcd'
        elif char in [u'\u0130', u'\xcd']:
            input_list[idx] = "I"

        # u'ı' - u'\u0131'
        # u'í' - u'\xed'
        # u'î' - u'\xee'
        # u'ï' - u'\xef'
        elif char in [u'\u0131', u'\xed', u'\xee', u'\xef']:
            input_list[idx] = "i"

        # u'Ľ' - u'\u013d'
        # u'Ł' - u'\u0141'
        elif char in [u'\u013d', u'\u0141']:
            input_list[idx] = "L"

        # u'ł' - u'\u0142'
        elif char in [u'\u0142']:
            input_list[idx] = "l"

        # u'Ñ' - u'\xd1'
        elif char in [u'\xd1']:
            input_list[idx] = "N"

        # u'ñ' - u'\xf1'
        # u'ń' - u'\u0144'
        # u'ņ' - u'\u0146'
        # u'ň' - u'\u0148'
        elif char in [u'\xf1', u'\u0144', u'\u0146', u'\u0148']:
            input_list[idx] = "n"

        # u'Ó' - u'\xd3'
        # u'Ö' - u'\xd6'
        # u'Ø' - u'\xd8'
        # u'Ō' - u'\u014c'
        elif char in [u'\xd3', u'\xd6', u'\xd8', u'\u014c']:
            input_list[idx] = "O"

        # u'ð' - u'\xf0'
        # u'ò' - u'\xf2'
        # u'ó' - u'\xf3'
        # u'ô' - u'\xf4'
        # u'õ' - u'\xf5'
        # u'ö' - u'\xf6'
        # u'ø' - u'\xf8'
        # u'ō' - u'\u014d'
        elif char in [u'\xf0', u'\xf2', u'\xf3', u'\xf4', u'\xf5', u'\xf6', u'\xf8', u'\u014d']:
            input_list[idx] = "o"

        # u'Þ' - u'\xde'
        elif char in [u'\xde']:
            input_list[idx] = "P"

        # u'þ' - u'\xfe'
        elif char in [u'\xfe']:
            input_list[idx] = "p"

        # u'ř' - u'\u0159'
        elif char in [u'\u0159']:
            input_list[idx] = "r"

        # u'Ś' - u'\u015a'
        # u'Ş' - u'\u015e'
        # u'Š' - u'\u0160'
        elif char in [u'\u015a', u'\u015e', u'\u0160']:
            input_list[idx] = "S"

        # u'ś' - u'\u015b'
        # u'ş' - u'\u015f'
        # u'š' - u'\u0161'
        elif char in [u'\u015b', u'\u015f', u'\u0161']:
            input_list[idx] = "s"

        # u'ţ' - u'\u0163'
        elif char in [u'\u0163']:
            input_list[idx] = "t"

        # u'Ü' - u'\xdc'
        elif char in [u'\xdc']:
            input_list[idx] = "U"

        # u'ú' - u'\xfa'
        # u'ü' - u'\xfc'
        # u'ū' - u'\u016b'
        # u'ů' - u'\u016f'
        elif char in [u'\xfa', u'\xfc', u'\u016b', u'\u016f']:
            input_list[idx] = "u"

        # u'ý' - u'\xfd'
        elif char in [u'\xfd']:
            input_list[idx] = "y"

        # u'Ż' - u'\u017b'
        # u'Ž' - u'\u017d'
        elif char in [u'\u017b', u'\u017d']:
            input_list[idx] = "Z"

        # u'ź' - u'\u017a'
        # u'ż' - u'\u017c'
        # u'ž' - u'\u017e'
        elif char in [u'\u017a', u'\u017c', u'\u017e']:
            input_list[idx] = "z"

    # Convert list back into a string to return
    return "".join(input_list)

    # Old solution that converts strings to ASCII, but some characters are skipped.
    # import unicodedata
    # return unicodedata.normalize('NFKD', input_text).encode('ascii', 'ignore')


def text_add_new_lines(text, max_length):
    """
    Adds new line characters to text
    Input: The text to add new lines to and the max length of the line
    Output: The text with new line characters added and the number of lines
    """

    num_lines = 1
    longest_line = 0

    # See if there are any spaces or if the text is too long
    if (' ' in text) and len(text) > max_length:

        # Split text by whitespace
        text_list = text.split()
        count = len(text_list[0])

        # Merge parts of text if less than max length, or add new line character
        while len(text_list) > 1:
            if count + len(text_list[1]) + 1 > max_length:
                text_list[0] = text_list[0] + '\n' + text_list[1]
                if count > longest_line:
                    longest_line = count
                count = len(text_list[1])
                num_lines += 1

                # Check if that was the last word and check for length
                if len(text_list) == 2:
                    if len(text_list[1]) > longest_line:
                        longest_line = text_list[1]
                del text_list[1]

            else:
                text_list[0] = text_list[0] + ' ' + text_list[1]
                count += len(text_list[1])
                del text_list[1]

        return_text = text_list[0]

    else:
        return_text = text
        longest_line = len(text)

    # Return the text, the number of lines, and the number of characters of the longest line
    return return_text, num_lines, longest_line


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
        if attribute in ['total_skillMoves']:
            labels.append(attribute[6:9].capitalize()+'.')
        if attribute in ['total_PAC', 'total_SHO', 'total_PAS', 'total_DRI', 'total_DEF', 'total_PHY']:
            labels.append(attribute[6:])
        else:
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
        if attribute in ['player']:
            team_info.append("Player")
        elif attribute in ['total_skillMoves']:
            total = 0
            for position in team['formation']['positions'].itervalues():
                player = position['player']
                total += player[attribute[6:]]
            team_info.append(str(total))
        elif attribute in ['total_PAC', 'total_SHO', 'total_PAS', 'total_DRI', 'total_DEF', 'total_PHY']:
            total = 0
            for position in team['formation']['positions'].itervalues():
                player = position['player']
                if not player['isGK']:
                    index = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY'].index(attribute[6:])
                    total += player['attributes'][index]['value']
            team_info.append(str(total))
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
                       "name", "price", "quality", "color", "rating", "formation", "style", "description", "chemistry",
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
    elif attribute in ["total_skillMoves"]:
        return "Total Skill Moves"
    elif attribute in ['total_PAC', 'total_SHO', 'total_PAS', 'total_DRI', 'total_DEF', 'total_PHY']:
        return "Total " + attribute[6:]
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
            image_info.save(image_file_name, quality=90)
            image_file.close()

    # In case of no internet connection
    except Exception as err:
        image_file_name = 'Images/no_internet.png'
        print "Error: " + str(err.args)
        print "File: " + image_file_name
        print "URL: " + image_url

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
            image_info.save(image_file_name, quality=90)
            image_file.close()

    # In case of no internet connection
    except Exception as err:
        if 'players' in image_url:
            source_image_file_name = 'Images/no_internet.png'
            image_file_name = 'Images/temp/no_internet_small_%s.png' % str(ratio)

            if not os.path.isfile(image_file_name):
                image_info = Image.open(source_image_file_name)
                image_info = image_info.resize((int(image_info.size[0]*ratio),
                                                int(image_info.size[1]*ratio)),
                                               Image.ANTIALIAS)
                image_info.save(image_file_name, quality=90)
        print "Error: " + str(err.args)
        print "File: " + image_file_name
        print "URL: " + image_url

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
        if file_name[-4:] in [".png"]:
            delete_image("Images/temp/" + file_name)
