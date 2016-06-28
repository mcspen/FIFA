from GUI import Button, Label, View, Window
from AppConfig import *
import AssignPlayers


def open_pick_formation_window(window_x, window_y, db_dict, win_previous):

    general_display = []

    # ========== Window ==========
    win_pick_formation = Window()
    win_pick_formation.title = pick_formation_win_title
    win_pick_formation.auto_position = False
    win_pick_formation.position = (window_x, window_y)
    win_pick_formation.size = (win_width, win_height)
    win_pick_formation.resizable = 0
    win_pick_formation.name = enter_text_title + " Window"
    win_pick_formation.show()

    # ========== Window Image View ==========
    class StartWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

    view = StartWindowImageView(size=win_pick_formation.size)

    # ========== Title ==========
    title = Label(text=pick_formation_title)
    title.font = title_font
    title.width = title_width
    title.height = title_height
    title.x = (win_pick_formation.width - title_width) / 2
    title.y = top_border
    title.color = title_color
    title.just = 'center'
    general_display.append(title)

    # ========== Button Functions ==========
    def formation_btn_func(formation):
        win_pick_formation.become_target()
        AssignPlayers.open_assign_players_window(win_pick_formation.x, win_pick_formation.y,
                                                 db_dict, formation, win_pick_formation)
        win_pick_formation.hide()

    def any_formation_btn_func():
        win_pick_formation.become_target()
        win_pick_formation.hide()

    def back_btn_func():
        win_pick_formation.become_target()
        win_previous.show()
        win_pick_formation.hide()

    # ========== Formation Button Declarations ==========
    formation_button_width = 200
    msg_y = title.bottom

    for formation in db_dict['formation_db'][1].db:
        formation_btn = Button(title=formation['name'],
                                  font=std_tf_font,
                                  width=formation_button_width, height=std_tf_height,
                                  x=(win_pick_formation.width - formation_button_width)/2, y=msg_y,
                                  action=(formation_btn_func, formation))
        general_display.append(formation_btn)

        msg_y += std_tf_height + 1

    msg_y += 9

    any_formation_btn = Button(title='Any Formation',
                               font=std_tf_font,
                               width=formation_button_width, height=std_tf_height,
                               x=(win_pick_formation.width - formation_button_width)/2, y=msg_y,
                               action=any_formation_btn_func)
    general_display.append(any_formation_btn)

    msg_y += std_tf_height + 10

    back_btn = Button('Back',
                      font=std_tf_font_bold,
                      width=button_width, height=button_height,
                      x=(win_pick_formation.width - button_width)/2, y=msg_y,
                      action=back_btn_func)
    general_display.append(back_btn)

    # ========== Add buttons to window ==========
    for item in general_display:
        view.add(item)

    win_pick_formation.add(view)
    view.become_target()
    win_pick_formation.show()
