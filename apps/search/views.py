from apps import controller
from apps.search.forms import SalesForm
from flask import Blueprint, render_template

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
    df = ""
    if form.validate_on_submit():
        tablename = form.tablename.data
        where = form.create_where()
        df = controller.create_df(tablename, where).to_html()
    return render_template("search/sales.html", form=form, df=df)


@search.route("/master/<tablename>")
def master(tablename):
    df = controller.create_df(tablename).to_html()
    return render_template("search/master.html", df=df)
