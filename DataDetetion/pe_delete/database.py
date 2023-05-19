from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

MASTER_DB_FILE = "data/master.sqlite"
WORKING_DB_FILE = "data/db.sqlite"
SQLALCHEMY_DATABASE_ROOT = "sqlite:///./"
SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_ROOT + WORKING_DB_FILE

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo="debug"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
