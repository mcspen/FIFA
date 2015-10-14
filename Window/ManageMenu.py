from GUI import Button,Label, View, Window

from AppConfig import *
import StartMenu
import PickFile
import EnterText
import CreateList
import json


def open_manage_menu(window_x, window_y, db_dict, settings=None):

    general_display_list = []
    lists_display_list = []
    databases_display_list = []
    defaults_display_list = []

    with open('configs.json', 'r') as f:
        default_databases = json.load(f)['default_databases']
        f.close()

    if settings is None:
        settings = {
            'mode': 'lists',
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
    title.x = (win_manage.width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'
    general_display_list.append(title)

    # Subtitle
    subtitle = Label(font=title_font_2, width=title_width, height=title_height,
                     x=(win_manage.width - title_width) / 2,
                     color=title_color, just = 'center')
    general_display_list.append(subtitle)

    # ========== Helper Functions ==========
    def remove_old_display():
        """
        Remove previous displayed items
        """
        if settings['mode'] == 'lists':
            for display_item in lists_display_list:
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
        if settings['mode'] == 'lists':
            subtitle.text = "Current Lists"
            for display_item in lists_display_list:
                view.add(display_item)
        elif settings['mode'] == 'databases':
            subtitle.text = "Current Databases"
            for display_item in databases_display_list:
                view.add(display_item)
        elif settings['mode'] == 'defaults':
            subtitle.text = "Default Files"
            for display_item in defaults_display_list:
                view.add(display_item)
        else:
            print "Settings mode is invalid."

    # ========== Button Toolbar Functions ==========
    def lists_btn_func():
        # Remove previous displayed items
        remove_old_display()

        settings['mode'] = 'lists'

        # Add new display items
        add_new_display()

        for btn in button_list:
            btn.enabled = 1
        lists_btn.enabled = 0

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
        # Remove previous displayed items
        remove_old_display()

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

    # ========== Current Lists Button Functions ==========
    def create_list_btn_func():
        settings['file_type'] = 'create_list'
        CreateList.open_create_list_window(win_manage.x, win_manage.y, db_dict, settings)
        win_manage.hide()

    def player_list_current_btn_func():
        settings['file_type'] = 'current_player_list'
        PickFile.open_pick_file_window(win_manage.x, win_manage.y, db_dict, settings)
        win_manage.hide()

    def formation_list_current_btn_func():
        settings['file_type'] = 'current_formation_list'
        PickFile.open_pick_file_window(win_manage.x, win_manage.y, db_dict, settings)
        win_manage.hide()

    def team_list_current_btn_func():
        settings['file_type'] = 'current_team_list'
        PickFile.open_pick_file_window(win_manage.x, win_manage.y, db_dict, settings)
        win_manage.hide()

    # ========== Current Databases Button Functions ==========
    def download_player_db_btn_func():
        settings['file_type'] = 'download_player_db'
        EnterText.open_enter_text_window(win_manage.x, win_manage.y, db_dict, settings, 'download')
        win_manage.hide()

    def player_db_current_btn_func():
        settings['file_type'] = 'current_player_db'
        PickFile.open_pick_file_window(win_manage.x, win_manage.y, db_dict, settings)
        win_manage.hide()

    def formation_db_current_btn_func():
        settings['file_type'] = 'current_formation_db'
        PickFile.open_pick_file_window(win_manage.x, win_manage.y, db_dict, settings)
        win_manage.hide()

    # ========== Defaults Button Functions ==========
    def player_db_default_btn_func():
        settings['file_type'] = 'default_player_db'
        PickFile.open_pick_file_window(win_manage.x, win_manage.y, db_dict, settings)
        win_manage.hide()

    def player_list_default_btn_func():
        settings['file_type'] = 'default_player_list'
        PickFile.open_pick_file_window(win_manage.x, win_manage.y, db_dict, settings)
        win_manage.hide()

    def formation_db_default_btn_func():
        settings['file_type'] = 'default_formation_db'
        PickFile.open_pick_file_window(win_manage.x, win_manage.y, db_dict, settings)
        win_manage.hide()

    def formation_list_default_btn_func():
        settings['file_type'] = 'default_formation_list'
        PickFile.open_pick_file_window(win_manage.x, win_manage.y, db_dict, settings)
        win_manage.hide()

    def team_list_default_btn_func():
        settings['file_type'] = 'default_team_list'
        PickFile.open_pick_file_window(win_manage.x, win_manage.y, db_dict, settings)
        win_manage.hide()

    # ========== Button Toolbar Declarations ==========
    lists_btn = Button("Lists", height=small_button_height, width=small_button_width,
                       font=small_button_font, action=lists_btn_func, style='default',
                       color=small_button_color, just='center')
    databases_btn = Button("Databases", height=small_button_height, width=small_button_width, font=small_button_font,
                           action=databases_btn_func, style='default', color=small_button_color, just='center')
    defaults_btn = Button("Defaults", height=small_button_height, width=small_button_width, font=small_button_font,
                          action=defaults_btn_func, style='default', color=small_button_color, just='center')
    back_btn = Button("Back", height=small_button_height, width=small_button_width, font=small_button_font,
                      action=back_btn_func, style='default', color=small_button_color, just='center')

    button_list = [lists_btn,
                   databases_btn,
                   defaults_btn,
                   back_btn]

    for button in button_list:
        general_display_list.append(button)

    # ========== Current Lists Button Declarations ==========
    create_list_btn = Button("Create New List", height=small_button_height,
                             width=small_button_width, font=small_button_font,
                             action=create_list_btn_func,
                             style='default', color=small_button_color, just='center')
    lists_display_list.append(create_list_btn)
    player_list_current_btn = Button(db_dict['player_list'][0], height=small_button_height,
                                     width=file_btn_width, font=small_button_font,
                                     action=player_list_current_btn_func,
                                     style='default', color=small_button_color, just='center')
    lists_display_list.append(player_list_current_btn)
    formation_list_current_btn = Button(db_dict['formation_list'][0], height=small_button_height,
                                        width=file_btn_width, font=small_button_font,
                                        action=formation_list_current_btn_func,
                                        style='default', color=small_button_color, just='center')
    lists_display_list.append(formation_list_current_btn)
    team_list_current_btn = Button(db_dict['team_list'][0], height=small_button_height,
                                   width=file_btn_width, font=small_button_font,
                                   action=team_list_current_btn_func,
                                   style='default', color=small_button_color, just='center')
    lists_display_list.append(team_list_current_btn)

    # ========== Current Databases Button Declarations ==========
    download_player_db_btn = Button("Download Player DB", height=small_button_height,
                                    width=small_button_width, font=small_button_font,
                                    action=download_player_db_btn_func,
                                    style='default', color=small_button_color, just='center')
    databases_display_list.append(download_player_db_btn)
    player_db_current_btn = Button(db_dict['player_db'][0], height=small_button_height,
                                   width=file_btn_width, font=small_button_font,
                                   action=player_db_current_btn_func,
                                   style='default', color=small_button_color, just='center')
    databases_display_list.append(player_db_current_btn)
    formation_db_current_btn = Button(db_dict['formation_db'][0], height=small_button_height,
                                      width=file_btn_width, font=small_button_font,
                                      action=formation_db_current_btn_func,
                                      style='default', color=small_button_color, just='center')
    databases_display_list.append(formation_db_current_btn)

    # ========== Defaults Button Declarations ==========
    player_db_default_btn = Button(default_databases['player_db'], height=small_button_height, width=file_btn_width,
                                   font=small_button_font, action=player_db_default_btn_func, style='default',
                                   color=small_button_color, just='center')
    defaults_display_list.append(player_db_default_btn)
    player_list_default_btn = Button(default_databases['player_list'], height=small_button_height,
                                     width=file_btn_width, font=small_button_font,
                                     action=player_list_default_btn_func,
                                     style='default', color=small_button_color, just='center')
    defaults_display_list.append(player_list_default_btn)
    formation_db_default_btn = Button(default_databases['formation_db'], height=small_button_height,
                                      width=file_btn_width, font=small_button_font,
                                      action=formation_db_default_btn_func,
                                      style='default', color=small_button_color, just='center')
    defaults_display_list.append(formation_db_default_btn)
    formation_list_default_btn = Button(default_databases['formation_list'], height=small_button_height,
                                        width=file_btn_width, font=small_button_font,
                                        action=formation_list_default_btn_func,
                                        style='default', color=small_button_color, just='center')
    defaults_display_list.append(formation_list_default_btn)
    team_list_default_btn = Button(default_databases['team_list'], height=small_button_height, width=file_btn_width,
                                   font=small_button_font, action=team_list_default_btn_func,
                                   style='default', color=small_button_color, just='center')
    defaults_display_list.append(team_list_default_btn)

    # ========== Toolbar Buttons ==========
    lists_btn.x = (win_width - len(button_list)*small_button_width - (len(button_list)-1)*small_button_spacing) / 2
    lists_btn.y = title.bottom + small_button_top_spacing
    if settings['mode'] == 'lists':
        lists_btn.enabled = 0

    databases_btn.x = lists_btn.right + small_button_spacing
    databases_btn.y = lists_btn.top
    if settings['mode'] == 'databases':
        databases_btn.enabled = 0

    defaults_btn.x = databases_btn.right + small_button_spacing
    defaults_btn.y = lists_btn.top
    if settings['mode'] == 'defaults':
        defaults_btn.enabled = 0

    back_btn.x = defaults_btn.right + small_button_spacing
    back_btn.y = lists_btn.top

    subtitle.y = lists_btn.bottom + top_border

    # ========== Lists Buttons ========
    lists_file_label_width = 200
    lists_buttons_x = win_width - file_btn_width - (win_width - file_btn_width - lists_file_label_width) / 2

    create_list_btn.x = (win_manage.width - button_width) / 2
    create_list_btn.y = subtitle.bottom + title_border

    player_list_current_btn.x = lists_buttons_x
    player_list_current_btn.y = create_list_btn.bottom + top_border

    formation_list_current_btn.x = lists_buttons_x
    formation_list_current_btn.y = player_list_current_btn.bottom + title_border

    team_list_current_btn.x = lists_buttons_x
    team_list_current_btn.y = formation_list_current_btn.bottom + title_border

    # ========== Databases Buttons ========
    dbs_file_label_width = 200
    dbs_buttons_x = win_width - file_btn_width - (win_width - file_btn_width - dbs_file_label_width) / 2

    download_player_db_btn.x = (win_manage.width - button_width) / 2
    download_player_db_btn.y = subtitle.bottom + title_border

    player_db_current_btn.x = dbs_buttons_x
    player_db_current_btn.y = download_player_db_btn.bottom + top_border

    formation_db_current_btn.x = dbs_buttons_x
    formation_db_current_btn.y = player_db_current_btn.bottom + title_border

    # ========== Defaults Buttons ==========
    default_file_label_width = 200
    default_buttons_x = win_width - file_btn_width - (win_width - file_btn_width - default_file_label_width) / 2

    player_db_default_btn.x = default_buttons_x
    player_db_default_btn.y = subtitle.bottom + title_border

    player_list_default_btn.x = default_buttons_x
    player_list_default_btn.y = player_db_default_btn.bottom + title_border

    formation_db_default_btn.x = default_buttons_x
    formation_db_default_btn.y = player_list_default_btn.bottom + title_border*2

    formation_list_default_btn.x = default_buttons_x
    formation_list_default_btn.y = formation_db_default_btn.bottom + title_border

    team_list_default_btn.x = default_buttons_x
    team_list_default_btn.y = formation_list_default_btn.bottom + title_border*2

    # ========== Lists Labels ==========
    player_list_current_text = "Player List:"
    lists_display_list.append(Label(text=player_list_current_text, font=title_tf_font,
                                    width=lists_file_label_width, height=std_tf_height,
                                    x=player_list_current_btn.left - lists_file_label_width,
                                    y=player_list_current_btn.top + 6, color=title_color))
    formation_list_current_text = "Formation List:"
    lists_display_list.append(Label(text=formation_list_current_text, font=title_tf_font,
                                    width=lists_file_label_width, height=std_tf_height,
                                    x=formation_list_current_btn.left - lists_file_label_width,
                                    y=formation_list_current_btn.top + 6, color=title_color))
    team_list_current_text = "Team List:"
    lists_display_list.append(Label(text=team_list_current_text, font=title_tf_font,
                                    width=lists_file_label_width, height=std_tf_height,
                                    x=team_list_current_btn.left - lists_file_label_width,
                                    y=team_list_current_btn.top + 6, color=title_color))

    # ========== Databases Labels ==========
    player_db_current_text = "Player Database:"
    databases_display_list.append(Label(text=player_db_current_text, font=title_tf_font,
                                        width=dbs_file_label_width, height=std_tf_height,
                                        x=player_list_current_btn.left - lists_file_label_width,
                                        y=player_list_current_btn.top + 6, color=title_color))
    formation_db_current_text = "Formation Database:"
    databases_display_list.append(Label(text=formation_db_current_text, font=title_tf_font,
                                        width=dbs_file_label_width, height=std_tf_height,
                                        x=formation_list_current_btn.left - lists_file_label_width,
                                        y=formation_list_current_btn.top + 6, color=title_color))

    # ========== Default File Labels ==========
    player_db_default_text = "Player Database:"
    defaults_display_list.append(Label(text=player_db_default_text, font=title_tf_font, width=default_file_label_width,
                                       height=std_tf_height, x=player_db_default_btn.left - default_file_label_width,
                                       y=player_db_default_btn.top + 6, color=title_color))
    player_list_default_text = "Player List:"
    defaults_display_list.append(Label(text=player_list_default_text, font=title_tf_font,
                                       width=default_file_label_width, height=std_tf_height,
                                       x=player_list_default_btn.left - default_file_label_width,
                                       y=player_list_default_btn.top + 6, color=title_color))
    formation_db_default_text = "Formation Database:"
    defaults_display_list.append(Label(text=formation_db_default_text, font=title_tf_font,
                                       width=default_file_label_width, height=std_tf_height,
                                       x=formation_db_default_btn.left - default_file_label_width,
                                       y=formation_db_default_btn.top + 6, color=title_color))
    formation_list_default_text = "Formation List:"
    defaults_display_list.append(Label(text=formation_list_default_text, font=title_tf_font,
                                       width=default_file_label_width, height=std_tf_height,
                                       x=formation_list_default_btn.left - default_file_label_width,
                                       y=formation_list_default_btn.top + 6, color=title_color))
    team_list_default_text = "Team List:"
    defaults_display_list.append(Label(text=team_list_default_text, font=title_tf_font, width=default_file_label_width,
                                       height=std_tf_height, x=team_list_default_btn.left - default_file_label_width,
                                       y=team_list_default_btn.top + 6, color=title_color))

    # ========== Add components to view and add view to window ==========
    for item in general_display_list:
        view.add(item)

    add_new_display()

    win_manage.add(view)
    view.become_target()
    win_manage.show()
