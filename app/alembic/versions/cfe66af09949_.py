"""Convert deals.status and deals.stage to ENUM

Revision ID: cfe66af09949
Revises: 8ebf1fc6fa4d
Create Date: 2025-11-21 12:20:55.785219
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfe66af09949'
down_revision: Union[str, Sequence[str], None] = '8ebf1fc6fa4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: convert VARCHAR columns to ENUM."""
    # 1. Create ENUM types
    op.execute("CREATE TYPE dealstatus AS ENUM ('NEW', 'IN_PROGRESS', 'WON', 'LOST')")
    op.execute("CREATE TYPE dealstage AS ENUM ('QUALIFICATION', 'PROPOSAL', 'NEGOTIATION', 'CLOSED')")

    # 2. Alter columns to ENUM using explicit casting
    op.alter_column(
        'deals',
        'status',
        type_=sa.Enum('NEW', 'IN_PROGRESS', 'WON', 'LOST', name='dealstatus'),
        postgresql_using="status::dealstatus",
        existing_nullable=False,
    )

    op.alter_column(
        'deals',
        'stage',
        type_=sa.Enum('QUALIFICATION', 'PROPOSAL', 'NEGOTIATION', 'CLOSED', name='dealstage'),
        postgresql_using="stage::dealstage",
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema: convert ENUM columns back to VARCHAR."""
    op.alter_column(
        'deals',
        'stage',
        type_=sa.VARCHAR(length=100),
        postgresql_using="stage::text",
        existing_nullable=False,
    )

    op.alter_column(
        'deals',
        'status',
        type_=sa.VARCHAR(length=50),
        postgresql_using="status::text",
        existing_nullable=False,
    )

    # Drop ENUM types
    op.execute("DROP TYPE IF EXISTS dealstatus")
    op.execute("DROP TYPE IF EXISTS dealstage")
