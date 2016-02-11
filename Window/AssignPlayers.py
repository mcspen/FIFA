from GUI import Button, Geometry, Image, Label, View, Window
from AppConfig import *
import json
import copy
from Logic.HelperFunctions import ascii_text, save_small_image
from Logic import Team
from Window import PlayerBio


def open_assign_players_window(window_x, window_y, db_dict, input_formation, win_previous, roster=None):

    formation = copy.deepcopy(input_formation)

    if roster is not None:
        for pos, player in roster.iteritems():
            if pos in formation['positions']:
                formation['positions'][pos]['player'] = player
            else:
                print "Invalid position. Position not in formation."

    # ========== Window ==========
    win_assign_players = Window()
    win_assign_players.title = team_bio_win_title
    win_assign_players.auto_position = False
    win_assign_players.position = (window_x, window_y)
    win_assign_players.size = (win_width, win_height)
    win_assign_players.resizable = 0
    win_assign_players.name = team_bio_title + " Window"
    win_assign_players.show()

    # ========== Load Formation Spacing ==========
    # Get attribute lists
    with open('configs.json', 'r') as f:
        team_spacing = json.load(f)['team_coordinates'][formation['name']]
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
    field_x_offset = (win_assign_players.width - field_width - button_width - 100) / 2
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
            for sym, pos in formation['positions'].iteritems():

                position_coordinates = team_spacing[sym]

                # Iterate through links of player
                for link in pos['links']:
                    colors = [red, orange, yellow, green]

                    if 'player' in pos and 'player' in formation['positions'][link]:
                        color_num = Team.Team.teammate_chemistry(pos['player'],
                                                                 formation['positions'][link]['player'])
                    else:
                        color_num = 0
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
            for sym, pos in formation['positions'].iteritems():
                position_coordinates = team_spacing[sym]
                if 'player' in pos:
                    player = pos['player']
                    box_file_name = 'Images/Cards/' + player['color'] + '_box.png'
                else:
                    box_file_name = 'Images/Cards/' + 'bronze' + '_box.png'
                box_image = Image(file=box_file_name)
                box_pos = ((dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2,
                             dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2))
                box_rect = box_image.bounds
                box_dst_rect = Geometry.offset_rect(box_rect, box_pos)
                box_image.draw(c, box_rect, box_dst_rect)

    view = StartWindowImageView(size=win_assign_players.size)

    # ========== Player Headshots ==========
    player_headshots = []
    name_height = 25

    # Player headshots
    class HeadshotImageView(View):
        def draw(self, c, r):
            dst_rect = (field_x_offset, field_y_offset, field_x_offset+field_width, field_y_offset+field_length)

            for sym, position in formation['positions'].iteritems():
                position_coordinates = team_spacing[sym]

                # Darker box for positions
                c.forecolor = darker
                c.fill_rect((dst_rect[0]+position_coordinates[0]*x_space-player_box_width/5-2*player_border,
                             dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+player_border,
                             dst_rect[0]+position_coordinates[0]*x_space+player_box_width/2-player_border,
                             dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2+name_height-4))

                # Get player information
                if 'player' in position:
                    player = position['player']

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
    for sym, position in formation['positions'].iteritems():
        # Get player information
        if 'player' in position:
            player = position['player']
        else:
            player = {'rating': '', 'position': '', 'name': unicode('Assign Player')}
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
        colors = [red, dark_orange, yellow, dark_green]
        if 'player' in position:
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
        def name_btn_func(current_player, symbol):
            # Go to player search page to add player
            if current_player['name'] == 'Assign Player':
                stuff = 0

            # Remove player from roster and info from formation
            else:
                roster.pop(symbol)
                formation['positions'][pos].pop('player')
                open_assign_players_window(win_assign_players.x, win_assign_players.y,
                                           db_dict, formation, win_previous, roster)
            #PlayerBio.open_player_bio_window(win_assign_players.x, win_assign_players.y, current_player, win_assign_players)
            win_assign_players.hide()

        name_color = darker
        player_name = ascii_text(player['name'])
        name_btn = Button(title=player_name, font=title_font_5,
                           width=player_box_width-4*player_border, height=name_height,
                           x=int(dst_rect[0]+position_coordinates[0]*x_space-player_box_height/2+2*player_border),
                           y=int(dst_rect[1]+position_coordinates[1]*y_space +
                                 player_box_height/2-player_border-name_height),
                           color=name_color, just='center',
                            action=(name_btn_func, player, sym))
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
        win_assign_players.become_target()

    # ========== Button Declarations ==========
    back_btn = Button("Back")

    # ========== Button Functions ==========
    def back_btn_func():
        win_assign_players.hide()
        win_previous.show()

    # ========== Buttons ==========
    button_x_offset = 50

    back_btn.x = win_assign_players.width - button_width - button_x_offset
    back_btn.y = top_border
    back_btn.height = small_button_height
    back_btn.width = button_width
    back_btn.font = small_button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = small_button_color
    labels_list.append(back_btn)

    # ========== Add buttons to window ==========
    for label in labels_list:
        view.add(label)

    display_headshots()

    win_assign_players.add(view)
    view.become_target()
    win_assign_players.show()
