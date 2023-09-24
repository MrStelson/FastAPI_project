"""Init db tables

Revision ID: 10d7f8386798
Revises: 
Create Date: 2023-09-24 21:03:55.679140

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10d7f8386798'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ad_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type_name')
    )
    op.create_table('app_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ad_category',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('category_name', sa.String(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['type_id'], ['ad_type.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('category_name')
    )
    op.create_table('app_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('registered_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('is_banned', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['app_role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ad',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['ad_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ad_comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('ad_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ad_id'], ['ad.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ad_complaint',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('ad_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ad_id'], ['ad.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ad_complaint')
    op.drop_table('ad_comment')
    op.drop_table('ad')
    op.drop_table('app_user')
    op.drop_table('ad_category')
    op.drop_table('app_role')
    op.drop_table('ad_type')
    # ### end Alembic commands ###
