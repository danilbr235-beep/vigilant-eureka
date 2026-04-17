"""stage3 add current_order_id for reserved codes

Revision ID: 20260416_02
Revises: 20260416_01
Create Date: 2026-04-16
"""

from alembic import op
import sqlalchemy as sa


revision = "20260416_02"
down_revision = "20260416_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("code_items", sa.Column("current_order_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_code_items_current_order_id_orders",
        "code_items",
        "orders",
        ["current_order_id"],
        ["id"],
    )
    op.create_index("ix_code_items_current_order_id", "code_items", ["current_order_id"])


def downgrade() -> None:
    op.drop_index("ix_code_items_current_order_id", table_name="code_items")
    op.drop_constraint("fk_code_items_current_order_id_orders", "code_items", type_="foreignkey")
    op.drop_column("code_items", "current_order_id")
