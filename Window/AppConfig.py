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
attribute_title = 'Add Attribute'

# Titles on the window bar at the top
win_start_title = 'FIFA Squad Builder'
win_search_title = win_start_title + ' - ' + search_title
win_players_title = win_start_title + ' - ' + players_title
win_formations_title = win_start_title + ' - ' + formations_title
win_teams_title = win_start_title + ' - ' + teams_title
win_manage_title = win_start_title + ' - ' + manage_title
win_attribute_title = win_start_title + ' - ' + attribute_title

# ========== Colors ==========
black = GUI.StdColors.black
dark_gray = GUI.StdColors.dark_grey
gray = GUI.StdColors.grey
light_gray = GUI.StdColors.light_grey
white = GUI.StdColors.white
red = GUI.StdColors.red
green = GUI.StdColors.green
blue = GUI.StdColors.blue
yellow = GUI.StdColors.yellow
cyan = GUI.StdColors.cyan
magenta = GUI.StdColors.magenta
clear = GUI.StdColors.clear

# ========== Window ==========
win_width = 800
win_height = 700
top_border = 30

# ========== View ==========
view_backcolor = black

# ========== Title ==========
title_border = 10
search_title_width = 95
start_title_width = 300
players_title_width = 105
formations_title_width = 165
teams_title_width = 90
manage_title_width = 190
attribute_title_width = 200
title_height = 50
title_font = Font("Times", 3 * system_font.size, ['bold'])
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

# ========== Textfields ==========
title_tf_font = Font("Times", 1.6 * system_font.size, ['bold'])
std_tf_font = Font("Times", 1.5 * system_font.size)
std_tf_width = 200
std_tf_height = 20
