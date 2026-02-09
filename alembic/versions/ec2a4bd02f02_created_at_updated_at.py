"""created_at; updated_at.

Revision ID: ec2a4bd02f02
Revises: 95716fee50e4
Create Date: 2025-10-01 01:12:29.593545

"""

from collections.abc import (
    Sequence,
)

import sqlalchemy as sa

from alembic import (
    op,
)

revision: str = "ec2a4bd02f02"
down_revision: str | Sequence[str] | None = "95716fee50e4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        table_name="movies",
        column=sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        table_name="users",
        column=sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        table_name="users",
        column_name="updated_at",
    )
    op.drop_column(
        table_name="movies",
        column_name="updated_at",
    )
