from flask import request
from flask import send_file

from flaskr import app
from ProgramData import PROGRAM_DIR

TEMP_CSV = PROGRAM_DIR / "download.csv"

@app.route("/download/<flg>", methods=["GET"])
def download(flg):
    user = system.load(request.remote_addr)
    df = db.sql.create_df(sql=user.form.to_sql(download=True))
    if flg != "master":
        df1, df2, df3 = arrage_df(df=df)
        # To File .csv
        if flg == "totall1":
            df = df1
        elif flg == "totall2":
            df = df2
        elif flg == "totall3":
            df = df3
    df.to_csv(TEMP_CSV, index=False, encoding="cp932", escapechar="|")
    return send_file(
        TEMP_CSV,
        download_name="download.csv"
    )
