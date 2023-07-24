from databases import Database
from sqlalchemy import create_engine, MetaData

from .settings import settings


# database = Database("sqlite:///./database/db.sqlite")
database = Database(settings.postgresql_url)

metadata = MetaData()

# engine = create_engine(
#     "sqlite:///./database/db.sqlite", connect_args={"check_same_thread": False})
engine = create_engine(settings.postgresql_url)
