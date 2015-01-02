"""create album table

Revision ID: 23b84f44d8d3
Revises: 7038cec1ed8
Create Date: 2014-12-31 12:27:25.943473

"""

# revision identifiers, used by Alembic.
revision = '23b84f44d8d3'
down_revision = '7038cec1ed8'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'album',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(64)),
        sa.Column('description', sa.String(255)),
        sa.Column('author', sa.Integer, sa.ForeignKey('user.id'), nullable = False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('timestamp_from', sa.DateTime),
        sa.Column('timestamp_to', sa.DateTime)
    )


def downgrade():
    op.drop_table('album')
