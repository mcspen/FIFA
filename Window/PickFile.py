from GUI import Button, Label, View, Window
from AppConfig import *
import FilesMenu
import EnterText
import EditMenu
import ConfirmPrompt
import CreateUltimateTeams
import SearchMenu
import StatusWindow
from Logic.PlayerDB import PlayerDB
from Logic.FormationDB import FormationDB
from Logic.TeamDB import TeamDB
from Logic import HelperFunctions
import json
from os import listdir


def open_pick_file_window(window_x, window_y, db_dict, settings):

    # ========== Window ==========
    win_pick_file = Window()
    win_pick_file.title = pick_file_win_title
    win_pick_file.auto_position = False
    win_pick_file.position = (window_x, window_y)
    win_pick_file.size = (win_width, win_height)
    win_pick_file.resizable = 0
    win_pick_file.name = pick_file_title + " Window"
    win_pick_file.show()

    # ========== Window Image View ==========
    class StartWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = StartWindowImageView(size=win_pick_file.size)

    display_list = []

    file_type = settings['file_type']

    # ========== Title ==========
    title = Label(text=pick_file_title)
    title.font = title_font
    title.width = title_width
    title.height = title_height
    title.x = (win_width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'
    display_list.append(title)

    # ========== Sub Title ==========
    def get_sub_title_text():
        if file_type == 'default_player_db':
            text = "default player database"
        elif file_type == 'default_player_list':
            text = "default player list"
        elif file_type == 'default_formation_db':
            text = "default formation database"
        elif file_type == 'default_formation_list':
            text = "default formation list"
        elif file_type == 'default_team_list':
            text = "default team list"
        elif file_type == 'current_player_db':
            text = "current player database"
        elif file_type == 'current_player_list':
            text = "current player list"
        elif file_type == 'current_formation_db':
            text = "current formation database"
        elif file_type == 'current_formation_list':
            text = "current formation list"
        elif file_type == 'current_team_list':
            text = "current team list"
        else:
            text = "a"
        return text

    sub_title = Label(font=title_font_2, width=title_width, height=title_height,
                      x=(win_pick_file.width-title_width)/2, y=title.bottom, color=title_color, just='center')
    sub_title_text = get_sub_title_text()
    sub_title.text = "Select %s file:" % sub_title_text
    display_list.append(sub_title)

    # ========== Display Files ==========
    def display_files():
        file_prefix = HelperFunctions.get_file_prefix(file_type)

        # Get corresponding file names
        all_files = listdir('JSONs/')
        file_list = []
        # Truncate file paths to just the names
        for filename in all_files:
            if filename[:8] == file_prefix:
                filename = filename[8:]
                filename = filename[:-5]
                file_list.append(filename)

        # Button Functions
        def select_file_func(file_name):

            # Save new default to config file
            if file_type[:7] == 'default':
                # Load configs
                configs = {}
                with open('configs.json', 'r') as config_file:
                    configs = json.load(config_file)
                    config_file.close()

                # Assign new file name to config
                configs['default_databases'][file_type[8:]] = file_name

                # Save configs
                with open('configs.json', 'w') as config_file:
                    json.dump(configs, config_file)
                    config_file.close()

            # Load db to db_dict
            elif file_type[:7] == 'current':

                if file_type[8:12] == 'play':
                    load_db = PlayerDB()
                elif file_type[8:12] == 'form':
                    load_db = FormationDB()
                elif file_type[8:12] == 'team':
                    load_db = TeamDB()
                else:
                    load_db = PlayerDB()
                    print "File type is invalid."

                if file_type[-2:] == 'db':
                    load_file_type = 'db'
                elif file_type[-4:] == 'list':
                    load_file_type = 'list'
                else:
                    load_file_type = 'Invalid'

                # Load db
                load_db.load(file_name, load_file_type)

                # Assign db to db_dict
                db_dict[file_type[8:]] = (file_name, load_db)

            else:
                print "File type is invalid."

            # Enable back button
            settings['file_changes'] = False
            settings['file_index'] = 0

            if settings['prev_window'] == 'team_creation':
                CreateUltimateTeams.open_create_ultimate_teams_window(
                    win_pick_file.x, win_pick_file.y, db_dict, settings['prev_window_value'],
                    file_name=settings['create_team_name'], roster=settings['roster'],
                    input_formation=settings['input_formation'])
            elif settings['prev_window'] == 'search':
                SearchMenu.open_search_menu(win_pick_file.x, win_pick_file.y, db_dict,
                                            settings['attr_dict'], settings['attr_list'], settings)
            else:
                FilesMenu.open_files_menu(win_pick_file.x, win_pick_file.y, db_dict, settings)
            win_pick_file.hide()

        def rename_file_func(file_name):
            # Get new name
            EnterText.open_enter_text_window(win_pick_file.x, win_pick_file.y, db_dict, settings,
                                             'rename', fill_text=file_name, file_prefix=file_prefix)
            settings['file_changes'] = True
            win_pick_file.hide()

        def edit_file_func(file_name):
            if file_type[8:12] == 'play':
                settings['edit_subject'] = 'players'
            elif file_type[8:12] == 'form':
                settings['edit_subject'] = 'formations'
            elif file_type[8:12] == 'team':
                settings['edit_subject'] = 'teams'
            else:
                print "Invalid file type."

            settings['file_name'] = file_name

            EditMenu.open_edit_menu(win_pick_file.x, win_pick_file.y, db_dict, settings=settings)
            settings['file_changes'] = True
            win_pick_file.hide()

        def update_prices_func(file_name):
            win_pick_file.become_target()
            # Open status window to start updating player prices
            settings['update_prices'] = True
            StatusWindow.open_status_window(win_pick_file.x, win_pick_file.y,
                                            db_dict, file_name, settings=settings, win_previous=win_pick_file)
            settings['file_changes'] = True
            win_pick_file.hide()

        def duplicate_file_func(file_name):
            # Get name for duplicate file and create
            EnterText.open_enter_text_window(win_pick_file.x, win_pick_file.y, db_dict, settings,
                                             'duplicate', fill_text=file_name, file_prefix=file_prefix)
            win_pick_file.hide()

        def delete_file_func(file_name):
            file_path = 'JSONs/' + file_prefix + file_name + '.json'
            ConfirmPrompt.open_confirm_prompt_window(win_pick_file.x, win_pick_file.y,
                                                     db_dict, settings, file_path, file_name)
            win_pick_file.hide()

        # Display appropriate files
        small_file_button_width = 75
        file_y = sub_title.bottom + small_button_top_spacing
        if file_type[:7] == 'default':
            file_x = (win_width - file_btn_width) / 2
        elif file_type[-2:] == 'db' and file_type[8:-3] == 'formation':
            file_x = (win_width - file_btn_width - 3*small_file_button_width - 3*file_btn_spacing) / 2
        elif (file_type[-2:] == 'db' and file_type[8:-3] == 'player') or \
             (file_type[-4:] == 'list' and file_type[8:-5] == 'formation'):
            file_x = (win_width - file_btn_width - 4*small_file_button_width - 4*file_btn_spacing) / 2
        else:
            file_x = (win_width - file_btn_width - 5*small_file_button_width - 5*file_btn_spacing) / 2

        if 'file_index' not in settings:
            settings['file_index'] = 0

        files_per_page = 10
        file_index = settings['file_index']

        # Previous page button function
        def previous_btn_func():
            settings['file_index'] -= files_per_page
            win_pick_file.hide()
            open_pick_file_window(win_pick_file.x, win_pick_file.y, db_dict, settings)

        # Next page button function
        def next_btn_func():
            settings['file_index'] += files_per_page
            win_pick_file.hide()
            open_pick_file_window(win_pick_file.x, win_pick_file.y, db_dict, settings)

        # Previous page button
        previous_btn = Button('<<< Previous Page', height=small_button_height, width=file_btn_width,
                          font=small_button_font, action=previous_btn_func, style='default',
                          x=(win_pick_file.width - 2*file_btn_width - button_spacing)/2, y=file_y,
                          color=small_button_color, just='center')
        display_list.append(previous_btn)

        if file_index < 1:
            previous_btn.enabled = 0

        # Next page button
        next_btn = Button('Next Page >>>', height=small_button_height, width=file_btn_width,
                          font=small_button_font, action=next_btn_func, style='default',
                          x=previous_btn.right + button_spacing, y=file_y,
                          color=small_button_color, just='center')
        display_list.append(next_btn)

        if file_index + files_per_page >= len(file_list):
            next_btn.enabled = 0

        file_y += top_border*2

        for filename in file_list[file_index:file_index + files_per_page]:

            # Select file button with name
            file_btn = Button(filename, height=small_button_height, width=file_btn_width,
                              font=small_button_font, action=(select_file_func, filename), style='default',
                              x=file_x, y=file_y,
                              color=small_button_color, just='center')

            # Rename file button
            rename_btn = Button('Rename', height=small_button_height, width=small_file_button_width,
                                font=small_button_font, action=(rename_file_func, filename), style='default',
                                x=file_btn.right + file_btn_spacing, y=file_y,
                                color=small_button_color, just='center')

            # Edit file button
            edit_btn = Button('Edit', height=small_button_height, width=small_file_button_width,
                              font=small_button_font, action=(edit_file_func, filename), style='default',
                              x=rename_btn.right + file_btn_spacing, y=file_y,
                              color=small_button_color, just='center')
            if file_type[8:12] == 'team':
                edit_btn.enabled = 0

            # Update prices button
            update_prices_btn = Button('Update Prices', height=small_button_height, width=small_file_button_width,
                                       font=small_button_font, action=(update_prices_func, filename), style='default',
                                       x=edit_btn.right + file_btn_spacing, y=file_y,
                                       color=small_button_color, just='center')

            # Duplicate file button
            duplicate_btn = Button('Duplicate', height=small_button_height, width=small_file_button_width,
                                   font=small_button_font, action=(duplicate_file_func, filename), style='default',
                                   x=update_prices_btn.right + file_btn_spacing, y=file_y,
                                   color=small_button_color, just='center')

            # Delete file button
            delete_btn = Button('Delete', height=small_button_height, width=small_file_button_width,
                                font=small_button_font, action=(delete_file_func, filename), style='default',
                                x=duplicate_btn.right + file_btn_spacing, y=file_y,
                                color=small_button_color, just='center')

            # Reposition buttons based on those being shown
            if 'db' in file_type and 'formation' in file_type:
                duplicate_btn.x = rename_btn.right + file_btn_spacing
                delete_btn.x = duplicate_btn.right + file_btn_spacing
            elif 'db' in file_type:
                update_prices_btn.x = rename_btn.right + file_btn_spacing
                duplicate_btn.x = update_prices_btn.right + file_btn_spacing
                delete_btn.x = duplicate_btn.right + file_btn_spacing
            elif 'list' in file_type and 'formation' in file_type:
                duplicate_btn.x = edit_btn.right + file_btn_spacing
                delete_btn.x = duplicate_btn.right + file_btn_spacing

            # Display buttons according to file type
            display_list.append(file_btn)
            if 'current' in file_type:
                display_list.append(rename_btn)
                if 'list' in file_type:
                    display_list.append(edit_btn)
                if 'player' in file_type or 'team' in file_type:
                    display_list.append(update_prices_btn)
                display_list.append(duplicate_btn)
                display_list.append(delete_btn)

            file_y += small_button_height + 3*file_btn_spacing

    # ========== Back Button Declaration ==========
    back_btn = Button("Back")

    def back_btn_func():
        settings['file_index'] = 0

        if settings['prev_window'] == 'team_creation':
            CreateUltimateTeams.open_create_ultimate_teams_window(
                win_pick_file.x, win_pick_file.y, db_dict, settings['prev_window_value'],
                file_name=settings['create_team_name'], roster=settings['roster'],
                input_formation=settings['input_formation'])
        elif settings['prev_window'] == 'search':
            SearchMenu.open_search_menu(win_pick_file.x, win_pick_file.y, db_dict,
                                        settings['attr_dict'], settings['attr_list'], settings)
        else:
            FilesMenu.open_files_menu(win_pick_file.x, win_pick_file.y, db_dict, settings)
        win_pick_file.hide()

    # ========== Back Button ==========
    back_btn.x = (win_width - button_width) / 2
    back_btn.y = win_pick_file.height - 70
    back_btn.height = button_height
    back_btn.width = button_width
    back_btn.font = button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = button_color
    back_btn.just = 'right'
    if settings['file_changes']:
        back_btn.enabled = 0
    else:
        back_btn.enabled = 1

    display_list.append(back_btn)

    display_files()

    # ========== Add buttons to window ==========
    for item in display_list:
        view.add(item)

    win_pick_file.add(view)
    view.become_target()
    win_pick_file.show()
