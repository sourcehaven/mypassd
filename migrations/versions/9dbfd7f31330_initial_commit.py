"""Initial commit;

Revision ID: 9dbfd7f31330
Revises: 
Create Date: 2023-08-14 00:28:22.274435

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '9dbfd7f31330'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sqlalchemy_utils.types.password.PasswordType(max_length=255), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=False),
    sa.Column('forename', sa.Unicode(length=255), nullable=True),
    sa.Column('surename', sa.Unicode(length=255), nullable=True),
    sa.Column('email', sqlalchemy_utils.types.email.EmailType(length=255), nullable=True),
    sa.Column('salt', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
