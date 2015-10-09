from GUI import Button, Label, RadioButton, RadioGroup, TextField, View, Window
from AppConfig import *
import PickFile
import json
from os import rename


def open_enter_text_window(window_x, window_y, db_dict, settings, box_type, fill_text='', file_prefix=''):

    if box_type == 'rename':
        title = 'Rename File'
        old_file_name = fill_text
        message_text = 'Enter new file name.'
    else:
        title = 'Enter Text'
        message_text = 'Enter text.'

    # ========== Window ==========
    win_enter_text = Window()
    win_enter_text.title = title
    win_enter_text.auto_position = False
    win_enter_text.position = (window_x+100, window_y+100)
    win_enter_text.size = (win_width-200, win_height-400)
    win_enter_text.resizable = 0
    win_enter_text.name = title + " Window"
    win_enter_text.show()

    # ========== Window Image View ==========
    class StartWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = StartWindowImageView(size=win_enter_text.size)

    # ========== Title ==========
    title = Label(text=title)
    title.font = title_font
    title.width = title_width
    title.height = title_height
    title.x = (win_enter_text.width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'

    # ========== Message Label ==========
    message = Label(font=title_font_2, width=win_enter_text.width - 50, height=title_height,
                    x=25, y=title.bottom + top_border, color=title_color, just='center')
    message.text = message_text

    # ========== Button Declarations ==========
    enter_btn = Button("Enter")
    back_btn = Button("Back")

    # ========== Button Functions ==========
    def enter_btn_func():
        # Rename file
        if box_type == 'rename':

            # Get new name
            new_file_name = value_tf.value

            if len(new_file_name) > 0:

                try:
                    # Rename file
                    rename('JSONs/' + file_prefix + old_file_name + '.json',
                           'JSONs/' + file_prefix + new_file_name + '.json')

                    # Disable pick file back button in case the selected file has changed
                    settings['file_changes'] = True

                    PickFile.open_pick_file_window(window_x, window_y, db_dict, settings)
                    win_enter_text.hide()

                except OSError as err:
                    message.text = "File already exists."

            else:
                message.text = "File name must be at least 1 character."

    def back_btn_func():
        PickFile.open_pick_file_window(window_x, window_y, db_dict, settings)
        win_enter_text.hide()

    # ========== Buttons ==========
    enter_btn.x = (win_enter_text.width - 2*button_width - button_spacing) / 2
    enter_btn.y = win_enter_text.height - 70
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
    value_tf.x = (win_enter_text.width - value_tf.width) / 2
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

    win_enter_text.add(view)
    view.become_target()
    win_enter_text.show()
