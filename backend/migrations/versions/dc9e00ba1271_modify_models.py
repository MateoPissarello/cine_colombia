"""modify models

Revision ID: dc9e00ba1271
Revises: 438b3212618a
Create Date: 2025-05-27 10:54:42.359417

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc9e00ba1271'
down_revision: Union[str, None] = '438b3212618a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ticket_sales',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('showtime_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('buyer_name', sa.String(), nullable=True),
    sa.Column('buyer_email', sa.String(), nullable=True),
    sa.Column('buyer_phone', sa.String(), nullable=True),
    sa.Column('tickets_sold', sa.Integer(), nullable=False),
    sa.Column('purchase_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['showtime_id'], ['movie_showtimes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ticket_sales_id'), 'ticket_sales', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ticket_sales_id'), table_name='ticket_sales')
    op.drop_table('ticket_sales')
    # ### end Alembic commands ###
