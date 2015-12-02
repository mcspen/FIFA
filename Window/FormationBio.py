from GUI import Button, Geometry, Image, Label, View, Window
from AppConfig import *
import json
from Logic.HelperFunctions import ascii_text, format_attr_name, convert_height, convert_weight, format_birthday,\
    save_image, get_file_prefix
from Logic import PlayerDB


def open_formation_bio_window(window_x, window_y, formation, win_previous, file_name, current_list):

    # ========== Window ==========
    win_formation_bio = Window()
    win_formation_bio.title = formation_bio_win_title
    win_formation_bio.auto_position = False
    win_formation_bio.position = (window_x, window_y)
    win_formation_bio.size = (win_width, win_height)
    win_formation_bio.resizable = 0
    win_formation_bio.name = formation_bio_title + " Window"
    win_formation_bio.show()

    # ========== Load Formation Spacing ==========
    # Get attribute lists
    with open('configs.json', 'r') as f:
        formation_spacing = json.load(f)['formation_coordinates'][formation['name']]
        f.close()

    labels_list = []

    # ========== Field Ratio ==========
    x_to_y_ratio = 1.25
    y_to_x_ratio = 0.8

    # Line specification
    line_color = white
    line_size = 2

    # Field
    field_color = dark_green
    field_length = 600
    field_width = field_length*y_to_x_ratio

    # Field positioning on screen
    # field_x_offset = (win_formation_bio.width - field_width) / 2
    field_x_offset = (win_formation_bio.width - field_width - button_width - 100) / 2
    field_y_offset = top_border + title_height + title_border

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
    x_space = int(field_width/12)
    y_space = int(field_length/12)
    player_box_width = 80
    player_box_height = 50

    # ========== Window Image View ==========
    class StartWindowImageView(View):
        def draw(self, c, r):
            c.backcolor = view_backcolor
            c.erase_rect(r)

            image_pos = (field_x_offset, field_y_offset)
            src_rect = (0, 0, field_width, field_length)
            dst_rect = Geometry.offset_rect(src_rect, image_pos)

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
            c.stroke_arc((dst_rect[0], dst_rect[1]), corner_semi_circle_radius, 0, 90)
            c.frame_arc((dst_rect[2], dst_rect[1]), corner_semi_circle_radius, 90, 180)
            c.stroke_arc((dst_rect[0], dst_rect[3]-line_size), corner_semi_circle_radius, 270, 0)
            c.frame_arc((dst_rect[2], dst_rect[3]-line_size), corner_semi_circle_radius, 180, 270)

            # Links
            for symbol, position in formation['positions'].iteritems():
                # Place links
                c.forecolor = yellow
                position_coordinates = formation_spacing[symbol]
                for link in position['links']:
                    link_coordinates = formation_spacing[link]
                    c.moveto(dst_rect[0]+position_coordinates[0]*x_space,
                             dst_rect[1]+position_coordinates[1]*y_space)
                    c.lineto(dst_rect[0]+link_coordinates[0]*x_space,
                             dst_rect[1]+link_coordinates[1]*y_space)
                    c.stroke()
                    # Get poly to work to get thicker lines?
                    """c.fill_poly(((int(dst_rect[0]+position_coordinates[0]*x_space)-line_size/2,
                                int(dst_rect[1]+position_coordinates[1]*y_space)-line_size/2),
                                 (int(dst_rect[0]+link_coordinates[0]*x_space+line_size/2),
                                int(dst_rect[1]+link_coordinates[1]*y_space)+line_size/2)))"""

            # Player Markers
            for symbol, position in formation['positions'].iteritems():
                # Player marker
                c.forecolor = lighter
                position_coordinates = formation_spacing[symbol]
                c.fill_oval((dst_rect[0]+position_coordinates[0]*x_space-player_box_width/2,
                             dst_rect[1]+position_coordinates[1]*y_space-player_box_height/2,
                             dst_rect[0]+position_coordinates[0]*x_space+player_box_width/2,
                             dst_rect[1]+position_coordinates[1]*y_space+player_box_height/2))

    view = StartWindowImageView(size=win_formation_bio.size)

    # ========== Button Declarations ==========
    add_formation_btn = Button()
    back_btn = Button("Back")

    # ========== Button Functions ==========
    def add_formation_btn_func():
        # Check if formation is already on selected formations list
        # Remove formation from list
        if formation in current_list.db:
            # Remove
            current_list.db.remove(formation)
            # Save
            current_list.sort(['name'])
            current_list.save(file_name, 'list', True)

            # Switch button title
            add_formation_btn.title = "Add Formation to List"

        # Add formation to the list
        else:
            # Add
            current_list.db.append(formation)
            # Save
            current_list.sort(['name'])
            current_list.save(file_name, 'list', True)

            # Switch button title
            add_formation_btn.title = "Remove Formation from List"

        win_formation_bio.become_target()

    def back_btn_func():
        win_formation_bio.hide()
        win_previous.show()

    # ========== Buttons ==========
    button_x_offset = 50

    add_formation_btn.x = win_width - button_width - button_x_offset
    add_formation_btn.y = top_border
    add_formation_btn.height = small_button_height
    add_formation_btn.width = button_width
    add_formation_btn.font = small_button_font
    add_formation_btn.action = add_formation_btn_func
    add_formation_btn.style = 'default'
    add_formation_btn.color = small_button_color

    # Check if formation is already on selected formations list
    if formation in current_list.db:
        add_formation_btn.title = "Remove Formation from List"
    else:
        add_formation_btn.title = "Add Formation to List"

    back_btn.x = add_formation_btn.left
    back_btn.y = add_formation_btn.bottom
    back_btn.height = small_button_height
    back_btn.width = button_width
    back_btn.font = small_button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = small_button_color

    # ========== Name ==========
    formation_name_label = Label(text=formation['name'],font=title_font, width=title_width, height=title_height,
                                 x=(win_width - title_width)/2, y=top_border, color=title_color, just='center')
    formation_name_label.x = (win_formation_bio.width - title_width - button_width - 100) / 2
    labels_list.append(formation_name_label)

    """# ========== Formation Info Labels ==========
    # Get attribute lists
    with open('configs.json', 'r') as f:
        attribute_lists = json.load(f)['formation_attributes']
        f.close()

    traits_offset_left = 25
    traits_label_width = 100
    traits_list_label_width = 500 - traits_label_width

    section_label_width = 115

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

    for idx, attr in enumerate(formation['attributes']):
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
            color = attr_color(formation[personal])
        # Change color for quality and color
        elif personal in ['quality', 'color', 'playerType']:
            color = quality_color(formation[personal])

        stat_label = Label(font=small_tf_font, width=personal_stat_width, height=std_tf_height,
                           x=label_x+5, y=label_y, color=color, just=personal_stat_just)
        if personal == 'height':
            centimeters = formation[personal]
            converted_height = convert_height(centimeters, 'string')
            stat_label.text = '%s (%d cm)' % (converted_height, centimeters)
        elif personal == 'weight':
            kilograms = formation[personal]
            pounds = convert_weight(kilograms)
            stat_label.text = '%.1f lb (%d kg)' % (pounds, kilograms)
        elif personal in ['club', 'league', 'nation']:
            stat_label.text = ascii_text(formation[personal]['name'])
        elif personal == 'birthdate':
            b_day = format_birthday(formation['birthdate'])
            stat_label.text = b_day
        elif personal == 'position':
            stat_label.text = '%s (%s)' % (formation['positionFull'], formation[personal])
        else:
            stat_label.text = str(formation[personal])
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
            stat_label.text = str(formation[db_info[:-2]]['id'])
        else:
            stat_label.text = str(formation[db_info])
        labels_list.append(stat_label)

        label_y += std_tf_height

    # ========== Detailed Attribute Sections ==========
    attribute_group_list = ['characteristics', 'pace', 'shooting', 'passing',
                            'goalkeeping', 'dribbling', 'defending', 'physicality']

    group_spacing = (win_formation_bio.width - 4*section_label_width)/5
    group_x = group_spacing
    group_y = personal_label.bottom + 150

    for idx, group in enumerate(attribute_group_list):

        if idx == 4:
            group_x = group_spacing
            group_y += 150

        stat_group_label = Label(font=std_tf_font_bold, width=section_label_width, height=std_tf_height,
                                 x=group_x, y=group_y, color=title_color, just='center')
        stat_group_label.text = group.capitalize()
        if idx in [1, 2, 3, 5, 6, 7] and not formation['isGK']:
            stat_group_label.text += ':'
        labels_list.append(stat_group_label)

        if idx in [1, 2, 3, 5, 6, 7] and not formation['isGK']:
            rating_offset = [0, 25, 12, 16, 0, 8, 6, 2]
            stat_group_rating_label = Label(font=std_tf_font_bold, width=20, height=std_tf_height,
                                            x=stat_group_label.right - rating_offset[idx],
                                            y=group_y, color=title_color, just='center')
            stat_group_rating_label.text = str(formation['attributes'][idx - (1 + int(idx/4))]['value'])
            stat_group_rating_label.color = attr_color(formation['attributes'][idx - (1 + int(idx/4))]['value'])
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
            if type(formation[attribute]) is int and attribute not in ['weakFoot', 'skillMoves']:
                color = attr_color(formation[attribute])

            elif attribute in ['weakFoot', 'skillMoves']:
                color = attr_color(40 + 10*formation[attribute])

            stat_label = Label(font=small_tf_font, width=stat_width, height=std_tf_height,
                               x=label_x, y=label_y, color=color, just='right')
            if attribute in ['weakFoot', 'skillMoves']:
                stat_label.text = '* '*formation[attribute]
            else:
                stat_label.text = str(formation[attribute])
            labels_list.append(stat_label)

            label_y += std_tf_height

        group_x += section_label_width + group_spacing

    # ========== Label Text ==========
    # Player's normal name
    player_name = ascii_text(formation['name'])
    player_name_label.text = player_name

    # Player's name
    player_full_name = ascii_text(formation['firstName']) + ' ' + ascii_text(formation['lastName'])
    player_full_name_label.text = player_full_name

    # Player's rating
    color = attr_color(formation['rating'])
    rating_big_label.text = str(formation['rating'])
    rating_big_label.color = color

    # Player's position
    color = attr_color(formation['rating'])
    position_big_label.text = formation['position']
    position_big_label.color = color

    # Player's traits
    traits_label.text = 'Traits:'
    traits_list = ''
    traits_list_2 = ''
    if formation['traits'] is not None:
        index = 0
        for trait in formation['traits']:
            if len(traits_list + trait) < 70:
                traits_list += trait + ', '
                index += 1
            else:
                break
        for trait in formation['traits'][index:]:
            traits_list_2 += trait + ', '
    else:
        traits_list = 'No traits..'
    traits_list_label.text = traits_list[:-2]
    traits_list_label_2.text = traits_list_2[:-2]

    # Player's specialities
    specialities_label.text = 'Specialities:'
    specialities_list = ''
    specialities_list_2 = ''
    if formation['specialities'] is not None:
        index = 0
        for speciality in formation['specialities']:
            if len(specialities_list + speciality) < 70:
                specialities_list += speciality + ', '
                index += 1
            else:
                break
        for speciality in formation['specialities'][index:]:
            specialities_list_2 += speciality + ', '
    else:
        specialities_list = 'No specialities..'
    specialities_list_label.text = specialities_list[:-2]
    specialities_list_label_2.text = specialities_list_2[:-2]"""

    # ========== Add buttons to window ==========
    view.add(add_formation_btn)
    view.add(back_btn)

    """view.add(player_name_label)
    view.add(player_full_name_label)
    view.add(rating_big_label)"""

    for label in labels_list:
        view.add(label)

    win_formation_bio.add(view)
    view.become_target()
    win_formation_bio.show()
