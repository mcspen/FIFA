from GUI import Button, Label, TextField, View, Window
from AppConfig import *
import PickFile
from os import remove


def open_confirm_prompt_window(window_x, window_y, db_dict, settings, file_path, file_name):

    # ========== Window ==========
    win_confirm_prompt = Window()
    win_confirm_prompt.title = confirm_prompt_win_title
    win_confirm_prompt.auto_position = False
    win_confirm_prompt.position = (window_x+100, window_y+100)
    win_confirm_prompt.size = (win_width-200, win_height-400)
    win_confirm_prompt.resizable = 0
    win_confirm_prompt.name = confirm_prompt_title + " Window"
    win_confirm_prompt.show()

    # ========== Window Image View ==========
    class StartWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = StartWindowImageView(size=win_confirm_prompt.size)

    # ========== Title ==========
    title = Label(text=confirm_prompt_title)
    title.font = title_font
    title.width = title_width
    title.height = title_height
    title.x = (win_confirm_prompt.width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'

    # ========== Message Label ==========
    message = Label(font=title_font_2, width=win_confirm_prompt.width - 50, height=title_height,
                    x=25, y=title.bottom + top_border, color=title_color, just='center')
    message.text = "Delete \"%s\"?" % file_name

    # ========== Button Declarations ==========
    yes_btn = Button("Yes")
    cancel_btn = Button("Cancel")

    # ========== Button Functions ==========
    def yes_btn_func():

        # Disable back button in case the selected file has changed
        settings['file_changes'] = True

        # Delete file
        try:
            remove(file_path)

        except Exception as err:
            message.text = "Error: " + err.args[1]

        PickFile.open_pick_file_window(window_x, window_y, db_dict, settings)
        win_confirm_prompt.hide()

    def cancel_btn_func():
        PickFile.open_pick_file_window(window_x, window_y, db_dict, settings)
        win_confirm_prompt.hide()

    # ========== Buttons ==========
    yes_btn.x = (win_confirm_prompt.width - 2*button_width - button_spacing) / 2
    yes_btn.y = win_confirm_prompt.height - 70
    yes_btn.height = button_height
    yes_btn.width = button_width
    yes_btn.font = button_font
    yes_btn.action = yes_btn_func
    yes_btn.style = 'default'
    yes_btn.color = button_color
    yes_btn.just = 'right'

    cancel_btn.x = yes_btn.right + button_spacing
    cancel_btn.y = yes_btn.top
    cancel_btn.height = button_height
    cancel_btn.width = button_width
    cancel_btn.font = button_font
    cancel_btn.action = cancel_btn_func
    cancel_btn.style = 'default'
    cancel_btn.color = button_color
    cancel_btn.just = 'right'

    # ========== Add buttons to window ==========
    view.add(title)
    view.add(message)
    view.add(yes_btn)
    view.add(cancel_btn)

    win_confirm_prompt.add(view)
    view.become_target()
    win_confirm_prompt.show()
