from datetime import datetime

from apps.app import db


class Earning(db.Model):

    # hostのsqlファイルと同名にする
    __tablename__ = "売上データ"

    # 作成するテーブルのカラムを定義
    id = db.Column(db.Integer, primary_key=True)
    # ブロック番号
    block_number = db.Column(db.Integer)
    block_row = db.Column(db.Integer)
    # 出荷伝票番号
    shipping_slip_number = db.Column(db.String)
    shipping_date = db.Column(db.Integer)
    # 伝票区分
    shipping_category = db.Column(db.Integer)
    # 運送会社コード
    shipping_campany_code = db.Column(db.Integer)
    # 運賃扱い区分
    fare_category = db.Column(db.Integer)
    # 委託区分
    consign_category = db.Column(db.Integer)
    # 得意先コード
    customer_code = db.Column(db.Integer)
    customer_kana = db.Column(db.String)
    customer_manager_code = db.Column(db.Integer)
    # 雑コード
    buyer_code = db.Column(db.Integer)
    # 送荷先コード
    destination_code = db.Column(db.Integer)
    destination_kana = db.Column(db.String)
    # 製品部品（営業）コード
    goods_sales_code = db.Column(db.Integer)
    goods_sales_kana = db.Column(db.String)
    goods_sales_grade = db.Column(db.Integer)
    # 数量
    quantity = db.Column(db.Integer)
    # 単価
    unit_price = db.Column(db.Integer)
    # 金額
    price = db.Column(db.Integer)
    # 原価
    cost = db.Column(db.Float)
    # オーダー番号
    order_number = db.Column(db.String)
    # 備考
    note = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 同期するときの比較する列名
    # ないときはすべてのデータを
    @property
    def sync_column(self):
        return self.shipping_date


class Shipping(db.Model):

    __tablename__ = "出荷データ（本社）"

    id = db.Column(db.Integer, primary_key=True)
    shipping_slip_number = db.Column(db.String)
    shipping_slip_row = db.Column(db.Integer)
    shipping_date = db.Column(db.Integer)
    shipping_category = db.Column(db.Integer)
    shipping_campany_code = db.Column(db.Integer)
    fare_category = db.Column(db.Integer)
    consign_category = db.Column(db.Integer)
    # 指示日
    instruction_date = db.Column(db.Integer)
    customer_code = db.Column(db.Integer)
    customer_kana = db.Column(db.String)
    customer_manager_code = db.Column(db.Integer)
    buyer_code = db.Column(db.Integer)
    destination_code = db.Column(db.Integer)
    destination_kana = db.Column(db.String)
    goods_sales_code = db.Column(db.Integer)
    goods_sales_kana = db.Column(db.String)
    goods_sales_grade = db.Column(db.Integer)
    # 部番
    parts_number = db.Column(db.String)
    order_number = db.Column(db.String)
    order_quantity = db.Column(db.Integer)
    back_order_category = db.Column(db.Integer)
    back_order_quantity = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Integer)
    price = db.Column(db.Integer)
    note = db.Column(db.String)
    input_day = db.Column(db.Integer)
    input_hour = db.Column(db.Integer)
    input_minute = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)

    @property
    def sync_column(self):
        return self.shipping_date


class ShippingKyusyu(db.Model):

    __tablename__ = "出荷データ（九州）"

    id = db.Column(db.Integer, primary_key=True)
    shipping_slip_number = db.Column(db.String)
    shipping_slip_row = db.Column(db.Integer)
    shipping_date = db.Column(db.Integer)
    shipping_category = db.Column(db.Integer)
    shipping_campany_code = db.Column(db.Integer)
    fare_category = db.Column(db.Integer)
    consign_category = db.Column(db.Integer)
    instruction_date = db.Column(db.Integer)
    customer_code = db.Column(db.Integer)
    customer_kana = db.Column(db.String)
    customer_manager_code = db.Column(db.Integer)
    buyer_code = db.Column(db.Integer)
    destination_code = db.Column(db.Integer)
    destination_kana = db.Column(db.String)
    goods_sales_code = db.Column(db.Integer)
    goods_sales_kana = db.Column(db.String)
    goods_sales_grade = db.Column(db.Integer)
    parts_number = db.Column(db.String)
    order_number = db.Column(db.String)
    order_quantity = db.Column(db.Integer)
    back_order_category = db.Column(db.Integer)
    back_order_quantity = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Integer)
    price = db.Column(db.Integer)
    note = db.Column(db.String)
    input_day = db.Column(db.Integer)
    input_hour = db.Column(db.Integer)
    input_minute = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)

    @property
    def sync_column(self):
        return self.shipping_date


class ShippingNagano(db.Model):

    __tablename__ = "出荷データ（長野）"

    id = db.Column(db.Integer, primary_key=True)
    shipping_slip_number = db.Column(db.String)
    shipping_slip_row = db.Column(db.Integer)
    shipping_date = db.Column(db.Integer)
    shipping_category = db.Column(db.Integer)
    shipping_campany_code = db.Column(db.Integer)
    fare_category = db.Column(db.Integer)
    consign_category = db.Column(db.Integer)
    instruction_date = db.Column(db.Integer)
    customer_code = db.Column(db.Integer)
    customer_kana = db.Column(db.String)
    customer_manager_code = db.Column(db.Integer)
    buyer_code = db.Column(db.Integer)
    destination_code = db.Column(db.Integer)
    destination_kana = db.Column(db.String)
    goods_sales_code = db.Column(db.Integer)
    goods_sales_kana = db.Column(db.String)
    goods_sales_grade = db.Column(db.Integer)
    parts_number = db.Column(db.String)
    order_number = db.Column(db.String)
    order_quantity = db.Column(db.Integer)
    back_order_category = db.Column(db.Integer)
    back_order_quantity = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Integer)
    price = db.Column(db.Integer)
    note = db.Column(db.String)
    input_day = db.Column(db.Integer)
    input_hour = db.Column(db.Integer)
    input_minute = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)

    @property
    def sync_column(self):
        return self.shipping_date


class Purchase(db.Model):

    __tablename__ = "仕入れデータ"

    id = db.Column(db.Integer, primary_key=True)
    # 仕入日付
    purchase_date = db.Column(db.Integer, nullable=False)
    purchase_category = db.Column(db.Integer)
    purchase_slip_number = db.Column(db.Integer)
    supplement_category = db.Column(db.String)
    # 仕入先コード
    supplier_code = db.Column(db.Integer)
    supplier_kana = db.Column(db.String)
    # 品目（工場）コード
    goods_factory_code = db.Column(db.String)
    goods_factory_kana = db.Column(db.String)
    # 機種（工場）コード
    parent_goods_code = db.Column(db.Integer)
    parent_goods_kana = db.Column(db.String)
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Float)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)

    @property
    def sync_column(self):
        return self.purchase_date


class ShippingCategoryMaster(db.Model):

    __tablename__ = "伝票区分マスタ"

    category = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)


class ConsignCategoryMaster(db.Model):

    __tablename__ = "委託区分マスタ"

    category = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)


class CustomerManagerCodeMaster(db.Model):

    __tablename__ = "得意先担当者コードマスタ"

    code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)


class ShippingCompanyCodeMaster(db.Model):

    __tablename__ = "運送会社コードマスタ"

    code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)


class FareCategoryMaster(db.Model):

    __tablename__ = "運賃扱い区分マスタ"

    category = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)


class PrefectureCodeMaster(db.Model):

    __tablename__ = "県コードマスタ"

    code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)


class CustomerCodeMaster(db.Model):

    __tablename__ = "得意先コードマスタ"

    code = db.Column(db.Integer, primary_key=True)
    kana = db.Column(db.String)
    name = db.Column(db.String)
    less_rate = db.Column(db.Integer)
    closing_date = db.Column(db.Integer)
    manager_code = db.Column(db.Integer)
    prefecture_code = db.Column(db.Integer)
    post_code = db.Column(db.Integer)
    address = db.Column(db.String)
    phone_number = db.Column(db.String)
    create_date = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)


class DestinationCodeMaster(db.Model):

    __tablename__ = "送荷先コードマスタ"

    code = db.Column(db.Integer, primary_key=True)
    kana = db.Column(db.String)
    name = db.Column(db.String)
    prefecture_code = db.Column(db.Integer)
    post_code = db.Column(db.String)
    address = db.Column(db.String)
    phone_number = db.Column(db.String)
    flg = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)


class GoodsSalesCodeMaster(db.Model):

    __tablename__ = "品目コードマスタ（営業）"

    code = db.Column(db.Integer, primary_key=True)
    kana = db.Column(db.String)
    parts_number = db.Column(db.String)
    wight = db.Column(db.Float)
    unit_price = db.Column(db.Float)
    unit_price_grade2 = db.Column(db.Integer)
    unit_price_past = db.Column(db.Float)
    cost = db.Column(db.Float)
    cost_grade2 = db.Column(db.Integer)
    abolition_category = db.Column(db.String)
    alternative_code = db.Column(db.Integer)
    create_date = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)


class SupplierCodeMaster(db.Model):

    __tablename__ = "仕入先コードマスタ"

    code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)


class GoodsFactoryCodeMaster(db.Model):

    __tablename__ = "品目コードマスタ（工場）"

    code = db.Column(db.String, primary_key=True)
    kana = db.Column(db.String)
    name = db.Column(db.String)
    category = db.Column(db.Integer)
    specification = db.Column(db.String)
    diagram = db.Column(db.String)
    parts_number = db.Column(db.String)
    supplier_code = db.Column(db.Integer)
    include_code = db.Column(db.Integer)
    material_unit_price = db.Column(db.Float)
    processing_unit_price = db.Column(db.Float)
    scan_category = db.Column(db.Integer)
    change_date = db.Column(db.Integer)
    create_date = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)
