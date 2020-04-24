"""base sintacsys changed

Revision ID: 74ff8d88e737
Revises: 8014af5c8fce
Create Date: 2020-04-22 11:06:55.766357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74ff8d88e737'
down_revision = '8014af5c8fce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorite_searches', sa.Column('statistic_start_date', sa.DateTime(), nullable=True))
    op.drop_column('favorite_searches', 'sttistic_start_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorite_searches', sa.Column('sttistic_start_date', sa.DateTime(), nullable=True))
    op.drop_column('favorite_searches', 'statistic_start_date')
    # ### end Alembic commands ###
