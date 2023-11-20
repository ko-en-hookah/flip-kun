# Flask初期化
from flask import Flask, request, render_template, jsonify
app = Flask(__name__, static_folder='./templates/img')

# ユーザーリスト
user_data = []

# 状態フラグ
is_answer_receiving = False

# DiscordBotToken
discord_bot_token = ''

# 管理画面リクエスト
@app.route('/')
def root():
    return render_template('index.html')

# 疎通確認API
@app.route('/api/check_connection/', methods=['GET'])
def connection_check():
    res = {
        'status': 'ok',
        'token': discord_bot_token
    }
    return res, 200

# Discord bot token登録API
@app.route('/api/set_token/', methods=['POST'])
def set_token():
    global discord_bot_token
    payload = request.json
    discord_bot_token = payload.get('token')
    return 'ok', 201

# ユーザー登録API
@app.route('/api/user/add', methods=['POST'])
def add_user():
    payload = request.json
    name = payload.get('name')
    if check_attendance(name):
        return 'this user already attendanced.', 207
    else:
        user_data.append({'name': name, 'answer': '', 'open': False})
        print(f'joined by {name}')
        return 'added ' + name, 201

# ユーザーデータ取得API
@app.route('/api/status/get_user_data/', methods=['GET'])
def check_user_data():
    return jsonify(user_data), 200

# ユーザー削除API
@app.route('/api/user/delete/', methods=['DELETE'])
def delete_user():
    global user_data
    name = request.json.get('name')
    print(name)
    delete_number = 0
    for i, w in enumerate(user_data):
        if w['name'] == name:
            delete_number = i
            break
    user_data.pop(delete_number)
    return 'deleted', 200

# 回答を全員オープン
@app.route('/api/status/answer_open_all/', methods=['POST'])
def answer_open_all():
    global user_data
    for i in range(len(user_data)):
        user_data[i]['open'] = True
    return 'ok', 200

# 特定のユーザーの回答をオープン
@app.route('/api/status/answer_open/', methods=['POST'])
def answer_open():
    global user_data
    payload = request.json
    delete_number = 0
    name = payload.get('name')
    for i, w in enumerate(user_data):
        if w['name'] == name:
            delete_number = i
    user_data[delete_number]['open'] = True
    return 'ok', 200

# 回答を全員クローズ
@app.route('/api/status/answer_close_all/', methods=['POST'])
def answer_close_all():
    global user_data
    for i in range(len(user_data)):
        user_data[i]['open'] = False
    return 'ok', 200

# 特定のユーザーの回答をクローズ
@app.route('/api/status/answer_close/', methods=['POST'])
def answer_close():
    global user_data
    payload = request.json
    delete_number = 0
    name = payload.get('name')
    for i, w in enumerate(user_data):
        if w['name'] == name:
            delete_number = i
    user_data[delete_number]['open'] = False
    return 'ok', 200

# 回答受付スタートAPI
@app.route('/api/status/answer_recieving_true/', methods=['POST'])
def answer_recieving_true():
    global is_answer_receiving
    is_answer_receiving = True
    return 'ok', 204

# 回答受付終了API
@app.route('/api/status/answer_recieving_false/', methods=['POST'])
def answer_recieving_false():
    global is_answer_receiving
    is_answer_receiving = False
    return 'ok', 204

# 回答受付状況確認API
@app.route('/api/status/check_answer_recieving_status/', methods=['GET'])
def check_answer_recieving_status():
    if is_answer_receiving:
        return 'True', 200
    else:
        return 'False', 200

# 参加者かどうかの確認関数
def check_attendance(name):
    for w in user_data:
        if w['name'] == name:
            return True
    return False

# 回答記録関数
def add_answer(name, text):
    for i, w in enumerate(user_data):
        if w['name'] == name:
            user_data[i]['answer'] = text
            print(f'{name}: {text}')

# 回答送信API
@app.route('/api/answer/', methods=['POST'])
def answer():
    payload = request.json
    name = payload.get('name')
    text = payload.get('text')
    # 回答を受付中、かつ、参加者からのDMである
    if is_answer_receiving == True and check_attendance(name):
        add_answer(name, text)
        return 'ok', 201
    # 回答を受付していない
    elif is_answer_receiving == False:
        return '回答を受け付けていません', 403
    # 参加登録をしていない人からのDM
    else:
        return '参加登録していません', 403
    
# フリップ画面
@app.route('/flip/<name>')
def flip(name):
    if check_attendance(name):
        # 参加者だった場合の処理
        return render_template('flip.html', name=name), 200
    else:
        return render_template('404.html'), 404
    
# フリップ画面からの情報取得
@app.route('/api/status/get_answer_and_open_status/', methods=['GET'])
def get_answer_and_open_status():
    name = request.args.get('name')
    print(name)
    if name == '':
        return 'no answer', 404
    else: 
        for w in user_data:
            if w['name'] == name:
                response = {
                    'answer':w['answer'],
                    'open':w['open']
                }
                return jsonify(response)