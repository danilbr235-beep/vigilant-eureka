from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base
from app.models import Order, OrderStatus
from app.services.reports_service import ReportsService


def make_session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(engine)


def test_dashboard_and_reports_summary_counts():
    db = make_session()
    db.add_all(
        [
            Order(
                external_order_id="O-1",
                sell_nominal_id=1,
                status=OrderStatus.fulfilled,
                customer_currency="EUR",
                customer_nominal=20,
                manual_review=False,
            ),
            Order(
                external_order_id="O-2",
                sell_nominal_id=1,
                status=OrderStatus.problem,
                customer_currency="USD",
                customer_nominal=10,
                manual_review=True,
            ),
        ]
    )
    db.commit()

    svc = ReportsService(db)
    summary = svc.dashboard_summary()
    assert summary["total_orders"] == 2
    assert summary["fulfilled_orders"] == 1
    assert summary["problem_orders"] == 1

    profit = svc.report_profit()
    assert profit["gross_nominal_fulfilled"] == 20.0
