from GUI import Button, Geometry, Image, Label, View, Window
from AppConfig import *
import json
from Logic.HelperFunctions import ascii_text, format_attr_name, convert_height, convert_weight, format_birthday,\
    save_image, get_file_prefix


def open_player_bio_window(window_x, window_y, player, db_dict, win_search):

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
    class StartWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

            image_pos = ((player_name_label.left - player_headshot.width)/2,
                         player_name_label.top)
            src_rect = player_headshot.bounds
            dst_rect = Geometry.offset_rect(src_rect, image_pos)

            c.forecolor = quality_color(player['color'])
            c.fill_rect((dst_rect[0]-2, dst_rect[1]-2, dst_rect[2]+2, dst_rect[3]+3*std_tf_height+2))
            c.forecolor = darker
            c.fill_rect((dst_rect[0], dst_rect[3]+5, dst_rect[2], dst_rect[3]+3*std_tf_height))

            player_headshot.draw(c, src_rect, dst_rect)

    view = StartWindowImageView(size=win_player_bio.size)

    # ========== Player Headshot ==========
    # player_headshot = Image(file = 'Images/headshot.png')

    image_url = player['headshotImgUrl']
    player_id = player['id']
    image_file_name = save_image(image_url, player_id)
    player_headshot = Image(file=image_file_name)

    # ========== Button Declarations ==========
    add_player_btn = Button()
    back_btn = Button("Back")

    # ========== Button Functions ==========
    def add_player_btn_func():
        # Check if player is already on selected players list
        # Remove player from list
        if player in db_dict['player_list'][1].db:

            # Remove
            db_dict['player_list'][1].db.remove(player)
            # Save
            db_dict['player_list'][1].sort(['rating'])
            db_dict['player_list'][1].save(db_dict['player_list'][0], 'list', True)

            # Switch button title
            add_player_btn.title = "Add Player to List"

        # Add player to the list
        else:

            # Add
            db_dict['player_list'][1].db.append(player)
            # Save
            db_dict['player_list'][1].sort(['rating'])
            db_dict['player_list'][1].save(db_dict['player_list'][0], 'list', True)

            # Switch button title
            add_player_btn.title = "Remove Player from List"

        win_player_bio.become_target()

    def back_btn_func():
        win_player_bio.hide()
        win_search.show()

    # ========== Buttons ==========
    button_x_offset = 50

    add_player_btn.x = win_width - button_width - button_x_offset
    add_player_btn.y = top_border
    add_player_btn.height = small_button_height
    add_player_btn.width = button_width
    add_player_btn.font = small_button_font
    add_player_btn.action = add_player_btn_func
    add_player_btn.style = 'default'
    add_player_btn.color = small_button_color

    # Check if player is already on selected players list
    if player in db_dict['player_list'][1].db:
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

    # ========== Name and Rating ==========
    player_name_label = Label(font=title_font, width=name_width, height=title_height, x=(win_width - name_width)/2,
                              y=top_border, color=title_color, just='center')
    labels_list.append(player_name_label)
    player_full_name_label = Label(font=title_tf_font, width=name_width, height=std_tf_height,
                                   x=(win_width - name_width)/2, y=player_name_label.bottom - title_border,
                                   color=title_color, just='center')
    labels_list.append(player_full_name_label)
    rating_big_label = Label(font=title_font, width=rating_big_width, height=title_height,
                             x=player_full_name_label.left - rating_big_width + 12,
                             y=player_full_name_label.top - title_border, color=title_color, just='center')
    labels_list.append(rating_big_label)
    position_big_label = Label(font=title_font_2, width=rating_big_width, height=title_height,
                               x=rating_big_label.left, y=rating_big_label.bottom-15, color=title_color, just='center')
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
    attr_title_label_width = 30
    attr_label_width = 20
    attribute_x_offset = 30
    label_x = (player_name_label.left - player_headshot.width)/2 + player_headshot.width/2 - attribute_x_offset
    label_y = player_name_label.top + player_headshot.height + 5

    for idx, attr in enumerate(player['attributes']):
        if idx == 3:
            label_x = (player_name_label.left - player_headshot.width)/2 + player_headshot.width/2 + attribute_x_offset
            label_y = player_name_label.top + player_headshot.height + 5

        stat_title_label = Label(font=small_tf_font, width=attr_title_label_width, height=std_tf_height,
                                 x=label_x-attr_title_label_width, y=label_y, color=title_color, just='right')
        stat_title_label.text = format_attr_name(attr['name'][-3:]) + ':'
        labels_list.append(stat_title_label)

        color = attr_color(attr['value'])

        stat_label = Label(font=small_tf_font, width=attr_label_width, height=std_tf_height,
                           x=label_x, y=label_y, color=color, just='right')
        stat_label.text = str(attr['value'])
        labels_list.append(stat_label)

        label_y += std_tf_height

    # ========== Personal Section ==========
    personal_label = Label(font=std_tf_font_bold, width=section_label_width, height=std_tf_height,
                           x=3*(win_width - 9*section_label_width)/10 + 2*section_label_width,
                           y=specialities_list_label_2.bottom + top_border, color=title_color, just='center')
    personal_label.text = "Personal"
    labels_list.append(personal_label)

    personal_title_stat_width = 100
    personal_stat_width = 60
    personal_stat_just = 'right'
    personal_x_offset = personal_stat_width + 60
    label_x = personal_label.left + section_label_width/2 - personal_x_offset
    label_y = personal_label.bottom

    for idx, personal in enumerate(attribute_lists['personal']):
        if idx == 7:
            personal_title_stat_width = 75
            personal_stat_width = 200
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
        elif personal in ['club', 'league', 'nation']:
            stat_label.text = ascii_text(player[personal]['name'])
        elif personal == 'birthdate':
            b_day = format_birthday(player['birthdate'])
            stat_label.text = b_day
        elif personal == 'position':
            stat_label.text = '%s (%s)' % (player['positionFull'], player[personal])
        else:
            stat_label.text = str(player[personal])
        labels_list.append(stat_label)

        label_y += std_tf_height

    # ========== Database Info Section ==========
    db_info_label = Label(font=std_tf_font_bold, width=section_label_width, height=std_tf_height,
                          x=7*(win_width - 9*section_label_width)/10 + 6*section_label_width,
                          y=personal_label.top, color=title_color, just='center')
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

    # ========== Detailed Attribute Sections ==========
    attribute_group_list = ['characteristics', 'pace', 'shooting', 'passing',
                            'goalkeeping', 'dribbling', 'defending', 'physicality']

    group_spacing = (win_player_bio.width - 4*section_label_width)/5
    group_x = group_spacing
    group_y = personal_label.bottom + 150

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

    # Player's name
    player_full_name = ascii_text(player['firstName']) + ' ' + ascii_text(player['lastName'])
    player_full_name_label.text = player_full_name

    # Player's rating
    color = attr_color(player['rating'])
    rating_big_label.text = str(player['rating'])
    rating_big_label.color = color

    # Player's position
    color = attr_color(player['rating'])
    position_big_label.text = player['position']
    position_big_label.color = color

    # Player's traits
    traits_label.text = 'Traits:'
    traits_list = ''
    traits_list_2 = ''
    if player['traits'] is not None:
        index = 0
        for trait in player['traits']:
            if len(traits_list + trait) < 70:
                traits_list += trait
                index += 1
                if trait != player['traits'][-1]:
                    traits_list += ', '
        for trait in player['traits'][index:]:
            traits_list_2 += trait
            if trait != player['traits'][-1]:
                traits_list_2 += ', '
    else:
        traits_list = 'No traits'
    traits_list_label.text = traits_list
    traits_list_label_2.text = traits_list_2

    # Player's specialities
    specialities_label.text = 'Specialities:'
    specialities_list = ''
    specialities_list_2 = ''
    if player['specialities'] is not None:
        index = 0
        for speciality in player['specialities']:
            if len(specialities_list + speciality) < 70:
                specialities_list += speciality
                index += 1
                if speciality != player['specialities'][-1]:
                    specialities_list += ', '
            else:
                break
        for speciality in player['specialities'][index:]:
            specialities_list_2 += speciality
            if speciality != player['specialities'][-1]:
                specialities_list_2 += ', '
    else:
        specialities_list = 'No traits'
    specialities_list_label.text = specialities_list
    specialities_list_label_2.text = specialities_list_2

    # ========== Add buttons to window ==========
    view.add(add_player_btn)
    view.add(back_btn)

    """view.add(player_name_label)
    view.add(player_full_name_label)
    view.add(rating_big_label)"""

    for label in labels_list:
        view.add(label)

    win_player_bio.add(view)
    view.become_target()
    win_player_bio.show()
