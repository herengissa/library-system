"""
Database connection utilities for the Library Management System.

This module centralizes the PostgreSQL connection handling so that the rest
of the application can focus on business logic. Connection parameters are
read from environment variables with sensible defaults for local development.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any, Dict, Generator

import psycopg2
from psycopg2 import OperationalError


def _get_connection_kwargs() -> Dict[str, Any]:
    """Return connection keyword arguments sourced from environment variables."""
    return {
        "dbname": os.getenv("POSTGRES_DB", "library_db"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": int(os.getenv("POSTGRES_PORT", "5432")),
    }


@contextmanager
def get_connection() -> Generator[psycopg2.extensions.connection, None, None]:
    """
    Yield a psycopg2 connection with automatic commit/rollback handling.

    Raises:
        OperationalError: If the database connection cannot be established.
    """
    conn = None
    try:
        conn = psycopg2.connect(**_get_connection_kwargs())
        yield conn
        conn.commit()
    except OperationalError as exc:
        raise OperationalError(f"Failed to connect to PostgreSQL: {exc}") from exc
    except Exception:
        if conn is not None:
            conn.rollback()
        raise
    finally:
        if conn is not None:
            conn.close()

