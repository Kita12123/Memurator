

環境構築
    git init --- Gitセットアップ
    git remote add origin eval https://github.com/Kita12123/Memurator.git --- GitHubと接続
    git pull origin master --- masterと
    (Mac)eval "$(pyenv init --path)"
    python -m venv .venv --- 仮想環境構築
    python -m pip install --upgrade pip --- 仮想環境pipアップグレード
    (Mac). .venv/bin/activate
    (Win).venv¥Scripts¥activate.bat
    pip install -r requirements.txt
    (Mac)pip uninstall pyodbc
    .venv/lib/...site-packagesにpyodbcフォルダを追加する --- pyodbcはMacで使えないため、存在するように認識させる必要がある