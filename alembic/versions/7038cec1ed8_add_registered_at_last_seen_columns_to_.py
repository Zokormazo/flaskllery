"""Add registered_at & last_seen columns to user

Revision ID: 7038cec1ed8
Revises: 1682a79c0592
Create Date: 2014-12-30 16:46:10.569412

"""

# revision identifiers, used by Alembic.
revision = '7038cec1ed8'
down_revision = '1682a79c0592'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('user', sa.Column('registered_at', sa.DateTime))
    op.add_column('user', sa.Column('last_seen', sa.DateTime))


def downgrade():
    op.drop_column('user', 'registered_at')
    op.drop_column('user', 'last_seen')
