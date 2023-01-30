"""empty message

Revision ID: af112517dd35
Revises: c0bfcd9ea018
Create Date: 2023-01-30 10:52:57.270006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af112517dd35'
down_revision = 'c0bfcd9ea018'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('eeo1_data',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('count_employees', sa.Integer(), nullable=False),
    sa.Column('job_category', sa.String(), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('race', sa.String(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('company', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('eeo1_data_line')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('eeo1_data_line',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('count_employees', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('job_category', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('gender', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('race', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('year', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('company', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='eeo1_data_line_pkey')
    )
    op.drop_table('eeo1_data')
    # ### end Alembic commands ###