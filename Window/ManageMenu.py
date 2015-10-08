from GUI import Button, Label, View, Window

from AppConfig import *
import StartMenu
import json


def open_manage_menu(window_x, window_y, db_dict, settings=None):

    with open('configs.json', 'r') as f:
        default_search = json.load(f)['default_search']
        f.close()

    if settings is None:
        settings = {
            'mode': 'players_list'
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

    display_list = []

    # ========== Title ==========
    title = Label(text=manage_title)
    title.font = title_font
    title.width = title_width
    title.height = title_height
    title.x = (win_width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'
    display_list.append(title)

    # ========== Button Toolbar Functions ==========
    def players_list_btn_func():
        settings['mode'] = 'players_list'

        for btn in button_list:
            btn.enabled = 1
        players_list_btn.enabled = 0

        win_manage.become_target()

    def formations_list_btn_func():
        settings['mode'] = 'formations_list'

        for btn in button_list:
            btn.enabled = 1
        formations_list_btn.enabled = 0

        win_manage.become_target()

    def teams_list_btn_func():
        settings['mode'] = 'teams_list'

        for btn in button_list:
            btn.enabled = 1
        teams_list_btn.enabled = 0

        win_manage.become_target()

    def databases_btn_func():
        settings['mode'] = 'databases'

        for btn in button_list:
            btn.enabled = 1
        databases_btn.enabled = 0

        win_manage.become_target()

    def defaults_btn_func():
        settings['mode'] = 'defaults'

        for btn in button_list:
            btn.enabled = 1
        defaults_btn.enabled = 0

        win_manage.become_target()

    def back_btn_func():
        StartMenu.open_start_menu(win_manage.x, win_manage.y, db_dict)
        win_manage.hide()

    # ========== Defaults Button Functions ==========
    def players_db_default_btn_func():
        win_manage.become_target()

    def players_list_default_btn_func():
        win_manage.become_target()

    def formations_db_default_btn_func():
        win_manage.become_target()

    def formations_list_default_btn_func():
        win_manage.become_target()

    def teams_list_default_btn_func():
        win_manage.become_target()

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
        display_list.append(button)

    # ========== Defaults Button Declarations ==========
    players_db_default_btn = Button("Select Default", height=small_button_height, width=small_button_width,
                                    font=small_button_font, action=players_db_default_btn_func, style='default',
                                    color=small_button_color, just='center')
    display_list.append(players_db_default_btn)
    players_list_default_btn = Button("Select Default", height=small_button_height,
                                      width=small_button_width, font=small_button_font,
                                      action=players_list_default_btn_func,
                                      style='default', color=small_button_color, just='center')
    display_list.append(players_list_default_btn)
    formations_db_default_btn = Button("Select Default", height=small_button_height,
                                       width=small_button_width, font=small_button_font,
                                       action=formations_db_default_btn_func,
                                       style='default', color=small_button_color, just='center')
    display_list.append(formations_db_default_btn)
    formations_list_default_btn = Button("Select Default", height=small_button_height,
                                         width=small_button_width, font=small_button_font,
                                         action=formations_list_default_btn_func,
                                         style='default', color=small_button_color, just='center')
    display_list.append(formations_list_default_btn)
    teams_list_default_btn = Button("Select Default", height=small_button_height, width=small_button_width,
                                    font=small_button_font, action=teams_list_default_btn_func,
                                    style='default', color=small_button_color, just='center')
    display_list.append(teams_list_default_btn)

    # ========== Toolbar Buttons ==========
    players_list_btn.x = (win_width - len(button_list)*small_button_width
                          - (len(button_list)-1)*small_button_spacing) / 2
    players_list_btn.y = title.bottom + small_button_top_spacing
    if settings['mode'] == 'players_list':
        defaults_btn.enabled = 0

    formations_list_btn.x = players_list_btn.right + small_button_spacing
    formations_list_btn.y = players_list_btn.top
    if settings['mode'] == 'formations_list':
        defaults_btn.enabled = 0

    teams_list_btn.x = formations_list_btn.right + small_button_spacing
    teams_list_btn.y = players_list_btn.top
    if settings['mode'] == 'teams_list':
        defaults_btn.enabled = 0

    databases_btn.x = teams_list_btn.right + small_button_spacing
    databases_btn.y = players_list_btn.top
    if settings['mode'] == 'databases':
        defaults_btn.enabled = 0

    defaults_btn.x = databases_btn.right + small_button_spacing
    defaults_btn.y = players_list_btn.top
    if settings['mode'] == 'defaults':
        defaults_btn.enabled = 0

    back_btn.x = defaults_btn.right + small_button_spacing
    back_btn.y = players_list_btn.top

    # ========== Defaults Buttons ==========
    players_db_default_btn.x = win_width / 4 - small_button_width/2
    players_db_default_btn.y = players_list_btn.bottom + top_border*2

    players_list_default_btn.x = win_width / 4 - small_button_width/2
    players_list_default_btn.y = players_db_default_btn.bottom + title_border

    formations_db_default_btn.x = win_width / 4 - small_button_width/2
    formations_db_default_btn.y = players_list_default_btn.bottom + title_border

    formations_list_default_btn.x = win_width / 4 - small_button_width/2
    formations_list_default_btn.y = formations_db_default_btn.bottom + title_border

    teams_list_default_btn.x = win_width / 4 - small_button_width/2
    teams_list_default_btn.y = formations_list_default_btn.bottom + title_border

    # ========== Add components to view and add view to window ==========
    for item in display_list:
        view.add(item)

    win_manage.add(view)
    view.become_target()
    win_manage.show()
