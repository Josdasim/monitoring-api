import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.app.main import app
from src.app.config.database import Base, get_db

# Database de prueba en memoria (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_engine():
    """
    Crea un motor de BD de prueba en memoria.
    Se crea y destruye para cada test (scope="function").
    """
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Crea una sesión de BD para cada test.
    """
    TestingSessionLocal = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=db_engine
    )
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """
    Cliente de prueba de FastAPI con BD en memoria.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_service_data():
    """Datos de ejemplo para crear un servicio."""
    return {
        "service_name": "Test Service",
        "service_url": "https://example.com",
        "check_interval": 60
    }


@pytest.fixture
def sample_health_check_data():
    """Datos de ejemplo para crear un health check."""
    from uuid import uuid7
    return {
        "service_id": uuid7(),
        "status": "UP",
        "response_time_ms": 150.5,
        "status_code": "200",
        "error_message": None
    }