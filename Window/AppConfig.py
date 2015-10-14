from GUI import Font
from GUI.StdFonts import system_font
import GUI.StdColors

# ========== Strings ==========
# Titles on top of windows
start_title = 'FIFA Squad Builder'
start_message_text = 'Select a Tab to Get Started!'
search_title = 'Search'
players_title = 'Players'
formations_title = 'Formations'
teams_title = 'Teams'
manage_title = 'Manage Files'
attribute_title = 'Attributes Menu'
player_bio_title = 'Player Bio'
file_title = 'File Menu'
confirm_prompt_title = 'Are you sure?'
edit_title = 'Edit'
create_list_title = 'Create New List'

# Titles on the window bar at the top
start_win_title = 'FIFA Squad Builder'
search_win_title = start_win_title + ' - ' + search_title
players_win_title = start_win_title + ' - ' + players_title
formations_win_title = start_win_title + ' - ' + formations_title
teams_win_title = start_win_title + ' - ' + teams_title
manage_win_title = start_win_title + ' - ' + manage_title
attribute_win_title = start_win_title + ' - ' + attribute_title
player_bio_win_title = start_win_title + ' - ' + player_bio_title
file_win_title = start_win_title + ' - ' + file_title
confirm_prompt_win_title = start_win_title + ' - ' + confirm_prompt_title
edit_win_title = start_win_title + ' - ' + edit_title
create_list_win_title = start_win_title + ' - ' + create_list_title

# ========== Colors ==========
black = GUI.StdColors.black
dark_gray = GUI.StdColors.dark_grey
gray = GUI.StdColors.grey
light_gray = GUI.StdColors.light_grey
white = GUI.StdColors.white
red = GUI.StdColors.red
orange = GUI.StdColors.rgb(1, 0.5, 0)
dark_orange = GUI.StdColors.rgb(1, 0.55, 0)
yellow = GUI.StdColors.yellow
green = GUI.StdColors.green
dark_green = GUI.StdColors.rgb(0, 0.55, 0)
light_green = GUI.StdColors.rgb(0, 0.7, 0)
blue = GUI.StdColors.blue
cyan = GUI.StdColors.cyan
magenta = GUI.StdColors.magenta
purple = GUI.StdColors.rgb(0.5, 0, 0.5)
clear = GUI.StdColors.clear
gold = GUI.StdColors.rgb(1, 0.84, 0)
light_gold = GUI.StdColors.rgb(0.83, 0.69, 0.22)
silver = GUI.StdColors.rgb(0.75, 0.75, 0.75)
dark_silver = GUI.StdColors.rgb(0.52, 0.52, 0.52)
bronze = GUI.StdColors.rgb(0.8, 0.5, 0.2)
dark_bronze = GUI.StdColors.rgb(0.59, 0.29, 0)
darker = GUI.StdColors.rgb(0, 0, 0, 0.75)


def attr_color(value):
    if value <= 50:
        color = red
    elif value <= 60:
        color = dark_orange
    elif value <= 70:
        color = yellow
    elif value <= 80:
        color = light_green
    else:
        color = dark_green

    return color


def quality_color(value):
    if value == 'bronze':
        color = dark_bronze
    elif value == 'rare_bronze':
        color = bronze
    elif value == 'silver':
        color = dark_silver
    elif value == 'rare_silver':
        color = silver
    elif value == 'gold':
        color = light_gold
    elif value == 'rare_gold':
        color = gold
    elif value == 'standard':
        color = white
    elif value == 'rare':
        color = gold
    elif value == 'purple':
        color = purple
    else:
        color = blue

    return color

# ========== Window ==========
win_width = 800
win_height = 700
top_border = 30

# ========== View ==========
view_backcolor = black

# ========== Title ==========
title_border = 10
title_width = 700
title_height = 50
title_color = white

# ========== Messages ==========
start_message_border = 10
start_message_width = 385
start_message_height = 50
start_message_font = Font("Times", 3 * system_font.size, ['bold'])
start_message_color = white

# ========== Buttons ==========
button_width = 125
button_height = 50
button_spacing = 15
button_font = Font("Times", 1.5 * system_font.size, ['bold'])
button_color = red

small_button_width = 110
small_button_height = 30
small_button_spacing = 3
small_button_font = Font("Times", 0.9 * system_font.size, ['bold'])
small_button_color = red
small_button_top_spacing = 10

tiny_button_height = 20

file_btn_width = 200
file_btn_spacing = 3

# ========== Textfields ==========
title_font = Font("Times", 3 * system_font.size, ['bold'])
title_font_2 = Font("Times", 2.5 * system_font.size, ['bold'])
title_tf_font = Font("Times", 1.6 * system_font.size, ['bold'])
std_tf_font = Font("Times", 1.5 * system_font.size)
std_tf_font_bold = Font("Times", 1.5 * system_font.size, ['bold'])
small_tf_font = Font("Times", 1.2 * system_font.size)
std_tf_width = 200
std_tf_height = 20
