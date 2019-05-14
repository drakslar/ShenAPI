"""empty message

Revision ID: e5dc2df7f407
Revises: 1065245f3828
Create Date: 2019-05-14 10:22:26.237628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5dc2df7f407'
down_revision = '1065245f3828'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('authenticated', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'authenticated')
    # ### end Alembic commands ###
