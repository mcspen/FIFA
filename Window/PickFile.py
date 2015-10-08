from GUI import Button, Label, RadioButton, RadioGroup, TextField, View, Window
from AppConfig import *
import ManageMenu
from Logic.HelperFunctions import format_attr_name
import json


def open_pick_file_window(window_x, window_y, db_dict, settings):

    # ========== Window ==========
    win_file = Window()
    win_file.title = file_win_title
    win_file.auto_position = False
    win_file.position = (window_x, window_y)
    win_file.size = (win_width, 400)
    win_file.resizable = 0
    win_file.name = file_title + " Window"
    win_file.show()

    # ========== Window Image View ==========
    class StartWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = StartWindowImageView(size=win_file.size)

    display_list = []

    # ========== Title ==========
    title = Label(text=file_title)
    title.font = title_font
    title.width = title_width
    title.height = title_height
    title.x = (win_width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'
    display_list.append(title)

    # ========== Button Declarations ==========
    back_btn = Button("Back")

    def back_btn_func():
        ManageMenu.open_manage_menu(win_file.x, win_file.y, db_dict, settings)
        win_file.hide()

    # ========== Buttons ==========
    back_btn.x = (win_width - button_width) / 2
    back_btn.y = win_file.height - 70
    back_btn.height = button_height
    back_btn.width = button_width
    back_btn.font = button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = button_color
    back_btn.just = 'right'
    display_list.append(back_btn)

    # ========== Add buttons to window ==========
    view.add(title)
    view.add(back_btn)


    win_file.add(view)
    view.become_target()
    win_file.show()
