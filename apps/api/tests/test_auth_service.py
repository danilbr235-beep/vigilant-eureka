from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.base import Base
from app.models import User, UserRole
from app.services.auth_service import AuthService


def make_session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(engine)


def test_login_and_refresh_flow_returns_new_tokens():
    db = make_session()
    user = User(email="admin@test.local", password_hash=hash_password("secret"), role=UserRole.admin, is_active=True)
    db.add(user)
    db.commit()

    access1, refresh1, _ = AuthService(db).login("admin@test.local", "secret")
    access2, refresh2, _ = AuthService(db).refresh(refresh1)

    assert access1 != access2
    assert refresh1 != refresh2
