from GUI import Font
from GUI.StdFonts import system_font
import GUI.StdColors

# ========== Config JSON Location ==========
config_filename = 'JSONs/configs.json'
futbin_filename = 'JSONs/futbin_id_dict.json'

# ========== Strings ==========
# Titles on top of windows
assign_players_title = 'Assign Players'
attribute_title = 'Attributes Menu'
confirm_prompt_title = 'Are you sure?'
create_list_title = 'Create New List'
create_ultimate_teams_title = 'Create Ultimate Teams'
edit_title = 'Edit'
enter_text_title = 'Enter Text'
files_title = 'Manage Files'
formation_bio_title = 'Formation Bio'
formations_title = 'Formations'
pick_file_title = 'File Menu'
pick_formation_title = 'Pick Formation'
pick_player_title = 'Pick Player'
pick_position_title = 'Pick New Position'
player_bio_title = 'Player Bio'
players_title = 'Players'
search_title = 'Search'
start_title = 'FIFA Squad Builder'
status_window_title = "Status"
team_bio_title = 'Team Bio'
teams_title = 'Teams'

# Titles on the window bar at the top
start_win_title = 'FIFA Squad Builder'

assign_players_win_title = start_win_title + ' - ' + assign_players_title
attribute_win_title = start_win_title + ' - ' + attribute_title
confirm_prompt_win_title = start_win_title + ' - ' + confirm_prompt_title
create_list_win_title = start_win_title + ' - ' + create_list_title
create_ultimate_teams_win_title = start_win_title + ' - ' + create_ultimate_teams_title
edit_win_title = start_win_title + ' - ' + edit_title
files_win_title = start_win_title + ' - ' + files_title
formation_bio_win_title = start_win_title + ' - ' + formation_bio_title
formations_win_title = start_win_title + ' - ' + formations_title
pick_file_win_title = start_win_title + ' - ' + pick_file_title
pick_formation_win_title = start_win_title + ' - ' + pick_formation_title
pick_player_win_title = start_win_title + ' - ' + pick_player_title
pick_position_win_title = start_win_title + ' - ' + pick_position_title
player_bio_win_title = start_win_title + ' - ' + player_bio_title
players_win_title = start_win_title + ' - ' + players_title
search_win_title = start_win_title + ' - ' + search_title
status_window_win_title = start_win_title + ' - ' + status_window_title
team_bio_win_title = start_win_title + ' - ' + team_bio_title
teams_win_title = start_win_title + ' - ' + teams_title

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
dark_yellow = GUI.StdColors.rgb(0.75, 0.75, 0)
green = GUI.StdColors.green
dark_green = GUI.StdColors.rgb(0, 0.55, 0)
light_green = GUI.StdColors.rgb(0, 0.7, 0)
blue = GUI.StdColors.blue
cyan = GUI.StdColors.cyan
magenta = GUI.StdColors.magenta
purple = GUI.StdColors.rgb(0.5, 0, 0.5)
clear = GUI.StdColors.clear
gold = GUI.StdColors.rgb(0.83, 0.69, 0.22)
light_gold = GUI.StdColors.rgb(1, 0.84, 0)
silver = GUI.StdColors.rgb(0.75, 0.75, 0.75)
dark_silver = GUI.StdColors.rgb(0.52, 0.52, 0.52)
light_bronze = GUI.StdColors.rgb(0.8, 0.5, 0.2)
bronze = GUI.StdColors.rgb(0.66, 0.53, 0.46)
darker = GUI.StdColors.rgb(0, 0, 0, 0.75)
barely_darker = GUI.StdColors.rgb(0, 0, 0, 0.25)
lighter = GUI.StdColors.rgb(1, 1, 1, 0.85)
barely_lighter = GUI.StdColors.rgb(1, 1, 1, 0.25)


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
        color = bronze
    elif value == 'rare_bronze':
        color = light_bronze
    elif value == 'silver':
        color = dark_silver
    elif value == 'rare_silver':
        color = silver
    elif value == 'gold':
        color = gold
    elif value == 'rare_gold':
        color = light_gold
    elif value == 'standard':
        color = white
    elif value == 'rare':
        color = gold
    elif value == 'purple':
        color = purple
    else:
        color = blue

    return color


def quality_text_color(value):
    if value in ['legend',
                 'green', 'motm', 'pink', 'purple', 'teal',
                 'totw_gold', 'totw_silver', 'totw_bronze',
                 'rare_gold', 'rare_silver', 'rare_bronze',
                 'gold', 'silver', 'bronze']:
        color = black
    elif value in ['toty', 'easports', 'tots_gold', 'tots_silver', 'tots_bronze']:
        color = white
    else:
        color = white

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
smaller_button_font = Font("Times", 0.8 * system_font.size, ['bold'])
small_button_color = red
small_button_top_spacing = 10

tiny_button_height = 20

file_btn_width = 200
file_btn_spacing = 3

# ========== Textfields ==========
title_font = Font("Times", 3 * system_font.size, ['bold'])
title_font_2 = Font("Times", 2.5 * system_font.size, ['bold'])
title_font_3 = Font("Times", 2.3 * system_font.size, ['bold'])
title_font_4 = Font("Times", 2.0 * system_font.size, ['bold'])
title_font_5 = Font("Times", 1.8 * system_font.size, ['bold'])
title_font_6 = Font("Times", 1.6 * system_font.size, ['bold'])
title_font_7 = Font("Times", 1.5 * system_font.size, ['bold'])
title_font_8 = Font("Times", 1.4 * system_font.size, ['bold'])
title_font_9 = Font("Times", 1.3 * system_font.size, ['bold'])
title_font_10 = Font("Times", 1.2 * system_font.size, ['bold'])
title_font_11 = Font("Times", 1.1 * system_font.size, ['bold'])
title_font_12 = Font("Times", 1.0 * system_font.size, ['bold'])
title_font_13 = Font("Times", 0.9 * system_font.size, ['bold'])
title_tf_font = Font("Times", 1.6 * system_font.size, ['bold'])
std_tf_font = Font("Times", 1.5 * system_font.size)
std_tf_font_bold = Font("Times", 1.5 * system_font.size, ['bold'])
small_tf_font = Font("Times", 1.2 * system_font.size)
smaller_tf_font = Font("Times", 1.1 * system_font.size)
smallest_tf_font = Font("Times", 1.0 * system_font.size)
std_tf_width = 210
std_tf_height = 20
std_tf_height_plus = 25
