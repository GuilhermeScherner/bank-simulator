"""Table transfer, users

Revision ID: 1c643bc5d6b8
Revises: 382ea58de0a8
Create Date: 2020-12-31 12:18:58.785494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c643bc5d6b8'
down_revision = '382ea58de0a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('cpf', sa.String(), nullable=True),
    sa.Column('balance', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('transfer', sa.Column('cpf_receiver', sa.String(), nullable=True))
    op.add_column('transfer', sa.Column('cpf_sender', sa.String(), nullable=True))
    op.add_column('transfer', sa.Column('description', sa.String(), nullable=True))
    op.drop_column('transfer', 'name')
    op.drop_column('transfer', 'cpf')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transfer', sa.Column('cpf', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('transfer', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('transfer', 'description')
    op.drop_column('transfer', 'cpf_sender')
    op.drop_column('transfer', 'cpf_receiver')
    op.drop_table('users')
    # ### end Alembic commands ###