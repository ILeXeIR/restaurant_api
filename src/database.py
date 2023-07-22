from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .settings import settings


engine = create_engine(
    "sqlite:///./database/db.sqlite", connect_args={"check_same_thread": False})
# engine = create_engine(settings.postgresql_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
