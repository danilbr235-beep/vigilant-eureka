from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import AuditLog, Order, OrderStatus


class ReportsService:
    def __init__(self, db: Session):
        self.db = db

    def dashboard_summary(self) -> dict:
        total_orders = self.db.scalar(select(func.count()).select_from(Order)) or 0
        problem_orders = self.db.scalar(select(func.count()).select_from(Order).where(Order.status == OrderStatus.problem)) or 0
        fulfilled_orders = self.db.scalar(select(func.count()).select_from(Order).where(Order.status == OrderStatus.fulfilled)) or 0

        return {
            "total_orders": int(total_orders),
            "fulfilled_orders": int(fulfilled_orders),
            "problem_orders": int(problem_orders),
        }

    def dashboard_charts(self) -> dict:
        rows = self.db.execute(
            select(Order.status, func.count(Order.id)).group_by(Order.status)
        ).all()
        return {"orders_by_status": [{"status": str(status.value if hasattr(status, 'value') else status), "count": count} for status, count in rows]}

    def report_profit(self) -> dict:
        # MVP proxy metric: sum of customer_nominal for fulfilled orders
        gross = self.db.scalar(
            select(func.coalesce(func.sum(Order.customer_nominal), 0)).where(Order.status == OrderStatus.fulfilled)
        )
        return {"gross_nominal_fulfilled": float(gross or 0)}

    def report_orders(self) -> dict:
        rows = self.db.execute(select(Order.status, func.count(Order.id)).group_by(Order.status)).all()
        return {"orders": [{"status": str(s.value if hasattr(s, 'value') else s), "count": int(c)} for s, c in rows]}

    def report_problems(self) -> dict:
        rows = self.db.scalars(select(Order).where(Order.status == OrderStatus.problem).order_by(Order.id.desc()).limit(100)).all()
        return {
            "items": [
                {
                    "id": r.id,
                    "external_order_id": r.external_order_id,
                    "customer_currency": r.customer_currency,
                    "customer_nominal": float(r.customer_nominal),
                }
                for r in rows
            ]
        }

    def report_audit(self) -> dict:
        rows = self.db.scalars(select(AuditLog).order_by(AuditLog.id.desc()).limit(200)).all()
        return {
            "items": [
                {
                    "id": r.id,
                    "action": r.action,
                    "entity_type": r.entity_type,
                    "entity_id": r.entity_id,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                }
                for r in rows
            ]
        }
