"""updated post-tag db

Revision ID: 4b6285828a0d
Revises: 4e3262c373d0
Create Date: 2013-07-23 21:29:10.780531

"""

# revision identifiers, used by Alembic.
revision = '4b6285828a0d'
down_revision = '4e3262c373d0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint()
    )
    op.drop_table(u'post_tags')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(u'post_tags',
    sa.Column(u'tag_id', sa.INTEGER(), nullable=True),
    sa.Column(u'post_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], [u'post.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], [u'tag.id'], ),
    sa.PrimaryKeyConstraint()
    )
    op.drop_table('tags')
    ### end Alembic commands ###
