import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models  # noqa: F401  (registra todas as tabelas no metadata)
from app import app
from database.database import Base, get_db


@pytest.fixture(scope="session")
def engine():
    """Banco PostgreSQL de teste.

    Padrao: Testcontainers sobe um PostgreSQL descartavel (exige Docker).
    Alternativa: se TEST_DATABASE_URL estiver definida, usa esse banco.
    """
    test_database_url = os.getenv("TEST_DATABASE_URL")

    if test_database_url:
        engine = create_engine(test_database_url)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        yield engine
        engine.dispose()
        return

    from testcontainers.postgres import PostgresContainer

    with PostgresContainer("postgres:16-alpine", driver="psycopg") as postgres:
        engine = create_engine(postgres.get_connection_url())
        Base.metadata.create_all(engine)
        yield engine
        engine.dispose()


@pytest.fixture
def db_session(engine):
    session = sessionmaker(bind=engine, autocommit=False, autoflush=False)()
    yield session
    session.close()

    # Cada teste comeca com o banco vazio.
    with engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
