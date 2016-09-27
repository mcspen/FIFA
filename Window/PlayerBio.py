from GUI import Button, Geometry, Image, Label, View, Window
from AppConfig import *
import json
from Logic.HelperFunctions import ascii_text, format_attr_name, convert_height, convert_weight, format_birthday,\
    save_image, save_small_image
from Logic import PlayerDB
from Logic import Player
from Window import AssignPlayers


def open_player_bio_window(window_x, window_y, player, win_previous, db_dict=None, file_name=None, current_list=None,
                           roster=None, pos_symbol=None, input_formation=None, pick_formations_page=None):

    if current_list is None:
        current_list = PlayerDB.PlayerDB()

    # ========== Window ==========
    win_player_bio = Window()
    win_player_bio.title = player_bio_win_title
    win_player_bio.auto_position = False
    win_player_bio.position = (window_x, window_y)
    win_player_bio.size = (win_width, win_height)
    win_player_bio.resizable = 0
    win_player_bio.name = player_bio_title + " Window"
    win_player_bio.show()

    # ========== Window Image View ==========
    class PlayerBioWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

            # Background image
            image_pos = ((player_name_label.left - player_background.width)/2, 5)
            src_rect = player_background.bounds
            dst_rect = Geometry.offset_rect(src_rect, image_pos)
            player_background.draw(c, src_rect, dst_rect)

            # Lines between summary stats
            c.forecolor = stat_line_color
            c.fill_rect((dst_rect[0]+22, dst_rect[1]+stat_line_y,
                         dst_rect[2]-22, dst_rect[1]+stat_line_y+1))
            c.fill_rect((dst_rect[0]+22, dst_rect[1]+stat_line_y+stat_line_spacing,
                         dst_rect[2]-22, dst_rect[1]+stat_line_y+stat_line_spacing+1))

            # Headshot
            image_pos = (image_pos[0]+player_headshot_pos[0], player_headshot_pos[1])
            src_rect = player_headshot.bounds
            headshot_dst_rect = Geometry.offset_rect(src_rect, image_pos)
            player_headshot.draw(c, src_rect, headshot_dst_rect)

            # Club
            if 'normal' in player['club']['imageUrls']:
                image_url = player['club']['imageUrls']['normal']['large']
            # FIFA 15 compatibility
            elif 'dark' in player['club']['imageUrls']:
                image_url = player['club']['imageUrls']['dark']['large']
            ratio = 0.75
            image_file_name = 'club_' + str(player['club']['id']) + '_' + str(ratio)
            image_file_name = save_small_image(image_url, image_file_name, ratio)
            club_image = Image(file=image_file_name)
            club_image_pos = club_pos
            club_rect = club_image.bounds
            club_dst_rect = Geometry.offset_rect(club_rect, club_image_pos)
            club_image.draw(c, club_rect, club_dst_rect)

            # Nation
            if 'imageUrls' in player['nation']:
                image_url = player['nation']['imageUrls']['large']
            # FIFA 15 compatibility
            elif 'imageUrl' in player['nation']:
                image_url = player['nation']['imgUrl']
            ratio = 0.75
            image_file_name = 'nation_' + str(player['nation']['id']) + '_' + str(ratio)
            image_file_name = save_small_image(image_url, image_file_name, ratio)
            nation_image = Image(file=image_file_name)
            nation_image_pos = (club_image_pos[0], club_image_pos[1]+club_image.size[1]+nation_spacing)
            nation_rect = nation_image.bounds
            nation_dst_rect = Geometry.offset_rect(nation_rect, nation_image_pos)
            nation_image.draw(c, nation_rect, nation_dst_rect)

            # Coins symbol
            image_file_name = 'Images/coins.png'
            coins_image = Image(file=image_file_name)
            coins_image_pos = coins_pos
            coins_rect = coins_image.bounds
            coins_dst_rect = Geometry.offset_rect(coins_rect, coins_image_pos)
            coins_image.draw(c, coins_rect, coins_dst_rect)

    view = PlayerBioWindowImageView(size=win_player_bio.size)

    # ========== Player Headshot ==========
    image_url = player['headshotImgUrl']
    image_file_name = player['id'] + '_full'
    # FIFA 15 compatibility
    if "130x130" in image_url:
        ratio = 120.0/130.0
        image_file_name = save_small_image(image_url, image_file_name, ratio)
    elif "120x120" in image_url:
        image_file_name = save_image(image_url, image_file_name)
    player_headshot = Image(file=image_file_name)

    # ========== Player Background ==========
    # Assign player background card
    if player['color'] in ['blue_purple', 'bronze', 'easports', 'fut_champions_bronze', 'fut_champions_gold',
                           'fut_champions_silver', 'gold', 'green', 'legend', 'motm', 'motm_2', 'ones_to_watch',
                           'pink_gold', 'pink', 'purple', 'rare_bronze', 'rare_gold', 'rare_silver', 'red_blue',
                           'silver', 'squad_building_challenge', 'teal', 'tots_bronze', 'tots_gold', 'tots_silver',
                           'totw_bronze', 'totw_gold', 'totw_silver', 'toty']:
        background_file = 'Images/Cards/' + player['color'] + '.png'
    else:
        background_file = 'Images/Cards/idk.png'

    player_background = Image(file=background_file)

    # Assign positioning for player card based on type
    if player['color'] in ['legend']:
        player_headshot_pos = (43, 15)
        club_pos = (51, 76)
        nation_spacing = 2
        coins_pos = (155, 222)
        stat_line_y = 173
        stat_line_spacing = 21
        name_y = 138
        rating_pos = (33, 35)
        stats_y = 159
        card_rating_pos_color = black
        card_name_color = black
        card_stat_color = black
        stat_line_color = barely_darker
        coins_color = black

    elif player['color'] in ['green', 'pink_gold']:
        player_headshot_pos = (43, 15)
        club_pos = (51, 76)
        nation_spacing = 1
        coins_pos = (155, 222)
        stat_line_y = 173
        stat_line_spacing = 21
        name_y = 138
        rating_pos = (33, 35)
        stats_y = 159
        card_rating_pos_color = black
        card_name_color = black
        card_stat_color = white
        stat_line_color = barely_lighter
        coins_color = black

    elif player['color'] in ['motm', 'motm_2', 'pink', 'purple', 'teal']:
        player_headshot_pos = (43, 15)
        club_pos = (51, 76)
        nation_spacing = 1
        coins_pos = (155, 222)
        stat_line_y = 173
        stat_line_spacing = 21
        name_y = 138
        rating_pos = (33, 35)
        stats_y = 159
        card_rating_pos_color = black
        card_name_color = white
        card_stat_color = white
        stat_line_color = barely_lighter
        coins_color = white

    elif player['color'] in ['toty', 'easports']:
        player_headshot_pos = (43, 15)
        club_pos = (51, 76)
        nation_spacing = 1
        coins_pos = (155, 222)
        stat_line_y = 173
        stat_line_spacing = 21
        name_y = 138
        rating_pos = (33, 35)
        stats_y = 159
        card_rating_pos_color = white
        card_name_color = white
        card_stat_color = white
        stat_line_color = barely_lighter
        coins_color = white

    elif player['color'] in ['tots_gold', 'tots_silver', 'tots_bronze']:
        player_headshot_pos = (43, 15)
        club_pos = (51, 76)
        nation_spacing = 1
        coins_pos = (155, 222)
        stat_line_y = 173
        stat_line_spacing = 21
        name_y = 138
        rating_pos = (33, 35)
        stats_y = 159
        card_rating_pos_color = white
        card_name_color = black
        card_stat_color = white
        stat_line_color = barely_lighter
        coins_color = black

    elif player['color'] in ['totw_gold', 'totw_silver', 'totw_bronze']:
        player_headshot_pos = (43, 15)
        club_pos = (51, 76)
        nation_spacing = 1
        coins_pos = (155, 222)
        stat_line_y = 173
        stat_line_spacing = 21
        name_y = 138
        rating_pos = (33, 35)
        stats_y = 159
        card_rating_pos_color = black
        card_name_color = white
        card_stat_color = white
        stat_line_color = barely_lighter
        coins_color = white

    elif player['color'] in ['rare_gold', 'rare_silver', 'rare_bronze']:
        player_headshot_pos = (43, 15)
        club_pos = (51, 76)
        nation_spacing = 1
        coins_pos = (155, 222)
        stat_line_y = 172
        stat_line_spacing = 21
        name_y = 138
        rating_pos = (33, 35)
        stats_y = 158
        card_rating_pos_color = black
        card_name_color = black
        card_stat_color = black
        stat_line_color = barely_darker
        coins_color = black

    elif player['color'] in ['gold', 'silver', 'bronze']:
        player_headshot_pos = (43, 15)
        club_pos = (51, 76)
        nation_spacing = 3
        coins_pos = (155, 222)
        stat_line_y = 173
        stat_line_spacing = 21
        name_y = 138
        rating_pos = (33, 35)
        stats_y = 159
        card_rating_pos_color = black
        card_name_color = black
        card_stat_color = black
        stat_line_color = barely_darker
        coins_color = black

    else:
        player_headshot_pos = (43, 15)
        club_pos = (51, 76)
        nation_spacing = 1
        coins_pos = (155, 222)
        stat_line_y = 173
        stat_line_spacing = 21
        name_y = 138
        rating_pos = (33, 35)
        stats_y = 159
        card_rating_pos_color = black
        card_name_color = black
        card_stat_color = black
        stat_line_color = barely_darker
        coins_color = black

    # ========== Button Declarations ==========
    add_player_btn = Button()
    back_btn = Button("Back")
    update_price_btn = Button("Update")

    # ========== Button Functions ==========
    def add_player_btn_func():
        # Assign player to roster if that is the current process
        if roster is not None and pos_symbol is not None and input_formation is not None:
            roster[pos_symbol] = player

            win_player_bio.hide()
            AssignPlayers.open_assign_players_window(win_player_bio.x, win_player_bio.y, db_dict,
                                                     input_formation, pick_formations_page, roster)

        # Check if player is already on selected players list
        # Remove player from list
        elif player in current_list.db:
            # Remove
            current_list.db.remove(player)
            # Save
            current_list.sort(['rating'])
            current_list.save(file_name, 'list', True)

            # Switch button title
            add_player_btn.title = "Add Player to List"

        # Add player to the list
        else:
            # Add
            current_list.db.append(player)
            # Save
            current_list.sort(['rating'])
            current_list.save(file_name, 'list', True)

            # Switch button title
            add_player_btn.title = "Remove Player from List"

        win_player_bio.become_target()

    def back_btn_func():
        win_player_bio.hide()
        win_previous.show()

    def update_price_btn_func():
        if db_dict is not None:
            # Get index in player list and player db
            if player in db_dict['player_list'][1].db:
                list_index = db_dict['player_list'][1].db.index(player)
            else:
                list_index = -1
            if player in db_dict['player_db'][1].db:
                db_index = db_dict['player_db'][1].db.index(player)
            else:
                db_index = -1

            # Load console type
            settings = {'console_type': ''}
            with open('configs.json', 'r') as f:
                settings["console_type"] = json.load(f)['console_type']
                f.close()

            # Get updated price
            new_price = Player.Player(player).get_price(settings["console_type"])

            # Update price displayed
            new_price_str = str(new_price)
            if new_price > 999999:
                new_price_str = new_price_str[:-6] + ',' + new_price_str[-6:-3] + ',' + new_price_str[-3:]
            elif new_price > 999:
                new_price_str = new_price_str[:-3] + ',' + new_price_str[-3:]
            elif new_price < 1:
                new_price_str = '?'
            price_label.text = str(new_price_str)

            # Assigned updated price
            if list_index > -1:
                updated_player = db_dict['player_list'][1].db[list_index]
                updated_player['price'] = new_price
                db_dict['player_list'][1].db[list_index] = updated_player
            if db_index > -1:
                updated_player = db_dict['player_db'][1].db[db_index]
                updated_player['price'] = new_price
                db_dict['player_db'][1].db[db_index] = updated_player
            player['price'] = new_price

            # Save
            if list_index > -1:
                db_dict['player_list'][1].sort(['rating'])
                db_dict['player_list'][1].save(db_dict['player_list'][0], 'list', True)
            if db_index > -1:
                db_dict['player_db'][1].sort(['rating'])
                db_dict['player_db'][1].save(db_dict['player_db'][0], 'db', True)

        win_player_bio.become_target()

    # ========== Buttons ==========
    button_x_offset = 85

    add_player_btn.x = win_player_bio.width - button_width - button_x_offset
    add_player_btn.y = top_border
    add_player_btn.height = small_button_height
    add_player_btn.width = button_width
    add_player_btn.font = small_button_font
    add_player_btn.action = add_player_btn_func
    add_player_btn.style = 'default'
    add_player_btn.color = small_button_color
    # Disable button if no lists selected
    if file_name is None and roster is None:
        add_player_btn.enabled = 0

    if roster is not None and pos_symbol is not None and input_formation is not None:
        add_player_btn.title = "Assign Player to Roster"

        # Get list of player base IDs
        base_ids = []
        for player_value in roster.itervalues():
            base_ids.append(player_value['baseId'])

        # Make sure any version player isn't already on team
        if player['baseId'] in base_ids:
            add_player_btn.title = "Player Already on Roster"
            add_player_btn.enabled = 0

    # Check if player is already on selected players list
    elif player in current_list.db:
        add_player_btn.title = "Remove Player from List"
    else:
        add_player_btn.title = "Add Player to List"

    back_btn.x = add_player_btn.left
    back_btn.y = add_player_btn.bottom
    back_btn.height = small_button_height
    back_btn.width = button_width
    back_btn.font = small_button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = small_button_color

    update_price_btn.x = add_player_btn.right
    update_price_btn.y = add_player_btn.top
    update_price_btn.height = small_button_height*2
    update_price_btn.width = button_width/3
    update_price_btn.font = small_button_font
    update_price_btn.action = update_price_btn_func
    update_price_btn.style = 'default'
    update_price_btn.color = small_button_color
    if db_dict is None:
        update_price_btn.enabled = 0

    # ========== Player Info Labels ==========
    # Get attribute lists
    with open('configs.json', 'r') as f:
        attribute_lists = json.load(f)['player_attributes']
        f.close()

    labels_list = []

    name_width = 300
    rating_big_width = 70

    traits_offset_left = 25
    traits_label_width = 100
    traits_list_label_width = 500 - traits_label_width

    section_label_width = 115

    # ========== Name ==========
    player_name_label = Label(font=title_font, width=name_width, height=title_height, x=(win_width - name_width)/2,
                              y=top_border, color=title_color, just='center')
    labels_list.append(player_name_label)
    player_full_name_label = Label(font=title_tf_font, width=name_width, height=std_tf_height,
                                   x=(win_width - name_width)/2, y=player_name_label.bottom - title_border,
                                   color=title_color, just='center')
    labels_list.append(player_full_name_label)

    # ========== Name on Card ==========
    name_on_card_label = Label(font=std_tf_font_bold, width=player_background.width, height=std_tf_height,
                               x=(player_name_label.left - player_background.width)/2,
                               y=name_y, color=card_name_color, just='center')
    labels_list.append(name_on_card_label)

    # ========== Rating and Position ==========
    rating_big_label = Label(font=title_font_3, width=rating_big_width, height=title_height,
                             x=rating_pos[0], y=rating_pos[1],
                             color=card_rating_pos_color, just='center')
    labels_list.append(rating_big_label)
    position_big_label = Label(font=title_font_6, width=rating_big_width, height=title_height,
                               x=rating_big_label.left, y=rating_big_label.bottom-27,
                               color=card_rating_pos_color, just='center')
    labels_list.append(position_big_label)

    # ========== Traits and Specialities ==========
    traits_label = Label(font=std_tf_font_bold, width=traits_label_width, height=std_tf_height,
                         x=player_full_name_label.left - traits_offset_left,
                         y=player_full_name_label.bottom+title_border*2, color=title_color, just='right')
    labels_list.append(traits_label)
    traits_list_label = Label(font=small_tf_font, width=traits_list_label_width, height=std_tf_height,
                              x=traits_label.right + small_button_spacing,
                              y=traits_label.top+3, color=title_color, just='left')
    labels_list.append(traits_list_label)
    traits_list_label_2 = Label(font=small_tf_font, width=traits_list_label_width, height=std_tf_height,
                                x=traits_label.right + small_button_spacing,
                                y=traits_list_label.bottom, color=title_color, just='left')
    labels_list.append(traits_list_label_2)
    specialities_label = Label(font=std_tf_font_bold, width=traits_label_width, height=std_tf_height,
                               x=traits_label.left,
                               y=traits_list_label_2.bottom, color=title_color, just='right')
    labels_list.append(specialities_label)
    specialities_list_label = Label(font=small_tf_font, width=traits_list_label_width, height=std_tf_height,
                                    x=specialities_label.right + small_button_spacing,
                                    y=specialities_label.top+3, color=title_color, just='left')
    labels_list.append(specialities_list_label)
    specialities_list_label_2 = Label(font=small_tf_font, width=traits_list_label_width, height=std_tf_height,
                                      x=specialities_label.right + small_button_spacing,
                                      y=specialities_list_label.bottom, color=title_color, just='left')
    labels_list.append(specialities_list_label_2)

    # ========== Attributes Under Picture Section ==========
    attr_title_label_width = 35
    attr_label_width = 20
    attribute_x_offset = 30
    label_x = (player_name_label.left - player_background.width)/2 + player_background.width/2 - attribute_x_offset - 10
    label_y = stats_y

    for idx, attr in enumerate(player['attributes']):
        if idx == 3:
            label_x += 2*attribute_x_offset + 10
            label_y = stats_y

        stat_label = Label(font=std_tf_font_bold, width=attr_label_width, height=std_tf_height,
                           x=label_x-attr_label_width-2, y=label_y, color=card_stat_color, just='right')
        stat_label.text = str(attr['value'])
        labels_list.append(stat_label)

        stat_title_label = Label(font=std_tf_font, width=attr_title_label_width, height=std_tf_height,
                                 x=label_x+1, y=label_y, color=card_stat_color, just='left')
        stat_title_label.text = format_attr_name(attr['name'][-3:])
        labels_list.append(stat_title_label)

        label_y += std_tf_height + 1

    # ========== Price Section ==========
    price_width = 80
    price = str(player['price'])
    if player['price'] > 999999:
        price = price[:-6] + ',' + price[-6:-3] + ',' + price[-3:]
    elif player['price'] > 999:
        price = price[:-3] + ',' + price[-3:]
    elif player['price'] < 1:
        price = '?'

    coins_pos = (coins_pos[0] - (9 - len(price)) * 3, coins_pos[1])

    price_label = Label(text=price,font=std_tf_font_bold, width=price_width, height=std_tf_height,
                              x=coins_pos[0] - price_width - 3,
                              y=coins_pos[1], color=coins_color, just='right')
    labels_list.append(price_label)

    # ========== Database Info Section ==========
    db_info_label = Label(font=std_tf_font_bold, width=section_label_width, height=std_tf_height,
                          x=win_player_bio.width * 5 / 50,
                          y=specialities_list_label_2.bottom + int(7.3*title_border), color=title_color, just='center')
    db_info_label.text = "Database Info"
    labels_list.append(db_info_label)

    db_info_title_label_width = 80
    db_info_label_width = 55
    attribute_x_offset = 40
    label_x = db_info_label.left + section_label_width/2 - attribute_x_offset
    label_y = db_info_label.bottom

    for idx, db_info in enumerate(attribute_lists['db']):
        if idx == 5:
            attribute_x_offset = 85
            db_info_title_label_width = 60
            db_info_label_width = 50
            label_x = db_info_label.left + section_label_width/2 + attribute_x_offset
            label_y = db_info_label.bottom

        if db_info == 'modelName':
                db_info_label_width = 95

        stat_title_label = Label(font=small_tf_font, width=db_info_title_label_width, height=std_tf_height,
                                 x=label_x-db_info_title_label_width, y=label_y, color=title_color, just='right')
        stat_title_label.text = format_attr_name(db_info) + ':'
        labels_list.append(stat_title_label)

        stat_label = Label(font=small_tf_font, width=db_info_label_width, height=std_tf_height,
                           x=label_x, y=label_y, color=title_color, just='right')
        if db_info in ['clubId', 'leagueId', 'nationId']:
            stat_label.text = str(player[db_info[:-2]]['id'])
        else:
            stat_label.text = str(player[db_info])
        labels_list.append(stat_label)

        label_y += std_tf_height

    # ========== Personal Section ==========
    personal_label = Label(font=std_tf_font_bold, width=section_label_width, height=std_tf_height,
                           x=win_player_bio.width * 29 / 50,
                           y=specialities_list_label_2.bottom + top_border, color=title_color, just='center')
    personal_label.text = "Personal"
    labels_list.append(personal_label)

    personal_title_stat_width = 100
    personal_stat_width = 65
    personal_stat_just = 'right'
    personal_x_offset = personal_stat_width + 60
    label_x = personal_label.left + section_label_width/2 - personal_x_offset
    label_y = personal_label.bottom

    for idx, personal in enumerate(attribute_lists['personal']):
        if idx == 7:
            personal_title_stat_width = 75
            personal_stat_width = 250
            personal_stat_just = 'left'
            personal_x_offset = personal_title_stat_width - 55
            label_x = personal_label.left + section_label_width/2 + personal_x_offset
            label_y = personal_label.bottom

        # Skip these since other labels use them
        if personal == 'positionFull':
            continue

        stat_title_label = Label(font=small_tf_font, width=personal_title_stat_width, height=std_tf_height,
                                 x=label_x-personal_title_stat_width, y=label_y, color=title_color, just='right')
        stat_title_label.text = format_attr_name(personal) + ':'
        labels_list.append(stat_title_label)

        color = white
        # Change color for rating and potential
        if personal in ['rating', 'potential']:
            color = attr_color(player[personal])
        # Change color for quality and color
        elif personal in ['quality', 'color', 'playerType']:
            color = quality_color(player[personal])

        stat_label = Label(font=small_tf_font, width=personal_stat_width, height=std_tf_height,
                           x=label_x+5, y=label_y, color=color, just=personal_stat_just)
        if personal == 'height':
            centimeters = player[personal]
            converted_height = convert_height(centimeters, 'string')
            stat_label.text = '%s (%d cm)' % (converted_height, centimeters)
        elif personal == 'weight':
            kilograms = player[personal]
            pounds = convert_weight(kilograms)
            stat_label.text = '%.1f lb (%d kg)' % (pounds, kilograms)
        elif personal in ['club', 'nation']:
            stat_label.text = ascii_text(player[personal]['name'])
        elif personal in ['league']:
            stat_label.text = '%s (%s)' % (ascii_text(player[personal]['name']),
                                           ascii_text(player[personal]['abbrName']))
        elif personal == 'birthdate':
            b_day = format_birthday(player['birthdate'])
            stat_label.text = b_day
        elif personal == 'position':
            stat_label.text = '%s (%s)' % (player['positionFull'], player[personal])
        else:
            stat_label.text = str(player[personal])
        labels_list.append(stat_label)

        label_y += std_tf_height

    # ========== Detailed Attribute Sections ==========
    attribute_group_list = ['characteristics', 'pace', 'shooting', 'passing',
                            'goalkeeping', 'dribbling', 'defending', 'physicality']

    group_spacing = (win_player_bio.width - 4*section_label_width)/5
    group_x = group_spacing
    group_y = personal_label.bottom + 175

    for idx, group in enumerate(attribute_group_list):

        if idx == 4:
            group_x = group_spacing
            group_y += 150

        stat_group_label = Label(font=std_tf_font_bold, width=section_label_width, height=std_tf_height,
                                 x=group_x, y=group_y, color=title_color, just='center')
        stat_group_label.text = group.capitalize()
        if idx in [1, 2, 3, 5, 6, 7] and not player['isGK']:
            stat_group_label.text += ':'
        labels_list.append(stat_group_label)

        if idx in [1, 2, 3, 5, 6, 7] and not player['isGK']:
            rating_offset = [0, 25, 12, 16, 0, 8, 6, 2]
            stat_group_rating_label = Label(font=std_tf_font_bold, width=20, height=std_tf_height,
                                            x=stat_group_label.right - rating_offset[idx],
                                            y=group_y, color=title_color, just='center')
            stat_group_rating_label.text = str(player['attributes'][idx - (1 + int(idx/4))]['value'])
            stat_group_rating_label.color = attr_color(player['attributes'][idx - (1 + int(idx/4))]['value'])
            labels_list.append(stat_group_rating_label)

        # ========== Detailed Attribute Stats Sections ==========
        stat_title_label_width = 110
        stat_width = 25
        label_y = stat_group_label.bottom
        label_x = stat_group_label.left + section_label_width/2 + 25

        if group == 'characteristics':
            stat_width = 60

        for attribute in attribute_lists[group]:
            stat_title_label = Label(font=small_tf_font, width=stat_title_label_width, height=std_tf_height,
                                     x=label_x-stat_title_label_width, y=label_y, color=title_color, just='right')
            stat_title_label.text = format_attr_name(attribute) + ':'
            labels_list.append(stat_title_label)

            color = white
            if type(player[attribute]) is int and attribute not in ['weakFoot', 'skillMoves']:
                color = attr_color(player[attribute])

            elif attribute in ['weakFoot', 'skillMoves']:
                color = attr_color(40 + 10*player[attribute])

            stat_label = Label(font=small_tf_font, width=stat_width, height=std_tf_height,
                               x=label_x, y=label_y, color=color, just='right')
            if attribute in ['weakFoot', 'skillMoves']:
                stat_label.text = '* '*player[attribute]
            else:
                stat_label.text = str(player[attribute])
            labels_list.append(stat_label)

            label_y += std_tf_height

        group_x += section_label_width + group_spacing

    # ========== Label Text ==========
    # Player's normal name
    player_name = ascii_text(player['name'])
    player_name_label.text = player_name
    name_on_card_label.text = player_name

    # Player's name
    player_full_name = ascii_text(player['firstName']) + ' ' + ascii_text(player['lastName'])
    player_full_name_label.text = player_full_name

    # Player's rating
    rating_big_label.text = str(player['rating'])

    # Player's position
    position_big_label.text = player['position']

    # Player's traits
    traits_label.text = 'Traits:'
    traits_list = ''
    traits_list_2 = ''
    if player['traits'] is not None:
        index = 0
        for trait in player['traits']:
            if len(traits_list + trait) < 70:
                traits_list += trait + ', '
                index += 1
            else:
                break
        for trait in player['traits'][index:]:
            traits_list_2 += trait + ', '
    else:
        traits_list = 'No traits..'

    if len(traits_list_2) > 0:
        traits_list_label.text = traits_list[:-1]
    else:
        traits_list_label.text = traits_list[:-2]
    traits_list_label_2.text = traits_list_2[:-2]

    # Player's specialities
    specialities_label.text = 'Specialities:'
    specialities_list = ''
    specialities_list_2 = ''
    if player['specialities'] is not None:
        index = 0
        for speciality in player['specialities']:
            if len(specialities_list + speciality) < 70:
                specialities_list += speciality + ', '
                index += 1
            else:
                break
        for speciality in player['specialities'][index:]:
            specialities_list_2 += speciality + ', '
    else:
        specialities_list = 'No specialities..'

    if len(specialities_list_2) > 0:
        specialities_list_label.text = specialities_list[:-1]
    else:
        specialities_list_label.text = specialities_list[:-2]
    specialities_list_label_2.text = specialities_list_2[:-2]

    # ========== Add buttons to window ==========
    view.add(add_player_btn)
    view.add(back_btn)
    view.add(update_price_btn)

    for label in labels_list:
        view.add(label)

    win_player_bio.add(view)
    view.become_target()
    win_player_bio.show()
