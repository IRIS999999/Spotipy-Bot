import spotipy

#配置spotify api相关
scopes = 'user-library-read'
CACHE = '.spotipyoauthcache'
sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id='5a8ccbe880b94df3859c6c0d601c24db',client_secret='7c2bccc60d9a400faaf3145a8990b214',redirect_uri='https://example.com/callback/',scope=scopes,cache_path=CACHE)
token_info = sp_oauth.get_cached_token()
if not token_info:
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    response = input('Paste the above link into your browser, then paste the redirect url here: ')
    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)

token = token_info['access_token']

#刷新token的函数
def refresh():
    global token_info, sp

    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        token = token_info['access_token']
        sp = spotipy.Spotify(auth=token)


sp = spotipy.Spotify(auth=token)


