from GUI import Button, Geometry, Image, Label, View, Window
from AppConfig import *
import json
from Logic.HelperFunctions import ascii_text, format_attr_name, convert_height, convert_weight, format_birthday,\
    save_image, get_file_prefix
from Logic import PlayerDB
from Logic import Team


def open_team_bio_window(window_x, window_y, team, win_previous, file_name, current_list):

    # ========== Window ==========
    win_team_bio = Window()
    win_team_bio.title = team_bio_win_title
    win_team_bio.auto_position = False
    win_team_bio.position = (window_x, window_y)
    win_team_bio.size = (win_width, win_height)
    win_team_bio.resizable = 0
    win_team_bio.name = team_bio_title + " Window"
    win_team_bio.show()

    # ========== Load Formation Spacing ==========
    # Get attribute lists
    with open('configs.json', 'r') as f:
        team_spacing = json.load(f)['team_coordinates'][team['formation']['name']]
        f.close()

    labels_list = []

    # ========== Field Ratio ==========
    y_to_x_ratio = 0.825

    # Line specification
    line_color = white
    line_size = 2

    # Field
    field_color = dark_green
    field_length = 680
    field_width = field_length*y_to_x_ratio

    # Field positioning on screen
    field_x_offset = (win_team_bio.width - field_width - button_width - 100) / 2
    field_y_offset = title_border

    # Center circle
    center_spot_x = field_x_offset + field_width/2
    center_spot_y = field_y_offset + field_length/2
    circle_radius = int(field_length/10)

    # Goal box
    penalty_spot_height = int(field_length*12/100)
    eighteen_box_height = int(field_length*18/100)
    eighteen_box_width = int(field_length*44/100)
    six_box_height = int(field_length*6/100)
    six_box_width = int(field_length*20/100)

    # Corner semi circles
    corner_semi_circle_radius = int(field_length*2/100)

    # ========== Player Spacing Values ==========
    x_space = int(field_width/20)
    y_space = int(field_length/24)
    player_box_width = 130
    player_box_height = 130
    link_size = 10

    # ========== Window Image View ==========
    image_pos = (field_x_offset, field_y_offset)
    src_rect = (0, 0, field_width, field_length)
    dst_rect = Geometry.offset_rect(src_rect, image_pos)

    class StartWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

            # Field and sidelines
            c.forecolor = field_color
            c.fill_rect((dst_rect[0]-5, dst_rect[1]-5, dst_rect[2]+5, dst_rect[3]+5))
            c.forecolor = line_color
            c.fill_rect((dst_rect[0], dst_rect[1], dst_rect[2], dst_rect[3]))
            c.forecolor = field_color
            c.fill_rect((dst_rect[0]+line_size, dst_rect[1]+line_size, dst_rect[2]-line_size, dst_rect[3]-line_size))

            # Center circle, center spot, and half-way line
            c.forecolor = line_color
            c.fill_oval((center_spot_x-circle_radius, center_spot_y-circle_radius,
                         center_spot_x+circle_radius, center_spot_y+circle_radius))
            c.forecolor = field_color
            c.fill_oval((center_spot_x-circle_radius+line_size, center_spot_y-circle_radius+line_size,
                         center_spot_x+circle_radius-line_size, center_spot_y+circle_radius-line_size))
            c.forecolor = line_color
            c.fill_rect((dst_rect[0], center_spot_y-line_size/2, dst_rect[2], center_spot_y+line_size/2))
            c.fill_oval((center_spot_x-line_size*2, center_spot_y-line_size*2,
                         center_spot_x+line_size*2, center_spot_y+line_size*2))

            # Goal box semi circle
            c.forecolor = line_color
            c.fill_oval((center_spot_x-circle_radius, dst_rect[1]+penalty_spot_height-circle_radius,
                         center_spot_x+circle_radius, dst_rect[1]+penalty_spot_height+circle_radius))
            c.fill_oval((center_spot_x-circle_radius, dst_rect[3]-penalty_spot_height-circle_radius,
                         center_spot_x+circle_radius, dst_rect[3]-penalty_spot_height+circle_radius))
            c.forecolor = field_color
            c.fill_oval((center_spot_x-circle_radius+line_size,
                         dst_rect[1]+penalty_spot_height-circle_radius+line_size,
                         center_spot_x+circle_radius-line_size,
                         dst_rect[1]+penalty_spot_height+circle_radius-line_size))
            c.fill_oval((center_spot_x-circle_radius+line_size,
                         dst_rect[3]-penalty_spot_height-circle_radius+line_size,
                         center_spot_x+circle_radius-line_size,
                         dst_rect[3]-penalty_spot_height+circle_radius-line_size))

            # Eighteen yard box
            c.forecolor = line_color
            c.fill_rect((center_spot_x-eighteen_box_width/2, dst_rect[1],
                         center_spot_x+eighteen_box_width/2, dst_rect[1]+eighteen_box_height))
            c.fill_rect((center_spot_x-eighteen_box_width/2, dst_rect[3]-eighteen_box_height,
                         center_spot_x+eighteen_box_width/2, dst_rect[3]))
            c.forecolor = field_color
            c.fill_rect((center_spot_x-eighteen_box_width/2+line_size,
                         dst_rect[1]+line_size,
                         center_spot_x+eighteen_box_width/2-line_size,
                         dst_rect[1]+eighteen_box_height-line_size))
            c.fill_rect((center_spot_x-eighteen_box_width/2+line_size,
                         dst_rect[3]-eighteen_box_height+line_size,
                         center_spot_x+eighteen_box_width/2-line_size,
                         dst_rect[3]-line_size))

            # Penalty spot
            c.forecolor = line_color
            c.fill_oval((center_spot_x-line_size*2, dst_rect[1]+six_box_height*2-line_size*2,
                         center_spot_x+line_size*2, dst_rect[1]+six_box_height*2+line_size*2))
            c.fill_oval((center_spot_x-line_size*2, dst_rect[3]-six_box_height*2-line_size*2,
                         center_spot_x+line_size*2, dst_rect[3]-six_box_height*2+line_size*2))

            # Six yard box
            c.forecolor = line_color
            c.fill_rect((center_spot_x-six_box_width/2, dst_rect[1],
                         center_spot_x+six_box_width/2, dst_rect[1]+six_box_height))
            c.fill_rect((center_spot_x-six_box_width/2, dst_rect[3]-six_box_height,
                         center_spot_x+six_box_width/2, dst_rect[3]))
            c.forecolor = field_color
            c.fill_rect((center_spot_x-six_box_width/2+line_size,
                         dst_rect[1]+line_size,
                         center_spot_x+six_box_width/2-line_size,
                         dst_rect[1]+six_box_height-line_size))
            c.fill_rect((center_spot_x-six_box_width/2+line_size,
                         dst_rect[3]-six_box_height+line_size,
                         center_spot_x+six_box_width/2-line_size,
                         dst_rect[3]-line_size))

            # Corner circles
            c.forecolor = line_color
            c.stroke_arc((dst_rect[0]+1, dst_rect[1]), corner_semi_circle_radius, 0, 90)
            c.frame_arc((dst_rect[2], dst_rect[1]), corner_semi_circle_radius, 90, 180)
            c.stroke_arc((dst_rect[0]+1, dst_rect[3]-line_size), corner_semi_circle_radius, 270, 0)
            c.frame_arc((dst_rect[2], dst_rect[3]-line_size), corner_semi_circle_radius, 180, 270)

            # Links
            for sym, pos in team['formation']['positions'].iteritems():

                position_coordinates = team_spacing[sym]

                for link in pos['links']:
                    colors = [red, orange, yellow, green]
                    color_num = Team.Team.teammate_chemistry(pos['player'],
                                                             team['formation']['positions'][symbol]['player'])
                    c.forecolor = colors[color_num]
                    link_coordinates = team_spacing[link]

                    # Determine line direction to decide which points to use
                    change_y = (link_coordinates[1]-position_coordinates[1])*y_space
                    change_x = (link_coordinates[0]-position_coordinates[0])*x_space+0.0001
                    ratio = change_y/change_x

                    # Horizontal width line
                    if abs(ratio) >= 1:
                        c.fill_poly([(int(dst_rect[0]+position_coordinates[0]*x_space)-link_size/2,
                                      int(dst_rect[1]+position_coordinates[1]*y_space)),
                                     (int(dst_rect[0]+position_coordinates[0]*x_space)+link_size/2,
                                      int(dst_rect[1]+position_coordinates[1]*y_space)),
                                     (int(dst_rect[0]+link_coordinates[0]*x_space+link_size/2),
                                      int(dst_rect[1]+link_coordinates[1]*y_space)),
                                     (int(dst_rect[0]+link_coordinates[0]*x_space-link_size/2),
                                      int(dst_rect[1]+link_coordinates[1]*y_space))])

                    # Vertical width line
                    else:
                        c.fill_poly([(int(dst_rect[0]+position_coordinates[0]*x_space),
                                      int(dst_rect[1]+position_coordinates[1]*y_space)-link_size/2),
                                     (int(dst_rect[0]+position_coordinates[0]*x_space),
                                      int(dst_rect[1]+position_coordinates[1]*y_space)+link_size/2),
                                     (int(dst_rect[0]+link_coordinates[0]*x_space),
                                      int(dst_rect[1]+link_coordinates[1]*y_space)+link_size/2),
                                     (int(dst_rect[0]+link_coordinates[0]*x_space),
                                      int(dst_rect[1]+link_coordinates[1]*y_space)-link_size/2)])

            # Player Markers
            for sym, pos in team['formation']['positions'].iteritems():
                c.forecolor = quality_color(pos['player']['color'])
                position_coordinates = team_spacing[sym]
                c.fill_rect((dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2,
                             dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2,
                             dst_rect[0]+position_coordinates[0]*x_space+player_box_width/2,
                             dst_rect[1]+position_coordinates[1]*y_space+player_box_height/2))

    view = StartWindowImageView(size=win_team_bio.size)

    # DELETE LATER ======================================================================================================================================================================
    # ========== Position Labels ==========
    label_width = player_box_width
    label_height = 35
    pos_label_color = blue

    for symbol, position in team['formation']['positions'].iteritems():
        pos_coordinates = team_spacing[symbol]
        label_x = int(dst_rect[0]+pos_coordinates[0]*x_space-label_width/2)
        label_y = int(dst_rect[1]+pos_coordinates[1]*y_space-label_height/2)

        pos_label = Label(text=position['symbol'],font=title_font_2, width=label_width, height=label_height,
                                 x=label_x, y=label_y, color=pos_label_color, just='center')
        labels_list.append(pos_label)
    # DELETE LATER ======================================================================================================================================================================

    # ========== Button Declarations ==========
    next_trait_btn = Button("Next Trait")
    back_btn = Button("Back")

    # ========== Button Functions ==========
    def next_trait_btn_func():
         win_team_bio.become_target()

    def back_btn_func():
        win_team_bio.hide()
        win_previous.show()

    # ========== Buttons ==========
    button_x_offset = 50

    next_trait_btn.x = win_team_bio.width - button_width - button_x_offset
    next_trait_btn.y = top_border
    next_trait_btn.height = small_button_height
    next_trait_btn.width = button_width
    next_trait_btn.font = small_button_font
    next_trait_btn.action = next_trait_btn_func
    next_trait_btn.style = 'default'
    next_trait_btn.color = small_button_color

    back_btn.x = next_trait_btn.left
    back_btn.y = next_trait_btn.bottom
    back_btn.height = small_button_height
    back_btn.width = button_width
    back_btn.font = small_button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = small_button_color

    """# ========== Name ==========
    team_name_label = Label(text="Rating: " + str(team['rating']), font=title_font,
                                 width=title_width, height=title_height,
                                 x=(win_width - title_width)/2, y=top_border, color=title_color, just='center')
    # Shift title over the field
    team_name_label.x = (win_team_bio.width - title_width - button_width - 100) / 2
    labels_list.append(team_name_label)"""

    # ========== Formation Info Title Label ==========
    info_title = Label(text="Team Info", font=title_font_2,
                             width=title_width, height=title_height,
                             x=next_trait_btn.right - button_width/2 - title_width/2,
                             y=back_btn.bottom + top_border*3,
                             color=title_color, just='center')
    labels_list.append(info_title)

    """# ========== Formation Info Labels ==========
    info_width = 110
    info_label_text = "Style:\n# Links:\n# Attackers:\n# Midfielders:\n# Defenders:"
    info_title_label = Label(text=info_label_text, font=std_tf_font_bold,
                             width=info_width, height=std_tf_height*5,
                             x=next_trait_btn.left - button_x_offset, y=info_title.bottom + title_border,
                             color=title_color, just='right')
    labels_list.append(info_title_label)

    # ========== Formation Info ==========
    info_text = (team['style'] + "\n" + str(team['num_links']) + "\n" + str(team['num_attackers']) +
                 "\n" + str(team['num_midfielders']) + "\n" + str(team['num_defenders']))
    info_label = Label(text=info_text, font=std_tf_font_bold,
                       width=info_width, height=std_tf_height*5,
                       x=info_title_label.right + 10, y=info_title_label.top,
                       color=title_color, just='left')
    labels_list.append(info_label)

    # ========== Description Label ==========
    description_title_label = Label(text="Description:", font=std_tf_font_bold,
                                    width=small_button_width, height=std_tf_height,
                                    x=next_trait_btn.left, y=info_title_label.bottom + top_border,
                                    color=title_color, just='center')
    labels_list.append(description_title_label)

    # ========== Description ==========
    description = team['description']
    description_text = ''
    max_chars = 25
    counter = 0
    for word in description.split():
        counter += len(word) + 1
        description_text += ' ' + word
        if counter >= max_chars:
            description_text += '\n'
            counter = 0
    description_label = Label(text=description_text, font=std_tf_font,
                              width=small_button_width+100, height=std_tf_height*13,
                              x=info_title_label.left, y=description_title_label.bottom + title_border,
                              color=title_color, just='left')
    labels_list.append(description_label)"""

    # ========== Add buttons to window ==========
    view.add(next_trait_btn)
    view.add(back_btn)

    for label in labels_list:
        view.add(label)

    win_team_bio.add(view)
    view.become_target()
    win_team_bio.show()
