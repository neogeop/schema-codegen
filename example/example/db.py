from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from example.config import get_settings

def get_engine(settings=Depends(get_settings)):
    return create_engine(settings.DATABASE_URL)

def get_session_factory(engine=Depends(get_engine)):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

def with_db_session(session_factory=Depends(get_session_factory)):
    with session_factory() as db:
        yield db
