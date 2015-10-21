from GUI import Button, Geometry, Image, Label, View, Window

from AppConfig import *
import SearchMenu
import TeamsMenu
import FilesMenu


def open_start_menu(window_x, window_y, db_dict):

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
            image_pos = (search_btn.bottom + top_border, (win_start.width - start_window_image.width)/2)
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
    search_btn.y = title.bottom + title_border
    search_btn.height = button_height
    search_btn.width = button_width
    search_btn.font = button_font
    search_btn.action = search_btn_func
    search_btn.style = 'default'
    search_btn.color = button_color
    search_btn.just = 'right'

    teams_btn.x = button_spacing + search_btn.right
    teams_btn.y = title.bottom + title_border
    teams_btn.height = button_height
    teams_btn.width = button_width
    teams_btn.font = button_font
    teams_btn.action = teams_btn_func
    teams_btn.style = 'default'
    teams_btn.color = button_color
    teams_btn.just = 'right'

    files_btn.x = button_spacing + teams_btn.right
    files_btn.y = title.bottom + title_border
    files_btn.height = button_height
    files_btn.width = button_width
    files_btn.font = button_font
    files_btn.action = files_btn_func
    files_btn.style = 'default'
    files_btn.color = button_color
    files_btn.just = 'right'

    # ========== Add components to view and add view to window ==========
    view.add(title)
    view.add(search_btn)
    view.add(teams_btn)
    view.add(files_btn)

    win_start.add(view)
    view.become_target()
    win_start.show()
