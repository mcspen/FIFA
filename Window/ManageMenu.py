from GUI import Button, Label, View, Window

from AppConfig import *
import StartMenu
import PickFile
import json


def open_manage_menu(window_x, window_y, db_dict, settings=None):

    general_display_list = []
    players_list_display_list = []
    formations_list_display_list = []
    teams_list_display_list = []
    databases_display_list = []
    defaults_display_list = []

    with open('configs.json', 'r') as f:
        default_databases = json.load(f)['default_databases']
        f.close()

    if settings is None:
        settings = {
            'mode': 'players_list',
            'file_changes': False
        }

    # ========== Window ==========
    win_manage = Window()
    win_manage.title = manage_win_title
    win_manage.auto_position = False
    win_manage.position = (window_x, window_y)
    win_manage.size = (win_width, win_height)
    win_manage.resizable = 0
    win_manage.name = "Manage Files Window"

    # ========== Window Image View ==========
    class FormationsWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = FormationsWindowImageView(size=win_manage.size)

    # ========== Title ==========
    title = Label(text=manage_title)
    title.font = title_font
    title.width = title_width
    title.height = title_height
    title.x = (win_width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'
    general_display_list.append(title)

    # ========== Helper Functions ==========
    def remove_old_display():
        """
        Remove previous displayed items
        """
        if settings['mode'] == 'players_list':
            for display_item in players_list_display_list:
                view.remove(display_item)
        elif settings['mode'] == 'formations_list':
            for display_item in formations_list_display_list:
                view.remove(display_item)
        elif settings['mode'] == 'teams_list':
            for display_item in teams_list_display_list:
                view.remove(display_item)
        elif settings['mode'] == 'databases':
            for display_item in databases_display_list:
                view.remove(display_item)
        elif settings['mode'] == 'defaults':
            for display_item in defaults_display_list:
                view.remove(display_item)
        else:
            print "Settings mode is invalid."

    def add_new_display():
        """
        Remove previous displayed items
        """
        if settings['mode'] == 'players_list':
            for display_item in players_list_display_list:
                view.add(display_item)
        elif settings['mode'] == 'formations_list':
            for display_item in formations_list_display_list:
                view.add(display_item)
        elif settings['mode'] == 'teams_list':
            for display_item in teams_list_display_list:
                view.add(display_item)
        elif settings['mode'] == 'databases':
            for display_item in databases_display_list:
                view.add(display_item)
        elif settings['mode'] == 'defaults':
            for display_item in defaults_display_list:
                view.add(display_item)
        else:
            print "Settings mode is invalid."

    # ========== Button Toolbar Functions ==========
    def players_list_btn_func():
        # Remove previous displayed items
        remove_old_display()

        settings['mode'] = 'players_list'

        # Add new display items
        add_new_display()

        for btn in button_list:
            btn.enabled = 1
        players_list_btn.enabled = 0

        win_manage.become_target()

    def formations_list_btn_func():
        # Remove previous displayed items
        remove_old_display()

        settings['mode'] = 'formations_list'

        # Add new display items
        add_new_display()

        for btn in button_list:
            btn.enabled = 1
        formations_list_btn.enabled = 0

        win_manage.become_target()

    def teams_list_btn_func():
        # Remove previous displayed items
        remove_old_display()

        settings['mode'] = 'teams_list'

        # Add new display items
        add_new_display()

        for btn in button_list:
            btn.enabled = 1
        teams_list_btn.enabled = 0

        win_manage.become_target()

    def databases_btn_func():
        # Remove previous displayed items
        remove_old_display()

        settings['mode'] = 'databases'

        # Add new display items
        add_new_display()

        for btn in button_list:
            btn.enabled = 1
        databases_btn.enabled = 0

        win_manage.become_target()

    def defaults_btn_func():
        settings['mode'] = 'defaults'

        # Add new display items
        add_new_display()

        for btn in button_list:
            btn.enabled = 1
        defaults_btn.enabled = 0

        win_manage.become_target()

    def back_btn_func():
        StartMenu.open_start_menu(win_manage.x, win_manage.y, db_dict)
        win_manage.hide()

    # ========== Defaults Button Functions ==========
    def players_db_default_btn_func():
        settings['file_type'] = 'default_player_db'
        PickFile.open_pick_file_window(win_manage.x, win_manage.y, db_dict, settings)
        win_manage.hide()

    def players_list_default_btn_func():
        settings['file_type'] = 'default_player_list'
        PickFile.open_pick_file_window(win_manage.x, win_manage.y, db_dict, settings)
        win_manage.hide()

    def formations_db_default_btn_func():
        settings['file_type'] = 'default_formation_db'
        PickFile.open_pick_file_window(win_manage.x, win_manage.y, db_dict, settings)
        win_manage.hide()

    def formations_list_default_btn_func():
        settings['file_type'] = 'default_formation_list'
        PickFile.open_pick_file_window(win_manage.x, win_manage.y, db_dict, settings)
        win_manage.hide()

    def teams_list_default_btn_func():
        settings['file_type'] = 'default_team_list'
        PickFile.open_pick_file_window(win_manage.x, win_manage.y, db_dict, settings)
        win_manage.hide()

    # ========== Button Toolbar Declarations ==========
    players_list_btn = Button("Players List", height=small_button_height, width=small_button_width,
                              font=small_button_font, action=players_list_btn_func, style='default',
                              color=small_button_color, just='center')
    formations_list_btn = Button("Formations List", height=small_button_height, width=small_button_width,
                                 font=small_button_font, action=formations_list_btn_func, style='default',
                                 color=small_button_color, just='center')
    teams_list_btn = Button("Teams List", height=small_button_height, width=small_button_width, font=small_button_font,
                            action=teams_list_btn_func, style='default', color=small_button_color, just='center')
    databases_btn = Button("Databases", height=small_button_height, width=small_button_width, font=small_button_font,
                           action=databases_btn_func, style='default', color=small_button_color, just='center')
    defaults_btn = Button("Defaults", height=small_button_height, width=small_button_width, font=small_button_font,
                          action=defaults_btn_func, style='default', color=small_button_color, just='center')
    back_btn = Button("Back", height=small_button_height, width=small_button_width, font=small_button_font,
                      action=back_btn_func, style='default', color=small_button_color, just='center')

    button_list = [players_list_btn,
                   formations_list_btn,
                   teams_list_btn,
                   databases_btn,
                   defaults_btn,
                   back_btn]

    for button in button_list:
        general_display_list.append(button)

    # ========== Defaults Button Declarations ==========
    players_db_default_btn = Button(default_databases['player_db'], height=small_button_height, width=file_btn_width,
                                    font=small_button_font, action=players_db_default_btn_func, style='default',
                                    color=small_button_color, just='center')
    defaults_display_list.append(players_db_default_btn)
    players_list_default_btn = Button(default_databases['player_list'], height=small_button_height,
                                      width=file_btn_width, font=small_button_font,
                                      action=players_list_default_btn_func,
                                      style='default', color=small_button_color, just='center')
    defaults_display_list.append(players_list_default_btn)
    formations_db_default_btn = Button(default_databases['formation_db'], height=small_button_height,
                                       width=file_btn_width, font=small_button_font,
                                       action=formations_db_default_btn_func,
                                       style='default', color=small_button_color, just='center')
    defaults_display_list.append(formations_db_default_btn)
    formations_list_default_btn = Button(default_databases['formation_list'], height=small_button_height,
                                         width=file_btn_width, font=small_button_font,
                                         action=formations_list_default_btn_func,
                                         style='default', color=small_button_color, just='center')
    defaults_display_list.append(formations_list_default_btn)
    teams_list_default_btn = Button(default_databases['team_list'], height=small_button_height, width=file_btn_width,
                                    font=small_button_font, action=teams_list_default_btn_func,
                                    style='default', color=small_button_color, just='center')
    defaults_display_list.append(teams_list_default_btn)

    # ========== Toolbar Buttons ==========
    players_list_btn.x = (win_width - len(button_list)*small_button_width
                          - (len(button_list)-1)*small_button_spacing) / 2
    players_list_btn.y = title.bottom + small_button_top_spacing
    if settings['mode'] == 'players_list':
        players_list_btn.enabled = 0

    formations_list_btn.x = players_list_btn.right + small_button_spacing
    formations_list_btn.y = players_list_btn.top
    if settings['mode'] == 'formations_list':
        formations_list_btn.enabled = 0

    teams_list_btn.x = formations_list_btn.right + small_button_spacing
    teams_list_btn.y = players_list_btn.top
    if settings['mode'] == 'teams_list':
        teams_list_btn.enabled = 0

    databases_btn.x = teams_list_btn.right + small_button_spacing
    databases_btn.y = players_list_btn.top
    if settings['mode'] == 'databases':
        databases_btn.enabled = 0

    defaults_btn.x = databases_btn.right + small_button_spacing
    defaults_btn.y = players_list_btn.top
    if settings['mode'] == 'defaults':
        defaults_btn.enabled = 0

    back_btn.x = defaults_btn.right + small_button_spacing
    back_btn.y = players_list_btn.top

    # ========== Defaults Buttons ==========
    default_file_label_width = 240
    default_buttons_x = win_width - file_btn_width - (win_width - file_btn_width - default_file_label_width) / 2

    players_db_default_btn.x = default_buttons_x
    players_db_default_btn.y = players_list_btn.bottom + top_border*2

    players_list_default_btn.x = default_buttons_x
    players_list_default_btn.y = players_db_default_btn.bottom + title_border

    formations_db_default_btn.x = default_buttons_x
    formations_db_default_btn.y = players_list_default_btn.bottom + title_border

    formations_list_default_btn.x = default_buttons_x
    formations_list_default_btn.y = formations_db_default_btn.bottom + title_border

    teams_list_default_btn.x = default_buttons_x
    teams_list_default_btn.y = formations_list_default_btn.bottom + title_border

    # ========== Default File Labels ==========
    player_db_default_text = "Default Player Database:"
    defaults_display_list.append(Label(text=player_db_default_text, font=title_tf_font, width=default_file_label_width,
                                       height=std_tf_height, x=players_db_default_btn.left - default_file_label_width,
                                       y=players_db_default_btn.top + 6, color=title_color))
    player_list_default_text = "Default Player List:"
    defaults_display_list.append(Label(text=player_list_default_text, font=title_tf_font,
                                       width=default_file_label_width, height=std_tf_height,
                                       x=players_list_default_btn.left - default_file_label_width,
                                       y=players_list_default_btn.top + 6, color=title_color))
    formation_db_default_text = "Default Formation Database:"
    defaults_display_list.append(Label(text=formation_db_default_text, font=title_tf_font,
                                       width=default_file_label_width, height=std_tf_height,
                                       x=formations_db_default_btn.left - default_file_label_width,
                                       y=formations_db_default_btn.top + 6, color=title_color))
    formation_list_default_text = "Default Formation List:"
    defaults_display_list.append(Label(text=formation_list_default_text, font=title_tf_font,
                                       width=default_file_label_width, height=std_tf_height,
                                       x=formations_list_default_btn.left - default_file_label_width,
                                       y=formations_list_default_btn.top + 6, color=title_color))
    team_list_default_text = "Default Team List:"
    defaults_display_list.append(Label(text=team_list_default_text, font=title_tf_font, width=default_file_label_width,
                                       height=std_tf_height, x=teams_list_default_btn.left - default_file_label_width,
                                       y=teams_list_default_btn.top + 6, color=title_color))

    # ========== Add components to view and add view to window ==========
    for item in general_display_list:
        view.add(item)

    add_new_display()

    win_manage.add(view)
    view.become_target()
    win_manage.show()
