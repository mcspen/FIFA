from GUI import Button, Label, View, Window
from AppConfig import *
import json
import unicodedata


def open_player_bio_window(window_x, window_y, player, win_search):

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
        win_player_bio.hide()
        win_search.show()

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

    # ========== Player Info ==========
    def printable_text(input_text):
        return unicodedata.normalize('NFKD', input_text).encode('ascii', 'ignore')

    player_info = []

    # Get attribute lists
    with open('configs.json', 'r') as f:
        attribute_lists = json.load(f)['player_attributes']
        f.close()

    # Get player's common name
    common_name = printable_text(player['commonName'])

    # Get player's name
    player_name = printable_text(player['firstName']) + ' ' + printable_text(player['lastName'])

    # If the player has a common name, use it
    if len(common_name) > 0:
        player_info.append(common_name)
    else:
        player_info.append(player_name)

    # Player's rating
    player_info.append(str(player['rating']))

    # Player's position
    player_info.append(player['position'])

    # Player's card color
    player_info.append(player['color'])

    # Player's nation
    nation = unicodedata.normalize('NFKD', player['nation']['name']).encode('ascii', 'ignore')
    player_info.append(nation[:20])

    # Player's league
    league = unicodedata.normalize('NFKD', player['league']['name']).encode('ascii', 'ignore')
    player_info.append(league[:20])

    # Get player's club
    club = unicodedata.normalize('NFKD', player['club']['name']).encode('ascii', 'ignore')
    player_info.append(club[:20])

    # ========== Player Info Labels ==========

    # ========== Add buttons to window ==========
    view.add(title)
    view.add(back_btn)

    win_player_bio.add(view)
    view.become_target()
    win_player_bio.show()
