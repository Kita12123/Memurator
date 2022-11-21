"""
FLASK Initialize
"""
import warnings
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

from ProgramFiles.flaskr.mod import schedule_fuction

# sqlite3でpyodbcに接続するとき、警告が出るので無視する
warnings.simplefilter("ignore")

# Flask app作成
app = Flask(__name__)

# 定期実行処理
Scheduler = BackgroundScheduler()
Scheduler.add_job(schedule_fuction, trigger="interval", minutes=60)
Scheduler.start()


from ProgramFiles.flaskr import main