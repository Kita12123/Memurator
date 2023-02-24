import pandas as pd
from flask import Blueprint, render_template

from apps import controller
from apps.crud.forms import CreateForm, ReadForm

# Blueprintでアプリを作成する
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@crud.route("/")
def index():
    read_form = ReadForm()
    create_form = CreateForm()
    if create_form.validate_on_submit():
        first_date_ = create_form.first_date.data.strftime(r"%Y%m%d")
        last_date_ = create_form.last_date.data.strftime(r"%Y%m%d")
        db_name = create_form.db_name.data
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
    return render_template(
        "crud/index.html",
        read_form=read_form,
        create_form=create_form
    )


@crud.route("/read", methods=["GET", "POST"])
def read():
    form = ReadForm()
    df = pd.DataFrame()
    if form.validate_on_submit():
        tablename = form.tablename.data
        where = form.where.data
        if where:
            df = controller.create_df(tablename, where)
        else:
            df = controller.create_df(tablename)
    return render_template(
        "crud/read.html",
        form=form,
        df=df.to_html(index=False)
    )
