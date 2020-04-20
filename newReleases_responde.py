from train import interpreter
from spotify_config import *
import pycountry

def newRleases_respond(message):
    # 刷新TOKEN
    refresh()

    #初始化
    country_code = ''
    albums_list = []
    phrase2 = ''
    phrase1 =''

    #实体识别
    entities = interpreter.parse(message)["entities"]
    for ent in entities:
        if str(ent["entity"]) == 'country':
            print(ent["value"])
            country = ent["value"].capitalize()
            country_code = pycountry.countries.get(name= country).alpha_2
            print(ent["value"])
        if country_code!='':
            print(country_code)
            results = sp.new_releases(country=country_code, limit=10, offset=0)
            numOfAlbums = len(results['albums']['items'])
            for i in range(0,numOfAlbums-1):
                album = results['albums']['items'][i]['name'] + ' by ' + results['albums']['items'][i]['artists'][0]['name']
                albums_list.append(album)
                #根据搜出来专辑的个数决定{}的个数，以免{}个数多于专辑个数而报错
                phrase2 = phrase2 +'\n {}'
        phrase1 = ' \U0001F929Got it! Here are new albums available in {}'.format(ent["value"])
    phrase2 = phrase2.format(*albums_list)
    response = phrase1 + phrase2
    return  response







