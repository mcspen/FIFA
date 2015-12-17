from GUI import Button, Label, RadioButton, RadioGroup, TextField, View, Window
from AppConfig import *
import SearchMenu
import EditMenu
from Logic.HelperFunctions import format_attr_name
import json


def open_attribute_window(window_x, window_y, db_dict, attr_dict, attr_list, attr_type, settings):

    # ========== Window ==========
    win_attribute = Window()
    win_attribute.title = attribute_win_title
    win_attribute.auto_position = False
    win_attribute.position = (window_x, window_y)
    win_attribute.size = (win_width, 500)
    win_attribute.resizable = 0
    win_attribute.name = attribute_title + " Window"
    win_attribute.show()

    # ========== Window Image View ==========
    class StartWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = StartWindowImageView(size=win_attribute.size)

    attribute_display_list = []

    # ========== Title ==========
    title = Label(text=attribute_title)
    title.font = title_font
    title.width = title_width
    title.height = title_height
    title.x = (win_width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'

    # ========== Button Declarations ==========
    enter_btn = Button("Enter")
    erase_btn = Button("Erase List")
    back_btn = Button("Back")

    # ========== Radio Button Action ==========
    def selection_made():
        enter_btn.enabled = 1
        win_attribute.become_target()

    def comp_selection_made():
        win_attribute.become_target()

    # ========== Attribute Radio Buttons ==========
    radio_group = RadioGroup(action=selection_made)
    radio_button_list = []

    config_file = '_attributes'
    if attr_type[:4] == 'play':
        config_file = 'player' + config_file
    elif attr_type[:4] == 'form':
        config_file = 'formation' + config_file
    elif attr_type[:4] == 'team':
        config_file = 'team' + config_file
    else:
        print "Invalid attribute type."

    with open('configs.json', 'r') as f:
            attributes_list = json.load(f)[config_file]['all']
            f.close()

    for idx, attribute in enumerate(attributes_list):
        button = RadioButton(attribute)

        if attr_type[:4] == 'play':
            if idx < 10:
                button.width = 45
                button.x = (idx / 10) * (button.width + 5) + 5
            elif idx < 30:
                button.width = 100
                button.x = (idx / 10) * (button.width + 5) - 50
            elif idx < 40:
                button.width = 110
                button.x = (idx / 10) * (button.width + 5) - 80
            else:
                button.width = 100
                button.x = (idx / 10) * (button.width + 5) - 40

            button.y = (idx % 10) * 25 + title.bottom + 5

            # Added for 81st item
            if idx == 80:
                button.x = 7 * (button.width + 5) - 40
                button.y = 10 * 25 + title.bottom + 5

        elif attr_type[:4] == 'form':
            button.width = 150
            button.x = (win_attribute.width - button.width) / 2
            button.y = idx * 25 + title.bottom + 5

        elif attr_type[:4] == 'team':
            button.width = 150
            button.x = (win_attribute.width - button.width) / 2
            button.y = idx * 25 + title.bottom + 5

        else:
            print "Invalid attribute type."

        button.group = radio_group
        button.value = attribute
        button.title = format_attr_name(attribute)

        radio_button_list.append(button)

    # ========== Button Functions ==========
    def enter_btn_func():
        valid = False
        return_value = None

        # Player
        if attr_type == 'player_sort':
            # Check for doubles
            if attr_list.count(radio_group.value) == 0:
                attr_list.append(radio_group.value)

            show_attributes(attribute_display_list)
            erase_btn.enabled = 1

        elif attr_type == 'player_search':
            # Value checks
            if radio_group.value in ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY", "DIV", "HAN", "KIC", "REF", "SPD", "POS",
                                     "acceleration", "aggression", "agility", "balance", "ballcontrol", "crossing",
                                     "curve", "dribbling", "finishing", "freekickaccuracy", "gkdiving", "gkhandling",
                                     "gkkicking", "gkpositioning", "gkreflexes", "headingaccuracy", "interceptions",
                                     "jumping", "longpassing", "longshots", "marking", "penalties", "positioning",
                                     "potential", "rating", "reactions", "shortpassing", "shotpower", "skillMoves",
                                     "slidingtackle", "sprintspeed", "stamina", "standingtackle", "strength", "vision",
                                     "volleys", "weakFoot"]:
                # Value should be an integer between 0 and 100
                if value_tf.value.isdigit():
                    return_value = int(value_tf.value)
                    if 0 < return_value < 100:
                        valid = True

            elif radio_group.value in ["age", "baseId", "clubId", "height", "id", "leagueId", "nationId", "weight"]:
                # Value should be an integer
                if value_tf.value.isdigit():
                    return_value = int(value_tf.value)
                    valid = True

            elif radio_group.value in ["atkWorkRate", "birthdate", "club", "color", "commonName", "defWorkRate",
                                       "firstName", "foot", "itemType", "lastName", "league", "modelName", "name",
                                       "name_custom", "nation", "playStyle", "playerType", "position", "positionFull",
                                       "quality", "specialities", "traits"]:
                # Value should be a string
                if type(value_tf.value) is str:
                    return_value = value_tf.value
                    valid = True

            elif radio_group.value in ["isGK", "isSpecialType"]:
                # Value should be a string
                if value_tf.value.upper() in ['T', 'F', 'TRUE', 'FALSE', 'Y', 'N', 'YES', 'NO']:
                    if value_tf.value.upper()[0] in ['T', 'Y']:
                        return_value = True
                    else:
                        return_value = False
                    valid = True

            if valid:
                attr_dict[radio_group.value] = (return_value, compare_group.value)
                value_tf.value = ''
                show_attributes(attribute_display_list)
                erase_btn.enabled = 1
            else:
                print "Invalid attribute value."

        # Formation
        elif attr_type == 'formation_sort':
            # Check for doubles
            if attr_list.count(radio_group.value) == 0:
                attr_list.append(radio_group.value)

            show_attributes(attribute_display_list)
            erase_btn.enabled = 1

        elif attr_type == 'formation_search':
            # Value checks
            if radio_group.value in ["num_attackers", "num_midfielders", "num_defenders"]:
                # Value should be an integer between 0 and 10
                if value_tf.value.isdigit():
                    return_value = int(value_tf.value)
                    if 0 < return_value < 10:
                        valid = True

            elif radio_group.value in ["num_links"]:
                # Value should be an integer
                if value_tf.value.isdigit():
                    return_value = int(value_tf.value)
                    valid = True

            elif radio_group.value in ["name", "style", "description", "position_all"]:
                # Value should be a string
                if type(value_tf.value) is str:
                    return_value = value_tf.value
                    valid = True

            if valid:
                attr_dict[radio_group.value] = (return_value, compare_group.value)
                value_tf.value = ''
                show_attributes(attribute_display_list)
                erase_btn.enabled = 1
            else:
                print "Invalid attribute value."

        # Team
        elif attr_type == 'team_sort':
            # Check for doubles
            if attr_list.count(radio_group.value) == 0:
                attr_list.append(radio_group.value)

            show_attributes(attribute_display_list)
            erase_btn.enabled = 1

        elif attr_type == 'team_search':
            # Value checks
            if radio_group.value in ["rating", "chemistry", "total_ic"]:
                # Value should be an integer between -1 and 111
                if value_tf.value.isdigit():
                    return_value = int(value_tf.value)
                    if -1 < return_value < 111:
                        valid = True

            elif radio_group.value in ["strength"]:
                # Value should be an integer
                if value_tf.value.isdigit():
                    return_value = int(value_tf.value)
                    valid = True

            elif radio_group.value in ["player", "formation", "manager_league", "manager_nation", "style"]:
                # Value should be a string
                if type(value_tf.value) is str:
                    return_value = value_tf.value
                    valid = True

            if valid:
                attr_dict[radio_group.value] = (return_value, compare_group.value)
                value_tf.value = ''
                show_attributes(attribute_display_list)
                erase_btn.enabled = 1
            else:
                print "Invalid attribute value."

        else:
            print 'Invalid attr_type for AddAttribute.'

        win_attribute.become_target()

    def erase_btn_func():
        if attr_type[-4:] == 'sort':
            del attr_list[:]
        elif attr_type[-6:] == 'search':
            attr_dict.clear()

        show_attributes(attribute_display_list)

        erase_btn.enabled = 0

    def back_btn_func():
        if settings['window'] == 'search':
            SearchMenu.open_search_menu(win_attribute.x, win_attribute.y, db_dict, attr_dict, attr_list, settings)
        elif settings['window'] == 'edit':
            EditMenu.open_edit_menu(win_attribute.x, win_attribute.y, db_dict, attr_dict, attr_list, settings)
        else:
            print "Invalid window setting."

        win_attribute.hide()

    def attr_btn_func(attr_to_remove):
        # Remove from attribute dict
        if attr_type[-6:] == 'search':
            attr_dict.pop(attr_to_remove, None)
            show_attributes(attribute_display_list)

            if len(attr_dict) < 1:
                erase_btn.enabled = 0

        # Remove from attribute list
        elif attr_type[-4:] == 'sort':
            if attr_to_remove in attr_list:
                attr_list.remove(attr_to_remove)
                show_attributes(attribute_display_list)

            if len(attr_list) < 1:
                erase_btn.enabled = 0

    # ========== Buttons ==========
    custom_button_width = 100

    erase_btn.x = (win_width - custom_button_width) / 2
    erase_btn.y = win_attribute.height - 70
    erase_btn.height = button_height
    erase_btn.width = custom_button_width
    erase_btn.font = button_font
    erase_btn.action = erase_btn_func
    erase_btn.style = 'default'
    erase_btn.color = button_color
    erase_btn.just = 'right'
    if (attr_type[-4:] == 'sort' and len(attr_list) == 0) or \
       (attr_type[-6:] == 'search' and len(attr_dict) == 0):
        erase_btn.enabled = 0

    enter_btn.x = erase_btn.left - button_spacing - custom_button_width
    enter_btn.y = erase_btn.top
    enter_btn.height = button_height
    enter_btn.width = custom_button_width
    enter_btn.font = button_font
    enter_btn.action = enter_btn_func
    enter_btn.style = 'default'
    enter_btn.color = button_color
    enter_btn.just = 'right'
    enter_btn.enabled = 0

    back_btn.x = erase_btn.right + button_spacing
    back_btn.y = erase_btn.top
    back_btn.height = button_height
    back_btn.width = custom_button_width
    back_btn.font = button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = button_color
    back_btn.just = 'right'

    # ========== Value Textfield ==========
    value_tf = TextField()
    value_tf.width = 200
    value_tf.x = (win_width - value_tf.width) / 2
    value_tf.y = enter_btn.top - 35
    value_tf.height = 25
    value_tf.font = std_tf_font

    # ========== Compare Radio Buttons ==========
    compare_group = RadioGroup(action=comp_selection_made)
    comp_button_list = []

    comp_button_width = 55
    comp_button_x = (win_attribute.width - 4*comp_button_width)/2

    for value in ['higher', 'exact', 'lower', 'not']:
        button = RadioButton()
        button.width = comp_button_width
        button.x = comp_button_x
        button.y = value_tf.top - value_tf.height - title_border
        button.group = compare_group
        button.value = value
        button.title = value.capitalize()

        comp_button_x += comp_button_width + 5

        comp_button_list.append(button)

    compare_group.value = 'higher'

    def show_attributes(display_list):

        # Remove old attribute buttons from screen
        for message in display_list:
            view.remove(message)

        del display_list[:]

        # Display new search attributes on screen
        message_x = 10
        message_y = win_attribute.height - 150

        if attr_type[-6:] == 'search':
            display_list.append(Label(text="Search Attributes:", font=title_tf_font, width=std_tf_width,
                                      height=std_tf_height, x=message_x, y=message_y, color=title_color))
            message_y += std_tf_height

            index = 0

            for key, search_value in attr_dict.iteritems():
                if index == 6:
                    message_x = back_btn.right + 10
                    message_y = win_attribute.height - 150

                msg_text = format_attr_name(key) + ": "
                if key in ['id', 'baseId', 'nationId', 'leagueId', 'clubId']:
                    msg_text += str(search_value[0])
                elif type(search_value[0]) is int:
                    msg_text += search_value[1].capitalize() + ' ' + str(search_value[0])
                elif search_value[1] == 'not':
                    msg_text += search_value[1].capitalize() + ' "' + str(search_value[0]) + '"'
                else:
                    msg_text += '"' + str(search_value[0]) + '"'

                attr_btn = Button(title=msg_text, font=std_tf_font, width=std_tf_width,
                                  height=std_tf_height, x=message_x, y=message_y, color=title_color,
                                  action=(attr_btn_func, key))
                message_y += std_tf_height + 1
                display_list.append(attr_btn)
                index += 1

        # Display new sort attributes on screen
        elif attr_type[-4:] == 'sort':
            display_list.append(Label(text="Sort Attributes:", font=title_tf_font, width=std_tf_width,
                                      height=std_tf_height, x=message_x, y=message_y, color=title_color))
            message_y += std_tf_height

            for index, sort_value in enumerate(attr_list):
                if index == 6:
                    message_x = back_btn.right + 10
                    message_y = win_attribute.height - 150

                attr_btn = Button(title=(format_attr_name(sort_value)), font=std_tf_font, width=std_tf_width,
                                  height=std_tf_height, x=message_x, y=message_y, color=title_color,
                                  action=(attr_btn_func, sort_value))
                message_y += std_tf_height + 1
                display_list.append(attr_btn)

        for attribute_label in display_list:
            view.add(attribute_label)

    show_attributes(attribute_display_list)

    # ========== Add buttons to window ==========
    view.add(title)
    view.add(enter_btn)
    view.add(erase_btn)
    view.add(back_btn)

    # Shows only for getting attribute for search, not sort
    if attr_type[-6:] == 'search':
        view.add(value_tf)

        for button in comp_button_list:
            view.add(button)

    for button in radio_button_list:
        view.add(button)

    win_attribute.add(view)
    view.become_target()
    win_attribute.show()
