# Spotify Bot
## 功能
Spotify Bot是一个基于自然语言处理技术的对话机器人。它是利用rasa_nlu，通过Spotipy包从spotify获取信息，使用pyTelegramBotAPI包构建Telegram的音乐领域的对话机器人，可以对四种意图进行多轮多次的问答。
## 意图一：向Spotify Bot打招呼，设定用户数据
![image](https://github.com/IRIS999999/Spotipy-Bot/blob/master/gifs/greet.gif)
* 打招呼可以是其他打招呼的语句，如`hello`,`good morning`等
* 但是输入用户名和歌单号只能按照bot的要求输入
## 意图二：推荐歌曲，选择是否加入playlist
![image](https://github.com/IRIS999999/Spotipy-Bot/blob/master/gifs/tracks.gif)
* 根据机器人的提示，告诉他你喜爱的歌手名称和流派（比如pop、rock、party等），机器人将这些特点作为推荐的 “种子” 来为你推荐
* 询问是否加入你设定的playlist里面时，可以选择同意，之后你的默认playlist里面就有这些歌曲了
* 当然也可以拒绝它，它将不会做其他操作
## 意图三：新专辑速递
![image](https://github.com/IRIS999999/Spotipy-Bot/blob/master/gifs/new_releases.gif)
* 如上图所示，Spotify Bot可以告知用户在特定国家新发行的专辑
## 意图四：根据用户要求的流行度和流派搜索歌手
![image](https://github.com/IRIS999999/Spotipy-Bot/blob/master/gifs/artist.gif)
* 告诉Spotify Bot喜爱的流派（可重复、多次告诉）
* 对歌手的流行度提出要求，除了`popular`和`not popular`，你可以有多种表述来形容流行度，如`prevailing`,`famous`,`niche`,
`little-known`等
* 支持带有否定的回答，如上图所示，用户要求是`not popular`，机器人推荐的便是不流行的小众歌手
# 引用
[构建rasa_nlu训练数据的好工具 rasa NLU Trainer](https://rasahq.github.io/rasa-nlu-trainer/) <br>
[Spotipy文档](https://spotipy.readthedocs.io/en/2.9.0/) <br>
[pyTelegramBotAPI文档](https://github.com/eternnoir/pyTelegramBotAPI) <br>
