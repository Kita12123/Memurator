"""
FLASK Initialize
"""
import warnings
from flask import Flask
from flask_apscheduler import APScheduler

# sqlite3でpyodbcに接続するとき、警告が出るので無視する
warnings.simplefilter("ignore")

# Flask app作成
app = Flask(__name__)

# 定期実行処理
class Config:
    SCHEDULER_API_ENABLED = True
app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


from ProgramFiles.flaskr import main