from GUI import Button, Label, RadioButton, RadioGroup, TextField, View, Window

from AppConfig import *
import StartMenu
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
                              x=(win_width - file_name_width)/2, y=title.bottom + title_border,
                              color=title_color, just='center')
    display_items.append(player_list_label)

    formation_list_label = Label(text="Formation List: " + db_dict['formation_list'][0], font=std_tf_font_bold,
                                 width=file_name_width, height=std_tf_height,
                                 x=(win_width - file_name_width)/2, y=player_list_label.bottom + title_border,
                                 color=title_color, just='center')
    display_items.append(formation_list_label)

    settings_indent = 2*win_width/5

    # ========== Team name ==========
    team_name_tf_width = 225
    team_name_label_width = 130
    team_list_name_label = Label(text="Team List Name: ", font=std_tf_font_bold,
                                 width=team_name_label_width, height=std_tf_height,
                                 x=settings_indent - team_name_label_width,
                                 y=formation_list_label.bottom + top_border,
                                 color=title_color, just='right')
    display_items.append(team_list_name_label)

    team_list_name_tf = TextField(font=std_tf_font, width=team_name_tf_width, height=std_tf_height + 5,
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

    # ========== Players per Position Label ==========
    players_per_pos_tf = TextField(font=std_tf_font, width=radio_btn_width, height=std_tf_height + 5)

    players_per_pos_label = Label(text="Players per Position: ", font=std_tf_font_bold,
                                       width=std_tf_width, height=std_tf_height,
                                       x=settings_indent - std_tf_width,
                                       y=process_type_label.bottom + title_border,
                                       color=title_color, just='right')
    display_items.append(players_per_pos_label)

    def get_players_per_pos_rg():
        if players_per_pos_radio_group.value == -1:
            settings['players_per_position'] = players_per_pos_radio_group.value
        else:
            settings['players_per_position'] = int(players_per_pos_tf.value)
        win_ultimate_teams.become_target()

    players_per_pos_radio_group = RadioGroup(action=get_players_per_pos_rg)

    # Players per Position Radio Buttons
    all_players_radio_btn = RadioButton('All', width=radio_btn_width,
                                        x=players_per_pos_label.right + radio_btn_space,
                                        y=players_per_pos_label.top, group=players_per_pos_radio_group, value=-1)
    display_items.append(all_players_radio_btn)

    specify_players_radio_btn = RadioButton('Specify: ', width=radio_btn_width,
                                            x=all_players_radio_btn.right + radio_btn_space,
                                            y=players_per_pos_label.top, group=players_per_pos_radio_group, value=-2)
    display_items.append(specify_players_radio_btn)

    if settings['players_per_position'] == -1:
        players_per_pos_radio_group.value = settings['players_per_position']
    else:
        players_per_pos_tf.value = str(settings['players_per_position'])
        players_per_pos_radio_group.value = -2

    players_per_pos_tf.x = specify_players_radio_btn.right + radio_btn_space
    players_per_pos_tf.y = players_per_pos_label.top
    display_items.append(players_per_pos_tf)

    # ========== Max Teams per Formation Label ==========
    teams_per_formation_tf = TextField(font=std_tf_font, width=radio_btn_width, height=std_tf_height + 5)

    teams_per_formation_label = Label(text="Max Teams per Formation: ", font=std_tf_font_bold,
                                       width=std_tf_width, height=std_tf_height,
                                       x=settings_indent - std_tf_width,
                                       y=players_per_pos_label.bottom + title_border,
                                       color=title_color, just='right')
    display_items.append(teams_per_formation_label)

    def get_teams_per_formation_rg():
        if teams_per_formation_radio_group.value == -1:
            settings['teams_per_formation'] = teams_per_formation_radio_group.value
        else:
            settings['teams_per_formation'] = int(teams_per_formation_tf.value)
        win_ultimate_teams.become_target()

    teams_per_formation_radio_group = RadioGroup(action=get_teams_per_formation_rg)

    # Max Teams per Formation Radio Buttons
    all_teams_per_formation_radio_btn = RadioButton('All', width=radio_btn_width,
                                        x=teams_per_formation_label.right + radio_btn_space,
                                        y=teams_per_formation_label.top,
                                        group=teams_per_formation_radio_group, value=-1)
    display_items.append(all_teams_per_formation_radio_btn)

    specify_teams_per_formation_radio_btn = RadioButton('Specify: ', width=radio_btn_width,
                                            x=all_players_radio_btn.right + radio_btn_space,
                                            y=teams_per_formation_label.top,
                                            group=teams_per_formation_radio_group, value=-2)
    display_items.append(specify_teams_per_formation_radio_btn)

    if settings['teams_per_formation'] == -1:
        teams_per_formation_radio_group.value = settings['teams_per_formation']
    else:
        teams_per_formation_tf.value = str(settings['teams_per_formation'])
        teams_per_formation_radio_group.value = -2

    teams_per_formation_tf.x = specify_teams_per_formation_radio_btn.right + radio_btn_space
    teams_per_formation_tf.y = teams_per_formation_label.top
    display_items.append(teams_per_formation_tf)

    # ========== Max Teams to Return Label ==========
    teams_to_return_tf = TextField(font=std_tf_font, width=radio_btn_width, height=std_tf_height + 5)

    teams_to_return_label = Label(text="Max Teams to Return: ", font=std_tf_font_bold,
                                       width=std_tf_width, height=std_tf_height,
                                       x=settings_indent - std_tf_width,
                                       y=teams_per_formation_label.bottom + title_border,
                                       color=title_color, just='right')
    display_items.append(teams_to_return_label)

    def get_teams_to_return_rg():
        if teams_to_return_radio_group.value == -1:
            settings['num_teams_returned'] = teams_to_return_radio_group.value
        else:
            settings['num_teams_returned'] = int(teams_to_return_tf.value)
        win_ultimate_teams.become_target()

    teams_to_return_radio_group = RadioGroup(action=get_teams_to_return_rg)

    # Max Teams to Return Radio Buttons
    max_teams_to_return_radio_btn = RadioButton('1000', width=radio_btn_width,
                                        x=teams_to_return_label.right + radio_btn_space,
                                        y=teams_to_return_label.top,
                                        group=teams_to_return_radio_group, value=1000)
    display_items.append(max_teams_to_return_radio_btn)

    specify_teams_to_return_radio_btn = RadioButton('Specify: ', width=radio_btn_width,
                                            x=max_teams_to_return_radio_btn.right + radio_btn_space,
                                            y=teams_to_return_label.top,
                                            group=teams_to_return_radio_group, value=-2)
    display_items.append(specify_teams_to_return_radio_btn)

    if settings['num_teams_returned'] >= 1000:
        teams_to_return_radio_group.value = 1000
    else:
        teams_to_return_tf.value = str(settings['num_teams_returned'])
        teams_to_return_radio_group.value = -2

    teams_to_return_tf.x = specify_teams_to_return_radio_btn.right + radio_btn_space
    teams_to_return_tf.y = teams_to_return_label.top
    display_items.append(teams_to_return_tf)

    # ========== Judging Teams Label ==========
    judging_teams_label = Label(text="How to Judge Teams: ", font=std_tf_font_bold,
                                       width=std_tf_width, height=std_tf_height,
                                       x=settings_indent - std_tf_width,
                                       y=teams_to_return_label.bottom + title_border,
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
    judging_edit_btn = Button("Edit", x=teams_to_return_tf.right - judging_edit_btn_width, y=judging_teams_label.top,
                              height=small_button_height-7, width=judging_edit_btn_width,
                              font=small_button_font, action=judging_edit_btn_func, style = 'default',
                              color=button_color, just='right')
    display_items.append(judging_edit_btn)

    # ========== Time Limit Label ==========
    time_limit_tf = TextField(font=std_tf_font, width=radio_btn_width, height=std_tf_height + 5)

    time_limit_label = Label(text="Time Limit: ", font=std_tf_font_bold,
                                       width=std_tf_width, height=std_tf_height,
                                       x=settings_indent - std_tf_width,
                                       y=judging_teams_label.bottom + title_border,
                                       color=title_color, just='right')
    display_items.append(time_limit_label)

    def get_time_limit_rg():
        if time_limit_radio_group.value == -1:
            settings['time_limit'] = time_limit_radio_group.value
        else:
            settings['time_limit'] = int(time_limit_tf.value)
        win_ultimate_teams.become_target()

    time_limit_radio_group = RadioGroup(action=get_time_limit_rg)

    # Max Teams to Return Radio Buttons
    days_time_limit_radio_btn = RadioButton('Days', width=radio_btn_width,
                                        x=time_limit_label.right + radio_btn_space,
                                        y=time_limit_label.top,
                                        group=time_limit_radio_group, value=-1)
    display_items.append(days_time_limit_radio_btn)

    hours_time_limit_radio_btn = RadioButton('Hours', width=radio_btn_width,
                                            x=days_time_limit_radio_btn.right + radio_btn_space,
                                            y=time_limit_label.top,
                                            group=time_limit_radio_group, value=-2)
    display_items.append(hours_time_limit_radio_btn)

    minutes_time_limit_radio_btn = RadioButton('Minutes', width=radio_btn_width,
                                            x=hours_time_limit_radio_btn.right + radio_btn_space,
                                            y=time_limit_label.top,
                                            group=time_limit_radio_group, value=-3)
    display_items.append(minutes_time_limit_radio_btn)

    if settings['time_limit'] >= 1000:
        time_limit_radio_group.value = 1000
    else:
        time_limit_tf.value = str(settings['time_limit'])
        time_limit_radio_group.value = -2

    time_limit_tf.x = minutes_time_limit_radio_btn.right + radio_btn_space
    time_limit_tf.y = time_limit_label.top
    display_items.append(time_limit_tf)

    # ========== Button Declarations ==========
    start_btn = Button("Start")
    back_btn = Button("Back")

    # ========== Button Functions ==========
    def start_btn_func():
        win_ultimate_teams.hide()

    def back_btn_func():
        StartMenu.open_start_menu(win_ultimate_teams.x, win_ultimate_teams.y, db_dict)
        win_ultimate_teams.hide()

    # ========== Buttons ==========
    start_btn.x = (win_width - 2*button_width - button_spacing) / 2
    start_btn.y = win_ultimate_teams.height - 75
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
