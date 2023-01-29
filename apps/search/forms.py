
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField
from wtforms.validators import ValidationError

kana = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾜｦﾝｧｨｩｪｫｯｬｭｮ"
abc = "ABCDEFGHIJELMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
num = "0123456789"
flg = ", "


def init_value(value: str, /) -> list[str]:
    """値の整形 and カンマで分ける"""
    values = value.replace(" ", "").replace("　", "").split(",")
    return [v for v in values if v]


def is_halfsize(value: str, /) -> bool:
    for v in value:
        if (v in kana or v in abc or v in num or v in flg):
            continue
        else:
            return False
    return True


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
        default=datetime.now(),
        validators=[]
    )
    last_date = DateField(
        "終了日付",
        default=datetime.now()
    )
    shipping_category = StringField(
        "伝票ｸﾌﾞﾝ,名"
    )
    shipping_category_filter = SelectField(
        "伝票区分フィルター",
        choices=["", "売上関係", "在庫関係"]
    )
    customer = StringField(
        "得意先ｺｰﾄﾞ,ｶﾅ,名"
    )
    buyer = StringField(
        "雑ｺｰﾄﾞ,ｶﾅ,名"
    )
    destination = StringField(
        "送荷先ｺｰﾄﾞ,ｶﾅ,名"
    )
    goods_sales = StringField(
        "製品部品ｺｰﾄﾞ,ｶﾅ"
    )

    def validate_goods_sales(self, goods_sales: StringField):
        goods_sales = goods_sales.data
        if not is_halfsize(goods_sales):
            raise ValidationError("全角が指定されています。")

    goods_sales_filter = SelectField(
        "製品部品フィルター",
        choices=["", "製品のみ", "部品のみ"]
    )
    shipping_slip_number = StringField(
        "出荷伝票NO"
    )

    def validate_shipping_slip_number(
        self, shipping_slip_number: StringField
    ):
        shipping_slip_number = shipping_slip_number.data
        if not is_halfsize(shipping_slip_number):
            raise ValidationError("全角が指定されています。")

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

        # 日付
        first_date = int(self.first_date.data.strftime(r"%Y%m%d"))
        last_date = int(self.last_date.data.strftime(r"%Y%m%d"))
        wheres.append(f"{first_date}<=伝票日付 AND 伝票日付<={last_date}")

        # 伝票区分
        w = []
        for v in init_value(self.shipping_category.data):
            if not v:
                continue
            elif v.isdigit():
                w.append(f"伝票区分={v}")
            elif is_halfsize(v):
                w.append(f"伝票区分名 LIKE'%{v}%'")
        if w:
            wheres.append(f"( {' OR '.join(w)} )")
        # 伝票区分フィルター
        if self.shipping_category_filter.data == "売上関係":
            wheres.append("伝票区分 in (10, 21, 30, 90)")
        elif self.shipping_category_filter.data == "在庫関係":
            wheres.append("伝票区分 in (10, 20, 21, 30, 90)")

        # 得意先
        w = []
        for v in init_value(self.customer.data):
            if not v:
                continue
            elif v.isdigit():
                if len(v) < 6:
                    i = 6 - len(v)
                    w.append(
                        f"""{v+("0"*i)}<=得意先コード
                            AND 得意先コード<={v+("9"*i)}"""
                    )
                else:
                    w.append(f"得意先コード={v}")
            elif is_halfsize(v):
                w.append(f"得意先カナ LIKE'%{v}%'")
            else:
                w.append(f"得意先名 LIKE'%{v}%'")
        if w:
            wheres.append(f"( {' OR '.join(w)} )")

        # 雑
        w = []
        for v in init_value(self.buyer.data):
            if not v:
                continue
            elif v.isdigit():
                w.append(f"雑コード={v}")
            elif is_halfsize(v):
                w.append(f"雑カナ LIKE'%{v}%'")
            else:
                w.append(f"雑名 LIKE'%{v}%'")
        if w:
            wheres.append(f"( {' OR '.join(w)} )")

        # 送荷先
        w = []
        for v in init_value(self.destination.data):
            if not v:
                continue
            elif v.isdigit():
                w.append(f"送荷先コード={v}")
            elif is_halfsize(v):
                w.append(f"送荷先カナ LIKE'%{v}%'")
            else:
                w.append(f"送荷先名 LIKE'%{v}%'")
        if w:
            wheres.append(f"( {' OR '.join(w)} )")

        # 品目（営業）
        w = []
        for v in init_value(self.goods_sales.data):
            if not v:
                continue
            elif v.isdigit():
                if len(v) < 7:
                    i = 7 - len(v)
                    w.append(
                        f"""{v+("0"*i)}<=製品部品コード
                            AND 製品部品コード<={v+("9"*i)}"""
                    )
                else:
                    w.append(f"製品部品コード={v}")
            elif is_halfsize(v):
                w.append(f"製品部品カナ LIKE'%{v}%'")
        if w:
            wheres.append(f"( {' OR '.join(w)} )")

        # 品目（営業）フィルター
        if self.goods_sales_filter.data == "製品のみ":
            wheres.append(f"製品部品コード<{10**8}")
        elif self.goods_sales_filter.data == "部品のみ":
            wheres.append(f"製品部品コード>={10**8}")

        # 出荷伝票NO
        if self.shipping_slip_number.data:
            wheres.append(f"出荷伝票番号={self.shipping_category.data}")

        return " AND ".join(wheres)
