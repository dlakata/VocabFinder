"""empty message

Revision ID: 4817d9bebb50
Revises: 55fb36b38510
Create Date: 2015-07-06 14:31:06.557043

"""

# revision identifiers, used by Alembic.
revision = '4817d9bebb50'
down_revision = '55fb36b38510'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('definition')
    op.add_column('vocab_set', sa.Column('difficulty', sa.String(length=30), nullable=True))
    op.add_column('vocab_set', sa.Column('num_words', sa.Integer(), nullable=True))
    op.add_column('vocab_set', sa.Column('public', sa.Boolean(), nullable=True))
    op.add_column('vocab_set', sa.Column('text', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vocab_set', 'text')
    op.drop_column('vocab_set', 'public')
    op.drop_column('vocab_set', 'num_words')
    op.drop_column('vocab_set', 'difficulty')
    op.create_table('definition',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('word', sa.VARCHAR(length=40), autoincrement=False, nullable=True),
    sa.Column('definition', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('set_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['set_id'], [u'vocab_set.id'], name=u'definition_set_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'definition_pkey')
    )
    ### end Alembic commands ###
