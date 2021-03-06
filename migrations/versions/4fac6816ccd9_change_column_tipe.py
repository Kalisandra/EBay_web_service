"""change column tipe

Revision ID: 4fac6816ccd9
Revises: 74ff8d88e737
Create Date: 2020-04-23 10:25:28.339796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fac6816ccd9'
down_revision = '74ff8d88e737'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('statistic_items', 'final_price',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('statistic_items', 'final_price',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)
    # ### end Alembic commands ###
