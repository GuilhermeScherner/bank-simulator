"""remove table transfer.py

Revision ID: 6e5f73996493
Revises: 1c643bc5d6b8
Create Date: 2020-12-31 15:24:31.278330

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6e5f73996493'
down_revision = '1c643bc5d6b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transfer.py')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transfer.py',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('value', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('cpf_receiver', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('cpf_sender', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='transfer_pkey')
    )
    # ### end Alembic commands ###
