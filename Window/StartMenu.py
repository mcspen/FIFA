from GUI import Button, Geometry, Image, Label, View, Window

from AppConfig import *
import SearchMenu
import PlayersMenu
import FormationsMenu
import TeamsMenu
import ManageMenu


def open_start_menu(window_x, window_y, db_dict):

    # ========== Window ==========
    win_start = Window()
    win_start.title = win_start_title
    win_start.auto_position = False
    win_start.position = (window_x, window_y)
    win_start.size = (win_width, win_height)
    win_start.resizable = 0
    win_start.name = "Start Window"

    # ========== Window Image View ==========
    class StartWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)
            image_pos = (players_btn.bottom + top_border, (win_start.width - start_window_image.width)/2)
            src_rect = start_window_image.bounds
            dst_rect = Geometry.offset_rect(src_rect, image_pos)
            #start_window_image.draw(c, src_rect, dst_rect)

    view = StartWindowImageView(size=win_start.size)

    # ========== Title ==========
    title = Label(text=start_title)
    title.font = title_font
    title.width = start_title_width
    title.height = title_height
    title.x = (win_width - start_title_width) / 2
    title.y = top_border
    title.color = title_color

    # ========== Button Declarations ==========
    search_btn = Button("Search")
    players_btn = Button("Players")
    formations_btn = Button("Formations")
    teams_btn = Button("Teams")
    manage_btn = Button("Manage Files")

    button_list = [search_btn,
                   players_btn,
                   formations_btn,
                   teams_btn,
                   manage_btn]

    # ========== Start Window Image ==========
    start_window_image = Image(file = 'messi.jpg')

    # ========== Button Functions ==========
    def search_btn_func():
        """print "Players players players"

        players_btn.enabled = 0

        player_db = PlayerDB()
        temp_time = time.time()
        player_db.load('player_db_16')
        print "Time to load DB: %f" % (time.time()-temp_time)

        players_btn.enabled = 1"""
        win_start.hide()
        SearchMenu.open_search_menu(win_start.x, win_start.y, db_dict)

    def players_btn_func():
        """print "Players players players"

        players_btn.enabled = 0

        player_db = PlayerDB()
        temp_time = time.time()
        player_db.load('player_db_16')
        print "Time to load DB: %f" % (time.time()-temp_time)

        players_btn.enabled = 1"""
        win_start.hide()
        PlayersMenu.open_players_menu(win_start.x, win_start.y, db_dict)

    def formations_btn_func():
        """print "Formations formations formations"
        view.remove(players_btn)
        formations_btn.enabled = 0
        teams_btn.enabled = 1"""
        win_start.hide()
        FormationsMenu.open_formations_menu(win_start.x, win_start.y, db_dict)

    def teams_btn_func():
        win_start.hide()
        TeamsMenu.open_teams_menu(win_start.x, win_start.y, db_dict)

    def manage_btn_func():
        win_start.hide()
        ManageMenu.open_manage_menu(win_start.x, win_start.y, db_dict)

    # ========== Buttons ==========
    search_btn.x = (win_width - len(button_list)*button_width - (len(button_list)-1)*button_spacing) / 2
    search_btn.y = title.bottom + title_border
    search_btn.height = button_height
    search_btn.width = button_width
    search_btn.font = button_font
    search_btn.action = search_btn_func
    search_btn.style = 'default'
    search_btn.color = button_color
    search_btn.just = 'right'

    players_btn.x = button_spacing + search_btn.right
    players_btn.y = title.bottom + title_border
    players_btn.height = button_height
    players_btn.width = button_width
    players_btn.font = button_font
    players_btn.action = players_btn_func
    players_btn.style = 'default'
    players_btn.color = button_color
    players_btn.just = 'right'

    formations_btn.x = button_spacing + players_btn.right
    formations_btn.y = title.bottom + title_border
    formations_btn.height = button_height
    formations_btn.width = button_width
    formations_btn.font = button_font
    formations_btn.action = formations_btn_func
    formations_btn.style = 'default'
    formations_btn.color = button_color
    formations_btn.just = 'right'

    teams_btn.x = button_spacing + formations_btn.right
    teams_btn.y = title.bottom + title_border
    teams_btn.height = button_height
    teams_btn.width = button_width
    teams_btn.font = button_font
    teams_btn.action = teams_btn_func
    teams_btn.style = 'default'
    teams_btn.color = button_color
    teams_btn.just = 'right'

    manage_btn.x = button_spacing + teams_btn.right
    manage_btn.y = title.bottom + title_border
    manage_btn.height = button_height
    manage_btn.width = button_width
    manage_btn.font = button_font
    manage_btn.action = manage_btn_func
    manage_btn.style = 'default'
    manage_btn.color = button_color
    manage_btn.just = 'right'

    # ========== Add components to view and add view to window ==========
    view.add(title)
    view.add(search_btn)
    view.add(players_btn)
    view.add(formations_btn)
    view.add(teams_btn)
    view.add(manage_btn)

    win_start.add(view)
    view.become_target()
    win_start.show()
