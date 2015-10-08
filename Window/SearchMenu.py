from GUI import Button, Label, RadioButton, RadioGroup, View, Window
import json
import math
import unicodedata
from AppConfig import *
import StartMenu
import AddAttribute
import PlayerBio
from Logic import PlayerDB
from Logic import FormationDB
from Logic import TeamDB
from Logic.HelperFunctions import format_attr_name, player_info_labels, player_info


def open_search_menu(window_x, window_y, db_dict, attr_dict=None, attr_list=None, settings=None):

    num_results = 20

    with open('configs.json', 'r') as f:
        default_search = json.load(f)['default_search']
        f.close()

    if attr_dict is None:
        attr_dict = {}
        for default in default_search['search_attributes']:
            attr_dict[default[0]] = (default[1], default[2])

    if attr_list is None:
        attr_list = default_search['sort_attributes']

    if settings is None:
        settings = {
            'mode': 'players',
            'p_db_rg': 'all_players',
            'f_db_rg': 'all_formations',
            'order_rg': True,
            'messages': {
                'search': [],
                'sort': [],
                'results': []
            }
        }

    # ========== Window ==========
    win_search = Window()
    win_search.title = search_win_title
    win_search.auto_position = False
    win_search.position = (window_x, window_y)
    win_search.size = (win_width, win_height)
    win_search.resizable = 0
    win_search.name = "Search Window"

    # ========== Window Image View ==========
    class FormationsWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = FormationsWindowImageView(size=win_search.size)

    # ========== Title ==========
    title = Label(text=search_title)
    title.font = title_font
    title.width = title_width
    title.height = title_height
    title.x = (win_width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'

    # ========== Action Button Declarations ==========
    start_btn = Button("Start")
    back_btn = Button("Back")

    # ========== Search Type Button Declarations ==========
    players_btn = Button("Players")
    formations_btn = Button("Formations")
    teams_btn = Button("Teams")

    search_type_button_list = [players_btn,
                               formations_btn,
                               teams_btn]

    # ========== Tool Button Declarations ==========
    attribute_btn = Button("Add Search Attribute")
    sort_btn = Button("Add Sort Attribute")
    reset_btn = Button("Reset Results")

    # ========== Action Button Functions ==========
    def start_btn_func():
        # Start button corresponds to players
        if settings['mode'] == 'players':
            search_results = db_dict[p_db_radio_group.value][1].search(attr_dict)
            search_results = PlayerDB.PlayerDB(search_results)
            search_results.sort(attr_list, sort_order_radio_group.value)
            # search_results.print_compare_info()  # num_results)

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
        elif settings['mode'] == 'formations':
            search_results = db_dict[f_db_radio_group.value][1].search(attr_dict)
            search_results = FormationDB.FormationDB(search_results)
            search_results.sort(attr_list, sort_order_radio_group.value)
            search_results.print_db_short()

        # Start button corresponds to teams
        elif settings['mode'] == 'teams':
            stuff = 0

        win_search.become_target()

    def back_btn_func():
        win_search.hide()
        StartMenu.open_start_menu(win_search.x, win_search.y, db_dict)

    # ========== Search Type Button Functions ==========
    def players_btn_func():
        for btn in search_type_button_list:
            btn.enabled = 1
        players_btn.enabled = 0
        settings['mode'] = 'players'

        # Reset screen
        reset_btn_func()

        view.remove(f_db_rg_msg)
        view.remove(all_formations_radio_btn)
        view.remove(my_formations_radio_btn)
        view.remove(t_db_rg_msg)

        view.add(p_db_rg_msg)
        view.add(all_players_radio_btn)
        view.add(my_players_radio_btn)

        win_search.become_target()

    def formations_btn_func():
        for btn in search_type_button_list:
            btn.enabled = 1
        formations_btn.enabled = 0
        settings['mode'] = 'formations'

        # Reset screen
        reset_btn_func()

        view.remove(p_db_rg_msg)
        view.remove(all_players_radio_btn)
        view.remove(my_players_radio_btn)
        view.remove(t_db_rg_msg)

        view.add(f_db_rg_msg)
        view.add(all_formations_radio_btn)
        view.add(my_formations_radio_btn)

        win_search.become_target()

    def teams_btn_func():
        for btn in search_type_button_list:
            btn.enabled = 1
        teams_btn.enabled = 0
        settings['mode'] = 'teams'

        # Reset screen
        reset_btn_func()

        view.remove(p_db_rg_msg)
        view.remove(all_players_radio_btn)
        view.remove(my_players_radio_btn)
        view.remove(f_db_rg_msg)
        view.remove(all_formations_radio_btn)
        view.remove(my_formations_radio_btn)

        view.add(t_db_rg_msg)

        win_search.become_target()

    # ========== Tool Button Functions ==========
    def attribute_btn_func():
        # Delete results
        del settings['messages']['results'][:]

        # Open new window and close current window
        win_search.hide()
        AddAttribute.open_attribute_window(win_search.x, win_search.y,
                                           db_dict, attr_dict, attr_list, 'search', settings)

    def sort_btn_func():
        # Delete results
        del settings['messages']['results'][:]

        # Open new window and close current window
        win_search.hide()
        AddAttribute.open_attribute_window(win_search.x, win_search.y, db_dict,
                                           attr_dict, attr_list, 'sort', settings)

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

        # Disable start button
        start_btn.enabled = 0

        win_search.become_target()

    def player_bio_btn_func(player):
        win_search.hide()
        PlayerBio.open_player_bio_window(win_search.x, win_search.y, player, db_dict, win_search)
        win_search.become_target()

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

    back_btn.x = start_btn.right + small_button_spacing
    back_btn.y = start_btn.top
    back_btn.height = small_button_height
    back_btn.width = small_button_width
    back_btn.font = small_button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = small_button_color
    back_btn.just = 'right'

    # ========== Search Type Buttons ==========
    players_btn.x = (win_width - 3*small_button_width - 2*small_button_spacing) / 2
    players_btn.y = start_btn.bottom + small_button_top_spacing
    players_btn.height = small_button_height
    players_btn.width = small_button_width
    players_btn.font = small_button_font
    players_btn.action = players_btn_func
    players_btn.style = 'default'
    players_btn.color = small_button_color
    players_btn.just = 'right'
    if settings['mode'] == 'players':
        players_btn.enabled = 0

    formations_btn.x = players_btn.right + small_button_spacing
    formations_btn.y = players_btn.top
    formations_btn.height = small_button_height
    formations_btn.width = small_button_width
    formations_btn.font = small_button_font
    formations_btn.action = formations_btn_func
    formations_btn.style = 'default'
    formations_btn.color = small_button_color
    formations_btn.just = 'right'
    if settings['mode'] == 'formations':
        formations_btn.enabled = 0

    teams_btn.x = formations_btn.right + small_button_spacing
    teams_btn.y = players_btn.top
    teams_btn.height = small_button_height
    teams_btn.width = small_button_width
    teams_btn.font = small_button_font
    teams_btn.action = teams_btn_func
    teams_btn.style = 'default'
    teams_btn.color = small_button_color
    teams_btn.just = 'right'
    if settings['mode'] == 'teams':
        teams_btn.enabled = 0

    # ========== Tool Buttons ==========
    attribute_btn.x = (win_width - 3*small_button_width - 2*small_button_spacing) / 2
    attribute_btn.y = players_btn.bottom + 5
    attribute_btn.height = small_button_height
    attribute_btn.width = small_button_width
    attribute_btn.font = small_button_font
    attribute_btn.action = attribute_btn_func
    attribute_btn.style = 'default'
    attribute_btn.color = small_button_color
    attribute_btn.just = 'right'

    sort_btn.x = attribute_btn.right + small_button_spacing
    sort_btn.y = attribute_btn.top
    sort_btn.height = small_button_height
    sort_btn.width = small_button_width
    sort_btn.font = small_button_font
    sort_btn.action = sort_btn_func
    sort_btn.style = 'default'
    sort_btn.color = small_button_color
    sort_btn.just = 'right'

    reset_btn.x = sort_btn.right + small_button_spacing
    reset_btn.y = attribute_btn.top
    reset_btn.height = small_button_height
    reset_btn.width = small_button_width
    reset_btn.font = small_button_font
    reset_btn.action = reset_btn_func
    reset_btn.style = 'default'
    reset_btn.color = small_button_color
    reset_btn.just = 'right'

    # ========== DB Radio Buttons ==========
    def get_attribute_p_db_rg():
        settings['p_db_rg'] = p_db_radio_group.value
        win_search.become_target()

    def get_attribute_f_db_rg():
        settings['f_db_rg'] = f_db_radio_group.value
        win_search.become_target()

    p_db_radio_group = RadioGroup(action=get_attribute_p_db_rg)
    f_db_radio_group = RadioGroup(action=get_attribute_f_db_rg)

    db_radio_btn_width = 125
    db_radio_btn_space = 5
    db_msg_width = 70

    # Players DB RG
    p_db_rg_msg =Label(text=("Database:"), font=std_tf_font, width=db_msg_width,
                     height=std_tf_height, color=title_color)
    p_db_rg_msg.x = (win_search.width - 2*db_radio_btn_width - db_radio_btn_space - db_msg_width) / 2
    p_db_rg_msg.y = reset_btn.bottom + db_radio_btn_space

    all_players_radio_btn = RadioButton(db_dict['all_players'][0])
    all_players_radio_btn.width = db_radio_btn_width
    all_players_radio_btn.x = p_db_rg_msg.right
    all_players_radio_btn.y = p_db_rg_msg.top
    all_players_radio_btn.group = p_db_radio_group
    all_players_radio_btn.value = 'all_players'

    my_players_radio_btn = RadioButton(db_dict['my_players'][0])
    my_players_radio_btn.width = db_radio_btn_width
    my_players_radio_btn.x = all_players_radio_btn.right + db_radio_btn_space
    my_players_radio_btn.y = all_players_radio_btn.top
    my_players_radio_btn.group = p_db_radio_group
    my_players_radio_btn.value = 'my_players'

    p_db_radio_group.value = settings['p_db_rg']

    # Formations DB RG
    f_db_rg_msg =Label(text=("Database:"), font=std_tf_font, width=db_msg_width,
                     height=std_tf_height, color=title_color)
    f_db_rg_msg.x = (win_search.width - 2*db_radio_btn_width - db_radio_btn_space - db_msg_width) / 2
    f_db_rg_msg.y = reset_btn.bottom + db_radio_btn_space

    all_formations_radio_btn = RadioButton(db_dict['all_formations'][0])
    all_formations_radio_btn.width = db_radio_btn_width
    all_formations_radio_btn.x = f_db_rg_msg.right
    all_formations_radio_btn.y = f_db_rg_msg.top
    all_formations_radio_btn.group = f_db_radio_group
    all_formations_radio_btn.value = 'all_formations'

    my_formations_radio_btn = RadioButton(db_dict['my_formations'][0])
    my_formations_radio_btn.width = db_radio_btn_width
    my_formations_radio_btn.x = all_formations_radio_btn.right + db_radio_btn_space
    my_formations_radio_btn.y = all_formations_radio_btn.top
    my_formations_radio_btn.group = f_db_radio_group
    my_formations_radio_btn.value = 'my_formations'

    f_db_radio_group.value = settings['f_db_rg']

    # Teams DB RG
    teams_db_msg_width = 250
    t_db_rg_msg =Label(text=("Database: " + db_dict['teams'][0]), font=std_tf_font, width=teams_db_msg_width,
                     height=std_tf_height, color=title_color)
    t_db_rg_msg.x = (win_search.width - teams_db_msg_width) / 2
    t_db_rg_msg.y = reset_btn.bottom + db_radio_btn_space

    if settings['mode'] == 'players':
        view.add(p_db_rg_msg)
        view.add(all_players_radio_btn)
        view.add(my_players_radio_btn)
    elif settings['mode'] == 'formations':
        view.add(f_db_rg_msg)
        view.add(all_formations_radio_btn)
        view.add(my_formations_radio_btn)
    elif settings['mode'] == 'teams':
        view.add(t_db_rg_msg)
    else:
        print "Error: Invalid mode."

    rg_1_bottom = all_players_radio_btn.bottom

    # ========== Sort Order Radio Buttons ==========
    def get_attribute_sort_order_rg():
        settings['order_rg'] = sort_order_radio_group.value
        win_search.become_target()

    sort_order_radio_group = RadioGroup(action=get_attribute_sort_order_rg)

    asc_desc_radio_btn_width = 75
    asc_msg_width = 80
    radio_btn_space = 5

    asc_desc_rg_msg =Label(text=("Sort Order:"), font=std_tf_font, width=asc_msg_width, height=std_tf_height,
                           color=title_color)
    asc_desc_rg_msg.x = (win_search.width - 2*asc_desc_radio_btn_width - radio_btn_space - asc_msg_width) / 2
    asc_desc_rg_msg.y = all_formations_radio_btn.bottom + radio_btn_space

    descend_radio_btn = RadioButton("Descending")
    descend_radio_btn.width = asc_desc_radio_btn_width
    descend_radio_btn.x = asc_desc_rg_msg.right
    descend_radio_btn.y = asc_desc_rg_msg.top
    descend_radio_btn.group = sort_order_radio_group
    descend_radio_btn.value = True

    ascend_radio_btn = RadioButton("Ascending")
    ascend_radio_btn.width = asc_desc_radio_btn_width
    ascend_radio_btn.x = descend_radio_btn.right + radio_btn_space
    ascend_radio_btn.y = descend_radio_btn.top
    ascend_radio_btn.group = sort_order_radio_group
    ascend_radio_btn.value = False

    sort_order_radio_group.value = settings['order_rg']

    # ========== Messages ==========
    lowest_msg_l = start_btn.top
    lowest_msg_r = start_btn.top

    attr_msg_offset = 25

    # Attribute Messages
    del settings['messages']['search'][:]
    del settings['messages']['sort'][:]

    if len(attr_dict) > 0:
        settings['messages']['search'].append(Label(text=("Search Attributes:"), font=title_tf_font, width=std_tf_width,
                               height=std_tf_height, x=attr_msg_offset, y=lowest_msg_l, color=title_color))
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
        settings['messages']['sort'].append(Label(text=("Sort Attributes:"), font=title_tf_font, width=std_tf_width,
                                   height=std_tf_height, x=teams_btn.right + 3*attr_msg_offset, y=lowest_msg_r,
                                   color=title_color))
        lowest_msg_r += std_tf_height

        for value in attr_list:
            attr_label = Label(text=(format_attr_name(value)), font=std_tf_font, width=std_tf_width, height=std_tf_height,
                               x=teams_btn.right + 3*attr_msg_offset, y=lowest_msg_r, color=title_color)
            lowest_msg_r += std_tf_height
            settings['messages']['sort'].append(attr_label)

    # Disable start button if no search or sort parameters
    if len(attr_dict) == 0 and len(attr_list) == 0:
        start_btn.enabled = 0
    else:
        start_btn.enabled = 1

    # ========== Previous, Add to List, Next Buttons ==========
    previous_btn = Button("<<< Previous %d" % num_results)
    add_to_list_btn = Button("Add Players to List")
    next_btn = Button("Next %d >>>" % num_results)
    total_num_results_label = Label()
    pages_label = Label()

    def add_to_list_btn_func(player_list=None, func_type=None):
        if func_type == 'add':
            added_players = []
            # Add current results to player list
            for player in player_list:
                if db_dict['my_players'][1].db.count(player) == 0:
                    db_dict['my_players'][1].db.append(player)
                    added_players.append(player)
            # Sort
            db_dict['my_players'][1].sort(['rating'])
            # Save
            db_dict['my_players'][1].save(db_dict['my_players'][0])

            # Change button title and action
            add_to_list_btn.title = "Remove Added Players"
            add_to_list_btn.action = (add_to_list_btn_func, player_list, 'remove')

            # Keep track of just added players
            settings['messages']['players_just_added'] = added_players

        elif func_type == 'remove':
            # Remove players just added
            for player in settings['messages']['players_just_added']:
                if db_dict['my_players'][1].db.count(player) > 0:
                    db_dict['my_players'][1].db.remove(player)
            # Sort
            db_dict['my_players'][1].sort(['rating'])
            # Save
            db_dict['my_players'][1].save(db_dict['my_players'][0])

            # Change button title and action
            add_to_list_btn.title = "Add Players to List"
            add_to_list_btn.action = (add_to_list_btn_func, player_list, 'add')

            # Delete the just added players list
            settings['messages'].pop('players_just_added', None)

        win_search.become_target()

    def previous_btn_func(display_player_db=None, attributes=None, index_range=None):
        if display_player_db is not None:
            # display previous results
            display_players(display_player_db, attributes, index_range)
        win_search.become_target()

    def next_btn_func(display_player_db=None, attributes=None, index_range=None):
        if display_player_db is not None:
            # display next results
            display_players(display_player_db, attributes, index_range)
        win_search.become_target()

    add_to_list_btn.x = attribute_btn.right + small_button_spacing
    add_to_list_btn.y = descend_radio_btn.bottom + 5
    add_to_list_btn.height = tiny_button_height
    add_to_list_btn.width = small_button_width
    add_to_list_btn.font = small_button_font
    add_to_list_btn.action = add_to_list_btn_func
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
    def display_players(display_player_db, attributes, index_range):
        # Remove old messages off page
        for message in settings['messages']['results']:
            view.remove(message)
        del settings['messages']['results'][:]

        # Add navigation buttons to page
        add_to_list_btn.action = (add_to_list_btn_func, display_player_db.db, 'add')

        previous_range = (index_range[0]-num_results, index_range[0])
        previous_btn.action = (previous_btn_func, display_player_db, attributes, previous_range)

        next_range = (index_range[1], index_range[1]+num_results)
        next_btn.action = (next_btn_func, display_player_db, attributes, next_range)

        total_num_results_label.text = str(len(display_player_db.db)) + " Players"
        pages_label.text = "Page %d of %d" % (int(index_range[1]/20), math.ceil(len(display_player_db.db)/20) + 1)

        if index_range[0] > 0:
            previous_btn.enabled = 1
        else:
            previous_btn.enabled = 0
        if index_range[1] <= len(display_player_db.db) - 1:
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
        stat_index = 0
        spacing_list = [125, 40, 40, 65, 115, 115, 115, 40]
        left_border = (win_width - sum(spacing_list[:-1]) - (len(labels) - len(spacing_list) + 1) * spacing_list[-1])/2
        msg_x = left_border
        msg_y = add_to_list_btn.bottom + 5

        for info_label in labels:
            player_label = Label(text=info_label, font=std_tf_font_bold, width=win_width-(2*left_border),
                               height=std_tf_height, x=msg_x, y=msg_y, color=title_color)
            settings['messages']['results'].append(player_label)
            msg_x += spacing_list[stat_index]

            if stat_index < len(spacing_list)-1:
                stat_index += 1

        msg_y += std_tf_height + 5

        # Print out players
        for idx, player in enumerate(display_player_db.db[index_range[0]:index_range[1]]):
            msg_x = left_border
            player_stats = player_info(player, attributes)
            stat_index = 0

            bio_btn = Button(title=player_stats[0], width=120, height=15, x=msg_x, y=msg_y,
                             action=(player_bio_btn_func, player))
            settings['messages']['results'].append(bio_btn)
            msg_x += spacing_list[stat_index]
            stat_index += 1

            for player_stat in player_stats[1:]:
                player_label = Label(text=player_stat, font=small_button_font, width=win_width-(2*left_border),
                                     height=std_tf_height, x=msg_x, y=msg_y, color=title_color)

                settings['messages']['results'].append(player_label)
                msg_x += spacing_list[stat_index]
                if stat_index < len(spacing_list) - 1:
                    stat_index += 1

            msg_y += std_tf_height

        for msg in settings['messages']['results']:
            view.add(msg)

    # ========== Add components to view and add view to window ==========
    view.add(title)
    view.add(start_btn)
    view.add(back_btn)
    view.add(players_btn)
    view.add(formations_btn)
    view.add(teams_btn)
    view.add(attribute_btn)
    view.add(sort_btn)
    view.add(reset_btn)

    view.add(descend_radio_btn)
    view.add(ascend_radio_btn)
    view.add(asc_desc_rg_msg)

    for msg in settings['messages']['search']:
        view.add(msg)
    for msg in settings['messages']['sort']:
        view.add(msg)
    for msg in settings['messages']['results']:
        view.add(msg)

    win_search.add(view)
    view.become_target()
    win_search.show()
