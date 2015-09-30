from GUI import Button, Label, RadioButton, RadioGroup, TextField, View, Window
from AppConfig import *
import SearchMenu
import json


def open_player_bio_window(window_x, window_y, db_dict, attr_dict, attr_list, settings, player):

    # ========== Window ==========
    win_player_bio = Window()
    win_player_bio.title = player_bio_win_title
    win_player_bio.auto_position = False
    win_player_bio.position = (window_x, window_y)
    win_player_bio.size = (win_width, 450)
    win_player_bio.resizable = 0
    win_player_bio.name = player_bio_title + " Window"
    win_player_bio.show()

    # ========== Window Image View ==========
    class StartWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = StartWindowImageView(size=win_player_bio.size)

    # ========== Title ==========
    title = Label(text=player_bio_title)
    title.font = title_font
    title.width = player_bio_title_width
    title.height = title_height
    title.x = (win_width - player_bio_title_width) / 2
    title.y = top_border
    title.color = title_color

    # ========== Button Declarations ==========
    back_btn = Button("Back")

    # ========== Button Functions ==========
    def back_btn_func():
        SearchMenu.open_search_menu(win_player_bio.x, win_player_bio.y,
                                    db_dict, attr_dict, attr_list, settings)
        win_player_bio.hide()

    # ========== Buttons ==========
    back_btn.x = (win_width - button_width) / 2
    back_btn.y = win_player_bio.height - button_height - button_spacing
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

    win_player_bio.add(view)
    view.become_target()
    win_player_bio.show()
