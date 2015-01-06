"""empty message

Revision ID: 4431a41e9dbd
Revises: 18a748a1f526
Create Date: 2015-01-06 10:07:02.360223

"""

# revision identifiers, used by Alembic.
revision = '4431a41e9dbd'
down_revision = '18a748a1f526'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('photo')
    op.drop_table('directory')
    op.drop_table('album')
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('album',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('author', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('timestamp_from', sa.DateTime(), nullable=True),
    sa.Column('timestamp_to', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('directory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(length=255), nullable=False),
    sa.Column('album', sa.Integer(), nullable=False),
    sa.Column('added_at', sa.DateTime(), nullable=False),
    sa.Column('refreshed_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['album'], ['album.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('photo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(length=255), nullable=False),
    sa.Column('album', sa.Integer(), nullable=False),
    sa.Column('directory', sa.Integer(), nullable=False),
    sa.Column('author', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('caption', sa.String(length=255), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('width', sa.Integer(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('added_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['album'], ['album.id'], ),
    sa.ForeignKeyConstraint(['author'], ['user.id'], ),
    sa.ForeignKeyConstraint(['directory'], ['directory.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_photo_path'), 'photo', ['path'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_photo_path'), table_name='photo')
    op.drop_table('photo')
    op.drop_table('directory')
    op.drop_table('album')
    ### end Alembic commands ###