環境構築

1. Pythonインストール
    https://www.python.org/
    ※3.11推奨

2. 仮想環境(.win)作成
    python -m venv .win
    .win\Scripts\activate.bat
    pip install -r requirements.txt

    ※ライブラリ
    pip install <lib_name> --use-pep517
    pandas
    flask
    Flask-APScheduler
    flake8
    pyodbc

3. サーバー設定
    pip install wfastcgi
    https://medium.com/@dpralay07/deploy-a-python-flask-application-in-iis-server-and-run-on-machine-ip-address-ddb81df8edf3


プログラム説明

・ProgramData/
    HOST接続文字列
    SQLデータベース
・ProgramFiles/
    ・db/
        SQLデータを操作モジュール
    ・flaskr/
        webサーバー構築モジュール
    ・log/
        ログ管理モジュール
・craft_db.py
    HOSTとSQLを同期させる
・flask_run.py
    webサーバーを立てるエントリポイント

gitの運用
・commit時にすること
    192.168.0.244(運用サーバー)にアップグレードしたファイルを置き換える
    commitする


課題

・index.html
    select句のselected判定をどうにかしたい。ifで全て書いていくのは微妙な気がする。
    OK:ロード中の印をつけたい。


メモ書き


・git

ブランチ
    確認
    git branch
    作成
    git branch <ブランチ名>
    変更
    git checkout <ブランチ名>
    削除
    git branch -D <ブランチ名>

コミット
    追加済みのファイル
    git commit .
    新規ファイルすべて
    git add .
    git commit

リモート
    追加
    git remote add origin https://github.com/Kita12123/M_Emurator.git
    git push -u origin master


変更注意

・SQLを変更するとき
    SQLに対応したファイルも変更する
    ProgramFiles/flaskr/mymod/sql/__init__.py

フォルダ構造

flaskr
├ common
│ ├ libs
│ └ models  --- モデル
│ 　 ├ user.py
│ 　 └ ・・・
├ config　---　設定フォルダ
│ ├ base_setting.py　--- 各環境共通設定
│ ├ local_setting.py　--- ローカル開発環境用設定 
│ └ production_setting.py --- 本番環境用設定
├ controllers --- コントローラ
│ ├ index.py
│ └ ・・・
├ interceptors 
│ ├ auth.py --- 認証系処理
│ └ error_handler.py　--- エラー処理
├ static　--- 静的ファイル置き場所
├ templates　--- テンプレート
│ ├ common
│ │ └ layout.html
│ └ index.html
├ application.py　--- 複数のファイルが利用するものを定義（Flaskインスタンス、DB、環境変数など）
├ manager.py --- アプリ実行用スクリプト（アプリの入り口）
├ requirements.py --- ライブラリ一覧
└ www.py --- ルーティング