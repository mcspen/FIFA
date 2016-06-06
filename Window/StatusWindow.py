from GUI import Button, Label, View, Window
from AppConfig import *
import FilesMenu
from Logic import Team
from Logic import TeamDB
from Logic import PlayerDB
import multiprocessing
import time


# ========== Create teams function ==========
def create_teams(db_dict, file_name):
    team = Team.Team()
    teams = TeamDB.TeamDB(team.create_team_ultimate(db_dict['player_list'][1], db_dict['formation_list'][1]))

    if len(teams.db) > 0:
        teams.save(file_name)
    else:
        print 'Not saved because no teams created.'


# ========== Download player db and save function ==========
def download_and_save_player_db(queue, new_db_name, get_prices):
    # Download player database
    player_db = PlayerDB.PlayerDB()
    player_db.download(queue, get_prices=get_prices)

    # Save player database
    player_db.save(new_db_name, 'db', True)


# ========== Update player prices function ==========
def update_player_prices(queue, file_name, settings):
    # Create player object and load the list or db
    if 'player' in settings['file_type']:
        if 'list' in settings['file_type']:
            file_type = 'list'
        else:
            file_type = 'db'
        object_list = PlayerDB.PlayerDB()
        object_list.load(file_name, file_type)

    # Create team object and load the list
    elif 'team' in settings['file_type']:
        file_type = 'Not used'
        object_list = TeamDB.TeamDB()
        object_list.load(file_name)

    else:
        print "Invalid file type."
        file_type = 'Not used'
        object_list = PlayerDB.PlayerDB()

    object_list.update_player_prices(queue=queue, console=settings['console'])

    # Save list/db and overwrite previous
    if 'player' in settings['file_type']:
        object_list.save(file_name, file_type, True)
    elif 'team' in settings['file_type']:
        object_list.save(file_name, True)
    else:
        print "Invalid file type."


def open_status_window(window_x, window_y, db_dict,
                       file_name=None, get_prices=None, settings=None, win_previous=None, win_next=None):

    display_list = []

    # ========== Window ==========
    status_window = Window()
    status_window.title = status_window_win_title
    status_window.auto_position = False
    status_window.position = (window_x, window_y)
    status_window.size = (win_width, win_height - 250)
    status_window.resizable = 0
    status_window.name = status_window_title

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
                              x=(win_width - title_width) / 2, y=title.bottom + title_border*3,
                              color=title_color, just='center')
    display_list.append(main_status_label)

    percent_status_label = Label(text="0%", font=title_font_2,
                              width=title_width, height=title_height,
                              x=(win_width - title_width) / 2, y=main_status_label.bottom - 5,
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
                                   width=title_width, height=title_height,
                                   x=(win_width - title_width) / 2, y=percent_status_label.bottom + 6,
                                   color=title_color, just='center')
    display_list.append(bar_status_label_bottom)
    bar_status_label_ends = Label(text=bar_status_text_ends, font=title_font,
                                  width=title_width, height=title_height,
                                  x=(win_width - title_width) / 2, y=percent_status_label.bottom,
                                  color=title_color, just='center')
    display_list.append(bar_status_label_ends)
    # Max bars = '|'*max_num_bars
    max_num_bars = 113
    bar_status_label_fill = Label(text='', font=title_font,
                                  width=title_width-22, height=title_height,
                                  x=(win_width - title_width) / 2 + 11, y=percent_status_label.bottom,
                                  color=title_color, just='left')
    display_list.append(bar_status_label_fill)

    time_passed_label = Label(text="Time Passed: 0 seconds", font=title_font_3,
                              width=title_width, height=title_height,
                              x=(win_width - title_width) / 2, y=bar_status_label_fill.bottom + title_border,
                              color=title_color, just='center')
    display_list.append(time_passed_label)

    time_left_label = Label(text="Time Remaining: ? seconds", font=title_font_3,
                              width=title_width, height=title_height,
                              x=(win_width - title_width) / 2, y=time_passed_label.bottom - 20,
                              color=title_color, just='center')
    display_list.append(time_left_label)

    # ========== Action Button Functions ==========
    def update_btn_func():
        if create_ultimate_teams_title in win_previous.title:
            stuff = 0

        elif "Download Player Database" in win_previous.title:
            if not queue.empty():
                tup = ()
                while not queue.empty():
                    tup = queue.get()

                if len(tup) == 1:
                    main_status_label.text = tup

                elif len(tup) == 2:
                    main_status_label.text = "Approximately %d of %d of players downloaded." % (tup[0]*24, tup[1]*24)
                    percent_status_label.text = str(float(tup[0])/tup[1]*100)[:5] + '%'
                    bar_status_label_fill.text = '|'*int(max_num_bars*float(tup[0])/tup[1])

                    if tup[0] == tup[1]:
                        stop_btn.title = "Done"
                        update_btn.enabled = 0

        elif 'update_prices' in settings:
            if settings['update_prices']:
                if not queue.empty():
                    tup = ()
                    while not queue.empty():
                        tup = queue.get()

                    if len(tup) == 1:
                        main_status_label.text = tup

                    elif len(tup) == 2:
                        main_status_label.text = "%d of %d of players updated." % (tup[0], tup[1])
                        percent_status_label.text = str(float(tup[0])/tup[1]*100)[:5] + '%'
                        bar_status_label_fill.text = '|'*int(max_num_bars*float(tup[0])/tup[1])

                        if tup[0] == tup[1]:
                            stop_btn.title = "Done"
                            update_btn.enabled = 0

        # Calculate time passed
        current_time = time.time()
        time_passed = current_time - start_time
        if time_passed < 60:
            time_passed_text = "Time Passed: %d seconds" % time_passed
        elif time_passed < 3600:
            time_passed_text = "Time Passed: %d minutes, %d seconds" % (time_passed/60, time_passed % 60)
        elif time_passed < 86400:
            time_passed_text = "Time Passed: %d hours, %d minutes, %d seconds" % \
                               (time_passed/3600, time_passed % 3600 / 60, time_passed % 60)
        else:
            time_passed_text = "Time Passed: %d days, %d hours, %d minutes, %d seconds" % \
                               (time_passed/86400, time_passed % 86400 / 3600,
                                time_passed % 3600 / 60, time_passed % 60)
        time_passed_label.text = time_passed_text

        # Calculate estimate time remaining based on time passed and percent completed
        if float(percent_status_label.text[:-1]) == 0.0:
            time_remaining_text = "Time Remaining: ? seconds"
        else:
            time_remaining = (time_passed / (float(percent_status_label.text[:-1])/100)) - time_passed
            if time_remaining < 60:
                time_remaining_text = "Time Remaining: %d seconds" % time_remaining
            elif time_remaining < 3600:
                time_remaining_text = "Time Remaining: %d minutes, %d seconds" % \
                                      (time_remaining/60, time_remaining % 60)
            elif time_remaining < 86400:
                time_remaining_text = "Time Remaining: %d hours, %d minutes, %d seconds" % \
                                      (time_remaining/3600, time_remaining % 3600 / 60, time_remaining % 60)
            else:
                time_remaining_text = "Time Remaining: %d days, %d hours, %d minutes, %d seconds" % \
                                      (time_remaining/86400, time_remaining % 86400 / 3600,
                                       time_remaining % 3600 / 60, time_remaining % 60)
        time_left_label.text = time_remaining_text

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

        elif 'update_prices' in settings:
            if settings['update_prices']:
                # Stop the current process
                if stop_btn.title == 'Stop':
                    if update_price_process.is_alive():
                        update_btn_func()
                        update_price_process.terminate()
                    # Update message and button
                    stop_btn.title = "Back"
                    main_status_label.text = 'Download stopped. Price updates not saved.'
                    update_btn.enabled = 0
                    status_window.become_target()

                # Change pages
                elif stop_btn.title in ['Back', 'Done']:
                    # Go to the next page
                    if win_next is not None:
                        # Go to next window
                        stuff = 0
                        """if win_next == 'FilesMenu':
                            FilesMenu.open_files_menu(status_window.x, status_window.y, db_dict, settings)
                            status_window.hide()"""

                    # Go to the previous page
                    elif win_previous is not None:
                        win_previous.show()
                        status_window.hide()

        status_window.become_target()

    # ========== Buttons ==========
    update_btn = Button("Current Status",
                        x=(status_window.width - 2*button_width - button_spacing) / 2,
                        y=time_left_label.bottom + 10,
                        height=button_height, width=button_width, font=button_font, action=update_btn_func,
                        style='default', color=button_color, just='right')
    display_list.append(update_btn)

    stop_btn = Button("Stop", x=update_btn.right + button_spacing, y=update_btn.top,
                      height=button_height, width=button_width, font=button_font, action=stop_btn_func,
                      style='default', color=button_color, just='right')
    display_list.append(stop_btn)

    # Get current time for the start time of the process
    start_time = time.time()

    # ========== Start team creation in new process ==========
    if create_ultimate_teams_title in win_previous.title:
        multiprocessing.Process(target=create_teams, args=(db_dict, file_name)).start()

        title.text = "Creating Ultimate Teams..."

    # ========== Start player downloading in new process ==========
    elif "Download Player Database" in win_previous.title:
        title.text = "Downloading Player Database..."

        queue = multiprocessing.Queue()
        download_process = multiprocessing.Process(target=download_and_save_player_db,
                                                   args=(queue, file_name, get_prices))
        download_process.start()

    # ========== Start updating player prices in new process ==========
    elif 'update_prices' in settings:
        if settings['update_prices']:
            title.text = "Updating '%s' Player Prices..." % file_name

            queue = multiprocessing.Queue()
            update_price_process = multiprocessing.Process(target=update_player_prices,
                                                           args=(queue, file_name, settings))
            update_price_process.start()

    # ========== Add components to view and add view to window ==========
    for msg in display_list:
        view.add(msg)

    status_window.add(view)
    view.become_target()
    status_window.show()
