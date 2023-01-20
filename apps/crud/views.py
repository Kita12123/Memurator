from flask import Blueprint, render_template

from apps.crud import controller
from apps.crud.forms import SyncingForm

# Blueprintでアプリを作成する
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@crud.route("/")
def index():
    """ユーザーの一覧を取得"""
    return render_template(
        "crud/index.html"
    )


@crud.route("/syncing", methods=["GET", "POST"])
def syncing():
    form = SyncingForm()
    if form.validate_on_submit():
        first_date_ = form.first_date.data.strftime(r"%Y%m%d")
        last_date_ = form.last_date.data.strftime(r"%Y%m%d")
        db_name = form.db_name.data
        first_date = int(first_date_) - 19500000
        last_date = int(last_date_) - 19500000
        if db_name == "すべて":
            controller.sync_host_all(
                first_date=first_date,
                last_date=last_date
            )
        else:
            controller.sync_host(
                db_name,
                first_date=first_date,
                last_date=last_date
            )
    return render_template("table/syncing.html", form=form)