"""Databasanslutning med SQLAlchemy."""

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass


def _get_database_url() -> str:
    """Hämtar databas-URL från miljövariabler."""
    dbname = os.getenv("POSTGRES_DB", "library_db")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"


# Skapa engine
_engine = create_engine(_get_database_url(), echo=False)
_SessionLocal = sessionmaker(bind=_engine, autocommit=False, autoflush=False)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Ger en databassession med automatisk commit/rollback."""
    session = _SessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()


def get_engine():
    """Hämtar SQLAlchemy engine (för migrations etc)."""
    return _engine

