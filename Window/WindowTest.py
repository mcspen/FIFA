from GUI import Button, Label, View, Window

from AppConfig import *
import StartMenu


def open_test_window(window_x, window_y, player_db, formation_db, player_list, formation_list, team_list):

    # ========== Window ==========
    win_test = Window()
    win_test.title = 'Test Window'
    win_test.auto_position = False
    win_test.position = (window_x, window_y)
    win_test.size = (win_width, 150)
    win_test.resizable = 0
    win_test.name = "Test Window"
    win_test.show()

    # ========== Window Image View ==========
    class StartWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = StartWindowImageView(size=win_test.size)

    # ========== Title ==========
    title = Label(text="Test Window - Go Back!")
    title.font = title_font
    title.width = 350
    title.height = title_height
    title.x = (win_width - 350) / 2
    title.y = top_border
    title.color = title_color

    # ========== Button Declarations ==========
    back_btn = Button("Back")

    # ========== Button Functions ==========
    def back_btn_func():
        StartMenu.open_start_menu(win_test.left, win_test.top,
                                  player_db, formation_db, player_list, formation_list, team_list)
        win_test.hide()

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

    # ========== Add buttons to window ==========
    view.add(title)
    view.add(back_btn)

    win_test.add(view)
    view.become_target()
    win_test.show()
