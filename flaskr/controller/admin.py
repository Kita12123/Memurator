from flask import render_template
from flask import request

from flaskr import app
from flaskr.common import log

@app.route("/admin", methods=["GET", "POST"])
def admin():
    log_texts = []
    sql_code = ""
    values = []
    if request.method == "POST":
        ok = request.form.get("ok", "")
        if ok == "設定変更":
            system.last_refresh_date = request.form["LastRefreshDate"]
        elif ok == "SQL送信":
            sql_code = request.form.get("sql_code")
            values = db.sql.create_list(sql=sql_code)
        elif ok == "info":
            log_texts = log.get_info()
        elif ok == "error":
            log_texts = log.get_error()
    return render_template(
        "admin.html",
        MyColor="default",
        log_texts=log_texts,
        sql_code=sql_code,
        LastRefreshDate=system.last_refresh_date,
        values=values
    )