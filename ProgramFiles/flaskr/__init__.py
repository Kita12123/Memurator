"""
FLASK Initialize
"""
import warnings
from flask import Flask
from flask_apscheduler import APScheduler


class Config:
    SCHEDULER_API_ENABLED = True


# sqlite3でpyodbcに接続するとき、警告が出るので無視する
warnings.simplefilter("ignore")

# Flask app作成
app = Flask(__name__)
app.config.from_object(Config())

# 定期実行処理
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

app.logger.info("*************** M emurator Run ***************")

from ProgramFiles.flaskr import main  # noqa <- flake8で無視する
