from GUI import Button, Geometry, Image, Label, View, Window
from AppConfig import *
import cStringIO
import json
import urllib
from Logic.HelperFunctions import ascii_text


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
            image_pos = (player_title_label.left - player_headshot.width - 20,
                         player_title_label.bottom - player_headshot.height)
            src_rect = player_headshot.bounds
            dst_rect = Geometry.offset_rect(src_rect, image_pos)
            player_headshot.draw(c, src_rect, dst_rect)

    view = StartWindowImageView(size=win_player_bio.size)

    # ========== Player Headshot ==========
    image_url = player['headshotImgUrl']
    print ascii_text(player['lastName'])
    print image_url
    #url_file = requests.get(image_url)
    #url_image = open(StringIO(url_file.content))
    #urllib.urlretrieve(image_url, 'C:\Users\mspencer\PycharmProjects\FIFA\Images')
    player_headshot = Image(file = 'Images/headshot.png')

    # ========== Title ==========
    title = Label(text=player_bio_title)
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
    player_info = []

    # Get attribute lists
    with open('configs.json', 'r') as f:
        attribute_lists = json.load(f)['player_attributes']
        f.close()

    # Get player's normal name
    player_name = ascii_text(player['commonName'])

    # Get player's name
    player_full_name = ascii_text(player['firstName']) + ' ' + ascii_text(player['lastName'])

    # Player's rating
    player_info.append(str(player['rating']))

    # Player's position
    player_info.append(player['position'])

    # Player's card color
    player_info.append(player['color'])

    # Player's nation
    nation = ascii_text(player['nation']['name'])
    player_info.append(nation[:20])

    # Player's league
    league = ascii_text(player['league']['name'])
    player_info.append(league[:20])

    # Get player's club
    club = ascii_text(player['club']['name'])
    player_info.append(club[:20])

    # ========== Player Info Labels ==========
    player_name_label = Label(font=title_font, width=400, height=title_height, x=(win_width - 400)/2,
                               y=title.bottom + top_border, color=title_color, just='center')
    player_name_label.text = str(player['rating']) + '  ' + player_name
    view.add(player_name_label)


    # ========== Add buttons to window ==========
    view.add(title)
    view.add(back_btn)

    win_player_bio.add(view)
    view.become_target()
    win_player_bio.show()
