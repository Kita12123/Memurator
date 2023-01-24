"""
FLASK Initialize
"""
import sys
import warnings

from flask import Flask, render_template
from flask_apscheduler import APScheduler
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from apps.config import config

sys.dont_write_bytecode = True

# sqlite3でpyodbcに接続するとき、警告が出るので無視する
warnings.simplefilter("ignore")

scheduler = APScheduler()
db = SQLAlchemy()


def page_not_found(e):
    """404 Not Found"""
    return render_template("404.html"), 404


def internal_server_error(e):
    """500 Internal Server Error"""
    return render_template("500.html"), 500


# コンフィグキーを渡す
def create_app(config_key):
    app = Flask(__name__)
    app.config.from_object(config[config_key])
    # デバッグツールバー設定
    DebugToolbarExtension(app)
    # データベース設定
    db.init_app(app)
    Migrate(app, db)
    # エラー
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    # 基盤アプリ登録
    from apps import views
    app.register_blueprint(views.apps)
    # データベース編集アプリ登録
    from apps.crud import views as crud_views
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    # データベース問い合わせアプリ登録
    from apps.search import views as search_views
    app.register_blueprint(search_views.search, url_prefix="/search")
    # 定期実行処理
    scheduler.init_app(app)
    scheduler.start()
    return app
