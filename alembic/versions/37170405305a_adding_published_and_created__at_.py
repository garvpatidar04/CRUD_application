"""adding published and created _at columns to posts

Revision ID: 37170405305a
Revises: cc080387606e
Create Date: 2024-09-28 12:13:50.605800

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text  
from sqlalchemy.sql.sqltypes import TIMESTAMP
import time


# revision identifiers, used by Alembic.
revision: str = '37170405305a'
down_revision: Union[str, None] = 'cc080387606e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column('posts',sa.Column('created_at', TIMESTAMP(timezone=True) , nullable=False, server_default=text('now()') ))


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
