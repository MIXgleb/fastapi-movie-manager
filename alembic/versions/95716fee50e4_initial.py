"""initial.

Revision ID: 95716fee50e4
Revises:
Create Date: 2025-09-18 23:08:57.320513

"""

from collections.abc import (
    Sequence,
)

import sqlalchemy as sa

from alembic import (
    op,
)

revision: str = "95716fee50e4"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        table_name="users",
        columns=(
            sa.Column(
                "username",
                sa.String(length=15),
                nullable=False,
            ),
            sa.Column(
                "hashed_password",
                sa.String(length=100),
                nullable=False,
            ),
            sa.Column(
                "role",
                sa.String(length=10),
                nullable=False,
            ),
            sa.Column(
                "id",
                sa.Integer(),
                nullable=False,
            ),
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.PrimaryKeyConstraint(
                "id",
                name=op.f("pk_users"),
            ),
            sa.UniqueConstraint(
                "username",
                name=op.f("uq_users_username"),
            ),
        ),
    )
    op.create_table(
        table_name="movies",
        columns=(
            sa.Column(
                "title",
                sa.String(length=50),
                nullable=False,
            ),
            sa.Column(
                "description",
                sa.String(length=100),
                nullable=False,
            ),
            sa.Column(
                "rate",
                sa.Float(),
                nullable=False,
            ),
            sa.Column(
                "user_id",
                sa.Integer(),
                nullable=False,
            ),
            sa.Column(
                "id",
                sa.Integer(),
                nullable=False,
            ),
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["users.id"],
                name=op.f(
                    "fk_movies_user_id_users",
                ),
            ),
            sa.PrimaryKeyConstraint(
                "id",
                name=op.f("pk_movies"),
            ),
            sa.UniqueConstraint(
                "title",
                name=op.f("uq_movies_title"),
            ),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(
        table_name="movies",
    )
    op.drop_table(
        table_name="users",
    )
