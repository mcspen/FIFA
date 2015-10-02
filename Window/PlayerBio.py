from GUI import Button, Geometry, Image, Label, View, Window
from AppConfig import *
import cStringIO
import json
import urllib
from Logic.HelperFunctions import ascii_text, format_attr_name


def open_player_bio_window(window_x, window_y, player, win_search):

    # ========== Window ==========
    win_player_bio = Window()
    win_player_bio.title = player_bio_win_title
    win_player_bio.auto_position = False
    win_player_bio.position = (window_x, window_y)
    win_player_bio.size = (win_width, 450)
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
            player_headshot.draw(c, src_rect, dst_rect)

    view = StartWindowImageView(size=win_player_bio.size)

    # ========== Player Headshot ==========
    image_url = player['headshotImgUrl']
    #url_file = requests.get(image_url)
    #url_image = open(StringIO(url_file.content))
    #urllib.urlretrieve(image_url, 'C:\Users\mspencer\PycharmProjects\FIFA\Images')
    player_headshot = Image(file = 'Images/headshot.png')

    # ========== Button Declarations ==========
    back_btn = Button("Back")

    # ========== Button Functions ==========
    def back_btn_func():
        win_player_bio.hide()
        win_search.show()

    # ========== Buttons ==========
    back_btn.x = (win_width - button_width) / 2
    back_btn.y = win_player_bio.height - button_height - button_spacing
    back_btn.height = button_height
    back_btn.width = button_width
    back_btn.font = button_font
    back_btn.action = back_btn_func
    back_btn.style = 'default'
    back_btn.color = button_color
    back_btn.just = 'right'

    # ========== Player Info Labels ==========
    # Get attribute lists
    with open('configs.json', 'r') as f:
        attribute_lists = json.load(f)['player_attributes']
        f.close()

    labels_list = []

    name_width = 300
    rating_big_width = 35

    traits_offset_left = 25
    traits_label_width = 100
    traits_list_label_width = 500 - traits_label_width

    section_label_width = 100

    # ========== Name and Rating ==========
    player_name_label = Label(font=title_font, width=name_width, height=title_height, x=(win_width - name_width)/2,
                               y=top_border, color=title_color, just='center')
    labels_list.append(player_name_label)
    player_full_name_label = Label(font=title_tf_font, width=name_width, height=std_tf_height,
                                   x=(win_width - name_width)/2, y=player_name_label.bottom - title_border,
                                   color=title_color, just='center')
    labels_list.append(player_full_name_label)
    rating_big_label = Label(font=title_font, width=rating_big_width, height=title_height,
                             x=player_full_name_label.left - rating_big_width - title_border,
                             y=player_full_name_label.top - title_border, color=title_color, just='center')
    labels_list.append(rating_big_label)

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

    # ========== Attributes Under piecture Section ==========
    '''attributes_label = Label(font=std_tf_font_bold, width=section_label_width, height=std_tf_height,
                               x=3*(win_width - 4*section_label_width)/5 + 2*section_label_width - 25,
                               y=personal_label.top, color=title_color, just='center')
    labels_list.append(attributes_label)

    attr_title_label_width = 30
    attr_label_width = 20
    attribute_x_offset = 30
    label_x = attributes_label.left + section_label_width/2 - attribute_x_offset
    label_y = attributes_label.bottom

    for idx, attr in enumerate(player['attributes']):
        if idx == 3:
            label_x = attributes_label.left + section_label_width/2 + attribute_x_offset
            label_y = attributes_label.bottom

        stat_title_label = Label(font=small_tf_font, width=attr_title_label_width, height=std_tf_height,
                               x=label_x-attr_title_label_width, y=label_y, color=title_color, just='right')
        stat_title_label.text = format_attr_name(attr['name'][-3:]) + ':'
        labels_list.append(stat_title_label)

        stat_label = Label(font=small_tf_font, width=attr_label_width, height=std_tf_height,
                               x=label_x, y=label_y, color=title_color, just='right')
        stat_label.text = str(attr['value'])
        labels_list.append(stat_label)

        label_y += std_tf_height'''


    attr_title_label_width = 30
    attr_label_width = 20
    attribute_x_offset = 30
    label_x = (player_name_label.left - player_headshot.width)/2 + player_headshot.width/2 - attribute_x_offset
    label_y = player_name_label.top + player_headshot.height

    for idx, attr in enumerate(player['attributes']):
        if idx == 3:
            label_x = (player_name_label.left - player_headshot.width)/2 + player_headshot.width/2 + attribute_x_offset
            label_y = player_name_label.top + player_headshot.height

        stat_title_label = Label(font=small_tf_font, width=attr_title_label_width, height=std_tf_height,
                               x=label_x-attr_title_label_width, y=label_y, color=title_color, just='right')
        stat_title_label.text = format_attr_name(attr['name'][-3:]) + ':'
        labels_list.append(stat_title_label)

        stat_label = Label(font=small_tf_font, width=attr_label_width, height=std_tf_height,
                               x=label_x, y=label_y, color=title_color, just='right')
        stat_label.text = str(attr['value'])
        labels_list.append(stat_label)

        label_y += std_tf_height

    # ========== Personal Section ==========
    personal_label = Label(font=std_tf_font_bold, width=section_label_width, height=std_tf_height,
                           #x=(win_width - 3*section_label_width)/4,
                           x=3*(win_width - 9*section_label_width)/10 + 2*section_label_width,
                           y=specialities_list_label_2.bottom + top_border, color=title_color, just='center')
    labels_list.append(personal_label)

    personal_title_stat_width = 100
    personal_stat_width = 55
    personal_stat_just = 'right'
    personal_x_offset = personal_stat_width + 50
    label_x = personal_label.left + section_label_width/2 - personal_x_offset
    label_y = personal_label.bottom

    for idx, personal in enumerate(attribute_lists['personal']):
        if idx == 7:
            personal_title_stat_width = 75
            personal_stat_width = 200
            personal_stat_just = 'left'
            personal_x_offset = personal_title_stat_width - 50
            label_x = personal_label.left + section_label_width/2 + personal_x_offset
            label_y = personal_label.bottom

        # Skip these since other labels use them
        if personal == 'positionFull':
            continue

        stat_title_label = Label(font=small_tf_font, width=personal_title_stat_width, height=std_tf_height,
                               x=label_x-personal_title_stat_width, y=label_y, color=title_color, just='right')
        stat_title_label.text = format_attr_name(personal) + ':'
        labels_list.append(stat_title_label)

        stat_label = Label(font=small_tf_font, width=personal_stat_width, height=std_tf_height,
                               x=label_x+3, y=label_y, color=title_color, just=personal_stat_just)
        if personal == 'height':
            centimeters = player[personal]
            inches = centimeters/2.54
            stat_label.text = '%d\'%.1f" (%d cm)' % (int(inches/12), inches % 12, centimeters)
        elif personal == 'weight':
            kilograms = player[personal]
            pounds = kilograms*2.20462
            stat_label.text = '%.1f lb (%d kg)' % (pounds, kilograms)
        elif personal in ['club', 'league', 'nation']:
            stat_label.text = ascii_text(player[personal]['name'])
        elif personal == 'birthdate':
            stat_label.text = '%s/%s/%s' % (player['birthdate'][6:7], player['birthdate'][-2:],
                                              player['birthdate'][:4])
        elif personal == 'position':
            stat_label.text = '%s (%s)' % (player['positionFull'], player[personal])
        else:
            stat_label.text = str(player[personal])
        labels_list.append(stat_label)

        label_y += std_tf_height

    # ========== Database Info Section ==========
    db_info_label = Label(font=std_tf_font_bold, width=section_label_width, height=std_tf_height,
                          #x=4*(win_width - 4*section_label_width)/5 + 3*section_label_width - 25,
                          x=7*(win_width - 9*section_label_width)/10 + 6*section_label_width,
                          y=personal_label.top, color=title_color, just='center')
    labels_list.append(db_info_label)

    db_info_title_label_width = 80
    db_info_label_width = 45
    attribute_x_offset = 30
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

    '''for characteristic in attribute_lists['characteristics']:
        stat_title_label = Label(font=std_tf_font, width=stat_title_label_width, height=std_tf_height,
                               x=label_x-stat_title_label_width, y=label_y, color=title_color, just='right')
        stat_title_label.text = format_attr_name(characteristic) + ':'
        labels_list.append(stat_title_label)

        stat_label = Label(font=std_tf_font, width=stat_width, height=std_tf_height,
                               x=label_x, y=label_y, color=title_color, just='right')
        if characteristic in ['weakFoot', 'skillMoves']:
            stat_label.text = '* '*player[characteristic]
        else:
            stat_label.text = str(player[characteristic])
        labels_list.append(stat_label)

        label_y += std_tf_height'''

    # ========== Label Text ==========
    # Player's normal name
    player_name = ascii_text(player['name'])
    player_name_label.text = player_name

    # Player's name
    player_full_name = ascii_text(player['firstName']) + ' ' + ascii_text(player['lastName'])
    player_full_name_label.text = player_full_name

    # Player's rating
    rating_big_label.text = str(player['rating'])

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

    # Player's Personal Info
    personal_label.text = "Personal"
    #attributes_label.text = "Attributes"
    db_info_label.text = "Database Info"
    '''characteristics_label.text = "Characteristics"
    pace_label.text = "Pace"
    dribbling_label.text = "Dribbling"
    shooting_label.text = "Shooting"
    goalkeeping_label.text = "Goalkeeping"
    defending_label.text = "Defending"
    passing_label.text = "Passing"
    physicality_label.text = "Physicality"'''

    # ========== Add buttons to window ==========
    view.add(back_btn)

    view.add(player_name_label)
    view.add(player_full_name_label)
    view.add(rating_big_label)

    '''view.add(traits_label)
    view.add(traits_list_label)
    view.add(traits_list_label_2)
    view.add(specialities_label)
    view.add(specialities_list_label)
    view.add(specialities_list_label_2)

    view.add(personal_label)
    view.add(attributes_label)
    view.add(db_info_label)'''

    for label in labels_list:
        view.add(label)

    win_player_bio.add(view)
    view.become_target()
    win_player_bio.show()
