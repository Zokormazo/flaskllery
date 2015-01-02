"""add photo table

Revision ID: 18a748a1f526
Revises: 439050c07ddd
Create Date: 2015-01-02 12:38:46.435876

"""

# revision identifiers, used by Alembic.
revision = '18a748a1f526'
down_revision = '439050c07ddd'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'photo',
        sa.Column('id', sa.Integer, primary_key = True),
        sa.Column('path', sa.String(255), nullable = False, index = True),
	sa.Column('album', sa.Integer, sa.ForeignKey('album.id'), nullable = False),
        sa.Column('title', sa.String(64)),
        sa.Column('caption', sa.String(255)),
        sa.Column('added_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('photo')
