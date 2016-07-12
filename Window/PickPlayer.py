from GUI import Button, Label, RadioButton, RadioGroup, View, Window
import math
from AppConfig import *
import AddAttribute
import PlayerBio
from Logic import PlayerDB
from Logic import Team
from Logic.HelperFunctions import format_attr_name, player_info_labels, player_info


def open_pick_player_window(window_x, window_y, db_dict, input_formation, win_previous, roster, pos_symbol,
                            pick_formations_page, attr_dict=None, attr_list=None, settings=None):

    num_results = 20
    general_display = []

    if attr_dict is None:
        attr_dict = {}

    if attr_list is None:
        attr_list = []

    if settings is None:
        settings = {
            'window': 'pick_player',
            'p_db_rg': 'player_db',
            'pos_search_rg': 'green',
            'order_rg': True,
            'messages': {
                'search': [],
                'sort': [],
                'results': []
            },
            'input_formation': input_formation,
            'roster': roster,
            'pos_symbol': pos_symbol,
            'win_previous': win_previous,
            'pick_formations_page': pick_formations_page}

        # Assign exact position as default position to search for.
        attr_dict['position'] = (input_formation['positions'][pos_symbol]['symbol'], 'exact')

        # Not position dependent - search all.
        if input_formation['name'] == 'Generic':
            settings['pos_search_rg'] = 'red'
            attr_dict.pop('position', None)

    # ========== Window ==========
    win_pick_player = Window()
    win_pick_player.title = pick_player_win_title + ' - ' + pos_symbol
    win_pick_player.auto_position = False
    win_pick_player.position = (window_x, window_y)
    win_pick_player.size = (win_width, win_height)
    win_pick_player.resizable = 0
    win_pick_player.name = pick_player_title + " Window"

    # ========== Window Image View ==========
    class PickPlayerWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = PickPlayerWindowImageView(size=win_pick_player.size)

    # ========== Title ==========
    title = Label(text=pick_player_title + ' - ' + pos_symbol)
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

    # ========== Tool Button Declarations ==========
    attribute_btn = Button("Add Search Attribute")
    sort_btn = Button("Add Sort Attribute")
    reset_btn = Button("Reset Results")

    # ========== Action Button Functions ==========
    def start_btn_func():
        # Search - if no attribute selected, return all
        if len(attr_dict) == 0:
            search_results = db_dict[p_db_radio_group.value][1]
        else:
            search_results = db_dict[p_db_radio_group.value][1].search(attr_dict)
            search_results = PlayerDB.PlayerDB(search_results)

        # Sort - if no attribute selected, use rating
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

        win_pick_player.become_target()

    def back_btn_func():
        win_pick_player.hide()
        win_previous.show()

    # ========== Tool Button Functions ==========
    def attribute_btn_func():
        # Delete results
        del settings['messages']['results'][:]

        # Set type argument
        attr_type = 'player_search'

        # Open new window and close current window
        win_pick_player.hide()
        AddAttribute.open_attribute_window(win_pick_player.x, win_pick_player.y, db_dict,
                                           attr_dict, attr_list, attr_type, settings)

    def sort_btn_func():
        # Delete results
        del settings['messages']['results'][:]

        # Set type argument
        attr_type = 'player_sort'

        # Open new window and close current window
        win_pick_player.hide()
        AddAttribute.open_attribute_window(win_pick_player.x, win_pick_player.y, db_dict,
                                           attr_dict, attr_list, attr_type, settings)

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

        win_pick_player.become_target()

    def create_attribute_messages():
        # ========== Messages ==========
        lowest_msg_l = start_btn.top
        lowest_msg_r = start_btn.top

        attr_msg_offset = 25

        # Attribute Messages
        del settings['messages']['search'][:]
        del settings['messages']['sort'][:]

        if len(attr_dict) > 0:
            settings['messages']['search'].append(
                Label(text="Search Attributes:", font=title_tf_font, width=std_tf_width,
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
                                                      height=std_tf_height, x=reset_btn.right + 3 * attr_msg_offset,
                                                      y=lowest_msg_r, color=title_color))
            lowest_msg_r += std_tf_height

            for value in attr_list:
                attr_label = Label(text=(format_attr_name(value)), font=std_tf_font, width=std_tf_width,
                                   height=std_tf_height, x=reset_btn.right + 3 * attr_msg_offset, y=lowest_msg_r,
                                   color=title_color)
                lowest_msg_r += std_tf_height
                settings['messages']['sort'].append(attr_label)

    create_attribute_messages()

    def player_bio_btn_func(player):
        win_pick_player.hide()
        PlayerBio.open_player_bio_window(win_pick_player.x, win_pick_player.y, player, win_pick_player, db_dict,
                                         db_dict['player_list'][0], db_dict['player_list'][1],
                                         roster, pos_symbol, input_formation, pick_formations_page)
        win_pick_player.become_target()

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

    # ========== Tool Buttons ==========
    attribute_btn.x = (win_width - 3*small_button_width - 2*small_button_spacing) / 2
    attribute_btn.y = start_btn.bottom + 10
    attribute_btn.height = small_button_height
    attribute_btn.width = small_button_width
    attribute_btn.font = small_button_font
    attribute_btn.action = attribute_btn_func
    attribute_btn.style = 'default'
    attribute_btn.color = small_button_color
    attribute_btn.just = 'right'
    general_display.append(attribute_btn)

    sort_btn.x = attribute_btn.right + small_button_spacing
    sort_btn.y = attribute_btn.top
    sort_btn.height = small_button_height
    sort_btn.width = small_button_width
    sort_btn.font = small_button_font
    sort_btn.action = sort_btn_func
    sort_btn.style = 'default'
    sort_btn.color = small_button_color
    sort_btn.just = 'right'
    general_display.append(sort_btn)

    reset_btn.x = sort_btn.right + small_button_spacing
    reset_btn.y = attribute_btn.top
    reset_btn.height = small_button_height
    reset_btn.width = small_button_width
    reset_btn.font = small_button_font
    reset_btn.action = reset_btn_func
    reset_btn.style = 'default'
    reset_btn.color = small_button_color
    reset_btn.just = 'right'
    general_display.append(reset_btn)

    # ========== DB Radio Buttons ==========
    def get_attribute_p_db_rg():
        settings['p_db_rg'] = p_db_radio_group.value
        win_pick_player.become_target()

    def get_attribute_pos_search_rg():
        if settings['pos_search_rg'] != pos_search_radio_group.value:
            button_click = True
        else:
            button_click = False

        settings['pos_search_rg'] = pos_search_radio_group.value

        # If new radio button was clicked, clear position in attribute dictionary.
        if button_click:
            attr_dict.pop('position', None)

        # Add position search terms if position and positionFull and not specified and not searching all players.
        if pos_search_radio_group.value != 'red' and button_click:
            temp_team = Team.Team()
            # Get positions of corresponding relevance
            search_positions_list = temp_team.related_positions(
                input_formation['positions'][pos_symbol]['symbol'], pos_search_radio_group.value)

            # Concatenate strings
            search_positions = ""
            for position in search_positions_list:
                search_positions += position + ', '
            search_positions = search_positions[:-2]
            if len(search_positions) < 1:
                search_positions = 'none'
            attr_dict['position'] = (search_positions, 'exact')

        # Erase current search attributes
        for message in settings['messages']['search']:
            view.remove(message)

        # Create new search attributes
        create_attribute_messages()

        # Display search attributes
        for message in settings['messages']['search']:
            view.add(message)

        win_pick_player.become_target()

    p_db_radio_group = RadioGroup(action=get_attribute_p_db_rg)
    pos_search_radio_group = RadioGroup(action=get_attribute_pos_search_rg)

    # Players DB RG
    db_radio_btn_width = 125
    db_radio_btn_space = 5
    db_msg_width = 70

    p_db_rg_msg = Label(text="Database:", font=std_tf_font, width=db_msg_width,
                        height=std_tf_height, color=title_color)
    p_db_rg_msg.x = (win_pick_player.width - 2*db_radio_btn_width - db_radio_btn_space - db_msg_width) / 2
    p_db_rg_msg.y = reset_btn.bottom + db_radio_btn_space

    player_db_radio_btn = RadioButton(db_dict['player_db'][0])
    player_db_radio_btn.width = db_radio_btn_width
    player_db_radio_btn.x = p_db_rg_msg.right
    player_db_radio_btn.y = p_db_rg_msg.top
    player_db_radio_btn.group = p_db_radio_group
    player_db_radio_btn.value = 'player_db'

    player_list_radio_btn = RadioButton(db_dict['player_list'][0])
    player_list_radio_btn.width = db_radio_btn_width
    player_list_radio_btn.x = player_db_radio_btn.right + db_radio_btn_space
    player_list_radio_btn.y = player_db_radio_btn.top
    player_list_radio_btn.group = p_db_radio_group
    player_list_radio_btn.value = 'player_list'

    p_db_radio_group.value = settings['p_db_rg']

    view.add(p_db_rg_msg)
    view.add(player_db_radio_btn)
    view.add(player_list_radio_btn)

    # Position Search RG
    pos_search_radio_btn_width = 60
    pos_search_msg_width = 140

    pos_search_rg_msg = Label(text="Positions to Search:", font=std_tf_font, width=pos_search_msg_width,
                        height=std_tf_height, color=title_color)
    pos_search_rg_msg.x = (win_pick_player.width-4*pos_search_radio_btn_width-db_radio_btn_space-pos_search_msg_width)/2
    pos_search_rg_msg.y = p_db_rg_msg.bottom + db_radio_btn_space

    pos_search_green_radio_btn = RadioButton("Exact")
    pos_search_green_radio_btn.width = pos_search_radio_btn_width
    pos_search_green_radio_btn.x = pos_search_rg_msg.right
    pos_search_green_radio_btn.y = pos_search_rg_msg.top
    pos_search_green_radio_btn.group = pos_search_radio_group
    pos_search_green_radio_btn.value = 'green'

    pos_search_yellow_radio_btn = RadioButton("Similar")
    pos_search_yellow_radio_btn.width = pos_search_radio_btn_width
    pos_search_yellow_radio_btn.x = pos_search_green_radio_btn.right + db_radio_btn_space
    pos_search_yellow_radio_btn.y = pos_search_green_radio_btn.top
    pos_search_yellow_radio_btn.group = pos_search_radio_group
    pos_search_yellow_radio_btn.value = 'yellow'

    pos_search_orange_radio_btn = RadioButton("Related")
    pos_search_orange_radio_btn.width = pos_search_radio_btn_width
    pos_search_orange_radio_btn.x = pos_search_yellow_radio_btn.right + db_radio_btn_space
    pos_search_orange_radio_btn.y = pos_search_yellow_radio_btn.top
    pos_search_orange_radio_btn.group = pos_search_radio_group
    pos_search_orange_radio_btn.value = 'orange'

    pos_search_red_radio_btn = RadioButton("All")
    pos_search_red_radio_btn.width = pos_search_radio_btn_width
    pos_search_red_radio_btn.x = pos_search_orange_radio_btn.right + db_radio_btn_space
    pos_search_red_radio_btn.y = pos_search_orange_radio_btn.top
    pos_search_red_radio_btn.group = pos_search_radio_group
    pos_search_red_radio_btn.value = 'red'

    pos_search_radio_group.value = settings['pos_search_rg']

    view.add(pos_search_rg_msg)
    view.add(pos_search_green_radio_btn)
    view.add(pos_search_yellow_radio_btn)
    view.add(pos_search_orange_radio_btn)
    view.add(pos_search_red_radio_btn)

    if input_formation['name'] == 'Generic':
        pos_search_green_radio_btn.enabled = 0
        pos_search_yellow_radio_btn.enabled = 0
        pos_search_orange_radio_btn.enabled = 0

    # ========== Sort Order Radio Buttons ==========
    def get_attribute_sort_order_rg():
        settings['order_rg'] = sort_order_radio_group.value
        win_pick_player.become_target()

    sort_order_radio_group = RadioGroup(action=get_attribute_sort_order_rg)

    asc_desc_radio_btn_width = 75
    asc_msg_width = 80
    radio_btn_space = 5

    asc_desc_rg_msg = Label(text="Sort Order:", font=std_tf_font, width=asc_msg_width, height=std_tf_height,
                            color=title_color)
    asc_desc_rg_msg.x = (win_pick_player.width - 2*asc_desc_radio_btn_width - radio_btn_space - asc_msg_width) / 2
    asc_desc_rg_msg.y = pos_search_green_radio_btn.bottom + radio_btn_space
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

    sort_order_radio_group.value = settings['order_rg']

    # ========== Previous, Add to List, Next Buttons ==========
    previous_btn = Button("<<< Previous %d" % num_results)
    add_to_list_btn = Button("")
    next_btn = Button("Next %d >>>" % num_results)
    total_num_results_label = Label()
    pages_label = Label()

    def previous_btn_func(results_list, attributes, index_range):
        # display previous results
        display_players(results_list, attributes, index_range)
        win_pick_player.become_target()

    def next_btn_func(results_list, attributes, index_range):
        # display next results
        display_players(results_list, attributes, index_range)
        win_pick_player.become_target()

    add_to_list_btn.x = attribute_btn.right + small_button_spacing
    add_to_list_btn.y = descend_radio_btn.bottom + 5
    add_to_list_btn.height = tiny_button_height
    add_to_list_btn.width = small_button_width
    add_to_list_btn.font = small_button_font
    add_to_list_btn.style = 'default'
    add_to_list_btn.color = small_button_color
    add_to_list_btn.just = 'right'
    add_to_list_btn.action = win_pick_player.become_target()

    previous_btn.height = tiny_button_height
    previous_btn.width = small_button_width
    previous_btn.x = add_to_list_btn.left - previous_btn.width - small_button_spacing
    previous_btn.y = add_to_list_btn.top
    previous_btn.font = small_button_font
    previous_btn.style = 'default'
    previous_btn.color = small_button_color
    previous_btn.just = 'right'

    next_btn.height = tiny_button_height
    next_btn.width = small_button_width
    next_btn.x = add_to_list_btn.right + small_button_spacing
    next_btn.y = add_to_list_btn.top
    next_btn.font = small_button_font
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
    def display_players(results_list, attributes, index_range):
        # Remove old messages off page
        for message in settings['messages']['results']:
            view.remove(message)
        del settings['messages']['results'][:]

        previous_range = (index_range[0]-num_results, index_range[0])
        previous_btn.action = (previous_btn_func, results_list, attributes, previous_range)

        next_range = (index_range[1], index_range[1]+num_results)
        next_btn.action = (next_btn_func, results_list, attributes, next_range)

        total_num_results_label.text = str(len(results_list.db)) + " Players"
        pages_label.text = "Page %d of %d" % (int(index_range[1]/num_results),
                                              math.ceil(len(results_list.db)/float(num_results)))

        if index_range[0] > 0:
            previous_btn.enabled = 1
        else:
            previous_btn.enabled = 0
        if index_range[1] <= len(results_list.db) - 1:
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
        # Spacing values for each of the stats
        spacing_list = [125, 40, 40, 65, 115, 115, 115, 40]
        # Calculate the maximum number of stat fields that will fit on screen
        max_player_fields = len(spacing_list[:-1]) + (win_pick_player.width - sum(spacing_list[:-1]))/spacing_list[-1]
        # Calculate the left border of the stats based on the number and width of the stats
        left_border = (win_width - sum(spacing_list[:-1]) -
                       (len(labels[:max_player_fields]) - len(spacing_list) + 1) * spacing_list[-1])/2
        msg_x = left_border
        msg_y = add_to_list_btn.bottom + 5

        for info_label in labels[:max_player_fields]:
            player_label = Label(text=info_label, font=std_tf_font_bold, width=spacing_list[stat_index]-5,
                                 height=std_tf_height, x=msg_x, y=msg_y, color=title_color)
            settings['messages']['results'].append(player_label)
            msg_x += spacing_list[stat_index]

            if stat_index < len(spacing_list)-1:
                stat_index += 1

        msg_y += std_tf_height + 5

        # Print out players
        for idx, player in enumerate(results_list.db[index_range[0]:index_range[1]]):
            msg_x = left_border
            player_stats = player_info(player, attributes)
            stat_index = 0

            # Check for names that are too long
            name = player_stats[0]
            if len(name) > 20:
                name = player['lastName']

            bio_btn = Button(title=name, width=spacing_list[stat_index]-5, height=15, x=msg_x, y=msg_y,
                             action=(player_bio_btn_func, player))
            settings['messages']['results'].append(bio_btn)
            msg_x += spacing_list[stat_index]
            stat_index += 1

            for player_stat in player_stats[1:max_player_fields]:
                player_label = Label(text=player_stat, font=small_button_font, width=spacing_list[stat_index]-5,
                                     height=std_tf_height, x=msg_x, y=msg_y, color=title_color)

                settings['messages']['results'].append(player_label)
                msg_x += spacing_list[stat_index]
                if stat_index < len(spacing_list) - 1:
                    stat_index += 1

            msg_y += std_tf_height

        for results_msg in settings['messages']['results']:
            view.add(results_msg)

    # ========== Add components to view and add view to window ==========
    for msg in general_display:
        view.add(msg)
    for msg in settings['messages']['search']:
        view.add(msg)
    for msg in settings['messages']['sort']:
        view.add(msg)
    for msg in settings['messages']['results']:
        view.add(msg)

    win_pick_player.add(view)
    view.become_target()
    win_pick_player.show()
