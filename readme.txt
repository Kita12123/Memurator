環境構築

1. Pythonインストール
    https://www.python.org/
    ※3.10推奨

2. 仮想環境(.win)作成
    python -m venv .win
    .win\Scripts\activate.bat
    pip install -r requirements.txt


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


課題

・index.html
    select句のselected判定をどうにかしたい。ifで全て書いていくのは微妙な気がする。
    ロード中の印をつけたい。


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