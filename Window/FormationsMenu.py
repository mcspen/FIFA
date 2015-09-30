from GUI import Button, Label, View, Window

from AppConfig import *
import StartMenu


def open_formations_menu(window_x, window_y, db_dict):

    # ========== Window ==========
    win_formations = Window()
    win_formations.title = formations_win_title
    win_formations.auto_position = False
    win_formations.position = (window_x, window_y)
    win_formations.size = (win_width, win_height)
    win_formations.resizable = 0
    win_formations.name = "Formations Window"

    # ========== Window Image View ==========
    class FormationsWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = FormationsWindowImageView(size=win_formations.size)

    # ========== Title ==========
    title = Label(text=formations_title)
    title.font = title_font
    title.width = formations_title_width
    title.height = title_height
    title.x = (win_width - formations_title_width) / 2
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
    search_formations_btn = Button("Search Formations")
    create_formations_list_btn = Button("Create Formations List")
    load_formations_list_btn = Button("Load Formations List")
    save_formations_list_btn = Button("Save Formations List")
    edit_formations_list_btn = Button("Edit Formations List")
    delete_formations_list_btn = Button("Delete Formations List")
    back_btn = Button("Back")

    button_list = [search_formations_btn,
                   create_formations_list_btn,
                   load_formations_list_btn,
                   save_formations_list_btn,
                   edit_formations_list_btn,
                   delete_formations_list_btn,
                   back_btn]

    # ========== Button Toolbar Functions ==========
    def search_formations_btn_func():
        for btn in button_list:
            btn.enabled = 1
        search_formations_btn.enabled = 0
        view.remove(start_message)
        #StartMenu.open_start_menu(win_players.left, win_players.top)
        #win_players.hide()

    def create_formations_list_btn_func():
        for btn in button_list:
            btn.enabled = 1
        create_formations_list_btn.enabled = 0
        view.remove(start_message)
        #StartMenu.open_start_menu(win_players.left, win_players.top)
        #win_players.hide()

    def load_formations_list_btn_func():
        for btn in button_list:
            btn.enabled = 1
        load_formations_list_btn.enabled = 0
        view.remove(start_message)
        #StartMenu.open_start_menu(win_players.left, win_players.top)
        #win_players.hide()

    def save_formations_list_btn_func():
        for btn in button_list:
            btn.enabled = 1
        save_formations_list_btn.enabled = 0
        view.remove(start_message)
        #StartMenu.open_start_menu(win_players.left, win_players.top)
        #win_players.hide()

    def edit_formations_list_btn_func():
        for btn in button_list:
            btn.enabled = 1
        edit_formations_list_btn.enabled = 0
        view.remove(start_message)
        #StartMenu.open_start_menu(win_players.left, win_players.top)
        #win_players.hide()

    def delete_formations_list_btn_func():
        for btn in button_list:
            btn.enabled = 1
        delete_formations_list_btn.enabled = 0
        view.remove(start_message)
        #StartMenu.open_start_menu(win_players.left, win_players.top)
        #win_players.hide()

    def back_btn_func():
        StartMenu.open_start_menu(win_formations.x, win_formations.y, db_dict)
        win_formations.hide()

    # ========== Toolbar Buttons ==========
    search_formations_btn.x = (win_width - len(button_list)*small_button_width
                               - (len(button_list)-1)*small_button_spacing) / 2
    search_formations_btn.y = title.bottom + small_button_top_spacing
    search_formations_btn.height = small_button_height
    search_formations_btn.width = small_button_width
    search_formations_btn.font = small_button_font
    search_formations_btn.action = search_formations_btn_func
    search_formations_btn.style = 'default'
    search_formations_btn.color = small_button_color
    search_formations_btn.just = 'right'

    create_formations_list_btn.x = search_formations_btn.right + small_button_spacing
    create_formations_list_btn.y = search_formations_btn.top
    create_formations_list_btn.height = small_button_height
    create_formations_list_btn.width = small_button_width
    create_formations_list_btn.font = small_button_font
    create_formations_list_btn.action = create_formations_list_btn_func
    create_formations_list_btn.style = 'default'
    create_formations_list_btn.color = small_button_color
    create_formations_list_btn.just = 'right'

    load_formations_list_btn.x = create_formations_list_btn.right + small_button_spacing
    load_formations_list_btn.y = search_formations_btn.top
    load_formations_list_btn.height = small_button_height
    load_formations_list_btn.width = small_button_width
    load_formations_list_btn.font = small_button_font
    load_formations_list_btn.action = load_formations_list_btn_func
    load_formations_list_btn.style = 'default'
    load_formations_list_btn.color = small_button_color
    load_formations_list_btn.just = 'right'

    save_formations_list_btn.x = load_formations_list_btn.right + small_button_spacing
    save_formations_list_btn.y = search_formations_btn.top
    save_formations_list_btn.height = small_button_height
    save_formations_list_btn.width = small_button_width
    save_formations_list_btn.font = small_button_font
    save_formations_list_btn.action = save_formations_list_btn_func
    save_formations_list_btn.style = 'default'
    save_formations_list_btn.color = small_button_color
    save_formations_list_btn.just = 'right'

    edit_formations_list_btn.x = save_formations_list_btn.right + small_button_spacing
    edit_formations_list_btn.y = search_formations_btn.top
    edit_formations_list_btn.height = small_button_height
    edit_formations_list_btn.width = small_button_width
    edit_formations_list_btn.font = small_button_font
    edit_formations_list_btn.action = edit_formations_list_btn_func
    edit_formations_list_btn.style = 'default'
    edit_formations_list_btn.color = small_button_color
    edit_formations_list_btn.just = 'right'

    delete_formations_list_btn.x = edit_formations_list_btn.right + small_button_spacing
    delete_formations_list_btn.y = search_formations_btn.top
    delete_formations_list_btn.height = small_button_height
    delete_formations_list_btn.width = small_button_width
    delete_formations_list_btn.font = small_button_font
    delete_formations_list_btn.action = delete_formations_list_btn_func
    delete_formations_list_btn.style = 'default'
    delete_formations_list_btn.color = small_button_color
    delete_formations_list_btn.just = 'right'

    back_btn.x = delete_formations_list_btn.right + small_button_spacing
    back_btn.y = search_formations_btn.top
    back_btn.height = small_button_height
    back_btn.width = small_button_width
    back_btn.font = small_button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = small_button_color
    back_btn.just = 'right'

    # ========== Add components to view and add view to window ==========
    view.add(title)
    view.add(search_formations_btn)
    view.add(create_formations_list_btn)
    view.add(load_formations_list_btn)
    view.add(save_formations_list_btn)
    view.add(edit_formations_list_btn)
    view.add(delete_formations_list_btn)
    view.add(back_btn)
    view.add(start_message)

    win_formations.add(view)
    view.become_target()
    win_formations.show()