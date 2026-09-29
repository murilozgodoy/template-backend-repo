from sqlalchemy import URL, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.settings import DatabaseSettings

_db = DatabaseSettings()

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=_db.db_user,
    password=_db.db_password.get_secret_value(),
    host=_db.db_host,
    port=_db.db_port,
    database=_db.db_name,
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
