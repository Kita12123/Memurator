from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class SalesForm(FlaskForm):

    tablename = SelectField(
        "データ名",
        choices=[
            "売上データ",
            "出荷データ（本社）",
            "出荷データ（九州）",
            "出荷データ（長野）"
        ]
    )
    first_date = DateField(
        "開始日付",
        validators=[DataRequired(message="日付は必須です。")],
        default=datetime.now()
    )
    last_date = DateField(
        "終了日付",
        validators=[DataRequired(message="日付は必須です。")],
        default=datetime.now()
    )
    customer_code = StringField(
        "得意先コード"
    )
    buyer_code = StringField(
        "雑コード"
    )
    destination_code = StringField(
        "送荷先コード"
    )
    goods_sales_code = StringField(
        "製品部品コード"
    )
    goods_sales_flg = SelectField(
        "製品部品フィルター",
        choices=["", "製品のみ", "部品のみ"]
    )
    shipping_category = StringField(
        "伝票区分"
    )
    shipping_slip_number = StringField(
        "出荷伝票番号"
    )

    submit_ok = SubmitField(
        "決定",
        name="ok"
    )

    submit_download = SubmitField(
        "ダウンロード",
        name="download"
    )

    def create_where(self) -> str:
        wheres = []

        first_date = int(self.first_date.data.strftime(r"%Y%m%d"))
        last_date = int(self.last_date.data.strftime(r"%Y%m%d"))
        wheres.append(f"{first_date}<=伝票日付 AND 伝票日付<={last_date}")

        if not self.customer_code:
            pass
        elif len(self.customer_code.data) < 6:
            i = 6 - len(self.customer_code.data)
            first_customer_code = self.customer_code.data + ("0"*i)
            last_customer_code = self.customer_code.data + ("9"*i)
            wheres.append(
                f"""{first_customer_code}<=得意先コード
                    AND 得意先コード<={last_customer_code}"""
            )
        else:
            wheres.append(f"得意先コード={self.customer_code.data}")

        if self.buyer_code.data:
            wheres.append(f"雑コード={self.buyer_code.data}")

        if self.destination_code.data:
            wheres.append(f"送荷先コード={self.destination_code.data}")

        if not self.goods_sales_code.data:
            pass
        elif len(self.goods_sales_code.data) < 7:
            i = 7 - len(self.goods_sales_code.data)
            first_goods_code = self.goods_sales_code.data + ("0"*i)
            last_goods_code = self.goods_sales_code.data + ("9"*i)
            wheres.append(
                f"{first_goods_code}<=製品部品コード<={last_goods_code}"
            )
        else:
            wheres.append(f"製品部品コード={self.goods_sales_code.data}")

        if self.goods_sales_flg.data == "製品のみ":
            wheres.append(f"製品部品コード<{10*8}")
        elif self.goods_sales_flg.data == "部品のみ":
            wheres.append(f"製品部品コード>={10*8}")

        if self.shipping_category.data:
            wheres.append(f"伝票区分={self.shipping_category.data}")

        if self.shipping_slip_number.data:
            wheres.append(f"出荷伝票番号={self.shipping_category.data}")

        return " AND ".join(wheres)
