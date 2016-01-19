from GUI import Button, Label, RadioButton, RadioGroup, TextField, View, Window
from AppConfig import *
import PickFile
import FilesMenu
import StatusWindow
from Logic.PlayerDB import PlayerDB
from os import rename
from os.path import isfile
from shutil import copyfile


def download_and_save(new_db_name):
    # Download player database
    player_db = PlayerDB()
    player_db.download()
    player_db.save(new_db_name, 'db', True)


def open_enter_text_window(window_x, window_y, db_dict, settings, box_type, fill_text='', file_prefix=''):

    general_display = []

    if box_type == 'rename':
        title = 'Rename File'
        old_file_name = fill_text
        message_text = 'Enter new file name.'
    elif box_type == 'duplicate':
        title = 'Duplicate File'
        old_file_name = fill_text
        message_text = 'Enter new file name.'
    elif box_type == 'download':
        title = 'Download Player Database'
        message_text = 'Enter player database name.'
        download_settings = {'overwrite_counter': 0, 'last_entered_text': ''}
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
    win_enter_text.name = enter_text_title + " Window"
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
    general_display.append(title)

    # ========== Message Label ==========
    message = Label(font=title_font_2, width=win_enter_text.width - 50, height=title_height,
                    x=25, y=title.bottom + top_border, color=title_color, just='center')
    message.text = message_text
    general_display.append(message)

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

                if not isfile('JSONs/' + file_prefix + new_file_name + '.json'):
                    # Rename file
                    rename('JSONs/' + file_prefix + old_file_name + '.json',
                           'JSONs/' + file_prefix + new_file_name + '.json')

                    # Disable pick file back button in case the selected file has changed
                    settings['file_changes'] = True

                    PickFile.open_pick_file_window(window_x, window_y, db_dict, settings)
                    win_enter_text.hide()

                else:
                    message.text = "A file with that name already exists."

            else:
                message.text = "File name must be at least 1 character."

        # Duplicate file
        elif box_type == 'duplicate':

            # Get new name
            duplicate_file_name = value_tf.value

            if len(duplicate_file_name) > 0:

                if not isfile('JSONs/' + file_prefix + duplicate_file_name + '.json'):
                    # Create duplicate file
                    copyfile('JSONs/' + file_prefix + old_file_name + '.json',
                             'JSONs/' + file_prefix + duplicate_file_name + '.json')

                    PickFile.open_pick_file_window(window_x, window_y, db_dict, settings)
                    win_enter_text.hide()

                else:
                    message.text = "A file with that name already exists."

            else:
                message.text = "File name must be at least 1 character."

        elif box_type == 'download':
            valid_name = False

            # Get new player database name
            new_player_db_name = value_tf.value

            if new_player_db_name != download_settings['last_entered_text']:
                download_settings['overwrite_counter'] = 0
                message.text = message_text

            if len(new_player_db_name) > 0:

                if not isfile('JSONs/play_db_' + new_player_db_name + '.json'):
                    valid_name = True

                else:
                    download_settings['last_entered_text'] = new_player_db_name

                    if download_settings['overwrite_counter'] == 0:
                        download_settings['overwrite_counter'] += 1
                        message.text = "File already exists. Overwrite?"
                    elif download_settings['overwrite_counter'] == 1:
                        download_settings['overwrite_counter'] += 1
                        message.text = "Are you sure you want to overwrite?"
                    elif download_settings['overwrite_counter'] == 2:
                        download_settings['overwrite_counter'] += 1
                        message.text = "Really, really, really sure?"
                    elif download_settings['overwrite_counter'] >= 3:
                        valid_name = True

                if valid_name:
                    # Open status window to start download of players
                    StatusWindow.open_status_window(win_enter_text.x, win_enter_text.y, db_dict,
                                                    get_prices=sort_order_radio_group.value,
                                                    file_name=new_player_db_name, settings=settings,
                                                    win_previous=win_enter_text, win_next='FilesMenu')
                    win_enter_text.hide()

            else:
                message.text = "File name must be at least 1 character."

    def back_btn_func():
        if box_type == 'download':
            FilesMenu.open_files_menu(window_x, window_y, db_dict, settings)
        else:
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
    general_display.append(enter_btn)

    back_btn.x = enter_btn.right + button_spacing
    back_btn.y = enter_btn.top
    back_btn.height = button_height
    back_btn.width = button_width
    back_btn.font = button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = button_color
    back_btn.just = 'right'
    general_display.append(back_btn)

    # ========== Value Textfield ==========
    value_tf = TextField()
    value_tf.width = 200
    value_tf.x = (win_enter_text.width - value_tf.width) / 2
    value_tf.y = enter_btn.top - 65
    value_tf.height = 25
    value_tf.font = std_tf_font
    value_tf.value = fill_text
    general_display.append(value_tf)

    def get_attribute_sort_order_rg():
        settings['order_rg'] = sort_order_radio_group.value
        win_enter_text.become_target()

    sort_order_radio_group = RadioGroup(action=get_attribute_sort_order_rg)

    prices_label_width = 85
    prices_button_width = 50
    prices_label = Label(text="Get Prices?:", font=std_tf_font, width=prices_label_width, height=std_tf_height,
                         color=title_color)
    prices_label.x = (win_enter_text.width - 2*prices_button_width - 10 - prices_label_width) / 2
    prices_label.y = enter_btn.top - 38
    prices_label.just = 'center'

    prices_yes = RadioButton("Yes")
    prices_yes.width = prices_button_width
    prices_yes.x = prices_label.right + 5
    prices_yes.y = prices_label.top
    prices_yes.group = sort_order_radio_group
    prices_yes.value = True

    prices_no = RadioButton("No")
    prices_no.width = prices_button_width
    prices_no.x = prices_yes.right + 5
    prices_no.y = prices_label.top
    prices_no.group = sort_order_radio_group
    prices_no.value = False

    sort_order_radio_group.value = True

    if box_type == 'download':
        value_tf.y = enter_btn.top - 75

        general_display.append(prices_label)
        general_display.append(prices_yes)
        general_display.append(prices_no)

    # ========== Add buttons to window ==========
    for item in general_display:
        view.add(item)

    win_enter_text.add(view)
    view.become_target()
    win_enter_text.show()
