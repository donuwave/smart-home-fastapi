"""add new table Face

Revision ID: 7a846ba210c0
Revises: 2459d3356b2d
Create Date: 2025-05-20 17:29:55.813607

"""
from alembic import op
import sqlalchemy as sa
# импортируем Vector
from pgvector.sqlalchemy import Vector

revision = "7a846ba210c0"
down_revision = "2459d3356b2d"
branch_labels = None
depends_on = None


def upgrade():
    # если вы ещё не включили расширение pgvector на сервере,
    # можно сделать это прямо в миграции:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    op.create_table(
        "faces",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "home_id",
            sa.Integer(),
            sa.ForeignKey("home.id", ondelete="CASCADE"),
            nullable=False
        ),
        sa.Column("name", sa.String(), nullable=False, unique=True, index=True),
        sa.Column(
            "embedding",
            Vector(128),            # здесь используем Vector
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=False),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=False),
            server_default=sa.text("now()"),
            server_onupdate=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_table("faces")
    # (опционально) удалить расширение, если больше не нужно:
    op.execute("DROP EXTENSION IF EXISTS vector;")
