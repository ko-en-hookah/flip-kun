# フリップくん

## ファイル構成

- `server.py`
- `bot.py`
- `templates`フォルダ
  - `img`フォルダ
    - `flip_cover.png`
    - `flip_flame.png`
  - `index.html`
  - `flip.html`
  - `404.html`

## 事前準備

1. Discord.pyのインストール

```Bash
pip install discord.py
```

2. Flaskのインストール

```Bash
pip install Flask
```

3. requestsのインストール

```Bash
pip install requests
```

4. dotenvのインストール

```Bash
pip install python-dotenv
```

必要に応じてvenvを構築してください。

5. .envファイルの作成

example_.envを参考に、.envファイルを作ってください。
必要な環境変数は以下。

- ENDPOINT
  - サーバーのエンドポイントとなります。基本的にはexample_.envに記載されている`http://127.0.0.1:5000`で問題ないです。
- DISCORD_TOKEN
  - Discord Developer Portalで作成したApplicationのtokenを入力してください。

## 実行

1. `server.py`を実行する

```Bash
flask --app server run
```

2. `http://127.0.0.1:5000`にアクセスする(以下、管理画面)

3. `bot.py`を実行する

```Bash
python app.py
```

## 使い方

### 参加者の登録

1. botにメンションを送る

```Plain
@XXX(bot) member
```

botから以下の様なメッセージが投稿されます。

```Plain
利用者をセットします。
参加者は、本投稿に何かしらのリアクションをつけてください。
```

2. 参加者が、投稿されたメッセージにリアクションする

botがリアクションを受け取ると、管理画面の「参加者リスト」にリアクションした人が並びます。

### OBSの設定

1. 参加者リストの右側にある「フリップ画面」リンクで飛んだ先のURLを、OBSのブラウザソースに入れる

その際の設定は以下

- 幅：1280px
- 高さ：720px
- CSS：なし(削除)

### フリップ使用

以下操作を行い、フリップを操作してください。

#### 回答状況受付切り替え

「回答受付状況」欄に、現在回答を受け付けているかどうかの表示があります。
「回答受付スタート」「回答受付終了」ボタンで切り替えることができます。

#### 回答オープン／クローズ

下記いずれかの方法で回答をオープン／クローズすることができる

- 参加者リスト各人の右にある「回答をオープン」／「回答をクローズ」ボタンを押す(個別オープン／クローズ)
- 参加者リスト下部の「回答全オープン」／「回答を全クローズ」ボタンを押す(全オープン／クローズ)

## フリップ画像のカスタマイズ

以下ファイルを差し替えることで対応できます。

- /templates/img/flip_cover.png
  - 回答クローズ時のカバー画像。720p以上の16:9のpng画像であればいけます。
- /templates/img/flip_flame.png
  - 回答オープン時の背景画像。720p以上の16:9のpng画像であればいけます。

## Licence

MIT