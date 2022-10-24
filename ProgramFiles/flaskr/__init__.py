"""
FLASK Initialize
"""
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from flask import Flask
import warnings
warnings.simplefilter("ignore")

from ProgramFiles import db
from ProgramFiles.flaskr.user_ins import USER
from ProgramFiles.log import dsp_except

def create_app() -> Flask:
    def schedule_func():
        now_hour = datetime.now().strftime(r"%H")
        USER.refresh()
        if now_hour in ["08", "10", "12", "14", "16"]:
            db.refresh_all()
    app = Flask(__name__)
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_func, trigger="interval", minutes=60)
    scheduler.start()
    try:
        return app
    except:
        dsp_except()
        scheduler.shutdown()
#refresh_all()
app = create_app()
#app = Flask(__name__)


from ProgramFiles.flaskr import main