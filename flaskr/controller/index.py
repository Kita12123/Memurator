from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import redirect
from flask import render_template
from flask import request

from flaskr import app
from flaskr import cache
from flaskr.model import crud


@app.route("/", methods=["GET", "POST"])
@cache.cached(timeout=60*3)
def index():
    if request.method=="POST":
        # サーチ機能
        form_dic = request.form.to_dict()
        db_name = form_dic.pop("db_name", "")
        cache.delete(request.remote_addr)
        cache.set(request.remote_addr, form_dic)
        return redirect(f"master/{db_name}")
    # フォームパラメータ初期値設定
    today = datetime.today()
    first_date = (today - relativedelta(month=1)).strftime(r"%Y-%m-%d")
    last_date = today.strftime(r"%Y-%m-%d")
    form_dic = cache.get_dict()
    first_date = form_dic.pop("first_date", first_date)
    last_date = form_dic.pop("last_date", last_date)
    return render_template(
        "index.html",
        user_dic=crud.user_load(request.remote_addr),
        first_date=first_date,
        last_date=last_date,
        **form_dic
    )
