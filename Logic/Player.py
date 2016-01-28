import json
import requests


class Player:
    """
    The Player class contains all of an individual player's information and attributes
    """

    def __init__(self, input_dict):
        """
        Initialization function - copies a dict from input.
        Input: Player dictionary.
        Output: None  -  the player is created.
        """

        # Custom Info
        if 'price' in input_dict:
            self.price = input_dict['price']
        else:
            self.price = 0

        # Summary Info
        self.id = input_dict['id']
        self.baseId = input_dict['baseId']
        self.name = input_dict['name']
        self.quality = input_dict['quality']
        self.color = input_dict['color']
        self.isGK = input_dict['isGK']
        self.positionFull = input_dict['positionFull']
        self.isSpecialType = input_dict['isSpecialType']
        self.itemType = input_dict['itemType']
        self.modelName = input_dict['modelName']
        self.rating = input_dict['rating']
        self.playerType = input_dict['playerType']

        # Name and Bio
        self.commonName = input_dict['commonName']
        self.firstName = input_dict['firstName']
        self.lastName = input_dict['lastName']
        self.league = input_dict['league']
        self.nation = input_dict['nation']
        self.club = input_dict['club']
        self.headshot = input_dict['headshot']
        self.headshotImgUrl = input_dict['headshotImgUrl']
        self.position = input_dict['position']
        self.playStyle = input_dict['playStyle']
        self.height = input_dict['height']
        self.weight = input_dict['weight']
        self.birthdate = input_dict['birthdate']
        self.age = input_dict['age']

        # Game stats
        self.acceleration = input_dict['acceleration']
        self.aggression = input_dict['aggression']
        self.agility = input_dict['agility']
        self.balance = input_dict['balance']
        self.ballcontrol = input_dict['ballcontrol']
        self.crossing = input_dict['crossing']
        self.curve = input_dict['curve']
        self.dribbling = input_dict['dribbling']
        self.finishing = input_dict['finishing']
        self.foot = input_dict['foot']
        self.freekickaccuracy = input_dict['freekickaccuracy']
        self.gkdiving = input_dict['gkdiving']
        self.gkhandling = input_dict['gkhandling']
        self.gkkicking = input_dict['gkkicking']
        self.gkpositioning = input_dict['gkpositioning']
        self.gkreflexes = input_dict['gkreflexes']
        self.headingaccuracy = input_dict['headingaccuracy']
        self.interceptions = input_dict['interceptions']
        self.jumping = input_dict['jumping']
        self.longpassing = input_dict['longpassing']
        self.longshots = input_dict['longshots']
        self.marking = input_dict['marking']
        self.penalties = input_dict['penalties']
        self.positioning = input_dict['positioning']
        self.potential = input_dict['potential']
        self.reactions = input_dict['reactions']
        self.shortpassing = input_dict['shortpassing']
        self.shotpower = input_dict['shotpower']
        self.skillMoves = input_dict['skillMoves']
        self.slidingtackle = input_dict['slidingtackle']
        self.sprintspeed = input_dict['sprintspeed']
        self.standingtackle = input_dict['standingtackle']
        self.stamina = input_dict['stamina']
        self.strength = input_dict['strength']
        self.vision = input_dict['vision']
        self.volleys = input_dict['volleys']
        self.weakFoot = input_dict['weakFoot']
        self.traits = input_dict['traits']
        self.atkWorkRate = input_dict['atkWorkRate']
        self.defWorkRate = input_dict['defWorkRate']
        self.attributes = input_dict['attributes']
        self.specialities = input_dict['specialities']

    def get_price(self, console='PS4', update_rating=0, update_price=-1):
        """
        Get's the price of the player from futbin.com
        Input: None.
        Output: The price, and the player's price is set.
        """

        # Skip price if player is legend and console is PS4
        # Legends are only on X-Box
        if console == 'PS4' and self.color == 'legend':
            self.price = -1
            return self.price

        if self.rating >= update_rating and self.price >= update_price:
            price_site_url_search = 'http://www.futbin.com/api/?term='
            price_site_url_player = 'http://www.futbin.com/16/player'
            player_name = ''
            player_id = ''

            try:
                # Create session
                sess = requests.Session()

                # Search for player and get id and name
                page_data = json.loads(sess.get(price_site_url_search + self.name).content)
                for player_data in page_data:
                    if int(player_data['rating']) == self.rating and\
                       player_data['position'] == self.position:
                        player_name = player_data['full_name']
                        player_id = player_data['id']
                        break

                if player_name != '' and player_id != '':
                    # Get page data of player
                    page_data = sess.get("%s/%s/%s" % (price_site_url_player, player_id, player_name)).content

                    # Get price
                    page_data = page_data.split()
                    if console == 'PS4':
                        index = page_data.index('id="pslowest"') + 1
                    else:
                        index = page_data.index('id="xboxlowest"') + 1

                    price = page_data[index]
                    price = int(price[13:-6])

                else:
                    price = 0

                self.price = price

            except Exception as err:
                print "Not connected to internet. Cannot get player price.\nOr Error:" + err.message

        return self.price
