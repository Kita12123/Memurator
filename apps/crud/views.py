import pandas as pd
from apps.crud import controller
from apps.crud.forms import CreateForm, ReadForm
from flask import Blueprint, render_template

# Blueprintでアプリを作成する
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@crud.route("/")
def index():
    return render_template(
        "crud/index.html"
    )


@crud.route("/create", methods=["GET", "POST"])
def create():
    form = CreateForm()
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
    return render_template("crud/create.html", form=form)


@crud.route("/read", methods=["GET", "POST"])
def read():
    form = ReadForm()
    df = pd.DataFrame()
    if form.validate_on_submit():
        tablename = form.tablename.data
        where = form.where.data
        form.tablename.default = tablename
        form.where.default = where
        if where:
            df = controller.create_df(tablename, where)
        else:
            df = controller.create_df(tablename)
    return render_template(
        "crud/read.html",
        form=form,
        df=df
    )
