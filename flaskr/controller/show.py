from flask import render_template
from flask import request

from flaskr import app
from flaskr.controller.common.user import load_user


@app.route("/", methods=["POST"])
def show():
    user = load_user(id=request.remote_addr)
    return render_template(
        "show.html",
        MyColor=user.mycolor,
        Department=user.department,
        LastRefreshDate=user.last_refresh_date
    )
