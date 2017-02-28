"""add password functions

Revision ID: 281540465c33
Revises: 38f6bc52e21c
Create Date: 2017-02-19 18:23:32.807426

"""

# revision identifiers, used by Alembic.
revision = '281540465c33'
down_revision = '38f6bc52e21c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('email', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_column('users', 'email')
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
