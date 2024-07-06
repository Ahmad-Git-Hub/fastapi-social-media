import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


try:
    DATABASE_URL = (
        f"postgresql+psycopg://{settings.database_username}:"
        f"{settings.database_password}@{settings.database_hostname}:"
        f"{settings.database_port}/{settings.database_name}"
    )

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info("Database connection initialized successfully.")

except Exception as e:
    logger.error(f"Failed to initialize database connection: {str(e)}")
    raise


engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    """
    Dependency to provide an independent database session per request.

    Yields:
        SQLAlchemy Session: A database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()