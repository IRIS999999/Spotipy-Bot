import re
from spotify_config import *
import spotipy

rules = {'user: (.*)': 'Hello, {}! Choose one of your playlists in case that you want me to add some tracks in it: \n {} just send me the number.',
         '(\d+)':'Wonderful! Feel free to ask me now!'
         }


# Define match_rule()
def greet_respond(rules, message, playlist_id,username):
    # 刷新TOKEN
    refresh()
    #缺省回答（message不匹配任何一个正则表达式）
    response = " \U00002757Please input as required!\U00002757"
    playlist_id = playlist_id
    username = username

    # 在rules字典中寻找正则匹配
    for key, value in rules.items():
        match = re.search(key, message)
        if match is not None:
            response = rules[key]
            if '{}' in response:
                username = match.group(1)
                response = response.format(*[username, {}])

                #若输入的用户名不存在，捕获异常，回答找不到该用户
                try:
                    playlists = sp.user_playlists(username, limit=20, offset=0)
                    playlist_phrase = ''
                    i = 0
                    for playlist in playlists['items']:
                        playlist_phrase = playlist_phrase + str(i) + ':' + playlist['name'] + '\n'
                        i = i+1
                    response = response.format(playlist_phrase)
                except spotipy.client.SpotifyException:
                    response = ' \U00002753Sorry, I cannot find this account. \U0001F914Are you sure this user ID is right? '
            else:
                playlist_number = int(match.group(1))
                playlists = sp.user_playlists(username, limit=20, offset=0)
                playlist_id = playlists['items'][playlist_number]['id']

    return response,username,playlist_id



