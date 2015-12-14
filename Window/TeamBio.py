from GUI import Button, Geometry, Image, Label, View, Window
from AppConfig import *
import json
from Logic.HelperFunctions import ascii_text, format_attr_name, convert_height, convert_weight, format_birthday,\
    save_image, save_small_image, get_file_prefix
from Logic import PlayerDB
from Logic import Team
from Window import PlayerBio


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
    player_border = 2
    player_box_width = 120 + player_border*2
    player_box_height = 120 + player_border*2
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
            # Iterate through players on team
            for sym, pos in team['formation']['positions'].iteritems():

                position_coordinates = team_spacing[sym]

                # Iterate through links of player
                for link in pos['links']:
                    colors = [red, orange, yellow, green]
                    color_num = Team.Team.teammate_chemistry(pos['player'],
                                                             team['formation']['positions'][link]['player'])
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
                """c.forecolor = darker
                c.fill_rect((dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+player_border,
                             dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+player_border,
                             dst_rect[0]+position_coordinates[0]*x_space+player_box_width/2-player_border,
                             dst_rect[1]+position_coordinates[1]*y_space+player_box_height/2-player_border))"""

    view = StartWindowImageView(size=win_team_bio.size)

    # ========== Player Headshots ==========
    player_headshots = []
    name_height = 25

    # Player headshots
    class HeadshotImageView(View):
        def draw(self, c, r):
            dst_rect = (field_x_offset, field_y_offset, field_x_offset+field_width, field_y_offset+field_length)

            for sym, position in team['formation']['positions'].iteritems():
                # Get player information
                player = position['player']
                position_coordinates = team_spacing[sym]

                # Card color box
                c.forecolor = quality_color(position['player']['color'])
                c.fill_rect((dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2,
                             dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2,
                             dst_rect[0]+position_coordinates[0]*x_space+player_box_width/2,
                             dst_rect[1]+position_coordinates[1]*y_space+player_box_height/2-name_height))

                # Darker box for positions
                c.forecolor = darker
                c.fill_rect((dst_rect[0]+position_coordinates[0]*x_space-player_box_width/5-2*player_border,
                             dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+player_border,
                             dst_rect[0]+position_coordinates[0]*x_space+player_box_width/2-player_border,
                             dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+name_height-4))

                # Headshot
                image_url = player['headshotImgUrl']
                ratio = 0.65
                image_file_name = player['id'] + '_' + str(ratio)
                image_file_name = save_small_image(image_url, image_file_name, ratio)
                player_headshot = Image(file=image_file_name)
                headshot_pos = ((dst_rect[0]+position_coordinates[0]*x_space +
                                 player_box_width/2-player_headshot.size[0]-player_border,
                                 dst_rect[1]+position_coordinates[1]*y_space +
                                 player_box_height/2-player_border-name_height-player_headshot.size[1]))
                headshot_rect = player_headshot.bounds
                headshot_dst_rect = Geometry.offset_rect(headshot_rect, headshot_pos)
                player_headshot.draw(c, headshot_rect, headshot_dst_rect)

                # Club
                image_url = player['club']['imageUrls']['normal']['large']
                ratio = 0.75
                image_file_name = 'club_' + str(player['club']['id']) + '_' + str(ratio)
                image_file_name = save_small_image(image_url, image_file_name, ratio)
                club_image = Image(file=image_file_name)
                club_image_pos = ((dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+player_border,
                                   headshot_pos[1]+player_headshot.size[1]/6))
                headshot_rect = club_image.bounds
                headshot_dst_rect = Geometry.offset_rect(headshot_rect, club_image_pos)
                club_image.draw(c, headshot_rect, headshot_dst_rect)

                # Nation
                image_url = player['nation']['imageUrls']['large']
                ratio = 0.75
                image_file_name = 'nation_' + str(player['nation']['id']) + '_' + str(ratio)
                image_file_name = save_small_image(image_url, image_file_name, ratio)
                nation_image = Image(file=image_file_name)
                nation_image_pos = ((dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+player_border,
                                     club_image_pos[1]+club_image.size[1]+5))
                headshot_rect = nation_image.bounds
                headshot_dst_rect = Geometry.offset_rect(headshot_rect, nation_image_pos)
                nation_image.draw(c, headshot_rect, headshot_dst_rect)

    player_headshots.append(HeadshotImageView(size=(int(field_x_offset+field_width+5),
                                                    int(field_y_offset+field_length+5))))

    # Player ratings, position, team, nation, and name
    rating_width = 30
    position_width = 45
    for sym, position in team['formation']['positions'].iteritems():
        # Get player information
        player = position['player']
        position_coordinates = team_spacing[sym]
        info_color = black  # quality_text_color(position['player']['color'])

        # Player rating
        rating_label = Label(text=str(player['rating']), font=title_font_3,
                             width=rating_width, height=title_height,
                             x=int(dst_rect[0]+position_coordinates[0]*x_space-player_box_height/2+2*player_border),
                             y=int(dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2)-1,
                             color=info_color, just='left')
        player_headshots.append(rating_label)

        # Player Position
        colors = [red, orange, yellow, dark_green]
        position_color = colors[Team.Team.position_chemistry(player['position'], position['symbol'])]
        position_label = Label(text=position['symbol'], font=std_tf_font_bold,
                               width=position_width, height=std_tf_height,
                               x=int(dst_rect[0]+position_coordinates[0]*x_space+player_box_height/2-
                                     2*player_border-2*position_width),
                               y=int(dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2)+player_border,
                               color=position_color, just='right')
        player_headshots.append(position_label)

        # Formation Position
        position_color = white
        position_label = Label(text='/'+player['position'], font=std_tf_font_bold,
                               width=position_width, height=std_tf_height,
                               x=int(dst_rect[0]+position_coordinates[0]*x_space+player_box_height/2-
                                     2*player_border-position_width),
                               y=int(dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2)+player_border,
                               color=position_color, just='left')
        player_headshots.append(position_label)

        # Player name button
        def name_btn_func(current_player):
            win_team_bio.hide()
            PlayerBio.open_player_bio_window(win_team_bio.x, win_team_bio.y, current_player, win_team_bio)
            win_team_bio.become_target()

        name_color = darker
        player_name = ascii_text(player['name'])
        name_btn = Button(title=player_name, font=title_font_5,
                           width=player_box_width-4*player_border, height=name_height,
                           x=int(dst_rect[0]+position_coordinates[0]*x_space-player_box_height/2+2*player_border),
                           y=int(dst_rect[1]+position_coordinates[1]*y_space +
                                 player_box_height/2-player_border-name_height),
                           color=name_color, just='center',
                            action=(name_btn_func, player))
        # Make font smaller for long names
        if len(player_name) > 11:
            name_btn.font = title_font_8
        if len(player_name) > 14:
            name_btn.font = title_font_9
        player_headshots.append(name_btn)

    def display_headshots():
        for item in player_headshots:
            view.add(item)
        win_team_bio.become_target()

    def hide_headshots():
        for item in player_headshots:
            view.remove(item)
        win_team_bio.become_target()

    # ========== Player Summary Stats ==========
    summary_stats = []

    attr_title_label_width = 30
    attr_label_width = 20
    attribute_x_offset = 30

    for sym, position in team['formation']['positions'].iteritems():
        # Get player information
        player = position['player']
        position_coordinates = team_spacing[sym]
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-attribute_x_offset+3)
        label_y = int(dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+player_border)

        for idx, attr in enumerate(player['attributes']):
            if idx == 3:
                label_x += 2*attribute_x_offset
                label_y = int(dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+player_border)

            stat_title_label = Label(font=small_tf_font, width=attr_title_label_width, height=std_tf_height,
                                     x=label_x-attr_title_label_width, y=label_y, color=title_color, just='right')
            stat_title_label.text = format_attr_name(attr['name'][-3:]) + ':'
            summary_stats.append(stat_title_label)

            color = attr_color(attr['value'])

            stat_label = Label(font=small_tf_font, width=attr_label_width, height=std_tf_height,
                               x=label_x, y=label_y, color=color, just='right')
            stat_label.text = str(attr['value'])
            summary_stats.append(stat_label)

            label_y += std_tf_height

    def display_summary_stats():
        for stat in summary_stats:
            view.add(stat)
        win_team_bio.become_target()

    def hide_summary_stats():
        for stat in summary_stats:
            view.remove(stat)
        win_team_bio.become_target()

    # ========== Button Declarations ==========
    next_trait_btn = Button("Next Trait")
    back_btn = Button("Back")

    # ========== Button Functions ==========
    def next_trait_btn_func():
        hide_headshots()
        display_summary_stats()
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

    display_headshots()

    win_team_bio.add(view)
    view.become_target()
    win_team_bio.show()
