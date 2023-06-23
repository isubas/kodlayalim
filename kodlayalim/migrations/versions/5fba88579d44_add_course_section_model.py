"""Add course section model

Revision ID: 5fba88579d44
Revises: 8f533db0ec63
Create Date: 2023-06-23 01:32:08.352220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fba88579d44'
down_revision = '8f533db0ec63'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course_section',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=140), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('course_section', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_course_section_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course_section', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_course_section_timestamp'))

    op.drop_table('course_section')
    # ### end Alembic commands ###
