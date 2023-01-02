from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import render_template
from flask import request

from flaskr import app
from flaskr.common import log

@app.route("/setting", methods=["GET", "POST"])
def setting():
    user = system.load(request.remote_addr)
    if request.method == "POST":
        click = request.form.get("ok")
        if click == "設定変更":
            user.update(
                MaxRows=int(request.form["MaxRows"]),
                Department=request.form["Department"],
                MyColor=request.form["MyColor"]
            )
            system.save_file()
        elif (
            click == "最新データ取得"
            and system.last_refresh_date != "更新中"
        ):
            sync.refresh_all(
                first_date=request.form["first_date"].replace("-", ""),
                last_date=request.form["last_date"].replace("-", ""),
                contain_master=request.form.get("contain_master")
            )
            system.save_file()
    last_month = datetime.today() - relativedelta(months=1)
    return render_template(
        "setting.html",
        MaxRows=user.max_rows,
        MyColor=user.mycolor,
        Department=user.department,
        LastRefreshDate=system.last_refresh_date,
        first_date=last_month.strftime(r"%Y-%m-01"),
        last_date=datetime.now().strftime((r"%Y-%m-%d")),
        log_texts=log.get_info()[-8:]
    )
