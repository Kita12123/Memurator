from flask import redirect
from flask import render_template
import traceback

from flaskr import app
from flaskr.common import log

def e_to_html(e) -> str:
    """HTML側で{% autoescape false %}にする"""
    return traceback.format_exception_only(e)[-1].replace(
        "¥n", "<br>").replace(
            "\n", "<br>").replace(
                " ", "&nbsp;")


@app.errorhandler(400)
def bad_request(e):
    log.LOGGER.debug(f"{e}")
    return render_template(
        "errors/400.html",
        MyColor="default",
        e=e_to_html(e)
    ), 400


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/"), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return redirect("/"), 405


@app.errorhandler(500)
def internal_server_error(e):
    log.LOGGER.debug(f"{e}")
    return render_template(
        "errors/500.html",
        MyColor="default",
        e=e_to_html(e)
    ), 500
