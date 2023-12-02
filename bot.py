# dotenvのセットアップ
from dotenv import load_dotenv
import os

load_dotenv('.env')

# 正規表現ライブラリのセットアップ

import re

# DiscordBotToken
discord_bot_token = os.environ.get('DISCORD_TOKEN')

# バージョン情報
version = '0.1.2'

# discord.py関連のセットアップ
import discord
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# requests関連のセットアップ
import requests
server_url = 'http://127.0.0.1:5000'

# Flaskサーバーとの疎通確認関数
def check_connection_to_server():
    global discord_bot_token
    connection_status = requests.get(server_url + '/api/check_connection/')
    if connection_status.json()['status'] == 'ok':
        return 'ok'
    else:
        return 'error'

# 起動時疎通確認
launch_connection_test = check_connection_to_server()
if launch_connection_test == 'ok':
    print('Connected server. Got bot token.')
else:
    print('Error!')

# メッセージ発出時
@client.event
async def on_message(message):

    # ヘルプコマンド
    if client.user in message.mentions:
        if message.content.endswith('help'):
            await message.channel.send('以下のコマンドが利用できます。\n\n@Bot server status\n@Bot version\n@Bot member\n\n詳細は、GitHub上の[README.md](https://github.com/ko-en-hookah/flip-kun)をご覧ください。')

    # 疎通確認コマンド
    if client.user in message.mentions:
        if re.search('server status', message.content):
            res = check_connection_to_server()
            if res == 'ok':
                await message.channel.send('サーバーと接続しています')
            else:
                await message.channel.send('サーバーとの接続が確認できません')

    # バージョン確認コマンド
    if client.user in message.mentions:
        if re.search('version', message.content):
            await message.channel.send(f'バージョン：{version}')

    # memberコマンド
    if client.user in message.mentions:
        if re.search('member', message.content):
            await message.channel.send('利用者をセットします。\n参加者は、本投稿に何かしらのリアクションをつけてください。')

    # memberコマンドのセルフリアクション
    if message.author == client.user:
        if message.content.startswith('利用者をセットします。'):
            await message.add_reaction('\N{sparkles}')

    # DM受信時(Bot自身からの投稿は除く)
    if isinstance(message.channel, discord.DMChannel) and message.author != client.user:
        res = requests.post(server_url + '/api/answer/', json={'name':message.author.name, 'text':message.content})
        if res.text == 'ok':
            await message.channel.send("登録しました。")
        elif res.text == '回答を受け付けていません':
            await message.channel.send('回答を受け付けていません')
        elif res.text == '参加登録していません':
            await message.channel.send('参加登録されていません')

# リアクション検知
@client.event
async def on_reaction_add(reaction, user):
    # リアクションが追加されたメッセージがBot自身によるもので、
    # リアクションを追加したユーザーがBot自身でない場合にのみ、ユーザー登録処理を実行
    if reaction.message.author == client.user and user != client.user:
        print(f'joined by {user.name}!')
        requests.post(server_url + '/api/user/add', json={'name':user.name})

# Discord botの実行
client.run(discord_bot_token)