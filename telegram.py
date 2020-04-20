import telebot
from config import TOKEN
from train import interpreter
from recommend_respond import *
from artist_respond import *
from greet_respond import *
from newReleases_responde import *

bot = telebot.TeleBot(TOKEN)

 #为意图初始化标识，为全局变量，为0代表该意图尚未发生
greetIntent = 0
artistIntent =0
recommendIntent = 0
newReleaseIntent = 0

#各种初始化
GetSingers=1
GetGenres=2
TellTracks=3
AddTracks=4
Final=5
state = GetSingers
artist_id_list = []
genre_list = []
recommendations_id_list=[]
pending = None
genre = ''
user=''
playlistID=''

#状态标签判断函数
def greetBoolen():
    global greetIntent
    if greetIntent == 1:
        return True
    return False

def artistBoolen():
    global artistIntent
    if artistIntent == 1:
        return True
    return False

def recommendBoolen():
    global recommendIntent
    if recommendIntent == 1:
        return True
    return False

def newRleaseBoolen():
    global newReleaseIntent
    if newReleaseIntent == 1:
        return True
    return False

def boolen():
    global recommendIntent,newReleaseIntent, greetIntent,artistIntent
    #只有当每一个状态的标签都为0时才能返回Ture
    #用于interpret_intent(message)
    if recommendIntent+greetIntent+artistIntent+newReleaseIntent == 0:
        return True
    return False

#最初的判断意图的函数（四种意图）
@bot.message_handler(func=lambda b: boolen())
def interpret_intent(message):
    intent = interpreter.parse(str(message.text))['intent']['name']
    if intent=='ask_recommendation':
        global recommendIntent
        #将意图标签置1，表示改意图开始执行
        recommendIntent = 1
        bot.send_message(reply_to_message_id=message.message_id, chat_id=message.chat.id, text="I'll recommend something you like! Please tell me your favourite artists first ~ \U0001F497 ")
    elif intent=='artist_search':
        global artistIntent
        artistIntent = 1
        bot.send_message(reply_to_message_id=message.message_id, chat_id=message.chat.id, text="I'd like to search for you! Please tell me the genre you prefer ~ \U0001F3A7 ")
    elif intent=='greet':
        global greetIntent
        greetIntent = 1
        bot.send_message(reply_to_message_id=message.message_id, chat_id=message.chat.id, text="Nice to meet youu\U0001F609! For better service, please tell me your Spotify user id in this format: user:your user_id")
    elif intent=='new_release':
        global newReleaseIntent
        newReleaseIntent = 1
        albums_list =[]
        results = sp.new_releases(country=None, limit=10, offset=0)
        numOfAlbums = len(results['albums']['items'])
        for i in range(0, numOfAlbums - 1):
            album = results['albums']['items'][i]['name'] + ' by ' + results['albums']['items'][i]['artists'][0]['name']
            albums_list.append(album)
        phrase1 = 'New album lately: \n {} \n {} \n {} \n {} \n {} \n {} \n {} \n {}'.format(*albums_list)
        phrase2 = '\n In case that some album may be unavailable in your country, you better tell me your country name ~\U0001F4AD'
        response = phrase1 + phrase2
        bot.send_message(reply_to_message_id=message.message_id, chat_id=message.chat.id, text=response)

#接受意图'ask_recommendation'
@bot.message_handler(func=lambda a: recommendBoolen())
def reommendation(message):
    global state,artist_id_list,genre_list,pending,recommendations_id_list
    global user, playlistID
    username = user
    playlist_id = playlistID
    state, pending, artist_id_list, genre_list,response,recommendations_id_list = send_message(state, pending, message, artist_id_list, genre_list,recommendations_id_list,username,playlist_id)

    #判断一个意图的结束，将意图标签置回0
    #将各种变量初始化，以防干扰下一个这样的意图
    if response=="\U0001F633If don't, that's OK ~" or response=="I already add them, ENJOY! \U0001F60A":
        global recommendIntent
        recommendIntent = 0
        state = GetSingers
        artist_id_list = []
        genre_list = []
        recommendations_id_list=[]
        pending = None

#接受意图'artist_search'
@bot.message_handler(func=lambda c: artistBoolen())
def artist_search(message):
    strMessage = str(message.text)
    global genre
    response, genre = artist_respond(strMessage, genre)
    bot.reply_to(message, response)
    endRespond = re.compile('OK! I made a fine selection for you.')
    if endRespond.search(response):
        global artistIntent
        artistIntent = 0
        genre = ''

#接受意图'greet'
@bot.message_handler(func=lambda d: greetBoolen())
def greet(message):
    strMessage = str(message.text)
    global user, playlistID
    playlist_id = playlistID
    username = user
    response,username,playlist_id = greet_respond(rules, strMessage,playlist_id,username)
    user = username
    playlistID = playlist_id
    bot.reply_to(message, response)
    endRespond = re.compile('Wonderful! Feel free to ask me now!')
    if endRespond.search(response):
        global greetIntent
        greetIntent = 0

#接受意图'new_release'
@bot.message_handler(func=lambda e: newRleaseBoolen())
def newRleases(message):
    strMessage = str(message.text)
    response = newRleases_respond(strMessage)
    bot.reply_to(message, response)
    endRespond = re.compile('Got it! Here are new albums available in')
    if endRespond.search(response):
        global newReleaseIntent
        newReleaseIntent = 0

if __name__ == '__main__':
    bot.polling()

