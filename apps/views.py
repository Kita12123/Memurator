from pathlib import Path

from flask import Blueprint, render_template, send_from_directory, url_for

apps = Blueprint(
    "apps",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@apps.route("/")
def index():
    return render_template("index.html")


@apps.route('/favicon.ico')
def favicon():
    """アイコン指定"""
    return send_from_directory(
        Path(__file__).parent / "static" / "image",
        'favicon.ico'
    )