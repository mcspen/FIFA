from GUI import Button, Label, View, Window
import json
from AppConfig import *
import StartMenu
import AddAttribute
from Logic import PlayerDB


def open_search_menu(window_x, window_y, player_db, formation_db, player_list,
                     formation_list, team_list, attr_dict=None, attr_list=None):

    if attr_dict is None:
        attr_dict = {}

    if attr_list is None:
        attr_list = []

    lowest_item = 0

    # ========== Window ==========
    win_search = Window()
    win_search.title = win_search_title
    win_search.auto_position = False
    win_search.position = (window_x, window_y)
    win_search.size = (win_width, win_height)
    win_search.resizable = 0
    win_search.name = "Search Window"

    # ========== Window Image View ==========
    class FormationsWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = FormationsWindowImageView(size=win_search.size)

    # ========== Title ==========
    title = Label(text=search_title)
    title.font = title_font
    title.width = search_title_width
    title.height = title_height
    title.x = (win_width - search_title_width) / 2
    title.y = top_border
    title.color = title_color

    # ========== Action Button Declarations ==========
    start_btn = Button("Start")
    back_btn = Button("Back")

    # ========== Search Type Button Declarations ==========
    players_btn = Button("Players")
    formations_btn = Button("Formations")
    teams_btn = Button("Teams")

    search_type_button_list = [players_btn,
                               formations_btn,
                               teams_btn]

    # ========== Tool Button Declarations ==========
    attribute_btn = Button("Add Attribute")
    sort_btn = Button("Sort Results")
    reset_btn = Button("Reset Results")

    # ========== Action Button Functions ==========
    def start_btn_func():
        search_results = player_db.search(attr_dict, 'higher')
        search_results = PlayerDB.PlayerDB(search_results)
        search_results.print_db(10)
        stuff = 0

    def back_btn_func():
        StartMenu.open_start_menu(win_search.left, win_search.top,
                                  player_db, formation_db, player_list, formation_list, team_list)
        win_search.hide()

    # ========== Search Type Button Functions ==========
    def players_btn_func():
        for btn in search_type_button_list:
            btn.enabled = 1
        players_btn.enabled = 0

    def formations_btn_func():
        for btn in search_type_button_list:
            btn.enabled = 1
        formations_btn.enabled = 0

    def teams_btn_func():
        for btn in search_type_button_list:
            btn.enabled = 1
        teams_btn.enabled = 0

    # ========== Tool Button Functions ==========
    def attribute_btn_func():
        AddAttribute.open_attribute_window(window_x, window_y, player_db, formation_db, player_list,
                                           formation_list, team_list, attr_dict)
        win_search.hide()

    def sort_btn_func():
        stuff = 0

    def reset_btn_func():
        sort_btn.enabled = 0
        reset_btn.enabled = 0

    # ========== Action Buttons ==========
    start_btn.x = (win_width - 2*small_button_width - small_button_spacing) / 2
    start_btn.y = title.bottom + small_button_top_spacing
    start_btn.height = small_button_height
    start_btn.width = small_button_width
    start_btn.font = small_button_font
    start_btn.action = start_btn_func
    start_btn.style = 'default'
    start_btn.color = small_button_color
    start_btn.just = 'right'
    start_btn.enabled = 0

    back_btn.x = start_btn.right + small_button_spacing
    back_btn.y = start_btn.top
    back_btn.height = small_button_height
    back_btn.width = small_button_width
    back_btn.font = small_button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = small_button_color
    back_btn.just = 'right'

    # ========== Search Type Buttons ==========
    players_btn.x = (win_width - 3*small_button_width - 2*small_button_spacing) / 2
    players_btn.y = start_btn.bottom + small_button_top_spacing
    players_btn.height = small_button_height
    players_btn.width = small_button_width
    players_btn.font = small_button_font
    players_btn.action = players_btn_func
    players_btn.style = 'default'
    players_btn.color = small_button_color
    players_btn.just = 'right'
    players_btn.enabled = 0  # start with player search

    formations_btn.x = players_btn.right + small_button_spacing
    formations_btn.y = players_btn.top
    formations_btn.height = small_button_height
    formations_btn.width = small_button_width
    formations_btn.font = small_button_font
    formations_btn.action = formations_btn_func
    formations_btn.style = 'default'
    formations_btn.color = small_button_color
    formations_btn.just = 'right'

    teams_btn.x = formations_btn.right + small_button_spacing
    teams_btn.y = players_btn.top
    teams_btn.height = small_button_height
    teams_btn.width = small_button_width
    teams_btn.font = small_button_font
    teams_btn.action = teams_btn_func
    teams_btn.style = 'default'
    teams_btn.color = small_button_color
    teams_btn.just = 'right'

    # ========== Tool Buttons ==========
    attribute_btn.x = (win_width - 3*small_button_width - 2*small_button_spacing) / 2
    attribute_btn.y = players_btn.bottom + 5
    attribute_btn.height = small_button_height
    attribute_btn.width = small_button_width
    attribute_btn.font = small_button_font
    attribute_btn.action = attribute_btn_func
    attribute_btn.style = 'default'
    attribute_btn.color = small_button_color
    attribute_btn.just = 'right'

    sort_btn.x = attribute_btn.right + small_button_spacing
    sort_btn.y = attribute_btn.top
    sort_btn.height = small_button_height
    sort_btn.width = small_button_width
    sort_btn.font = small_button_font
    sort_btn.action = sort_btn_func
    sort_btn.style = 'default'
    sort_btn.color = small_button_color
    sort_btn.just = 'right'
    sort_btn.enabled = 0  # no results at start

    reset_btn.x = sort_btn.right + small_button_spacing
    reset_btn.y = attribute_btn.top
    reset_btn.height = small_button_height
    reset_btn.width = small_button_width
    reset_btn.font = small_button_font
    reset_btn.action = reset_btn_func
    reset_btn.style = 'default'
    reset_btn.color = small_button_color
    reset_btn.just = 'right'
    reset_btn.enabled = 0  # no results at start
    lowest_item = reset_btn.bottom

    # ========== Messages ==========
    # Attribute Messages
    if len(attr_dict) > 0:
        start_btn.enabled = 1

        for key, value in attr_dict.iteritems():
            attr_label = Label(text=(key + ": " + str(value)), font=std_tf_font, width=std_tf_width,
                               height=std_tf_height, x=attribute_btn.left, y=lowest_item, color=title_color)
            lowest_item += std_tf_height
            view.add(attr_label)
            win_search.add(view)

    # ========== Add components to view and add view to window ==========
    view.add(title)
    view.add(start_btn)
    view.add(back_btn)
    view.add(players_btn)
    view.add(formations_btn)
    view.add(teams_btn)
    view.add(attribute_btn)
    view.add(sort_btn)
    view.add(reset_btn)

    win_search.add(view)
    view.become_target()
    win_search.show()
