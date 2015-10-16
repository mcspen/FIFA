from GUI import Button, Label, TextField, View, Window
from AppConfig import *
import ManageMenu
from Logic.HelperFunctions import get_file_prefix, player_info_labels, player_info
from Logic.PlayerDB import PlayerDB
from Logic.FormationDB import FormationDB
from Logic.TeamDB import TeamDB
from os.path import isfile
import math


def open_create_list_window(window_x, window_y, db_dict, settings):

    message_text = 'Select list type.'
    create_list_settings = dict()
    create_list_settings['results'] = []
    num_results = 5

    # ========== Window ==========
    win_create_list = Window()
    win_create_list.title = create_list_win_title
    win_create_list.auto_position = False
    win_create_list.position = (window_x+100, window_y+100)
    win_create_list.size = (win_width-100, win_height-200)
    win_create_list.resizable = 0
    win_create_list.name = create_list_title + " Window"
    win_create_list.show()

    # ========== Window Image View ==========
    class StartWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = StartWindowImageView(size=win_create_list.size)

    # ========== Title ==========
    title = Label(text=create_list_title)
    title.font = title_font
    title.width = title_width
    title.height = title_height
    title.x = (win_create_list.width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'

    # ========== Message Label ==========
    message = Label(font=title_font_2, width=win_create_list.width - 50, height=title_height,
                    x=25, y=title.bottom + top_border, color=title_color, just='center')
    message.text = message_text

    # ========== Button Declarations ==========
    enter_btn = Button("Enter")
    back_btn = Button("Back")

    player_list_btn = Button("Player")
    formation_list_btn = Button("Formation")
    team_list_btn = Button("Team")

    # ========== Results Navigation Item Declarations ==========
    previous_btn = Button("<<< Previous %d" % num_results)
    next_btn = Button("Next %d >>>" % num_results)
    total_num_results_label = Label()
    pages_label = Label()

    # ========== Button Functions ==========
    def enter_btn_func():
        # Get file name and save
        if create_list_settings['process_step'] == 'file name':

            # Get file name and file prefix
            file_name = value_tf.value
            file_prefix = get_file_prefix('current_' + create_list_settings['list_type'] + '_list')

            if len(file_name) > 0:

                if not isfile('JSONs/' + file_prefix + file_name + '.json'):

                    # Create list object, set message, and set process step
                    if create_list_settings['list_type'] == 'player':
                        new_list = PlayerDB()
                        message.text = "Enter player rating/name or just name."
                        create_list_settings['process_step'] = 'get player'

                    elif create_list_settings['list_type'] == 'formation':
                        new_list = FormationDB()
                        message.text = "Enter formation stuff."
                        create_list_settings['process_step'] = 'get formation'

                    elif create_list_settings['list_type'] == 'team':
                        new_list = TeamDB()
                        message.text = "Enter team stuff."
                        create_list_settings['process_step'] = 'get team'

                    else:
                        new_list = PlayerDB()
                        print "Invalid list type."

                    # Assign file name and file object
                    create_list_settings['list'] = new_list
                    create_list_settings['file_name'] = file_name

                    # Clear box content
                    value_tf.value = ''

                else:
                    message.text = "A file with that name already exists."

            else:
                message.text = "File name must be at least 1 character."

        # Get player to add to list
        elif create_list_settings['process_step'] == 'get player':
            # Get file name and file prefix
            player_input = value_tf.value

            # Remove result messages off page
            for result_message in create_list_settings['results']:
                view.remove(result_message)

            if len(player_input) > 0:
                search_dict = {}

                # Check for rating
                if player_input.split(' ')[0].isdigit():
                    # Check if there is a name and rating
                    if len(player_input.split(' ')) > 1:
                        search_dict['rating'] = (int(player_input.split(' ')[0]), 'exact')

                        # Get name
                        search_dict['name_custom'] = (player_input.split(' ', 1)[1], 'exact')

                    else:
                        message.text = "Invalid. Ex: '99 Superman'  or 'Superman'."

                # No rating, just name (or invalid)
                else:
                    search_dict['name_custom'] = (player_input, 'exact')

                # Valid input
                if len(search_dict) > 0:
                    # Search for players
                    results = PlayerDB(db_dict['player_db'][1].search(search_dict))
                    results.sort(['name'])

                    # No matching players found
                    if len(results.db) == 0:
                        message.text = "Unable to find player. Try again."

                    # If only one player in results, add player.
                    elif len(results.db) == 1:
                        add_player_btn_func(results.db[0])

                    else:
                        message.text = "Multiple players found. Pick correct one."
                        display_players(results, [], (0, num_results))

                value_tf.become_target()

            else:
                message.text = "Invalid. Ex: '99 Superman'  or 'Superman'."
                value_tf.become_target()

        # Get formation to add to list
        elif create_list_settings['process_step'] == 'get formation':
            stuff = 0

        # Get team to add to list
        elif create_list_settings['process_step'] == 'get team':
            stuff = 0

        # Invalid process step
        else:
            print "Create file process step is invalid."

    def back_btn_func():
        ManageMenu.open_manage_menu(window_x, window_y, db_dict, settings)
        win_create_list.hide()

    def list_type_func(list_type):
        # Remove list type buttons
        view.remove(player_list_btn)
        view.remove(formation_list_btn)
        view.remove(team_list_btn)

        # Add textfield, enabled enter button, and change message
        view.add(value_tf)
        enter_btn.enabled = 1
        message.text = "Enter file name."
        create_list_settings['list_type'] = list_type

        # Set list type
        create_list_settings['process_step'] = 'file name'
        value_tf.become_target()

    # ========== Action Buttons ==========
    enter_btn.x = (win_create_list.width - 2*button_width - button_spacing) / 2
    enter_btn.y = win_create_list.height - button_height - 40
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

    # ========== List Type Buttons ==========
    player_list_btn.x = (win_create_list.width - 3*button_width - 2*button_spacing) / 2
    player_list_btn.y = message.bottom + top_border
    player_list_btn.height = button_height
    player_list_btn.width = button_width
    player_list_btn.font = button_font
    player_list_btn.action = (list_type_func, 'player')
    player_list_btn.style = 'default'
    player_list_btn.color = button_color
    player_list_btn.just = 'right'

    formation_list_btn.x = player_list_btn.right + button_spacing
    formation_list_btn.y = player_list_btn.top
    formation_list_btn.height = button_height
    formation_list_btn.width = button_width
    formation_list_btn.font = button_font
    formation_list_btn.action = (list_type_func, 'formation')
    formation_list_btn.style = 'default'
    formation_list_btn.color = button_color
    formation_list_btn.just = 'right'
    formation_list_btn.enabled = 0  # Not implemented yet

    team_list_btn.x = formation_list_btn.right + button_spacing
    team_list_btn.y = player_list_btn.top
    team_list_btn.height = button_height
    team_list_btn.width = button_width
    team_list_btn.font = button_font
    team_list_btn.action = (list_type_func, 'team')
    team_list_btn.style = 'default'
    team_list_btn.color = button_color
    team_list_btn.just = 'right'
    team_list_btn.enabled = 0  # Not implemented yet

    # ========== Value Textfield ==========
    value_tf = TextField()
    value_tf.width = 200
    value_tf.x = (win_create_list.width - value_tf.width) / 2
    value_tf.y = message.bottom + top_border
    value_tf.height = 25
    value_tf.font = std_tf_font

    # ========== Players navigation functions ==========
    def previous_btn_func(display_player_db=None, attributes=None, index_range=None):
        if display_player_db is not None:
            # display previous results
            display_players(display_player_db, attributes, index_range)
        win_create_list.become_target()

    def next_btn_func(display_player_db=None, attributes=None, index_range=None):
        if display_player_db is not None:
            # display next results
            display_players(display_player_db, attributes, index_range)
        win_create_list.become_target()

    def add_player_btn_func(player):
        # Check for duplicates
        if create_list_settings['list'].db.count(player) == 0:
            # Add player, sort, and save
            create_list_settings['list'].db.append(player)
            create_list_settings['list'].sort(['rating'])
            create_list_settings['list'].save(create_list_settings['file_name'], 'list', True)

            # Remove result messages off page
            for result_message in create_list_settings['results']:
                view.remove(result_message)

            # Reset page
            value_tf.value = ''
            message.text = "Added player! Enter next player."
            back_btn.title = "Done"
            value_tf.become_target()

        # Duplicate player, don't add
        else:
            message.text = "Player already on list."
            win_create_list.become_target()

    # ========== Display Players Buttons ==========
    previous_btn.height = tiny_button_height
    previous_btn.width = small_button_width
    previous_btn.x = (win_create_list.width - 2*small_button_width - small_button_spacing) / 2
    previous_btn.y = value_tf.bottom + top_border
    previous_btn.font = small_button_font
    previous_btn.action = previous_btn_func
    previous_btn.style = 'default'
    previous_btn.color = small_button_color
    previous_btn.just = 'right'

    next_btn.height = tiny_button_height
    next_btn.width = small_button_width
    next_btn.x = previous_btn.right + small_button_spacing
    next_btn.y = previous_btn.top
    next_btn.font = small_button_font
    next_btn.action = next_btn_func
    next_btn.style = 'default'
    next_btn.color = small_button_color
    next_btn.just = 'right'

    total_num_results_label.font = std_tf_font
    total_num_results_label.width = 100
    total_num_results_label.height = std_tf_height
    total_num_results_label.x = previous_btn.left + - 100 - 10
    total_num_results_label.y = previous_btn.top
    total_num_results_label.color = title_color
    total_num_results_label.just = 'right'

    pages_label.font = std_tf_font
    pages_label.width = 125
    pages_label.height = std_tf_height
    pages_label.x = next_btn.right + 10
    pages_label.y = previous_btn.top
    pages_label.color = title_color
    pages_label.just = 'left'

    # ========== Display players from search ==========
    def display_players(results_list, attributes, index_range):
        # Remove old messages off page
        for result_message in create_list_settings['results']:
            view.remove(result_message)
        del create_list_settings['results'][:]

        # Add navigation buttons to page
        previous_range = (index_range[0]-num_results, index_range[0])
        previous_btn.action = (previous_btn_func, results_list, attributes, previous_range)

        next_range = (index_range[1], index_range[1]+num_results)
        next_btn.action = (next_btn_func, results_list, attributes, next_range)

        total_num_results_label.text = str(len(results_list.db)) + " Players"
        pages_label.text = "Page %d of %d" % (int(index_range[1]/num_results),
                                              math.ceil(len(results_list.db)/num_results) + 1)

        if index_range[0] > 0:
            previous_btn.enabled = 1
        else:
            previous_btn.enabled = 0
        if index_range[1] <= len(results_list.db) - 1:
            next_btn.enabled = 1
        else:
            next_btn.enabled = 0

        create_list_settings['results'].append(previous_btn)
        create_list_settings['results'].append(next_btn)
        create_list_settings['results'].append(total_num_results_label)
        create_list_settings['results'].append(pages_label)

        # Print out labels
        labels = [''] + player_info_labels(attributes)
        stat_index = 0
        add_btn_width = 30
        add_btn_space = add_btn_width + 10
        spacing_list = [add_btn_space, 125, 40, 40, 65, 115, 115, 115]
        left_border = (win_create_list.width - sum(spacing_list)) / 2
        msg_x = left_border + add_btn_space
        msg_y = previous_btn.bottom + 5

        for info_label in labels:
            player_label = Label(text=info_label, font=std_tf_font_bold, width=win_width-(2*left_border),
                                 height=std_tf_height, x=msg_x, y=msg_y, color=title_color)
            create_list_settings['results'].append(player_label)
            msg_x += spacing_list[stat_index]
            stat_index += 1

        msg_y += std_tf_height + 5

        # Print out players
        for idx, player in enumerate(results_list.db[index_range[0]:index_range[1]]):
            msg_x = left_border
            player_stats = player_info(player, attributes)
            stat_index = 0

            add_btn = Button("Add", width=add_btn_width, height=15, x=msg_x, y=msg_y,
                             action=(add_player_btn_func, player))
            create_list_settings['results'].append(add_btn)
            msg_x += spacing_list[stat_index]
            stat_index += 1

            for player_stat in player_stats:
                player_label = Label(text=player_stat, font=small_button_font, width=win_width-(2*left_border),
                                     height=std_tf_height, x=msg_x, y=msg_y, color=title_color)

                create_list_settings['results'].append(player_label)
                msg_x += spacing_list[stat_index]
                stat_index += 1

            msg_y += std_tf_height

        for results_msg in create_list_settings['results']:
            view.add(results_msg)

    # ========== Add items to window ==========
    view.add(title)
    view.add(message)
    view.add(enter_btn)
    view.add(back_btn)
    view.add(player_list_btn)
    view.add(formation_list_btn)
    view.add(team_list_btn)

    win_create_list.add(view)
    view.become_target()
    win_create_list.show()
