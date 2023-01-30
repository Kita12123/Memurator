from flask import Blueprint, render_template

from apps import controller
from apps.search import controller as search_controller
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
    if form.validate_on_submit():
        tablename = form.tablename.data
        where = form.create_where()
        df, messages = search_controller.create_df_sales(tablename, where)
        df_dsp = df[
            list(search_controller.SALES_COLUMNS_DIC.keys())
        ].rename(columns=search_controller.SALES_COLUMNS_DIC)
        return render_template(
            "search/sales.html",
            tablename=tablename,
            form=form,
            messages=messages,
            table_columns=df_dsp.columns,
            table_data=df_dsp.values.tolist(),
        )
    return render_template(
        "search/sales.html",
        form=form
    )


@search.route("/factory", methods=["GET", "POST"])
def factory():
    pass


@search.route("/master/<tablename>")
def master(tablename):
    df = controller.create_df(tablename)
    return render_template(
        "search/master.html",
        table_columns=df.columns,
        table_values=df.values.tolist()
    )
