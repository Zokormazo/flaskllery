"""create user table

Revision ID: 1682a79c0592
Revises:
Create Date: 2014-12-30 12:10:56.102308

"""

# revision identifiers, used by Alembic.
revision = '1682a79c0592'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),

        # User authentication information
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('password', sa.String(255), nullable=False, server_default=''),
        sa.Column('reset_password_token', sa.String(100), nullable=False, server_default=''),

        # User email information
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('confirmed_at', sa.DateTime),

        # User activity information
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='0'),
    )


def downgrade():
    op.drop_table('user')
