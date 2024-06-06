import lxml.etree as ET



FILE_PATH = 'data/data/bot_data.xml'
path_template = './/{}'
filter = '[@id="{}"]'



class BotMessageText:
    bot_data = ET.parse(FILE_PATH)
    category = 'text'
    path = path_template.format(category) + filter

    start             = bot_data.xpath(path.format('start'))[0].text
    incorrect_request = bot_data.xpath(path.format('incorrect_request'))[0].text

    del bot_data, category, path
