from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from example.config import get_settings
from contextlib import contextmanager

def get_engine(settings=Depends(get_settings)):
    return create_engine(settings.DATABASE_URL)

def get_session_factory(engine=Depends(get_engine)):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db_context(session_factory=Depends(get_session_factory)):
    db = session_factory()
    try:
        yield db
    finally:
        db.close()

# FastAPI dependency
async def get_db(session_factory=Depends(get_session_factory)):
    with get_db_context(session_factory) as db:
        yield db
