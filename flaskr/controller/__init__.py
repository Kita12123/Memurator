from datetime import datetime
from dateutil.relativedelta import relativedelta

from flaskr.controller import *
from flaskr import scheduler

@scheduler.task("interval", id="refresh_db", seconds=1*60*60)
def schedule_fuction():
    now_time = datetime.now()
    if now_time.strftime(r"%H") in ["08", "10", "12", "14", "16", "18"]:
        last_month = datetime.today() - relativedelta(months=1)
        sync.refresh_all(
            first_date=last_month.strftime(r"%Y%m00"),
            last_date=str(999999 + 19500000),
            contain_master=True
        )