"""Add question and answer model

Revision ID: e8e2b91cf519
Revises: 54e3c0584888
Create Date: 2023-06-23 17:44:38.463757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8e2b91cf519'
down_revision = '54e3c0584888'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('answers', sa.Text(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('answer_number', sa.Integer(), nullable=True),
    sa.Column('correct_answer_number', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_answer_timestamp'), ['timestamp'], unique=False)

    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('option_a', sa.String(), nullable=True),
    sa.Column('option_b', sa.String(), nullable=True),
    sa.Column('option_c', sa.String(), nullable=True),
    sa.Column('option_d', sa.String(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('correct_option', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_question_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_question_timestamp'))

    op.drop_table('question')
    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_answer_timestamp'))

    op.drop_table('answer')
    # ### end Alembic commands ###
