from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField
from wtforms.validators import DataRequired

from apps.app import db


# ユーザー新規作成とユーザー編集フォームクラス
class SyncingForm(FlaskForm):

    db_tables = [
        table for table in db.metadata.tables
        if table not in ("ユーザー")
    ]
    db_tables.sort()

    first_date = DateField(
        "開始日付",
        validators=[
            DataRequired(message="開始日付は必須です。")
        ],
        default=datetime.now() - relativedelta(months=1, day=1)
    )
    last_date = DateField(
        "終了日付",
        default=datetime.now()
    )
    db_name = SelectField(
        "データ名",
        choices=["すべて", *db_tables],
        validators=[DataRequired(message="データ名は必須です。")]
    )

    submit = SubmitField("データ同期")
