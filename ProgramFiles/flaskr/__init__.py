"""
FLASK Initialize
"""
#from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
#from ProgramFiles.db import refresh_schedule
#from ProgramFiles.log import dsp_except

#def create_app() -> Flask:
#    app = Flask(__name__)
#    scheduler = BackgroundScheduler()
#    scheduler.add_job(refresh_schedule, trigger="interval", minutes=30)
#    scheduler.start()
#    try:
#        return app
#    except:
#        dsp_except()
#        scheduler.shutdown()
#app = create_app()
app = Flask(__name__)


from ProgramFiles.flaskr import main