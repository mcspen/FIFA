from GUI import Button, Label, View, Window
from AppConfig import *
from Logic import Team
from Logic import TeamDB
import multiprocessing


# ========== Create teams function ==========
def create_teams(db_dict, file_name):
    team = Team.Team()
    teams = TeamDB.TeamDB(team.create_team_ultimate(db_dict['player_list'][1], db_dict['formation_list'][1]))

    if len(teams.db) > 0:
        teams.save(file_name)
    else:
        print 'Not saved because no teams created.'

def open_status_window(window_x, window_y, db_dict, file_name, win_previous):

    display_list = []

    # ========== Window ==========
    status_window = Window()
    status_window.title = search_win_title
    status_window.auto_position = False
    status_window.position = (window_x, window_y)
    status_window.size = (win_width, win_height)
    status_window.resizable = 0
    status_window.name = status_window_win_title

    # ========== Window Image View ==========
    class WindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = WindowImageView(size=status_window.size)

    # ========== Title ==========
    title = Label(text=status_window_title)
    title.font = title_font
    title.width = title_width
    title.height = title_height
    title.x = (win_width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'
    display_list.append(title)

    # ========== Button Declarations ==========
    stop_btn = Button("Stop")

    # ========== Action Button Functions ==========
    def start_btn_func():
        blah = 0

    # ========== Buttons ==========
    stop_btn.x = (status_window.width - button_width) / 2
    stop_btn.y = status_window.height - 100
    stop_btn.height = button_height
    stop_btn.width = button_width
    stop_btn.font = button_font
    stop_btn.action = start_btn_func
    stop_btn.style = 'default'
    stop_btn.color = button_color
    stop_btn.just = 'right'
    display_list.append(stop_btn)

    # ========== Start team creation in new process ==========
    multiprocessing.Process(target=create_teams, args=(db_dict, file_name)).start()

    # ========== Add components to view and add view to window ==========
    for msg in display_list:
        view.add(msg)

    status_window.add(view)
    view.become_target()
    status_window.show()
