"""add user role

Revision ID: 3c8d4e2b9a10
Revises: 2b7c9f1a8d3e
Create Date: 2026-06-17
"""

from alembic import op
import sqlalchemy as sa


revision = "3c8d4e2b9a10"
down_revision = "2b7c9f1a8d3e"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.String(length=20),
            nullable=False,
            server_default="user",
        ),
    )


def downgrade():
    op.drop_column("users", "role")