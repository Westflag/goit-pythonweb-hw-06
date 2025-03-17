"""Initial migration

Revision ID: 832e8710c806
Revises: 
Create Date: 2025-03-17 13:54:44.746698

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '832e8710c806'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
