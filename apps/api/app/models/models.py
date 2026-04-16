import enum
from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    operator = "operator"
    viewer = "viewer"


class CodeStatus(str, enum.Enum):
    new = "new"
    reserved = "reserved"
    sent = "sent"
    redeemed = "redeemed"
    problem = "problem"
    archived = "archived"


class OrderStatus(str, enum.Enum):
    new = "new"
    reserved = "reserved"
    fulfilled = "fulfilled"
    problem = "problem"
    completed = "completed"


class WarningStatus(str, enum.Enum):
    ok = "ok"
    low_margin = "low_margin"
    loss = "loss"
    no_combo = "no_combo"
    stale_rate = "stale_rate"
    low_stock = "low_stock"
    manual_review = "manual_review"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class SupplierCodeType(Base):
    __tablename__ = "supplier_code_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    currency: Mapped[str] = mapped_column(String(8), index=True)
    nominal: Mapped[float] = mapped_column(Numeric(12, 2))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class PurchaseBatch(Base):
    __tablename__ = "purchase_batches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplier_name: Mapped[str] = mapped_column(String(255))
    purchased_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class CodeItem(Base):
    __tablename__ = "code_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplier_code_type_id: Mapped[int] = mapped_column(ForeignKey("supplier_code_types.id"), index=True)
    purchase_batch_id: Mapped[int] = mapped_column(ForeignKey("purchase_batches.id"), index=True)
    encrypted_code: Mapped[str] = mapped_column(Text)
    masked_code: Mapped[str] = mapped_column(String(64), index=True)
    cost_rub: Mapped[float] = mapped_column(Numeric(12, 2))
    status: Mapped[CodeStatus] = mapped_column(Enum(CodeStatus, name="code_status"), index=True)
    reserved_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    current_order_id: Mapped[int | None] = mapped_column(ForeignKey("orders.id"), nullable=True, index=True)


class SellNominal(Base):
    __tablename__ = "sell_nominals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    currency: Mapped[str] = mapped_column(String(8), index=True)
    nominal: Mapped[float] = mapped_column(Numeric(12, 2), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class PricingConfig(Base):
    __tablename__ = "pricing_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    marketplace_fee_percent: Mapped[float] = mapped_column(Numeric(8, 4))
    risk_reserve_percent: Mapped[float] = mapped_column(Numeric(8, 4))
    min_profit_rub: Mapped[float] = mapped_column(Numeric(12, 2))
    target_profit_percent: Mapped[float] = mapped_column(Numeric(8, 4))
    rounding_rule: Mapped[str] = mapped_column(String(32))
    max_codes_per_order: Mapped[int] = mapped_column(Integer)
    underfill_tolerance_percent: Mapped[float] = mapped_column(Numeric(8, 4))
    overfill_tolerance_percent: Mapped[float] = mapped_column(Numeric(8, 4))
    ad_allocation_mode: Mapped[str] = mapped_column(String(32))
    default_ad_cost_per_sale: Mapped[float] = mapped_column(Numeric(12, 2))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class PromotionCostRule(Base):
    __tablename__ = "promotion_cost_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    currency: Mapped[str | None] = mapped_column(String(8), nullable=True)
    nominal_min: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    nominal_max: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    ad_cost_rub: Mapped[float] = mapped_column(Numeric(12, 2))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class FxRate(Base):
    __tablename__ = "fx_rates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    from_currency: Mapped[str] = mapped_column(String(8), index=True)
    to_currency: Mapped[str] = mapped_column(String(8), index=True)
    rate: Mapped[float] = mapped_column(Numeric(18, 8))
    source: Mapped[str] = mapped_column(String(64), default="manual")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, index=True)


class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sell_nominal_id: Mapped[int] = mapped_column(ForeignKey("sell_nominals.id"), index=True)
    recommended_price_rub: Mapped[float] = mapped_column(Numeric(12, 2))
    combo_payload: Mapped[dict] = mapped_column(JSON)
    expected_profit_rub: Mapped[float] = mapped_column(Numeric(12, 2))
    margin_percent: Mapped[float] = mapped_column(Numeric(8, 4))
    status: Mapped[WarningStatus] = mapped_column(Enum(WarningStatus, name="warning_status"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, index=True)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_order_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    sell_nominal_id: Mapped[int] = mapped_column(ForeignKey("sell_nominals.id"), index=True)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus, name="order_status"), index=True)
    customer_currency: Mapped[str] = mapped_column(String(8))
    customer_nominal: Mapped[float] = mapped_column(Numeric(12, 2))
    manual_review: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class OrderFulfillment(Base):
    __tablename__ = "order_fulfillments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)
    operator_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    delivered_payload: Mapped[dict] = mapped_column(JSON)
    fulfilled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(64), index=True)
    entity_type: Mapped[str] = mapped_column(String(64), index=True)
    entity_id: Mapped[str] = mapped_column(String(64), index=True)
    payload: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, index=True)


Index("ix_fx_rates_pair_fetched", FxRate.from_currency, FxRate.to_currency, FxRate.fetched_at.desc())
Index("ix_price_snapshots_nominal_created", PriceSnapshot.sell_nominal_id, PriceSnapshot.created_at.desc())
Index("ix_audit_logs_entity_created", AuditLog.entity_type, AuditLog.entity_id, AuditLog.created_at.desc())
