from GUI import Button, Label, TextField, View, Window
from AppConfig import *
import ManageMenu
from Logic.PlayerDB import PlayerDB
from os import rename
from os.path import isfile
from shutil import copyfile
import multiprocessing


def open_create_list_window(window_x, window_y, db_dict, settings):

    fill_text = 'Temp Fill'
    message_text = 'Temp Message'

    # ========== Window ==========
    win_create_list = Window()
    win_create_list.title = create_list_win_title
    win_create_list.auto_position = False
    win_create_list.position = (window_x+100, window_y+100)
    win_create_list.size = (win_width-200, win_height-400)
    win_create_list.resizable = 0
    win_create_list.name = create_list_title + " Window"
    win_create_list.show()

    # ========== Window Image View ==========
    class StartWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = StartWindowImageView(size=win_create_list.size)

    # ========== Title ==========
    title = Label(text=create_list_title)
    title.font = title_font
    title.width = title_width
    title.height = title_height
    title.x = (win_create_list.width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'

    # ========== Message Label ==========
    message = Label(font=title_font_2, width=win_create_list.width - 50, height=title_height,
                    x=25, y=title.bottom + top_border, color=title_color, just='center')
    message.text = message_text

    # ========== Button Declarations ==========
    enter_btn = Button("Enter")
    back_btn = Button("Back")

    # ========== Button Functions ==========
    def enter_btn_func():
        stuff = 0

    def back_btn_func():
        ManageMenu.open_manage_menu(window_x, window_y, db_dict, settings)
        win_create_list.hide()

    # ========== Buttons ==========
    enter_btn.x = (win_create_list.width - 2*button_width - button_spacing) / 2
    enter_btn.y = win_create_list.height - 70
    enter_btn.height = button_height
    enter_btn.width = button_width
    enter_btn.font = button_font
    enter_btn.action = enter_btn_func
    enter_btn.style = 'default'
    enter_btn.color = button_color
    enter_btn.just = 'right'

    back_btn.x = enter_btn.right + button_spacing
    back_btn.y = enter_btn.top
    back_btn.height = button_height
    back_btn.width = button_width
    back_btn.font = button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = button_color
    back_btn.just = 'right'

    # ========== Value Textfield ==========
    value_tf = TextField()
    value_tf.width = 200
    value_tf.x = (win_create_list.width - value_tf.width) / 2
    value_tf.y = enter_btn.top - 50
    value_tf.height = 25
    value_tf.font = std_tf_font
    value_tf.value = fill_text

    # ========== Add buttons to window ==========
    view.add(title)
    view.add(message)
    view.add(value_tf)
    view.add(enter_btn)
    view.add(back_btn)

    win_create_list.add(view)
    view.become_target()
    win_create_list.show()
