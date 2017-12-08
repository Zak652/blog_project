"""empty message

Revision ID: 3f5a3f9e7f9b
Revises: 
Create Date: 2017-12-08 03:57:23.527321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f5a3f9e7f9b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('entries', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'entries', 'users', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'entries', type_='foreignkey')
    op.drop_column('entries', 'author_id')
    # ### end Alembic commands ###