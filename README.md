Trelloをコマンドライン上から事項するためのpythonプログラムです。今のところ
- ボード一覧
- リスト一覧
- カード一覧
- カード作成、別リストへ移動、削除

のみが利用可能です。

# 実行環境
```
Pytho 3.8
pip 20.2.4
```


# Require
``` requirements.txt
python-dateutil==2.8.1
python-dotenv==0.15.0
```

# Install
## 必要ライブラリのインストール
```
pip install -r requirements.txt
```

## Trello-CLIのインストール
```
git clone https://github.com/yokohama/trello_cli.git
cd trello_cli
pip install dist/Trello_CLI-0.0.1-py3-none-any.whl
```

## 環境変数のファイルを作成

```
# trello_cliがインストールされたフォルダを検索
$ find ~/ -name trello_cli -print
/home/username/anaconda3/lib/python3.8/site-packages/trello_cli #環境による

$ touch /home/username/anaconda3/lib/python3.8/site-packages/trello_cli/.env
```

## 環境変数ファイルに内容を記述する
``` .env
TRELLO_API_KEY=xxxxxxxxxxxxxx
TRELLO_API_SECRET=xxxxxxxxxxxxxxxx
TRELLO_TOKEN=xxxxxxxxxxxxxxxxxxxxx
```

# Usage
```
$trello
```
