from GUI import Button, Geometry, Image, Label, RadioButton, RadioGroup, View, Window

from AppConfig import *
import SearchMenu
import TeamsMenu
import FilesMenu
import json


def open_start_menu(window_x, window_y, db_dict):

    view_item_list = []

    # Load console type
    settings = {'console_type': ''}
    with open('configs.json', 'r') as f:
        settings["console_type"] = json.load(f)['console_type']
        f.close()

    # ========== Window ==========
    win_start = Window()
    win_start.title = start_win_title
    win_start.auto_position = False
    win_start.position = (window_x, window_y)
    win_start.size = (win_width, win_height)
    win_start.resizable = 0
    win_start.name = start_title + " Window"

    # ========== Window Image View ==========
    class StartWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)
            image_pos = ((win_start.width - start_window_image.width)/2, search_btn.bottom + title_border)
            src_rect = start_window_image.bounds
            dst_rect = Geometry.offset_rect(src_rect, image_pos)
            start_window_image.draw(c, src_rect, dst_rect)

    view = StartWindowImageView(size=win_start.size)

    # ========== Start Window Image ==========
    start_window_image = Image(file='Images/start_menu_image.jpg')

    # ========== Title ==========
    title = Label(text=start_title)
    title.font = title_font
    title.width = title_width
    title.height = title_height
    title.x = (win_width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'
    view_item_list.append(title)

    # ========== Sort Order Radio Buttons ==========
    def save_console_type():
        """
        Save the console type
        """

        # Load configurations
        with open('configs.json', 'r') as config_file:
            configurations = json.load(config_file)
            config_file.close()

        # Edit configurations
        configurations['console_type'] = settings["console_type"]

        # Save the settings
        with open('configs.json', 'w') as config_file:
            json.dump(configurations, config_file)
            config_file.close()

    def get_attribute_console_rg():
        settings["console_type"] = console_radio_group.value
        win_start.become_target()
        save_console_type()

    console_radio_group = RadioGroup(action=get_attribute_console_rg)

    console_radio_btn_width = 75
    console_label_width = 80
    radio_btn_space = 5

    console_rg_label = Label(text="Sort Order:", font=std_tf_font, width=console_label_width, height=std_tf_height,
                            color=title_color)
    console_rg_label.x = (win_start.width - 2 * console_radio_btn_width - radio_btn_space - console_label_width) / 2
    console_rg_label.y = title.bottom + radio_btn_space
    view_item_list.append(console_rg_label)

    playstation_radio_btn = RadioButton("PlayStation")
    playstation_radio_btn.width = console_radio_btn_width
    playstation_radio_btn.x = console_rg_label.right
    playstation_radio_btn.y = console_rg_label.top
    playstation_radio_btn.group = console_radio_group
    playstation_radio_btn.value = 'PLAYSTATION'
    view_item_list.append(playstation_radio_btn)

    xbox_radio_btn = RadioButton("Xbox")
    xbox_radio_btn.width = console_radio_btn_width
    xbox_radio_btn.x = playstation_radio_btn.right + radio_btn_space
    xbox_radio_btn.y = playstation_radio_btn.top
    xbox_radio_btn.group = console_radio_group
    xbox_radio_btn.value = 'XBOX'
    view_item_list.append(xbox_radio_btn)

    if settings["console_type"] in ['PLAYSTATION', 'XBOX']:
        console_radio_group.value = settings["console_type"]
    else:
        print "Invalid console type."

    # ========== Button Declarations ==========
    search_btn = Button("Search")
    teams_btn = Button("Teams")
    files_btn = Button("Files")

    button_list = [search_btn,
                   teams_btn,
                   files_btn]

    # ========== Button Functions ==========
    def search_btn_func():
        win_start.hide()
        SearchMenu.open_search_menu(win_start.x, win_start.y, db_dict)

    def teams_btn_func():
        win_start.hide()
        TeamsMenu.open_teams_menu(win_start.x, win_start.y, db_dict)

    def files_btn_func():
        win_start.hide()
        FilesMenu.open_files_menu(win_start.x, win_start.y, db_dict)

    # ========== Buttons ==========
    search_btn.x = (win_width - len(button_list)*button_width - (len(button_list)-1)*button_spacing) / 2
    search_btn.y = console_rg_label.bottom + title_border
    search_btn.height = button_height
    search_btn.width = button_width
    search_btn.font = button_font
    search_btn.action = search_btn_func
    search_btn.style = 'default'
    search_btn.color = button_color
    search_btn.just = 'right'
    view_item_list.append(search_btn)

    teams_btn.x = button_spacing + search_btn.right
    teams_btn.y = search_btn.top
    teams_btn.height = button_height
    teams_btn.width = button_width
    teams_btn.font = button_font
    teams_btn.action = teams_btn_func
    teams_btn.style = 'default'
    teams_btn.color = button_color
    teams_btn.just = 'right'
    view_item_list.append(teams_btn)

    files_btn.x = button_spacing + teams_btn.right
    files_btn.y = search_btn.top
    files_btn.height = button_height
    files_btn.width = button_width
    files_btn.font = button_font
    files_btn.action = files_btn_func
    files_btn.style = 'default'
    files_btn.color = button_color
    files_btn.just = 'right'
    view_item_list.append(files_btn)

    # ========== Add components to view and add view to window ==========
    for item in view_item_list:
        view.add(item)

    win_start.add(view)
    view.become_target()
    win_start.show()
