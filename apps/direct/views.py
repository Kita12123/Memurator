from flask import Blueprint, render_template

direct = Blueprint(
    "direct",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@direct.route("/")
def index():
    return render_template(
        "direct/index.html"
    )
