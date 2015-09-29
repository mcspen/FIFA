from GUI import Button, Label, RadioButton, RadioGroup, View, Window
import unicodedata
from AppConfig import *
import StartMenu
import AddAttribute
from Logic import PlayerDB
from Logic import FormationDB
from Logic import TeamDB


def open_search_menu(window_x, window_y, db_dict, attr_dict=None, attr_list=None, settings=None):

    if attr_dict is None:
        attr_dict = {}

    if attr_list is None:
        attr_list = []

    if settings is None:
        settings = {
            'mode': 'players',
            'p_db_rg': 'all_players',
            'f_db_rg': 'all_formations',
            'precision_rg': 'higher',
            'order_rg': True
        }

    # ========== Window ==========
    win_search = Window()
    win_search.title = win_search_title
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
    title.width = search_title_width
    title.height = title_height
    title.x = (win_width - search_title_width) / 2
    title.y = top_border
    title.color = title_color

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
            search_results = db_dict[p_db_radio_group.value][1].search(attr_dict, precision_radio_group.value)
            search_results = PlayerDB.PlayerDB(search_results)
            search_results.sort(attr_list, sort_order_radio_group.value)
            search_results.print_compare_info(10)

            display_players(search_results, 0)

        # Start button corresponds to formations
        elif settings['mode'] == 'formations':
            search_results = db_dict[f_db_radio_group.value][1].search(attr_dict, precision_radio_group.value)
            search_results = FormationDB.FormationDB(search_results)
            search_results.sort(attr_list, sort_order_radio_group.value)
            search_results.print_db_short()

        # Start button corresponds to teams
        elif settings['mode'] == 'teams':
            stuff = 0

    def back_btn_func():
        StartMenu.open_start_menu(win_search.x, win_search.y, db_dict)
        win_search.hide()

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

    # ========== Tool Button Functions ==========
    def attribute_btn_func():
        AddAttribute.open_attribute_window(win_search.x, win_search.y,
                                           db_dict, attr_dict, attr_list, 'search', settings)
        win_search.hide()

    def sort_btn_func():
        AddAttribute.open_attribute_window(win_search.x, win_search.y, db_dict,
                                           attr_dict, attr_list, 'sort', settings)
        win_search.hide()

    def reset_btn_func():
        # Remove messages off page
        for message in search_messages:
            view.remove(message)
        for message in sort_messages:
            view.remove(message)
        for message in players_displayed:
            view.remove(message)

        # Delete the attribute parameters for search and sort
        attr_dict.clear()
        del attr_list[:]
        del players_displayed[:]

        # Disable start button
        start_btn.enabled = 0

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

    def get_attribute_f_db_rg():
        settings['f_db_rg'] = f_db_radio_group.value

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

    # ========== Precision Radio Buttons ==========
    def get_attribute_precision_rg():
        settings['precision_rg'] = precision_radio_group.value

    precision_radio_group = RadioGroup(action=get_attribute_precision_rg)

    radio_btn_width = 60
    radio_btn_space = 5
    pre_msg_width = 120

    precision_rg_msg =Label(text=("Search Compare:"), font=std_tf_font, width=pre_msg_width, height=std_tf_height,
                            color=title_color)
    precision_rg_msg.x = (win_search.width - 3*radio_btn_width - 2*radio_btn_space - pre_msg_width) / 2
    precision_rg_msg.y = rg_1_bottom + radio_btn_space

    higher_radio_btn = RadioButton("Higher")
    higher_radio_btn.width = radio_btn_width
    higher_radio_btn.x = precision_rg_msg.right
    higher_radio_btn.y = precision_rg_msg.top
    higher_radio_btn.group = precision_radio_group
    higher_radio_btn.value = 'higher'

    exact_radio_btn = RadioButton("Exact")
    exact_radio_btn.width = radio_btn_width
    exact_radio_btn.x = higher_radio_btn.right + radio_btn_space
    exact_radio_btn.y = higher_radio_btn.top
    exact_radio_btn.group = precision_radio_group
    exact_radio_btn.value = 'exact'

    lower_radio_btn = RadioButton("Lower")
    lower_radio_btn.width = radio_btn_width
    lower_radio_btn.x = exact_radio_btn.right + radio_btn_space
    lower_radio_btn.y = higher_radio_btn.top
    lower_radio_btn.group = precision_radio_group
    lower_radio_btn.value = 'lower'

    precision_radio_group.value = settings['precision_rg']

    # ========== Precision Radio Buttons ==========
    def get_attribute_sort_order_rg():
        settings['order_rg'] = sort_order_radio_group.value

    sort_order_radio_group = RadioGroup(action=get_attribute_sort_order_rg)

    asc_desc_radio_btn_width = 75
    asc_msg_width = 80

    asc_desc_rg_msg =Label(text=("Sort Order:"), font=std_tf_font, width=asc_msg_width, height=std_tf_height,
                           color=title_color)
    asc_desc_rg_msg.x = (win_search.width - 2*asc_desc_radio_btn_width - radio_btn_space - asc_msg_width) / 2
    asc_desc_rg_msg.y = higher_radio_btn.bottom + radio_btn_space

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

    attr_msg_offset = 50

    search_messages = []
    sort_messages = []

    # Attribute Messages
    if len(attr_dict) > 0:
        search_messages.append(Label(text=("Search Attributes:"), font=title_tf_font, width=std_tf_width,
                               height=std_tf_height, x=attr_msg_offset, y=lowest_msg_l, color=title_color))
        lowest_msg_l += std_tf_height

        for key, value in attr_dict.iteritems():
            attr_label = Label(text=(key + ": " + str(value)), font=std_tf_font, width=std_tf_width,
                               height=std_tf_height, x=attr_msg_offset, y=lowest_msg_l, color=title_color)
            lowest_msg_l += std_tf_height
            search_messages.append(attr_label)

        for message in search_messages:
            view.add(message)
        win_search.add(view)

    if len(attr_list) > 0:
        sort_messages.append(Label(text=("Sort Attributes:"), font=title_tf_font, width=std_tf_width,
                                   height=std_tf_height, x=teams_btn.right + attr_msg_offset, y=lowest_msg_r,
                                   color=title_color))
        lowest_msg_r += std_tf_height

        for value in attr_list:
            attr_label = Label(text=(str(value)), font=std_tf_font, width=std_tf_width, height=std_tf_height,
                               x=teams_btn.right + attr_msg_offset, y=lowest_msg_r, color=title_color)
            lowest_msg_r += std_tf_height
            sort_messages.append(attr_label)

        for message in sort_messages:
            view.add(message)
        win_search.add(view)

    # Disable start button if no search or sort parameters
    if len(attr_dict) == 0 and len(attr_list) == 0:
        start_btn.enabled = 0
    else:
        start_btn.enabled = 1

    # Display players from search
    players_displayed = []

    def display_players(display_player_db, start_index):
        # Remove messages off page
        for message in players_displayed:
            view.remove(message)
        del players_displayed[:]

        msg_y = ascend_radio_btn.bottom + start_message_border

        for player in display_player_db.db[start_index:start_index+20]:
            player_name = unicodedata.normalize('NFKD', player['firstName']).encode('ascii', 'ignore') + ' ' + \
                          unicodedata.normalize('NFKD', player['lastName']).encode('ascii', 'ignore')
            player_text = player_name
            player_label = Label(text=player_text, font=std_tf_font, width=200,
                               height=std_tf_height, x=100, y=msg_y, color=title_color)
            msg_y += std_tf_height
            players_displayed.append(player_label)

        for label in players_displayed:
            view.add(label)
        win_search.add(view)

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

    view.add(higher_radio_btn)
    view.add(exact_radio_btn)
    view.add(lower_radio_btn)
    view.add(precision_rg_msg)
    view.add(descend_radio_btn)
    view.add(ascend_radio_btn)
    view.add(asc_desc_rg_msg)

    win_search.add(view)
    view.become_target()
    win_search.show()
