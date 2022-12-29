from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from flaskr.model import Base


# モデルクラスの定義にはdb.Modelクラスを継承する必要がある。
class Earning(Base):
    """売上データ"""

    # hostのsqlファイルと同名にする
    __tablename__ = "earnings"

    # 作成するテーブルのカラムを定義
    id = Column(Integer, primary_key=True)
    # ブロック番号
    block_number = Column(Integer)
    block_row = Column(Integer)
    # 出荷伝票番号
    shipping_slip_number = Column(String)
    shipping_date = Column(Integer)
    # 伝票区分
    shipping_category = Column(Integer)
    # 運送会社コード
    shipping_campany_code = Column(Integer)
    # 運賃扱い区分
    fare_category = Column(Integer)
    # 得意先コード
    customer_code = Column(Integer)
    customer_kana = Column(String)
    customer_manager_code = Column(Integer)
    # 雑コード
    buyer_code = Column(Integer)
    # 委託区分
    consign_category = Column(Integer)
    # 送荷先コード
    destination_code = Column(Integer)
    destination_kana = Column(String)
    # 製品部品（営業）コード
    goods_sales_code = Column(Integer)
    goods_sales_kana = Column(String)
    goods_sales_grade = Column(Integer)
    # 数量
    quantity = Column(Integer)
    # 単価
    unit_price = Column(Integer)
    # 金額
    price = Column(Integer)
    # 原価
    cost = Column(Float)
    # オーダー番号
    order_number = Column(String)
    # 備考
    note = Column(String)

    # 同期するときの比較する列名
    # ないときはすべてのデータを
    @property
    def sync_column(self):
        return self.shipping_date


class Shipping(Base):
    """出荷データ（本社）"""

    __tablename__ = "shippings"

    id = Column(Integer, primary_key=True)
    shipping_slip_number = Column(String)
    shipping_slip_row = Column(Integer)
    shipping_date = Column(Integer)
    shipping_category = Column(Integer)
    shipping_campany_code = Column(Integer)
    fare_category = Column(Integer)
    # 指示日
    instruction_date = Column(Integer)
    customer_code = Column(Integer)
    customer_kana = Column(String)
    customer_manager_code = Column(Integer)
    buyer_code = Column(Integer)
    consign_category = Column(Integer)
    destination_code = Column(Integer)
    destination_kana = Column(String)
    goods_sales_code = Column(Integer)
    goods_sales_kana = Column(String)
    goods_sales_grade = Column(Integer)
    # 部番
    parts_number = Column(String)
    order_number = Column(String)
    order_quantity = Column(Integer)
    back_order_category = Column(Integer)
    back_order_quantity = Column(Integer)
    shipping_quantity = Column(Integer)
    unit_price = Column(Integer)
    price = Column(Integer)
    note = Column(String)
    input_day = Column(Integer)
    input_hour = Column(Integer)
    input_minute = Column(Integer)

    @property
    def sync_column(self):
        return self.shipping_date


class ShippingKyusyu(Base):
    """出荷データ（九州）"""

    __tablename__ = "shippings_kyusyu"

    id = Column(Integer, primary_key=True)
    shipping_slip_number = Column(String)
    shipping_slip_row = Column(Integer)
    shipping_date = Column(Integer)
    shipping_category = Column(Integer)
    shipping_campany_code = Column(Integer)
    fare_category = Column(Integer)
    instruction_date = Column(Integer)
    customer_code = Column(Integer)
    customer_kana = Column(String)
    customer_manager_code = Column(Integer)
    buyer_code = Column(Integer)
    consign_category = Column(Integer)
    destination_code = Column(Integer)
    destination_kana = Column(String)
    goods_sales_code = Column(Integer)
    goods_sales_kana = Column(String)
    goods_sales_grade = Column(Integer)
    parts_number = Column(String)
    order_number = Column(String)
    order_quantity = Column(Integer)
    back_order_category = Column(Integer)
    back_order_quantity = Column(Integer)
    shipping_quantity = Column(Integer)
    unit_price = Column(Integer)
    price = Column(Integer)
    note = Column(String)
    input_day = Column(Integer)
    input_hour = Column(Integer)
    input_minute = Column(Integer)

    @property
    def sync_column(self):
        return self.shipping_date


class ShippingNagano(Base):
    """出荷データ（長野）"""

    __tablename__ = "shippings_nagano"


    id = Column(Integer, primary_key=True)
    shipping_slip_number = Column(String)
    shipping_slip_row = Column(Integer)
    shipping_date = Column(Integer)
    shipping_category = Column(Integer)
    shipping_campany_code = Column(Integer)
    fare_category = Column(Integer)
    instruction_date = Column(Integer)
    customer_code = Column(Integer)
    customer_kana = Column(String)
    customer_manager_code = Column(Integer)
    buyer_code = Column(Integer)
    consign_category = Column(Integer)
    destination_code = Column(Integer)
    destination_kana = Column(String)
    goods_sales_code = Column(Integer)
    goods_sales_kana = Column(String)
    goods_sales_grade = Column(Integer)
    parts_number = Column(String)
    order_number = Column(String)
    order_quantity = Column(Integer)
    back_order_category = Column(Integer)
    back_order_quantity = Column(Integer)
    shipping_quantity = Column(Integer)
    unit_price = Column(Integer)
    price = Column(Integer)
    note = Column(String)
    input_day = Column(Integer)
    input_hour = Column(Integer)
    input_minute = Column(Integer)

    @property
    def sync_column(self):
        return self.shipping_date


class Purchase(Base):
    """仕入データ"""

    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True)
    # 仕入日付
    purchase_date = Column(Integer, nullable=False)
    purchase_category = Column(Integer)
    supplement_category = Column(String)
    # 仕入先コード
    supplier_code = Column(Integer)
    supplier_kana = Column(String)
    # 品目（工場）コード
    goods_factory_code = Column(String)
    goods_factory_kana = Column(String)
    # 機種（工場）コード
    parent_goods_code = Column(Integer)
    parent_goods_kana = Column(String)
    quantity = Column(Integer)
    unit_price1 = Column(Float)
    unit_price2 = Column(Float)
    price1 = Column(Integer)
    price2 = Column(Integer)
    # 勘定科目コード
    payment_code1 = Column(Integer)
    payment_code2 = Column(Integer)

    @property
    def sync_column(self):
        return self.purchase_date


class ShippingCategoryMaster(Base):
    """"伝票区分マスター"""

    __tablename__ = "shipping_categories"

    id = Column(Integer, primary_key=True)
    category = Column(Integer, unique=True)
    name = Column(String)


class ConsignCategoryMaster(Base):
    """委託区分マスター"""

    __tablename__ = "consign_categories"

    id = Column(Integer, primary_key=True)
    category = Column(Integer, unique=True)
    name = Column(String)


class CustomerManagerCodeMaster(Base):
    """得意先担当者コードマスター"""

    __tablename__ = "customer_manager_codes"

    id = Column(Integer, primary_key=True)
    code = Column(Integer, unique=True)
    name = Column(String)


class ShippingCompanyCodeMaster(Base):
    """運送会社コードマスター"""

    __tablename__ = "shipping_campany_codes"

    id = Column(Integer, primary_key=True)
    code = Column(Integer, unique=True)
    name = Column(String)


class PrefectureCodeMaster(Base):
    """県コードマスター"""

    __tablename__ = "prefecture_codes"

    id = Column(Integer, primary_key=True)
    code = Column(Integer, unique=True)
    name = Column(String)


class CustomerCodeMaster(Base):
    """得意先コードマスター"""

    __tablename__ = "customer_codes"

    id = Column(Integer, primary_key=True)
    code = Column(Integer, unique=True)
    kana = Column(String)
    name = Column(String)
    less_rate = Column(Integer)
    closing_date = Column(Integer)
    manager_code = Column(Integer)
    prefecture_code = Column(Integer)
    post_code = Column(String)
    address = Column(String)
    phone_number = Column(String)
    create_date = Column(Integer)


class GoodsSalesCodeMaster(Base):
    """品目コードマスター（営業）"""

    __tablename__ = "goods_sales_codes"

    id = Column(Integer, primary_key=True)
    code = Column(Integer, unique=True)
    kana = Column(String)
    parts_number = Column(String)
    wight = Column(Float)
    unit_price = Column(Float)
    unit_price_grade2 = Column(Integer)
    unit_price_past = Column(Float)
    cost = Column(Float)
    cost_grade2 = Column(Integer)
    abolition_category = Column(String)
    alternative_code = Column(Integer)
    create_date = Column(Integer)


class SupplierCodeMaster(Base):
    """仕入先コードマスター"""

    __tablename__ = "supplier_codes"

    id = Column(Integer, primary_key=True)
    code = Column(Integer, unique=True)
    name = Column(String)


class GoodsFactoryCodeMaster(Base):
    """品目コードマスター（工場）"""

    __tablename__ = "goods_factory_codes"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    kana = Column(String)
    name = Column(String)
    category = Column(Integer)
    specification = Column(String)
    diagram = Column(String)
    parts_number = Column(String)
    supplier_code = Column(Integer)
    include_code = Column(Integer)
    material_unit_price = Column(Float)
    processing_unit_price = Column(Float)
    scan_category = Column(Integer)
    change_date = Column(Integer)
    create_date = Column(Integer)
