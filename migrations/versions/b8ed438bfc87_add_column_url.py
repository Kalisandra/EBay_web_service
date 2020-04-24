"""add column url

Revision ID: b8ed438bfc87
Revises: 4fac6816ccd9
Create Date: 2020-04-23 11:27:32.668648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8ed438bfc87'
down_revision = '4fac6816ccd9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('statistic_items', 'item_id',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('statistic_items', 'query_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('statistic_items', 'query_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('statistic_items', 'item_id',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###
