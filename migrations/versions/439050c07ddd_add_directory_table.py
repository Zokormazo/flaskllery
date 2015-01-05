"""add directory table

Revision ID: 439050c07ddd
Revises: 23b84f44d8d3
Create Date: 2015-01-02 10:46:35.056904

"""

# revision identifiers, used by Alembic.
revision = '439050c07ddd'
down_revision = '23b84f44d8d3'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'directory',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('path', sa.String(255), nullable=False),
        sa.Column('album', sa.Integer, sa.ForeignKey('album.id'), nullable=False),
        sa.Column('added_at', sa.DateTime, nullable=False),
        sa.Column('refreshed_at', sa.DateTime)
    )

def downgrade():
    op.drop_table('directory')
