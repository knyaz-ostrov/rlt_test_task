import json



FILE_PATH = 'data/data/config.json'



class BotConfig:
    with open(FILE_PATH) as file:
        __bot_config = json.load(file)['bot']

    token = __bot_config['token']



class MongoConfig:
    with open(FILE_PATH) as file:
        __mongo_config = json.load(file)['mongodb']

    database   = __mongo_config['database']
    collection = __mongo_config['collection']
