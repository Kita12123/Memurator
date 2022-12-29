from flask import render_template
from flask import request

from flaskr import app
from flaskr.controller.common.user import load_user


def adjust_request():
    req = request.form.to_dict()


@app.route("/", methods=["GET", "POST"])
def index():
    user = load_user(id=request.remote_addr)
    if request.method == "POST":
        title = request.form["db_name"]
        form_dic = {}
    else:
        title =  user.department
        form_dic = {}
    return render_template(
        "index.html",
        mycolor=user.mycolor,
        department=user.department,
        title=title,
        form_dic=form_dic,
    )
