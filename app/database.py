from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import variables

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{variables.user}:{variables.passowrd}@{variables.host}/{variables.dbname}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency provide independent session per request 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()