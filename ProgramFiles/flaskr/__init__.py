"""
FLASK Initialize
"""
import warnings
from flask import Flask
from flask_apscheduler import APScheduler

from ProgramData import SYSTEMDIR
from ProgramFiles.flaskr import mod


class Config:
    SCHEDULER_API_ENABLED = True


# ログ管理インスタンス
log = mod.Log(
    folder=SYSTEMDIR,
    toaddrs=["h-kitaura@minoru-sangyo.co.jp"]
)

# sqlite3でpyodbcに接続するとき、警告が出るので無視する
warnings.simplefilter("ignore")

# Flask app作成
app = Flask(__name__)
app.config.from_object(Config())
app.logger.setLevel(mod.DEBUG)
app.logger.addHandler(log.handler_default)
app.logger.addHandler(log.handler_debug_file)
app.logger.addHandler(log.handler_info_file)
app.logger.addHandler(log.handler_error_file)

# 定期実行処理
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

app.logger.info("*************** M emurator Run ***************")

from ProgramFiles.flaskr import main  # noqa <- flake8で無視する
