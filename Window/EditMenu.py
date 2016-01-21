from GUI import Button, Label, RadioButton, RadioGroup, TextField, View, Window
import json
import math
from AppConfig import *
import PickFile
import PickPosition
import AddAttribute
import PlayerBio
import FormationBio
import TeamBio
from Logic import PlayerDB
from Logic import FormationDB
from Logic import TeamDB
from Logic.HelperFunctions import format_attr_name, player_info_labels, player_info
from Logic.HelperFunctions import formation_info_labels, formation_info


def open_edit_menu(window_x, window_y, db_dict, attr_dict=None, attr_list=None, settings=None):

    list_players = PlayerDB.PlayerDB()
    list_formations = FormationDB.FormationDB()
    list_teams = TeamDB.TeamDB()

    if settings['edit_subject'] == 'players':
        list_players.load(settings['file_name'], 'list')
    elif settings['edit_subject'] == 'formations':
        list_formations.load(settings['file_name'], 'list')
    elif settings['edit_subject'] == 'teams':
        list_teams.load(settings['file_name'])

    if attr_dict is None:
        attr_dict = {}

    if attr_list is None:
        attr_list = []

    if settings is None:
        settings = {
            'window': 'edit',
            'edit_type': 'add',
            'edit_mode': 'simple',
            'edit_subject': 'players',
            'sort_order': True,
            'messages': {
                'search': [],
                'sort': [],
                'results': []
            }
        }
    else:
        if 'window' not in settings:
            settings['window'] = 'edit'
        if 'edit_type' not in settings:
            settings['edit_type'] = 'add'
        if 'edit_mode' not in settings:
            settings['edit_mode'] = 'simple'
        if 'edit_subject' not in settings:
            settings['edit_subject'] = 'players'
        if 'sort_order' not in settings:
            settings['sort_order'] = True
        if 'messages' not in settings:
            settings['messages'] = {'search': [], 'sort': [], 'results': []}

    num_results = 20
    general_display = []
    simple_display = []
    advanced_display = []

    # ========== Window ==========
    win_edit = Window()
    win_edit.title = edit_win_title
    win_edit.auto_position = False
    win_edit.position = (window_x, window_y)
    win_edit.size = (win_width, win_height)
    win_edit.resizable = 0
    win_edit.name = edit_title + " Window"

    # ========== Window Image View ==========
    class FormationsWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = FormationsWindowImageView(size=win_edit.size)

    # ========== Title ==========
    title = Label(text=edit_title + ' File: ' + settings['file_name'])
    title.font = title_font
    title.width = title_width
    title.height = title_height
    title.x = (win_width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'
    general_display.append(title)

    # ========== Action Button Declarations ==========
    start_btn = Button("Start")
    back_btn = Button("Back")

    # ========== Mode Button Declarations ==========
    simple_btn = Button("Simple")
    advanced_btn = Button("Advanced")

    # ========== Tool Button Declarations ==========
    attribute_btn = Button("Add Search Attribute")
    sort_btn = Button("Add Sort Attribute")
    reset_btn = Button("Reset Results")

    # ========== Simple Field Declarations ==========
    rating_label = Label("Rating: ")
    rating_tf = TextField()
    name_label = Label("Name: ")
    name_tf = TextField()

    # ========== Action Button Functions ==========
    def start_btn_func():
        # Search for players based on attributes
        if settings['edit_subject'] == 'players':

            # Get the attributes to search with based on what mode is in use
            if simple_btn.enabled == 0:
                if len(name_tf.value) > 0:
                    search_dict = {'name_custom': (name_tf.value, 'exact')}
                else:
                    search_dict = {}
                if rating_tf.value.isdigit():
                    search_dict['rating'] = (int(rating_tf.value), 'exact')
            else:
                search_dict = attr_dict

            # Get players from database to add and search
            if settings['edit_type'] == 'add':

                db_players = db_dict['player_db'][1]

                if len(search_dict) == 0:
                    search_results = db_players
                else:
                    search_results = db_players.search(search_dict)
                    search_results = PlayerDB.PlayerDB(search_results)

            # Get players from list to edit or delete and search
            else:
                if len(search_dict) == 0:
                    search_results = list_players
                else:
                    search_results = list_players.search(search_dict)
                    search_results = PlayerDB.PlayerDB(search_results)

            # Sort players - if no attribute selected, use rating
            if len(attr_list) == 0:
                search_results.sort(['rating'], sort_order_radio_group.value)
            else:
                search_results.sort(attr_list, sort_order_radio_group.value)

            # Get attributes list and avoid duplicates
            attributes_list = []

            for attr in attr_list:
                if attributes_list.count(attr) == 0:
                    attributes_list.append(attr)

            for attr_key in attr_dict.iterkeys():
                if attributes_list.count(attr_key) == 0:
                    attributes_list.append(attr_key)

            display_players(search_results, attributes_list, (0, num_results))

        # Start button corresponds to formations
        elif settings['edit_subject'] == 'formations':

            # Get the attributes to search with based on what mode is in use
            if simple_btn.enabled == 0:
                if len(name_tf.value) > 0:
                    search_dict = {'name': (name_tf.value, 'exact')}
                else:
                    search_dict = {}
            else:
                search_dict = attr_dict

            # Get formations from database to add and search
            if settings['edit_type'] == 'add':

                db_formations = db_dict['formation_db'][1]

                if len(search_dict) == 0:
                    search_results = db_formations
                else:
                    search_results = db_formations.search(search_dict)
                    search_results = FormationDB.FormationDB(search_results)

            # Get formations from list to edit or delete and search
            else:
                if len(search_dict) == 0:
                    search_results = list_formations
                else:
                    search_results = list_formations.search(search_dict)
                    search_results = FormationDB.FormationDB(search_results)

            # Sort formations - if no attribute selected, use name
            if len(attr_list) == 0:
                search_results.sort(['name'], sort_order_radio_group.value)
            else:
                search_results.sort(attr_list, sort_order_radio_group.value)

            # Get attributes list and avoid duplicates
            attributes_list = []

            for attr in attr_list:
                if attributes_list.count(attr) == 0:
                    attributes_list.append(attr)

            for attr_key in attr_dict.iterkeys():
                if attributes_list.count(attr_key) == 0:
                    attributes_list.append(attr_key)

            display_formations(search_results, attributes_list, (0, num_results))

        # Start button corresponds to teams
        elif settings['edit_subject'] == 'teams':
            stuff = 0

        win_edit.become_target()

    def back_btn_func():
        # Clean up
        reset_btn_func()

        win_edit.hide()
        PickFile.open_pick_file_window(win_edit.x, win_edit.y, db_dict, settings)

    # ========== Search Type Button Functions ==========
    def simple_btn_func():
        simple_btn.enabled = 0
        advanced_btn.enabled = 1
        settings['edit_mode'] = 'simple'

        for display_item in advanced_display:
            view.remove(display_item)

        clean_results()

        for display_item in simple_display:
            view.add(display_item)

        name_tf.become_target()

    def advanced_btn_func():
        advanced_btn.enabled = 0
        simple_btn.enabled = 1
        settings['edit_mode'] = 'advanced'

        for display_item in simple_display:
            view.remove(display_item)

        clean_results()
        display_attributes()

        for display_item in advanced_display:
            view.add(display_item)

        win_edit.become_target()

    # ========== Tool Button Functions ==========
    def attribute_btn_func():
        # Delete results
        del settings['messages']['results'][:]

        attr_type = ''
        if settings['edit_subject'] == 'players':
            attr_type = 'player_search'
        elif settings['edit_subject'] == 'formations':
            attr_type = 'formation_search'
        elif settings['team_subject'] == 'teams':
            attr_type = 'player_search'
        else:
            print "Invalid edit_subject settings."

        # Open new window and close current window
        win_edit.hide()
        AddAttribute.open_attribute_window(win_edit.x, win_edit.y,
                                           db_dict, attr_dict, attr_list, attr_type, settings)

    def sort_btn_func():
        # Delete results
        del settings['messages']['results'][:]

        attr_type = ''
        if settings['edit_subject'] == 'players':
            attr_type = 'player_sort'
        elif settings['edit_subject'] == 'formations':
            attr_type = 'formation_sort'
        elif settings['team_subject'] == 'teams':
            attr_type = 'player_sort'
        else:
            print "Invalid edit_subject settings."

        # Open new window and close current window
        win_edit.hide()
        AddAttribute.open_attribute_window(win_edit.x, win_edit.y, db_dict,
                                           attr_dict, attr_list, attr_type, settings)

    def display_attributes():
        for search_item in settings['messages']['search']:
            view.add(search_item)
        for sort_item in settings['messages']['sort']:
            view.add(sort_item)

    def clean_results():
        # Remove messages off page
        for message in settings['messages']['search']:
            view.remove(message)
        for message in settings['messages']['sort']:
            view.remove(message)
        for message in settings['messages']['results']:
            view.remove(message)

        del settings['messages']['results'][:]

        win_edit.become_target()

    def reset_btn_func():
        # Remove messages off page
        for message in settings['messages']['search']:
            view.remove(message)
        for message in settings['messages']['sort']:
            view.remove(message)
        for message in settings['messages']['results']:
            view.remove(message)

        # Delete the attribute parameters for search and sort
        attr_dict.clear()
        del attr_list[:]
        del settings['messages']['results'][:]

        win_edit.become_target()

    def player_bio_btn_func(player):
        win_edit.become_target()
        PlayerBio.open_player_bio_window(win_edit.x, win_edit.y, player, win_edit, settings['file_name'], list_players)
        win_edit.hide()

    def formation_bio_btn_func(formation):
        win_edit.become_target()
        FormationBio.open_formation_bio_window(
                win_edit.x, win_edit.y, formation, win_edit, settings['file_name'], list_formations)
        win_edit.hide()

    def add_btn_func(list_item, btn):
        if settings['edit_subject'] == 'players':
            # Check if player is already on selected players list
            # Remove player from list
            player_data = list_players.search({'id': (list_item['id'], 'exact')})
            if len(player_data) > 0:
                # Remove
                list_players.db.remove(player_data[0])
                # Save
                list_players.sort(['rating'])
                list_players.save(settings['file_name'], 'list', True)

                # Switch button title
                btn.title = "+"

            # Add player to the list
            else:
                # Add
                list_players.db.append(list_item)
                # Save
                list_players.sort(['rating'])
                list_players.save(settings['file_name'], 'list', True)

                # Switch button title
                btn.title = "-"

        elif settings['edit_subject'] == 'formations':
            # Check if formation is already on selected formations list
            # Remove formation from list
            if list_item in list_formations.db:
                # Remove
                list_formations.db.remove(list_item)
                # Save
                list_formations.sort(['name'])
                list_formations.save(settings['file_name'], 'list', True)

                # Switch button title
                btn.title = "+"

            # Add formation to the list
            else:
                # Add
                list_formations.db.append(list_item)
                # Save
                list_formations.sort(['name'])
                list_formations.save(settings['file_name'], 'list', True)

                # Switch button title
                btn.title = "-"

        win_edit.become_target()

    def pos_btn_func(player, btn):
        # Open window to get position
        win_edit.hide()
        PickPosition.open_pick_position_window(win_edit.x, win_edit.y, player, list_players, settings, btn, win_edit)
        win_edit.become_target()

    # ========== Action Buttons ==========
    start_btn.x = (win_width - 2*small_button_width - small_button_spacing) / 2
    start_btn.y = title.bottom + small_button_top_spacing
    start_btn.height = small_button_height
    start_btn.width = small_button_width
    start_btn.font = small_button_font
    start_btn.action = start_btn_func
    start_btn.style = 'default'
    start_btn.color = small_button_color
    start_btn.just = 'right'
    general_display.append(start_btn)

    back_btn.x = start_btn.right + small_button_spacing
    back_btn.y = start_btn.top
    back_btn.height = small_button_height
    back_btn.width = small_button_width
    back_btn.font = small_button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = small_button_color
    back_btn.just = 'right'
    general_display.append(back_btn)

    # ========== Edit Type Radio Buttons ==========
    def get_edit_type_rg():
        settings['edit_type'] = edit_type_radio_group.value
        win_edit.become_target()

    edit_type_radio_group = RadioGroup(action=get_edit_type_rg)

    radio_btn_width = 125
    radio_btn_space = 5

    # Edit Type
    type_add_radio_btn = RadioButton()
    if settings['edit_subject'] == 'players':
        type_add_radio_btn.title = 'Add Players'
    elif settings['edit_subject'] == 'formations':
        type_add_radio_btn.title = 'Add Formations'
    elif settings['edit_subject'] == 'teams':
        type_add_radio_btn.title = 'Add Teams'
    type_add_radio_btn.width = radio_btn_width
    type_add_radio_btn.x = (win_edit.width - 2*radio_btn_width - radio_btn_space) / 2
    type_add_radio_btn.y = start_btn.bottom + small_button_top_spacing
    type_add_radio_btn.group = edit_type_radio_group
    type_add_radio_btn.value = 'add'
    general_display.append(type_add_radio_btn)

    type_edit_radio_btn = RadioButton()
    if settings['edit_subject'] == 'players':
        type_edit_radio_btn.title = 'Edit/Delete Players'
    elif settings['edit_subject'] == 'formations':
        type_edit_radio_btn.title = 'Edit/Delete Forms'
    elif settings['edit_subject'] == 'teams':
        type_edit_radio_btn.title = 'Edit/Delete Teams'
    type_edit_radio_btn.width = radio_btn_width
    type_edit_radio_btn.x = type_add_radio_btn.right + radio_btn_space
    type_edit_radio_btn.y = type_add_radio_btn.top
    type_edit_radio_btn.group = edit_type_radio_group
    type_edit_radio_btn.value = 'edit'
    general_display.append(type_edit_radio_btn)

    edit_type_radio_group.value = settings['edit_type']

    # ========== Mode Buttons ==========
    simple_btn.x = (win_width - 2*small_button_width - small_button_spacing) / 2
    simple_btn.y = type_add_radio_btn.bottom + small_button_top_spacing
    simple_btn.height = small_button_height
    simple_btn.width = small_button_width
    simple_btn.font = small_button_font
    simple_btn.action = simple_btn_func
    simple_btn.style = 'default'
    simple_btn.color = small_button_color
    simple_btn.just = 'right'
    if settings['edit_mode'] == 'simple':
        simple_btn.enabled = 0
    general_display.append(simple_btn)

    advanced_btn.x = simple_btn.right + small_button_spacing
    advanced_btn.y = simple_btn.top
    advanced_btn.height = small_button_height
    advanced_btn.width = small_button_width
    advanced_btn.font = small_button_font
    advanced_btn.action = advanced_btn_func
    advanced_btn.style = 'default'
    advanced_btn.color = small_button_color
    advanced_btn.just = 'right'
    if settings['edit_mode'] == 'advanced':
        advanced_btn.enabled = 0
    general_display.append(advanced_btn)

    # ========== Sort Order Radio Buttons ==========
    def get_attribute_sort_order_rg():
        settings['sort_order'] = sort_order_radio_group.value
        win_edit.become_target()

    sort_order_radio_group = RadioGroup(action=get_attribute_sort_order_rg)

    asc_desc_radio_btn_width = 75
    asc_msg_width = 80
    radio_btn_space = 5

    asc_desc_rg_msg = Label(text="Sort Order:", font=std_tf_font, width=asc_msg_width, height=std_tf_height,
                            color=title_color)
    asc_desc_rg_msg.x = (win_edit.width - 2*asc_desc_radio_btn_width - radio_btn_space - asc_msg_width) / 2
    asc_desc_rg_msg.y = simple_btn.bottom + radio_btn_space
    general_display.append(asc_desc_rg_msg)

    descend_radio_btn = RadioButton("Descending")
    descend_radio_btn.width = asc_desc_radio_btn_width
    descend_radio_btn.x = asc_desc_rg_msg.right
    descend_radio_btn.y = asc_desc_rg_msg.top
    descend_radio_btn.group = sort_order_radio_group
    descend_radio_btn.value = True
    general_display.append(descend_radio_btn)

    ascend_radio_btn = RadioButton("Ascending")
    ascend_radio_btn.width = asc_desc_radio_btn_width
    ascend_radio_btn.x = descend_radio_btn.right + radio_btn_space
    ascend_radio_btn.y = descend_radio_btn.top
    ascend_radio_btn.group = sort_order_radio_group
    ascend_radio_btn.value = False
    general_display.append(ascend_radio_btn)

    sort_order_radio_group.value = settings['sort_order']

    # ========== Tool Buttons ==========
    attribute_btn.x = (win_width - 3*small_button_width - 2*small_button_spacing) / 2
    attribute_btn.y = asc_desc_rg_msg.bottom + 5
    attribute_btn.height = small_button_height
    attribute_btn.width = small_button_width
    attribute_btn.font = small_button_font
    attribute_btn.action = attribute_btn_func
    attribute_btn.style = 'default'
    attribute_btn.color = small_button_color
    attribute_btn.just = 'right'
    advanced_display.append(attribute_btn)

    sort_btn.x = attribute_btn.right + small_button_spacing
    sort_btn.y = attribute_btn.top
    sort_btn.height = small_button_height
    sort_btn.width = small_button_width
    sort_btn.font = small_button_font
    sort_btn.action = sort_btn_func
    sort_btn.style = 'default'
    sort_btn.color = small_button_color
    sort_btn.just = 'right'
    advanced_display.append(sort_btn)

    reset_btn.x = sort_btn.right + small_button_spacing
    reset_btn.y = attribute_btn.top
    reset_btn.height = small_button_height
    reset_btn.width = small_button_width
    reset_btn.font = small_button_font
    reset_btn.action = reset_btn_func
    reset_btn.style = 'default'
    reset_btn.color = small_button_color
    reset_btn.just = 'right'
    advanced_display.append(reset_btn)

    # ========== Simple Fields ==========
    label_width = 50
    rating_tf_width = 30
    field_spacing = 20

    rating_label.font = std_tf_font
    rating_label.width = label_width
    rating_label.height = std_tf_height
    rating_label.x = (win_edit.width - 2*label_width - std_tf_width - rating_tf_width - field_spacing) / 2
    rating_label.y = asc_desc_rg_msg.bottom + 5
    rating_label.color = title_color
    if settings['edit_subject'] != 'formations':
        simple_display.append(rating_label)

    rating_tf.font = std_tf_font
    rating_tf.width = rating_tf_width
    rating_tf.height = 25
    rating_tf.x = rating_label.right
    rating_tf.y = rating_label.top
    if settings['edit_subject'] != 'formations':
        simple_display.append(rating_tf)

    name_label.font = std_tf_font
    name_label.width = label_width
    name_label.height = std_tf_height
    if settings['edit_subject'] != 'formations':
        name_label.x = rating_tf.right + field_spacing
    else:
        name_label.x = (win_edit.width - label_width - std_tf_width) / 2
    name_label.y = rating_label.top
    name_label.color = title_color
    simple_display.append(name_label)

    name_tf.font = std_tf_font
    name_tf.width = std_tf_width
    name_tf.height = 25
    name_tf.x = name_label.right
    name_tf.y = rating_label.top
    simple_display.append(name_tf)

    # ========== Messages ==========
    lowest_msg_l = start_btn.top
    lowest_msg_r = start_btn.top

    attr_msg_offset = 25

    # Attribute Messages
    del settings['messages']['search'][:]
    del settings['messages']['sort'][:]

    if len(attr_dict) > 0:
        settings['messages']['search'].append(Label(text="Search Attributes:", font=title_tf_font, width=std_tf_width,
                                                    height=std_tf_height, x=attr_msg_offset, y=lowest_msg_l,
                                                    color=title_color))
        lowest_msg_l += std_tf_height

        for key, value in attr_dict.iteritems():
            msg_text = format_attr_name(key) + ": "
            if key in ['id', 'baseId', 'nationId', 'leagueId', 'clubId']:
                msg_text += str(value[0])
            elif type(value[0]) is int:
                msg_text += value[1].capitalize() + ' ' + str(value[0])
            elif value[1] == 'not':
                msg_text += value[1].capitalize() + ' "' + str(value[0]) + '"'
            else:
                msg_text += '"' + str(value[0]) + '"'

            attr_label = Label(text=msg_text, font=std_tf_font, width=std_tf_width,
                               height=std_tf_height, x=attr_msg_offset, y=lowest_msg_l, color=title_color)
            lowest_msg_l += std_tf_height
            settings['messages']['search'].append(attr_label)

    if len(attr_list) > 0:
        settings['messages']['sort'].append(Label(text="Sort Attributes:", font=title_tf_font, width=std_tf_width,
                                                  height=std_tf_height, x=advanced_btn.right + 3*attr_msg_offset,
                                                  y=lowest_msg_r, color=title_color))
        lowest_msg_r += std_tf_height

        for value in attr_list:
            attr_label = Label(text=(format_attr_name(value)), font=std_tf_font, width=std_tf_width,
                               height=std_tf_height, x=advanced_btn.right + 3*attr_msg_offset, y=lowest_msg_r,
                               color=title_color)
            lowest_msg_r += std_tf_height
            settings['messages']['sort'].append(attr_label)

    # ========== Previous, Add to List, Next Buttons ==========
    previous_btn = Button("<<< Previous %d" % num_results)
    add_to_list_btn = Button()
    next_btn = Button("Next %d >>>" % num_results)
    total_num_results_label = Label()
    pages_label = Label()

    def add_to_list_btn_func(input_list, func_type):
        import copy
        item_list = copy.deepcopy(input_list)

        if settings['edit_subject'] == 'players':
            if func_type == 'add all':
                added_players = []
                # Add current results to player list
                for player in item_list:
                    if list_players.db.count(player) == 0:
                        list_players.db.append(player)
                        added_players.append(player)

                # Sort
                list_players.sort(['rating'])
                # Save
                list_players.save(settings['file_name'], 'list', True)

                # Change button title and action
                add_to_list_btn.title = "Remove Added Players"
                add_to_list_btn.action = (add_to_list_btn_func, item_list, 'remove select')

                # Keep track of just added players
                settings['messages']['players_changed'] = added_players

            elif func_type == 'remove all':
                removed_players = []
                # Remove current results from player list
                for player in item_list:
                    if list_players.db.count(player) > 0:
                        list_players.db.remove(player)
                        removed_players.append(player)

                # Sort
                list_players.sort(['rating'])
                # Save
                list_players.save(settings['file_name'], 'list', True)

                # Change button title and action
                add_to_list_btn.title = "Add Removed Players"
                add_to_list_btn.action = (add_to_list_btn_func, item_list, 'add select')

                # Keep track of just removed players
                settings['messages']['players_changed'] = removed_players

            elif func_type == 'add select':
                # Add select players back to player list
                for player in settings['messages']['players_changed']:
                    if list_players.db.count(player) == 0:
                        list_players.db.append(player)

                # Sort
                list_players.sort(['rating'])
                # Save
                list_players.save(settings['file_name'], 'list', True)

                # Change button title and action
                add_to_list_btn.title = "Remove Added Players"
                add_to_list_btn.action = (add_to_list_btn_func, item_list, 'remove select')

            elif func_type == 'remove select':
                # Remove select players from player list
                for player in settings['messages']['players_changed']:
                    if list_players.db.count(player) > 0:
                        list_players.db.remove(player)

                # Sort
                list_players.sort(['rating'])
                # Save
                list_players.save(settings['file_name'], 'list', True)

                # Change button title and action
                add_to_list_btn.title = "Add Removed Players"
                add_to_list_btn.action = (add_to_list_btn_func, item_list, 'add select')

        elif settings['edit_subject'] == 'formations':
            if func_type == 'add all':
                added_formations = []
                # Add current results to formation list
                for formation in item_list:
                    if list_formations.db.count(formation) == 0:
                        list_formations.db.append(formation)
                        added_formations.append(formation)

                # Sort
                list_formations.sort(['name'])
                # Save
                list_formations.save(settings['file_name'], 'list', True)

                # Change button title and action
                add_to_list_btn.title = "Remove Added Forms"
                add_to_list_btn.action = (add_to_list_btn_func, item_list, 'remove select')

                # Keep track of just added formations
                settings['messages']['formations_changed'] = added_formations

            elif func_type == 'remove all':
                removed_formations = []
                # Remove current results from formation list
                for formation in item_list:
                    if formation in list_formations.db:
                        list_formations.db.remove(formation)
                        removed_formations.append(formation)

                # Sort
                list_formations.sort(['name'])
                # Save
                list_formations.save(settings['file_name'], 'list', True)

                # Change button title and action
                add_to_list_btn.title = "Add Removed Forms"
                add_to_list_btn.action = (add_to_list_btn_func, item_list, 'add select')

                # Keep track of just removed formations
                settings['messages']['formations_changed'] = removed_formations

            elif func_type == 'add select':
                # Add select formations back to formation list
                for formation in settings['messages']['formations_changed']:
                    if list_formations.db.count(formation) == 0:
                        list_formations.db.append(formation)

                # Sort
                list_formations.sort(['name'])
                # Save
                list_formations.save(settings['file_name'], 'list', True)

                # Change button title and action
                add_to_list_btn.title = "Remove Added Forms"
                add_to_list_btn.action = (add_to_list_btn_func, item_list, 'remove select')

            elif func_type == 'remove select':
                # Remove select formations from formation list
                for formation in settings['messages']['formations_changed']:
                    if list_formations.db.count(formation) > 0:
                        list_formations.db.remove(formation)

                # Sort
                list_formations.sort(['name'])
                # Save
                list_formations.save(settings['file_name'], 'list', True)

                # Change button title and action
                add_to_list_btn.title = "Add Removed Forms"
                add_to_list_btn.action = (add_to_list_btn_func, item_list, 'add select')

        del item_list
        win_edit.become_target()

    def previous_btn_func(display_db=None, attributes=None, index_range=None):
        if display_db is not None:
            # display previous results
            if settings['edit_subject'] == 'players':
                display_players(display_db, attributes, index_range)
            elif settings['edit_subject'] == 'formations':
                display_formations(display_db, attributes, index_range)
            #elif settings['edit_subject'] == 'teams':
                #display_teams(display_db, attributes, index_range)
        win_edit.become_target()

    def next_btn_func(display_db=None, attributes=None, index_range=None):
        if display_db is not None:
            # display next results
            if settings['edit_subject'] == 'players':
                display_players(display_db, attributes, index_range)
            elif settings['edit_subject'] == 'formations':
                display_formations(display_db, attributes, index_range)
            # elif settings['edit_subject'] == 'teams':
                # display_teams(display_db, attributes, index_range)
        win_edit.become_target()

    add_to_list_btn.x = attribute_btn.right + small_button_spacing
    add_to_list_btn.y = attribute_btn.bottom + 5
    add_to_list_btn.height = tiny_button_height
    add_to_list_btn.width = small_button_width
    add_to_list_btn.font = small_button_font
    add_to_list_btn.style = 'default'
    add_to_list_btn.color = small_button_color
    add_to_list_btn.just = 'right'

    previous_btn.height = tiny_button_height
    previous_btn.width = small_button_width
    previous_btn.x = add_to_list_btn.left - previous_btn.width - small_button_spacing
    previous_btn.y = add_to_list_btn.top
    previous_btn.font = small_button_font
    previous_btn.action = previous_btn_func
    previous_btn.style = 'default'
    previous_btn.color = small_button_color
    previous_btn.just = 'right'

    next_btn.height = tiny_button_height
    next_btn.width = small_button_width
    next_btn.x = add_to_list_btn.right + small_button_spacing
    next_btn.y = add_to_list_btn.top
    next_btn.font = small_button_font
    next_btn.action = next_btn_func
    next_btn.style = 'default'
    next_btn.color = small_button_color
    next_btn.just = 'right'

    total_num_results_label.font = std_tf_font
    total_num_results_label.width = 100
    total_num_results_label.height = std_tf_height
    total_num_results_label.x = previous_btn.left + - 100 - 10
    total_num_results_label.y = add_to_list_btn.top
    total_num_results_label.color = title_color
    total_num_results_label.just = 'right'

    pages_label.font = std_tf_font
    pages_label.width = 125
    pages_label.height = std_tf_height
    pages_label.x = next_btn.right + 10
    pages_label.y = add_to_list_btn.top
    pages_label.color = title_color
    pages_label.just = 'left'

    # ========== Display players from search ==========
    def display_players(display_db, attributes, index_range):
        # Remove old messages off page
        for message in settings['messages']['results']:
            view.remove(message)
        del settings['messages']['results'][:]

        # Add navigation buttons to page
        if settings['edit_type'] == 'add':
            add_to_list_btn.title = 'Add All Players'
            add_to_list_btn.action = (add_to_list_btn_func, display_db.db, 'add all')
        elif settings['edit_type'] == 'edit':
            add_to_list_btn.title = 'Remove All Players'
            add_to_list_btn.action = (add_to_list_btn_func, display_db.db, 'remove all')
        else:
            print "Invalid edit type."

        previous_range = (index_range[0]-num_results, index_range[0])
        previous_btn.action = (previous_btn_func, display_db, attributes, previous_range)

        next_range = (index_range[1], index_range[1]+num_results)
        next_btn.action = (next_btn_func, display_db, attributes, next_range)

        total_num_results_label.text = str(len(display_db.db)) + " Players"
        pages_label.text = "Page %d of %d" % (int(index_range[1]/num_results),
                                              math.ceil(len(display_db.db) / float(num_results)))

        if index_range[0] > 0:
            previous_btn.enabled = 1
        else:
            previous_btn.enabled = 0
        if index_range[1] <= len(display_db.db) - 1:
            next_btn.enabled = 1
        else:
            next_btn.enabled = 0

        settings['messages']['results'].append(add_to_list_btn)
        settings['messages']['results'].append(previous_btn)
        settings['messages']['results'].append(next_btn)
        settings['messages']['results'].append(total_num_results_label)
        settings['messages']['results'].append(pages_label)

        # Print out labels
        labels = player_info_labels(attributes)
        stat_index = 1
        spacing_list = [25, 125, 40, 40, 65, 115, 115, 115, 40]
        left_border = (win_width - sum(spacing_list[:-1]) - (len(labels) - len(spacing_list) + 2) * spacing_list[-1])/2
        msg_x = left_border + spacing_list[0]
        msg_y = add_to_list_btn.bottom + 5

        for info_label in labels:
            player_label = Label(text=info_label, font=std_tf_font_bold, width=spacing_list[stat_index]-5,
                                 height=std_tf_height, x=msg_x, y=msg_y, color=title_color)
            settings['messages']['results'].append(player_label)
            msg_x += spacing_list[stat_index]

            if stat_index < len(spacing_list)-1:
                stat_index += 1

        msg_y += std_tf_height + 5

        # Print out players
        for idx, player in enumerate(display_db.db[index_range[0]:index_range[1]]):
            msg_x = left_border
            player_stats = player_info(player, attributes)
            stat_index = 0

            player_data = list_players.search({'id': (player['id'], 'exact')})
            if len(player_data) > 0:
                add_btn_text = '-'
                temp_player = player_data[0]
            else:
                add_btn_text = '+'
                temp_player = player
            add_btn = Button(title=add_btn_text, width=spacing_list[stat_index]-5, height=15, x=msg_x, y=msg_y)
            add_btn.action = (add_btn_func, temp_player, add_btn)
            settings['messages']['results'].append(add_btn)
            msg_x += spacing_list[stat_index]
            stat_index += 1

            # Check for names that are too long
            name = player_stats[0]
            if len(name) > 20:
                name = player['lastName']

            bio_btn = Button(title=name, width=spacing_list[stat_index]-5, height=15, x=msg_x, y=msg_y,
                             action=(player_bio_btn_func, temp_player))
            settings['messages']['results'].append(bio_btn)
            msg_x += spacing_list[stat_index]
            stat_index += 1

            for player_stat in player_stats[1:]:
                player_label = Label(text=player_stat, font=small_button_font, width=spacing_list[stat_index]-5,
                                     height=std_tf_height, x=msg_x, y=msg_y, color=title_color)
                settings['messages']['results'].append(player_label)

                # Save values for position edit button
                if stat_index == 3:
                    edit_x = msg_x
                    edit_y = msg_y

                msg_x += spacing_list[stat_index]
                if stat_index < len(spacing_list) - 1:
                    stat_index += 1

            if settings['edit_type'] == 'edit':
                pos_btn = Button(title=player_stats[2], width=28, height=15, x=edit_x, y=edit_y)
                pos_btn.action = (pos_btn_func, player, pos_btn)
                settings['messages']['results'].append(pos_btn)

            msg_y += std_tf_height

        for results_msg in settings['messages']['results']:
            view.add(results_msg)

    # ========== Display formations from search ==========
    def display_formations(display_db, attributes, index_range):
        # Remove old messages off page
        for message in settings['messages']['results']:
            view.remove(message)
        del settings['messages']['results'][:]

        # Add navigation buttons to page
        if settings['edit_type'] == 'add':
            add_to_list_btn.title = 'Add All Formations'
            add_to_list_btn.action = (add_to_list_btn_func, display_db.db, 'add all')
        elif settings['edit_type'] == 'edit':
            add_to_list_btn.title = 'Remove All Formations'
            add_to_list_btn.action = (add_to_list_btn_func, display_db.db, 'remove all')
        else:
            print "Invalid edit type."

        previous_range = (index_range[0]-num_results, index_range[0])
        previous_btn.action = (previous_btn_func, display_db, attributes, previous_range)

        next_range = (index_range[1], index_range[1]+num_results)
        next_btn.action = (next_btn_func, display_db, attributes, next_range)

        total_num_results_label.text = str(len(display_db.db)) + " Formations"
        pages_label.text = "Page %d of %d" % (int(index_range[1]/num_results),
                                              math.ceil(len(display_db.db)/float(num_results)))

        if index_range[0] > 0:
            previous_btn.enabled = 1
        else:
            previous_btn.enabled = 0
        if index_range[1] <= len(display_db.db) - 1:
            next_btn.enabled = 1
        else:
            next_btn.enabled = 0

        settings['messages']['results'].append(add_to_list_btn)
        settings['messages']['results'].append(previous_btn)
        settings['messages']['results'].append(next_btn)
        settings['messages']['results'].append(total_num_results_label)
        settings['messages']['results'].append(pages_label)

        # Print out labels
        labels = formation_info_labels()
        stat_index = 1
        spacing_list = [25, 100, 100, 55, 55, 55, 55, 140, 160]
        left_border = (win_edit.width - sum(spacing_list))/2
        msg_x = left_border + spacing_list[0]
        msg_y = add_to_list_btn.bottom + 5

        for info_label in labels:
            formation_label = Label(text=info_label, font=std_tf_font_bold, width=spacing_list[stat_index]-5,
                                    height=std_tf_height, x=msg_x, y=msg_y, color=title_color)
            settings['messages']['results'].append(formation_label)
            msg_x += spacing_list[stat_index]

            if stat_index < len(spacing_list)-1:
                stat_index += 1

        msg_y += std_tf_height + 5

        # Print out formations
        for idx, formation in enumerate(display_db.db[index_range[0]:index_range[1]]):
            msg_x = left_border
            formation_stats = formation_info(formation)
            stat_index = 0

            if formation in list_formations.db:
                add_btn_text = '-'
            else:
                add_btn_text = '+'

            add_btn = Button(title=add_btn_text, width=spacing_list[stat_index]-5, height=15, x=msg_x, y=msg_y)
            add_btn.action = (add_btn_func, formation, add_btn)
            settings['messages']['results'].append(add_btn)
            msg_x += spacing_list[stat_index]
            stat_index += 1

            bio_btn = Button(title=formation['name'], width=spacing_list[stat_index]-5, height=15, x=msg_x, y=msg_y,
                             action=(formation_bio_btn_func, formation))
            settings['messages']['results'].append(bio_btn)
            msg_x += spacing_list[stat_index]
            stat_index += 1

            for formation_stat in formation_stats[1:]:
                formation_label = Label(text=formation_stat, font=small_button_font, width=spacing_list[stat_index]-5,
                                        height=std_tf_height, x=msg_x, y=msg_y, color=title_color)
                settings['messages']['results'].append(formation_label)

                msg_x += spacing_list[stat_index]
                if stat_index < len(spacing_list) - 1:
                    stat_index += 1

            msg_y += std_tf_height

        for results_msg in settings['messages']['results']:
            view.add(results_msg)

    # ========== Add components to view and add view to window ==========
    for item in general_display:
        view.add(item)

    if settings['edit_mode'] == 'simple':
        for item in simple_display:
            view.add(item)
    elif settings['edit_mode'] == 'advanced':
        for item in advanced_display:
            view.add(item)
        display_attributes()

    for msg in settings['messages']['results']:
        view.add(msg)

    win_edit.add(view)
    view.become_target()
    win_edit.show()
