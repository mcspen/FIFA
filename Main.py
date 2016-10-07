import json
import multiprocessing

import FifaApp
from Window.AppConfig import config_filename
from Logic.FormationDB import FormationDB
from Logic.PlayerDB import PlayerDB
from Logic.TeamDB import TeamDB
from Logic.HelperFunctions import delete_all_temp_images

if __name__ == '__main__':
    multiprocessing.freeze_support()

    # Load defaults
    with open(config_filename, 'r') as f:
        configs = json.load(f)
        f.close()
    default_dbs = configs['default_databases']

    # Set defaults
    player_db = PlayerDB()
    player_list = PlayerDB()
    formation_db = FormationDB()
    formation_list = FormationDB()
    team_list = TeamDB()

    player_db.load(default_dbs['player_db'], 'db')
    player_list.load(default_dbs['player_list'], 'list')
    formation_db.load(default_dbs['formation_db'], 'db')
    formation_list.load(default_dbs['formation_list'], 'list')
    team_list.load(default_dbs['team_list'])

    db_dict = {
        'player_db': (default_dbs['player_db'], player_db),
        'player_list': (default_dbs['player_list'], player_list),
        'formation_db': (default_dbs['formation_db'], formation_db),
        'formation_list': (default_dbs['formation_list'], formation_list),
        'team_list': (default_dbs['team_list'], team_list)
    }

    FifaApp.start_app(db_dict)
    # delete_all_temp_images()
