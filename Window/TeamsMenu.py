from GUI import Button, Label, View, Window

from AppConfig import *
import StartMenu


def open_teams_menu(window_x, window_y, db_dict):

    # ========== Window ==========
    win_teams = Window()
    win_teams.title = teams_win_title
    win_teams.auto_position = False
    win_teams.position = (window_x, window_y)
    win_teams.size = (win_width, win_height)
    win_teams.resizable = 0
    win_teams.name = "Teams Window"

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
    back_btn = Button("Back")

    search_teams_btn = Button("Search Teams")
    create_team_btn = Button("Create Team")
    create_teams_list_btn = Button("Create Teams List")
    load_teams_list_btn = Button("Load Teams List")
    save_teams_list_btn = Button("Save Teams List")
    edit_formations_list_btn = Button("Edit Teams List")
    delete_formations_list_btn = Button("Delete Teams List")

    # ========== Button Functions ==========
    def back_btn_func():
        StartMenu.open_start_menu(win_teams.x, win_teams.y, db_dict)
        win_teams.hide()

    # ========== Buttons ==========
    back_btn.x = (win_width - button_width) / 2
    back_btn.y = title.bottom
    back_btn.height = button_height
    back_btn.width = button_width
    back_btn.font = button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = button_color
    back_btn.just = 'right'

    # ========== Add components to view and add view to window ==========
    view.add(title)
    view.add(back_btn)

    win_teams.add(view)
    view.become_target()
    win_teams.show()
