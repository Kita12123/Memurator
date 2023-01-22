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
