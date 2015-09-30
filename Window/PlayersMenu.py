from GUI import Button, Label, View, Window

from AppConfig import *
import StartMenu


def open_players_menu(window_x, window_y, db_dict):

    # ========== Window ==========
    win_players = Window()
    win_players.title = players_win_title
    win_players.auto_position = False
    win_players.position = (window_x, window_y)
    win_players.size = (win_width, win_height)
    win_players.resizable = 0
    win_players.name = "Players Window"

    # ========== Window Image View ==========
    class FormationsWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = FormationsWindowImageView(size=win_players.size)

    # ========== Title ==========
    title = Label(text=players_title)
    title.font = title_font
    title.width = players_title_width
    title.height = title_height
    title.x = (win_width - players_title_width) / 2
    title.y = top_border
    title.color = title_color

    # ========== Messages ==========
    start_message = Label(text=start_message_text)
    start_message.font = start_message_font
    start_message.width = start_message_width
    start_message.height = start_message_height
    start_message.x = (win_width - start_message_width) / 2
    start_message.y = (win_height - start_message_height) / 2
    start_message.color = start_message_color

    # ========== Button Toolbar Declarations ==========
    search_players_btn = Button("Search Players")
    create_players_list_btn = Button("Create Players List")
    load_players_list_btn = Button("Load Players List")
    save_players_list_btn = Button("Save Players List")
    edit_players_list_btn = Button("Edit Players List")
    delete_players_list_btn = Button("Delete Players List")
    back_btn = Button("Back")

    button_list = [search_players_btn,
                   create_players_list_btn,
                   load_players_list_btn,
                   save_players_list_btn,
                   edit_players_list_btn,
                   delete_players_list_btn,
                   back_btn]

    # ========== Button Toolbar Functions ==========
    def search_players_btn_func():
        for btn in button_list:
            btn.enabled = 1
        search_players_btn.enabled = 0
        view.remove(start_message)
        #StartMenu.open_start_menu(win_players.left, win_players.top)
        #win_players.hide()

    def create_players_list_btn_func():
        for btn in button_list:
            btn.enabled = 1
        create_players_list_btn.enabled = 0
        view.remove(start_message)
        #StartMenu.open_start_menu(win_players.left, win_players.top)
        #win_players.hide()

    def load_players_list_btn_func():
        for btn in button_list:
            btn.enabled = 1
        load_players_list_btn.enabled = 0
        view.remove(start_message)
        #StartMenu.open_start_menu(win_players.left, win_players.top)
        #win_players.hide()

    def save_players_list_btn_func():
        for btn in button_list:
            btn.enabled = 1
        save_players_list_btn.enabled = 0
        view.remove(start_message)
        #StartMenu.open_start_menu(win_players.left, win_players.top)
        #win_players.hide()

    def edit_players_list_btn_func():
        for btn in button_list:
            btn.enabled = 1
        edit_players_list_btn.enabled = 0
        view.remove(start_message)
        #StartMenu.open_start_menu(win_players.left, win_players.top)
        #win_players.hide()

    def delete_players_list_btn_func():
        for btn in button_list:
            btn.enabled = 1
        delete_players_list_btn.enabled = 0
        view.remove(start_message)
        #StartMenu.open_start_menu(win_players.left, win_players.top)
        #win_players.hide()

    def back_btn_func():
        StartMenu.open_start_menu(win_players.x, win_players.y, db_dict)
        win_players.hide()

    # ========== Toolbar Buttons ==========
    search_players_btn.x = (win_width - len(button_list)*small_button_width
                            - (len(button_list)-1)*small_button_spacing) / 2
    search_players_btn.y = title.bottom + small_button_top_spacing
    search_players_btn.height = small_button_height
    search_players_btn.width = small_button_width
    search_players_btn.font = small_button_font
    search_players_btn.action = search_players_btn_func
    search_players_btn.style = 'default'
    search_players_btn.color = small_button_color
    search_players_btn.just = 'right'

    create_players_list_btn.x = search_players_btn.right + small_button_spacing
    create_players_list_btn.y = search_players_btn.top
    create_players_list_btn.height = small_button_height
    create_players_list_btn.width = small_button_width
    create_players_list_btn.font = small_button_font
    create_players_list_btn.action = create_players_list_btn_func
    create_players_list_btn.style = 'default'
    create_players_list_btn.color = small_button_color
    create_players_list_btn.just = 'right'

    load_players_list_btn.x = create_players_list_btn.right + small_button_spacing
    load_players_list_btn.y = search_players_btn.top
    load_players_list_btn.height = small_button_height
    load_players_list_btn.width = small_button_width
    load_players_list_btn.font = small_button_font
    load_players_list_btn.action = load_players_list_btn_func
    load_players_list_btn.style = 'default'
    load_players_list_btn.color = small_button_color
    load_players_list_btn.just = 'right'

    save_players_list_btn.x = load_players_list_btn.right + small_button_spacing
    save_players_list_btn.y = search_players_btn.top
    save_players_list_btn.height = small_button_height
    save_players_list_btn.width = small_button_width
    save_players_list_btn.font = small_button_font
    save_players_list_btn.action = save_players_list_btn_func
    save_players_list_btn.style = 'default'
    save_players_list_btn.color = small_button_color
    save_players_list_btn.just = 'right'

    edit_players_list_btn.x = save_players_list_btn.right + small_button_spacing
    edit_players_list_btn.y = search_players_btn.top
    edit_players_list_btn.height = small_button_height
    edit_players_list_btn.width = small_button_width
    edit_players_list_btn.font = small_button_font
    edit_players_list_btn.action = edit_players_list_btn_func
    edit_players_list_btn.style = 'default'
    edit_players_list_btn.color = small_button_color
    edit_players_list_btn.just = 'right'

    delete_players_list_btn.x = edit_players_list_btn.right + small_button_spacing
    delete_players_list_btn.y = search_players_btn.top
    delete_players_list_btn.height = small_button_height
    delete_players_list_btn.width = small_button_width
    delete_players_list_btn.font = small_button_font
    delete_players_list_btn.action = delete_players_list_btn_func
    delete_players_list_btn.style = 'default'
    delete_players_list_btn.color = small_button_color
    delete_players_list_btn.just = 'right'

    back_btn.x = delete_players_list_btn.right + small_button_spacing
    back_btn.y = search_players_btn.top
    back_btn.height = small_button_height
    back_btn.width = small_button_width
    back_btn.font = small_button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = small_button_color
    back_btn.just = 'right'

    # ========== Add components to view and add view to window ==========
    view.add(title)
    view.add(search_players_btn)
    view.add(create_players_list_btn)
    view.add(load_players_list_btn)
    view.add(save_players_list_btn)
    view.add(edit_players_list_btn)
    view.add(delete_players_list_btn)
    view.add(back_btn)
    view.add(start_message)

    win_players.add(view)
    view.become_target()
    win_players.show()
