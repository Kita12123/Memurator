from flask import Blueprint, render_template

from apps import controller
from apps.crud.forms import ReadForm
from apps.search.forms import SalesForm

search = Blueprint(
    "search",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@search.route("/")
def index():
    return render_template(
        "search/index.html"
    )


@search.route("/sales", methods=["GET", "POST"])
def sales():
    form = SalesForm()
    df_lists = []
    if form.validate_on_submit():
        tablename = form.tablename.data
        where = form.create_where()
        df = controller.create_df(tablename, where)
        df_lists = df.values.tolist()
        return render_template(
            "search/sales.html",
            tablename=tablename,
            form=form,
            df_lists=df_lists
        )
    return render_template(
        "search/sales.html",
        tablename="フォーム",
        form=form,
        df_lists=df_lists
    )


@search.route("/factory", methods=["GET", "POST"])
def factory():
    form = SalesForm()
    df = ""
    if form.validate_on_submit():
        tablename = form.tablename.data
        where = form.create_where()
        df = controller.create_df(tablename, where).to_html()
        read_form = ReadForm(
            tablename=tablename,
            where=where
        )
        return render_template("crud/read.html", form=read_form, df=df)
    return render_template("search/sales.html", form=form, df=df)


@search.route("/master/<tablename>")
def master(tablename):
    df = controller.create_df(tablename).to_html()
    return render_template("search/master.html", df=df)
