"""empty message

Revision ID: 3529efdbfa11
Revises: 17a21b64d28b
Create Date: 2016-06-03 12:13:22.071988

"""

# revision identifiers, used by Alembic.
revision = '3529efdbfa11'
down_revision = '17a21b64d28b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('video',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('cover', sa.String(length=200), nullable=True),
    sa.Column('web_url', sa.String(length=200), nullable=True),
    sa.Column('posted', sa.Boolean(), nullable=True),
    sa.Column('date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('h_ceph_url', sa.String(length=200), nullable=True),
    sa.Column('h_cloud_url', sa.String(length=200), nullable=True),
    sa.Column('h_height', sa.Integer(), nullable=True),
    sa.Column('h_brate', sa.Integer(), nullable=True),
    sa.Column('m_ceph_url', sa.String(length=200), nullable=True),
    sa.Column('m_cloud_url', sa.String(length=200), nullable=True),
    sa.Column('m_height', sa.Integer(), nullable=True),
    sa.Column('m_brate', sa.Integer(), nullable=True),
    sa.Column('l_ceph_url', sa.String(length=200), nullable=True),
    sa.Column('l_cloud_url', sa.String(length=200), nullable=True),
    sa.Column('l_height', sa.Integer(), nullable=True),
    sa.Column('l_brate', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_video_web_url', 'video', ['web_url'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_video_web_url', 'video')
    op.drop_table('video')
    ### end Alembic commands ###
