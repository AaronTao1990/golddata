"""empty message

Revision ID: 3553585058c6
Revises: 3529efdbfa11
Create Date: 2016-06-03 15:57:24.332451

"""

# revision identifiers, used by Alembic.
revision = '3553585058c6'
down_revision = '3529efdbfa11'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('video', sa.Column('stream_url', sa.String(length=200), nullable=True))
    op.add_column('video', sa.Column('vct', sa.String(length=200), nullable=True))
    op.add_column('video', sa.Column('vsct', sa.String(length=200), nullable=True))
    op.create_index('ix_video_stream_url', 'video', ['stream_url'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_video_stream_url', 'video')
    op.drop_column('video', 'vsct')
    op.drop_column('video', 'vct')
    op.drop_column('video', 'stream_url')
    ### end Alembic commands ###
