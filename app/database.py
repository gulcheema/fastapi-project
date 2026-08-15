from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_hostname}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)


# Enable SSL only when connecting to Neon
connect_args = {}

if "neon.tech" in settings.database_hostname:
    connect_args = {"sslmode": "require"}


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args
)


sessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()