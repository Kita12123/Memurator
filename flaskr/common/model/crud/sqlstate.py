import sqlalchemy
from sqlalchemy.sql import (
    and_,
    case,
    or_,
    select
)

from flaskr.common.model import Base
from flaskr.common.model.database import (
    ConsignCategoryMaster,
    CustomerManagerCodeMaster,
    DestinationCodeMaster,
    Earning,
    FareCategoryMaster,
    ShippingCompanyCodeMaster,
    ShippingCategoryMaster
)


def to_sql_display_sales(tablename, /, *args):
    table:Earning = Base.metadata.tables.get(tablename)
    select([
        case(
            (table.shipping_date==0, 0),
            (table.shipping_date==9999999, 99999999),
            else_=table.shipping_date+19500000
        ).label("伝票日付"),
        ShippingCategoryMaster.name.label("伝票区分名＊"),
        ConsignCategoryMaster.name.label("委託区分名＊"),
        FareCategoryMaster.name.label("扱い区分"),
        ShippingCompanyCodeMaster.name.label("運送会社名＊"),
        CustomerManagerCodeMaster.name.label("担当者名＊"),
        table.customer_code.label("得意先コード"),
        table.customer_kana.label("得意先カナ"),
        case(
            (or_(
                (table.customer_code>=500000, table.customer_code< 600000),
                (table.customer_code>=333800, table.customer_code<=333899)
            ), table.buyer_code),
            else_=""
        ).label("雑コード"),
        case(
            (or_(
                (table.customer_code>=500000, table.customer_code< 600000),
                (table.customer_code>=333800, table.customer_code<=333899)
            ), DestinationCodeMaster.kana),
            else_=""
        ).label("雑カナ＊"),
        table.destination_code.label("送荷先コード"),
        table.destination_kana.label("送荷先カナ"),
        table.goods_sales_code.label("製品部品コード"),
        table.goods_sales_kana.label("製品部品カナ"),
        table.goods_sales_grade.label("級区分"),
        case(
            (table.shipping_category==30, table.quantity * -1),
            (table.shipping_category==90, table.quantity * -1),
            else_=table.quantity
        ).label("数量"),
        table.unit_price.label("単価"),
        case(
            (table.shipping_category==30, table.quantity * -1 * table.unit_price),
            (table.shipping_category==90, table.quantity * -1 * table.unit_price),
            else_=table.quantity * table.unit_price
        ).label("金額"),
        table.shipping_slip_number.label("出荷伝票番号"),
        table.note.label("備考")
    ]).select_from(
        table
    ).join(
        ConsignCategoryMaster, ConsignCategoryMaster.category==table.consign_category, isouter=True
    ).join(
        CustomerManagerCodeMaster, CustomerManagerCodeMaster.code==table.customer_manager_code, isouter=True
    ).join(
        DestinationCodeMaster, DestinationCodeMaster.code==table.destination_code, isouter=True
    ).join(
        FareCategoryMaster, FareCategoryMaster.category==table.fare_category, isouter=True
    ).join(
        ShippingCompanyCodeMaster, ShippingCompanyCodeMaster.code==table.shipping_campany_code, isouter=True
    ).join(
        ShippingCategoryMaster, ShippingCategoryMaster.category==table.shipping_category, isouter=True
    ).where(and_(*args))
