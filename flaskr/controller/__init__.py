from datetime import datetime
from flask import send_from_directory
import os

from flaskr import app
from flaskr import scheduler
from flaskr.model.crud.sync_host import sync_host_all


@scheduler.task("interval", id="refresh_db", seconds=1*60*60)
def schedule_fuction():
    now_time = datetime.now()
    if now_time.strftime(r"%H") in ["08", "10", "12", "14", "16", "18"]:
        sync_host_all()


@app.route('/favicon.ico')
def favicon():
    """Select ico"""
    return send_from_directory(
        os.path.join(app.root_path, 'static/image/ico'),
        'favicon.ico'
    )
