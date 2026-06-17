"""add auth0 identity fields to users

Revision ID: 2b7c9f1a8d3e
Revises: 1fe4caf55858
Create Date: 2026-06-17
"""

from alembic import op
import sqlalchemy as sa


revision = "2b7c9f1a8d3e"
down_revision = "1fe4caf55858"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column(
            "auth_provider",
            sa.String(length=20),
            nullable=False,
            server_default="local",
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "external_id",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.create_unique_constraint(
        "uq_users_external_id",
        "users",
        ["external_id"],
    )


def downgrade():
    op.drop_constraint(
        "uq_users_external_id",
        "users",
        type_="unique",
    )

    op.drop_column("users", "external_id")
    op.drop_column("users", "auth_provider")