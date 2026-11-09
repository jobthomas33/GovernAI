import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app import models  # noqa: F401


@pytest.fixture
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    TestingSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    Base.metadata.create_all(engine)

    def override_get_db():
        with TestingSession() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    test_client.close()
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


def system_payload():
    return {"name": "Claims Triage", "owner": "A. Owner", "department": "Claims",
            "business_purpose": "Prioritize incoming claims", "deployment_status": "pilot"}


def assessment_payload(**overrides):
    values = {"personal_data_usage": True, "automated_decision_making": True,
              "customer_impact": True, "human_oversight": False,
              "transparency_available": False, "monitoring_enabled": False}
    return values | overrides
