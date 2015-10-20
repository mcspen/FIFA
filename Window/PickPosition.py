from GUI import Button, Label, RadioButton, RadioGroup, TextField, View, Window
from AppConfig import *
import SearchMenu
import EditMenu
from Logic.HelperFunctions import format_attr_name
import json


def open_pick_position_window(window_x, window_y, player, player_db, settings, btn, previous_window):

    # ========== Window ==========
    win_position = Window()
    win_position.title = pick_position_win_title
    win_position.auto_position = False
    win_position.position = (window_x, window_y)
    win_position.size = (win_width, 500)
    win_position.resizable = 0
    win_position.name = pick_position_title + " Window"
    win_position.show()

    # ========== Window Image View ==========
    class StartWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = StartWindowImageView(size=win_position.size)

    display_list = []

    # ========== Title ==========
    title = Label(text=pick_position_title)
    title.font = title_font
    title.width = title_width
    title.height = title_height
    title.x = (win_width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'
    display_list.append(title)

    # ========== Button Function ==========
    def pos_btn_func(position_short, position_full):
        # Edit player's position
        player_data = player_db.search({'id': (player['id'], 'exact')})
        player_index = player_db.db.index(player_data[0])
        player_db.db[player_index]['position'] = position_short
        player_db.db[player_index]['positionFull'] = position_full

        # Save
        player_db.save(settings['file_name'], 'list', True)

        # Change button symbol
        btn.title = position_short
        win_position.hide()
        previous_window.show()

    def back_btn_func():
        # Go back
        win_position.hide()
        previous_window.show()

    # ========== Position Buttons ==========
    msg_x = (win_position.width - 5*button_width - 4*button_spacing) / 2
    msg_y = title.bottom + title_border
    positions = [
        ('LW', 'Left Wing'), ('LF', 'Left Forward'), ('ST', 'Striker'), ('RF', 'Right Forward'), ('RW', 'Right Wing'),
        ('CF', 'Centre Forward'),
        ('CAM', 'Centre Attacking Midfielder'),
        ('LM', 'Left Midfielder'), ('CM', 'Centre Midfielder'), ('RM', 'Right Midfielder'),
        ('CDM', 'Centre Defensive Midfielder'),
        ('LWB', 'Left Wing Back'), ('LB', 'Left Back'), ('CB', 'Centre Back'), ('RB', 'Right Back'),
        ('RWB', 'Right Wing Back'),
        ('GK', 'Goalkeeper')]

    for index, pos in enumerate(positions):
        if pos[0] in ['CAM', 'CDM']:
            width = button_width + 65
        else:
            width = button_width

        if index == 5:
            msg_x = (win_position.width - width) / 2
            msg_y += small_button_height + button_spacing
        elif index == 6:
            msg_x = (win_position.width - width) / 2
            msg_y += small_button_height + button_spacing
        elif index == 7:
            msg_x = (win_position.width - 3*width - 2*button_spacing) / 2
            msg_y += small_button_height + button_spacing
        elif index == 10:
            msg_x = (win_position.width - width) / 2
            msg_y += small_button_height + button_spacing
        elif index == 11:
            msg_x = (win_position.width - 5*width - 4*button_spacing) / 2
            msg_y += small_button_height + button_spacing
        elif index == 16:
            msg_x = (win_position.width - width) / 2
            msg_y += small_button_height + button_spacing

        position_title = pos[0] + ' - ' + pos[1]
        pos_btn = Button(title=position_title, width=width, height=small_button_height, x=msg_x, y=msg_y,
                         action=(pos_btn_func, pos[0], pos[1]), font=smaller_tf_font)
        display_list.append(pos_btn)

        msg_x += width + button_spacing

    # ========== Back Button ==========
    msg_x = (win_position.width - button_width) / 2
    msg_y += small_button_height + top_border
    back_btn = Button("Back", width=button_width, height=button_height, x=msg_x, y=msg_y,
                      action=back_btn_func, font=button_font)
    display_list.append(back_btn)

    # ========== Add buttons to window ==========
    for item in display_list:
        view.add(item)

    win_position.add(view)
    view.become_target()
    win_position.show()
