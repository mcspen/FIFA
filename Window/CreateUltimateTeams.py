from GUI import Button, Label, RadioButton, RadioGroup, TextField, View, Window

from AppConfig import *
import TeamsMenu
import json


def open_create_ultimate_teams_window(window_x, window_y, db_dict):

    display_items = []

    # Get create ultimate team configuration values
    with open('ultimate_team_configs.json', 'r') as f:
        settings = json.load(f)
        f.close()

    # ========== Window ==========
    win_ultimate_teams = Window()
    win_ultimate_teams.title = create_ultimate_teams_win_title
    win_ultimate_teams.auto_position = False
    win_ultimate_teams.position = (window_x, window_y)
    win_ultimate_teams.size = (win_width, win_height)
    win_ultimate_teams.resizable = 0
    win_ultimate_teams.name = create_ultimate_teams_title + " Window"

    # ========== Window Image View ==========
    class FormationsWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = FormationsWindowImageView(size=win_ultimate_teams.size)

    # ========== Title ==========
    title = Label(text=create_ultimate_teams_title)
    title.font = title_font
    title.width = title_width
    title.height = title_height
    title.x = (win_width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'
    display_items.append(title)

    # ========== Settings ==========
    # ========== Current player list and formation list ==========
    file_name_width = 400
    player_list_label = Label(text="Player List: " + db_dict['player_list'][0], font=std_tf_font_bold,
                              width=file_name_width, height=std_tf_height,
                              x=(win_width - file_name_width)/2, y=title.bottom + title_border*3,
                              color=title_color, just='center')
    display_items.append(player_list_label)

    formation_list_label = Label(text="Formation List: " + db_dict['formation_list'][0], font=std_tf_font_bold,
                                 width=file_name_width, height=std_tf_height,
                                 x=(win_width - file_name_width)/2, y=player_list_label.bottom + title_border,
                                 color=title_color, just='center')
    display_items.append(formation_list_label)

    settings_indent = 3*win_width/7

    # ========== Team name ==========
    tf_width = 235
    team_name_label_width = 130
    disabled_msg = "Disabled"


    team_list_name_label = Label(text="Team List Name: ", font=std_tf_font_bold,
                                 width=team_name_label_width, height=std_tf_height,
                                 x=settings_indent - team_name_label_width,
                                 y=formation_list_label.bottom + title_border*4,
                                 color=title_color, just='right')
    display_items.append(team_list_name_label)

    team_list_name_tf = TextField(font=std_tf_font, width=tf_width, height=std_tf_height + 5,
                                  x=team_list_name_label.right + small_button_spacing, y=team_list_name_label.top)
    display_items.append(team_list_name_tf)

    radio_btn_width = 75
    radio_btn_space = 5

    # ========== Process Type Label ==========
    process_type_label = Label(text="Processing Type: ", font=std_tf_font_bold,
                               width=std_tf_width, height=std_tf_height,
                               x=settings_indent - std_tf_width,
                               y=team_list_name_label.bottom + title_border,
                               color=title_color, just='right')
    display_items.append(process_type_label)

    def get_process_type_rg():
        settings['process_type'] = process_type_radio_group.value
        win_ultimate_teams.become_target()

    process_type_radio_group = RadioGroup(action=get_process_type_rg)

    # Process Type Radio Buttons
    multi_process_radio_btn = RadioButton('Multi', width=radio_btn_width,
                                          x=process_type_label.right + radio_btn_space,
                                          y=process_type_label.top, group=process_type_radio_group, value='multi')
    display_items.append(multi_process_radio_btn)

    single_process_radio_btn = RadioButton('Single', width=radio_btn_width,
                                           x=multi_process_radio_btn.right + radio_btn_space,
                                           y=process_type_label.top, group=process_type_radio_group, value='single')
    display_items.append(single_process_radio_btn)

    process_type_radio_group.value = settings['process_type']

    # ========== Judging Teams Label ==========
    judging_teams_label = Label(text="How to Judge Teams: ", font=std_tf_font_bold,
                                       width=std_tf_width, height=std_tf_height,
                                       x=settings_indent - std_tf_width,
                                       y=process_type_label.bottom + title_border,
                                       color=title_color, just='right')
    display_items.append(judging_teams_label)

    judging_teams_attributes = Label(font=std_tf_font,
                                       width=std_tf_width, height=std_tf_height,
                                       x=judging_teams_label.right + radio_btn_space,
                                       y=judging_teams_label.top,
                                       color=title_color, just='left')
    judging_teams_attributes_text = ''
    for attr in settings['sort_attributes']:
        judging_teams_attributes_text += attr + ', '
    judging_teams_attributes.text = judging_teams_attributes_text[:-2]
    display_items.append(judging_teams_attributes)

    # Judging Teams Edit Button
    def judging_edit_btn_func():
        win_ultimate_teams.hide()

    judging_edit_btn_width = 40
    judging_edit_btn = Button("Edit",
                              #x=teams_to_return_tf.right - judging_edit_btn_width,
                              x=judging_teams_attributes.right,
                              y=judging_teams_label.top,
                              height=small_button_height-7, width=judging_edit_btn_width,
                              font=small_button_font, action=judging_edit_btn_func, style = 'default',
                              color=button_color, just='right')
    display_items.append(judging_edit_btn)

    # ========== Limits Label ==========
    limits_label = Label(text="Limitations", font=title_font_3,
                                       width=std_tf_width, height=title_height-25,
                                       x=(win_ultimate_teams.width - std_tf_width)/2,
                                       y=judging_teams_label.bottom + title_border*5,
                                       color=title_color, just='center')
    display_items.append(limits_label)

    # ========== Players per Position Label ==========
    players_per_pos_tf = TextField(font=std_tf_font, width=tf_width, height=std_tf_height + 5)

    def players_per_pos_btn_func():
        if not settings['players_per_position'][0]:
            settings['players_per_position'][0] = True
            players_per_pos_tf.value = str(settings['players_per_position'][1])
            players_per_pos_tf.enabled = 1

        else:
            # Get value from text field and assign to settings
            if str.isdigit(players_per_pos_tf.value):
                settings['players_per_position'][1] = int(players_per_pos_tf.value)

            settings['players_per_position'][0] = False
            players_per_pos_tf.value = disabled_msg
            players_per_pos_tf.enabled = 0

        win_ultimate_teams.become_target()

    players_per_pos_btn = Button(title="Players per Position", font=std_tf_font_bold,
                                 width=std_tf_width, height=std_tf_height,
                                 x=settings_indent - std_tf_width,
                                 y=limits_label.bottom + title_border,
                                 action=players_per_pos_btn_func,
                                 color=title_color, just='right')
    display_items.append(players_per_pos_btn)

    players_per_pos_tf.x = players_per_pos_btn.right + radio_btn_space
    players_per_pos_tf.y = players_per_pos_btn.top
    display_items.append(players_per_pos_tf)

    # Disable based on settings
    if not settings['players_per_position'][0]:
        players_per_pos_tf.value = disabled_msg
        players_per_pos_tf.enabled = 0
    else:
        players_per_pos_tf.value = str(settings['players_per_position'][1])

    # ========== Max Teams per Formation Label ==========
    teams_per_formation_tf = TextField(font=std_tf_font, width=tf_width, height=std_tf_height + 5)

    def teams_per_formation_btn_func():
        if not settings['teams_per_formation'][0]:
            settings['teams_per_formation'][0] = True
            teams_per_formation_tf.value = str(settings['teams_per_formation'][1])
            teams_per_formation_tf.enabled = 1

        else:
            # Get value from text field and assign to settings
            if str.isdigit(teams_per_formation_tf.value):
                settings['teams_per_formation'][1] = int(teams_per_formation_tf.value)

            settings['teams_per_formation'][0] = False
            teams_per_formation_tf.value = disabled_msg
            teams_per_formation_tf.enabled = 0

        win_ultimate_teams.become_target()

    teams_per_formation_btn = Button(title="Max Teams per Formation", font=std_tf_font_bold,
                                     width=std_tf_width, height=std_tf_height,
                                     x=settings_indent - std_tf_width,
                                     y=players_per_pos_btn.bottom + title_border,
                                     action=teams_per_formation_btn_func,
                                     color=title_color, just='right')
    display_items.append(teams_per_formation_btn)

    teams_per_formation_tf.x = teams_per_formation_btn.right + radio_btn_space
    teams_per_formation_tf.y = teams_per_formation_btn.top
    display_items.append(teams_per_formation_tf)

    # Disable based on settings
    if not settings['teams_per_formation'][0]:
        teams_per_formation_tf.value = disabled_msg
        teams_per_formation_tf.enabled = 0
    else:
        teams_per_formation_tf.value = str(settings['teams_per_formation'][1])

    # ========== Max Teams to Return Label ==========
    teams_to_return_tf = TextField(font=std_tf_font, width=tf_width, height=std_tf_height + 5)

    def teams_to_return_btn_func():
        if not settings['num_teams_returned'][0]:
            settings['num_teams_returned'][0] = True
            teams_to_return_tf.value = str(settings['num_teams_returned'][1])
            teams_to_return_tf.enabled = 1

        else:
            # Get value from text field and assign to settings
            if str.isdigit(teams_to_return_tf.value):
                settings['num_teams_returned'][1] = int(teams_to_return_tf.value)

            settings['num_teams_returned'][0] = False
            teams_to_return_tf.value = disabled_msg
            teams_to_return_tf.enabled = 0

        win_ultimate_teams.become_target()

    teams_to_return_btn = Button(title="Max Teams to Return", font=std_tf_font_bold,
                                 width=std_tf_width, height=std_tf_height,
                                 x=settings_indent - std_tf_width,
                                 y=teams_per_formation_btn.bottom + title_border,
                                 action=teams_to_return_btn_func,
                                 color=title_color, just='right')
    display_items.append(teams_to_return_btn)

    teams_to_return_tf.x = teams_to_return_btn.right + radio_btn_space
    teams_to_return_tf.y = teams_to_return_btn.top
    display_items.append(teams_to_return_tf)

    # Disable based on settings
    if not settings['num_teams_returned'][0]:
        teams_to_return_tf.value = disabled_msg
        teams_to_return_tf.enabled = 0
    else:
        teams_to_return_tf.value = str(settings['num_teams_returned'][1])

    # ========== Time Limit Label ==========
    time_limit_tf = TextField(font=std_tf_font, width=tf_width, height=std_tf_height + 5)

    def time_limit_btn_func():
        if not settings['time_limit'][0]:
            settings['time_limit'][0] = True

            time_limit_val = 0.0
            if settings['time_limit'][2] == 'days':
                time_limit_val = settings['time_limit'][1] / 86400.0
            elif settings['time_limit'][2] == 'hours':
                time_limit_val = settings['time_limit'][1] / 3600.0
            if settings['time_limit'][2] == 'minutes':
                time_limit_val = settings['time_limit'][1] / 60.0
            time_limit_tf.value = str(time_limit_val)

            time_limit_tf.enabled = 1
            days_time_limit_radio_btn.enabled = 1
            hours_time_limit_radio_btn.enabled = 1
            minutes_time_limit_radio_btn.enabled = 1
            time_limit_radio_group.enabled = 1

        else:
            # Get value from text field, convert to seconds, and assign to settings
            try:
                if settings['time_limit'][2] == 'days':
                    settings['time_limit'][1] = float(time_limit_tf.value) * 86400.0
                elif settings['time_limit'][2] == 'hours':
                    settings['time_limit'][1] = float(time_limit_tf.value) * 3600.0
                elif settings['time_limit'][2] == 'minutes':
                    settings['time_limit'][1] = float(time_limit_tf.value) * 60.0
            except ValueError:
                print "Invalid time limit."

            settings['time_limit'][0] = False
            time_limit_tf.value = disabled_msg
            time_limit_tf.enabled = 0
            days_time_limit_radio_btn.enabled = 0
            hours_time_limit_radio_btn.enabled = 0
            minutes_time_limit_radio_btn.enabled = 0
            time_limit_radio_group.enabled = 0

        win_ultimate_teams.become_target()

    time_limit_btn = Button(title="Time Limit", font=std_tf_font_bold,
                            width=std_tf_width, height=std_tf_height,
                            x=settings_indent - std_tf_width,
                            y=teams_to_return_btn.bottom + title_border,
                            action=time_limit_btn_func,
                            color=title_color, just='right')
    display_items.append(time_limit_btn)

    def get_time_limit_rg():
        # Get value from text field, convert to seconds, and assign to settings
        if time_limit_tf.value == '':
            time_limit_tf.value = '0'
        else:
            try:
                if settings['time_limit'][2] == 'days':
                    settings['time_limit'][1] = float(time_limit_tf.value) * 86400.0
                elif settings['time_limit'][2] == 'hours':
                    settings['time_limit'][1] = float(time_limit_tf.value) * 3600.0
                elif settings['time_limit'][2] == 'minutes':
                    settings['time_limit'][1] = float(time_limit_tf.value) * 60.0
            except ValueError:
                print "Invalid time limit."

        # Get new time limit units
        settings['time_limit'][2] = time_limit_radio_group.value

        time_limit_val = 0.0
        if settings['time_limit'][2] == 'days':
            time_limit_val = settings['time_limit'][1] / 86400.0
        elif settings['time_limit'][2] == 'hours':
            time_limit_val = settings['time_limit'][1] / 3600.0
        elif settings['time_limit'][2] == 'minutes':
            time_limit_val = settings['time_limit'][1] / 60.0
        time_limit_tf.value = str(time_limit_val)

        win_ultimate_teams.become_target()

    time_limit_radio_group = RadioGroup(action=get_time_limit_rg)

    # Max Teams to Return Radio Buttons
    days_time_limit_radio_btn = RadioButton('Days', width=radio_btn_width,
                                            x=time_limit_btn.right + radio_btn_space,
                                            y=time_limit_btn.bottom + title_border,
                                            group=time_limit_radio_group, value='days')
    display_items.append(days_time_limit_radio_btn)

    hours_time_limit_radio_btn = RadioButton('Hours', width=radio_btn_width,
                                             x=days_time_limit_radio_btn.right + radio_btn_space,
                                             y=days_time_limit_radio_btn.top,
                                             group=time_limit_radio_group, value='hours')
    display_items.append(hours_time_limit_radio_btn)

    minutes_time_limit_radio_btn = RadioButton('Minutes', width=radio_btn_width,
                                               x=hours_time_limit_radio_btn.right + radio_btn_space,
                                               y=days_time_limit_radio_btn.top,
                                               group=time_limit_radio_group, value='minutes')
    display_items.append(minutes_time_limit_radio_btn)

    time_limit_radio_group.value = settings['time_limit'][2]

    time_limit_tf.x = time_limit_btn.right + radio_btn_space
    time_limit_tf.y = time_limit_btn.top
    display_items.append(time_limit_tf)

    # Disable based on settings
    if not settings['time_limit'][0]:
        time_limit_tf.value = disabled_msg
        time_limit_tf.enabled = 0
        days_time_limit_radio_btn.enabled = 0
        hours_time_limit_radio_btn.enabled = 0
        minutes_time_limit_radio_btn.enabled = 0
        time_limit_radio_group.enabled = 0
    else:
        time_limit_value = 0.0
        if settings['time_limit'][2] == 'days':
            time_limit_value = settings['time_limit'][1] / 86400.0
        elif settings['time_limit'][2] == 'hours':
            time_limit_value = settings['time_limit'][1] / 3600.0
        elif settings['time_limit'][2] == 'minutes':
            time_limit_value = settings['time_limit'][1] / 60.0
        time_limit_tf.value = str(time_limit_value)

    # ========== Button Declarations ==========
    start_btn = Button("Start")
    back_btn = Button("Back")

    # ========== Button Functions ==========
    def save_settings():
        """
        Save the ultimate team creation configuration settings
        """

        # Get the values from the text fields
        # Players per position
        if str.isdigit(players_per_pos_tf.value):
                settings['players_per_position'][1] = int(players_per_pos_tf.value)
        # Teams per formation
        if str.isdigit(teams_per_formation_tf.value):
                settings['teams_per_formation'][1] = int(teams_per_formation_tf.value)
        # Number of teams returned
        if str.isdigit(teams_to_return_tf.value):
                settings['num_teams_returned'][1] = int(teams_to_return_tf.value)
        # Time limit
        if time_limit_tf.value != disabled_msg:
            try:
                if settings['time_limit'][2] == 'days':
                    settings['time_limit'][1] = float(time_limit_tf.value) * 86400.0
                elif settings['time_limit'][2] == 'hours':
                    settings['time_limit'][1] = float(time_limit_tf.value) * 3600.0
                elif settings['time_limit'][2] == 'minutes':
                    settings['time_limit'][1] = float(time_limit_tf.value) * 60.0
            except ValueError:
                print "Invalid time limit."

        # Save the settings
        with open('ultimate_team_configs.json', 'w') as config_file:
            json.dump(settings, config_file)
            config_file.close()

    def start_btn_func():
        save_settings()
        win_ultimate_teams.hide()

    def back_btn_func():
        save_settings()
        TeamsMenu.open_teams_menu(win_ultimate_teams.x, win_ultimate_teams.y, db_dict)
        win_ultimate_teams.hide()

    # ========== Buttons ==========
    start_btn.x = (win_width - 2*button_width - button_spacing) / 2
    start_btn.y = win_ultimate_teams.height - 100
    start_btn.height = button_height
    start_btn.width = button_width
    start_btn.font = button_font
    start_btn.action = start_btn_func
    start_btn.style = 'default'
    start_btn.color = button_color
    start_btn.just = 'right'
    display_items.append(start_btn)

    back_btn.x = start_btn.right + button_spacing
    back_btn.y = start_btn.top
    back_btn.height = button_height
    back_btn.width = button_width
    back_btn.font = button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = button_color
    back_btn.just = 'right'
    display_items.append(back_btn)

    # ========== Add components to view and add view to window ==========
    for item in display_items:
        view.add(item)

    win_ultimate_teams.add(view)
    view.become_target()
    win_ultimate_teams.show()
