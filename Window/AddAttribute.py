from GUI import Button, Label, RadioButton, RadioGroup, TextField, View, Window
from AppConfig import *
import SearchMenu
import json


def open_attribute_window(window_x, window_y, db_dict, attr_dict, attr_list, attr_type, settings):

    # ========== Window ==========
    win_attribute = Window()
    win_attribute.title = attribute_win_title
    win_attribute.auto_position = False
    win_attribute.position = (window_x, window_y)
    win_attribute.size = (win_width, 450)
    win_attribute.resizable = 0
    win_attribute.name = attribute_title + " Window"
    win_attribute.show()

    # ========== Window Image View ==========
    class StartWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = StartWindowImageView(size=win_attribute.size)

    # ========== Title ==========
    title = Label(text=attribute_title)
    title.font = title_font
    title.width = attribute_title_width
    title.height = title_height
    title.x = (win_width - attribute_title_width) / 2
    title.y = top_border
    title.color = title_color

    # ========== Button Declarations ==========
    enter_btn = Button("Enter")
    back_btn = Button("Back")

    # ========== Radio Button Action ==========
    def get_attribute():
        enter_btn.enabled = 1
        win_attribute.become_target()

    # ========== Radio Buttons ==========
    radio_group = RadioGroup(action=get_attribute)
    radio_button_list = []

    with open('configs.json', 'r') as f:
            attributes_list = json.load(f)['player_attributes']
            f.close()

    erase_option = 'ERASE LIST'
    attributes_list.append(erase_option)

    for idx, attribute in enumerate(attributes_list):
        button = RadioButton(attribute)

        if idx < 10:
            button.width = 55
            button.x = (idx / 10) * (button.width + 5) + 5
        else:
            button.width = 100
            button.x = (idx / 10) * (button.width + 5) - 40

        button.y = (idx % 10) * 25 + title.bottom + 5
        button.group = radio_group
        button.value = attribute

        radio_button_list.append(button)

    # ========== Button Functions ==========
    def enter_btn_func():
        valid = False
        return_value = None

        if attr_type == 'sort':
            # Erase option
            if radio_group.value == erase_option:
                del attr_list[:]
            else:
                # Check for doubles
                if attr_list.count(radio_group.value) == 0:
                    attr_list.append(radio_group.value)

            SearchMenu.open_search_menu(win_attribute.x, win_attribute.y,
                                        db_dict, attr_dict, attr_list, settings)
            win_attribute.hide()

        elif attr_type == 'search':
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
                                       "quality"]:
                # Value should be a string
                if type(value_tf.value) is str:
                    return_value = value_tf.value
                    valid = True

            elif radio_group.value in ["isGK", "isSpecialType"]:
                # Value should be a string
                if value_tf.value.upper() in ['T', 'F', 'TRUE', 'FALSE']:
                    if value_tf.value.upper()[0] == 'T':
                        return_value = True
                    else:
                        return_value = False
                    valid = True

            if radio_group.value == erase_option:
                attr_dict.clear()
                SearchMenu.open_search_menu(win_attribute.x, win_attribute.y, db_dict,
                                            attr_dict, attr_list, settings)
                win_attribute.hide()

            elif valid:
                attr_dict[radio_group.value] = return_value
                SearchMenu.open_search_menu(win_attribute.x, win_attribute.y, db_dict,
                                            attr_dict, attr_list, settings)
                win_attribute.hide()
            else:
                print "Invalid attribute value."

        else:
            print 'Invalid attr_type for AddAttribute.'
            SearchMenu.open_search_menu(win_attribute.x, win_attribute.y,
                                        db_dict, attr_dict, attr_list, settings)
            win_attribute.hide()

    def back_btn_func():
        SearchMenu.open_search_menu(win_attribute.x, win_attribute.y,
                                    db_dict, attr_dict, attr_list, settings)
        win_attribute.hide()

    # ========== Buttons ==========
    enter_btn.x = (win_width - 2*button_width - button_spacing) / 2
    enter_btn.y = win_attribute.height - 70
    enter_btn.height = button_height
    enter_btn.width = button_width
    enter_btn.font = button_font
    enter_btn.action = enter_btn_func
    enter_btn.style = 'default'
    enter_btn.color = button_color
    enter_btn.just = 'right'
    enter_btn.enabled = 0

    back_btn.x = enter_btn.right + button_spacing
    back_btn.y = enter_btn.top
    back_btn.height = button_height
    back_btn.width = button_width
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

    # ========== Add buttons to window ==========
    view.add(title)
    view.add(enter_btn)
    view.add(back_btn)

    # Shows only for getting attribute for search, not sort
    if attr_type == 'search':
        view.add(value_tf)

    for button in radio_button_list:
        view.add(button)

    win_attribute.add(view)
    view.become_target()
    win_attribute.show()
