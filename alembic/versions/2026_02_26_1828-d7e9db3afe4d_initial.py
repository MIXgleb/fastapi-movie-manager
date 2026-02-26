"""
initial.

Create users and movies tables.

Revision ID: d7e9db3afe4d
Revises:
Create Date: 2026-02-26 18:28:04.279636

"""

from collections.abc import (
    Sequence,
)

import sqlalchemy as sa

from alembic import (
    op,
)

revision: str = "d7e9db3afe4d"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    _ = op.create_table(
        "users",
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
            sa.Enum(
                "GUEST",
                "USER",
                "ADMIN",
                name="userrole",
            ),
            server_default="GUEST",
            nullable=False,
        ),
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_users"),
        ),
    )
    _ = op.create_table(
        "movies",
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
            sa.Numeric(
                precision=2,
                scale=1,
            ),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.Uuid(),
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
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            sqltext="rate >= 0 AND rate <= 5.0",
            name=op.f("ck_movies_check_rate_range"),
        ),
        sa.ForeignKeyConstraint(
            columns=["user_id"],
            refcolumns=["users.id"],
            name=op.f("fk_movies_user_id_users"),
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_movies"),
        ),
    )

    op.create_index(
        index_name=op.f("ix_users_username"),
        table_name="users",
        columns=["username"],
        unique=True,
    )
    op.create_index(
        index_name=op.f("ix_movies_title"),
        table_name="movies",
        columns=["title"],
        unique=True,
    )
    op.create_index(
        index_name=op.f("ix_movies_user_id"),
        table_name="movies",
        columns=["user_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        index_name=op.f("ix_movies_user_id"),
        table_name="movies",
    )
    op.drop_index(
        index_name=op.f("ix_movies_title"),
        table_name="movies",
    )
    op.drop_index(
        index_name=op.f("ix_users_username"),
        table_name="users",
    )

    op.drop_table(
        table_name="movies",
    )
    op.drop_table(
        table_name="users",
    )
