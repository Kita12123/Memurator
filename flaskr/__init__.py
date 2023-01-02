"""
FLASK Initialize
"""
import warnings
from flask import Flask
from flask_caching import Cache
from flask_apscheduler import APScheduler

from flaskr.common.log import LOGGER

LOGGER.info("M emurator START")


class Config:
    SCHEDULER_API_ENABLED = True

# sqlite3でpyodbcに接続するとき、警告が出るので無視する
warnings.simplefilter("ignore")

# キャッシュ設定
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

# Flask app作成
app = Flask(__name__)
app.config.from_object(Config())
cache.init_app(app)

# 定期実行処理
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
