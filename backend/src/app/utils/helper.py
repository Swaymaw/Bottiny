import os
from functools import lru_cache

from sqlalchemy.pool import NullPool

from src.app.db.database import Database


@lru_cache(maxsize=1)
def get_db_engine():
    db = Database(os.environ["DATABASE_URL"], poolclass=NullPool)
    return db
