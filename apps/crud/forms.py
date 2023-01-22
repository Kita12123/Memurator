from datetime import datetime

from apps.app import db
from dateutil.relativedelta import relativedelta
from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

TABLES = sorted([table for table in db.metadata.tables])


class CreateForm(FlaskForm):

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
        choices=["すべて", *TABLES],
        validators=[DataRequired(message="データ名は必須です。")]
    )

    submit = SubmitField("データ同期")


class ReadForm(FlaskForm):

    tablename = SelectField(
        "データ名",
        choices=TABLES,
        validators=[DataRequired(message="データ名は必須です。")]
    )
    where = StringField(
        "WHERE句"
    )

    submit = SubmitField("データ同期")
