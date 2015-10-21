from GUI import Button, Label, View, Window

from AppConfig import *
import StartMenu


def open_create_ultimate_teams_window(window_x, window_y, db_dict):

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

    # ========== Button Declarations ==========
    back_btn = Button("Back")

    # ========== Button Functions ==========

    def back_btn_func():
        StartMenu.open_start_menu(win_ultimate_teams.x, win_ultimate_teams.y, db_dict)
        win_ultimate_teams.hide()

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

    win_ultimate_teams.add(view)
    view.become_target()
    win_ultimate_teams.show()
