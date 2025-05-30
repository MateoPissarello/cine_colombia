"""modify models

Revision ID: 438b3212618a
Revises: acd1f9b30459
Create Date: 2025-05-26 20:24:36.372947

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '438b3212618a'
down_revision: Union[str, None] = 'acd1f9b30459'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('showtime_snapshots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cinema_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('data', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['cinema_id'], ['cinemas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_showtime_snapshots_id'), 'showtime_snapshots', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_showtime_snapshots_id'), table_name='showtime_snapshots')
    op.drop_table('showtime_snapshots')
    # ### end Alembic commands ###
