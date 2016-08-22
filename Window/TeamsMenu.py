from GUI import Button, Label, View, Window

from AppConfig import *
import StartMenu
import CreateUltimateTeams
import PickFormation


def open_teams_menu(window_x, window_y, db_dict):

    # ========== Window ==========
    win_teams = Window()
    win_teams.title = teams_win_title
    win_teams.auto_position = False
    win_teams.position = (window_x, window_y)
    win_teams.size = (win_width, win_height)
    win_teams.resizable = 0
    win_teams.name = teams_title + " Window"

    # ========== Window Image View ==========
    class FormationsWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = FormationsWindowImageView(size=win_teams.size)

    # ========== Title ==========
    title = Label(text=teams_title)
    title.font = title_font
    title.width = title_width
    title.height = title_height
    title.x = (win_width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'

    # ========== Button Declarations ==========
    create_ultimate_teams_btn = Button("Generate Ultimate Teams")
    manually_create_teams_btn = Button("Build Ultimate Teams")
    back_btn = Button("Back")

    # ========== Button Functions ==========
    def create_ultimate_teams_btn_func():
        win_teams.become_target()
        CreateUltimateTeams.open_create_ultimate_teams_window(win_teams.x, win_teams.y, db_dict, win_teams)
        win_teams.hide()

    def manually_create_teams_btn_func():
        win_teams.become_target()
        PickFormation.open_pick_formation_window(win_teams.x, win_teams.y, db_dict, win_teams)
        win_teams.hide()

    def back_btn_func():
        win_teams.become_target()
        StartMenu.open_start_menu(win_teams.x, win_teams.y, db_dict)
        win_teams.hide()

    # ========== Buttons ==========
    create_ultimate_teams_btn.x = (win_width - file_btn_width) / 2
    create_ultimate_teams_btn.y = title.bottom + top_border
    create_ultimate_teams_btn.height = button_height
    create_ultimate_teams_btn.width = file_btn_width
    create_ultimate_teams_btn.font = button_font
    create_ultimate_teams_btn.action = create_ultimate_teams_btn_func
    create_ultimate_teams_btn.style = 'default'
    create_ultimate_teams_btn.color = button_color
    create_ultimate_teams_btn.just = 'right'

    manually_create_teams_btn.x = (win_width - file_btn_width) / 2
    manually_create_teams_btn.y = create_ultimate_teams_btn.bottom + top_border
    manually_create_teams_btn.height = button_height
    manually_create_teams_btn.width = file_btn_width
    manually_create_teams_btn.font = button_font
    manually_create_teams_btn.action = manually_create_teams_btn_func
    manually_create_teams_btn.style = 'default'
    manually_create_teams_btn.color = button_color
    manually_create_teams_btn.just = 'right'

    back_btn.x = (win_width - button_width) / 2
    back_btn.y = manually_create_teams_btn.bottom + top_border*2
    back_btn.height = button_height
    back_btn.width = button_width
    back_btn.font = button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = button_color
    back_btn.just = 'right'

    # ========== Add components to view and add view to window ==========
    view.add(title)
    view.add(create_ultimate_teams_btn)
    view.add(manually_create_teams_btn)
    view.add(back_btn)

    win_teams.add(view)
    view.become_target()
    win_teams.show()
