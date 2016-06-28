from GUI import Button, Geometry, Image, Label, View, Window
from AppConfig import *
import json
import operator
from Logic.HelperFunctions import ascii_text, format_attr_name, save_small_image, text_add_new_lines
from Logic import Team
import PlayerBio


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

            # Player Card Box Backgrounds
            for sym, pos in team['formation']['positions'].iteritems():
                position_coordinates = team_spacing[sym]
                player = pos['player']
                box_file_name = 'Images/Cards/' + player['color'] + '_box.png'
                box_image = Image(file=box_file_name)
                box_pos = ((dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2,
                             dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2))
                box_rect = box_image.bounds
                box_dst_rect = Geometry.offset_rect(box_rect, box_pos)
                box_image.draw(c, box_rect, box_dst_rect)

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
                club_rect = club_image.bounds
                club_dst_rect = Geometry.offset_rect(club_rect, club_image_pos)
                club_image.draw(c, club_rect, club_dst_rect)

                # Nation
                image_url = player['nation']['imageUrls']['large']
                ratio = 0.75
                image_file_name = 'nation_' + str(player['nation']['id']) + '_' + str(ratio)
                image_file_name = save_small_image(image_url, image_file_name, ratio)
                nation_image = Image(file=image_file_name)
                nation_image_pos = (club_image_pos[0], club_image_pos[1]+club_image.size[1]+5)
                nation_rect = nation_image.bounds
                nation_dst_rect = Geometry.offset_rect(nation_rect, nation_image_pos)
                nation_image.draw(c, nation_rect, nation_dst_rect)

    player_headshots.append(HeadshotImageView(size=(int(field_x_offset+field_width+5),
                                                    int(field_y_offset+field_length+5))))

    # Player ratings, position, team, nation, and name
    rating_width = 30
    position_width = 45
    for sym, position in team['formation']['positions'].iteritems():
        # Get player information
        player = position['player']
        position_coordinates = team_spacing[sym]
        info_color = quality_text_color(position['player']['color'])

        # Player rating
        rating_label = Label(text=str(player['rating']), font=title_font_3,
                             width=rating_width, height=title_height,
                             x=int(dst_rect[0]+position_coordinates[0]*x_space-player_box_height/2+2*player_border),
                             y=int(dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2)-1,
                             color=info_color, just='left')
        player_headshots.append(rating_label)

        # Player Position
        colors = [red, dark_orange, yellow, dark_green]
        position_color = colors[Team.Team.position_chemistry(player['position'], position['symbol'])]
        position_label = Label(text=player['position'], font=std_tf_font_bold,
                               width=position_width, height=std_tf_height,
                               x=int(dst_rect[0]+position_coordinates[0]*x_space+player_box_height/2 -
                                     2*player_border-2*position_width),
                               y=int(dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2)+player_border,
                               color=position_color, just='right')
        player_headshots.append(position_label)

        # Formation Position
        position_color = white
        position_label = Label(text='/'+position['symbol'], font=std_tf_font_bold,
                               width=position_width, height=std_tf_height,
                               x=int(dst_rect[0]+position_coordinates[0]*x_space+player_box_height/2 -
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
        if len(player_name) > 10:
            name_btn.font = title_font_8
        if len(player_name) > 13:
            name_btn.font = title_font_9
        if len(player_name) > 15:
            name_btn.font = title_font_10
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

    # Darker box to display stats on
    class StatsBoxImageView(View):
        def draw(self, c, r):
            dst_rect = (field_x_offset, field_y_offset, field_x_offset+field_width, field_y_offset+field_length)

            for sym, position in team['formation']['positions'].iteritems():
                # Get player coordinates
                position_coordinates = team_spacing[sym]

                # Darker box to display stats
                c.forecolor = darker
                c.fill_rect((dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+player_border,
                             dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+player_border,
                             dst_rect[0]+position_coordinates[0]*x_space+player_box_width/2-player_border,
                             dst_rect[1]+position_coordinates[1]*y_space+player_box_height/2-player_border))

    summary_stats.append(StatsBoxImageView(size=(int(field_x_offset+field_width+5),
                                                 int(field_y_offset+field_length+5))))

    attr_title_label_width = 30
    attr_label_width = 20
    attribute_x_offset = 30

    for sym, position in team['formation']['positions'].iteritems():
        # Get player information
        player = position['player']
        position_coordinates = team_spacing[sym]
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+2*player_border)
        label_y = int(dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+2*player_border)

        # Player rating
        rating_summary_width = 25
        rating_summary_label = Label(text=str(player['rating']), font=title_font_5,
                                     width=rating_summary_width, height=std_tf_height,
                                     x=label_x, y=label_y, just='right')
        rating_summary_label.color = attr_color(player['rating'])
        summary_stats.append(rating_summary_label)

        # Player name
        label_x = rating_summary_label.right
        name_summary_label = Label(text=ascii_text(player['name']), font=std_tf_font_bold,
                                   width=player_box_width-rating_summary_width-2*player_border, height=std_tf_height,
                                   x=label_x, y=label_y, color=white, just='center')
        if len(ascii_text(player['name'])) > 10:
            name_summary_label.font = title_font_9
            name_summary_label.y += 2
        if len(ascii_text(player['name'])) > 13:
            name_summary_label.font = title_font_11
            name_summary_label.y += 2
        if len(ascii_text(player['name'])) > 15:
            name_summary_label.font = title_font_13
            name_summary_label.y += 2
        summary_stats.append(name_summary_label)

        # Summary Stats
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-attribute_x_offset+3)
        label_y = rating_summary_label.bottom + player_border

        for idx, attr in enumerate(player['attributes']):
            if idx == 3:
                label_x += 2*attribute_x_offset
                label_y = rating_summary_label.bottom

            stat_title_label = Label(font=small_tf_font, width=attr_title_label_width, height=std_tf_height,
                                     x=label_x-attr_title_label_width, y=label_y, color=title_color, just='right')
            stat_title_label.text = format_attr_name(attr['name'][-3:]) + ':'
            summary_stats.append(stat_title_label)

            color = attr_color(attr['value'])

            stat_label = Label(font=small_tf_font, width=attr_label_width, height=std_tf_height,
                               x=label_x, y=label_y, color=color, just='right')
            stat_label.text = str(attr['value'])
            summary_stats.append(stat_label)

            label_y += std_tf_height - 5

        # Weak foot label
        label_y += 5
        star_label_width = 70
        star_width = 35
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-star_label_width) + 15
        weak_foot_label = Label(text="Weak Foot: ", font=small_tf_font,
                            width=star_label_width, height=std_tf_height,
                            x=label_x, y=label_y,
                            color=title_color, just='right')
        summary_stats.append(weak_foot_label)

        # Weak foot stars label
        colors = [red, dark_orange, yellow, light_green, dark_green]
        star_color = colors[player['weakFoot']-1]
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space) + 15
        weak_foot_stars_label = Label(font=small_tf_font,
                                  width=star_width, height=std_tf_height,
                                  x=label_x, y=label_y,
                                  color=star_color, just='left')
        weak_foot_stars_label.text = '*'*player['weakFoot']
        summary_stats.append(weak_foot_stars_label)

        label_y += std_tf_height - 5

        # Skill moves label
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-star_label_width) + 15
        skill_label = Label(text="Skill Moves: ", font=small_tf_font,
                            width=star_label_width, height=std_tf_height,
                            x=label_x, y=label_y,
                            color=title_color, just='right')
        summary_stats.append(skill_label)

        # Skill moves stars label
        colors = [red, dark_orange, yellow, light_green, dark_green]
        star_color = colors[player['skillMoves']-1]
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space) + 15
        skill_stars_label = Label(font=small_tf_font,
                                  width=star_width, height=std_tf_height,
                                  x=label_x, y=label_y,
                                  color=star_color, just='left')
        skill_stars_label.text = '*'*player['skillMoves']
        summary_stats.append(skill_stars_label)

        label_y += std_tf_height - 4

        # Price label
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+player_border)
        price_label = Label(text="Price: %d" % player['price'], font=small_tf_font,
                            width=player_box_width-2*player_border, height=std_tf_height,
                            x=label_x, y=label_y,
                            color=title_color, just='center')
        summary_stats.append(price_label)

    def display_summary_stats():
        for stat in summary_stats:
            view.add(stat)
        win_team_bio.become_target()

    def hide_summary_stats():
        for stat in summary_stats:
            view.remove(stat)
        win_team_bio.become_target()

    # ========== Player Strength Stats ==========
    strength_stats = []
    num_strengths = 6

    # Darker box to display stats on
    class StrengthsBoxImageView(View):
        def draw(self, c, r):
            dst_rect = (field_x_offset, field_y_offset, field_x_offset+field_width, field_y_offset+field_length)

            for sym, position in team['formation']['positions'].iteritems():
                # Get player coordinates
                position_coordinates = team_spacing[sym]

                # Darker box to display stats
                c.forecolor = darker
                c.fill_rect((dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+player_border,
                             dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+player_border,
                             dst_rect[0]+position_coordinates[0]*x_space+player_box_width/2-player_border,
                             dst_rect[1]+position_coordinates[1]*y_space+player_box_height/2-player_border))

    strength_stats.append(StrengthsBoxImageView(size=(int(field_x_offset+field_width+5),
                                                      int(field_y_offset+field_length+5))))

    for sym, position in team['formation']['positions'].iteritems():
        # Get player information
        player = position['player']
        position_coordinates = team_spacing[sym]
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+2*player_border)
        label_y = int(dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+2*player_border)

        # Player rating
        rating_summary_width = 25
        rating_summary_label = Label(text=str(player['rating']), font=title_font_5,
                                     width=rating_summary_width, height=std_tf_height,
                                     x=label_x, y=label_y, just='right')
        rating_summary_label.color = attr_color(player['rating'])
        strength_stats.append(rating_summary_label)

        # Player name
        label_x = rating_summary_label.right
        name_summary_label = Label(text=ascii_text(player['name']), font=std_tf_font_bold,
                                   width=player_box_width-rating_summary_width-2*player_border, height=std_tf_height,
                                   x=label_x, y=label_y, color=white, just='center')
        if len(ascii_text(player['name'])) > 10:
            name_summary_label.font = title_font_9
            name_summary_label.y += 2
        if len(ascii_text(player['name'])) > 13:
            name_summary_label.font = title_font_11
            name_summary_label.y += 2
        if len(ascii_text(player['name'])) > 15:
            name_summary_label.font = title_font_13
            name_summary_label.y += 2
        strength_stats.append(name_summary_label)

        # Strength Label
        strength_label_width = 2*player_box_width/3-5
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-strength_label_width+25)
        label_y = rating_summary_label.bottom + player_border

        strength_labels = Label(font=smallest_tf_font,
                                width=strength_label_width,
                                height=std_tf_height*num_strengths,
                                x=label_x, y=label_y, color=white, just='right')

        skip_list = ['itemType', 'color', 'playerType', 'headshotImgUrl', 'quality', 'commonName', 'name', 'firstName',
                     'positionFull', 'foot', 'position', 'atkWorkRate', 'defWorkRate', 'modelName', 'lastName',
                     'playStyle', 'birthdate', 'id', 'specialities', 'traits', 'attributes', 'club', 'nation', 'league',
                     'headshot', 'baseId', 'height', 'skillMoves', 'weakFoot', 'isSpecialType', 'isGK', 'weight',
                     'rating', 'potential', 'price']
        sorted_attributes = sorted(player.items(), key=operator.itemgetter(1), reverse=True)

        strength_text = ''
        index = 0
        for strength in sorted_attributes:
            if strength[0] not in skip_list:
                strength_text += format_attr_name(strength[0]) + ':\n'
                index += 1
                if index == num_strengths:
                    break

        strength_labels.text = strength_text[:-1]
        strength_stats.append(strength_labels)

        # Strength Stat Label
        label_x = strength_labels.right + 3

        strength_stat_labels = Label(font=smallest_tf_font,
                                     width=player_box_width-strength_label_width-2*player_border,
                                     height=std_tf_height*num_strengths,
                                     x=label_x, y=label_y, color=white, just='left')

        strength_stat_text = ''
        index = 0
        for strength in sorted_attributes:
            if strength[0] not in skip_list:
                strength_stat_text += str(strength[1]) + '\n'
                index += 1
                if index == num_strengths:
                    break

        strength_stat_labels.text = strength_stat_text[:-1]
        strength_stats.append(strength_stat_labels)

    def display_strength_stats():
        for stat in strength_stats:
            view.add(stat)
        win_team_bio.become_target()

    def hide_strength_stats():
        for stat in strength_stats:
            view.remove(stat)
        win_team_bio.become_target()

    # ========== Player Traits ==========
    traits_list = []

    # Darker box to display stats on
    class TraitsBoxImageView(View):
        def draw(self, c, r):
            dst_rect = (field_x_offset, field_y_offset, field_x_offset+field_width, field_y_offset+field_length)

            for sym, position in team['formation']['positions'].iteritems():
                # Get player coordinates
                position_coordinates = team_spacing[sym]

                # Darker box to display stats
                c.forecolor = darker
                c.fill_rect((dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+player_border,
                             dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+player_border,
                             dst_rect[0]+position_coordinates[0]*x_space+player_box_width/2-player_border,
                             dst_rect[1]+position_coordinates[1]*y_space+player_box_height/2-player_border))

    traits_list.append(TraitsBoxImageView(size=(int(field_x_offset+field_width+5),
                                                int(field_y_offset+field_length+5))))

    for sym, position in team['formation']['positions'].iteritems():
        # Get player information
        player = position['player']
        position_coordinates = team_spacing[sym]
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+2*player_border)
        label_y = int(dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+2*player_border)

        # Player rating
        rating_summary_width = 25
        rating_summary_label = Label(text=str(player['rating']), font=title_font_5,
                                     width=rating_summary_width, height=std_tf_height,
                                     x=label_x, y=label_y, just='right')
        rating_summary_label.color = attr_color(player['rating'])
        traits_list.append(rating_summary_label)

        # Player name
        label_x = rating_summary_label.right
        name_summary_label = Label(text=ascii_text(player['name']), font=std_tf_font_bold,
                                   width=player_box_width-rating_summary_width-2*player_border, height=std_tf_height,
                                   x=label_x, y=label_y, color=white, just='center')
        if len(ascii_text(player['name'])) > 10:
            name_summary_label.font = title_font_9
            name_summary_label.y += 2
        if len(ascii_text(player['name'])) > 13:
            name_summary_label.font = title_font_11
            name_summary_label.y += 2
        if len(ascii_text(player['name'])) > 15:
            name_summary_label.font = title_font_13
            name_summary_label.y += 2
        traits_list.append(name_summary_label)

        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+2*player_border)
        label_y = rating_summary_label.bottom + player_border

        # Traits Label
        traits_label = Label(font=smallest_tf_font,
                             width=player_box_width-4*player_border,
                             x=label_x, y=label_y, just='center')

        if player['traits'] is not None:
            traits_stat_text = ''
            for trait in player['traits']:
                if trait == 'Avoids Using Weaker Foot':
                    trait_text = 'Avoids Weaker Foot'
                elif trait == 'Tries To Beat Defensive Line':
                    trait_text = 'Tries To Beat Def. Line'
                elif trait == 'Takes Powerful Driven Free Kicks':
                    trait_text = 'Pwrful Driven Free Kicks'
                elif '-' in trait:
                    hyphen_index = trait.index('-')
                    trait_text = trait[hyphen_index+2:]
                else:
                    trait_text = trait
                traits_stat_text += trait_text + '\n'

            if len(player['traits']) > 5:
                traits_stat_text += str(len(player['traits'])-5) + ' More Not Shown' + '\n'

            traits_label.text = traits_stat_text[:-1]
            traits_label.color = dark_green
            traits_label.height = std_tf_height*len(player['traits'])

        else:
            traits_label.text = 'No Traits'
            traits_label.color = red
            traits_label.height = std_tf_height

        traits_list.append(traits_label)

    def display_traits():
        for stat in traits_list:
            view.add(stat)
        win_team_bio.become_target()

    def hide_traits():
        for stat in traits_list:
            view.remove(stat)
        win_team_bio.become_target()

    # ========== Player Specialities ==========
    specialities_list = []

    # Darker box to display stats on
    class SpecialitiesBoxImageView(View):
        def draw(self, c, r):
            dst_rect = (field_x_offset, field_y_offset, field_x_offset+field_width, field_y_offset+field_length)

            for sym, position in team['formation']['positions'].iteritems():
                # Get player coordinates
                position_coordinates = team_spacing[sym]

                # Darker box to display stats
                c.forecolor = darker
                c.fill_rect((dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+player_border,
                             dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+player_border,
                             dst_rect[0]+position_coordinates[0]*x_space+player_box_width/2-player_border,
                             dst_rect[1]+position_coordinates[1]*y_space+player_box_height/2-player_border))

    specialities_list.append(SpecialitiesBoxImageView(size=(int(field_x_offset+field_width+5),
                                                            int(field_y_offset+field_length+5))))

    for sym, position in team['formation']['positions'].iteritems():
        # Get player information
        player = position['player']
        position_coordinates = team_spacing[sym]
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+2*player_border)
        label_y = int(dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+2*player_border)

        # Player rating
        rating_summary_width = 25
        rating_summary_label = Label(text=str(player['rating']), font=title_font_5,
                                     width=rating_summary_width, height=std_tf_height,
                                     x=label_x, y=label_y, just='right')
        rating_summary_label.color = attr_color(player['rating'])
        specialities_list.append(rating_summary_label)

        # Player name
        label_x = rating_summary_label.right
        name_summary_label = Label(text=ascii_text(player['name']), font=std_tf_font_bold,
                                   width=player_box_width-rating_summary_width-2*player_border, height=std_tf_height,
                                   x=label_x, y=label_y, color=white, just='center')
        if len(ascii_text(player['name'])) > 10:
            name_summary_label.font = title_font_9
            name_summary_label.y += 2
        if len(ascii_text(player['name'])) > 13:
            name_summary_label.font = title_font_11
            name_summary_label.y += 2
        if len(ascii_text(player['name'])) > 15:
            name_summary_label.font = title_font_13
            name_summary_label.y += 2
        specialities_list.append(name_summary_label)

        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+2*player_border)
        label_y = rating_summary_label.bottom + player_border

        # Specialities Label
        specialities_label = Label(font=smallest_tf_font,
                                   width=player_box_width-4*player_border,
                                   x=label_x, y=label_y, color=white, just='center')

        if player['specialities'] is not None:
            specialities_text = ''
            for speciality in player['specialities'][:5]:
                if speciality == 'Avoids Using Weaker Foot':
                    speciality_text = 'Avoids Weaker Foot'
                elif '-' in speciality:
                    hyphen_index = speciality.index('-')
                    speciality_text = speciality[hyphen_index+2:]
                else:
                    speciality_text = speciality
                specialities_text += speciality_text + '\n'

            if len(player['specialities']) > 5:
                specialities_text += str(len(player['specialities'])-5) + ' More Not Shown' + '\n'

            specialities_label.text = specialities_text[:-1]
            specialities_label.color = dark_green
            specialities_label.height = std_tf_height*len(player['specialities'])

        else:
            specialities_label.text = 'No Specialities'
            specialities_label.color = red
            specialities_label.height = std_tf_height

        specialities_list.append(specialities_label)

    def display_specialities():
        for stat in specialities_list:
            view.add(stat)
        win_team_bio.become_target()

    def hide_specialities():
        for stat in specialities_list:
            view.remove(stat)
        win_team_bio.become_target()

    # ========== Player Team, League, and Nation ==========
    team_league_nation_list = []

    # Darker box to display stats on and player's club/nation images
    class TeamLeagueNationBoxImageView(View):
        def draw(self, c, r):
            dst_rect = (field_x_offset, field_y_offset, field_x_offset+field_width, field_y_offset+field_length)

            for sym, position in team['formation']['positions'].iteritems():
                # Get player information
                player = position['player']
                position_coordinates = team_spacing[sym]

                # Darker box to display stats
                c.forecolor = darker
                c.fill_rect((dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+player_border,
                             dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+player_border,
                             dst_rect[0]+position_coordinates[0]*x_space+player_box_width/2-player_border,
                             dst_rect[1]+position_coordinates[1]*y_space+player_box_height/2-player_border))

                # Club
                image_url = player['club']['imageUrls']['normal']['large']
                ratio = 0.75
                image_file_name = 'club_' + str(player['club']['id']) + '_' + str(ratio)
                image_file_name = save_small_image(image_url, image_file_name, ratio)
                club_image = Image(file=image_file_name)
                club_image_pos = ((dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+2*player_border,
                                   dst_rect[1]+position_coordinates[1]*y_space-player_box_height/4))
                headshot_rect = club_image.bounds
                headshot_dst_rect = Geometry.offset_rect(headshot_rect, club_image_pos)
                club_image.draw(c, headshot_rect, headshot_dst_rect)

                # Nation
                image_url = player['nation']['imageUrls']['large']
                ratio = 0.75
                image_file_name = 'nation_' + str(player['nation']['id']) + '_' + str(ratio)
                image_file_name = save_small_image(image_url, image_file_name, ratio)
                nation_image = Image(file=image_file_name)
                nation_image_pos = ((club_image_pos[0],
                                     club_image_pos[1]+club_image.size[1]+30))
                headshot_rect = nation_image.bounds
                headshot_dst_rect = Geometry.offset_rect(headshot_rect, nation_image_pos)
                nation_image.draw(c, headshot_rect, headshot_dst_rect)

    team_league_nation_list.append(TeamLeagueNationBoxImageView(size=(int(field_x_offset+field_width+5),
                                                                      int(field_y_offset+field_length+5))))

    for sym, position in team['formation']['positions'].iteritems():
        # Get player information
        player = position['player']
        position_coordinates = team_spacing[sym]
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+2*player_border)
        label_y = int(dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+2*player_border)

        # Player rating
        rating_summary_width = 25
        rating_summary_label = Label(text=str(player['rating']), font=title_font_5,
                                     width=rating_summary_width, height=std_tf_height,
                                     x=label_x, y=label_y, just='right')
        rating_summary_label.color = attr_color(player['rating'])
        team_league_nation_list.append(rating_summary_label)

        # Player name
        label_x = rating_summary_label.right
        name_summary_label = Label(text=ascii_text(player['name']), font=std_tf_font_bold,
                                   width=player_box_width-rating_summary_width-2*player_border, height=std_tf_height,
                                   x=label_x, y=label_y, color=white, just='center')
        if len(ascii_text(player['name'])) > 10:
            name_summary_label.font = title_font_9
            name_summary_label.y += 2
        if len(ascii_text(player['name'])) > 13:
            name_summary_label.font = title_font_11
            name_summary_label.y += 2
        if len(ascii_text(player['name'])) > 15:
            name_summary_label.font = title_font_13
            name_summary_label.y += 2
        team_league_nation_list.append(name_summary_label)

        # League Title Label
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+3*player_border)
        label_y = rating_summary_label.bottom + 45
        league_title_width = 45
        league_title_label = Label(text="League:", font=title_font_11,
                                   width=league_title_width, height=std_tf_height,
                                   x=label_x, y=label_y, color=white, just='left')
        team_league_nation_list.append(league_title_label)

        image_width = 35
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+2*player_border+image_width)
        label_y = rating_summary_label.bottom + 13

        # Club Label
        club_label = Label(font=std_tf_font_bold,
                           width=player_box_width-4*player_border-image_width, height=std_tf_height,
                           x=label_x, y=label_y, color=white, just='center')

        club_text, num_lines, longest_line = text_add_new_lines(ascii_text(player['club']['abbrName']), 11)
        club_label.text = club_text
        club_label.height = num_lines*std_tf_height

        if num_lines > 1:
            club_label.y -= 6
            club_label.font = title_font_9

        if longest_line > 9:
            club_label.font = title_font_9
        if longest_line > 12:
            club_label.font = title_font_11
        team_league_nation_list.append(club_label)

        label_y = rating_summary_label.bottom + 43

        # League Label
        league_label = Label(text=ascii_text(player['league']['abbrName']), font=std_tf_font_bold,
                             width=player_box_width-4*player_border-image_width, height=std_tf_height,
                             x=label_x, y=label_y, color=white, just='center')
        team_league_nation_list.append(league_label)

        label_y = rating_summary_label.bottom + 72

        # Nation Label
        nation_label = Label(font=std_tf_font_bold,
                           width=player_box_width-4*player_border-image_width, height=std_tf_height,
                           x=label_x, y=label_y, color=white, just='center')

        nation_text, num_lines, longest_line = text_add_new_lines(ascii_text(player['nation']['abbrName']), 11)
        nation_label.text = nation_text
        nation_label.height = num_lines*std_tf_height

        if num_lines > 1:
            nation_label.y -= 6
            nation_label.font = title_font_9

        if longest_line > 9:
            nation_label.font = title_font_9
        if longest_line > 12:
            nation_label.font = title_font_11
        team_league_nation_list.append(nation_label)

    def display_team_league_nation():
        for stat in team_league_nation_list:
            view.add(stat)
        win_team_bio.become_target()

    def hide_team_league_nation():
        for stat in team_league_nation_list:
            view.remove(stat)
        win_team_bio.become_target()

    # ========== Chemistry and Links ==========
    chemistry_list = []

    # Darker box to display stats on and Link Lines
    class ChemistryBoxImageView(View):
        def draw(self, c, r):
            dst_rect = (field_x_offset, field_y_offset, field_x_offset+field_width, field_y_offset+field_length)

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

            # Draw darker boxes
            for sym, position in team['formation']['positions'].iteritems():
                # Get player information
                position_coordinates = team_spacing[sym]

                # Darker box to display stats
                c.forecolor = darker
                c.fill_rect((dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+player_border,
                             dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+player_border,
                             dst_rect[0]+position_coordinates[0]*x_space+player_box_width/2-player_border,
                             dst_rect[1]+position_coordinates[1]*y_space+player_box_height/2-player_border))

    chemistry_list.append(ChemistryBoxImageView(size=(int(field_x_offset+field_width+5),
                                                      int(field_y_offset+field_length+5))))

    for sym, position in team['formation']['positions'].iteritems():
        # Get player information
        player = position['player']
        position_coordinates = team_spacing[sym]
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+2*player_border)
        label_y = int(dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+2*player_border)

        # Player rating
        rating_summary_width = 25
        rating_summary_label = Label(text=str(player['rating']), font=title_font_5,
                                     width=rating_summary_width, height=std_tf_height,
                                     x=label_x, y=label_y, just='right')
        rating_summary_label.color = attr_color(player['rating'])
        chemistry_list.append(rating_summary_label)

        # Player name
        label_x = rating_summary_label.right
        name_summary_label = Label(text=ascii_text(player['name']), font=std_tf_font_bold,
                                   width=player_box_width-rating_summary_width-2*player_border, height=std_tf_height,
                                   x=label_x, y=label_y, color=white, just='center')
        if len(ascii_text(player['name'])) > 10:
            name_summary_label.font = title_font_9
            name_summary_label.y += 2
        if len(ascii_text(player['name'])) > 13:
            name_summary_label.font = title_font_11
            name_summary_label.y += 2
        if len(ascii_text(player['name'])) > 15:
            name_summary_label.font = title_font_13
            name_summary_label.y += 2
        chemistry_list.append(name_summary_label)

        chemistry_label_width = 42
        chemistry_info_width = 30
        chemistry_point_width = 33

        # === Position ====
        # Position Label
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+2*player_border)
        label_y = rating_summary_label.bottom + 5
        position_title_label = Label(text="Position:", font=title_font_13,
                                     width=chemistry_label_width, height=std_tf_height,
                                     x=label_x, y=label_y, color=white, just='right')
        chemistry_list.append(position_title_label)

        # Position Stat
        colors = [red, dark_orange, yellow, dark_green]
        position_chem_number = Team.Team.position_chemistry(player['position'], position['symbol'])
        position_color = colors[position_chem_number]
        position_label = Label(text=player['position'] + '\n/' + position['symbol'], font=title_font_13,
                               width=chemistry_info_width, height=std_tf_height*2,
                               x=position_title_label.right + 5, y=label_y-7, color=position_color, just='center')
        chemistry_list.append(position_label)

        # Position Score
        position_tiers = ['Bad', 'Okay', 'Good', 'Perfect']
        position_tier = position_tiers[position_chem_number]
        position_point = Label(text=position_tier, font=title_font_13,
                               width=chemistry_point_width, height=std_tf_height,
                               x=position_label.right + 5, y=label_y, color=position_color, just='center')
        chemistry_list.append(position_point)

        label_y = position_title_label.bottom - 3

        # === Link Chemistry ====
        link_total = 0

        link_label_width = 30
        link_point_width = 40

        for link in position['links']:
            # Link Label
            link_title_label = Label(text=link.upper(), font=title_font_13,
                                         width=link_label_width, height=std_tf_height,
                                         x=label_x, y=label_y, color=white, just='right')
            chemistry_list.append(link_title_label)

            # Link Score
            link_score = Team.Team.teammate_chemistry(player, team['formation']['positions'][link]['player'])
            score_color = colors[link_score]
            link_point = Label(text=str(link_score) + ' match', font=title_font_13,
                                   width=link_point_width, height=std_tf_height,
                                   x=link_title_label.right + 5, y=label_y, color=score_color, just='left')
            chemistry_list.append(link_point)

            link_total += link_score
            label_y = link_title_label.bottom - 9

        # === Link Average ====
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space + 13 + 5)
        label_y = position_title_label.bottom - 3
        avg_title_width = 20
        # Link Average Label
        link_avg_title_label = Label(text='Avg:', font=title_font_13,
                                     width=avg_title_width, height=std_tf_height,
                                     x=label_x, y=label_y, color=white, just='right')
        chemistry_list.append(link_avg_title_label)

        # Link Average Stat
        avg_width = 20
        link_avg = float(link_total)/len(position['links'])
        if link_avg < 0.3:
            link_point_color = red
        elif link_avg < 1:
            link_point_color = dark_orange
        elif link_avg <= 1.6:
            link_point_color = yellow
        else:
            link_point_color = dark_green
        link_avg_label = Label(text=str(link_avg)[:4], font=title_font_13,
                               width=avg_width, height=std_tf_height,
                               x=link_avg_title_label.right + 2, y=label_y,
                               color=link_point_color, just='left')
        chemistry_list.append(link_avg_label)

        # === Position Links Chem Points ====
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space + 13 + 4)
        label_y = link_avg_title_label.bottom - 9
        pl_chem_title_width = 30
        # Position Links Chem Points Label
        pl_chem_title_label = Label(text='Chem:', font=title_font_13,
                                     width=pl_chem_title_width, height=std_tf_height,
                                     x=label_x, y=label_y, color=white, just='right')
        chemistry_list.append(pl_chem_title_label)

        # Position Links Chem Points Stat
        pl_chem_width = 20
        # Calculate Position Links Chemistry
        bad_points = [0, 1, 2, 3]
        okay_points = [1, 3, 5, 6]
        good_points = [2, 5, 8, 9]
        perfect_points = [2, 5, 9, 10]

        if link_avg < 0.3:
            pl_chem_points = bad_points[position_chem_number]
        elif link_avg < 1:
            pl_chem_points = okay_points[position_chem_number]
        elif link_avg <= 1.6:
            pl_chem_points = good_points[position_chem_number]
        else:
            pl_chem_points = perfect_points[position_chem_number]

        # Assign Position Links Chemistry Color
        if pl_chem_points < 4:
            pl_chem_color = red
        elif pl_chem_points < 7:
            pl_chem_color = dark_orange
        elif pl_chem_points <= 8:
            pl_chem_color = yellow
        else:
            pl_chem_color = dark_green
        pl_chem_label = Label(text=str(pl_chem_points), font=title_font_13,
                              width=pl_chem_width, height=std_tf_height,
                              x=pl_chem_title_label.right + 2, y=label_y,
                              color=pl_chem_color, just='left')
        chemistry_list.append(pl_chem_label)

        # === Manager Chemistry Points ====
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space + 13 + 9)
        label_y = pl_chem_title_label.bottom - 9
        manager_chem_title_width = 25

        # Manager Chemistry Points Label
        manager_chem_title_label = Label(text='Mgr:', font=title_font_13,
                                         width=manager_chem_title_width, height=std_tf_height,
                                         x=label_x, y=label_y, color=white, just='right')
        chemistry_list.append(manager_chem_title_label)

        # Manager Chemistry Points Stat
        manager_chem_width = 20
        if ((team['manager']['league'] == player['league']['name']) or
                (team['manager']['nation'] == player['nation']['name'])):
            manager_points = 1
            manager_points_color = dark_green
        else:
            manager_points = 0
            manager_points_color = red

        manager_chem_label = Label(text=str(manager_points), font=title_font_13,
                                   width=manager_chem_width, height=std_tf_height,
                                   x=manager_chem_title_label.right + 2, y=label_y,
                                   color=manager_points_color, just='left')
        chemistry_list.append(manager_chem_label)

        # === Loyalty Chemistry Points ====
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space + 13 + 4)
        label_y = manager_chem_title_label.bottom - 9
        loyalty_chem_title_width = 30

        # Loyalty Chemistry Points Label
        loyalty_chem_title_label = Label(text='Loyal:', font=title_font_13,
                                         width=loyalty_chem_title_width, height=std_tf_height,
                                         x=label_x, y=label_y, color=white, just='right')
        chemistry_list.append(loyalty_chem_title_label)

        # Loyalty Chemistry Points Stat
        loyalty_chem_width = 20
        loyalty_points = 1
        if loyalty_points == 1:
            loyalty_points_color = dark_green
        else:
            loyalty_points_color = red

        loyalty_chem_label = Label(text=str(loyalty_points), font=title_font_13,
                                   width=loyalty_chem_width, height=std_tf_height,
                                   x=loyalty_chem_title_label.right + 2, y=label_y,
                                   color=loyalty_points_color, just='left')
        chemistry_list.append(loyalty_chem_label)

        # === Total Chemistry Points ====
        label_x = int(dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2+2*player_border + 7)
        label_y = int(dst_rect[1]+position_coordinates[1]*y_space + player_box_height/2 - player_border - 18)
        total_chem_title_width = 90

        # Total Chemistry Points Label
        total_chem_title_label = Label(text='Total Chemistry:', font=title_font_11,
                                       width=total_chem_title_width, height=std_tf_height,
                                       x=label_x, y=label_y, color=white, just='right')
        chemistry_list.append(total_chem_title_label)

        # Total Chemistry Points Stat
        total_chem_width = 30
        total_chem_points = pl_chem_points + manager_points + loyalty_points
        if total_chem_points > 10:
            total_chem_points = 10

        if total_chem_points < 4:
            total_chem_color = red
        elif total_chem_points < 7:
            total_chem_color = dark_orange
        elif total_chem_points < 10:
            total_chem_color = yellow
        else:
            total_chem_color = dark_green

        total_chem_label = Label(text=str(total_chem_points), font=title_font_11,
                                 width=total_chem_width, height=std_tf_height,
                                 x=total_chem_title_label.right + 2, y=label_y,
                                 color=total_chem_color, just='left')
        chemistry_list.append(total_chem_label)

    def display_chemistry():
        for stat in chemistry_list:
            view.add(stat)
        win_team_bio.become_target()

    def hide_chemistry():
        for stat in chemistry_list:
            view.remove(stat)
        win_team_bio.become_target()

    def hide_all():
        # Hide all displayed items
        hide_headshots()
        hide_summary_stats()
        hide_strength_stats()
        hide_traits()
        hide_specialities()
        hide_team_league_nation()
        hide_chemistry()

    # ========== Button Declarations ==========
    back_btn = Button("Back")
    headshot_trait_btn = Button("Picture")
    summary_trait_btn = Button("Stat Summary")
    strengths_trait_btn = Button("Strengths")
    traits_btn = Button("Traits")
    specialities_btn = Button("Specialities")
    team_league_nation_btn = Button("Team/League/Nation")
    chemistry_btn = Button("Chemistry")

    # ========== Button Functions ==========
    def back_btn_func():
        win_team_bio.hide()
        win_previous.show()

    def headshot_trait_btn_func():
        # Hide all
        hide_all()

        # Display headshots
        display_headshots()
        win_team_bio.become_target()

    def summary_trait_btn_func():
        # Hide all
        hide_all()

        # Display summary stats
        display_summary_stats()
        win_team_bio.become_target()

    def strengths_trait_btn_func():
        # Hide all
        hide_all()

        # Display strengths
        display_strength_stats()
        win_team_bio.become_target()

    def traits_btn_func():
        # Hide all
        hide_all()

        # Display traits and specialities
        display_traits()
        win_team_bio.become_target()

    def specialities_btn_func():
        # Hide all
        hide_all()

        # Display traits and specialities
        display_specialities()
        win_team_bio.become_target()

    def team_league_nation_btn_func():
        # Hide all
        hide_all()

        # Display chemistry
        display_team_league_nation()
        win_team_bio.become_target()

    def chemistry_btn_func():
        # Hide all
        hide_all()

        # Display links
        display_chemistry()
        win_team_bio.become_target()

    # ========== Buttons ==========
    button_x_offset = 50

    back_btn.x = win_team_bio.width - button_width - button_x_offset
    back_btn.y = top_border
    back_btn.height = small_button_height
    back_btn.width = button_width
    back_btn.font = small_button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = small_button_color
    labels_list.append(back_btn)

    headshot_trait_btn.x = back_btn.left
    headshot_trait_btn.y = back_btn.bottom + top_border
    headshot_trait_btn.height = small_button_height
    headshot_trait_btn.width = button_width
    headshot_trait_btn.font = small_button_font
    headshot_trait_btn.action = headshot_trait_btn_func
    headshot_trait_btn.style = 'default'
    headshot_trait_btn.color = small_button_color
    labels_list.append(headshot_trait_btn)

    summary_trait_btn.x = back_btn.left
    summary_trait_btn.y = headshot_trait_btn.bottom
    summary_trait_btn.height = small_button_height
    summary_trait_btn.width = button_width
    summary_trait_btn.font = small_button_font
    summary_trait_btn.action = summary_trait_btn_func
    summary_trait_btn.style = 'default'
    summary_trait_btn.color = small_button_color
    labels_list.append(summary_trait_btn)

    strengths_trait_btn.x = back_btn.left
    strengths_trait_btn.y = summary_trait_btn.bottom
    strengths_trait_btn.height = small_button_height
    strengths_trait_btn.width = button_width
    strengths_trait_btn.font = small_button_font
    strengths_trait_btn.action = strengths_trait_btn_func
    strengths_trait_btn.style = 'default'
    strengths_trait_btn.color = small_button_color
    labels_list.append(strengths_trait_btn)

    traits_btn.x = back_btn.left
    traits_btn.y = strengths_trait_btn.bottom
    traits_btn.height = small_button_height
    traits_btn.width = button_width
    traits_btn.font = small_button_font
    traits_btn.action = traits_btn_func
    traits_btn.style = 'default'
    traits_btn.color = small_button_color
    labels_list.append(traits_btn)

    specialities_btn.x = back_btn.left
    specialities_btn.y = traits_btn.bottom
    specialities_btn.height = small_button_height
    specialities_btn.width = button_width
    specialities_btn.font = small_button_font
    specialities_btn.action = specialities_btn_func
    specialities_btn.style = 'default'
    specialities_btn.color = small_button_color
    labels_list.append(specialities_btn)

    team_league_nation_btn.x = back_btn.left
    team_league_nation_btn.y = specialities_btn.bottom
    team_league_nation_btn.height = small_button_height
    team_league_nation_btn.width = button_width
    team_league_nation_btn.font = small_button_font
    team_league_nation_btn.action = team_league_nation_btn_func
    team_league_nation_btn.style = 'default'
    team_league_nation_btn.color = small_button_color
    labels_list.append(team_league_nation_btn)

    chemistry_btn.x = back_btn.left
    chemistry_btn.y = team_league_nation_btn.bottom
    chemistry_btn.height = small_button_height
    chemistry_btn.width = button_width
    chemistry_btn.font = small_button_font
    chemistry_btn.action = chemistry_btn_func
    chemistry_btn.style = 'default'
    chemistry_btn.color = small_button_color
    labels_list.append(chemistry_btn)

    # ========== Formation Info Title Label ==========
    info_title = Label(text="Team Info", font=title_font_2,
                       width=title_width, height=title_height,
                       x=headshot_trait_btn.right - button_width/2 - title_width/2,
                       y=chemistry_btn.bottom + top_border,
                       color=title_color, just='center')
    labels_list.append(info_title)

    # ========== Team Info Labels ==========
    info_title_width = 85
    info_label_text = "Name:\nRating:\nStrength:\nChemistry:\nFormation:\nStyle:"
    info_title_label = Label(text=info_label_text, font=title_font_7,
                             width=info_title_width, height=std_tf_height*6,
                             x=headshot_trait_btn.left - 45, y=info_title.bottom - title_border,
                             color=title_color, just='right')
    labels_list.append(info_title_label)

    # ========== Team Info ==========
    info_width = 130
    info_text = ("No Names Yet" + "\n" + str(team['rating'])[:7] + "\n" + str(team['strength']) + "\n" +
                 str(team['chemistry']) + "\n" + team['formation']['name'] + "\n" + team['formation']['style'])
    info_label = Label(text=info_text, font=title_font_7,
                       width=info_width, height=std_tf_height*6,
                       x=info_title_label.right + 10, y=info_title_label.top,
                       color=title_color, just='left')
    labels_list.append(info_label)

    # ========== Manager Title Label ==========
    manager_title = Label(text="Suggested Manager", font=title_font_5,
                       width=title_width, height=std_tf_height+5,
                       x=headshot_trait_btn.right - button_width/2 - title_width/2,
                       y=info_title_label.bottom + top_border,
                       color=title_color, just='center')
    labels_list.append(manager_title)

    # ========== Manager Labels ==========
    manager_info_title_width = 45
    manager_info_label_text = "League:\nNation:"
    manager_title_label = Label(text=manager_info_label_text, font=title_font_10,
                                width=manager_info_title_width, height=std_tf_height*5,
                                x=headshot_trait_btn.left - 40, y=manager_title.bottom,
                                color=title_color, just='right')
    labels_list.append(manager_title_label)

    # ========== Manager Info ==========
    manager_info_width = 155
    league_name = ascii_text(team['manager']['league'])
    if len(league_name) > 23:
        league_name = league_name[:23] + '...'
    nation_name = ascii_text(team['manager']['nation'])
    if len(nation_name) > 23:
        nation_name = nation_name[:23] + '...'
    manager_info_text = (league_name + "\n" + nation_name)
    manager_label = Label(text=manager_info_text, font=title_font_10,
                          width=manager_info_width, height=std_tf_height*5,
                          x=manager_title_label.right + 6, y=manager_title_label.top,
                          color=title_color, just='left')
    labels_list.append(manager_label)

    # ========== Add buttons to window ==========
    for label in labels_list:
        view.add(label)

    display_headshots()

    win_team_bio.add(view)
    view.become_target()
    win_team_bio.show()
