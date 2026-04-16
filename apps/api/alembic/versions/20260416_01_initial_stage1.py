"""initial stage1 schema

Revision ID: 20260416_01
Revises: 
Create Date: 2026-04-16
"""

from alembic import op
import sqlalchemy as sa


revision = "20260416_01"
down_revision = None
branch_labels = None
depends_on = None


user_role = sa.Enum("admin", "operator", "viewer", name="user_role")
code_status = sa.Enum("new", "reserved", "sent", "redeemed", "problem", "archived", name="code_status")
order_status = sa.Enum("new", "reserved", "fulfilled", "problem", "completed", name="order_status")
warning_status = sa.Enum(
    "ok", "low_margin", "loss", "no_combo", "stale_rate", "low_stock", "manual_review", name="warning_status"
)


def upgrade() -> None:
    user_role.create(op.get_bind(), checkfirst=True)
    code_status.create(op.get_bind(), checkfirst=True)
    order_status.create(op.get_bind(), checkfirst=True)
    warning_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_role", "users", ["role"])

    op.create_table(
        "supplier_code_types",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("nominal", sa.Numeric(12, 2), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_supplier_code_types_currency", "supplier_code_types", ["currency"])

    op.create_table(
        "purchase_batches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("supplier_name", sa.String(length=255), nullable=False),
        sa.Column("purchased_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
    )

    op.create_table(
        "code_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("supplier_code_type_id", sa.Integer(), sa.ForeignKey("supplier_code_types.id"), nullable=False),
        sa.Column("purchase_batch_id", sa.Integer(), sa.ForeignKey("purchase_batches.id"), nullable=False),
        sa.Column("encrypted_code", sa.Text(), nullable=False),
        sa.Column("masked_code", sa.String(length=64), nullable=False),
        sa.Column("cost_rub", sa.Numeric(12, 2), nullable=False),
        sa.Column("status", code_status, nullable=False),
        sa.Column("reserved_until", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_code_items_status", "code_items", ["status"])

    op.create_table(
        "sell_nominals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("nominal", sa.Numeric(12, 2), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    op.create_table(
        "pricing_configs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("marketplace_fee_percent", sa.Numeric(8, 4), nullable=False),
        sa.Column("risk_reserve_percent", sa.Numeric(8, 4), nullable=False),
        sa.Column("min_profit_rub", sa.Numeric(12, 2), nullable=False),
        sa.Column("target_profit_percent", sa.Numeric(8, 4), nullable=False),
        sa.Column("rounding_rule", sa.String(length=32), nullable=False),
        sa.Column("max_codes_per_order", sa.Integer(), nullable=False),
        sa.Column("underfill_tolerance_percent", sa.Numeric(8, 4), nullable=False),
        sa.Column("overfill_tolerance_percent", sa.Numeric(8, 4), nullable=False),
        sa.Column("ad_allocation_mode", sa.String(length=32), nullable=False),
        sa.Column("default_ad_cost_per_sale", sa.Numeric(12, 2), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    op.create_table(
        "promotion_cost_rules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=128), nullable=False, unique=True),
        sa.Column("currency", sa.String(length=8), nullable=True),
        sa.Column("nominal_min", sa.Numeric(12, 2), nullable=True),
        sa.Column("nominal_max", sa.Numeric(12, 2), nullable=True),
        sa.Column("ad_cost_rub", sa.Numeric(12, 2), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    op.create_table(
        "fx_rates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("from_currency", sa.String(length=8), nullable=False),
        sa.Column("to_currency", sa.String(length=8), nullable=False),
        sa.Column("rate", sa.Numeric(18, 8), nullable=False),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_fx_rates_pair_fetched", "fx_rates", ["from_currency", "to_currency", "fetched_at"])

    op.create_table(
        "price_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sell_nominal_id", sa.Integer(), sa.ForeignKey("sell_nominals.id"), nullable=False),
        sa.Column("recommended_price_rub", sa.Numeric(12, 2), nullable=False),
        sa.Column("combo_payload", sa.JSON(), nullable=False),
        sa.Column("expected_profit_rub", sa.Numeric(12, 2), nullable=False),
        sa.Column("margin_percent", sa.Numeric(8, 4), nullable=False),
        sa.Column("status", warning_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_price_snapshots_nominal_created", "price_snapshots", ["sell_nominal_id", "created_at"])

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("external_order_id", sa.String(length=128), nullable=False, unique=True),
        sa.Column("sell_nominal_id", sa.Integer(), sa.ForeignKey("sell_nominals.id"), nullable=False),
        sa.Column("status", order_status, nullable=False),
        sa.Column("customer_currency", sa.String(length=8), nullable=False),
        sa.Column("customer_nominal", sa.Numeric(12, 2), nullable=False),
        sa.Column("manual_review", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_orders_status", "orders", ["status"])

    op.create_table(
        "order_fulfillments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("operator_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("delivered_payload", sa.JSON(), nullable=False),
        sa.Column("fulfilled_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("actor_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.String(length=64), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_audit_logs_entity_created", "audit_logs", ["entity_type", "entity_id", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_audit_logs_entity_created", table_name="audit_logs")
    op.drop_table("audit_logs")
    op.drop_table("order_fulfillments")
    op.drop_index("ix_orders_status", table_name="orders")
    op.drop_table("orders")
    op.drop_index("ix_price_snapshots_nominal_created", table_name="price_snapshots")
    op.drop_table("price_snapshots")
    op.drop_index("ix_fx_rates_pair_fetched", table_name="fx_rates")
    op.drop_table("fx_rates")
    op.drop_table("promotion_cost_rules")
    op.drop_table("pricing_configs")
    op.drop_table("sell_nominals")
    op.drop_index("ix_code_items_status", table_name="code_items")
    op.drop_table("code_items")
    op.drop_table("purchase_batches")
    op.drop_index("ix_supplier_code_types_currency", table_name="supplier_code_types")
    op.drop_table("supplier_code_types")
    op.drop_index("ix_users_role", table_name="users")
    op.drop_table("users")

    warning_status.drop(op.get_bind(), checkfirst=True)
    order_status.drop(op.get_bind(), checkfirst=True)
    code_status.drop(op.get_bind(), checkfirst=True)
    user_role.drop(op.get_bind(), checkfirst=True)
