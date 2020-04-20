from train import interpreter
from spotify_config import *
from telegram import bot


def send_message(state, pending, message,artist_id_list,genre_list,recommendations_id_list,username,playlist_id):
    # 刷新TOKEN
    refresh()
    recommendations_name_list = []
    #这里传进来的message是telebot的message对象，要先转换为str类型才可进行实体识别
    strMessage = str(message.text)

    #识别意图，提取实体
    intent = interpreter.parse(strMessage)['intent']['name']
    entities = interpreter.parse(strMessage)["entities"]
    for ent in entities:
        if str(ent["entity"]) =='artist':
            artist = sp.search(q='artist:' + str(ent["value"]), type='artist')
            artist_id = artist['artists']['items'][0]['id']
            #保存artis的id用于作为seed_artists进行搜寻
            artist_id_list.append(artist_id)
        elif str(ent["entity"]) =='genre':
            #提取genre，作为seed_genres
            genre_list.append(ent["value"])

    #intent!='affirm'的原因是当用户同意加入歌单后，就不能再通过sp.recommendations()重新搜寻一批新的歌出来
    if len(artist_id_list) and len(genre_list) and intent!='affirm' :
        recommendations = sp.recommendations(seed_artists=artist_id_list, seed_genres=genre_list, limit=10)
        for i in range(0,6):
            #保存歌曲名字，用于展现给用户
            recommendations_name_list.append(recommendations['tracks'][i]['name'])
            #保存歌曲id，用于添加进歌单
            recommendations_id_list.append(recommendations['tracks'][i]['id'])
    #更新状态，改变pending_state
    new_state, response, pending_state = policy_rules[(state, intent)]
    response = str(response).format(*recommendations_name_list)
    bot.reply_to(message, response)

    #若用户回答为肯定，则推进待定时间
    if pending is not None and intent == 'affirm':
        new_state, response, pending_state = policy_rules[pending]
        sp.user_playlist_add_tracks(user = username, playlist_id = playlist_id, tracks=recommendations_id_list, position=None)
        bot.reply_to(message, response)
    if pending_state is not None:
        pending = (pending_state, intent)
    return new_state, pending, artist_id_list, genre_list,response,recommendations_id_list

#定义状态
GetSingers=1
GetGenres=2
TellTracks=3
AddTracks=4
Final=5

# Define the policy rules
policy_rules = {
    (GetSingers, "tell_singers"): (GetGenres, "For a better recommendation, please let me know the genres you like.\U0001F9E1", None),
    (GetGenres, "tell_genres"): (TellTracks, "\U0001F61CGreat! Here are some tracks for you: \n{},\n{},\n{}, \n{},\n{}, \n{}. \nDo you want to add them in your playlist? ", AddTracks),
    (AddTracks, "tell_genres"): (Final, "I already add them, ENJOY! \U0001F60A", None),
    (TellTracks,"deny"):(Final, "\U0001F633If don't, that's OK ~",None),
    (TellTracks, "affirm"):(Final, "OK, wait few seconds\U0001F60E.", None)
}

'''
#用于测试
def send_messages(messages):
    state = GetSingers
    artist_id_list = []
    genre_list = []
    pending = None
    for msg in messages:
        state, pending,artist_id_list,genre_list = send_message(state, pending, msg,artist_id_list,genre_list)

# Send the messages
send_messages([
    "i love artists like Taylor Swift, Kali Uchis, Harry Styles.",
    "the styles like: jazz, k-pop, pop",
    "yes"
])
'''