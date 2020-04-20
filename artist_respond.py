from train import  interpreter
from spotify_config import *
import random



artist_responses = [
    "I'm sorry :( I couldn't find anything like that",
    '{} is a great singer!',
    '{} or {} would work!',
    '{}, {} or {} would work!',
    '{} must be the one you like \U0001F388, but I know others too: {}, {}, {}.'
]


#判断被否定的实体，用result储存并返回
def negated_ents(phrase, ent_vals):
    ents = [e for e in ent_vals if e in phrase]
    ends = sorted([phrase.index(e) + len(e) for e in ents])
    start = 0
    chunks = []
    for end in ends:
        chunks.append(phrase[start:end])
        start = end
    result = {}
    for chunk in chunks:
        for ent in ents:
            if ent in chunk:
                if str(ent) == 'popular' or str(ent) == 'not_popular':
                    if "not" in chunk or "n't" in chunk:
                        result[ent] = False
                    else:
                        result[ent] = True
    return result


#根据genre搜寻歌手
# 被modify_artists(params, neg_params, genre)和artist_respond(message, genre)两个函数用到
def get_artists(genre,entity):
    artists = {}

    #offset指的是从搜寻结果的offset位置开始取
    #当用户要求流行度时，当前搜寻出来的歌手不一定有满足的，所以设置随机数，在modify_artists()函数中重复搜寻
    if entity == 'popularity':
        offset = random.randint(0, 500)
    offset = 0
    results = sp.search(q='genre:' + genre, offset=offset, limit=50, type='artist')
    numOfArtists = len(results['artists']['items'])
    for i in range(0, (numOfArtists - 1)):
        artists[results['artists']['items'][i]['name']] = results['artists']['items'][i]['popularity']

     # 把artists中popularity的整数值变为popular和not_popular
    for k, v in artists.items():
        if v >= 60:
            artists[k] = 'popular'
        elif v < 40:
            artists[k] = 'not_popular'
        elif v >= 40 or v <= 60:
            artists[k] = 'mid'

    return artists,numOfArtists

#根据否定实体筛选歌手
def modify_artists(params, neg_params, genre):
    artists, numOfArtists = get_artists(genre,'popularity')

    #使用get_artists()多次搜寻，直到符合要求为止
    if 'popular' in params or 'not_popular' in neg_params:
        while('popular' not in artists.values()):
            artists,numOfArtists = get_artists(genre,'popularity')
    if 'not_popular' in params or 'popular' in neg_params:
        while ('not_popular' not in artists.values()):
            artists,numOfArtists = get_artists(genre,'popularity')

    if len(neg_params) > 0:
        for key in list(artists.keys()):
            if artists[key] == neg_params[0] or artists[key] == 'mid':
                del artists[key]
                continue
    elif len(params) > 0:
        artists = {k:v for k,v in artists.items() if v==params[0]}

    return artists,numOfArtists



def artist_respond(message, genre):
    # 刷新TOKEN
    refresh()

    params = {}
    neg_params = {}
    response_template = "{}"

    entities = interpreter.parse(message)["entities"]
    ent_vals = [e["value"] for e in entities]

    #防止用户再次发问，或者说不相关的话
    if len(ent_vals)==0:
        return "I'd like to search for you! Please tell me the genre you prefer\U0000270D ~  ", genre
    popularity_negated = negated_ents(message, ent_vals)

    for ent in entities:
        #当实体为genre时候，循环丰富genre语句
        if str(ent["entity"]) =='genre':
            print(ent["value"])
            genre = genre + '&' + str(ent["value"])
            print(genre)
            artists,numOfArtists=get_artists(genre,ent["entity"])

        #当实体为流行度时，进入甄别否定实体并筛选的阶段
        elif str(ent["entity"]) == 'popularity':
            response_template = " \U0001F44COK! I made a fine selection for you. {} "
            if ent["value"] in popularity_negated and not popularity_negated[ent["value"]]:
                neg_params = [str(ent["value"])]
            else:
                params = [str(ent["value"])]
            artists,numOfArtists = modify_artists(params, neg_params, genre)

    #在artist_responses[]中选择回答模式，若人数大于四则都选择第4种模式
    n = min(numOfArtists, 4)
    names = artists.keys()
    response = response_template.format(artist_responses[n].format(*names))
    return response, genre



genre = ''

'''
#测试用
for message in ["Which singer do you think I like", "artists built for party","i prefer genres like: soul， too","show me niche singers"]:
    print("USER: {}".format(message))
    response, genre = artist_respond(message, genre)
    print("BOT: {}".format(response))
'''