"""foreign-key in posts table

Revision ID: 66b8e3129005
Revises: f289a4eef45d
Create Date: 2024-09-29 00:08:13.137650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66b8e3129005'
down_revision: Union[str, None] = 'f289a4eef45d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                    sa.Column('owner_id', sa.Integer(), nullable=False),
                    )
    op.create_foreign_key(constraint_name='usersposts_fkey', source_table='posts',
                        referent_table='users', local_cols=['owner_id'],
                        remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint(table_name='posts', constraint_name='usersposts_fkey')
    op.drop_column('posts', 'owner_id')
