from GUI import Button, Label, View, Window
from AppConfig import *
import FilesMenu
from Logic import Team
from Logic import TeamDB
from Logic import PlayerDB
import multiprocessing


# ========== Create teams function ==========
def create_teams(db_dict, file_name):
    team = Team.Team()
    teams = TeamDB.TeamDB(team.create_team_ultimate(db_dict['player_list'][1], db_dict['formation_list'][1]))

    if len(teams.db) > 0:
        teams.save(file_name)
    else:
        print 'Not saved because no teams created.'


# ========== Create teams function ==========
def download_and_save_player_db(queue, new_db_name):
    # Download player database
    player_db = PlayerDB.PlayerDB()
    player_db.download(queue)
    player_db.save(new_db_name, 'db', True)


def open_status_window(window_x, window_y, db_dict, file_name=None, settings=None, win_previous=None, win_next=None):

    display_list = []

    # ========== Window ==========
    status_window = Window()
    status_window.title = search_win_title
    status_window.auto_position = False
    status_window.position = (window_x, window_y)
    status_window.size = (win_width, win_height - 250)
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

    # ========== Status Labels ==========
    main_status_label = Label(text="Click the 'Current Status' button for updates.", font=title_font_3,
                              width=title_width, height=title_height,
                              x=(win_width - title_width) / 2, y=title.bottom + title_border*5,
                              color=title_color, just='center')
    display_list.append(main_status_label)

    percent_status_label = Label(text="0%", font=title_font_2,
                              width=title_width, height=title_height,
                              x=(win_width - title_width) / 2, y=main_status_label.bottom + title_border,
                              color=title_color, just='center')
    display_list.append(percent_status_label)

    bar_status_text_line = "_"*48
    bar_status_text_ends = "(" + " "*84 + ")"
    bar_status_label_top = Label(text=bar_status_text_line, font=title_font_2,
                                 width=title_width, height=title_height*3,
                                 x=(win_width - title_width) / 2, y=percent_status_label.bottom - 22,
                                 color=title_color, just='center')
    display_list.append(bar_status_label_top)
    bar_status_label_bottom = Label(text=bar_status_text_line, font=title_font_2,
                                   width=title_width, height=title_height*3,
                                   x=(win_width - title_width) / 2, y=percent_status_label.bottom + 6,
                                   color=title_color, just='center')
    display_list.append(bar_status_label_bottom)
    bar_status_label_ends = Label(text=bar_status_text_ends, font=title_font,
                                  width=title_width, height=title_height*3,
                                  x=(win_width - title_width) / 2, y=percent_status_label.bottom,
                                  color=title_color, just='center')
    display_list.append(bar_status_label_ends)
    # Max bars = '|'*max_num_bars
    max_num_bars = 113
    bar_status_label_fill = Label(text='', font=title_font,
                                  width=title_width-22, height=title_height*3,
                                  x=(win_width - title_width) / 2 + 11, y=percent_status_label.bottom,
                                  color=title_color, just='left')
    display_list.append(bar_status_label_fill)

    # ========== Action Button Functions ==========
    def update_btn_func():
        if create_ultimate_teams_title in win_previous.title:
            stuff = 0

        elif "Download Player Database" in win_previous.title:
            if not queue.empty():
                tup = ()
                while not queue.empty():
                    tup = queue.get()

                main_status_label.text = "Approximately %d of %d of players downloaded." % (tup[0]*24, tup[1]*24)
                percent_status_label.text = str(float(tup[0])/tup[1]*100)[:5] + '%'
                bar_status_label_fill.text = '|'*int(max_num_bars*float(tup[0])/tup[1])

                if tup[0] == tup[1]:
                    stop_btn.title = "Done"
                    update_btn.enabled = 0

        status_window.become_target()

    def stop_btn_func():
        if create_ultimate_teams_title in win_previous.title:
            stuff = 0

        elif "Download Player Database" in win_previous.title:
            # Stop the current process
            if stop_btn.title == 'Stop':
                if download_process.is_alive():
                    update_btn_func()
                    download_process.terminate()
                # Update message and button
                stop_btn.title = "Back"
                main_status_label.text = 'Download stopped. Players not saved.'
                update_btn.enabled = 0
                status_window.become_target()

            # Change pages
            elif stop_btn.title in ['Back', 'Done']:
                # Go to the next page
                if win_next is not None:
                    if win_next == 'FilesMenu':
                        FilesMenu.open_files_menu(status_window.x, status_window.y, db_dict, settings)
                        status_window.hide()

                # Go to the previous page
                elif win_previous is not None:
                    win_previous.show()
                    status_window.hide()

        status_window.become_target()

    # ========== Buttons ==========
    update_btn = Button("Current Status",
                        x=(status_window.width - 2*button_width - button_spacing) / 2,
                        y=bar_status_label_fill.bottom - 20,
                        height=button_height, width=button_width, font=button_font, action=update_btn_func,
                        style='default', color=button_color, just='right')
    display_list.append(update_btn)

    stop_btn = Button("Stop", x=update_btn.right + button_spacing, y=update_btn.top,
                      height=button_height, width=button_width, font=button_font, action=stop_btn_func,
                      style='default', color=button_color, just='right')
    display_list.append(stop_btn)

    # ========== Start team creation in new process ==========
    if create_ultimate_teams_title in win_previous.title:
        multiprocessing.Process(target=create_teams, args=(db_dict, file_name)).start()

        title.text = "Creating Ultimate Teams..."

    # ========== Start player downloading in new process ==========
    elif "Download Player Database" in win_previous.title:
        title.text = "Downloading Player Database..."

        queue = multiprocessing.Queue()
        download_process = multiprocessing.Process(target=download_and_save_player_db, args=(queue, file_name))
        download_process.start()

    # ========== Add components to view and add view to window ==========
    for msg in display_list:
        view.add(msg)

    status_window.add(view)
    view.become_target()
    status_window.show()
