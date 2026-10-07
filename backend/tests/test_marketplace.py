import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.services.marketplace import seed_marketplace, list_agents, get_agent_by_id

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    seed_marketplace(db)
    yield db
    db.close()

def test_seed_agents(db_session):
    agents = list_agents(db_session)
    assert len(agents) >= 10

def test_get_agent_details(db_session):
    agent = get_agent_by_id(db_session, "ProductSearchAgent-A")
    assert agent is not None
    assert agent.name == "E-Commerce Fast Search Agent"
    assert "product_search" in agent.capabilities
