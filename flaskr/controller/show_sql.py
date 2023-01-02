from flask import render_template

from flaskr import app

@app.route("/show_sql", methods=["GET"])
def show_sql():
    user = system.load(request.remote_addr)
    sql_display = user.form.to_sql(
        download=False
    ).replace(" ", "&emsp;").replace("\n", "<br>")
    sql_download = user.form.to_sql(
        download=True
    ).replace(" ", "&emsp;").replace("\n", "<br>")
    return render_template(
        "show_sql.html",
        MyColor=user.mycolor,
        sql_display=sql_display,
        sql_download=sql_download
    )