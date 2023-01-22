"""empty message

Revision ID: 8e40a57e32c0
Revises: 9900b9d1c2f9
Create Date: 2023-01-22 13:58:12.536199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e40a57e32c0'
down_revision = '9900b9d1c2f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('仕入れデータ',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('purchase_date', sa.Integer(), nullable=False),
    sa.Column('purchase_category', sa.Integer(), nullable=True),
    sa.Column('purchase_slip_number', sa.Integer(), nullable=True),
    sa.Column('supplement_category', sa.String(), nullable=True),
    sa.Column('supplier_code', sa.Integer(), nullable=True),
    sa.Column('supplier_kana', sa.String(), nullable=True),
    sa.Column('goods_factory_code', sa.String(), nullable=True),
    sa.Column('goods_factory_kana', sa.String(), nullable=True),
    sa.Column('parent_goods_code', sa.Integer(), nullable=True),
    sa.Column('parent_goods_kana', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('unit_price', sa.Float(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('仕入データ')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('仕入データ',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('purchase_date', sa.INTEGER(), nullable=False),
    sa.Column('purchase_category', sa.INTEGER(), nullable=True),
    sa.Column('purchase_slip_number', sa.INTEGER(), nullable=True),
    sa.Column('supplement_category', sa.VARCHAR(), nullable=True),
    sa.Column('supplier_code', sa.INTEGER(), nullable=True),
    sa.Column('supplier_kana', sa.VARCHAR(), nullable=True),
    sa.Column('goods_factory_code', sa.VARCHAR(), nullable=True),
    sa.Column('goods_factory_kana', sa.VARCHAR(), nullable=True),
    sa.Column('parent_goods_code', sa.INTEGER(), nullable=True),
    sa.Column('parent_goods_kana', sa.VARCHAR(), nullable=True),
    sa.Column('quantity', sa.INTEGER(), nullable=True),
    sa.Column('unit_price', sa.FLOAT(), nullable=True),
    sa.Column('price', sa.INTEGER(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('仕入れデータ')
    # ### end Alembic commands ###
